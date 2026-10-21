"""Creatures, vehicles, plants, buildings and props for the Jonah, Daniel, David, Noah and Joseph picture-book videos.

Every public drawing function returns SVG markup — one ``<g filter="url(#wobble-fine)">…</g>``, no ``<svg>``
wrapper — to be placed inside ``art.style.svg_doc(...)``. Shapes use the ``art.style.P`` palette, umber ink
outlines (``art.style.INK``) of 3-5 px at scale 1 with round joins; never pure black or pure white.
This module does not import art/characters.py (the throne / ash-heap geometry that matches the king is
hard-coded), so it is safe to import from anywhere.

Conventions (read these first)
------------------------------
* Signature style ``fn(x, y, scale=1.0, facing=1, **options)``. ``(x, y)`` is the ANCHOR in stage px (listed
  for each function). ``facing=1`` faces / moves right, ``facing=-1`` mirrors around the anchor's x.
* ``scale`` multiplies everything, including ink width (a 0.5-scale drawing has ~2 px lines, as distant
  things should). Scale 1 is "person scale": an adult (Jonah, art/characters.py) is ~330 px tall.
* BBox = rendered alpha extent MEASURED at scale 1, facing=1, as (left, top, right, bottom) px relative to
  the anchor, wobble included. For facing=-1 use (-right, top, -left, bottom); multiply everything by scale.
* Local -> stage: ``local_to_stage(x, y, scale, facing, lx, ly)`` converts a documented local point (the
  ship bed, the fish mouth, ...) to stage px for a drawing placed at (x, y, scale, facing).
* clipPath / mask / gradient ids are derived from the parameters, so many copies may share one document.
* Animate by rendering a flipbook of frames with different option values (all "0..1" / "-1..1" options are
  continuous and look good at intermediate values), or by moving the layer with engine.motion.
* RENDERING COST: every unique markup is rasterised once (measured on a 2112 x 1188 layer: fish ~1.2 s,
  castor frame ~0.9 s, gull ~0.6 s, full-width skyline ~1.5 s) and then cached, so never feed a per-frame
  float into an option. Use a small
  fixed flipbook of quantised values and pick the nearest frame: fish mouth in steps of 1/8, tail ~6 phases
  (e.g. sin at 0, 60, 120 ... deg), eye per beat; castor growth / wither in steps of 0.1 (or 0, .25, .5, .75,
  1); bird wing 4-6 phases; sway 2-4 phases. Keep nineveh_skyline / city_wall / ziggurat on static layers.
* Compositions whose coordinates are absolute (city_wall, nineveh_skyline, harbor_dock) take x0 / x1 / y in
  stage px and have no facing.

1. THE GREAT FISH
-----------------
fish(x, y, scale=1.0, facing=1, mouth=0.0, eye='open', tail=0.0, blush=True, part='all')
    Anchor: centre of the round body (about the level of the top of the pectoral fin).
    A huge friendly blue fish, ~1400 px long at scale 1 (tail tip -791 .. snout +605): blue body
    P['fish'], darker back P['fish_dark'], light belly / lower jaw P['fish_belly'], light spots
    P['fish_spot'], scale arcs, a gill line ending at the belly colour, dorsal / anal / pectoral fins, a
    vertical forked tail fin, one big kind eye with highlights, rosy cheek, a smile that curls up at the corner.
    BBox: mouth 0 (-791, -462, 605, 359); .33 right 593; .66 right 589; mouth 1 (-791, -462, 588, 371);
          tail=+1 left -879; tail=-1 left -879, bottom 419.
    Options:
      mouth 0..1  the jaw opens: lower jaw swings down, the throat stretches into a soft pouch that stays
                  close to the belly line, the snout lifts, the lip tips curl in so the opening is rounded;
                  dark-red inside P['mouth_inside'] with a pink tongue. Smooth at every value. At 1 the
                  opening is ~415 px tall — a 330 px person fits (see fish_mouth_points()['box']).
      eye         'open' | 'closed' (sleepy curve with lashes) | 'happy' (^ arc) | 'surprised' (big eye,
                  small pupil, raised brow).
      tail -1..1  tail fin bends around the peduncle (+1 = up, -1 = down, 22 deg); the pectoral fin
                  counter-flaps. Cycle it for swimming (quantise: see RENDERING COST).
      blush       rosy cheek on/off.
      part        'all' | 'back' | 'front'. SWALLOW / SPIT RECIPE (same x, y, scale, facing, mouth, eye, tail
                  for all three):  fish(..., part='back')  ->  in_fish_mouth(jonah(...), x, y, scale, facing,
                  mouth)  ->  fish(..., part='front').  'back' = tail, fins, body, mouth cavity, face; 'front' =
                  lower jaw + pouch, upper-lip rim, gill, pectoral fin, so a figure between them is inside the
                  mouth: hidden by the jaws and head, visible through the opening and in the water in front.
fish_mouth_points(mouth=0.0) -> {'corner', 'upper', 'lower', 'center', 'box'}
    Local (scale 1, facing right) key points: corner = back of the mouth (hinge); upper / lower = lip tips;
    center = middle of the dark opening (aim swallowed things here); box = (x0, y0, x1, y1), the largest
    axis-aligned rectangle inside the dark opening (a point when the mouth is closed).
      mouth 0    corner (274, 30)  upper (588, 16)   lower (596, 28)  center (426, 48)  box: point (426, 48)
      mouth .33  corner (256, 42)  upper (583, -32)  lower (579, 103) center (464, 55)  box (366, 13, 562, 97)
      mouth .66  corner (233, 57)  upper (576, -92)  lower (558, 197) center (437, 60)  box (335, -58, 539, 178)
      mouth 1    corner (214, 70)  upper (570, -142) lower (540, 274) center (410, 71)  box (300, -111, 520, 253)
    The eye is at about (380, -118) closed .. (340, -222) wide open. Convert with local_to_stage().
fish_mouth_path(mouth=1.0, x=0.0, y=0.0, scale=1.0, facing=1, reach=1600.0) -> SVG path data (stage px)
    Clip region for a fish drawn at (x, y, scale, facing): the dark mouth opening plus the open water in front
    of the lips (the half-plane beyond the line from the upper to the lower lip tip, `reach` px deep). The
    head, cheeks and jaws are outside it. Use it in your own <clipPath>, or use in_fish_mouth().
in_fish_mouth(markup, x, y, scale=1.0, facing=1, mouth=1.0) -> markup
    Wraps figure markup in a clip of fish_mouth_path(); x, y, scale, facing, mouth are the FISH's. See the
    swallow recipe under fish(part=...). Example (props_fish.png): Jonah at 0.8 x the fish scale, placed at
    local_to_stage(.., center[0], center[1] + 132) with pose='float'.

2. THE SHIP
-----------
ship(x, y, scale=1.0, facing=1, sail='full', cutaway=False, lantern=True, oars=False, part='all', flag=True)
    Anchor: hull centre on the WATERLINE (y=0). Ancient Phoenician-style merchant ship, bow on the facing
    side: curved planked hull (P['wood'] tones) with a teal / terracotta painted band, raised bow post,
    curling stern post, rail with a row of round painted shields, one mast, yard and square striped sail
    P['sail'] / P['sail_stripe'], stays and sheets, a pennant, a big steering oar at the stern.
    BBox (-602, -944, 525, 126) for every sail; oars=True bottom 158. The hull below the waterline (y 0..+98)
    is drawn: cover it with your sea layer. Stays / sheets never get thinner than ~2.6 px on screen.
    Geometry (local, facing right): deck / feet of people standing on board SHIP_DECK_Y = -165 (valid for
    |x| < 300); rail top ~-220; mast x=-10 from -170 to -930; yard y~-850 spanning x -318..298; sail foot
    ~-500..-550 (just above the head of an adult standing on deck); stern curl x -520..-420, y -440..-175;
    bow knob (488, -358); stern lantern hook (-428, -372).
    Options:
      sail     'full' (billowing, striped) | 'furled' (rolled under the yard, tied) | 'torn' (ragged edges, a
               hole, a flapping loose strip, yard tilted - for the storm).
      cutaway  True shows the hull in dollhouse cross-section with a warm lantern-lit hold: two amphorae and a
               sack (stern side), a straw mattress with pillow and folded teal blanket, a crate with a sack on
               it (bow side), ribs and deck beams, and a small lantern hanging from a deck beam.
               SHIP_INTERIOR = (-360, -146, 360, 34): the hold rectangle (x0, top, x1, bottom; bottom corners
               rounded, floor surface y~18). Its lower part is BELOW the waterline: in cutaway shots draw the
               sea in front only below y~+40 (or translucent).
               SHIP_BED = (-130, 240, -4): mattress x0, x1 and its top surface y; the pillow is at x~-100.
               SHIP_SLEEP = (48, -2): put jonah(*local_to_stage(x, y, scale, facing, *SHIP_SLEEP), scale,
               facing, pose='sleep') here - he lies on the mattress with his head on the pillow; ~140 px of
               headroom above him.
               SHIP_HOLD_LANTERN = (200, -140): the hook of the hold lantern (toward the bow, clear of the
               sleeper's head); the lantern hangs down to y~-75. Its warm glow is centred near x~60.
      lantern  a small lit lantern hanging from the stern post (no glow halo in cutaway).
      oars     a row of 7 oars dipping into the water.
      part     'all' | 'back' | 'front'. 'back' = flag, stays, mast, sail, sheets, hull, posts and the cutaway
               hold; 'front' = rail with shields, steering oar, oars, stern lantern. Draw ship(part='back') ->
               characters standing on deck (feet at SHIP_DECK_Y) -> ship(part='front') so the rail hides
               their shins.
      flag     the pennant on the masthead.

3. PROPS
--------
crate(x, y, scale=1.0, rot=0)
    Anchor: centre. Planked wooden box with a diagonal brace, top and side faces. BBox (-54, -59, 69, 49).
jar(x, y, scale=1.0, rot=0, color=None)
    Anchor: centre. Terracotta amphora with two handles, cream band, wavy line; color overrides the clay.
    BBox (-54, -86, 54, 82).
sack(x, y, scale=1.0, rot=0, color=None, seed=0)
    Anchor: bottom centre. Lumpy burlap sack tied with rope, with a patch; seed varies the lumps.
    BBox (-60, -122, 58, 5).
lots_jar(x, y, scale=1.0, sticks=5)
    Anchor: bottom centre. Clay pot the lots are drawn from, with wooden lot sticks poking out (sticks=0 for
    an empty pot). BBox (-51, -150, 51, 4); sticks=0 (-51, -90, 51, 4); pot rim at y~-78.
lot(x, y, scale=1.0, rot=0, marked=False)
    Anchor: centre. A small flat wooden lot stick 76 x 22. marked=True adds a glowing orange-gold mark and a
    soft golden halo (the lot that falls on Jonah). BBox (-41, -14, 41, 14); marked incl. halo (-75, -54, 75, 54).
lantern(x, y, scale=1.0, lit=True)
    Anchor: the top hook ring (hang it from a beam). Oil lantern 58 x 136 (bottom tip y~135); lit adds a warm
    flame and a soft glow halo. BBox unlit (-30, -3, 29, 136); lit incl. halo (-113, -24, 112, 200).
rope_coil(x, y, scale=1.0)
    Anchor: bottom centre. Three-loop coil of rope with a loose end to the right. BBox (-59, -66, 91, 5).
scroll(x, y, scale=1.0, rot=0, opened=False)
    Anchor: centre. Closed: rolled parchment with a red tie, BBox (-77, -23, 76, 46). opened=True: parchment
    between two wooden rollers with lines of writing, BBox (-100, -79, 100, 79).
booth(x, y, scale=1.0, facing=1, shade=False)
    Anchor: bottom centre (ground, between the front posts). Jonah's little shelter (Jonah 4:5) in a slight
    3/4 view: rough stick posts, a front and a back A-frame (the back frame is offset by BOOTH_DEPTH =
    (54, -28)), a ridge pole, and a striped cloth thrown over the ridge - its sloped top is visible, sagging
    between the rafters, hanging past the eaves at the sides with ragged hems and as a short shade cloth at
    the back; the inside under the roof is shaded; leafy branches lie on the cloth. facing=-1 mirrors.
    BBox (-205, -432, 245, 13). Front posts at x=-158 and 146, front eaves y~-238, front apex (0, -374), back
    apex (54, -402). BOOTH_SEAT = (-140, -250, 132, 0): the open space under the roof (x0, top, x1, ground)
    where a seated Jonah fits (draw him after the booth). A standing adult (330 px) fits only near the centre:
    his head rises above the eaves into the gable, under the ridge.
    shade=True adds a soft cool shadow ellipse on the ground under the roof (x ~-170..190; BBox bottom 35),
    so the shade reads even before the castor plant grows.
throne(x, y, scale=1.0, facing=1)
    Anchor: the FLOOR UNDER THE SEATED KING'S ANCHOR - i.e. pass the same x, y, scale, facing as
    characters.king(x, y, scale, facing, pose='sit_throne', throne=False), and draw the throne first.
    (It is not centred on its own anchor: the back is at x -86..-12, the seat runs x -90..60.)
    Assyrian throne in side view: tall back upholstered in royal purple P['royal'] with gold studs, a blue
    glazed rosette band and a gold pine-cone finial sitting on the top rail; a purple cushion; a wooden seat
    box with a gold band and tassel; a far-side armrest with a blue rosette band on gold supports ending in a
    little gold lion head; gold turned legs with lion paws; a small footstool in front (x 70..152, top y~-46)
    whose back edge is under the seated king's feet. BBox (-93, -299, 154, 3). KING_SEAT_Y = -74 is the
    cushion top (under the king's hips); armrest top y~-160; back top y~-262, finial to ~-296.
    The empty throne works for "the king rose from his throne" (draw king(pose='stand' / 'remove_crown')
    beside it). NOTE: characters.king(pose='sit_throne', throne=True) still draws its own older wooden chair;
    use throne=False + props.throne() so the occupied and the empty throne match.
ash_pile(x, y, scale=1.0, smoke=False, facing=1, part='all')
    Anchor: bottom centre of the mound (ground). The heap of ashes the king sits in (Jonah 3:6): a lumpy grey
    mound ~76 px high (pale ash on top, darker below, speckled), dark charcoal lumps, two half-burnt sticks
    (one with a glowing ember tip), a low pale lip of ash spreading in front and scattered specks at the edge.
    BBox (-185, -79, 177, 5); part='back' (the mound + sticks + smoke) (-125, -79, 127, 4); part='front' (the
    low lip, lumps, specks) (-184, -17, 178, 5). smoke=True adds three soft translucent puffs / curls rising
    to y~-261 (drawn with part 'all' / 'back').
    With the king: ash_pile(x + KING_ASH_DX*scale*facing, y, scale, facing=facing, part='back', smoke=...) ->
    characters.king(x, y, scale, facing, pose='sit_ashes', ashes=False) -> ash_pile(same, part='front').
    KING_ASH_DX = 21.8 (scale 1, facing right).

4. PLANTS
---------
castor_plant(x, y, scale=1.0, growth=1.0, wither=0.0, bite=0.0, side=1, seed=0)
    Anchor: root point on the ground (centre of a small soil mound). The castor-oil plant (蓖麻, Ricinus
    communis), drawn as a giant herb: a thick glossy GREEN stem (P['leaf_dark'] toward P['leaf']) with a
    red-purple flush down one side and pale node rings (no bark), reddish petioles, very large peltate
    palm-shaped leaves with 7-9 pointed lobes and pale veins (P['leaf']), a side branch, spiky red seed
    clusters at the top. side=+1 leans / spreads the canopy to the right (+x), side=-1 to the left (mirror).
    Stem height castor_height(growth) = 30 + 470 * growth**2.2 (g 0: 30, .25: 52, .5: 132, .75: 280, 1: 500).
    BBox (side=1): growth 0 (-49, -44, 48, 12) sprout with two seed-leaves; .25 (-53, -80, 52, 12);
          .5 (-99, -196, 93, 13) about waist high; .75 (-151, -369, 219, 13);
          1 (-220, -622, 503, 14) taller than a standing man; wither .5 (-181, -556, 513, 14);
          wither 1 (-91, -531, 459, 19); bite 1 (-200, -622, 530, 14); wither 1 + bite 1 (-85, -519, 468, 17).
    Shade: at growth=1 the leaves form a canopy between y~-620 and -330 spanning x -210..500, densest over
    CASTOR_SHADE = (-180, 400) (ground x-range of the shade for a high sun, relative to the anchor; mirror
    for side=-1). Put the booth at x + CASTOR_BOOTH_DX*scale*side (CASTOR_BOOTH_DX = 270) so the canopy arches
    over its roof (see props_castor.png).
    Options (all continuous; check 0 / .25 / .5 / .75 / 1):
      growth 0..1  sprout -> waist-high bush -> tall plant; leaves are born one by one and unfold, the
                   branch grows from .4 to .85, seed clusters appear after .68, seed-leaves vanish by .37.
      wither 0..1  two phases so the SAME leaves stay recognisable: 0..0.7 every leaf keeps its pointed
                   palmate silhouette but swings down on its drooping petiole until it hangs face-on below
                   it, the lobe tips cup and hook toward the centre, the colour goes P['leaf'] -> P['leaf_dry']
                   (reached at .7) with brown spots; 0.7..1 the leaves shrink and crumple into limp brown
                   (P['leaf_dead']) hanging hands, and the stem bends over.
      bite 0..1    a scalloped notch eaten into the stem 16 px above the ground on the side opposite the
                   canopy (pale pith rim, crumbs); at 1 it reaches ~3/4 through the stem and the plant leans
                   3.5 deg away from it (toward the canopy). It is a small detail: show it in a close-up
                   (scale >= 2 or a camera zoom); in a wide shot the lean and the worm carry it. For the worm:
                   worm(x - WORM_BITE_DX*scale*side, y, scale, facing=side, chomp=...) puts its mouth in the
                   notch (WORM_BITE_DX = 52).
      seed         varies leaf spin.
castor_height(growth) -> stem height in px at scale 1 (see above).
palm_tree(x, y, scale=1.0, lean=0.0, sway=0.0, dates=True)
    Anchor: base of the trunk. Date palm ~600 px tall: ringed tapering trunk, a crown of drooping feathery
    pinnate fronds (central rib with a comb of narrow pointed leaflets; darker back fronds), date clusters.
    lean -1..1 moves the crown +-150 px sideways (crown at (150*lean, -430)); sway -1..1 swings the fronds for
    wind. BBox lean 0 (-229, -602, 230, 6); lean 1 (-79, -602, 380, 6); lean -1 (-379, -602, 79, 6);
    sway 1 (-220, -604, 229, 6).
olive_tree(x, y, scale=1.0, seed=0)
    Anchor: base of the trunk. Gnarled olive: a twisted grey-brown trunk with a knot hole, splitting into three
    limbs, each carrying its own silvery grey-green clump (plus one small low clump) with sky gaps between
    them, slim silver leaves and small dark olives; seed varies leaf / olive placement. BBox (-202, -379, 201, 6).
bush(x, y, scale=1.0, variant=0)
    Anchor: base centre. variant 0 green, 1 green with pink flowers, 2 dry grey-olive desert shrub with bare
    forked twigs, 3 dark green with red berries. BBox 0 / 1 / 3 (-99, -112, 104, 19); 2 (-98, -102, 94, 6).
grass_tuft(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base centre. variant 0 green (-41, -59, 37, 3), 1 dry yellow (-47, -55, 43, 3), 2 green with red /
    yellow wild flowers (-47, -93, 54, 3). sway -1..1 bends the blades (sway 1: right edge ~49).
seaweed(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base on the sea floor. variant 0 olive kelp ribbons (-46, -248, 41, 4); 1 pink bubbly weed
    (-84, -129, 81, 7); 2 teal sea-grass (-72, -185, 76, 3); 3 orange branching coral (-117, -155, 109, 12).
    sway -1..1 bends the tips (variant 0 sway 1: right edge 81); animate with a few phases for currents.
reeds(x, y, scale=1.0, variant=0, sway=0.0)
    Anchor: base centre. Clump of reed blades with three brown cattails; variant changes the blade pattern.
    BBox (-65, -290, 79, 5); sway 1 (-39, -289, 140, 5).

5. CREATURES
------------
worm(x, y, scale=1.0, facing=1, chomp=0.0, crawl=0.0)
    Anchor: bottom centre (on the ground). Small cute pink caterpillar-like worm with green spots, antennae, a
    big dot eye and rosy cheek; head on the facing side. Body ~62 px long. BBox (-35, -44, 45, 3) for every
    option. Mouth at local (40, -11). chomp 0..1 opens a round mouth with tiny teeth; crawl 0..1 arches the
    middle of the body like an inchworm.
gull(x, y, scale=1.0, facing=1, wing=0.0, pose='fly')
    Anchor: body centre. Cream seagull with grey wings, black wing tips with white spots, yellow beak.
    pose 'fly' | 'stand' (wings folded, orange legs, feet at y~+40). In flight both wings show: the near wing
    in front of the body and the far wing peeking out behind it.
      wing  1  wings up in a V (raised wing no longer than ~1.1 x the body)   BBox (-76, -107, 66, 21)
      wing .5  half up                                                       (-76, -93, 66, 21)
      wing  0  GLIDE: wings level, seen nearly edge-on as slim arched blades swept back over the tail, far
               wing a sliver above the back                                  (-89, -40, 66, 21)
      wing -.5 sweeping down                                                 (-80, -28, 66, 41)
      wing -1  down-stroke: near wing below the body, far wing tip under the belly (-76, -28, 66, 69)
      stand                                                                  (-65, -36, 61, 42)
    Cycle wing (1, .5, 0, -.5, -1, -.5, 0, .5) for flapping, hold 0 for drifting / gliding gulls.
dove(x, y, scale=1.0, facing=1, wing=0.0, pose='fly')
    Anchor: body centre. Plump cream-white dove with a rosy breast, round head, short pink beak, short tail and
    soft lavender wings with rounded feather tips; same wing / pose options as gull, smaller.
    BBox wing 1 (-56, -87, 51, 22); .5 (-56, -74, 51, 22); 0 (-71, -34, 51, 22); -.5 (-64, -32, 51, 33);
    -1 (-56, -32, 51, 54); stand (-47, -39, 47, 38).
small_fish(x, y, scale=1.0, facing=1, color='orange', tail=0.0)
    Anchor: centre. Little striped round fish with a big eye. color: a FISH_COLORS name ('orange', 'yellow',
    'pink', 'teal', 'purple', 'blue', 'red') or any hex. tail -1..1 bends the tail. BBox (-58, -28, 40, 25);
    tail +-1 (-62, -31, 40, 25).
animal(x, y, scale=1.0, facing=1, kind='sheep', sackcloth=False)
    Anchor: bottom centre (hooves on the ground). Cute rounded picture-book animals, head on the facing side,
    open dot eyes and rosy cheeks:
      'sheep'  fluffy cream wool, tan face                                     BBox (-95, -147, 121, 3)
      'goat'   round cream body with brown patches, short sturdy legs, short thick curved neck, big head,
               curled horns, floppy ear, beard                                 (-91, -256, 139, 3)
      'cow'    cream with brown patches, pink muzzle                           (-139, -226, 195, 3)
      'donkey' grey, long ears, dark mane                                      (-115, -303, 170, 3)
      'camel'  tan dromedary: rounded barrel body with ONE hump in the middle of the back, legs set in
               under the body with knobbly knees and pad feet, long neck dipping then rising, soft muzzle,
               open eye with lashes                                            (-139, -358, 284, 3)
    sackcloth=True drapes a burlap blanket with a patch and a rope tie over the back (Jonah 3:8); on the camel
    it follows the hump and back with a sag on each flank. The BBox does not change.

6. BUILDINGS
------------
house(x, y, scale=1.0, variant=0, facing=1)
    Anchor: bottom centre of the front wall (ground). Flat-roofed mud-brick house at person scale (doors
    ~330 px tall), front face + a 3/4 side face on the facing side, roof beam ends, small dark windows,
    exposed bricks. facing=-1 mirrors (side face and stairs swap sides).
      0 one storey, pot on the roof                      BBox (-325, -653, 386, 13), roof y~-510
      1 two storeys, outside stair up to a landing and an upper door, teal awning
                                                         (-431, -890, 331, 20), roof y~-845
      2 wide, striped door awning, rooftop shade, pots   (-394, -733, 452, 13), roof y~-524
      3 palm-frond roof shade, laundry line, bush        (-305, -786, 457, 17), roof y~-594
    For background streets use scale 0.2-0.5.
city_wall(x0, x1, y, height=260, gate=None, doors_open=0.0, towers=True, seed=0, ink=1.0)
    Anchor: ground line y, from x0 to x1 (absolute stage px, no scale). Thick Assyrian mud-brick wall with
    stepped crenellations, brick courses, base band and projecting towers every ~420*k px (k = height/260;
    every detail scales with k). Wall top y-height, merlons to y-height-34k, towers to y-height-90k.
    gate=(gx, width) adds an arched gate centred at gx: flanking towers 120k wide reaching y-1.45*height-34k,
    blue glazed rosette bands, an arched opening from y up to y - 0.62*height - width/2 with tall studded
    wooden doors; doors_open 0..1 swings them open showing the passage and the bright far side.
    A 330 px adult walks through comfortably with height >= 520 and width >= 220. ink multiplies every
    outline width (e.g. 0.6 for a distant wall drawn at small height). BBox ~ (x0-4, top, x1+4, y+4):
    h 260 no gate top y-353; h 300 with gate top y-478.
ziggurat(x, y, scale=1.0)
    Anchor: bottom centre. Stepped temple tower: three tiers with buttress lines, a central stair and a small
    shrine with a glazed rosette band on top. Drawn at person scale (huge): BBox (-771, -1199, 770, 4); use
    scale 0.2-0.5 in backgrounds.
nineveh_skyline(x0, x1, y, scale=1.0, seed=0, haze=0.35, tint=None)
    Anchor: ground line y from x0 to x1 (absolute). Dense distant panorama for far backgrounds: one or two
    ziggurats or a palace, rows of flat-roofed houses with tiny windows, towers, date palms and a
    crenellated city wall with towers in front. Colours are mixed toward tint (default P['sky_warm']) by
    haze 0..1 (distance). Height ~505*scale (ziggurat top), wall 110*scale.
    BBox ~ (x0 - 76*scale, y - 506*scale, x1 + 75*scale, y + 3). Static layers only (see RENDERING COST).
harbor_dock(x0, x1, y, depth=250, bollards=True, scale=1.0)
    Anchor: y = the plank walking surface (feet of people on the pier), from x0 to x1 (absolute). Wooden pier:
    planks, front beam, posts every 150*scale px going down to y+depth (dark and wet lower half, put the sea
    in front), cross braces, bollards with rope. scale shrinks planks, posts, bollards and ink for a distant
    pier (x0, x1, y and depth stay in stage px). BBox ~ (x0-4, y-50*scale, x1+4, y+depth+3).
signpost(x, y, scale=1.0, left_text='他施', right_text='尼尼微')
    Anchor: foot of the post (ground). Wooden post with two arrow boards painted in LXGW WenKai: the upper
    board points LEFT (left_text, default '他施' Tarshish, west, centred y=-276), the lower board points
    RIGHT (right_text, default '尼尼微' Nineveh, east, centred y=-196); each board is 50*len(text)+70 px long.
    Pass '' to omit a board. Text is never mirrored. BBox with the defaults (-199, -343, 249, 9).

7. DANIEL FILM (Daniel 6)
-------------------------
lion(x, y, scale=1.0, facing=1, pose='stand', mouth=0.0, eyes='open', tail=0.0, variant=0)
    Anchor: ground under the middle of the body (paws on the ground line). A big, friendly picture-book lion,
    never frightening: warm ochre body LION['body'] with a cream belly, a round scalloped rust mane with a lighter
    inner ring and curls, round ears, a round face with big dot eyes (highlights), soft brows, puffy cream muzzle
    with whisker dots, a rounded pink-brown nose, rosy cheeks, big soft round paws, a tail with a dark tuft.
    Scale 1 is BIG (mane top ~ an adult's head): use 0.7-0.85 next to people for a big-but-cosy lion.
    pose (BBox at scale 1, facing 1; lioness in brackets):
      'stand'   (-227, -335, 236, 2)  [(-227, -306, 220, 2)]  head centre ~(150, -240)
      'walk_a' / 'walk_b'  same box; alternate every ~0.3 s while moving x (legs swap, the head bobs 6 px)
      'sit'     (-133, -372, 181, 5)  [(-133, -325, 166, 5)]  sitting up like a cat, front legs straight, tail curled
                forward on the ground; head centre ~(96, -278)
      'lie'     (-280, -191, 279, 2)  [(-280, -161, 279, 2)]  lying like a big cat, chin resting on the front paws,
                tail out behind; head centre ~(186, -96)
      'sleep'   (-184, -183, 279, 9)  [(-184, -156, 279, 9)]  as 'lie' but curled: head tipped onto the paws, eyes
                closed (eyes='open' is shown closed; pass 'half' to peek), tail curled round in front
    mouth 0..1  0 = closed smile; > 0 opens a soft round yawn / gentle roar: dark-red inside, pink tongue, two
                small BLUNT rounded teeth (no fangs). 1 = big yawn (the chin drops ~30 px). Quantise (0, .33, .66, 1).
    eyes        'open' | 'closed' | 'happy' (^ arcs) | 'half' (sleepy lids).
    tail -1..1  swings the tail tip up (+1: top -372 when standing) or down; in 'lie' it lifts the tail end, in
                'sit' / 'sleep' it curls the tip. 3-4 phases are enough for a lazy swish.
    variant     0 lion (mane), 1 lioness (no mane, lighter tan LIONESS, slimmer and a little lower, cheek ruffs).
lion_den(x, y, scale=1.0, part='all', view='cutaway', light=0.0)
    view='cutaway' (default): the den in dollhouse cross-section. Anchor: the GROUND SURFACE at the centre of the
    round opening. Above y=0 only a few rim stones and grass tufts (paint your own sky / ground to the sides; the
    ground line runs on beyond x +-770). Below: the cut earth (strata, pebbles, ragged section edge, x -778..779,
    down to y~710) around a dim chamber walled with rounded field stones, a straw-strewn sandy floor, and the
    round shaft through the ceiling (stonework at its far side). BBox (-778, -40, 779, 710).
      DEN_FLOOR_Y = 600   floor surface inside (feet of figures and lions inside: y + 600*scale)
      DEN_INNER = (-640, 96, 640, 600)   chamber x0, ceiling underside, x1, floor
      DEN_OPENING = (-140, 140)          x-range of the hole (it runs from y=0 down to the ceiling at 96)
      A standing adult (340 px) fits easily; at scale 0.5-0.6 the whole den fills the lower half of a frame.
      light 0..1: a soft beam of light falling from the opening onto the floor (dawn sun / the angel's glow;
      add FX glow on top). Keep 0 when the stone is on.
    part: 'back' = earth, chamber, walls, floor, light, shaft, rim stones; 'front' = foreground rocks and straw
      along the floor's front edge and grass tufts beside the hole. Recipe: lion_den(part='back') -> lions and
      Daniel inside (feet at y + DEN_FLOOR_Y*scale) -> lion_den(part='front') -> people standing on the ground
      (feet at y) -> den_stone over the hole (anchor at (x, y + 8*scale), it is wider than the hole).
      A figure on a rope in the shaft (daniel pose='hold_rope') goes between back and front.
    view='outside': the pit mouth seen from ground level and a little above: a dark hole (ellipse DEN_HOLE =
      (210, 62) rx, ry around the anchor) ringed by 18 stones. BBox (-270, -99, 270, 99). part='back' = the dark
      hole and the far stones, part='front' = the near stones. Someone going down / coming up: draw
      in_den_hole(figure_markup, x, y, scale) between the parts; it clips the figure to what shows above the
      near rim (everything above the ground line plus the hole).
in_den_hole(markup, x, y, scale=1.0) -> markup   (see lion_den view='outside')
den_stone(x, y, scale=1.0, sealed=False, roll=0.0)
    Anchor: bottom centre (ground contact). A big round boulder (DEN_STONE_R = (170, 128) half-width / half-height;
    centre at (0, -128)), grey-tan with cracks, moss and a highlight. BBox (-177, -262, 168, 3).
    roll (degrees) turns the cracks and moss about the centre: animate rolling = move x by roll*pi/180*128*scale
    while changing roll. sealed=True: the king's sealing cord runs over the stone to two wooden pegs in the ground
    on each side, with a terracotta clay seal (royal rosette) pressed on it at the top front. BBox
    (-212, -262, 211, 3).
upstairs_window(x, y, scale=1.0, open=1.0, part='all', wall=True, interior=False, glow=0.0)
    Anchor: the middle of the SILL TOP (bottom centre of the opening). Daniel's upstairs window: a wooden-framed
    opening WINDOW_OPENING = (-95, -262, 95, 0) with a lintel beam (beam ends), a sill, and two teal plank
    shutters with battens, hinges and knobs. open 0..1: 0 closed, .5 the shutters stand out toward the viewer
    (seen nearly edge-on), 1 swung flat against the wall on both sides (continuous; quantise in 0.25 steps).
    wall=True draws a mud-brick wall patch WINDOW_WALL = (-300, -470, 300, 200) around it (BBox = that patch);
    wall=False draws only the frame, sill and shutters to put on your own wall (BBox (-193, -299, 192, 18)
    open, (-141, -299, 140, 18) closed). part 'back' = the dim room seen through the opening (glow 0..1 warms
    it with lamp light), 'front' = wall, frame, sill, shutters. Daniel praying: window(part='back') ->
    characters.daniel(x, y + WINDOW_FLOOR_Y*scale, scale, facing, pose='kneel_pray') -> window(part='front')
    (WINDOW_FLOOR_Y = 90). interior=True is the view from inside the room: no back fill (your sky / distant
    Jerusalem shows through the opening) and a paler plaster wall.
royal_seal(x, y, scale=1.0, kind='ring')
    Anchor: centre. kind='ring': the king's signet ring standing upright - a gold band with a blue carved seal
    stone (rosette) on top. BBox (-39, -38, 38, 56). kind='impression': the clay seal lump with the stamped
    rosette (as on the sealed den stone and the decree). BBox (-36, -34, 34, 31).
decree(x, y, scale=1.0, rot=0, sealed=True)
    Anchor: centre. The king's decree: a parchment sheet between two rollers with a red title line and wavy
    writing; sealed=True adds the clay seal with two red ribbon tails at the bottom. BBox (-110, -126, 109, 143).
    Post it on a wall with rot=0 (s05), or hold it up beside the king. (characters.king(pose='sign' /
    'sit_sign') draws its own small decree in his hand.)
persian_column(x, y, scale=1.0, height=600)
    Anchor: bottom centre. Persepolis-style column: square plinth, bell-shaped base with petals, slender fluted
    shaft (`height` px), painted blue ring, palm capital, and two friendly kneeling bull fore-parts back to back
    (happy closed eyes, little horns, painted collars) holding a wooden beam end between them. Total height
    ~ height + 378; BBox at height 600 (-190, -978, 189, 2). Use scale 0.4-0.6 for a palace hall.
cushion(x, y, scale=1.0, color=None)   Anchor: bottom centre. Plump cushion with gold corner tassels (default
    P['royal_light']). BBox (-89, -61, 89, 17).
oil_lamp(x, y, scale=1.0, lit=True)   Anchor: bottom centre. Small clay oil lamp with a handle; lit adds a flame
    at the spout (x~50, y~-40) and a soft glow. BBox lit (-47, -103, 101, 14), unlit (-47, -34, 51, 2).
food_tray(x, y, scale=1.0)   Anchor: bottom centre. Brass tray of bread, grapes, figs, a pomegranate and a gold
    cup (the king's untouched supper, s09). BBox (-118, -83, 117, 18).
lyre(x, y, scale=1.0, facing=1)   Anchor: bottom centre. Musicians' wooden lyre with curved arms, crossbar,
    strings and sound box. BBox (-68, -194, 66, 2).
couch(x, y, scale=1.0, facing=1)   Anchor: bottom centre. The king's bed: wooden frame on gold lion-paw legs, a
    raised headrest on the left (facing=1), purple mattress, cream pillow, folded lilac blanket. Mattress top
    y~-122. BBox (-233, -227, 203, 2). Seat characters.king(pose='sit_sad', throne=False) on it at
    (x + 20*scale, y - 85*scale).

8. DAVID FILM (1 Samuel 17)                         sheets: python3 tools/props_sheet.py david_items david_creatures
---------------------------                                 david_camp valley
Person scale as everywhere (adult 330 px; David ~252, Goliath ~634 at the same scale: see art/characters.py).
sling(x, y, scale=1.0, facing=1, angle=0.0, length=96, stone=True, released=False)
    Anchor: the finger loop at the hand end. Two cords run `length` px to a leather pouch (with a grey stone unless
    stone=False). angle: direction of the strap from the hand in degrees, 0 = hanging down, 90 = toward facing,
    180 = straight up (any value: rotate it for a whirl). BBox angle 0 (-12, -8, 12, 106); 90 (-8, -14, 107, 12);
    180 (-13, -108, 11, 7). released=True: one cord let go, wavy, the open pouch at its end (angle 110:
    (-8, -50, 145, 7)). (characters.david draws its own sling in the sling poses.)
stone(x, y, scale=1.0, seed=0)   Anchor: bottom centre. A smooth pebble ~40 x 26 with a highlight; seed 0-4 varies
    shape / colour. BBox about (-21, -26, 19, 1). Use scale 0.5-0.7 for the flying stone (and a whoosh line).
five_stones(x, y, scale=1.0, n=5)   Anchor: bottom centre. A little pile: 3 below, 2 on top (n = 0..5 shown, so
    'one, two, three, four, five' can count up). BBox n=5 (-52, -36, 47, 1).
shepherd_bag(x, y, scale=1.0, facing=1, stones=0, strap=True)   Anchor: bottom centre. Leather bag with a flap and
    button and a carrying strap (to y~-158); stones 1-5 opens the flap with stones peeking out. BBox (-48, -158, 47, 2).
staff(x, y, scale=1.0, facing=1, rot=0.0)   Anchor: the bottom tip. Shepherd's crook ~300 px tall, hook toward
    facing. BBox (-6, -305, 61, 7). rot rotates about the tip (rot=-84 lays it on the ground pointing back).
bread_basket(x, y, scale=1.0, handle=True)   Anchor: bottom centre. Wicker basket with two loaves and a round
    cheese with a cut wedge; rim y=-56, handle top y=-104. BBox (-71, -112, 69, 2); handle=False (-71, -92, 69, 2).
harp(x, y, scale=1.0, facing=1)   Anchor: bottom centre. David's small shepherd's harp (kinnor lyre): sound box,
    two uneven curved arms, slanted yoke with gold pegs, six strings. BBox (-56, -173, 59, 2). (lyre() is the
    bigger palace lyre.)
helmet_bronze(x, y, scale=1.0, facing=1, rot=0.0, crest=True, plume=None, circlet=False)   Anchor: bottom centre
    (resting on the ground, side view). Bronze helmet with brim band and rivets; crest = Goliath's red comb;
    plume (colour) + circlet=True = Saul's helmet (as taken off David). BBox crest (-60, -125, 67, 0); Saul style
    (-64, -144, 67, 0).
spear(x, y, scale=1.0, rot=0.0, kind='soldier')   Anchor: the middle of the shaft (lying horizontally at rot=0,
    head toward +x). 'soldier' 360 px (-200, -8, 181, 7); 'goliath' 900 px, shaft as thick as a weaver's beam
    (-474, -18, 452, 16).
sword(x, y, scale=1.0, rot=0.0)   Anchor: centre. Sword in its leather scabbard, bronze guard and pommel (hilt
    on the left). BBox (-110, -29, 114, 28).
round_shield(x, y, scale=1.0, kind='israel', rot=0.0)   Anchor: centre, r=46. 'israel' wood and leather with a
    bronze rim, studs and boss; 'philistine' bronze with rings and studs. BBox (-49, -48, 48, 47).
tall_shield(x, y, scale=1.0, rot=0.0)   Anchor: centre. Goliath's great woven oval shield (the shield-bearer's),
    bronze rim and boss. BBox (-82, -158, 80, 149).
camp_stool(x, y, scale=1.0, facing=1)   Anchor: the FLOOR UNDER king(pose='sit', stool=False)'s anchor (pass the
    same x, y, scale, facing; draw it first). Folding X-frame stool with a leather seat; seat top KING_STOOL_Y =
    -74. BBox (-76, -81, 67, 4).
bear(x, y, scale=1.0, facing=1, pose='stand', mouth=0.0)   Anchor: ground under the middle of the body. A brown
    picture-book bear (BEAR colours), friendly: round ears, cream muzzle, dot eyes, rosy cheeks, round paws.
    BEAR_POSES: 'stand' / 'walk_a' / 'walk_b' on all fours (-165, -225, 234, 2) (alternate walk ~0.3 s);
    'roar' up on the hind legs, paws raised, a big open (blunt-toothed, never fierce) mouth (-110, -389, 148, 2);
    'run_a' / 'run_b' bounding (-177, -238, 233, 2) / (-165, -220, 233, 0). mouth 0..1 opens the mouth in any pose
    (roar defaults to 0.8). Scale 0.6-0.8 next to David for the memory bubble.
sheep(x, y, scale=1.0, facing=1, variant=0, pose='stand', lamb=False)   Anchor: bottom centre. Flock sheep in the
    style of animal('sheep'): variant 0 cream / tan face, 1 cream / dark-brown face and legs, 2 soft grey wool,
    3 cream with a brown patch. SHEEP_POSES: stand (-95, -147, 104, 2), graze (head down nibbling, -95, -147, 120,
    7), walk_a / walk_b (-95, -147, 106, 2), bleat (head up, eyes closed, sound arcs, -95, -161, 131, 2).
    lamb=True: a small lamb with a big head (stand (-64, -107, 75, 1)) - the lamb the lion / bear grabs.
tent(x, y, scale=1.0, facing=1, side='israel', flag=True, wave=0.0)   Anchor: bottom centre (ground at the door).
    'israel': low wide striped goat-hair tent with poles, guy ropes and a dark doorway, a blue banner with a cream
    band on a pole (-305, -342, 305, 3); 'philistine': tall peaked tent in red / ochre stripes with a red two-tailed
    pennant (-235, -411, 235, 3). flag=False drops the banner (Israel top -194, Philistine -313). wave 0..1 ripples
    the flag (2-4 phases). An adult fits the doorway at scale 1; use 0.25-0.4 for distant camps.
brook(x0, x1, y, width=60.0, scale=1.0, phase=0.0, seed=0, pebbles=True)   Absolute stage coordinates (no facing):
    a gently meandering stream running from x0 to x1 around the line y (~width px wide), blue gradient water,
    foam ripple lines that slide downstream with phase 0..1 (loop it), smooth pebbles along both banks. BBox about
    (x0-4, y-0.5*width-14*scale-12, x1+4, y+0.6*width+14*scale+12). For David picking stones (s10): kneel him on
    the bank, see characters.david(pose='kneel_pick').
day_counter(x, y, scale=1.0, n=7, filled=0.0, icons='pair', gap=64, pop=0.0)   Anchor: centre of the row. A picture
    -book day counter: n days in a row; icons='pair' = a smiling sun (morning) above a crescent moon (evening) per
    day, 'sun' or 'moon' = one row. filled counts done: with 'pair' 0.5 fills the next sun, 1.0 its moon too (so 40
    days = morning + evening shouts). Unfilled icons are faint outlines. pop 0..1 bumps the newest filled icon
    (scale up and back) as it appears. BBox n=7 pair (-229, -63, 227, 48); single row (-229, -37, 228, 36).
    Width ~ (n-1)*gap*scale + 40*scale: use scale 0.6-1, e.g. n=10 rows, or show 'many' by sliding.
valley_elah(x0, x1, y, scale=1.0, part='all', camps=True, brook=True, seed=0, bottom=None, wave=0.0)
    The Valley of Elah backdrop (static layers only: ~3 s to rasterise a full stage, then cached). Absolute stage
    coordinates: from x0 to x1, y = the VALLEY FLOOR line between the hills, painted down to bottom (default
    y + 320*scale). Two grassy hills face each other with plateaus VALLEY_HILL_H*scale (330) above the floor: LEFT
    = Israel's camp (striped goat-hair tents, blue banners), RIGHT = the Philistine camp (peaked red tents, red
    pennants); between them the valley floor recedes to hazy far ridges, and a brook winds from the far end down to
    the front centre, with pebbles. Olive trees and dry bushes on the hills. part: 'back' = far ridges, valley floor
    and brook; 'hills' = the two near hills with trees, rocks and camps (so figures in the valley can stand between
    the parts); 'all' both. camps=False leaves the plateaus empty (put your own tents / soldiers there).
    wave animates the banners. Sky not included.
valley_ground(x, x0, x1, y, scale=1.0) -> stage y of the ground surface at stage x (hill tops, slopes, and y on the
    valley floor between x0+0.44*(x1-x0) and x0+0.56*(x1-x0)): the anchor y for figures on the hills.
valley_points(x0, x1, y, scale=1.0) -> {'israel_camp', 'philistine_camp' (ground points on the plateaus, ~9% in
    from each side), 'left_edge', 'right_edge' (feet of the slopes on the floor), 'brook' (front of the brook,
    y + 40*scale), 'centre'}. For x0=0, x1=2112, y=900: israel_camp (190, 557), philistine_camp (1922, 583),
    left_edge (929, 900), right_edge (1183, 900). Figures standing in the valley foreground can use y up to
    `bottom` (the floor continues toward the viewer); in perspective, scale them up as they come forward.
Constants: BRONZE, BRONZE_DARK, BRONZE_LIGHT, LEATHER, CORD, IRON, CREST_RED, WICKER, STONE_COLS, BEAR, BEAR_POSES,
SHEEP_POSES, TENT_SIDES, KING_STOOL_Y, VALLEY_HILL_H.

9. NOAH FILM (Genesis 6-9)                sheets: python3 tools/props_sheet.py noah_ark noah_animals noah_pairs
--------------------------                        noah_weather noah_items (+ characters_noah_group.png)
Person scale as everywhere (adult 330 px). Noah, his family and the child are in art/characters.py (NOAH FILM).
God is never drawn as a person; the flood is water and weather only - never people or animals in danger.

THE ARK
ark(x, y, scale=1.0, facing=1, door=0.0, window=0.0, ramp=True, progress=1.0, floating=False, wet=False, glow=0.0,
    lamps=0.0, blocks=None)
    Anchor: grounded (floating=False) = the ground under the middle of the keel (the round bottom touches it there);
    floating=True = the WATERLINE at the middle (the keel hangs ARK_DRAFT = 150 px below it: paint the sea in front).
    A big warm picture-book boat-house, bow toward facing: a long round-bottomed hull of planks (nail pairs, a
    rub strake, a teal painted band under the gunwale cap rail), a row of small square portholes (the middle deck),
    a big side door, and on top a cabin of vertical boards (the third deck) with five small windows and one larger
    window with two teal shutters near the top, under a wide shingled gable roof with a ridge cap.
    ARK_LEN = 1915 px hull length at scale 1 (~6 adults; 2.5-3 houses). Use scale 0.25-0.6 in most shots.
    BBox (-966, -1026, 990, 4) (ramp=False right 980); floating (-966, -876, 980, 152); progress .15 (-916, -626, 914, 12).
    Geometry (local, scale 1, facing right, grounded; floating adds +ARK_DRAFT to every y):
      ARK_DOOR = (150, -560, 410, -170)    door opening x0, top, x1, sill (390 px tall: an adult, the elephants at
                                           scale <= 0.9 and a bowing giraffe fit)
      ARK_RAMP = ((150, -170), (440, -170), (980, 0))  landing along the sill, top of the slope, foot on the ground
      ARK_WINDOW = (-520, -860, -280, -630) the high window; ARK_WINDOW_STAND = (-400, -480): anchor for a person
                                           inside looking out (head and hands show in the opening)
      ARK_DECK_Y = -605 (top of the hull / cabin floor), ARK_ROOF_Y = -1010 (ridge, x -690..712; eaves y -868,
      x -775..795: birds on the roof stand on the ridge)
    Options:
      door 0..1 ('closed' / 'open')  the plank door (Z brace, iron hinges) is hinged on its left jamb and swings out
               toward the viewer (edge-on at ~.5, flat against the hull at 1); open shows a dark warm hold with straw
               and a little hanging lamp. Quantise in steps of .1-.125 ('God shut the door': 1 -> 0 over ~1 s).
      glow 0..1  a golden rim of light round the door edges + a soft halo (God shuts the door, 7:16).
      window 0..1 ('closed' / 'open')  the two teal shutters swing open (flat against the wall at 1).
      lamps 0..1  warm lamplight in the small cabin windows and the high window (night, inside life).
      ramp       the plank ramp with cleats (grounded and finished only), in front of the hull, from the door down
                 toward facing; ark_ramp_y() gives its surface.
      progress 0..1  building in stages (quantise to ~0.05): 0-.12 the keel beam grows from the middle on wooden
                 blocks; .06-.22 the curved ribs rise (fence-like skeleton) and the gunwale rail; .22-.55 the hull
                 planks fill in from the keel up (the ribs still show above), with the dark door opening; .55-.8 the
                 cabin posts, then its boards from the bottom up; .8-1 rafters, then the roof boards from the eaves
                 up; a ladder leans on the hull while building (.2-1). Door panel / shutters / ramp appear at 1.
      blocks     cradle blocks under the keel; None = while building (progress < 1, grounded) only.
      wet        darker wood, soft highlight streaks on planks / wall / roof, drips from the gunwale and the eaves
                 (in the rain, floating, just landed on Ararat).
ark_points(x, y, scale=1.0, facing=1, floating=False) -> dict of stage points: 'door' (sill centre), 'door_box'
    (x0, top, x1, sill), 'ramp_top', 'ramp_bottom', 'window_box', 'window_stand', 'windows' (5 small window boxes,
    stern to bow), 'deck', 'roof' [stern end, bow end of the ridge], 'roof_mid', 'eaves', 'bow', 'stern', 'waterline'.
ark_ramp_y(sx, x, y, scale=1.0, facing=1) -> stage y of the ramp surface at stage x (the ground y off the ramp):
    animals walking up use y = ark_ramp_y(their x, ...) each frame.
in_ark_door(markup, x, y, scale=1.0, facing=1, floating=False) -> markup clipped for someone going in at the door: the
    doorway (down past the sill) plus everything on the ramp side of the bow-side jamb, so they vanish behind the
    stern-side jamb. Draw it after the ark (same x, y, scale, facing).
in_ark_window(markup, ...) -> clipped to the high window opening (Noah looking out: noah(*ark_points(...)['window_stand'],
    scale, facing, pose='release_dove' / 'open_window' / 'hold_leaf'), drawn after the ark; open the shutters).
in_ark_porthole(markup, i, ...) -> clipped to small cabin window i (0-4): a peeking animal / a bird.
ANIMALS (two by two)
ark_animal(x, y, scale=1.0, facing=1, kind='elephant', pose='stand', female=False, eyes='open', phase=0.0)
    Anchor: the ground under the middle of the body (all feet on the ground line, also in walk frames). Friendly,
    round picture-book animals in the style of lion() / bear() / sheep(): 4 px umber ink, dot eyes with highlights and
    brows, rosy cheeks. female=True: a pink ribbon bow on the head, eyelashes and ~6% smaller (males: elephant tusks,
    stag antlers, the green-headed mallard, the lion's mane - see animal_pair). eyes 'open' | 'closed' | 'happy'.
    Walk: alternate walk_a / walk_b every ~0.3 s while moving x. ARK_ANIMALS, ARK_ANIMAL_POSES[kind].
    kind       poses                                       bbox stand (male; female ~0.94x)   notes
    elephant   stand walk_a walk_b trunk_up spray sleep    (-227, -413, 300, 2)  grey-blue, big pink-lined ear;
               trunk_up (top -554): trumpeting with sound arcs; spray (top -674): a fountain of drops from the raised
               trunk; sleep (-242, -331, 320, 16): lying, trunk curled, z's.
    giraffe    stand walk_a walk_b bow                     (-145, -692, 218, 2)  ~2.1 x an adult; bow (-145, -418,
               334, 2): neck lowered forward (to go in at the door / to drink).
    zebra      stand walk_a walk_b                         (-145, -346, 190, 2)
    horse      stand walk_a walk_b                         (-162, -376, 208, 2)  chestnut, dark mane, white blaze
    deer       stand walk_a walk_b                         (-134, -395, 170, 2)  dappled; stag antlers (doe -316)
    rabbit     stand hop sleep                             (-66, -169, 64, 2)    hop: phase 0 crouch (-66,-156,65,3),
               .25 push-off (-91,-173,82,2), .5 in the air (-107,-186,88,-67: 67 px up), .75 landing on the front
               paws (-86,-140,83,1); 4 frames ~0.08 s each while moving x ~70*scale per cycle. sleep (-66,-130,108,4)
    turtle     stand walk_a walk_b                         (-95, -91, 122, 5)
    duck       stand walk_a walk_b swim                    (-67, -117, 83, 1)    mallard drake (green head) / brown
               duck; swim: anchor = the waterline (-78, -86, 83, 15)
    monkey     stand walk_a walk_b wave sit                (-90, -175, 46, 3)    upright, curly tail
    hippo      stand walk_a walk_b yawn                    (-209, -226, 256, 2)  lavender-grey, pink muzzle; yawn: a
               big friendly yawn (blunt teeth)
    fox        stand walk_a walk_b sit sleep               (-186, -182, 146, 2)  bushy white-tipped tail; sleep curled
butterfly(x, y, scale=1.0, flap=0.0, color='orange', rot=0.0)   Anchor: body centre. flap 0..1 closes and reopens the
    wings (cycle 0, .25, .5, .75 fast). BUTTERFLY_COLORS orange blue yellow pink purple. BBox (-47, -37, 47, 28).
songbird(x, y, scale=1.0, facing=1, wing=0.0, pose='fly', color='blue', female=False)   Anchor: body centre. A small
    round bird (blue / red / yellow / brown / green, SONGBIRD_COLORS) with the dove / gull wing cycle (wing -1..1,
    cycle 1, .5, 0, -.5, -1, ...); pose 'perch' (feet at y~+32); female: duller colours. BBox wing 1 (-48, -70, 43,
    19), wing -1 (-48, -30, 43, 42), perch (-48, -30, 43, 32).
dove(..., leaf=False)   (section 5) leaf=True: a fresh olive leaf in the dove's beak (8:11), fly and stand.
animal_pair(kind, x, y, scale=1.0, facing=1, pose='stand', phase=0.0, eyes='open', gap=None)
    He and she side by side for the 'two by two' queue: the male at (x, y) in front, the female a little ahead
    (toward facing, gap*scale, default per kind ~0.3 body lengths) and 18*scale higher (farther away), drawn first,
    in the opposite walk frame (so they don't march in step) and with her bow. kind: PAIR_KINDS = ARK_ANIMALS + lion
    (lion + lioness at 0.8 x lion() scale), bear, sheep, cow, goat, donkey, camel (these four only stand), dove,
    songbird (flying; phase = wing phase 0..1). Unknown poses fall back to 'stand'. BBox walk_a e.g. elephant
    (-227, -407, 422, 2), giraffe (-145, -692, 307, 1), zebra (-145, -346, 283, 2), lion (-182, -262, 319, 1),
    rabbit (-66, -170, 108, 2), camel (-138, -367, 412, 1).
WEATHER, WATER, LANDSCAPE
rain(phase=0.0, intensity=0.6, x0=0, y0=0, x1=W, y1=H, angle=10, seed=0, color=None, drops=None, scale=1.0)
    Absolute stage coordinates (a layer helper, no anchor): slanted pale streaks clipped to the box (x0, y0, x1, y1);
    the count grows with intensity (0..1.5). intensity < 0.3 (or drops=True) draws separate outlined drops instead
    ('drip, drip...'). phase 0..1 loops seamlessly (each streak falls once per cycle at its own speed): 6-8 phases
    at ~0.06 s. Cost ~1.5 s per full-stage frame at intensity 1 -> render a small flipbook.
puddle(x, y, scale=1.0, width=260, ripple=0.0, splash=0.0, sky=None)   Anchor: centre of the puddle on the ground.
    Flat puddle reflecting the sky (sky colour), ripple 0..1 loops expanding rings, splash 0..1 a crown of water and
    flying drops (rise to ~.5, falling and landing by 1). BBox (-137, -31, 135, 30); splash .5 top -63.
flood_sea(x0, x1, level, phase=0.0, bottom=None, storm=0.0, seed=0, scale=1.0, foam=True)
    Absolute coordinates: a wide body of water whose surface is at stage y = level, four wave bands to `bottom`
    (default stage bottom), foam crests; phase 0..1 loops; storm 0..1 darkens it to slate and raises the waves.
    Animate the rising flood by moving `level` (quantise ~10 px) and draw it in FRONT of hills / houses / Ararat
    so they disappear under it; draw it in front of a floating ark (anchor at the waterline) to hide the keel.
dark_cloud(x, y, scale=1.0, width=620, height=230, seed=0, light=0.0, flash=0.0)   Anchor: centre. A heavy slate
    storm cloud with a lighter front bank; light 0..1 greys it, flash 0..1 a soft golden glow inside (distant
    lightning, gentle). BBox (-379, -251, 384, 128) at the defaults.
rainbow(x, y, scale=1.0, progress=1.0, radius=900, band=30, glow=True)   Anchor: centre of the arc on its base line.
    Seven soft bands RAINBOW = red, orange, yellow, green, cyan, blue, violet (红橙黄绿青蓝紫) from the outside in;
    progress 0..1 draws them ONE BAND AT A TIME in that order (band i sweeps in from the left foot over the top
    during progress i/7 .. (i+1)/7): key band k as the narrator names it -> progress (k+1)/7. The feet fade out
    (put clouds / hills over them); glow = a soft golden haze behind. BBox (-1038, -1024, 1036, -48). ~2 s per
    frame (blur): render the 8 key values only.
ararat(x, y, scale=1.0, snow=True, green=0.0, seed=0, facing=1)   Anchor: bottom centre. Mount Ararat: the big
    snow-capped Greater Ararat (left) and the smaller Lesser Ararat (right, hazier), rocky ridges, a shady east side.
    ARARAT_LEDGE = (-260, -640, 260): the saddle (x0, y, x1) on the big mountain's shoulder where the ark rests:
    ark(x, y + ARARAT_LEDGE[1]*scale, ~0.25*scale, ramp=False, wet=True). green 0..1: grass and bushes return on the
    lower slopes. BBox (-1038, -1083, 1010, 33). Mountain tops above the flood: draw flood_sea in front.
football_field(x, y, scale=1.0, goals=True)   Anchor: bottom centre of the near touchline. A little green pitch in
    perspective with mown stripes, white lines, centre circle, boxes, two goals with nets and a ball. FOOTBALL_LEN =
    1000 px (near touchline at scale 1). Size comparison '比一个足球场还要长': the ark is ~137 m, a pitch ~100 m, so
    draw ark(..., scale = pitch_scale * 1.37 * FOOTBALL_LEN / ARK_LEN, ramp=False). BBox (-502, -284, 500, 18).
BUILDING AND FOOD
saw(x, y, scale=1.0, facing=1, rot=0.0)        Anchor: the grip. Hand saw, blade toward +x. BBox (-29, -28, 172, 21).
hammer(x, y, scale=1.0, facing=1, rot=0.0)     Anchor: the grip; handle toward +x, iron head across it at x~91.
    BBox (-23, -34, 106, 25).
plank(x, y, scale=1.0, rot=0.0, length=260, seed=0)   Anchor: centre. BBox (-133, -16, 132, 15).
timber_pile(x, y, scale=1.0, facing=1, kind='mixed')  Anchor: bottom centre. 'logs' (round ends toward the viewer,
    stacked 3-2-1) (-108, -212, 202, 3); 'planks' (six on two sleepers) (-117, -159, 156, 3); 'mixed' (logs with
    planks on top) (-117, -235, 202, 3).
sawhorse(x, y, scale=1.0, facing=1, plank=True)  Anchor: bottom centre. A-frame trestle (top -118) with a plank
    across it. BBox (-137, -147, 197, 9); plank=False (-127, -121, 127, 9).
nails(x, y, scale=1.0, box=True, n=9)   Anchor: bottom centre. An open box of nails + three loose ones (-57, -67, 138, 4);
    box=False a few loose nails (-80, -20, 47, 5).
pitch_bucket(x, y, scale=1.0, facing=1, brush=True)   Anchor: bottom centre. Wooden bucket of glossy black pitch
    (6:14) with drips and a brush. BBox (-49, -185, 60, 2).
food_basket(x, y, scale=1.0, kind='fruit')   Anchor: bottom centre, rim y=-56. kind 'fruit' (apples, pear, grapes)
    (-70, -101, 69, 2), 'grain' (heaped grain and ears, top -130), 'veg' (carrots, a melon, greens, top -109),
    'bread' (= bread_basket(handle=False)). sack() and jar() (section 3) are the food sacks and jars.
hay(x, y, scale=1.0, facing=1, kind='bale')   Anchor: bottom centre. 'bale' (-83, -112, 94, 2), 'bundle' a sheaf
    tied in the middle, lying (-93, -53, 97, -11), 'pile' a soft heap (-112, -76, 113, 2) - animal food / bedding.
olive_branch(x, y, scale=1.0, facing=1, rot=0.0, leaves=5, olives=True)   Anchor: the cut end; the twig grows
    toward +x. BBox (-5, -37, 146, 20). olive_leaf(x, y, scale=1.0, facing=1, rot=0.0): one leaf, anchor at its stem,
    pointing +x, BBox (-2, -8, 45, 5) (the dove's leaf: dove(leaf=True)).
altar(x, y, scale=1.0, fire=1.0, phase=0.0, smoke=True)   Anchor: bottom centre. A small heap of rounded field stones
    with sticks on top (8:20); fire 0..1 a friendly flame with a warm glow, phase 0..1 flickers it (3-4 phases),
    smoke = soft translucent wisps rising. BBox (-138, -422, 137, 4); fire=0 (-124, -158, 120, 4).
Constants: TIMBER, TIMBER_LIGHT, TIMBER_DARK, PITCH, OLIVE_LEAF, OLIVE_LEAF_DARK, RAINBOW, BOW_PINK, RAIN_COL, HAY,
ARK_*, ARARAT_LEDGE, FOOTBALL_LEN, ELEPHANT, GIRAFFE, RABBIT, TURTLE, DUCK, MONKEY, HIPPO, FOX (colours),
ARK_ANIMALS, ARK_ANIMAL_POSES, PAIR_KINDS, BUTTERFLY_COLORS, SONGBIRD_COLORS.
RENDER COST (2112 x 1188 layer, uncached): ark ~1.2 s, noah_family ~1.0 s, an animal / pair ~1 s, flood_sea ~1.2 s,
rain (intensity 1, full stage) ~1.6 s, ararat ~1.5 s, rainbow ~2 s - same range as the existing library; quantise
every option into a small flipbook (see RENDERING COST above).

10. JOSEPH FILM (Genesis 37-50)              sheets: python3 tools/props_sheet.py joseph_items joseph_animals joseph_egypt
-------------------------------                     (+ characters_joseph_group.png: pit, chariot, caravan with people)
Person scale as everywhere (adult 330 px). Joseph, Jacob, the brothers, Pharaoh, Egyptians, traders and the modern
siblings are in art/characters.py (JOSEPH FILM). God is never drawn as a person; nothing violent is ever shown: the pit is
dry, the coat is only torn and dirty, the prison is plain.
THE COAT, THE DREAMS
coat_of_colours(x, y, scale=1.0, facing=1, state='held', torn=False, dirty=False, progress=1.0, rot=0.0)
    The coat of many colours on its own: a long-sleeved robe in bold bands (COAT_BANDS = red, yellow, blue, green,
    purple, orange, the same colours as characters.joseph's coat) on a cream base (COAT_BASE). progress 0..1 reveals the
    colours one at a time exactly like joseph(progress=...) (colour k at (k+1)/6). state:
      'held'    hanging, front view; Anchor: the TOP CENTRE (the neck, where hands hold it up) (-128, -2, 127, 264)
      'lying'   laid flat on the ground (hem toward facing); Anchor: bottom centre (-134, -104, 132, 3)
      'folded'  a neat folded stack; Anchor: bottom centre (-81, -57, 80, 12)
      'bundle'  crumpled up (in someone's arms / thrown down); Anchor: centre (-115, -84, 100, 86)
    torn=True ragged hem, a torn short sleeve, a dark rip (no blood ever); dirty=True brown dirt smudges (37:31-33).
    (characters.jacob(pose='give' / 'cry') draws it in his hands.)
wheat_sheaf(x, y, scale=1.0, facing=1, bow=0.0, rise=1.0, glow=0.0, ripe=1.0, kind='standing', seed=0)
    Anchor: bottom centre (the cut stalk ends on the ground). A bound sheaf of golden wheat: spreading stalk ends, a
    twisted straw tie at y=-92, a fan of ears up to ~-245. BBox standing (-78, -249, 76, 3).
      bow 0..1   the top bends toward facing at the tie (up to 62 deg) and the bundle leans 8 deg: the brothers' sheaves
                 bowing (bow=1 (-42, -209, 168, 5)); give each a facing toward Joseph's sheaf.
      rise 0..1  0 lying on its side .. 1 standing up (rotates about the cut ends): 'my sheaf rose and stood upright'.
      glow 0..1  a soft golden halo behind it (Joseph's sheaf) (-139, -306, 138, 5).
      ripe 0..1  green (0) .. golden (1).  kind='bundle': a sheaf lying on the field (-130, -130, 122, 24).
    Quantise bow / rise in steps of ~0.1-0.125.
dream_bubble(x, y, w=600, h=380, tail=None, inner='', pop=1.0, fill='#fbf6ea', glow=True, seed=0)
    ABSOLUTE stage coordinates (centre x, y; size w x h). A soft cloud-shaped dream frame (scalloped edge, umber outline,
    a golden glow behind), three shrinking circles trailing toward tail=(tx, ty) (the sleeper's head), and ``inner``
    (markup in stage coordinates, e.g. cows, sheaves, a vine) CLIPPED to the cloud. pop 0..1 grows it from its centre
    (ease in ~0.5 s; quantise 0, .25, .5, .75, 1). BBox about (x - w/2 - 41, y - h/2 - 40, x + w/2 + 41, y + h/2 + 84)
    plus the tail. Several bubbles may share a document (ids derive from x, y, w, h, seed).
grapevine(x, y, scale=1.0, grow=1.0, facing=1)   Anchor: bottom centre. The cupbearer's dream vine (Gen 40:9-11): a
    twisted stem with three branches; grow 0..1: 0-.4 the branches grow out one by one, .3-.5 leaves, .5-.75 blossoms,
    .7-1 grape clusters (green, ripening to purple at 1). BBox grow=1 (-128, -287, 131, 9). Steps of ~0.1.
bread_baskets(x, y, scale=1.0, n=3, birds=0)   Anchor: bottom centre (rest it on the baker's head). The baker's dream
    (40:16-17): n flat wicker baskets stacked, the top one heaped with loaves and a round cake; birds 1-3 small birds
    pecking on top. BBox n=3 (-80, -164, 78, 2); birds=3 top -190.
cow(x, y, scale=1.0, facing=1, kind='fat', pose='stand', phase=0.0, mouth=0.0)   Anchor: ground under the middle of the
    body. Pharaoh's dream cows (41:1-4), comic and friendly: 'fat' = round glossy cream cow with brown patches and
    happy ^ eyes (-138, -226, 193, 1); 'thin' = a bony cow on long thin knobbly legs, ribs, big round hungry eyes
    (-119, -251, 177, 2). pose: 'stand', 'walk' (phase 0..1, diagonal gait, a little bob; 'walk_a' / 'walk_b' = phase 0
    / .5), 'graze' (head down: fat (-138, -201, 203, 1), thin (-119, -199, 187, 2)). mouth 0..1 opens the mouth (the
    thin cows 'eat' the fat ones: munch 0 / .8 alternately - keep it comic, never show eating literally).
    Walk: 8 phases at ~0.08 s while moving x ~87*scale per cycle.
THE PIT, THE CARAVAN, SILVER
pit(x, y, scale=1.0, facing=1, view='outside', part='all', rope=0.0, width=400)
    The dry, empty pit (37:24: 'there was no water in it').
      view='outside'  Anchor: centre of the round opening on the ground. A ring of rounded field stones round a dark
                      hole (ellipse PIT_R = (150, 46) half-axes), the far inner wall's stone courses showing, dry grass
                      tufts; BBox (-221, -75, 219, 86). part='back' (shadow, hole, inner wall, back rim) / 'front' (front
                      rim stones and tufts): FIGURE-IN-THE-PIT RECIPE: pit(part='back') -> in_pit(figure) -> pit(part=
                      'front'), all at the same x, y, scale. For Joseph calling from deep down use joseph(x, y +
                      300*scale, scale, pose='call_up', coat='torn'): only his face and raised hands show.
      view='cutaway'  Anchor: the GROUND LINE at the centre of the opening; a cross-section of the earth (soil layers,
                      pebbles) from x-width to x+width, the stone-lined shaft (2*150 wide) PIT_DEPTH = 470 deep with a
                      lit back wall and a sandy floor with dry grass. Stand a figure on PIT_FLOOR = (0, 470) (local):
                      joseph(x, y + PIT_DEPTH*scale, scale, pose='call_up') - his raised hands stay ~70 px below the rim.
                      Brothers stand on the ground line beside it (x +- (rx + 60)*scale). BBox (-402, -25, 401, 540).
      rope 0..1       a rope hanging into the pit from the rim (0 = none, 1 = to near the floor): being pulled up -
                      joseph(pose='hold_rope') + brothers(pose='pull') at the rim.
in_pit(markup, x, y, scale=1.0)   Clip markup to the pit opening seen from outside (everything above the front rim edge
    stays visible). x, y, scale = the PIT's.
camel(x, y, scale=1.0, facing=1, pose='stand', phase=0.0, load=True, bridle=True, eyes='open')   Anchor: ground under
    the middle of the body. A caravan camel in the style of animal('camel'): one hump, knobbly knees, pad feet, lashes.
    load=True: a red saddle blanket with gold / blue stripes and fringe over the hump, a rolled teal rug on top, a
    burlap bundle and a leather spice bag tied on the flanks. bridle=True: a red halter with gold tassels and a lead rope
    hanging forward to CAMEL_LEAD = (300, -150) (local; a trader in pose 'lead' walks ahead holding it).
    pose 'walk' with phase 0..1 = a PACE (both legs of one side swing together, as camels walk), the body bobbing and
    the head nodding a little ('walk_a' / 'walk_b' = phase 0 / .5). BBox stand (-138, -357, 304, 2), walk (union of
    phases) (-145, -365, 304, 2). Walk: 8 phases (0, 1/8 ...) at ~0.09 s while moving x ~113*scale per cycle (the
    planted feet then do not slide). A caravan: camels every ~460*scale, a trader leading, the next camel's rope optional.
donkey(x, y, scale=1.0, facing=1, pose='stand', phase=0.0, sacks=2)   Anchor: ground under the middle of the body. The
    grey donkey of animal('donkey') with a red saddle cloth and grain sacks hanging on both flanks (sacks 0 / 1 / 2);
    pose 'walk' + phase (diagonal gait, bob, nodding head; walk_a / walk_b; ~87*scale per cycle). BBox
    (-115, -308, 169, 2). The brothers'
    journey to Egypt and back (42-43).
coins(x, y, scale=1.0, n=20, kind='pile', seed=0)   Anchor: bottom centre. Silver coins (SILVER) with a rim, a stamped
    mark and a highlight: 'pile' a little heap of n (20: (-78, -51, 78, 3)), 'row' counted out in rows of ten (count
    up n = 1..20 for '二十块银子': (-150, -62, 149, -3)), 'stacks' stacks of five, 'pouch' a leather money pouch with
    coins at its mouth and a few beside it ((-46, -96, 102, 5)). (characters.trader(pose='give' / 'count') holds some.)
EGYPT
pyramids(x, y, scale=1.0, n=3, haze=0.0, facing=1, ground=True)   Anchor: bottom centre. Three (n=1..3) sand-coloured
    pyramids with a lit and a shaded face, faint courses and gold capstones on a low desert ground band (ground=False
    leaves it off). haze 0..1 blends them toward the day sky for distance. BBox (-764, -520, 902, 28) at scale 1: use
    0.2-0.6 on the horizon (static layer).
nile(x0, x1, y, width=150.0, scale=1.0, phase=0.0, seed=0, reeds=True)   ABSOLUTE stage coordinates: the Nile as a wide
    band from x0 to x1 centred on y, green banks, blue gradient water with ripples sliding with phase 0..1 (loop it),
    lily pads and pink lotus, papyrus clumps along the near bank. BBox ~ (x0, y - width/2 - 20, x1, y + width/2 + 34).
papyrus(x, y, scale=1.0, sway=0.0)   Anchor: bottom centre. A papyrus clump (-64, -140, 51, 1).
field(x0, x1, y, depth=120.0, scale=1.0, ripe=1.0, dry=0.0, seed=0)   ABSOLUTE stage coordinates: a band of wheat
    (rows of stalks with ears) from x0 to x1, top at ~y, soil down to y + depth. ripe 0..1 green -> golden (the seven
    good years); dry 0..1 withers it to short dry stubble on cracked earth (the famine, 41:54).
egypt_house(x, y, scale=1.0, variant=0, facing=1)   Anchor: bottom centre. variant 0: a whitewashed flat-roofed house with
    high barred windows and a painted lintel over the door (-296, -456, 352, 4); variant 1: Potiphar's villa with a
    columned porch and a painted frieze (-442, -496, 440, 6). Doors are 260 px tall at scale 1: an adult walks in at
    scale >= 1.35; use 0.4-0.8 for houses further back.
egypt_column(x, y, scale=1.0, height=420)   Anchor: bottom centre. A painted papyrus-bundle column with blue / red bands
    and an open green capital (-75, -439, 73, 2) at height 420. Palms: palm_tree() (section 4).
granary(x, y, scale=1.0, fill=1.0, facing=1)   Anchor: bottom centre. Pharaoh's storehouses (41:48-49): three domed mud
    silos behind a yard wall, each with a cutaway window showing its grain LEVEL, a ladder, and in front golden grain
    heaps 'like mountains' and a row of sacks. fill 0..1: the silo levels rise one after another (left first), the
    heaps grow and sacks appear. GRANARY_W = 820; BBox (-414, -418, 412, 30). Quantise fill in steps of ~0.1.
grain_heap(x, y, scale=1.0, size=1.0, seed=0)   Anchor: bottom centre. A golden grain heap, ~300 x 200 at size 1
    ((-153, -203, 152, 2)); size up to 3 for mountains.
grain_sacks(x, y, scale=1.0, n=1, open_=False, facing=1)   Anchor: bottom centre. n 1..6 burlap grain sacks in a little
    stack (1: (-54, -110, 51, 4); 6: (-123, -242, 124, 4)); open_=True opens the first one, heaped with grain, a little
    spilled.
egypt_throne(x, y, scale=1.0, facing=1)   Anchor: the FLOOR under pharaoh(pose='sit_throne', throne=False) (same x, y,
    scale, facing; draw it first): gilded lion-legged throne with a tall back of coloured feather bands, a cushion
    (seat top EGYPT_SEAT_Y = -73), an armrest ending in a little lion head and a footstool. BBox (-89, -325, 167, -1).
signet_ring(x, y, scale=1.0, rot=0.0)   Anchor: centre. Pharaoh's ring (41:42) = royal_seal(kind='ring'):
    (-39, -38, 38, 56).
gold_chain(x, y, scale=1.0, state='held')   'held': hanging in a U from two hands (anchor = the middle between them, the
    hands at x +- 70, the pendant at y+172) (-79, -7, 78, 191); 'lying': a loose loop (-79, -7, 78, 119).
prison_window(x, y, scale=1.0, light=1.0, wall=True, facing=1)   Anchor: centre of a small high barred window (a
    glimpse of sky and green outside) in a patch of rough stone wall (wall=False: just the window); light 0..1 a soft
    beam slanting down into the cell (use it for 'God was with Joseph' together with engine.fx glow). BBox
    (-232, -173, 295, 439) with the beam.
prison_bars(x, y, scale=1.0, width=300, height=400, open_=0.0, facing=1)   Anchor: bottom centre. A barred prison door in
    a stone frame, dark cell behind; open_ 0..1 swings it open on its left hinge. BBox (-171, -421, 170, 2).
chariot(x, y, scale=1.0, facing=1, part='all', wheel=0.0, horse=True, phase=0.0)   Anchor: ground under the wheel.
    Joseph's chariot (41:43): a gilded car with lapis / carnelian / teal stripes, six-spoked wheels (radius 80), a pole to
    a chestnut horse (ark_animal('horse') style) with a blue saddle pad, gold tassels, a red plume and bridle, reins to
    the front rail. wheel 0..1 turns the spokes (one spoke spacing per cycle; turn wheel by distance / (2*pi*80*scale)
    * 6 when moving); phase 0..1 switches the horse's walk frame (<.5 walk_a, else walk_b). BBox (-96, -404, 576, 7).
    RIDER RECIPE: chariot(part='back') -> joseph(*local_to_stage(x, y, scale, facing, *CHARIOT_STAND), scale, facing,
    attire='ruler', pose='ride_wave') (or CHARIOT_SEAT with pose='ride', seated on the bench) -> chariot(part='front')
    (the car's near side covers his legs). CHARIOT_STAND = (4, -96), CHARIOT_SEAT = (-20, -96).
toy(x, y, scale=1.0, facing=1, kind='horse', rot=0.0)   Anchor: bottom centre. The siblings' toy: a little wooden horse
    on red wheels (-68, -144, 71, 3) or a striped ball (-36, -71, 36, 2). characters.child(toy=...) holds it.
Constants: COAT_BANDS, COAT_BASE, WHEAT, WHEAT_DARK, SILVER, SILVER_DARK, LINEN_P, LAPIS_P, CARNELIAN_P, MUD, MUD_DARK,
NILE, PAPYRUS, PIT_R, PIT_DEPTH, PIT_FLOOR, CAMEL_LEAD, CHARIOT_STAND, CHARIOT_SEAT, EGYPT_SEAT_Y, GRANARY_W.
RENDER COST: like the rest of the library (camel / cow / donkey ~ an ark_animal, granary ~ a house, pyramids / nile on
static layers); quantise every 0..1 option into a small flipbook.

Helpers / constants
-------------------
local_to_stage(x, y, scale, facing, lx, ly) -> (stage_x, stage_y); castor_height(growth);
fish_mouth_points(mouth); fish_mouth_path(...); in_fish_mouth(...).
SHIP_DECK_Y = -165, SHIP_INTERIOR, SHIP_BED, SHIP_SLEEP, SHIP_HOLD_LANTERN (ship, section 2);
BOOTH_SEAT, BOOTH_DEPTH (booth); KING_SEAT_Y, KING_ASH_DX (throne / ash_pile); CASTOR_SHADE,
CASTOR_BOOTH_DX, WORM_BITE_DX (castor_plant); FISH_COLORS (small_fish); HOUSE_K = 2.2 and ZIGGURAT_K = 2.4
are the internal up-scales of the house / ziggurat drawings (informational). Daniel film: LION, LIONESS (colours),
LION_POSES, DEN_FLOOR_Y, DEN_INNER, DEN_OPENING, DEN_HOLE, DEN_STONE_R, WINDOW_OPENING, WINDOW_FLOOR_Y, WINDOW_WALL,
SHUTTER; in_den_hole(...).
Contact sheets of everything: ``python3 tools/props_sheet.py [fish ship items castor plants creatures
buildings daniel david_items ... noah_ark noah_animals noah_pairs noah_weather noah_items joseph_items
joseph_animals joseph_egypt]``
-> build/preview/props_*.png (red cross = anchor, dashed figure = 330 px adult at the same scale).
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

_FISH_LIP_U = [(274, 30), (345, 47), (430, 54), (518, 44), (588, 16)]      # closed mouth (a gentle smile),
_FISH_LIP_L = [(274, 30), (345, 41), (430, 48), (518, 38), (596, 28)]      # corner -> tip
# wide-open targets (mouth=1): a rounded throat at the back, bowed lips, protruding rounded lip tips
_FISH_OPEN_U = [(214, 70), (216, 0), (236, -62), (284, -118), (352, -158), (430, -180), (500, -184), (546, -170),
                (570, -142)]
_FISH_OPEN_L = [(214, 70), (216, 138), (238, 202), (284, 254), (346, 290), (414, 310), (476, 314), (516, 302),
                (540, 274)]
_FISH_FORE = [((590, -40), (584, -192)), ((556, -122), (564, -238)), ((500, -200), (500, -284)),
              ((418, -252), (420, -312)), ((268, -296), (268, -326)), ((80, -315), (80, -322))]
_FISH_POUCH = [((598, 62), (538, 322)), ((570, 150), (500, 350)), ((486, 232), (424, 366)), ((380, 284), (336, 364)),
               ((268, 304), (252, 340)), ((205, 302), (200, 316))]
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
    front += _p(f"M{_f(236 - 8 * e)},-205 Q{_f(162 - 40 * e)},-40 {_f(204 - 48 * e)},{_f(116 + 6 * e)}", sw=4.5)
    front += _p(f"M{_f(205 - 8 * e)},-150 Q{_f(150 - 40 * e)},-30 {_f(196 - 46 * e)},110", sw=3, stroke=dark,
                extra='opacity="0.4"')
    pb = (182, 104)
    fan = [(196, 70), (120, 60), (40, 92), (6, 140), (24, 176), (70, 182), (120, 160), (176, 136)]
    fan_rays = ""
    for q in ((45, 98), (25, 140), (55, 172), (110, 160)):
        fan_rays += _line(170, 104, q[0] + 10, q[1] - 4, sw=3, color=dark, extra='opacity="0.5"')
    front += _g(_p(_sm(fan, closed=True), fin_col, 4.5) + fan_rays,
                f"translate({_f(-30 * e)},{_f(10 * e)}) rotate({-10 * tl:.2f} {pb[0]} {pb[1]})")
    if m < 0.5:  # smile: the mouth line curls up into a little dimple at the corner
        a = 1 - m * 2
        front += _p(f"M{_f(C[0] + 14)},{_f(C[1] + 8)} Q{_f(C[0] - 6)},{_f(C[1] + 2)} {_f(C[0] - 12)},{_f(C[1] - 18)}",
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
    if r[2] < r[0] or r[3] < r[1]:          # (nearly) closed mouth: collapse to a point between the lips
        cx_, cy_ = (r[0] + r[2]) / 2, (r[1] + r[3]) / 2
        r = (cx_, cy_, cx_, cy_)
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


BOOTH_DEPTH = (54, -28)        # offset of the back frame (slight 3/4 view from the front-right, above)


def _booth(shade=False):
    """Jonah's little shelter (Jonah 4:5) in a slight 3/4 view: rough sticks lashed into a front and a back
    A-frame, a striped cloth thrown over the ridge so its sloped top is visible, sagging between the rafters and
    hanging down past the eaves at the sides and back; the inside under the roof is in shade."""
    wood, wd = P["wood"], P["wood_dark"]
    cloth = S.mix(P["headcloth"], P["sand"], 0.3)
    cloth_d = S.shade(cloth, -0.18)
    under = S.mix(S.shade(cloth, -0.45), P["ink_soft"], 0.15)
    stripe = P["sail_stripe"]
    DX, DY = BOOTH_DEPTH
    out = ""
    if shade:      # soft cool shadow on the ground under the roof (inside BOOTH_SEAT)
        out += _ell(10, -6, 182, 30, S.mix(P["ink"], P["sky_day_top"], 0.3), 0,
                    extra='opacity="0.5" filter="url(#soft)"')
    # front-frame key points (the back frame is the same shifted by BOOTH_DEPTH)
    FL, FR, FA = (-178, -236), (178, -240), (0, -374)          # front left / right eave, front apex
    BL, BR, BA = (FL[0] + DX, FL[1] + DY), (FR[0] + DX, FR[1] + DY), (FA[0] + DX, FA[1] + DY)
    # back posts (farther: base higher, thinner, darker)
    out += _stick([(-112 + DX * 0.9, -16), (-115 + DX, -150), (-110 + DX, -258 + DY)], 9, S.shade(wd, 0.05), 3)
    out += _stick([(146 + DX * 0.9, -18), (149 + DX, -140), (146 + DX, -262 + DY)], 9, S.shade(wd, 0.05), 3)
    # shady inside of the roof seen through the open front: the underside of the far slope, and a short shade
    # cloth hanging from the back eave
    gid = _uid("boothund", 0)
    out += (f'<defs>{S.lin_grad(gid, [(0, S.shade(under, -0.1)), (0.7, under), (1, S.mix(under, cloth, 0.4))])}</defs>')
    out += _p(_poly([FL, FA, (FR[0] - 4, FR[1] - 4), (BR[0] - 8, BR[1] + 8), (BL[0] + 8, BL[1] + 8)]), f"url(#{gid})", 0)
    back_curtain = [(BL[0] + 10, BL[1] + 2), (BR[0] - 10, BR[1] + 2), (BR[0] - 14, -196), (BR[0] - 60, -188),
                    (BA[0] + 20, -198), (BA[0] - 40, -190), (BL[0] + 60, -200), (BL[0] + 14, -192)]
    out += _p(_poly(back_curtain), S.mix(under, cloth, 0.45), 3)
    for xx in (-60, 20, 100):
        out += _line(xx + DX * 0.5, -246, xx + DX * 0.5 + 3, -200, sw=2.5, color=S.shade(under, -0.15),
                     extra='opacity="0.5"')
    # front posts: uneven sticks, the tops poke up past the tie bar
    out += _stick([(-158, 2), (-162, -120), (-156, -200), (-160, -292)], 13, wood, 3.5, knots=(0.45,))
    out += _stick([(146, 2), (150, -110), (146, -205), (152, -284)], 13, wood, 3.5, knots=(0.62,))
    out += _stick([(-196, -256), (-40, -260), (194, -254)], 9, S.shade(wood, -0.1), 3)
    for bx, by in ((-158, 0), (146, 0)):
        out += _ell(bx - 14, by - 2, 15, 7, P["stone"], 3) + _ell(bx + 14, by - 1, 11, 6, P["stone_dark"], 3)
    # the cloth: two sloped panels from the front rafters back to the ridge pole, sagging between the frames,
    # the side edges hanging below the eaves with ragged hems
    def slope(e_front, e_back, sgn):
        hem = []
        for i in range(7):
            u = i / 6
            p = _lerp2((e_front[0] + sgn * 14, e_front[1] + 30), (e_back[0] + sgn * 10, e_back[1] + 26), u)
            hem.append((p[0], p[1] + (10 if i % 2 else 0)))
        sag = _lerp2(_lerp2(FA, BA, 0.5), _lerp2(e_front, e_back, 0.5), 0.55)
        sag = (sag[0], sag[1] + 12)
        top = [FA, BA]
        pts = top + [_lerp2(BA, e_back, 0.5), (e_back[0] + sgn * 6, e_back[1] + 4)] + list(reversed(hem)) + \
            [(e_front[0] + sgn * 6, e_front[1] + 4), _lerp2(e_front, FA, 0.5)]
        d = _poly(pts)
        inner = _p(_poly([_lerp2(e_front, FA, 0.6), sag, _lerp2(e_back, BA, 0.6), BA, FA]), S.shade(cloth, 0.12), 0,
                   extra='opacity="0.6" filter="url(#soft)"')
        for k in (0.18, 0.3):                    # two terracotta stripes running along the hem
            a_ = _lerp2(e_front, FA, k)
            b_ = _lerp2(e_back, BA, k)
            inner += _line(a_[0], a_[1] + 8, b_[0], b_[1] + 8, sw=7, color=stripe, extra='opacity="0.85"')
        inner += _p(f"M{_f(FA[0])},{_f(FA[1])} Q{_f(sag[0])},{_f(sag[1])} {_f(e_back[0])},{_f(e_back[1])}", sw=3,
                    stroke=cloth_d, extra='opacity="0.6"')
        return _p(d, cloth, 0) + _clip(_uid("boothsl", sgn), d, inner) + _p(d, sw=4)
    out += slope(FL, BL, -1) + slope(FR, BR, 1)
    # front edge of the cloth hanging a little below the front rafters (striped, scalloped)
    for e, sgn in ((FL, -1), (FR, 1)):
        hem = []
        for i in range(9):
            u = i / 8
            p = _lerp2(FA, e, u)
            hem.append((p[0], p[1] + 14 + (8 if i % 2 else 0) + 6 * u))
        d = _poly([FA, (e[0] + sgn * 8, e[1] + 2)] + list(reversed(hem)))
        out += _p(d, cloth_d, 0) + _clip(_uid("boothhem", sgn), d, _line(FA[0], FA[1] + 10, e[0], e[1] + 12, sw=6,
                                                                         color=stripe, extra='opacity="0.8"'))
        out += _p(d, sw=3.5)
    # ridge pole and rafters crossing at both apexes, ends sticking out above the cloth
    out += _stick([(BA[0] - 2, BA[1] - 4), (FA[0] + 2, FA[1] - 2)], 9, wd, 3.2)
    out += _stick([(BL[0] + 4, BL[1]), (BA[0] + 26, BA[1] - 22)], 8, S.shade(wd, 0.05), 3)
    out += _stick([(BR[0] - 4, BR[1]), (BA[0] - 22, BA[1] - 20)], 8, S.shade(wd, 0.05), 3)
    out += _stick([(-176, -228), (-80, -300), (30, -400)], 10, wd, 3.5)
    out += _stick([(174, -232), (84, -298), (-26, -394)], 10, wd, 3.5)
    out += _lashing(0, -372) + _lashing(BA[0], BA[1] + 2, 0.8) + _lashing(-158, -262, 0.85) + _lashing(148, -260, 0.85)
    # a few leafy branches laid on the cloth
    for sx, sy, ang in ((-130, -284, -30), (60, -360, 28)):
        out += _g(_p("M0,0 Q60,-6 128,-2", sw=4, stroke=P["leaf_dark"]) +
                  "".join(_ell(16 + 24 * i, -5 - (i % 2) * 8, 14, 6, P["leaf"] if i % 2 else P["leaf_dark"], 2.5,
                               extra=f'transform="rotate({-30 + 60 * (i % 2)} {16 + 24 * i} {-5 - (i % 2) * 8})"')
                          for i in range(5)), f"translate({sx},{sy}) rotate({ang})")
    return out


def booth(x, y, scale=1.0, facing=1, shade=False):
    return _place(_booth(shade), x, y, scale, facing)


# Seated-king geometry, measured once from art/characters.king (scale 1, facing right, relative to the king's
# anchor = the floor under him). Hard-coded so that importing props never touches characters' private API.
KING_SEAT_Y = -74          # top of the throne cushion = under the hips of king(pose='sit_throne', throne=False)
KING_ASH_DX = 21.8         # x from king(pose='sit_ashes')'s anchor to the centre of his ash heap
_GOLD = P["crown"]
_GOLD_DARK = S.shade(P["crown"], -0.32)


def _rosette(cx, cy, r, petal=CREAM, heart=None, sw=0.0):
    out = ""
    for j in range(8):
        a = j * math.pi / 4
        out += _circ(cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a), r * 0.36, petal, 0)
    return out + _circ(cx, cy, r * 0.34, heart or _GOLD, sw)


def _lion_leg(x, top, bottom, w=20):
    """Turned gold throne leg ending in a lion's paw (side view, paw pointing toward +x)."""
    out = _p(f"M{_f(x - w / 2)},{_f(top)} Q{_f(x - w * 0.2)},{_f((top + bottom) / 2)} {_f(x - w * 0.38)},{_f(bottom - 22)} "
             f"L{_f(x + w * 0.38)},{_f(bottom - 22)} Q{_f(x + w * 0.2)},{_f((top + bottom) / 2)} {_f(x + w / 2)},{_f(top)} Z",
             _GOLD, 3.5)
    for yy in (top + 14, (top + bottom) / 2):                        # turned rings
        out += _ell(x, yy, w * 0.56, 5, _GOLD_DARK, 3)
    paw = (f"M{_f(x - w * 0.55)},{_f(bottom)} Q{_f(x - w * 0.7)},{_f(bottom - 24)} {_f(x - w * 0.1)},{_f(bottom - 26)} "
           f"Q{_f(x + w * 0.9)},{_f(bottom - 28)} {_f(x + w * 1.25)},{_f(bottom - 8)} Q{_f(x + w * 1.35)},{_f(bottom)} "
           f"{_f(x + w * 1.1)},{_f(bottom)} Z")
    out += _p(paw, _GOLD, 3.5)
    for k in (0.25, 0.65):                                           # toes
        tx = x + w * k
        out += _p(f"M{_f(tx)},{_f(bottom)} Q{_f(tx + 3)},{_f(bottom - 8)} {_f(tx + 1)},{_f(bottom - 13)}", sw=2.4,
                  stroke=_GOLD_DARK)
    return out


def _throne():
    """Assyrian throne in side view, built around king(pose='sit_throne', throne=False) at the same anchor."""
    wood, wd = P["wood"], P["wood_dark"]
    purple, lav = P["royal"], P["royal_light"]
    out = ""
    # footstool in front (the seated king's feet rest at its back edge)
    out += _lion_leg(84, -26, 0, 12) + _lion_leg(132, -26, 0, 12)
    out += _rect(70, -36, 82, 14, wood, 3.5, rx=5) + _line(74, -29, 148, -29, sw=2.5, color=_GOLD)
    out += _p("M72,-36 Q110,-46 150,-36 Z", lav, 3)
    # back legs and stretcher
    out += _lion_leg(-70, -62, 0) + _lion_leg(42, -62, 0)
    out += _rect(-74, -34, 120, 10, wd, 3, rx=4) + _rect(-60, -32, 92, 5, _GOLD, 0, rx=2)
    # tall back: wooden frame, royal purple upholstery with gold studs, attached gold finial
    top = -262
    back = f"M-86,-58 L-86,{top + 30} Q-86,{top} -58,{top} L-36,{top} Q-12,{top} -12,{top + 30} L-12,-58 Z"
    out += _p(back, wood, 4)
    inner = f"M-78,-72 L-78,{top + 34} Q-78,{top + 9} -56,{top + 9} L-38,{top + 9} Q-20,{top + 9} -20,{top + 34} L-20,-72 Z"
    out += _p(inner, purple, 3)
    out += _p(f"M-70,-78 L-70,{top + 40} Q-70,{top + 18} -54,{top + 18}", sw=4, stroke=lav, extra='opacity="0.7"')
    for yy in range(top + 50, -90, 34):
        out += _circ(-49, yy, 4.5, _GOLD, 2)
    out += _rect(-90, top + 52, 82, 18, "#4f86b0", 3, rx=3)           # glazed rosette band across the back
    for cx_ in (-74, -49, -24):
        out += _rosette(cx_, top + 61, 9, "#f4e3b0")
    # finial: a gold pine-cone sitting ON the top rail (no gap)
    fx, fy = -49, top + 2
    out += _p(f"M{fx - 15},{fy} Q{fx - 18},{fy - 22} {fx},{fy - 36} Q{fx + 18},{fy - 22} {fx + 15},{fy} Z", _GOLD, 3.5)
    out += _p(f"M{fx - 10},{fy - 10} L{fx + 10},{fy - 20} M{fx - 10},{fy - 20} L{fx + 10},{fy - 10}", sw=2.2,
              stroke=_GOLD_DARK)
    out += _ell(fx, fy, 19, 6, _GOLD_DARK, 3)
    # seat box with a gold edge, royal cushion on top (its top is KING_SEAT_Y)
    out += _rect(-90, -64, 150, 26, wood, 4, rx=6)
    out += _line(-84, -50, 54, -50, sw=3, color=_GOLD)
    for cx_ in (-62, -22, 18):
        out += _circ(cx_, -50, 4, _GOLD, 2)
    out += _p("M-88,-62 Q-90,-80 -70,-80 L50,-80 Q66,-78 62,-62 Z", purple, 3.5)
    out += _p("M-70,-75 L48,-75", sw=4, stroke=lav, extra='opacity="0.6"')
    out += _circ(62, -66, 5, _GOLD, 2.5)                                 # tassel
    out += _p("M62,-62 L60,-50 M64,-62 L66,-50", sw=2.4, stroke=_GOLD_DARK)
    # armrest (far side, behind the king): a bar with a blue rosette band, carried on a gold post at the front,
    # ending in a little gold lion head
    out += _rect(-14, -150, 14, 80, _GOLD, 3.5, rx=5)                   # rear support
    out += _rect(34, -146, 18, 76, _GOLD, 3.5, rx=6)                    # front post
    out += _ell(43, -112, 11, 5, _GOLD_DARK, 2.5)
    out += _rect(-24, -160, 92, 22, wood, 4, rx=9)
    out += _rect(-18, -156, 72, 14, "#4f86b0", 0, rx=5)
    for cx_ in (-8, 16, 40):
        out += _rosette(cx_, -149, 6.5, "#f4e3b0")
    out += _circ(66, -150, 14, _GOLD, 3.5)
    out += _p("M60,-150 Q66,-160 74,-150", sw=2.2, stroke=_GOLD_DARK)
    out += _circ(70, -152, 2.4, INK, 0)
    return out


def throne(x, y, scale=1.0, facing=1):
    return _place(_throne(), x, y, scale, facing)


def _ash_heap(part="all"):
    """Lumpy mound of ashes centred on x=0: pale ash on top, darker underneath, charcoal lumps, two half-burnt
    sticks, a scattered soft edge. part='back' = the mound, 'front' = the low lip of ash and lumps that lie in
    front of someone sitting in it."""
    pale, mid_, darkash = S.shade(P["ash"], 0.35), P["ash"], S.shade(P["ash"], -0.18)
    coal = S.mix(P["ash"], INK, 0.7)
    rng = random.Random(17)
    back, front = "", ""
    if part in ("all", "back"):
        mound = [(-124, 0), (-114, -18), (-98, -30), (-84, -44), (-66, -48), (-48, -62), (-24, -66), (-6, -76),
                 (16, -72), (36, -64), (54, -56), (70, -50), (90, -38), (110, -24), (124, 0)]
        md = _sm(mound, closed=False, tension=0.85) + " Z"
        inner = _p(_sm([(-130, -6), (-80, -16), (-20, -14), (40, -20), (130, -8), (130, 10), (-130, 10)]), darkash, 0)
        inner += _p(_sm([(-70, -46), (-30, -66), (10, -66), (50, -52), (30, -40), (-20, -44), (-56, -36)]), pale, 0,
                    extra='opacity="0.9"')
        for _ in range(40):                                              # speckled grey grain
            px, py = rng.uniform(-110, 110), rng.uniform(-66, -4)
            inner += _circ(px, py, rng.uniform(1.6, 3.4), rng.choice((pale, darkash, coal)), 0, extra='opacity="0.55"')
        back += _p(md, mid_, 0) + _clip(_uid("ashm", 0), md, inner) + _p(md, sw=4)
        # two half-burnt sticks poking out of the heap, charred black at the buried end, an ember at one tip
        for (x0, y0, x1, y1) in ((-64, -30, -112, -70), (52, -36, 104, -66)):
            back += _tube(f"M{x0},{y0} L{x1},{y1}", 10, P["wood"], 3.2)
            back += _tube(f"M{x0},{y0} L{_f(_lerp(x0, x1, 0.45))},{_f(_lerp(y0, y1, 0.45))}", 10, coal, 3.2)
        back += _circ(-112, -70, 4, P["sun_hot"], 2.2) + _circ(-112, -70, 1.8, P["glow"], 0)
        for cx_, cy_, r_ in ((-30, -52, 9), (16, -60, 7), (-74, -18, 8), (70, -22, 9), (32, -30, 6), (-6, -24, 7)):
            back += _p(S.blob(cx_, cy_, r_ * 1.25, r_, 0.25, 7, int(cx_ * 7 + cy_)), coal, 2.8)
    if part in ("all", "front"):
        lip = [(-150, 2), (-128, -10), (-90, -14), (-40, -12), (10, -15), (60, -12), (110, -14), (146, -6), (156, 2)]
        front += _p(_sm(lip, closed=False, tension=0.8) + " Z", pale, 3.5)
        for cx_, cy_, r_ in ((-104, -5, 6), (-20, -6, 5), (88, -6, 6), (130, -4, 4)):
            front += _p(S.blob(cx_, cy_, r_ * 1.3, r_, 0.25, 7, int(cx_ * 3)), coal, 2.4)
        for _ in range(14):                                              # scattered soft edge
            px = rng.choice((-1, 1)) * rng.uniform(150, 182)
            front += _circ(px, rng.uniform(-6, 0), rng.uniform(2, 4), mid_, 0, extra='opacity="0.7"')
    return back + front


def _ash_smoke(phase=0.0):
    """Two or three soft translucent curls of smoke rising from the heap (y -60 .. -230)."""
    c = S.mix(P["ash"], P["storm_cloud_light"], 0.3)
    out = ""
    for x0, h, ph, op in ((-34, 170, 0.0, 0.8), (26, 136, 1.8, 0.7), (-2, 110, 3.3, 0.6)):
        for k in range(7):
            u = k / 6
            px = x0 + 22 * math.sin(ph + phase + u * 3.2) * u
            py = -60 - h * u
            r = 10 + 16 * u
            out += _circ(px, py, r, c, 0, extra=f'opacity="{op * (1 - 0.75 * u):.2f}" filter="url(#soft)"')
        pts = [(x0 + 22 * math.sin(ph + phase + k / 6 * 3.2) * k / 6, -60 - h * k / 6) for k in range(7)]
        out += _p(_sm(pts, closed=False), sw=3, stroke=c, extra=f'opacity="{op * 0.8:.2f}"')
    return out


def ash_pile(x, y, scale=1.0, smoke=False, facing=1, part="all"):
    body = (_ash_smoke() if smoke and part != "front" else "") + _ash_heap(part)
    return _place(body, x, y, scale, facing)


# ====================================================================== 4. plants


def _palmate(cx, cy, r, lobes, spin, tilt, hang, fill, vein, wither=0.0, seed=0, sw=4.0):
    """Peltate palm-shaped leaf (castor) attached at (cx, cy). Geometry is transformed in python so the ink
    stays even. Withering has two phases so the same leaf stays recognisable through a flipbook:
    0 .. 0.7  the blade keeps its 7-9 pointed lobes but swings down on the petiole (it ends up hanging below
              the stalk tip, seen face-on) while the lobe tips cup and curl in toward the centre;
    0.7 .. 1  the blade shrinks and crumples: the fan closes downward into a limp, wrinkled 'hand'."""
    rng = random.Random(seed)
    w = _clamp(wither)
    da = _smooth(w / 0.7)                       # phase A: droop + curl
    db = _smooth((w - 0.7) / 0.3)               # phase B: shrink + crumple
    comp = 1 - 0.14 * da - 0.3 * db             # the top lobes swing down, then the fan half-closes
    spin_e = math.radians(spin * (1 - da))
    tilt_e = tilt + (0.9 - tilt) * da           # a hanging blade is seen face-on
    hang_e = math.radians(hang * (1 - da))
    size = 1 - 0.06 * da - 0.2 * db
    ca, sa = math.cos(hang_e), math.sin(hang_e)
    oy = r * size * (0.5 * da + 0.12 * db)      # blade centre slides below the stalk tip as it hangs

    def tf(px, py):
        qx, qy = px * math.cos(spin_e) - py * math.sin(spin_e), px * math.sin(spin_e) + py * math.cos(spin_e)
        qy *= tilt_e
        return (cx + qx * ca - qy * sa, cy + oy + qx * sa + qy * ca)

    n = lobes
    hw = math.pi / n * comp
    rs = r * size * (0.34 + 0.06 * w)
    d = ""
    tips = []
    for i in range(n):
        rel = 2 * math.pi * (i - (n - 1) / 2) / n
        a = math.pi / 2 + rel * comp + rng.uniform(-0.04, 0.04) + db * rng.uniform(-0.12, 0.12)
        lob = _lerp(0.72 - 0.28 * math.cos(rel), 0.86 - 0.1 * abs(rel) / math.pi, db)
        rt = r * size * lob * rng.uniform(0.93, 1.05) * (1 - 0.14 * da) * (1 + db * rng.uniform(-0.12, 0.08))
        bw = hw * (0.82 - 0.1 * da + 0.06 * db)
        s0 = (rs * math.cos(a - hw), rs * math.sin(a - hw))
        s1 = (rs * math.cos(a + hw), rs * math.sin(a + hw))
        cup = 0.86 + 0.1 * da                    # cupped sides: the tip sits inside the lobe's curve
        c0 = (rt * cup * math.cos(a - bw), rt * cup * math.sin(a - bw))
        c1 = (rt * cup * math.cos(a + bw), rt * cup * math.sin(a + bw))
        curl = (0.22 * da + 0.1 * db) * rng.uniform(0.6, 1.2) * (-1 if rel >= 0 else 1)   # hook toward the middle
        t = (rt * math.cos(a + curl), rt * math.sin(a + curl))
        tips.append((a, rt))
        P0, C0, T, C1, P1 = tf(*s0), tf(*c0), tf(*t), tf(*c1), tf(*s1)
        if i == 0:
            d += f"M{_f(P0[0])},{_f(P0[1])}"
        d += (f" Q{_f(C0[0])},{_f(C0[1])} {_f(T[0])},{_f(T[1])}"
              f" Q{_f(C1[0])},{_f(C1[1])} {_f(P1[0])},{_f(P1[1])}")
    hub = tf(0, -rs * (0.5 + 0.5 * da))      # the sinus where the petiole meets the blade
    d += f" L{_f(hub[0])},{_f(hub[1])} Z"
    under = (f'<path d="{d}" fill="{S.shade(fill, -0.3)}" '
             f'transform="translate({_f(2 - 2 * da)},{_f(5 + 3 * tilt_e)})"/>')
    vein_c = S.mix(vein, S.shade(fill, -0.28), w)
    inner = ""
    c = tf(0, 0)
    for a, rt in tips:
        e = tf(rt * 0.78 * math.cos(a), rt * 0.78 * math.sin(a))
        inner += _line(c[0], c[1], e[0], e[1], sw=sw * 0.7, color=vein_c, extra='opacity="0.85"')
    if da > 0.05:                                 # the cupped lobe edges catch a darker fold
        for a, rt in tips:
            e0 = tf(rt * 0.45 * math.cos(a - hw * 0.5), rt * 0.45 * math.sin(a - hw * 0.5))
            e1 = tf(rt * 0.85 * math.cos(a - hw * 0.25), rt * 0.85 * math.sin(a - hw * 0.25))
            inner += _line(e0[0], e0[1], e1[0], e1[1], sw=sw * 0.8, color=S.shade(fill, -0.3),
                           extra=f'opacity="{0.5 * da:.2f}"')
    if w > 0.25:
        spot = S.shade(P["leaf_dead"], -0.25)
        for k in range(int(2 + 7 * w)):
            a, rt = tips[rng.randrange(n)]
            rr = rng.uniform(0.35, 0.8) * rt
            spt = tf(rr * math.cos(a), rr * math.sin(a))
            inner += _ell(spt[0], spt[1], 4 + 6 * w, 3 + 3 * w, spot, 0, extra=f'opacity="{0.25 + 0.45 * w:.2f}"')
    cid = _uid("leaf", round(cx, 1), round(cy, 1), round(r, 1), seed, round(w, 3))
    out = under + _p(d, fill, 0) + _clip(cid, d, inner) + _p(d, sw=sw)
    out += _circ(hub[0], hub[1], 3 + r * 0.03, vein_c, 0)
    return out


def _leaf_col(w, base=None):
    base = base or P["leaf"]
    if w <= 0.7:
        return S.mix(base, P["leaf_dry"], _smooth(w / 0.7) * 0.85 + 0.15 * w / 0.7)
    return S.mix(P["leaf_dry"], P["leaf_dead"], (w - 0.7) / 0.3)


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
    # a giant herb, not a tree: green stem with a red-purple flush (castor stems are glossy and reddish)
    stem_c = S.mix(S.mix(P["leaf_dark"], P["leaf"], 0.25), brown, w * 0.8)
    flush_c = S.mix("#a3405a", brown, w * 0.6)
    pet_c = S.mix(S.mix(P["leaf_dark"], "#b8484f", 0.55), brown, w * 0.8)
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
    fl = [(p[0] - nx * h * 0.8, p[1] - ny * h * 0.8) for p, (nx, ny), h in
          ((stem_pt(j / N), normal(j / N), hw(j / N)) for j in range(0, N + 1))]
    stem += _clip(_uid("stemfl", g, w, b, sd), stem_d, _p(_sm(fl, closed=False), sw=base_w * 0.75, stroke=flush_c,
                                                           extra='opacity="0.6"'))      # red-purple flush
    hl = [(p[0] + nx * h * 0.4, p[1] + ny * h * 0.4) for p, (nx, ny), h in
          ((stem_pt(j / N), normal(j / N), hw(j / N)) for j in range(1, N))]
    stem += _p(_sm(hl, closed=False), sw=max(2, base_w * 0.32), stroke=S.shade(stem_c, 0.42),
               extra='opacity="0.75"')                                     # glossy highlight
    ring = S.mix(P["leaf_light"], "#f1e3c8", 0.5)
    for f in (0.26, 0.38, 0.5, 0.6, 0.68, 0.8, 0.92):                       # pale node rings, not bark
        if f * Hs > 20:
            p = stem_pt(f)
            nx, ny = normal(f)
            h = hw(f) * 1.05
            a_, b_ = (p[0] + nx * h, p[1] + ny * h), (p[0] - nx * h, p[1] - ny * h)
            stem += _p(f"M{_f(a_[0])},{_f(a_[1])} Q{_f(p[0] - ny * 5)},{_f(p[1] + nx * 5 + 4)} {_f(b_[0])},{_f(b_[1])}",
                       sw=3.2, stroke=ring, extra='opacity="0.85"')
    stem += _p(stem_d, sw=3.5 + g)
    # bite notch: one concave scallop with little tooth nicks, pale pith along the cut
    if b > 0.01:
        fb = min(16.0, Hs * 0.45) / Hs
        p = stem_pt(fb)
        nx, ny = normal(fb)
        e = (p[0] - sd * abs(nx) * hw(fb) * 1.05, p[1])
        rb = hw(fb) * (0.3 + 1.2 * b)            # at bite=1 the notch reaches ~3/4 through the stem
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
    plant = back_l + branch + stem + cot + front_l + seeds
    if b > 0.01:      # the gnawed stem leans a little away from the notch (toward the canopy)
        plant = _g(plant, f"rotate({sd * 3.5 * _smooth(b):.2f} 0 -4)")
    return mound + plant


def castor_plant(x, y, scale=1.0, growth=1.0, wither=0.0, bite=0.0, side=1, seed=0):
    return _place(_castor(growth, wither, bite, side, seed), x, y, scale)


def _frond(base, ang, length, droop, width, col, seed=0, lite=False):
    """Simple palm frond: a tapered, arching feather with a soft comb of rounded leaflet tips (used for distant
    palms and roof shades; lite=True drops the leaflet lines and most points for far backgrounds)."""
    a = math.radians(ang)
    end = (base[0] + math.cos(a) * length, base[1] + math.sin(a) * length + droop)
    ctrl = (base[0] + math.cos(a) * length * 0.6, base[1] + math.sin(a) * length * 0.6 - droop * 0.25)

    def at(t):
        u = 1 - t
        return (u * u * base[0] + 2 * u * t * ctrl[0] + t * t * end[0], u * u * base[1] + 2 * u * t * ctrl[1] + t * t * end[1])

    N = 14 if lite else 40
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
    if lite:
        out = _p(d, col, 3.2)
    else:
        out = _p(d, col, 0) + _clip(_uid("frond", round(base[0], 1), round(base[1], 1), ang, length, col), d, inner)
        out += _p(d, sw=3.2)
    out += _p(f"M{_f(base[0])},{_f(base[1])} Q{_f(ctrl[0])},{_f(ctrl[1])} {_f(end[0])},{_f(end[1])}", sw=3,
              stroke=S.shade(col, -0.38))
    return out


def _pinnate(base, ang, length, droop, width, col, n=12, sw=2.6):
    """Date-palm frond: a drooping central rib with a comb of narrow pointed leaflets on both sides, angled toward
    the tip and hanging a little with gravity (one filled outline, so the ink stays clean)."""
    a = math.radians(ang)
    end = (base[0] + math.cos(a) * length, base[1] + math.sin(a) * length + droop)
    ctrl = (base[0] + math.cos(a) * length * 0.62, base[1] + math.sin(a) * length * 0.62 - droop * 0.3)

    def at(t):
        u = 1 - t
        return (u * u * base[0] + 2 * u * t * ctrl[0] + t * t * end[0], u * u * base[1] + 2 * u * t * ctrl[1] + t * t * end[1])

    def frame(t):
        p, q = at(max(0, t - 0.01)), at(min(1, t + 0.01))
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy) or 1
        return (dx / ln, dy / ln), (-dy / ln, dx / ln)
    sides = []
    for s in (1, -1):
        pts = []
        for i in range(n):
            t0 = 0.1 + 0.86 * i / n
            t1 = 0.1 + 0.86 * (i + 0.8) / n
            r0, r1 = at(t0), at(t1)
            (tx, ty), (nx, ny) = frame(t0)
            L = width * (0.45 + 0.55 * math.sin(math.pi * min(1.0, (t0 - 0.05) * 1.08)) ** 0.7)
            dx, dy = tx * 0.62 + s * nx * 0.78, ty * 0.62 + s * ny * 0.78 + 0.3     # forward, out, a little down
            dl = math.hypot(dx, dy) or 1
            tip = (r0[0] + dx / dl * L, r0[1] + dy / dl * L)
            bulge = 6.5
            c0 = ((r0[0] + tip[0]) / 2 - tx * bulge, (r0[1] + tip[1]) / 2 - ty * bulge)
            c1 = ((r1[0] + tip[0]) / 2 + tx * bulge, (r1[1] + tip[1]) / 2 + ty * bulge)
            pts.append((r0, c0, tip, c1, r1))
        sides.append(pts)
    tipp = at(1.0)
    d = f"M{_f(base[0])},{_f(base[1])}"
    for r0, c0, tip, c1, r1 in sides[0]:
        d += f" L{_f(r0[0])},{_f(r0[1])} Q{_f(c0[0])},{_f(c0[1])} {_f(tip[0])},{_f(tip[1])} Q{_f(c1[0])},{_f(c1[1])} {_f(r1[0])},{_f(r1[1])}"
    d += f" L{_f(tipp[0])},{_f(tipp[1])}"
    for r0, c0, tip, c1, r1 in reversed(sides[1]):
        d += f" L{_f(r1[0])},{_f(r1[1])} Q{_f(c1[0])},{_f(c1[1])} {_f(tip[0])},{_f(tip[1])} Q{_f(c0[0])},{_f(c0[1])} {_f(r0[0])},{_f(r0[1])}"
    d += " Z"
    out = _p(d, col, sw)
    out += _p(f"M{_f(base[0])},{_f(base[1])} Q{_f(ctrl[0])},{_f(ctrl[1])} {_f(end[0])},{_f(end[1])}", sw=sw * 1.1,
              stroke=S.shade(col, -0.4))
    return out


def _palm(lean=0.0, sway=0.0, dates=True, detail=True):
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
    fr = ((lambda b, a_, l_, d_, w_, c_: _pinnate(b, a_, l_, d_, w_ * 1.25, c_)) if detail else
          (lambda b, a_, l_, d_, w_, c_: _frond(b, a_, l_, d_, w_, c_, lite=True)))
    for ang, ln, dr in ((-150, 200, 70), (-110, 190, 40), (-70, 195, 40), (-30, 200, 70)):
        out += fr(top, ang + sw_, ln, dr, 30, S.mix(P["leaf_dark"], P["olive"], 0.3))
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
        out += fr(top, ang + sw_ * (1.4 if abs(ang) > 90 else 1), ln, dr, 34, P["leaf"])
    out += _circ(top[0], top[1] + 4, 14, S.shade(trunk_c, -0.2), 3.5)
    return out


def palm_tree(x, y, scale=1.0, lean=0.0, sway=0.0, dates=True):
    return _place(_palm(lean, sway, dates), x, y, scale)


def _cluster(circles, fill, sw=4.0):
    a = "".join(_circ(cx, cy, r, fill, sw * 2) for cx, cy, r in circles)
    b = "".join(_circ(cx, cy, r, fill, 0) for cx, cy, r in circles)
    return a + b


def _olive(seed=0):
    """Gnarled olive: a twisted trunk that splits into three limbs (with a dark hollow), each carrying its own
    silvery grey-green clump of foliage, with sky showing between the clumps; small dark olives."""
    rng = random.Random(seed)
    bark, bark_d = "#9a8c78", "#6f6252"
    leaf, leaf_d, silver = "#a3b08a", "#7d8c69", "#dfe5c8"
    out = ""
    # limbs (tubes) twisting out of the trunk toward the three clumps
    limbs = [[(-18, -110), (-46, -160), (-92, -196), (-118, -232)], [(4, -116), (8, -180), (-4, -236), (10, -284)],
             [(20, -104), (52, -150), (96, -178), (122, -210)]]
    for pts in limbs:
        out += _band(pts, 30, 14, bark)
    out += _band([(-30, -150), (-52, -186), (-46, -214)], 14, 8, bark, 3.5)                 # a little side twig
    # trunk: two twisted strands with a split / hollow in the middle
    trunk = ("M-44,0 Q-30,-30 -36,-60 Q-44,-96 -20,-120 Q-2,-132 12,-122 Q34,-104 28,-66 Q24,-34 44,0 Z")
    out += _p(trunk, bark, 4)
    out += _p("M2,-44 Q-12,-60 -4,-84 Q10,-74 12,-58 Q12,-48 2,-44 Z", S.shade(bark_d, -0.3), 3.2)       # knot hole
    out += _p("M-34,-6 Q-10,-40 -30,-74 Q-40,-100 -12,-118", sw=3, stroke=bark_d, extra='opacity="0.8"')   # twisted
    out += _p("M30,-6 Q4,-30 22,-64 Q30,-92 6,-120", sw=3, stroke=bark_d, extra='opacity="0.8"')          # strands
    out += _p("M-14,-4 Q10,-24 -6,-40", sw=3, stroke=bark_d, extra='opacity="0.6"')
    out += _p("M-24,-30 Q-20,-60 -26,-90", sw=6, stroke=S.shade(bark, 0.3), extra='opacity="0.5"')
    out += _ell(-50, -2, 16, 6, bark, 3) + _ell(48, -2, 14, 6, bark, 3)                                   # root flare
    # three separate foliage clumps (sky gaps between them)
    clumps = [(-128, -262, 72, 44), (8, -318, 84, 50), (130, -240, 66, 42), (-58, -214, 40, 26)]
    for k, (cx, cy, rx, ry) in enumerate(clumps):
        circles = [(cx + rx * 0.62 * math.cos(a), cy + ry * 0.55 * math.sin(a), ry * rng.uniform(0.55, 0.7))
                   for a in (math.pi * (0.1 + 0.4 * j) for j in range(5))]
        circles += [(cx, cy - ry * 0.15, ry * 0.85), (cx - rx * 0.45, cy + ry * 0.2, ry * 0.6),
                    (cx + rx * 0.45, cy + ry * 0.2, ry * 0.6)]
        out += _cluster(circles, leaf, 4)
        out += _ell(cx, cy + ry * 0.45, rx * 0.8, ry * 0.32, leaf_d, 0, extra='opacity="0.6" filter="url(#soft)"')
        for _ in range(16):                                     # slim silver leaves
            a = rng.uniform(0, 2 * math.pi)
            rr = rng.uniform(0, 1) ** 0.6
            px, py = cx + rx * 0.8 * rr * math.cos(a), cy - 6 + ry * 0.6 * rr * math.sin(a)
            rot = rng.uniform(-50, 50)
            out += _ell(px, py, 9, 3, silver if rng.random() < 0.7 else leaf_d, 0,
                        extra=f'transform="rotate({rot:.0f} {_f(px)} {_f(py)})" opacity="0.9"')
        for _ in range(3):
            px, py = cx + rng.uniform(-rx * 0.6, rx * 0.6), cy + rng.uniform(-ry * 0.3, ry * 0.4)
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


# flap keyframes: wing value -> (screen angle of the span in degrees, 0 = forward, 90 = straight up, 180 = back;
# length factor; apparent breadth of the wing (1 = full chord, small = seen edge-on); upward arch)
_FLAP = [(-1.0, 248, 0.86, 1.0, 0.04), (-0.5, 212, 0.9, 0.78, 0.08), (0.0, 172, 0.86, 0.44, 0.16),
         (0.5, 128, 1.0, 0.9, 0.1), (1.0, 98, 1.0, 1.0, 0.08)]


def _flap(w):
    w = _clamp(w, -1, 1)
    for a, b in zip(_FLAP, _FLAP[1:]):
        if w <= b[0]:
            t = (w - a[0]) / (b[0] - a[0])
            return tuple(_lerp(a[i], b[i], t) for i in range(1, 5))
    return _FLAP[-1][1:]


def _wing(sh, ang, length, col, tip_col=None, round_=False, chord=44.0, breadth=1.0, arch=0.1, uid="w"):
    """Flying bird wing in screen space: root at the shoulder sh, the span pointing at screen angle `ang`
    (degrees, 0 = toward the head, 90 = up, 180 = toward the tail), `breadth` = apparent chord (1 = flat-on,
    ~0.35 = seen nearly edge-on in a glide). Leading edge on the front / top side, scalloped feather tips
    on the trailing edge, optional dark tip (gull)."""
    a = math.radians(ang)
    V = (math.cos(a) * length, -math.sin(a) * length)
    vl = math.hypot(*V) or 1.0
    u = (V[0] / vl, V[1] / vl)
    n = (-u[1], u[0])
    if n[0] - n[1] < 0:                         # the perpendicular toward front / up = leading edge side
        n = (-n[0], -n[1])
    N = 36

    def ctr(t):
        bow = arch * vl * math.sin(math.pi * min(1.0, t))
        return (sh[0] + V[0] * t + n[0] * bow, sh[1] + V[1] * t + n[1] * bow)
    lead, trail = [], []
    for i in range(N + 1):
        t = i / N
        c = ctr(t)
        ch = (chord * (1 - t) ** 0.6 + 8) * breadth
        dep = 0.0
        if t > 0.4 and breadth > 0.5:            # rounded feather tips with small notches
            dep = (7 if round_ else 6) * breadth * abs(math.sin(math.pi * (t - 0.4) / 0.15))
        lead.append((c[0] + n[0] * ch * 0.38, c[1] + n[1] * ch * 0.38))
        trail.append((c[0] - n[0] * (ch * 0.62 + dep), c[1] - n[1] * (ch * 0.62 + dep)))
    tip = ctr(1.05)
    ch0 = (chord + 8) * breadth
    root = (sh[0] - u[0] * ch0 * 0.35 - n[0] * ch0 * 0.12, sh[1] - u[1] * ch0 * 0.35 - n[1] * ch0 * 0.12)
    pts = lead + [tip] + list(reversed(trail)) + [root]        # rounded shoulder, no straight cut at the root
    d = _sm(pts, closed=True, tension=0.75)
    out = _p(d, col, 0)
    k0 = int(N * 0.64)
    if tip_col:
        out += _p(_sm(lead[k0:] + [tip] + list(reversed(trail[k0:])), closed=True, tension=0.75), tip_col, 0)
        for j in (k0 + 4, k0 + 8):               # white mirror spots on the black tip
            q = _lerp2(lead[j], trail[j], 0.45)
            out += _circ(q[0], q[1], 2.6 * breadth + 1, CREAM, 0, extra='opacity="0.85"')
    if breadth > 0.5:
        for f in (0.3, 0.62):                    # two soft feather rows
            row = [_lerp2(lead[j], trail[j], f) for j in range(2, int(N * 0.8), 4)]
            out += _p(_sm(row, closed=False), sw=2.4, stroke=S.shade(col, -0.25), extra='opacity="0.55"')
    else:                                        # edge-on: one highlight along the leading edge
        out += _p(_sm([_lerp2(lead[j], trail[j], 0.3) for j in range(2, N - 4, 4)], closed=False), sw=2.4,
                  stroke=S.shade(col, 0.4), extra='opacity="0.7"')
    return out + _p(d, sw=3.5)


def _bird(kind="gull", wing=0.0, pose="fly"):
    wv = _clamp(wing, -1, 1)
    dove = kind == "dove"
    if dove:
        bodyc, wingc, tipc, beak, feet = "#f6f0e4", "#d9d1e2", None, "#e8a0a0", "#e58f8f"
        hr, wl = 20, 96
        body = [(-48, 2), (-26, -16), (6, -22), (28, -16), (42, 0), (34, 18), (8, 26), (-22, 22), (-44, 12)]
        tail = [(-40, 0), (-64, -6), (-72, 4), (-66, 14), (-40, 12)]
        head = (40, -20)
    else:
        bodyc, wingc, tipc, beak, feet = "#f7f2e7", "#b9c4cb", "#5f6a74", "#f2b84b", "#f09a4a"
        hr, wl = 16, 112
        body = [(-62, 4), (-30, -14), (10, -18), (34, -10), (40, 6), (20, 20), (-20, 18), (-58, 12)]
        tail = [(-50, 0), (-84, -6), (-90, 6), (-84, 14), (-50, 12)]
        head = (42, -16)
    out = ""
    if pose == "stand":
        if dove:
            body = [(-40, -8), (-18, -24), (12, -26), (30, -14), (34, 6), (20, 24), (-12, 24), (-36, 8)]
            tail = [(-32, -4), (-58, 6), (-60, 16), (-52, 20), (-28, 12)]
            head = (34, -30)
        else:
            body = [(-48, -8), (-22, -24), (12, -24), (32, -12), (34, 6), (16, 22), (-16, 22), (-44, 6)]
            tail = [(-40, -4), (-74, 8), (-76, 18), (-66, 22), (-36, 12)]
            head = (36, -26)
        for lx in (-6, 8):
            out += _line(lx, 18, lx + 2, 46, sw=6.5, color=INK) + _line(lx, 18, lx + 2, 46, sw=2.8, color=feet)
            out += _p(f"M{lx - 8},48 L{lx + 2},44 L{lx + 14},48 Z", feet, 2.5)
    sh = (-6, -12 if pose == "fly" else -14)
    if pose == "fly":
        ang, lf, br, arch = _flap(wv)
        # far wing: peeks out as a V above the back when the wings are up, as a thin sliver over the back in a
        # glide and as a short tip below the belly on the down-stroke
        if wv >= 0:
            fang, flen, fsh = ang - 14 - 10 * wv, 0.86 - 0.26 * (1 - wv) ** 3, (sh[0] + 10, sh[1] - 4 - 4 * (1 - wv))
        else:
            fang, flen, fsh = ang + 34 * (-wv), 0.62, (sh[0] + 14, sh[1] + 8)
        far_col = S.shade(wingc, -0.18)
        out += _wing(fsh, fang, wl * lf * flen, far_col, S.shade(tipc, -0.1) if tipc else None, dove, 38,
                     max(0.32, br * 0.9), arch, "f")
    tcol = S.mix(bodyc, wingc, 0.4) if dove else bodyc
    out += _p(_sm(tail, closed=True, tension=0.6), tcol, 3.5)
    if not dove:
        out += _clip(_uid("gtail", pose), _sm(tail, closed=True, tension=0.6), _rect(-100, -20, 22, 50, tipc, 0))
        out += _p(_sm(tail, closed=True, tension=0.6), sw=3.5)
    out += _p(_sm(body, closed=True), bodyc, 3.8)
    if dove:      # plump rosy-cream breast
        bd = _sm(body, closed=True)
        out += _clip(_uid("dbreast", pose), bd, _ell(28, 10, 26, 18, "#f6dcd2", 0, extra='opacity="0.8"'))
        out += _p(bd, sw=3.8)
    out += _circ(head[0], head[1], hr, bodyc, 3.8)
    bx = head[0] + hr - 3
    if dove:
        out += _p(f"M{_f(bx)},{_f(head[1] - 3)} Q{_f(bx + 10)},{_f(head[1] + 1)} {_f(bx + 9)},{_f(head[1] + 4)} "
                  f"L{_f(bx)},{_f(head[1] + 5)} Z", beak, 2.8)
        out += _dot_eye(head[0] + 6, head[1] - 4, 3.8)
        out += _blush(head[0] + 6, head[1] + 7, 5.5, 3.2, 0.6)
    else:
        out += _p(f"M{_f(bx)},{_f(head[1] - 4)} L{_f(bx + 24)},{_f(head[1] + 1)} Q{_f(bx + 22)},{_f(head[1] + 8)} "
                  f"{_f(bx)},{_f(head[1] + 6)} Z", beak, 2.8)
        out += _circ(bx + 17, head[1] + 4, 2.2, "#d9544d", 0)
        out += _dot_eye(head[0] + 5, head[1] - 4, 3.6)
        out += _blush(head[0] + 4, head[1] + 6, 5, 3, 0.55)
    if pose == "fly":
        for lx in ((-36, -28) if not dove else (-24, -16)):     # feet tucked back under the tail
            out += _p(f"M{lx},16 L{lx - 16},22", sw=5, stroke=INK) + _p(f"M{lx},16 L{lx - 16},22", sw=2, stroke=feet)
        out += _wing(sh, ang, wl * lf, wingc, tipc, dove, 44 if not dove else 40, br, arch, "n")
    else:
        if dove:
            fw = [(-12, -16), (18, -16), (24, -2), (0, 12), (-34, 10), (-50, 4)]
        else:
            fw = [(-16, -16), (20, -16), (26, -2), (0, 10), (-40, 10), (-62, 4)]
        out += _p(_sm(fw, closed=True, tension=0.7), wingc, 3.5)
        if not dove:
            out += _clip(_uid("fw", kind), _sm(fw, closed=True, tension=0.7), _rect(-70, -30, 34, 50, tipc, 0))
            out += _p(_sm(fw, closed=True, tension=0.7), sw=3.5)
        out += _p("M-10,-6 Q6,-2 14,-8 M-24,2 Q-6,6 6,2", sw=2.5, stroke=S.shade(wingc, -0.3))
    return out


def gull(x, y, scale=1.0, facing=1, wing=0.0, pose="fly"):
    return _place(_bird("gull", wing, pose), x, y, scale * 0.82, facing)


def dove(x, y, scale=1.0, facing=1, wing=0.0, pose="fly", leaf=False):
    body = _bird("dove", wing, pose)
    if leaf:                  # Genesis 8:11: a freshly plucked olive leaf in its beak (Noah film)
        hx, hy = (34, -30) if pose == "stand" else (40, -20)
        body += _g(_olive_leaf(40, OLIVE_LEAF, 28), f"translate({hx + 22},{hy + 1})")
        body += _circ(hx + 23, hy + 1, 3, P["wood"], 1.8)
    return _place(body, x, y, scale * 0.75, facing)


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


_CAMEL_BACK = [(-122, -206), (-112, -230), (-90, -242), (-64, -246), (-48, -264), (-28, -302), (0, -316), (28, -302),
               (48, -264), (68, -248), (96, -244)]


def _band(center, w0, w1, fill, sw=4.0):
    """Closed smooth shape of varying width (w0 -> w1) around an open centre line (necks, tails)."""
    left, right = [], []
    n = len(center)
    for i, p in enumerate(center):
        q0, q1 = center[max(0, i - 1)], center[min(n - 1, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        w = _lerp(w0, w1, i / max(1, n - 1)) / 2
        left.append((p[0] - dy / ln * w, p[1] + dx / ln * w))
        right.append((p[0] + dy / ln * w, p[1] - dx / ln * w))
    return _p(_sm(left + list(reversed(right)), closed=True, tension=0.8), fill, sw)


def _drape(back, depth, seed=0):
    """Burlap blanket laid over a curved back (e.g. a hump): the top edge follows `back` (left -> right, a little
    above it), the cloth hangs `depth` px down the flank with a sagging, ragged hem and a rope tie."""
    rng = random.Random(seed)
    col, dark = P["sackcloth"], P["sackcloth_dark"]
    top = [(x, y - 5) for x, y in back]
    x0, x1 = top[0][0], top[-1][0]
    ybase = max(y for _, y in back) + depth          # hem line under the lowest back point
    hem = []
    n = 10
    for i in range(n + 1):
        u = i / n
        sag = 12 * math.sin(2 * math.pi * u) ** 2 - 6 * math.sin(math.pi * u) ** 8   # a sag on each flank
        hem.append((_lerp(x1 + 6, x0 - 6, u), ybase + sag + (7 if i % 2 else 0) + rng.uniform(-3, 3)))
    d = _sm(top, closed=False, tension=0.8) + " " + " ".join(f"L{_f(px)},{_f(py)}" for px, py in hem) + " Z"
    inner = ""
    for k in range(-14, 16):                          # weave follows the drape: threads hang straight down
        xx = (x0 + x1) / 2 + k * 9
        inner += _line(xx, min(y for _, y in back) - 20, xx + 3, ybase + 20, sw=1.6, color=dark, extra='opacity="0.35"')
    for j in range(1, 9):
        pts = [(x, y - 5 + j * (ybase - y + 5) / 9) for x, y in back]
        inner += _p(_sm(pts, closed=False), sw=1.6, stroke=dark, extra='opacity="0.3"')
    # fold shadows where the cloth falls off the hump
    inner += _p(_sm([(back[2][0] + 6, back[2][1] + 10), (back[2][0] - 4, ybase - 10)], closed=False), sw=8,
                stroke=S.shade(col, -0.2), extra='opacity="0.45" filter="url(#soft)"')
    inner += _p(_sm([(back[-3][0] - 6, back[-3][1] + 10), (back[-3][0] + 4, ybase - 10)], closed=False), sw=8,
                stroke=S.shade(col, -0.2), extra='opacity="0.45" filter="url(#soft)"')
    px, py = (x0 + x1) / 2 + (x1 - x0) * 0.2, ybase - depth * 0.45
    inner += _rect(px - 11, py - 9, 22, 18, S.shade(col, 0.2), 2, extra=f'transform="rotate(8 {_f(px)} {_f(py)})"')
    inner += _p(f"M{_f(px - 10)},{_f(py - 7)} l4,0 m4,0 l4,0 m4,0 l3,0", sw=1.8, stroke=dark)
    out = _p(d, col, 0) + _clip(_uid("drape", x0, x1, depth, seed), d, inner) + _p(d, sw=3.5)
    # rope girth hanging straight down the flank from the top of the back
    mid = min(back, key=lambda q: q[1])
    rx = mid[0] + 26
    ry = [q[1] for q in back if q[0] >= rx][:1] or [mid[1]]
    rope = f"M{_f(rx)},{_f(ry[0] - 2)} Q{_f(rx + 6)},{_f((ry[0] + ybase) / 2)} {_f(rx + 2)},{_f(ybase + 6)}"
    out += _p(rope, sw=6.5, stroke=INK) + _p(rope, sw=3, stroke=P["wood_light"])
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
        # short sturdy legs, round barrel, short thick neck with a gentle curve, big friendly head
        out += _qleg((-36, -84), -40, 24, 12, coat, hind=True, far=True, hoof="cloven", bend=0.6)
        out += _qleg((50, -84), 56, 22, 12, coat, far=True, hoof="cloven", bend=0.4)
        out += _qleg((-54, -82), -58, 26, 13, coat, hind=True, hoof="cloven", bend=0.6)
        out += _qleg((34, -82), 38, 24, 13, coat, hoof="cloven", bend=0.4)
        out += _p("M-74,-118 Q-96,-138 -86,-152 Q-70,-142 -64,-120 Z", coat, 3.4)          # perky tail
        # short thick neck with a gentle curve (drawn first: its root tucks under the shoulder)
        out += _band([(40, -112), (62, -136), (78, -154), (90, -168)], 58, 44, coat)
        out += _p("M70,-118 Q86,-136 96,-150", sw=3, stroke=S.shade(coat, -0.2), extra='opacity="0.45"')
        bd = [(-84, -100), (-76, -128), (-46, -144), (0, -142), (40, -146), (70, -136), (86, -112), (80, -84),
              (50, -66), (0, -62), (-50, -66), (-80, -80)]
        belly = _p(_sm([(-70, -80), (0, -84), (70, -82), (70, -40), (-70, -40)]), S.shade(coat, 0.25), 0)
        out += _body(bd, coat, _ell(-36, -116, 30, 20, patch, 0) + _ell(22, -132, 18, 10, patch, 0), belly, "goat")
        if sackcloth:
            out += _sackcloth(-60, 50, -142, -84, 12, 2)
        out += _tube("M86,-194 Q74,-228 52,-234 Q36,-236 36,-220", 11, horn, 3.2)
        out += _tube("M100,-196 Q98,-232 78,-246 Q62,-250 60,-234", 11, S.shade(horn, 0.15), 3.2)
        for k in (0.35, 0.6):
            out += _p(f"M{_f(80 - 30 * k)},{_f(-210 - 26 * k)} l6,8", sw=2, stroke=S.shade(horn, -0.35))
        out += _ell(70, -180, 22, 9, coat, 3.4, extra='transform="rotate(24 70 -180)"')             # floppy ear
        out += _ell(68, -179, 12, 4, "#d9b2a2", 0, extra='transform="rotate(24 68 -179)"')
        head = [(80, -192), (100, -202), (120, -196), (132, -176), (136, -156), (126, -144), (106, -144), (90, -156),
                (80, -174)]
        out += _p(_sm(head), coat, 4)
        out += _ell(102, -192, 13, 8, patch, 0, extra='opacity="0.8"')
        out += _p("M122,-146 Q128,-122 116,-112 Q108,-126 108,-144 Z", S.shade(coat, -0.15), 3)      # beard
        out += _dot_eye(110, -176, 4.8) + _blush(118, -160, 6.5, 3.8)
        out += _circ(132, -156, 2.4, INK, 0)
        out += _p("M121,-150 Q126,-146 131,-150", sw=2.4)
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
        light = S.shade(coat, 0.3)
        # legs set in under the barrel (hind pair back, front pair forward), knobbly knees, soft pad feet
        out += _qleg((-62, -190), -66, 40, 15, coat, hind=True, far=True, hoof="pad", knob=1.3, bend=0.5)
        out += _qleg((72, -190), 80, 36, 15, coat, far=True, hoof="pad", knob=1.3, bend=0.35)
        out += _qleg((-80, -188), -84, 42, 16, coat, hind=True, hoof="pad", knob=1.3, bend=0.5)
        out += _qleg((56, -188), 60, 38, 16, coat, hoof="pad", knob=1.3, bend=0.35)
        out += _p("M-118,-222 Q-136,-190 -130,-160", sw=7, stroke=INK) + _p("M-118,-222 Q-136,-190 -130,-160", sw=3,
                                                                             stroke=coat)
        out += _ell(-130, -156, 6, 11, dark, 3)
        # rounded barrel with ONE hump rising from the middle of the back; the back line runs on in front of
        # and behind it
        # neck (drawn first so its root tucks under the shoulder): forward and gently down from the chest, then
        # up into the head
        neck = [(92, -222), (138, -210), (172, -226), (192, -262), (202, -306)]
        out += _band(neck, 50, 34, coat)
        out += _p(_sm([(122, -214), (156, -214), (182, -238)], closed=False), sw=3, stroke=dark, extra='opacity="0.35"')
        # rounded barrel with ONE hump rising from the middle of the back; the back line runs on in front of
        # and behind it
        bd = _CAMEL_BACK + [(118, -230), (128, -202), (116, -174), (70, -158), (0, -154), (-70, -158), (-110, -170),
                            (-128, -184)]
        belly = _p(_sm([(-120, -184), (0, -178), (124, -186), (124, -140), (-120, -140)]), light, 0)
        shine = _p("M-30,-286 Q-10,-306 16,-306", sw=7, stroke=light, extra='opacity="0.75"')
        shine += _p("M-56,-246 Q0,-232 56,-246", sw=3, stroke=dark, extra='opacity="0.3"')
        out += _body(bd, coat, shine, belly, "camel")
        if sackcloth:
            out += _drape(_CAMEL_BACK[1:-1], 50, seed=5)
        # head: round brow, long soft muzzle with a droopy lip, small ear, open dot eye with lashes
        out += _ell(196, -342, 9, 13, coat, 3.2, extra='transform="rotate(-30 196 -342)"')
        out += _ell(197, -341, 4, 7, "#d7a98a", 0, extra='transform="rotate(-30 197 -341)"')
        hd = [(198, -334), (214, -352), (240, -354), (262, -342), (276, -324), (278, -306), (266, -296),
              (240, -298), (214, -304), (200, -316)]
        out += _p(_sm(hd), coat, 4)
        out += _p("M262,-300 Q272,-290 282,-302", S.shade(coat, -0.06), 3)
        out += _p("M266,-322 Q270,-326 274,-322", sw=2.6)
        out += _dot_eye(232, -332, 4.6)
        out += _p("M226,-338 l-4,-6 M231,-340 l-1,-7 M236,-339 l2,-6", sw=2)
        out += _blush(240, -316, 7, 4)
        out += _p("M258,-306 Q264,-302 270,-306", sw=2.4)
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
        out += _door(40, 68, 146) + _window(-50, -150) + _window(10, -320, 30, 40) + _window(70, -320, 30, 40)
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
        # the stair arrives at a small landing in front of an upper-storey door
        out += _p(f"M{x0 - 14},-196 L{x0 + 76},-196 L{x0 + 76},-186 L{x0 - 14},-186 Z", S.shade(col, 0.15), 3)
        out += _g(_door(x0 + 40, 50, 104, S.shade(P["wood"], -0.05)), "translate(0,-196)")
        out += _line(x0 - 12, -196, x0 - 12, -226, sw=3, color=P["wood_dark"])
        out += _line(x0 - 66, -10, x0 - 12, -224, sw=3, color=P["wood_dark"])                   # hand rail
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
                palms += _g(_palm(rng.uniform(-0.3, 0.3), 0, False, detail=False),
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


# ====================================================================== 7. Daniel film (Daniel 6)

LION = {"body": "#e3a95c", "shade": "#c98b45", "belly": "#f3d6a0", "mane": "#b9632d", "mane_hi": "#d4823c",
        "muzzle": "#f8e8c8", "nose": "#a2594b", "ear_in": "#e7a08c", "tuft": "#9a5228"}
LIONESS = {"body": "#e8bb7c", "shade": "#cf9b5c", "belly": "#f6e0b4", "mane": "#d9a464", "mane_hi": "#e8bb7c",
           "muzzle": "#faecd0", "nose": "#a8625a", "ear_in": "#eaa894", "tuft": "#a0602e"}
LION_POSES = ("stand", "walk_a", "walk_b", "sit", "lie", "sleep")
_TONGUE = "#e8857c"


def _lion_paw(cx, cy, col, sw=3.6, rx=29, ry=16, rot=0.0):
    """Big soft round paw (side view) with three toe lines; (cx, cy) = middle of its flat underside."""
    tr = f'transform="rotate({rot:.1f} {_f(cx)} {_f(cy)})"' if rot else ""
    out = _p(f"M{_f(cx - rx)},{_f(cy)} Q{_f(cx - rx)},{_f(cy - 2 * ry)} {_f(cx + rx * 0.2)},{_f(cy - 2 * ry)} "
             f"Q{_f(cx + rx * 1.15)},{_f(cy - 2 * ry)} {_f(cx + rx)},{_f(cy)} Z", col, sw, extra=tr)
    for k in (0.15, 0.5):
        tx = cx + rx * k
        out += _p(f"M{_f(tx)},{_f(cy - 1)} Q{_f(tx + 2)},{_f(cy - ry * 0.6)} {_f(tx - 1)},{_f(cy - ry * 0.95)}", sw=2.4,
                  stroke=S.shade(col, -0.35), extra=tr)
    return out


def _big_cat_leg(top, paw, w0, w1, col, sw=3.8):
    """Tapered round-ended column from the body (top) to the ground point of the paw."""
    (x0, y0), (x1, y1) = top, paw
    y1p = y1 - 12
    d = (f"M{_f(x0 - w0 / 2)},{_f(y0)} Q{_f(x0 - w0 / 2 + (x1 - x0) * 0.3)},{_f((y0 + y1p) / 2)} "
         f"{_f(x1 - w1 / 2)},{_f(y1p)} L{_f(x1 + w1 / 2)},{_f(y1p)} "
         f"Q{_f(x0 + w0 / 2 + (x1 - x0) * 0.6)},{_f((y0 + y1p) / 2)} {_f(x0 + w0 / 2)},{_f(y0)} Z")
    return _p(d, col, sw) + _lion_paw(x1 + 4, y1, col)


def _lion_tail(pts, col, tuft, sw=3.8):
    d = _sm(pts, closed=False)
    out = _tube(d, 13, col, sw)
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    a = math.degrees(math.atan2(by - ay, bx - ax))
    out += _g(_p("M-6,-11 Q12,-20 30,-8 Q40,0 30,8 Q12,20 -6,11 Q2,0 -6,-11 Z", tuft, sw) +
              _p("M6,-6 Q18,-4 26,0 M6,6 Q18,4 26,0", sw=2.2, stroke=S.shade(tuft, -0.3)),
              f"translate({_f(bx)},{_f(by)}) rotate({a:.1f})")
    return out


def _lion_head(cx, cy, mouth=0.0, eyes="open", maned=True, C=None, tilt=0.0, look=(0.0, 0.0)):
    """Round friendly lion face in a slight 3/4 view toward +x; (cx, cy) = centre of the face."""
    C = C or LION
    out = ""
    m = _clamp(mouth)
    if maned:               # scalloped mane: big soft petals around the face, a lighter inner ring
        R = 96
        n = 16
        pts = []
        for i in range(n * 2):
            a = 2 * math.pi * i / (n * 2) - math.pi / 2
            r = R * (1.0 if i % 2 == 0 else 0.86)
            pts.append((cx - 12 + r * math.cos(a), cy + 2 + r * 0.98 * math.sin(a)))
        out += _p(_sm(pts, tension=0.9), C["mane"], 4.2)
        pts = []
        for i in range(n * 2):
            a = 2 * math.pi * (i + 0.5) / (n * 2) - math.pi / 2
            r = 76 * (1.0 if i % 2 == 0 else 0.9)
            pts.append((cx - 6 + r * math.cos(a), cy + 4 + r * 0.98 * math.sin(a)))
        out += _p(_sm(pts, tension=0.9), C["mane_hi"], 0)
        for i in range(10):                  # a few curl strokes in the mane
            a = 2 * math.pi * i / 10 + 0.3
            px, py = cx - 12 + 84 * math.cos(a), cy + 2 + 82 * math.sin(a)
            out += _p(f"M{_f(px - 8 * math.sin(a))},{_f(py + 8 * math.cos(a))} q{_f(6 * math.cos(a))},{_f(6 * math.sin(a))} "
                      f"{_f(16 * math.sin(a))},{_f(-16 * math.cos(a))}", sw=2.4, stroke=S.shade(C["mane"], -0.25))
    # ears
    for ex, ey in ((cx - 38, cy - 50), (cx + 34, cy - 54)):
        out += _circ(ex, ey, 17, C["body"], 3.8) + _circ(ex + 1, ey + 2, 8.5, C["ear_in"], 0)
    # face
    fr = 60 if maned else 56
    face = [(cx - fr * 0.95, cy - 4), (cx - fr * 0.75, cy - fr * 0.72), (cx, cy - fr * 0.98), (cx + fr * 0.8, cy - fr * 0.7),
            (cx + fr * 1.02, cy + 4), (cx + fr * 0.78, cy + fr * 0.72), (cx + 4, cy + fr * 0.96),
            (cx - fr * 0.72, cy + fr * 0.74)]
    out += _p(_sm(face), C["body"], 4)
    if not maned:            # lioness: soft cheek ruff
        for sx in (-1, 1):
            bx = cx + sx * fr * 0.92 + (6 if sx > 0 else 0)
            out += _p(f"M{_f(bx)},{_f(cy - 6)} l{_f(sx * 10)},8 l{_f(-sx * 6)},6 l{_f(sx * 8)},8", sw=2.6,
                      stroke=S.shade(C["body"], -0.3))
    # brows, eyes
    lx, ly = look
    ex0, ex1, ey = cx - 18, cx + 26, cy - 12
    for ex in (ex0, ex1):
        out += _p(f"M{_f(ex - 10)},{_f(ey - 16)} Q{_f(ex)},{_f(ey - 23)} {_f(ex + 10)},{_f(ey - 17)}", sw=3,
                  stroke=S.shade(C["body"], -0.45))
        if eyes == "half":
            out += _p(f"M{_f(ex - 9)},{_f(ey)} L{_f(ex + 9)},{_f(ey)} Q{_f(ex + 8)},{_f(ey + 10)} {_f(ex)},{_f(ey + 10)} "
                      f"Q{_f(ex - 8)},{_f(ey + 10)} {_f(ex - 9)},{_f(ey)} Z", PUPIL, 0)
            out += _p(f"M{_f(ex - 11)},{_f(ey)} L{_f(ex + 11)},{_f(ey)}", sw=3.2)
        else:
            k = {"closed": "closed", "happy": "happy"}.get(eyes, "open")
            if k == "open":
                out += _circ(ex + lx * 4, ey + ly * 4, 10.5, PUPIL, 0) + _circ(ex + lx * 4 - 3.5, ey + ly * 4 - 4, 4, HILITE, 0)
                out += _circ(ex + lx * 4 + 3, ey + ly * 4 + 3, 1.4, HILITE, 0)
            else:
                out += _dot_eye(ex, ey + (3 if k == "closed" else 0), 8, k)
    # muzzle: two puffy cheeks and a chin, the nose on top
    mx, my = cx + 6, cy + 20
    chin_drop = 30 * m
    out += _ell(mx + 2, my + 22 + chin_drop * 0.6, 18, 13 + chin_drop * 0.3, C["muzzle"], 3.4)   # chin
    if m > 0.02:            # open mouth: soft round yawn, pink tongue, two blunt little teeth
        mw, mh = 13 + 9 * m, 6 + 26 * m
        oy = my + 12
        out += _p(f"M{_f(mx + 2 - mw)},{_f(oy)} Q{_f(mx + 2 - mw)},{_f(oy + mh * 1.25)} {_f(mx + 2)},{_f(oy + mh * 1.25)} "
                  f"Q{_f(mx + 2 + mw)},{_f(oy + mh * 1.25)} {_f(mx + 2 + mw)},{_f(oy)} Z", P["mouth_inside"], 3.4)
        out += _ell(mx + 2, oy + mh * 1.0, mw * 0.62, mh * 0.32 + 2, _TONGUE, 0)
        for tx in (mx + 2 - mw * 0.55, mx + 2 + mw * 0.55):
            out += _p(f"M{_f(tx - 4.5)},{_f(oy + 1)} L{_f(tx - 4)},{_f(oy + 4 + 4 * m)} Q{_f(tx)},{_f(oy + 8 + 5 * m)} "
                      f"{_f(tx + 4)},{_f(oy + 4 + 4 * m)} L{_f(tx + 4.5)},{_f(oy + 1)} Z", CREAM, 2.2)
    for sx in (-1, 1):
        out += _ell(mx + sx * 15, my + 4, 18, 14, C["muzzle"], 3.4)
        for k in range(3):
            out += _circ(mx + sx * (11 + k * 6), my + 1 + (k % 2) * 6, 1.6, S.shade(C["muzzle"], -0.45), 0)
    if m <= 0.02:           # closed: a gentle smile under the cheeks
        out += _p(f"M{_f(mx - 12)},{_f(my + 18)} Q{_f(mx)},{_f(my + 24)} {_f(mx + 2)},{_f(my + 15)} "
                  f"Q{_f(mx + 4)},{_f(my + 24)} {_f(mx + 16)},{_f(my + 18)}", sw=2.8)
    out += _p(f"M{_f(mx - 12)},{_f(my - 12)} Q{_f(mx)},{_f(my - 16)} {_f(mx + 12)},{_f(my - 12)} Q{_f(mx + 10)},{_f(my - 2)} "
              f"{_f(mx)},{_f(my + 2)} Q{_f(mx - 10)},{_f(my - 2)} {_f(mx - 12)},{_f(my - 12)} Z", C["nose"], 3)
    out += _ell(mx - 3, my - 11, 4, 2, HILITE, 0, extra='opacity="0.7"')
    out += _blush(cx - 40, cy + 14, 10, 6) + _blush(cx + 52, cy + 12, 9, 6)
    if tilt:
        out = _g(out, f"rotate({tilt:.1f} {_f(cx)} {_f(cy)})")
    return out


def _lion(pose="stand", mouth=0.0, eyes="open", tail=0.0, variant=0):
    if pose not in LION_POSES:
        raise ValueError(f"lion: unknown pose {pose!r}; choose from {LION_POSES}")
    C = LIONESS if variant % 2 else LION
    maned = not (variant % 2)
    col, far = C["body"], S.shade(C["body"], -0.16)
    sl = 0.88 if not maned else 1.0           # the lioness is a little slimmer and lower
    out = ""
    tw = _clamp(tail, -1, 1)
    if pose in ("stand", "walk_a", "walk_b"):
        bx, by = -10, -160 * sl
        hl, hh = 140, 72 * sl
        # leg ground x positions (far hind, far front, near hind, near front)
        fx = {"stand": (-78, 124, -112, 96), "walk_a": (-46, 150, -142, 70), "walk_b": (-116, 94, -78, 130)}[pose]
        lift = {"stand": (0, 0, 0, 0), "walk_a": (0, 0, 8, 0), "walk_b": (0, 10, 0, 0)}[pose]
        tail_pts = [(bx - hl + 8, by - 22), (bx - hl - 42, by - 40 + 8 * tw), (bx - hl - 66, by - 92 - 40 * tw),
                    (bx - hl - 52, by - 130 - 46 * tw)]
        out += _lion_tail(tail_pts, col, C["tuft"])
        out += _big_cat_leg((-84, by + 20), (fx[0], -5 - lift[0]), 50 * sl, 38 * sl, far)
        out += _big_cat_leg((104, by + 20), (fx[1], -5 - lift[1]), 46 * sl, 36 * sl, far)
        out += _big_cat_leg((-104, by + 24), (fx[2], -lift[2]), 58 * sl, 40 * sl, col)
        out += _big_cat_leg((84, by + 24), (fx[3], -lift[3]), 50 * sl, 38 * sl, col)
        body = [(bx - hl, by + 4), (bx - hl + 26, by - hh + 8), (bx - 20, by - hh + 4), (bx + hl - 50, by - hh - 4),
                (bx + hl + 4, by - 10), (bx + hl - 10, by + hh - 6), (bx + hl - 60, by + hh + 4), (bx, by + hh - 10),
                (bx - hl + 40, by + hh - 2)]
        belly = _ell(bx + 10, by + hh - 2, hl * 0.84, hh * 0.40, C["belly"], 0)
        out += _body(body, col, "", belly, f"lion{variant}{pose}")
        out += _p(f"M{_f(bx - hl + 26)},{_f(by - 30)} Q{_f(bx - hl + 80)},{_f(by - 64)} {_f(bx - hl + 104)},{_f(by + 20)}",
                  sw=3, stroke=C["shade"], extra='opacity="0.7"')                                  # haunch line
        out += _p(f"M{_f(bx + hl - 70)},{_f(by - 20)} Q{_f(bx + hl - 92)},{_f(by + 24)} {_f(bx + hl - 82)},{_f(by + hh)}",
                  sw=3, stroke=C["shade"], extra='opacity="0.6"')                                  # shoulder line
        hx, hy = 150, by - 80 + (6 if pose != "stand" else 0)
        out += _lion_head(hx, hy, mouth, eyes, maned, C)
    elif pose == "sit":
        tail_pts = [(-110, -24), (-60, -6), (10, -8), (66, -20 - 20 * tw)]
        out += _big_cat_leg((96, -190 * sl), (112, -5), 40 * sl, 32 * sl, far)                          # far front
        body = [(-130, -40), (-120, -128 * sl), (-60, -196 * sl), (20, -250 * sl), (96, -236 * sl), (118, -150 * sl),
                (96, -60), (40, -8), (-60, -4), (-118, -10)]
        belly = _ell(80, -130 * sl, 34, 90 * sl, C["belly"], 0, extra='transform="rotate(-18 80 -130)"')
        out += _body(body, col, "", belly, f"lion{variant}sit")
        out += _lion_tail(tail_pts, col, C["tuft"])
        out += _ell(-58, -66, 70, 62 * sl, col, 3.8)                                                 # haunch
        out += _p("M-110,-60 Q-90,-118 -40,-124", sw=2.6, stroke=C["shade"], extra='opacity="0.6"')
        out += _lion_paw(-6, 0, col)                                                                 # hind paw
        out += _big_cat_leg((76, -176 * sl), (82, 0), 50 * sl, 36 * sl, col)                            # near front
        out += _ell(76, -176 * sl, 22 * sl, 30 * sl, col, 0)                       # blend the leg into the chest
        out += _p(f"M{_f(56)},{_f(-196 * sl)} Q{_f(48)},{_f(-150 * sl)} {_f(54)},{_f(-104 * sl)}", sw=3,
                  stroke=C["shade"], extra='opacity="0.6"')
        hx, hy = 96, -278 * sl - (0 if maned else 6)
        out += _lion_head(hx, hy, mouth, eyes, maned, C)
    else:  # lie / sleep: lying like a big cat, head resting on the front paws
        sleep = pose == "sleep"
        by = -64 * sl
        if sleep:
            tail_pts = [(-170, -36), (-150, -6), (-40, -2), (60, -10 - 14 * tw)]
        else:
            tail_pts = [(-170, -40), (-220, -26), (-258, -40 - 30 * tw), (-262, -76 - 40 * tw)]
        out += _lion_tail(tail_pts, col, C["tuft"]) if not sleep else ""
        out += _p(_sm([(110, -50), (228, -40), (232, -16), (110, -14)]), far, 3.8)                     # far forearm
        out += _lion_paw(226, -8, far)
        body = [(-180, -30), (-160, by - 52 * sl), (-60, by - 70 * sl), (60, by - 66 * sl), (130, by - 30),
                (140, -22), (100, -2), (-60, -2), (-160, -4)]
        belly = _ell(-10, -14, 150, 24, C["belly"], 0)
        out += _body(body, col, "", belly, f"lion{variant}{pose}")
        out += _ell(-110, -58 * sl, 66, 52 * sl, col, 3.8)                                            # haunch
        out += _p("M-160,-50 Q-130,-104 -70,-100", sw=2.6, stroke=C["shade"], extra='opacity="0.6"')
        out += _lion_paw(-40, 0, col)                                                                 # hind paw
        if sleep:
            out += _lion_tail(tail_pts, col, C["tuft"])
        hx, hy = 186 - (10 if sleep else 0), -96 + (8 if sleep else 0) + (0 if maned else 8)
        out += _lion_head(hx, hy, mouth, "closed" if (sleep and eyes == "open") else eyes, maned, C,
                          tilt=10 if sleep else 0)
        out += _p(_sm([(96, -46), (250, -40), (252, -12), (96, -10)]), col, 3.8)                       # near forearm
        out += _lion_paw(248, 0, col)
    return out


def lion(x, y, scale=1.0, facing=1, pose="stand", mouth=0.0, eyes="open", tail=0.0, variant=0):
    return _place(_lion(pose, mouth, eyes, tail, variant), x, y, scale, facing)


# ---------------------------------------------------------------------- the lions' den
DEN_FLOOR_Y = 600                      # floor surface inside the den (feet of figures inside), cutaway view
DEN_INNER = (-640, 96, 640, 600)       # chamber: x0, ceiling (underside of the ground slab), x1, floor
DEN_OPENING = (-140, 140)              # x-range of the round hole through the ceiling (y 0 .. 96)
DEN_HOLE = (210, 62)                   # view='outside': rx, ry of the pit mouth ellipse centred on the anchor
_EARTH = "#b88e62"
_EARTH_DARK = "#93694a"
_DEN_STONE = "#c7b49a"
_DEN_DARK = "#4a3a34"


def _den_cave():
    """Chamber outline (local, cutaway): flat-ish ceiling with the hole, rounded walls, flat floor."""
    x0, top, x1, fl = DEN_INNER
    o0, o1 = DEN_OPENING
    return (f"M{o0},{top} L{x0 + 120},{top + 8} Q{x0 + 10},{top + 30} {x0},{top + 200} "
            f"Q{x0 - 16},{fl - 120} {x0 + 30},{fl + 40} L{x1 - 30},{fl + 40} Q{x1 + 16},{fl - 120} {x1},{top + 200} "
            f"Q{x1 - 10},{top + 30} {x1 - 120},{top + 8} L{o1},{top} L{o1},{-2} L{o0},{-2} Z")


def _den_back(light=0.0):
    x0, top, x1, fl = DEN_INNER
    o0, o1 = DEN_OPENING
    rng = random.Random(6)
    out = ""
    # earth mass in section: ragged cut edge at the sides and bottom, strata and pebbles
    edge = [(-770, -2), (770, -2)]
    for i in range(13):
        u = i / 12
        edge.append((770 + rng.uniform(-14, 10), _lerp(30, 690, u)))
    for i in range(17):
        u = i / 16
        edge.append((_lerp(770, -770, u), 700 + rng.uniform(-16, 12)))
    for i in range(13):
        u = i / 12
        edge.append((-770 + rng.uniform(-10, 14), _lerp(690, 30, u)))
    ed = _poly(edge)
    gid = _uid("earth")
    inner = ""
    for k, yy in enumerate(range(60, 700, 70)):
        inner += _p(_sm([(-800, yy + rng.uniform(-8, 8)), (-300, yy + 16), (200, yy - 12), (800, yy + 6)], closed=False),
                    sw=3, stroke=S.shade(_EARTH, -0.12 if k % 2 else 0.1), extra='opacity="0.8"')
    for _ in range(46):
        px, py = rng.uniform(-750, 750), rng.uniform(20, 680)
        r = rng.uniform(6, 15)
        inner += _ell(px, py, r * 1.4, r, S.shade(_EARTH, rng.choice((-0.2, 0.18))), 2.5, extra='opacity="0.9"')
    out += (f'<defs>{S.lin_grad(gid, [(0, S.shade(_EARTH, 0.12)), (1, _EARTH_DARK)])}</defs>' +
            _p(ed, f"url(#{gid})", 0) + _clip(_uid("earthc"), ed, inner) + _p(ed, sw=4.5))
    # the chamber: dim, warm, stone-block walls
    cave = _den_cave()
    cg = _uid("cave")
    walls = ""
    yy = top - 14
    while yy < fl + 40:                      # rough courses of rounded field stones, no two alike
        h = rng.uniform(36, 52)
        xx = x0 - 60 - rng.uniform(0, 50)
        while xx < x1 + 60:
            w = rng.uniform(56, 110)
            walls += _p(S.blob(xx + w / 2, yy + h / 2, w / 2 - 3, h / 2 - 3, 0.07, 8, seed=int(xx * 7 + yy)),
                        S.shade(S.mix(_DEN_STONE, P["sand"], 0.25), rng.uniform(-0.14, 0.06)), 2.8,
                        stroke=S.shade(_DEN_DARK, 0.15))
            xx += w + rng.uniform(2, 6)
        yy += h + 3
    shade_d = (f'<defs>{S.lin_grad(cg, [(0, _DEN_DARK, 0.78), (0.55, _DEN_DARK, 0.45), (1, _DEN_DARK, 0.2)])}</defs>'
               f'<rect x="{x0 - 40}" y="{-10}" width="{x1 - x0 + 80}" height="{fl + 60}" fill="url(#{cg})"/>')
    walls += shade_d
    # floor: sandy earth with scattered straw
    floor = _p(f"M{x0 - 40},{fl - 6} Q0,{fl - 18} {x1 + 40},{fl - 6} L{x1 + 40},{fl + 60} L{x0 - 40},{fl + 60} Z",
               S.mix(P["sand_dark"], _DEN_DARK, 0.25), 0)
    for _ in range(40):
        px = rng.uniform(x0 + 20, x1 - 20)
        py = fl + rng.uniform(-4, 30)
        a = rng.uniform(-0.5, 0.5)
        floor += _line(px, py, px + 26 * math.cos(a), py + 26 * math.sin(a), sw=3,
                       color=S.mix(P["leaf_dry"], P["sand"], rng.uniform(0, 0.5)), extra='opacity="0.85"')
    walls += floor
    walls += _p(f"M{x0 - 40},{fl - 6} Q0,{fl - 18} {x1 + 40},{fl - 6}", sw=3, stroke=S.shade(_DEN_DARK, 0.2))
    if light > 0:           # sunlight / moonlight falling through the hole onto the floor
        lg = _uid("denlight", light)
        walls += (f'<defs>{S.lin_grad(lg, [(0, P["glow"], 0.75 * light), (1, P["glow"], 0.15 * light)])}</defs>'
                  f'<path d="M{o0 + 10},{top} L{o1 - 10},{top} L{o1 + 120},{fl + 10} L{o0 - 120},{fl + 10} Z" '
                  f'fill="url(#{lg})"/>'
                  f'<ellipse cx="0" cy="{fl + 8}" rx="{(o1 - o0) / 2 + 130}" ry="34" fill="{P["glow"]}" '
                  f'opacity="{0.45 * light:.2f}" filter="url(#soft)"/>')
    out += _p(cave, _DEN_DARK, 0) + _clip(_uid("cavec"), cave, walls)
    # the round shaft through the ceiling: its far wall is curved stonework
    shaft = f"M{o0},-2 L{o1},-2 L{o1},{top} L{o0},{top} Z"
    sh = ""
    for r_, yy in enumerate(range(-4, top, 32)):
        for k, xx in enumerate(range(o0 - 20 + (24 if r_ % 2 else 0), o1 + 20, 56)):
            sh += _rect(xx, yy + 2, 50, 28, S.shade(_DEN_STONE, -0.18 - 0.1 * (yy / top)), 2.4, rx=9)
    out += _clip(_uid("shaft"), shaft, sh + f'<rect x="{o0}" y="-2" width="{o1 - o0}" height="{top + 4}" '
                 f'fill="{_DEN_DARK}" opacity="0.35"/>')
    out += _p(cave, sw=5)
    # the cut ground slab around the hole: a lip of stones at the mouth (left and right halves)
    for sx in (-1, 1):
        for k in range(3):
            cx = sx * (152 + k * 34)
            out += _ell(cx, -8 - (2 - k) * 2, 22, 13, S.shade(_DEN_STONE, -0.05 * k), 3.5)
    return out


def _den_front():
    x0, _top, x1, fl = DEN_INNER
    rng = random.Random(9)
    out = ""
    # foreground rocks and straw along the floor's front edge, a few rocks at the chamber's corners
    for cx, cy, rx, ry in ((x0 + 60, fl + 22, 66, 40), (x0 + 150, fl + 34, 40, 24), (x1 - 70, fl + 20, 70, 44),
                           (x1 - 170, fl + 34, 36, 22), (-260, fl + 40, 30, 18), (300, fl + 42, 26, 16)):
        out += _p(S.blob(cx, cy, rx, ry, 0.12, 9, seed=int(cx)), S.shade(_DEN_STONE, -0.2), 4)
        out += _p(f"M{_f(cx - rx * 0.5)},{_f(cy - ry * 0.45)} Q{_f(cx)},{_f(cy - ry * 0.8)} {_f(cx + rx * 0.45)},"
                  f"{_f(cy - ry * 0.5)}", sw=3, stroke=S.shade(_DEN_STONE, 0.15))
    for _ in range(16):
        px = rng.uniform(x0 + 60, x1 - 60)
        py = fl + 44
        for j in range(4):
            a = -math.pi / 2 + rng.uniform(-0.9, 0.9)
            ln = rng.uniform(16, 30)
            out += _line(px, py, px + ln * math.cos(a), py + ln * math.sin(a), sw=3.2,
                         color=S.mix(P["leaf_dry"], P["sand"], rng.uniform(0, 0.4)))
    # the cut ends of the ground slab beside the hole (front face of the section), with grass tufts on top
    for sx in (-1, 1):
        out += _g(_grass(1), f"translate({sx * 300},0) scale(0.7)")
        out += _g(_grass(0), f"translate({sx * 560},0) scale(0.6)")
    return out


def _den_outside():
    """The pit mouth seen from ground level and a little above: a ring of stones round a dark hole."""
    rx, ry = DEN_HOLE
    back, front = "", ""
    hg = _uid("hole")
    back += (f'<defs>{S.rad_grad(hg, [(0, "#20160f"), (0.7, _DEN_DARK), (1, S.shade(_DEN_DARK, 0.2))], cy=0.7)}</defs>'
             f'<ellipse cx="0" cy="0" rx="{rx}" ry="{ry}" fill="url(#{hg})" stroke="{INK}" stroke-width="4"/>')
    back += _p(f"M{-rx + 14},{-6} Q0,{-ry + 2} {rx - 14},{-6} L{rx - 30},{12} Q0,{-ry + 30} {-rx + 30},{12} Z",
               S.shade(_DEN_STONE, -0.35), 0, extra='opacity="0.85"')
    n = 18
    for i in range(n):
        a = 2 * math.pi * (i + 0.5) / n
        cx, cy = (rx + 26) * math.cos(a), (ry + 16) * math.sin(a)
        stone = _ell(cx, cy, 34, 20, S.shade(_DEN_STONE, -0.06 * (i % 3)), 3.5)
        stone += _p(f"M{_f(cx - 18)},{_f(cy - 9)} Q{_f(cx)},{_f(cy - 16)} {_f(cx + 16)},{_f(cy - 9)}", sw=2.5,
                    stroke=S.shade(_DEN_STONE, 0.18))
        if math.sin(a) < 0:
            back += stone
        else:
            front += stone
    return back, front


def lion_den(x, y, scale=1.0, part="all", view="cutaway", light=0.0):
    if part not in ("all", "back", "front"):
        raise ValueError(f"lion_den: part must be 'all', 'back' or 'front', not {part!r}")
    if view == "outside":
        b, f = _den_outside()
    elif view == "cutaway":
        b = _den_back(light) if part != "front" else ""
        f = _den_front() if part != "back" else ""
    else:
        raise ValueError(f"lion_den: view must be 'cutaway' or 'outside', not {view!r}")
    body = (b if part != "front" else "") + (f if part != "back" else "")
    return _place(body, x, y, scale, 1, filt="wobble")


def in_den_hole(markup, x, y, scale=1.0):
    """Clip figure markup to what shows above the near rim of lion_den(view='outside') at (x, y, scale):
    everything above the ground line plus the dark hole (e.g. Daniel being lowered in)."""
    rx, ry = DEN_HOLE[0] * scale, DEN_HOLE[1] * scale
    d = (f"M{_f(x - 4000)},{_f(y - 4000)} L{_f(x + 4000)},{_f(y - 4000)} L{_f(x + 4000)},{_f(y)} L{_f(x + rx)},{_f(y)} "
         f"A{_f(rx)},{_f(ry)} 0 0 1 {_f(x - rx)},{_f(y)} L{_f(x - 4000)},{_f(y)} Z")
    cid = _uid("denhole", x, y, scale)
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{markup}</g>'


DEN_STONE_R = (170, 128)               # den_stone: half-width and half-height of the boulder


def _den_stone(sealed=False, roll=0.0):
    rx, ry = DEN_STONE_R
    col = "#bdb2a2"
    out = ""
    pts = []
    rng = random.Random(3)
    for i in range(14):
        a = 2 * math.pi * i / 14
        k = 1 + rng.uniform(-0.035, 0.035)
        pts.append((rx * k * math.cos(a), -ry + ry * k * math.sin(a)))
    d = _sm(pts)
    gid = _uid("stoneg")
    inner = (f'<defs>{S.rad_grad(gid, [(0, S.shade(col, 0.25)), (0.6, col), (1, S.shade(col, -0.22))], cx=0.38, cy=0.3, r=0.75)}</defs>'
             f'<rect x="{-rx - 10}" y="{-2 * ry - 10}" width="{2 * rx + 20}" height="{2 * ry + 20}" fill="url(#{gid})"/>')
    tex = ""
    for (x0, y0, x1, y1, x2, y2) in ((-90, -40, -40, -70, -10, -50), (40, -190, 70, -150, 110, -160),
                                     (-120, -170, -100, -140, -70, -150), (60, -60, 90, -80, 130, -70)):
        tex += _p(f"M{x0},{y0} Q{x1},{y1} {x2},{y2}", sw=3, stroke=S.shade(col, -0.3))
    for cx, cy, r in ((-60, -110, 14), (90, -110, 10), (10, -200, 9), (-120, -80, 8)):
        tex += _ell(cx, cy, r * 1.3, r, S.shade(col, -0.12), 0, extra='opacity="0.8"')
    for cx, cy in ((-130, -40), (120, -36), (-30, -18)):
        tex += _ell(cx, cy, 22, 9, P["olive"], 0, extra='opacity="0.55"')                          # moss
    if roll:
        tex = _g(tex, f"rotate({roll:.1f} 0 {-ry})")
    inner += tex
    out += _p(d, col, 0) + _clip(_uid("stonec", roll), d, inner) + _p(d, sw=4.5)
    out += _p(f"M{-rx * 0.55},{-ry * 1.62} Q{-rx * 0.2},{-ry * 1.9} {rx * 0.2},{-ry * 1.78}", sw=6,
              stroke=S.shade(col, 0.35), extra='opacity="0.7"')
    if sealed:              # the king's seal: a cord across the stone pegged to the ground, a clay seal on it
        for sx in (-1, 1):
            px = sx * (rx + 34)
            out += _p(f"M{px - 6},2 L{px - 5},-34 Q{px},-42 {px + 5},-34 L{px + 6},2 Z", P["wood"], 3)
        cord = f"M{-rx - 34},-30 Q{-rx * 0.9},{-ry * 1.25} 0,{-ry - 10} Q{rx * 0.9},{-ry * 1.25} {rx + 34},-30"
        out += _p(cord, sw=8, stroke=INK) + _p(cord, sw=4, stroke="#d8b878")
        out += _royal_impression(0, -ry - 10, 1.0)
    return out


def _royal_impression(cx, cy, k=1.0):
    """Lump of clay pressed with the king's signet: a rosette with a little crown above it."""
    clay = P["terracotta"]
    out = _p(S.blob(cx, cy, 34 * k, 30 * k, 0.08, 9, seed=4), clay, 4 * k)
    out += _circ(cx, cy, 22 * k, S.shade(clay, -0.12), 2.6 * k)
    for j in range(8):
        a = j * math.pi / 4
        out += _ell(cx + 11 * k * math.cos(a), cy + 11 * k * math.sin(a), 5 * k, 3.2 * k, S.shade(clay, -0.32), 0,
                    extra=f'transform="rotate({j * 45} {_f(cx + 11 * k * math.cos(a))} {_f(cy + 11 * k * math.sin(a))})"')
    out += _circ(cx, cy, 4.5 * k, S.shade(clay, -0.4), 0)
    out += _ell(cx - 14 * k, cy - 16 * k, 8 * k, 4 * k, S.shade(clay, 0.3), 0, extra='opacity="0.7"')
    return out


def den_stone(x, y, scale=1.0, sealed=False, roll=0.0):
    return _place(_den_stone(sealed, roll), x, y, scale, 1)


# ---------------------------------------------------------------------- Daniel's upstairs window
WINDOW_OPENING = (-95, -262, 95, 0)    # the opening (x0, top, x1, sill top) relative to the anchor
WINDOW_FLOOR_Y = 90                    # suggested floor inside: a kneeling Daniel there shows head and chest
WINDOW_WALL = (-300, -470, 300, 200)   # extent of the wall patch drawn with wall=True
SHUTTER = "#5f9a92"


def _shutter(sx, op, col=SHUTTER):
    """One shutter hinged at x = sx*95; op 0 closed (covering half the opening) .. 1 swung flat on the wall."""
    _x0, top, _x1, sill = WINDOW_OPENING
    hx = sx * 95
    th = math.pi * _clamp(op)
    fx = hx - sx * (95 * math.cos(th) + 16 * math.sin(th))     # + the panel's thickness when edge-on
    e = 18 * math.sin(th)                   # the free edge comes toward the viewer and looks a little bigger
    pts = [(hx, top + 2), (fx, top + 2 - e), (fx, sill - 2 + e * 0.7), (hx, sill - 2)]
    face = col if th <= math.pi / 2 else S.shade(col, -0.12)
    out = _p(_poly(pts), face, 4)
    for k in (0.33, 0.66):                  # plank joints
        a, b = _lerp2(pts[0], pts[1], k), _lerp2(pts[3], pts[2], k)
        out += _line(a[0], a[1] + 6, b[0], b[1] - 6, sw=2.4, color=S.shade(face, -0.3))
    for t in (0.16, 0.84):                  # battens
        a, b = _lerp2(pts[0], pts[3], t), _lerp2(pts[1], pts[2], t)
        out += _p(_poly([(a[0], a[1] - 7), (b[0], b[1] - 7), (b[0], b[1] + 7), (a[0], a[1] + 7)]),
                  S.shade(face, 0.12), 3)
    for t in (0.16, 0.84):                  # hinges on the frame side
        a = _lerp2(pts[0], pts[3], t)
        out += _circ(a[0], a[1], 5, P["wood_dark"], 2)
    if abs(fx - hx) > 20:                   # a little knob on the free edge
        k = _lerp2(pts[1], pts[2], 0.5)
        out += _circ(k[0] + sx * 6 * (1 if th <= math.pi / 2 else -1), k[1], 5, P["crown"], 2.2)
    return out


def _upwindow(op=1.0, part="all", wall=True, interior=False, glow=0.0):
    x0, top, x1, sill = WINDOW_OPENING
    opening = (f"M{x0},{sill} L{x0},{top + 14} Q{x0},{top} {x0 + 14},{top} L{x1 - 14},{top} Q{x1},{top} {x1},{top + 14} "
               f"L{x1},{sill} Z")
    back, front = "", ""
    if not interior:                        # the dim room seen through the opening
        ig = _uid("winin", glow)
        back += (f'<defs>{S.rad_grad(ig, [(0, S.mix("#6b4c36", P["glow"], 0.7 * glow)), (1, "#4a3428")], cy=0.75, r=0.8)}'
                 f'</defs><path d="{opening}" fill="url(#{ig})"/>')
        back += _p(f"M{x0},{sill - 60} L{x1},{sill - 70}", sw=3, stroke="#3a281e", extra='opacity="0.5"')
    if wall:
        wx0, wy0, wx1, wy1 = WINDOW_WALL
        col = S.mix(P["sand"], P["stone"], 0.4) if not interior else S.mix(P["sand_light"], P["stone"], 0.3)
        d = f"M{wx0},{wy0} L{wx1},{wy0} L{wx1},{wy1} L{wx0},{wy1} Z " + opening
        front += f'<path d="{d}" fill="{col}" fill-rule="evenodd"/>'
        cid = _uid("winwall", interior)
        front += (f'<clipPath id="{cid}"><path d="{d}" clip-rule="evenodd"/></clipPath>'
                  f'<g clip-path="url(#{cid})">{_bricks(wx0 + 20, wx1 - 20, wy1 - 20, wy0 + 20, col, 11, 5)}</g>')
    # frame, lintel beam with beam ends, sill
    front += _p(opening, "none", 12, stroke=INK) + _p(opening, "none", 6, stroke=P["wood"])
    front += _rect(x0 - 44, top - 34, x1 - x0 + 88, 26, P["wood"], 4, rx=6)
    for bx in (x0 - 32, x1 + 32):
        front += _circ(bx, top - 21, 7, P["wood_dark"], 2.4)
    front += _line(x0 - 36, top - 24, x1 + 36, top - 24, sw=2.4, color=P["wood_dark"], extra='opacity="0.6"')
    front += _rect(x0 - 32, sill - 4, x1 - x0 + 64, 20, P["wood_light"], 4, rx=5)
    front += _line(x0 - 26, sill + 4, x1 + 26, sill + 4, sw=2.4, color=P["wood"], extra='opacity="0.7"')
    front += _shutter(-1, op) + _shutter(1, op)
    if part == "back":
        return back
    if part == "front":
        return front
    return back + front


def upstairs_window(x, y, scale=1.0, open=1.0, part="all", wall=True, interior=False, glow=0.0):
    if part not in ("all", "back", "front"):
        raise ValueError(f"upstairs_window: part must be 'all', 'back' or 'front', not {part!r}")
    return _place(_upwindow(open, part, wall, interior, glow), x, y, scale, 1)


# ---------------------------------------------------------------------- royal things
def _signet_ring():
    """The king's signet ring standing upright: a gold band with a carved blue seal stone on top."""
    gold, dark = _GOLD, _GOLD_DARK
    out = _p("M-30,18 A30,30 0 1 0 30,18 A30,30 0 1 0 -30,18", sw=22, stroke=INK)
    out += _p("M-30,18 A30,30 0 1 0 30,18 A30,30 0 1 0 -30,18", sw=14, stroke=gold)
    out += _p("M-24,34 A22,22 0 0 0 4,46", sw=4, stroke=S.shade(gold, 0.35), extra='opacity="0.8"')
    out += _p("M-30,-16 Q-32,-4 -18,-2 L18,-2 Q32,-4 30,-16 Z", dark, 4)            # bezel shoulders
    out += _ell(0, -20, 32, 16, gold, 4)
    out += _ell(0, -21, 23, 10.5, "#3f6f9e", 3)                                       # carved stone
    for j in range(8):
        a = j * math.pi / 4
        out += _ell(11 * math.cos(a), -21 + 5 * math.sin(a), 3.6, 2.2, "#cfe2ea", 0, extra='opacity="0.85"')
    out += _circ(0, -21, 2.8, "#cfe2ea", 0)
    out += _ell(-11, -26, 6, 2.4, HILITE, 0, extra='opacity="0.8"')
    return out


def royal_seal(x, y, scale=1.0, kind="ring"):
    if kind == "ring":
        return _place(_signet_ring(), x, y, scale)
    if kind == "impression":
        return _place(_royal_impression(0, 0, 1.0), x, y, scale)
    raise ValueError(f"royal_seal: kind must be 'ring' or 'impression', not {kind!r}")


def _decree(sealed=True):
    parch, roll = "#efdfb8", "#e2cb98"
    out = _p("M-86,-110 L86,-110 Q80,0 86,110 L-86,110 Q-80,0 -86,-110 Z", parch, 4)
    out += _p("M-58,-80 L58,-80", sw=7, stroke=P["sail_stripe"], extra='opacity="0.85"')     # a red title line
    for i, yy in enumerate(range(-52, 60, 18)):
        x0, x1 = -62, 62 - (i % 3) * 16
        d = f"M{x0},{yy}"
        xx = x0
        while xx < x1:
            d += " q4,-5 8,0 q4,5 8,0"
            xx += 16
        out += _p(d, sw=2.4, stroke=P["ink_soft"], extra='opacity="0.8"')
    for yy in (-112, 112):
        out += _rect(-100, yy - 11, 200, 22, roll, 4, rx=10)
        for sx in (-108, 100):
            out += _rect(sx, yy - 6, 8, 12, P["wood"], 3, rx=3)
    if sealed:
        out += _p("M-6,80 Q-18,112 -26,130 L-14,128 L-10,140 Q-2,112 4,84 Z", P["sail_stripe"], 3)
        out += _p("M6,80 Q18,112 28,128 L16,130 L14,142 Q4,112 -2,84 Z", S.shade(P["sail_stripe"], -0.15), 3)
        out += _royal_impression(0, 76, 0.8)
    return out


def decree(x, y, scale=1.0, rot=0, sealed=True):
    return _place(_decree(sealed), x, y, scale, 1, rot)


def _bull_protome(sx, base_y):
    """One friendly kneeling bull fore-part of a Persepolis capital, facing outward (sx = -1 left, +1 right)."""
    col, dark = "#ece0c6", "#b8a684"
    out = ""
    b = [(sx * 10, base_y), (sx * 10, base_y - 92), (sx * 70, base_y - 104), (sx * 120, base_y - 84),
         (sx * 128, base_y - 30), (sx * 96, base_y)]
    out += _p(_sm(b), col, 4)
    out += _p(f"M{sx * 26},{base_y - 64} Q{sx * 48},{base_y - 82} {sx * 74},{base_y - 70}", sw=2.6, stroke=dark)
    for k in range(3):                              # curly chest hair
        cx = sx * (60 + k * 18)
        out += _p(f"M{cx - 6},{base_y - 40} q6,-8 12,0", sw=2.4, stroke=dark)
    out += _p(f"M{sx * 96},{base_y} L{sx * 96},{base_y - 26} Q{sx * 130},{base_y - 30} {sx * 138},{base_y - 8} "
              f"L{sx * 134},{base_y} Z", col, 3.6)                                     # folded foreleg
    out += _rect(min(sx * 134, sx * 112) - 0, base_y - 9, 22, 9, _GOLD_DARK, 2.6, rx=3)  # hoof
    # head
    hx, hy = sx * 142, base_y - 104
    out += _tube(f"M{hx - sx * 18},{hy - 26} Q{hx - sx * 30},{hy - 58} {hx - sx * 6},{hy - 64}", 9, "#e8d6a8", 3)
    out += _tube(f"M{hx + sx * 8},{hy - 30} Q{hx + sx * 20},{hy - 60} {hx + sx * 40},{hy - 58}", 9, "#e8d6a8", 3)
    out += _ell(hx - sx * 30, hy - 14, 18, 10, col, 3.4, extra=f'transform="rotate({sx * -30} {hx - sx * 30} {hy - 14})"')
    out += _p(_sm([(hx - sx * 26, hy - 30), (hx + sx * 14, hy - 38), (hx + sx * 34, hy - 10), (hx + sx * 38, hy + 22),
                   (hx + sx * 22, hy + 38), (hx - sx * 6, hy + 34), (hx - sx * 26, hy + 6)]), col, 4)
    out += _ell(hx + sx * 24, hy + 26, 18, 13, "#e2cba2", 3.2)                      # muzzle
    out += _circ(hx + sx * 18, hy + 26, 2.6, INK, 0) + _circ(hx + sx * 32, hy + 24, 2.6, INK, 0)
    out += _dot_eye(hx + sx * 8, hy - 6, 5, "happy") + _blush(hx - sx * 6, hy + 12, 8, 5)
    out += _rect(hx - 30, hy + 38, 60, 9, "#4f86b0", 2.6, rx=4)                     # painted collar
    return out


def _column(height=600):
    stone, dark = "#ece0c6", "#c4b494"
    out = ""
    out += _rect(-80, -30, 160, 30, S.shade(stone, -0.08), 4, rx=4)                     # plinth
    out += _p("M-66,-30 Q-70,-70 -38,-98 L38,-98 Q70,-70 66,-30 Z", stone, 4)          # bell base
    for k in (-0.6, -0.2, 0.2, 0.6):
        out += _p(f"M{k * 60:.1f},-32 Q{k * 46:.1f},-70 {k * 30:.1f},-96", sw=2.4, stroke=dark)
    out += _p("M-60,-46 Q0,-30 60,-46", sw=2.4, stroke=dark)
    top = -98 - height
    out += _rect(-32, top, 64, height + 2, stone, 4)                                       # shaft
    for k in (-18, -6, 6, 18):
        out += _line(k, top + 8, k, -104, sw=2.4, color=dark, extra='opacity="0.8"')
    out += _rect(-38, top - 14, 76, 16, "#4f86b0", 3.4, rx=4)                              # painted ring
    out += _p(f"M-36,{top - 14} Q-80,{top - 50} -74,{top - 78} L74,{top - 78} Q80,{top - 50} 36,{top - 14} Z",
              stone, 4)                                                                    # palm / lotus capital
    for k in (-0.7, -0.35, 0, 0.35, 0.7):
        out += _p(f"M{k * 30:.1f},{top - 16} Q{k * 58:.1f},{top - 46} {k * 72:.1f},{top - 74}", sw=2.4, stroke=dark)
    out += _rect(-60, top - 106, 120, 28, S.shade(stone, -0.05), 4, rx=4)
    for xx in (-40, -14, 12, 38):
        out += _p(f"M{xx},{top - 102} q6,10 0,20", sw=2.4, stroke=_GOLD_DARK)
    base_y = top - 106
    out += _rect(-40, base_y - 74, 80, 44, P["wood"], 4, rx=4)                            # beam end between the bulls
    out += _circ(0, base_y - 52, 9, P["wood_dark"], 2.4)
    out += _bull_protome(-1, base_y) + _bull_protome(1, base_y)
    return out


def persian_column(x, y, scale=1.0, height=600):
    return _place(_column(height), x, y, scale)


# ---------------------------------------------------------------------- small palace props
def _cushion(col=None):
    col = col or P["royal_light"]
    out = _p("M-78,0 Q-92,-26 -74,-52 Q0,-64 74,-52 Q92,-26 78,0 Q0,8 -78,0 Z", col, 4)
    out += _p("M-60,-40 Q0,-50 60,-40", sw=3, stroke=S.shade(col, 0.3), extra='opacity="0.8"')
    out += _p("M-40,-16 Q0,-8 40,-16", sw=2.4, stroke=S.shade(col, -0.25))
    for sx in (-1, 1):
        for cy in (-52, -2):
            out += _circ(sx * 80, cy, 6, _GOLD, 2.4)
            out += _p(f"M{sx * 82},{cy + 4} l{sx * 6},14 l{sx * -10},0 Z", _GOLD, 2.2)
    return out


def cushion(x, y, scale=1.0, color=None):
    return _place(_cushion(color), x, y, scale)


def _oil_lamp(lit=True, gid="ol"):
    clay = P["terracotta"]
    out = ""
    if lit:
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.9), (0.4, P["gold"], 0.35), (1, P["gold"], 0)])}</defs>'
                f'<ellipse cx="36" cy="-44" rx="90" ry="80" fill="url(#{gid})" filter="url(#soft)"/>')
    out += _p("M-40,-16 Q-50,-6 -38,-4 Q-46,-30 -30,-30", sw=6, stroke=INK) + \
        _p("M-40,-16 Q-50,-6 -38,-4 Q-46,-30 -30,-30", sw=2.5, stroke=clay)                   # handle
    out += _p("M-36,-4 Q-40,-30 0,-32 Q30,-32 44,-22 L50,-14 Q34,-2 0,0 Q-30,2 -36,-4 Z", clay, 4)
    out += _ell(-4, -28, 12, 4, S.shade(clay, -0.4), 2.5)                                       # fill hole
    out += _p("M-26,-12 Q0,-6 30,-12", sw=2.4, stroke=S.shade(clay, 0.3))
    if lit:
        out += _p("M48,-20 Q36,-38 46,-58 Q50,-44 58,-40 Q62,-26 48,-20 Z", P["sun_hot"], 3)
        out += _p("M49,-24 Q44,-34 48,-44 Q54,-34 49,-24 Z", P["glow"], 0)
    return out


def oil_lamp(x, y, scale=1.0, lit=True):
    return _place(_oil_lamp(lit, _uid("oil", lit)), x, y, scale)


def _food_tray():
    brass = "#d9a845"
    out = ""
    out += _ell(0, -12, 116, 28, S.shade(brass, -0.15), 4)
    out += _ell(0, -16, 106, 22, brass, 3)
    out += _p("M-60,-26 Q-62,-56 -30,-58 Q0,-60 -2,-28 Z", "#e2b36a", 3.6)                    # bread
    out += _p("M-52,-40 l14,-4 M-44,-30 l14,-4 M-36,-48 l12,-3", sw=2.4, stroke="#b9853f")
    for cx, cy in ((26, -50), (40, -50), (33, -60), (19, -38), (33, -38), (47, -38), (26, -28), (40, -28)):
        out += _circ(cx, cy, 8, "#8a5aa0", 2.6)                                                  # grapes
    out += _p("M33,-66 q2,-10 10,-14", sw=3, stroke=P["leaf_dark"])
    out += _ell(46, -74, 10, 6, P["leaf"], 2.4, extra='transform="rotate(-25 46 -74)"')
    out += _circ(74, -32, 14, "#c0533a", 3.4) + _p("M70,-46 l4,-6 l4,6", sw=2.6)            # pomegranate
    out += _ell(-10, -26, 10, 8, "#8a5a3a", 2.6) + _ell(6, -24, 9, 7, "#8a5a3a", 2.6)        # figs / dates
    out += _p("M-96,-42 L-74,-42 L-78,-26 Q-85,-22 -92,-26 Z", _GOLD, 3)                     # cup
    out += _line(-85, -24, -85, -14, sw=4, color=_GOLD_DARK) + _ell(-85, -13, 9, 3, _GOLD, 2.4)
    return out


def food_tray(x, y, scale=1.0):
    return _place(_food_tray(), x, y, scale)


def _lyre():
    wood = P["wood"]
    out = ""
    out += _tube("M-36,-40 Q-60,-100 -44,-160 Q-40,-176 -54,-184", 12, wood, 3.6)
    out += _tube("M36,-40 Q60,-100 44,-160 Q40,-176 54,-184", 12, wood, 3.6)
    out += _tube("M-58,-158 L58,-158", 10, P["wood_dark"], 3.4)
    for k in range(6):
        xx = -25 + k * 10
        out += _line(xx * 1.15, -154, xx, -28, sw=2, color="#efe2c4")
    out += _p("M-52,-46 Q-58,0 -30,0 L30,0 Q58,0 52,-46 Z", P["wood_light"], 4)              # sound box
    out += _rect(-34, -34, 68, 10, wood, 2.6, rx=4)
    out += _circ(0, -16, 6, P["wood_dark"], 2.2)
    for xx in (-54, 54):
        out += _circ(xx, -184, 6, _GOLD, 2.4)
    return out


def lyre(x, y, scale=1.0, facing=1):
    return _place(_lyre(), x, y, scale, facing)


def _couch():
    wood, purple, lav = P["wood"], P["royal"], P["royal_light"]
    out = ""
    out += _lion_leg(-170, -60, 0, 18) + _lion_leg(150, -60, 0, 18)
    out += _p("M-226,-150 Q-240,-210 -206,-224 Q-190,-226 -186,-206 L-186,-70 L-226,-70 Z", wood, 4)  # headrest
    out += _circ(-206, -214, 9, _GOLD, 2.6)
    out += _rect(-220, -86, 420, 28, wood, 4, rx=8)
    out += _line(-210, -72, 190, -72, sw=3, color=_GOLD)
    out += _p("M-196,-86 Q-200,-122 -170,-122 L180,-122 Q206,-120 200,-86 Z", purple, 4)       # mattress
    out += _p("M-150,-112 L180,-112", sw=4, stroke=lav, extra='opacity="0.6"')
    out += _p("M-184,-120 Q-196,-158 -160,-158 L-110,-156 Q-90,-150 -98,-120 Z", "#efe2c4", 3.6)  # pillow
    out += _p("M60,-122 Q40,-80 70,-60 L196,-60 Q206,-90 200,-120 Z", lav, 3.6)                # folded blanket
    for xx in (90, 130, 170):
        out += _line(xx, -112, xx - 6, -66, sw=2.2, color=S.shade(lav, -0.25))
    return out


def couch(x, y, scale=1.0, facing=1):
    return _place(_couch(), x, y, scale, facing)


# ====================================================================== 8. David film (1 Samuel 17)
BRONZE = "#c8914f"
BRONZE_DARK = S.shade(BRONZE, -0.32)
BRONZE_LIGHT = S.shade(BRONZE, 0.42)
LEATHER = "#8b5a35"
LEATHER_LIGHT = "#b98552"
CORD = "#c9a46a"
IRON = "#a9adab"
CREST_RED = "#b8473c"
WICKER = "#c9995a"
STONE_COLS = ("#b9b2a6", "#c9bca6", "#a8a49c", "#cdb79a", "#b4a99a")


# ---------------------------------------------------------------------- shapes shared with art/characters.py
def _bread_basket(handle=True):
    """Wicker basket of bread loaves and a cheese, anchor bottom centre; rim y=-56, handle top y=-104."""
    out = ""
    if handle:
        out += _tube("M-50,-54 Q-46,-104 0,-104 Q46,-104 50,-54", 8, WICKER, 3.2)
    out += _p(_sm([(-60, -60), (-34, -82), (-6, -84), (4, -62), (-30, -52)]), "#d9a25e", 3.4)          # loaf 1
    out += _p("M-44,-70 l10,-8 M-30,-68 l10,-9 M-16,-68 l8,-8", sw=2.4, stroke="#a8743c")
    out += _p(_sm([(-6, -58), (14, -86), (40, -88), (52, -64), (24, -54)]), "#e2b36a", 3.4)             # loaf 2
    out += _p("M10,-70 l9,-9 M24,-70 l9,-9 M37,-70 l7,-8", sw=2.4, stroke="#b9853f")
    out += _circ(40, -60, 17, "#f2cf6b", 3.2) + _p("M40,-60 L57,-62 L52,-49 Z", "#f8e6a8", 2.4)          # cheese
    out += _circ(30, -64, 2.5, "#d9b04a", 0) + _circ(44, -70, 2, "#d9b04a", 0)
    body = "M-60,-58 L60,-58 Q58,-22 46,-4 Q44,0 36,0 L-36,0 Q-44,0 -46,-4 Q-58,-22 -60,-58 Z"
    weave = ""
    for k, yy in enumerate(range(-50, 0, 10)):
        off = 7 if k % 2 else 0
        for xx in range(-70 + off, 70, 14):
            weave += f"M{xx},{yy} q7,-5 14,0 "
    for xx in range(-48, 56, 16):
        weave += f"M{xx},-56 L{xx * 0.78:.1f},-2 "
    out += _p(body, WICKER, 0) + _clip(_uid("bsk", handle), body, _p(weave, sw=2.0, stroke=S.shade(WICKER, -0.3)))
    out += _p(body, sw=3.8)
    out += _tube("M-62,-58 L62,-58", 9, S.shade(WICKER, 0.12), 3.2)
    return out


def _harp():
    """Small shepherd's harp (kinnor lyre): sound box below, two uneven curved arms, slanted yoke, 6 strings."""
    wood, wd = P["wood_light"], P["wood"]
    out = ""
    out += _tube("M-30,-34 Q-46,-80 -36,-118 Q-32,-130 -42,-138", 10, wd, 3.4)
    out += _tube("M30,-34 Q48,-96 40,-140 Q38,-156 48,-164", 10, wd, 3.4)
    out += _tube("M-48,-128 L52,-156", 9, P["wood_dark"], 3.2)
    for k in range(6):
        u = (k + 0.5) / 6
        xt, yt = -36 + 80 * u, -130 - 25 * u
        out += _line(xt, yt, -24 + 48 * u, -30, sw=1.8, color="#efe2c4")
    out += _p("M-42,-36 Q-48,0 -20,0 L20,0 Q48,0 42,-36 Q0,-46 -42,-36 Z", wood, 3.8)
    out += _ell(0, -18, 9, 7, P["wood_dark"], 2.4)
    out += _rect(-28, -36, 56, 7, wd, 2.4, rx=3)
    for k in range(6):
        u = (k + 0.5) / 6
        out += _circ(-36 + 80 * u, -131 - 25 * u, 2.6, _GOLD, 1.4)
    return out


def _round_shield(r=46, kind="israel"):
    """Round shield centred on (0, 0): 'israel' wood and leather with a bronze rim and boss, 'philistine' bronze
    with rings and studs."""
    if kind == "philistine":
        face, ring = BRONZE, BRONZE_DARK
        out = _circ(0, 0, r, face, 4)
        out += _circ(0, 0, r * 0.74, "none", 2.6, stroke=ring) + _circ(0, 0, r * 0.46, "none", 2.4, stroke=ring)
        for k in range(10):
            a = 2 * math.pi * k / 10
            out += _circ(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a), r * 0.05, BRONZE_LIGHT, 0)
        out += _circ(0, 0, r * 0.2, BRONZE_LIGHT, 3)
        out += _p(f"M{_f(-r * 0.55)},{_f(-r * 0.5)} Q{_f(-r * 0.2)},{_f(-r * 0.82)} {_f(r * 0.25)},{_f(-r * 0.8)}", sw=3.4,
                  stroke=BRONZE_LIGHT, extra='opacity="0.8"')
        return out
    face = "#a0683e"
    out = _circ(0, 0, r, face, 4)
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.3
        out += _line(r * 0.25 * math.cos(a), r * 0.25 * math.sin(a), r * 0.84 * math.cos(a), r * 0.84 * math.sin(a),
                     sw=2.2, color=S.shade(face, -0.3))
    out += _circ(0, 0, r * 0.9, "none", r * 0.13, stroke=BRONZE) + _circ(0, 0, r * 0.83, "none", 1.6)
    for k in range(8):
        a = 2 * math.pi * k / 8
        out += _circ(r * 0.9 * math.cos(a), r * 0.9 * math.sin(a), r * 0.045, BRONZE_LIGHT, 0)
    out += _circ(0, 0, r * 0.24, BRONZE, 3) + _circ(-r * 0.07, -r * 0.08, r * 0.07, BRONZE_LIGHT, 0)
    return out


def _tall_shield(ry=150):
    """Goliath's great tall shield (carried by his shield-bearer), centred on (0, 0): a woven oval with a bronze
    rim, ribs and a boss."""
    rx = ry * 0.5
    d = f"M0,{_f(-ry)} C{_f(rx * 1.3)},{_f(-ry)} {_f(rx * 1.3)},{_f(ry)} 0,{_f(ry)} C{_f(-rx * 1.3)},{_f(ry)} {_f(-rx * 1.3)},{_f(-ry)} 0,{_f(-ry)} Z"
    col = "#d9b878"
    weave = ""
    for yy in range(int(-ry), int(ry), 12):
        weave += f"M{_f(-rx * 1.1)},{yy} q{_f(rx * 0.55)},6 {_f(rx * 1.1)},0 q{_f(rx * 0.55)},-6 {_f(rx * 1.1)},0 "
    inner = _p(weave, sw=2.0, stroke=S.shade(col, -0.25))
    for xx in (-0.5, 0.0, 0.5):
        inner += _line(xx * rx, -ry, xx * rx * 1.05, ry, sw=6, color=S.shade(col, -0.18))
    out = _p(d, col, 0) + _clip(_uid("tsh", ry), d, inner)
    out += _p(d, "none", 14, stroke=BRONZE) + _p(d, "none", 4)
    out += _circ(0, 0, rx * 0.28, BRONZE, 3.4) + _circ(-rx * 0.08, -rx * 0.09, rx * 0.08, BRONZE_LIGHT, 0)
    return out


def _camp_stool(w=110, h=67):
    """Folding X-frame camp stool, anchor bottom centre: seat top y = -h."""
    wood = P["wood"]
    out = _tube(f"M{_f(-w / 2 + 6)},{_f(-h + 4)} L{_f(w / 2 - 8)},-4", 9, S.shade(wood, -0.15), 3.2)
    out += _tube(f"M{_f(w / 2 - 6)},{_f(-h + 4)} L{_f(-w / 2 + 8)},-4", 9, wood, 3.2)
    out += _circ(0, -h / 2, 5, BRONZE, 2.4)
    for sx in (-1, 1):
        out += _rect(sx * (w / 2 - 8) - 9, -6, 18, 7, P["wood_dark"], 2.4, rx=3)
    out += _p(f"M{_f(-w / 2 - 6)},{_f(-h - 4)} Q0,{_f(-h + 8)} {_f(w / 2 + 6)},{_f(-h - 4)} L{_f(w / 2 + 6)},{_f(-h + 4)} "
              f"Q0,{_f(-h + 16)} {_f(-w / 2 - 6)},{_f(-h + 4)} Z", LEATHER, 3.4)
    for sx in (-1, 1):
        out += _circ(sx * (w / 2 + 2), -h, 5, P["wood_dark"], 2.4)
    return out


# ---------------------------------------------------------------------- small things
def _sling(angle=0.0, length=96, stone=True, released=False):
    a = math.radians(angle)
    d = (math.sin(a), math.cos(a))
    n = (-d[1], d[0])
    out = _circ(0, 0, 6, "none", 3.4, stroke=CORD) + _circ(0, 0, 6, "none", 1.2)
    if released:
        pts = [(d[0] * length * t + n[0] * 8 * math.sin(t * 7) * t, d[1] * length * t + n[1] * 8 * math.sin(t * 7) * t)
               for t in [j / 10 for j in range(11)]]
        out += _tube(_sm(pts, closed=False), 2.4, CORD, 1.5)
        ex, ey = pts[-1]
        loose = [(ex + d[0] * (10 + 8 * j) + n[0] * 10 * math.sin(j * 1.4 + 1),
                  ey + d[1] * (10 + 8 * j) + n[1] * 10 * math.sin(j * 1.4 + 1)) for j in range(6)]
        out += _tube(_sm([(ex, ey)] + loose, closed=False), 2.4, CORD, 1.5)
        out += _ell(ex, ey, 12, 3.6, LEATHER, 2.4, extra=f'transform="rotate({math.degrees(math.atan2(d[1], d[0])):.1f} {_f(ex)} {_f(ey)})"')
        return out
    px, py = d[0] * length, d[1] * length
    for sg in (1, -1):
        out += _tube(f"M0,0 L{_f(px + sg * n[0] * 6.5)},{_f(py + sg * n[1] * 6.5)}", 2.4, CORD, 1.5)
    cx, cy = px + d[0] * 4, py + d[1] * 4
    if stone:
        out += _ell(px, py, 7.5, 6.5, STONE_COLS[0], 2.4)
    out += _ell(cx, cy, 11, 6, LEATHER, 2.4, extra=f'transform="rotate({math.degrees(math.atan2(n[1], n[0])):.1f} {_f(cx)} {_f(cy)})"')
    return out


def sling(x, y, scale=1.0, facing=1, angle=0.0, length=96, stone=True, released=False):
    return _place(_sling(angle, length, stone, released), x, y, scale, facing)


def _stone(seed=0, r=14):
    rng = random.Random(seed)
    col = STONE_COLS[seed % len(STONE_COLS)]
    rx, ry = r * rng.uniform(1.05, 1.3), r * rng.uniform(0.7, 0.85)
    out = _p(S.blob(0, -ry, rx, ry, 0.06, 9, seed=seed), col, 3.2)
    out += _ell(-rx * 0.35, -ry * 1.35, rx * 0.32, ry * 0.18, HILITE, 0, extra='opacity="0.7"')
    out += _p(f"M{_f(-rx * 0.6)},{_f(-ry * 0.45)} q{_f(rx * 0.5)},{_f(ry * 0.3)} {_f(rx * 1.1)},0", sw=2,
              stroke=S.shade(col, -0.2), extra='opacity="0.6"')
    return out


def stone(x, y, scale=1.0, seed=0):
    return _place(_stone(seed), x, y, scale)


def five_stones(x, y, scale=1.0, n=5):
    spots = [(-34, 0, 0), (-4, 0, 1), (28, 0, 2), (-18, -15, 3), (12, -16, 4)]
    out = "".join(_g(_stone(sd, 13 if i < 3 else 12), f"translate({dx},{dy})") for i, (dx, dy, sd) in
                  enumerate(spots[:max(0, min(5, n))]))
    return _place(out, x, y, scale)


def _shepherd_bag(stones=0, strap=True):
    out = ""
    if strap:
        out += _tube("M-30,-56 Q-20,-150 0,-152 Q22,-150 32,-56", 6, LEATHER, 2.8)
    if stones:
        for i in range(min(5, stones)):
            out += _g(_stone(i, 9), f"translate({-22 + i * 11},{-60 - (i % 2) * 7})")
    body = [(-40, -60), (40, -60), (44, -30), (28, -2), (-28, -2), (-44, -30)]
    out += _p(_sm(body, tension=0.7), LEATHER_LIGHT, 3.8)
    out += _p("M-28,-14 L28,-14", sw=1.8, stroke=S.shade(LEATHER, -0.2), extra='stroke-dasharray="4 4"')
    if stones:      # flap folded open behind
        out += _p("M-40,-60 Q0,-74 40,-60 Q0,-66 -40,-60 Z", LEATHER, 2.6)
    else:
        out += _p(_sm([(-41, -61), (41, -61), (30, -30), (0, -20), (-30, -30)], tension=0.7), LEATHER, 3.4)
        out += _circ(0, -28, 4.5, CORD, 2)
    return out


def shepherd_bag(x, y, scale=1.0, facing=1, stones=0, strap=True):
    return _place(_shepherd_bag(stones, strap), x, y, scale, facing)


def _crook_staff():
    pts = [(0, 0), (0, -230), (2, -268), (14, -290), (36, -296), (54, -282), (56, -258)]
    d = _sm(pts, closed=False)
    return _tube(d, 9, P["wood"], 3.4) + _p(_sm(pts[:3], closed=False), sw=2, stroke=P["wood_light"], extra='opacity="0.7"')


def staff(x, y, scale=1.0, facing=1, rot=0.0):
    return _place(_crook_staff(), x, y, scale, facing, rot)


def bread_basket(x, y, scale=1.0, handle=True):
    return _place(_bread_basket(handle), x, y, scale)


def harp(x, y, scale=1.0, facing=1):
    return _place(_harp(), x, y, scale, facing)


def round_shield(x, y, scale=1.0, kind="israel", rot=0.0):
    return _place(_round_shield(46, kind), x, y, scale, 1, rot)


def tall_shield(x, y, scale=1.0, rot=0.0):
    return _place(_tall_shield(150), x, y, scale, 1, rot)


KING_STOOL_Y = -74         # camp_stool seat top = under the hips of king(pose='sit', stool=False) (attire 'saul')


def camp_stool(x, y, scale=1.0, facing=1):
    return _place(_g(_camp_stool(126, -KING_STOOL_Y), "translate(-4,0)"), x, y, scale, facing)


def _helmet_side(crest=True, plume=None, circlet=False):
    col = BRONZE
    out = ""
    if crest:
        out += _p("M-44,-58 Q-40,-118 10,-124 Q52,-122 60,-86 Q50,-104 12,-108 Q-24,-104 -30,-58 Z", CREST_RED, 3.4)
        for k in range(7):
            u = (k + 0.5) / 7
            x0 = -36 + 90 * u
            out += _line(x0, -64 - 40 * math.sin(math.pi * (0.2 + 0.7 * u)), x0 + 6, -98 - 18 * math.sin(math.pi * u),
                         sw=1.8, color=S.shade(CREST_RED, -0.3))
    if plume:
        out += _tube("M0,-90 Q-20,-130 -54,-134", 14, plume, 2.6)
    out += _p("M-56,-6 Q-62,-40 -46,-66 Q-16,-98 22,-92 Q56,-84 62,-44 L58,-14 Q30,-22 6,-20 Q-4,-6 -24,-2 Z", col, 4)
    out += _p("M-36,-62 Q-6,-86 30,-80", sw=4, stroke=BRONZE_LIGHT, extra='opacity="0.85"')
    out += _tube("M-52,-18 Q-10,-32 60,-20", 8, BRONZE_DARK, 3)
    for x0 in (-30, 0, 30):
        out += _circ(x0, -26 + abs(x0) * 0.1, 2.6, BRONZE_LIGHT, 0)
    if circlet:
        out += _tube("M-50,-42 Q0,-60 60,-46", 8, _GOLD, 2.6)
        for x0, y0 in ((-24, -54), (8, -58), (38, -54)):
            out += _p(f"M{x0 - 6},{y0} L{x0},{y0 - 16} L{x0 + 6},{y0} Z", _GOLD, 2)
    return out


def helmet_bronze(x, y, scale=1.0, facing=1, rot=0.0, crest=True, plume=None, circlet=False):
    return _place(_helmet_side(crest, plume, circlet), x, y, scale, facing, rot)


def _spear(kind="soldier"):
    if kind == "goliath":
        L, w, hl, hw = 900, 22, 104, 22
    else:
        L, w, hl, hw = 360, 7, 40, 10
    out = _tube(f"M{_f(-L / 2)},0 L{_f(L / 2 - hl)},0", w, P["wood"], 3.4 if kind != "goliath" else 4)
    tip = L / 2
    out += _p(f"M{_f(tip - hl)},{_f(-hw * 0.45)} Q{_f(tip - hl * 0.55)},{_f(-hw)} {_f(tip)},0 "
              f"Q{_f(tip - hl * 0.55)},{_f(hw)} {_f(tip - hl)},{_f(hw * 0.45)} Z", IRON, 3.4)
    out += _line(tip - hl + 6, 0, tip - 10, 0, sw=2, color=S.shade(IRON, -0.35))
    out += _rect(tip - hl - 10, -w * 0.7, 12, w * 1.4, BRONZE, 2.6, rx=3)
    out += _tube(f"M{_f(-L / 2 - 14)},0 L{_f(-L / 2)},0", w * 0.7, IRON, 2.8)
    return out


def spear(x, y, scale=1.0, rot=0.0, kind="soldier"):
    return _place(_spear(kind), x, y, scale, 1, rot)


def _sword():
    out = _tube("M-60,0 L100,0", 14, S.shade(LEATHER, -0.1), 3.4)           # scabbard
    out += _tube("M88,0 L104,0", 16, BRONZE, 3)
    out += _tube("M-64,-24 L-64,24", 8, BRONZE, 3)                           # cross-guard
    out += _tube("M-96,0 L-66,0", 9, LEATHER, 3)                             # grip
    out += _circ(-100, 0, 8, BRONZE, 3)
    for x0 in (-20, 30):
        out += _line(x0, -7, x0, 7, sw=2, color=BRONZE_LIGHT)
    return out


def sword(x, y, scale=1.0, rot=0.0):
    return _place(_sword(), x, y, scale, 1, rot)


# ---------------------------------------------------------------------- the bear
BEAR = {"body": "#8e5f3e", "shade": "#74492e", "muzzle": "#d9b08a", "nose": "#4a3426", "ear_in": "#c98d6c",
        "paw": "#e0bd94"}
BEAR_POSES = ("stand", "walk_a", "walk_b", "roar", "run_a", "run_b")


def _bear_head(cx, cy, mouth=0.0, tilt=0.0):
    C = BEAR
    out = ""
    for ex, ey in ((cx - 36, cy - 42), (cx + 26, cy - 48)):
        out += _circ(ex, ey, 18, C["body"], 3.8) + _circ(ex + 1, ey + 2, 9, C["ear_in"], 0)
    out += _p(S.blob(cx, cy, 56, 52, 0.04, 12, seed=4), C["body"], 4)
    out += _p(f"M{_f(cx - 40)},{_f(cy - 30)} Q{_f(cx - 20)},{_f(cy - 46)} {_f(cx + 4)},{_f(cy - 44)}", sw=3,
              stroke=S.shade(C["body"], 0.25), extra='opacity="0.6"')
    mx, my = cx + 30, cy + 16
    m = _clamp(mouth)
    out += _ell(mx, my + 2 + 10 * m, 34, 25 + 8 * m, C["muzzle"], 3.6)
    if m > 0.02:
        mw, mh = 14 + 8 * m, 6 + 20 * m
        oy = my + 10
        out += _p(f"M{_f(mx + 6 - mw)},{_f(oy)} Q{_f(mx + 6 - mw)},{_f(oy + mh * 1.2)} {_f(mx + 6)},{_f(oy + mh * 1.2)} "
                  f"Q{_f(mx + 6 + mw)},{_f(oy + mh * 1.2)} {_f(mx + 6 + mw)},{_f(oy)} Z", P["mouth_inside"], 3.2)
        out += _ell(mx + 6, oy + mh * 0.95, mw * 0.6, mh * 0.3 + 2, _TONGUE, 0)
        for tx in (mx + 6 - mw * 0.5, mx + 6 + mw * 0.5):
            out += _p(f"M{_f(tx - 4)},{_f(oy + 1)} L{_f(tx - 3.5)},{_f(oy + 5 + 3 * m)} Q{_f(tx)},{_f(oy + 9 + 4 * m)} "
                      f"{_f(tx + 3.5)},{_f(oy + 5 + 3 * m)} L{_f(tx + 4)},{_f(oy + 1)} Z", CREAM, 2.2)
    else:
        out += _p(f"M{_f(mx - 6)},{_f(my + 14)} Q{_f(mx + 6)},{_f(my + 22)} {_f(mx + 18)},{_f(my + 12)}", sw=2.8)
    out += _ell(mx + 22, my - 8, 13, 9, C["nose"], 3) + _ell(mx + 18, my - 11, 4, 2, HILITE, 0, extra='opacity="0.7"')
    for ex, ey in ((cx - 8, cy - 12), (cx + 26, cy - 16)):
        out += _dot_eye(ex, ey, 7.5)
        out += _p(f"M{_f(ex - 9)},{_f(ey - 15)} Q{_f(ex)},{_f(ey - 21)} {_f(ex + 9)},{_f(ey - 16)}", sw=3,
                  stroke=S.shade(C["body"], -0.45))
    out += _blush(cx - 26, cy + 14, 10, 6) + _blush(cx + 56, cy + 8, 7, 5)
    if tilt:
        out = _g(out, f"rotate({tilt:.1f} {_f(cx)} {_f(cy)})")
    return out


def _bear(pose="stand", mouth=0.0):
    if pose not in BEAR_POSES:
        raise ValueError(f"bear: unknown pose {pose!r}; choose from {BEAR_POSES}")
    C = BEAR
    col, far = C["body"], S.shade(C["body"], -0.18)
    out = ""
    if pose == "roar":       # up on the hind legs, front paws up, a big (friendly) roar
        out += _big_cat_leg((-40, -110), (-56, 0), 56, 44, far)
        out += _p(S.blob(0, -190, 92, 128, 0.04, 12, seed=2), col, 4)
        out += _ell(16, -170, 56, 86, S.shade(col, 0.22), 0, extra='opacity="0.8"')
        out += _big_cat_leg((24, -100), (34, 0), 60, 46, col)
        out += _tube("M-50,-260 Q-92,-300 -84,-350", 40, far, 4)
        out += _ell(-84, -358, 22, 18, C["paw"], 3.4)
        out += _p(_sm([(-150, -240), (-120, -200)], closed=False), sw=0)
        out += _bear_head(28, -318, mouth if mouth > 0 else 0.8, tilt=-8)
        out += _tube("M54,-252 Q110,-280 120,-330", 40, col, 4)
        out += _ell(122, -340, 24, 19, C["paw"], 3.4)
        for k in range(3):
            out += _circ(110 + k * 12, -358 + (k % 2) * -2, 5, C["paw"], 2.2)
        return out
    if pose in ("stand", "walk_a", "walk_b"):
        fx = {"stand": (-70, 120, -100, 92), "walk_a": (-40, 146, -130, 64), "walk_b": (-104, 88, -70, 124)}[pose]
        lift = {"stand": (0, 0, 0, 0), "walk_a": (0, 0, 8, 0), "walk_b": (0, 10, 0, 0)}[pose]
        by, bob, tilt = -130, 0, 0
    else:
        fx = {"run_a": (-150, 190, -110, 150), "run_b": (-40, 60, -10, 96)}[pose]
        lift = {"run_a": (14, 24, 0, 0), "run_b": (0, 0, 16, 10)}[pose]
        by, bob, tilt = -136, (-14 if pose == "run_a" else 0), (-6 if pose == "run_a" else 4)
    body_pts = [(-150, by + 10), (-136, by - 56), (-60, by - 74), (40, by - 82), (110, by - 60), (140, by - 10),
                (120, by + 50), (40, by + 62), (-60, by + 62), (-136, by + 46)]
    inner = ""
    out += _circ(-150, by - 20 + bob, 13, col, 3.4)                                   # stubby tail
    out += _big_cat_leg((-80, by + 24 + bob), (fx[0], -5 - lift[0]), 58, 46, far)
    out += _big_cat_leg((96, by + 20 + bob), (fx[1], -5 - lift[1]), 56, 44, far)
    bd = _g(_body(body_pts, col, "", _ell(0, by + 46, 110, 22, S.shade(col, 0.18), 0), f"bear{pose}"),
            f"translate(0,{bob}) rotate({tilt} 0 {by})")
    out += bd
    out += _p(f"M{-110},{by - 30 + bob} Q{-70},{by - 70 + bob} {-40},{by + 10 + bob}", sw=3, stroke=C["shade"],
              extra='opacity="0.6"')
    out += _big_cat_leg((-100, by + 30 + bob), (fx[2], -lift[2]), 64, 48, col)
    out += _big_cat_leg((78, by + 30 + bob), (fx[3], -lift[3]), 60, 46, col)
    hx, hy = 168, by - 26 + bob + (8 if pose.startswith("run") else 0)
    out += _bear_head(hx, hy, mouth, tilt=6 if pose.startswith("run") else 0)
    return out + inner


def bear(x, y, scale=1.0, facing=1, pose="stand", mouth=0.0):
    return _place(_bear(pose, mouth), x, y, scale, facing)


# ---------------------------------------------------------------------- sheep variants
SHEEP_POSES = ("stand", "graze", "walk_a", "walk_b", "bleat")
_SHEEP = [dict(wool="#f6efe0", face="#dcb89c", leg="#6b5040"), dict(wool="#f3ead8", face="#5e4a40", leg="#4f3e36"),
          dict(wool="#e6e0d6", face="#e2c2a8", leg="#7a6050"), dict(wool="#f8f1e2", face="#caa384", leg="#6b5040")]


def _sheep(variant=0, pose="stand", lamb=False):
    if pose not in SHEEP_POSES:
        raise ValueError(f"sheep: unknown pose {pose!r}; choose from {SHEEP_POSES}")
    c = _SHEEP[variant % 4]
    wool, face, leg = c["wool"], c["face"], c["leg"]
    k = 0.66 if lamb else 1.0
    hk = 1.18 if lamb else 1.0              # lambs: bigger head for their size
    out = ""
    lx = {"stand": ((-28, 44), (-46, 24)), "graze": ((-28, 44), (-46, 24)), "bleat": ((-28, 44), (-46, 24)),
          "walk_a": ((-14, 58), (-60, 12)), "walk_b": ((-40, 30), (-30, 40))}[pose]
    lh = 46 * k
    for x_ in lx[0]:
        out += _leg(x_ * k, -lh, 0, 13 * k + 1, S.shade(leg, -0.15))
    circles = [(-74 * k, -84 * k, 16 * k)]
    for i in range(12):
        a = 2 * math.pi * i / 12
        circles.append((70 * k * math.cos(a) * 0.95, -80 * k + 38 * k * math.sin(a), 24 * k))
    circles.append((0, -80 * k, 52 * k))
    for x_ in lx[1]:
        out += _leg(x_ * k, -lh, 0, 14 * k + 1, leg)
    out += _cluster(circles, wool, 3.8)
    for cx, cy in ((-30, -96), (10, -104), (-10, -72), (30, -78), (-46, -70)):
        out += _p(f"M{_f(cx * k - 8 * k)},{_f(cy * k)} q{_f(4 * k)},{_f(-7 * k)} {_f(8 * k)},0 q{_f(4 * k)},{_f(7 * k)} "
                  f"{_f(8 * k)},0", sw=2.4, stroke=S.shade(wool, -0.2))
    if variant % 4 == 3:
        out += _ell(-20 * k, -92 * k, 22 * k, 14 * k, "#c8a07a", 0, extra='opacity="0.55"')
    hx, hy, rot = {"stand": (76, -96, 22), "walk_a": (78, -94, 22), "walk_b": (78, -98, 22), "graze": (88, -34, 70),
                   "bleat": (74, -112, -4)}[pose]
    hx, hy = hx * k, hy * k
    h = hk * (k if not lamb else 0.78)
    out += _ell(hx - 22 * h, hy - 14 * h, 17 * h, 8 * h, face, 3.4, extra=f'transform="rotate({rot - 46} {_f(hx - 22 * h)} {_f(hy - 14 * h)})"')
    out += _ell(hx, hy, 25 * h, 31 * h, face, 3.8, extra=f'transform="rotate({rot} {_f(hx)} {_f(hy)})"')
    out += _cluster([(hx - 14 * h, hy - 28 * h, 12 * h), (hx - 2 * h, hy - 32 * h, 13 * h), (hx + 10 * h, hy - 26 * h, 11 * h)]
                    if pose != "graze" else [(hx - 24 * h, hy - 18 * h, 12 * h), (hx - 16 * h, hy - 30 * h, 12 * h)],
                    wool, 3.2)
    eye_kind = "closed" if pose == "bleat" else "open"
    ex, ey = (hx + 8 * h, hy - 4 * h) if pose != "graze" else (hx + 2 * h, hy + 2 * h)
    eye_col = HILITE if variant % 4 == 1 else None
    if eye_col:
        out += _circ(ex, ey, 6 * h, "#e8dccb", 0)
    out += _dot_eye(ex, ey, 4.2 * h, eye_kind) + _blush(ex + 4 * h, ey + 12 * h, 6 * h, 3.6 * h)
    if pose == "bleat":
        out += _ell(hx + 14 * h, hy + 22 * h, 6 * h, 5 * h, P["mouth_inside"], 2.4)
        for j in range(2):
            r = 18 + 12 * j
            out += _p(f"M{_f(hx + 34 * h + r * 0.5)},{_f(hy + 4 * h - r * 0.7)} Q{_f(hx + 34 * h + r)},{_f(hy + 4 * h)} "
                      f"{_f(hx + 34 * h + r * 0.5)},{_f(hy + 4 * h + r * 0.7)}", sw=2.6, stroke=P["ink_soft"])
    elif pose == "graze":
        out += _tube(f"M{_f(hx + 14 * h)},{_f(hy + 28 * h)} q4,8 10,10", 3, P["leaf"], 2)
    else:
        out += _p(f"M{_f(hx + 15 * h)},{_f(hy + 16 * h)} q4,4 8,0", sw=2.6)
    return out


def sheep(x, y, scale=1.0, facing=1, variant=0, pose="stand", lamb=False):
    return _place(_sheep(variant, pose, lamb), x, y, scale, facing)


# ---------------------------------------------------------------------- camps
TENT_SIDES = ("israel", "philistine")


def _flag_pole(x, top, bottom, col, col2, kind="banner", wave=0.0):
    out = _tube(f"M{x},{bottom} L{x},{top}", 6, P["wood_dark"], 3)
    out += _circ(x, top - 4, 6, _GOLD, 2.4)
    w = 8 * math.sin(wave * 2 * math.pi)
    if kind == "banner":       # Israel: a square tribal banner
        d = (f"M{x + 2},{top + 6} Q{x + 40},{top + 2 + w} {x + 80},{top + 8} L{x + 82},{top + 66} "
             f"Q{x + 42},{top + 60 - w} {x + 2},{top + 64} Z")
        out += _p(d, col, 3.4)
        out += _p(f"M{x + 8},{top + 30} Q{x + 42},{top + 26 + w} {x + 78},{top + 32}", sw=8, stroke=col2)
        out += _circ(x + 42, top + 46, 7, col2, 2)
    else:                      # Philistine: a long two-tailed pennant
        d = (f"M{x + 2},{top + 4} Q{x + 50},{top + 4 + w} {x + 110},{top + 14} L{x + 86},{top + 24} L{x + 112},{top + 34} "
             f"Q{x + 50},{top + 38 - w} {x + 2},{top + 40} Z")
        out += _p(d, col, 3.4)
        out += _p(f"M{x + 6},{top + 22} Q{x + 50},{top + 20 + w} {x + 92},{top + 24}", sw=5, stroke=col2)
    return out


def _tent(side="israel", flag=True, wave=0.0):
    if side not in TENT_SIDES:
        raise ValueError(f"tent: unknown side {side!r}; choose from {TENT_SIDES}")
    out = ""
    if side == "israel":       # low wide goat-hair tent with stripes, poles and guy ropes
        cloth, stripe = "#6a5546", "#8a7360"
        for sx in (-1, 1):
            out += _line(sx * 230, -118, sx * 300, 0, sw=2.4, color=S.shade(CORD, -0.2))
            out += _line(sx * 120, -170, sx * 260, 0, sw=2.4, color=S.shade(CORD, -0.2))
            out += _rect(sx * 300 - 4, -14, 8, 16, P["wood_dark"], 2.2)
        roof = "M-250,-112 Q-200,-176 -120,-180 Q-60,-196 0,-186 Q70,-198 130,-180 Q210,-172 250,-112 L232,-104 L-232,-104 Z"
        walls = "M-232,-108 L232,-108 L222,0 L-222,0 Z"
        out += _p(walls, S.shade(cloth, 0.12), 4)
        st = ""
        for xx in range(-240, 250, 34):
            st += f"M{xx},-200 L{xx},4 "
        out += _clip(_uid("tw", side), walls, _p(st, sw=10, stroke=S.shade(cloth, 0.22)))
        out += _p("M-62,0 L-50,-96 Q0,-110 50,-96 L62,0 Z", "#3a2a22", 3.4)                        # doorway
        out += _p("M-50,-96 Q-90,-60 -86,0 L-62,0 Z", S.shade(cloth, 0.3), 3)                      # door flap
        out += _p(roof, cloth, 4)
        rs = ""
        for xx in range(-230, 240, 46):
            rs += f"M{xx},-112 Q{xx * 1.02:.1f},-150 {xx * 0.9:.1f},-190 "
        out += _clip(_uid("tr", side), roof, _p(rs, sw=12, stroke=stripe, extra='opacity="0.8"'))
        for xx in (-120, 0, 130):
            out += _circ(xx, -186 + (8 if xx else 0), 6, P["wood_dark"], 2.4)
        if flag:
            out += _flag_pole(150, -330, -170, "#3f6f9e", "#efe2c4", "banner", wave)
        return out
    cloth, stripe = "#e8c27a", "#b5523b"   # peaked striped tent
    for sx in (-1, 1):
        out += _line(sx * 60, -250, sx * 230, 0, sw=2.4, color=S.shade(CORD, -0.2))
        out += _rect(sx * 230 - 4, -14, 8, 16, P["wood_dark"], 2.2)
    d = "M0,-300 Q-60,-200 -190,-30 Q-196,-6 -180,0 L180,0 Q196,-6 190,-30 Q60,-200 0,-300 Z"
    st = ""
    for k in range(-6, 7):
        st += f"M0,-300 L{k * 34},{4} "
    out += _p(d, cloth, 0) + _clip(_uid("tp", side), d, _p(st, sw=16, stroke=stripe, extra='opacity="0.9"'))
    out += _p(d, "none", 4)
    out += _p("M-40,0 Q-4,-150 0,-170 Q4,-150 40,0 Z", "#3a2a22", 3.4)
    out += _p("M0,-170 Q-30,-90 -70,-6 L-40,0 Q-14,-120 0,-170 Z", S.shade(cloth, 0.2), 3)
    out += _p("M-150,-60 Q0,-76 150,-60", sw=8, stroke=S.shade(stripe, -0.15))
    if flag:
        out += _flag_pole(0, -400, -296, CREST_RED, "#3f7f86", "pennant", wave)
    else:
        out += _circ(0, -304, 7, _GOLD, 2.4)
    return out


def tent(x, y, scale=1.0, facing=1, side="israel", flag=True, wave=0.0):
    return _place(_tent(side, flag, wave), x, y, scale, facing)


# ---------------------------------------------------------------------- the brook
def _brook(x0, x1, y, width=60.0, phase=0.0, seed=0, pebbles=True, s=1.0):
    rng = random.Random(seed)
    n = max(6, int((x1 - x0) / (90 * s)))
    top, bot, mid = [], [], []
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        cy = y + 14 * s * math.sin(i * 1.3 + seed)
        w = width * (0.5 + 0.1 * math.sin(i * 2.1 + seed * 0.7))
        top.append((xx, cy - w * 0.8))
        bot.append((xx, cy + w))
        mid.append((xx, cy))
    d = _sm(top, closed=False) + " " + " ".join(f"L{_f(px)},{_f(py)}" for px, py in reversed(bot)) + " Z"
    d = "M" + d[1:]
    gid = _uid("brk", x0, x1, y, width)
    defs = S.lin_grad(gid, [(0, P["sea_light"]), (0.6, P["sea"]), (1, S.shade(P["sea"], -0.1))], 0, 0, 0, 1)
    out = f"<defs>{defs}</defs>"
    out += _p(d, f"url(#{gid})", 0)
    inner = ""
    for j in range(int((x1 - x0) / (70 * s)) + 2):
        xx = x0 + ((j * 70 * s + phase * 70 * s) % (x1 - x0 + 70 * s)) - 35 * s
        k = int(_clamp((xx - x0) / (x1 - x0 + 1e-6)) * n)
        cy = mid[min(n, max(0, k))][1] + (j % 3 - 1) * width * 0.25
        inner += _p(f"M{_f(xx)},{_f(cy)} q{_f(12 * s)},{_f(-5 * s)} {_f(26 * s)},0", sw=3.2 * s, stroke=P["foam"],
                    extra='opacity="0.85"')
    out += _clip(gid + "c", d, inner)
    out += _p(d, "none", 3.6 * s)
    if pebbles:
        for i in range(int((x1 - x0) / (26 * s))):
            xx = rng.uniform(x0, x1)
            k = min(n, max(0, int((xx - x0) / (x1 - x0) * n)))
            side = rng.choice((0, 1))
            yy = (top if side == 0 else bot)[k][1] + rng.uniform(-6, 6) * s
            r = rng.uniform(5, 11) * s
            out += _ell(xx, yy, r * 1.3, r * 0.85, rng.choice(STONE_COLS), 2.4 * s)
    return out


def brook(x0, x1, y, width=60.0, scale=1.0, phase=0.0, seed=0, pebbles=True):
    return _place(_brook(x0, x1, y, width * scale, phase, seed, pebbles, scale), 0, 0, 1.0)


# ---------------------------------------------------------------------- picture-book day counter
def _sun_icon(r, filled=True):
    out = ""
    for k in range(8):
        a = 2 * math.pi * k / 8
        out += _line(r * 1.3 * math.cos(a), r * 1.3 * math.sin(a), r * 1.75 * math.cos(a), r * 1.75 * math.sin(a),
                     sw=3.2, color=P["sun_hot"] if filled else P["ink_soft"])
    out += _circ(0, 0, r, P["sun"] if filled else P["paper"], 3.2)
    if filled:
        out += _dot_eye(-r * 0.32, -r * 0.1, r * 0.11) + _dot_eye(r * 0.32, -r * 0.1, r * 0.11)
        out += _p(f"M{_f(-r * 0.3)},{_f(r * 0.25)} Q0,{_f(r * 0.5)} {_f(r * 0.3)},{_f(r * 0.25)}", sw=2.4)
    return out


def _moon_icon(r, filled=True):
    d = (f"M{_f(r * 0.2)},{_f(-r)} A{_f(r)},{_f(r)} 0 1 0 {_f(r * 0.2)},{_f(r)} "
         f"A{_f(r * 0.78)},{_f(r * 0.78)} 0 1 1 {_f(r * 0.2)},{_f(-r)} Z")
    out = _p(d, "#f2d27a" if filled else P["paper"], 3.2)
    if filled:
        out += _p(f"M{_f(-r * 0.68)},{_f(-r * 0.12)} q{_f(r * 0.1)},{_f(r * 0.1)} {_f(r * 0.2)},0", sw=2.2)
        out += _blush(-r * 0.62, r * 0.22, r * 0.12, r * 0.08, 0.7)
    return out


def _day_counter(n=7, filled=0.0, icons="pair", gap=64, pop=0.0, r=20):
    out = ""
    x0 = -(n - 1) * gap / 2
    last = None
    for i in range(n):
        xx = x0 + i * gap
        f_sun = filled - i >= (0.5 if icons == "pair" else 1.0) - 1e-9
        f_moon = filled - i >= 1.0 - 1e-9
        if f_sun or f_moon:
            last = (i, f_moon)
        items = []
        if icons in ("pair", "sun"):
            items.append(("sun", -r * 1.3 if icons == "pair" else 0, f_sun))
        if icons in ("pair", "moon"):
            items.append(("moon", r * 1.3 if icons == "pair" else 0, f_moon if icons == "pair" else filled - i >= 1 - 1e-9))
        for kind, dy, on in items:
            ic = _sun_icon(r, on) if kind == "sun" else _moon_icon(r, on)
            out += _g(ic, f"translate({_f(xx)},{_f(dy)})", '' if on else 'opacity="0.45"')
    if last is not None and pop > 0:
        i, moon = last
        k = 1 + 0.4 * math.sin(math.pi * _clamp(pop))
        kind = "moon" if (moon and icons != "sun") else "sun"
        dy = (r * 1.3 if kind == "moon" else -r * 1.3) if icons == "pair" else 0
        ic = _sun_icon(r, True) if kind == "sun" else _moon_icon(r, True)
        out += _g(ic, f"translate({_f(x0 + i * gap)},{_f(dy)}) scale({k:.3f})")
    return out


def day_counter(x, y, scale=1.0, n=7, filled=0.0, icons="pair", gap=64, pop=0.0):
    return _place(_day_counter(n, filled, icons, gap, pop), x, y, scale)


# ---------------------------------------------------------------------- the valley of Elah (backdrop)
VALLEY_HILL_H = 330        # plateau height of the two hills above the valley floor at scale 1


def valley_ground(x, x0, x1, y, scale=1.0):
    """Stage y of the ground surface at stage x for valley_elah(x0, x1, y, scale): the hill tops / slopes and the
    valley floor (= y between the hills). Put figures' anchors here."""
    u = (x - x0) / float(x1 - x0)
    hl = 1.0 - _smooth((u - 0.16) / 0.28)
    hr = _smooth((u - 0.56) / 0.28)
    wob = 1.0 + 0.04 * math.sin(u * 19.0)
    return y - VALLEY_HILL_H * scale * (hl + hr) * wob


def valley_points(x0, x1, y, scale=1.0):
    """Key stage points of valley_elah(x0, x1, y, scale): 'israel_camp' and 'philistine_camp' (ground points on the
    plateaus), 'left_edge' / 'right_edge' (where each hill's slope meets the valley floor), 'brook' (front of the
    brook on the valley floor) and 'centre' (middle of the valley floor)."""
    W = x1 - x0

    def gp(u):
        xx = x0 + W * u
        return (xx, valley_ground(xx, x0, x1, y, scale))
    return {"israel_camp": gp(0.09), "philistine_camp": gp(0.91), "left_edge": gp(0.44), "right_edge": gp(0.56),
            "brook": (x0 + W * 0.505, y + 40 * scale), "centre": (x0 + W * 0.5, y)}


def _valley(x0, x1, y, s=1.0, part="all", camps=True, brook_=True, seed=0, bottom=None, wave=0.0):
    W = x1 - x0
    Hh = VALLEY_HILL_H * s
    bottom = y + 320 * s if bottom is None else bottom
    rng = random.Random(seed)
    out = ""
    green, green_d, green_l = "#9cbb5e", "#7fa24a", "#b8cf7a"
    if part in ("all", "back"):
        # far ridges (hazy), then the receding valley floor between the hills
        far = S.hill(x0 - 80, x1 + 80, y - Hh * 0.62, Hh * 0.75, seed=seed + 3, bumps=4, bottom=y)
        out += _p(far, S.mix(green_l, P["sky_day"], 0.55), 2.6)
        far2 = S.hill(x0 + W * 0.25, x1 - W * 0.2, y - Hh * 0.56, Hh * 0.45, seed=seed + 5, bumps=3, bottom=y)
        out += _p(far2, S.mix(green, P["sky_day"], 0.4), 2.8)
        gid = _uid("vfl", x0, x1, y, s)
        out += f"<defs>{S.lin_grad(gid, [(0, S.mix(green_l, P['sky_day'], 0.3)), (1, green)])}</defs>"
        out += _rect(x0 - 80, y - Hh * 0.6, W + 160, bottom - y + Hh * 0.6 + 4, f"url(#{gid})", 0)
        out += _line(x0 - 80, y - Hh * 0.6, x1 + 80, y - Hh * 0.6, sw=2.6 * s)
        for _ in range(int(W / (40 * s))):
            xx, yy = rng.uniform(x0, x1), rng.uniform(y - Hh * 0.55, bottom)
            k = 0.4 + (yy - y + Hh * 0.6) / (Hh * 0.6 + bottom - y)
            out += _p(f"M{_f(xx)},{_f(yy)} q{_f(8 * s * k)},{_f(-4 * s * k)} {_f(16 * s * k)},0", sw=2.4 * s * k,
                      stroke=green_d, extra='opacity="0.5"')
        if brook_:
            mid = (x0 + x1) / 2
            ys = [y - Hh * 0.58 + (bottom - y + Hh * 0.58) * t for t in [j / 9 for j in range(10)]]
            cl = [(mid + W * 0.035 * math.sin(j * 1.25 + seed), yy) for j, yy in enumerate(ys)]
            left = [(cx - (4 + 70 * (j / 9) ** 1.6) * s, cy) for j, (cx, cy) in enumerate(cl)]
            right = [(cx + (4 + 70 * (j / 9) ** 1.6) * s, cy) for j, (cx, cy) in enumerate(cl)]
            d = _sm(left, closed=False) + " L" + " L".join(f"{_f(px)},{_f(py)}" for px, py in [right[-1]])
            d += " " + _sm(right[::-1], closed=False).replace("M", "L", 1) + " Z"
            bid = _uid("vbk", x0, x1, y, s)
            out += f"<defs>{S.lin_grad(bid, [(0, P['sea_pale']), (1, P['sea'])])}</defs>"
            out += _p(d, f"url(#{bid})", 3 * s)
            for j in range(2, 9):
                cx, cy = cl[j]
                w = (4 + 70 * (j / 9) ** 1.6) * s
                out += _p(f"M{_f(cx - w * 0.4)},{_f(cy)} q{_f(w * 0.2)},{_f(-3 * s)} {_f(w * 0.45)},0", sw=2.6 * s,
                          stroke=P["foam"], extra='opacity="0.8"')
                for sg in (-1, 1):
                    r = (3 + 6 * j / 9) * s
                    out += _ell(cx + sg * (w + r * 1.2), cy + rng.uniform(-8, 8) * s, r * 1.3, r * 0.8,
                                rng.choice(STONE_COLS), 2 * s)
    if part in ("all", "hills"):
        for side in (-1, 1):
            if side < 0:
                us = [-0.04 + 0.5 * i / 40 for i in range(41)]
                base = [(x0 + W * 0.36, bottom)]
            else:
                us = [0.54 + 0.5 * i / 40 for i in range(41)]
                base = [(x1 + W * 0.04, bottom)]
            pts = [(x0 + W * u, valley_ground(x0 + W * u, x0, x1, y, s)) for u in us]
            if side < 0:
                pts += [(x0 + W * 0.40, y + 0.25 * (bottom - y)), (x0 + W * 0.36, bottom), (x0 - W * 0.04, bottom)]
            else:
                pts = [(x0 + W * 0.64, bottom), (x0 + W * 0.60, y + 0.25 * (bottom - y))] + pts + [(x1 + W * 0.04, bottom)]
            d = _sm(pts, closed=True, tension=0.6)
            hid = _uid("vh", side, x0, x1, y, s)
            gid = hid + "g"
            defs = f"<defs>{S.lin_grad(gid, [(0, green_l), (0.5, green), (1, green_d)])}</defs>"
            inner = ""
            for _ in range(int(W / (30 * s))):
                u = rng.uniform(0.0, 0.5) if side < 0 else rng.uniform(0.5, 1.0)
                xx = x0 + W * u
                yy = rng.uniform(valley_ground(xx, x0, x1, y, s) + 10 * s, bottom)
                inner += _p(f"M{_f(xx)},{_f(yy)} q{_f(7 * s)},{_f(-5 * s)} {_f(14 * s)},0", sw=2.4 * s,
                            stroke=green_d, extra='opacity="0.55"')
            for _ in range(5):
                u = rng.uniform(0.02, 0.36) if side < 0 else rng.uniform(0.64, 0.98)
                xx = x0 + W * u
                yy = rng.uniform(valley_ground(xx, x0, x1, y, s) + 60 * s, bottom - 20 * s)
                inner += _p(S.blob(xx, yy, 26 * s, 14 * s, 0.12, 9, seed=int(xx)), "#c7b79a", 2.6 * s)
            out += defs + _p(d, f"url(#{gid})", 0) + _clip(hid, d, inner) + _p(d, "none", 4 * s)
        deco = ""
        for u, kind, sc in ((0.03, "olive", 0.32), (0.30, "bush", 0.45), (0.37, "bush", 0.35), (0.62, "bush", 0.4),
                            (0.97, "olive", 0.3), (0.71, "bush", 0.32)):
            xx = x0 + W * u
            yy = valley_ground(xx, x0, x1, y, s) + 6 * s
            deco += olive_tree(xx, yy, sc * s, seed=int(u * 100)) if kind == "olive" else bush(xx, yy, sc * s, variant=2)
        if camps:
            for u, sd, sc in ((0.07, "israel", 0.34), (0.16, "israel", 0.3), (0.24, "israel", 0.26),
                              (0.93, "philistine", 0.34), (0.84, "philistine", 0.3), (0.76, "philistine", 0.26)):
                xx = x0 + W * u
                deco += tent(xx, valley_ground(xx, x0, x1, y, s) + 4 * s, sc * s, 1 if sd == "israel" else -1, sd,
                             wave=wave + u)
        out += deco
    return out


def valley_elah(x0, x1, y, scale=1.0, part="all", camps=True, brook=True, seed=0, bottom=None, wave=0.0):
    return _place(_valley(x0, x1, y, scale, part, camps, brook, seed, bottom, wave), 0, 0, 1.0, filt="wobble")


# ====================================================================== 9. Noah film (Genesis 6-9)
# The ark, animals two by two, rain / flood / rainbow, building tools and food (module doc section 9).
TIMBER = "#b37b49"
TIMBER_LIGHT = "#d3a06a"
TIMBER_DARK = "#7c4e2c"
PITCH = "#3e322b"
OLIVE_LEAF = "#8ea66b"
OLIVE_LEAF_DARK = "#5f7647"
RAINBOW = ("#e86a5c", "#f29a4c", "#f5d05c", "#8cc463", "#5dbcb4", "#5f92d6", "#9c7bc8")     # 红橙黄绿青蓝紫
BOW_PINK = "#ec90a8"
RAIN_COL = "#b8d3e2"


def _nail_line(pts, sw=2.0, col=None):
    return _p(_sm(pts, closed=False), sw=sw, stroke=col or TIMBER_DARK, extra='opacity="0.7"')


def _bow(cx, cy, k=1.0, col=BOW_PINK, rot=0.0):
    """Little ribbon bow (the 'she' of an animal pair): two loops, two short tails, a round knot."""
    out = _p(f"M0,0 Q{_f(-16 * k)},{_f(-14 * k)} {_f(-20 * k)},{_f(-2 * k)} Q{_f(-16 * k)},{_f(10 * k)} 0,0 Z", col, 3)
    out += _p(f"M0,0 Q{_f(16 * k)},{_f(-14 * k)} {_f(20 * k)},{_f(-2 * k)} Q{_f(16 * k)},{_f(10 * k)} 0,0 Z", col, 3)
    out += _p(f"M{_f(-2 * k)},{_f(2 * k)} L{_f(-8 * k)},{_f(14 * k)} M{_f(2 * k)},{_f(2 * k)} L{_f(8 * k)},{_f(14 * k)}",
              sw=3.2 * max(0.7, k), stroke=S.shade(col, -0.25))
    out += _circ(0, 0, 4.5 * k, S.shade(col, -0.1), 2.4)
    return _g(out, f"translate({_f(cx)},{_f(cy)}) rotate({rot:.1f})")


# ---------------------------------------------------------------------- tools and timber
def _olive_leaf(length=44.0, col=None, rot=0.0):
    """A slim pointed olive leaf, stem end at (0, 0), pointing +x (then rotated by rot)."""
    col = col or OLIVE_LEAF
    L, w = length, length * 0.2
    d = f"M0,0 Q{_f(L * 0.35)},{_f(-w * 1.3)} {_f(L)},{_f(-w * 0.15)} Q{_f(L * 0.4)},{_f(w * 1.05)} 0,0 Z"
    out = _p(d, col, 2.6) + _p(f"M{_f(L * 0.05)},0 Q{_f(L * 0.5)},{_f(-w * 0.2)} {_f(L * 0.92)},{_f(-w * 0.12)}",
                                sw=1.5, stroke=S.shade(col, 0.45), extra='opacity="0.9"')
    out += _ell(L * 0.45, -w * 0.45, L * 0.18, w * 0.18, S.shade(col, 0.55), 0, extra='opacity="0.6"')
    return _g(out, f"rotate({rot:.1f})") if rot else out


def _olive_sprig(leaves=5, olives=True, length=110.0):
    """A small olive twig: stem end at (0, 0), growing toward +x, slim silver-green leaves in pairs."""
    out = _tube(f"M0,0 Q{_f(length * 0.5)},{_f(-length * 0.08)} {_f(length)},{_f(-length * 0.04)}", 4, TIMBER, 2.2)
    for i in range(leaves):
        t = (i + 1) / (leaves + 0.6)
        px, py = length * t, -length * 0.08 * math.sin(math.pi * t) * 0.9
        side = -1 if i % 2 == 0 else 1
        L = 44 * (1.0 - 0.25 * t)
        out += _g(_olive_leaf(L, OLIVE_LEAF if i % 2 else S.mix(OLIVE_LEAF, "#c9d3b0", 0.35), side * 38 - 6),
                  f"translate({_f(px)},{_f(py)})")
    out += _g(_olive_leaf(40, OLIVE_LEAF, -6), f"translate({_f(length * 0.97)},{_f(-length * 0.04)})")
    if olives:
        for (t, dy) in ((0.42, 12), (0.7, 11)):
            out += _ell(length * t, dy, 6, 7.5, "#5c4a63", 2.2) + _circ(length * t - 2, dy - 3, 1.8, HILITE, 0)
    return out


def olive_branch(x, y, scale=1.0, facing=1, rot=0.0, leaves=5, olives=True):
    return _place(_olive_sprig(leaves, olives), x, y, scale, facing, rot)


def olive_leaf(x, y, scale=1.0, facing=1, rot=0.0):
    return _place(_olive_leaf(44), x, y, scale, facing, rot)


def _saw_shape():
    """Hand saw: wooden grip around (0, 0), the blade runs +x to ~170 with teeth along its lower edge."""
    blade = "M22,-14 L168,-4 Q174,4 166,12.8 " + " ".join(
        f"L{_f(30 + (14 - i) * 9 + 4.5)},{_f(19.5)} L{_f(30 + (14 - i) * 9)},{_f(12.5)}" for i in range(15)) + " L22,14 Z"
    out = _p(blade, IRON, 3.2)
    out += _p("M30,-8 L160,-1", sw=3, stroke=S.shade(IRON, 0.45), extra='opacity="0.8"')
    out += _circ(150, 3, 3, S.shade(IRON, -0.3), 0)
    grip = "M-26,-22 Q-30,-2 -22,20 L26,18 L26,-18 Q8,-30 -26,-22 Z"
    out += _p(grip, TIMBER, 3.4)
    out += _p("M-14,-10 Q-16,2 -10,10 L12,9 L12,-10 Q0,-14 -14,-10 Z", PITCH, 2.6, extra='opacity="0.85"')
    out += _circ(18, -8, 2.5, CREAM, 0) + _circ(18, 8, 2.5, CREAM, 0)
    return out


def saw(x, y, scale=1.0, facing=1, rot=0.0):
    return _place(_saw_shape(), x, y, scale, facing, rot)


def _hammer_shape():
    """Hammer: grip at (0, 0), the wooden handle runs +x to 84, a stubby iron head across it at x~92."""
    out = _tube("M-14,0 L86,0", 10, TIMBER_LIGHT, 3.2)
    out += _p("M-10,-2 L40,-2", sw=2.4, stroke=S.shade(TIMBER_LIGHT, 0.4), extra='opacity="0.7"')
    out += _rect(78, -28, 26, 52, S.shade(IRON, -0.1), 3.4, rx=5)
    out += _rect(80, -32, 22, 10, S.shade(IRON, 0.15), 3, rx=3)
    out += _line(84, -20, 84, 14, sw=2.4, color=S.shade(IRON, 0.45), extra='opacity="0.8"')
    return out


def hammer(x, y, scale=1.0, facing=1, rot=0.0):
    return _place(_hammer_shape(), x, y, scale, facing, rot)


def _plank_shape(length=260.0, w=26.0, col=None, seed=0):
    """One plank, centred on (0, 0), along x."""
    col = col or TIMBER
    rng = random.Random(seed)
    L = length / 2
    out = _rect(-L, -w / 2, length, w, col, 3.4, rx=4)
    for k in range(2):
        yy = -w / 2 + w * (0.33 + 0.33 * k) + rng.uniform(-2, 2)
        x0 = -L + rng.uniform(10, 40)
        out += _p(f"M{_f(x0)},{_f(yy)} Q{_f(0)},{_f(yy + rng.uniform(-3, 3))} {_f(L - rng.uniform(10, 40))},{_f(yy)}",
                  sw=1.8, stroke=S.shade(col, -0.25), extra='opacity="0.7"')
    kx = rng.uniform(-L * 0.5, L * 0.5)
    out += _ell(kx, 0, 7, 3.5, S.shade(col, -0.2), 1.6)
    out += _line(-L + 4, -w / 2 + 3, L - 4, -w / 2 + 3, sw=2, color=S.shade(col, 0.35), extra='opacity="0.7"')
    return out


def plank(x, y, scale=1.0, rot=0.0, length=260, seed=0):
    return _place(_plank_shape(length, 26, None, seed), x, y, scale, 1, rot)


def _log_end(cx, cy, r, col=None):
    col = col or TIMBER
    out = _circ(cx, cy, r, S.shade(col, 0.3), 3.4)
    out += _circ(cx, cy, r * 0.62, "none", 1.8, stroke=S.shade(col, -0.1)) + _circ(cx, cy, r * 0.28, "none", 1.8,
                                                                                 stroke=S.shade(col, -0.1))
    out += _circ(cx, cy, r, "none", r * 0.18, stroke=S.shade(col, -0.25), extra='opacity="0.8"')
    out += _circ(cx, cy, r, "none", 3.4)
    return out


def _timber_pile(kind="mixed"):
    out = ""
    if kind in ("logs", "mixed"):
        # side view: logs stacked 3-2-1, their round ends toward the viewer, long bodies receding to the right
        rows = [(-70, -34, 34), (0, -34, 34), (70, -34, 34), (-35, -94, 33), (35, -94, 33)]
        if kind == "logs":
            rows.append((0, -152, 32))
        for cx, cy, r in rows:
            out += _p(f"M{_f(cx)},{_f(cy - r)} L{_f(cx + 130)},{_f(cy - r - 26)} L{_f(cx + 130)},{_f(cy + r - 26)} "
                      f"L{_f(cx)},{_f(cy + r)} Z", TIMBER_DARK, 3.4)
            out += _p(f"M{_f(cx + 20)},{_f(cy - r * 0.4 - 4)} L{_f(cx + 120)},{_f(cy - r * 0.4 - 24)}", sw=2,
                      stroke=S.shade(TIMBER_DARK, 0.3), extra='opacity="0.6"')
        for cx, cy, r in rows:
            out += _log_end(cx, cy, r)
    if kind in ("planks", "mixed"):
        base = -128 if kind == "mixed" else 0
        n = 4 if kind == "mixed" else 6
        for i in range(n):
            yy = base - 13 - i * 26
            dx = (i % 2) * 18 - 9
            out += _g(_plank_shape(250, 26, TIMBER if i % 2 else TIMBER_LIGHT, seed=i), f"translate({_f(dx + 20)},{_f(yy)})")
        if kind == "planks":
            out += _rect(-80, -6, 16, 8, TIMBER_DARK, 2.4) + _rect(100, -6, 16, 8, TIMBER_DARK, 2.4)
    return out


def timber_pile(x, y, scale=1.0, facing=1, kind="mixed"):
    return _place(_timber_pile(kind), x, y, scale, facing)


def _sawhorse(plank_=True):
    out = ""
    for x0 in (-96, 96):
        out += _tube(f"M{x0 - 22},0 L{x0},-108", 12, TIMBER_DARK, 3)
    out += _rect(-120, -118, 240, 18, TIMBER, 3.4, rx=3)
    for x0 in (-96, 96):
        out += _tube(f"M{x0 + 22},0 L{x0},-108", 12, TIMBER, 3)
        out += _line(x0 - 16, -46, x0 + 16, -46, sw=6, color=INK) + _line(x0 - 16, -46, x0 + 16, -46, sw=2.5,
                                                                         color=TIMBER_LIGHT)
    if plank_:
        out += _g(_plank_shape(330, 26, TIMBER_LIGHT, seed=3), "translate(30,-131)")
    return out


def sawhorse(x, y, scale=1.0, facing=1, plank=True):
    return _place(_sawhorse(plank), x, y, scale, facing)


def _nails(n=9, box=True):
    rng = random.Random(4)
    out = ""

    def nail(x, y, a, L=30):
        tx, ty = x + L * math.cos(math.radians(a)), y + L * math.sin(math.radians(a))
        return (_line(x, y, tx, ty, sw=6.5, color=INK) + _line(x, y, tx, ty, sw=3, color=S.shade(IRON, -0.05)) +
                _ell(x, y, 6.5, 3, S.shade(IRON, 0.1), 2.2, extra=f'transform="rotate({a + 90:.0f} {_f(x)} {_f(y)})"'))
    if box:
        for i in range(n):
            a = -90 + rng.uniform(-35, 35)
            out += nail(-34 + 68 * i / max(1, n - 1) + rng.uniform(-4, 4), -58 + rng.uniform(-6, 4), a + 180, 34)
        out += _p("M-50,-48 L50,-48 L46,0 L-46,0 Z", TIMBER, 3.6)
        out += _line(-48, -24, 48, -24, sw=2.2, color=TIMBER_DARK, extra='opacity="0.7"')
        out += _p("M-52,-50 L52,-50", sw=9, stroke=INK) + _p("M-52,-50 L52,-50", sw=4, stroke=TIMBER_LIGHT)
        for i in range(3):
            out += nail(64 + i * 22, -4 - (i % 2) * 6, rng.uniform(-20, 20) + (180 if i == 1 else 0), 28)
    else:
        for i in range(n):
            out += nail(rng.uniform(-50, 50), -4 - rng.uniform(0, 10), rng.uniform(-30, 30) + rng.choice((0, 180)), 28)
    return out


def nails(x, y, scale=1.0, box=True, n=9):
    return _place(_nails(n, box), x, y, scale)


def _pitch_bucket(brush=True):
    out = ""
    if brush:
        out += _tube("M10,-96 L54,-178", 8, TIMBER_LIGHT, 3)
    body = "M-44,-86 L44,-86 L36,0 L-36,0 Z"
    out += _p("M-46,-86 Q0,-128 46,-86", sw=5, stroke=INK) + _p("M-46,-86 Q0,-128 46,-86", sw=2.2, stroke=IRON)
    out += _p(body, TIMBER, 3.6)
    for yy in (-66, -18):
        out += _p(f"M{_f(-42 + (yy + 86) * 0.09)},{_f(yy)} L{_f(42 - (yy + 86) * 0.09)},{_f(yy)}", sw=7, stroke=INK)
        out += _p(f"M{_f(-42 + (yy + 86) * 0.09)},{_f(yy)} L{_f(42 - (yy + 86) * 0.09)},{_f(yy)}", sw=3.5,
                  stroke=S.shade(IRON, -0.1))
    out += _ell(0, -86, 44, 10, PITCH, 3.4)
    out += _ell(-12, -88, 14, 3, "#8c7a6c", 0, extra='opacity="0.8"')                     # glossy pitch
    out += _p("M-30,-80 Q-32,-62 -28,-52 Q-24,-60 -24,-80 Z", PITCH, 2.4)               # drips down the side
    out += _p("M16,-80 Q16,-70 19,-64 Q22,-70 22,-80 Z", PITCH, 2.2)
    if brush:
        out += _p("M-6,-104 L18,-112 L22,-84 L2,-80 Z", PITCH, 3)                          # brush head in the pitch
        out += _rect(4, -118, 20, 12, TIMBER_DARK, 2.6, rx=2, extra='transform="rotate(-20 14 -112)"')
    return out


def pitch_bucket(x, y, scale=1.0, facing=1, brush=True):
    return _place(_pitch_bucket(brush), x, y, scale, facing)


# ---------------------------------------------------------------------- food for people and animals
def _fruit(cx, cy, kind, r=15):
    if kind == "apple":
        return (_circ(cx, cy, r, "#e0614f", 3) + _ell(cx - r * 0.35, cy - r * 0.35, r * 0.25, r * 0.16, HILITE, 0,
                                                      extra='opacity="0.7"') +
                _line(cx, cy - r, cx + 2, cy - r - 7, sw=2.6) + _olive_leaf_small(cx + 3, cy - r - 4))
    if kind == "pear":
        return _p(f"M{_f(cx)},{_f(cy - r * 1.3)} Q{_f(cx + r * 0.6)},{_f(cy - r * 0.6)} {_f(cx + r)},{_f(cy + r * 0.3)} "
                  f"Q{_f(cx)},{_f(cy + r * 1.4)} {_f(cx - r)},{_f(cy + r * 0.3)} Q{_f(cx - r * 0.6)},{_f(cy - r * 0.6)} "
                  f"{_f(cx)},{_f(cy - r * 1.3)} Z", "#c9cf5a", 3)
    if kind == "grapes":
        out = ""
        for i, (dx, dy) in enumerate(((-8, -8), (8, -8), (0, 0), (-10, 6), (10, 6), (0, 12), (0, -16))):
            out += _circ(cx + dx, cy + dy, 7.5, "#8a5aa8" if i % 2 else "#7a4c98", 2.2)
        return out
    if kind == "carrot":
        return (_p(f"M{_f(cx - 8)},{_f(cy - 14)} L{_f(cx + 8)},{_f(cy - 14)} L{_f(cx + 1)},{_f(cy + 26)} Z", "#ee8a3c", 2.8) +
                _p(f"M{_f(cx)},{_f(cy - 14)} q-8,-14 -4,-20 M{_f(cx)},{_f(cy - 14)} q6,-14 2,-22", sw=4,
                   stroke=P["leaf"]))
    if kind == "melon":
        return (_ell(cx, cy, r * 1.5, r * 1.2, "#7fae55", 3) +
                _p(f"M{_f(cx - r)},{_f(cy - r * 0.6)} Q{_f(cx)},{_f(cy - r * 1.2)} {_f(cx + r)},{_f(cy - r * 0.6)} "
                   f"M{_f(cx - r * 1.3)},{_f(cy)} Q{_f(cx)},{_f(cy - r * 0.4)} {_f(cx + r * 1.3)},{_f(cy)}", sw=2.4,
                   stroke=S.shade("#7fae55", -0.3)))
    return ""


def _olive_leaf_small(cx, cy):
    return _g(_olive_leaf(14, P["leaf"], -30), f"translate({_f(cx)},{_f(cy)})")


def _food_basket(kind="fruit"):
    """Wicker basket (rim y=-56) heaped with food. kind: fruit | grain | veg | bread."""
    if kind == "bread":
        return _bread_basket(handle=False)
    out = ""
    if kind == "fruit":
        out += _fruit(-30, -64, "pear") + _fruit(26, -66, "grapes") + _fruit(-6, -72, "apple", 16)
        out += _fruit(40, -60, "apple", 13) + _fruit(-46, -60, "apple", 13)
    elif kind == "grain":
        out += _p("M-56,-56 Q-40,-92 0,-96 Q40,-92 56,-56 Z", "#e8c46a", 3.4)
        rng = random.Random(2)
        for _ in range(22):
            gx, gy = rng.uniform(-44, 44), rng.uniform(-88, -62)
            if abs(gx) < 52 - (gy + 96) * 0.1 and (gy + 96) > abs(gx) * 0.35:
                out += _ell(gx, gy, 3.6, 2.2, "#c99a3c", 0, extra=f'transform="rotate({rng.uniform(-40, 40):.0f} {_f(gx)} {_f(gy)})"')
        for xx in (-20, 6, 28):
            out += _tube(f"M{xx},-70 Q{xx + 6},-110 {xx + 14},-126", 3, "#d9b25a", 1.8)
            for k in range(4):
                out += _ell(xx + 6 + k * 2.4, -100 - k * 7, 3.6, 6, "#e8c46a", 1.8)
    elif kind == "veg":
        out += _fruit(-34, -66, "carrot") + _fruit(-18, -70, "carrot") + _fruit(18, -64, "melon", 16)
        out += _p("M-4,-58 Q-8,-90 14,-92 Q30,-88 26,-60 Z", "#8cbf5a", 3) + _p("M10,-62 L10,-88", sw=2,
                                                                                 stroke=S.shade("#8cbf5a", -0.3))
    body = "M-60,-58 L60,-58 Q58,-22 46,-4 Q44,0 36,0 L-36,0 Q-44,0 -46,-4 Q-58,-22 -60,-58 Z"
    weave = ""
    for k, yy in enumerate(range(-50, 0, 10)):
        off = 7 if k % 2 else 0
        for xx in range(-70 + off, 70, 14):
            weave += f"M{xx},{yy} q7,-5 14,0 "
    for xx in range(-48, 56, 16):
        weave += f"M{xx},-56 L{xx * 0.78:.1f},-2 "
    out += _p(body, WICKER, 0) + _clip(_uid("fbsk", kind), body, _p(weave, sw=2.0, stroke=S.shade(WICKER, -0.3)))
    out += _p(body, sw=3.8)
    out += _tube("M-62,-58 L62,-58", 9, S.shade(WICKER, 0.12), 3.2)
    return out


def food_basket(x, y, scale=1.0, kind="fruit"):
    return _place(_food_basket(kind), x, y, scale)


HAY = "#e6c060"


def _hay(kind="bale"):
    out = ""
    rng = random.Random({"bale": 1, "bundle": 2, "pile": 3}.get(kind, 0))
    dk = S.shade(HAY, -0.28)
    if kind == "bale":
        out += _p("M-80,-92 L-58,-108 L92,-108 L80,-92 Z", S.shade(HAY, 0.2), 3.6)
        out += _p("M80,-92 L92,-108 L92,-14 L80,0 Z", S.shade(HAY, -0.12), 3.6)
        out += _rect(-80, -92, 160, 92, HAY, 3.6, rx=8)
        for _ in range(26):
            x0, y0 = rng.uniform(-72, 70), rng.uniform(-84, -8)
            out += _line(x0, y0, x0 + rng.uniform(10, 22), y0 + rng.uniform(-3, 3), sw=1.8, color=dk, extra='opacity="0.6"')
        for xx in (-36, 36):
            out += _p(f"M{xx},-92 L{xx},0 M{xx},-92 L{xx + 12},-108", sw=5, stroke=TIMBER_DARK)
        for _ in range(8):
            x0 = rng.uniform(-70, 70)
            out += _line(x0, -92, x0 + rng.uniform(-8, 8), -104 - rng.uniform(0, 8), sw=2, color=dk)
    elif kind == "bundle":           # a sheaf tied in the middle (anchor: bottom centre of the lying sheaf)
        out += _p("M-90,-30 Q-60,-58 -10,-40 Q60,-62 96,-34 Q60,-6 -10,-20 Q-60,-2 -90,-30 Z", HAY, 3.4)
        for _ in range(16):
            x0, y0 = rng.uniform(-80, 80), rng.uniform(-44, -18)
            out += _line(x0, y0, x0 + rng.uniform(12, 24), y0 + rng.uniform(-3, 3), sw=1.8, color=dk, extra='opacity="0.6"')
        out += _ell(-8, -30, 9, 18, TIMBER_DARK, 3)
    else:                            # pile: a soft heap of loose hay
        out += _p("M-110,0 Q-90,-46 -40,-64 Q0,-84 44,-62 Q96,-44 112,0 Z", HAY, 3.6)
        for _ in range(34):
            x0, y0 = rng.uniform(-90, 90), rng.uniform(-60, -8)
            if abs(x0) < 100 + y0 * 1.1:
                out += _line(x0, y0, x0 + rng.uniform(-14, 14), y0 + rng.uniform(-6, 6), sw=1.8, color=dk, extra='opacity="0.6"')
        for _ in range(9):
            x0 = rng.uniform(-80, 80)
            yt = -60 + abs(x0) * 0.45
            out += _line(x0, yt + 4, x0 + rng.uniform(-10, 10), yt - 12, sw=2, color=dk)
    return out


def hay(x, y, scale=1.0, facing=1, kind="bale"):
    return _place(_hay(kind), x, y, scale, facing)


# ---------------------------------------------------------------------- the altar (Genesis 8:20)
def _flame(phase=0.0, k=1.0):
    ph = 2 * math.pi * phase
    sway = 8 * math.sin(ph)
    h = 92 * k * (1 + 0.08 * math.sin(2 * ph))
    outer = (f"M{_f(-34 * k)},0 Q{_f(-40 * k)},{_f(-h * 0.45)} {_f(-10 * k + sway * 0.4)},{_f(-h * 0.7)} "
             f"Q{_f(-4 * k)},{_f(-h * 0.88)} {_f(sway)},{_f(-h)} Q{_f(14 * k + sway * 0.5)},{_f(-h * 0.7)} "
             f"{_f(26 * k)},{_f(-h * 0.55)} Q{_f(40 * k)},{_f(-h * 0.3)} {_f(34 * k)},0 Z")
    hi = h * 0.62
    inner = (f"M{_f(-18 * k)},0 Q{_f(-20 * k)},{_f(-hi * 0.5)} {_f(sway * 0.6)},{_f(-hi)} "
             f"Q{_f(18 * k)},{_f(-hi * 0.5)} {_f(18 * k)},0 Z")
    return _p(outer, "#f3a243", 3.2) + _p(inner, "#fbd66b", 0) + _ell(0, -8 * k, 10 * k, 6 * k, "#fff0b8", 0)


def _altar(fire=1.0, phase=0.0, smoke=True):
    out = ""
    fire = _clamp(fire)
    if fire > 0:
        gid = _uid("altglow", round(fire, 2))
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.85 * fire), (1, P["glow"], 0)])}</defs>'
                f'<ellipse cx="0" cy="-150" rx="{_f(170 * (0.6 + 0.4 * fire))}" ry="{_f(150 * (0.6 + 0.4 * fire))}" '
                f'fill="url(#{gid})"/>')
    if smoke and fire > 0:
        ph = phase * 2 * math.pi
        for j in range(3):
            yy = -230 - j * 70 - 30 * ((phase + j / 3) % 1)
            xx = 16 * math.sin(ph + j * 1.7) + j * 10
            r = 22 + j * 9
            out += _circ(xx, yy, r * 0.8, "#efeae2", 0, extra=f'opacity="{0.45 - 0.1 * j:.2f}"')
            out += _p(f"M{_f(xx - r * 0.6)},{_f(yy + r * 0.2)} q{_f(r * 0.4)},{_f(-r * 0.7)} {_f(r * 0.9)},{_f(-r * 0.3)}",
                      sw=2.4, stroke=S.shade("#e7e1d6", -0.3), extra=f'opacity="{0.5 - 0.1 * j:.2f}"')
    stones = [(-78, -26, 36, 26), (-18, -24, 38, 25), (44, -26, 38, 27), (92, -22, 26, 22), (-100, -20, 22, 20),
              (-52, -72, 36, 24), (10, -74, 38, 26), (66, -70, 32, 24), (-20, -114, 46, 20), (40, -112, 34, 19)]
    for i, (cx, cy, rx, ry) in enumerate(stones):
        col = STONE_COLS[i % len(STONE_COLS)]
        out += _p(S.blob(cx, cy, rx, ry, 0.08, 9, seed=i + 3), col, 3.6)
        out += _ell(cx - rx * 0.3, cy - ry * 0.45, rx * 0.35, ry * 0.18, HILITE, 0, extra='opacity="0.45"')
    # sticks on top
    for x0, x1, yy in ((-56, 56, -134), (-48, 50, -142), (-30, 60, -128)):
        out += _tube(f"M{x0},{yy} L{x1},{yy - 8}", 9, TIMBER_DARK, 3)
    if fire > 0:
        out += _g(_flame(phase, 0.55 + 0.45 * fire), "translate(4,-136)")
    return out


def altar(x, y, scale=1.0, fire=1.0, phase=0.0, smoke=True):
    return _place(_altar(fire, phase, smoke), x, y, scale)


# ---------------------------------------------------------------------- weather and water
def _raindrop_d(x, y, s):
    return (f"M{_f(x)},{_f(y - 1.6 * s)} C{_f(x + 0.3 * s)},{_f(y - 1.0 * s)} {_f(x + 0.85 * s)},{_f(y - 0.45 * s)} "
            f"{_f(x + 0.85 * s)},{_f(y + 0.3 * s)} A{_f(0.85 * s)},{_f(0.85 * s)} 0 0 1 {_f(x - 0.85 * s)},{_f(y + 0.3 * s)} "
            f"C{_f(x - 0.85 * s)},{_f(y - 0.45 * s)} {_f(x - 0.3 * s)},{_f(y - 1.0 * s)} {_f(x)},{_f(y - 1.6 * s)} Z")


def rain(phase=0.0, intensity=0.6, x0=0, y0=0, x1=None, y1=None, angle=10.0, seed=0, color=None, drops=None,
         scale=1.0):
    """Rain layer in absolute stage coordinates (see module doc)."""
    x1 = S.W if x1 is None else x1
    y1 = S.H if y1 is None else y1
    it = _clamp(intensity, 0.0, 1.5)
    col = color or RAIN_COL
    drops = it < 0.3 if drops is None else drops
    rng = random.Random(seed)
    span_y = (y1 - y0) + 240
    tan = math.tan(math.radians(angle))
    n = int(((x1 - x0) * span_y) / (2112 * 1188) * (60 + 900 * it) / max(0.4, scale))
    out = []
    for _ in range(n):
        bx = rng.uniform(x0 - 100, x1 + 100)
        by = rng.uniform(0, span_y)
        v = rng.uniform(0.75, 1.25)
        yy = (by + phase * span_y * v) % span_y + y0 - 120
        xx = bx - (yy - y0) * tan
        L = (40 + 70 * it) * rng.uniform(0.6, 1.2) * scale
        if drops:
            s = rng.uniform(8, 12) * scale
            out.append(f'<path d="{_raindrop_d(xx, yy, s)}" fill="{col}" stroke="{S.shade(col, -0.35)}" '
                       f'stroke-width="{_f(1.8 * scale)}" opacity="0.9"/>')
        else:
            op = rng.uniform(0.45, 0.85)
            out.append(f'<path d="M{_f(xx)},{_f(yy)} l{_f(-L * tan)},{_f(L)}" stroke="{col}" '
                       f'stroke-width="{_f(rng.uniform(2.2, 4.0) * scale)}" stroke-linecap="round" opacity="{op:.2f}"/>')
    cid = _uid("rainclip", x0, y0, x1, y1)
    return (f'<clipPath id="{cid}"><rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}"/>'
            f'</clipPath><g clip-path="url(#{cid})">{"".join(out)}</g>')


def _puddle(w=260.0, ripple=0.0, splash=0.0, sky=None):
    sky = sky or "#cfe3ea"
    h = w * 0.2
    out = _ell(0, 0, w / 2 + 6, h / 2 + 4, S.shade(P["earth"], -0.15), 0, extra='opacity="0.45"')
    pd = f"M{_f(-w / 2)},0 Q{_f(-w / 2)},{_f(-h / 2)} {_f(-w * 0.1)},{_f(-h / 2)} Q{_f(w * 0.25)},{_f(-h * 0.62)} " \
         f"{_f(w / 2)},{_f(-h * 0.1)} Q{_f(w * 0.48)},{_f(h * 0.5)} 0,{_f(h / 2)} Q{_f(-w / 2)},{_f(h * 0.5)} {_f(-w / 2)},0 Z"
    gid = _uid("pudg", w)
    out += (f'<defs>{S.lin_grad(gid, [(0, S.shade(sky, 0.3)), (1, S.shade(sky, -0.2))])}</defs>'
            f'<path d="{pd}" fill="url(#{gid})" {_st(3.2, S.shade(sky, -0.5))}/>')
    out += _ell(-w * 0.18, -h * 0.15, w * 0.16, h * 0.12, HILITE, 0, extra='opacity="0.6"')
    rp = ripple % 1.0
    inner = ""
    for j in range(3):
        t = (rp + j / 3) % 1.0
        cx = [(-w * 0.2), (w * 0.18), (0)][j]
        inner += _ell(cx, 0, 12 + t * w * 0.22, (12 + t * w * 0.22) * 0.25, "none", 2.2,
                      stroke=S.shade(sky, 0.55), extra=f'opacity="{0.9 * (1 - t):.2f}"')
    out += _clip(_uid("pudc", w, round(rp, 3)), pd, inner)
    sp = _clamp(splash)
    if sp > 0:
        a = math.sin(math.pi * sp)
        out += _ell(0, -2, w * 0.2 * (0.6 + 0.4 * sp), h * 0.22 * (0.6 + 0.4 * sp), "none", 2.6,
                    stroke=S.shade(sky, 0.5), extra=f'opacity="{1 - 0.6 * sp:.2f}"')
        crown = ""
        for k in range(-3, 4):
            if k == 0:
                continue
            hgt = (36 - 6 * abs(k)) * a + 4
            bx = k * w * 0.05 * (0.6 + 0.6 * sp)
            tx_, ty_ = bx * 1.5, -hgt
            crown += (f'<path d="M{_f(bx - 6)},0 Q{_f(bx * 1.25)},{_f(-hgt * 0.5)} {_f(tx_ - 3)},{_f(ty_ + 6)} '
                      f'L{_f(tx_ + 3)},{_f(ty_ + 6)} Q{_f(bx * 1.2 + 4)},{_f(-hgt * 0.4)} {_f(bx + 6)},0 Z" '
                      f'fill="{S.shade(sky, 0.25)}" {_st(2.2, S.shade(sky, -0.45))}/>')
            crown += f'<circle cx="{_f(tx_)}" cy="{_f(ty_)}" r="5.5" fill="{S.shade(sky, 0.25)}" {_st(2.2, S.shade(sky, -0.45))}/>'
        out += f'<g opacity="{0.4 + 0.6 * a:.2f}">{crown}</g>' if a > 0.05 else ""
        for k in range(8):
            ang = math.radians(-160 + k * 140 / 7)
            dist = w * (0.12 + 0.42 * sp)
            dx = math.cos(ang) * dist
            dy = math.sin(ang) * dist * 0.9 + w * 0.6 * sp * sp * 0.8
            if dy < h * 0.4:
                s = 9 * (1 - 0.35 * sp)
                out += f'<path d="{_raindrop_d(dx, dy - 4, s)}" fill="{S.shade(sky, 0.2)}" {_st(2, S.shade(sky, -0.45))}/>'
    return out


def puddle(x, y, scale=1.0, width=260, ripple=0.0, splash=0.0, sky=None):
    return _place(_puddle(width, ripple, splash, sky), x, y, scale)


def flood_sea(x0, x1, level, phase=0.0, bottom=None, storm=0.0, seed=0, scale=1.0, foam=True):
    """Wide flood water in absolute stage coordinates (see module doc)."""
    bottom = S.H + 60 if bottom is None else bottom
    st = _clamp(storm)
    ph = 2 * math.pi * (phase % 1.0)
    calm = [P["sea_light"], P["sea"], S.mix(P["sea"], P["sea_deep"], 0.5), P["sea_deep"]]
    rough = [P["storm_sea_light"], S.mix(P["storm_sea_light"], P["storm_sea"], 0.5), P["storm_sea"],
             S.shade(P["storm_sea"], -0.2)]
    cols = [S.mix(a, b, st) for a, b in zip(calm, rough)]
    out = []
    bands = [(0, 9, 260, 0.6), (34, 13, 320, 1.0), (92, 17, 380, 1.5), (176, 22, 460, 2.1)]
    for i, (dy, amp, wl, sp) in enumerate(bands):
        y = level + dy * scale
        a = amp * scale * (1 + 1.6 * st)
        wlen = wl * scale
        d = S.wave_band(y, a, wlen, ph * (1 if i % 2 == 0 else -1) + i * 1.3, x0=x0 - 40, x1=x1 + 40, bottom=bottom,
                        jitter=0, seed=seed + i)
        out.append(f'<path d="{d}" fill="{cols[i]}" {_st(3.4 * scale)}/>' if i == 0 else
                   f'<path d="{d}" fill="{cols[i]}" {_st(3.0 * scale, S.shade(cols[i], -0.35))}/>')
        if foam:
            fl = S.wave_line(y - a * 0.25, a * 0.7, wlen, ph * (1 if i % 2 == 0 else -1) + i * 1.3 + 0.5, x0=x0 - 40,
                             x1=x1 + 40)
            out.append(f'<path d="{fl}" fill="none" stroke="{P["foam"]}" stroke-width="{_f((3 + 2 * st) * scale)}" '
                       f'stroke-linecap="round" stroke-dasharray="{_f(wlen * 0.22)} {_f(wlen * 0.3)}" opacity="{0.55 + 0.3 * st:.2f}"/>')
    cid = _uid("floodc", x0, x1, bottom)
    body = "".join(out)
    return (f'<clipPath id="{cid}"><rect x="{_f(x0)}" y="{_f(level - 200 * scale)}" width="{_f(x1 - x0)}" '
            f'height="{_f(bottom - level + 200 * scale)}"/></clipPath><g filter="url(#wobble)"><g clip-path="url(#{cid})">{body}</g></g>')


def _dark_cloud(w=620.0, h=230.0, seed=0, light=0.0, flash=0.0):
    base = S.mix(P["storm_cloud"], P["storm_cloud_light"], _clamp(light))
    under = S.shade(base, -0.25)
    out = S.cloud(0, 0, w, h, fill=base, seed=seed, puffs=6, sw=4, shade_fill=under)
    lite = S.shade(base, 0.12)                     # a lighter front bank of puffs gives the cloud depth
    out += S.cloud(-w * 0.08, h * 0.12, w * 0.62, h * 0.55, fill=lite, seed=seed + 11, puffs=4, sw=3)
    rng = random.Random(seed)
    for _ in range(4):
        cx, cy = rng.uniform(-w * 0.32, w * 0.3), rng.uniform(-h * 0.5, -h * 0.1)
        out += _p(f"M{_f(cx - 30)},{_f(cy)} Q{_f(cx)},{_f(cy - 18)} {_f(cx + 34)},{_f(cy - 4)}", sw=3,
                  stroke=S.shade(base, 0.3), extra='opacity="0.6"')
    if flash > 0:
        gid = _uid("cloudflash", w, h)
        out += (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.75), (0.6, P["glow"], 0.25), (1, P["glow"], 0)])}</defs>'
                f'<ellipse cx="0" cy="{_f(-h * 0.05)}" rx="{_f(w * 0.42)}" ry="{_f(h * 0.42)}" fill="url(#{gid})" '
                f'opacity="{_clamp(flash):.2f}"/>')
    return out


def dark_cloud(x, y, scale=1.0, width=620, height=230, seed=0, light=0.0, flash=0.0):
    return _place(_dark_cloud(width, height, seed, light, flash), x, y, scale, 1, filt="wobble")


def _rainbow(progress=1.0, r=900.0, band=30.0, glow=True):
    pr = _clamp(progress) * 7
    out = ""
    if glow and pr > 0:
        out += f'<path d="M{_f(-r - band)},0 A{_f(r + band)},{_f(r + band)} 0 0 1 {_f(r + band)},0" fill="none" ' \
               f'stroke="{P["glow"]}" stroke-width="{_f(band * 9)}" opacity="{0.35 * min(1, pr / 7):.2f}" filter="url(#blur-md)"/>'
    for i, col in enumerate(RAINBOW):
        f = _clamp(pr - i)
        if f <= 0:
            continue
        rr = r - i * band
        a = math.pi * (1 - f)                     # the band sweeps in from the left foot over the top to the right
        ex, ey = rr * math.cos(a), -rr * math.sin(a)
        large = 0
        d = f"M{_f(-rr)},0 A{_f(rr)},{_f(rr)} 0 {large} 1 {_f(ex)},{_f(ey)}"
        out += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{_f(band + 1.5)}" stroke-linecap="butt" ' \
               f'opacity="0.92"/>'
    mid = _uid("rbmask", r, band)
    lid = _uid("rbfade", r, band)
    span = r + band
    mask = (f'<defs><linearGradient id="{lid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.72" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="{_f(-span * 1.6)}" y="{_f(-span * 1.6)}" '
            f'width="{_f(span * 3.2)}" height="{_f(span * 1.7)}"><rect x="{_f(-span * 1.6)}" y="{_f(-span * 1.1)}" '
            f'width="{_f(span * 3.2)}" height="{_f(span * 1.1)}" fill="url(#{lid})"/></mask></defs>')
    return mask + f'<g mask="url(#{mid})">{out}</g>'


def rainbow(x, y, scale=1.0, progress=1.0, radius=900, band=30, glow=True):
    return _place(_rainbow(progress, radius, band, glow), x, y, scale, 1, filt=None)


# ---------------------------------------------------------------------- the ark
ARK_DOOR = (150, -560, 410, -170)          # door opening x0, top, x1, sill (local, grounded, facing right)
ARK_WINDOW = (-520, -860, -280, -630)      # the high window opening x0, top, x1, sill
ARK_WINDOW_STAND = (-400, -480)            # anchor for a person standing inside at the high window
ARK_RAMP = ((150, -170), (440, -170), (980, 0))   # landing start, top of the slope, foot on the ground
ARK_DECK_Y = -605                          # floor of the top deck (cabin) / top of the hull
ARK_ROOF_Y = -1010                         # roof ridge
ARK_LEN = 1915                             # hull length (stern -950 .. bow +965)
ARK_DRAFT = 150                            # floating=True: the keel sits this far below the waterline
ARK_HULL = "#a36b40"
ARK_CABIN = "#c99060"
ARK_ROOF = "#87523a"
ARK_BAND = "#4f8f8a"


def _ark_sheer(x):
    return -610 - 40 * (abs(x) / 950) ** 4


def _ark_keel(x):
    ax = abs(x)
    if ax <= 900:
        return -300 * (ax / 900) ** 3
    return -300 - (ax - 900) * 4


def _ark_hull_pts():
    top = [(x, _ark_sheer(x)) for x in [-950 + i * (1915 / 24) for i in range(25)]]
    bow = [(978, -560), (968, -450), (940, -370)]
    keel = [(x, _ark_keel(x)) for x in [900 - i * 75 for i in range(25)]]
    stern = [(-930, -380), (-955, -470), (-962, -565)]
    return top + bow + keel + stern


def _ark_row_y(x, t):
    k = _ark_keel(max(-900, min(900, x)))
    return k + (_ark_sheer(x) - k) * t


def _ark_ramp():
    (lx0, ly), (tx, ty), (bx, by) = ARK_RAMP
    th = 22
    out = ""
    for px in (640, 860):                                  # posts under the slope
        yy = ty + (by - ty) * (px - tx) / (bx - tx)
        if yy < -12:
            out += _rect(px - 9, yy, 18, -yy, TIMBER_DARK, 3.2)
    dep = 46                                               # the walking surface recedes toward the hull
    deck = [(lx0 - 10, ly - dep), (tx + 12, ty - dep), (bx + 4, by - dep * 0.7), (bx + 10, by), (tx, ty), (lx0 - 10, ly)]
    out += _p(_poly(deck), TIMBER_LIGHT, 3.4)
    for k in (0.33, 0.66):                                  # board seams along the ramp
        a_ = [(lx0 - 10, ly - dep * k), (tx + 12 * k, ty - dep * k), (bx + 10 - 6 * k, by - dep * 0.7 * k)]
        out += _p(_poly(a_, closed=False), sw=2.2, stroke=TIMBER_DARK, extra='opacity="0.6"')
    surf = [(lx0 - 10, ly), (tx, ty), (bx + 10, by)]
    under = [(bx + 10, by + 4), (bx - 26, by + 4), (tx + 6, ty + th), (lx0 - 10, ly + th)]
    d = _poly(surf + under)
    out += _p(d, TIMBER, 3.6)
    L = math.hypot(bx - tx, by - ty)
    n = int(L / 64)
    for i in range(1, n):                                   # cleats across the boards so the animals don't slip
        t = i / n
        cx, cy = tx + (bx - tx) * t, ty + (by - ty) * t
        out += _p(f"M{_f(cx)},{_f(cy - 3)} L{_f(cx + 8)},{_f(cy - dep * (1 - 0.3 * t) + 4)}", sw=6, stroke=INK)
        out += _p(f"M{_f(cx)},{_f(cy - 3)} L{_f(cx + 8)},{_f(cy - dep * (1 - 0.3 * t) + 4)}", sw=2.6, stroke=TIMBER_DARK)
    for xx in range(int(lx0) + 30, int(tx), 60):
        out += _line(xx, ly + 3, xx, ly + th - 3, sw=2, color=TIMBER_DARK, extra='opacity="0.7"')
    return out


def _ark_door_svg(door, glow, glow_only=False):
    x0, top, x1, sill = ARK_DOOR
    w, h = x1 - x0, sill - top
    out = ""
    if glow_only:
        return _ark_door_glow(x0, top, w, h, glow)
    op = _clamp(door)
    gid = _uid("arkin", round(op, 3))
    out += (f'<defs>{S.rad_grad(gid, [(0, "#8a5a36"), (0.6, "#4e3426"), (1, "#3a281f")], cx=0.5, cy=0.8, r=0.8)}</defs>'
            f'<rect x="{x0}" y="{top}" width="{w}" height="{h}" fill="url(#{gid})"/>')
    if op > 0:                                              # straw on the floor, a post and a lamp glow inside
        out += _p(f"M{x0 + 6},{sill - 2} Q{x0 + w * 0.3},{sill - 26} {x0 + w * 0.6},{sill - 12} Q{x0 + w * 0.8},{sill - 24} "
                  f"{x1 - 6},{sill - 4} Z", "#c9a050", 0, extra='opacity="0.8"')
        out += _rect(x0 + w * 0.62, top + 10, 16, h - 20, "#3a281f", 0, extra='opacity="0.7"')
        out += _line(x0 + w * 0.32, top, x0 + w * 0.32, top + 40, sw=3, color="#2a1d16")
        out += _g(_lantern_body(True, False, _uid("arklamp")), f"translate({_f(x0 + w * 0.32)},{_f(top + 40)}) scale(0.62)")
    # frame
    out += _rect(x0 - 16, top - 18, w + 32, 22, TIMBER_DARK, 3.4, rx=4)
    out += _rect(x0 - 14, top - 4, 16, h + 4, TIMBER_DARK, 3, rx=2) + _rect(x1 - 2, top - 4, 16, h + 4, TIMBER_DARK, 3, rx=2)
    out += _rect(x0 - 20, sill - 4, w + 40, 16, TIMBER_LIGHT, 3.4, rx=4)
    # the panel, hinged on the left jamb, swinging out toward the viewer
    th = math.pi * 0.96 * op
    fx = x0 + w * math.cos(th) - 18 * math.sin(th)
    e = 30 * math.sin(th)
    if abs(fx - x0) > 3:
        pts = [(x0, top + 2), (fx, top + 2 - e), (fx, sill - 2 + e * 0.6), (x0, sill - 2)]
        face = ARK_CABIN if th <= math.pi / 2 else S.shade(ARK_CABIN, -0.15)
        out += _p(_poly(pts), face, 4)
        for k in range(1, 5):
            a, b = _lerp2(pts[0], pts[1], k / 5), _lerp2(pts[3], pts[2], k / 5)
            out += _line(a[0], a[1] + 4, b[0], b[1] - 4, sw=2.2, color=S.shade(face, -0.3))
        for t in (0.14, 0.86):
            a, b = _lerp2(pts[0], pts[3], t), _lerp2(pts[1], pts[2], t)
            out += _p(_poly([(a[0], a[1] - 9), (b[0], b[1] - 9), (b[0], b[1] + 9), (a[0], a[1] + 9)]),
                      S.shade(face, -0.12), 3)
        a, b = _lerp2(pts[0], pts[3], 0.86), _lerp2(pts[1], pts[2], 0.14)        # Z brace
        out += _p(f"M{_f(a[0])},{_f(a[1])} L{_f(b[0])},{_f(b[1])}", sw=16, stroke=INK)
        out += _p(f"M{_f(a[0])},{_f(a[1])} L{_f(b[0])},{_f(b[1])}", sw=9, stroke=S.shade(face, -0.12))
        for t in (0.14, 0.86):
            a = _lerp2(pts[0], pts[3], t)
            out += _circ(a[0] + 4, a[1], 6, S.shade(IRON, -0.2), 2.2)
        if abs(fx - x0) > 40:
            k = _lerp2(pts[1], pts[2], 0.5)
            out += _circ(k[0] - 16 * (1 if th <= math.pi / 2 else -1), k[1], 9, S.shade(IRON, -0.15), 2.6)
    return out


def _ark_door_glow(x0, top, w, h, glow):
    out = ""
    g_ = _clamp(glow)
    if g_ > 0:
        out += (f'<rect x="{x0 - 8}" y="{top - 8}" width="{w + 16}" height="{h + 12}" fill="none" stroke="{P["glow"]}" '
                f'stroke-width="{_f(30 * g_)}" opacity="{0.55 * g_:.2f}" filter="url(#blur-md)"/>'
                f'<rect x="{x0 - 1}" y="{top - 1}" width="{w + 2}" height="{h + 2}" fill="none" stroke="{P["gold"]}" '
                f'stroke-width="{_f(7 * g_ + 1)}" opacity="{0.9 * g_:.2f}"/>')
    return out


def _ark_shutter(sx, op, x0, top, x1, sill, col):
    """One window shutter hinged at the left (sx=-1) or right (sx=1) jamb; op 0 closed .. 1 flat on the wall."""
    hw = (x1 - x0) / 2
    hx = x0 if sx < 0 else x1
    th = math.pi * _clamp(op)
    fx = hx - sx * (hw * math.cos(th) + 14 * math.sin(th))
    e = 16 * math.sin(th)
    pts = [(hx, top + 2), (fx, top + 2 - e), (fx, sill - 2 + e * 0.7), (hx, sill - 2)]
    face = col if th <= math.pi / 2 else S.shade(col, -0.12)
    out = _p(_poly(pts), face, 3.6)
    for k in (0.33, 0.66):
        a, b = _lerp2(pts[0], pts[1], k), _lerp2(pts[3], pts[2], k)
        out += _line(a[0], a[1] + 6, b[0], b[1] - 6, sw=2.2, color=S.shade(face, -0.3))
    for t in (0.2, 0.8):
        a, b = _lerp2(pts[0], pts[3], t), _lerp2(pts[1], pts[2], t)
        out += _p(_poly([(a[0], a[1] - 6), (b[0], b[1] - 6), (b[0], b[1] + 6), (a[0], a[1] + 6)]), S.shade(face, 0.12), 2.6)
    return out


def _ark_window_svg(op, glow=0.0):
    x0, top, x1, sill = ARK_WINDOW
    w, h = x1 - x0, sill - top
    gid = _uid("arkwin", round(glow, 2))
    out = (f'<defs>{S.rad_grad(gid, [(0, S.mix("#6b4c36", P["glow"], 0.6 * glow)), (1, "#3e2c22")], cy=0.7, r=0.8)}</defs>'
           f'<rect x="{x0}" y="{top}" width="{w}" height="{h}" fill="url(#{gid})"/>')
    out += _rect(x0 - 26, top - 24, w + 52, 22, TIMBER_DARK, 3.4, rx=4)
    out += _rect(x0 - 12, top - 4, 12, h + 4, TIMBER_DARK, 3) + _rect(x1, top - 4, 12, h + 4, TIMBER_DARK, 3)
    out += _rect(x0 - 24, sill - 2, w + 48, 18, TIMBER_LIGHT, 3.4, rx=4)
    out += _ark_shutter(-1, op, x0, top, x1, sill, ARK_BAND) + _ark_shutter(1, op, x0, top, x1, sill, ARK_BAND)
    return out


def _ark(door=0.0, window=0.0, ramp=True, progress=1.0, floating=False, wet=False, glow=0.0, lamps=0.0,
         blocks=None):
    p = _clamp(progress)
    done = p >= 0.999
    hull_c = S.shade(ARK_HULL, -0.16) if wet else ARK_HULL
    cab_c = S.shade(ARK_CABIN, -0.14) if wet else ARK_CABIN
    roof_c = S.shade(ARK_ROOF, -0.14) if wet else ARK_ROOF
    keel_t = _clamp(p / 0.12)
    ribs_t = _clamp((p - 0.06) / 0.16)
    plank_t = _clamp((p - 0.22) / 0.33)
    cabin_t = _clamp((p - 0.55) / 0.25)
    roof_t = _clamp((p - 0.8) / 0.2)
    if blocks is None:
        blocks = (not floating) and not done
    out = ""
    hull_pts = _ark_hull_pts()
    hull_d = _sm(hull_pts, closed=True, tension=0.6)
    # ---- cradle blocks under the keel (building on dry land)
    if blocks:
        for bx in (-720, -450, -180, 180, 450, 720):
            ky = _ark_keel(bx)
            if ky < -14:
                for j, yy in enumerate(range(0, int(-ky) - 6, 30)):
                    out += _rect(bx - 44 + (j % 2) * 8, -yy - 28, 88, 28, TIMBER_DARK if j % 2 else TIMBER, 3.2, rx=3)
    # ---- keel and ribs (seen above the planking while building)
    if not done:
        if ribs_t > 0:
            xs = list(range(-840, 861, 120))
            n = max(1, int(round(len(xs) * ribs_t)))
            xs = sorted(xs, key=abs)[:n]
            for rx in xs:
                ky, sy = _ark_keel(rx), _ark_sheer(rx)
                bow = 26 if rx > 0 else -26
                out += _tube(f"M{_f(rx)},{_f(ky)} Q{_f(rx + bow * abs(rx) / 900)},{_f((ky + sy) / 2)} {_f(rx)},{_f(sy)}",
                             16, TIMBER_DARK, 3.4)
            if ribs_t >= 1:
                out += _tube("M960,-380 Q982,-520 966,-650", 18, TIMBER_DARK, 3.4)
                out += _tube("M-940,-390 Q-966,-520 -952,-650", 18, TIMBER_DARK, 3.4)
                out += _tube(_sm([(x, _ark_sheer(x) + 6) for x in range(-950, 966, 80)], closed=False), 12, TIMBER, 3.2)
        if keel_t > 0:
            L = 900 * keel_t
            pts = [(x, _ark_keel(x) - 8) for x in [-L + i * (2 * L / 20) for i in range(21)]]
            out += _tube(_sm(pts, closed=False), 22, TIMBER, 3.6)
    # ---- hull planking (fills from the keel upward while building)
    if plank_t > 0:
        hull = _p(hull_d, hull_c, 0)
        inner = ""
        rows = 9
        for r in range(rows):
            t0, t1 = r / rows, (r + 1) / rows
            if r % 2:
                top_ = [(x, _ark_row_y(x, t1)) for x in range(-980, 1001, 60)]
                bot = [(x, _ark_row_y(x, t0)) for x in range(1000, -981, -60)]
                inner += _p(_poly(top_ + bot), S.shade(hull_c, 0.07), 0)
            seam = [(x, _ark_row_y(x, t1)) for x in range(-980, 1001, 40)]
            inner += _p(_sm(seam, closed=False), sw=2.6, stroke=S.shade(hull_c, -0.35), extra='opacity="0.8"')
            rng = random.Random(r)
            x = -950 + rng.uniform(0, 200)
            while x < 960:                                  # butt joints and nail pairs
                ya, yb = _ark_row_y(x, t0), _ark_row_y(x, t1)
                inner += _line(x, ya - 3, x, yb + 3, sw=2.2, color=S.shade(hull_c, -0.35), extra='opacity="0.7"')
                for yy in (ya + (yb - ya) * 0.3, ya + (yb - ya) * 0.7):
                    inner += _circ(x + 7, yy, 2.2, S.shade(hull_c, -0.45), 0)
                x += rng.uniform(220, 360)
        # wale (rub strake) and the painted band under the gunwale
        band_a = [(x, _ark_row_y(x, 0.86)) for x in range(-980, 1001, 40)]
        band_b = [(x, _ark_row_y(x, 0.95)) for x in range(1000, -981, -40)]
        inner += _p(_poly(band_a + band_b), ARK_BAND, 2.6)
        for k in range(-940, 960, 64):
            yy = (_ark_row_y(k, 0.86) + _ark_row_y(k, 0.95)) / 2
            inner += _circ(k, yy, 5, S.shade(ARK_BAND, 0.45), 0)
        inner += _tube(_sm([(x, _ark_row_y(x, 0.5)) for x in range(-980, 1001, 40)], closed=False), 14,
                       S.shade(hull_c, -0.2), 3)
        # portholes on the middle deck
        for wx in range(-780, 820, 140):
            if 90 < wx < 470:
                continue
            wy = _ark_row_y(wx, 0.72)
            inner += _rect(wx - 24, wy - 22, 48, 42, TIMBER_DARK, 3.2, rx=6)
            inner += _rect(wx - 16, wy - 15, 32, 28, "#3e2c22", 0, rx=4)
            inner += _line(wx - 16, wy - 1, wx + 16, wy - 1, sw=2.4, color=TIMBER_DARK)
        # the door
        x0, top, x1, sill = ARK_DOOR
        if done:
            inner += _ark_door_svg(door, 0.0)
        else:
            inner += _rect(x0, top, x1 - x0, sill - top, "#3e2c22", 0)
            inner += _rect(x0 - 14, top - 18, x1 - x0 + 28, 20, TIMBER_DARK, 3, rx=3)
        if wet:                                             # a soft sheen along the planks
            for k in range(3):
                pts = [(x, _ark_row_y(x, 0.2 + 0.27 * k) - 6) for x in range(-700 + 80 * k, 640 - 60 * k, 40)]
                inner += _p(_sm(pts, closed=False), sw=7, stroke=HILITE, extra='opacity="0.28"')
        inner += _p(hull_d, sw=4.2)
        ycut = 30 - 700 * plank_t
        cid = _uid("arkhull", round(p, 4), wet, door, glow)
        rid = _uid("arkcut", round(p, 4), wet)
        out += (f'<clipPath id="{cid}"><path d="{hull_d}"/></clipPath><clipPath id="{rid}"><rect x="-1100" y="{_f(ycut)}" '
                f'width="2200" height="1200"/></clipPath><g clip-path="url(#{rid})">{hull}'
                f'<g clip-path="url(#{cid})">{inner}</g>{_p(hull_d, sw=4.2)}</g>')
        if plank_t < 1:
            out += _clip(_uid("arkcutl", round(p, 4)), hull_d,
                         _p(_sm([(x, ycut) for x in range(-1000, 1020, 60)], closed=False), sw=4, stroke=INK))
        else:                                               # gunwale cap rail
            out += _tube(_sm([(x, _ark_sheer(x) + 2) for x in range(-955, 972, 55)], closed=False), 12,
                         S.shade(hull_c, 0.2), 3.4)
    # ---- the cabin (third deck)
    cx0, cx1, cbot, ctop = -700, 720, ARK_DECK_Y + 4, -880
    if cabin_t > 0:
        posts = list(range(cx0, cx1 + 1, 237))
        if cabin_t < 1 or not done:
            for px in posts:
                out += _rect(px - 10, ctop, 20, cbot - ctop, TIMBER_DARK, 3.2)
            out += _rect(cx0 - 14, ctop - 8, cx1 - cx0 + 28, 20, TIMBER_DARK, 3.2)
        wall = _rect(cx0, ctop, cx1 - cx0, cbot - ctop, cab_c, 0)
        for bx in range(cx0 + 36, cx1, 36):
            wall += _line(bx, ctop, bx, cbot, sw=2.2, color=S.shade(cab_c, -0.28), extra='opacity="0.75"')
            if (bx // 36) % 3 == 0:
                wall += _circ(bx - 18, ctop + 30, 2, S.shade(cab_c, -0.4), 0) + _circ(bx - 18, cbot - 26, 2,
                                                                                  S.shade(cab_c, -0.4), 0)
        for wx in (-120, 70, 260, 450, 630):                # small windows: animals can peek out
            wall += _rect(wx - 34, -812, 68, 62, TIMBER_DARK, 3.2, rx=4)
            wall += _rect(wx - 25, -804, 50, 46, "#3e2c22", 0, rx=3)
            if lamps > 0:
                wall += _rect(wx - 25, -804, 50, 46, P["glow"], 0, rx=3, extra=f'opacity="{0.75 * _clamp(lamps):.2f}"')
        wall += _rect(cx0, cbot - 22, cx1 - cx0, 22, S.shade(cab_c, -0.12), 0)
        wall += _rect(cx0, ctop, cx1 - cx0, 26, PITCH, 0, extra='opacity="0.25"')          # shade under the eaves
        if done:
            wall += _ark_window_svg(window, 0.8 * _clamp(lamps))
        else:
            x0, top, x1, sill = ARK_WINDOW
            wall += _rect(x0, top, x1 - x0, sill - top, "#3e2c22", 0)
        if wet:
            wall += _p(f"M{cx0 + 40},{ctop + 60} L{cx1 - 60},{ctop + 50}", sw=8, stroke=HILITE, extra='opacity="0.25"')
        wall += _rect(cx0, ctop, cx1 - cx0, cbot - ctop, "none", 4)
        ycut = cbot + 4 - (cbot - ctop + 12) * cabin_t
        rid = _uid("arkcab", round(p, 4), wet, window, lamps)
        out += (f'<clipPath id="{rid}"><rect x="-1100" y="{_f(ycut)}" width="2200" height="900"/></clipPath>'
                f'<g clip-path="url(#{rid})">{wall}</g>')
    # ---- the roof
    if roof_t > 0:
        ex0, ex1, ey = -775, 795, -868
        rx0, rx1, ry = -690, 712, ARK_ROOF_Y
        if not done:
            for k in range(9):
                t = k / 8
                a = (_lerp(ex0, ex1, t), ey)
                b = (_lerp(rx0, rx1, t), ry)
                out += _tube(f"M{_f(a[0])},{_f(a[1])} L{_f(b[0])},{_f(b[1])}", 12, TIMBER_DARK, 3)
            out += _tube(f"M{rx0},{ry} L{rx1},{ry}", 16, TIMBER_DARK, 3.2)
        rd = f"M{ex0},{ey} L{ex1},{ey} Q{ex1 + 6},{ey - 10} {rx1 + 10},{ry + 4} L{rx0 - 10},{ry + 4} Q{ex0 - 6},{ey - 10} {ex0},{ey} Z"
        roof = _p(rd, roof_c, 0)
        sh = ""
        nrow = 6
        for r in range(nrow):
            t = (r + 0.5) / nrow
            yy = _lerp(ey, ry, t)
            xa, xb = _lerp(ex0, rx0, t), _lerp(ex1, rx1, t)
            d = f"M{_f(xa - 20)},{_f(yy)}"
            n = int((xb - xa) / 46)
            for i in range(n + 1):
                d += f" q{_f((xb - xa) / n / 2)},{_f(16)} {_f((xb - xa) / n)},0"
            sh += _p(d, sw=2.6, stroke=S.shade(roof_c, -0.35), extra='opacity="0.8"')
            sh += _p(d.replace("q", "q").replace(f"M{_f(xa - 20)},{_f(yy)}", f"M{_f(xa - 20)},{_f(yy + 4)}"), sw=3,
                     stroke=S.shade(roof_c, 0.2), extra='opacity="0.35"')
        if wet:
            sh += _p(f"M{ex0 + 80},{ey - 40} L{ex1 - 140},{ey - 60}", sw=10, stroke=HILITE, extra='opacity="0.3"')
        roof += _clip(_uid("arkroofc", wet, round(p, 3)), rd, sh) + _p(rd, sw=4.2)
        roof += _tube(f"M{rx0 - 18},{ry} L{rx1 + 18},{ry}", 20, S.shade(roof_c, -0.2), 3.6)        # ridge cap
        roof += _tube(f"M{ex0 - 6},{ey + 2} L{ex1 + 6},{ey + 2}", 10, S.shade(roof_c, 0.15), 3)    # eave board
        ycut = ey + 14 - (ey - ry + 40) * roof_t
        rid = _uid("arkroof", round(p, 4), wet)
        out += (f'<clipPath id="{rid}"><rect x="-1100" y="{_f(ycut)}" width="2200" height="900"/></clipPath>'
                f'<g clip-path="url(#{rid})">{roof}</g>')
    # ---- a ladder leaning on the hull while building
    if 0.2 < p < 0.999:
        lx = -560
        a, b = (lx - 120, 0), (lx + 10, -660)
        for off in (-22, 22):
            out += _tube(f"M{_f(a[0] + off)},{_f(a[1])} L{_f(b[0] + off)},{_f(b[1])}", 9, TIMBER_LIGHT, 3)
        for k in range(1, 12):
            t = k / 12
            q = _lerp2(a, b, t)
            out += _line(q[0] - 22, q[1], q[0] + 22, q[1], sw=8, color=INK) + _line(q[0] - 22, q[1], q[0] + 22, q[1], sw=4,
                                                                                    color=TIMBER_LIGHT)
    if wet and plank_t >= 1:                                # drips from the gunwale and the eaves
        for k, wx in enumerate((-820, -520, -180, 120, 480, 760)):
            yy = _ark_sheer(wx) + 30 + (k % 2) * 16
            out += f'<path d="{_raindrop_d(wx, yy, 7)}" fill="{P["sea_pale"]}" {_st(2.2)}/>'
        if roof_t >= 1:
            for k, wx in enumerate((-640, -300, 40, 380, 700)):
                out += f'<path d="{_raindrop_d(wx, -836 + (k % 2) * 18, 7)}" fill="{P["sea_pale"]}" {_st(2.2)}/>'
    if ramp and done and not floating:
        out += _ark_ramp()
    if done and glow > 0:
        out += _ark_door_svg(door, glow, glow_only=True)
    if floating:
        out = _g(out, f"translate(0,{ARK_DRAFT})")
    return out


def ark(x, y, scale=1.0, facing=1, door=0.0, window=0.0, ramp=True, progress=1.0, floating=False, wet=False,
        glow=0.0, lamps=0.0, blocks=None):
    if isinstance(door, str):
        door = {"closed": 0.0, "open": 1.0}[door]
    if isinstance(window, str):
        window = {"closed": 0.0, "open": 1.0}[window]
    return _place(_ark(door, window, ramp, progress, floating, wet, glow, lamps, blocks), x, y, scale, facing)


def _ark_local(lx, ly, floating):
    return (lx, ly + (ARK_DRAFT if floating else 0))


def ark_points(x, y, scale=1.0, facing=1, floating=False):
    """Stage coordinates of the ark's key places (see module doc)."""
    def st(lx, ly):
        return local_to_stage(x, y, scale, facing, *_ark_local(lx, ly, floating))

    def box(b):
        (ax, ay), (bx, by) = st(b[0], b[1]), st(b[2], b[3])
        return (min(ax, bx), ay, max(ax, bx), by)
    x0, top, x1, sill = ARK_DOOR
    return {"door": st((x0 + x1) / 2, sill), "door_box": box(ARK_DOOR), "ramp_top": st(*ARK_RAMP[1]),
            "ramp_bottom": st(*ARK_RAMP[2]), "window_box": box(ARK_WINDOW), "window_stand": st(*ARK_WINDOW_STAND),
            "windows": [box((wx - 25, -804, wx + 25, -758)) for wx in (-120, 70, 260, 450, 630)],
            "deck": st(0, ARK_DECK_Y), "roof": [st(-690, ARK_ROOF_Y), st(712, ARK_ROOF_Y)], "roof_mid": st(10, ARK_ROOF_Y),
            "eaves": [st(-775, -868), st(795, -868)], "bow": st(965, -655), "stern": st(-950, -650),
            "waterline": y if floating else y - ARK_DRAFT * scale}


def ark_ramp_y(sx, x, y, scale=1.0, facing=1):
    """Stage y of the ramp surface (landing + slope) at stage x for an ark drawn at (x, y, scale, facing),
    grounded. Outside the ramp it returns the ground line y."""
    lx = (sx - x) / scale * (1 if facing >= 0 else -1)
    (l0, ly), (tx, ty), (bx, by) = ARK_RAMP
    if l0 <= lx <= tx:
        return y + ly * scale
    if tx < lx <= bx:
        return y + (ty + (by - ty) * (lx - tx) / (bx - tx)) * scale
    return y


def _ark_clip_markup(markup, region_local, x, y, scale, facing, floating, tag):
    sx = scale * (1 if facing >= 0 else -1)
    off = ARK_DRAFT if floating else 0
    cid = _uid("arkclip", tag, region_local, x, y, scale, facing, floating)
    return (f'<clipPath id="{cid}"><path d="{region_local}" transform="translate({_f(x)},{_f(y)}) scale({sx:.4f},{scale:.4f}) '
            f'translate(0,{off})"/></clipPath><g clip-path="url(#{cid})">{markup}</g>')


def in_ark_door(markup, x, y, scale=1.0, facing=1, floating=False):
    """Clip figure markup to what shows of someone going in at the door: the doorway (down to the ramp) plus
    everything on the ramp side of the right-hand jamb (see module doc)."""
    x0, top, x1, sill = ARK_DOOR
    reg = f"M{x0},{top} L{x1},{top} L{x1},-3000 L3000,-3000 L3000,3000 L{x0},3000 L{x0},{sill + 40} Z"
    return _ark_clip_markup(markup, reg, x, y, scale, facing, floating, "door")


def in_ark_window(markup, x, y, scale=1.0, facing=1, floating=False):
    """Clip figure markup to the high window opening (someone inside looking out, see module doc)."""
    x0, top, x1, sill = ARK_WINDOW
    reg = f"M{x0},{top} L{x1},{top} L{x1},{sill} L{x0},{sill} Z"
    return _ark_clip_markup(markup, reg, x, y, scale, facing, floating, "window")


def in_ark_porthole(markup, i, x, y, scale=1.0, facing=1, floating=False):
    """Clip markup to the i-th small cabin window (0-4, stern to bow): a bird / a giraffe head peeking out."""
    wx = (-120, 70, 260, 450, 630)[i % 5]
    reg = f"M{wx - 25},-804 L{wx + 25},-804 L{wx + 25},-758 L{wx - 25},-758 Z"
    return _ark_clip_markup(markup, reg, x, y, scale, facing, floating, f"port{i}")


# ---------------------------------------------------------------------- Mount Ararat, the football pitch
ARARAT_LEDGE = (-260, -640, 260)           # x0, y, x1 of the saddle where the ark comes to rest (local, scale 1)


def _ararat(snow=True, green=0.0, seed=0):
    rng = random.Random(seed)
    rock, rock_d, rock_l = "#a49184", "#7f6e64", "#c9b8a8"
    g_ = _clamp(green)
    out = ""
    # Lesser Ararat (right, behind)
    small = [(160, 0), (330, -380), (480, -700), (560, -760), (650, -690), (820, -420), (1000, 0)]
    sd = _sm(small, tension=0.55)
    out += _p(sd, S.mix(rock, P["sky_day"], 0.25), 0) + _clip(_uid("ararat2", seed), sd, _p(_sm(
        [(560, -770), (660, -690), (830, -420), (1010, 10), (640, 10), (600, -400)], tension=0.6), rock_d, 0,
        extra='opacity="0.25"')) + _p(sd, sw=4)
    out += _p(_sm([(470, -690), (560, -760), (650, -690), (610, -640), (565, -666), (520, -630)], tension=0.6),
              "#f4f1ea", 3) if snow else ""
    # Greater Ararat (left, big, with the saddle on its right shoulder)
    big = [(-1000, 0), (-820, -420), (-640, -860), (-520, -1040), (-430, -1080), (-330, -1000), (-260, -760),
           (-200, -660), (0, -640), (220, -650), (300, -560), (520, -260), (720, 0)]
    bd = _sm(big, tension=0.55)
    inner = ""
    for k in range(7):                                   # rocky ridges running down
        x0 = -760 + k * 190 + rng.uniform(-40, 40)
        inner += _p(f"M{_f(x0 + 160)},{_f(-900 + abs(k - 2) * 90)} Q{_f(x0 + 60)},{_f(-500)} {_f(x0 - 20)},{_f(-80)}",
                    sw=3, stroke=rock_d, extra='opacity="0.55"')
    inner += _ell(-380, -560, 260, 340, rock_l, 0, extra='opacity="0.35" filter="url(#soft)"')
    inner += _p(_sm([(-430, -1090), (-300, -980), (-200, -660), (100, -620), (360, -400), (760, 20), (-60, 20),
                     (-260, -300), (-360, -700)], tension=0.6), rock_d, 0, extra='opacity="0.32"')     # shady east flanks
    for k in range(9):                                   # little rock ledges
        lx_, ly_ = rng.uniform(-820, 560), rng.uniform(-820, -120)
        inner += _p(f"M{_f(lx_)},{_f(ly_)} q{_f(24)},{_f(-8)} {_f(50)},{_f(2)}", sw=3, stroke=rock_d, extra='opacity="0.6"')
    if g_ > 0:                                           # grass returning on the lower slopes
        gd = S.hill(-1100, 1100, 40, 420 * g_, seed=3, bottom=60, bumps=4)
        inner += _p(gd, S.mix(P["grass"], rock, 0.25), 0, extra=f'opacity="{0.4 + 0.6 * g_:.2f}"')
        for _ in range(int(14 * g_)):
            tx, ty = rng.uniform(-850, 650), rng.uniform(-160 * g_, -10)
            inner += _p(S.blob(tx, ty - 22, 26, 20, 0.1, 8, seed=rng.randint(0, 99)), P["leaf_dark"], 2.6)
    if snow:
        cap = [(-700, -860), (-600, -980), (-520, -1040), (-430, -1080), (-330, -1000), (-280, -880), (-340, -905),
               (-400, -850), (-470, -920), (-540, -840), (-610, -900)]
        inner += _p(_sm(cap, tension=0.7), "#f6f3ec", 3)
        inner += _p("M-560,-1000 Q-500,-1030 -440,-1060", sw=5, stroke=HILITE, extra='opacity="0.8"')
    out += _p(bd, rock, 0) + _clip(_uid("ararat", snow, round(g_, 2), seed), bd, inner) + _p(bd, sw=4.4)
    return out


def ararat(x, y, scale=1.0, snow=True, green=0.0, seed=0, facing=1):
    return _place(_ararat(snow, green, seed), x, y, scale, facing, filt="wobble")


FOOTBALL_LEN = 1000                        # length of the pitch's near touchline at scale 1


def _football_field(goals=True):
    W0, W1, D = 1000, 800, 280
    line = "#fbf6ea"
    pitch = f"M{-W0 / 2},0 L{W0 / 2},0 L{W1 / 2},{-D} L{-W1 / 2},{-D} Z"
    inner = ""
    n = 10
    for i in range(n):                                    # mown stripes
        if i % 2:
            continue
        a0, a1 = i / n, (i + 1) / n
        pts = [(-W0 / 2 + W0 * a0, 0), (-W0 / 2 + W0 * a1, 0), (-W1 / 2 + W1 * a1, -D), (-W1 / 2 + W1 * a0, -D)]
        inner += _p(_poly(pts), S.shade(P["grass"], 0.12), 0)
    m = 18

    def pp(u, v):          # u 0..1 along, v 0..1 depth (0 = near)
        w = _lerp(W0, W1, v) - 2 * m
        return (-w / 2 + w * u, -m * 0.6 - (D - 1.2 * m) * v)
    def ln(pts, closed=False):
        return _p(_poly([pp(*q) for q in pts], closed), sw=4, stroke=line)
    inner += ln([(0, 0), (1, 0), (1, 1), (0, 1)], True) + ln([(0.5, 0), (0.5, 1)])
    cc = [pp(0.5 + 0.075 * math.cos(a) * (1.0), 0.5 + 0.28 * math.sin(a)) for a in [i * math.pi / 12 for i in range(24)]]
    inner += _p(_poly(cc), sw=4, stroke=line) + _circ(*pp(0.5, 0.5), 4, line, 0)
    for side in (0, 1):
        s0 = 0 if side == 0 else 1
        k = 1 if side == 0 else -1
        inner += ln([(s0, 0.2), (s0 + k * 0.15, 0.2), (s0 + k * 0.15, 0.8), (s0, 0.8)])
        inner += ln([(s0, 0.36), (s0 + k * 0.055, 0.36), (s0 + k * 0.055, 0.64), (s0, 0.64)])
    out = _p(pitch, P["grass"], 0) + _clip(_uid("pitch"), pitch, inner) + _p(pitch, sw=4)
    out += _p(f"M{-W0 / 2},0 L{W0 / 2},0 L{W0 / 2},16 L{-W0 / 2},16 Z", P["grass_dark"], 3.4)
    if goals:
        for side in (-1, 1):
            gx = side * (W0 + W1) / 4 + side * 2
            gy = -D / 2
            net = ""
            for k in range(6):
                net += _line(gx + side * k * 5, gy - 50 + k * 4, gx + side * k * 5, gy + 30 - k * 2, sw=1.4,
                             color="#d9d6cc")
            for k in range(5):
                net += _line(gx, gy - 46 + k * 18, gx + side * 28, gy - 30 + k * 12, sw=1.4, color="#d9d6cc")
            out += net
            out += _p(f"M{_f(gx)},{_f(gy + 38)} L{_f(gx)},{_f(gy - 52)} L{_f(gx - side * 4)},{_f(gy - 54)} "
                      f"L{_f(gx - side * 4)},{_f(gy + 34)}", sw=8, stroke=INK)
            out += _p(f"M{_f(gx)},{_f(gy + 38)} L{_f(gx)},{_f(gy - 52)}", sw=4, stroke=line)
            out += _p(f"M{_f(gx)},{_f(gy - 52)} L{_f(gx + side * 30)},{_f(gy - 36)} L{_f(gx + side * 30)},{_f(gy + 26)} "
                      f"L{_f(gx)},{_f(gy + 38)}", sw=3, stroke=INK, extra='fill="none"')
    out += _circ(*pp(0.56, 0.38), 9, line, 2.6)            # a ball
    return out


def football_field(x, y, scale=1.0, goals=True):
    return _place(_football_field(goals), x, y, scale)


# ---------------------------------------------------------------------- animals two by two
ARK_ANIMALS = ("elephant", "giraffe", "zebra", "horse", "deer", "rabbit", "turtle", "duck", "monkey", "hippo", "fox")
ARK_ANIMAL_POSES = {
    "elephant": ("stand", "walk_a", "walk_b", "trunk_up", "spray", "sleep"),
    "giraffe": ("stand", "walk_a", "walk_b", "bow"),
    "zebra": ("stand", "walk_a", "walk_b"),
    "horse": ("stand", "walk_a", "walk_b"),
    "deer": ("stand", "walk_a", "walk_b"),
    "rabbit": ("stand", "hop", "sleep"),
    "turtle": ("stand", "walk_a", "walk_b"),
    "duck": ("stand", "walk_a", "walk_b", "swim"),
    "monkey": ("stand", "walk_a", "walk_b", "wave", "sit"),
    "hippo": ("stand", "walk_a", "walk_b", "yawn"),
    "fox": ("stand", "walk_a", "walk_b", "sit", "sleep"),
}
_SIZE = {"elephant": 1.22, "giraffe": 1.0, "zebra": 0.92, "horse": 1.0, "deer": 0.9, "rabbit": 0.95, "turtle": 0.9,
         "duck": 0.95, "monkey": 0.95, "hippo": 1.05, "fox": 1.0}
_NAIL = "#f1e8d6"
_FEET4 = {"stand": (0, 0, 0, 0), "walk_a": (30, 30, -30, -26), "walk_b": (-26, -26, 30, 34)}
_LIFT4 = {"stand": (0, 0, 0, 0), "walk_a": (0, 0, 7, 0), "walk_b": (0, 8, 0, 0)}


def _a_eye(ex, ey, r, eyes="open", female=False, brow=None, browk=1.0):
    k = {"open": "open", "closed": "closed", "happy": "happy"}.get(eyes, "open")
    out = _dot_eye(ex, ey, r, k)
    if female and k == "open":
        for i, (dx, dy) in enumerate(((-1.0, -1.15), (-0.2, -1.55), (0.6, -1.35))):
            out += _line(ex + dx * r * 0.9, ey + dy * r * 0.75, ex + dx * r * 1.35 - 1, ey + dy * r * 1.05 - 3,
                         sw=max(1.8, r * 0.3))
    if brow:
        out += _p(f"M{_f(ex - r * 1.3)},{_f(ey - r * 2.0 * browk)} Q{_f(ex)},{_f(ey - r * 2.7 * browk)} "
                  f"{_f(ex + r * 1.3)},{_f(ey - r * 2.1 * browk)}", sw=max(2.2, r * 0.38), stroke=brow)
    return out


def _col_leg(top, foot_x, w0, w1, col, lift=0.0, nails=_NAIL, far=False):
    """Stout column leg (elephant, hippo) from the body point `top` to a flat foot on the ground at foot_x."""
    if far:
        col = S.shade(col, -0.16)
    tx, ty = top
    gy = -lift - (4 if far else 0)
    d = (f"M{_f(tx - w0 / 2)},{_f(ty)} Q{_f((tx + foot_x) / 2 - w0 * 0.55)},{_f((ty + gy) / 2)} {_f(foot_x - w1 / 2)},{_f(gy - 6)} "
         f"Q{_f(foot_x - w1 / 2)},{_f(gy)} {_f(foot_x - w1 / 2 + 6)},{_f(gy)} L{_f(foot_x + w1 / 2 - 6)},{_f(gy)} "
         f"Q{_f(foot_x + w1 / 2)},{_f(gy)} {_f(foot_x + w1 / 2)},{_f(gy - 6)} "
         f"Q{_f((tx + foot_x) / 2 + w0 * 0.5)},{_f((ty + gy) / 2)} {_f(tx + w0 / 2)},{_f(ty)}")
    out = _p(d + " Z", col, 0) + _p(d, sw=3.8)
    if nails:
        for k in (-0.28, 0.02, 0.32):
            nx = foot_x + k * w1
            out += _p(f"M{_f(nx - 6)},{_f(gy)} Q{_f(nx - 6)},{_f(gy - 10)} {_f(nx)},{_f(gy - 10)} Q{_f(nx + 6)},{_f(gy - 10)} "
                      f"{_f(nx + 6)},{_f(gy)} Z", nails, 2.4)
    return out


def _zs(cx, cy, k=1.0):
    out = ""
    for j, (dx, dy, sz) in enumerate(((0, 0, 14), (22, -26, 18), (50, -58, 22))):
        x0, y0, h = cx + dx * k, cy + dy * k, sz * k / 2
        out += _p(f"M{_f(x0 - h)},{_f(y0 - h)} L{_f(x0 + h)},{_f(y0 - h)} L{_f(x0 - h)},{_f(y0 + h)} L{_f(x0 + h)},{_f(y0 + h)}",
                  sw=3.2, stroke=P["ink_soft"])
    return out


# ---- elephant
ELEPHANT = {"body": "#a9afbd", "shade": "#8d93a2", "ear_in": "#e8b7b6", "tusk": "#f6efdf"}


def _elephant(pose="stand", female=False, eyes="open"):
    C = ELEPHANT
    col, far = C["body"], S.shade(C["body"], -0.16)
    out = ""
    if pose == "sleep":
        out += _p(S.blob(-20, -100, 170, 96, 0.03, 12, seed=5), col, 4)
        out += _ell(-40, -40, 140, 26, S.shade(col, 0.15), 0, extra='opacity="0.6"')
        for fx in (-120, 60):
            out += _p(f"M{fx - 44},0 Q{fx - 44},-36 {fx},-36 Q{fx + 44},-36 {fx + 44},0 Z", col, 3.6)
            for k in (-16, 0, 16):
                out += _p(f"M{fx + k - 6},0 Q{fx + k - 6},-9 {fx + k},-9 Q{fx + k + 6},-9 {fx + k + 6},0 Z", _NAIL, 2.2)
        out += _circ(-188, -120, 9, col, 3)
        out += _tube("M170,-70 Q230,-56 238,-24 Q240,0 214,-2 Q196,-6 204,-22 Q214,-34 222,-22", 30, col, 4)
        out += _circ(140, -110, 66, col, 4)
        ear = "M126,-170 Q60,-176 54,-110 Q56,-52 116,-50 Q100,-110 126,-170 Z"
        out += _p(ear, col, 3.8) + _p("M114,-154 Q74,-152 72,-110 Q74,-74 106,-66 Q96,-110 114,-154 Z", C["ear_in"], 0)
        out += _a_eye(162, -116, 7, "closed", female, S.shade(col, -0.45)) + _blush(176, -94, 10, 6)
        if not female:
            out += _tube("M186,-70 Q206,-60 214,-74", 9, C["tusk"], 3)
        else:
            out += _bow(120, -172, 1.0, rot=-15)
        out += _zs(200, -200, 1.0)
        return out
    walk = pose if pose in _FEET4 else "stand"
    fx = (-85, 95, -115, 70)
    fx = tuple(a + b for a, b in zip(fx, _FEET4[walk]))
    lift = _LIFT4[walk]
    bob = 5 if walk != "stand" else 0
    out += _tube(f"M-158,{-236 + bob} Q-176,{-200 + bob} -176,{-150 + bob}", 7, far, 3.2)
    out += _p(f"M-184,{-154 + bob} Q-176,{-126 + bob} -168,{-154 + bob} Z", S.shade(col, -0.4), 2.6)
    out += _col_leg((-80, -170 + bob), fx[0], 58, 54, col, lift[0], far=True)
    out += _col_leg((96, -170 + bob), fx[1], 56, 52, col, lift[1], far=True)
    out += _p(S.blob(-15, -215 + bob, 150, 112, 0.03, 12, seed=2), col, 4)
    out += _ell(-20, -132 + bob, 120, 28, S.shade(col, 0.15), 0, extra='opacity="0.6"')
    out += _p(f"M-130,{-260 + bob} Q-90,{-318 + bob} -20,{-322 + bob}", sw=4, stroke=S.shade(col, 0.3), extra='opacity="0.6"')
    out += _col_leg((-112, -150 + bob), fx[2], 64, 58, col, lift[2])
    out += _col_leg((72, -150 + bob), fx[3], 60, 56, col, lift[3])
    hx, hy = 128, -262 + bob
    up = pose in ("trunk_up", "spray")
    if up:
        trunk = [(hx + 46, hy + 14), (hx + 92, hy - 10), (hx + 112, hy - 70), (hx + 96, hy - 124), (hx + 116, hy - 146)]
    else:
        trunk = [(hx + 44, hy + 22), (hx + 76, hy + 56), (hx + 90, hy + 108), (hx + 86, hy + 150), (hx + 104, hy + 160)]
    out += _band(trunk, 46, 24, col)
    tip = trunk[-1]
    out += _ell(tip[0] + 2, tip[1], 12, 9, S.shade(col, -0.1), 3, extra=f'transform="rotate({-60 if up else 30} {_f(tip[0])} {_f(tip[1])})"')
    for k in range(1, 4):
        q = _lerp2(trunk[0], trunk[2], k / 4)
        out += _p(f"M{_f(q[0] - 12)},{_f(q[1] - (6 if up else -4))} q12,{'-6' if up else '6'} 24,0", sw=2.4,
                  stroke=S.shade(col, -0.3), extra='opacity="0.6"')
    out += _circ(hx, hy, 74, col, 4)
    if up:
        out += _p(f"M{hx + 22},{hy + 36} Q{hx + 34},{hy + 56} {hx + 52},{hy + 36} Z", P["mouth_inside"], 3)
    else:
        out += _p(f"M{hx + 18},{hy + 40} Q{hx + 32},{hy + 50} {hx + 44},{hy + 38}", sw=3)
    if not female:
        out += _tube(f"M{hx + 48},{hy + 44} Q{hx + 64},{hy + 60} {hx + 78},{hy + 50}", 10, C["tusk"], 3)
    ear = (f"M{hx - 10},{hy - 66} Q{hx - 104},{hy - 70} {hx - 104},{hy + 6} Q{hx - 100},{hy + 80} {hx - 30},{hy + 80} "
           f"Q{hx - 46},{hy + 10} {hx - 10},{hy - 66} Z")
    out += _p(ear, col, 3.8)
    out += _p(f"M{hx - 20},{hy - 50} Q{hx - 88},{hy - 50} {hx - 88},{hy + 6} Q{hx - 84},{hy + 60} {hx - 38},{hy + 62} "
              f"Q{hx - 50},{hy + 6} {hx - 20},{hy - 50} Z", C["ear_in"], 0)
    out += _a_eye(hx + 24, hy - 20, 8, eyes, female, S.shade(col, -0.45))
    out += _blush(hx + 40, hy + 12, 11, 7)
    if female:
        out += _bow(hx - 10, hy - 70, 1.1, rot=-10)
    if up:
        mx, my = trunk[-1]
        if pose == "trunk_up":
            for j, r in enumerate((26, 44)):
                out += _p(f"M{_f(mx + r * 0.3)},{_f(my - r)} Q{_f(mx + r)},{_f(my - r * 0.6)} {_f(mx + r * 0.95)},{_f(my + r * 0.1)}",
                          sw=3.4, stroke=P["ink_soft"])
        else:
            rng = random.Random(7)
            for j in range(14):
                t = j / 13
                a = math.radians(-110 + 80 * t)
                dist = 30 + 90 * rng.uniform(0.5, 1.0)
                px, py = mx + 10 + math.cos(a) * dist * 0.8, my - 30 + math.sin(a) * dist + 60 * t * t
                out += f'<path d="{_raindrop_d(px, py, rng.uniform(7, 10))}" fill="{P["sea_pale"]}" {_st(2.4)}/>'
            for w_, c_ in ((22, INK), (16, P["sea_pale"])):
                out += _p(f"M{_f(mx)},{_f(my - 8)} Q{_f(mx + 6)},{_f(my - 60)} {_f(mx + 40)},{_f(my - 96)}", sw=w_ * 0.6,
                          stroke=c_, extra='opacity="0.9"')
    return out


# ---- giraffe
GIRAFFE = {"coat": "#f3c768", "patch": "#c98142", "mane": "#a8602e", "muzzle": "#f7e0b0"}


def _giraffe(pose="stand", female=False, eyes="open"):
    C = GIRAFFE
    col, pc = C["coat"], C["patch"]
    walk = pose if pose in _FEET4 else "stand"
    fx = tuple(a + b * 0.9 for a, b in zip((-74, 92, -98, 70), _FEET4[walk]))
    lift = _LIFT4[walk]
    out = ""
    out += _tube("M-112,-336 Q-132,-300 -136,-238", 6, S.shade(col, -0.15), 3)
    out += _p("M-144,-246 Q-136,-214 -126,-244 Z", C["mane"], 2.6)
    for i, (hx, f_, hind) in enumerate(((-66, fx[0], True), (78, fx[1], False), (-86, fx[2], True), (58, fx[3], False))):
        out += _qleg((hx, -300), f_, 38, 17, col, hind=hind, far=i < 2, ground=-lift[i], bend=0.4)
    body = [(-122, -332), (-100, -374), (-30, -394), (60, -414), (112, -392), (126, -344), (100, -296), (20, -282),
            (-70, -286), (-114, -304)]
    bow = pose == "bow"
    if bow:
        neck = [(70, -380), (150, -372), (220, -344), (262, -322)]
        head = (290, -318)
    else:
        neck = [(76, -380), (112, -470), (140, -560), (152, -604)]
        head = (172, -628)
    # neck (with patches) then body
    nd_out = _band(neck, 62, 36, col)
    nd_centre = neck
    rng = random.Random(3)
    patches = ""
    bd = _sm(body)
    for (cx, cy) in ((-80, -340), (-30, -366), (24, -350), (66, -380), (-64, -298), (-10, -310), (44, -312), (96, -340)):
        patches += _p(S.blob(cx + rng.uniform(-4, 4), cy, 22, 18, 0.18, 7, seed=rng.randint(0, 99)), pc, 0)
    body_svg = _p(bd, col, 0) + _clip(_uid("gbody", pose), bd, patches) + _p(bd, sw=4)
    out += nd_out
    npatch = ""
    for k in range(1, 6):
        q = _lerp2(nd_centre[0], nd_centre[-1], k / 6)
        npatch += _p(S.blob(q[0] + rng.uniform(-6, 6), q[1], 14, 12, 0.2, 7, seed=rng.randint(0, 99)), pc, 0)
    # clip neck patches to the neck band
    left, right = [], []
    n = len(neck)
    for i, p_ in enumerate(neck):
        q0, q1 = neck[max(0, i - 1)], neck[min(n - 1, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        w = _lerp(62, 36, i / (n - 1)) / 2 - 3
        left.append((p_[0] - dy / ln * w, p_[1] + dx / ln * w))
        right.append((p_[0] + dy / ln * w, p_[1] - dx / ln * w))
    ndp = _sm(left + list(reversed(right)), closed=True, tension=0.8)
    out += _clip(_uid("gneck", pose), ndp, npatch)
    # mane along the back of the neck
    mane = []
    for i in range(n - 1):
        q0, q1 = neck[max(0, i - 1)], neck[min(n - 1, i + 1)]
        dx, dy = q1[0] - q0[0], q1[1] - q0[1]
        ln = math.hypot(dx, dy) or 1
        mane.append((right[i][0] + dy / ln * 3, right[i][1] - dx / ln * 3))
    out += _p(_sm(mane, closed=False), sw=13, stroke=INK) + _p(_sm(mane, closed=False), sw=7, stroke=C["mane"])
    out += body_svg
    # head
    hx, hy = head
    rot = 28 if bow else 18
    hd = _g(_p("M-30,-14 Q-28,-30 -6,-30 Q30,-30 42,-6 Q48,14 30,20 Q0,26 -20,16 Q-34,6 -30,-14 Z", col, 4)
            + _ell(30, 4, 18, 14, C["muzzle"], 3) + _circ(38, -2, 2.4, INK, 0)
            + _p("M22,14 Q30,18 38,12", sw=2.6), f"translate({hx},{hy}) rotate({rot})")
    horns = ""
    for dx in (-14, 2):
        a = _rot(hx + dx, hy - 28, hx, hy, rot)
        b = _rot(hx + dx - 4, hy - 52, hx, hy, rot)
        horns += _tube(f"M{_f(a[0])},{_f(a[1])} L{_f(b[0])},{_f(b[1])}", 8, col, 3) + _circ(b[0], b[1], 7, C["mane"], 2.8)
    e1 = _rot(hx - 22, hy - 12, hx, hy, rot)
    out += horns
    out += _ell(e1[0] - 12, e1[1] - 2, 16, 7, col, 3, extra=f'transform="rotate({rot + 20} {_f(e1[0] - 12)} {_f(e1[1] - 2)})"')
    out += hd
    ex, ey = _rot(hx + 4, hy - 10, hx, hy, rot)
    out += _a_eye(ex, ey, 6, eyes, female, S.shade(col, -0.5)) + _blush(ex + 10, ey + 14, 8, 5)
    if female:
        out += _bow(hx - 22, hy - 36, 0.9, rot=-20)
    return out


# ---- horse / zebra / deer
_EQUINE = {
    "horse": dict(coat="#c27d46", mane="#6a3f26", muzzle="#9a5f36", belly=None, hoof="#4e3a2e", stripes=None),
    "zebra": dict(coat="#f7f2e8", mane="#3e3538", muzzle="#5a5052", belly=None, hoof="#3e3538", stripes="#3e3538"),
    "deer": dict(coat="#c98a54", mane=None, muzzle="#7a5638", belly="#f3e2c4", hoof="#4e3a2e", stripes=None),
}


def _equine(kind="horse", pose="stand", female=False, eyes="open"):
    C = _EQUINE[kind]
    col = C["coat"]
    deer = kind == "deer"
    zebra = kind == "zebra"
    walk = pose if pose in _FEET4 else "stand"
    fx = tuple(a + b * 0.95 for a, b in zip((-86, 86, -108, 66), _FEET4[walk]))
    lift = _LIFT4[walk]
    lw0, lw1 = (26, 11) if deer else (32, 15)
    top = -176 if deer else -170
    out = ""
    # tail
    if zebra:
        out += _tube("M-124,-214 Q-142,-180 -146,-140", 6, col, 3) + _p("M-156,-148 Q-146,-104 -136,-148 Z", C["mane"], 2.6)
    elif deer:
        out += _p("M-122,-224 Q-150,-236 -146,-206 Q-136,-196 -120,-206 Z", C["belly"], 3)
    else:
        out += _p("M-122,-214 Q-158,-208 -160,-150 Q-158,-112 -140,-104 Q-150,-150 -132,-180 Q-126,-196 -118,-200 Z",
                  C["mane"], 3.4)
    legs_col = col
    for i, (hx, f_, hind) in enumerate(((-82, fx[0], True), (80, fx[1], False), (-98, fx[2], True), (64, fx[3], False))):
        out += _qleg((hx, top), f_, lw0, lw1, legs_col, hind=hind, far=i < 2, ground=-lift[i], bend=0.5)
        if zebra:
            for k in range(3):
                yy = -30 - k * 30 - (5 if i < 2 else 0) - lift[i]
                xx = f_ + (hx - f_) * (k + 1) * 0.12
                out += _line(xx - 8, yy, xx + 8, yy - 2, sw=5, color=C["stripes"], extra='opacity="0.9"')
    body = [(-134, -196), (-122, -238), (-82, -254), (-24, -244), (30, -242), (86, -254), (120, -228), (130, -188),
            (110, -152), (40, -140), (-40, -142), (-112, -152)]
    if deer:
        body = [(x * 0.92, y - 8) for x, y in body]
    bd = _sm(body)
    inner = ""
    if C["belly"]:
        inner += _ell(0, -150, 110, 22, C["belly"], 0)
    if zebra:
        for k in range(-5, 6):
            x0 = k * 22
            inner += _p(f"M{x0 - 6},-260 Q{x0 + 6},-210 {x0 - 2},-170", sw=9, stroke=C["stripes"])
        inner += _p("M-128,-230 Q-100,-200 -126,-176 M-120,-238 Q-86,-210 -116,-170", sw=7, stroke=C["stripes"])
    if deer:
        rng = random.Random(4)
        for _ in range(9):
            inner += _circ(rng.uniform(-90, 70), rng.uniform(-236, -206), rng.uniform(3.5, 5.5), "#f6ead2", 0)
    body_svg = _p(bd, col, 0) + (_clip(_uid("eqb", kind, pose), bd, inner) if inner else "") + _p(bd, sw=4)
    # neck and head
    if deer:
        neck = [(70, -224), (98, -270), (116, -312), (122, -330)]
        out += _band(neck, 52, 38, col)
        hx, hy = 138, -338
    else:
        neck = [(80, -222), (112, -262), (138, -300), (150, -322)]
        out += _band(neck, 62, 44, col)
        hx, hy = 156, -324
    if zebra:
        for k in range(4):
            q = _lerp2(neck[0], neck[-1], 0.15 + k * 0.22)
            out += _p(f"M{_f(q[0] - 26)},{_f(q[1] - 2)} Q{_f(q[0])},{_f(q[1] - 8)} {_f(q[0] + 22)},{_f(q[1] + 12)}", sw=8,
                      stroke=C["stripes"])
    if C["mane"] and not zebra:                        # flowing mane
        mane = [(hx - 14, hy - 22), (hx - 32, hy + 8), (hx - 52, hy + 42), (hx - 74, hy + 76), (hx - 88, hy + 100)]
        out += _band(mane, 26, 16, C["mane"])
        out += _p(f"M{hx - 2},{hy - 22} Q{hx + 14},{hy - 18} {hx + 16},{hy - 6} Q{hx},{hy - 10} {hx - 8},{hy - 12} Z",
                  C["mane"], 2.6)
        if female:
            out += _bow(hx - 40, hy + 22, 0.9, rot=-30)
    if zebra:                                           # short upright striped mane
        mane = [(hx - 14, hy - 22), (hx - 34, hy + 6), (hx - 56, hy + 40), (hx - 80, hy + 74), (hx - 92, hy + 96)]
        out += _band(mane, 26, 18, col)
        for k in range(5):
            q = _lerp2(mane[0], mane[-1], k / 4.5)
            out += _line(q[0] - 6, q[1] - 8, q[0] + 6, q[1] + 6, sw=6, color=C["stripes"])
    out += body_svg
    if deer:
        head = (f"M{hx - 22},{hy - 4} Q{hx - 18},{hy - 28} {hx + 6},{hy - 26} Q{hx + 28},{hy - 22} {hx + 46},{hy + 4} "
                f"Q{hx + 54},{hy + 18} {hx + 40},{hy + 22} Q{hx + 10},{hy + 24} {hx - 12},{hy + 16} Q{hx - 26},{hy + 8} {hx - 22},{hy - 4} Z")
    else:
        head = (f"M{hx - 24},{hy - 20} Q{hx - 6},{hy - 32} {hx + 14},{hy - 22} Q{hx + 34},{hy - 6} {hx + 48},{hy + 30} "
                f"Q{hx + 54},{hy + 50} {hx + 38},{hy + 56} Q{hx + 18},{hy + 60} {hx + 4},{hy + 40} Q{hx - 14},{hy + 14} {hx - 24},{hy - 20} Z")
    # ears (behind the head) and antlers
    if deer:
        if not female:
            ant = TIMBER_LIGHT
            for dx, s_ in ((-10, 1), (6, 1)):
                bx, by = hx + dx, hy - 22
                out += _tube(f"M{bx},{by} Q{bx - 10},{by - 30} {bx - 4},{by - 62}", 7, ant, 2.8)
                out += _tube(f"M{bx - 7},{by - 26} Q{bx - 26},{by - 38} {bx - 30},{by - 56}", 6, ant, 2.6)
                out += _tube(f"M{bx - 5},{by - 46} Q{bx + 10},{by - 56} {bx + 12},{by - 72}", 6, ant, 2.6)
        for dx, rot in ((-20, -40), (-6, -20)):
            out += _ell(hx + dx - 10, hy - 26, 20, 9, col, 3.2, extra=f'transform="rotate({rot} {hx + dx} {hy - 18})"')
            out += _ell(hx + dx - 10, hy - 26, 12, 4.5, "#e9b7a6", 0, extra=f'transform="rotate({rot} {hx + dx} {hy - 18})"')
    else:
        for dx in (-14, 0):
            out += _p(f"M{hx + dx - 8},{hy - 22} L{hx + dx - 4},{hy - 50} L{hx + dx + 8},{hy - 24} Z", col, 3)
            out += _p(f"M{hx + dx - 4},{hy - 26} L{hx + dx - 2},{hy - 42} L{hx + dx + 3},{hy - 27} Z",
                      C["stripes"] or "#e9b7a6", 0)
    out += _p(head, col, 4)
    mx, my = (hx + 40, hy + 8) if deer else (hx + 34, hy + 42)
    out += _clip(_uid("eqm", kind), head, _ell(mx + 6, my + 6, 24, 20, C["muzzle"], 0, extra='opacity="0.9"')) + _p(head, sw=4)
    if kind == "horse":                                  # white blaze
        out += _p(f"M{hx - 2},{hy - 22} Q{hx + 14},{hy + 2} {hx + 26},{hy + 26} Q{hx + 20},{hy + 30} {hx + 16},{hy + 22} "
                  f"Q{hx + 4},{hy} {hx - 8},{hy - 18} Z", CREAM, 0)
    if zebra:
        for k in range(3):
            out += _p(f"M{hx - 16 + k * 12},{hy - 20 + k * 6} Q{hx - 4 + k * 12},{hy - 4 + k * 10} {hx - 16 + k * 10},{hy + 10 + k * 10}",
                      sw=6, stroke=C["stripes"])
    if not C["mane"] or zebra:
        pass
    nx, ny = (hx + 48, hy + 6) if deer else (hx + 40, hy + 44)
    out += _circ(nx, ny, 3.2 if deer else 3, INK, 0)
    out += _p(f"M{nx - 12},{ny + 10} Q{nx - 6},{ny + 14} {nx},{ny + 10}", sw=2.6)
    ex, ey = (hx + 8, hy - 8) if deer else (hx + 8, hy - 4)
    out += _a_eye(ex, ey, 5.5, eyes, female, S.shade(col, -0.45) if not zebra else None)
    out += _blush(ex + 12, ey + 14, 8, 5)
    if female and (deer or zebra):
        out += _bow(hx - 18, hy - 22, 0.9, rot=-20)
    return out


# ---- rabbit
RABBIT = {"coat": "#d9c3a8", "belly": "#f6ecdc", "ear_in": "#efb1ad"}


def _rabbit_head(cx, cy, rot=0.0, eyes="open", female=False, ears_back=0.0):
    C = RABBIT
    col = C["coat"]
    out = ""
    for dx, a in ((-8, -12 - 50 * ears_back), (10, 6 - 46 * ears_back)):
        out += _g(_ell(0, -32, 11, 32, col, 3.4) + _ell(0, -32, 5.5, 22, C["ear_in"], 0),
                  f"translate({_f(cx + dx)},{_f(cy - 20)}) rotate({_f(a)})")
    out += _ell(cx, cy, 30, 27, col, 3.8)
    out += _ell(cx + 18, cy + 10, 13, 10, C["belly"], 0)
    out += _circ(cx + 28, cy + 4, 4, "#e8949c", 1.8)
    out += _p(f"M{_f(cx + 20)},{_f(cy + 14)} Q{_f(cx + 24)},{_f(cy + 18)} {_f(cx + 28)},{_f(cy + 12)}", sw=2.2)
    out += _a_eye(cx + 10, cy - 4, 5, eyes, female)
    out += _blush(cx + 16, cy + 8, 6, 4)
    if female:
        out += _bow(cx - 2, cy - 26, 0.75)
    return _g(out, f"rotate({rot:.1f} {_f(cx)} {_f(cy)})") if rot else out


def _rabbit(pose="stand", female=False, eyes="open", phase=0.0):
    C = RABBIT
    col = C["coat"]
    far = S.shade(col, -0.15)
    out = ""
    if pose == "sleep":
        out += _cluster([(-52, -36, 13)], C["belly"], 3)
        out += _p(S.blob(-4, -32, 56, 32, 0.04, 10, seed=1), col, 3.8)
        out += _ell(-6, -10, 40, 9, C["belly"], 0, extra='opacity="0.7"')
        out += _ell(40, -4, 18, 7, col, 3)
        out += _rabbit_head(40, -40, 10, "closed", female, ears_back=1.0)
        out += _zs(70, -86, 0.7)
        return out
    frame = int(round(_clamp(phase) * 4)) % 4 if pose == "hop" else -1
    if frame in (-1, 0):                       # sitting / crouched (gather)
        dy = 6 if frame == 0 else 0
        out += _ell(28, -6, 10, 6, far, 2.8)
        out += _cluster([(-52, -46 + dy, 13)], C["belly"], 3)
        out += _p(S.blob(-6, -46 + dy, 46, 42 - dy, 0.04, 10, seed=2), col, 3.8)
        out += _ell(-4, -40 + dy, 26, 22, C["belly"], 0, extra='opacity="0.6"')
        out += _circ(-22, -34 + dy, 30, col, 3.6)
        out += _ell(2, -7, 30, 8, col, 3.2)
        out += _ell(34, -6, 10, 6, col, 2.8)
        out += _rabbit_head(36, -92 + dy * 2, 0, eyes, female, ears_back=0.5 if frame == 0 else 0.0)
    elif frame == 1:                           # push off: stretched up and forward, hind feet still down
        out += _ell(-58, -8, 26, 7, far, 2.8)
        out += _tube("M-40,-30 L-60,-8", 14, far, 3)
        out += _cluster([(-52, -62, 13)], C["belly"], 3)
        out += _g(_p(S.blob(0, 0, 54, 30, 0.04, 10, seed=3), col, 3.8)
                  + _ell(4, 10, 36, 12, C["belly"], 0, extra='opacity="0.6"'), "translate(-4,-66) rotate(-24)")
        out += _tube("M-30,-44 L-62,-10", 16, col, 3.2) + _ell(-66, -7, 28, 7, col, 3)
        out += _tube("M34,-84 L58,-70", 9, col, 2.8)
        out += _rabbit_head(54, -112, -10, eyes, female, ears_back=0.9)
    elif frame == 2:                           # airborne, stretched out
        out += _cluster([(-62, -98, 13)], C["belly"], 3)
        out += _tube("M-36,-92 L-78,-82", 12, far, 3)
        out += _g(_p(S.blob(0, 0, 58, 28, 0.04, 10, seed=4), col, 3.8)
                  + _ell(4, 10, 40, 12, C["belly"], 0, extra='opacity="0.6"'), "translate(-6,-104) rotate(-6)")
        out += _tube("M-40,-96 L-84,-86", 14, col, 3) + _ell(-90, -84, 20, 7, col, 3, extra='transform="rotate(10 -90 -84)"')
        out += _tube("M34,-96 L62,-78", 9, col, 2.8)
        out += _rabbit_head(60, -124, 0, eyes, female, ears_back=1.0)
    else:                                      # landing on the front paws, hind legs up behind
        out += _cluster([(-46, -96, 13)], C["belly"], 3)
        out += _tube("M-30,-84 L-62,-104", 12, far, 3)
        out += _g(_p(S.blob(0, 0, 54, 30, 0.04, 10, seed=5), col, 3.8)
                  + _ell(4, 10, 36, 12, C["belly"], 0, extra='opacity="0.6"'), "translate(-2,-70) rotate(22)")
        out += _tube("M-26,-82 L-66,-100", 15, col, 3) + _ell(-70, -102, 20, 7, col, 3, extra='transform="rotate(-20 -70 -102)"')
        out += _tube("M34,-46 L44,-8", 10, col, 2.8) + _ell(48, -6, 11, 6, col, 2.6)
        out += _rabbit_head(56, -66, 16, eyes, female, ears_back=0.7)
    return out


# ---- turtle
TURTLE = {"shell": "#7ea35b", "pattern": "#a8c67c", "skin": "#b9cf8a", "rim": "#5e7e43"}


def _turtle(pose="stand", female=False, eyes="open"):
    C = TURTLE
    skin, far = C["skin"], S.shade(C["skin"], -0.15)
    walk = pose if pose in ("walk_a", "walk_b") else "stand"
    lx = {"stand": (-50, 46, -34, 62), "walk_a": (-60, 58, -24, 50), "walk_b": (-40, 36, -44, 70)}[walk]
    bob = -3 if walk != "stand" else 0
    out = ""
    for x_ in lx[2:]:
        out += _ell(x_, -12, 17, 13, far, 3.2)
    out += _p(f"M-84,{-26 + bob} L-104,{-18 + bob} L-84,{-14 + bob} Z", skin, 2.8)
    hx, hy = 112, -56 + bob + (-4 if walk == "walk_a" else 0)
    out += _band([(66, -36 + bob), (88, -46 + bob), (hx - 10, hy + 4)], 28, 24, skin)
    out += _circ(hx, hy, 22, skin, 3.6)
    out += _a_eye(hx + 6, hy - 6, 4.6, eyes, female) + _blush(hx + 12, hy + 6, 6, 4)
    out += _p(f"M{hx + 8},{hy + 9} Q{hx + 14},{hy + 13} {hx + 20},{hy + 7}", sw=2.4)
    if female:
        out += _bow(hx - 6, hy - 22, 0.7)
    for x_ in lx[:2]:
        out += _ell(x_, -10, 19, 14, skin, 3.4)
    shell = f"M-90,{-30 + bob} Q-84,{-94 + bob} 0,{-98 + bob} Q84,{-94 + bob} 90,{-30 + bob} Z"
    inner = ""
    for cx, cy, r in ((0, -66, 22), (-46, -52, 18), (46, -52, 18), (-24, -84, 12), (24, -84, 12), (-74, -38, 10), (74, -38, 10)):
        pts = [(cx + r * math.cos(math.pi / 3 * k), cy + bob + r * 0.8 * math.sin(math.pi / 3 * k)) for k in range(6)]
        inner += _p(_poly(pts), C["pattern"], 2.4, stroke=S.shade(C["shell"], -0.3))
    inner += _ell(-30, -80 + bob, 22, 8, HILITE, 0, extra='opacity="0.35"')
    out += _p(shell, C["shell"], 0) + _clip(_uid("tshell", walk), shell, inner) + _p(shell, sw=4)
    out += _rect(-96, -36 + bob, 192, 16, C["rim"], 3.4, rx=8)
    return out


# ---- duck
DUCK = {"m_head": "#3f8a5a", "m_breast": "#9a5a3e", "m_body": "#d2cec6", "m_wing": "#9a9188", "spec": "#4a6fb3",
        "f_body": "#bf9264", "f_dark": "#8a6340", "bill_m": "#f2c14e", "bill_f": "#e59a52", "feet": "#f09a4a"}


def _duck(pose="stand", female=False, eyes="open"):
    C = DUCK
    body_c = C["f_body"] if female else C["m_body"]
    head_c = C["f_body"] if female else C["m_head"]
    bill = C["bill_f"] if female else C["bill_m"]
    out = ""
    swim = pose == "swim"
    tilt = {"walk_a": -4, "walk_b": 4}.get(pose, 0)
    if not swim:
        legs = {"stand": ((-8, -6), (10, 10)), "walk_a": ((-18, -24), (14, 22)), "walk_b": ((-4, 6), (6, -2))}.get(pose, ((-8, -6), (10, 10)))
        for (hx, fx_), c in zip(legs, (S.shade(C["feet"], -0.15), C["feet"])):
            out += _line(hx, -22, fx_, -4, sw=9, color=INK) + _line(hx, -22, fx_, -4, sw=4.5, color=c)
            out += _p(f"M{fx_ - 8},0 L{fx_ + 18},0 L{fx_ + 2},-8 Z", c, 2.6)
    g = ""
    g += _p("M-52,-58 Q-74,-80 -66,-50 Q-60,-42 -46,-46 Z", C["f_dark"] if female else "#4a4446", 3)       # tail
    if not female:
        g += _p("M-58,-62 q-6,-12 4,-14", sw=3)
    bd = "M-60,-50 Q-58,-80 -10,-78 Q30,-80 46,-60 Q56,-40 36,-22 Q0,-14 -40,-22 Q-62,-30 -60,-50 Z"
    inner = ""
    if female:
        rng = random.Random(6)
        for _ in range(14):
            inner += _ell(rng.uniform(-52, 40), rng.uniform(-70, -30), 5, 3, C["f_dark"], 0, extra='opacity="0.7"')
    else:
        inner += _ell(34, -48, 26, 30, C["m_breast"], 0)
    g += _p(bd, body_c, 0) + _clip(_uid("duckb", female), bd, inner) + _p(bd, sw=3.8)
    wing = "M-40,-60 Q-6,-74 22,-56 Q10,-36 -24,-38 Q-46,-42 -40,-60 Z"
    g += _p(wing, C["f_dark"] if female else C["m_wing"], 3.2)
    g += _p("M-30,-46 L-6,-44 L-10,-38 L-32,-40 Z", C["spec"], 2)
    hx, hy = 40, -98
    g += _band([(28, -66), (34, -82), (hx, hy + 8)], 30, 28, head_c)
    if not female:
        g += _p("M23,-72 Q34,-68 46,-74", sw=6, stroke=CREAM)
    g += _circ(hx, hy, 22, head_c, 3.6)
    g += _p(f"M{hx + 16},{hy - 2} Q{hx + 40},{hy - 6} {hx + 46},{hy + 4} Q{hx + 40},{hy + 12} {hx + 16},{hy + 10} Z", bill, 3)
    g += _p(f"M{hx + 20},{hy + 5} L{hx + 42},{hy + 5}", sw=1.8)
    g += _a_eye(hx + 4, hy - 6, 4.4, eyes, female) + _blush(hx + 4, hy + 8, 6, 3.6)
    if female:
        g += _p(f"M{hx - 18},{hy - 4} Q{hx},{hy - 2} {hx + 14},{hy - 8}", sw=3, stroke=C["f_dark"])
        g += _bow(hx - 8, hy - 20, 0.7)
    if swim:
        out += _g(g, "translate(0,32)")
        out += _p("M-80,0 Q-60,-6 -40,0 T0,0 T40,0 T80,0", sw=3, stroke=S.shade(P["sea_light"], -0.3))
        return out
    out += _g(g, f"rotate({tilt} 0 -20)") if tilt else g
    return out


# ---- monkey
MONKEY = {"fur": "#9a6a45", "face": "#f2cba2", "dark": "#74492e"}


def _monkey(pose="stand", female=False, eyes="open"):
    C = MONKEY
    fur, face, far = C["fur"], C["face"], S.shade(C["fur"], -0.15)
    out = ""
    sit = pose == "sit"
    base = 34 if sit else 0
    # tail: a long curl
    out += _tube(f"M-24,{-66 + base} Q-80,{-60 + base} -86,{-120 + base} Q-90,{-170 + base} -56,{-170 + base} "
                 f"Q-36,{-166 + base} -42,{-146 + base} Q-48,{-132 + base} -60,{-140 + base}", 9, fur, 3.2)
    if sit:
        out += _ell(-6, -24, 46, 26, far, 3.6)
        out += _ell(26, -10, 22, 10, face, 3)
        out += _ell(-30, -10, 22, 10, S.shade(face, -0.08), 3)
    else:
        legs = {"stand": ((-12, -16), (12, 18)), "walk_a": ((-12, -30), (12, 30)), "wave": ((-12, -16), (12, 18)),
                "walk_b": ((-12, 10), (12, -8))}[pose]
        for (hx, fx_), c in zip(legs, (far, fur)):
            out += _tube(f"M{hx},-56 Q{(hx + fx_) / 2 - 8},-30 {fx_},-14", 18, c, 3.4)
            out += _ell(fx_ + 8, -7, 17, 8, face if c == fur else S.shade(face, -0.1), 3)
    by = -88 + base
    sw = {"walk_a": 1, "walk_b": -1}.get(pose, 0)
    # far arm
    out += _tube(f"M14,{by - 22} Q{24 + 10 * sw},{by + 4} {22 + 14 * sw},{by + 34}", 13, far, 3.2)
    out += _circ(22 + 14 * sw, by + 38, 8, S.shade(face, -0.1), 2.8)
    out += _ell(0, by, 32, 38, fur, 3.8)
    out += _ell(6, by + 8, 20, 24, face, 0, extra='opacity="0.9"')
    hx, hy = 8, by - 62
    out += _circ(hx - 28, hy + 2, 14, fur, 3.2) + _circ(hx - 28, hy + 2, 7, face, 0)
    out += _circ(hx, hy, 32, fur, 3.8)
    out += _p(f"M{hx - 8},{hy - 16} Q{hx + 4},{hy - 26} {hx + 14},{hy - 14} Q{hx + 26},{hy - 26} {hx + 34},{hy - 10} "
              f"Q{hx + 42},{hy + 14} {hx + 26},{hy + 24} Q{hx + 6},{hy + 30} {hx - 6},{hy + 16} Q{hx - 14},{hy} {hx - 8},{hy - 16} Z",
              face, 3)
    out += _a_eye(hx + 8, hy - 6, 4.8, eyes, female) + _a_eye(hx + 26, hy - 6, 4.8, eyes, female)
    out += _circ(hx + 22, hy + 6, 2.2, INK, 0) + _circ(hx + 28, hy + 6, 2.2, INK, 0)
    out += _p(f"M{hx + 12},{hy + 14} Q{hx + 22},{hy + 22} {hx + 32},{hy + 12}", sw=2.6)
    out += _blush(hx + 4, hy + 10, 6, 4) + _blush(hx + 36, hy + 8, 5, 3.5)
    if female:
        out += _bow(hx - 10, hy - 30, 0.8)
    # near arm
    if pose == "wave":
        out += _tube(f"M-14,{by - 22} Q-30,{by - 50} -26,{by - 86}", 13, fur, 3.2)
        out += _ell(-26, by - 96, 10, 12, face, 2.8)
        for k in (0, 1):
            out += _p(f"M{-50 - 10 * k},{by - 110 + 4 * k} q-6,14 0,28", sw=2.6, stroke=P["ink_soft"])
    elif sit:
        out += _tube(f"M-14,{by - 20} Q-20,{by + 20} 4,{by + 34}", 13, fur, 3.2) + _circ(8, by + 36, 8, face, 2.8)
    else:
        out += _tube(f"M-14,{by - 22} Q{-26 - 10 * sw},{by + 4} {-24 - 14 * sw},{by + 34}", 13, fur, 3.2)
        out += _circ(-24 - 14 * sw, by + 38, 8, face, 2.8)
    return out


# ---- hippo
HIPPO = {"body": "#a597b8", "pink": "#e5b2ba", "dark": "#857a99"}


def _hippo(pose="stand", female=False, eyes="open"):
    C = HIPPO
    col = C["body"]
    walk = pose if pose in _FEET4 else "stand"
    fx = tuple(a + b * 0.8 for a, b in zip((-100, 92, -126, 70), _FEET4[walk]))
    lift = _LIFT4[walk]
    bob = 4 if walk != "stand" else 0
    out = ""
    out += _p(f"M-178,{-130 + bob} L-196,{-118 + bob} L-180,{-108 + bob} Z", col, 2.8)
    out += _col_leg((-96, -80 + bob), fx[0], 52, 50, col, lift[0], nails=C["pink"], far=True)
    out += _col_leg((94, -80 + bob), fx[1], 50, 48, col, lift[1], nails=C["pink"], far=True)
    out += _p(S.blob(-20, -122 + bob, 162, 90, 0.03, 12, seed=6), col, 4)
    out += _ell(-20, -52 + bob, 130, 24, C["pink"], 0, extra='opacity="0.55"')
    out += _p(f"M-140,{-170 + bob} Q-80,{-214 + bob} 0,{-212 + bob}", sw=4, stroke=S.shade(col, 0.3), extra='opacity="0.6"')
    out += _col_leg((-122, -70 + bob), fx[2], 56, 54, col, lift[2], nails=C["pink"])
    out += _col_leg((70, -70 + bob), fx[3], 54, 52, col, lift[3], nails=C["pink"])
    hx, hy = 128, -150 + bob
    yawn = pose == "yawn"
    for ex_ in (hx - 22, hx + 2):
        out += _ell(ex_, hy - 44, 9, 12, col, 3) + _ell(ex_, hy - 44, 4, 6, C["pink"], 0)
    out += _ell(hx, hy, 54, 46, col, 4)
    if yawn:
        out += _p(f"M{hx + 20},{hy - 4} Q{hx + 96},{hy - 70} {hx + 128},{hy - 30} Q{hx + 120},{hy + 10} {hx + 40},{hy + 18} Z",
                  col, 4)                                                    # upper jaw lifted
        out += _p(f"M{hx + 30},{hy + 14} Q{hx + 118},{hy - 24} {hx + 120},{hy - 20} Q{hx + 136},{hy + 40} {hx + 70},{hy + 66} "
                  f"Q{hx + 30},{hy + 66} {hx + 30},{hy + 14} Z", P["mouth_inside"], 3.6)
        out += _ell(hx + 80, hy + 44, 30, 12, _TONGUE, 0)
        out += _p(f"M{hx + 30},{hy + 36} Q{hx + 60},{hy + 90} {hx + 112},{hy + 50} Q{hx + 132},{hy + 40} {hx + 134},{hy + 24} "
                  f"Q{hx + 130},{hy + 70} {hx + 80},{hy + 80} Q{hx + 40},{hy + 80} {hx + 30},{hy + 36} Z", C["pink"], 3.6)
        for tx, ty in ((hx + 104, hy - 16), (hx + 66, hy - 2)):
            out += _rect(tx - 6, ty, 12, 16, CREAM, 2.4, rx=5)
        out += _circ(hx + 116, hy - 48, 3.4, INK, 0)
    else:
        out += _ell(hx + 52, hy + 26, 62, 46, C["pink"], 4)
        out += _ell(hx + 78, hy - 6, 6, 4, S.shade(C["pink"], -0.45), 0) + _ell(hx + 100, hy + 2, 6, 4, S.shade(C["pink"], -0.45), 0)
        out += _p(f"M{hx + 30},{hy + 46} Q{hx + 66},{hy + 62} {hx + 102},{hy + 44}", sw=3.2)
        out += _ell(hx + 50, hy + 20, 16, 6, HILITE, 0, extra='opacity="0.4"')
    ex, ey = hx + 16, hy - 24
    out += _ell(ex, ey + 2, 13, 12, col, 3)
    out += _a_eye(ex + 2, ey, 6, "closed" if yawn else eyes, female)
    out += _blush(hx + 20, hy + 8, 10, 6)
    if female:
        out += _bow(hx - 12, hy - 58, 0.9)
    return out


# ---- fox
FOX = {"coat": "#e3874a", "white": "#f7efe0", "sock": "#5e4436"}


def _fox_head(hx, hy, eyes, female, rot=0.0):
    C = FOX
    col = C["coat"]
    out = ""
    for dx, k in ((-26, 0.9), (-4, 1.0)):
        out += _p(f"M{hx + dx - 12},{hy - 14} L{hx + dx - 4},{hy - 14 - 38 * k} L{hx + dx + 14},{hy - 18} Z", col, 3.2)
        out += _p(f"M{hx + dx - 6},{hy - 18} L{hx + dx - 3},{hy - 12 - 28 * k} L{hx + dx + 8},{hy - 20} Z", C["sock"], 0)
    hd = f"M{hx - 34},{hy - 6} Q{hx - 30},{hy - 30} {hx - 2},{hy - 28} Q{hx + 24},{hy - 24} {hx + 50},{hy + 6} " \
         f"Q{hx + 44},{hy + 16} {hx + 20},{hy + 20} Q{hx - 20},{hy + 30} {hx - 34},{hy - 6} Z"
    out += _p(hd, col, 0) + _clip(_uid("foxh"), hd, _p(f"M{hx - 10},{hy + 30} Q{hx + 6},{hy + 2} {hx + 52},{hy + 4} L{hx + 52},{hy + 40} Z",
                                                      C["white"], 0)) + _p(hd, sw=3.8)
    out += _circ(hx + 50, hy + 4, 5, INK, 0)
    out += _p(f"M{hx + 30},{hy + 14} Q{hx + 36},{hy + 18} {hx + 42},{hy + 12}", sw=2.4)
    out += _a_eye(hx + 10, hy - 8, 5, eyes, female) + _blush(hx + 14, hy + 6, 6, 4)
    if female:
        out += _bow(hx - 16, hy - 26, 0.75)
    return _g(out, f"rotate({rot:.1f} {hx} {hy})") if rot else out


def _fox(pose="stand", female=False, eyes="open"):
    C = FOX
    col = C["coat"]
    out = ""
    if pose == "sleep":
        out += _p(S.blob(0, -36, 70, 36, 0.04, 10, seed=8), col, 3.8)
        out += _band([(-60, -30), (-40, -2), (20, 4), (70, -4), (88, -20)], 44, 28, col)
        out += _p("M70,-26 Q96,-26 96,-14 Q90,2 66,2 Z", C["white"], 3)
        out += _fox_head(30, -46, "closed", female, rot=14)
        out += _zs(70, -100, 0.7)
        return out
    if pose == "sit":
        out += _band([(-40, -20), (-90, -12), (-120, -30), (-128, -60)], 44, 34, col)
        out += _p("M-118,-46 Q-138,-60 -128,-84 Q-112,-74 -110,-56 Z", C["white"], 3)
        out += _ell(-20, -36, 46, 36, col, 3.8)
        out += _ell(10, -6, 26, 9, col, 3)
        out += _tube("M20,-70 L22,-8", 13, C["sock"], 3) + _tube("M36,-70 L40,-8", 13, C["sock"], 3)
        out += _p("M0,-110 Q34,-120 44,-90 Q46,-60 30,-50 Q10,-60 0,-110 Z", col, 3.8)
        out += _p("M22,-104 Q40,-100 40,-80 Q34,-62 24,-62 Q18,-80 22,-104 Z", C["white"], 0)
        out += _fox_head(34, -128, "open" if eyes == "open" else eyes, female)
        return out
    walk = pose if pose in _FEET4 else "stand"
    fx = tuple(a + b * 0.55 for a, b in zip((-48, 52, -62, 40), _FEET4[walk]))
    lift = tuple(v * 0.6 for v in _LIFT4[walk])
    out += _band([(-60, -84), (-110, -80), (-150, -64), (-170, -40)], 46, 36, col)
    out += _p("M-150,-50 Q-172,-60 -184,-36 Q-170,-20 -152,-34 Z", C["white"], 3)
    for i, (hx, f_, hind) in enumerate(((-44, fx[0], True), (46, fx[1], False), (-56, fx[2], True), (36, fx[3], False))):
        out += _qleg((hx, -70), f_, 18, 10, C["sock"], hind=hind, far=i < 2, ground=-lift[i], bend=0.6)
    bd = [(-74, -84), (-56, -106), (0, -110), (44, -106), (76, -92), (80, -66), (50, -54), (-20, -52), (-66, -60)]
    out += _p(_sm(bd), col, 3.8)
    out += _p("M46,-66 Q70,-70 76,-90 Q86,-70 70,-56 Z", C["white"], 0)
    out += _band([(54, -96), (74, -114), (86, -122)], 40, 34, col)
    out += _fox_head(92, -128, eyes, female)
    return out


def _ark_animal(kind="elephant", pose="stand", female=False, eyes="open", phase=0.0):
    if kind not in ARK_ANIMAL_POSES:
        raise ValueError(f"ark_animal: unknown kind {kind!r}; choose from {ARK_ANIMALS}")
    if pose not in ARK_ANIMAL_POSES[kind]:
        raise ValueError(f"ark_animal: {kind} has no pose {pose!r}; choose from {ARK_ANIMAL_POSES[kind]}")
    if kind == "elephant":
        body = _elephant(pose, female, eyes)
    elif kind == "giraffe":
        body = _giraffe(pose, female, eyes)
    elif kind in _EQUINE:
        body = _equine(kind, pose, female, eyes)
    elif kind == "rabbit":
        body = _rabbit(pose, female, eyes, phase)
    elif kind == "turtle":
        body = _turtle(pose, female, eyes)
    elif kind == "duck":
        body = _duck(pose, female, eyes)
    elif kind == "monkey":
        body = _monkey(pose, female, eyes)
    elif kind == "hippo":
        body = _hippo(pose, female, eyes)
    else:
        body = _fox(pose, female, eyes)
    k = _SIZE[kind] * (0.94 if female and kind not in ("duck",) else 1.0)
    return _upscale(body, k) if abs(k - 1) > 1e-6 else body


def ark_animal(x, y, scale=1.0, facing=1, kind="elephant", pose="stand", female=False, eyes="open", phase=0.0):
    return _place(_ark_animal(kind, pose, female, eyes, phase), x, y, scale, facing)


# ---- butterflies and small birds
BUTTERFLY_COLORS = {"orange": ("#f2a03c", "#7a4a2e"), "blue": ("#79acd9", "#3f5f8a"), "yellow": ("#f5d05c", "#9a7a2e"),
                    "pink": ("#ee9ab0", "#9a4f68"), "purple": ("#a88ad0", "#5f4a86")}


def _butterfly(flap=0.0, color="orange"):
    c, d = BUTTERFLY_COLORS[color] if color in BUTTERFLY_COLORS else (color, S.shade(color, -0.5))
    k = 0.18 + 0.82 * abs(math.cos(math.pi * _clamp(flap)))
    out = ""
    for sx in (-1, 1):
        wing = (f"M0,-2 Q{_f(sx * 20)},-40 {_f(sx * 40)},-34 Q{_f(sx * 50)},-20 {_f(sx * 36)},-4 Z "
                f"M0,0 Q{_f(sx * 30)},4 {_f(sx * 30)},20 Q{_f(sx * 22)},34 {_f(sx * 6)},20 Z")
        g = _p(wing, c, 2.8) + _circ(sx * 28, -24, 5, CREAM, 0) + _circ(sx * 18, 14, 4, CREAM, 0)
        g += _p(f"M{_f(sx * 40)},-34 Q{_f(sx * 50)},-20 {_f(sx * 36)},-4", sw=5, stroke=d)
        out += _g(g, f"scale({k:.3f},1)")
    out += _ell(0, 2, 4.5, 16, P["ink"], 0)
    out += _p("M-1,-12 Q-6,-26 -12,-30 M1,-12 Q6,-26 12,-30", sw=2)
    out += _circ(-12, -30, 2.4, INK, 0) + _circ(12, -30, 2.4, INK, 0)
    return out


def butterfly(x, y, scale=1.0, flap=0.0, color="orange", rot=0.0):
    return _place(_butterfly(flap, color), x, y, scale, 1, rot)


SONGBIRD_COLORS = {"blue": ("#5f92d6", "#f2a35a"), "red": ("#d9574a", "#f0b07a"), "yellow": ("#f2cf4e", "#f7e7a8"),
                   "brown": ("#a87a54", "#ead6b8"), "green": ("#7fb55a", "#f0e2a0")}


def _songbird(wing=0.0, pose="fly", color="blue", female=False):
    back, breast = SONGBIRD_COLORS[color] if color in SONGBIRD_COLORS else (color, S.shade(color, 0.5))
    if female:
        back, breast = S.mix(back, "#b8ab9c", 0.45), S.mix(breast, "#e8ddd0", 0.45)
    out = ""
    if pose == "perch":
        for lx in (-4, 6):
            out += _line(lx, 14, lx + 1, 30, sw=5, color=INK) + _line(lx, 14, lx + 1, 30, sw=2, color="#e8a070")
    sh = (-4, -8)
    if pose == "fly":
        ang, lf, br, arch = _flap(wing)
        out += _wing((sh[0] + 6, sh[1] - 3), ang - 16, 52 * lf * 0.8, S.shade(back, -0.18), None, True, 20, max(0.32, br * 0.9), arch, "sf")
    out += _p("M-22,-2 L-46,-10 L-44,6 Z", back, 3)
    out += _p(S.blob(0, 0, 24, 18, 0.03, 9, seed=1), back, 3.4)
    out += _clip(_uid("sbb", color, female), S.blob(0, 0, 24, 18, 0.03, 9, seed=1), _ell(10, 8, 18, 14, breast, 0))
    out += _p(S.blob(0, 0, 24, 18, 0.03, 9, seed=1), sw=3.4)
    out += _circ(20, -14, 13, back, 3.4)
    out += _clip(_uid("sbh", color, female), "M7,-14 A13,13 0 1 0 33,-14 A13,13 0 1 0 7,-14 Z", _ell(26, -6, 9, 8, breast, 0))
    out += _circ(20, -14, 13, "none", 3.4)
    out += _p("M31,-17 L42,-13 L31,-9 Z", "#e8b04a", 2.4)
    out += _dot_eye(24, -17, 3) + _blush(24, -8, 4, 2.6)
    if pose == "fly":
        out += _wing(sh, ang, 58 * lf, back, None, True, 22, br, arch, "sn")
    else:
        out += _p("M-14,-6 Q2,-12 14,-2 Q4,8 -14,4 Z", S.shade(back, -0.1), 3)
    return out


def songbird(x, y, scale=1.0, facing=1, wing=0.0, pose="fly", color="blue", female=False):
    return _place(_songbird(wing, pose, color, female), x, y, scale, facing)


# ---- pairs
_PAIR_DX = {"elephant": 150, "giraffe": 110, "zebra": 110, "horse": 120, "deer": 110, "rabbit": 50, "turtle": 70,
            "duck": 50, "monkey": 50, "hippo": 140, "fox": 80, "lion": 150, "bear": 140, "sheep": 90, "cow": 120,
            "goat": 90, "donkey": 110, "camel": 140, "dove": 70, "songbird": 50}
# where the ribbon bow goes on the existing library animals (local, scale 1, facing right)
_OLD_BOW = {"sheep": (70, -132), "cow": (124, -188), "goat": (94, -198), "donkey": (116, -236), "camel": (214, -354),
            "bear": (160, -214), "lion": (128, -300)}
PAIR_KINDS = ARK_ANIMALS + ("lion", "bear", "sheep", "cow", "goat", "donkey", "camel", "dove", "songbird")
_OTHER_WALK = {"walk_a": "walk_b", "walk_b": "walk_a"}


def _one(kind, x, y, scale, facing, pose, female, eyes, phase):
    if kind in ARK_ANIMALS:
        p_ = pose if pose in ARK_ANIMAL_POSES[kind] else ("stand" if pose != "hop" else "stand")
        return ark_animal(x, y, scale, facing, kind, p_, female, eyes, phase)
    bow = ""
    if female and kind in _OLD_BOW:
        bx, by = _OLD_BOW[kind]
        if kind in ("lion", "bear") and pose in ("walk_a", "walk_b"):
            by += 6
        bow = _place(_bow(bx, by, 1.0), x, y, scale * (0.8 if kind == "lion" else 1.0), facing)
    if kind == "lion":
        p_ = pose if pose in LION_POSES else "stand"
        k = 0.8
        return lion(x, y, scale * k, facing, pose=p_, variant=1 if female else 0, eyes=eyes if eyes != "happy" else "happy") + bow
    if kind == "bear":
        p_ = pose if pose in BEAR_POSES else "stand"
        return bear(x, y, scale, facing, pose=p_) + bow
    if kind == "sheep":
        p_ = pose if pose in SHEEP_POSES else "stand"
        return sheep(x, y, scale, facing, variant=3 if female else 0, pose=p_) + bow
    if kind in ("cow", "goat", "donkey", "camel"):
        return animal(x, y, scale, facing, kind=kind) + bow
    if kind == "dove":
        return dove(x, y, scale, facing, wing=(phase * 2 - 1) if pose != "stand" else 0.0, pose="stand" if pose == "stand" else "fly")
    if kind == "songbird":
        return songbird(x, y, scale, facing, wing=(phase * 2 - 1), pose="perch" if pose == "stand" else "fly",
                        color="blue", female=female)
    raise ValueError(f"animal_pair: unknown kind {kind!r}; choose from {PAIR_KINDS}")


def animal_pair(kind, x, y, scale=1.0, facing=1, pose="stand", phase=0.0, eyes="open", gap=None):
    """Two of a kind (he and she) side by side for the 'two by two' queue (see module doc)."""
    if kind not in PAIR_KINDS:
        raise ValueError(f"animal_pair: unknown kind {kind!r}; choose from {PAIR_KINDS}")
    sx = 1 if facing >= 0 else -1
    dx = (_PAIR_DX[kind] if gap is None else gap) * scale
    dy = (-18 if kind not in ("dove", "songbird") else -40) * scale
    fpose = _OTHER_WALK.get(pose, pose)
    fphase = (phase + 0.5) % 1.0
    if kind in ("dove", "songbird") and pose != "stand":
        fphase = (phase + 0.35) % 1.0
    back = _one(kind, x + sx * dx, y + dy, scale * 0.96, facing, fpose, True, eyes, fphase)
    front = _one(kind, x, y, scale, facing, pose, False, eyes, phase)
    return back + front


# ====================================================================== 10. Joseph film (Genesis 37-50)
COAT_BANDS = ("#d9534a", "#f2c84b", "#4f86c6", "#6fae55", "#8e64b0", "#ef9440")   # 红 黄 蓝 绿 紫 橙 (= characters)
COAT_BASE = "#f1e6cc"
WHEAT = "#e9c25a"
WHEAT_DARK = "#c4953a"
SILVER = "#cfd3d2"
SILVER_DARK = "#8e9594"
LINEN_P = "#f6f0e2"
LAPIS_P = "#3f6fa8"
CARNELIAN_P = "#c9533f"
MUD = "#d9b98a"
MUD_DARK = "#b8946a"
NILE = "#4f97b5"
PAPYRUS = "#7fa24f"
DIRT = "#9a7a52"
PIT_R = (150, 46)                # pit opening half-width / half-depth (ellipse on the ground, outside view)
PIT_DEPTH = 470                  # cutaway: floor of the pit below the ground line (anchor of a figure inside)
PIT_FLOOR = (0, 470)
CAMEL_LEAD = (300, -150)         # camel(bridle=True): end of the lead rope (local, facing right)
CAMEL_WALK = 40                  # camel: x a walk cycle (phase 0 -> 1) covers at scale 1 is ~2 * 40 = 80 px ... see doc
CHARIOT_STAND = (4, -96)         # chariot: anchor of a person standing in the car (joseph pose 'ride_wave')
CHARIOT_SEAT = (-20, -96)        # chariot: anchor of a person seated in the car (joseph pose 'ride')
EGYPT_SEAT_Y = -73               # egypt_throne: seat top above the floor (pharaoh 'sit_throne', throne=False)
GRANARY_W = 820                  # granary width at scale 1


def _alpha_k(k, progress, n=len(COAT_BANDS)):
    return _clamp(progress * n - k)


# ---------------------------------------------------------------------- the coat of many colours
_COAT_HELD = [(-20, 0), (-60, 6), (-74, 14), (-126, 150), (-98, 164), (-62, 58), (-80, 252), (-40, 262), (0, 258),
              (40, 262), (80, 252), (62, 58), (98, 164), (126, 150), (74, 14), (60, 6), (20, 0), (0, 30)]


def _coat_body_d(torn=False):
    pts = list(_COAT_HELD)
    if torn:                      # ragged hem and a short, torn right sleeve
        hem = [(-80, 252), (-66, 236), (-54, 258), (-38, 240), (-22, 262), (-6, 236), (10, 260), (26, 238), (42, 262),
               (58, 242), (80, 252)]
        pts = pts[:6] + hem + [(62, 58), (88, 110), (100, 96), (98, 118), (114, 102), (74, 14), (60, 6), (20, 0), (0, 30)]
    return "M" + " L".join(f"{_f(x)},{_f(y)}" for x, y in pts) + " Z", pts


def _coat_shape(state="held", torn=False, dirty=False, progress=1.0):
    """The coat on its own (local, see coat_of_colours)."""
    if state == "bundle":         # crumpled up: the coat squashed and twisted, with soft fold lines
        body = _coat_shape("held", torn, dirty, progress)
        out = _g(body, "rotate(-16) scale(0.95,0.55) translate(0,-131)")
        for a, b in (((-50, -30), (-14, 30)), ((24, -40), (44, 24)), ((-80, 6), (-40, 40))):
            out += _p(f"M{a[0]},{a[1]} Q{(a[0] + b[0]) / 2 + 12},{(a[1] + b[1]) / 2} {b[0]},{b[1]}", sw=3,
                      stroke=S.shade(COAT_BASE, -0.45), extra='opacity="0.6"')
        return out
    if state == "folded":
        out = ""
        for k, (w, y0) in enumerate(((150, -12), (140, -34), (130, -54))):
            d = f"M{-w / 2},{y0} L{w / 2},{y0} L{w / 2 + 4},{y0 + 22} L{-w / 2 - 4},{y0 + 22} Z"
            inner = "".join(_rect(-w / 2 - 10 + j * 26, y0 - 2, 26, 30, COAT_BANDS[(j + k * 2) % 6], 0) for j in range(8))
            out += _p(d, COAT_BASE, 0) + _clip(_uid("cfold", k), d, inner) + _p(d, sw=3.6)
        return out
    d, pts = _coat_body_d(torn)
    inner = ""
    for k in range(15):
        j = k % 6
        a = _alpha_k(j, progress)
        if a <= 0:
            continue
        op = f'opacity="{a:.2f}"' if a < 1 else ""
        inner += _rect(-130, -4 + k * 19, 260, 19.5, COAT_BANDS[j], 0, extra=op)
    if progress > 0:
        for k in range(1, 15):
            inner += _line(-130, -4 + k * 19, 130, -4 + k * 19, sw=1.6, color=S.shade(COAT_BASE, -0.3),
                           extra='opacity="0.5"')
    inner += _p("M-34,40 Q-40,150 -30,250 M30,40 Q38,150 30,250", sw=3, stroke=S.shade(COAT_BASE, -0.4),
                extra='opacity="0.35"')
    if dirty:
        inner += _coat_dirt(1.0)
    out = _p(d, COAT_BASE, 0) + _clip(_uid("coat", torn, dirty, round(progress, 3)), d, inner) + _p(d, sw=4)
    out += _p("M-20,0 L0,30 L20,0", sw=3.2)                                     # neck opening
    out += _p("M-62,52 Q-58,30 -60,8 M62,52 Q58,30 60,8", sw=2.4, stroke=S.shade(COAT_BASE, -0.4), extra='opacity="0.6"')
    if torn:                      # a rip in the body (a dark slit, never blood)
        out += _p("M-30,120 L-18,150 L-28,170 L-14,196 L-24,200 L-36,176 L-26,152 L-40,124 Z", "#6b5442", 2.6)
    return out


def _coat_dirt(k=1.0):
    rng = random.Random(7)
    s = ""
    for _ in range(9):
        x, y, r = rng.uniform(-80, 80) * k, rng.uniform(20, 240) * (k if k < 1.1 else 0.35) - (0 if k < 1.1 else 60), \
            rng.uniform(10, 22)
        s += _ell(x, y, r * 1.4, r, "#8a6a45", 0, extra='opacity="0.42"')
    return s


def coat_of_colours(x, y, scale=1.0, facing=1, state="held", torn=False, dirty=False, progress=1.0, rot=0.0):
    """The coat of many colours on its own (see module doc, section 10)."""
    if state not in ("held", "lying", "folded", "bundle"):
        raise ValueError(f"coat_of_colours: state must be held / lying / folded / bundle, not {state!r}")
    body = _coat_shape("held" if state == "lying" else state, torn, dirty, _clamp(progress))
    if state == "lying":          # laid flat on the ground, seen from a little above (hem toward facing)
        body = _g(body, "translate(0,-50) scale(1,0.42) translate(-131,0) rotate(-90)")
    return _place(body, x, y, scale, facing, rot)


# ---------------------------------------------------------------------- wheat sheaves (the dream)
def _ear(x, y, ang, L=34, col=WHEAT):
    """One ear of wheat (a plump spike of grains with whiskers) pointing at screen angle ang (deg, -90 = up)."""
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    out = ""
    for k in range(5):
        t = 0.18 + k * 0.17
        cx, cy = x + dx * L * t, y + dy * L * t
        for sg in (-1, 1):
            gx, gy = cx + nx * 4.2 * sg, cy + ny * 4.2 * sg
            out += _ell(gx, gy, 5.2, 3.2, col, 1.8, extra=f'transform="rotate({ang:.0f} {_f(gx)} {_f(gy)})"')
    out += _ell(x + dx * L * 1.02, y + dy * L * 1.02, 4.5, 3.0, col, 1.8, extra=f'transform="rotate({ang:.0f} {_f(x + dx * L * 1.02)} {_f(y + dy * L * 1.02)})"')
    for sg in (-1, 1):            # whiskers
        out += _line(x + dx * L * 0.9, y + dy * L * 0.9, x + dx * L * 1.5 + nx * 7 * sg, y + dy * L * 1.5 + ny * 7 * sg,
                     sw=1.4, color=WHEAT_DARK)
    return out


def _sheaf(bow=0.0, glow=0.0, ripe=1.0, seed=0):
    """A bound sheaf standing on its stalk ends: anchor bottom centre; the tie at y=-92, ears up to ~-230.
    bow 0..1 bends the top (above the tie) toward +x by up to 62 deg and leans the bundle 8 deg."""
    col = S.mix("#9fbf5a", WHEAT, _clamp(ripe))
    dark = S.mix("#6f9040", WHEAT_DARK, _clamp(ripe))
    rng = random.Random(seed)
    out = ""
    if glow > 0:
        gid = _uid("shglow", seed, glow)
        out += f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.95 * glow), (0.6, P["gold"], 0.35 * glow), (1, P["gold"], 0)])}</defs>'
        out += _ell(0, -150, 170, 190, f"url(#{gid})", 0)
    # lower bundle: stalks spreading a little toward the cut ends
    low = "M-26,-92 L-40,-4 Q0,6 40,-4 L26,-92 Z"
    stalks = ""
    for k in range(-6, 7):
        stalks += _line(k * 2.2, -92, k * 6.4, 0, sw=2.0, color=dark, extra='opacity="0.75"')
    out += _p(low, col, 0) + _clip(_uid("shl", seed, ripe), low, stalks) + _p(low, sw=3.6)
    for k in range(-5, 6):        # cut ends
        out += _ell(k * 7.2, -2, 3.4, 2.2, S.shade(col, -0.25), 1.4)
    # upper part: a fan of stalks with ears, bent at the tie
    top = ""
    upper = "M-24,-92 Q-46,-150 -58,-196 L58,-196 Q46,-150 24,-92 Z"
    st_ = ""
    for k in range(-6, 7):
        st_ += _line(k * 2.0, -92, k * 9.5, -200, sw=2.0, color=dark, extra='opacity="0.7"')
    top += _p(upper, col, 0) + _clip(_uid("shu", seed, ripe), upper, st_) + _p(upper, sw=3.6)
    angs = [-90 + a for a in (-38, -26, -14, -4, 6, 16, 28, 40)]
    for i, a in enumerate(angs):
        bx, by = 9.5 * (i - 3.5) * 1.3, -196 + abs(i - 3.5) * 4
        top += _ear(bx, by, a + rng.uniform(-4, 4), 30 + rng.uniform(-3, 5), col)
    for i, a in enumerate((-110, -78, -96, -64)):
        top += _ear(rng.uniform(-30, 30), -190 - rng.uniform(4, 16), a, 28, S.shade(col, 0.08))
    ang = 62 * _clamp(bow)
    out += f'<g transform="rotate({ang:.1f} 0 -92)">{top}</g>'
    # the twisted straw tie
    out += _tube("M-29,-96 Q0,-84 29,-96", 11, S.shade(col, -0.18), 3.2)
    out += _p("M-18,-98 l6,8 M-4,-96 l6,8 M10,-97 l6,8", sw=1.8, stroke=S.shade(col, -0.45))
    lean = 8 * _clamp(bow)
    return _g(out, f"rotate({lean:.1f})") if lean else out


def wheat_sheaf(x, y, scale=1.0, facing=1, bow=0.0, rise=1.0, glow=0.0, ripe=1.0, kind="standing", seed=0):
    """A sheaf of wheat (see module doc, section 10)."""
    if kind not in ("standing", "bundle"):
        raise ValueError(f"wheat_sheaf: kind must be 'standing' or 'bundle', not {kind!r}")
    body = _sheaf(bow, glow, ripe, seed)
    r = _clamp(rise) if kind == "standing" else 0.0
    if r < 1.0:                   # lying on its side (a bundle) .. standing up: rotate about the cut ends
        u = 1 - r
        body = _g(body, f"translate({_f(118 * u)},{_f(-38 * u)}) rotate({-86 * u:.1f} 0 0)")
    return _place(body, x, y, scale, facing)


# ---------------------------------------------------------------------- the dry pit
def _rim_stone(cx, cy, rx, ry, col, sw=3.2):
    return _ell(cx, cy, rx, ry, col, sw)


def _pit_outside(part="all", rope=0.0):
    rx, ry = PIT_R
    stones = ("#c9bca6", "#b9b2a6", "#d6c7aa", "#a8a49c", "#cdb79a")
    out = ""
    if part in ("all", "back"):
        out += _ell(0, 6, rx + 70, ry + 34, P["sand_dark"], 0, extra='opacity="0.35" filter="url(#soft)"')
        hole = f"M{-rx},0 A{rx},{ry} 0 1 1 {rx},0 A{rx},{ry} 0 1 1 {-rx},0 Z"
        gid = _uid("pitg", rx)
        out += f'<defs>{S.lin_grad(gid, [(0, "#6b5442"), (0.5, "#4a3a30"), (1, "#3a2e28")], 0, 0, 0, 1)}</defs>'
        out += _p(hole, f"url(#{gid})", 0)
        inner = ""
        for k in range(4):        # courses of the stone lining on the far inner wall
            yy = -ry + 12 + k * 18
            for j in range(-6, 7):
                xx = j * 24 + (12 if k % 2 else 0)
                inner += _ell(xx, yy, 12, 7, "#7a6655", 1.8, stroke="#3a2e28", extra='opacity="0.85"')
        out += _clip(gid + "c", hole, inner + _ell(0, ry * 0.9, rx * 0.9, ry * 0.8, "#2e2420", 0, extra='opacity="0.7"'))
        for j in range(18):       # back rim stones
            a = math.pi + math.pi * j / 17
            out += _rim_stone(rx * 1.04 * math.cos(a), ry * 1.06 * math.sin(a) - 4, 19, 12, stones[j % 5])
        if rope > 0:
            L = 10 + 120 * _clamp(rope)
            out += _tube(f"M60,-10 Q66,{_f(L * 0.5)} 58,{_f(L)}", 5, P["wood_light"], 2.4)
    if part in ("all", "front"):
        for j in range(18):       # front rim stones (cover the lower edge of the hole)
            a = math.pi * j / 17
            out += _rim_stone(rx * 1.05 * math.cos(a), ry * 1.10 * math.sin(a) + 2, 20, 13, stones[(j + 2) % 5])
        rng = random.Random(3)
        for _ in range(6):        # dry grass tufts by the rim
            x0 = rng.choice((-1, 1)) * rng.uniform(rx * 0.7, rx * 1.2)
            y0 = rng.uniform(-ry * 0.2, ry * 1.1) + 10
            for k in range(4):
                out += _line(x0, y0, x0 + (k - 1.5) * 7, y0 - 22 - k % 2 * 8, sw=2.6, color=P["leaf_dry"])
    return out


def _pit_cutaway(rope=0.0, w=400):
    rx = PIT_R[0]
    D = PIT_DEPTH
    out = ""
    soil = f"M{-w},0 L{w},0 L{w},{D + 70} L{-w},{D + 70} Z"
    gid = _uid("pitsoil", w)
    out += f'<defs>{S.lin_grad(gid, [(0, "#c9a070"), (0.5, "#b0845a"), (1, "#8f6a48")], 0, 0, 0, 1)}</defs>'
    layers = ""
    rng = random.Random(11)
    for k in range(1, 5):
        yy = k * (D + 70) / 5
        layers += _p(_sm([(-w - 20, yy), (-w / 2, yy + rng.uniform(-14, 14)), (0, yy + rng.uniform(-14, 14)),
                          (w / 2, yy + rng.uniform(-14, 14)), (w + 20, yy)], closed=False), sw=3,
                     stroke=S.shade("#b0845a", -0.2), extra='opacity="0.4"')
    for _ in range(26):
        layers += _ell(rng.uniform(-w, w), rng.uniform(20, D + 60), rng.uniform(5, 12), rng.uniform(4, 8),
                       rng.choice(("#c9bca6", "#a8a49c", "#d6c7aa")), 2.2)
    out += _clip(gid + "c", soil, _rect(-w - 10, -10, 2 * w + 20, D + 90, f"url(#{gid})", 0) + layers)
    # the shaft: back wall of stone courses, side linings, sandy dry floor
    shaft = f"M{-rx},0 L{rx},0 L{rx},{D} L{-rx},{D} Z"
    sg = _uid("pitsh", rx)
    out += f'<defs>{S.lin_grad(sg, [(0, "#8a7462"), (0.45, "#5e4c40"), (1, "#4a3c34")], 0, 0, 0, 1)}</defs>'
    wall = ""
    for k in range(int(D / 30) + 1):
        yy = k * 30 + 14
        for j in range(-6, 7):
            xx = j * 46 + (23 if k % 2 else 0)
            wall += _rect(xx - 21, yy - 13, 42, 26, "#7a6655", 2.0, rx=8, stroke="#3e322b",
                          extra='opacity="0.9"')
    light = _p(f"M{-rx + 20},0 L{rx - 60},0 L{rx - 30},{D} L{-rx + 70},{D} Z", P["glow"], 0, extra='opacity="0.16"')
    out += _p(shaft, f"url(#{sg})", 0) + _clip(sg + "c", shaft, wall + light) + _p(shaft, sw=4)
    for sx in (-1, 1):            # side linings (stones seen in section)
        for k in range(int(D / 34) + 1):
            out += _rect(sx * rx - (24 if sx > 0 else 0), k * 34 + 2, 24, 32, ("#b9b2a6", "#a8a49c", "#c9bca6")[k % 3],
                         3, rx=6)
    floor = f"M{-rx},{D - 24} Q-60,{D - 34} 0,{D - 28} Q70,{D - 36} {rx},{D - 22} L{rx},{D} L{-rx},{D} Z"
    out += _p(floor, "#d9b98a", 3.4)
    for xx, r in ((-96, 7), (-40, 5), (52, 8), (104, 6), (10, 4)):
        out += _ell(xx, D - 22, r * 1.4, r * 0.8, "#a8a49c", 2)
    for xx in (-120, 86):
        for k in range(4):
            out += _line(xx, D - 26, xx + (k - 1.5) * 6, D - 46 - (k % 2) * 8, sw=2.4, color=P["leaf_dry"])
    # rim stones at ground level and the ground line beyond
    out += _line(-w, 0, -rx - 26, 0, sw=4) + _line(rx + 26, 0, w, 0, sw=4)
    for sx in (-1, 1):
        for j in range(3):
            out += _rim_stone(sx * (rx + 4 + j * 26), -10 + (j % 2) * 3, 17, 12, ("#c9bca6", "#d6c7aa", "#b9b2a6")[j])
    if rope > 0:
        L = 20 + (D - 60) * _clamp(rope)
        out += _tube(f"M{rx - 30},-14 Q{rx - 18},{_f(L * 0.5)} {rx - 36},{_f(L)}", 6, P["wood_light"], 2.6)
    return out


def pit(x, y, scale=1.0, facing=1, view="outside", part="all", rope=0.0, width=400):
    """The dry, empty pit (see module doc, section 10)."""
    if view == "cutaway":
        return _place(_pit_cutaway(rope, width), x, y, scale, facing)
    if view != "outside":
        raise ValueError(f"pit: view must be 'outside' or 'cutaway', not {view!r}")
    if part not in ("all", "back", "front"):
        raise ValueError(f"pit: part must be all / back / front, not {part!r}")
    return _place(_pit_outside(part, rope), x, y, scale, facing)


def in_pit(markup, x, y, scale=1.0):
    """Clip figure markup to the pit opening seen from outside (the part above the rim stays visible)."""
    rx, ry = PIT_R[0] * scale, PIT_R[1] * scale
    d = (f"M{_f(x - rx)},{_f(y)} A{_f(rx)},{_f(ry)} 0 0 0 {_f(x + rx)},{_f(y)} L{_f(x + rx)},{_f(y - 2000)} "
         f"L{_f(x - rx)},{_f(y - 2000)} Z")
    return _clip(_uid("inpit", x, y, scale), d, markup)


# ---------------------------------------------------------------------- silver coins
def _coin(cx, cy, r=13.0, tilt=0.0):
    """One silver coin (local markup) with a rim, a stamped mark and a highlight."""
    ry = r * (1 - 0.55 * tilt)
    out = _ell(cx, cy + 2.4, r, ry, SILVER_DARK, 2.2)
    out += _ell(cx, cy, r, ry, SILVER, 2.4)
    out += _ell(cx, cy, r * 0.68, ry * 0.68, "none", 1.4, stroke=SILVER_DARK, extra='opacity="0.8"')
    out += _p(f"M{_f(cx - r * 0.25)},{_f(cy)} L{_f(cx)},{_f(cy - ry * 0.32)} L{_f(cx + r * 0.25)},{_f(cy)} "
              f"L{_f(cx)},{_f(cy + ry * 0.32)} Z", SILVER_DARK, 0, extra='opacity="0.7"')
    out += _ell(cx - r * 0.38, cy - ry * 0.4, r * 0.22, ry * 0.12, HILITE, 0, extra='opacity="0.9"')
    return out


def _coin_pouch(open_=True):
    """Leather money pouch, anchor bottom centre; open_ shows silver coins at the mouth."""
    out = _p("M-40,-10 Q-52,-50 -26,-72 L26,-72 Q52,-50 40,-10 Q0,6 -40,-10 Z", LEATHER, 4)
    out += _p("M-26,-72 Q0,-60 26,-72", sw=3)
    if open_:
        for k, (dx, dy) in enumerate(((-12, -76), (8, -80), (-2, -88), (18, -72))):
            out += _coin(dx, dy, 10, 0.5)
    out += _tube("M-28,-66 Q0,-56 28,-66", 4, CORD, 2)
    out += _p("M24,-64 q14,10 6,24", sw=4, stroke=INK) + _p("M24,-64 q14,10 6,24", sw=2, stroke=CORD)
    out += _ell(-14, -36, 9, 14, S.shade(LEATHER, 0.25), 0, extra='opacity="0.6"')
    return out


def coins(x, y, scale=1.0, n=20, kind="pile", seed=0):
    """Silver coins (see module doc, section 10)."""
    n = max(0, int(n))
    out = ""
    if kind == "row":             # counted out in rows of 10 (count up by n)
        for i in range(n):
            r, c = divmod(i, 10)
            out += _coin(-135 + c * 30, -16 - r * 34, 13, 0.45)
    elif kind == "stacks":        # stacks of 5
        for i in range(n):
            s_, k = divmod(i, 5)
            out += _coin(-60 + s_ * 34, -10 - k * 7, 14, 0.6)
    elif kind == "pouch":
        out += _coin_pouch(True)
        for i in range(min(n, 6)):
            out += _coin(46 + i * 11, -6 - (i % 2) * 6, 11, 0.6)
    elif kind == "pile":
        rng = random.Random(seed)
        placed = 0
        row = 0
        while placed < n:
            w = max(1, 7 - row)
            for j in range(w):
                if placed >= n:
                    break
                out += _coin((j - (w - 1) / 2) * 22 + rng.uniform(-4, 4), -10 - row * 10 + rng.uniform(-2, 2), 13, 0.62)
                placed += 1
            row += 1
    else:
        raise ValueError(f"coins: kind must be pile / row / stacks / pouch, not {kind!r}")
    return _place(out, x, y, scale)


# ---------------------------------------------------------------------- Egyptian scenery
def _pyramid(cx, w, h, col, lit, haze=0.0):
    out = _p(f"M{_f(cx - w / 2)},0 L{_f(cx)},{_f(-h)} L{_f(cx + w / 2)},0 Z", col, 4)
    out += _p(f"M{_f(cx)},{_f(-h)} L{_f(cx + w / 2)},0 L{_f(cx + w * 0.12)},0 Z", lit, 0)
    d = f"M{_f(cx - w / 2)},0 L{_f(cx)},{_f(-h)} L{_f(cx + w / 2)},0 Z"
    lines = ""
    for k in range(1, 12):
        yy = -h * k / 12
        lines += _line(cx - w / 2 * (1 - k / 12), yy, cx + w / 2 * (1 - k / 12), yy, sw=1.8,
                       color=S.shade(col, -0.18), extra='opacity="0.5"')
    out += _clip(_uid("pyr", cx, w, h), d, lines)
    out += _p(d, sw=4)
    out += _p(f"M{_f(cx - w * 0.04)},{_f(-h * 0.92)} L{_f(cx)},{_f(-h)} L{_f(cx + w * 0.04)},{_f(-h * 0.92)} Z", P["gold"], 2.4)
    return out


def _pyramids(n=3, haze=0.0, ground=True):
    sand = S.mix(P["sand"], P["sky_day"], 0.6 * haze)
    lit = S.mix(P["sand_light"], P["sky_day"], 0.6 * haze)
    out = ""
    specs = [(-420, 520, 330), (180, 820, 520), (640, 380, 240)][:max(1, min(3, n))]
    for cx, w, h in sorted(specs, key=lambda s: -s[2]):
        out += _pyramid(cx, w, h, sand, lit)
    if ground:
        out += _p("M-760,0 Q-300,-16 0,-6 Q400,-14 900,0 L900,24 L-760,24 Z", S.shade(sand, -0.08), 3)
    return out


def pyramids(x, y, scale=1.0, n=3, haze=0.0, facing=1, ground=True):
    """The pyramids on the horizon (see module doc, section 10)."""
    return _place(_pyramids(n, _clamp(haze), ground), x, y, scale, facing, filt="wobble")


def _papyrus(x, y, h, k=1.0, sway=0.0):
    out = ""
    for j, (dx, hh, a) in enumerate(((-10, h, -8), (0, h * 1.15, 2), (12, h * 0.9, 10), (-20, h * 0.75, -16))):
        tx, ty = x + dx * k + sway * 8 + math.sin(math.radians(a)) * hh, y - hh * k
        out += _line(x + dx * k * 0.3, y, tx, ty, sw=3.2 * k, color=S.shade(PAPYRUS, -0.25))
        umb = f"M{_f(tx)},{_f(ty + 4 * k)} L{_f(tx - 22 * k)},{_f(ty - 16 * k)} Q{_f(tx)},{_f(ty - 30 * k)} {_f(tx + 22 * k)},{_f(ty - 16 * k)} Z"
        out += _p(umb, PAPYRUS if j % 2 else S.shade(PAPYRUS, 0.15), 2.6 * k)
        for q in (-14, -5, 5, 14):
            out += _line(tx, ty, tx + q * k, ty - 22 * k, sw=1.4 * k, color=S.shade(PAPYRUS, -0.35), extra='opacity="0.7"')
    return out


def _nile(x0, x1, y, width=150.0, phase=0.0, seed=0, reeds=True, s=1.0):
    rng = random.Random(seed)
    n = max(6, int((x1 - x0) / (120 * s)))
    top, bot = [], []
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        top.append((xx, y - width * 0.5 + 6 * s * math.sin(i * 1.1 + seed)))
        bot.append((xx, y + width * 0.5 + 8 * s * math.sin(i * 0.9 + seed + 1)))
    d = _sm(top, closed=False) + " " + " ".join(f"L{_f(px)},{_f(py)}" for px, py in reversed(bot)) + " Z"
    gid = _uid("nile", x0, x1, y, width)
    out = f'<defs>{S.lin_grad(gid, [(0, S.shade(NILE, 0.35)), (0.5, NILE), (1, S.shade(NILE, -0.12))], 0, 0, 0, 1)}</defs>'
    bank = _sm([(x, yy - 16 * s) for x, yy in top], closed=False) + " " + " ".join(
        f"L{_f(px)},{_f(py + 26 * s)}" for px, py in reversed(bot)) + " Z"
    out += _p(bank, S.mix(P["grass"], P["sand"], 0.35), 3 * s)
    out += _p(d, f"url(#{gid})", 0)
    inner = ""
    L = 90 * s
    for j in range(int((x1 - x0) / L) + 3):
        for r in range(3):
            xx = x0 + ((j * L + r * L * 0.37 + phase * L) % (x1 - x0 + L)) - L / 2
            yy = y + (r - 1) * width * 0.28
            inner += _p(f"M{_f(xx)},{_f(yy)} q{_f(14 * s)},{_f(-5 * s)} {_f(30 * s)},0", sw=3 * s, stroke=P["foam"],
                        extra='opacity="0.8"')
    for _ in range(int((x1 - x0) / (260 * s))):
        lx, ly = rng.uniform(x0, x1), y + rng.uniform(-0.3, 0.35) * width
        inner += _ell(lx, ly, 18 * s, 7 * s, P["leaf"], 2 * s)
        if rng.random() < 0.5:
            inner += _ell(lx + 6 * s, ly - 6 * s, 6 * s, 5 * s, "#f2c6d6", 1.8 * s)
    out += _clip(gid + "c", d, inner)
    out += _p(d, "none", 3.6 * s)
    if reeds:
        for i in range(int((x1 - x0) / (170 * s))):
            xx = x0 + (i + rng.uniform(0.1, 0.9)) * 170 * s
            k = min(n, max(0, int((xx - x0) / (x1 - x0) * n)))
            out += _papyrus(xx, bot[k][1] + 10 * s, rng.uniform(70, 110), s * rng.uniform(0.8, 1.05))
    return out


def nile(x0, x1, y, width=150.0, scale=1.0, phase=0.0, seed=0, reeds=True):
    """The Nile: a wide river band in absolute stage coordinates (see module doc, section 10)."""
    return _place(_nile(x0, x1, y, width * scale, phase, seed, reeds, scale), 0, 0, 1.0)


def papyrus(x, y, scale=1.0, sway=0.0):
    """A clump of papyrus (anchor bottom centre), ~130 px tall."""
    return _place(_papyrus(0, 0, 100, 1.0, sway), x, y, scale)


def _lotus_column(height=420, col=None):
    col = col or "#efe2c4"
    out = _rect(-46, -24, 92, 24, S.shade(col, -0.1), 3.6, rx=4)
    out += _p(f"M-30,-24 L-34,{-height + 70} L34,{-height + 70} L30,-24 Z", col, 4)
    for k in range(1, 4):         # fluting
        out += _line(-30 + k * 15, -30, -32 + k * 16, -height + 76, sw=1.8, color=S.shade(col, -0.2), extra='opacity="0.7"')
    for yy in (-height + 92, -height + 108):
        out += _rect(-36, yy, 72, 9, (LAPIS_P if yy % 2 else CARNELIAN_P), 2.4, rx=2)
    cap = f"M-34,{-height + 72} Q-74,{-height + 30} -66,{-height + 4} L66,{-height + 4} Q74,{-height + 30} 34,{-height + 72} Z"
    out += _p(cap, "#7fa24f", 4)
    for j in range(-3, 4):
        out += _p(f"M{j * 9},{-height + 70} Q{j * 18},{-height + 30} {j * 19},{-height + 6}", sw=2.4,
                  stroke=("#3f6fa8", "#e9d9ae")[j % 2], extra='opacity="0.85"')
    out += _rect(-72, -height - 16, 144, 22, S.shade(col, -0.05), 3.6, rx=3)
    return out


def egypt_column(x, y, scale=1.0, height=420):
    """A painted papyrus column (see module doc, section 10)."""
    return _place(_lotus_column(height), x, y, scale)


def _egypt_house(variant=0):
    wall, dark = "#efe2c4", "#d8c49a"
    out = ""
    if variant % 2 == 0:          # plain whitewashed house: flat roof, high small windows, a painted door
        out += _p("M-280,0 L-280,-420 L300,-420 L300,0 Z", wall, 4)
        out += _p("M300,0 L300,-420 L350,-450 L350,-24 Z", dark, 4)
        out += _p("M-280,-420 L-230,-450 L350,-450 L300,-420 Z", S.shade(wall, 0.08), 4)
        out += _rect(-290, -432, 600, 18, S.shade(dark, -0.05), 3.4, rx=3)
        for xx in (-200, 150):
            out += _rect(xx, -330, 60, 34, "#4a3a34", 3.4, rx=2)
            for k in (1, 2):
                out += _line(xx + k * 20, -330, xx + k * 20, -296, sw=3, color=wall)
        out += _rect(-60, -260, 130, 260, "#5a3a2a", 4, rx=4)
        out += _rect(-74, -286, 158, 28, LAPIS_P, 3.4, rx=3)
        for xx in range(-62, 80, 18):
            out += _circ(xx, -272, 4, P["gold"], 0)
        out += _rect(-60, -260, 130, 260, "none", 4, rx=4)
        out += _p("M-280,-80 Q0,-70 300,-84", sw=6, stroke="#d8c49a", extra='opacity="0.6"')
        for xx, yy in ((-250, -60), (240, -40), (-150, -200), (210, -230)):
            out += _ell(xx, yy, 14, 6, S.shade(wall, -0.12), 0, extra='opacity="0.6"')
        return out
    # villa with a columned porch (Potiphar's house)
    out += _p("M-420,0 L-420,-470 L420,-470 L420,0 Z", wall, 4)
    out += _rect(-440, -490, 880, 26, S.shade(dark, -0.05), 3.6, rx=3)
    out += _rect(-300, -360, 600, 360, "#6b5442", 4)
    out += _rect(-60, -260, 120, 260, "#3e322b", 4, rx=4)
    for xx in (-240, 240):
        out += _rect(xx - 30, -300, 60, 40, "#4a3a34", 3.2, rx=2)
    out += _rect(-320, -380, 640, 26, P["terracotta"], 3.6, rx=3)
    for xx in range(-300, 320, 40):
        out += _p(f"M{xx},-376 l10,10 l10,-10", sw=2.4, stroke=P["gold"])
    for xx in (-330, -110, 110, 330):
        out += _g(_lotus_column(380), f"translate({xx},0) scale(0.9)")
    out += _rect(-440, -12, 880, 14, S.shade(dark, -0.1), 3.4, rx=3)
    return out


def egypt_house(x, y, scale=1.0, variant=0, facing=1):
    """An Egyptian house (see module doc, section 10)."""
    return _place(_egypt_house(variant), x, y, scale, facing, filt="wobble")


# ---------------------------------------------------------------------- grain, granary
def _grain_heap(w, h, seed=0):
    rng = random.Random(seed)
    d = f"M{_f(-w / 2)},0 Q{_f(-w * 0.22)},{_f(-h * 1.05)} 0,{_f(-h)} Q{_f(w * 0.22)},{_f(-h * 1.05)} {_f(w / 2)},0 Z"
    inner = ""
    for _ in range(int(w * h / 260) + 6):
        gx, gy = rng.uniform(-w / 2, w / 2), rng.uniform(-h, 0)
        inner += _ell(gx, gy, 3.6, 2.2, WHEAT_DARK, 0, extra=f'transform="rotate({rng.uniform(-50, 50):.0f} {_f(gx)} {_f(gy)})"')
    inner += _p(f"M{_f(-w * 0.18)},{_f(-h * 0.8)} Q0,{_f(-h * 0.98)} {_f(w * 0.16)},{_f(-h * 0.84)}", sw=6,
                stroke=S.shade(WHEAT, 0.35), extra='opacity="0.8"')
    return _p(d, WHEAT, 0) + _clip(_uid("gheap", w, h, seed), d, inner) + _p(d, sw=3.8)


def _grain_sack(open_=False, seed=0):
    col = P["sackcloth"]
    out = _sack(1.0, col, seed) if not open_ else ""
    if open_:
        r = random.Random(seed)
        pts = [(-26, -78), (-46, -60), (-54, -28), (-50, -4), (0, 2), (50, -4), (54, -28), (46, -60), (26, -78)]
        out += _p(_sm(pts, closed=False) + " Z", col, 4)
        out += _p("M-34,-80 Q0,-104 34,-80 Q0,-66 -34,-80 Z", WHEAT, 3.4)
        for k in range(8):
            gx = r.uniform(-24, 24)
            out += _ell(gx, -82 - r.uniform(0, 10), 3.4, 2.2, WHEAT_DARK, 0)
        out += _p("M-30,-78 Q-40,-90 -48,-80", sw=7, stroke=INK) + _p("M-30,-78 Q-40,-90 -48,-80", sw=3.4, stroke=col)
        out += _ell(60, -4, 26, 7, WHEAT, 2.4)
    for k in (-1, 1):
        out += _p(f"M{k * 8},-56 l0,26 M{k * 8 - 8},-44 l16,0", sw=3, stroke=S.shade(col, -0.4), extra='opacity="0.5"')
    return out


def grain_sacks(x, y, scale=1.0, n=1, open_=False, facing=1):
    """Grain sacks (see module doc, section 10): n 1..6 in a little stack."""
    pos = [(0, 0, 0), (-70, 0, 1), (70, 0, 2), (-35, -66, 3), (35, -66, 4), (0, -132, 5)]
    out = ""
    for i, (dx, dy, sd) in enumerate(pos[:max(1, min(6, int(n)))]):
        out += _g(_grain_sack(open_ and i == 0, sd), f"translate({dx},{dy}) scale(0.9)")
    return _place(out, x, y, scale, facing)


def _silo(cx, h, fill, k=1.0):
    w = 150 * k
    d = (f"M{_f(cx - w / 2)},0 L{_f(cx - w / 2)},{_f(-h * 0.55)} Q{_f(cx - w / 2)},{_f(-h)} {_f(cx)},{_f(-h)} "
         f"Q{_f(cx + w / 2)},{_f(-h)} {_f(cx + w / 2)},{_f(-h * 0.55)} L{_f(cx + w / 2)},0 Z")
    out = _p(d, MUD, 4)
    out += _p(f"M{_f(cx - w * 0.3)},{_f(-h * 0.85)} Q{_f(cx)},{_f(-h * 0.97)} {_f(cx + w * 0.2)},{_f(-h * 0.9)}", sw=6,
              stroke=S.shade(MUD, 0.3), extra='opacity="0.7"')
    # a cutaway window showing the grain level inside
    wx0, wx1, wy0, wy1 = cx - w * 0.26, cx + w * 0.26, -h * 0.72, -16
    win = f"M{_f(wx0)},{_f(wy1)} L{_f(wx0)},{_f(wy0 + 20)} Q{_f(cx)},{_f(wy0 - 14)} {_f(wx1)},{_f(wy0 + 20)} L{_f(wx1)},{_f(wy1)} Z"
    lev = wy1 - (wy1 - wy0) * _clamp(fill)
    inner = _rect(wx0 - 4, wy0 - 30, wx1 - wx0 + 8, wy1 - wy0 + 40, "#5a4434", 0)
    if fill > 0:
        inner += _p(f"M{_f(wx0 - 4)},{_f(lev + 6)} Q{_f(cx)},{_f(lev - 12)} {_f(wx1 + 4)},{_f(lev + 6)} L{_f(wx1 + 4)},{_f(wy1 + 4)} "
                    f"L{_f(wx0 - 4)},{_f(wy1 + 4)} Z", WHEAT, 2.4)
        for j in range(6):
            inner += _ell(cx - w * 0.2 + j * w * 0.08, lev + 10 + (j % 2) * 8, 3, 2, WHEAT_DARK, 0)
    out += _clip(_uid("silo", cx, h, round(fill, 3)), win, inner) + _p(win, sw=3.4)
    out += _p(f"M{_f(cx - 22 * k)},{_f(-h + 6)} L{_f(cx - 18 * k)},{_f(-h - 14)} L{_f(cx + 18 * k)},{_f(-h - 14)} "
              f"L{_f(cx + 22 * k)},{_f(-h + 6)}", "#8a6a45", 3.4)
    return out


def _granary(fill=1.0):
    fill = _clamp(fill)
    out = ""
    # back wall of the yard
    out += _p("M-410,0 L-410,-150 L410,-150 L410,0 Z", S.shade(MUD, 0.12), 4)
    for xx in range(-390, 400, 52):
        out += _line(xx, -150, xx, -6, sw=1.8, color=MUD_DARK, extra='opacity="0.5"')
    # three domed silos (their windows show the level rising)
    for cx, h, k, lag in ((-250, 340, 1.0, 0.0), (0, 400, 1.12, 0.12), (250, 340, 1.0, 0.24)):
        out += _silo(cx, h, (fill - lag) / (1 - lag) if fill > lag else 0.0, k)
    # a ladder against the middle silo
    out += _line(70, -10, 108, -300, sw=7, color=P["wood_dark"]) + _line(100, -6, 138, -296, sw=7, color=P["wood_dark"])
    for k in range(1, 8):
        t = k / 8
        out += _line(70 + 38 * t, -10 - 290 * t, 100 + 38 * t, -6 - 290 * t, sw=5, color=P["wood"])
    # heaps in the yard 'like mountains': they grow with fill
    if fill > 0.05:
        out += _g(_grain_heap(260 * (0.4 + 0.6 * fill), 150 * fill, 1), "translate(-140,6)")
        out += _g(_grain_heap(320 * (0.4 + 0.6 * fill), 210 * fill, 2), "translate(110,10)")
    if fill > 0.5:
        out += _g(_grain_heap(160 * fill, 90 * (fill - 0.3), 3), "translate(-330,12)")
    for i in range(int(fill * 6 + 0.01)):
        out += _g(_grain_sack(False, i), f"translate({-360 + i * 34},{20 + (i % 2) * 8}) scale(0.55)")
    return out


def granary(x, y, scale=1.0, fill=1.0, facing=1):
    """Pharaoh's storehouses (see module doc, section 10)."""
    return _place(_granary(fill), x, y, scale, facing)


def grain_heap(x, y, scale=1.0, size=1.0, seed=0):
    """A heap of golden grain (anchor bottom centre), ~300 x 200 px at size 1."""
    return _place(_grain_heap(300 * (0.4 + 0.6 * _clamp(size, 0, 3)), 200 * _clamp(size, 0, 3), seed), x, y, scale)


# ---------------------------------------------------------------------- royal things
def _egypt_throne():
    """Gilded Egyptian throne with lion legs, a high back behind the sitter and a footstool. Anchor: the floor under
    pharaoh(pose='sit_throne', throne=False); seat top EGYPT_SEAT_Y."""
    g, gd = P["gold"], _GOLD_DARK
    out = ""
    out += _rect(64, -26, 86, 22, g, 3.4, rx=4) + _rect(70, -22, 74, 8, LAPIS_P, 0, rx=2)        # footstool
    for xx in (-70, 46):          # lion legs
        out += _p(f"M{xx - 9},{-46} L{xx - 7},-18 Q{xx - 10},-4 {xx + 12},-2 Q{xx + 18},-8 {xx + 9},-18 L{xx + 9},-64 Z", g, 3.4)
        out += _p(f"M{xx},-8 l4,0 m3,0 l4,0", sw=1.8, stroke=gd)
    back = "M-96,-50 L-96,-300 Q-96,-322 -74,-322 L-60,-322 Q-40,-322 -40,-300 L-40,-50 Z"
    out += _p(back, g, 4)
    feathers = ""
    for k in range(10):
        yy = -300 + k * 24
        feathers += _p(f"M-96,{yy} Q-68,{yy + 18} -40,{yy}", sw=7, stroke=(LAPIS_P, CARNELIAN_P, "#3b8b89")[k % 3])
    out += _clip(_uid("ethr"), back, feathers)
    out += _p(back, sw=4)
    out += _rect(-102, -58, 160, 22, g, 4, rx=6)
    for xx in range(-90, 50, 16):
        out += _rect(xx, -54, 8, 14, (LAPIS_P if (xx // 16) % 2 else CARNELIAN_P), 0, rx=2)
    out += _p("M-98,-56 Q-100,-73 -78,-73 L44,-73 Q60,-71 56,-56 Z", "#e8d6aa", 3.4)
    out += _rect(-16, -134, 12, 76, g, 3.2, rx=4) + _rect(-26, -144, 84, 18, g, 3.6, rx=8)
    out += _circ(58, -135, 12, g, 3.4) + _circ(62, -137, 2.2, INK, 0)
    return _g(out, "translate(16,0)")


def egypt_throne(x, y, scale=1.0, facing=1):
    """Pharaoh's gilded throne (see module doc, section 10)."""
    return _place(_egypt_throne(), x, y, scale, facing)


def signet_ring(x, y, scale=1.0, rot=0.0):
    """Pharaoh's signet ring (Gen 41:42): the gold ring with a carved blue stone of royal_seal(kind='ring')."""
    return _place(_signet_ring(), x, y, scale, 1, rot)


def _chain_loop(state="held"):
    out = ""
    if state == "held":           # hanging from two hands: a U of gold links with a pendant
        pts = [(-70 + 140 * i / 24, 150 * math.sin(math.pi * i / 24) ** 1.3) for i in range(25)]
        pend = (0, 172)
    else:                          # lying in a loose loop
        pts = [(80 * math.cos(2 * math.pi * i / 26) * 1.2, 30 * math.sin(2 * math.pi * i / 26)) for i in range(26)]
        pend = (0, 44)
    for i, (px, py) in enumerate(pts):
        out += _ell(px, py, 7.5, 5, P["gold"], 2.2, extra=f'transform="rotate({(i % 2) * 70} {_f(px)} {_f(py)})"')
    out += _circ(pend[0], pend[1], 18, P["gold"], 3) + _circ(pend[0], pend[1], 8, LAPIS_P, 0)
    out += _circ(pend[0] - 5, pend[1] - 5, 3, HILITE, 0)
    return out


def gold_chain(x, y, scale=1.0, state="held"):
    """Joseph's gold chain (see module doc, section 10)."""
    return _place(_chain_loop(state), x, y, scale)


# ---------------------------------------------------------------------- the prison
def _prison_window(light=1.0, wall=True):
    out = ""
    if wall:
        rng = random.Random(4)
        for r in range(6):
            for c in range(5):
                xx, yy = -230 + c * 96 + (48 if r % 2 else 0), -170 + r * 58
                out += _rect(xx, yy, 92, 54, rng.choice(("#a8998a", "#9a8c7e", "#b3a596")), 3, rx=10)
    out += _rect(-74, -64, 148, 128, "#5a4a42", 4, rx=6)
    out += _rect(-62, -52, 124, 104, "#cfe0e6", 0, rx=4)
    out += _p("M-62,20 Q-20,6 20,14 Q50,20 62,10 L62,52 L-62,52 Z", "#bfd6a0", 0, extra='opacity="0.8"')
    for xx in (-36, -12, 12, 36):
        out += _rect(xx - 5, -58, 10, 116, "#6e6a66", 3)
    out += _rect(-62, -10, 124, 9, "#6e6a66", 3)
    if light > 0:
        gid = _uid("pbeam", round(light, 2))
        out += f'<defs>{S.lin_grad(gid, [(0, P["glow"], 0.55 * light), (1, P["glow"], 0)], 0, 0, 0.4, 1)}</defs>'
        out += _p("M-60,50 L60,50 L280,520 L-60,520 Z", f"url(#{gid})", 0)
    return out


def prison_window(x, y, scale=1.0, light=1.0, wall=True, facing=1):
    """A small high barred window with a beam of light (see module doc, section 10)."""
    return _place(_prison_window(_clamp(light), wall), x, y, scale, facing)


def _prison_bars(w=300, h=400, open_=0.0):
    out = _rect(-w / 2 - 18, -h - 18, w + 36, h + 18, "#7a6a5a", 4, rx=6)
    out += _rect(-w / 2, -h, w, h, "#3e322b", 3, rx=4)
    gate = ""
    for k in range(7):
        xx = -w / 2 + 14 + k * (w - 28) / 6
        gate += _rect(xx - 6, -h + 4, 12, h - 6, "#6e6a66", 3, rx=4)
    for yy in (-h + 30, -h / 2, -40):
        gate += _rect(-w / 2 + 4, yy, w - 8, 12, "#6e6a66", 3, rx=4)
    gate += _rect(w / 2 - 40, -h / 2 - 22, 26, 34, "#8e8a86", 3, rx=4)
    k = 1 - 0.85 * _clamp(open_)
    out += _g(gate, f"translate({_f(-w / 2)},0) scale({k:.3f},1) translate({_f(w / 2)},0)")
    return out


def prison_bars(x, y, scale=1.0, width=300, height=400, open_=0.0, facing=1):
    """A barred prison door in a stone frame (anchor bottom centre); open_ 0..1 swings it open (hinge left)."""
    return _place(_prison_bars(width, height, open_), x, y, scale, facing)


# ---------------------------------------------------------------------- animals: camel, donkey, cows
def _gait(phase, off, A, lift, duty=0.6):
    """Foot x offset and lift for one leg of a walk cycle (stance moves the foot back, swing lifts it forward)."""
    u = (phase + off) % 1.0
    if u < duty:
        t = u / duty
        return A * (1 - 2 * t), 0.0
    t = (u - duty) / (1 - duty)
    return -A + 2 * A * _smooth(t), lift * math.sin(math.pi * t)


def _camel(pose="stand", phase=0.0, load=True, bridle=True, eyes="open"):
    coat, dark = "#d9ad72", "#b48650"
    light = S.shade(coat, 0.3)
    walk = pose == "walk"
    bob = -4 * math.sin(4 * math.pi * phase) if walk else 0.0
    out = ""
    # pace: both legs of one side move together (far side half a cycle later)
    legs = [((-62, -190), -66, True, True, 0.5), ((72, -190), 80, False, True, 0.5),
            ((-80, -188), -84, True, False, 0.0), ((56, -188), 60, False, False, 0.0)]
    for (hip, fx, hind, far, off) in legs:
        dx, lf = _gait(phase, off, 34, 26) if walk else (0.0, 0.0)
        hip_ = (hip[0], hip[1] + bob)
        out += _qleg(hip_, fx + dx, 40 if hind else 37, 15, coat, hind=hind, far=far, hoof="pad", knob=1.3,
                     bend=0.5 if hind else 0.35, ground=-lf)
    body = ""
    sw_ = 6 * math.sin(2 * math.pi * phase) if walk else 0
    body += _p(f"M-118,-222 Q{-136 + sw_},-190 {-130 + sw_},-160", sw=7, stroke=INK) + \
        _p(f"M-118,-222 Q{-136 + sw_},-190 {-130 + sw_},-160", sw=3, stroke=coat)
    body += _ell(-130 + sw_, -156, 6, 11, dark, 3)
    hb = 3 * math.sin(2 * math.pi * phase + 1) if walk else 0
    neck = [(92, -222), (138, -210), (172, -226 + hb), (192, -262 + hb), (202, -306 + hb)]
    body += _band(neck, 50, 34, coat)
    body += _p(_sm([(122, -214), (156, -214), (182, -238 + hb)], closed=False), sw=3, stroke=dark, extra='opacity="0.35"')
    bd = _CAMEL_BACK + [(118, -230), (128, -202), (116, -174), (70, -158), (0, -154), (-70, -158), (-110, -170),
                        (-128, -184)]
    belly = _p(_sm([(-120, -184), (0, -178), (124, -186), (124, -140), (-120, -140)]), light, 0)
    shine = _p("M-30,-286 Q-10,-306 16,-306", sw=7, stroke=light, extra='opacity="0.75"')
    shine += _p("M-56,-246 Q0,-232 56,-246", sw=3, stroke=dark, extra='opacity="0.3"')
    body += _body(bd, coat, shine, belly, "camelj")
    if load:
        body += _camel_load()
    head = ""
    head += _ell(196, -342, 9, 13, coat, 3.2, extra='transform="rotate(-30 196 -342)"')
    head += _ell(197, -341, 4, 7, "#d7a98a", 0, extra='transform="rotate(-30 197 -341)"')
    hd = [(198, -334), (214, -352), (240, -354), (262, -342), (276, -324), (278, -306), (266, -296), (240, -298),
          (214, -304), (200, -316)]
    head += _p(_sm(hd), coat, 4)
    head += _p("M262,-300 Q272,-290 282,-302", S.shade(coat, -0.06), 3)
    head += _p("M266,-322 Q270,-326 274,-322", sw=2.6)
    head += _dot_eye(232, -332, 4.6, eyes if eyes in ("open", "closed", "happy") else "open")
    head += _p("M226,-338 l-4,-6 M231,-340 l-1,-7 M236,-339 l2,-6", sw=2)
    head += _blush(240, -316, 7, 4)
    head += _p("M258,-306 Q264,-302 270,-306", sw=2.4)
    if bridle:                    # a red halter with tassels and a lead rope hanging forward
        head += _p("M214,-350 Q206,-322 214,-300 M214,-304 Q244,-292 270,-300", sw=8, stroke=INK)
        head += _p("M214,-350 Q206,-322 214,-300 M214,-304 Q244,-292 270,-300", sw=4.4, stroke=CARNELIAN_P)
        for xx in (230, 250):
            head += _p(f"M{xx},-296 l-2,14 l6,0 Z", P["gold"], 1.8)
        head += _tube(f"M268,-298 Q{CAMEL_LEAD[0] - 10},{(CAMEL_LEAD[1] - 298) / 2 + 30} {CAMEL_LEAD[0]},{CAMEL_LEAD[1]}",
                      4.5, P["wood_light"], 2.2)
    body += _g(head, f"translate(0,{_f(hb)})") if hb else head
    out += _g(body, f"translate(0,{_f(bob)})") if bob else body
    return out


def _camel_load():
    """Saddle blanket over the hump, rolled rugs and bulging bundles on both flanks, a spice bag."""
    out = ""
    out += _p("M-96,-236 Q-60,-260 -40,-286 Q0,-322 40,-286 Q60,-260 96,-240 L92,-190 Q0,-170 -92,-190 Z",
              CARNELIAN_P, 4)
    for k, col in enumerate((P["gold"], LAPIS_P, P["gold"])):
        y0 = -204 + k * 8
        out += _p(f"M-92,{y0} Q0,{y0 + 18} 92,{y0 - 2}", sw=4, stroke=col)
    for xx in range(-84, 96, 18):
        out += _line(xx, -186 + abs(xx) * 0.02, xx, -174, sw=2.6, color=P["gold"])
    out += _g(_sack(1.0, P["sackcloth"], 4), "translate(-72,-180) rotate(8) scale(0.72)")     # bundles on the flanks
    out += _p("M-96,-226 Q-72,-214 -48,-226", sw=4, stroke=CORD)
    out += _g(_sack(1.0, "#b98552", 6), "translate(70,-176) rotate(-6) scale(0.7)")         # spice bag
    for xx in (52, 70, 88):
        out += _p(f"M{xx},-182 l-2,14 l7,0 Z", P["gold"], 1.8)
    out += _rect(-34, -330, 70, 30, "#5f8a85", 3.6, rx=14)                    # a rolled rug on the hump
    for xx in (-20, 0, 20):
        out += _line(xx, -330, xx, -300, sw=3, color="#e8d6aa")
    out += _ell(-34, -315, 9, 15, S.shade("#5f8a85", -0.2), 3)
    out += _p("M-44,-300 Q0,-280 46,-300", sw=4, stroke=CORD)
    return out


def camel(x, y, scale=1.0, facing=1, pose="stand", phase=0.0, load=True, bridle=True, eyes="open"):
    """A caravan camel (see module doc, section 10)."""
    if pose in ("walk_a", "walk_b"):
        pose, phase = "walk", (0.0 if pose == "walk_a" else 0.5)
    if pose not in ("stand", "walk"):
        raise ValueError(f"camel: pose must be stand / walk / walk_a / walk_b, not {pose!r}")
    return _place(_camel(pose, phase % 1.0, load, bridle, eyes), x, y, scale, facing)


def _donkey(pose="stand", phase=0.0, sacks=2):
    coat, light, dark = "#aaa39b", "#e2d9cb", "#5e554e"
    walk = pose == "walk"
    bob = -3 * math.sin(4 * math.pi * phase) if walk else 0.0
    out = ""
    # walk: diagonal pairs (far hind + near front, then the others)
    for (hip, fx, hind, far, off) in (((-58, -118), -62, True, True, 0.5), ((64, -118), 74, False, True, 0.0),
                                      ((-74, -116), -78, True, False, 0.0), ((50, -116), 54, False, False, 0.5)):
        dx, lf = _gait(phase, off, 26, 18) if walk else (0.0, 0.0)
        out += _qleg((hip[0], hip[1] + bob), fx + dx, 30 if hind else 28, 13 if far else 14, coat, hind=hind, far=far,
                     bend=0.6 if hind else 0.4, ground=-lf)
    b = ""
    b += _p("M-96,-166 Q-110,-126 -106,-96", sw=7, stroke=INK) + _p("M-96,-166 Q-110,-126 -106,-96", sw=3, stroke=coat)
    b += _p("M-106,-106 Q-118,-86 -106,-76 Q-94,-86 -106,-106 Z", dark, 3)
    bd = [(-102, -146), (-88, -178), (-40, -188), (10, -182), (60, -190), (92, -172), (102, -142), (88, -112),
          (40, -98), (-20, -96), (-76, -106)]
    belly = _p(_sm([(-90, -118), (0, -118), (95, -122), (95, -80), (-90, -80)]), light, 0)
    b += _body(bd, coat, "", belly, "donkj")
    if sacks:
        b += _p("M-60,-196 Q0,-212 60,-198 L56,-172 Q0,-160 -56,-172 Z", CARNELIAN_P, 3.6)     # saddle cloth
        b += _p("M-56,-180 Q0,-168 56,-182", sw=3, stroke=P["gold"])
        b += _g(_grain_sack(False, 1), "translate(-34,-104) rotate(6) scale(0.82)")
        if sacks > 1:
            b += _g(_grain_sack(False, 2), "translate(30,-100) rotate(-6) scale(0.82)")
        b += _tube("M-56,-190 Q-30,-176 -34,-176 M56,-190 Q30,-174 30,-174", 4, CORD, 2)
    b += _p("M58,-180 Q80,-220 102,-240 L134,-214 Q106,-182 96,-132 Z", coat, 4)
    b += _p("M66,-186 Q86,-224 106,-246", sw=12, stroke=INK) + _p("M66,-186 Q86,-224 106,-246", sw=6, stroke=dark)
    nod = 4 * math.sin(2 * math.pi * phase) if walk else 0
    h = ""
    for ex, rot in ((110, -16), (126, 12)):
        h += _ell(ex, -268, 10, 34, coat, 3.6, extra=f'transform="rotate({rot} {ex} -240)"')
        h += _ell(ex, -278, 4.5, 18, "#d7b2a8", 0, extra=f'transform="rotate({rot} {ex} -240)"')
        h += _p(f"M{ex - 9},-292 Q{ex},-308 {ex + 9},-292 Z", dark, 2.5, extra=f'transform="rotate({rot} {ex} -240)"')
    h += _ell(128, -214, 26, 30, coat, 4)
    h += _ell(142, -186, 26, 19, light, 3.8, extra='transform="rotate(20 142 -186)"')
    h += _circ(148, -186, 2.6, INK, 0) + _circ(158, -182, 2.6, INK, 0)
    h += _dot_eye(136, -220, 4.4) + _blush(142, -204, 6, 3.5)
    h += _p("M144,-174 Q150,-170 156,-174", sw=2.5)
    b += _g(h, f"translate(0,{_f(nod)})") if nod else h
    out += _g(b, f"translate(0,{_f(bob)})") if bob else b
    return out


def donkey(x, y, scale=1.0, facing=1, pose="stand", phase=0.0, sacks=2):
    """A pack donkey (see module doc, section 10)."""
    if pose in ("walk_a", "walk_b"):
        pose, phase = "walk", (0.0 if pose == "walk_a" else 0.5)
    if pose not in ("stand", "walk"):
        raise ValueError(f"donkey: pose must be stand / walk / walk_a / walk_b, not {pose!r}")
    return _place(_donkey(pose, phase % 1.0, int(sacks)), x, y, scale, facing)


def _cow(kind="fat", pose="stand", phase=0.0, mouth=0.0):
    fat = kind == "fat"
    coat = "#f3ead8" if fat else "#e2d4ba"
    patch = "#9b6542" if fat else "#8a6a52"
    muzzle = "#f0b2b0"
    walk = pose == "walk"
    out = ""
    k = 1.0 if fat else 0.86
    hy = -100 if fat else -128                     # hip height: the thin cows stand on long bony legs
    bob = -3 * math.sin(4 * math.pi * phase) if walk else 0.0
    for (hx, fx, hind, far, off) in ((-70, -74, True, True, 0.5), (74, 84, False, True, 0.0), (-90, -94, True, False, 0.0),
                                     (56, 62, False, False, 0.5)):
        dx, lf = _gait(phase, off, 26, 18) if walk else (0.0, 0.0)
        w0, w1 = (38, 21) if fat else (22, 13)
        out += _qleg((hx * k, hy + bob + (0 if hind or fat else -2)), fx * k + dx, w0, w1, coat, hind=hind, far=far,
                     hoof="cloven", bend=0.5 if hind else 0.3, ground=-lf, knob=0.0 if fat else 0.9)
    b = ""
    b += _p(f"M{-118 * k},{hy - 52} Q{-136 * k},{hy - 12} {-130 * k},{hy + 22}", sw=7, stroke=INK)
    b += _p(f"M{-118 * k},{hy - 52} Q{-136 * k},{hy - 12} {-130 * k},{hy + 22}", sw=3, stroke=coat)
    b += _p(f"M{-130 * k},{hy + 14} Q{-142 * k},{hy + 32} {-130 * k},{hy + 40} Q{-118 * k},{hy + 32} {-130 * k},{hy + 14} Z", patch, 3)
    if fat:
        bd = [(-128, -124), (-118, -172), (-70, -196), (-10, -194), (50, -198), (104, -184), (132, -148),
              (124, -100), (84, -72), (20, -60), (-50, -64), (-104, -84)]
        pt = _ell(-62, -150, 44, 30, patch, 0) + _ell(46, -118, 34, 28, patch, 0) + _ell(-104, -104, 18, 16, patch, 0)
        belly = _p(_sm([(-110, -94), (0, -96), (110, -96), (110, -40), (-110, -40)]), S.shade(coat, 0.3), 0)
        pt += _p("M-40,-178 Q0,-192 40,-180", sw=8, stroke=HILITE, extra='opacity="0.5"')
        b += _body(bd, coat, pt, belly, "cowfat")
        b += _ell(-22, -64, 15, 8, muzzle, 3)
    else:
        bd = [(-108, -150), (-100, -186), (-60, -196), (-10, -188), (40, -196), (84, -190), (104, -160), (96, -136),
              (60, -128), (0, -124), (-60, -128), (-96, -134)]
        pt = _ell(-50, -170, 26, 16, patch, 0) + _ell(40, -160, 20, 14, patch, 0)
        for j in range(4):        # ribs and bony hips (thin, not sad-scary: a comic 'hungry' cow)
            xx = -24 + j * 16
            pt += _p(f"M{xx},-180 Q{xx + 6},-160 {xx},-140", sw=2.6, stroke=S.shade(coat, -0.3), extra='opacity="0.7"')
        pt += _ell(-80, -186, 12, 8, S.shade(coat, 0.2), 0)
        b += _body(bd, coat, pt, "", "cowthin")
    hx, hyy = (140, -150) if fat else (124, -176)
    if pose == "graze":
        hx, hyy = hx + 10, hyy + 90
    head = ""
    head += _tube(f"M{hx - 22},{hyy - 40} Q{hx - 36},{hyy - 56} {hx - 30},{hyy - 68}", 8, "#efe2c0", 3)
    head += _tube(f"M{hx + 20},{hyy - 42} Q{hx + 34},{hyy - 56} {hx + 28},{hyy - 68}", 8, "#efe2c0", 3)
    head += _ell(hx - 36, hyy - 24, 19, 9, coat, 3.4, extra=f'transform="rotate(-20 {hx - 36} {hyy - 24})"')
    head += _ell(hx + 34, hyy - 26, 19, 9, coat, 3.4, extra=f'transform="rotate(20 {hx + 34} {hyy - 26})"')
    hw = 1.0 if fat else 0.86
    head += _p(_sm([(hx - 26 * hw, hyy - 38), (hx + 20 * hw, hyy - 40), (hx + 30 * hw, hyy - 4), (hx + 20 * hw, hyy + 24),
                    (hx - 20 * hw, hyy + 24), (hx - 32 * hw, hyy - 4)]), coat, 4)
    head += _ell(hx, hyy - 28, 15, 10, patch, 0, extra='opacity="0.9"')
    mo = _clamp(mouth)
    head += _ell(hx, hyy + 28, 30 * hw, 19, muzzle, 3.8)
    if mo > 0:
        head += _ell(hx, hyy + 38, 14 * hw, 4 + 9 * mo, P["mouth_inside"], 2.6)
        head += _ell(hx, hyy + 42 + 4 * mo, 7, 3 + 2 * mo, "#e8857c", 0)
    head += _ell(hx - 10, hyy + 26, 3.4, 4, S.shade(muzzle, -0.5), 0) + _ell(hx + 10, hyy + 26, 3.4, 4, S.shade(muzzle, -0.5), 0)
    if fat:
        head += _dot_eye(hx - 13, hyy - 8, 4.6, "happy") + _dot_eye(hx + 13, hyy - 8, 4.6, "happy")
    else:                         # big round hungry eyes
        head += _ell(hx - 12, hyy - 8, 8, 9, "#fbf6ea", 2.4) + _ell(hx + 12, hyy - 8, 8, 9, "#fbf6ea", 2.4)
        head += _dot_eye(hx - 10, hyy - 6, 4.2) + _dot_eye(hx + 14, hyy - 6, 4.2)
    head += _blush(hx - 22, hyy + 8, 6, 3.5) + _blush(hx + 22, hyy + 8, 6, 3.5)
    b += head
    out += _g(b, f"translate(0,{_f(bob)})") if bob else b
    return out


def cow(x, y, scale=1.0, facing=1, kind="fat", pose="stand", phase=0.0, mouth=0.0):
    """Pharaoh's dream cows (see module doc, section 10)."""
    if kind not in ("fat", "thin"):
        raise ValueError(f"cow: kind must be 'fat' or 'thin', not {kind!r}")
    if pose in ("walk_a", "walk_b"):
        pose, phase = "walk", (0.0 if pose == "walk_a" else 0.5)
    if pose not in ("stand", "walk", "graze"):
        raise ValueError(f"cow: pose must be stand / walk / walk_a / walk_b / graze, not {pose!r}")
    return _place(_cow(kind, pose, phase % 1.0, mouth), x, y, scale, facing)


# ---------------------------------------------------------------------- chariot
_CH_R = 80                        # wheel radius; the axle is at y=-_CH_R, the car floor at CHARIOT_STAND[1]


def _wheel(cx, cy, r, phase=0.0, col=None):
    col = col or P["gold"]
    out = _circ(cx, cy, r, "none", 15, stroke=INK) + _circ(cx, cy, r, "none", 8, stroke=S.shade(P["wood"], 0.05))
    for k in range(6):
        a = 2 * math.pi * (k / 6 + phase / 6)
        out += _tube(f"M{_f(cx)},{_f(cy)} L{_f(cx + (r - 4) * math.cos(a))},{_f(cy + (r - 4) * math.sin(a))}", 6, P["wood_light"], 2.4)
    out += _circ(cx, cy, r * 0.2, col, 3.2)
    out += _circ(cx, cy, r, "none", 2.0, stroke=S.shade(P["wood"], 0.4), extra='opacity="0.6"')
    return out


_CAR = "M-66,-96 L82,-96 Q92,-180 90,-252 Q78,-272 58,-262 Q0,-226 -56,-214 Q-68,-210 -66,-196 Z"


def _chariot(part="all", wheel=0.0, horse=True, phase=0.0):
    r = _CH_R
    out = ""
    if part in ("all", "back"):
        hx, hk = 380, 0.94
        if horse:
            pose = "walk_a" if (phase % 1.0) < 0.5 else "walk_b"
            out += _g(_equine("horse", pose), f"translate({hx},0) scale({hk})")
            out += _p("M352,-250 Q392,-266 444,-244 L436,-218 Q392,-234 356,-226 Z", LAPIS_P, 3.4)     # saddle pad
            for xx in (366, 386, 406, 426):
                out += _p(f"M{xx},-226 l-2,14 l7,0 Z", P["gold"], 1.8)
            ex, ey = hx + 138 * hk, -374 * hk                          # the ears: a red plume between them
            out += _p(f"M{_f(ex - 6)},{_f(ey + 18)} Q{_f(ex - 14)},{_f(ey - 30)} {_f(ex + 4)},{_f(ey - 50)} "
                      f"Q{_f(ex + 6)},{_f(ey - 20)} {_f(ex + 4)},{_f(ey + 18)} Z", CARNELIAN_P, 3)
            mx, my = hx + 190 * hk, -282 * hk                          # bridle and reins to the front rail
            out += _p(f"M{_f(hx + 132 * hk)},{_f(-346 * hk)} L{_f(mx)},{_f(my)}", sw=7, stroke=INK)
            out += _p(f"M{_f(hx + 132 * hk)},{_f(-346 * hk)} L{_f(mx)},{_f(my)}", sw=3.5, stroke=CARNELIAN_P)
            out += _p(f"M{_f(mx)},{_f(my)} Q{_f(hx + 60)},{_f(-300)} 86,-236", sw=2.8, stroke=S.shade(LEATHER, -0.1))
        out += _wheel(-14, -r - 4, r - 6, wheel, _GOLD_DARK)                                       # far wheel
        out += _tube(f"M60,-120 Q220,-150 {hx + 20},-236", 10, P["wood"], 3)                           # pole
        out += _p("M-62,-96 L66,-96 L74,-238 Q66,-252 50,-246 Q0,-212 -52,-202 Z", S.shade(P["gold"], -0.18), 4)
        out += _rect(-70, -166, 64, 18, P["wood_light"], 3.4, rx=6) + _rect(-62, -150, 12, 54, P["wood"], 3)  # seat
    if part in ("all", "front"):
        out += _p(_CAR, P["gold"], 0)
        deco = ""
        for k in range(7):
            yy = -104 - k * 24
            deco += _p(f"M-80,{yy + 20} L100,{yy - 34}", sw=8, stroke=(LAPIS_P, CARNELIAN_P, "#3b8b89")[k % 3], extra='opacity="0.85"')
        deco += _p("M-66,-214 Q0,-228 58,-264", sw=10, stroke=S.shade(P["gold"], 0.25))
        out += _clip(_uid("char2"), _CAR, deco)
        out += _p(_CAR, sw=4)
        out += _rect(-74, -104, 166, 16, P["wood"], 3.4, rx=5)
        out += _wheel(6, -r, r, wheel)
    return out


def chariot(x, y, scale=1.0, facing=1, part="all", wheel=0.0, horse=True, phase=0.0):
    """Joseph's chariot with its horse (see module doc, section 10)."""
    if part not in ("all", "back", "front"):
        raise ValueError(f"chariot: part must be all / back / front, not {part!r}")
    return _place(_chariot(part, wheel % 1.0, horse, phase), x, y, scale, facing)


# ---------------------------------------------------------------------- dreams: vine, baskets, bubble
def _grapevine(grow=1.0):
    g = _clamp(grow)
    out = _tube("M0,0 Q-10,-60 6,-120 Q18,-160 0,-190", 12, "#8a5a3a", 3.4)
    br = [("M4,-120 Q60,-150 100,-200", (100, -200)), ("M2,-150 Q-60,-180 -96,-226", (-96, -226)),
          ("M0,-188 Q10,-240 30,-280", (30, -280))]
    for i, (d, tip) in enumerate(br):
        t = _clamp(g / 0.4 - i * 0.25)
        if t <= 0:
            continue
        x0, y0 = (float(v) for v in d[1:].split(" ")[0].split(","))
        out += _tube(d, 7, "#8a5a3a", 3) if t >= 1 else _g(_tube(d, 7, "#8a5a3a", 3),
                                                           f"translate({_f(x0)},{_f(y0)}) scale({t:.3f}) translate({_f(-x0)},{_f(-y0)})")
        if t < 1:
            continue
        if g > 0.3:               # leaves
            lk = _clamp((g - 0.3) / 0.2)
            for j, (lx, ly) in enumerate(((tip[0] * 0.5, tip[1] * 0.75), (tip[0] * 0.85, tip[1] * 0.9))):
                out += _g(_leaf(lx, ly, 26 * lk, j + i), "")
        if 0.5 < g <= 0.75:      # blossoms
            for j in range(4):
                out += _circ(tip[0] + (j - 1.5) * 8, tip[1] + 16 + (j % 2) * 8, 5, "#f4ead0", 2)
        if g > 0.7:               # grapes: green, then ripe purple
            ripe = _clamp((g - 0.75) / 0.25)
            col = S.mix("#a8c870", "#7a4a9a", ripe)
            cx, cy = tip[0], tip[1] + 30
            for row in range(4):
                for j in range(4 - row):
                    gx, gy = cx + (j - (3 - row) / 2) * 15, cy + row * 13
                    out += _circ(gx, gy, 8, col, 2.4) + _circ(gx - 3, gy - 3, 2.2, HILITE, 0, extra='opacity="0.8"')
    return out


def _leaf(x, y, r, seed=0):
    if r <= 0:
        return ""
    d = (f"M{_f(x)},{_f(y + r)} Q{_f(x - r * 1.1)},{_f(y + r * 0.2)} {_f(x - r * 0.6)},{_f(y - r * 0.7)} "
         f"Q{_f(x)},{_f(y - r * 0.4)} {_f(x + r * 0.6)},{_f(y - r * 0.7)} Q{_f(x + r * 1.1)},{_f(y + r * 0.2)} {_f(x)},{_f(y + r)} Z")
    return _p(d, P["leaf"] if seed % 2 else S.shade(P["leaf"], 0.12), 2.6) + _line(x, y + r, x, y - r * 0.4, sw=1.6,
                                                                                   color=P["leaf_dark"])


def grapevine(x, y, scale=1.0, grow=1.0, facing=1):
    """The cupbearer's dream vine (see module doc, section 10)."""
    return _place(_grapevine(grow), x, y, scale, facing)


def _bread_stack(n=3, birds=0):
    out = ""
    for k in range(max(1, min(3, int(n)))):
        y0 = -k * 40
        body = f"M-70,{y0 - 38} L70,{y0 - 38} Q66,{y0 - 6} 56,{y0} L-56,{y0} Q-66,{y0 - 6} -70,{y0 - 38} Z"
        weave = "".join(f"M{xx},{y0 - 36} L{xx * 0.85:.1f},{y0} " for xx in range(-60, 70, 14))
        out += _p(body, WICKER, 0) + _clip(_uid("bst", k), body, _p(weave, sw=2, stroke=S.shade(WICKER, -0.3)))
        out += _p(body, sw=3.6) + _tube(f"M-72,{y0 - 38} L72,{y0 - 38}", 7, S.shade(WICKER, 0.12), 3)
    top = -max(1, min(3, int(n))) * 40 + 40 - 38
    for dx, w in ((-34, 34), (4, 40), (40, 30)):
        out += _ell(dx, top - 12, w, 16, "#e2b36a", 3)
        out += _p(f"M{dx - w * 0.5},{top - 16} l8,-6 M{dx},{top - 18} l8,-6", sw=2.2, stroke="#a8743c")
    out += _circ(-8, top - 30, 15, "#d99a4e", 3) + _p(f"M-18,{top - 34} q10,-8 20,0", sw=2, stroke="#a8743c")
    for j in range(max(0, int(birds))):
        bx = (-46, 40, -4)[j % 3]
        out += _g(_songbird(0.0, "perch", ("brown", "blue", "yellow")[j % 3]), f"translate({bx},{top - 54}) scale(0.62)")
    return out


def bread_baskets(x, y, scale=1.0, n=3, birds=0):
    """The baker's dream: n stacked flat baskets of bread (see module doc, section 10)."""
    return _place(_bread_stack(n, birds), x, y, scale)


def dream_bubble(x, y, w=600, h=380, tail=None, inner="", pop=1.0, fill="#fbf6ea", glow=True, seed=0):
    """A soft cloud-shaped dream frame (absolute stage coordinates, see module doc, section 10)."""
    k = _smooth(_clamp(pop))
    if k <= 0:
        return ""
    rng = random.Random(seed)
    circles = []
    nb = 12
    for i in range(nb):
        a = 2 * math.pi * i / nb
        rr = min(w, h) * rng.uniform(0.17, 0.22)
        circles.append((x + (w / 2 - rr * 0.55) * math.cos(a), y + (h / 2 - rr * 0.55) * math.sin(a), rr))
    core = _ell(x, y, w / 2 - min(w, h) * 0.1, h / 2 - min(w, h) * 0.1, fill, 0)
    shape = "".join(_circ(cx, cy, r, fill, 0) for cx, cy, r in circles) + core
    outline = "".join(_circ(cx, cy, r, fill, 9) for cx, cy, r in circles)
    gl = ""
    if glow:
        gid = _uid("dbg", x, y, w, h)
        gl = (f'<defs>{S.rad_grad(gid, [(0, P["glow"], 0.8), (0.7, P["gold"], 0.25), (1, P["gold"], 0)])}</defs>'
              + _ell(x, y, w * 0.68, h * 0.72, f"url(#{gid})", 0))
    tl = ""
    if tail:
        tx, ty = tail
        for j, t in enumerate((0.25, 0.55, 0.8)):
            px, py = _lerp(x, tx, 0.55 + t * 0.45), _lerp(y + h * 0.3 * (1 if ty > y else -1), ty, t)
            tl += _circ(px, py, 22 - j * 6, fill, 3.4)
    cid = _uid("dbc", x, y, w, h, seed)
    clipd = "".join(f"M{_f(cx - r)},{_f(cy)} a{_f(r)},{_f(r)} 0 1 0 {_f(2 * r)},0 a{_f(r)},{_f(r)} 0 1 0 {_f(-2 * r)},0 Z "
                    for cx, cy, r in circles)
    clipd += (f"M{_f(x - w / 2 + min(w, h) * 0.1)},{_f(y)} a{_f(w / 2 - min(w, h) * 0.1)},{_f(h / 2 - min(w, h) * 0.1)} 0 1 0 "
              f"{_f(w - min(w, h) * 0.2)},0 a{_f(w / 2 - min(w, h) * 0.1)},{_f(h / 2 - min(w, h) * 0.1)} 0 1 0 "
              f"{_f(-(w - min(w, h) * 0.2))},0 Z")
    body = gl + tl + outline + shape + _clip(cid, clipd, inner)
    if k < 1:
        body = f'<g transform="translate({_f(x)},{_f(y)}) scale({k:.3f}) translate({_f(-x)},{_f(-y)})">{body}</g>'
    return f'<g filter="url(#wobble-fine)">{body}</g>'


# ---------------------------------------------------------------------- the children's toy
def _toy(kind="horse", rot=0.0):
    if kind == "ball":
        out = _circ(0, -34, 34, "#f2c84b", 4)
        out += _clip(_uid("ball"), "M-34,-34 A34,34 0 1 0 34,-34 A34,34 0 1 0 -34,-34 Z",
                     _p("M-12,-68 Q14,-34 -12,0 L-40,0 L-40,-68 Z", "#d9534a", 0) +
                     _p("M14,-68 Q40,-34 14,0 L40,0 L40,-68 Z", "#4f86c6", 0))
        out += _circ(0, -34, 34, "none", 4) + _ell(-12, -50, 9, 5, HILITE, 0, extra='opacity="0.8" transform="rotate(-30 -12 -50)"')
        return _g(out, f"rotate({rot:.1f} 0 -34)") if rot else out
    if kind != "horse":
        raise ValueError(f"toy: kind must be 'horse' or 'ball', not {kind!r}")
    wood, red = "#e2a85e", "#d9534a"
    out = _rect(-52, -30, 104, 12, P["wood"], 3.4, rx=5)
    for xx in (-36, 36):
        out += _circ(xx, -10, 12, red, 3.4) + _circ(xx, -10, 3, P["gold"], 0)
    for xx in (-30, 26):
        out += _rect(xx - 6, -64, 12, 38, wood, 3.2, rx=4)
    out += _p("M-44,-62 Q-46,-96 0,-96 Q36,-96 40,-70 Q20,-56 -40,-56 Z", wood, 3.6)
    out += _p("M24,-86 Q30,-128 48,-136 Q66,-138 70,-122 Q72,-108 58,-104 Q48,-100 42,-80 Z", wood, 3.6)
    out += _p("M24,-90 Q20,-122 40,-140", sw=8, stroke=INK) + _p("M24,-90 Q20,-122 40,-140", sw=4, stroke=red)
    out += _p("M-44,-84 Q-62,-80 -64,-58", sw=7, stroke=INK) + _p("M-44,-84 Q-62,-80 -64,-58", sw=3.4, stroke=red)
    out += _circ(54, -122, 3, INK, 0) + _ell(48, -134, 5, 8, wood, 2.6, extra='transform="rotate(-20 48 -134)"')
    out += _p("M-10,-80 Q4,-88 18,-80", sw=5, stroke="#4f86c6")
    return _g(out, f"rotate({rot:.1f} 0 0)") if rot else out


def toy(x, y, scale=1.0, facing=1, kind="horse", rot=0.0):
    """The children's toy: a little wooden horse on wheels or a striped ball (see module doc, section 10)."""
    return _place(_toy(kind, rot), x, y, scale, facing)


# ---------------------------------------------------------------------- fields (good years / famine)
def _field(x0, x1, y, depth=120.0, ripe=1.0, dry=0.0, seed=0, s=1.0):
    rng = random.Random(seed)
    soil = S.mix("#b9935f", "#c9a77a", dry)
    out = _p(f"M{_f(x0)},{_f(y - depth * 0.15)} L{_f(x1)},{_f(y - depth * 0.15)} L{_f(x1)},{_f(y + depth)} "
             f"L{_f(x0)},{_f(y + depth)} Z", soil, 3 * s)
    if dry > 0:                   # cracked dry earth
        for _ in range(int((x1 - x0) / (60 * s))):
            cx, cy = rng.uniform(x0, x1), y + rng.uniform(0.1, 0.9) * depth
            pts = [(cx, cy)]
            for j in range(3):
                pts.append((pts[-1][0] + rng.uniform(-30, 30) * s, pts[-1][1] + rng.uniform(-10, 14) * s))
            out += _p(_sm(pts, closed=False), sw=2.4 * s, stroke=S.shade(soil, -0.35), extra=f'opacity="{0.8 * dry:.2f}"')
    col = S.mix(S.mix("#9fbf5a", WHEAT, ripe), "#c9b07a", dry)
    rows = 4
    for r in range(rows):
        yy = y + depth * r / rows
        k = (0.6 + 0.4 * r / rows) * s
        hgt = (90 * (1 - 0.7 * dry)) * k
        for i in range(int((x1 - x0) / (16 * k)) + 1):
            xx = x0 + i * 16 * k + rng.uniform(-5, 5) * k
            tip = (xx + rng.uniform(-6, 6) * k + 10 * dry * k, yy - hgt * rng.uniform(0.8, 1.1))
            out += _line(xx, yy, tip[0], tip[1] + (hgt * 0.3 * dry), sw=2.4 * k, color=S.shade(col, -0.25))
            if dry < 0.6:
                out += _ell(tip[0], tip[1], 4 * k, 10 * k, col, 1.8 * k)
    return out


def field(x0, x1, y, depth=120.0, scale=1.0, ripe=1.0, dry=0.0, seed=0):
    """A wheat field band in absolute stage coordinates (see module doc, section 10)."""
    return _place(_field(x0, x1, y, depth * scale, _clamp(ripe), _clamp(dry), seed, scale), 0, 0, 1.0)
