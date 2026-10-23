"""People library: Jonah, sailors, the ship's captain, the king of Nineveh and townspeople; for the Daniel film
(stories/daniel) also Daniel, King Darius (king(attire='darius')), the jealous officials and the palace guards; for
the David film (stories/david) David, Goliath, his shield-bearer, Israelite / Philistine soldiers, King Saul
(king(attire='saul')), Eliab and Jesse (section DAVID FILM); for the Noah film (stories/noah) Noah, his wife, Shem,
Ham, Japheth, their wives, noah_family() and a modern child in a raincoat (section NOAH FILM); for the Joseph film
(stories/joseph) Joseph (shepherd with the coat of many colours / slave / prisoner / ruler), Jacob, the brothers and
Benjamin, brothers_group(), Pharaoh, Egyptians, the Ishmaelite traders, hug_pair() and the modern siblings
(child(sibling=...)) (section JOSEPH FILM); for the Storm film (stories/storm) Jesus, the twelve disciples,
disciples_group(), the Galilean villagers, villager_crowd() and the girl in pyjamas (child(outfit='pyjamas')) (section
STORM FILM); for the Nativity film (stories/nativity) Mary, Joseph the carpenter, baby_jesus(), toddler_jesus(), the
angels and angel_choir(), the shepherds, the wise men, the Bethlehem townsfolk and townsfolk_crowd(), and the boy in
a Christmas jumper (child(outfit='jumper')) (section NATIVITY FILM at the end).

Every public drawing function returns SVG markup - one ``<g>`` element, NO ``<svg>`` wrapper - to be
placed inside ``art.style.svg_doc(...)`` (it uses that document's ``#wobble-fine`` filter; ``ground_shadow``
uses ``#soft``). Markup is self-contained (inline clip paths with content-derived ids), so the same figure
can appear several times in one document. Preview everything with ``python3 tools/character_sheet.py``
(sheets in build/preview/characters_*.png, including ``characters_compositions.png``: figures used together).

COMMON CONVENTIONS (all people functions)
-----------------------------------------
fn(x, y, scale=1.0, facing=1, pose=..., expr=None, ..., marks=True)

* (x, y)  anchor in stage px = the GROUND CONTACT POINT. Put it on your ground line.
          - standing / walking / running: on the ground under the pelvis (between the feet); the anchor stays
            under the pelvis in walk_a/walk_b and run_a/run_b, so flipping frames while moving x never slides;
          - sitting on the ground (sit*, wake, sit_ashes): the seat touches the ground right at the anchor and
            the heels rest on the same line;
          - kneeling: under the hips (knees and toes on the ground line);
          - 'sleep' and 'carried': under the hip; the flat underside of the body lies on the anchor line
            (for 'carried' that line is the lifting hands, see sailor 'lift');
          - airborne 'fall' and 'float': bottom-centre of the figure's bounding box.
* scale   1.0 = adult about 330 px tall on the 2112x1188 stage. Outlines (4 px) scale with the figure.
* facing  1 faces / moves right, -1 mirrors to face left. A bbox (l, t, r, b) mirrors to (-r, t, -l, b).
* expr    None = the pose's natural expression (listed per pose), or one of EXPRESSIONS:
            neutral, happy, sad, scared (wide eyes with small pupils, teeth, sweat drop, tremble marks),
            angry, surprised (big dark eyes, round 'o'), sleepy (closed eyes), peaceful (closed eyes, smile),
            dizzy (spiral eyes), shout (wide open mouth, raised brows - not angry), call (earnest open mouth,
            for proclaiming), sorry (downcast eyes, blush), worried, tired (droopy lids, panting, 3 sweat drops),
            sly (lids lowered, sideways glance, lopsided smirk - gentle, not scary), smug (heavy level lids,
            raised brows, smirk).
          Unknown pose / expr / attire / kind names raise ValueError listing the valid ones.
* marks   False hides motion / sound / sleep marks (z's, sound arcs, shake and fan arcs, tremble lines),
          e.g. the moment Jonah is woken. Water drops (wet=True) and sweat drops always show.
* Bounding boxes below are (left, top, right, bottom) in px relative to the anchor at scale=1, facing=1,
  measured from rendered figures (outline + wobble included, +-3 px). Multiply by ``scale``.
  bottom 0..5 = outline on the ground line. Head centres (stand): adult (2, -282), woman (2, -271),
  child (2, -179), elder (22, -273), captain (2, -304), king (2, -293).
* Style: 3/4 view facing ``facing``, round head (~3.7 heads tall), dot eyes with highlight, soft nose dot,
  rosy cheeks, umber ink outlines (art.style.INK, 4 px, round joins). No pure black or white anywhere.

Animation tips: walk = alternate walk_a/walk_b about every 0.25 s while moving x (a 2-frame flipbook layer);
run = run_a/run_b about every 0.15 s. Keep breathing subtle. Put each moving character on its own layer;
add ``ground_shadow`` on the layer below.

jonah(x, y, scale=1.0, facing=1, pose='stand', expr=None, wet=False, marks=True)
--------------------------------------------------------------------------------
The hero; identical design in every pose: ochre-orange robe (P['jonah_robe']) with darker hem band and
cuffs (P['jonah_robe_dark']), teal waist sash with knot (P['jonah_sash']), cream head-cloth (P['headcloth'])
with a brown band (P['headcloth_stripe']) and a striped flap hanging behind the neck (it flies up in
fall / float / run), short brown beard (P['beard']), skin P['skin'], brown sandals.
wet=True: robe and cloth ~22% darker with soaked patches at the hem, three seaweed strands draped over the
head-cloth (one down onto the shoulder), outlined drops (with highlight) falling from beard, hem, flap and
fingertips. Adds up to ~13 px to the bbox; drops never go below the ground line except in fall / float /
carried.
  pose          bbox (l, t, r, b)        natural expr  notes
  stand         (-69, -333,  58, 0)      neutral
  walk_a        (-88, -332,  83, 1)      neutral       stride frame 1 ('walk' is an alias)
  walk_b        (-66, -335, 104, 0)      neutral       stride frame 2
  run_a         (-118, -303, 122, 0)     neutral       run frame 1 (leaning, back foot kicked up)
  run_b         (-92, -297, 141, 0)      neutral       run frame 2
  sleep         (-205, -191,  96, 0)     sleepy        curled on his side, knees drawn up under the robe,
                (marks=False: top -130)                cheek resting on both palms; HEAD ON THE LEFT for
                                                       facing=1 (right for -1); z's rise above the head.
                                                       Points at scale 1: head (-136, -79), upper shoulder
                                                       (-80, -75), hands (-123, -13), pelvis (0, -35)
  kneel_pray    (-90, -290,  49, 5)      peaceful      kneeling, palms together, head tilted up
  sit           (-74, -229, 119, 3)      neutral       on the ground, knees up, hands resting on the knees
  sit_sulk      (-72, -228, 117, 2)      angry         sitting, knees up, arms crossed, chin down
  sit_faint     (-87, -225, 124, 5)      tired         slumped back on one palm (on the ground behind him),
                                                       head drooping, weak fanning hand at the chin
  sit_happy     (-129, -230, 144, 5)     happy         legs stretched out, arms open
  preach        (-73, -337,  68, 0)      call          one arm raised high, open hand, earnest open mouth
  point         (-69, -334, 150, 0)      neutral       arm straight out toward ``facing``
  arms_up       (-76, -334,  74, 0)      happy         both arms up
  fall          (-152, -277, 150, 6)     scared        tumbling through the air: body tilted 58 deg forward
                                                       (head toward ``facing``), arms flung up, both knees
                                                       bent with the near foot kicked up behind, robe blown up
                                                       to the shins, head-cloth flap and sash streaming up
  float         (-135, -333, 138, 3)     scared        underwater: tilted 18 deg, arms spread slightly up,
                                                       knees bent, wavy hem flaring up, flap drifting up and
                                                       sash tails drifting out in front
  refuse        (-71, -338, 139, 0)      angry         body and head turned AWAY from ``facing``, near arm out
                                                       at chest height toward ``facing`` with palm out ('no'),
                                                       head-shake marks on the face side
  confess       (-56, -330,  82, 0)      sorry         hand on chest, head bowed
  listen        (-86, -352,  64, 0)      neutral       head tilted up, eyes up, near hand cupped at the ear
                (marks=False: (-85, -334, 58, 0))      (cheek height, over the head-cloth edge, cup opening
                                                       toward ``facing``), sound arcs from above-front
  wake          (-65, -229, 140, 5)      sleepy        sitting up, legs out, rubbing an eye, other arm
                                                       stretched up
  carried       (-181, -131, 141, 52)    worried       lying on his back, held up overhead by the sailors
                                                       (Jonah 1:15): head lifted toward the viewer, near hand
                                                       on the chest, far arm dangling below the line (that is
                                                       the bottom 52), knees slightly bent, flap hanging down.
                                                       HEAD ON THE LEFT for facing=1. Points at scale 1: head
                                                       (-128, -79), pelvis (0, -36), feet (110..120, -16).
                                                       Body spans x -181..+141, so centre it with
                                                       x = middle_hand_x + 20*scale (see compositions sheet)

sailor(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, marks=True)
---------------------------------------------------------------------------------
Knee-length striped tunic with short sleeves, rope belt, bare legs, sandals. variant (taken mod 4):
  0 blue/cream stripes, red headband, curly dark-brown hair, light skin, clean-shaven
  1 red/cream stripes, blue knitted cap, short black beard, medium-brown skin
  2 teal/cream stripes, ochre headband, black curly hair, deep-brown skin, clean-shaven
  3 ochre/brown stripes, green knitted cap, full ginger beard, fair skin
Both feet stay planted on the ground line in every pose. Hand centres (far, near) at scale 1 are the
same for every variant (use hand_positions for other scales / facings).
  pose     bbox (union of variants)  natural expr  notes
  stand    (-61, -344,  56, 0)       neutral
  scared   (-94, -345,  81, 0)       scared        hands up beside the face (marks=False: top -335)
  throw    (-98, -340,  66, 0)       worried       body arched back, stepping forward, both hands raised
                                                   together up and in front of the head, heaving something
                                                   overboard: hands (54, -322), (17, -303)
  carry    (-47, -308, 108, 0)       worried       crouched, both knees bent, arms forward at hip height:
                                                   hands (97, -109), (63, -118)
  pray     (-96, -341,  55, 0)       scared        both hands raised to the sky, looking up
  point    (-61, -345, 150, 0)       neutral       hand (126, -215)
  pull     (-111, -309, 103, 0)      angry         leaning back, front leg braced straight, back knee bent,
                                                   straight arms angled down along one rope line through the
                                                   fists (81, -166) and (37, -151) (rope rises toward the front)
  lift     (-70, -340,  65, 0)       worried       both hands up beside the head (52, -317), (-55, -316),
                                                   lifting a person together with others: e.g. 3 sailors
                                                   120*scale apart, then jonah(pose='carried') at x = middle
                                                   sailor x + 20*scale, y = hand-centre y + 6*scale, drawn
                                                   BEHIND the sailors so their hands hold him

captain(x, y, scale=1.0, facing=1, pose='stand', expr=None, marks=True)
-----------------------------------------------------------------------
Bigger, broader man: short rounded deep-red seaman's cap with rolled brim and knot, grey hair and a short
grey beard, long open blue coat (lapels, both front edges showing) over a narrow cream red-striped tunic
that ends just above the coat hem, rope belt on the tunic, sandals.
  stand    (-61, -365,  67, 0)   neutral
  wake     (-46, -293, 166, 1)   worried   crouching and leaning far forward; hands at (154, -74) (far) and
                                           (100, -109) (near). To wake the sleeping Jonah, use the SAME facing
                                           as Jonah and the same ground line: captain_x = jonah_x -
                                           facing*234*scale puts the far hand on Jonah's upper shoulder and the
                                           near hand just above his head; draw the captain on the layer behind
                                           Jonah and pass marks=False to Jonah (or compute it with body_points:
                                           Jonah's shoulders[0] minus the captain's hands[0]).
  point    (-61, -365, 167, 0)   neutral
  worried  (-68, -368,  62, 0)   worried   both hands on his head

king(x, y, scale=1.0, facing=1, pose='stand', attire=None, expr=None, throne=True, ashes=True, marks=True)
---------------------------------------------------------------------------------------------------------
Assyrian king of Nineveh, gentle and friendly: long dark hair with soft waves, long curled beard (wavy
curl rows), short moustache with the mouth always visible below it.
attire='royal': tall cylindrical gold crown (P['crown']) with rosettes and a top spike, purple robe
  (P['royal']) with gold hem border and fringe, light-purple diagonal shawl with gold trim, gold collar,
  sash and cuffs.
attire='sackcloth': crown removed (hair shows), burlap robe (P['sackcloth']) with stitched patch, rope belt,
  light ash speckles on hair / forehead / lower cheek (never near the eyes) and on the robe, barefoot.
attire=None (default): 'royal', except pose='sit_ashes' which is always sackcloth (Jonah 3:6);
  sit_ashes with attire='royal' raises ValueError.
  pose          bbox royal              bbox sackcloth          natural expr
  stand         (-56, -397, 62, 0)      (-56, -344, 62, 0)      neutral (sackcloth: sad)
  sit_throne    (-92, -344, 120, 1)     (-92, -292, 112, 1)     neutral  seated with a horizontal lap, hands
                                                                         on the knees, feet on the ground.
                throne=True draws a high-backed wooden throne with gold knobs behind him, standing on the
                anchor's ground line. throne=False: just the seated figure, bbox (-61, -344, 120, 0); supply
                a seat whose top is ~67 px above the ground (the seat bottom), from x-60 to x+70.
  sit_ashes     -                       (-85, -230, 127, 2)     sad      on the ground, knees up, head bowed,
                hands on the knees; ashes=True draws a grey ash heap under him (ashes=False: (-39, -230, 116, 0))
  kneel_pray    (-94, -346, 53, 5)      (-90, -300, 53, 4)      peaceful
  remove_crown  (-59, -346, 102, 0)     (-59, -344, 102, 0)     sorry    bare-headed, holding the crown (tipped
                toward the viewer, spike and rosettes showing) in front of his chest, hands at its sides
                (hands (92, -182) and (16, -180)); also in sackcloth
attire='darius' (Daniel 6, never chosen by default): King Darius of Persia - a tall gold crown with stepped
  crenellations and a row of blue / lilac jewels, a purple robe (DARIUS_ROBE) strewn with small gold flowers, wide
  gold hem, gold sash with tails, gold collar and cuffs, no shawl, curled dark beard and hair (DARIUS_HAIR).
  remove_crown holds the crenellated crown; sit_ashes is not allowed. Use throne=False + props.throne() for
  every seated pose (sit_throne / sit_sign / sit_sad: same seat height, props.KING_SEAT_Y).
  More poses (added for Darius; they work in every attire). bbox and hands [far, near] for attire='darius':
  stand         (-56, -388, 62, 0)    neutral   hands (48, -127), (-38, -126)
  walk_a/walk_b (-93, -388, 87, 1) / (-71, -390, 110, 0)   neutral
  pace_a/pace_b (-93, -387, 100, 1) / (-65, -391, 100, 0)  worried  walking with the hands behind the back, head
                bowed (flip every ~0.35 s while moving x slowly: thinking how to save Daniel / the sleepless night)
  sign          (-54, -390, 110, 0)   neutral   standing; a decree hangs from its roller in the far hand (77, -230),
                the near hand (64, -180) presses the gold seal onto it (a red seal mark shows)
  sit_sign      (-92, -337, 120, 1)   neutral   the same seated (the decree rests on the knee); hands (86, -168),
                (63, -130). With throne=False draw props.throne() first at the same anchor
  sad           (-54, -386, 107, 0)   sad       standing, head bowed, front hand on the forehead (71, -298)
  sit_sad       (-92, -325, 133, 1)   sad       seated, leaning forward, chin in the near hand (46, -182), the
                other hand on the knee (80, -83) (on the throne, or on props.couch(): king at couch_x + 20*scale,
                y - 85*scale)
  call_out      (-60, -384, 169, 0)   call      leaning forward, both arms out and down: calling into the den
  reach_out     (-60, -388, 155, 0)   happy     arms forward at chest height, open hands
  hug           (-60, -390, 121, 0)   happy     hugging someone: draw daniel(x + 95*scale*facing, y, scale, -facing)
                FIRST, then the king, whose arms come round Daniel's shoulders; hands (107, -241), (86, -219)
  arms_up       (-81, -391, 78, 0)    happy     both arms up for joy

citizen(x, y, scale=1.0, facing=1, kind='man', variant=0, pose='stand', attire='normal', expr=None, marks=True)
------------------------------------------------------------------------------------------------------------
Townspeople of Nineveh in long Mesopotamian robes. kind:
  'man'    curled beard; diagonal shawl; even variants long dark hair, odd variants a wrapped cap
  'woman'  veil over the head draping down the back, waist sash
  'child'  knee tunic with rope belt; even variants boy (curly hair), odd variants girl (ponytail, ribbon)
  'elder'  white hair and beard, shawl, slightly stooped with a walking stick in stand / walk / sad;
           odd variants wear a wrapped cap
variant (mod 4) robe + wrap colours: 0 sand + terracotta, 1 plum-rose + ochre, 2 olive + golden ochre,
  3 indigo + cream; skin tones vary from light to deep brown. No citizen wears Jonah's orange robe with a
  cream head-cloth, so Jonah stays recognisable in crowds.
attire='sackcloth': burlap robe, rope belt, ash speckles, barefoot, no shawl or cap (women keep a burlap
  veil). Natural expr becomes 'sad' for stand / walk.
  pose         man                   woman                 child                 elder                natural
  stand        (-54, -337, 58, 0)    (-54, -321, 53, 0)    (-54, -224, 43, 0)    (-49, -327, 70, 3)   neutral
  walk/walk_a  (-88, -336, 83, 1)    (-84, -320, 78, 1)    (-57, -225, 57, 0)    (-86, -322, 81, 3)   neutral
  walk_b       (-66, -338, 105, 0)   (-61, -321, 99, 0)    (-48, -227, 71, 0)    (-61, -327, 112, 3)  neutral
  listen       (-56, -337, 54, 0)    (-58, -321, 51, 0)    (-58, -224, 40, 0)    (-49, -327, 64, 0)   worried
               (head slightly up toward the speaker, hand to chin)
  kneel_pray   (-90, -294, 49, 5)    (-85, -278, 44, 4)    (-71, -200, 37, 3)    (-87, -285, 47, 5)   peaceful
  point        (-54, -337, 150, 0)   (-54, -321, 143, 0)   (-54, -224, 104, 0)   (-52, -328, 146, 0)  neutral
  sad          (-51, -333, 89, 0)    (-48, -316, 83, 0)    (-33, -219, 71, 0)    (-50, -318, 106, 3)  sad
               (head bowed, arms hanging)
  cheer        (-99, -337, 103, 0)   (-93, -321, 96, 0)    (-69, -224, 72, 0)    (-96, -328, 100, 0)  happy
               (arms up in a V, e.g. children playing)
  (bboxes are unions over the 4 variants and both attires)

daniel(x, y, scale=1.0, facing=1, pose='stand', expr=None, marks=True)          [Daniel film]
-------------------------------------------------------------------------
Daniel: a kind grown man (a little taller than Jonah; head centre (2, -287)), deep-blue robe (DANIEL_BLUE) with a
darker hem band and cuffs, gold sash with knot, cream head-cloth with a gold band and a cream flap with blue
stripes hanging behind, short rounded dark-brown beard with a few grey flecks and a moustache, skin DANIEL_SKIN.
Never orange / teal like Jonah, so the two heroes are never confused. Same rig and conventions as jonah().
  pose        bbox (l, t, r, b)       natural expr  notes (hands at scale 1, facing 1)
  stand       (-70, -340, 60, 0)      neutral
  walk_a      (-91, -340, 85, 1)      neutral       stride frames (alternate every ~0.25 s)
  walk_b      (-69, -342, 107, 0)     neutral
  kneel_pray  (-92, -296, 51, 5)      peaceful      palms together (41, -169), head tilted up (praying at the window)
  kneel_up    (-92, -298, 70, 5)      happy         kneeling, both arms lifted in thanks (57, -280), (-70, -276)
  kneel_bow   (-92, -295, 89, 5)      peaceful      kneeling, head bowed over the praying hands (55, -157)
  sit         (-75, -233, 120, 3)     neutral       on the ground, knees up, hands on the knees (pass expr='peaceful'
                                                    or 'happy' for the calm night among the lions)
  sit_pray    (-74, -233, 120, 3)     peaceful      on the ground, praying hands (43, -105)
  explain     (-70, -340, 67, 0)      happy         near hand open, palm up in front (50, -173): talking
  point       (-70, -340, 155, 0)     neutral       hand (130, -219)
  look_up     (-80, -337, 84, 0)      happy         head tipped back, eyes up, hands open at his sides (from the den)
  answer      (-70, -341, 75, 0)      call          looking up, front hand raised and open (62, -323): answering the
                                                    king from the den
  bow         (-54, -330, 112, 0)     peaceful      polite bow, hand on chest (42, -213)
  read        (-70, -338, 113, 0)     neutral       an open hand-scroll held at chest height between (39, -194) and
                                                    (101, -201), looking down at it (working in the palace)
  hold_rope   (-68, -343, 87, -1)     happy         being pulled up: fists in front of the chest (65, -260), (67, -224),
                                                    legs hanging; draw the rope straight up from the far hand (the
                                                    anchor is the lowest sole: move y to lift him)
  arms_up     (-79, -340, 76, 0)      happy
  sad         (-56, -335, 87, 0)      sad           head bowed, arms hanging
  listen      (-70, -340, 56, 0)      worried       hand to chin, head slightly up
Put him at y = window_y + props.WINDOW_FLOOR_Y*scale behind props.upstairs_window(part='front') (pose
'kneel_pray', facing toward Jerusalem): head, head-cloth and praying hands show in the opening.

official(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, marks=True)   [Daniel film]
--------------------------------------------------------------------------------------
The jealous Persian court officials (gentle, never frightening): ankle-length robes covered in small repeating
motifs, contrasting hem band, cuffs and belt, curled hair and beards. variant (mod 4):
  0 crimson robe with gold diamonds, tall rounded maroon felt hat with a gold band, black pointed beard
  1 green robe with cream flowers, cream turban with a red jewel and feather, short curled beard
  2 rust robe with blue dots, tall cream fluted hat with a teal band, grey pointed beard and grey hair (older)
  3 mustard robe with maroon diamonds, teal turban with a gold jewel and feather, deep-brown skin
Tall hats reach ~376 px above the ground, turbans ~350.
  pose      bbox (union of variants)  natural expr  notes
  stand     (-62, -376, 59, 0)        neutral
  walk_a/_b (-89, -376, 83, 1) / (-67, -377, 105, 0)   neutral  (hurrying to the king; with expr='sad' when led away)
  whisper   (-51, -374, 88, 0)        sly           leaning in, hand raised beside the mouth (two officials face to
                                                    face ~110*scale apart)
  point     (-62, -376, 151, 0)       sly           pass expr='shout' / 'surprised' for '看！他在向他的上帝祷告！'
  bow       (-49, -347, 164, 0)       smug          deep bow to the king, hands together in front (flattering)
  peek      (-55, -352, 114, 0)       sly           crouched on tiptoe, leaning forward, hands up in front as if at a
                                                    wall corner (spying on Daniel's window)
  scheme    (-57, -375, 60, 0)        sly           hands rubbed together in front of the belly
  read      (-52, -373, 112, 0)       worried       searching Daniel's records (open scroll in both hands)
  sad       (-48, -366, 107, 0)       sad           head bowed, arms hanging

guard(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, spear=None, marks=True)   [Daniel film]
-------------------------------------------------------------------------------------------------
Friendly palace guards: knee-length tunic with a contrasting hem and neck, rope belt, trousers in soft boots,
rounded bronze helmet with a little plume, a round painted shield slung on the back, and a spear (wooden shaft,
small leaf blade, gold ball butt) held upright in the near hand. variant (mod 4): 0 brick red / blue shield,
stubble; 1 olive / red shield, young, clean-shaven, deep skin; 2 ochre / green shield, brown beard; 3 blue-grey /
ochre shield, curled beard. spear=None: spear in stand / walk_a / walk_b, none in push / pull_rope; spear=False
in stand / walk gives a relaxed empty hand instead; spear=True forces it.
  pose       bbox (union)            natural expr  hands [far, near] at scale 1
  stand      (-75, -388, 74, 0)      neutral       spear hand (63, -180); spear tip ~-388
  walk_a/_b  (-88, -388, 83, 1) / (-71, -390, 103, 0)   neutral  the spear arm stays still, the other swings
  push       (-71, -322, 170, 1)     worried       leaning in, both palms flat forward (162, -176), (116, -189):
                                                   rolling the stone (props.den_stone is ~170*stone_scale wide on
                                                   each side of its anchor, its centre ~128*stone_scale up)
  pull_rope  (-117, -314, 103, 0)    happy         leaning back on a rope through the fists (81, -166), (37, -151)
                                                   (as sailor 'pull'): pulling Daniel up out of the den

ground_shadow(x, y, scale=1.0, width=120, opacity=0.22, color=None)
--------------------------------------------------------------------
Soft blurred oval contact shadow centred on an anchor point (uses the #soft filter). Put it on a layer
under the figure. Suggested width: standing 120, sitting/kneeling 200, sleep 300, child 90 (none for
'carried', 'fall' or 'float').
bbox about (-width/2, -12, width/2, 20) * scale.

hand_positions(fn, x, y, scale=1.0, facing=1, **kw) -> [(x, y) far hand, (x, y) near hand]
---------------------------------------------------------------------------------------------
Stage coordinates of both hand centres of the figure ``fn(x, y, scale, facing, **kw)`` would draw, e.g.
``hand_positions(sailor, 800, 900, 0.8, -1, variant=2, pose='pull')`` -> where to run the rope.
The hand offsets quoted above are these values at scale=1, facing=1 (mirror x for facing=-1).

body_points(fn, x, y, scale=1.0, facing=1, **kw) -> dict
---------------------------------------------------------
Stage coordinates of key points of that figure: 'head' (centre), 'head_top', 'hands' [far, near],
'shoulders' [far, near], 'pelvis', 'feet' [far ankle, near ankle] and 'bbox' (left, top, right, bottom).
Use it to attach props (a cargo jar on carrying hands, a stick, a rope) or to place figures relative to
each other (see captain 'wake').

Constants: EXPRESSIONS, JONAH_POSES, SAILOR_POSES, CAPTAIN_POSES, KING_POSES, KING_ATTIRES, CITIZEN_POSES,
CITIZEN_KINDS, CITIZEN_ATTIRES, DANIEL_POSES, OFFICIAL_POSES, GUARD_POSES (tuples of the valid names);
DANIEL_BLUE, DANIEL_SKIN, DARIUS_ROBE, DARIUS_HAIR (colours). hand_positions / body_points work for daniel,
official and guard too. Daniel-film sheets: python3 tools/character_sheet.py daniel.

DAVID FILM (1 Samuel 17, stories/david)                     sheets: python3 tools/character_sheet.py david
=======================================
Same conventions as above (anchor = ground between the feet, facing, scale, marks, bboxes at scale 1 / facing 1
measured from renders). hand_positions / body_points work for every function below.
SCALE: at the same ``scale`` David is ~252 px to the top of his curls (a boy of ~12, head centre (2, -200)),
adults ~330-400 (Eliab -364, Saul -399 with helmet plume), Goliath ~634 to the helmet top (2x an adult, head
centre (2, -512)); his spear reaches -924 (raised in 'shout': -1118). Put all of them on the same ground line
with the same scale. Line weight is the same 4 px for all (Goliath is NOT a scaled-up adult: his face, belt and
armour details keep the library's line weight).
New expressions (ALL_EXPRESSIONS = EXPRESSIONS + DAVID_EXPRESSIONS; any function accepts them):
  brave (lowered brows, firm closed smile), puzzled (one brow up, slanted mouth), laugh (^ eyes, open laughing
  mouth with teeth), cross (frowning brows, pout), sneer (lidded eyes, lopsided toothy grin - cartoon-smug),
  kind (soft brows, smile, warm blush), roar (angry brows + wide shouting mouth).

david(x, y, scale=1.0, facing=1, pose='stand', expr=None, bag=True, staff=False, basket=False, armor=False,
      phase=0.0, stone=True, marks=True)
---------------------------------------------------------------------------------------------------------
The shepherd boy: child proportions, round face with ruddy cheeks, a mop of reddish-brown curls (DAVID_HAIR),
short-sleeved warm-green knee tunic (DAVID_TUNIC) with a rope belt, sandals. bag=True: leather shepherd's bag on
the back hip with its strap across the chest (bag=False hides it).
  pose           bbox                     natural expr  notes (hands [far, near] at scale 1)
  stand          (-51, -252, 45, 0)       happy
  walk_a/walk_b  (-64, -254, 62, 0) / (-50, -256, 77, 0)   planted-foot stride frames (alternate ~0.25 s)
  run_a/run_b    (-84, -233, 88, 0) / (-64, -228, 102, 0)  brave   (alternate ~0.15 s)
  talk           (-54, -252, 50, 0)       happy         near hand open, palm up
  point_up       (-61, -251, 68, 0)       brave         front hand raised, finger pointing up to heaven, face up
  kneel_pick     (-61, -196, 119, 0)      happy         one knee down, bending forward, both hands at the brook
                                                        bed in front (~(55, -60)): picking a stone; head (68, -144)
  hold_sling     (-54, -253, 47, 0)       brave         the sling hangs from the near hand, loaded (stone=False:
                                                        empty pouch). staff=True: the crook in the far hand
                                                        (-54, -292, 109, 2) - 'he took his staff and his sling'
  sling_spin     (-76, -252, 168, 0)      brave         front arm raised forward, the sling whirling round the
                 (union of phases)                      hand: phase 0..1 = pouch position on the whirl (0 front,
                                                        .25 near side, .5 back, .75 far side) with swirl lines;
                                                        the back half is drawn behind the head. Flipbook 8 phases
                                                        (0, .125 ... .875) at ~0.06 s each.
  sling_release  (-79, -244, 244, 0)      brave         lunging, front arm thrown forward, one cord let go, the
                                                        empty pouch whipping forward, whoosh marks; front hand
                                                        (104, -144) = where the stone leaves (props.stone flies on)
  carry_basket   (-51, -252, 75, 0)       happy         a basket of bread and cheese in both hands in front
  sit_harp       (-48, -181, 93, 7)       peaceful      sitting on the ground, knees up, playing a small harp
  cheer          (-74, -251, 77, 0)       happy         both arms up
  pray           (-60, -251, 42, 0)       peaceful      standing, palms together, face lifted
  kneel_pray     (-69, -224, 38, 3)       peaceful
  armor_wobble   (-113, -246, 88, 0)      worried       leaning back, arms out for balance, back foot lifted
Options:
  staff=True     shepherd's crook in the near hand for stand / walk_a / walk_b (top ~-293, crook to x+83);
                 far hand for hold_sling; ignored in other poses (lay props.staff() beside him instead).
  basket=True    stand / walk_a / walk_b with the bread basket hanging from the near hand.
  armor=True     Saul's armour, far too big (17:38-39): a bronze helmet with circlet and red plume slid down over
                 his eyes (nose, cheeks and mouth show), a long grey chain-mail coat pooling on the ground, a big
                 leather belt, a long sword in its scabbard dragging on the ground behind. Use with stand / walk_a /
                 walk_b / talk / armor_wobble: bbox about (-117, -302, 95, 2). Every other option still works.

goliath(x, y, scale=1.0, facing=1, pose='stand', expr=None, progress=1.0, bump=False, spear=True, sword=True,
        marks=True)
------------------------------------------------------------------------------------------------------------
The Philistine champion, big and loud but cartoon-friendly: heroic proportions, bushy brows, a full dark beard (big
jaw), a bronze helmet with a red comb crest (sits high: the FOREHEAD shows), bronze scale corselet with a leather
belt and leather strips over a red tunic (GOLIATH_TUNIC), bronze greaves, sandals, a sword hanging at the hip
(sword=False hides it) and a huge spear 'like a weaver's beam' (GOLIATH_SPEAR_LEN = 900 px, iron head).
spear=True: upright in the near hand (stand / stride), raised high in the far hand (shout), resting upright in the
far hand (laugh, mock_point); never in fall / lying (draw props.spear(kind='goliath') lying nearby).
Figure alone (spear=False) stand: (-100, -632, 142, 0); head centre (2, -512).
  pose           bbox (with spear)         natural expr  notes
  stand          (-100, -924, 168, 2)      sneer
  stride_a/_b    (-156, -924, 180, 4) / (-98, -924, 192, 4)   angry   heavy walk; alternate ~0.35 s (boom, boom)
  shout          (-146, -1118, 184, 0)     roar          spear raised, other fist forward, sound arcs at the mouth
  laugh          (-194, -926, 156, 2)      laugh         head back, hand on the belly, 'ha ha' ticks
  mock_point     (-94, -926, 210, 2)       sneer         leaning, pointing down-forward at someone small
  fall           progress=0..1             surprised     arms flung forward; the whole body pivots about the toes
                 0: (-124, -628, 150, 0)   (x = 0.9*55 px in front of the anchor) from upright (0) to lying face
                 .5: (-32, -558, 544, 4)   down (1); it is lifted so it never sinks below the ground. The angle is
                 1: (48, -274, 676, 0)     90*progress: ease it in the scene (slow start, fast end) and quantise
                                           (e.g. 0, .1, .25, .45, .7, 1). The head ends ~600*scale toward facing.
  lying          (48, -324, 672, 0)        dizzy         flat on his front (same place as fall progress=1), arms
                                                        forward, head lifted with spiral eyes. bump=True adds three
                                                        circling stars over the head.
bump=True (any pose): a round pink bump on the forehead where the stone hit (no blood, ever).
goliath_head_point(x, y, scale=1.0, facing=1, pose='stand', progress=1.0) -> (x, y) stage point of the forehead
  (where the stone lands): stand (30, -544), stride_a (53, -545), lying (552, -148) at scale 1; follows 'fall'.

shield_bearer(x, y, scale=1.0, facing=1, pose='walk_a', variant=0, expr=None, marks=True)
----------------------------------------------------------------------------------------
A Philistine (soldier(side='philistine') look, variant 0-3) walking in front of Goliath behind the champion's huge
tall woven shield (bronze rim and boss, ~300 px tall) held in front of him: only his reed crown, face, shoulder,
near hand and legs show. poses stand (-50, -342, 117, 0), walk_a (-88, -342, 117, 1), walk_b (-62, -344, 117, 0).
Put him ~200-260*scale in front of Goliath (toward facing).

soldier(x, y, scale=1.0, facing=1, side='israel', variant=0, pose='stand', expr=None, spear=None, shake=0.0,
        marks=True)
-------------------------------------------------------------------------------------------------------------
Crowd soldiers on the adult rig (330 px). side='israel': simple knee tunics in blues / browns, rope belt, small
round leather cap, beards vary, round wood-and-leather shield with bronze rim; side='philistine': clean-shaven,
an upright crown of reeds / feathers on a patterned band, short kilt with a fringe, a sash, round bronze shield.
variant 0-3 (mod 4) changes colours, skin tone and hair / beard (SOLDIER_SIDES, SOLDIER_POSES).
spear=None: a spear in stand / walk_a / walk_b (False: empty hand); the shield hangs on the back except in cower.
  pose        bbox (union of variants and sides)  natural expr
  stand       (-75, -388, 74, 0)                  neutral     spear tip ~-388
  walk_a/_b   (-88, -388, 83, 1) / (-71, -390, 103, 0)
  cower       (-47, -306, 124, 0)                 scared      crouched, knees bent, shield held up in front of
                                                              the face (scared eyes peek over it), knee tremble
                                                              marks; shake=0..1 jitters the body (+-3.5 px):
                                                              cycle 0, .25, .5, .75 for trembling
  run_a/run_b (-118, -313, 122, 0) / (-92, -306, 141, 0)  scared  fleeing (give facing away from the danger)
  cheer       (-99, -343, 103, 0)                 happy       arms up (Israel's victory)
  point       (-75, -343, 100, 0)                 surprised   pointing toward facing

king(..., attire='saul', stool=True)  - King Saul
-------------------------------------------------
attire='saul' (never a default): tall (metrics 1.1 x an adult), dark curly hair and full dark beard, bronze helmet
with a gold circlet of points and a lilac plume, bronze scale corselet with leather strips over a blue tunic
(SAUL_TUNIC) with a gold hem, purple cloak hanging down his back with a gold clasp, bronze greaves, sword at the hip.
New poses (KING_EXTRA_POSES; they work in every attire): 'sit' (on a folding camp stool, hands on the knees;
stool=False draws no stool - use props.camp_stool() at the same x, y, scale, facing), 'talk' (open hand, kind),
'bless' (hand raised, palm out, kind). All older king poses work for Saul except sit_ashes / remove_crown
(ValueError). Natural expressions: neutral (stand / walk), kind (talk / bless); pass worried / surprised / kind.
  stand (-84, -399, 65, 0)  talk (-84, -398, 72, 0)  bless (-84, -396, 74, 0) palm (66, -270)
  walk_a/_b (-98, -402, 93, 0) / (-78, -404, 118, 0)  sit (-87, -341, 127, 3)  sit_throne (-95, -341, 127, 1)

eliab(x, y, scale=1.0, facing=1, pose='stand', expr=None, marks=True)
--------------------------------------------------------------------
David's eldest brother: a tall young Israelite soldier (1.07 x an adult): teal tunic with ochre trim, leather cap,
dark stubble beard, shield on his back. ELIAB_POSES: stand (-81, -364, 61, 0), walk_a/_b (-95, -364, 89, 1) /
(-77, -366, 113, 0), talk (-81, -363, 71, 0) neutral, scold (-77, -363, 109, 0) cross - finger pointing at David,
other fist on the hip, hands_hips (-81, -364, 69, 0) cross. Expressions: pass 'cross' or 'neutral' (or any).

jesse(x, y, scale=1.0, facing=1, pose='stand', expr=None, marks=True)
--------------------------------------------------------------------
David's old father: white hair and beard, cream head-wrap, warm rust robe with an ochre shawl, slightly stooped with
a walking stick (stand / walk / talk). JESSE_POSES: stand (-50, -327, 70, 3), walk_a/_b (-86, -322, 81, 3) /
(-61, -327, 113, 3), talk (-50, -327, 69, 3) happy, give (-56, -326, 140, 0) happy - holding out the basket of
bread and cheese in both hands (hands (125, -181), (79, -196)): stand David 'carry_basket' facing him to take it.

Constants (David film): DAVID_POSES, GOLIATH_POSES, SOLDIER_POSES, SOLDIER_SIDES, SHIELD_BEARER_POSES,
KING_EXTRA_POSES, ELIAB_POSES, JESSE_POSES, DAVID_EXPRESSIONS, ALL_EXPRESSIONS, GOLIATH_SPEAR_LEN; colours
DAVID_TUNIC, DAVID_SKIN, DAVID_HAIR, GOLIATH_SKIN, GOLIATH_TUNIC, SAUL_TUNIC, SAUL_HAIR, BRONZE (+ _DARK / _LIGHT),
LEATHER, CORD, MAIL. God is never drawn: show him as light (art.style / engine.fx), never as a figure.

NOAH FILM (Genesis 6-9, stories/noah)                       sheets: python3 tools/character_sheet.py noah
=====================================
Same rig and conventions as above (anchor = ground under the pelvis, between the feet; facing; scale; marks; bboxes
(l, t, r, b) at scale 1 / facing 1 measured from renders, wobble included). hand_positions / body_points work for
every function here (for child(pose='jump') subtract CHILD_JUMP*scale from their y).
SCALE: at the same ``scale`` Noah is ~333 px tall (head centre (2, -282)), his wife ~314, the sons 339-349, the
daughters-in-law 311-321, the child ~223 (head centre (2, -179)). Put them all on one ground line with one scale.
New expressions (NOAH_EXPRESSIONS; every function accepts them): determined (lowered brows, firm closed smile),
amazed (big shining eyes, raised brows, open delighted 'oh!' mouth). Also useful: kind, happy, puzzled, worried,
peaceful, surprised, laugh (DAVID_EXPRESSIONS / EXPRESSIONS).

noah(x, y, scale=1.0, facing=1, pose='stand', expr=None, phase=0.0, item='sack', dove=False, sawhorse=True,
     marks=True)
----------------------------------------------------------------------------------------------------------
Noah: a kind, sturdy, lively grandfather - long wavy white beard (beard kind 'long', moustache curling up into a
smile), bushy grey brows, smile wrinkles at the eyes, a grey tuft at the temple, a pale sage-cream head-cloth
(NOAH_CLOTH) with a green band (NOAH_BAND) and a flap down the back, a warm brown robe (NOAH_ROBE) with an ochre
hem band and cuffs (NOAH_TRIM), a rope belt, sandals. Never orange / teal (Jonah) or blue (Daniel).
  pose          bbox (l, t, r, b)        natural expr  notes (hands [far, near] at scale 1)
  stand         (-69, -333, 60, 0)       kind          hands (47, -122), (-37, -121)
  walk_a/walk_b (-90, -332, 84, 1) / (-69, -335, 105, 0)   happy   planted-foot stride frames; walk_c
  walk_c        (-67, -337, 59, 0)       happy         the passing frame (feet together): cycle a, c, b, c every
                                                       ~0.2 s while moving x (or a/b only, as the other films)
  talk          (-69, -334, 65, 0)       happy         near hand open, palm up (48, -171)
  pray          (-67, -334, 57, 0)       peaceful      standing, palms together (48, -204), face lifted
  kneel_pray    (-91, -290, 52, 5)       peaceful
  point_up      (-66, -334, 93, 0)       determined    finger up to heaven (81, -305)
  scratch_head  (-69, -368, 81, 0)       puzzled       hand on top of the head, other fist on the hip, a '?' mark
                                                       (marks=False hides it): "a boat here, so far from the sea?"
  nod           (-67, -329, 70, 0)       kind          head bowed 22 deg: alternate with 'stand' (~0.3 s) to nod yes
  saw           (-57, -300, 377, 6)      determined    leaning over a plank on a low sawhorse in front (the trestle
                                                       stands at x+236*scale, plank top ~-103); the saw slides along
                                                       its blade: phase 0 pulled back, .5 pushed forward, 1 back
                                                       (flipbook 0, .25, .5, .75 at ~0.12 s; sawdust specks when
                                                       marks). sawhorse=False: only the saw in the hand
                                                       (-57, -300, 230, 0), for sawing a plank of your own.
  hammer        phase 0 (-122, -366, 175, 0), .5 (-59, -392, 175, 0), 1 (-59, -332, 192, 0)   determined
                                                       hammer raised behind the head (0) .. swung down so the head
                                                       strikes the nail (1); the far hand holds the nail at NOAH_NAIL
                                                       = (146, -250) (put the hull / plank there); impact ticks at
                                                       phase >= .85. Flipbook e.g. 0, .35, .7, 1, 1 (hold), .5 ...
  carry         item='sack' (-129, -333, 61, 0) / 'hay' (-145, ...): a sack / a hay sheaf on the shoulder behind
                the head, steadied by the near hand; item='basket' (fruit), 'grain', 'veg' (-65, -333, 87, 0) or
                'jar' (amphora, right 77): held in both hands in front of the chest. CARRY_ITEMS. natural happy
  carry_walk_a/_b  the same carrying while walking (stride frames, bbox like carry with walk_a / walk_b legs)
  open_window   (-75, -334, 82, 0)       happy         both arms up, palms out, pushing the shutters open
  release_dove  (-67, -334, 135, 0)      kind          both arms reaching forward-up, open hands (120, -261),
                                                       (57, -275); dove=True puts a white dove (wings up) just
                                                       leaving the hands (top -371). Use props.dove for the flight.
  hold_leaf     (-67, -380, 81, 0)       amazed        far hand raised (61, -316) holding an olive twig up
  cheer         (-101, -334, 106, 0)     happy         both arms up
  wave          (-69, -334, 109, 0)      happy         far hand up, open; phase 0..1 swings the forearm (+-18 deg),
                                                       wave marks beside the hand (flipbook 0, .25, .5, .75)

noah_wife(...), shem(...), ham(...), japheth(...), daughter_in_law(x, y, scale, facing, variant=0..2, ...)
--------------------------------------------------------------------------------------------------------
Same signature and the SAME pose list as noah() (FAMILY_POSES = NOAH_POSES), including saw / hammer / carry
(item default 'basket' for the women, 'sack' for the men) and the dove / sawhorse options:
  noah_wife          plum-rose robe, cream veil with a rose edge, golden sash, smile wrinkles (head (2, -265))
  shem               eldest: blue robe with cream trim, dark curly hair and a full dark beard (head (2, -293))
  ham                terracotta robe, golden headband, black curly hair, short black beard, deep-brown skin
                     (head (2, -296), the tallest and broadest son)
  japheth            youngest: leaf-green robe, ginger curls and stubble, fair skin (head (2, -287))
  daughter_in_law    0 (Shem's wife) saffron robe, teal veil; 1 (Ham's) lilac robe, coral veil, brown skin;
                     2 (Japheth's) rose-pink robe, sky-blue veil (heads (2, -268) / (2, -271) / (2, -263))
  stand bboxes: wife (-52, -314, 53, 0), shem (-53, -345, 61, 0), ham (-64, -349, 64, 0), japheth (-51, -339, 58, 0),
  daughters-in-law (-54, -321, 54, 0) (union). Other poses: like Noah's, scaled to their height (e.g. saw / hammer
  extend to x +377 / +175; women's carry with a basket (-48, -317, 87, 0)).
family_member(name, x, y, scale=1.0, facing=1, **kw): any of FAMILY = ('noah', 'noah_wife', 'shem', 'ham',
  'japheth', 'daughter_in_law0', 'daughter_in_law1', 'daughter_in_law2') by name.

noah_family(x, y, scale=1.0, facing=1, pose='stand', expr=None, gap=150, items=None, marks=True)
---------------------------------------------------------------------------------------------
All eight at once, drawn back to front in one <g>. Anchor x = 85*scale left of Noah's feet (the middle of the group)
for the portrait; pose (FAMILY_GROUP_POSES) is given to everybody.
  group portrait  stand / cheer / pray / talk / wave / nod / kneel_pray: front row daughter_in_law0 (-255),
                  noah_wife (-85), Noah (+85, facing left toward his wife), daughter_in_law2 (+255); back row (36-40 px
                  higher, 0.97 x) daughter_in_law1 (-340), Shem (-170), Ham (0), Japheth (+170) - every face shows.
                  Left half faces right, right half faces left (facing=-1 mirrors the whole group).
                  bbox stand (-392, -378, 306, 4), cheer (-431, -379, 343, 4), kneel_pray (-423, -334, 337, 9).
  walking line    walk_a / walk_b / carry_walk_a / carry_walk_b: a procession toward `facing`, Noah leading AT x, the
                  others behind him every gap*scale px (wife, Shem, his wife, Ham, his wife, Japheth, his wife);
                  neighbours alternate stride frames. carry_*: items (list, cycled) default sack, basket, sack, grain,
                  hay, veg, sack, jar. bbox (-1109, -351, 105, 1) at gap 150 (mirror for facing=-1). Flip walk_a /
                  walk_b every ~0.25 s while moving x.

child(x, y, scale=1.0, facing=1, pose='stand', expr=None, hood=False, boots=True, coat=None, phase=0.0, marks=True)
-----------------------------------------------------------------------------------------------------------------
A little modern child (5-6 years, the story's listener) for the opening and the ending: a sunny yellow raincoat
(CHILD_COAT; coat='#7fb6d6' etc. for another colour) with toggle buttons, red rubber boots (CHILD_BOOTS;
boots=False shows bare legs and sandals), short brown hair; hood=True puts the hood up (otherwise it hangs at the
back). On the _CHILD rig (citizen(kind='child') size, 223 px). CHILD_POSES:
  stand        (-42, -223, 43, 4)    happy
  walk_a/_b    (-57, -224, 57, 1) / (-48, -226, 71, 0)
  peek_window  (-38, -223, 66, 4)    amazed   standing on tiptoe at a window, both hands on the sill in front at
                                              (54, -147), (46, -140): put the sill top ~ y-140*scale, nose ~ x+40
  splash       (-84, -204, 80, 3)    laugh    landing in a puddle: knees bent, arms flung up and out (pair with
                                              props.puddle(x, y, scale, splash=...))
  jump         (-65, -260, 60, -44)  laugh    in the air: the soles CHILD_JUMP = 46 px above the anchor's ground
                                              line (alternate jump / splash for jumping in puddles)
  point_up     (-54, -222, 60, 3)    amazed   pointing at the rainbow
  wave         (-45, -223, 55, 4)    happy    far hand up; phase swings it (as Noah's wave)
  smile_up     (-57, -221, 40, 4)    happy    face lifted, hands clasped at the chest
  cheer        (-69, -222, 72, 3)    laugh
  (hood=True adds ~2-3 px at the top.)

Constants (Noah film): NOAH_POSES, FAMILY_POSES, FAMILY_GROUP_POSES, CARRY_ITEMS, FAMILY, CHILD_POSES, CHILD_JUMP,
NOAH_NAIL, NOAH_EXPRESSIONS; colours NOAH_ROBE, NOAH_TRIM, NOAH_CLOTH, NOAH_BAND, NOAH_SKIN, NOAH_BEARD, CHILD_COAT,
CHILD_BOOTS. God is never drawn as a person (golden light only, see ART_GUIDE.md).

JOSEPH FILM (Genesis 37-50, stories/joseph)                 sheets: python3 tools/character_sheet.py joseph
===========================================
Same rig and conventions as above (anchor = ground under the pelvis, between the feet; facing; scale; marks; bboxes
(l, t, r, b) at scale 1 / facing 1 measured from renders, wobble included). hand_positions / body_points work for every
function here. Sheets: characters_joseph_poses / _attires / _expr / _brothers / _jacob_pharaoh / _egyptians / _siblings
and characters_joseph_group (groups, hugs, the pit, the chariot, the caravan, scale checks).
SCALE: at the same ``scale`` teen Joseph is ~325 px (head centre (2, -276)), adult Joseph ~339 (ruler 341 with the
headcloth), the brothers 340-350 (staff tops ~-387), Jacob ~325 (staff top -369), Pharaoh ~355, Egyptians 320-345
(a guard's spear -396), Benjamin ~228, the modern big sister ~243 and little brother ~207. One ground line, one scale.
New expressions (JOSEPH_EXPRESSIONS; every function accepts them): proud (happy ^ eyes, big grin, chin up), crying
(eyes squeezed shut, sad brows, open wobbly mouth, two tear streams with drops, a falling drop), tearful (happy tears:
^ eyes, grin, blush and tear streams - the reunion), jealous (narrow sideways glance, frowning brows, pout), ashamed
(downcast eyes, sad brows, blush, wobbly mouth). Also useful: kind, happy, sad, worried, amazed, determined, angry, sly,
scared, cross, puzzled, peaceful. Tears are tears only - nothing in this film is violent.

joseph(x, y, scale=1.0, facing=1, pose='stand', expr=None, attire='shepherd', coat='colours', progress=1.0,
       chain=True, ring=True, item='sack', marks=True)
---------------------------------------------------------------------------------------------------------------
The same face in every attire: round face, rosy cheeks, short dark curls (JOSEPH_HAIR), no beard, skin JOSEPH_SKIN.
attire (JOSEPH_ATTIRES):
  'shepherd'  the teen (~17, slim: metrics 0.96 x an adult). coat (JOSEPH_COATS):
              'colours' the coat of many colours: a long, long-sleeved robe in bold bands, top to hem and along the
                        sleeves, repeating red, yellow, blue, green, purple, orange (COAT_BANDS, 红黄蓝绿紫橙) on a cream
                        base (COAT_BASE). progress 0..1 reveals the colours ONE AT A TIME in that order: colour k fades
                        in over progress k/6 .. (k+1)/6, so key red -> 1/6, yellow -> 2/6, blue -> 3/6, green -> 4/6
                        as the narrator names them (progress 0 = a plain cream robe; quantise to the 7 key values).
              'torn'    the bare cream under-tunic after the coat is pulled off: knee length, short sleeves, rope belt,
                        barefoot, dust smudges and a little rip at the hem (the pit, the caravan).
              None      the clean under-tunic (sandals).
  'slave'     adult (metrics 1.01): sleeveless white linen work tunic, blue cloth belt, barefoot (Potiphar's house).
  'prisoner'  adult: plain grey-brown tunic, rope belt, barefoot, a little dusty.
  'ruler'     vizier of Egypt: long white pleated linen robe with a pale-gold hem, gold sash, broad bead collar
              (gold / lapis / carnelian), a white court headcloth with thin gold stripes and a gold band (lappets in
              front of the shoulders, two dark curls at the temple), gold sandals. chain=True the gold chain with a
              round pendant (Gen 41:42), ring=True the signet ring on the near hand; pass chain=False / ring=False
              for the moment before Pharaoh gives them.
  pose (JOSEPH_POSES)  bbox shepherd (adult attires ~14 px taller)  natural expr (teen / adult)  notes
  stand          (-49, -325, 53, 0)     happy / kind
  walk_a/walk_b  (-84, -324, 78, 1) / (-61, -326, 98, 0)   planted-foot stride frames (alternate ~0.25 s; 'walk' = walk_a)
  run_a/run_b    (-112, -296, 116, 0) / (-90, -290, 133, 0)  happy   (alternate ~0.15 s)
  talk           (-53, -324, 71, 0)     happy     near hand open, palm up
  explain        (-53, -324, 103, 0)    kind      both hands open in front (interpreting the dreams)
  point          (-50, -325, 142, 0)    happy
  point_up       (-64, -324, 85, 0)     determined / kind   finger up to heaven ('能解梦的不是我，是上帝')
  pray           (-62, -324, 50, 0)     peaceful  standing, palms together
  kneel_pray     (-85, -283, 43, 4)     peaceful
  sleep          (-184, -181, 94, 0)    sleepy    curled on his side, head on the LEFT for facing=1, z's
  dream          (-184, -181, 94, 0)    peaceful  the same, smiling in his sleep (put PR.dream_bubble above him)
  call_up        (-72, -325, 68, 0)     call      both arms raised, face up: calling from the bottom of the pit
  hold_rope      (-62, -327, 82, 0)     worried   fists in front of the chest, being pulled up (rope from the far hand)
  sit            (-57, -223, 117, 3)    neutral   on the ground, knees up (the prison floor)
  sad            (-48, -318, 85, 0)     sad       head bowed, arms hanging (led away to Egypt)
  cry            (-48, -322, 77, 0)     crying    a fist at the chin, the other at the chest ('再也忍不住了，大哭起来')
  hug            (-54, -323, 118, 0)    tearful   arms round someone in front (hands (100, -214), (88, -198)): use
                                                  hug_pair(), or draw the other person first at x + 95*scale*facing
  open_arms      (-132, -325, 129, 0)   tearful   arms spread wide, welcoming
  give           (-54, -323, 138, 0)    kind      both hands forward, palms up (giving grain / receiving the ring)
  comfort        (-53, -323, 89, 0)     kind      near hand on the shoulder of someone ~95*scale in front (hand
                                                  (92, -262)); draw that person FIRST ('bless' = this pose for Jacob)
  bow            (-49, -313, 109, 0)    kind      polite standing bow, hand on chest (before Pharaoh)
  ride           ruler (-71, -290, 115, 0)  kind  seated, hands forward on the rail: in the chariot (PR.CHARIOT_SEAT)
  ride_wave      ruler (-68, -342, 77, 0)   kind  standing in the chariot (PR.CHARIOT_STAND), far hand waving, near
                                                  hand on the rail
  carry / carry_walk_a / carry_walk_b  (-128, -324, 54, 0)  determined  item='sack' / 'hay' on the shoulder or
                 'basket' / 'grain' / 'veg' / 'jar' in front (as noah(pose='carry')): the hard-working servant

jacob(x, y, scale=1.0, facing=1, pose='stand', expr=None, staff=True, stool=True, progress=1.0, marks=True)
---------------------------------------------------------------------------------------------------------
Joseph's old father: long wavy white beard, bushy grey brows, smile wrinkles, cream head-cloth with a plum band and a
flap at the back, warm plum robe (JACOB_ROBE) with a gold hem, a cream shawl with blue trim, slightly stooped, a
shepherd's crook (staff=True) in stand / walk / talk / sad / bless. Not Noah (brown robe) or Jesse (rust robe).
  pose (JACOB_POSES)  bbox                 natural expr  notes
  stand          (-54, -369, 100, 2)     kind
  walk_a/walk_b  (-86, -365, 103, 2) / (-61, -370, 108, 2)  kind   (going down to Egypt)
  talk           (-54, -369, 123, 2)     happy     far hand open
  sad            (-50, -360, 106, 2)     sad
  bless          (-57, -369, 125, 2)     kind      far hand raised, palm out
  sit            (-70, -274, 110, 4)     kind      on a low wooden three-legged stool (stool=False: no stool)
  give           (-61, -323, 178, 0)     happy     holding the new coat up by its shoulders to show it (coat top centre
                                                   between the hands, ~0.64 x coat_of_colours); progress 0..1 reveals its
                                                   bands exactly like joseph(progress=...)
  cry            (-39, -216, 119, 3)     crying    sitting on the ground holding the torn, dirty coat against him
                                                   (Gen 37:34-35: tears only)
  hug            (-57, -322, 118, 0)     tearful   see hug_pair (Jacob meets Joseph in Egypt, 46:29)
  open_arms      (-136, -325, 133, 0)    tearful

brothers(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, staff=None, item='sack', marks=True)
(brother() is the same function)
---------------------------------------------------------------------------------------------------------
Joseph's brothers. variant 0-9: the ten older brothers (BROTHER_NAMES Reuben, Simeon, Levi, Judah, Dan, Naphtali, Gad,
Asher, Issachar, Zebulun): bearded shepherds in knee-to-calf robes with a rope belt, each a different robe colour and
head-dress: 0 olive green, cream head-cloth, full dark beard (Reuben); 1 brick red, ochre wrap, short black beard;
2 slate blue, red headband, stubble; 3 mustard, cream head-cloth, full brown beard, brown shawl (Judah); 4 brown, teal
wrap, pointed beard; 5 teal-grey, ochre headband; 6 dusty lilac, head-cloth, full beard; 7 terracotta, cream wrap,
deep skin; 8 moss green, ochre headband; 9 rose-brown, bare curly head (the youngest of the ten). Slightly different
heights / widths. variant='benjamin': Joseph's little full brother, a small boy (child rig, ~228 px) with Joseph's
curls and skin in a sky-blue knee tunic (BENJAMIN_TUNIC). staff=None: a crook in the near hand for stand / walk_a /
walk_b / talk (False: none; never for Benjamin).
  pose (BROTHER_POSES)  bbox (union of 0-9)   natural expr   notes
  stand          (-69, -387, 100, 2)     neutral  (with staff; -345 without)
  walk_a/walk_b  (-90, -387, 106, 2) / (-64, -388, 106, 2)  neutral
  run_a/run_b    (-120, -314, 125, 0) / (-94, -308, 145, 0)  worried
  talk           (-69, -387, 116, 2)     neutral  far hand open (pass 'jealous' / 'angry': '凭什么只给他做？')
  point          (-69, -346, 154, 0)     angry    ('看，那个做梦的来了！')
  cross_arms     (-70, -345, 64, 0)      jealous  arms folded
  whisper        (-53, -344, 90, 0)      sly      hand by the mouth (two brothers face to face ~110*scale apart)
  pull           (-114, -315, 104, 0)    determined  leaning back on a rope through the fists (81, -166), (37, -151)
                                                  (as sailor 'pull'): pulling Joseph up out of the pit
  bow            (-89, -218, 191, 5)     worried  kneeling, bent low, hands flat on the ground in front, head bowed:
                                                  bowing before Joseph (42:6) - the sheaves dream come true
  kneel_pray     (-92, -301, 48, 5)      peaceful
  hug            (-60, -344, 120, 0)     tearful  (hug_pair with Joseph)
  sad            (-55, -340, 91, 0)      ashamed  head bowed (showing Jacob the coat; frightened of Joseph)
  scared         (-98, -347, 85, 0)      scared   hands up by the face ('哥哥们吓坏了')
  cheer          (-101, -345, 106, 0)    happy
  carry / carry_walk_a / carry_walk_b   (-130, -345, 59, 0)  neutral  grain sacks on the shoulder (item as joseph)
  Benjamin: stand (-45, -228, 43, 0), walk (-57, -230, 57, 0), the other poses scaled to the child rig.

brothers_group(x, y, scale=1.0, facing=1, pose='stand', n=10, expr=None, gap=150, exprs=None, marks=True)
---------------------------------------------------------------------------------------------------------
The ten older brothers at once (drawn back to front in one <g>). expr applies to all; exprs (a list) cycles per brother.
  group     stand / talk / cross_arms / point / sad / scared / hug / cheer / whisper: two rows centred on x - back row
            (34 px higher, 0.96 x) variants 4, 8, 1, 5, 9 at -330 .. +330, front row 6, 2, 0, 3, 7 at -410 .. +245;
            the left half faces right, the right half left (whisper: the right-facing ones whisper, the others fold
            their arms). bbox cross_arms (-478, -366, 380, 0) at scale 1.
  kneeling  bow / kneel_pray: two staggered rows, everybody facing ``facing`` (toward Joseph): front row at x-460,
            -230, 0, +230, +460, back row (40 px higher) halfway between; bbox bow (-545, -242, 755, 5).
  line      walk_a / walk_b / run_a / run_b / carry_walk_a / carry_walk_b: a line toward facing, variant 0 leading AT x,
            the others every gap*scale behind, neighbours in opposite frames (the journey to Egypt with grain sacks);
            bbox walk_a about (-1440, -388, 103, 2) at gap 150.
  n < 10 draws the first n of them.

pharaoh(x, y, scale=1.0, facing=1, pose='stand', expr=None, throne=True, marks=True)
---------------------------------------------------------------------------------
The king of Egypt, friendly: a gold-and-lapis striped nemes headdress with lappets and a little gold cobra at the brow,
kohl-lined eyes, a narrow plaited false beard under the chin (the mouth stays free), bare chest with a broad bead collar
(gold / lapis / carnelian), gold armbands and bracelets, a long white pleated linen kilt-robe with a gold belt and a
gold front apron, gold sandals. Skin PHARAOH_SKIN.
  pose (PHARAOH_POSES)  bbox            natural expr   notes
  stand          (-70, -355, 61, 0)     neutral
  walk_a/walk_b  (-94, -354, 88, 1) / (-70, -357, 111, 0)  neutral
  talk           (-70, -355, 74, 0)     happy      (pass 'kind': '上帝和你同在...')
  sit_throne     (-89, -324, 167, 0)    neutral    on his gilded Egyptian throne (throne=True draws it behind him;
                                                   throne=False: (-73, -301, 120, 0), use props.egypt_throne at the same
                                                   x, y, scale, facing: seat top EGYPT_SEAT_Y = -73)
  sleep          (-202, -202, 98, 7)    sleepy     lying on his side, z's (dreaming: add PR.dream_bubble; or put him on
                                                   props.couch)
  point          (-70, -355, 160, 0)    neutral
  give_ring      (-63, -354, 97, 0)     kind       arm forward, the signet ring held up in the fingers (~(84, -230))
  amazed         (-128, -356, 127, 0)   amazed     hands open, raised a little
  worried        (-74, -358, 58, 0)     worried    hands on his head (nobody can explain the dream)

egyptian(x, y, scale=1.0, facing=1, kind='servant', variant=0, pose='stand', expr=None, prisoner=False, spear=None,
         item='sack', marks=True)
---------------------------------------------------------------------------------------------------------------
Egyptians, all with kohl-lined eyes; variant 0-3 varies skin (EGYPT_SKIN) and belt / band colours. kind (EGYPTIAN_KINDS):
  'servant'    black bob hair, bare chest, short white pleated linen kilt, coloured belt, barefoot
  'guard'      white-and-blue striped khat headcloth, bare chest with a leather cross-strap, kilt with a striped apron,
               sandals, a spear (spear=None: in stand / walk; True / False to force)
  'wise'       wise men / magicians: shaven heads, long robes (0 deep blue with gold dots, 1 brown with diamonds and a white
               pointed beard, 2 green with flowers), gold sash and collar; variant 0 holds a scroll when standing
  'potiphar'   the rich master, plump and smiling: shoulder-length black wig, long white pleated robe with a red sash and
               hem, a big bead collar, gold sandals; pose 'give' holds out a ring of big keys (trusting Joseph)
  'woman'      long black wig with a coloured headband, long white sheath dress, bead collar, sash
  'cupbearer'  bob hair, gold collar, knee kilt; holds a gold cup in 'stand' and 'give' (Gen 40)
  'baker'      plump, shaven head, kilt with a white baker's apron
prisoner=True (cupbearer / baker / servant): a plain dusty prison tunic, rope belt, barefoot; the cupbearer with stubble,
the baker bald and round (they look puzzled about their dreams: pose 'shrug' or expr 'worried' / 'puzzled').
  pose (EGYPTIAN_POSES)  bbox servant (others similar; Potiphar ~10 px wider)   natural expr   notes
  stand          (-56, -337, 56, 0)    neutral (Potiphar happy)    guard (-64, -396, 75, 0) with the spear
  walk_a/walk_b  (-80, -333, 76, 0) / (-64, -335, 105, 0)
  bow            (-84, -209, 189, 0)   peaceful   kneeling, bent low, hands on the ground (people bow as Joseph's
                                                  chariot passes, 41:43)
  shrug          (-111, -367, 108, 0)  puzzled    palms up, a '?' (marks=False hides it): the wise men cannot explain
  lead / lead_b  (-88, -333, 124, 0)   neutral    walking (frames a / b), near hand back at hip height holding the person
                                                  / rope behind; a guard carries the spear in the far hand behind him
  carry / carry_walk_a / carry_walk_b  (-129, -337, 57, 0)  item 'sack' (grain) etc.
  give           (-50, -336, 146, 0)   happy (Potiphar)   arm forward (keys for Potiphar, the cup for the cupbearer)
  talk, point, sit (-63, -234, 114, 0), sad, cheer, amazed, worried, kneel_bow (= bow)

trader(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, marks=True)
--------------------------------------------------------------------------------
Ishmaelite spice traders of the caravan (Gen 37:25-28): long robes with bold horizontal stripes, a red sash, a desert
head-cloth held by a dark double cord, full beard. variant 0 sand / brown stripes, 1 sage / cream with a red
head-cloth, 2 rust / yellow. TRADER_POSES: stand (-69, -333, 59, 0) happy, walk_a / walk_b, talk, point, lead / lead_b
(-89, -332, 124, 1) walking with the near hand back holding the camel's lead rope (put the hand near props.CAMEL_LEAD),
give (-62, -333, 96, 0) holding out three silver coins, count (-69, -332, 81, 0) an open money pouch in both hands.

hug_pair(x, y, scale=1.0, facing=1, a=None, b=None, gap=95)
-----------------------------------------------------------
Two people hugging: a = (fn, kwargs) stands at x facing ``facing``, b = (fn, kwargs) stands gap*scale in front of him
facing back; both get pose='hug' unless their kwargs say otherwise; b is drawn first, then a, whose arms come round b.
Default: Joseph (ruler, tearful) and Jacob (tearful). E.g. hug_pair(x, y, s, a=(joseph, dict(attire='ruler')),
b=(brothers, dict(variant=3, expr='crying'))) or the siblings: a=(child, dict(sibling='big')), b=(child,
dict(sibling='little')), gap=70. bbox default (-58, -341, 151, 0); the siblings at gap 70 (-54, -245, 100, 0).

child(..., sibling=None, toy=None)  - the modern siblings (opening squabble and ending)
-------------------------------------------------------------------------------------
child() keeps its raincoat look and output by default; new options:
  sibling='big'     the big sister (~7, 243 px): coral dress with a cream collar and a pocket, brown hair in a ponytail
                    with a yellow ribbon and a side fringe, red shoes
  sibling='little'  the little brother (~4, 207 px): blue t-shirt with yellow stripes, navy shorts, light sneakers,
                    curly light-brown hair
  toy='horse' / 'ball'  the shared toy (props.toy) held: in 'share' in both hands in front, in 'tug' gripped and reaching
                    out in front, in stand / walk / sulk hanging from the near hand.
  New poses (SIBLING_POSES; they work for the raincoat child too). bbox big / little:
  tug       (-99, -224, 79, 0) / (-67, -195, 71, 0)   cross    leaning back, both fists forward at hip height (a tug of
            war over the toy: give one child toy='horse' and put the other, facing back, ~150*scale away)
  sulk      (-59, -244, 56, 0) / (-50, -205, 31, 0)   cross    arms folded, body and head turned AWAY from facing
  sorry     (-52, -244, 63, 0) / (-37, -204, 54, 0)   sorry    head bowed, hands behind the back
  hug       (-54, -245, 75, 0) / (-31, -207, 78, 0)   happy    arms round someone in front (~70*scale away)
  share     (-54, -246, 59, 0) / (-30, -206, 53, 0)   kind     holding the toy out in both hands
  Every expression works (cross, crying, sorry, kind, happy, laugh ...).

Constants (Joseph film): JOSEPH_POSES, JOSEPH_ATTIRES, JOSEPH_COATS, JOSEPH_EXPRESSIONS, JACOB_POSES, BROTHER_POSES,
BROTHER_NAMES, BROTHERS_GROUP_POSES, PHARAOH_POSES, EGYPTIAN_KINDS, EGYPTIAN_POSES, TRADER_POSES, SIBLINGS,
SIBLING_POSES; colours JOSEPH_SKIN, JOSEPH_HAIR, COAT_BANDS, COAT_BASE, TUNIC, LINEN, EGYPT_SKIN, EGYPT_HAIR, LAPIS,
CARNELIAN, JACOB_ROBE, PHARAOH_SKIN, BENJAMIN_TUNIC, SIB_DRESS, SIB_SHIRT, SIB_SHORTS. God is never drawn as a person:
show his presence as soft golden light (engine.fx / art.style), never as a figure.

STORM FILM (Mark 4:35-41, stories/storm)                     sheets: python3 tools/character_sheet.py storm
========================================
Same rig and conventions as above (anchor = ground under the pelvis, between the feet; facing; scale; marks; bboxes
(l, t, r, b) at scale 1 / facing 1 measured from renders, wobble included). hand_positions / body_points work for every
function here. Sheets: characters_storm_jesus / _expr / _disciples / _disciple_poses / _villagers / _child and
characters_storm_group (Jesus with the twelve, crowds, the crew in the fishing boat, the child's room). New designs only:
nothing here reuses the Jonah film's sailors; the boat, lake and sky are in art/props.py section 11.
SCALE: at the same ``scale`` Jesus is ~342 px (head centre (2, -287)), the disciples 327-350 (John, the youngest, 327;
Peter sturdy and broad; James the tallest, 350), villagers like the other films' adults (men ~337, women ~317, elders
~327, children ~224), the pyjama girl ~225. The fishing boat (props.fishing_boat) is BOAT_LEN = 1500 px at scale 1
(about 4.5 adults): draw boat and people at the SAME scale (0.35-0.6 in most shots) - 13 people fit in two rows.
New expressions (STORM_EXPRESSIONS; every function accepts them): warm (soft smile, warm blush - Jesus' default),
smile (^ eyes, smile, blush), calm (soft downcast eyes, serene smile - just woken, unafraid), gentle_question (raised
soft brows, small open mouth, blush - '你们为什么这样害怕呢？'), command (level calm brows, speaking mouth - '住了吧！静了吧！',
authoritative, never angry), panicked (wide frightened eyes, open shouting mouth, sweat drops, tremble marks), awed
(big eyes looking up, small 'o', raised brows - reverent wonder). Also useful: kind, happy, sleepy, peaceful, scared,
amazed, ashamed, tired, worried, shout.

jesus(x, y, scale=1.0, facing=1, pose='stand', expr=None, glow=0.0, cushion=True, wind=0.0, phase=0.0, mantle=True,
      marks=True)
-------------------------------------------------------------------------------------------------------------------
A kind, calm man of about thirty, drawn with respect (never comic, no halo): warm brown skin (JESUS_SKIN), dark
shoulder-length hair with a soft side part (JESUS_HAIR), a short neat beard and moustache (the mouth always shows), a
long cream robe (JESUS_ROBE) with a sand hem band and cuffs, a muted gold cloth belt with a knot, brown sandals, and a
warm red mantle (JESUS_MANTLE) crossing the chest from the far shoulder and falling down his back.
  glow 0..1   a very soft warm light round the whole figure (calm presence in the storm; a wide gradient, never a ring).
              Adds up to ~(-160, -410, 180, 30) to the bbox at 1 - quantise (0, .3, .6, 1).
  wind 0..1   the back of the mantle streams out behind (away from facing): stand_command in the wind (bbox left -137).
  mantle      False: robe only.   cushion  sleep / wake: the stern cushion (props.boat_cushion) under the head.
  pose (JESUS_POSES)  bbox                  natural expr     notes (hands [far, near] at scale 1)
  stand          (-71, -342, 56, 0)      warm
  walk_a/walk_b  (-90, -342, 84, 1) / (-67, -343, 98, 0)   warm   planted-foot stride frames (alternate ~0.25 s)
  sit            (-74, -290, 116, 0)     warm      seated on a bench / the stern platform edge: the anchor is the FLOOR
                                                   under his feet, the seat ~70 px above it (no seat is drawn: use
                                                   props.STERN_SEAT, or your own bench / rock)
  teach          (-74, -290, 116, 0)     smile     seated, near hand open in front (58, -172): telling the crowd
  teach_stand    (-71, -342, 73, 0)      smile     standing, near hand open, palm up
  sleep          (-237, -192, 96, 3)     sleepy    lying on his side, HEAD ON THE LEFT for facing=1, cheek on the cushion
                                                   (centre JESUS_CUSHION_DX = -150 from the anchor), the mantle over his
                                                   legs like a blanket, soft z's (marks=False: top -127; cushion=False:
                                                   left -197). Head (-142, -78). In the boat: anchor at props.STERN_SLEEP
  wake           (-237, -190, 129, 5)    calm      rising up on one elbow (far palm on the floor), head lifted (-99, -134),
                                                   the same cushion, blanket and anchor as sleep (cut sleep -> wake)
  stand_command  (-82, -343, 104, 0)     command   standing firm, far arm raised toward the wind and the waves, palm out
                                                   (93, -299): '住了吧！静了吧！' (combine with wind=1 -> 0 and glow)
  turn_kind      (-68, -341, 114, 0)     gentle_question  turned toward the disciples, both hands open, palms up
                                                   (97, -160), (55, -176), head tilted
  bless          (-71, -342, 71, 0)      warm      near hand raised, palm out (60, -256)
  wave           (-71, -342, 110, 0)     smile     far hand up (67, -320); phase 0..1 swings the forearm (+-16 deg)
  point          (-71, -342, 101, 0)     warm      near arm pointing forward (77, -241): 'let us go across to the other side'
  pray           (-71, -342, 55, 0)      peaceful  standing, palms together
  JESUS_EXPRESSIONS lists the suitable ones (warm, kind, smile, calm, sleepy, gentle_question, command, peaceful, happy).

disciples(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, phase=0.0, shake=0.0, item='bucket', wind=0.0,
          wet=False, oar=True, net=True, marks=True)      (disciple() is the same function)
----------------------------------------------------------------------------------------------------------------------
The twelve, as fishermen and working men: knee-length tunics with two woven stripes above the hem, short ROLLED
sleeves (a rolled band shows), a knotted cloth belt in a contrasting colour, BARE FEET, sun-browned skin; most wear a
fisherman's kerchief knotted at the back of the head (two short tails that stream in the wind). variant 0-11
(DISCIPLE_NAMES) or a name for the four fishermen (DISCIPLE_LOOKS):
  0 'peter'   sturdy and broad (metrics 1.03 x 1.18), curly hair and a full CURLY beard streaked with grey, slate-teal
              tunic with gold stripes, rust-red kerchief and belt                             head (2, -289)
  1 'andrew'  Peter's brother (same skin and hair), a short square beard, honey-sand tunic, teal kerchief    (2, -280)
  2 'james'   the tallest (350 px), full black beard, wine tunic, cream kerchief, gold belt                  (2, -294)
  3 'john'    the youngest: beardless, light-brown curls, a thin ochre headband with tails, sage tunic        (2, -272)
  4-11        Philip (dusty rose, wrap cap), Bartholomew (dusty blue, full brown beard, headband), Matthew (lilac
              with gold stripes, trim beard, cream kerchief), Thomas (olive, stubble, deep-brown skin, bare curly head),
              James son of Alphaeus (sand with brown stripes, pointed beard, teal wrap), Thaddaeus (rust-brown,
              headband), Simon (slate grey, full black beard, sage kerchief), Judas (mustard, maroon wrap)
  stand bboxes: union (-67, -350, 62, 0); John (-59, -327, 52, 0).
  wet=True    darker tunic and kerchief, soaked patches and water drops (the storm and just after it).
  wind 0..1   the kerchief tails stream back.
  pose (DISCIPLE_POSES)  bbox (union)         natural expr  notes (hands [far, near] at scale 1)
  stand          (-67, -350, 62, 0)       happy
  walk_a/walk_b  (-85, -346, 80, 0) / (-71, -348, 109, 0)   happy   planted-foot stride frames
  sit            (-72, -296, 113, -1)     happy     on a bench / thwart: anchor = floor under his feet, seat ~70 px up
  row            (-130, -302, 127, 59)    happy     seated rowing with an oar: phase 0..1 = the stroke (0 catch: leaning
                                                    forward, hands out (86, -158); .25 drive, blade deep; .5 finish:
                                                    leaning back, hands at the chest; .75 recovery, blade lifted). The oar
                                                    runs from the hands through the oarlock props.ROW_PIVOT = (40, -118)
                                                    (anchor coords) to the blade below the anchor line (bottom 59 = the
                                                    blade in the water). Rowers face the STERN: in props.fishing_boat(facing
                                                    =f) sit them at boat_points()['seats'] with facing=-f and give the boat
                                                    oars='out', row=<the same phase>. 6-8 phases at ~0.12 s per stroke.
                                                    oar=False: hands only.
  pull_rope      (-106, -514, 175, 1)     worried   leaning back, hauling the sail rope hand over hand: fists (70, -299),
                                                    (43, -240); the rope runs up-forward 230 px past the top fist (to the
                                                    yard: boat_points()['yard']) with a slack tail below
  bail           (-71, -346, 237, 2)      worried   bailing with a bucket (item='bucket') or a clay bowl ('bowl'): phase 0
                                                    scoop (bent low, hands (99, -66)), .35 lift (full, at the chest), .65
                                                    throw over the side (arms up and forward, the vessel tipped, a water arc
                                                    with drops flying out toward facing), 1 = 0. Face him toward the
                                                    nearer gunwale. 6-8 phases at ~0.1 s.
  cling          (-40, -322, 109, 1)      scared    knees bent, leaning in, both fists gripping a mast / post in front at
                                                    (82, -267) and (85, -209): stand at boat_points()['cling'] facing the
                                                    mast (props.BOAT_CLING). shake 0..1 jitters him and adds knee tremble
  scared         (-101, -351, 89, 0)      scared    arms up by the face; shake 0..1 jitters (+-3.5 px, cycle 0 .25 .5 .75)
  shout          (-58, -350, 140, -1)     shout     one hand at the mouth, the other arm flung forward: '抓紧！'
  wake_shake     (-42, -332, 162, 1)      panicked  leaning forward, both hands on the shoulder of someone lying on a raised
                                                    platform at chest height: hands (124, -251), (102, -233), shake arcs.
                                                    In the boat: boat_points()['wake'] facing -f puts the hands on Jesus
                                                    asleep at STERN_SLEEP ('老师！老师！'). phase 0..1 jitters the body
                                                    (+-3.5 px): cycle 0, .25, .5, .75 for the shaking
  wake_shake_low (-40, -277, 187, 1)      panicked  crouching, hands low (155, -80), (107, -109): someone asleep on the same
                                                    floor (as captain 'wake')
  wonder         (-128, -350, 127, -1)    amazed    both hands open and lifted a little, head up ('这到底是谁？')
  whisper        (-53, -349, 91, -1)      awed      leaning in, hand by the mouth (pairs face to face ~110*scale apart)
  kneel          (-90, -308, 55, 0)       awed      kneeling, palms together, face lifted
  wave           (-70, -350, 127, 0)      happy     far hand up, phase swings it
  point          (-67, -350, 106, 0)      happy
  push           (-70, -305, 180, 2)      happy     leaning in, both palms forward (173, -171), (118, -190): pushing the boat
                                                    off the beach (put the hull ~170*scale in front)
  cast_net       (-175, -348, 220, -1)    happy     throwing a round cast net: phase 0 the gathered net swung back by the
                                                    legs, .5 swinging forward at the hip, .85-1 released - the net flies open
                                                    ahead (umbrella of mesh with lead weights, ~260 px ahead at 1) on a line
                                                    from the near hand (props.fishing_net(kind='cast') for the net alone)
  haul_net       (-108, -326, 275, 43)    laugh     leaning back hauling a heavy net full of flapping fish hand over hand:
                                                    two lines from the fists to the net bag (centre ~(210, -10)); phase
                                                    0..1 alternates the hands and flaps the fish (in a boat the bag hangs
                                                    over the gunwale: the hull covers its lower half)
DISCIPLE_EXPRESSIONS: happy, tired, scared, panicked, amazed, ashamed, awed, worried, shout, determined, kind.

disciples_group(x, y, scale=1.0, facing=1, pose='stand', n=12, expr=None, gap=150, exprs=None, poses=None, phase=0.0,
                marks=True)
-------------------------------------------------------------------------------------------------------------------
Several of the twelve at once (DISCIPLES_GROUP_POSES: stand, wonder, whisper, scared, kneel, wave, walk_a, walk_b, point,
shout, sit). group: two rows centred on x (back row 34 px higher, 0.96 x: Bartholomew, Thaddaeus, James son of Alphaeus,
Simon, Judas, Philip; front row Matthew, Thomas, Andrew, Peter (at x), James, John), the left half facing right, the right
half left; whisper pairs whisperers with wonderers; poses (a list, cycled by variant) overrides pose per person; exprs
likewise. line: walk_a / walk_b = a line walking toward facing, Peter leading AT x, the others every gap*scale behind,
neighbours in opposite frames (Jesus walking with his friends: jesus(x + 60*scale, ...) in front). bbox group stand at
scale 0.5: (-272, -182, 264, 0).

villager(x, y, scale=1.0, facing=1, kind='man', variant=0, pose='stand', expr=None, phase=0.0, rider=None, marks=True)
--------------------------------------------------------------------------------------------------------------------
The Galilean lakeshore crowd (VILLAGER_KINDS): 'man' (long robe with two hem stripes, cloth belt with tails, beard
varies, a head-cloth with a flap for variants 0, 1, 3, 4), 'woman' (long robe, soft veil), 'child' (knee tunic, rope
belt; even variants boys with curls, odd variants girls with a ponytail and ribbon), 'elder' (white hair and beard,
shawl, stooped with a stick when standing / walking; odd variants a wrapped cap). variant 0-5 (mod 6): plum, teal, sand-gold,
olive, brick, indigo robes with contrasting stripes and veils; skins from light to deep brown. Not the Nineveh citizens.
  pose (VILLAGER_POSES)   man                    woman                  child                 elder
  stand          (-69, -337, 60, 0)     (-53, -317, 52, 0)     (-54, -224, 43, 0)    (-50, -327, 70, 3)   happy
  walk_a/walk_b  (-90, -337, 84, 1) / (-68, -339, 104, 0) ...  walking home: alternate every ~0.25 s; happy
  listen         (-68, -337, 55, 0)     hand at the chin, head up toward the speaker; kind
  sit            (-74, -231, 120, 3)    on the ground, knees up, hands on the knees; happy
  sit_listen     (-61, -232, 118, 2)    sitting, chin on the hand, looking up (children at the front); kind
  kneel          (-92, -295, 51, 5)     kneeling, palms together; kind
  wave           (-69, -339, 109, 0)    far hand up, phase swings it (waving goodbye as the boat leaves); happy
  cheer / point / nod   arms up / pointing / head bowed 22 deg (alternate with stand to nod)
  carry, carry_walk_a/_b  (-65, -337, 87, 0)  a basket of fruit in both hands (going home at sunset)
  shoulders      (-66, -401, 58, 0)     kind='man' only: a little child (rider = its variant, default variant+1) rides
                                         on his shoulders - its laughing face and waving arm rise behind and above his
                                         head; his back arm is raised holding it (his face stays clear)
villager_crowd(x, y, scale=1.0, facing=1, n=12, pose='stand', width=900, rows=3, seed=0, poses=None, expr=None,
               phase=0.0, marks=True)
  A mixed crowd of n villagers in up to `rows` rows centred on x, spread over width*scale; each row behind is 46*scale
  higher and 6% smaller (drawn first); children go to the front; walk poses alternate frames; listen / sit_listen / sit
  / kneel / nod / walk face `facing`, other poses face the middle; with n >= 8 a father in the back row carries a child
  (pose stand / listen / wave / cheer). VILLAGER_CROWD_POSES.

child(..., outfit=None, pillow=True)  - the girl at home at night (opening and ending)
-------------------------------------------------------------------------------------
child() keeps every earlier look and output by default. outfit='pyjamas' (CHILD_OUTFITS): a little girl (~5, 225 px) in
periwinkle pyjamas with yellow stars (top and trousers, CHILD's rig), dark hair in a bob with a bun and a yellow bobble,
bare feet. All CHILD_POSES / SIBLING_POSES work in pyjamas, plus STORM_CHILD_POSES (they work for every outfit /
sibling too):
  hug_pillow  (-44, -225, 67, 0)   worried   standing, hugging her star pillow (props.pillow) to her chest
                                             (pillow=False: arms only); pass expr='scared' for the rattling window
  sit_hug     (-45, -165, 85, 3)   worried   sitting (knees up) hugging the pillow - on the floor, or on the bed:
                                             child(x, y + props.BED_TOP*scale, ...) on props.bed(x', y, scale)
  pray        (-57, -225, 39, 0)   peaceful  standing, hands folded, eyes closed
  kneel_pray  (-68, -202, 38, 0)   peaceful  kneeling by the bed
  sit_pray    (-59, -167, 88, 3)   peaceful  sitting, hands folded (on the bed)
  (also smile_up / happy / kind for the warm calm ending, peek_window at props.window_wind)

Constants (Storm film): JESUS_POSES, JESUS_EXPRESSIONS, JESUS_CUSHION_DX, DISCIPLE_NAMES, DISCIPLE_LOOKS, DISCIPLE_POSES,
DISCIPLE_EXPRESSIONS, DISCIPLES_GROUP_POSES, BAIL_ITEMS, VILLAGER_KINDS, VILLAGER_POSES, VILLAGER_CROWD_POSES,
STORM_CHILD_POSES, CHILD_OUTFITS, STORM_EXPRESSIONS; colours JESUS_SKIN, JESUS_HAIR, JESUS_ROBE, JESUS_TRIM,
JESUS_MANTLE, JESUS_SASH, PYJAMA, PYJAMA_STAR. Boat geometry (seats, stern platform, oarlocks) lives in art/props.py
section 11 (fishing_boat, boat_points, ROW_PIVOT, row_hands).

NATIVITY FILM (Luke 1-2, Matthew 2, stories/nativity)        sheets: python3 tools/character_sheet.py nativity
=====================================================
Same rig and conventions as above (anchor = ground under the pelvis, between the feet; facing; scale; marks; bboxes
(l, t, r, b) at scale 1 / facing 1 measured from renders, wobble included). hand_positions / body_points work for every
function here. Sheets: characters_nativity_mary / _expr / _joseph / _baby / _angel / _shepherds / _magi / _townsfolk /
_child and characters_nativity_group (the scale line-up, the journey, the stable, the shepherds with the glory and the
choir, the wise men's visit). New designs only, with this film's palette (starry-night blues, warm lamplight, the gold of
the star): nothing reuses the Jesus of the Storm film, the Joseph of the Joseph film or any earlier main cast. The stable,
manger, animals, places and skies are in art/props.py section 12.
SCALE: at the same ``scale`` Mary is ~314 px (head centre (2, -263)), Joseph ~355 with his staff (head (2, -285)), the
angels ~375 + wings (head (2, -316): tall, gentle figures of light), the shepherds 330-345 (crooks to -387; the boy ~240,
head (2, -186)), the wise men ~345 + crowns / turbans (to -390), townsfolk like the other films' adults (men ~338, women
~317, children ~224), the jumper boy ~229 (head (2, -179)), toddler_jesus ~165 (head (2, -122)), baby_jesus a bundle
~143 x 69. Animals at the same scale: props.donkey back ~-190 (Mary's seat DONKEY_SEAT), props.ox ~290 tall, props.camel
riding seat CAMEL_SEAT ~-336. One ground line, one scale.
New expressions (NATIVITY_EXPRESSIONS; every function accepts them): startled (big eyes, raised brows, small open mouth,
blush - gentle, never fear), tender (eyes looking down, soft smile, blush - at the baby), joyful (^ eyes, open smile,
blush), weary (droopy lids, a soft smile, no sweat drops), sing (^ eyes, open 'ah' mouth - the angels), proclaim (earnest
open mouth, blush - the angel speaking kindly), hush (closed eyes, small 'o'), question (one brow raised, small open
mouth - 'how can this be?'), thoughtful (eyes down to the side, soft smile - Mary keeps these things in her heart). In
this film's functions expr='tired' draws 'weary'. Also useful: kind, calm, awed, amazed, happy, peaceful, sleepy, scared,
surprised, sorry, worried, laugh.

mary(x, y, scale=1.0, facing=1, pose='stand', expr=None, phase=0.0, baby=True, glow=0.0, pregnant=False, marks=True)
-------------------------------------------------------------------------------------------------------------------
Mary of Nazareth, a kind young woman of about 16-18: olive skin (MARY_SKIN), dark hair (MARY_HAIR) showing as a soft
centre-parted fringe and a lock in front of the ear under a soft blue head-veil (MARY_VEIL) with a light-blue edge that
falls down her back, tiny lashes, a simple warm-cream dress (MARY_DRESS) with a thin gold-ochre hem, cuffs and neckline
(MARY_TRIM), a blue sash (MARY_BLUE), sandals.
  pregnant=True  visibly expecting (Luke 2:5, '马利亚的肚子已经大大的了'): a round, gentle belly under the dress that clearly
                 stands out past her front line (~25 px at scale 1, still readable at scale 0.45), an empire sash above it;
                 works in every pose (walk / ride / sit / stand / question / startled on the journey, in the street and at
                 the inn). In sit and ride her near hand rests on top of the belly (the far hand on the knee). stand bbox
                 (-52, -314, 51, 0); the other bboxes are unchanged.
  glow 0..1      a very soft warm light round her (no halo ring).   baby  False hides the baby / toddler in the poses
                 that hold one.   phase  sweep / walk cycles.
  pose (MARY_POSES)  bbox (l, t, r, b)       natural expr  notes (hands [far, near] at scale 1)
  stand          (-52, -314, 49, 0)       kind
  walk_a/_b/_c   (-78, -315, 74, 0) / (-58, -316, 80, 0) / (-61, -318, 53, 0)   kind   planted-foot stride frames and the
                                                     passing frame; pose='walk' + phase 0..1 cycles a, c, b, c (flip every
                                                     ~0.2 s while moving x)
  sweep          (-62, -310, 193, 0)      kind       sweeping with a palm-fibre broom; phase 0..1 swings the broom head
                                                     forward and back along the floor (4-6 phases, little dust puffs when
                                                     marks)
  carry_jar      (-83, -314, 51, 0)       kind       a tall clay water jar on the back shoulder, steadied by the raised near
                                                     hand; carry_jar_walk_a / _b the same while walking (-80, -316, 80, 0)
  startled       (-71, -315, 100, 0)      startled   a step back, hand to the chest, the other hand lifted ('马利亚吓了一跳')
  question       (-62, -315, 101, 0)      question   hand on the chest, the other open, palm up, head tilted ('可是，我还没有
                                                     结婚呀…')
  bow            (-47, -309, 86, 0)       calm       head bowed, hands folded: her 'yes' ('我愿意')
  pray           (-59, -314, 49, 0)       peaceful   standing, hands folded, face lifted
  kneel          (-83, -276, 52, 4)       tender     kneeling, hands folded, looking down (by the manger)
  kneel_up       (-83, -273, 39, 4)       awed       kneeling, face lifted
  smile_down     (-47, -311, 66, 0)       tender     standing, hands folded low, smiling down at the baby
  listen_think   (-47, -312, 68, 0)       thoughtful near hand on the heart, head tilted (Luke 2:19)
  hold_baby      (-49, -311, 80, 0)       tender     cradling the swaddled baby across her chest (its head in the crook of her
                                                     near arm); hands (65, -164), (13, -151)
  lay_baby       (-51, -277, 170, 2)      tender     bending forward, laying the baby down: the baby's underside is at
                                                     (MARY_LAY_DX, MARY_LAY_Y) = (112, -112): put props.manger at
                                                     (x + 112*scale*facing, y + 12*scale) so its bed (MANGER_BED) is there
                 Seated poses: the anchor is the FLOOR under her feet, the seat is ~64 px above it (props.FAMILY_SEAT bench,
                 a step, or props.hay(kind='bale', scale=0.58)):
  sit            (-56, -266, 104, 0)      kind       hands in her lap
  sit_baby       (-45, -263, 104, 0)      tender     seated, cradling the baby
  wrap           (-36, -258, 117, 0)      tender     seated with the baby on her lap, wrapping a long cloth band round him
  sit_think      (-42, -264, 104, 0)      thoughtful seated, hand on the heart
  sit_hold       (-51, -266, 104, 0)      kind       seated with toddler_jesus on her lap, her near arm round him
                                                     (Matthew 2:11)
  ride           (-58, -202, 92, 89)      kind       seated side-saddle: the anchor is the SEAT (the donkey's back), the legs
                                                     hang below it: mary(*props.donkey_points(dx, dy, s, pose=...)['seat'], s,
                                                     f, pose='ride', pregnant=True) on donkey(dx, dy, s, f, saddle='blue')
  ride_baby      (-54, -201, 92, 89)      tender     the same, holding the baby
MARY_EXPRESSIONS lists the suitable ones (kind, startled, calm, tender, tired, joyful, awed, question, thoughtful, ...).

joseph_carpenter(x, y, scale=1.0, facing=1, pose='stand', expr=None, phase=0.0, staff=True, lamp=1.0, marks=True)
---------------------------------------------------------------------------------------------------------------
Joseph of Nazareth, Mary's husband: a gentle carpenter in his twenties, short dark wavy hair with a thin woven rust
headband, a short close-cropped dark beard (beard kind 'carpenter'), an ochre tunic (JOSEPH_C_TUNIC) under an open warm
brown cloak with cream and rust stripes down it (JOSEPH_C_CLOAK / _STRIPE / _BAND), a rope belt, sandals and a straight
knobby walking staff (staff=False: none). Not the Joseph of the Joseph film (beardless, coat of colours).
  pose (JOSEPH_CARPENTER_POSES)  bbox     natural expr  notes (hands [far, near])
  stand          (-52, -353, 69, 3)       warm       the staff in the near hand (top above his head)
  walk_a/_b/_c   (-90, -353, 84, 4) / (-63, -355, 100, 4) / (-67, -358, 74, 4)   warm   with the staff; pose='walk' + phase
                                                     cycles a, c, b, c
  lead_a/lead_b  (-90, -335, 125, 1)      kind       walking ahead of the donkey, the near fist back at JOSEPH_LEAD_HAND =
                                                     (-72, -139) holding its lead rope: joseph_carpenter(lead_x -
                                                     JOSEPH_LEAD_HAND[0]*s*f, y, s, f, pose='lead_a') with lead_x =
                                                     props.donkey_points(...)['lead'][0] and donkey(bridle=True); pose='lead'
                                                     + phase (<.5 a, else b). No staff.
  knock          (-59, -353, 146, 4)      kind       knocking at a door in front (fist (118, -249)); phase 0..1 moves the fist
                                                     to and fro (knock marks when it touches, marks=True)
  point          (-54, -353, 153, 3)      kind
  talk           (-52, -353, 120, 3)      kind       far hand open
  worry          (-52, -335, 80, 0)       worried    hand at the chin ('no room anywhere')
  kneel          (-91, -293, 54, 5)       tender     kneeling, hands folded
  watch          (-56, -333, 89, 3)       tender     both hands resting on the top of his staff, head tilted: watching tenderly
  hold_lamp      (-52, -353, 219, 3)      kind       a clay oil lamp held up on the far palm (111, -231), warm glow (lamp 0..1)
  sit            (-55, -284, 116, 0)      kind       seated: anchor = floor, seat ~67 px up
  cheer          (-100, -336, 106, 0)     joyful
JOSEPH_CARPENTER_EXPRESSIONS: kind, worried, tender, joyful, tired (= weary), happy, awed, peaceful (default stand / walk:
'warm', from the Storm film).

baby_jesus(x, y, scale=1.0, facing=1, state='in_manger', hand=False, glow=0.0, marks=True)
---------------------------------------------------------------------------------------------
The newborn Jesus wrapped in cloths (Luke 2:7): a cream bundle with crossing swaddling bands, a cloth hood round a sweet
round face with a little curl of dark hair, rosy cheeks; drawn with respect, no halo. HEAD ON THE LEFT for facing=1.
Anchor: the bottom centre of the bundle (lying). bbox (-74, -65, 69, 4).
  state (BABY_STATES)  'in_manger' sleeping, lying flat - put the anchor on props.manger's bed (MANGER_BED; see
                       props.manger_points / stable_points); 'held' sleeping, the head end tilted up 14 deg (-81, -56, 63, 9);
                       'awake' open shining eyes, a smile and a tiny hand by the chin; 'wrap' as in_manger.
  hand   True shows the tiny hand also when asleep.   glow 0..1  a soft golden light round him (gentle, no ring).
Mary draws the baby herself in hold_baby / sit_baby / ride_baby / lay_baby / wrap (baby=False to leave it out).

toddler_jesus(x, y, scale=1.0, facing=1, pose='sit', expr=None, phase=0.0, glow=0.0, marks=True)
--------------------------------------------------------------------------------------------------
Jesus at about one or two (Matthew 2:11, the wise men's visit): soft dark curls, Mary's skin, a little cream tunic with a
pale-blue hem, barefoot; big head, chubby limbs (~165 px). TODDLER_POSES:
  sit        (-46, -120, 54, 28)   happy    sitting (on a lap / seat): the anchor is the SEAT, the legs forward below it
  sit_reach  (-42, -120, 72, 27)   amazed   sitting, both arms reaching forward (to the gifts)
  sit_wave   (-48, -120, 54, 28)   laugh    sitting, waving (phase swings the hand)
  stand      (-43, -165, 44, 0)    happy    reach (-36, -164, 75, 0) amazed; wave (-43, -165, 41, 0) laugh
mary(pose='sit_hold') draws him on her lap.

angel(x, y, scale=1.0, facing=1, pose='stand', expr=None, variant=0, glow=0.7, wings=None, phase=0.0, lift=None,
      marks=True)
-------------------------------------------------------------------------------------------------------------------
An angel of the Lord (Gabriel / the angel of the shepherds: variant 0) - a tall, gentle figure of light, never
frightening: a long warm-white robe (ANGEL_ROBE) with gold hem, cuffs, neckline and sash (ANGEL_GOLD), bare feet, soft
shoulder-length honey-brown hair, a kind face with blush, and big soft feathered wings (cream, rows of rounded feathers,
a warm gold tint at the tips) behind both shoulders. No halo; a warm radial glow behind (glow 0..1) with a few twinkling
sparkles (marks=True). variant 1-5: choir looks (skin and hair vary: dark curls, golden waves, short hair).
  wings 0..1   None = the pose's default; 0 folded down behind, 1 spread wide and up. phase 0..1 (loop): a gentle wing
               flutter (+-5 deg) and, in 'float', a +-6 px bob.
  lift         hover this many px above the anchor (float default ANGEL_FLOAT_LIFT = 46): keep the anchor on the ground
               line under the angel ('the angel stood by them'; draw a soft ground_shadow there).
  pose (ANGEL_POSES)  bbox glow=0 (union of variants)   natural expr   notes
  stand        (-165, -407, 121, 0)    warm       arms a little open; wings .45
  float        (-216, -440, 164, -45)  warm       hovering, toes pointing down, the hem fluttering; wings .8
  announce     (-221, -378, 170, 0)    proclaim   far arm raised, open palm (hand (69, -348)): '不要怕！'; wings .9
  sing         (-211, -377, 160, 0)    sing       arms open and lifted, face up; wings .75
  point_down   (-205, -376, 154, 0)    warm       pointing down toward Bethlehem; wings .7
  wings_open   (-221, -378, 172, 0)    joyful     arms spread, wings fully open
  bless        (-191, -378, 142, 0)    warm       near hand raised, palm out
  kneel        (-135, -387, 92, 12)    peaceful   kneeling in adoration, hands folded, wings folded
  glow adds about (-300, -470, 300, 120) round the body at 1 (quantise 0, .3, .6, 1).

angel_choir(x0, x1, y, n=9, phase=0.0, scale=0.36, rows=2, seed=0, glow=0.6, poses=None, depth=0.28)
------------------------------------------------------------------------------------------------------
The heavenly host (Luke 2:13): n smaller angels of light (variants 1-5) spread over the sky between x0 and x1 (ABSOLUTE
stage px) on the line y (front row anchors; each row behind is 230*scale higher and smaller, drawn first), floating in a
gentle arc (the middle ones higher), the two halves facing the middle. Poses cycle ANGEL_CHOIR_POSES (sing, announce,
wings_open, sing, float, ...) or the list `poses`; phase loops their wings at staggered phases (render 4-6 frames). Put
props.heaven_light behind them.

shepherds(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, phase=0.0, crook=True, lamb=True, marks=True)
(shepherd() is the same function)
---------------------------------------------------------------------------------------------------------------------
The shepherds in the fields near Bethlehem: knee-length wool tunics in earth colours under a sheepskin vest (cream or
brown fleece with little curls and a shaggy edge, open at the front), a cord belt, head-cloths with a flap, sandals and a
shepherd's crook (crook=False: none). variant 0-5:
  0 young shepherd, brown head-cloth, stubble        1 the old shepherd: curly white beard, bushy white brows, cream
  head-cloth, grey-brown tunic, a little stooped      2 the boy (child rig, ~240 px): curly hair, rust tunic (the lamb)
  3 sturdy, deep-brown skin, rust head-cloth, olive tunic   4 lanky, ochre headband, sand tunic, dark fleece
  5 full black beard, indigo head-cloth, slate-blue tunic
  pose (SHEPHERD_POSES)  bbox adults (union) / boy          natural expr  notes
  stand          (-71, -387, 105, 2) / (-53, -276, 76, 2)    kind       with the crook
  walk_a/walk_b  (-93, -386, 111, 2) / (-64, -388, 111, 2)   kind       'walk' + phase (<.5 a)
  run_a/run_b    (-122, -312, 128, 0) / (-94, -305, 148, 0)  joyful     hurrying to Bethlehem ('run' + phase)
  sit            (-76, -236, 121, 3)                         kind       on the ground by the fire (pass 'sleepy')
  sit_warm       (-63, -236, 142, 3)                         kind       hands held out to the fire
  sleep          (-211, -200, 97, 0)                         sleepy     lying curled by the fire, head on the left, z's
  shield_eyes    (-138, -329, 71, 0) / (-91, -222, 63, 0)    scared     leaning back, a hand raised palm-out before the face
                                                                        against the great light ('牧羊人都吓坏了')
  kneel          (-93, -300, 50, 5)                          awed       kneeling, hands folded, face up (at the manger / under
                                                                        the singing host)
  point_up       (-70, -343, 92, 0)                          amazed     look_up (-115, -341, 122, 0) amazed
  hold_lamb      (-67, -342, 97, 0) / (-42, -237, 70, 0)     happy      a lamb (props.sheep(lamb=True)) in both arms
                                                                        (lamb=False: arms only)
  cheer          (-104, -344, 110, 0)                        joyful
  tell           (-146, -344, 143, 0)                        joyful     arms wide: telling everyone ('见到人就说')
  lean           (-55, -341, 102, 2)                         kind       both hands on the crook in front, watching the flock
SHEPHERD_EXPRESSIONS: sleepy, scared, amazed, joyful, awed, happy, kind, peaceful.

wise_men(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, phase=0.0, gift=None, gift_open=0.0,
         gift_glow=0.0, marks=True)      (wise_man() is the same function)
-------------------------------------------------------------------------------------------------------------
Learned men from the East who studied the stars (Matthew gives no number or names; three gifts, so three here; the
traditional names WISE_MEN_NAMES only label the looks): long robes with small gold patterns, wide gold hems, gold cuffs,
sash and collar, a cape falling down the back, gold sandals.
  0 'Melchior'  the oldest: fair, a long two-pointed white beard, a five-pointed gold crown with jewels over a cream
                head-cloth, deep-red robe with gold dots, gold cape; gift 'gold'
  1 'Caspar'    young: light stubble, a tall cream-and-gold turban with a green jewel and a little plume, green robe with
                gold diamonds, gold-ochre cape; gift 'frankincense'
  2 'Balthasar' dark skin, a neat short pointed black beard, a tall rounded orange-red crown-cap with a gold band, pearls
                and a blue jewel, purple robe with gold flowers, rust cape; gift 'myrrh'
  gift       None = the variant's own treasure, or 'gold' / 'frankincense' / 'myrrh' (props.GIFT_KINDS); gift_open 0..1
             lifts its lid / stopper, gift_glow 0..1 a golden glow and twinkles (quantise 0, .5, 1).
  pose (WISE_MEN_POSES)  bbox (union of 0-2)   natural expr  notes
  stand          (-76, -390, 64, 0)       kind
  walk_a/walk_b  (-96, -388, 85, 1) / (-70, -390, 104, 0)   kind   ('walk' + phase)
  ride           (-78, -267, 102, 99)     kind       seated on a camel: the anchor is the SEAT: wise_men(*props.camel_points(
                                                     cx, cy, s, pose=..., phase=...)['seat'], s, f, variant=v, pose='ride') on
                                                     camel(cx, cy, s, f, saddle='red' / 'green' / 'purple', load=False)
  point_up       (-78, -389, 87, 0)       awed       pointing at the star ('有一颗特别的星星')
  look_up        (-101, -387, 107, 0)     amazed
  study          (-76, -379, 85, 0)       thoughtful an open star chart held at the chest, looking down at it
  carry_gift     (-73, -385, 77, 0)       kind       holding the treasure at the chest (procession)
  present        (-63, -374, 158, 0)      joyful     bowing a little, the treasure held out
  kneel_offer    (-93, -340, 111, 6)      joyful     kneeling, the treasure held out (hands (88, -127), (65, -122)): open
                                                     it with gift_open / gift_glow as it is named ('黄金、乳香，还有没药')
  bow            (-90, -224, 236, 5)      peaceful   kneeling, bowed low, hands on the ground: worship ('跪下来拜他')
WISE_MEN_EXPRESSIONS: kind, awed, amazed, joyful, thoughtful, peaceful, happy.

townsfolk(x, y, scale=1.0, facing=1, kind='man', variant=0, pose='stand', expr=None, phase=0.0, item=None, marks=True)
-------------------------------------------------------------------------------------------------------------------
The people of Bethlehem (Luke 2: everyone travelling home to be registered) with this film's look - not the Galilean
villagers or the Nineveh citizens. variant 0-5 (mod 6) varies colours and skin. TOWNSFOLK_KINDS:
  'man'              long robe (indigo, rust, sand, plum, olive, slate-teal), cord belt, beard; a head-cloth with a dark
                     band (variants 0, 2, 3, 5) or a wrapped cap
  'woman'            a Bethlehem dress in deep indigo / wine / brown / green / violet with a red cross-stitched chest panel
                     and an embroidered band above the hem, red cuffs, a long cream veil, a gold sash
  'child'            knee tunic; odd variants girls in little embroidered dresses with a ponytail
  'elder'            white hair and beard, shawl, stooped, a stick when standing / walking
  'traveller'        a man as above with a dusty robe and a walking staff (stand / walk); 'traveller_woman' likewise
  'innkeeper'        plump and kind: bald with a grey fringe, a grey moustache and beard, rust robe with a cream apron front
  'herald'           the emperor's herald (Luke 2:1): a short cream tunic with a red hem and sash, a red cloak down his back,
                     short hair, clean-shaven; reads the decree from a scroll
  item (TOWNSFOLK_ITEMS) for carry / carry_walk_a / carry_walk_b / squeeze: 'bundle' (a cloth bundle on the back, a strap
  across the chest; default for travellers), 'sack' (on the shoulder), 'basket', 'jar' (in front; default for women),
  'hen' (a basket with a cheerful hen, bobbing with phase) and 'pots' (a wobbly stack of pots) - the comic busy street.
  pose (TOWNSFOLK_POSES)  bbox man / woman (others similar)      natural expr  notes
  stand          (-70, -338, 60, 0) / (-53, -317, 52, 0)     happy      travellers with a staff (-70, -355, 70, 3)
  walk_a/walk_b  (-90, -338, 84, 1) / (-65, -340, 102, 0)    happy      'walk' + phase (<.5 a)
  carry, carry_walk_a/_b  (-90, -338, 87, 1) (a traveller with a bundle (-83, -338, 60, 0))
  squeeze        (-73, -385, 57, 0) / (-56, -365, 51, 0)     surprised  arms up holding the item above the head, squeezed in
                                                                        the crowd
  look_around    hands on the hips, looking about (puzzled): 'where can we stay?'
  shake_head     (-111, -321, 122, 0) innkeeper             sorry      palms out, head tilting with phase (+-9 deg, loop
                                                                        0, .25, .5, .75) and shake marks: 'no room!'
  read           (-71, -335, 76, 0) herald                  neutral    an open scroll held at the chest
  announce       (-75, -338, 126, 0) herald                 call       the scroll raised, reading the decree aloud
  hold_lamp      a clay oil lamp on the palm (the innkeeper at the door at night)
  talk, point, wave (phase), cheer, listen, sit (-75, -232, 120, 3), sleep
townsfolk_crowd(x, y, scale=1.0, facing=1, n=14, pose='walk', width=1200, rows=3, seed=0, phase=0.0, animals=True, busy=1.0,
                marks=True)
  A busy street crowd centred on x (each row behind 44*scale higher, 6% smaller, drawn first; children in front). pose
  'walk': travellers with bundles, women with jars, a pot carrier and a hen basket going both ways in alternating stride
  frames (busy 0..1 = how many carry things); 'squeeze': packed, half of them holding their bundles overhead and the rest
  looking around ('就像过年时的火车站一样挤'); also stand / talk / look_around / cheer / listen / wave
  (TOWNSFOLK_CROWD_POSES). animals=True adds a laden donkey and a goat. For a really crowded street use n 24-36, rows 4.

child(..., outfit='jumper', item=None)  - the boy at the Christmas tree (opening and ending)
------------------------------------------------------------------------------------------
child() keeps every earlier look and output. outfit='jumper' (CHILD_OUTFITS): a little boy (~5, 229 px) with dark curly
hair and warm brown skin in a red knitted Christmas jumper (JUMPER) with a cream band of little green trees, cream cuffs,
green trousers and cream socks (no shoes indoors). All CHILD / SIBLING / STORM poses work in the jumper; the new
NATIVITY_CHILD_POSES work for every outfit / sibling too:
  decorate   (-61, -228, 72, 0)    happy    reaching up to hang a bauble (item='bauble' default, or 'star') on the tree:
                                            the bauble hangs from the far hand (59, -177) - stand him ~100*scale in front of
                                            props.christmas_tree, facing it
  place      (-56, -203, 92, 0)    kind     kneeling, putting a little figure down in front (item 'figure' = the baby in its
                                            manger (default), 'sheep', 'star', 'gift' - props.nativity_figure kinds): hands
                                            (79, -65), (39, -70)
  kneel_look (-38, -176, 62, 0)    amazed   sitting back on his heels, looking at the nativity set
  hold_star  (-59, -229, 117, 0)   joyful   holding a glowing star up in front of him (for the top of the tree)
  (also smile_up, pray, point_up, cheer, wave for the ending)

Constants (Nativity film): MARY_POSES, MARY_EXPRESSIONS, MARY_LAY_DX, MARY_LAY_Y, JOSEPH_CARPENTER_POSES,
JOSEPH_CARPENTER_EXPRESSIONS, JOSEPH_LEAD_HAND, BABY_STATES, TODDLER_POSES, ANGEL_LOOKS, ANGEL_POSES, ANGEL_FLOAT_LIFT,
ANGEL_CHOIR_POSES, SHEPHERD_POSES, SHEPHERD_EXPRESSIONS, WISE_MEN_NAMES, WISE_MEN_POSES, WISE_MEN_EXPRESSIONS,
TOWNSFOLK_KINDS, TOWNSFOLK_POSES, TOWNSFOLK_ITEMS, TOWNSFOLK_CROWD_POSES, NATIVITY_CHILD_POSES, CHILD_ITEMS,
NATIVITY_EXPRESSIONS; colours MARY_SKIN, MARY_HAIR, MARY_VEIL, MARY_LINING, MARY_DRESS, MARY_BLUE, MARY_TRIM,
JOSEPH_C_SKIN, JOSEPH_C_HAIR, JOSEPH_C_TUNIC, JOSEPH_C_CLOAK, JOSEPH_C_STRIPE, JOSEPH_C_BAND, BABY_SKIN, BABY_CLOTH,
BABY_BAND, TODDLER_TUNIC, ANGEL_ROBE, ANGEL_GOLD, ANGEL_WING, ANGEL_FEATHER, LAMPLIGHT, STAFF_WOOD, JUMPER, JUMPER_KNIT,
JUMPER_TROUSERS, JUMPER_SOCKS. Baby and toddler Jesus and the angels are drawn with respect; God the Father is never
drawn - his glory is light only (props.glory / heaven_light / the_star).
"""
import hashlib
import math

from art.style import INK, P, fmt, mix, shade, smooth_path

# ======================================================================= constants
OW = 4.0                  # silhouette outline width (px at scale 1)
LW = 3.0                  # inner detail line width (faces, folds)
EYE = "#3a271b"           # pupils: deep umber, never black
HI = "#fffaf0"            # highlights: warm off-white, never pure white
EYE_WHITE = "#fbf3e3"     # whites of wide frightened eyes / teeth (cream, not white)
SANDAL = "#8b5a35"
SANDAL_DARK = "#6b4127"
TONGUE = "#e08479"
GOLD = P["crown"]
GOLD_DARK = shade(P["crown"], -0.32)
DRIP = P["sea_pale"]      # water and sweat drops (outlined + highlight so they read on any background)
MARK = P["ink_soft"]      # motion / sound / sleep marks

# ======================================================================= vectors


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _mul(a, k):
    return (a[0] * k, a[1] * k)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _len(a):
    return math.hypot(a[0], a[1])


def _nrm(a):
    n = _len(a) or 1.0
    return (a[0] / n, a[1] / n)


def _rot(a, deg):
    """Rotate a vector; positive degrees turn clockwise on screen (y points down)."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (a[0] * c - a[1] * s, a[0] * s + a[1] * c)


def _dv(deg):
    """Limb angle -> unit direction. 0 = hanging down, 90 = forward, 180 = up, -90 = backward."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


def _vdeg(v):
    """Inverse of _dv: direction vector -> limb angle."""
    return math.degrees(math.atan2(v[0], v[1]))


def _ang(v):
    """Screen angle of a vector in degrees (0 = +x, 90 = down) for SVG rotate()."""
    return math.degrees(math.atan2(v[1], v[0]))


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _pt(p):
    return f"{fmt(p[0])},{fmt(p[1])}"


# ======================================================================= polygons


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _rounded(pts, r, k=5):
    """Convex polygon -> densely sampled polygon with rounded corners (stays convex)."""
    n = len(pts)
    out = []
    for i in range(n):
        a, v, b = pts[i - 1], pts[i], pts[(i + 1) % n]
        la, lb = _len(_sub(a, v)), _len(_sub(b, v))
        p1 = _lerp(v, a, min(r / la, 0.5) if la else 0)
        p2 = _lerp(v, b, min(r / lb, 0.5) if lb else 0)
        for j in range(k + 1):
            t = j / k
            q = _add(_add(_mul(p1, (1 - t) ** 2), _mul(v, 2 * t * (1 - t))), _mul(p2, t * t))
            out.append(q)
    return out


def _clip(poly, p0, n):
    """Keep the part of a polygon where (p - p0) . n >= 0 (Sutherland-Hodgman, one half-plane)."""
    out = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n), _dot(_sub(b, p0), n)
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            t = da / (da - db)
            out.append(_lerp(a, b, t))
    return out


def _band(poly, p0, n, d0, d1):
    """Part of a polygon between the lines (p - p0) . n = d0 and = d1."""
    c = _clip(poly, _add(p0, _mul(n, d0)), n)
    return _clip(c, _add(p0, _mul(n, d1)), _mul(n, -1)) if c else []


def _d(pts, closed=True):
    if not pts:
        return ""
    return "M" + " L".join(_pt(p) for p in pts) + (" Z" if closed else "")


# ======================================================================= svg helpers


def _st(w=OW, col=INK):
    return f'stroke="{col}" stroke-width="{fmt(w)}" stroke-linejoin="round" stroke-linecap="round"'


def _tube(pts, w, col, ow=OW):
    """Outlined round-capped tube along a polyline (limbs, sleeves, ropes)."""
    d = _d(pts, closed=False)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{fmt(w + 2 * ow)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{fmt(w)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _union(polys, fill, ow=OW):
    """Several overlapping shapes drawn with one outer ink outline (no inner seams)."""
    ds = [_d(p) for p in polys if p]
    return ("".join(f'<path d="{d}" fill="{fill}" {_st(2 * ow)}/>' for d in ds) +
            "".join(f'<path d="{d}" fill="{fill}"/>' for d in ds))


def _poly(pts, fill, sw=LW, extra=""):
    if not pts or len(pts) < 3:
        return ""
    st = _st(sw) if sw else ""
    return f'<path d="{_d(pts)}" fill="{fill}" {st} {extra}/>'


def _clip_id(*parts):
    return "cp" + hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


def _ell(cx, cy, rx, ry, fill, sw=None, extra=""):
    st = _st(sw) if sw else ""
    return f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="{fill}" {st} {extra}/>'


def _line(d, w=LW, col=INK, extra=""):
    return f'<path d="{d}" fill="none" {_st(w, col)} {extra}/>'


def _drop(x, y, s, fill=DRIP, sw=2.2):
    """Outlined water / sweat drop, tip up, with a small highlight. About 1.7*s wide, 2.75*s tall."""
    d = (f'<path d="M{fmt(x)},{fmt(y - 1.6 * s)} C{fmt(x + 0.3 * s)},{fmt(y - 1.0 * s)} {fmt(x + 0.85 * s)},'
         f'{fmt(y - 0.45 * s)} {fmt(x + 0.85 * s)},{fmt(y + 0.3 * s)} A{fmt(0.85 * s)},{fmt(0.85 * s)} 0 0 1 '
         f'{fmt(x - 0.85 * s)},{fmt(y + 0.3 * s)} C{fmt(x - 0.85 * s)},{fmt(y - 0.45 * s)} {fmt(x - 0.3 * s)},'
         f'{fmt(y - 1.0 * s)} {fmt(x)},{fmt(y - 1.6 * s)} Z" fill="{fill}" {_st(sw)}/>')
    d += (f'<ellipse cx="{fmt(x - 0.33 * s)}" cy="{fmt(y + 0.12 * s)}" rx="{fmt(0.18 * s)}" ry="{fmt(0.3 * s)}" '
          f'fill="{HI}" opacity="0.95"/>')
    return d


def _zglyph(cx, cy, size, mirror=1, col=MARK, w=3.2):
    """A sleeping 'Z' that always reads left-to-right (mirror=-1 undoes a mirrored parent)."""
    h = size / 2
    d = f"M{fmt(-h)},{fmt(-h)} L{fmt(h)},{fmt(-h)} L{fmt(-h)},{fmt(h)} L{fmt(h)},{fmt(h)}"
    return (f'<g transform="translate({fmt(cx)},{fmt(cy)}) scale({mirror},1)">'
            f'<path d="{d}" fill="none" {_st(w, col)}/></g>')


# ======================================================================= metrics

_ADULT = dict(R=44, T=100, neck=46, ua=50, fa=46, th=60, sh=58, aw=22, lw=17, hr=11, fl=30,
              sw=25, hw=13, ww=31, shw=37, flare=22, sdrop=14, seat=20, ank=12)
_CHILD = dict(R=39, T=57, neck=39, ua=31, fa=28, th=35, sh=33, aw=17, lw=14, hr=9.5, fl=22,
              sw=19, hw=10, ww=24, shw=28, flare=12, sdrop=10, seat=15, ank=10)


def _metrics(base, k=1.0, wide=1.0, **over):
    m = {key: v * k for key, v in base.items()}
    for key in ("sw", "ww", "shw", "hw"):
        m[key] *= wide
    m.update(over)
    return m


# ======================================================================= expressions

EXPRS = {
    #            eyes      brow (inner, outer, lift)   mouth          extras
    "neutral":   dict(eyes="dot", brow=(0.0, 0.0, 0.0), mouth="smile"),
    "happy":     dict(eyes="dot", brow=(-0.03, 0.02, -0.06), mouth="grin"),
    "sad":       dict(eyes="dot", brow=(-0.10, 0.05, 0.0), mouth="frown", look=(0, 0.05)),
    "scared":    dict(eyes="fear", brow=(-0.13, 0.05, -0.03), mouth="scared", sweat=1, tremble=True),
    "angry":     dict(eyes="dot", brow=(0.11, -0.05, 0.03), mouth="grumpy"),
    "surprised": dict(eyes="big", brow=(-0.03, -0.03, -0.12), mouth="o"),
    "sleepy":    dict(eyes="closed", brow=(0.0, 0.02, 0.04), mouth="small_o"),
    "peaceful":  dict(eyes="closed", brow=(-0.03, 0.02, 0.0), mouth="smile"),
    "dizzy":     dict(eyes="spiral", brow=(-0.07, 0.03, -0.04), mouth="wave"),
    "shout":     dict(eyes="dot", brow=(-0.02, -0.03, -0.08), mouth="shout"),
    "call":      dict(eyes="dot", brow=(-0.07, 0.02, -0.07), mouth="call"),
    "sorry":     dict(eyes="down", brow=(-0.10, 0.05, 0.03), mouth="wobble", blush=True),
    "worried":   dict(eyes="dot", brow=(-0.09, 0.04, -0.02), mouth="flat"),
    "tired":     dict(eyes="droop", brow=(-0.11, 0.05, 0.02), mouth="pant", sweat=3),
    # Daniel film: the jealous officials (gentle, never scary)
    "sly":       dict(eyes="narrow", brow=(-0.02, -0.07, -0.04), mouth="smirk", look=(0.05, 0.0)),
    "smug":      dict(eyes="lidded", brow=(-0.02, -0.03, -0.07), mouth="smirk"),
}
EXPRESSIONS = tuple(EXPRS)
_SWEAT = ((1.04, -0.20, 0.095), (1.20, 0.22, 0.07), (1.17, -0.62, 0.06))   # head-frame (x, y, size) in R


def _face(R, skin, expr, look=(0, 0), brow_col=INK, mouth=True, tremble=True, brow_w=3.4):
    """Eyes, brows, nose, cheeks, mouth in head-frame coordinates (3/4 view facing +x).

    Returns (face, overlay): overlay (sweat drops, tremble marks) is drawn after any headwear."""
    E = EXPRS.get(expr, EXPRS["neutral"])
    lx = look[0] + E.get("look", (0, 0))[0]
    ly = look[1] + E.get("look", (0, 0))[1]
    s = ""
    ck = mix(skin, P["cheek"], 0.8)
    big = 1.35 if E.get("blush") else 1.0
    s += _ell(-0.30 * R, 0.36 * R, 0.16 * R * big, 0.10 * R * big, ck, extra='opacity="0.85"')
    s += _ell(0.67 * R, 0.38 * R, 0.12 * R * big, 0.09 * R * big, ck, extra='opacity="0.85"')
    eyes = [(-0.10 * R, 0.04 * R), (0.40 * R, 0.04 * R)]
    kind = E["eyes"]
    for i, (ex, ey) in enumerate(eyes):
        inner = 1 if i == 0 else -1          # direction from this eye toward the nose bridge
        if kind in ("dot", "big", "down"):
            k = 1.2 if kind == "big" else (0.9 if kind == "down" else 1.0)
            cx, cy = ex + lx * R, ey + ly * R + (0.07 * R if kind == "down" else 0)
            rx, ry = 0.118 * R * k, 0.15 * R * k
            s += _ell(cx, cy, rx, ry, EYE)
            s += f'<circle cx="{fmt(cx - 0.35 * rx)}" cy="{fmt(cy - 0.38 * ry)}" r="{fmt(0.36 * rx)}" fill="{HI}"/>'
            if kind == "down":
                s += _line(f"M{fmt(cx - 1.5 * rx)},{fmt(cy - 0.6 * ry)} Q{fmt(cx)},{fmt(cy - 1.3 * ry)} "
                           f"{fmt(cx + 1.5 * rx)},{fmt(cy - 0.6 * ry)}", w=2.6)
        elif kind == "fear":                 # wide whites, small pupils: reads as fright, not delight
            cx, cy = ex + lx * R, ey + ly * R - 0.01 * R
            rx, ry = 0.145 * R, 0.185 * R
            s += _ell(cx, cy, rx, ry, EYE_WHITE, sw=2.6)
            px, py = cx + 0.02 * R + lx * 0.4 * R, cy + 0.03 * R
            s += _ell(px, py, 0.068 * R, 0.08 * R, EYE)
            s += f'<circle cx="{fmt(px - 0.025 * R)}" cy="{fmt(py - 0.03 * R)}" r="{fmt(0.022 * R)}" fill="{HI}"/>'
        elif kind == "droop":                # heavy lids drooping toward the outer corners (weak, tired)
            cx, cy = ex + lx * R, ey + ly * R + 0.03 * R
            rx, ry = 0.118 * R, 0.15 * R
            s += (f'<path d="M{fmt(cx - rx)},{fmt(cy - 0.05 * ry)} A{fmt(rx)},{fmt(ry)} 0 0 0 {fmt(cx + rx)},'
                  f'{fmt(cy - 0.05 * ry)} Z" fill="{EYE}"/>')
            xi, xo = cx + inner * 1.3 * rx, cx - inner * 1.4 * rx
            s += _line(f"M{fmt(xo)},{fmt(cy + 0.25 * ry)} Q{fmt(cx)},{fmt(cy - 0.45 * ry)} {fmt(xi)},"
                       f"{fmt(cy - 0.22 * ry)}", w=3.0)
        elif kind == "closed":
            s += _line(f"M{fmt(ex - 0.13 * R)},{fmt(ey)} Q{fmt(ex)},{fmt(ey + 0.12 * R)} {fmt(ex + 0.13 * R)},{fmt(ey)}",
                       w=3.4)
        elif kind == "arc":                  # laughing: happy upturned arcs (David film)
            s += _line(f"M{fmt(ex - 0.13 * R)},{fmt(ey + 0.05 * R)} Q{fmt(ex)},{fmt(ey - 0.13 * R)} "
                       f"{fmt(ex + 0.13 * R)},{fmt(ey + 0.05 * R)}", w=3.6)
        elif kind == "squeeze":              # Joseph film: crying - eyes squeezed shut, a wavy lid line and lashes
            sl = -inner * 0.05 * R
            s += _line(f"M{fmt(ex - 0.14 * R)},{fmt(ey - 0.01 * R + sl)} Q{fmt(ex - 0.05 * R)},{fmt(ey + 0.09 * R)} "
                       f"{fmt(ex + 0.01 * R)},{fmt(ey + 0.03 * R)} T{fmt(ex + 0.14 * R)},{fmt(ey - 0.01 * R - sl)}", w=3.4)
            for dx in (-0.07, 0.05):
                s += _line(f"M{fmt(ex + dx * R)},{fmt(ey + 0.07 * R)} l{fmt(0.01 * R)},{fmt(0.07 * R)}", w=2.0)
        elif kind == "spiral":
            pts = []
            for j in range(22):
                a = j * 0.62
                rr = 0.02 * R + 0.0058 * R * j
                pts.append((ex + rr * math.cos(a), ey + rr * math.sin(a)))
            s += _line(smooth_path(pts, closed=False), w=2.4)
        elif kind in ("narrow", "lidded"):   # sly / smug: the upper lid lowered over the dot eye
            cx, cy = ex + lx * R, ey + ly * R + 0.02 * R
            rx, ry = 0.125 * R, 0.15 * R
            if kind == "narrow":             # lid slants a little down toward the nose: a sideways glance
                y0, sl = cy - 0.12 * ry, 0.12
            else:                            # heavy, level lids: pleased with himself
                y0, sl = cy + 0.05 * ry, -0.05
            ell = [(cx + rx * math.cos(2 * math.pi * j / 28), cy + ry * math.sin(2 * math.pi * j / 28))
                   for j in range(28)]
            vis = _clip(ell, (cx, y0), _nrm((-sl * inner, 1.0)))
            s += _poly(vis, EYE, sw=0)
            s += f'<circle cx="{fmt(cx - 0.3 * rx)}" cy="{fmt(cy + 0.32 * ry)}" r="{fmt(0.26 * rx)}" fill="{HI}"/>'
            xa, xb = cx - 1.3 * rx, cx + 1.3 * rx
            ya, yb = y0 + sl * inner * (xa - cx), y0 + sl * inner * (xb - cx)
            s += _line(f"M{fmt(xa)},{fmt(ya + 0.05 * ry)} Q{fmt(cx)},{fmt(y0 - 0.32 * ry)} {fmt(xb)},{fmt(yb + 0.05 * ry)}",
                       w=3.2)
    bi, bo, bl = E["brow"]
    for i, (ex, ey) in enumerate(eyes):
        if i == 0:
            xo, xi = ex - 0.14 * R, ex + 0.09 * R
        else:
            xi, xo = ex - 0.09 * R, ex + 0.14 * R
        if i == 1 and "brow2" in E:          # asymmetric brows (puzzled): the near brow differs
            bi, bo, bl = E["brow2"]
        yb = -0.24 * R + bl * R
        yi, yo = yb + bi * R, yb + bo * R
        cx, cy = (xi + xo) / 2, (yi + yo) / 2 - 0.05 * R
        s += _line(f"M{fmt(xo)},{fmt(yo)} Q{fmt(cx)},{fmt(cy)} {fmt(xi)},{fmt(yi)}", w=brow_w, col=brow_col)
    # nose: small soft oval between and below the eyes, a faint 'c' under it (never a full ink curve)
    nx, ny = 0.30 * R, 0.25 * R
    s += _ell(nx, ny, 0.085 * R, 0.068 * R, shade(skin, -0.13))
    s += _line(f"M{fmt(nx - 0.07 * R)},{fmt(ny + 0.02 * R)} Q{fmt(nx - 0.01 * R)},{fmt(ny + 0.10 * R)} "
               f"{fmt(nx + 0.07 * R)},{fmt(ny + 0.03 * R)}", w=2.2, col=P["ink_soft"], extra='opacity="0.6"')
    if mouth:
        s += _mouth(R, E["mouth"])
    over = ""
    for (hx, hy, k) in _SWEAT[:E.get("sweat", 0)]:
        over += _drop(hx * R, hy * R, k * R)
    if E.get("tears"):                       # Joseph film: tear streams down both cheeks, a drop at each end
        for k, (tx, l) in enumerate(((-0.13, 0.62), (0.44, 0.55))):
            x0, y0 = tx * R, 0.16 * R
            d = (f"M{fmt(x0)},{fmt(y0)} Q{fmt(x0 - 0.05 * R)},{fmt(y0 + l * 0.45 * R)} "
                 f"{fmt(x0 + 0.01 * R)},{fmt(y0 + l * R)}")
            over += _line(d, w=0.11 * R + 2.4, col=INK, extra='opacity="0.5"')
            over += _line(d, w=0.11 * R, col=DRIP)
            over += _drop(x0 + 0.01 * R, y0 + (l + 0.16) * R, 0.085 * R)
        if E["tears"] > 1:                   # sobbing: one more drop falling beside the face
            over += _drop(-0.42 * R, 1.02 * R, 0.07 * R)
    if E.get("tremble") and tremble:
        for (hx, hy, sg) in ((1.30, -0.05, 1), (-1.32, -0.25, -1)):
            for j in (0, 1):
                x0 = (hx + sg * 0.13 * j) * R
                over += _line(f"M{fmt(x0)},{fmt((hy - 0.22) * R)} l{fmt(sg * 0.05 * R)},{fmt(0.11 * R)} "
                              f"l{fmt(-sg * 0.05 * R)},{fmt(0.11 * R)} l{fmt(sg * 0.05 * R)},{fmt(0.11 * R)}",
                              w=2.6, col=MARK)
    return s, over


def _mouth(R, kind, mx=None, my=None):
    mx = 0.18 * R if mx is None else mx
    my = 0.55 * R if my is None else my
    MI = P["mouth_inside"]

    def P_(x, y):
        return f"{fmt(mx + x * R)},{fmt(my + y * R)}"

    if kind == "smile":
        return _line(f"M{P_(-0.15, -0.02)} Q{P_(0, 0.13)} {P_(0.15, -0.02)}", w=3.2)
    if kind == "grin":
        return (f'<path d="M{P_(-0.19, -0.05)} Q{P_(0, 0.36)} {P_(0.19, -0.05)} Q{P_(0, 0.0)} {P_(-0.19, -0.05)} Z" '
                f'fill="{MI}" {_st(2.8)}/>'
                f'<path d="M{P_(-0.08, 0.14)} Q{P_(0, 0.08)} {P_(0.09, 0.14)} Q{P_(0, 0.20)} {P_(-0.08, 0.14)} Z" '
                f'fill="{TONGUE}"/>')
    if kind == "frown":
        return _line(f"M{P_(-0.14, 0.06)} Q{P_(0, -0.07)} {P_(0.14, 0.06)}", w=3.2)
    if kind == "grumpy":
        return _line(f"M{P_(-0.15, 0.05)} Q{P_(-0.05, -0.04)} {P_(0.02, -0.01)} T{P_(0.15, 0.06)}", w=3.4)
    if kind == "scared":
        # wide wobbly 'aaah' with a row of upper teeth and a dark inside (no tongue)
        top = (f"M{P_(-0.20, 0.03)} Q{P_(-0.14, -0.04)} {P_(-0.07, 0.02)} Q{P_(0, -0.04)} {P_(0.07, 0.02)} "
               f"Q{P_(0.14, -0.04)} {P_(0.20, 0.03)}")
        outline = top + f" Q{P_(0.19, 0.25)} {P_(0, 0.25)} Q{P_(-0.19, 0.25)} {P_(-0.20, 0.03)} Z"
        teeth = (f"M{P_(-0.17, 0.035)} Q{P_(-0.12, -0.02)} {P_(-0.07, 0.03)} Q{P_(0, -0.02)} {P_(0.07, 0.03)} "
                 f"Q{P_(0.12, -0.02)} {P_(0.17, 0.035)} L{P_(0.16, 0.085)} Q{P_(0, 0.065)} {P_(-0.16, 0.085)} Z")
        return (f'<path d="{outline}" fill="{shade(MI, -0.38)}"/>' + f'<path d="{teeth}" fill="{EYE_WHITE}"/>'
                + f'<path d="{outline}" fill="none" {_st(2.8)}/>')
    if kind == "o":
        return _ell(mx, my + 0.06 * R, 0.09 * R, 0.13 * R, MI, sw=2.8)
    if kind == "small_o":
        return _ell(mx, my + 0.03 * R, 0.05 * R, 0.065 * R, MI, sw=2.6)
    if kind == "small_open":
        return _ell(mx, my + 0.03 * R, 0.08 * R, 0.05 * R, MI, sw=2.6)
    if kind == "pant":
        return _ell(mx, my + 0.05 * R, 0.08 * R, 0.075 * R, shade(MI, -0.25), sw=2.6)
    if kind == "wave":
        return _line(f"M{P_(-0.17, 0.03)} Q{P_(-0.11, -0.05)} {P_(-0.05, 0.03)} T{P_(0.07, 0.03)} T{P_(0.17, 0.03)}",
                     w=3.0)
    if kind == "shout":
        return (_ell(mx, my + 0.08 * R, 0.17 * R, 0.19 * R, MI, sw=2.8) +
                _ell(mx + 0.01 * R, my + 0.19 * R, 0.10 * R, 0.06 * R, TONGUE))
    if kind == "call":
        d = (f"M{P_(-0.14, 0.0)} Q{P_(0, -0.03)} {P_(0.14, 0.0)} Q{P_(0.12, 0.22)} {P_(0, 0.22)} "
             f"Q{P_(-0.12, 0.22)} {P_(-0.14, 0.0)} Z")
        return (f'<path d="{d}" fill="{MI}" {_st(2.8)}/>' +
                _ell(mx + 0.01 * R, my + 0.15 * R, 0.07 * R, 0.04 * R, TONGUE))
    if kind == "wobble":
        return _line(f"M{P_(-0.12, 0.05)} Q{P_(-0.06, -0.02)} {P_(0, 0.02)} T{P_(0.12, 0.04)}", w=3.0)
    if kind == "flat":
        return _line(f"M{P_(-0.12, 0.03)} Q{P_(-0.04, -0.01)} {P_(0.02, 0.02)} T{P_(0.13, 0.01)}", w=3.0)
    if kind == "smirk":           # lopsided little smile pulled up toward the face side, with a dimple tick
        return (_line(f"M{P_(-0.12, 0.04)} Q{P_(0.02, 0.10)} {P_(0.15, -0.05)}", w=3.2) +
                _line(f"M{P_(0.13, -0.08)} Q{P_(0.17, -0.05)} {P_(0.165, -0.01)}", w=2.4))
    return _mouth_extra(R, kind, P_, mx, my)


# ======================================================================= head parts (head frame)


def _ear(R, skin):
    return (_ell(-0.84 * R, 0.12 * R, 0.17 * R, 0.22 * R, skin, sw=3.2) +
            _line(f"M{fmt(-0.80 * R)},{fmt(0.02 * R)} Q{fmt(-0.92 * R)},{fmt(0.12 * R)} {fmt(-0.80 * R)},{fmt(0.24 * R)}",
                  w=2.4))


def _polar(R, deg, k=1.0):
    a = math.radians(deg)
    return (R * k * math.cos(a), R * k * math.sin(a))


def _hair_cap(R, col, style="short", front=-28, back=165, line=-0.42):
    """Hair covering the top/back of the head. Angles in screen degrees (-90 = top, 180 = back)."""
    outer = []
    n = 16
    for i in range(n + 1):
        deg = front - (front - (back - 360)) * i / n
        k = 1.07
        if style == "curly":
            k = 1.03 + (0.08 if i % 2 else 0.0)
        outer.append(_polar(R, deg, k))
    inner = [_polar(R, back, 0.9), _polar(R, back - 25, 0.92), (-0.55 * R, line * R - 0.05 * R),
             (0.05 * R, line * R - 0.10 * R), (0.55 * R, line * R)]
    pts = outer + inner
    return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'


_MOUSTACHED = ("full", "white", "captain", "assyrian", "assyrian_short", "trim", "pointed", "long",
               "jesus", "curly", "fisher",   # these three: Storm film
               "carpenter", "elder_curl", "magus", "magus_short")   # Nativity film (_nativity_beard)


def _beard(R, col, kind):
    if kind is None:
        return ""
    if kind == "short":      # Jonah: short beard along the jaw, open below the mouth
        pts = [(-0.84 * R, 0.10 * R), (-0.86 * R, 0.55 * R), (-0.46 * R, 0.98 * R), (0.16 * R, 1.10 * R),
               (0.62 * R, 0.94 * R), (0.88 * R, 0.52 * R), (0.70 * R, 0.62 * R), (0.20 * R, 0.76 * R),
               (-0.28 * R, 0.66 * R), (-0.62 * R, 0.32 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
    if kind == "stubble":
        pts = [(-0.80 * R, 0.30 * R), (-0.72 * R, 0.70 * R), (-0.30 * R, 0.98 * R), (0.18 * R, 1.04 * R),
               (0.64 * R, 0.86 * R), (0.84 * R, 0.55 * R), (0.66 * R, 0.66 * R), (0.20 * R, 0.78 * R),
               (-0.30 * R, 0.70 * R), (-0.62 * R, 0.45 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.0)}/>'
    if kind in ("full", "white", "captain"):  # elder / captain: rounded beard (captain's a little shorter)
        L = 1.20 if kind == "captain" else 1.42
        pts = [(-0.86 * R, 0.0), (-0.92 * R, 0.60 * R), (-0.55 * R, (L - 0.22) * R), (0.10 * R, L * R),
               (0.68 * R, (L - 0.24) * R), (0.92 * R, 0.55 * R), (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R),
               (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.18)
        s += _line(f"M{fmt(-0.25 * R)},{fmt((L - 0.45) * R)} q{fmt(0.05 * R)},{fmt(0.16 * R)} {fmt(0.02 * R)},"
                   f"{fmt(0.26 * R)}", w=2.2, col=dark)
        s += _line(f"M{fmt(0.38 * R)},{fmt((L - 0.45) * R)} q{fmt(0.02 * R)},{fmt(0.14 * R)} {fmt(-0.04 * R)},"
                   f"{fmt(0.24 * R)}", w=2.2, col=dark)
        return s
    if kind in ("assyrian", "assyrian_short"):
        L = 1.52 if kind == "assyrian" else 1.30
        pts = [(-0.86 * R, -0.05 * R), (-0.88 * R, 0.55 * R), (-0.62 * R, (L - 0.05) * R), (-0.20 * R, L * R),
               (0.12 * R, (L + 0.06) * R), (0.46 * R, L * R), (0.74 * R, (L - 0.12) * R), (0.92 * R, 0.55 * R),
               (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R), (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        curl = mix(col, "#c9b29a", 0.55)
        rows = 3 if kind == "assyrian" else 2
        for r_ in range(rows):
            yy = (1.00 + r_ * 0.20) * R
            x0, x1 = (-0.62 + 0.06 * r_) * R, (0.70 - 0.04 * r_) * R
            n = 5
            w = (x1 - x0) / n
            d = f"M{fmt(x0)},{fmt(yy)}"
            for i in range(n):
                d += f" q{fmt(w / 2)},{fmt(0.13 * R)} {fmt(w)},0"
            s += f'<path d="{d}" fill="none" {_st(2.2, curl)}/>'
        return s
    if kind == "trim":         # Daniel: short rounded beard, dark with a little grey at the chin and jaw
        L = 1.10
        pts = [(-0.86 * R, 0.0), (-0.90 * R, 0.55 * R), (-0.55 * R, (L - 0.18) * R), (0.10 * R, L * R),
               (0.66 * R, (L - 0.20) * R), (0.90 * R, 0.52 * R), (0.70 * R, 0.64 * R), (0.20 * R, 0.82 * R),
               (-0.30 * R, 0.70 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        grey = mix(col, "#e6e0d6", 0.62)            # a little grey: soft flecks inside the beard
        for (x0, y0, w0) in ((-0.30, 0.90, 0.20), (0.18, 0.96, 0.24), (-0.70, 0.42, 0.14), (0.62, 0.74, 0.14)):
            s += _line(f"M{fmt((x0 - w0 / 2) * R)},{fmt(y0 * R)} q{fmt(w0 / 4 * R)},{fmt(0.06 * R)} {fmt(w0 / 2 * R)},0 "
                       f"t{fmt(w0 / 2 * R)},0", w=2.4, col=grey)
        return s
    if kind == "long":         # Noah film: a long, wavy grandfather's beard flowing down onto the chest
        pts = [(-0.86 * R, -0.02 * R), (-0.97 * R, 0.62 * R), (-0.86 * R, 1.22 * R), (-0.58 * R, 1.72 * R),
               (-0.30 * R, 1.98 * R), (-0.04 * R, 2.16 * R), (0.10 * R, 2.02 * R), (0.32 * R, 2.08 * R),
               (0.52 * R, 1.80 * R), (0.80 * R, 1.30 * R), (0.95 * R, 0.56 * R), (0.70 * R, 0.66 * R),
               (0.20 * R, 0.86 * R), (-0.30 * R, 0.74 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.2)
        for x0, y0, x1, y1 in ((-0.55, 0.95, -0.38, 1.62), (-0.10, 1.05, -0.04, 1.86), (0.38, 1.02, 0.30, 1.70),
                               (-0.76, 0.55, -0.70, 1.10)):
            s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} Q{fmt((x0 + 0.12) * R)},{fmt((y0 + y1) / 2 * R)} "
                       f"{fmt(x1 * R)},{fmt(y1 * R)}", w=2.2, col=dark)
        return s
    if kind in ("jesus", "curly", "fisher"):    # Storm film: see _storm_beard
        return _storm_beard(R, col, kind)
    if kind in _NATIVITY_BEARDS:               # Nativity film: see _nativity_beard
        return _nativity_beard(R, col, kind)
    if kind == "pointed":      # an official: neat beard ending in a soft point, a curl row across it
        pts = [(-0.86 * R, 0.0), (-0.88 * R, 0.55 * R), (-0.50 * R, 1.10 * R), (0.08 * R, 1.62 * R),
               (0.52 * R, 1.16 * R), (0.90 * R, 0.55 * R), (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R),
               (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        curl = mix(col, "#c9b29a", 0.5)
        d = f"M{fmt(-0.48 * R)},{fmt(1.04 * R)}"
        for i in range(4):
            d += f" q{fmt(0.115 * R)},{fmt(0.12 * R)} {fmt(0.23 * R)},0"
        s += f'<path d="{d}" fill="none" {_st(2.2, curl)}/>'
        s += _line(f"M{fmt(0.06 * R)},{fmt(1.22 * R)} q{fmt(0.03 * R)},{fmt(0.16 * R)} {fmt(0.02 * R)},{fmt(0.28 * R)}",
                   w=2.0, col=curl)
        return s
    return ""


def _moustache(R, col, kind):
    """Short moustache well above the mouth, so the mouth (drawn after it) always shows."""
    if kind not in _MOUSTACHED:
        return ""
    mx, my = 0.18 * R, 0.45 * R
    if kind == "long":         # Noah: a full moustache whose ends curl up a little (a smiling grandfather)
        w = 0.30 * R
        return (f'<path d="M{fmt(mx - w)},{fmt(my - 0.02 * R)} Q{fmt(mx - 0.20 * R)},{fmt(my - 0.10 * R)} '
                f'{fmt(mx)},{fmt(my - 0.03 * R)} Q{fmt(mx + 0.20 * R)},{fmt(my - 0.12 * R)} {fmt(mx + w)},{fmt(my - 0.05 * R)} '
                f'Q{fmt(mx + 0.22 * R)},{fmt(my + 0.11 * R)} {fmt(mx)},{fmt(my + 0.10 * R)} '
                f'Q{fmt(mx - 0.22 * R)},{fmt(my + 0.12 * R)} {fmt(mx - w)},{fmt(my - 0.02 * R)} Z" fill="{col}" {_st(2.4)}/>')
    w = 0.22 * R
    return (f'<path d="M{fmt(mx - w)},{fmt(my + 0.08 * R)} Q{fmt(mx - 0.13 * R)},{fmt(my - 0.05 * R)} '
            f'{fmt(mx)},{fmt(my)} Q{fmt(mx + 0.13 * R)},{fmt(my - 0.05 * R)} {fmt(mx + w)},{fmt(my + 0.08 * R)} '
            f'Q{fmt(mx + 0.10 * R)},{fmt(my + 0.05 * R)} {fmt(mx)},{fmt(my + 0.06 * R)} '
            f'Q{fmt(mx - 0.10 * R)},{fmt(my + 0.05 * R)} {fmt(mx - w)},{fmt(my + 0.08 * R)} Z" '
            f'fill="{col}" {_st(2.4)}/>')


# ---------------------------------------------------------------- headwear (head frame)


def _cloth_cap(R, col, edge=None):
    """Head-cloth / veil covering top and back of head; front edge across the forehead."""
    pts = [(0.94 * R, -0.34 * R), (0.80 * R, -0.80 * R), (0.25 * R, -1.10 * R), (-0.45 * R, -1.04 * R),
           (-0.98 * R, -0.62 * R), (-1.14 * R, 0.05 * R), (-1.10 * R, 0.62 * R), (-0.80 * R, 0.72 * R),
           (-0.64 * R, 0.30 * R), (-0.62 * R, -0.22 * R), (-0.20 * R, -0.48 * R), (0.45 * R, -0.50 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.6)}/>'
    s += _line(f"M{fmt(-0.30 * R)},{fmt(-0.88 * R)} Q{fmt(-0.78 * R)},{fmt(-0.45 * R)} {fmt(-0.86 * R)},{fmt(0.40 * R)}",
               w=2.2, col=shade(col, -0.22))
    if edge:
        s += _tube(_spline_pts([(0.97 * R, -0.37 * R), (0.45 * R, -0.58 * R), (-0.18 * R, -0.54 * R),
                                (-0.64 * R, -0.22 * R), (-0.70 * R, 0.25 * R)]), 0.15 * R, edge, ow=2.4)
    return s


def _spline_pts(pts, steps=6):
    """Catmull-Rom sampled points (open curve) for tubes."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        for j in range(steps):
            t = j / steps
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def _headband(R, col, tails=True):
    s = ""
    if tails:
        s += _tube([(-0.92 * R, -0.25 * R), (-1.25 * R, 0.10 * R), (-1.32 * R, 0.42 * R)], 0.10 * R, col, ow=2.4)
        s += _tube([(-0.92 * R, -0.25 * R), (-1.10 * R, 0.25 * R), (-1.08 * R, 0.55 * R)], 0.10 * R, col, ow=2.4)
    s += _tube(_spline_pts([(0.98 * R, -0.40 * R), (0.45 * R, -0.58 * R), (-0.25 * R, -0.56 * R),
                            (-0.92 * R, -0.25 * R)]), 0.15 * R, col, ow=2.6)
    return s


def _knit_cap(R, col):
    dome = [(0.92 * R, -0.40 * R), (0.80 * R, -0.88 * R), (0.20 * R, -1.22 * R), (-0.55 * R, -1.12 * R),
            (-1.0 * R, -0.58 * R), (-1.02 * R, -0.22 * R)]
    s = f'<path d="{smooth_path(dome + [(0.0, -0.50 * R)])}" fill="{col}" {_st(3.4)}/>'
    s += _tube(_spline_pts([(0.98 * R, -0.42 * R), (0.40 * R, -0.60 * R), (-0.35 * R, -0.56 * R),
                            (-1.02 * R, -0.20 * R)]), 0.18 * R, shade(col, -0.15), ow=2.6)
    for x in (-0.45, -0.05, 0.35):
        s += _line(f"M{fmt(x * R)},{fmt(-0.74 * R)} Q{fmt((x + 0.06) * R)},{fmt(-0.96 * R)} {fmt((x + 0.02) * R)},"
                   f"{fmt(-1.10 * R)}", w=2.0, col=shade(col, -0.25))
    s += f'<circle cx="{fmt(-0.05 * R)}" cy="{fmt(-1.24 * R)}" r="{fmt(0.13 * R)}" fill="{shade(col, 0.2)}" {_st(2.6)}/>'
    return s


def _sea_cap(R, col):
    """Captain's short rounded seaman's cap: soft dome, rolled brim, small knot at the back."""
    dome = [(0.95 * R, -0.42 * R), (0.88 * R, -0.86 * R), (0.42 * R, -1.18 * R), (-0.30 * R, -1.20 * R),
            (-0.86 * R, -0.92 * R), (-1.06 * R, -0.42 * R), (-1.04 * R, -0.20 * R), (0.0, -0.52 * R)]
    s = f'<path d="{smooth_path(dome)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(-0.55 * R)},{fmt(-1.02 * R)} Q{fmt(0.10 * R)},{fmt(-1.10 * R)} {fmt(0.70 * R)},{fmt(-0.86 * R)}",
               w=2.2, col=shade(col, -0.28))
    s += _tube(_spline_pts([(1.0 * R, -0.42 * R), (0.40 * R, -0.62 * R), (-0.35 * R, -0.58 * R),
                            (-1.06 * R, -0.22 * R)]), 0.19 * R, shade(col, -0.2), ow=2.6)
    s += _tube([(-1.02 * R, -0.30 * R), (-1.22 * R, -0.02 * R), (-1.18 * R, 0.22 * R)], 0.12 * R, shade(col, -0.2),
               ow=2.4)
    s += f'<circle cx="{fmt(-1.02 * R)}" cy="{fmt(-0.32 * R)}" r="{fmt(0.12 * R)}" fill="{shade(col, -0.1)}" {_st(2.4)}/>'
    return s


def _crown(R, col=GOLD, x0=0.0, y0=0.0, k=1.0, tilt=0.0):
    """Tall Assyrian crown (truncated cone with small top spike). Base centre at (x0, y0).

    tilt 0..1 shows more of the top rim (crown tipped toward the viewer, e.g. when held)."""
    def q(x, y):
        return f"{fmt(x0 + x * R * k)},{fmt(y0 + y * R * k)}"
    dark = GOLD_DARK
    rt = 0.15 + 0.22 * tilt          # depth of the rim curves
    rb = 0.18 + 0.12 * tilt
    s = (f'<path d="M{q(-0.72, 0.02)} L{q(-0.62, -1.15)} Q{q(0.05, -1.15 - rt)} {q(0.72, -1.15)} L{q(0.82, 0.02)} '
         f'Q{q(0.05, 0.02 + rb)} {q(-0.72, 0.02)} Z" fill="{col}" {_st(3.4)}/>')
    s += (f'<path d="M{q(-0.62, -1.15)} Q{q(0.05, -1.15 + rt)} {q(0.72, -1.15)} Q{q(0.05, -1.15 - rt)} {q(-0.62, -1.15)} Z" '
          f'fill="{shade(col, 0.18)}" {_st(2.6)}/>')
    s += (f'<path d="M{q(-0.10, -1.15 - rt * 0.4)} L{q(0.06, -1.62 - rt * 0.4)} L{q(0.22, -1.15 - rt * 0.4)} Z" '
          f'fill="{col}" {_st(2.8)}/>')
    for yy in (-0.32, -0.80):
        s += _line(f"M{q(-0.70, yy)} Q{q(0.05, yy + 0.16 + 0.1 * tilt)} {q(0.80, yy)}", w=2.4, col=dark)
    for xx in (-0.40, 0.05, 0.50):
        yy = -0.52 + (0.06 + 0.08 * tilt if xx == 0.05 else 0.0)
        s += (f'<circle cx="{fmt(x0 + xx * R * k)}" cy="{fmt(y0 + yy * R * k)}" r="{fmt(0.10 * R * k)}" '
              f'fill="{P["royal_light"]}" {_st(2.0)}/>')
    return s


def _wrap(R, col, stripe=None):
    """Simple wrapped cap (townspeople / elders)."""
    pts = [(0.94 * R, -0.38 * R), (0.75 * R, -0.97 * R), (0.0, -1.20 * R), (-0.80 * R, -0.97 * R),
           (-1.04 * R, -0.32 * R), (-0.5 * R, -0.54 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    for yy in (-0.66, -0.90):
        s += _line(f"M{fmt(-0.95 * R)},{fmt((yy + 0.28) * R)} Q{fmt(0.0)},{fmt((yy - 0.22) * R)} {fmt(0.88 * R)},"
                   f"{fmt(yy * R)}", w=2.2, col=shade(col, -0.22))
    s += _tube(_spline_pts([(0.98 * R, -0.40 * R), (0.40 * R, -0.57 * R), (-0.35 * R, -0.53 * R),
                            (-1.04 * R, -0.24 * R)]), 0.14 * R, stripe or shade(col, -0.15), ow=2.4)
    return s


# ---------------------------------------------------------------- headwear for the Daniel film (head frame)


def _tall_hat(R, col, band):
    """Persian official's tall rounded felt hat: a soft fluted cylinder, slightly wider at the rounded top."""
    pts = [(0.95 * R, -0.40 * R), (0.92 * R, -1.10 * R), (0.86 * R, -1.72 * R), (0.45 * R, -2.02 * R),
           (-0.30 * R, -2.04 * R), (-0.84 * R, -1.76 * R), (-0.94 * R, -1.10 * R), (-1.02 * R, -0.30 * R),
           (-0.45 * R, -0.50 * R), (0.20 * R, -0.56 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    fl = shade(col, -0.2)
    for x0 in (-0.55, -0.18, 0.20, 0.56):        # soft vertical flutes
        s += _line(f"M{fmt(x0 * R)},{fmt(-0.62 * R)} Q{fmt((x0 + 0.04) * R)},{fmt(-1.30 * R)} {fmt(x0 * 0.9 * R)},"
                   f"{fmt(-1.90 * R)}", w=2.2, col=fl)
    s += _line(f"M{fmt(-0.55 * R)},{fmt(-1.86 * R)} Q{fmt(0.05 * R)},{fmt(-1.98 * R)} {fmt(0.62 * R)},{fmt(-1.80 * R)}",
               w=2.0, col=shade(col, 0.25))
    s += _tube(_spline_pts([(0.98 * R, -0.46 * R), (0.40 * R, -0.62 * R), (-0.35 * R, -0.58 * R),
                            (-1.02 * R, -0.36 * R)]), 0.20 * R, band, ow=2.6)
    for x0, y0 in ((0.62, -0.57), (0.05, -0.64), (-0.55, -0.55)):
        s += f'<circle cx="{fmt(x0 * R)}" cy="{fmt(y0 * R)}" r="{fmt(0.055 * R)}" fill="{shade(band, 0.35)}"/>'
    return s


def _turban(R, col, band):
    """Rounded wrapped turban with a jewel at the front and a short tail at the back."""
    s = _tube([(-0.98 * R, -0.42 * R), (-1.26 * R, -0.05 * R), (-1.22 * R, 0.30 * R)], 0.22 * R, shade(col, -0.08),
              ow=2.6)
    pts = [(0.98 * R, -0.36 * R), (1.08 * R, -0.86 * R), (0.66 * R, -1.38 * R), (-0.10 * R, -1.52 * R),
           (-0.90 * R, -1.24 * R), (-1.18 * R, -0.60 * R), (-1.04 * R, -0.20 * R), (-0.50 * R, -0.50 * R),
           (0.25 * R, -0.56 * R)]
    s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    wl = shade(col, -0.22)
    for k in range(4):
        y0 = -0.66 - 0.20 * k
        s += _line(f"M{fmt(-1.02 * R)},{fmt((y0 + 0.30) * R)} Q{fmt(-0.10 * R)},{fmt((y0 - 0.30) * R)} "
                   f"{fmt(1.00 * R)},{fmt((y0 - 0.02) * R)}", w=2.2, col=wl)
    s += (f'<path d="M{fmt(0.66 * R)},{fmt(-0.96 * R)} Q{fmt(0.40 * R)},{fmt(-1.30 * R)} {fmt(0.52 * R)},{fmt(-1.58 * R)} '
          f'Q{fmt(0.84 * R)},{fmt(-1.30 * R)} {fmt(0.66 * R)},{fmt(-0.96 * R)} Z" fill="{shade(band, 0.25)}" {_st(2.4)}/>')
    s += _line(f"M{fmt(0.66 * R)},{fmt(-0.98 * R)} Q{fmt(0.58 * R)},{fmt(-1.28 * R)} {fmt(0.54 * R)},{fmt(-1.50 * R)}",
               w=1.8, col=shade(band, -0.3))
    s += _ell(0.70 * R, -0.80 * R, 0.17 * R, 0.20 * R, band, sw=2.6)
    s += _ell(0.70 * R, -0.80 * R, 0.07 * R, 0.08 * R, shade(band, 0.35))
    return s


def _darius_crown(R, x0=0.0, y0=0.0, k=1.0):
    """King Darius' crown: a tall gold band with stepped crenellations on top and a row of jewels."""
    def q(x, y):
        return f"{fmt(x0 + x * R * k)},{fmt(y0 + y * R * k)}"
    gold, dark = GOLD, GOLD_DARK
    xl, xr, yt, mh = -0.80, 0.90, -1.12, 0.34
    s = (f'<path d="M{q(xl + 0.02, yt)} Q{q(0.05, yt - 0.22)} {q(xr - 0.02, yt)} L{q(xr - 0.02, yt + 0.08)} '
         f'L{q(xl + 0.02, yt + 0.08)} Z" fill="{dark}" {_st(2.6)}/>')       # the inner back rim
    n = 4
    w = (xr - xl) / (n + (n - 1) * 0.55)
    top = f"M{q(xl - 0.02, 0.02)} L{q(xl, yt)}"
    for i in range(n):
        a = xl + i * w * 1.55
        st_ = w / 4
        top += (f" L{q(a, yt - mh * 0.45)} L{q(a + st_, yt - mh * 0.45)} L{q(a + st_, yt - mh)} "
                f"L{q(a + w - st_, yt - mh)} L{q(a + w - st_, yt - mh * 0.45)} L{q(a + w, yt - mh * 0.45)} "
                f"L{q(a + w, yt)}")
        if i < n - 1:
            top += f" Q{q(a + w * 1.275, yt + 0.05)} {q(a + w * 1.55, yt)}"
    top += f" L{q(xr + 0.02, 0.02)} Q{q(0.05, 0.22)} {q(xl - 0.02, 0.02)} Z"
    s += f'<path d="{top}" fill="{gold}" {_st(3.4)}/>'
    s += _line(f"M{q(xl, -0.22)} Q{q(0.05, -0.04)} {q(xr, -0.22)}", w=2.4, col=dark)
    s += _line(f"M{q(xl, -0.86)} Q{q(0.05, -0.70)} {q(xr, -0.86)}", w=2.4, col=dark)
    for i, xx in enumerate((-0.52, -0.12, 0.30, 0.68)):
        yy = -0.52 + (0.07 if 0 < i < 3 else 0.02)
        col = P["royal_light"] if i % 2 == 0 else "#4f86b0"
        s += f'<circle cx="{fmt(x0 + xx * R * k)}" cy="{fmt(y0 + yy * R * k)}" r="{fmt(0.11 * R * k)}" fill="{col}" {_st(2.0)}/>'
    return s


def _helmet(R, col, plume):
    """Palace guard's rounded bronze helmet with a brim band, a back neck flap and a little plume."""
    s = _tube([(-0.05 * R, -1.20 * R), (-0.25 * R, -1.50 * R), (-0.60 * R, -1.58 * R)], 0.17 * R, plume, ow=2.4)
    pts = [(0.96 * R, -0.40 * R), (0.92 * R, -0.84 * R), (0.45 * R, -1.20 * R), (-0.25 * R, -1.24 * R),
           (-0.86 * R, -0.96 * R), (-1.10 * R, -0.42 * R), (-1.12 * R, 0.10 * R), (-0.80 * R, 0.12 * R),
           (-0.62 * R, -0.36 * R), (0.10 * R, -0.54 * R)]
    s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(-0.55 * R)},{fmt(-1.00 * R)} Q{fmt(0.05 * R)},{fmt(-1.16 * R)} {fmt(0.62 * R)},{fmt(-0.92 * R)}",
               w=3.0, col=shade(col, 0.35))
    s += _tube(_spline_pts([(1.0 * R, -0.42 * R), (0.40 * R, -0.62 * R), (-0.35 * R, -0.58 * R),
                            (-1.00 * R, -0.30 * R)]), 0.16 * R, shade(col, -0.22), ow=2.6)
    s += f'<circle cx="{fmt(-0.05 * R)}" cy="{fmt(-1.22 * R)}" r="{fmt(0.10 * R)}" fill="{shade(col, -0.1)}" {_st(2.4)}/>'
    return s


# ======================================================================= hands & feet


def _hand(W, d, style, skin, hr):
    """Hand at wrist W, forearm direction d (unit)."""
    if style == "none":
        return ""
    pp = _rot(d, -90)
    st = _st(3.2)
    if style == "fist":
        c = _add(W, _mul(d, 0.45 * hr))
        return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'
    if style == "open":
        c = _add(W, _mul(d, 0.75 * hr))
        a = _ang(d)
        th = _add(_add(W, _mul(d, 0.45 * hr)), _mul(pp, 0.85 * hr))
        return (f'<ellipse cx="{fmt(th[0])}" cy="{fmt(th[1])}" rx="{fmt(0.42 * hr)}" ry="{fmt(0.32 * hr)}" '
                f'transform="rotate({fmt(a - 30)} {fmt(th[0])} {fmt(th[1])})" fill="{skin}" {st}/>'
                f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(1.22 * hr)}" ry="{fmt(0.88 * hr)}" '
                f'transform="rotate({fmt(a)} {fmt(c[0])} {fmt(c[1])})" fill="{skin}" {st}/>')
    if style == "cup":            # hand cupped behind the ear: fingers up, hollow opening toward +x
        c = _add(W, (0.15 * hr, -0.85 * hr))
        return (_ell(c[0], c[1], 0.88 * hr, 1.30 * hr, skin, sw=3.2,
                     extra=f'transform="rotate(12 {fmt(c[0])} {fmt(c[1])})"') +
                _line(f"M{fmt(c[0] + 0.45 * hr)},{fmt(c[1] - 0.85 * hr)} Q{fmt(c[0] - 0.55 * hr)},{fmt(c[1] - 0.1 * hr)} "
                      f"{fmt(c[0] + 0.35 * hr)},{fmt(c[1] + 0.85 * hr)}", w=2.2))
    if style == "palm":           # open palm facing out, fingers up ('stop')
        c = _add(W, (0, -0.7 * hr))
        s = (f'<ellipse cx="{fmt(c[0] - 0.85 * hr)}" cy="{fmt(c[1] + 0.25 * hr)}" rx="{fmt(0.42 * hr)}" '
             f'ry="{fmt(0.30 * hr)}" transform="rotate(-35 {fmt(c[0] - 0.85 * hr)} {fmt(c[1] + 0.25 * hr)})" '
             f'fill="{skin}" {st}/>')
        s += _ell(c[0], c[1], 0.95 * hr, 1.25 * hr, skin, sw=3.2)
        for dx in (-0.32, 0.0, 0.32):
            s += _line(f"M{fmt(c[0] + dx * hr)},{fmt(c[1] - 1.18 * hr)} l0,{fmt(0.55 * hr)}", w=2.0)
        return s
    if style == "ground":         # palm flat on the ground, fingers pointing away from the body
        sx = 1 if d[0] >= 0 else -1
        c = _add(W, (sx * 0.55 * hr, 0.25 * hr))
        return _ell(c[0], c[1], 1.30 * hr, 0.62 * hr, skin, sw=3.2)
    if style == "pillow":         # both palms together, lying flat under a sleeping cheek
        s = ""
        for dy, dx in ((0.62, 0.2), (-0.55, -0.15)):
            c = _add(W, (dx * hr, dy * hr))
            s += _ell(c[0], c[1], 1.55 * hr, 0.66 * hr, skin, sw=3.2,
                      extra=f'transform="rotate(-6 {fmt(c[0])} {fmt(c[1])})"')
        return s
    if style == "point":
        c = _add(W, _mul(d, 0.45 * hr))
        tip = _add(W, _mul(d, 2.2 * hr))
        base = _add(W, _mul(d, 0.9 * hr))
        return (_tube([base, tip], 0.62 * hr, skin, ow=3.0) +
                f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>')
    if style == "pray":           # two palms pressed together, fingertips up
        c = W
        return (f'<path d="M{fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Q{fmt(c[0] + 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} '
                f'{fmt(c[0] + 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} L{fmt(c[0] - 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} '
                f'Q{fmt(c[0] - 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} {fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Z" '
                f'fill="{skin}" {st}/>' +
                _line(f"M{fmt(c[0])},{fmt(c[1] - 1.7 * hr)} L{fmt(c[0])},{fmt(c[1] + 0.5 * hr)}", w=2.0))
    c = _add(W, _mul(d, 0.45 * hr))
    return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'


_SOLE = ((-0.40, 0.40), (1.02, 0.40), (-0.34, 0.20), (0.95, 0.12))
_SOLE_BARE = ((-0.34, 0.24), (0.85, 0.30), (0.15, 0.30), (0.95, 0.12))


def _sole_off(fa, fl, bare=False):
    """How far below the ankle the lowest point of a foot at angle ``fa`` reaches."""
    return max(_rot((x * fl, y * fl), fa)[1] for x, y in (_SOLE_BARE if bare else _SOLE)) + 1.5


def _foot(A, ang, skin, fl, sandal=SANDAL, bare=False):
    """Foot at ankle A pointing along screen angle ``ang`` (0 = +x). Returns (svg, sole points)."""
    def q(x, y):
        v = _rot((x, y), ang)
        return (A[0] + v[0], A[1] + v[1])
    foot = [q(-0.30 * fl, -0.15 * fl), q(-0.34 * fl, 0.20 * fl), q(0.15 * fl, 0.30 * fl), q(0.85 * fl, 0.30 * fl),
            q(0.95 * fl, 0.12 * fl), q(0.60 * fl, -0.08 * fl), q(0.05 * fl, -0.26 * fl)]
    s = ""
    if not bare:
        sole = [q(-0.40 * fl, 0.24 * fl), q(1.00 * fl, 0.24 * fl), q(1.02 * fl, 0.40 * fl), q(-0.40 * fl, 0.40 * fl)]
        s += f'<path d="{smooth_path(sole)}" fill="{sandal}" {_st(3.0)}/>'
    s += f'<path d="{smooth_path(foot)}" fill="{skin}" {_st(3.0)}/>'
    if not bare:
        s += _tube([q(0.30 * fl, -0.12 * fl), q(0.40 * fl, 0.24 * fl)], 0.12 * fl, sandal, ow=1.8)
    soles = [q(x * fl, y * fl) for x, y in (_SOLE_BARE if bare else _SOLE)]
    return s, soles


# ======================================================================= poses


def _P(**kw):
    """Pose record. Keys:
    t, h      torso tilt / extra head tilt in degrees (+ = leaning forward / looking down)
    legs      per leg (far, near): (thigh_deg, shin_deg) forward kinematics, or ("ik", ankle_dx, knee[, lift])
              = foot planted on the ground at x = ankle_dx (knee +1 bends forward / up, 0 straight)
    arms      per arm (far, near): ("fk", upper_deg, fore_deg) or ("ik", target_kind, x, y, bend)
    ground    'feet' (soles on the ground), 'seat' (sitting on the ground), 'body' (lying), 'air'
    lap       seated robe built from a thigh hull and a shin hull
    drop      pelvis lowered by this many px (crouch) for 'ik' legs
    held      lying on raised hands, not on the floor (water drops may fall below the anchor line)
    """
    base = dict(t=0, h=0, legs=((3, 1), (-3, -1)), arms=(("fk", 8, 3), ("fk", -8, -3)),
                hands=("fist", "fist"), ground="feet", lap=False, drop=0, hem=None, flare=0,
                far_front=False, near_back=False, tail=None, flip=False, spin=0, marks=(),
                expr="neutral", look=(0, 0), feet=(None, None), far_over_head=False, fan_arm=0,
                billow=0, sash_dir=None, flat_back=False, near_hidden=False, reach=1.0, held=False)
    base.update(kw)
    return base


_SEATED = dict(ground="seat", lap=True, hem=0.97, flare=-10)

POSES = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -58, -46), ("fk", 26, 46))),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 48), ("fk", -24, -14))),
    "run_a": _P(t=14, legs=((58, 22), (-24, -118)), arms=(("fk", -82, -42), ("fk", 62, 128)),
                hem=0.66, tail=-102, flare=-4),
    "run_b": _P(t=14, legs=((-24, -118), (58, 22)), arms=(("fk", 62, 128), ("fk", -60, -20)),
                hem=0.66, tail=-102, flare=-4),
    "sleep": _P(t=-80, h=22, ground="body", flat_back=True, legs=(("ik", 40, 1), ("ik", 58, 1)),
                arms=(("ik", "pillow", 0.30, 0, 1), ("ik", "pillow", 0.10, 0, 1)),
                hands=("pillow", "none"), far_front=True, near_hidden=True, tail=(-40, -92),
                expr="sleepy", marks=("zzz",), hem=0.97, flare=-6),
    "kneel_pray": _P(t=-4, h=-16, legs=((4, -88), (0, -92)),
                     arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)),
                     hands=("none", "pray"), expr="peaceful", feet=(100, 100), hem=0.97),
    "sit": _P(t=-3, legs=(("ik", 80, 1), ("ik", 90, 1)),
              arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), **_SEATED),
    "sit_sulk": _P(t=-2, h=12, legs=(("ik", 76, 1), ("ik", 86, 1)),
                   arms=(("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
                   far_front=True, expr="angry", **_SEATED),
    "sit_faint": _P(t=-12, h=40, legs=(("ik", 84, 1), ("ik", 112, 1)),
                    arms=(("ik", "headw", 0.62, 1.12, 1), ("ik", "ground", -66, 0, -1)),
                    hands=("open", "ground"), far_front=True, marks=("fan",), fan_arm=0, expr="tired", **_SEATED),
    "sit_happy": _P(t=-6, h=-6, legs=(("ik", 112, 1), ("ik", 120, 1)),
                    arms=(("fk", 118, 145), ("fk", -112, -140)), hands=("open", "open"), expr="happy", **_SEATED),
    "preach": _P(t=-3, h=-6, legs=((8, 3), (-7, -3)),
                 arms=(("fk", 152, 168), ("fk", 30, 74)), hands=("open", "open"), expr="call"),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 84, 88), ("fk", -8, -3)), hands=("point", "fist")),
    "arms_up": _P(h=-6, arms=(("fk", 150, 168), ("fk", -150, -168)), hands=("open", "open"), expr="happy"),
    # fall: tumbling (body tilted 58 deg forward), arms flung up, knees bent with the near foot kicked up,
    # robe blown up to the shins, flap and sash streaming upward (limb angles are body-frame, before the spin)
    "fall": _P(spin=58, ground="air", legs=((85, -30), (0, -95)), arms=(("fk", -150, -122), ("fk", -90, -112)),
               hands=("open", "open"), tail=(-105, -140), expr="scared", billow=30, sash_dir=-115, hem=0.70),
    "float": _P(spin=18, ground="air", h=-4, legs=((22, -22), (-6, -40)), arms=(("fk", 108, 126), ("fk", -102, -120)),
                hands=("open", "open"), tail=(-100, -140), expr="scared", billow=22, sash_dir=150, hem=0.86),
    "refuse": _P(flip=True, t=-4, h=8, legs=((14, 4), (-10, -14)),
                 arms=(("fk", 8, 3), ("fk", -74, -92)), hands=("fist", "palm"), marks=("shake",),
                 expr="angry", tail=-30),
    "confess": _P(t=6, h=18, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
                  expr="sorry"),
    "listen": _P(h=-14, arms=(("fk", 14, 8), ("ik", "head", -0.66, 0.16, -1)), hands=("fist", "cup"),
                 look=(0.03, -0.08), marks=("sound",)),
    # carried: lying on his back, held up by the sailors (Jonah 1:15); underside flat on the anchor line
    "carried": _P(t=-86, h=46, ground="body", flat_back=True, legs=(("ik", 110, 1), ("ik", 124, 1)),
                  arms=(("fk", 6, 2), ("ik", "torso", 0.5, 0.62, 1)), hands=("open", "open"), tail=(-10, 5),
                  expr="worried", hem=0.90, flare=-4, held=True),
    "wake": _P(t=2, h=-4, legs=(("ik", 108, 1), ("ik", 116, 1)),
               arms=(("fk", 148, 172), ("ik", "head", -0.14, 0.10, -1)), hands=("open", "fist"),
               expr="sleepy", **_SEATED),
    # ---- generic poses used by the other characters
    "scared": _P(t=-4, legs=((10, 2), (-8, -4)),
                 arms=(("ik", "headw", 1.15, 0.45, 1), ("ik", "headw", -1.15, 0.45, -1)),
                 hands=("open", "open"), expr="scared"),
    "throw": _P(t=-14, h=-16, drop=4, legs=(("ik", 40, 1), ("ik", -34, 1)), reach=1.12,
                arms=(("ik", "abs", 58, -330, 1), ("ik", "abs", 40, -338, -1)), hands=("open", "open"),
                near_back=True, expr="worried"),
    "carry": _P(t=16, drop=28, legs=(("ik", 40, 1), ("ik", -28, 1)),
                arms=(("ik", "abs", 92, -112, 1), ("ik", "abs", 74, -104, 1)), expr="worried"),
    "pray": _P(t=-6, h=-20, arms=(("fk", 158, 172), ("fk", -158, -172)), hands=("open", "open"),
               expr="scared", look=(0.02, -0.06)),
    "pull": _P(t=-24, drop=18, legs=(("ik", 66, 0), ("ik", -20, 1)),
               arms=(("ik", "abs", 80, -166, 1), ("ik", "abs", 34, -152, 1)), expr="angry"),
    "lift": _P(t=-2, h=-12, legs=((12, 2), (-10, -2)), arms=(("fk", 150, 174), ("fk", -150, -178)),
               hands=("open", "open"), expr="worried"),
    "wake_other": _P(t=40, h=-12, drop=40, legs=(("ik", 56, 1), ("ik", -26, 1)),
                     arms=(("fk", 30, 50), ("ik", "abs", 112, -92, 1)), hands=("fist", "open"), expr="worried"),
    "worried": _P(t=-2, arms=(("ik", "head", 0.80, -0.78, 1), ("ik", "head", -0.80, -0.75, -1)),
                  hands=("open", "open"), expr="worried", far_over_head=True),
    "sit_throne": _P(t=-2, lap=True, legs=((86, 4), (82, 2)),
                     arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), hem=0.97, flare=-8),
    "sit_ashes": _P(t=6, h=26, legs=(("ik", 80, 1), ("ik", 90, 1)),
                    arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), expr="sad", **_SEATED),
    "remove_crown": _P(t=-2, h=8, arms=(("ik", "torso", 1.55, 0.58, 1), ("ik", "torso", 1.15, 0.60, 1)),
                       expr="sorry"),
    "walk": None,          # alias -> walk_a (filled below)
    "sad": _P(t=6, h=24, arms=(("fk", 6, 2), ("fk", -6, -2)), expr="sad"),
    "cheer": _P(h=-8, legs=((10, 4), (-8, -2)), arms=(("fk", 128, 150), ("fk", -132, -155)),
                hands=("open", "open"), expr="happy"),
    "listen_chin": _P(h=-6, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
                      expr="worried"),
}
POSES["walk"] = POSES["walk_a"]

# ---- Daniel film (Daniel 6): Daniel, King Darius, the officials and the palace guards
_KNEEL = dict(legs=((4, -88), (0, -92)), feet=(100, 100), hem=0.97)
POSES.update({
    "explain": _P(h=-2, arms=(("fk", 12, 6), ("fk", 30, 80)), hands=("fist", "open"), expr="happy"),
    "look_up": _P(h=-24, arms=(("fk", 20, 30), ("fk", -18, -26)), hands=("open", "open"), look=(0.03, -0.10),
                  expr="happy"),
    "answer": _P(h=-22, arms=(("fk", 152, 168), ("fk", 20, 40)), hands=("open", "open"), look=(0.03, -0.10),
                 expr="call"),
    "bow": _P(t=18, h=18, legs=((6, 2), (-4, -2)), arms=(("fk", 26, 20), ("ik", "torso", 0.55, 0.74, 1)),
              hands=("fist", "open"), expr="peaceful"),
    "bow_low": _P(t=32, h=8, legs=((6, 2), (-4, -2)), arms=(("ik", "abs", 64, -196, 1), ("ik", "abs", 60, -188, 1)),
                  hands=("none", "fist"), expr="smug"),
    "kneel_up": _P(t=-6, h=-22, arms=(("fk", 148, 166), ("fk", -150, -170)), hands=("open", "open"),
                   look=(0.02, -0.06), expr="happy", **_KNEEL),
    "kneel_bow": _P(t=8, h=18, arms=(("ik", "torso", 1.55, 0.62, 1), ("ik", "torso", 1.55, 0.62, 1)),
                    hands=("none", "pray"), expr="peaceful", **_KNEEL),
    "sit_pray": _P(t=-3, h=-10, legs=(("ik", 80, 1), ("ik", 90, 1)),
                   arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)),
                   hands=("none", "pray"), expr="peaceful", **_SEATED),
    "read": _P(h=14, arms=(("ik", "body", 96, -60, 1), ("ik", "body", 34, -54, 1)), hands=("fist", "fist"),
               look=(0.03, 0.07)),
    "hold_rope": _P(h=-14, legs=((8, 2), (-6, -10)), arms=(("ik", "body", 66, -112, 1),
                                                           ("ik", "body", 62, -80, 1)),
                    hands=("fist", "fist"), expr="happy", look=(0.02, -0.05)),
    "whisper": _P(t=10, h=-2, legs=((8, 3), (-6, -2)), arms=(("fk", 8, 3), ("ik", "head", 1.08, 0.50, 1)),
                  hands=("fist", "open"), expr="sly"),
    "peek": _P(t=22, h=-16, drop=14, legs=(("ik", 30, 1), ("ik", -32, 1)),
               arms=(("ik", "abs", 96, -212, 1), ("ik", "abs", 78, -190, 1)), hands=("open", "open"),
               expr="sly", look=(0.04, -0.02)),
    "scheme": _P(h=6, arms=(("ik", "torso", 1.45, 0.45, 1), ("ik", "torso", 1.45, 0.45, 1)),
                 hands=("none", "fist"), expr="sly"),
    "sign": _P(h=12, arms=(("ik", "body", 74, -84, 1), ("ik", "body", 62, -40, 1)), hands=("fist", "fist"),
               look=(0.03, 0.06)),
    "sit_sign": _P(t=-2, h=12, lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8,
                   arms=(("ik", "body", 82, -76, 1), ("ik", "body", 70, -38, 1)), hands=("fist", "fist"),
                   look=(0.03, 0.06)),
    "sad_head": _P(t=4, h=22, arms=(("ik", "head", 0.78, -0.50, 1), ("fk", -6, -2)), hands=("open", "fist"),
                   far_over_head=True, expr="sad"),
    "sit_sad": _P(t=14, h=16, lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8,
                  arms=(("ik", "knee", 0, 0.25, 1), ("ik", "head", 0.42, 1.05, 1)), hands=("fist", "fist"),
                  expr="sad"),
    "pace_a": _P(t=6, h=14, legs=((24, 8), (-20, -34)),
                 arms=(("ik", "torso", -1.35, 0.32, -1), ("ik", "torso", -1.35, 0.32, -1)), hands=("none", "fist"),
                 expr="worried"),
    "pace_b": _P(t=6, h=14, legs=((-20, -34), (24, 8)),
                 arms=(("ik", "torso", -1.35, 0.32, -1), ("ik", "torso", -1.35, 0.32, -1)), hands=("none", "fist"),
                 expr="worried"),
    "call_out": _P(t=16, h=10, legs=((10, 3), (-8, -3)), arms=(("fk", 66, 82), ("fk", 72, 90)), hands=("open", "open"),
                   expr="call"),
    "reach_out": _P(t=4, legs=((10, 3), (-8, -3)), arms=(("fk", 74, 84), ("fk", 80, 94)), hands=("open", "open"),
                    expr="happy"),
    "hug": _P(t=6, h=4, legs=((10, 3), (-8, -3)), arms=(("ik", "abs", 104, -236, 1), ("ik", "abs", 92, -218, 1)),
              hands=("open", "open"), expr="happy"),
    "guard_stand": _P(arms=(("fk", 14, 8), ("fk", 48, 80))),
    "guard_walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -46, -36), ("fk", 48, 80))),
    "guard_walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 46), ("fk", 48, 80))),
    "push": _P(t=26, drop=24, legs=(("ik", 52, 1), ("ik", -52, 0)),
               arms=(("fk", 86, 92), ("fk", 80, 88)), hands=("palm", "palm"),
               expr="worried"),
    "pull_rope": _P(t=-24, drop=18, legs=(("ik", 66, 0), ("ik", -20, 1)),
                    arms=(("ik", "abs", 80, -166, 1), ("ik", "abs", 34, -152, 1)), expr="happy"),
})


# ======================================================================= the rig


def _ik(S, T, L1, L2, bend):
    d = _sub(T, S)
    dist = _len(d)
    dn = _nrm(d) if dist > 1e-6 else (0.0, 1.0)
    dist = max(min(dist, (L1 + L2) * 0.999), abs(L1 - L2) + 1.0)
    a = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
    hh = math.sqrt(max(L1 * L1 - a * a, 0.0))
    perp = (-dn[1], dn[0])
    E = _add(_add(S, _mul(dn, a)), _mul(perp, hh * bend))
    W = _add(S, _mul(dn, dist))
    return E, W


def _leg_ik(H, tx, ty, L1, L2, knee):
    """Knee and ankle with the ankle on (tx, ty). If that is out of reach, tx slides toward the hip so the
    foot still reaches the ground line ty. knee: +1 knee forward / up, -1 backward, 0 straight."""
    L = (L1 + L2) * 0.995
    dy = ty - H[1]
    if abs(dy) >= L:
        tx, ty = H[0], H[1] + math.copysign(L, dy)
    else:
        dxm = math.sqrt(L * L - dy * dy)
        tx = max(H[0] - dxm, min(H[0] + dxm, tx))
    if knee == 0:
        A = (tx, ty)
        d = _nrm(_sub(A, H))
        dist = min(_len(_sub(A, H)), L1 + L2)
        A = _add(H, _mul(d, dist))
        return _add(H, _mul(d, dist * L1 / (L1 + L2))), A
    return _ik(H, (tx, ty), L1, L2, -knee)


def _leg_point(H, K, A, th, d):
    """Point at distance d along the leg polyline hip->knee->ankle, plus local direction."""
    if d <= th:
        dirv = _nrm(_sub(K, H))
        return _add(H, _mul(dirv, d)), dirv, True
    dirv = _nrm(_sub(A, K))
    return _add(K, _mul(dirv, d - th)), dirv, False


def _tail_dirs(ps, ha):
    """Head-cloth flap: start direction d0 and end direction d1 (body frame)."""
    spec = ps["tail"]
    if isinstance(spec, tuple):
        return _dv(spec[0]), _dv(spec[1])
    d0 = _nrm(_rot((-0.30, 1.0), ha))
    d1 = _dv(spec) if spec is not None else _nrm(_add(d0, _dv(-10)))
    return d0, d1


def _billow(poly, Hm, um, amt, seed=0):
    """Replace the hem edge of a skirt polygon by a wide, wavy edge whose corners lift (cloth flying up).
    Returns (new polygon, hem edge polyline)."""
    nv = (-um[1], um[0])
    cut = _sub(Hm, _mul(um, amt * 0.7))
    top = _clip(poly, cut, _mul(um, -1))
    if len(top) < 3:
        return poly, []
    on = [abs(_dot(_sub(p, cut), um)) < 0.6 for p in top]
    idx = None
    for i in range(len(top)):
        if on[i] and on[(i + 1) % len(top)]:
            idx = i
            break
    if idx is None:
        return poly, []
    p0, p1 = top[idx], top[(idx + 1) % len(top)]
    a, b = (p0, p1) if _dot(_sub(p0, cut), nv) < _dot(_sub(p1, cut), nv) else (p1, p0)
    A2 = _add(_sub(a, _mul(nv, amt * 0.95)), _mul(um, amt * 0.05))
    B2 = _add(_add(b, _mul(nv, amt * 0.95)), _mul(um, amt * 0.05))
    edge = []
    n = 9
    for i in range(n + 1):
        t = i / n
        q = _lerp(A2, B2, t)
        sag = math.sin(math.pi * t) * amt * 0.95
        wave = math.sin(t * math.pi * 4 + seed) * amt * 0.22 * math.sin(math.pi * t)
        edge.append(_add(q, _mul(um, sag + wave)))
    ins = edge if (p0 is a) else edge[::-1]
    out = top[:idx + 1] + ins + top[idx + 1:]
    return out, edge


_LAST = {}   # info about the most recently built figure (used by hand_positions / body_points)


def _figure(D, m, ps, expr, facing=1, marks=True):
    """Build a person. Returns (inner svg in anchor coords, bbox).

    D: design dict, m: metrics dict, ps: pose dict (POSES entry, possibly modified)."""
    if expr not in EXPRS:
        raise ValueError(f"unknown expr {expr!r}; choose from {EXPRESSIONS}")
    t, h = ps["t"], ps["h"]
    u = _rot((0, -1), t)
    f = _rot((1, 0), t)

    def tp(fx, uy):
        return (f[0] * fx + u[0] * uy, f[1] * fx + u[1] * uy)

    R = m["R"]
    fl = m["fl"]
    bare = D.get("bare", False)
    pel = (0.0, 0.0)
    mode = ps["ground"]
    ext = []   # (x, y, r) for bbox / airborne grounding

    # ---------------- reference ground (body coords: pelvis at the origin, y down)
    seat = m["seat"] * (1.3 if mode == "seat" else 1.0)
    seat_pts = [tp(m["ww"] * 0.8, -seat), tp(-m["ww"] * 0.9, -seat), tp(0, -seat)]
    if mode == "seat":
        G = max(p[1] for p in seat_pts) + OW
    elif mode == "body":
        G = max(tp(-m["ww"], 0)[1], tp(-m["shw"], m["T"] - 16)[1], tp(-m["ww"] - 1, 2)[1]) + OW
    else:
        G = 4 + m["th"] + m["sh"] + _sole_off(0, fl, bare) - ps["drop"]

    # ---------------- legs
    hips = [tp(m["hw"], -4), tp(-m["hw"], -4)]
    legs, fangs = [], []
    any_ik = False
    for i, spec in enumerate(ps["legs"]):
        H = hips[i]
        fa_given = ps["feet"][i]
        if spec[0] == "ik":
            any_ik = True
            dx, knee = spec[1], spec[2]
            lift = spec[3] if len(spec) > 3 else 0
            fa = 0.0 if fa_given is None else fa_given
            for _ in range(3):
                K, A = _leg_ik(H, dx, G - lift - _sole_off(fa, fl, bare), m["th"], m["sh"], knee)
                if fa_given is None:
                    fa = max(-90.0, min(0.0, _ang(_rot(_nrm(_sub(A, K)), -90))))
            a1, a2 = _vdeg(_sub(K, H)), _vdeg(_sub(A, K))
        else:
            a1, a2 = spec
            K = _add(H, _mul(_dv(a1), m["th"]))
            A = _add(K, _mul(_dv(a2), m["sh"]))
            fa = _ang(_rot(_dv(a2), -90)) if fa_given is None else fa_given
        legs.append((H, K, A, a1, a2))
        fangs.append(fa)
        ext.append((K[0], K[1], m["lw"] / 2 + OW))

    feet_svg, low = [], []
    for i, (H, K, A, a1, a2) in enumerate(legs):
        sv, soles = _foot(A, fangs[i], D["leg"], fl, D.get("sandal", SANDAL), bare=bare)
        feet_svg.append(sv)
        ext += [(x, y, 0) for x, y in soles]
        ext.append((A[0], A[1], m["lw"] / 2 + OW))
        low += [y + 1.5 for x, y in soles] + [A[1] + m["lw"] / 2 + OW, K[1] + m["lw"] / 2 + OW]
    if mode == "feet" and not any_ik:
        G = max(low)

    # ---------------- head
    N = tp(0, m["T"])
    ha = t + h
    Hc = _add(N, _rot((2.0, -m["neck"]), ha))

    def hw(hx, hy):
        v = _rot((hx * R, hy * R), ha)
        return (Hc[0] + v[0], Hc[1] + v[1])

    ext.append((Hc[0], Hc[1], R + OW))
    top = hw(0, -1.0 - D.get("hat_h", 0.08))
    ext.append((top[0], top[1], 2))
    if D.get("tail"):
        d0, d1 = _tail_dirs(ps, ha)
        ext += [(x, y, OW) for x, y in _cloth_tail_pts(hw(-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R)[0]]

    # ---------------- robe hulls
    hem_frac = D["hem"] if ps["hem"] is None else min(D["hem"], ps["hem"])
    hem_d = hem_frac * (m["th"] + m["sh"])
    flare = max(2.0, m["flare"] * D.get("flare_k", 1.0) + ps["flare"])
    waist = [tp(m["ww"] + 1, 2), tp(-m["ww"] - 1, 2), tp(m["ww"] - 4, -10), tp(-m["ww"] + 4, -10)]
    hem_pts, hem_dirs, hem_side, knee_t, knee_s = [], [], [], [], []
    for (H, K, A, a1, a2) in legs:
        Q, dq, on_thigh = _leg_point(H, K, A, m["th"], hem_d)
        nq = (-dq[1], dq[0])
        wq = m["lw"] / 2 + flare
        hem_side += [_add(Q, _mul(nq, wq)), _sub(Q, _mul(nq, wq))]
        if not on_thigh:
            wk = m["lw"] / 2 + 9
            dk = _nrm(_sub(K, H))
            nk = (-dk[1], dk[0])
            knee_t += [_add(K, _mul(nk, wk)), _sub(K, _mul(nk, wk))]
            ds = _nrm(_sub(A, K))
            ns = (-ds[1], ds[0])
            knee_s += [_add(K, _mul(ns, wk)), _sub(K, _mul(ns, wk))]
        hem_pts.append(Q)
        hem_dirs.append(dq)
    bod_pts = [tp(m["shw"], m["T"] - 16), tp(-m["shw"], m["T"] - 16), tp(m["shw"] - 13, m["T"] + 1),
               tp(-m["shw"] + 13, m["T"] + 1), tp(0, m["T"] + 3), tp(m["ww"], -2), tp(-m["ww"], -2)]
    if ps["lap"] and knee_t:
        skirt_sets = [waist + seat_pts[:2] + knee_t, knee_t + knee_s + hem_side]
    else:
        skirt_sets = [waist + knee_t + hem_side + (seat_pts[:2] if mode == "seat" else [])]
    if ps["flat_back"]:     # lying: the underside of the robe rests flat on the floor
        floor = G - OW

        def flat(pts):
            return [(x, floor if y > floor - 16 else y) for x, y in pts]
        bod_pts = flat(bod_pts)
        skirt_sets = [flat(s_) for s_ in skirt_sets]
    skirts = [_rounded(_hull(s_), 14) for s_ in skirt_sets]
    bodice = _rounded(_hull(bod_pts), 13)
    Hm = _mul(_add(hem_pts[0], hem_pts[1]), 0.5)
    um = _nrm(_add(hem_dirs[0], hem_dirs[1]))
    hem_edge = None
    if ps["billow"]:
        skirts[-1], hem_edge = _billow(skirts[-1], Hm, um, ps["billow"])
    robe_polys = [bodice] + skirts
    if mode in ("seat", "body") or D.get("robe_floor"):     # cloth lies on the floor: never below the ground line
        robe_polys = [_clip(p_, (0, G - OW), (0, -1)) for p_ in robe_polys]
        robe_polys = [p_ for p_ in robe_polys if len(p_) > 2]
    for poly in robe_polys:
        ext += [(x, y, OW) for x, y in poly]

    # ---------------- arms
    L1, L2 = m["ua"] * ps["reach"], m["fa"] * ps["reach"]
    S = [tp(m["sw"], m["T"] - m["sdrop"]), tp(-m["sw"], m["T"] - m["sdrop"])]
    arms = []
    for i, spec in enumerate(ps["arms"]):
        if spec[0] == "fk":
            E = _add(S[i], _mul(_dv(spec[1]), L1))
            W = _add(E, _mul(_dv(spec[2]), L2))
        else:
            kind, x, y, bend = spec[1], spec[2], spec[3], spec[4]
            if kind == "torso":
                T_ = tp(x * m["sw"], y * m["T"])
            elif kind == "head":
                T_ = hw(x, y)
            elif kind == "headw":
                T_ = (Hc[0] + x * R, Hc[1] + y * R)
            elif kind == "knee":
                K = legs[int(x)][1]
                T_ = (K[0], K[1] - y * R)
            elif kind == "pillow":       # under the cheek: below the head, on the floor
                T_ = (Hc[0] + x * R, G - OW - 1.3 * m["hr"])
            elif kind == "ground":       # palm on the floor at body x
                T_ = (x, G - OW - y - 0.5 * m["hr"])
            elif kind == "abs":          # anchor coordinates (x right of the anchor, y up negative)
                T_ = (x, G + y)
            elif kind == "body":         # body coordinates (pelvis origin)
                T_ = (x, y)
            else:
                T_ = _add(S[i], (x * (L1 + L2), y * (L1 + L2)))
            E, W = _ik(S[i], T_, L1, L2, bend)
        arms.append((S[i], E, W))
        ext += [(E[0], E[1], m["aw"] / 2 + OW), (W[0], W[1], m["hr"] + OW)]

    # ---------------- transform & grounding
    flip = -1 if ps["flip"] else 1
    spin = ps["spin"]

    def xf(p):
        return _rot((p[0] * flip, p[1]), spin)

    st = {"pel": pel, "u": u, "f": f, "tp": tp, "legs": legs, "arms": arms, "Hc": Hc, "hw": hw, "ha": ha,
          "S": S, "N": N, "m": m, "ground": G, "robe": robe_polys, "hemp": robe_polys[-1], "Hm": Hm, "um": um,
          "hem_edge": hem_edge, "facing": facing * flip, "ext": ext, "mode": mode}
    marks_svg = _marks(D, st, ps, expr) if marks else ""     # may add to ext
    tx = [(xf((x, y)), r) for x, y, r in ext]
    minx = min(p[0] - r for p, r in tx)
    maxx = max(p[0] + r for p, r in tx)
    if mode == "air":
        gy = max(p[1] + r for p, r in tx)
        ax = (minx + maxx) / 2
    else:
        gy, ax = G, 0.0

    # ======================== draw
    out = []
    if D.get("behind"):
        out.append(D["behind"](st))
    out.append(_back_layer(D, st, ps))

    def arm_svg(i):
        Sx, E, W = arms[i]
        skin = D["skin"]
        s = ""
        sl = D.get("sleeve_len", 1.0)
        if sl < 1.0:
            s += _tube([Sx, E, W], m["aw"] * 0.82, skin)
            mid = _lerp(Sx, E, min(1.0, sl * 2)) if sl <= 0.5 else _lerp(E, W, (sl - 0.5) * 2)
            pts = [Sx, mid] if sl <= 0.5 else [Sx, E, mid]
            s += _tube(pts, m["aw"], D["sleeve"])
        else:
            s += _tube([Sx, E, W], m["aw"], D["sleeve"])
            if D.get("cuff"):
                dw = _nrm(_sub(W, E))
                c0 = _sub(W, _mul(dw, 8))
                s += (f'<path d="M{_pt(c0)} L{_pt(W)}" stroke="{D["cuff"]}" stroke-width="{fmt(m["aw"])}" '
                      f'stroke-linecap="butt"/>')
                s += _line(f"M{_pt(_add(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))} "
                           f"L{_pt(_sub(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))}", w=2.2)
        dw = _nrm(_sub(W, E))
        if D.get("arm_deco"):        # Joseph film: decoration over the sleeve (coat bands), under the hand
            s += D["arm_deco"](st, i, Sx, E, W)
        s += _hand(W, dw, ps["hands"][i], skin, m["hr"])
        return s

    if ps["near_hidden"]:
        out.append(arm_svg(1))
    if not ps["far_front"] and not ps["far_over_head"]:
        out.append(arm_svg(0))
    for i in (0, 1):
        H, K, A, a1, a2 = legs[i]
        out.append(_tube([H, K, A], m["lw"], D["leg"]))
        out.append(feet_svg[i])
        if D.get("legwear"):
            out.append(D["legwear"](st, i))
    out.append(_robe(D, st, ps))
    if ps["far_front"]:
        out.append(arm_svg(0))
    if D.get("mid"):
        out.append(D["mid"](st))
    if ps["near_back"]:
        out.append(arm_svg(1))
    out.append(_head_svg(D, st, ps, expr, marks))
    if ps["far_over_head"]:
        out.append(arm_svg(0))
    if not ps["near_back"] and not ps["near_hidden"]:
        out.append(arm_svg(1))
    if D.get("front"):
        out.append(D["front"](st))
    out.append(marks_svg)
    out.append(_wet_marks(D, st, ps))
    body = "".join(out)
    tf = f"translate({fmt(-ax)},{fmt(-gy)})"
    if spin:
        tf += f" rotate({fmt(spin)})"
    if flip < 0:
        tf += " scale(-1,1)"
    bbox = (minx - ax, min(p[1] - r for p, r in tx) - gy, maxx - ax, max(p[1] + r for p, r in tx) - gy)

    def to_anchor(p):
        q = xf(p)
        return (q[0] - ax, q[1] - gy)
    hands = [to_anchor(_add(W, _mul(_nrm(_sub(W, E)), 0.5 * m["hr"]))) for (Sx, E, W) in arms]
    _LAST.clear()
    _LAST.update(hands=hands, head=to_anchor(Hc), head_top=to_anchor(top), shoulders=[to_anchor(p) for p in S],
                 pelvis=to_anchor(pel), feet=[to_anchor(lg[2]) for lg in legs], bbox=bbox,
                 pts=[(p[0] - ax, p[1] - gy, r) for p, r in tx])
    return f'<g transform="{tf}">{body}</g>', bbox


# ---------------------------------------------------------------- robe


def _robe(D, st, ps):
    m, tp, u, f, pel = st["m"], st["tp"], st["u"], st["f"], st["pel"]
    polys = st["robe"]
    hemp = st["hemp"]
    col = D["robe"]
    lim = m["ww"] + 2

    def torso(b):
        """Clip a band to the torso strip |(p - pel) . f| <= ww + 2 (belts never run along a lap)."""
        if len(b) < 3:
            return []
        b = _clip(b, _sub(pel, _mul(f, lim)), f)
        return _clip(b, _add(pel, _mul(f, lim)), _mul(f, -1)) if len(b) > 2 else []

    s = ""
    if D.get("fringe"):
        # fringe: dashed strip just below the hem edge (drawn first, the robe covers its top)
        chain = [p for p in hemp if _dot(_sub(p, st["Hm"]), st["um"]) > -3]
        if len(chain) > 2:
            chain = sorted(chain, key=lambda p: _dot(_sub(p, st["Hm"]), (-st["um"][1], st["um"][0])))
            off = [_add(p, _mul(st["um"], 4)) for p in chain]
            s += (f'<path d="{_d(off, closed=False)}" fill="none" stroke="{D["fringe"]}" stroke-width="10" '
                  f'stroke-dasharray="2.6 3.2"/>')
    s += _union(polys, col)
    cid = _clip_id("robe", *[_d(p) for p in polys])
    clip = f'<clipPath id="{cid}">' + "".join(f'<path d="{_d(p)}"/>' for p in polys) + "</clipPath>"
    inner = ""
    # soft shade on the back side of the body for volume
    for poly in polys:
        sh_ = _clip(poly, _sub(pel, _mul(f, 0.42 * m["ww"])), _mul(f, -1))
        inner += _poly(sh_, shade(col, -0.10), sw=0, extra='opacity="0.55"')
    # stripes (sailor tunics): bands perpendicular to the torso axis
    if D.get("stripes"):
        sc, sp, sw_ = D["stripes"]
        k = -8
        while k * sp < m["T"] + 30:
            d0 = k * sp
            for poly in polys:
                inner += _poly(_band(poly, pel, u, d0, d0 + sw_), sc, sw=0)
            k += 1
    if D.get("robe_deco"):      # Joseph film: extra decoration inside the robe clip (coat bands, pleats, dust)
        inner += D["robe_deco"](st, polys)
    # small repeating motifs (Persian court robes): a staggered grid that follows the torso axis
    if D.get("pattern"):
        pc, pk, sp = D["pattern"]
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        n = int(max(max(xs) - min(xs), max(ys) - min(ys)) / sp) + 2
        cx0, cy0 = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        mot = ""
        for i in range(-n // 2 - 1, n // 2 + 2):
            for j in range(-n // 2 - 1, n // 2 + 2):
                c = _add((cx0, cy0), tp((i + (0.5 if j % 2 else 0.0)) * sp, j * sp * 0.92))
                if pk == "diamond":
                    r_ = 0.22 * sp
                    mot += _poly([(c[0], c[1] - r_), (c[0] + r_ * 0.75, c[1]), (c[0], c[1] + r_), (c[0] - r_ * 0.75, c[1])],
                                 pc, sw=0)
                elif callable(pk):
                    mot += pk(c, sp)
                elif pk == "flower":
                    mot += (f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(0.17 * sp)}" fill="{pc}"/>'
                            f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(0.07 * sp)}" fill="{shade(pc, 0.45)}"/>')
                else:
                    mot += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(0.11 * sp)}" fill="{pc}"/>'
        inner += f'<g opacity="0.85">{mot}</g>'
    # folds
    fold = shade(col, -0.16)
    if ps["lap"]:
        for (H, K, A, a1, a2) in st["legs"][:1]:
            a, b = _lerp(K, A, 0.22), _lerp(K, A, 0.8)
            ds = _nrm(_sub(A, K))
            mid = _add(_lerp(a, b, 0.5), _mul((-ds[1], ds[0]), 4))
            inner += _line(f"M{_pt(a)} Q{_pt(mid)} {_pt(b)}", w=2.4, col=fold, extra='opacity="0.8"')
    else:
        for x0, x1 in ((-0.45, -0.62), (0.35, 0.50)):
            a = tp(x0 * m["ww"], -14)
            b = _add(st["Hm"], _mul(f, x1 * m["ww"]))
            b = _sub(b, _mul(st["um"], 16))
            mid = _add(_lerp(a, b, 0.5), _mul(f, 3))
            inner += _line(f"M{_pt(a)} Q{_pt(mid)} {_pt(b)}", w=2.4, col=fold, extra='opacity="0.8"')
    # hem band
    hem = D.get("hem_col")
    hw_ = D.get("hem_w", 13)
    if hem:
        if st["hem_edge"]:
            e = st["hem_edge"]
            inner += (f'<path d="{_d(e, closed=False)}" fill="none" stroke="{hem}" stroke-width="{fmt(2 * hw_)}" '
                      f'stroke-linejoin="round" stroke-linecap="round"/>')
            inner += _line(_d([_sub(p, _mul(st["um"], hw_)) for p in e], closed=False), w=2.6)
        else:
            hb = _clip(hemp, _sub(st["Hm"], _mul(st["um"], hw_)), st["um"])
            inner += _poly(hb, hem, sw=0)
            inner += _line(_d(_band_edge(hemp, st["Hm"], st["um"], -hw_), closed=False), w=2.6)
    # coat (captain): open coat over a narrow striped tunic strip showing down the front
    belt_clip = torso
    if D.get("tunic"):
        c0, wt = 0.28 * m["ww"], 0.30 * m["ww"]
        tun = []
        for poly in polys:
            b = _band(poly, pel, f, c0 - wt, c0 + wt)
            if len(b) > 2:
                b = _clip(b, _sub(st["Hm"], _mul(st["um"], 6)), _mul(st["um"], -1))
            if len(b) > 2:
                tun.append(b)
        for b in tun:
            inner += _poly(b, D["tunic"], sw=0)
        if D.get("tunic_stripes"):
            sc, sp, sw_ = D["tunic_stripes"]
            for k in range(-8, 8):
                for b in tun:
                    inner += _poly(_band(b, pel, u, k * sp, k * sp + sw_), sc, sw=0)
        for b in tun:      # tunic hem line
            inner += _line(_d(_band_edge(b, st["Hm"], st["um"], -6), closed=False), w=2.2)
        for poly in polys:  # coat front edges
            for e in (c0 - wt, c0 + wt):
                ch = _band_edge(poly, pel, f, e)
                if len(ch) == 2:
                    inner += _line(_d(ch, closed=False), w=2.8)
        lap_col = shade(col, 0.16)
        for e, sg in ((c0 - wt, -1), (c0 + wt, 1)):     # lapels folding back at the chest
            p0 = tp(e, m["T"] - 2)
            p1 = tp(e + sg * 11, m["T"] - 10)
            p2 = tp(e, m["T"] - 40)
            inner += _poly([p0, p1, p2], lap_col, sw=2.4)

        def tunic_strip(b):
            if len(b) < 3:
                return []
            b = _clip(b, tp(c0 - wt, 0), f)
            return _clip(b, tp(c0 + wt, 0), _mul(f, -1)) if len(b) > 2 else []
        belt_clip = tunic_strip         # the captain's belt is on the tunic, inside the open coat
    # texture (sackcloth)
    if D.get("texture") == "sack":
        tcol = P["sackcloth_dark"]
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        d = ""
        yy = y0
        while yy < y1:
            d += f"M{fmt(x0)},{fmt(yy)} L{fmt(x1)},{fmt(yy + 3)} "
            yy += 9
        xx = x0
        while xx < x1:
            d += f"M{fmt(xx)},{fmt(y0)} L{fmt(xx + 4)},{fmt(y1)} "
            xx += 11
        inner += f'<path d="{d}" fill="none" stroke="{tcol}" stroke-width="1.6" opacity="0.45"/>'
        pc = tp(-0.35 * m["ww"], 0.45 * m["T"])
        inner += (f'<rect x="{fmt(pc[0] - 9)}" y="{fmt(pc[1] - 8)}" width="18" height="16" rx="3" '
                  f'fill="{shade(P["sackcloth"], -0.08)}" stroke="{tcol}" stroke-width="2" stroke-dasharray="3 3"/>')
    # shawl: diagonal band from the near shoulder to the far hip (stays on the torso)
    if D.get("shawl"):
        n = _nrm(_add(_mul(u, 0.80), _mul(f, 0.60)))
        p0 = tp(-0.1 * m["ww"], 0.55 * m["T"])
        for poly in polys:
            inner += _poly(torso(_band(poly, p0, n, -13, 13)), D["shawl"], sw=2.6)
        if D.get("shawl_trim"):
            for poly in polys:
                for off in (-9, 9):
                    inner += _poly(torso(_band(poly, p0, n, off - 1.5, off + 1.5)), D["shawl_trim"], sw=0)
    if D.get("collar"):
        c0_, c1_, c2_ = tp(-m["shw"] * 0.55, m["T"] - 2), tp(m["shw"] * 0.55, m["T"] - 2), tp(0, m["T"] - 22)
        inner += _line(f"M{_pt(c0_)} Q{_pt(c2_)} {_pt(c1_)}", w=7, col=D["collar"])
        inner += _line(f"M{_pt(c0_)} Q{_pt(c2_)} {_pt(c1_)}", w=1.8, col=GOLD_DARK)
    if D.get("neck_v"):
        a, b, c = tp(-11, m["T"] + 1), tp(12, m["T"] + 1), tp(1, m["T"] - 20)
        inner += _poly([a, c, b], D["neck_v"], sw=2.6)
    # belt / sash: always waist-wide, whatever the legs do
    knot = ""                   # sash knot and tails: drawn after the clipped robe so drifting tails show
    if D.get("sash"):
        lo, hi = (3, 18) if ps["lap"] else (-6, 11)     # seated: the waist sits higher above the seat
        for poly in polys:
            inner += _poly(torso(_band(poly, pel, u, lo, hi)), D["sash"], sw=2.8)
        if D.get("sash_tail", True):
            k0 = tp(0.45 * m["ww"], lo + 8)
            if ps["lap"]:
                k1 = _add(k0, _mul(_dv(30 - ps["t"]), 18))
                k2 = _add(k0, _mul(_dv(5 - ps["t"]), 22))
            elif ps["sash_dir"] is not None:
                k1 = _add(k0, _mul(_dv(ps["sash_dir"] - ps["t"]), 30))
                k2 = _add(k0, _mul(_dv(ps["sash_dir"] - ps["t"] - 28), 36))
            else:
                k1 = _add(tp(0.55 * m["ww"], -26), _mul(f, 2))
                k2 = tp(0.35 * m["ww"], -34)
            knot += _tube([k0, k1], 7, D["sash"], ow=2.6) + _tube([k0, k2], 7, D["sash"], ow=2.6)
            knot += f'<circle cx="{fmt(k0[0])}" cy="{fmt(k0[1])}" r="6.5" fill="{D["sash"]}" {_st(2.6)}/>'
    if D.get("rope_belt"):
        rc = D["rope_belt"]
        blo = 6 if ps["lap"] else -3
        bands = [belt_clip(_band(poly, pel, u, blo, blo + 9)) for poly in polys]
        for b in bands:
            inner += _poly(b, rc, sw=2.4)
        for b in bands:
            if len(b) > 2:
                xs = sorted(b, key=lambda p: _dot(p, f))
                a, z = xs[0], xs[-1]
                for i in range(1, 7):
                    q = _lerp(a, z, i / 7)
                    inner += _line(f"M{_pt(_add(q, _mul(u, 4)))} L{_pt(_sub(_add(q, _mul(f, 4)), _mul(u, 3)))}",
                                   w=1.6, col=shade(rc, -0.35))
        kx = 0.40 * m["ww"] if not D.get("tunic") else 0.28 * m["ww"]
        k0 = tp(kx, blo + 4)
        tl = 16 if ps["lap"] else 30
        inner += _tube([k0, tp(kx + 0.08 * m["ww"], blo + 4 - tl)], 4.5, rc, ow=2.2)
        inner += _tube([k0, tp(kx - 0.12 * m["ww"], blo + 8 - tl)], 4.5, rc, ow=2.2)
    if D.get("ash"):
        acol = P["ash"]
        for fx, uy, r in ((-0.4, 0.3, 7), (0.5, 0.75, 5), (0.1, -0.9, 8), (0.3, 0.2, 4), (-0.2, -0.5, 4)):
            c = tp(fx * m["ww"], uy * m["T"] * (0.6 if uy < 0 else 1))
            inner += _ell(c[0], c[1], r * 1.3, r, acol, extra='opacity="0.42"')
    if D.get("wet"):            # darker soaked patches along the hem
        for k, (fx, r) in enumerate(((-0.55, 15), (0.1, 18), (0.65, 13))):
            c = _add(_sub(st["Hm"], _mul(st["um"], 10 + 6 * (k % 2))), _mul((-st["um"][1], st["um"][0]),
                                                                             fx * m["ww"]))
            inner += _ell(c[0], c[1], r * 1.3, r, shade(col, -0.22), extra='opacity="0.55"')
    s += clip + f'<g clip-path="url(#{cid})">{inner}</g>' + knot
    return s


def _band_edge(poly, p0, n, d):
    """Points along the chord (p - p0) . n = d of a convex polygon (2 points)."""
    pts = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n) - d, _dot(_sub(b, p0), n) - d
        if (da >= 0) != (db >= 0):
            pts.append(_lerp(a, b, da / (da - db)))
    return pts[:2]


# ---------------------------------------------------------------- head assembly


def _back_layer(D, st, ps):
    """Things hanging behind the body: head-cloth tail, veil drape, long Assyrian hair."""
    R, hw, ha = st["m"]["R"], st["hw"], st["ha"]
    s = ""
    tail = D.get("tail")
    if tail:
        col, stripe = tail
        if D.get("wet"):
            col = shade(col, -0.22)
        d0, d1 = _tail_dirs(ps, ha)
        s += _cloth_tail(hw(-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R, col, stripe)
    if D.get("veil"):
        col = D["veil"]
        A0 = hw(-0.70, 0.10)
        A1 = hw(0.15, 0.25)
        bot = (A0[0] - 0.15 * R, A0[1] + 2.0 * R)
        pts = [hw(-0.95, -0.5), A0, (A0[0] - 0.55 * R, A0[1] + 1.0 * R), bot, (bot[0] + 0.9 * R, bot[1] - 0.2 * R),
               A1]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    if D.get("long_hair"):
        col = D["long_hair"]
        pts = [hw(-0.95, -0.3), hw(-1.20, 0.5), hw(-1.12, 1.25), hw(-0.40, 1.42), hw(0.05, 1.0), hw(-0.3, 0.2)]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
        wave = shade(col, 0.22)
        for x0 in (-1.0, -0.72, -0.44):          # soft vertical waves down the hair mass
            pts = [hw(x0, 0.30), hw(x0 - 0.08, 0.55), hw(x0 + 0.02, 0.80), hw(x0 - 0.06, 1.05), hw(x0 + 0.02, 1.25)]
            s += f'<path d="{smooth_path(pts, closed=False)}" fill="none" {_st(2.2, wave)}/>'
    if D.get("ponytail"):
        col = D["ponytail"]
        c = hw(-1.08, -0.15)
        s += _ell(c[0], c[1], 0.30 * R, 0.36 * R, col, sw=3.2)
    return s


def _cloth_tail_pts(A0, d0, d1, L, w0, w1):
    """Outline points and centre-line sampler of a flowing cloth flap."""
    P1 = _add(A0, _mul(d0, L * 0.45))
    P2 = _add(P1, _mul(d1, L * 0.62))

    def at(t):
        a = _add(_add(_mul(A0, (1 - t) ** 2), _mul(P1, 2 * t * (1 - t))), _mul(P2, t * t))
        dd = _nrm(_add(_mul(_sub(P1, A0), 2 * (1 - t)), _mul(_sub(P2, P1), 2 * t)))
        nv = (-dd[1], dd[0])
        w = w0 + (w1 - w0) * t
        return a, dd, nv, w
    left, right = [], []
    for i in range(9):
        a, dd, nv, w = at(i / 8)
        left.append(_add(a, _mul(nv, w)))
        right.append(_sub(a, _mul(nv, w)))
    a, dd, nv, w = at(1.0)
    tip = [_add(_add(a, _mul(dd, 0.10 * L)), _mul(nv, 0.45 * w)), _add(a, _mul(dd, 0.04 * L)),
           _add(_add(a, _mul(dd, 0.12 * L)), _mul(nv, -0.5 * w))]
    return left + tip + right[::-1], at


def _cloth_tail(A0, d0, d1, L, w0, w1, col, stripe=None):
    """Flowing cloth flap: leaves A0 along d0, bends toward d1 (quadratic centre line)."""
    pts, at = _cloth_tail_pts(A0, d0, d1, L, w0, w1)
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    a, _, _, w = at(0.35)
    end, _, n_end, _ = at(0.7)
    s += _line(f"M{_pt(_add(A0, _mul(_rot(d0, -90), 0.1 * L)))} Q{_pt(a)} {_pt(_add(end, _mul(n_end, 0.2 * w)))}",
               w=2.0, col=shade(col, -0.2))
    if stripe:
        for t0 in (0.60, 0.78):
            p0, _, n0, ww0 = at(t0)
            p1, _, n1, ww1 = at(t0 + 0.09)
            quad = [_add(p0, _mul(n0, ww0 * 0.97)), _add(p1, _mul(n1, ww1 * 0.97)),
                    _sub(p1, _mul(n1, ww1 * 0.97)), _sub(p0, _mul(n0, ww0 * 0.97))]
            s += _poly(quad, stripe, sw=2.2)
    return s


def _blade(cl, wmax, col):
    """Seaweed blade: wavy closed shape around a centre line, tapered at both ends."""
    left, right = [], []
    n = len(cl)
    for i, p in enumerate(cl):
        a, b = cl[max(i - 1, 0)], cl[min(i + 1, n - 1)]
        d = _nrm(_sub(b, a))
        nv = (-d[1], d[0])
        t = i / (n - 1)
        w = wmax * (math.sin(math.pi * min(0.96, 0.08 + t)) ** 0.6) * (1 + 0.25 * math.sin(i * 1.7))
        left.append(_add(p, _mul(nv, w)))
        right.append(_sub(p, _mul(nv, w)))
    return f'<path d="{smooth_path(left + right[::-1])}" fill="{col}" {_st(2.4)}/>'


def _head_svg(D, st, ps, expr, marks=True):
    R, Hc, ha = st["m"]["R"], st["Hc"], st["ha"]
    skin = D["skin"]
    s = ""
    hair = D.get("hair")
    hat = D.get("hat")
    beard = D.get("beard")
    moustache = bool(beard) and beard[0] in _MOUSTACHED
    if D.get("ears", True):
        s += _ear(R, skin)
    s += _ell(0, 0, R, R * 0.97, skin, sw=OW)
    if hair:
        s += _hair_cap(R, hair, D.get("hair_style", "short"))
        if D.get("ears", True):
            s += _ear(R, skin)
    if D.get("ponytail"):
        s += _tube([(-0.60 * R, -0.55 * R), (-1.0 * R, -0.28 * R)], 0.16 * R, D.get("ribbon", P["terracotta"]),
                   ow=2.4)
    face, over = _face(R, skin, expr, ps["look"], mouth=not moustache, tremble=marks, brow_w=D.get("brow_w", 3.4),
                       brow_col=D.get("brow_col", INK))
    s += face
    mouth_kind = EXPRS[expr]["mouth"]
    if beard:
        kind, bcol = beard
        s += _beard(R, bcol, kind)
        if moustache:
            s += _moustache(R, bcol, kind)
            s += _mouth(R, mouth_kind, my=0.66 * R)
        else:
            s += _mouth(R, mouth_kind)
    if D.get("ash"):            # ash sprinkled on the head: light speckles on hair / forehead, never near the eyes
        acol = mix(P["ash"], HI, 0.25)
        for hx, hy, r in ((-0.55, -0.80, 0.055), (-0.18, -0.95, 0.05), (0.22, -0.90, 0.06), (0.52, -0.72, 0.045),
                          (-0.80, -0.50, 0.05), (0.02, -0.74, 0.04)):
            s += f'<circle cx="{fmt(hx * R)}" cy="{fmt(hy * R)}" r="{fmt(r * R)}" fill="{acol}" opacity="0.7"/>'
        for hx, hy, r in ((0.05, -0.50, 0.03), (0.30, -0.53, 0.025), (-0.55, 0.55, 0.03), (-0.45, 0.66, 0.025)):
            s += f'<circle cx="{fmt(hx * R)}" cy="{fmt(hy * R)}" r="{fmt(r * R)}" fill="{P["ash"]}" opacity="0.4"/>'
    if hat:
        kind = hat[0]
        if kind == "headcloth":
            col = hat[1]
            if D.get("wet"):
                col = shade(col, -0.22)
            s += _cloth_cap(R, col, edge=hat[2])
        elif kind == "veil":
            s += _cloth_cap(R, hat[1], edge=hat[2])
        elif kind == "headband":
            s += _headband(R, hat[1])
        elif kind == "knit":
            s += _knit_cap(R, hat[1])
        elif kind == "seacap":
            s += _sea_cap(R, hat[1])
        elif kind == "crown":
            s += _crown(R, x0=0.05 * R, y0=-0.55 * R)
        elif kind == "wrap":
            s += _wrap(R, hat[1], hat[2] if len(hat) > 2 else None)
        elif kind == "tallhat":
            s += _tall_hat(R, hat[1], hat[2])
        elif kind == "turban":
            s += _turban(R, hat[1], hat[2])
        elif kind == "darius":
            s += _darius_crown(R, x0=0.05 * R, y0=-0.55 * R)
        elif kind == "helmet":
            s += _helmet(R, hat[1], hat[2])
        elif kind == "custom":               # David film: hat = ("custom", fn) with fn(R) -> head-frame markup
            s += hat[1](R)
    if D.get("seaweed"):        # strands draped over the head-cloth and down onto the shoulder
        c1 = _spline_pts([(0.30 * R, -1.08 * R), (-0.30 * R, -1.10 * R), (-0.85 * R, -0.78 * R),
                          (-1.18 * R, -0.10 * R), (-1.20 * R, 0.55 * R), (-1.02 * R, 1.25 * R)], steps=3)
        c2 = _spline_pts([(0.05 * R, -1.12 * R), (-0.55 * R, -0.96 * R), (-0.98 * R, -0.42 * R),
                          (-0.92 * R, 0.25 * R), (-0.70 * R, 0.80 * R)], steps=3)
        c3 = _spline_pts([(0.40 * R, -1.02 * R), (0.85 * R, -0.70 * R), (1.08 * R, -0.36 * R),
                          (1.10 * R, 0.0)], steps=3)
        s += (_blade(c1, 0.12 * R, P["leaf"]) + _blade(c2, 0.10 * R, P["olive"]) +
              _blade(c3, 0.08 * R, P["leaf_dark"]))
    s += over
    return f'<g transform="translate({_pt(Hc)}) rotate({fmt(ha)})">{s}</g>'


def _marks(D, st, ps, expr):
    """Motion / sound / sleep marks in body coordinates (adds their extent to st['ext'])."""
    R, Hc = st["m"]["R"], st["Hc"]
    s = ""
    mk = ps["marks"]
    mcol = MARK
    ext = st["ext"]
    if "shake" in mk:          # head shaking 'no': marks on the face side only
        for k in (0, 1):
            cx = Hc[0] + R * (1.30 + 0.25 * k)
            s += _line(f"M{fmt(cx)},{fmt(Hc[1] - 0.45 * R)} Q{fmt(cx + 0.14 * R)},{fmt(Hc[1])} "
                       f"{fmt(cx)},{fmt(Hc[1] + 0.45 * R)}", w=3.2, col=mcol)
            ext.append((cx + 0.14 * R, Hc[1], 3))
    if "fan" in mk:            # weak fanning near the chin: two soft little arcs
        W = st["arms"][ps["fan_arm"]][2]
        for k in range(2):
            r = 0.38 * R + k * 0.18 * R
            s += _line(f"M{fmt(W[0] + r * 0.9)},{fmt(W[1] - r * 0.5)} Q{fmt(W[0] + r * 1.12)},{fmt(W[1])} "
                       f"{fmt(W[0] + r * 0.9)},{fmt(W[1] + r * 0.5)}", w=2.2, col=mcol, extra='opacity="0.7"')
            ext.append((W[0] + r * 1.12, W[1], 2))
    if "zzz" in mk:
        mir = st["facing"]
        for k, (dx, dy, sz) in enumerate(((0.55, -1.30, 0.30), (0.95, -1.75, 0.38), (1.42, -2.25, 0.48))):
            c = (Hc[0] + dx * R, Hc[1] + dy * R)
            s += _zglyph(c[0], c[1], sz * R, mirror=mir, w=3.0 + k * 0.4)
            ext.append((c[0], c[1], sz * R * 0.6))
    if "sound" in mk:          # a voice from above and in front: arcs arriving at the listener
        src = (Hc[0] + 1.75 * R, Hc[1] - 1.55 * R)
        dirv = _nrm(_sub(Hc, src))
        nv = (-dirv[1], dirv[0])
        for k, r in enumerate((0.30, 0.52, 0.74)):
            c = _add(src, _mul(dirv, (0.40 + 0.20 * k) * R))
            a = _add(c, _mul(nv, r * R))
            b = _sub(c, _mul(nv, r * R))
            q = _add(c, _mul(dirv, 0.22 * R))
            s += _line(f"M{_pt(a)} Q{_pt(q)} {_pt(b)}", w=2.8, col=mcol, extra='opacity="0.85"')
            ext += [(a[0], a[1], 2), (b[0], b[1], 2)]
    return s


def _wet_marks(D, st, ps):
    """Water dripping from a soaked figure: beard, hem, head-cloth flap and fingertips."""
    if not D.get("wet"):
        return ""
    R = st["m"]["R"]
    floor = st["ground"] - 2 if st["mode"] != "air" and not ps["held"] else None

    def drop(p, k):              # drops never sink below the ground line
        y = p[1] if floor is None else min(p[1], floor - 1.15 * k)
        return _drop(p[0], y, k)
    s = ""
    hemp = st["hemp"]
    um = st["um"]
    chain = [p for p in hemp if _dot(_sub(p, st["Hm"]), um) > -2]
    chain = sorted(chain, key=lambda p: _dot(p, (-um[1], um[0])))
    if chain:
        for i, k in enumerate((0.12, 0.5, 0.88)):
            p = chain[int(k * (len(chain) - 1))]
            s += drop(_add(p, _mul(um, 14 + 8 * (i % 2))), 5.5)
    for (Sx, E, W) in st["arms"]:
        dw = _nrm(_sub(W, E))
        p = _add(W, _mul(dw, 2.0 * st["m"]["hr"]))
        s += drop((p[0], p[1] + 12), 5.0)
    chin = st["hw"](0.16, 1.32)
    s += drop((chin[0], chin[1] + 4), 5.0)
    if D.get("tail"):
        d0, d1 = _tail_dirs(ps, st["ha"])
        pts, _ = _cloth_tail_pts(st["hw"](-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R)
        tip = max(pts, key=lambda p: p[1])
        s += drop((tip[0], tip[1] + 14), 4.8)
    return s


# ======================================================================= public API


def ground_shadow(x, y, scale=1.0, width=120, opacity=0.22, color=None):
    """Soft oval contact shadow centred on an anchor point (put it on a layer *below* the figure)."""
    c = color or P["ink"]
    return (f'<ellipse cx="{x:.2f}" cy="{y + 4 * scale:.2f}" rx="{width * scale / 2:.2f}" ry="{width * scale * 0.11:.2f}" '
            f'fill="{c}" opacity="{opacity}" filter="url(#soft)"/>')


def hand_positions(fn, x, y, scale=1.0, facing=1, **kw):
    """Stage coordinates of both hand centres [(x, y) far hand, (x, y) near hand] of the figure that
    ``fn(x, y, scale, facing, **kw)`` draws (fn is jonah, sailor, captain, king or citizen)."""
    return body_points(fn, x, y, scale, facing, **kw)["hands"]


def body_points(fn, x, y, scale=1.0, facing=1, **kw):
    """Stage coordinates of key points of the figure ``fn(x, y, scale, facing, **kw)`` would draw:
    {'head': centre of the head, 'head_top', 'hands': [far, near], 'shoulders': [far, near],
     'pelvis', 'feet': [far ankle, near ankle], 'bbox': (left, top, right, bottom)}."""
    fn(x, y, scale, facing, **kw)
    sx = scale * (1 if facing >= 0 else -1)

    def st(p):
        return (x + p[0] * sx, y + p[1] * scale)
    l, t, r, b = _LAST["bbox"]
    xs = sorted((x + l * sx, x + r * sx))
    return {"head": st(_LAST["head"]), "head_top": st(_LAST["head_top"]),
            "hands": [st(p) for p in _LAST["hands"]], "shoulders": [st(p) for p in _LAST["shoulders"]],
            "pelvis": st(_LAST["pelvis"]), "feet": [st(p) for p in _LAST["feet"]],
            "bbox": (xs[0], y + t * scale, xs[1], y + b * scale)}


def _wrap_out(inner, x, y, scale, facing, label):
    sx = scale * (1 if facing >= 0 else -1)
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({sx:.5g},{scale:.5g})" data-who="{label}">'
            f'<g filter="url(#wobble-fine)">{inner}</g></g>')


def _resolve_pose(pose, allowed, who):
    if pose not in allowed:
        raise ValueError(f"{who}: unknown pose {pose!r}; choose from {sorted(allowed)}")
    return dict(POSES[pose])


def _check_expr(expr, who):
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{who}: unknown expr {expr!r}; choose from {EXPRESSIONS}")


def _fsign(facing):
    return 1 if facing >= 0 else -1


JONAH_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "sleep", "kneel_pray", "sit", "sit_sulk",
               "sit_faint", "sit_happy", "preach", "point", "arms_up", "fall", "float", "refuse", "confess",
               "listen", "wake", "carried")


def _jonah_design(wet=False):
    robe = P["jonah_robe"]
    if wet:
        robe = shade(robe, -0.22)
    return dict(robe=robe, sleeve=robe, hem_col=shade(P["jonah_robe_dark"], -0.15 if wet else 0),
                cuff=P["jonah_robe_dark"], sash=P["jonah_sash"], skin=P["skin"], leg=P["skin"], hem=0.90,
                hat=("headcloth", P["headcloth"], P["headcloth_stripe"]),
                tail=(P["headcloth"], P["headcloth_stripe"]), ears=False,
                beard=("short", P["beard"]), neck_v=shade(P["headcloth"], -0.22 if wet else 0), wet=wet, seaweed=wet)


def jonah(x, y, scale=1.0, facing=1, pose="stand", expr=None, wet=False, marks=True):
    ps = _resolve_pose(pose, JONAH_POSES + ("walk",), "jonah")
    _check_expr(expr, "jonah")
    e = expr or ps["expr"]
    inner, _ = _figure(_jonah_design(wet), _ADULT, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")


# ---------------------------------------------------------------- sailors
SAILOR_POSES = ("stand", "scared", "throw", "carry", "pray", "point", "pull", "lift")
_SAILORS = [
    dict(stripe=("#4a78a8", P["headcloth"]), skin="#eab48c", hair="#4a2f1f", hair_style="curly",
         hat=("headband", "#c0533a"), beard=None),
    dict(stripe=("#c0533a", P["headcloth"]), skin="#b9805a", hair="#2f2420", hair_style="short",
         hat=("knit", "#3f6f9e"), beard=("stubble", "#2f2420")),
    dict(stripe=(P["jonah_sash"], P["headcloth"]), skin="#8d5a3b", hair="#2a201b", hair_style="curly",
         hat=("headband", "#e0a23c"), beard=None),
    dict(stripe=("#d9a03c", "#8a5a36"), skin="#f0c6a2", hair="#a0582e", hair_style="short",
         hat=("knit", P["grass_dark"]), beard=("full", "#a0582e")),
]


def _sailor_design(variant):
    v = _SAILORS[variant % 4]
    base, stripe = v["stripe"][1], v["stripe"][0]
    return dict(robe=base, sleeve=stripe, hem_col=stripe, stripes=(stripe, 22, 10), skin=v["skin"],
                leg=v["skin"], hem=0.50, sleeve_len=0.45, rope_belt="#b98a52", hair=v["hair"],
                hair_style=v["hair_style"], hat=v["hat"], beard=v["beard"], flare_k=0.6, hem_w=9)


_SAILOR_M = dict(_ADULT, lw=20.0)


def sailor(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, marks=True):
    ps = _resolve_pose(pose, SAILOR_POSES, "sailor")
    _check_expr(expr, "sailor")
    e = expr or ps["expr"]
    inner, _ = _figure(_sailor_design(variant), _SAILOR_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"sailor{variant}-{pose}")


# ---------------------------------------------------------------- captain
CAPTAIN_POSES = ("stand", "wake", "point", "worried")
_CAPTAIN_M = _metrics(_ADULT, 1.08, 1.18)
_COAT = "#3f6f9e"


def _captain_design():
    return dict(robe=_COAT, sleeve=_COAT, tunic="#efe2c4", tunic_stripes=("#c0533a", 26, 6),
                hem_col="#2f5680", cuff="#2f5680", skin="#dba27c", leg="#dba27c", hem=0.86,
                rope_belt="#8b5a35", hair="#a9a49c", hair_style="short", hat=("seacap", "#a33f35"),
                beard=("captain", "#b5b0a7"))


def captain(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    ps = _resolve_pose("wake_other" if pose == "wake" else pose,
                       CAPTAIN_POSES[:1] + ("wake_other",) + CAPTAIN_POSES[2:], "captain")
    _check_expr(expr, "captain")
    e = expr or ps["expr"]
    inner, _ = _figure(_captain_design(), _CAPTAIN_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"captain-{pose}")


# ---------------------------------------------------------------- held props (Daniel film)
PARCH = "#efdfb8"
PARCH_ROLL = "#e2cb98"
SEAL_RED = "#b8473c"


def _writing(x0, x1, y0, y1, rows=4):
    """Wavy lines of writing between x0..x1 and y0..y1 (soft ink)."""
    s = ""
    for i in range(rows):
        yy = y0 + (y1 - y0) * (i + 0.5) / rows
        xe = x1 - (x1 - x0) * (0.25 if i % 2 else 0.05)
        d = f"M{fmt(x0)},{fmt(yy)}"
        n = max(1, int((xe - x0) / 10))
        w = (xe - x0) / n
        for _ in range(n):
            d += f" q{fmt(w / 4)},-3 {fmt(w / 2)},0 q{fmt(w / 4)},3 {fmt(w / 2)},0"
        s += _line(d, w=2.0, col=P["ink_soft"], extra='opacity="0.75"')
    return s


def _read_front(D):
    """An open hand-scroll held in both hands in front of the chest (pose 'read')."""
    def front(st):
        W0, W1 = st["arms"][0][2], st["arms"][1][2]
        hr, skin = st["m"]["hr"], D["skin"]
        xa, xb = sorted((W0[0], W1[0]))
        yc = (W0[1] + W1[1]) / 2
        h = 33
        s = _poly([(xa, yc - h), (xb, yc - h - 3), (xb, yc + h - 3), (xa, yc + h)], PARCH, sw=3.0)
        s += _writing(xa + 10, xb - 10, yc - h + 8, yc + h - 10, rows=4)
        for W in (W0, W1):
            s += (f'<rect x="{fmt(W[0] - 7)}" y="{fmt(W[1] - h - 9)}" width="14" height="{fmt(2 * h + 18)}" rx="6" '
                  f'fill="{PARCH_ROLL}" {_st(3.0)}/>')
            s += f'<circle cx="{fmt(W[0])}" cy="{fmt(W[1] + 4)}" r="{fmt(hr)}" fill="{skin}" {_st(3.2)}/>'
        return s
    return front


def _sign_front(D, seated=False):
    """A decree hanging from a roller in the far hand; the near hand presses the royal seal onto it."""
    def front(st):
        W0, W1 = st["arms"][0][2], st["arms"][1][2]
        hr, skin = st["m"]["hr"], D["skin"]
        x0, x1 = W0[0] - 30, W0[0] + 26
        top = W0[1]
        bot = (top + 64) if seated else (top + 96)
        s = (f'<path d="M{fmt(x0 + 3)},{fmt(top)} L{fmt(x1 - 3)},{fmt(top)} L{fmt(x1)},{fmt(bot - 8)} '
             f'Q{fmt((x0 + x1) / 2)},{fmt(bot + 6)} {fmt(x0)},{fmt(bot - 4)} Z" fill="{PARCH}" {_st(3.0)}/>')
        s += _writing(x0 + 8, x1 - 8, top + 10, bot - 30, rows=3)
        s += (f'<rect x="{fmt(x0 - 9)}" y="{fmt(top - 7)}" width="{fmt(x1 - x0 + 18)}" height="14" rx="6" '
              f'fill="{PARCH_ROLL}" {_st(3.0)}/>')
        s += f'<circle cx="{fmt(W0[0])}" cy="{fmt(W0[1])}" r="{fmt(hr)}" fill="{skin}" {_st(3.2)}/>'
        sx, sy = W1[0] - 6, W1[1] + 18                                     # the stamp's face on the sheet
        s += f'<circle cx="{fmt(sx + 9)}" cy="{fmt(sy + 4)}" r="8" fill="{SEAL_RED}" {_st(2.4)}/>'
        s += (f'<rect x="{fmt(sx - 8)}" y="{fmt(sy - 30)}" width="16" height="30" rx="5" fill="{GOLD}" {_st(2.8)}/>'
              f'<ellipse cx="{fmt(sx)}" cy="{fmt(sy - 1)}" rx="11" ry="4.5" fill="{GOLD_DARK}" {_st(2.4)}/>'
              f'<circle cx="{fmt(sx)}" cy="{fmt(sy - 34)}" r="7" fill="{GOLD}" {_st(2.6)}/>')
        s += f'<circle cx="{fmt(W1[0])}" cy="{fmt(W1[1] - 6)}" r="{fmt(hr)}" fill="{skin}" {_st(3.2)}/>'
        return s
    return front


# ---------------------------------------------------------------- king
KING_POSES = ("stand", "sit_throne", "sit_ashes", "kneel_pray", "remove_crown",
              # added for King Darius (Daniel 6); they work in every attire
              "walk_a", "walk_b", "pace_a", "pace_b", "sign", "sit_sign", "sad", "sit_sad", "call_out",
              "reach_out", "hug", "arms_up")
KING_ATTIRES = ("royal", "sackcloth", "darius", "saul")
_KING_ALIAS = {"sad": "sad_head"}
_KING_SEATED = ("sit_throne", "sit_sign", "sit_sad")
DARIUS_HAIR = "#2e221d"
DARIUS_ROBE = "#74489a"
_KING_M = _metrics(_ADULT, 1.04, 1.08)
KING_HAIR = "#3a2b25"


def _throne(st):
    """High-backed wooden throne with gold trim, drawn behind a seated figure."""
    m, pel, legs = st["m"], st["pel"], st["legs"]
    g = st["ground"] or 0
    K = legs[1][1]
    seat_y = pel[1] + m["seat"] * 0.75
    xb0, xb1 = pel[0] - m["ww"] - 46, pel[0] - m["ww"] + 22
    top = st["Hc"][1] - 0.55 * m["R"]
    wood, wd = P["wood"], P["wood_dark"]
    cush = P["royal_light"]
    xm = (xb0 + xb1) / 2
    x_front = K[0] + 4
    s = ""
    for xx in (xb0 + 10, x_front - 10):
        s += (f'<rect x="{fmt(xx - 8)}" y="{fmt(seat_y)}" width="16" height="{fmt(g - seat_y - 8)}" rx="4" '
              f'fill="{wd}" {_st(3.2)}/>')
        s += _ell(xx + 4, g - 7, 13, 7, GOLD, sw=2.8)
    s += (f'<rect x="{fmt(xb0 + 14)}" y="{fmt(seat_y + (g - seat_y) * 0.55)}" width="{fmt(x_front - xb0 - 30)}" '
          f'height="9" rx="3" fill="{wd}" {_st(2.6)}/>')
    s += (f'<path d="M{fmt(xb0)},{fmt(seat_y)} L{fmt(xb0)},{fmt(top + 26)} Q{fmt(xm)},{fmt(top - 16)} '
          f'{fmt(xb1)},{fmt(top + 26)} L{fmt(xb1)},{fmt(seat_y)} Z" fill="{wood}" {_st(OW)}/>')
    s += (f'<path d="M{fmt(xb0 + 10)},{fmt(seat_y - 14)} L{fmt(xb0 + 10)},{fmt(top + 32)} Q{fmt(xm)},'
          f'{fmt(top + 4)} {fmt(xb1 - 10)},{fmt(top + 32)} L{fmt(xb1 - 10)},{fmt(seat_y - 14)} Z" '
          f'fill="{cush}" {_st(2.6)}/>')
    for k in range(3):
        yy = top + 46 + k * 34
        if yy < seat_y - 20:
            s += f'<circle cx="{fmt(xm)}" cy="{fmt(yy)}" r="5" fill="{GOLD}" {_st(2.0)}/>'
    for xx in (xb0, xb1):
        s += f'<circle cx="{fmt(xx)}" cy="{fmt(top + 24)}" r="9" fill="{GOLD}" {_st(2.8)}/>'
    s += f'<circle cx="{fmt(xm)}" cy="{fmt(top - 16)}" r="11" fill="{GOLD}" {_st(2.8)}/>'
    s += (f'<rect x="{fmt(xb0 - 8)}" y="{fmt(seat_y - 6)}" width="{fmt(x_front - xb0 + 16)}" height="20" rx="7" '
          f'fill="{wood}" {_st(OW)}/>')
    s += _line(f"M{fmt(xb0 + 2)},{fmt(seat_y + 4)} L{fmt(x_front - 2)},{fmt(seat_y + 4)}", w=3, col=GOLD)
    return s


def _ash_heap(st):
    pel, g = st["pel"], st["ground"] or 0
    m = st["m"]
    w = 2.2 * m["th"] + 70
    cx = pel[0] + 0.35 * m["th"]
    d = (f"M{fmt(cx - w / 2)},{fmt(g)} Q{fmt(cx - w / 3)},{fmt(g - 26)} {fmt(cx - w / 8)},{fmt(g - 20)} "
         f"Q{fmt(cx)},{fmt(g - 34)} {fmt(cx + w / 6)},{fmt(g - 22)} Q{fmt(cx + w / 2.6)},{fmt(g - 24)} "
         f"{fmt(cx + w / 2)},{fmt(g)} Z")
    s = f'<path d="{d}" fill="{P["ash"]}" {_st(OW)}/>'
    for dx, dy in ((-0.3, -9), (0.05, -14), (0.32, -8), (-0.12, -6)):
        s += _ell(cx + dx * w, g + dy, 7, 3.5, shade(P["ash"], -0.2), extra='opacity="0.7"')
    return s


def _king_design(attire, pose, throne, ashes):
    sack = attire == "sackcloth"
    D = dict(skin="#d9a27a", leg="#d9a27a", hem=0.95, ears=False, long_hair=KING_HAIR, hair=KING_HAIR,
             hair_style="curly", beard=("assyrian", KING_HAIR), sandal=GOLD_DARK)
    if sack:
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], sandal=None, bare=True)
    else:
        D.update(robe=P["royal"], sleeve=P["royal"], hem_col=GOLD, fringe=GOLD, shawl=P["royal_light"],
                 shawl_trim=GOLD, cuff=GOLD, sash=GOLD, sash_tail=False, collar=GOLD, hem_w=11)
        if pose != "remove_crown":
            D.update(hat=("crown",), hat_h=1.75)
    if attire == "darius":       # Persian king: crenellated crown, purple robe with gold flowers, curled beard
        D.update(skin="#dba57f", leg="#dba57f", long_hair=DARIUS_HAIR, hair=DARIUS_HAIR,
                 beard=("assyrian", DARIUS_HAIR), robe=DARIUS_ROBE, sleeve=DARIUS_ROBE, hem_col=GOLD, hem_w=14,
                 fringe=None, shawl=None, cuff=GOLD, sash=GOLD, sash_tail=True, collar=GOLD,
                 pattern=(shade(GOLD, 0.1), "flower", 27), neck_v=shade(GOLD, 0.25))
        if pose != "remove_crown":
            D.update(hat=("darius",), hat_h=1.55)
    if pose in _KING_SEATED and throne:
        D["behind"] = _throne
    if pose in ("sign", "sit_sign"):
        D["front"] = _sign_front(D, pose == "sit_sign")
    if pose == "sit_ashes" and ashes:
        D["behind"] = _ash_heap
    if pose == "remove_crown":
        def held(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            R = st["m"]["R"]
            c = _lerp(W0, W1, 0.5)
            cr = (_darius_crown(R, x0=-0.05 * R, y0=0.58 * R) if attire == "darius" else
                  _crown(R, x0=-0.05 * R, y0=0.58 * R, k=1.0, tilt=1.0))
            s = f'<g transform="translate({_pt(c)}) rotate(-8)">{cr}</g>'
            for W in (W0, W1):
                s += f'<circle cx="{fmt(W[0])}" cy="{fmt(W[1])}" r="{fmt(st["m"]["hr"])}" fill="{D["skin"]}" {_st(3.2)}/>'
            return s
        D["front"] = held
    return D


def king(x, y, scale=1.0, facing=1, pose="stand", attire=None, expr=None, throne=True, ashes=True, marks=True,
         stool=True):
    if pose not in KING_POSES + KING_EXTRA_POSES:
        raise ValueError(f"king: unknown pose {pose!r}; choose from {sorted(KING_POSES + KING_EXTRA_POSES)}")
    ps = dict(POSES[_KING_ALIAS.get(pose, pose)])
    if attire == "saul" or pose in KING_EXTRA_POSES:
        return _king_david_film(x, y, scale, facing, pose, attire, expr, ps, throne, stool, marks)
    _check_expr(expr, "king")
    if attire is None:
        attire = "sackcloth" if pose == "sit_ashes" else "royal"
    if attire not in KING_ATTIRES:
        raise ValueError(f"king: unknown attire {attire!r}; choose from {KING_ATTIRES}")
    if pose == "sit_ashes" and attire in ("royal", "darius"):
        raise ValueError("king: pose 'sit_ashes' is in sackcloth (Jonah 3:6) - use attire='sackcloth' or omit it")
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose == "stand":
        e = "sad"
    D = _king_design(attire, pose, throne, ashes)
    if pose == "remove_crown":
        R = _KING_M["R"]
        cx, cy = 50.0, -40.0
        ps["arms"] = (("ik", "body", cx + 0.80 * R, cy, 1), ("ik", "body", cx - 0.86 * R, cy + 2, 1))
        ps["hands"] = ("none", "none")
    inner, _ = _figure(D, _KING_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"king-{pose}")


# ---------------------------------------------------------------- citizens
CITIZEN_POSES = ("stand", "walk", "walk_a", "walk_b", "listen", "kneel_pray", "point", "sad", "cheer")
CITIZEN_KINDS = ("man", "woman", "child", "elder")
CITIZEN_ATTIRES = ("normal", "sackcloth")
_CIT_COL = [
    dict(robe="#d9b98a", trim=P["terracotta"], skin="#e2a77e", hair="#4a2f1f"),
    dict(robe="#94505e", trim="#d9b46a", skin="#c68a62", hair="#2f2420"),
    dict(robe=P["olive"], trim="#e0b25a", skin="#a46b47", hair="#2a201b"),
    dict(robe="#4b5a8f", trim="#e8d3a8", skin="#eab48c", hair="#5a3a24"),
]


def _citizen_design(kind, variant, attire):
    c = _CIT_COL[variant % 4]
    robe = c["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.22), skin=c["skin"], leg=c["skin"], hem=0.90,
             cuff=shade(robe, -0.22))
    if kind == "man":
        D.update(hair=c["hair"], hair_style="curly", beard=("assyrian_short", c["hair"]), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25), hat=("wrap", c["trim"], shade(c["trim"], -0.2))
                 if variant % 2 else None, long_hair=None if variant % 2 else c["hair"])
    elif kind == "woman":
        D.update(hair=c["hair"], hair_style="short", hat=("veil", c["trim"], shade(robe, -0.1)),
                 veil=c["trim"], ears=False, sash=shade(c["trim"], -0.15), sash_tail=True)
    elif kind == "child":
        girl = variant % 2 == 1
        D.update(hair=c["hair"], hair_style="short" if girl else "curly", hem=0.56, flare_k=0.9,
                 rope_belt=c["trim"], sleeve_len=0.55)
        if girl:
            D.update(ponytail=c["hair"], ribbon=c["trim"])
    elif kind == "elder":
        D.update(hair="#e4ddd0", hair_style="short", beard=("white", "#ece6da"), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25))
        if variant % 2:
            D.update(hat=("wrap", c["trim"], shade(c["trim"], -0.25)))
    if attire == "sackcloth":
        for key in ("shawl", "shawl_trim", "sash", "hat"):
            D.pop(key, None)
        if kind == "woman":
            D.update(hat=("veil", P["sackcloth"], None), veil=P["sackcloth"])
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], bare=True)
    return D


def _cane(st):
    W = st["arms"][1][2]
    g = st["ground"] or 0
    return (_tube([(W[0] + 2, W[1] - 10), (W[0] + 8, g - 2)], 6, P["wood"], ow=2.6) +
            _tube([(W[0] + 2, W[1] - 10), (W[0] - 8, W[1] - 16)], 6, P["wood"], ow=2.6))


def citizen(x, y, scale=1.0, facing=1, kind="man", variant=0, pose="stand", attire="normal", expr=None,
            marks=True):
    if kind not in CITIZEN_KINDS:
        raise ValueError(f"citizen: unknown kind {kind!r}; choose from {CITIZEN_KINDS}")
    if attire not in CITIZEN_ATTIRES:
        raise ValueError(f"citizen: unknown attire {attire!r}; choose from {CITIZEN_ATTIRES}")
    _check_expr(expr, "citizen")
    _resolve_pose(pose, CITIZEN_POSES, "citizen")
    ps = dict(POSES["listen_chin" if pose == "listen" else pose])
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose in ("stand", "walk", "walk_a", "walk_b"):
        e = "sad"
    D = _citizen_design(kind, variant, attire)
    m = _ADULT
    if kind == "child":
        m = _CHILD
    elif kind == "woman":
        m = _metrics(_ADULT, 0.96, 0.92)
    elif kind == "elder":
        m = _metrics(_ADULT, 0.97, 1.0)
        if pose in ("stand", "walk", "walk_a", "walk_b", "sad", "listen"):
            ps["t"] = ps["t"] + 8
            if pose != "listen":
                ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
                D["front"] = _cane
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"{kind}{variant}-{pose}")


# ======================================================================= Daniel film (Daniel 6)
# ---------------------------------------------------------------- Daniel
DANIEL_POSES = ("stand", "walk_a", "walk_b", "kneel_pray", "kneel_up", "kneel_bow", "sit", "sit_pray", "explain",
                "point", "look_up", "answer", "bow", "read", "hold_rope", "arms_up", "sad", "listen")
DANIEL_BLUE = "#41629a"
DANIEL_SKIN = "#e2a882"
_DANIEL_M = _metrics(_ADULT, 1.02, 1.05)


def _daniel_design():
    blue = DANIEL_BLUE
    return dict(robe=blue, sleeve=blue, hem_col=shade(blue, -0.28), cuff=shade(blue, -0.28), sash=P["gold"],
                skin=DANIEL_SKIN, leg=DANIEL_SKIN, hem=0.92, hat=("headcloth", P["headcloth"], P["gold"]),
                tail=(P["headcloth"], blue), ears=False, beard=("trim", "#57392a"),
                neck_v=shade(P["headcloth"], -0.12))


def daniel(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    """Daniel: kind grown man, deep-blue robe, gold sash, cream head-cloth with a gold band (see module doc)."""
    if pose not in DANIEL_POSES:
        raise ValueError(f"daniel: unknown pose {pose!r}; choose from {sorted(DANIEL_POSES)}")
    _check_expr(expr, "daniel")
    ps = dict(POSES["listen_chin" if pose == "listen" else pose])
    if pose in ("kneel_pray", "sit"):
        ps["expr"] = "peaceful" if pose == "kneel_pray" else "neutral"
    e = expr or ps["expr"]
    D = _daniel_design()
    if pose == "read":
        D["front"] = _read_front(D)
    inner, _ = _figure(D, _DANIEL_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"daniel-{pose}")


# ---------------------------------------------------------------- the jealous officials
OFFICIAL_POSES = ("stand", "walk_a", "walk_b", "whisper", "point", "bow", "peek", "scheme", "read", "sad")
_OFFICIAL_ALIAS = {"bow": "bow_low"}
_OFFICIALS = [
    dict(robe="#a8434a", pattern=("#f0c870", "diamond"), trim="#e6b45a", hat=("tallhat", "#6b3a3a", "#e6b45a"),
         skin="#e2a77e", hair="#2c211c", beard=("pointed", "#2c211c")),
    dict(robe="#547a40", pattern=("#eadcae", "flower"), trim="#e9d9ae", hat=("turban", "#eadbb8", "#c0533a"),
         skin="#b9805a", hair="#3a2a22", beard=("assyrian_short", "#3a2a22")),
    dict(robe="#9a5a36", pattern=("#8fcad3", "dots"), trim="#5fa8a6", hat=("tallhat", "#e0c48e", "#3b8b89"),
         skin="#d39a72", hair="#9d968c", beard=("pointed", "#a8a196")),
    dict(robe="#c49a3c", pattern=("#8a3c3c", "diamond"), trim="#8a3c3c", hat=("turban", "#3c7d84", "#e8b63c"),
         skin="#8d5a3b", hair="#2a201b", beard=("assyrian_short", "#5e3a26")),
]


def _official_design(variant):
    v = _OFFICIALS[variant % 4]
    sp = 22 if v["pattern"][1] != "dots" else 18
    return dict(robe=v["robe"], sleeve=v["robe"], hem_col=v["trim"], cuff=v["trim"], hem_w=12, skin=v["skin"],
                leg=v["skin"], hem=0.97, flare_k=0.8, pattern=(v["pattern"][0], v["pattern"][1], sp),
                sash=shade(v["trim"], -0.18), sash_tail=False, hair=v["hair"], hair_style="curly",
                long_hair=v["hair"] if v["hat"][0] == "tallhat" else None, hat=v["hat"],
                hat_h=1.10 if v["hat"][0] == "tallhat" else 0.56, beard=v["beard"], sandal=SANDAL_DARK)


_OFFICIAL_M = _metrics(_ADULT, 1.0, 1.04)


def official(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, marks=True):
    """One of the jealous Persian officials (variant 0-3); gentle 'sly' / 'smug' faces (see module doc)."""
    if pose not in OFFICIAL_POSES:
        raise ValueError(f"official: unknown pose {pose!r}; choose from {sorted(OFFICIAL_POSES)}")
    _check_expr(expr, "official")
    ps = dict(POSES[_OFFICIAL_ALIAS.get(pose, pose)])
    if pose == "point":
        ps["expr"] = "sly"
    if pose == "read":
        ps["expr"] = "worried"
    e = expr or ps["expr"]
    D = _official_design(variant)
    if pose == "read":
        D["front"] = _read_front(D)
    inner, _ = _figure(D, _OFFICIAL_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"official{variant % 4}-{pose}")


# ---------------------------------------------------------------- palace guards
GUARD_POSES = ("stand", "walk_a", "walk_b", "push", "pull_rope")
_GUARD_ALIAS = {"stand": "guard_stand", "walk_a": "guard_walk_a", "walk_b": "guard_walk_b"}
_GUARDS = [
    dict(tunic="#b5523b", trim="#e8c27a", legs="#7a5c42", skin="#dca57c", hair="#3a2a22",
         beard=("stubble", "#3a2a22"), helmet="#c99252", plume="#c0533a", shield="#4f86b0"),
    dict(tunic="#6f8a45", trim="#e9d9ae", legs="#5e4a3a", skin="#a46b47", hair="#241b17", beard=None,
         helmet="#c99252", plume="#e0a23c", shield="#b5523b"),
    dict(tunic="#c99a42", trim="#8a3c3c", legs="#6b4a3a", skin="#e8b28c", hair="#7a4a2a",
         beard=("short", "#7a4a2a"), helmet="#b98a4e", plume="#3b8b89", shield="#6f8a45"),
    dict(tunic="#4f7f8f", trim="#e6b45a", legs="#5a4636", skin="#c68a62", hair="#2f2420",
         beard=("assyrian_short", "#2f2420"), helmet="#c99252", plume="#c0533a", shield="#c99a42"),
]
SPEAR_WOOD = "#9a6a40"
SPEAR_TIP = "#c9c2b4"


def _shield_back(col):
    """Round shield slung on the back (drawn behind the body)."""
    def behind(st):
        m, tp = st["m"], st["tp"]
        c = tp(-0.95 * m["ww"], 0.62 * m["T"])
        r = 0.98 * m["R"]
        s = f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}" fill="{col}" {_st(OW)}/>'
        s += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r * 0.78)}" fill="none" {_st(2.6, GOLD)}/>'
        for k in range(8):
            a = math.pi * k / 4
            s += (f'<circle cx="{fmt(c[0] + 0.55 * r * math.cos(a))}" cy="{fmt(c[1] + 0.55 * r * math.sin(a))}" '
                  f'r="{fmt(0.07 * r)}" fill="{GOLD}"/>')
        s += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r * 0.26)}" fill="{GOLD}" {_st(2.6)}/>'
        return s
    return behind


def _spear_front(D):
    """Upright spear in the near hand: wooden shaft, soft leaf-shaped blade, round pomegranate butt."""
    def front(st):
        W, R, skin = st["arms"][1][2], st["m"]["R"], D["skin"]
        hr = st["m"]["hr"]
        x = W[0] + 2
        y_top = st["Hc"][1] - 2.25 * R
        y_bot = min(st["ground"] - 6, W[1] + 150)
        s = _tube([(x, y_bot), (x, y_top + 30)], 7, SPEAR_WOOD, ow=3.0)
        s += (f'<path d="M{fmt(x)},{fmt(y_top - 6)} Q{fmt(x + 13)},{fmt(y_top + 16)} {fmt(x + 6)},{fmt(y_top + 34)} '
              f'L{fmt(x - 6)},{fmt(y_top + 34)} Q{fmt(x - 13)},{fmt(y_top + 16)} {fmt(x)},{fmt(y_top - 6)} Z" '
              f'fill="{SPEAR_TIP}" {_st(3.0)}/>')
        s += _line(f"M{fmt(x)},{fmt(y_top + 2)} L{fmt(x)},{fmt(y_top + 28)}", w=1.8, col=shade(SPEAR_TIP, -0.3))
        s += f'<rect x="{fmt(x - 6)}" y="{fmt(y_top + 32)}" width="12" height="9" rx="3" fill="{GOLD}" {_st(2.4)}/>'
        s += f'<circle cx="{fmt(x)}" cy="{fmt(y_bot - 2)}" r="9" fill="{GOLD}" {_st(2.6)}/>'
        s += _line(f"M{fmt(x - 4)},{fmt(y_bot - 11)} L{fmt(x)},{fmt(y_bot - 15)} L{fmt(x + 4)},{fmt(y_bot - 11)}",
                   w=2.2, col=GOLD_DARK)
        s += f'<circle cx="{fmt(W[0] + 0.3 * hr)}" cy="{fmt(W[1] + 0.2 * hr)}" r="{fmt(hr)}" fill="{skin}" {_st(3.2)}/>'
        return s
    return front


def _guard_design(variant, spear):
    v = _GUARDS[variant % 4]
    D = dict(robe=v["tunic"], sleeve=v["tunic"], hem_col=v["trim"], cuff=v["trim"], hem_w=10, skin=v["skin"],
             leg=v["legs"], hem=0.60, flare_k=0.7, rope_belt="#8b5a35", hair=v["hair"], hair_style="short",
             hat=("helmet", v["helmet"], v["plume"]), hat_h=0.45, beard=v["beard"], sandal=SANDAL_DARK,
             neck_v=v["trim"], behind=_shield_back(v["shield"]))
    if spear:
        D["front"] = _spear_front(D)
    return D


def guard(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, spear=None, marks=True):
    """Friendly palace guard (variant 0-3) with a round shield on his back and a spear (see module doc)."""
    if pose not in GUARD_POSES:
        raise ValueError(f"guard: unknown pose {pose!r}; choose from {sorted(GUARD_POSES)}")
    _check_expr(expr, "guard")
    ps = dict(POSES[_GUARD_ALIAS.get(pose, pose)])
    if spear is None:
        spear = pose in ("stand", "walk_a", "walk_b")
    if not spear and pose in _GUARD_ALIAS:       # empty hand: relaxed arm instead of the spear grip
        ps["arms"] = (ps["arms"][0], POSES[pose]["arms"][1])
    e = expr or ps["expr"]
    inner, _ = _figure(_guard_design(variant, spear), _ADULT, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"guard{variant % 4}-{pose}")


# ======================================================================= David film (1 Samuel 17)
# David (a shepherd boy), Goliath, his shield-bearer, Israelite / Philistine soldiers, King Saul
# (king(attire='saul')), Eliab and Jesse. See the module doc section "David film".


def _prp():
    from art import props as PR          # lazy: art.props never imports this module
    return PR


BRONZE = "#c99a48"
BRONZE_DARK = shade(BRONZE, -0.32)
BRONZE_LIGHT = shade(BRONZE, 0.42)
LEATHER = "#8b5a35"
LEATHER_LIGHT = "#b98552"
CORD = "#c9a46a"
IRON = "#a9adab"
CREST_RED = "#b8473c"
MAIL = "#a3a6a0"
DAVID_TUNIC = "#7fa24f"
DAVID_SKIN = "#efbb94"
DAVID_HAIR = "#a5552c"
GOLIATH_SKIN = "#dc9c78"
GOLIATH_TUNIC = "#a8433a"
SAUL_TUNIC = "#4a6aa0"
GOLIATH_HAIR = "#3a2a22"
SAUL_HAIR = "#2b2220"

# ---------------------------------------------------------------- expressions and mouths
EXPRS.update({
    "brave":   dict(eyes="dot", brow=(0.07, -0.03, 0.01), mouth="firm"),
    "puzzled": dict(eyes="dot", brow=(0.05, 0.0, 0.05), brow2=(-0.05, -0.03, -0.13), mouth="puzzle",
                    look=(0.02, -0.03)),
    "laugh":   dict(eyes="arc", brow=(-0.03, 0.02, -0.08), mouth="laugh"),
    "cross":   dict(eyes="dot", brow=(0.13, -0.06, 0.05), mouth="pout"),
    "sneer":   dict(eyes="lidded", brow=(0.10, -0.06, 0.02), mouth="sneer"),
    "kind":    dict(eyes="dot", brow=(-0.09, 0.04, -0.03), mouth="smile", blush=True),
    "roar":    dict(eyes="dot", brow=(0.12, -0.06, 0.02), mouth="shout"),
})
DAVID_EXPRESSIONS = ("brave", "puzzled", "laugh", "cross", "sneer", "kind", "roar")
ALL_EXPRESSIONS = EXPRESSIONS + DAVID_EXPRESSIONS


def _mouth_extra(R, kind, P_, mx, my):
    """Mouth shapes added for the David film (called by _mouth for kinds it does not know)."""
    MI = P["mouth_inside"]
    if kind == "laugh":             # big open D-shaped laugh: top teeth, tongue
        outline = (f"M{P_(-0.22, -0.03)} Q{P_(0, 0.03)} {P_(0.22, -0.03)} Q{P_(0.21, 0.33)} {P_(0, 0.35)} "
                   f"Q{P_(-0.21, 0.33)} {P_(-0.22, -0.03)} Z")
        teeth = (f"M{P_(-0.19, -0.01)} Q{P_(0, 0.04)} {P_(0.19, -0.01)} L{P_(0.18, 0.05)} Q{P_(0, 0.10)} "
                 f"{P_(-0.18, 0.05)} Z")
        return (f'<path d="{outline}" fill="{MI}"/>' + f'<path d="{teeth}" fill="{EYE_WHITE}"/>' +
                _ell(mx, my + 0.25 * R, 0.11 * R, 0.065 * R, TONGUE) + f'<path d="{outline}" fill="none" {_st(2.8)}/>')
    if kind == "firm":              # closed, confident little smile
        return (_line(f"M{P_(-0.15, 0.01)} Q{P_(-0.01, 0.09)} {P_(0.15, -0.03)}", w=3.2) +
                _line(f"M{P_(0.13, -0.06)} Q{P_(0.17, -0.03)} {P_(0.16, 0.01)}", w=2.4))
    if kind == "puzzle":            # slanted 'hmm?'
        return _line(f"M{P_(-0.09, 0.07)} Q{P_(0.02, 0.01)} {P_(0.13, 0.0)}", w=3.2)
    if kind == "pout":              # cross frown with a pushed-out lower lip
        return (_line(f"M{P_(-0.12, 0.07)} Q{P_(0, -0.04)} {P_(0.12, 0.07)}", w=3.4) +
                _line(f"M{P_(-0.05, 0.13)} Q{P_(0, 0.15)} {P_(0.05, 0.13)}", w=2.2, col=P["ink_soft"]))
    if kind == "cry":               # Joseph film: an open, wobbly, downturned crying mouth
        d = (f"M{P_(-0.16, 0.10)} Q{P_(-0.08, -0.02)} {P_(0, 0.0)} Q{P_(0.08, -0.02)} {P_(0.16, 0.10)} "
             f"Q{P_(0.10, 0.24)} {P_(0, 0.22)} Q{P_(-0.10, 0.24)} {P_(-0.16, 0.10)} Z")
        return (f'<path d="{d}" fill="{MI}" {_st(2.8)}/>' + _ell(mx, my + 0.17 * R, 0.06 * R, 0.035 * R, TONGUE))
    if kind == "awe":               # Noah film: open, delighted 'oh!' smile
        d = (f"M{P_(-0.13, 0.0)} Q{P_(0, 0.03)} {P_(0.13, 0.0)} Q{P_(0.12, 0.26)} {P_(0, 0.27)} "
             f"Q{P_(-0.12, 0.26)} {P_(-0.13, 0.0)} Z")
        return f'<path d="{d}" fill="{MI}" {_st(2.8)}/>' + _ell(mx, my + 0.19 * R, 0.07 * R, 0.045 * R, TONGUE)
    if kind == "sneer":             # lopsided grin showing teeth (cartoon-smug, not scary)
        d = (f"M{P_(-0.15, 0.03)} Q{P_(0.03, 0.08)} {P_(0.19, -0.07)} Q{P_(0.14, 0.13)} {P_(0.0, 0.14)} "
             f"Q{P_(-0.12, 0.12)} {P_(-0.15, 0.03)} Z")
        return (f'<path d="{d}" fill="{EYE_WHITE}" {_st(2.8)}/>' +
                _line(f"M{P_(-0.12, 0.075)} Q{P_(0.03, 0.105)} {P_(0.16, 0.0)}", w=1.8, col=P["ink_soft"]))
    return ""


# ---------------------------------------------------------------- headwear (head frame, fn(R))


def _union_circles(circ, col, ow=3.0):
    return ("".join(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{col}" {_st(2 * ow)}/>' for x, y, r in circ)
            + "".join(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{col}"/>' for x, y, r in circ))


def _curls_svg(R, col, cheeks=True):
    """Reddish-brown curly mop: a ring of round curls over the top and back of the head, two fringe curls."""
    circ = []
    for i, a in enumerate(range(-36, -186, -21)):
        x, y = _polar(R, a, 0.97)
        circ.append((x, y, (0.27 if i % 2 else 0.235) * R))
    circ += [(0.58 * R, -0.66 * R, 0.17 * R), (0.30 * R, -0.77 * R, 0.19 * R), (-0.10 * R, -0.80 * R, 0.2 * R)]
    s = _union_circles(circ, col)
    dark = shade(col, -0.28)
    for x, y, r in circ:
        s += _line(f"M{fmt(x - 0.45 * r)},{fmt(y + 0.1 * r)} Q{fmt(x - 0.2 * r)},{fmt(y - 0.55 * r)} {fmt(x + 0.35 * r)},"
                   f"{fmt(y - 0.25 * r)}", w=2.0, col=dark)
    if cheeks:                      # ruddy (1 Sam 16:12): an extra warm flush over the cheeks
        s += _ell(-0.30 * R, 0.38 * R, 0.21 * R, 0.13 * R, P["cheek"], extra='opacity="0.38"')
        s += _ell(0.68 * R, 0.40 * R, 0.16 * R, 0.12 * R, P["cheek"], extra='opacity="0.38"')
    return s


def _bronze_helmet_svg(R, col=BRONZE, crest=None, circlet=False, plume=None, guard=1.0):
    """Bronze helmet sitting high on the head (the forehead shows): dome, neck guard, brim band with rivets.
    crest: colour of a comb crest arching front-to-back; circlet: gold royal band; plume: a small plume colour."""
    s = ""
    if crest:
        outer, inner = [], []
        for i in range(10):
            u = i / 9
            a = -62 - 112 * u
            outer.append(_polar(R, a, 1.17 + 0.46 * math.sin(math.pi * (0.15 + 0.75 * u))))
            inner.append(_polar(R, a, 1.06))
        s += f'<path d="{smooth_path(outer + inner[::-1])}" fill="{crest}" {_st(3.2)}/>'
        for i in range(1, 9):
            u = i / 9
            a = -62 - 112 * u
            p0, p1 = _polar(R, a, 1.12), _polar(R, a, 1.12 + 0.36 * math.sin(math.pi * (0.15 + 0.75 * u)))
            s += _line(f"M{_pt(p0)} L{_pt(p1)}", w=2.0, col=shade(crest, -0.3))
    if plume:
        s += _tube([(-0.05 * R, -1.22 * R), (-0.30 * R, -1.62 * R), (-0.66 * R, -1.70 * R)], 0.2 * R, plume, ow=2.4)
    pts = [(0.93 * R, -0.50 * R), (0.88 * R, -0.92 * R), (0.42 * R, -1.24 * R), (-0.28 * R, -1.28 * R),
           (-0.88 * R, -0.98 * R), (-1.13 * R, -0.44 * R), (-1.15 * R, (-0.44 + 0.72 * guard) * R),
           (-0.84 * R, (-0.44 + 0.80 * guard) * R),
           (-0.70 * R, -0.30 * R), (0.10 * R, -0.62 * R)]
    s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(-0.58 * R)},{fmt(-1.02 * R)} Q{fmt(0.0)},{fmt(-1.18 * R)} {fmt(0.58 * R)},{fmt(-0.98 * R)}",
               w=3.2, col=shade(col, 0.4))
    if guard > 0.7:
        s += _line(f"M{fmt(-0.98 * R)},{fmt(-0.20 * R)} Q{fmt(-0.95 * R)},{fmt(0.10 * R)} {fmt(-1.0 * R)},{fmt(0.24 * R)}",
                   w=2.2, col=shade(col, -0.25))
    s += _tube(_spline_pts([(0.97 * R, -0.52 * R), (0.42 * R, -0.70 * R), (-0.30 * R, -0.68 * R),
                            (-1.02 * R, -0.36 * R)]), 0.15 * R, shade(col, -0.22), ow=2.6)
    for x0, y0 in ((0.62, -0.62), (0.15, -0.70), (-0.35, -0.66), (-0.80, -0.48)):
        s += f'<circle cx="{fmt(x0 * R)}" cy="{fmt(y0 * R)}" r="{fmt(0.045 * R)}" fill="{shade(col, 0.45)}"/>'
    if circlet:
        s += _tube(_spline_pts([(0.92 * R, -0.80 * R), (0.35 * R, -0.98 * R), (-0.40 * R, -0.95 * R),
                                (-0.98 * R, -0.66 * R)]), 0.13 * R, GOLD, ow=2.4)
        for x0, y0 in ((0.62, -0.92), (0.05, -1.0), (-0.52, -0.92)):
            s += (f'<path d="M{fmt((x0 - 0.1) * R)},{fmt((y0 - 0.04) * R)} L{fmt(x0 * R)},{fmt((y0 - 0.30) * R)} '
                  f'L{fmt((x0 + 0.1) * R)},{fmt((y0 - 0.04) * R)} Z" fill="{GOLD}" {_st(2.2)}/>')
            s += f'<circle cx="{fmt(x0 * R)}" cy="{fmt((y0 - 0.33) * R)}" r="{fmt(0.05 * R)}" fill="{P["royal_light"]}"/>'
    return s


def _david_head(armor):
    def hat(R):
        if not armor:
            return _curls_svg(R, DAVID_HAIR, cheeks=True)
        # Saul's helmet, far too big: it slides down over his eyes (only the nose, cheeks and mouth show)
        s = _ell(-0.30 * R, 0.40 * R, 0.21 * R, 0.13 * R, P["cheek"], extra='opacity="0.38"')
        s += _ell(0.68 * R, 0.42 * R, 0.16 * R, 0.12 * R, P["cheek"], extra='opacity="0.38"')
        s += (f'<g transform="translate({fmt(-0.05 * R)},{fmt(1.40 * R)}) rotate(7)">'
              f'{_bronze_helmet_svg(2.0 * R, BRONZE, plume=CREST_RED, circlet=True, guard=0.45)}</g>')
        return s
    return hat


def _leather_cap_svg(R, col):
    """Israelite soldier's small rounded leather cap with seams, a rolled edge and a top knob."""
    pts = [(0.95 * R, -0.40 * R), (0.86 * R, -0.90 * R), (0.30 * R, -1.20 * R), (-0.45 * R, -1.16 * R),
           (-0.98 * R, -0.72 * R), (-1.10 * R, -0.22 * R), (-0.66 * R, -0.36 * R), (0.10 * R, -0.52 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    for x in (-0.40, 0.25):
        s += _line(f"M{fmt(x * R)},{fmt(-0.62 * R)} Q{fmt((x + 0.08) * R)},{fmt(-0.95 * R)} {fmt((x - 0.02) * R)},"
                   f"{fmt(-1.16 * R)}", w=2.0, col=shade(col, -0.3))
    s += _tube(_spline_pts([(0.98 * R, -0.42 * R), (0.40 * R, -0.60 * R), (-0.35 * R, -0.56 * R),
                            (-1.08 * R, -0.24 * R)]), 0.15 * R, shade(col, -0.15), ow=2.6)
    s += f'<circle cx="{fmt(-0.08 * R)}" cy="{fmt(-1.20 * R)}" r="{fmt(0.10 * R)}" fill="{shade(col, 0.15)}" {_st(2.4)}/>'
    return s


def _feather_band_svg(R, band, feather):
    """Philistine feathered headdress: a patterned band round the head with a crown of upright feathers."""
    s = ""
    n = 12
    for k in range(n):                   # a neat crown of upright reeds / feathers (Medinet Habu style)
        u = k / (n - 1)
        x = (-0.86 + 1.66 * u) * R
        by = -0.50 * R - 0.14 * R * (1 - ((x / R - 0.05) / 0.95) ** 2)
        top = by - (0.62 + 0.06 * math.sin(math.pi * u)) * R
        x2 = x + 0.05 * R * (u - 0.5)
        w = 0.085 * R
        pts = [(x - w, by), (x2 - w * 0.9, top + w), (x2, top - 0.02 * R), (x2 + w * 0.9, top + w), (x + w, by)]
        col = feather if k % 2 == 0 else shade(feather, -0.14)
        s += f'<path d="{smooth_path(pts, tension=0.5)}" fill="{col}" {_st(2.4)}/>'
        s += _line(f"M{fmt(x)},{fmt(by - 0.06 * R)} L{fmt(x2)},{fmt(top + 0.12 * R)}", w=1.4, col=shade(feather, -0.35))
    s += _tube(_spline_pts([(0.98 * R, -0.40 * R), (0.45 * R, -0.62 * R), (-0.25 * R, -0.62 * R),
                            (-1.0 * R, -0.30 * R)]), 0.2 * R, band, ow=2.6)
    for x0, y0 in ((0.62, -0.52), (0.15, -0.63), (-0.35, -0.60), (-0.80, -0.40)):
        s += f'<circle cx="{fmt(x0 * R)}" cy="{fmt(y0 * R)}" r="{fmt(0.05 * R)}" fill="{shade(band, 0.5)}"/>'
    return s


def _goliath_head(bump):
    def hat(R):
        s = _bronze_helmet_svg(R, BRONZE, crest=CREST_RED)
        if bump:                    # the cartoon bump where the stone hit (no blood)
            s += _ell(0.38 * R, -0.43 * R, 0.17 * R, 0.13 * R, "#ec9a86", sw=2.8)
            s += _ell(0.33 * R, -0.47 * R, 0.06 * R, 0.035 * R, HI, extra='opacity="0.85"')
        return s
    return hat


# ---------------------------------------------------------------- held / worn items (body-frame hooks)


def _hooks(*fns):
    fns = [f for f in fns if f]
    if not fns:
        return None
    return lambda st: "".join(f(st) for f in fns)


def _fist(W, hr, skin, dx=0.0, dy=0.0):
    return f'<circle cx="{fmt(W[0] + dx)}" cy="{fmt(W[1] + dy)}" r="{fmt(hr)}" fill="{skin}" {_st(3.2)}/>'


def _bag_mid(st):
    """Leather shepherd's bag on the back hip, its strap across the chest from the near shoulder."""
    m, tp = st["m"], st["tp"]
    top = tp(-0.80 * m["ww"], 4)
    w, h = 0.70 * m["ww"] + 16, 0.45 * m["T"] + 4
    cx, y0 = top[0] - 2, top[1]
    s = _tube([_add(st["S"][1], (-2, -3)), tp(0.1 * m["ww"], 0.45 * m["T"]), (cx + 0.3 * w, y0 + 3)], 4.5, LEATHER,
              ow=2.2)
    body = [(cx - w / 2, y0), (cx + w / 2, y0), (cx + w / 2 + 2, y0 + 0.6 * h), (cx + w * 0.3, y0 + h),
            (cx - w * 0.3, y0 + h), (cx - w / 2 - 2, y0 + 0.6 * h)]
    s += f'<path d="{smooth_path(body, tension=0.7)}" fill="{LEATHER_LIGHT}" {_st(3.0)}/>'
    flap = [(cx - w / 2 - 1, y0 - 1), (cx + w / 2 + 1, y0 - 1), (cx + w * 0.35, y0 + 0.5 * h), (cx, y0 + 0.62 * h),
            (cx - w * 0.35, y0 + 0.5 * h)]
    s += f'<path d="{smooth_path(flap, tension=0.7)}" fill="{LEATHER}" {_st(2.8)}/>'
    s += f'<circle cx="{fmt(cx)}" cy="{fmt(y0 + 0.5 * h)}" r="3.6" fill="{CORD}" {_st(1.8)}/>'
    s += _line(f"M{fmt(cx - w * 0.3)},{fmt(y0 + 0.82 * h)} l{fmt(w * 0.2)},0 m{fmt(w * 0.12)},0 l{fmt(w * 0.2)},0",
               w=1.6, col=shade(LEATHER, -0.2), extra='stroke-dasharray="3 3"')
    return s


def _crook(x, y_top, y_bot, hook=1, w=7.0):
    """Shepherd's crook: straight shaft, a round hook at the top curling toward ``hook`` (+1 = +x)."""
    h = hook
    pts = _spline_pts([(x, y_bot), (x, y_top + 30), (x, y_top + 6), (x + 6 * h, y_top - 14), (x + 22 * h, y_top - 22),
                       (x + 36 * h, y_top - 12), (x + 38 * h, y_top + 6)], steps=5)
    return _tube(pts, w, P["wood"], ow=3.0) + _line(_d(pts[:-6], closed=False), w=1.6, col=P["wood_light"],
                                                       extra='opacity="0.7"')


def _staff_near(D):
    def front(st):
        W, R = st["arms"][1][2], st["m"]["R"]
        return _crook(W[0] + 2, st["Hc"][1] - 1.55 * R, st["ground"] - 4) + _fist(W, st["m"]["hr"], D["skin"], 0.5)
    return front


def _staff_far(st):
    W, R = st["arms"][0][2], st["m"]["R"]
    return _crook(W[0] + 1, st["Hc"][1] - 1.55 * R, st["ground"] - 4)


def _basket_hang(D, k=0.55):
    def front(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        return (f'<g transform="translate({fmt(W[0] + 3)},{fmt(W[1] + 104 * k)}) scale({k})">'
                f'{_prp()._bread_basket()}</g>' + _fist(W, hr, D["skin"], 1))
    return front


def _basket_carry(D, k=0.6):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        cx = (W0[0] + W1[0]) / 2
        y = max(W0[1], W1[1]) + 58 * k
        return (f'<g transform="translate({fmt(cx)},{fmt(y)}) scale({k})">{_prp()._bread_basket(handle=False)}</g>'
                + _fist(W1, hr, D["skin"], 0, 2))
    return front


def _harp_front(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        b = st["tp"](0.95 * st["m"]["ww"], -6)
        s = f'<g transform="translate({fmt(b[0] + 8)},{fmt(b[1] + 10)}) rotate(14) scale(0.6)">{_prp()._harp()}</g>'
        s += _fist(W0, hr, D["skin"]) + _hand(W1, (0.3, 1.0), "open", D["skin"], hr)
        return s
    return front


def _sling_cords(W, Pc, d, stone=True, open_=False):
    """Two thin cords from the hand W to a leather pouch at Pc (d = unit direction hand -> pouch)."""
    n = (-d[1], d[0])
    a, b = _add(Pc, _mul(n, 6.5)), _sub(Pc, _mul(n, 6.5))
    s = _tube([W, a], 2.4, CORD, ow=1.5) + _tube([W, b], 2.4, CORD, ow=1.5)
    c = _add(Pc, _mul(d, 4))
    if stone and not open_:
        sc = _sub(c, _mul(d, 4))
        s += _ell(sc[0], sc[1], 7.5, 6.5, "#b9b2a6", sw=2.4)
    rot = _ang(n)
    s += (f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(11 if not open_ else 12)}" ry="{fmt(6 if not open_ else 3.5)}" '
          f'transform="rotate({fmt(rot)} {fmt(c[0])} {fmt(c[1])})" fill="{LEATHER}" {_st(2.4)}/>')
    return s


def _sling_spin_hooks(D, phase, stone):
    """sling_spin: the far (front-shoulder) hand whirls the sling; the half of the whirl behind the boy is drawn
    behind the body and head, the near half in front. Returns (behind, front)."""
    a = 2 * math.pi * phase

    def geo(st):
        W, R = st["arms"][0][2], st["m"]["R"]
        L = 2.4 * R
        rx, ry = 0.88 * L, 0.30 * L
        Pc = (W[0] + rx * math.cos(a), W[1] + ry * math.sin(a) - 0.25 * rx * math.cos(a))
        return W, rx, ry, Pc

    def swirl(st):
        W, rx, ry, Pc = geo(st)
        s = ""
        for k, (span, wid, op) in enumerate(((1.9, 3.2, 0.55), (1.2, 2.4, 0.4))):
            pts = []
            for j in range(14):
                aa = a - 0.25 - span * j / 13
                kk = 1.0 + 0.10 * (k + 1)
                pts.append((W[0] + rx * kk * math.cos(aa), W[1] + ry * kk * math.sin(aa) - 0.25 * rx * kk * math.cos(aa)))
            s += _line(smooth_path(pts, closed=False), w=wid, col=MARK, extra=f'opacity="{op}"')
        return s

    def back_half(st):
        return math.cos(a) < -0.15 or (math.sin(a) < 0 and math.cos(a) < 0.25)

    def behind(st):
        W, rx, ry, Pc = geo(st)
        s = swirl(st)
        if back_half(st):
            s += _sling_cords(W, Pc, _nrm(_sub(Pc, W)), stone)
        return s

    def front(st):
        W, rx, ry, Pc = geo(st)
        if back_half(st):
            return ""
        return _sling_cords(W, Pc, _nrm(_sub(Pc, W)), stone) + _fist(W, st["m"]["hr"], D["skin"])
    return behind, front


def _sling_front(D, mode, phase=0.0, stone=True):
    """The sling (a long strap with a pouch) in the near hand: 'hold' hanging, 'spin' whirling overhead
    (pouch at ``phase`` 0..1 round a tilted circle, with swirl lines), 'release' (strap trailing forward)."""
    def front(st):
        W, hr, skin = st["arms"][0 if mode == "release" else 1][2], st["m"]["hr"], D["skin"]
        L = 2.4 * st["m"]["R"]
        s = ""
        if mode == "hold":
            d = _nrm((0.12, 1.0))
            s += _sling_cords(W, _add(W, _mul(d, 0.8 * L)), d, stone)
        elif mode == "spin":
            rx, ry = 0.88 * L, 0.30 * L
            c = W
            a = 2 * math.pi * phase
            Pc = (c[0] + rx * math.cos(a), c[1] + ry * math.sin(a) - 0.25 * rx * math.cos(a))
            # swirl: two trailing arcs behind the pouch (motion lines)
            for k, (span, wid, op) in enumerate(((1.9, 3.2, 0.55), (1.2, 2.4, 0.4))):
                pts = []
                for j in range(14):
                    aa = a - 0.25 - span * j / 13
                    kk = 1.0 + 0.10 * (k + 1)
                    pts.append((c[0] + rx * kk * math.cos(aa), c[1] + ry * kk * math.sin(aa) - 0.25 * rx * kk * math.cos(aa)))
                s += _line(smooth_path(pts, closed=False), w=wid, col=MARK, extra=f'opacity="{op}"')
            s += _sling_cords(W, Pc, _nrm(_sub(Pc, W)), stone)
        else:   # release: the strap whips forward, one cord let go, the pouch open and empty
            d = _nrm((1.0, -0.35))
            nv = (-d[1], d[0])
            pts = [_add(_add(W, _mul(d, L * t)), _mul(nv, 8 * math.sin(t * 7.0) * t)) for t in
                   [j / 10 for j in range(11)]]
            s += _tube(pts, 2.4, CORD, ow=1.5)
            end = pts[-1]
            loose = [_add(_add(end, _mul(d, 10 + 8 * j)), _mul(nv, 10 * math.sin(j * 1.4 + 1))) for j in range(6)]
            s += _tube([end] + loose, 2.4, CORD, ow=1.5)
            s += (f'<ellipse cx="{fmt(end[0])}" cy="{fmt(end[1])}" rx="12" ry="3.6" '
                  f'transform="rotate({fmt(_ang(d))} {fmt(end[0])} {fmt(end[1])})" fill="{LEATHER}" {_st(2.4)}/>')
            for j in range(3):          # whoosh marks behind the arm
                p0 = _add(W, (-30 - 14 * j, 22 + 16 * j))
                s += _line(f"M{_pt(p0)} q22,-6 40,-18", w=2.6, col=MARK, extra='opacity="0.6"')
        return s + _fist(W, hr, skin)
    return front


def _sword_hang(st, drag=False, scale_k=1.0):
    """A sword in a scabbard hanging from the belt at the near hip (drag=True: much too long, its tip trailing on the
    ground behind - Saul's sword on David)."""
    m, tp = st["m"], st["tp"]
    h0 = tp(0.55 * m["ww"], -2)
    if drag:
        tip = (-0.95 * (m["th"] + m["sh"]), st["ground"] - 6)
    elif len(st["robe"]) > 2:           # seated (lap): the scabbard lies back along the seat
        tip = _add(h0, _mul(_nrm((-1.0, 0.45)), 0.62 * (m["th"] + m["sh"])))
    else:
        tip = _add(h0, _mul(_nrm((-0.45, 1.0)), 0.80 * (m["th"] + m["sh"])))
    d = _nrm(_sub(tip, h0))
    w = 0.30 * m["aw"] * scale_k + 4
    s = _tube([h0, tip], w, shade(LEATHER, -0.1), ow=OW * 0.8)
    s += _tube([_sub(tip, _mul(d, w * 1.6)), tip], w + 2, BRONZE, ow=OW * 0.7)
    for t in (0.3, 0.6):
        q = _lerp(h0, tip, t)
        s += _line(f"M{_pt(_add(q, _mul((-d[1], d[0]), w / 2)))} L{_pt(_sub(q, _mul((-d[1], d[0]), w / 2)))}", w=2.0,
                   col=BRONZE_LIGHT)
    nv = (-d[1], d[0])
    g0 = _sub(h0, _mul(d, 2))
    s += _tube([_add(g0, _mul(nv, w * 1.3)), _sub(g0, _mul(nv, w * 1.3))], w * 0.55, BRONZE, ow=OW * 0.7)
    grip = _sub(g0, _mul(d, w * 1.9))
    s += _tube([g0, grip], w * 0.6, LEATHER, ow=OW * 0.7)
    s += f'<circle cx="{fmt(grip[0])}" cy="{fmt(grip[1])}" r="{fmt(w * 0.5)}" fill="{BRONZE}" {_st(OW * 0.7)}/>'
    return s


def _corselet(col=BRONZE, scale_col=BRONZE_DARK, sp=26, belt=LEATHER, strips=0):
    """Bronze scale armour over the torso (drawn after the tunic): the bodice of the robe plus the top of the
    skirt down to the belt, a scale pattern, a leather belt and optional leather strips (pteruges) below it."""
    mot = _scale_motif(scale_col)

    def mid(st):
        m, pel, u, f, tp = st["m"], st["pel"], st["u"], st["f"], st["tp"]
        lim = m["ww"] + 3
        polys = [st["robe"][0]]
        for poly in st["robe"][1:]:
            b = _band(poly, pel, u, -12, 6)
            if len(b) > 2:
                b = _clip(b, _sub(pel, _mul(f, lim)), f)
            if len(b) > 2:
                b = _clip(b, _add(pel, _mul(f, lim)), _mul(f, -1))
            if len(b) > 2:
                polys.append(b)
        s = ""
        if strips:
            for k in range(strips):
                x0 = (-0.85 + 1.7 * k / max(1, strips - 1)) * m["ww"]
                w = 1.5 * m["ww"] / strips
                q = [tp(x0 - w / 2, -4), tp(x0 + w / 2, -4), tp(x0 + w / 2, -0.30 * m["th"]), tp(x0 - w / 2, -0.30 * m["th"])]
                s += _poly(q, shade(belt, 0.12 if k % 2 else 0.0), sw=2.6)
        s += _union(polys, col)
        cid = _clip_id("corselet", *[_d(p) for p in polys])
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        n = int(max(max(xs) - min(xs), max(ys) - min(ys)) / sp) + 2
        cx0, cy0 = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        inner = ""
        for i in range(-n // 2 - 1, n // 2 + 2):
            for j in range(-n // 2 - 1, n // 2 + 2):
                inner += mot(_add((cx0, cy0), tp((i + (0.5 if j % 2 else 0.0)) * sp, j * sp * 0.8)), sp)
        for poly in polys:
            inner += _poly(_clip(poly, _sub(pel, _mul(f, 0.42 * m["ww"])), _mul(f, -1)), shade(col, -0.12), sw=0,
                           extra='opacity="0.5"')
        s += (f'<clipPath id="{cid}">' + "".join(f'<path d="{_d(p)}"/>' for p in polys) + "</clipPath>"
              + f'<g clip-path="url(#{cid})">{inner}</g>')
        for poly in polys:
            b = _band(poly, pel, u, -8, 8)
            if len(b) > 2:
                b = _clip(b, _sub(pel, _mul(f, lim)), f)
            if len(b) > 2:
                b = _clip(b, _add(pel, _mul(f, lim)), _mul(f, -1))
            s += _poly(b, belt, sw=2.6)
        return s
    return mid


def _greaves(col=BRONZE):
    def legwear(st, i):
        H, K, A, a1, a2 = st["legs"][i]
        lw = st["m"]["lw"]
        p0, p1 = _lerp(K, A, 0.14), _lerp(K, A, 0.93)
        c = col if i == 1 else shade(col, -0.12)
        s = _tube([p0, p1], lw + 6, c, ow=OW * 0.8)
        d = _nrm(_sub(p1, p0))
        s += _line(f"M{_pt(_add(_lerp(p0, p1, 0.12), _mul((-d[1], d[0]), lw * 0.25)))} "
                   f"L{_pt(_add(_lerp(p0, p1, 0.88), _mul((-d[1], d[0]), lw * 0.25)))}", w=2.6, col=shade(col, 0.4),
                   extra='opacity="0.8"')
        return s
    return legwear


def _scale_motif(col):
    def mot(c, sp):
        r = 0.44 * sp
        return (f'<path d="M{fmt(c[0] - r)},{fmt(c[1] - 0.3 * r)} Q{fmt(c[0] - r)},{fmt(c[1] + 0.9 * r)} {fmt(c[0])},'
                f'{fmt(c[1] + 0.9 * r)} Q{fmt(c[0] + r)},{fmt(c[1] + 0.9 * r)} {fmt(c[0] + r)},{fmt(c[1] - 0.3 * r)}" '
                f'fill="none" stroke="{col}" stroke-width="2"/>')
    return mot


def _ring_motif(col):
    def mot(c, sp):
        return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(0.30 * sp)}" fill="none" stroke="{col}" stroke-width="1.5"/>'
    return mot


def _tremble_lines(st, phase):
    """Little shake marks beside the knees (cowering soldiers)."""
    s = ""
    for (H, K, A, a1, a2), sg in zip(st["legs"], (-1, 1)):
        x0 = K[0] + sg * (st["m"]["lw"] + 10)
        for j in (0, 1):
            xx = x0 + sg * 8 * j
            s += _line(f"M{fmt(xx)},{fmt(K[1] - 12)} l{fmt(sg * 5)},7 l{fmt(-sg * 5)},7 l{fmt(sg * 5)},7", w=2.4,
                       col=MARK, extra='opacity="0.8"')
    return s


# ---------------------------------------------------------------- poses
_BOY = dict(R=40, T=64, neck=41, ua=35, fa=31, th=41, sh=39, aw=17, lw=14.5, hr=9.5, fl=23, sw=20, hw=10.5, ww=24,
            shw=29, flare=12, sdrop=10, seat=15, ank=10)
_GIANT = _metrics(_ADULT, 1.85, 1.22, R=74, neck=80, hr=21)
_SAUL_M = _metrics(_ADULT, 1.1, 1.1)
_ELIAB_M = _metrics(_ADULT, 1.07, 1.04)
_JESSE_M = _metrics(_ADULT, 0.97, 1.02)

POSES.update({
    # David
    "dv_stand_staff": _P(arms=(("fk", 14, 8), ("fk", 40, 76))),
    "dv_walk_a_staff": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -46, -36), ("fk", 40, 76))),
    "dv_walk_b_staff": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 46), ("fk", 40, 76))),
    "dv_walk_a_basket": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -46, -36), ("fk", 12, 22))),
    "dv_walk_b_basket": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 46), ("fk", 12, 22))),
    "dv_stand_basket": _P(arms=(("fk", 14, 8), ("fk", 12, 22))),
    "dv_talk": _P(h=-4, arms=(("fk", 12, 6), ("fk", 34, 86)), hands=("fist", "open"), expr="happy"),
    "dv_point_up": _P(h=-16, legs=((5, 2), (-5, -2)), arms=(("fk", 132, 162), ("fk", -10, -4)), hands=("point", "fist"),
                      look=(0.03, -0.10), expr="brave"),
    "dv_kneel_pick": _P(t=38, h=4, legs=((84, 4), (6, -92)), feet=(None, 100),
                        arms=(("ik", "knee", 0, 0.25, 1), ("ik", "abs", 96, -8, 1)), hands=("fist", "fist"),
                        look=(0.04, 0.10), expr="happy", hem=0.97),
    "dv_hold_sling": _P(h=-4, legs=((8, 3), (-7, -3)), arms=(("fk", 14, 8), ("fk", 22, 30)), expr="brave"),
    "dv_hold_sling_staff": _P(h=-4, legs=((8, 3), (-7, -3)), arms=(("fk", 26, 66), ("fk", 22, 30)), expr="brave"),
    "dv_sling_spin": _P(t=-4, h=-6, legs=((18, 6), (-18, -8)), arms=(("fk", 124, 140), ("fk", -46, -24)),
                        hands=("fist", "open"), expr="brave", look=(0.03, -0.04)),
    "dv_sling_release": _P(t=16, h=-6, legs=((40, 14), (-30, -52)), arms=(("fk", 100, 94), ("fk", -64, -42)),
                           hands=("fist", "open"), expr="brave", hem=0.66),
    "dv_carry_basket": _P(arms=(("ik", "body", 46, -40, 1), ("ik", "body", 22, -36, 1)), hands=("none", "none")),
    "dv_sit_harp": _P(t=-2, h=8, legs=(("ik", 66, 1), ("ik", 80, 1)),
                      arms=(("ik", "body", 46, -98, 1), ("ik", "body", 58, -58, 1)), hands=("none", "none"),
                      expr="peaceful", **_SEATED),
    "dv_pray": _P(h=-14, arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)),
                  hands=("none", "pray"), expr="peaceful", look=(0.02, -0.05)),
    "dv_armor_wobble": _P(t=-12, h=12, legs=((24, 6), (-26, -64)), arms=(("fk", 104, 118), ("fk", -98, -116)),
                          hands=("open", "open"), expr="worried"),
    # Goliath
    "gl_stand": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 18, 10), ("fk", 62, 92)), expr="sneer"),
    "gl_stride_a": _P(t=5, legs=((22, 8), (-18, -30)), arms=(("fk", -34, -24), ("fk", 62, 92)), expr="angry"),
    "gl_stride_b": _P(t=5, legs=((-18, -30), (22, 8)), arms=(("fk", 26, 40), ("fk", 62, 92)), expr="angry"),
    "gl_shout": _P(t=-6, h=-8, legs=((12, 4), (-10, -4)), arms=(("fk", 150, 168), ("fk", 70, 100)), expr="roar"),
    "gl_laugh": _P(t=-10, h=-22, legs=((8, 3), (-7, -3)), arms=(("fk", 26, 44), ("ik", "torso", 1.15, 0.30, 1)),
                   hands=("fist", "open"), expr="laugh"),
    "gl_mock": _P(t=10, h=10, legs=((8, 3), (-7, -3)), arms=(("fk", 26, 44), ("fk", 64, 42)), hands=("fist", "point"),
                  expr="sneer", look=(0.03, 0.08)),
    "gl_fall": _P(h=-12, legs=((3, 1), (-3, -1)), arms=(("fk", 150, 164), ("fk", 124, 150)), hands=("open", "open"),
                  expr="surprised"),
    "gl_lying": _P(h=-62, legs=((2, 0), (-2, 0)), arms=(("fk", 168, 176), ("fk", 160, 170)), hands=("open", "open"),
                   expr="dizzy"),
    # shield-bearer, soldiers
    "sb_stand": _P(arms=(("fk", 30, 60), ("ik", "body", 46, -86, 1)), hands=("none", "fist")),
    "sb_walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", 30, 60), ("ik", "body", 46, -86, 1)),
                    hands=("none", "fist")),
    "sb_walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 30, 60), ("ik", "body", 46, -86, 1)),
                    hands=("none", "fist")),
    "so_cower": _P(t=10, h=6, drop=34, legs=(("ik", 34, 1), ("ik", -28, 1)),
                   arms=(("ik", "headw", 0.95, 0.75, 1), ("ik", "headw", 0.55, 0.95, 1)), hands=("none", "fist"),
                   expr="scared"),
    "so_point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 14, 8), ("fk", 84, 88)), hands=("fist", "point"),
                   expr="surprised"),
    # Saul (king attire='saul', also valid for the other attires), Eliab, Jesse
    "king_sit_stool": _P(t=-2, lap=True, legs=((86, 4), (82, 2)),
                         arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), hem=0.97, flare=-8),
    "king_talk": _P(h=-2, arms=(("fk", 12, 6), ("fk", 30, 82)), hands=("fist", "open"), expr="kind"),
    "king_bless": _P(h=-6, arms=(("fk", 12, 6), ("fk", 78, 132)), hands=("fist", "palm"), expr="kind"),
    "el_scold": _P(t=4, h=4, legs=((10, 3), (-8, -3)), arms=(("ik", "torso", -1.15, 0.05, -1), ("fk", 70, 80)),
                   hands=("fist", "point"), expr="cross"),
    "el_hips": _P(h=-4, legs=((10, 3), (-8, -3)), arms=(("ik", "torso", -1.2, 0.04, -1), ("ik", "torso", 1.25, 0.04, 1)),
                  hands=("fist", "fist"), expr="cross"),
    "js_give": _P(t=6, h=4, legs=((10, 3), (-8, -3)), arms=(("fk", 62, 80), ("fk", 70, 84)), hands=("none", "none"),
                  expr="happy"),
})


def _check_pose(pose, allowed, who):
    if pose not in allowed:
        raise ValueError(f"{who}: unknown pose {pose!r}; choose from {sorted(allowed)}")


def _check_expr2(expr, who):
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{who}: unknown expr {expr!r}; choose from {ALL_EXPRESSIONS}")


# ---------------------------------------------------------------- David
DAVID_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "talk", "point_up", "kneel_pick", "hold_sling",
               "sling_spin", "sling_release", "carry_basket", "sit_harp", "cheer", "pray", "kneel_pray",
               "armor_wobble")
_DAVID_POSE = {"walk": "walk_a", "talk": "dv_talk", "point_up": "dv_point_up", "kneel_pick": "dv_kneel_pick",
               "hold_sling": "dv_hold_sling", "sling_spin": "dv_sling_spin", "sling_release": "dv_sling_release",
               "carry_basket": "dv_carry_basket", "sit_harp": "dv_sit_harp", "pray": "dv_pray",
               "armor_wobble": "dv_armor_wobble"}
_DAVID_NATURAL = {"stand": "happy", "walk_a": "happy", "walk_b": "happy", "run_a": "brave", "run_b": "brave",
                  "kneel_pray": "peaceful"}


def _david_design(armor=False, bag=True):
    t = DAVID_TUNIC
    D = dict(robe=t, sleeve=t, hem_col=shade(t, -0.25), skin=DAVID_SKIN, leg=DAVID_SKIN, hem=0.58, flare_k=0.9,
             sleeve_len=0.45, rope_belt=CORD, hair=DAVID_HAIR, hair_style="curly", hat=("custom", _david_head(False)),
             hat_h=0.30, neck_v=shade(t, 0.28), hem_w=9)
    if armor:
        D.update(robe=MAIL, sleeve=MAIL, hem_col=shade(MAIL, -0.22), hem=1.05, flare_k=2.3, sleeve_len=1.0,
                 cuff=shade(MAIL, -0.25), robe_floor=True, rope_belt=None, sash=LEATHER, sash_tail=False,
                 pattern=(None, _ring_motif(shade(MAIL, -0.3)), 12), hat=("custom", _david_head(True)), hat_h=1.2,
                 neck_v=None)
    return D


def david(x, y, scale=1.0, facing=1, pose="stand", expr=None, bag=True, staff=False, basket=False, armor=False,
          phase=0.0, stone=True, marks=True):
    """David, the shepherd boy of about 12 (see module doc, 'David film')."""
    _check_pose(pose, DAVID_POSES + ("walk",), "david")
    _check_expr2(expr, "david")
    key = _DAVID_POSE.get(pose, pose)
    ps = dict(POSES[key])
    if pose in _DAVID_NATURAL:
        ps["expr"] = _DAVID_NATURAL[pose]
    D = _david_design(armor, bag)
    behind, mid, front = None, None, None
    if staff and not armor and pose in ("stand", "walk", "walk_a", "walk_b"):
        ps = dict(POSES[{"stand": "dv_stand_staff", "walk": "dv_walk_a_staff", "walk_a": "dv_walk_a_staff",
                         "walk_b": "dv_walk_b_staff"}[pose]])
        ps["expr"] = "happy"
        front = _staff_near(D)
    elif basket and pose in ("stand", "walk", "walk_a", "walk_b"):
        ps = dict(POSES[{"stand": "dv_stand_basket", "walk": "dv_walk_a_basket", "walk_a": "dv_walk_a_basket",
                         "walk_b": "dv_walk_b_basket"}[pose]])
        ps["expr"] = "happy"
        front = _basket_hang(D)
    if pose == "hold_sling":
        if staff:
            ps = dict(POSES["dv_hold_sling_staff"])
            behind = _staff_far
        front = _sling_front(D, "hold", stone=stone)
    elif pose == "sling_spin":
        behind, front = _sling_spin_hooks(D, phase, stone)
    elif pose == "sling_release":
        front = _sling_front(D, "release")
    elif pose == "carry_basket":
        front = _basket_carry(D)
    elif pose == "sit_harp":
        front = _harp_front(D)
    if armor:
        mid = lambda st: _sword_hang(st, drag=True)          # noqa: E731
    elif bag:
        mid = _bag_mid
    D["behind"], D["mid"], D["front"] = behind, mid, front
    e = expr or ps["expr"]
    m = _metrics(_BOY, 1.0, 1.22) if armor else _BOY
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"david-{pose}")


# ---------------------------------------------------------------- Goliath
GOLIATH_POSES = ("stand", "stride_a", "stride_b", "shout", "laugh", "mock_point", "fall", "lying")
_GOLIATH_POSE = {"stand": "gl_stand", "stride_a": "gl_stride_a", "stride_b": "gl_stride_b", "stride": "gl_stride_a",
                 "shout": "gl_shout", "laugh": "gl_laugh", "mock_point": "gl_mock", "fall": "gl_fall",
                 "lying": "gl_lying"}
GOLIATH_SPEAR_LEN = 900


def _giant_spear(W, d, L=GOLIATH_SPEAR_LEN, grip=0.42, ground=None):
    """Goliath's spear: a shaft 'like a weaver's beam' through the hand W along direction d (butt -> tip)."""
    butt = _sub(W, _mul(d, grip * L))
    if ground is not None and butt[1] > ground - 24:
        k = (ground - 24 - W[1]) / (-d[1] * L) if d[1] else grip
        butt = _sub(W, _mul(d, k * L))
    tip = _add(butt, _mul(d, L))
    nv = (-d[1], d[0])
    s = _tube([butt, _sub(tip, _mul(d, 100))], 22, P["wood"], ow=OW)
    s += _line(f"M{_pt(_add(butt, _mul(nv, 4)))} L{_pt(_add(_sub(tip, _mul(d, 110)), _mul(nv, 4)))}", w=3,
               col=P["wood_light"], extra='opacity="0.7"')
    for t in (0.06, 0.5):          # bronze rings
        q = _add(butt, _mul(d, t * L))
        s += _tube([q, _add(q, _mul(d, 16))], 28, BRONZE, ow=3.2)
    base = _sub(tip, _mul(d, 104))
    head = [_add(base, _mul(nv, 9)), _add(_add(base, _mul(d, 40)), _mul(nv, 22)), tip,
            _sub(_add(base, _mul(d, 40)), _mul(nv, 22)), _sub(base, _mul(nv, 9))]
    s += f'<path d="{smooth_path(head, tension=0.6)}" fill="{IRON}" {_st(OW)}/>'
    s += _line(f"M{_pt(_add(base, _mul(d, 8)))} L{_pt(_sub(tip, _mul(d, 14)))}", w=2.4, col=shade(IRON, -0.35))
    s += _tube([_sub(base, _mul(d, 6)), _add(base, _mul(d, 8))], 26, BRONZE, ow=3.2)
    s += _tube([_sub(butt, _mul(d, 18)), butt], 14, IRON, ow=3.2)
    return s


def _goliath_items(D, pose, spear, sword):
    hr = _GIANT["hr"]

    def behind(st):
        if not spear or pose not in ("laugh", "mock_point", "shout"):
            return ""
        W = st["arms"][0][2]
        if pose == "shout":
            return _giant_spear(W, _nrm((0.12, -1.0)), grip=0.40)
        return _giant_spear(W, (0.0, -1.0), ground=st["ground"])

    armour = _corselet(BRONZE, BRONZE_DARK, 30, strips=7)

    def mid(st):
        return armour(st) + (_sword_hang(st, scale_k=1.0) if sword else "")

    def front(st):
        s = ""
        W = st["arms"][1][2]
        if spear and pose in ("stand", "stride_a", "stride_b", "stride"):
            s += _giant_spear(W, _nrm((0.07, -1.0)), ground=st["ground"]) + _fist(W, hr, D["skin"], 1)
        if pose == "shout":             # loud voice: arcs in front of the mouth
            mo = st["hw"](0.75, 0.62)
            for k in range(3):
                r = 26 + 26 * k
                s += _line(f"M{fmt(mo[0] + r * 0.55)},{fmt(mo[1] - r * 0.85)} Q{fmt(mo[0] + r * 1.15)},{fmt(mo[1])} "
                           f"{fmt(mo[0] + r * 0.55)},{fmt(mo[1] + r * 0.85)}", w=4.0, col=MARK, extra='opacity="0.75"')
        if pose == "laugh":             # 'ha ha' ticks round the head
            Hc, R = st["Hc"], st["m"]["R"]
            for (dx, dy, a) in ((1.45, -0.9, -30), (1.7, -0.25, 0), (-1.45, -1.0, 30)):
                c = (Hc[0] + dx * R, Hc[1] + dy * R)
                s += (f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate({a})">'
                      + _line("M-14,-8 Q0,-14 14,-8", w=4.0, col=MARK) + _line("M-10,6 Q0,0 10,6", w=4.0, col=MARK)
                      + "</g>")
        return s
    return behind, mid, front


def _goliath_design(pose, bump, spear, sword):
    D = dict(robe=GOLIATH_TUNIC, sleeve=GOLIATH_TUNIC, hem_col=shade(GOLIATH_TUNIC, -0.3), hem_w=20,
             skin=GOLIATH_SKIN, leg=GOLIATH_SKIN, hem=0.50, flare_k=0.8, sleeve_len=0.40, hair=GOLIATH_HAIR,
             hair_style="curly",
             beard=("full", GOLIATH_HAIR), hat=("custom", _goliath_head(bump)), hat_h=0.62, brow_w=7.5,
             neck_v=shade(BRONZE, 0.3), ears=False, legwear=_greaves(), sandal=SANDAL_DARK)
    D["behind"], D["mid"], D["front"] = _goliath_items(D, pose, spear, sword)
    return D


def _stars_svg(c, R):
    s = ""
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.4
        p = (c[0] + 1.05 * R * math.cos(a), c[1] + 0.32 * R * math.sin(a))
        r1, r0 = 0.20 * R, 0.08 * R
        pts = []
        for j in range(10):
            rr = r1 if j % 2 == 0 else r0
            aa = -math.pi / 2 + j * math.pi / 5
            pts.append((p[0] + rr * math.cos(aa), p[1] + rr * math.sin(aa)))
        s += f'<path d="{_d(pts)}" fill="{P["gold"]}" {_st(2.6)}/>'
    s += (f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(1.05 * R)}" ry="{fmt(0.32 * R)}" fill="none" '
          f'stroke="{MARK}" stroke-width="2.6" stroke-dasharray="10 9" opacity="0.6"/>')
    return s


def goliath(x, y, scale=1.0, facing=1, pose="stand", expr=None, progress=1.0, bump=False, spear=True, sword=True,
            marks=True):
    """Goliath of Gath, the giant champion: big and loud, cartoon-friendly (see module doc, 'David film')."""
    _check_pose(pose, GOLIATH_POSES + ("stride",), "goliath")
    _check_expr2(expr, "goliath")
    ps = dict(POSES[_GOLIATH_POSE[pose]])
    D = _goliath_design(pose, bump, spear, sword)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _GIANT, ps, e, _fsign(facing), marks)
    if pose in ("fall", "lying"):
        th = 90.0 if pose == "lying" else 90.0 * max(0.0, min(1.0, progress))
        px = 0.9 * _GIANT["fl"]
        a = math.radians(th)
        lift = max([0.0] + [(qx - px) * math.sin(a) + qy * math.cos(a) + r for qx, qy, r in _LAST["pts"]])
        extra = ""
        if pose == "lying" and bump:
            hx, hy = _LAST["head"]
            hx2 = px + (hx - px) * math.cos(a) - hy * math.sin(a)
            hy2 = (hx - px) * math.sin(a) + hy * math.cos(a) - lift
            extra = _stars_svg((hx2 + 0.2 * _GIANT["R"], hy2 - 1.45 * _GIANT["R"]), _GIANT["R"])
        inner = (f'<g transform="translate(0,{fmt(-lift)}) rotate({fmt(th)} {fmt(px)} 0)">{inner}</g>' + extra)
    return _wrap_out(inner, x, y, scale, facing, f"goliath-{pose}")


def goliath_head_point(x, y, scale=1.0, facing=1, pose="stand", progress=1.0):
    """Stage point of Goliath's forehead (where the stone hits) for goliath(x, y, scale, facing, pose, progress)."""
    goliath(0, 0, 1.0, 1, pose=pose, progress=progress, spear=False)
    hx, hy = _LAST["head"]
    R = _GIANT["R"]
    fx, fy = hx + 0.38 * R, hy - 0.43 * R
    if pose in ("fall", "lying"):
        th = 90.0 if pose == "lying" else 90.0 * max(0.0, min(1.0, progress))
        px = 0.9 * _GIANT["fl"]
        a = math.radians(th)
        lift = max([0.0] + [(qx - px) * math.sin(a) + qy * math.cos(a) + r for qx, qy, r in _LAST["pts"]])
        fx, fy = px + (fx - px) * math.cos(a) - fy * math.sin(a), (fx - px) * math.sin(a) + fy * math.cos(a) - lift
    return (x + fx * scale * _fsign(facing), y + fy * scale)


# ---------------------------------------------------------------- soldiers and the shield-bearer
SOLDIER_POSES = ("stand", "walk_a", "walk_b", "cower", "run_a", "run_b", "cheer", "point")
SOLDIER_SIDES = ("israel", "philistine")
_ISRAEL = [
    dict(tunic="#5b7fa6", trim="#e3c88f", skin="#e2a77e", hair="#3a2a22", beard=("short", "#3a2a22"), cap="#8b5a35"),
    dict(tunic="#8a6440", trim="#c9714a", skin="#b9805a", hair="#2f2420", beard=("stubble", "#2f2420"), cap="#6b4127"),
    dict(tunic="#46698a", trim="#efe2c4", skin="#d39a72", hair="#5a3a24", beard=None, cap="#a0683e"),
    dict(tunic="#a77d4f", trim="#5b7fa6", skin="#8d5a3b", hair="#241b17", beard=("full", "#241b17"), cap="#7a4a2a"),
]
_PHILISTINE = [
    dict(tunic="#b5523b", trim="#efe2c4", skin="#e0a67c", hair="#3a2a22", band="#3f6f9e", feather="#efe2c4"),
    dict(tunic="#3f7f86", trim="#e8c27a", skin="#c68a62", hair="#2a201b", band="#b5523b", feather="#e8c27a"),
    dict(tunic="#c99a42", trim="#7b4f6e", skin="#a46b47", hair="#241b17", band="#3f7f86", feather="#f0e2c0"),
    dict(tunic="#7b4f6e", trim="#e3c88f", skin="#eab48c", hair="#5a3a24", band="#c99a42", feather="#d9a464"),
]


def _soldier_design(side, variant):
    if side == "israel":
        v = _ISRAEL[variant % 4]
        return dict(robe=v["tunic"], sleeve=v["tunic"], hem_col=v["trim"], cuff=v["trim"], hem_w=9, skin=v["skin"],
                    leg=v["skin"], hem=0.58, flare_k=0.7, sleeve_len=0.5, rope_belt="#8b5a35", hair=v["hair"],
                    hair_style="short", hat=("custom", lambda R, c=v["cap"]: _leather_cap_svg(R, c)), hat_h=0.24,
                    beard=v["beard"], neck_v=v["trim"], sandal=SANDAL_DARK), "israel"
    v = _PHILISTINE[variant % 4]
    return dict(robe=v["tunic"], sleeve=v["tunic"], hem_col=v["trim"], hem_w=9, skin=v["skin"], leg=v["skin"],
                hem=0.46, flare_k=0.9, sleeve_len=0.4, sash=shade(v["trim"], -0.2), sash_tail=True, fringe=v["trim"],
                hair=v["hair"], hair_style="curly", ears=False,
                hat=("custom", lambda R, b=v["band"], f=v["feather"]: _feather_band_svg(R, b, f)), hat_h=0.80,
                beard=None, neck_v=v["trim"], sandal=SANDAL_DARK, shawl=shade(v["tunic"], -0.25)), "philistine"


def _shield_on_back(kind):
    def behind(st):
        m, tp = st["m"], st["tp"]
        c = tp(-0.95 * m["ww"], 0.60 * m["T"])
        r = 0.98 * m["R"]
        return f'<g transform="translate({fmt(c[0])},{fmt(c[1])})">{_prp()._round_shield(r, kind)}</g>'
    return behind


def _shield_up(D, kind):
    def front(st):
        Hc, R, hr = st["Hc"], st["m"]["R"], st["m"]["hr"]
        c = (Hc[0] + 1.02 * R, Hc[1] + 1.02 * R)
        W = st["arms"][1][2]
        return (f'<g transform="translate({fmt(c[0])},{fmt(c[1])})">{_prp()._round_shield(1.02 * R, kind)}</g>'
                + _fist(W, hr, D["skin"]))
    return front


def soldier(x, y, scale=1.0, facing=1, side="israel", variant=0, pose="stand", expr=None, spear=None, shake=0.0,
            marks=True):
    """An Israelite or Philistine soldier for crowds (see module doc, 'David film')."""
    if side not in SOLDIER_SIDES:
        raise ValueError(f"soldier: unknown side {side!r}; choose from {SOLDIER_SIDES}")
    _check_pose(pose, SOLDIER_POSES, "soldier")
    _check_expr2(expr, "soldier")
    D, kind = _soldier_design(side, variant)
    key = {"stand": "guard_stand", "walk_a": "guard_walk_a", "walk_b": "guard_walk_b", "cower": "so_cower",
           "point": "so_point"}.get(pose, pose)
    if spear is None:
        spear = pose in ("stand", "walk_a", "walk_b")
    if not spear and pose in ("stand", "walk_a", "walk_b"):
        key = pose
    ps = dict(POSES[key])
    if pose in ("run_a", "run_b"):
        ps["expr"] = "scared"
    D["behind"] = _shield_on_back(kind) if pose != "cower" else None
    if pose == "cower":
        f = _shield_up(D, kind)
        D["front"] = (lambda st: f(st) + _tremble_lines(st, shake)) if marks else f
    elif spear:
        D["front"] = _spear_front(D)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _ADULT, ps, e, _fsign(facing), marks)
    if pose == "cower" and shake:
        inner = f'<g transform="translate({fmt(3.5 * math.sin(2 * math.pi * shake))},0)">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"soldier-{side}{variant % 4}-{pose}")


SHIELD_BEARER_POSES = ("stand", "walk_a", "walk_b")


def _big_shield_front(D):
    def front(st):
        m = st["m"]
        top = -(m["T"] + m["neck"] - 0.25 * m["R"])
        bot = 0.62 * (m["th"] + m["sh"])
        c = (0.95 * m["ww"] + 30, (top + bot) / 2)
        s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])})">{_prp()._tall_shield((bot - top) / 2)}</g>'
        W = st["arms"][1][2]
        return s + _fist(W, m["hr"], D["skin"])
    return front


def shield_bearer(x, y, scale=1.0, facing=1, pose="walk_a", variant=0, expr=None, marks=True):
    """Goliath's shield-bearer: a Philistine carrying the champion's huge tall shield in front of him."""
    _check_pose(pose, SHIELD_BEARER_POSES, "shield_bearer")
    _check_expr2(expr, "shield_bearer")
    D, _ = _soldier_design("philistine", variant)
    D["front"] = _big_shield_front(D)
    ps = dict(POSES["sb_" + pose])
    e = expr or ps["expr"]
    inner, _ = _figure(D, _ADULT, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"shield_bearer-{pose}")


# ---------------------------------------------------------------- Saul (king attire='saul')


def _camp_stool_behind(st):
    pel, m, g = st["pel"], st["m"], st["ground"]
    seat_y = pel[1] + m["seat"] * 0.75 + 4
    K = st["legs"][1][1]
    xa, xb = pel[0] - m["ww"] - 18, min(K[0] - 8, pel[0] + m["ww"] + 34)
    return f'<g transform="translate({fmt((xa + xb) / 2)},{fmt(g)})">{_prp()._camp_stool(xb - xa, g - seat_y)}</g>'


def _saul_cape(st):
    """Purple cloak hanging from the shoulders down the back."""
    m, tp, g = st["m"], st["tp"], st["ground"]
    a = tp(-m["shw"] + 2, m["T"] - 4)
    b = tp(0.25 * m["shw"], m["T"] + 2)
    lap = st["mode"] == "seat" or st["legs"][0][1][1] < 0
    y_bot = (g - 0.25 * (m["th"] + m["sh"])) if not lap else g - 10
    back = (min(a[0], tp(-m["ww"], 0)[0]) - 38, y_bot)
    pts = [b, a, (a[0] - 18, a[1] + 0.4 * (y_bot - a[1])), (back[0], back[1] - 6), (back[0] + 30, back[1] + 4),
           (back[0] + 70, back[1] - 4), tp(0, 0)]
    col = P["royal"]
    s = f'<path d="{smooth_path(pts, tension=0.8)}" fill="{col}" {_st(OW)}/>'
    s += _line(f"M{_pt(_lerp(a, back, 0.25))} Q{fmt(back[0] + 8)},{fmt((a[1] + y_bot) / 2)} {fmt(back[0] + 26)},"
               f"{fmt(back[1] - 6)}", w=2.4, col=shade(col, -0.25))
    s += _line(f"M{_pt(_lerp(a, back, 0.1))} L{fmt(back[0] + 60)},{fmt(back[1] - 10)}", w=2.4, col=shade(col, 0.2),
               extra='opacity="0.7"')
    return s


def _saul_clasp(st):
    p = st["tp"](0.45 * st["m"]["shw"], st["m"]["T"] - 14)
    return f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="8" fill="{GOLD}" {_st(2.6)}/>' + \
        f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="3" fill="{P["royal_light"]}"/>'


def _saul_design(pose, stool):
    D = dict(robe=SAUL_TUNIC, sleeve=SAUL_TUNIC, hem_col=GOLD, hem_w=11, skin="#d9a27a", leg="#d9a27a",
             hem=0.66, flare_k=0.8, sleeve_len=0.55, hair=SAUL_HAIR, hair_style="curly",
             beard=("full", SAUL_HAIR), hat=("custom", lambda R: _bronze_helmet_svg(R, BRONZE, circlet=True,
                                                                                  plume=P["royal_light"])),
             hat_h=0.75, ears=False, legwear=_greaves(), sandal=SANDAL_DARK)
    beh = [_saul_cape]
    if pose == "sit" and stool:
        beh.insert(0, _camp_stool_behind)
    D["behind"] = _hooks(*beh)
    armour = _corselet(BRONZE, BRONZE_DARK, 17, strips=6)
    D["mid"] = lambda st: armour(st) + _sword_hang(st) + _saul_clasp(st)     # noqa: E731
    return D


KING_EXTRA_POSES = ("sit", "talk", "bless")      # added for Saul; they work in every attire
_KING_ALIAS.update({"sit": "king_sit_stool", "talk": "king_talk", "bless": "king_bless"})


def _king_david_film(x, y, scale, facing, pose, attire, expr, ps, throne, stool, marks):
    """king() for attire='saul' and for the poses sit / talk / bless (any attire)."""
    _check_expr2(expr, "king")
    if attire is None:
        attire = "royal"
    if attire not in KING_ATTIRES:
        raise ValueError(f"king: unknown attire {attire!r}; choose from {KING_ATTIRES}")
    if attire == "saul" and pose in ("sit_ashes", "remove_crown"):
        raise ValueError(f"king: pose {pose!r} is not available for attire='saul'")
    if attire == "saul":
        D = _saul_design(pose, stool)
        if pose in _KING_SEATED and throne:
            D["behind"] = _hooks(_throne, D["behind"])
        m = _SAUL_M
    else:
        D = _king_design(attire, pose, throne, True)
        if pose == "sit" and stool:
            D["behind"] = _camp_stool_behind
        m = _KING_M
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"king-{pose}")


# ---------------------------------------------------------------- Eliab and Jesse
ELIAB_POSES = ("stand", "walk_a", "walk_b", "talk", "scold", "hands_hips")
_ELIAB_POSE = {"talk": "explain", "scold": "el_scold", "hands_hips": "el_hips"}


def _eliab_design():
    t = "#3f6f6a"
    return dict(robe=t, sleeve=t, hem_col="#d9a03c", cuff="#d9a03c", hem_w=10, skin="#dca57c", leg="#dca57c",
                hem=0.60, flare_k=0.7, sleeve_len=0.5, rope_belt="#8b5a35", hair="#3a2618", hair_style="curly",
                hat=("custom", lambda R: _leather_cap_svg(R, "#7a4a2a")), hat_h=0.24, beard=("stubble", "#3a2618"),
                neck_v="#d9a03c", sandal=SANDAL_DARK, behind=_shield_on_back("israel"))


def eliab(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    """Eliab, David's eldest brother: a tall young Israelite soldier (see module doc, 'David film')."""
    _check_pose(pose, ELIAB_POSES, "eliab")
    _check_expr2(expr, "eliab")
    ps = dict(POSES[_ELIAB_POSE.get(pose, pose)])
    if pose == "talk":
        ps["expr"] = "neutral"
    e = expr or ps["expr"]
    inner, _ = _figure(_eliab_design(), _ELIAB_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"eliab-{pose}")


JESSE_POSES = ("stand", "walk_a", "walk_b", "talk", "give")


def _jesse_design(pose):
    robe, wrap = "#b0603e", "#e0b25a"
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.25), cuff=shade(robe, -0.25), skin="#dca07a",
             leg="#dca07a", hem=0.92, hair="#e4ddd0", hair_style="short", beard=("white", "#ece6da"), shawl=wrap,
             shawl_trim=shade(wrap, -0.25), hat=("wrap", "#efe2c4", shade("#efe2c4", -0.25)))
    if pose == "give":
        def front(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            k = 0.62
            cx, yy = (W0[0] + W1[0]) / 2, max(W0[1], W1[1]) + 58 * k
            return (f'<g transform="translate({fmt(cx)},{fmt(yy)}) scale({k})">{_prp()._bread_basket(handle=False)}</g>'
                    + _fist(W0, st["m"]["hr"], D["skin"], 0, 2) + _fist(W1, st["m"]["hr"], D["skin"], 0, 2))
        D["front"] = front
    else:
        D["front"] = _cane
    return D


def jesse(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    """Jesse of Bethlehem, David's old father: white beard, warm robe, walking stick (see module doc)."""
    _check_pose(pose, JESSE_POSES, "jesse")
    _check_expr2(expr, "jesse")
    ps = dict(POSES[{"talk": "explain", "give": "js_give"}.get(pose, pose)])
    if pose != "give":
        ps["t"] = ps["t"] + 8
        near = ("fk", 22, 30) if pose != "talk" else ("fk", 30, 70)
        ps["arms"] = (ps["arms"][0] if pose != "talk" else ("fk", 12, 6), near)
        ps["hands"] = ("fist", "fist")
        ps["expr"] = "happy" if pose == "talk" else "neutral"
    e = expr or ps["expr"]
    inner, _ = _figure(_jesse_design(pose), _JESSE_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"jesse-{pose}")


# ======================================================================= Noah film (Genesis 6-9)
# Noah, his wife, Shem, Ham, Japheth and their wives, noah_family(), and a modern child in a raincoat
# (module doc section "NOAH FILM").

EXPRS.update({
    "determined": dict(eyes="dot", brow=(0.08, -0.04, 0.02), mouth="firm"),
    "amazed":     dict(eyes="big", brow=(-0.05, -0.04, -0.15), mouth="awe"),
})
NOAH_EXPRESSIONS = ("determined", "amazed")

NOAH_ROBE = "#8c5b3e"
NOAH_TRIM = "#d6a447"
NOAH_CLOTH = "#e6e3c6"
NOAH_BAND = "#6f9068"
NOAH_SKIN = "#e8b08a"
NOAH_BEARD = "#eeeae2"
CHILD_COAT = "#f2c43c"
CHILD_BOOTS = "#d4523f"

NOAH_POSES = ("stand", "walk_a", "walk_b", "walk_c", "talk", "pray", "kneel_pray", "point_up", "scratch_head", "nod",
              "saw", "hammer", "carry", "carry_walk_a", "carry_walk_b", "open_window", "release_dove", "hold_leaf",
              "cheer", "wave")
FAMILY_POSES = NOAH_POSES
CARRY_ITEMS = ("sack", "hay", "basket", "grain", "veg", "jar")

_NH_POSES = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3)), expr="kind"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -40, -30), ("fk", 26, 42)), expr="happy"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 44), ("fk", -24, -14)), expr="happy"),
    "walk_c": _P(t=3, legs=((5, 1), (-8, -16)), arms=(("fk", 4, 8), ("fk", 2, 8)), expr="happy"),
    "talk": _P(h=-2, arms=(("fk", 12, 6), ("fk", 30, 82)), hands=("fist", "open"), expr="happy"),
    "pray": _P(h=-14, arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)), hands=("none", "pray"),
               expr="peaceful", look=(0.02, -0.05)),
    "kneel_pray": dict(POSES["kneel_pray"]),
    "point_up": _P(h=-16, legs=((5, 2), (-5, -2)), arms=(("fk", 132, 162), ("fk", -10, -4)), hands=("point", "fist"),
                   look=(0.03, -0.10), expr="determined"),
    "scratch_head": _P(h=10, legs=((6, 2), (-5, -2)), arms=(("ik", "torso", -1.15, 0.05, -1), ("ik", "head", -0.92, -0.52, -1)),
                       hands=("fist", "fist"), expr="puzzled"),
    "nod": _P(h=22, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="kind"),
    "open_window": _P(h=-18, arms=(("fk", 146, 164), ("fk", -150, -172)), hands=("palm", "palm"), expr="happy",
                      look=(0.02, -0.06)),
    "release_dove": _P(h=-12, arms=(("fk", 104, 122), ("fk", 112, 132)), hands=("open", "open"), expr="kind",
                       look=(0.03, -0.06)),
    "hold_leaf": _P(h=-12, legs=((6, 2), (-5, -2)), arms=(("fk", 150, 170), ("fk", 22, 48)), hands=("fist", "open"),
                    expr="amazed", look=(0.03, -0.08)),
    "cheer": dict(POSES["cheer"]),
}
_NH_NATURAL = {"kneel_pray": "peaceful", "cheer": "happy", "saw": "determined", "hammer": "determined",
               "carry": "happy", "carry_walk_a": "happy", "carry_walk_b": "happy", "wave": "happy"}


def _nh_saw_pose(phase):
    """Leaning over a plank on a sawhorse in front; the saw slides along its blade (phase 0 back, .5 forward)."""
    st_ = -22 * math.cos(2 * math.pi * phase)
    hx, hy = _NH_SAW_HAND[0] + _NH_SAW_DIR[0] * st_, _NH_SAW_HAND[1] + _NH_SAW_DIR[1] * st_
    return _P(t=24, h=10, drop=16, legs=(("ik", 30, 1), ("ik", -34, 1)), reach=1.1,
              arms=(("ik", "abs", 112, -122, 1), ("ik", "abs", hx, hy, 1)), hands=("open", "none"),
              look=(0.04, 0.08), expr="determined")


_NH_SAW_DIR = (0.866, 0.5)          # the saw blade slants 30 deg down toward facing
_NH_SAW_HAND = (134, -147)          # grip at mid-stroke (anchor coords, y up negative)
_NH_TRESTLE = (236, 0.72)           # sawhorse x and scale (its plank top ends up at y ~ -103)


_NH_SHOULDER = (14, -266)
NOAH_NAIL = (146, -250)              # hammer pose: where the nail head is (anchor coords at scale 1, facing 1)
_NH_HAMMER_ANG = (-168.0, -62.0)     # handle direction (screen degrees) raised .. at the strike


def _nh_hammer_ease(p):
    return _clamp01(p) ** 1.6


def _nh_hammer_arm(phase):
    p = _nh_hammer_ease(phase)
    a = math.radians(_NH_HAMMER_ANG[1])
    hd = (math.cos(a), math.sin(a))
    face = (-hd[1], hd[0])                        # the head's front end (local +y) points along this
    strike = (NOAH_NAIL[0] - 91 * hd[0] - 26 * face[0], NOAH_NAIL[1] - 91 * hd[1] - 26 * face[1])
    raised = (_NH_SHOULDER[0] - 24, _NH_SHOULDER[1] - 92)
    v0, v1 = _sub(raised, _NH_SHOULDER), _sub(strike, _NH_SHOULDER)
    a0, a1 = math.atan2(v0[1], v0[0]), math.atan2(v1[1], v1[0])
    r0, r1 = _len(v0), _len(v1)
    aa, rr = a0 + (a1 - a0) * p, r0 + (r1 - r0) * p
    return _NH_SHOULDER[0] + rr * math.cos(aa), _NH_SHOULDER[1] + rr * math.sin(aa)


def _clamp01(v):
    return max(0.0, min(1.0, float(v)))


def _nh_hammer_pose(phase):
    hx, hy = _nh_hammer_arm(phase)
    return _P(t=6, h=-2, legs=(("ik", 30, 1), ("ik", -26, 1)),
              arms=(("ik", "abs", NOAH_NAIL[0] + 18, NOAH_NAIL[1] + 8, 1), ("ik", "abs", hx, hy, -1)), hands=("fist", "none"),
              expr="determined", look=(0.04, 0.02))


def _nh_carry_pose(item, walk=None):
    legs = {None: ((3, 1), (-3, -1)), "a": ((24, 8), (-20, -34)), "b": ((-20, -34), (24, 8))}[walk]
    t = 4 if walk else 2
    if item in ("sack", "hay"):           # on the shoulder, steadied by the near hand behind the head
        swing = {None: ("fk", 12, 8), "a": ("fk", -30, -20), "b": ("fk", 26, 40)}[walk]
        return _P(t=t, legs=legs, arms=(swing, ("ik", "headw", -1.25, 0.25, -1)), hands=("fist", "fist"),
                  expr="happy")
    return _P(t=t, legs=legs, arms=(("ik", "body", 58, -58, 1), ("ik", "body", 30, -54, 1)), hands=("none", "none"),
              expr="happy")


def _nh_items(D, pose, phase, item, dove, sawhorse, marks):
    """Hooks (behind, mid, front) for held things."""
    PR = _prp()
    skin = D["skin"]
    behind = mid = front = None
    if pose in ("carry", "carry_walk_a", "carry_walk_b"):
        if item in ("sack", "hay"):
            def mid(st):
                c = (st["Hc"][0] - 1.15 * st["m"]["R"], st["Hc"][1] + 0.70 * st["m"]["R"])
                if item == "sack":
                    body = f'<g transform="translate({fmt(c[0] + 6)},{fmt(c[1] + 50)}) rotate(-62) scale(0.8)">{PR._sack(1.0, None, 3)}</g>'
                else:
                    body = f'<g transform="translate({fmt(c[0] - 4)},{fmt(c[1] + 36)}) rotate(-34) scale(1.05)">{PR._hay("bundle")}</g>'
                return body
        else:
            def front(st):
                W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
                cx = (W0[0] + W1[0]) / 2
                if item == "jar":
                    y = (W0[1] + W1[1]) / 2 + 6
                    s_ = f'<g transform="translate({fmt(cx)},{fmt(y)}) scale(0.62)">{PR._amphora()}</g>'
                else:
                    k = 0.62
                    kind = {"basket": "fruit", "grain": "grain", "veg": "veg"}[item]
                    y = max(W0[1], W1[1]) + 50 * k
                    s_ = f'<g transform="translate({fmt(cx)},{fmt(y)}) scale({k})">{PR._food_basket(kind)}</g>'
                return s_ + _fist(W0, hr, skin, 0, 2) + _fist(W1, hr, skin, 0, 2)
    elif pose == "saw":
        def front(st):
            G = st["ground"]
            W = st["arms"][1][2]
            hr = st["m"]["hr"]
            s_ = ""
            blade = f'<g transform="translate({fmt(W[0])},{fmt(W[1])}) rotate(30) scale(0.85)">{PR._saw_shape()}</g>'
            tx, tk = _NH_TRESTLE
            ptop = 131 * tk + 13 * tk
            cut = (_NH_SAW_HAND[0] + _NH_SAW_DIR[0] * (-_NH_SAW_HAND[1] - ptop) / _NH_SAW_DIR[1], G - ptop)
            if sawhorse:
                horse = f'<g transform="translate({tx},{fmt(G)}) scale({tk})">{PR._sawhorse(False)}</g>'
                s_ += horse + blade
                # the plank's front face covers the blade where it is in the cut
                s_ += (f'<g transform="translate({fmt(tx + 30 * tk)},{fmt(G - 131 * tk)}) scale({tk})">'
                       f'{PR._plank_shape(330, 26, PR.TIMBER_LIGHT, 3)}</g>')
                if marks:
                    for k, (dx, dy) in enumerate(((-8, 26), (6, 40), (-16, 52), (10, 64))):
                        s_ += f'<circle cx="{fmt(cut[0] + dx)}" cy="{fmt(cut[1] + dy)}" r="{2.6 + (k % 2)}" fill="#e8c890"/>'
            else:
                s_ += blade
            s_ += _fist(W, hr, skin, 2, 0)
            return s_
    elif pose == "hammer":
        def front(st):
            W = st["arms"][1][2]
            hr = st["m"]["hr"]
            ang = _NH_HAMMER_ANG[0] + (_NH_HAMMER_ANG[1] - _NH_HAMMER_ANG[0]) * _nh_hammer_ease(phase)
            s_ = f'<g transform="translate({fmt(W[0])},{fmt(W[1])}) rotate({fmt(ang)})">{_prp()._hammer_shape()}</g>'
            s_ += _fist(W, hr, skin)
            G = st["ground"]
            nail = (NOAH_NAIL[0], G + NOAH_NAIL[1])
            s_ += (f'<path d="M{fmt(nail[0])},{fmt(nail[1])} L{fmt(nail[0] + 26)},{fmt(nail[1])}" {_st(6.5)}/>'
                   f'<path d="M{fmt(nail[0])},{fmt(nail[1])} L{fmt(nail[0] + 26)},{fmt(nail[1])}" {_st(3, "#9a9e9c")}/>')
            if marks and phase >= 0.85:
                hp = nail
                for a in (-50, -10, 30, 70):
                    v = _rot((1, 0), a)
                    s_ += _line(f"M{_pt(_add(hp, _mul(v, 30)))} L{_pt(_add(hp, _mul(v, 46)))}", w=3.2, col=MARK)
            return s_
    elif pose == "release_dove" and dove:
        def front(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            c = ((W0[0] + W1[0]) / 2 + 18, min(W0[1], W1[1]) - 34)
            return f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate(-16) scale(0.62)">{PR._bird("dove", 0.9, "fly")}</g>'
    elif pose == "hold_leaf":
        def front(st):
            W, hr = st["arms"][0][2], st["m"]["hr"]
            return (f'<g transform="translate({fmt(W[0] + 2)},{fmt(W[1] + 4)}) rotate(-78) scale(0.62)">'
                    f'{PR._olive_sprig(3, False, 80)}</g>' + _fist(W, hr, skin))
    elif pose == "scratch_head" and marks:
        def front(st):
            Hc, R = st["Hc"], st["m"]["R"]
            x0, y0 = Hc[0] + 1.25 * R, Hc[1] - 1.45 * R
            return (_line(f"M{fmt(x0 - 9)},{fmt(y0 - 6)} Q{fmt(x0 - 6)},{fmt(y0 - 22)} {fmt(x0 + 8)},{fmt(y0 - 20)} "
                          f"Q{fmt(x0 + 20)},{fmt(y0 - 14)} {fmt(x0 + 10)},{fmt(y0 - 2)} Q{fmt(x0 + 1)},{fmt(y0 + 6)} {fmt(x0 + 1)},{fmt(y0 + 14)}",
                          w=4.2, col=MARK) + f'<circle cx="{fmt(x0 + 1)}" cy="{fmt(y0 + 26)}" r="3.4" fill="{MARK}"/>')
    elif pose == "wave" and marks:
        def front(st):
            W = st["arms"][0][2]
            s_ = ""
            for k in (0, 1):
                r = 26 + 14 * k
                s_ += _line(f"M{fmt(W[0] + r)},{fmt(W[1] - r * 0.6)} Q{fmt(W[0] + r * 1.15)},{fmt(W[1])} {fmt(W[0] + r)},{fmt(W[1] + r * 0.6)}",
                            w=2.8, col=MARK)
            return s_
    return behind, mid, front


def _nh_pose(pose, phase=0.0, item="sack"):
    if pose == "saw":
        return _nh_saw_pose(phase)
    if pose == "hammer":
        return _nh_hammer_pose(phase)
    if pose == "carry":
        return _nh_carry_pose(item)
    if pose in ("carry_walk_a", "carry_walk_b"):
        return _nh_carry_pose(item, pose[-1])
    if pose == "wave":
        f = 168 + 18 * math.sin(2 * math.pi * phase)
        return _P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 146, f), ("fk", -8, -3)), hands=("open", "fist"),
                  expr="happy")
    return dict(_NH_POSES[pose])


# ---------------------------------------------------------------- designs
def _aged(R, skin, hair=None):
    """Grandparent touches in the head frame: smile wrinkles at the eye corners, a soft forehead line and, with
    hair, a grey tuft at the temple joining the beard."""
    lc = shade(skin, -0.32)
    s = ""
    if hair:
        s += f'<path d="{smooth_path([(-0.78 * R, -0.30 * R), (-0.56 * R, -0.24 * R), (-0.50 * R, 0.05 * R), (-0.62 * R, 0.30 * R), (-0.86 * R, 0.22 * R)])}" fill="{hair}" {_st(2.6)}/>'
    for dy in (-0.04, 0.07):
        s += _line(f"M{fmt(-0.30 * R)},{fmt((0.02 + dy) * R)} l{fmt(-0.12 * R)},{fmt(dy * 0.8 * R)}", w=2.0, col=lc)
    s += _line(f"M{fmt(0.62 * R)},{fmt(0.04 * R)} l{fmt(0.12 * R)},{fmt(-0.03 * R)}", w=2.0, col=lc)
    s += _line(f"M{fmt(-0.05 * R)},{fmt(-0.40 * R)} Q{fmt(0.22 * R)},{fmt(-0.45 * R)} {fmt(0.50 * R)},{fmt(-0.40 * R)}",
               w=2.0, col=lc, extra='opacity="0.8"')
    return s


def _noah_hat(R):
    return _aged(R, NOAH_SKIN, "#e7e1d8") + _cloth_cap(R, NOAH_CLOTH, edge=NOAH_BAND)


def _wife_hat(R):
    F = _FAMILY["wife"]
    return _aged(R, F["skin"]) + _cloth_cap(R, F["veil"], edge=F["veil_edge"])


_FAMILY = {
    "noah": dict(robe=NOAH_ROBE, trim=NOAH_TRIM, skin=NOAH_SKIN, hair="#e4ddd0", beard=("long", NOAH_BEARD),
                 hat=("custom", _noah_hat), tail=(NOAH_CLOTH, None), belt="#d9b77a",
                 m=_metrics(_ADULT, 1.0, 1.1), brow_w=5.0, brow_col="#9a9088"),
    "wife": dict(robe="#98587a", trim="#e8c8a0", skin="#e6ad88", hair="#d9d2c8", veil="#efe2cc", veil_edge="#c98a9a",
                 sash="#e0b25a", m=_metrics(_ADULT, 0.94, 0.96)),
    "shem": dict(robe="#4d6e9c", trim="#e9dcc0", skin="#dfa47c", hair="#4a2f1f", hair_style="curly",
                 beard=("full", "#4a2f1f"), belt="#e9dcc0", m=_metrics(_ADULT, 1.04, 1.04)),
    "ham": dict(robe="#b5553a", trim="#e0b25a", skin="#9a6342", hair="#2a201b", hair_style="curly",
                beard=("short", "#2a201b"), hat=("headband", "#e0b25a"), belt="#e0b25a", m=_metrics(_ADULT, 1.05, 1.1)),
    "japheth": dict(robe="#6e9a4c", trim="#ead9a8", skin="#f0c49e", hair="#b0602e", hair_style="curly",
                    beard=("stubble", "#b0602e"), belt="#c9a46a", m=_metrics(_ADULT, 1.02, 0.98)),
    "dil0": dict(robe="#e0a33c", trim="#8a5a3c", skin="#e2a77e", hair="#4a2f1f", veil="#3f8f8a", veil_edge="#2f6f6a",
                 sash="#3f8f8a", m=_metrics(_ADULT, 0.95, 0.92)),
    "dil1": dict(robe="#a88cc8", trim="#f0e3cf", skin="#b07850", hair="#2a201b", veil="#e07a5f", veil_edge="#b85a44",
                 sash="#e07a5f", m=_metrics(_ADULT, 0.96, 0.95)),
    "dil2": dict(robe="#e39aa6", trim="#f6ecd8", skin="#f0c09a", hair="#8a4a2a", veil="#7fb6d6", veil_edge="#5a90b4",
                 sash="#7fb6d6", m=_metrics(_ADULT, 0.93, 0.9)),
}


def _family_design(who):
    F = _FAMILY[who]
    robe = F["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=F["trim"], cuff=F["trim"], skin=F["skin"], leg=F["skin"], hem=0.92,
             hem_w=11, hair=F["hair"], hair_style=F.get("hair_style", "short"))
    if "veil" in F:
        D.update(hat=("veil", F["veil"], F["veil_edge"]), veil=F["veil"], ears=False, sash=F["sash"], sash_tail=True,
                 hem_col=shade(robe, -0.2), cuff=shade(robe, -0.2))
    else:
        D.update(rope_belt=F["belt"], beard=F["beard"], neck_v=F["trim"])
        if F.get("hat"):
            D["hat"] = F["hat"]
        if F.get("tail"):
            D.update(tail=F["tail"], ears=False)
    if F.get("brow_w"):
        D["brow_w"] = F["brow_w"]
    if F.get("brow_col"):
        D["brow_col"] = F["brow_col"]
    if who == "wife":
        D["hat"] = ("custom", _wife_hat)
    return D


def _family_figure(who, x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, label):
    if pose not in NOAH_POSES:
        raise ValueError(f"{label}: unknown pose {pose!r}; choose from {NOAH_POSES}")
    if item not in CARRY_ITEMS:
        raise ValueError(f"{label}: unknown item {item!r}; choose from {CARRY_ITEMS}")
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{label}: unknown expr {expr!r}; choose from {ALL_EXPRESSIONS + NOAH_EXPRESSIONS}")
    ps = _nh_pose(pose, phase, item)
    if pose in _NH_NATURAL:
        ps["expr"] = _NH_NATURAL[pose]
    D = _family_design(who)
    D["behind"], D["mid"], D["front"] = _nh_items(D, pose, phase, item, dove, sawhorse, marks)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _FAMILY[who]["m"], ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"{label}-{pose}")


def noah(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, item="sack", dove=False, sawhorse=True,
         marks=True):
    """Noah: a kind, sturdy grandfather with a long white beard (see module doc, 'NOAH FILM')."""
    return _family_figure("noah", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, "noah")


def noah_wife(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, item="basket", dove=False, sawhorse=True,
              marks=True):
    """Noah's wife (see module doc, 'NOAH FILM')."""
    return _family_figure("wife", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, "noah_wife")


def shem(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, item="sack", dove=False, sawhorse=True,
         marks=True):
    """Shem, Noah's eldest son (see module doc, 'NOAH FILM')."""
    return _family_figure("shem", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, "shem")


def ham(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, item="sack", dove=False, sawhorse=True,
        marks=True):
    """Ham, Noah's second son (see module doc, 'NOAH FILM')."""
    return _family_figure("ham", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, "ham")


def japheth(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, item="sack", dove=False, sawhorse=True,
            marks=True):
    """Japheth, Noah's youngest son (see module doc, 'NOAH FILM')."""
    return _family_figure("japheth", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks, "japheth")


def daughter_in_law(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, phase=0.0, item="basket",
                    dove=False, sawhorse=True, marks=True):
    """The sons' wives: variant 0 Shem's (teal veil), 1 Ham's (coral veil), 2 Japheth's (sky-blue veil)."""
    return _family_figure(f"dil{variant % 3}", x, y, scale, facing, pose, expr, phase, item, dove, sawhorse, marks,
                          f"daughter_in_law{variant % 3}")


FAMILY = ("noah", "noah_wife", "shem", "ham", "japheth", "daughter_in_law0", "daughter_in_law1", "daughter_in_law2")


def family_member(name, x, y, scale=1.0, facing=1, **kw):
    """Any of the eight by name (FAMILY): e.g. family_member('ham', ...) or 'daughter_in_law1'."""
    if name.startswith("daughter_in_law"):
        return daughter_in_law(x, y, scale, facing, variant=int(name[-1]), **kw)
    fn = {"noah": noah, "noah_wife": noah_wife, "shem": shem, "ham": ham, "japheth": japheth}.get(name)
    if fn is None:
        raise ValueError(f"family_member: unknown name {name!r}; choose from {FAMILY}")
    return fn(x, y, scale, facing, **kw)


# (name, dx, dy, facing) of the group portrait at scale 1: back row (sons) first, then the front row
_GROUP = [("daughter_in_law1", -340, -36, 1), ("shem", -170, -36, 1), ("ham", 0, -40, 1), ("japheth", 170, -36, -1),
          ("daughter_in_law0", -255, 0, 1), ("noah_wife", -85, 0, 1), ("noah", 85, 4, -1),
          ("daughter_in_law2", 255, 0, -1)]
_LINE = ["noah", "noah_wife", "shem", "daughter_in_law0", "ham", "daughter_in_law1", "japheth", "daughter_in_law2"]
FAMILY_GROUP_POSES = ("stand", "cheer", "pray", "talk", "wave", "nod", "kneel_pray", "walk_a", "walk_b",
                      "carry_walk_a", "carry_walk_b")


def noah_family(x, y, scale=1.0, facing=1, pose="stand", expr=None, gap=150, items=None, marks=True):
    """All eight together (see module doc): a group portrait, or a walking line for the walk poses."""
    if pose not in FAMILY_GROUP_POSES:
        raise ValueError(f"noah_family: unknown pose {pose!r}; choose from {FAMILY_GROUP_POSES}")
    sx = 1 if facing >= 0 else -1
    out = ""
    if pose.startswith("walk") or pose.startswith("carry_walk"):
        other = {"walk_a": "walk_b", "walk_b": "walk_a", "carry_walk_a": "carry_walk_b",
                 "carry_walk_b": "carry_walk_a"}[pose]
        default_items = ["sack", "basket", "sack", "grain", "hay", "veg", "sack", "jar"]
        for i in reversed(range(8)):             # Noah leads; the last in line is drawn first
            name = _LINE[i]
            p_ = pose if i % 2 == 0 else other
            kw = dict(pose=p_, expr=expr, marks=marks)
            if pose.startswith("carry"):
                kw["item"] = (items or default_items)[i % len(items or default_items)]
            out += family_member(name, x - sx * i * gap * scale, y, scale, facing, **kw)
        return f'<g data-who="noah_family-{pose}">{out}</g>'
    for name, dx, dy, f in _GROUP:
        f_ = f * sx
        out += family_member(name, x + sx * dx * scale, y + dy * scale, scale * (0.97 if dy < 0 else 1.0), f_,
                             pose=pose, expr=expr, marks=marks)
    return f'<g data-who="noah_family-{pose}">{out}</g>'


# ---------------------------------------------------------------- the child (opening and ending scenes)
CHILD_POSES = ("stand", "walk_a", "walk_b", "peek_window", "splash", "jump", "point_up", "wave", "smile_up", "cheer")
_CH_POSES = {
    "stand": _P(arms=(("fk", 12, 8), ("fk", -10, -4)), expr="happy"),
    "walk_a": dict(POSES["walk_a"], expr="happy"),
    "walk_b": dict(POSES["walk_b"], expr="happy"),
    "peek_window": _P(t=6, h=-8, arms=(("ik", "abs", 54, -142, 1), ("ik", "abs", 42, -138, 1)), hands=("open", "open"),
                      expr="amazed", look=(0.05, -0.05)),
    "splash": _P(drop=18, legs=(("ik", 26, 1), ("ik", -24, 1)), arms=(("fk", 118, 138), ("fk", -114, -136)),
                 hands=("open", "open"), expr="laugh"),
    "jump": _P(h=-6, legs=((58, -10), (20, -70)), arms=(("fk", 140, 160), ("fk", -136, -160)), hands=("open", "open"),
               expr="laugh"),
    "point_up": _P(h=-18, legs=((5, 2), (-5, -2)), arms=(("fk", 136, 164), ("fk", -10, -4)), hands=("point", "fist"),
                   look=(0.03, -0.10), expr="amazed"),
    "smile_up": _P(h=-22, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)), hands=("none", "pray"),
                   look=(0.03, -0.10), expr="happy"),
    "cheer": dict(POSES["cheer"], expr="laugh"),
}
CHILD_JUMP = 46          # pose='jump': the soles are this many px (x scale) above the anchor's ground line


def _hood(R, col):
    s = _cloth_cap(R, col, edge=shade(col, -0.18))
    s += _line(f"M{fmt(-0.20 * R)},{fmt(-1.02 * R)} Q{fmt(-0.70 * R)},{fmt(-0.62 * R)} {fmt(-0.92 * R)},{fmt(0.10 * R)}",
               w=2.2, col=shade(col, -0.25))
    return s


def _child_design(ps_legs, hood, boots, coat):
    c = coat
    D = dict(robe=c, sleeve=c, hem_col=shade(c, -0.12), cuff=shade(c, -0.15), skin="#f2c29c", leg="#f2c29c", hem=0.62,
             flare_k=1.15, hem_w=8, hair="#5a3a24", hair_style="short", sandal=CHILD_BOOTS, neck_v=shade(c, -0.15))
    if hood:
        D.update(hat=("custom", lambda R: _hood(R, c)), hat_h=0.16, ears=False)

    def buttons(st):
        tp, m = st["tp"], st["m"]
        s_ = ""
        for k in (0.82, 0.52, 0.22, -0.12):
            p = tp(0.42 * m["ww"], k * m["T"])
            s_ += f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="3.6" fill="{shade(c, -0.35)}"/>'
        if not hood:                     # the hood hanging down the back
            q = tp(-0.80 * m["shw"], m["T"] - 6)
            s_ += _ell(q[0] - 2, q[1] + 4, 11, 12, shade(c, -0.06), sw=3)
        return s_
    D["mid"] = buttons
    if boots:
        def legwear(st, i):
            H, K, A, a1, a2 = st["legs"][i]
            fl, lw = st["m"]["fl"], st["m"]["lw"]
            col = CHILD_BOOTS if i == 1 else shade(CHILD_BOOTS, -0.15)
            ds = _nrm(_sub(A, K))
            fa = _ang(_rot(ds, -90))
            if ps_legs[i][0] == "ik":
                fa = max(-90.0, min(0.0, fa))
            top = _sub(A, _mul(ds, 0.55 * _len(_sub(A, K))))
            s_ = _tube([top, A], lw + 8, col, ow=3.2)

            def q(x, y_):
                v = _rot((x * fl, y_ * fl), fa)
                return (A[0] + v[0], A[1] + v[1])
            pts = [q(-0.46, -0.30), q(-0.50, 0.40), q(1.10, 0.40), q(1.12, 0.06), q(0.70, -0.18), q(0.10, -0.40)]
            s_ += f'<path d="{smooth_path(pts, tension=0.6)}" fill="{col}" {_st(3.2)}/>'
            s_ += _line(f"M{_pt(q(-0.48, 0.30))} L{_pt(q(1.10, 0.30))}", w=3.0, col=shade(col, -0.35))
            s_ += _line(f"M{_pt(_add(top, (-(lw + 6) / 2, 3)))} L{_pt(_add(top, ((lw + 6) / 2, 3)))}", w=2.2,
                        col=shade(col, 0.35))
            return s_
        D["legwear"] = legwear
    return D


def child(x, y, scale=1.0, facing=1, pose="stand", expr=None, hood=False, boots=True, coat=None, phase=0.0,
          marks=True, sibling=None, toy=None, outfit=None, pillow=True, item=None):
    """A little modern child in a raincoat and rubber boots (opening / ending, see module doc); Joseph film:
    sibling='big' / 'little' (play clothes), the poses tug / sulk / sorry / hug / share and toy='horse' / 'ball';
    Storm film: outfit='pyjamas' (the girl at home at night) and the poses of STORM_CHILD_POSES; Nativity film:
    outfit='jumper' (the boy at the Christmas tree), the poses of NATIVITY_CHILD_POSES and item=..."""
    if outfit == "jumper" or pose in NATIVITY_CHILD_POSES:
        return _child_nativity(x, y, scale, facing, pose, expr, phase, marks, outfit, pillow, sibling, hood, boots,
                               coat, toy, item)
    if outfit is not None or pose in STORM_CHILD_POSES:
        return _child_storm(x, y, scale, facing, pose, expr, phase, marks, outfit, pillow, sibling, hood, boots, coat)
    if sibling is not None or toy is not None or pose in SIBLING_POSES:
        return _child_joseph(x, y, scale, facing, pose, expr, hood, boots, coat, phase, marks, sibling, toy)
    if pose not in CHILD_POSES:
        raise ValueError(f"child: unknown pose {pose!r}; choose from {CHILD_POSES}")
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"child: unknown expr {expr!r}; choose from {ALL_EXPRESSIONS + NOAH_EXPRESSIONS}")
    if pose == "wave":
        f = 166 + 18 * math.sin(2 * math.pi * phase)
        ps = _P(h=-4, arms=(("fk", 146, f), ("fk", -10, -4)), hands=("open", "fist"), expr="happy")
    else:
        ps = dict(_CH_POSES[pose])
    D = _child_design(ps["legs"], hood, boots, coat or CHILD_COAT)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _CHILD, ps, e, _fsign(facing), marks)
    if pose == "jump":
        inner = f'<g transform="translate(0,{-CHILD_JUMP})">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"child-{pose}")


# ======================================================================= Joseph film (Genesis 37-50)
# Joseph (teen shepherd with the coat of many colours, slave, prisoner, ruler of Egypt), Jacob, the brothers and
# Benjamin, Pharaoh, Egyptians, the Ishmaelite traders, hug_pair(); and the modern siblings via child(sibling=...).
# Module doc section "JOSEPH FILM".

EXPRS.update({
    "proud":   dict(eyes="arc", brow=(-0.04, -0.03, -0.10), mouth="grin", look=(0.02, -0.04)),
    "crying":  dict(eyes="squeeze", brow=(-0.13, 0.06, 0.0), mouth="cry", tears=2),
    "tearful": dict(eyes="arc", brow=(-0.10, 0.05, -0.02), mouth="grin", tears=1, blush=True),
    "jealous": dict(eyes="narrow", brow=(0.10, -0.05, 0.04), mouth="pout", look=(0.06, 0.0)),
    "ashamed": dict(eyes="down", brow=(-0.12, 0.06, 0.04), mouth="wobble", blush=True, look=(0.0, 0.06)),
})
JOSEPH_EXPRESSIONS = ("proud", "crying", "tearful", "jealous", "ashamed")

JOSEPH_SKIN = "#e9b38c"
JOSEPH_HAIR = "#3b2619"
COAT_BANDS = ("#d9534a", "#f2c84b", "#4f86c6", "#6fae55", "#8e64b0", "#ef9440")   # 红 黄 蓝 绿 紫 橙
COAT_BASE = "#f1e6cc"
TUNIC = "#e6d6b2"
LINEN = "#f6f0e2"
EGYPT_SKIN = ("#c98f68", "#b07a52", "#d9a37a", "#9a6342")
EGYPT_HAIR = "#2a2320"
LAPIS = "#3f6fa8"
CARNELIAN = "#c9533f"
JACOB_ROBE = "#86424c"
PHARAOH_SKIN = "#c98f68"

_JOSEPH_TEEN_M = _metrics(_ADULT, 0.96, 0.9)
_JOSEPH_M = _metrics(_ADULT, 1.01, 0.97)
_JACOB_M = _metrics(_ADULT, 0.97, 1.02)
_PHARAOH_M = _metrics(_ADULT, 1.05, 1.06)


def _band_alpha(k, progress, n=len(COAT_BANDS)):
    """Coat progress 0..1 -> visibility of colour k (colour k fades in over progress k/n .. (k+1)/n)."""
    return _clamp01(progress * n - k)


# ---------------------------------------------------------------- heads (head frame, fn(R))
def _joseph_curls(R, col=JOSEPH_HAIR):
    """Joseph's short dark curls: a ring of small curls over the top and back, two curls on the forehead."""
    circ = []
    for i, a in enumerate(range(-40, -172, -22)):
        x, y = _polar(R, a, 0.98)
        circ.append((x, y, (0.23 if i % 2 else 0.20) * R))
    circ += [(0.52 * R, -0.70 * R, 0.15 * R), (0.24 * R, -0.82 * R, 0.17 * R), (-0.10 * R, -0.86 * R, 0.18 * R),
             (-0.96 * R, -0.30 * R, 0.17 * R)]
    s = _union_circles(circ, col)
    lite = shade(col, 0.28)
    for x, y, r in circ:
        s += _line(f"M{fmt(x - 0.45 * r)},{fmt(y + 0.15 * r)} Q{fmt(x - 0.15 * r)},{fmt(y - 0.55 * r)} {fmt(x + 0.40 * r)},"
                   f"{fmt(y - 0.20 * r)}", w=1.8, col=lite)
    return s


def _eyeliner(R, col=INK):
    """Egyptian kohl: a short wing at the outer corner of each eye."""
    return (_line(f"M{fmt(-0.22 * R)},{fmt(0.0)} l{fmt(-0.10 * R)},{fmt(-0.04 * R)}", w=2.2, col=col) +
            _line(f"M{fmt(0.53 * R)},{fmt(0.0)} l{fmt(0.10 * R)},{fmt(-0.05 * R)}", w=2.2, col=col))


def _nemes(R, base, stripe=None, band=GOLD, cobra=False, lappet=True, stripes=7):
    """Egyptian royal / court headcloth: smooth cap over the head with a band at the forehead, side panels
    flaring down behind the cheek to the shoulders, a lappet hanging in front of the shoulder (lappet=False:
    a khat gathered into a bag at the back of the neck). stripe: colour of horizontal stripes (None: plain)."""
    main = [(0.97 * R, -0.38 * R), (0.92 * R, -0.88 * R), (0.42 * R, -1.20 * R), (-0.35 * R, -1.18 * R),
            (-0.98 * R, -0.80 * R), (-1.25 * R, -0.15 * R)]
    if lappet:
        main += [(-1.44 * R, 0.70 * R), (-1.50 * R, 1.28 * R), (-1.04 * R, 1.34 * R), (-0.80 * R, 0.62 * R)]
    else:
        main += [(-1.30 * R, 0.30 * R), (-1.20 * R, 0.62 * R), (-0.84 * R, 0.55 * R), (-0.74 * R, 0.30 * R)]
    main += [(-0.72 * R, 0.02 * R), (-0.60 * R, -0.34 * R), (0.30 * R, -0.50 * R)]
    lap = [(-0.84 * R, 0.30 * R), (-0.60 * R, 0.38 * R), (-0.48 * R, 1.86 * R), (-0.80 * R, 1.92 * R),
           (-0.98 * R, 0.95 * R)]
    s = ""
    shapes = [smooth_path(main, tension=0.85)] + ([smooth_path(lap, tension=0.7)] if lappet else [])
    for d in shapes:
        s += f'<path d="{d}" fill="{base}" {_st(3.4)}/>'
        if stripe:
            cid = _clip_id("nemes", R, base, stripe, d[:40])
            lines = ""
            for k in range(stripes * 2 + 4):
                yy = (-1.25 + 0.24 * k) * R
                lines += (f'<path d="M{fmt(-1.6 * R)},{fmt(yy + 0.10 * R)} Q{fmt(-0.3 * R)},{fmt(yy - 0.06 * R)} '
                          f'{fmt(1.1 * R)},{fmt(yy - 0.02 * R)}" fill="none" stroke="{stripe}" '
                          f'stroke-width="{fmt(0.10 * R)}"/>')
            s += f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{lines}</g>'
            s += f'<path d="{d}" fill="none" {_st(3.4)}/>'
    if not lappet:            # the gathered bag at the back of the neck
        s += _ell(-1.18 * R, 0.52 * R, 0.24 * R, 0.17 * R, shade(base, -0.08), sw=2.8)
    s += _line(f"M{fmt(-0.25 * R)},{fmt(-0.95 * R)} Q{fmt(-0.80 * R)},{fmt(-0.55 * R)} {fmt(-0.95 * R)},{fmt(0.30 * R)}",
               w=2.0, col=shade(base, -0.22))
    if band:
        s += _tube(_spline_pts([(0.99 * R, -0.42 * R), (0.45 * R, -0.58 * R), (-0.25 * R, -0.55 * R),
                                (-0.66 * R, -0.32 * R)]), 0.13 * R, band, ow=2.4)
    if cobra:                 # the little rearing cobra (uraeus) at the brow, friendly
        cx, cy = 0.80 * R, -0.62 * R
        s += (f'<path d="M{fmt(cx - 0.06 * R)},{fmt(cy + 0.08 * R)} Q{fmt(cx - 0.14 * R)},{fmt(cy - 0.20 * R)} '
              f'{fmt(cx + 0.02 * R)},{fmt(cy - 0.36 * R)} Q{fmt(cx + 0.18 * R)},{fmt(cy - 0.40 * R)} {fmt(cx + 0.16 * R)},'
              f'{fmt(cy - 0.26 * R)} Q{fmt(cx + 0.08 * R)},{fmt(cy - 0.10 * R)} {fmt(cx + 0.08 * R)},{fmt(cy + 0.08 * R)} Z" '
              f'fill="{GOLD}" {_st(2.4)}/>')
        s += _ell(cx + 0.03 * R, cy - 0.20 * R, 0.06 * R, 0.09 * R, LAPIS)
        s += f'<circle cx="{fmt(cx + 0.11 * R)}" cy="{fmt(cy - 0.32 * R)}" r="{fmt(0.025 * R)}" fill="{INK}"/>'
    return s


def _vizier_head(R):
    """Joseph as ruler: a white court headcloth with thin gold stripes and band; dark curls at the temple."""
    s = _nemes(R, LINEN, "#e6c97e", GOLD, lappet=True)
    circ = [(-0.62 * R, -0.24 * R, 0.13 * R), (-0.64 * R, 0.02 * R, 0.12 * R)]
    s += _union_circles(circ, JOSEPH_HAIR, 2.4)
    for x, y, r in circ:
        s += _line(f"M{fmt(x - 0.4 * r)},{fmt(y + 0.1 * r)} Q{fmt(x - 0.1 * r)},{fmt(y - 0.5 * r)} {fmt(x + 0.4 * r)},{fmt(y - 0.2 * r)}",
                   w=1.6, col=shade(JOSEPH_HAIR, 0.3))
    return s


def _false_beard(R, col="#3a2a22"):
    """Pharaoh's narrow plaited ceremonial beard under the chin (the mouth stays free)."""
    x0, x1, y0, y1 = 0.08 * R, 0.30 * R, 0.86 * R, 1.52 * R
    s = (f'<path d="M{fmt(x0)},{fmt(y0)} L{fmt(x1)},{fmt(y0)} L{fmt(x1 + 0.05 * R)},{fmt(y1)} '
         f'Q{fmt((x0 + x1) / 2 + 0.03 * R)},{fmt(y1 + 0.10 * R)} {fmt(x0 + 0.04 * R)},{fmt(y1)} Z" fill="{col}" {_st(2.6)}/>')
    for k in range(1, 6):
        yy = y0 + (y1 - y0) * k / 6
        s += _line(f"M{fmt(x0 + 0.02 * R)},{fmt(yy)} q{fmt(0.11 * R)},{fmt(0.05 * R)} {fmt(0.24 * R)},0", w=1.6,
                   col=shade(col, 0.35))
    s += _line(f"M{fmt(x0)},{fmt(y0 + 0.02 * R)} Q{fmt(-0.40 * R)},{fmt(0.86 * R)} {fmt(-0.62 * R)},{fmt(0.42 * R)}", w=1.8,
               col=shade(col, 0.2), extra='opacity="0.7"')
    return s


def _bob_wig(R, col=EGYPT_HAIR, length=0.55, band=None):
    """Egyptian black bob: straight fringe, hair falling to the jaw (length in R; ~1.4 for women)."""
    pts = [(0.98 * R, -0.40 * R), (0.92 * R, -0.90 * R), (0.40 * R, -1.22 * R), (-0.40 * R, -1.20 * R),
           (-1.02 * R, -0.82 * R), (-1.24 * R, -0.10 * R), (-1.22 * R, length * R), (-0.95 * R, (length + 0.05) * R),
           (-0.52 * R, length * R), (-0.48 * R, -0.18 * R), (-0.10 * R, -0.42 * R), (0.45 * R, -0.44 * R)]
    s = f'<path d="{smooth_path(pts, tension=0.75)}" fill="{col}" {_st(3.4)}/>'
    lite = shade(col, 0.30)
    for x0 in (-1.05, -0.86, -0.68):
        s += _line(f"M{fmt(x0 * R)},{fmt(-0.55 * R)} L{fmt((x0 - 0.04) * R)},{fmt((length - 0.08) * R)}", w=1.8, col=lite)
    s += _line(f"M{fmt(-0.40 * R)},{fmt(-0.98 * R)} Q{fmt(0.20 * R)},{fmt(-1.10 * R)} {fmt(0.66 * R)},{fmt(-0.86 * R)}",
               w=2.6, col=lite, extra='opacity="0.7"')
    if band:
        s += _tube(_spline_pts([(0.97 * R, -0.62 * R), (0.40 * R, -0.80 * R), (-0.40 * R, -0.76 * R),
                                (-1.10 * R, -0.42 * R)]), 0.12 * R, band, ow=2.2)
    return s


def _bald(R, skin):
    """Shaven head (Egyptian wise men / the baker): a shine on the scalp and a faint hairline shadow."""
    return (_ell(0.05 * R, -0.70 * R, 0.30 * R, 0.12 * R, HI, extra='opacity="0.45" transform="rotate(-14)"') +
            _line(f"M{fmt(-0.85 * R)},{fmt(-0.30 * R)} Q{fmt(-0.55 * R)},{fmt(-0.62 * R)} {fmt(-0.10 * R)},{fmt(-0.78 * R)}",
                  w=2.0, col=shade(skin, -0.18), extra='opacity="0.7"'))


def _trader_cloth(R, col, cord):
    """Desert traveller's head-cloth held by a dark cord ring (Ishmaelite traders)."""
    s = _cloth_cap(R, col)
    s += _tube(_spline_pts([(0.97 * R, -0.52 * R), (0.40 * R, -0.70 * R), (-0.40 * R, -0.66 * R),
                            (-0.98 * R, -0.36 * R)]), 0.13 * R, cord, ow=2.2)
    s += _tube(_spline_pts([(0.94 * R, -0.66 * R), (0.40 * R, -0.84 * R), (-0.40 * R, -0.80 * R),
                            (-0.96 * R, -0.50 * R)]), 0.10 * R, cord, ow=2.2)
    return s


# ---------------------------------------------------------------- worn things (body-frame hooks)
def _coat_robe_deco(progress, bw=19.0):
    """The coat of many colours: bold bands across the robe, colour k shown once progress >= (k+1)/6."""
    def deco(st, polys):
        m, pel, u = st["m"], st["pel"], st["u"]
        s = ""
        d = m["T"] + 12.0
        k = 0
        lo = -(m["th"] + m["sh"]) - 30
        while d > lo:
            j = k % len(COAT_BANDS)
            a = _band_alpha(j, progress)
            if a > 0:
                op = "" if a >= 1 else f'opacity="{a:.2f}"'
                for poly in polys:
                    s += _poly(_band(poly, pel, u, d - bw, d), COAT_BANDS[j], sw=0, extra=op)
            d -= bw
            k += 1
        if progress > 0:         # soft stitch lines between the bands
            d = m["T"] + 12.0 - bw
            while d > lo:
                for poly in polys:
                    e = _band_edge(poly, pel, u, d)
                    if len(e) == 2:
                        s += _line(_d(e, closed=False), w=1.6, col=shade(COAT_BASE, -0.25), extra='opacity="0.6"')
                d -= bw
        return s
    return deco


def _coat_sleeve_deco(progress, bw=16.0):
    n = len(COAT_BANDS)

    def deco(st, i, Sx, E, W):
        if progress <= 0:
            return ""
        aw = st["m"]["aw"]
        dw = _nrm(_sub(W, E))
        W2 = _sub(W, _mul(dw, 9))
        d = _d([Sx, E, W2], closed=False)
        s = ""
        for j, col in enumerate(COAT_BANDS):
            a = _band_alpha(j, progress)
            if a <= 0:
                continue
            op = "" if a >= 1 else f' opacity="{a:.2f}"'
            s += (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{fmt(aw - 0.5)}" stroke-linecap="butt" '
                  f'stroke-linejoin="round" stroke-dasharray="{fmt(bw)} {fmt((n - 1) * bw)}" '
                  f'stroke-dashoffset="{fmt(-j * bw)}"{op}/>')
        return s
    return deco


def _dust_deco(seed=0):
    """Dust smudges and a little rip at the hem (the under-tunic after the pit)."""
    def deco(st, polys):
        m, tp = st["m"], st["tp"]
        s = ""
        for fx, uy, r in ((-0.5, 0.55, 9), (0.45, 0.25, 7), (0.1, -0.35, 10), (-0.35, -0.75, 8), (0.55, -0.95, 7)):
            c = tp(fx * m["ww"], uy * m["T"] if uy > 0 else uy * (m["th"] + m["sh"]) * 0.5)
            s += _ell(c[0], c[1], r * 1.4, r, P["sackcloth_dark"], extra='opacity="0.35"')
        Hm, um = st["Hm"], st["um"]
        nv = (-um[1], um[0])
        a = _add(Hm, _mul(nv, 0.30 * m["ww"]))
        s += _poly([_sub(a, _mul(nv, 7)), _sub(_add(a, _mul(nv, 1)), _mul(um, 18)), _add(a, _mul(nv, 9)),
                    _add(_add(a, _mul(nv, 9)), _mul(um, 8)), _sub(_add(a, _mul(nv, -7)), _mul(um, -8))],
                   P["paper"], sw=2.4)
        return s
    return deco


def _pleat_deco(col, n=7):
    """Fine vertical pleats on a linen skirt (Egyptian kilts / robes)."""
    def deco(st, polys):
        m, pel, f, u = st["m"], st["pel"], st["f"], st["u"]
        s = ""
        for k in range(n):
            x = (-0.8 + 1.6 * k / (n - 1)) * m["ww"]
            a = _add(pel, _add(_mul(f, x), _mul(u, -6)))
            b = _add(st["Hm"], _mul(f, x * 1.25))
            s += _line(f"M{_pt(a)} L{_pt(b)}", w=1.6, col=col, extra='opacity="0.55"')
        return s
    return deco


def _collar_pts(st, k=1.0):
    m, tp = st["m"], st["tp"]
    T, shw = m["T"], m["shw"]
    outer = [tp(-0.95 * shw, T - 5), tp(-0.62 * shw, T - 26 * k), tp(0.08 * shw, T - 34 * k), tp(0.72 * shw, T - 24 * k),
             tp(0.98 * shw, T - 5)]
    inner = [tp(0.55 * shw, T + 1), tp(0.06 * shw, T - 11), tp(-0.55 * shw, T + 1)]
    return outer, inner


def _broad_collar(st, cols=(GOLD, LAPIS, CARNELIAN), k=1.0):
    """Egyptian broad bead collar (wesekh) round the neck: gold with rows of blue and red beads."""
    outer, inner = _collar_pts(st, k)
    s = f'<path d="{smooth_path(outer + inner, tension=0.8)}" fill="{cols[0]}" {_st(3.0)}/>'
    for t, col in ((0.38, cols[1]), (0.70, cols[2])):
        row = [_lerp(outer[j], _lerp(inner[0], inner[-1], 1 - j / 4) if j not in (2,) else inner[1], t)
               for j in range(5)]
        row = [_lerp(outer[0], inner[2], t), _lerp(outer[1], inner[2], t * 0.9), _lerp(outer[2], inner[1], t),
               _lerp(outer[3], inner[0], t * 0.9), _lerp(outer[4], inner[0], t)]
        s += (f'<path d="{smooth_path(row, closed=False)}" fill="none" stroke="{col}" stroke-width="{fmt(5 * k)}" '
              f'stroke-linecap="round" stroke-dasharray="{fmt(4 * k)} {fmt(3 * k)}"/>')
    s += f'<path d="{smooth_path(outer, closed=False)}" fill="none" {_st(2.2, GOLD_DARK)}/>'
    return s


def _gold_chain(st):
    """A gold chain of links round the neck with a round pendant on the chest (Gen 41:42)."""
    m, tp = st["m"], st["tp"]
    T, shw = m["T"], m["shw"]
    pts = _spline_pts([tp(-0.62 * shw, T - 6), tp(-0.30 * shw, T - 36), tp(0.12 * shw, T - 48), tp(0.55 * shw, T - 34),
                       tp(0.78 * shw, T - 8)], steps=5)
    s = ""
    for j, p in enumerate(pts[1:-1]):
        s += f'<ellipse cx="{fmt(p[0])}" cy="{fmt(p[1])}" rx="4.2" ry="3.2" fill="{GOLD}" {_st(1.6)}/>'
    c = tp(0.12 * shw, T - 58)
    s += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="10" fill="{GOLD}" {_st(2.4)}/>'
    s += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="4.5" fill="{LAPIS}"/>'
    s += f'<circle cx="{fmt(c[0] - 3)}" cy="{fmt(c[1] - 3)}" r="1.8" fill="{HI}"/>'
    return s


def _bare_chest(skin, belt, apron=None, collar=None, strap=None, chain=False, kilt_top=10):
    """Mid hook for a bare upper body over a linen kilt: skin-coloured chest, belt, optional front apron,
    leather chest strap (guards), broad collar and gold chain."""
    def mid(st):
        m, pel, u, f, tp = st["m"], st["pel"], st["u"], st["f"], st["tp"]
        lim = m["ww"] + 3
        bod = _clip(st["robe"][0], tp(0, kilt_top - 6), u)
        s = _poly(bod, skin, sw=OW) if len(bod) > 2 else ""
        s += _line(f"M{_pt(tp(-0.10 * m['ww'], m['T'] - 30))} Q{_pt(tp(0.25 * m['ww'], m['T'] - 40))} "
                   f"{_pt(tp(0.55 * m['ww'], m['T'] - 32))}", w=2.0, col=shade(skin, -0.2), extra='opacity="0.6"')
        if strap:
            a, b = tp(-0.85 * m["shw"], m["T"] - 4), tp(0.55 * m["ww"], kilt_top + 6)
            s += _tube([a, b], 9, strap, ow=2.4)
        for poly in st["robe"]:
            bb = _band(poly, pel, u, kilt_top - 9, kilt_top + 4)
            if len(bb) > 2:
                bb = _clip(bb, _sub(pel, _mul(f, lim)), f)
            if len(bb) > 2:
                bb = _clip(bb, _add(pel, _mul(f, lim)), _mul(f, -1))
            s += _poly(bb, belt, sw=2.6)
        if apron:
            top = tp(0.30 * m["ww"], kilt_top - 9)
            bot = _add(st["Hm"], _mul(f, 0.30 * m["ww"]))
            bot = _sub(bot, _mul(st["um"], 6))
            w0, w1 = 0.30 * m["ww"], 0.46 * m["ww"]
            q = [_sub(top, _mul(f, w0)), _add(top, _mul(f, w0)), _add(bot, _mul(f, w1)), _sub(bot, _mul(f, w1))]
            s += _poly(q, apron, sw=2.6)
            for t in (0.3, 0.55, 0.8):
                s += _line(_d([_lerp(q[0], q[3], t), _lerp(q[1], q[2], t)], closed=False), w=1.8,
                           col=shade(apron, -0.3))
        if collar:
            s += _broad_collar(st, collar)
        if chain:
            s += _gold_chain(st)
        return s
    return mid


def _armbands(col=GOLD, upper=True, wrist=True):
    def deco(st, i, Sx, E, W):
        s = ""
        aw = st["m"]["aw"]
        if upper:
            p = _lerp(Sx, E, 0.62)
            dv = _nrm(_sub(E, Sx))
            nv = (-dv[1], dv[0])
            s += _tube([_add(p, _mul(nv, aw / 2)), _sub(p, _mul(nv, aw / 2))], 6, col, ow=2.0)
        if wrist:
            dv = _nrm(_sub(W, E))
            p = _sub(W, _mul(dv, 5))
            nv = (-dv[1], dv[0])
            s += _tube([_add(p, _mul(nv, aw * 0.42)), _sub(p, _mul(nv, aw * 0.42))], 6, col, ow=2.0)
        return s
    return deco


def _ring_on(W, hr, col=GOLD):
    """A signet ring on the hand at W (a gold dot with a blue stone)."""
    return (f'<circle cx="{fmt(W[0] + 0.2 * hr)}" cy="{fmt(W[1] + 0.55 * hr)}" r="{fmt(0.42 * hr)}" fill="{col}" {_st(1.8)}/>'
            f'<circle cx="{fmt(W[0] + 0.2 * hr)}" cy="{fmt(W[1] + 0.55 * hr)}" r="{fmt(0.18 * hr)}" fill="{LAPIS}"/>')


def _question_mark(Hc, R):
    x0, y0 = Hc[0] + 1.25 * R, Hc[1] - 1.45 * R
    return (_line(f"M{fmt(x0 - 9)},{fmt(y0 - 6)} Q{fmt(x0 - 6)},{fmt(y0 - 22)} {fmt(x0 + 8)},{fmt(y0 - 20)} "
                  f"Q{fmt(x0 + 20)},{fmt(y0 - 14)} {fmt(x0 + 10)},{fmt(y0 - 2)} Q{fmt(x0 + 1)},{fmt(y0 + 6)} {fmt(x0 + 1)},"
                  f"{fmt(y0 + 14)}", w=4.2, col=MARK) + f'<circle cx="{fmt(x0 + 1)}" cy="{fmt(y0 + 26)}" r="3.4" fill="{MARK}"/>')


# ---------------------------------------------------------------- poses
_JS = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "walk_a": dict(POSES["walk_a"]),
    "walk_b": dict(POSES["walk_b"]),
    "run_a": dict(POSES["run_a"]),
    "run_b": dict(POSES["run_b"]),
    "talk": dict(POSES["dv_talk"]),
    "point": dict(POSES["point"]),
    "point_up": dict(POSES["dv_point_up"]),
    "pray": dict(POSES["dv_pray"]),
    "kneel_pray": dict(POSES["kneel_pray"]),
    "sleep": dict(POSES["sleep"]),
    "dream": dict(POSES["sleep"], expr="peaceful"),
    "sit": dict(POSES["sit"]),
    "sad": dict(POSES["sad"]),
    "hug": _P(t=6, h=4, legs=((10, 3), (-8, -3)), arms=(("ik", "abs", 100, -214, 1), ("ik", "abs", 88, -198, 1)),
              hands=("open", "open"), expr="happy"),
    "bow": dict(POSES["bow"]),
    "hold_rope": dict(POSES["hold_rope"], expr="worried"),
    "call_up": _P(h=-26, legs=((6, 2), (-5, -2)), arms=(("fk", 146, 166), ("fk", -162, -172)), hands=("open", "open"),
                  look=(0.03, -0.12), expr="call"),
    "cry": _P(t=6, h=14, arms=(("ik", "torso", 1.30, 0.55, 1), ("ik", "head", 0.70, 1.45, 1)), hands=("fist", "fist"),
              expr="crying"),
    "open_arms": _P(h=-6, legs=((8, 3), (-7, -3)), arms=(("fk", 92, 118), ("fk", -88, -112)), hands=("open", "open"),
                    expr="tearful"),
    "give": _P(t=6, h=4, legs=((10, 3), (-8, -3)), arms=(("fk", 62, 80), ("fk", 70, 84)), hands=("open", "open"),
               expr="kind"),
    "explain": _P(h=-4, arms=(("fk", 26, 64), ("fk", 40, 96)), hands=("open", "open"), expr="kind"),
    "comfort": _P(t=4, h=10, legs=((8, 3), (-7, -3)), arms=(("fk", 12, 6), ("ik", "abs", 92, -262, 1)),
                  hands=("fist", "open"), expr="kind"),
    "ride": _P(t=-2, lap=True, legs=((86, 4), (82, 2)), arms=(("ik", "body", 84, -58, 1), ("ik", "body", 70, -48, 1)),
               hem=0.97, flare=-8, expr="kind"),
    "ride_wave": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 146, 168), ("ik", "body", 64, -40, 1)),
                    hands=("open", "fist"), expr="kind"),
    "cross_arms": _P(h=6, legs=((8, 3), (-7, -3)), arms=(("ik", "torso", -0.15, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
                     far_front=True, expr="jealous"),
    "kneel_bow": _P(t=60, h=30, arms=(("ik", "abs", 132, -6, 1), ("ik", "abs", 116, -6, 1)),
                    hands=("ground", "ground"), expr="ashamed", **_KNEEL),
    "scared": dict(POSES["scared"]),
    "cheer": dict(POSES["cheer"]),
    "pull": dict(POSES["pull"]),
    "whisper": dict(POSES["whisper"]),
    "shrug": _P(h=-4, legs=((8, 3), (-7, -3)), arms=(("fk", 22, 112), ("fk", -24, -112)), hands=("open", "open"),
                expr="puzzled"),
    "lead": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", 40, 72), ("fk", -42, -26)), hands=("fist", "fist")),
    "lead_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 40, 72), ("fk", -42, -26)), hands=("fist", "fist")),
    "sit_throne": dict(POSES["sit_throne"]),
    "give_ring": _P(t=4, legs=((8, 3), (-7, -3)), arms=(("fk", 12, 6), ("fk", 78, 96)), hands=("fist", "fist"),
                    expr="kind"),
    "amazed": _P(h=-8, legs=((8, 3), (-7, -3)), arms=(("fk", 40, 118), ("fk", -36, -112)), hands=("open", "open"),
                 expr="amazed"),
    "worried": dict(POSES["worried"]),
    "count": _P(h=12, arms=(("ik", "body", 66, -66, 1), ("ik", "body", 42, -58, 1)), hands=("none", "fist"),
                look=(0.03, 0.08), expr="happy"),
}


def _js_pose(name):
    return dict(_JS[name])


def _check_js(pose, allowed, who):
    if pose not in allowed:
        raise ValueError(f"{who}: unknown pose {pose!r}; choose from {allowed}")


def _check_js_expr(expr, who):
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{who}: unknown expr {expr!r}; choose from {tuple(EXPRS)}")


def _carry_hooks(D, pose, item):
    """Carrying (sack on the shoulder / basket or jar in front), shared with the Noah section."""
    if pose in ("carry", "carry_walk_a", "carry_walk_b"):
        return _nh_items(D, "carry", 0.0, item, False, False, False)
    return None, None, None


def _carry_pose(pose, item):
    if pose == "carry":
        return _nh_carry_pose(item)
    return _nh_carry_pose(item, pose[-1])


# ---------------------------------------------------------------- Joseph
JOSEPH_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "talk", "explain", "point", "point_up", "pray",
                "kneel_pray", "sleep", "dream", "call_up", "hold_rope", "sit", "sad", "cry", "hug", "open_arms", "give",
                "ride", "ride_wave", "comfort", "bow", "carry", "carry_walk_a", "carry_walk_b")
JOSEPH_ATTIRES = ("shepherd", "slave", "prisoner", "ruler")
JOSEPH_COATS = ("colours", "torn", None)
_JS_NATURAL = {"stand": "happy", "walk_a": "happy", "walk_b": "happy", "run_a": "happy", "run_b": "happy",
               "talk": "happy", "point_up": "determined", "sleep": "sleepy", "dream": "peaceful", "sad": "sad",
               "kneel_pray": "peaceful", "pray": "peaceful", "hug": "tearful", "bow": "kind", "point": "happy",
               "sit": "neutral", "carry": "determined", "carry_walk_a": "determined", "carry_walk_b": "determined"}
_JS_ADULT_NATURAL = {"stand": "kind", "walk_a": "kind", "walk_b": "kind", "talk": "kind", "point": "kind",
                     "point_up": "kind", "sit": "neutral"}


def _joseph_design(attire, coat, progress, chain, ring, pose):
    D = dict(skin=JOSEPH_SKIN, leg=JOSEPH_SKIN, hair=JOSEPH_HAIR, hair_style="curly",
             hat=("custom", _joseph_curls), hat_h=0.12, sandal=SANDAL)
    if attire == "shepherd":
        if coat == "colours":
            D.update(robe=COAT_BASE, sleeve=COAT_BASE, hem=0.90, cuff=COAT_BANDS[4],
                     neck_v=shade(TUNIC, -0.08), robe_deco=_coat_robe_deco(progress),
                     arm_deco=_coat_sleeve_deco(progress))
        else:
            D.update(robe=TUNIC, sleeve=TUNIC, hem=0.60, flare_k=0.85, sleeve_len=0.5, hem_col=shade(TUNIC, -0.16),
                     hem_w=8, rope_belt=CORD, neck_v=shade(TUNIC, -0.18))
            if coat == "torn":
                D["robe_deco"] = _dust_deco()
                D["bare"] = True
    elif attire == "slave":       # sleeveless linen work tunic, cloth belt, barefoot
        D.update(robe=LINEN, sleeve=LINEN, sleeve_len=0.18, hem=0.62, flare_k=0.8, hem_col=shade(LINEN, -0.12), hem_w=7,
                 sash="#5d8fb0", sash_tail=True, bare=True, neck_v=shade(LINEN, -0.15), robe_deco=_pleat_deco(shade(LINEN, -0.25), 5))
    elif attire == "prisoner":    # plain grey-brown tunic, rope belt, barefoot, a little dusty
        col = "#a99c86"
        D.update(robe=col, sleeve=col, sleeve_len=0.5, hem=0.64, flare_k=0.8, hem_col=shade(col, -0.18), hem_w=8,
                 rope_belt="#8b6a45", bare=True, neck_v=shade(col, -0.2), robe_deco=_dust_deco(1))
    else:                         # ruler: vizier of Egypt
        D.update(robe=LINEN, sleeve=LINEN, hem=0.95, hem_col="#e3c47a", hem_w=9, cuff=GOLD, sash=GOLD, sash_tail=True,
                 robe_deco=_pleat_deco(shade(LINEN, -0.22), 7), sandal=GOLD_DARK, ears=False,
                 hat=("custom", _vizier_head), hat_h=0.22,
                 hair=None)
        D["mid"] = lambda st: _broad_collar(st) + (_gold_chain(st) if chain else "")    # noqa: E731
        if ring:
            D["front"] = lambda st: _ring_on(st["arms"][1][2], st["m"]["hr"])          # noqa: E731
    return D


def joseph(x, y, scale=1.0, facing=1, pose="stand", expr=None, attire="shepherd", coat="colours", progress=1.0,
           chain=True, ring=True, item="sack", marks=True):
    """Joseph (Genesis 37-50): teen shepherd with the coat of many colours, slave, prisoner or ruler of Egypt
    (see module doc, 'JOSEPH FILM')."""
    _check_js(pose, JOSEPH_POSES + ("walk",), "joseph")
    _check_js_expr(expr, "joseph")
    if attire not in JOSEPH_ATTIRES:
        raise ValueError(f"joseph: unknown attire {attire!r}; choose from {JOSEPH_ATTIRES}")
    if coat not in JOSEPH_COATS:
        raise ValueError(f"joseph: unknown coat {coat!r}; choose from {JOSEPH_COATS}")
    pose = "walk_a" if pose == "walk" else pose
    D = _joseph_design(attire, coat, _clamp01(progress), chain, ring, pose)
    if pose.startswith("carry"):
        ps = _carry_pose(pose, item)
        b, mi, fr = _carry_hooks(D, pose, item)
        D["behind"] = b
        D["mid"] = _hooks(D.get("mid"), mi)
        D["front"] = _hooks(D.get("front"), fr)
    else:
        ps = _js_pose(pose)
    if attire != "shepherd" and pose in _JS_ADULT_NATURAL:
        ps["expr"] = _JS_ADULT_NATURAL[pose]
    elif pose in _JS_NATURAL:
        ps["expr"] = _JS_NATURAL[pose]
    m = _JOSEPH_TEEN_M if attire == "shepherd" else _JOSEPH_M
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"joseph-{attire}-{pose}")


# ---------------------------------------------------------------- Jacob
JACOB_POSES = ("stand", "walk_a", "walk_b", "talk", "sit", "give", "cry", "hug", "sad", "bless", "open_arms")


def _jacob_hat(R):
    return _aged(R, "#e2a882", "#e7e1d8") + _cloth_cap(R, "#efe6d2", edge=JACOB_ROBE)


def _jacob_stool(st):
    """A low wooden three-legged stool under a seated figure (drawn behind)."""
    pel, m, g = st["pel"], st["m"], st["ground"]
    seat_y = pel[1] + m["seat"] * 0.75 + 4
    K = st["legs"][1][1]
    xa, xb = pel[0] - m["ww"] - 14, min(K[0] - 10, pel[0] + m["ww"] + 30)
    wood, wd = P["wood"], P["wood_dark"]
    s = ""
    for x0, x1 in ((xa + 10, xa + 2), (xb - 10, xb - 2), ((xa + xb) / 2, (xa + xb) / 2 + 4)):
        s += _tube([(x0, seat_y + 6), (x1, g - 3)], 10, wd, ow=3.0)
    s += (f'<rect x="{fmt(xa - 6)}" y="{fmt(seat_y - 4)}" width="{fmt(xb - xa + 12)}" height="15" rx="6" fill="{wood}" '
          f'{_st(3.4)}/>')
    s += _line(f"M{fmt(xa)},{fmt(seat_y + 1)} L{fmt(xb)},{fmt(seat_y + 1)}", w=2.0, col=P["wood_light"])
    return s


def _jacob_coat_front(D, kind, progress):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        PR = _prp()
        if kind == "give":         # holding the new coat up by its shoulders to show it
            cx, top = (W0[0] + W1[0]) / 2, min(W0[1], W1[1]) + 4
            k = 0.64
            s = f'<g transform="translate({fmt(cx)},{fmt(top)}) scale({k:.3f})">{PR._coat_shape("held", progress=progress)}</g>'
            return s + _fist(W0, hr, D["skin"], 0, 1) + _fist(W1, hr, D["skin"], 0, 1)
        # cry: the torn, dirty coat held to his chest, hanging over his knees
        c = ((W0[0] + W1[0]) / 2, min(W0[1], W1[1]) - 4)
        s = (f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate(-8) scale(0.42)">'
             f'{PR._coat_shape("held", torn=True, dirty=True)}</g>')
        return s + _fist(W0, hr, D["skin"], 0, 0) + _fist(W1, hr, D["skin"], 0, 0)
    return front


def _jacob_design(pose, staff, stool, progress):
    robe = JACOB_ROBE
    D = dict(robe=robe, sleeve=robe, hem_col="#d9b25a", cuff="#d9b25a", hem_w=10, skin="#e2a882", leg="#e2a882",
             hem=0.93, hair="#e4ddd0", hair_style="short", beard=("long", "#efeae2"), shawl="#e8d6aa",
             shawl_trim="#5f7f9a", hat=("custom", _jacob_hat), tail=("#efe6d2", JACOB_ROBE), ears=False,
             brow_w=5.0, brow_col="#9a9088", rope_belt=None)
    if pose == "give":
        D["front"] = _jacob_coat_front(D, "give", progress)
    elif pose == "cry":
        D["front"] = _jacob_coat_front(D, "cry", progress)
    elif pose == "sit" and stool:
        D["behind"] = _jacob_stool
    elif staff and pose in ("stand", "walk_a", "walk_b", "talk", "sad", "bless"):
        D["front"] = _staff_near(D)
    return D


_JC = {
    "stand": _P(t=8, arms=(("fk", 14, 8), ("fk", 30, 72)), expr="kind"),
    "walk_a": _P(t=10, legs=((24, 8), (-20, -34)), arms=(("fk", -40, -30), ("fk", 30, 72)), expr="kind"),
    "walk_b": _P(t=10, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 44), ("fk", 30, 72)), expr="kind"),
    "talk": _P(t=8, arms=(("fk", 26, 74), ("fk", 30, 72)), hands=("open", "fist"), expr="happy"),
    "sad": _P(t=12, h=22, arms=(("fk", 6, 2), ("fk", 30, 72)), expr="sad"),
    "bless": _P(t=6, h=-4, arms=(("fk", 84, 140), ("fk", 30, 72)), hands=("palm", "fist"), expr="kind"),
    "sit": dict(POSES["king_sit_stool"], expr="kind"),
    "give": _P(t=4, h=-2, legs=((10, 3), (-8, -3)), arms=(("ik", "abs", 168, -214, 1), ("ik", "abs", 70, -220, 1)),
               hands=("none", "none"), expr="happy", look=(0.03, -0.02)),
    "cry": _P(t=14, h=18, legs=(("ik", 80, 1), ("ik", 92, 1)),
              arms=(("ik", "torso", 1.40, 1.0, 1), ("ik", "torso", 1.20, 0.95, 1)), hands=("none", "none"),
              expr="crying", **_SEATED),
    "hug": dict(_JS["hug"], expr="tearful"),
    "open_arms": dict(_JS["open_arms"], expr="tearful"),
}


def jacob(x, y, scale=1.0, facing=1, pose="stand", expr=None, staff=True, stool=True, progress=1.0, marks=True):
    """Jacob (Israel), Joseph's old father: long white beard, plum robe, striped shawl, staff (see module doc)."""
    _check_js(pose, JACOB_POSES + ("walk",), "jacob")
    _check_js_expr(expr, "jacob")
    pose = "walk_a" if pose == "walk" else pose
    ps = dict(_JC[pose])
    if not staff and pose in ("stand", "walk_a", "walk_b", "talk", "sad", "bless"):
        ps["arms"] = (ps["arms"][0], ("fk", 10, 6) if pose != "bless" else ("fk", 10, 6))
    D = _jacob_design(pose, staff, stool, _clamp01(progress))
    e = expr or ps["expr"]
    inner, _ = _figure(D, _JACOB_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"jacob-{pose}")


# ---------------------------------------------------------------- the brothers and Benjamin
BROTHER_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "talk", "point", "cross_arms", "whisper", "pull",
                 "bow", "kneel_pray", "hug", "sad", "scared", "cheer", "carry", "carry_walk_a", "carry_walk_b")
BROTHER_NAMES = ("Reuben", "Simeon", "Levi", "Judah", "Dan", "Naphtali", "Gad", "Asher", "Issachar", "Zebulun")
_BROTHERS = [
    dict(robe="#6f8f5a", trim="#e3d2a6", skin="#dca57c", hair="#3a2618", beard=("full", "#3a2618"),
         hat=("headcloth", "#ece0c4", "#6f8f5a"), tail=("#ece0c4", "#6f8f5a"), shawl="#e3d2a6"),
    dict(robe="#9a4a3c", trim="#e0b25a", skin="#c98f68", hair="#241b17", beard=("short", "#241b17"),
         hat=("wrap", "#e0b25a", "#a8743c")),
    dict(robe="#4e6d92", trim="#e6d6b2", skin="#d9a37a", hair="#2f2420", beard=("stubble", "#2f2420"),
         hat=("headband", "#c0533a")),
    dict(robe="#b8873c", trim="#7a4a2a", skin="#d39a72", hair="#5a3a24", beard=("full", "#5a3a24"),
         hat=("headcloth", "#efe2c4", "#7a4a2a"), tail=("#efe2c4", "#7a4a2a"), shawl="#7a4a2a"),
    dict(robe="#7a5a3e", trim="#5fa8a6", skin="#c68a62", hair="#2a201b", beard=("pointed", "#2a201b"),
         hat=("wrap", "#5fa8a6", "#3b7d7b")),
    dict(robe="#5f8a85", trim="#e0a23c", skin="#dca57c", hair="#3a2a22", beard=("short", "#3a2a22"),
         hat=("headband", "#e0a23c")),
    dict(robe="#8a6a9a", trim="#ead9b4", skin="#e2a77e", hair="#4a2f1f", beard=("full", "#4a2f1f"),
         hat=("headcloth", "#ead9b4", "#8a6a9a"), tail=("#ead9b4", "#8a6a9a"), shawl="#ead9b4"),
    dict(robe="#c4704a", trim="#efe2c4", skin="#b07a52", hair="#241b17", beard=("stubble", "#241b17"),
         hat=("wrap", "#efe2c4", "#c4704a")),
    dict(robe="#6a7a4a", trim="#d9a03c", skin="#d39a72", hair="#4a3020", beard=("short", "#4a3020"),
         hat=("headband", "#d9a03c")),
    dict(robe="#a65a6a", trim="#e9dcc0", skin="#e2a77e", hair="#3a2618", beard=("stubble", "#3a2618"), hat=None),
]
BENJAMIN_TUNIC = "#88b5c9"


def _brother_design(variant, pose, staff):
    if variant == "benjamin":
        t = BENJAMIN_TUNIC
        D = dict(robe=t, sleeve=t, hem_col=shade(t, -0.2), hem_w=7, skin=JOSEPH_SKIN, leg=JOSEPH_SKIN, hem=0.56,
                 flare_k=0.9, sleeve_len=0.55, rope_belt=CORD, hair=JOSEPH_HAIR, hair_style="curly",
                 hat=("custom", _joseph_curls), hat_h=0.12, neck_v=shade(t, 0.3))
        return D
    v = _BROTHERS[int(variant) % 10]
    robe = v["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=v["trim"], cuff=v["trim"], hem_w=10, skin=v["skin"], leg=v["skin"],
             hem=0.80, flare_k=0.9, sleeve_len=0.62, rope_belt="#8b6a45", hair=v["hair"], hair_style="curly",
             beard=v["beard"], neck_v=v["trim"], sandal=SANDAL)
    if v.get("hat"):
        D["hat"] = v["hat"]
    if v.get("tail"):
        D.update(tail=v["tail"], ears=False)
    if v.get("shawl"):
        D.update(shawl=v["shawl"], shawl_trim=shade(v["shawl"], -0.25))
    if staff:
        D["front"] = _staff_near(D)
    return D


_BR = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", 40, 76))),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -46, -36), ("fk", 40, 76))),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 46), ("fk", 40, 76))),
    "talk": _P(h=-2, arms=(("fk", 26, 74), ("fk", 40, 76)), hands=("open", "fist"), expr="happy"),
}
_BR_NATURAL = {"stand": "neutral", "walk_a": "neutral", "walk_b": "neutral", "point": "angry", "pull": "determined",
               "bow": "worried", "kneel_pray": "peaceful", "hug": "tearful", "sad": "ashamed", "run_a": "worried",
               "run_b": "worried", "carry": "neutral", "carry_walk_a": "neutral", "carry_walk_b": "neutral",
               "talk": "neutral"}


def brothers(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, staff=None, item="sack", marks=True):
    """One of Joseph's brothers: variant 0-9 = the ten older brothers (bearded shepherds), 'benjamin' = the
    youngest, a small boy (see module doc, 'JOSEPH FILM'). brother() is the same function."""
    _check_js(pose, BROTHER_POSES + ("walk",), "brothers")
    _check_js_expr(expr, "brothers")
    if variant != "benjamin" and not isinstance(variant, int):
        raise ValueError(f"brothers: variant must be 0-9 or 'benjamin', not {variant!r}")
    pose = "walk_a" if pose == "walk" else pose
    ben = variant == "benjamin"
    if staff is None:
        staff = not ben and pose in _BR
    use_staff = staff and pose in _BR and not ben
    D = _brother_design(variant, pose, use_staff)
    if pose.startswith("carry"):
        ps = _carry_pose(pose, item)
        D["behind"], D["mid"], D["front"] = _carry_hooks(D, pose, item)
    elif use_staff:
        ps = dict(_BR[pose])
    else:
        ps = dict(_JS.get(pose) or POSES[pose])
    if pose == "bow":
        ps = _js_pose("kneel_bow")
    ps["expr"] = _BR_NATURAL.get(pose, ps["expr"])
    if ben and pose in ("stand", "walk_a", "walk_b", "talk"):
        ps["expr"] = "happy"
    e = expr or ps["expr"]
    m = _CHILD if ben else _metrics(_ADULT, 1.0 + 0.012 * (int(variant) % 5 - 2), 1.0 + 0.03 * (int(variant) % 3 - 1))
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"brother{variant}-{pose}")


brother = brothers

# (variant, dx, dy, facing) at scale 1: back row (drawn first, 34 px higher, 0.96 x) then the front row
_BR_GROUP = [(4, -330, -34, 1), (8, -165, -34, 1), (1, 0, -36, 1), (5, 165, -34, -1), (9, 330, -34, -1),
             (6, -410, 0, 1), (2, -245, 0, 1), (0, -82, 0, 1), (3, 82, 0, -1), (7, 245, 0, -1)]
BROTHERS_GROUP_POSES = ("stand", "talk", "cross_arms", "point", "bow", "kneel_pray", "sad", "scared", "hug", "cheer",
                        "walk_a", "walk_b", "run_a", "run_b", "carry_walk_a", "carry_walk_b", "whisper")


def brothers_group(x, y, scale=1.0, facing=1, pose="stand", n=10, expr=None, gap=150, exprs=None, marks=True):
    """The ten older brothers together (see module doc): a group in two rows, or a line for walk / run poses."""
    _check_js(pose, BROTHERS_GROUP_POSES, "brothers_group")
    sx = 1 if facing >= 0 else -1
    n = max(1, min(10, int(n)))
    out = ""
    if pose.startswith(("walk", "run", "carry_walk")):
        other = {"walk_a": "walk_b", "walk_b": "walk_a", "run_a": "run_b", "run_b": "run_a",
                 "carry_walk_a": "carry_walk_b", "carry_walk_b": "carry_walk_a"}[pose]
        for i in reversed(range(n)):
            p_ = pose if i % 2 == 0 else other
            e = (exprs[i % len(exprs)] if exprs else expr)
            out += brothers(x - sx * i * gap * scale, y, scale, facing, variant=i, pose=p_, expr=e, marks=marks)
        return f'<g data-who="brothers_group-{pose}">{out}</g>'
    if pose in ("bow", "kneel_pray"):          # kneeling: two staggered rows, everybody facing the same way
        for i in reversed(range(n)):
            back = i % 2 == 1
            dx = (-460 + 230 * (i // 2)) + (115 if back else 0)
            e = (exprs[i % len(exprs)] if exprs else expr)
            out += brothers(x + sx * dx * scale, y - (40 if back else 0) * scale, scale * (0.96 if back else 1.0), sx,
                            variant=i, pose=pose, expr=e, marks=marks)
        return f'<g data-who="brothers_group-{pose}">{out}</g>'
    members = [g for g in _BR_GROUP if g[0] < n] if n < 10 else _BR_GROUP
    for v, dx, dy, f in members:
        p_ = pose
        if pose == "whisper":
            p_ = "whisper" if f > 0 else "cross_arms"
        e = (exprs[v % len(exprs)] if exprs else expr)
        k = 0.96 if dy < 0 else 1.0
        out += brothers(x + sx * dx * scale, y + dy * scale, scale * k, f * sx, variant=v, pose=p_, expr=e, marks=marks)
    return f'<g data-who="brothers_group-{pose}">{out}</g>'


# ---------------------------------------------------------------- Pharaoh
PHARAOH_POSES = ("stand", "walk_a", "walk_b", "talk", "sit_throne", "sleep", "point", "give_ring", "amazed", "worried")


def _pharaoh_head(R):
    return _nemes(R, GOLD, LAPIS, GOLD_DARK, cobra=True) + _false_beard(R) + _eyeliner(R)


def _pharaoh_design(pose, throne):
    skin = PHARAOH_SKIN
    D = dict(robe=LINEN, sleeve=skin, sleeve_len=0.0, skin=skin, leg=skin, hem=0.92, hem_col=GOLD, hem_w=8,
             flare_k=1.0, ears=False, hat=("custom", _pharaoh_head), hat_h=0.24, sandal=GOLD_DARK,
             robe_deco=_pleat_deco(shade(LINEN, -0.22), 9), arm_deco=_armbands())
    D["mid"] = _bare_chest(skin, GOLD, apron="#e8c25a", collar=(GOLD, LAPIS, CARNELIAN))
    if pose == "sit_throne" and throne:
        def behind(st):
            pel, g = st["pel"], st["ground"]
            return f'<g transform="translate({fmt(pel[0])},{fmt(g)})">{_prp()._egypt_throne()}</g>'
        D["behind"] = behind
    if pose == "give_ring":
        def front(st):
            W, hr = st["arms"][1][2], st["m"]["hr"]
            return (f'<g transform="translate({fmt(W[0] + 6)},{fmt(W[1] - 10)}) scale(0.32)">{_prp()._signet_ring()}</g>'
                    + _fist(W, hr, skin, 0, 2))
        D["front"] = front
    return D


def pharaoh(x, y, scale=1.0, facing=1, pose="stand", expr=None, throne=True, marks=True):
    """Pharaoh, king of Egypt: blue-gold striped nemes with a cobra, false beard, broad collar, white pleated
    kilt-robe (see module doc, 'JOSEPH FILM')."""
    _check_js(pose, PHARAOH_POSES + ("walk",), "pharaoh")
    _check_js_expr(expr, "pharaoh")
    pose = "walk_a" if pose == "walk" else pose
    ps = _js_pose(pose)
    if pose in ("stand", "walk_a", "walk_b", "sit_throne"):
        ps["expr"] = "neutral"
    D = _pharaoh_design(pose, throne)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _PHARAOH_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"pharaoh-{pose}")


# ---------------------------------------------------------------- Egyptians
EGYPTIAN_KINDS = ("servant", "guard", "wise", "potiphar", "woman", "cupbearer", "baker")
EGYPTIAN_POSES = ("stand", "walk_a", "walk_b", "talk", "point", "bow", "kneel_bow", "shrug", "carry", "carry_walk_a",
                  "carry_walk_b", "lead", "lead_b", "give", "sit", "sad", "cheer", "amazed", "worried")
_EG_KILT = ["#e9d39a", "#c9533f", "#3f6fa8", "#6f8a45"]          # belts / aprons per variant
_EG_WISE = [dict(robe="#2f4f7f", pat=("#e8c25a", "dots")), dict(robe="#8a5a2a", pat=("#f0dca0", "diamond")),
            dict(robe="#4f6f3f", pat=("#e9d9ae", "flower"))]


def _scroll_front(D):
    def front(st):
        W0, hr = st["arms"][0][2], st["m"]["hr"]
        return (f'<rect x="{fmt(W0[0] - 8)}" y="{fmt(W0[1] - 34)}" width="16" height="56" rx="7" fill="{PARCH_ROLL}" '
                f'{_st(3.0)}/>' + _fist(W0, hr, D["skin"]))
    return front


def _keys_front(D):
    """A ring of big wooden keys held out (Potiphar trusts Joseph with the house)."""
    def front(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        c = (W[0] + 4, W[1] + 18)
        s = f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="11" fill="none" {_st(7)}/>'
        s += f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="11" fill="none" {_st(3.2, GOLD)}/>'
        for ang, ln in ((60, 46), (100, 40), (135, 34)):
            a = math.radians(ang)
            p0 = (c[0] + 11 * math.cos(a), c[1] + 11 * math.sin(a))
            p1 = (p0[0] + ln * math.cos(a), p0[1] + ln * math.sin(a))
            s += _tube([p0, p1], 6, P["wood_light"], ow=2.4)
            s += _tube([p1, (p1[0] + 9 * math.cos(a + 1.57), p1[1] + 9 * math.sin(a + 1.57))], 5, P["wood_light"], ow=2.2)
        return s + _fist(W, hr, D["skin"], 0, 0)
    return front


def _cup_front(D):
    def front(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        x, y0 = W[0] + 4, W[1] - 8
        s = (f'<path d="M{fmt(x - 13)},{fmt(y0 - 22)} L{fmt(x + 13)},{fmt(y0 - 22)} Q{fmt(x + 12)},{fmt(y0 - 4)} {fmt(x)},'
             f'{fmt(y0 - 2)} Q{fmt(x - 12)},{fmt(y0 - 4)} {fmt(x - 13)},{fmt(y0 - 22)} Z" fill="{GOLD}" {_st(2.6)}/>')
        s += _ell(x, y0 - 22, 13, 4, "#8a2f4a", sw=2.2)
        return s + _fist(W, hr, D["skin"], 0, 2)
    return front


def _egyptian_design(kind, variant, prisoner, spear, pose):
    v = int(variant)
    skin = EGYPT_SKIN[v % 4]
    wig = ("custom", lambda R: _bob_wig(R) + _eyeliner(R))
    if prisoner and kind in ("cupbearer", "baker", "servant"):
        col = "#b7aa90" if kind != "baker" else "#c9b48a"
        D = dict(robe=col, sleeve=col, sleeve_len=0.5, skin=skin, leg=skin, hem=0.64, flare_k=0.8,
                 hem_col=shade(col, -0.18), hem_w=8, rope_belt="#8b6a45", bare=True, neck_v=shade(col, -0.2),
                 robe_deco=_dust_deco(2 + v), hair=EGYPT_HAIR, hair_style="short")
        if kind == "baker":
            D.update(hair=None, hat=("custom", lambda R: _bald(R, skin)), hat_h=0.0)
        else:
            D.update(beard=("stubble", "#3a2a22"))
        return D, (_metrics(_ADULT, 0.98, 1.16) if kind == "baker" else _metrics(_ADULT, 1.0, 0.96))
    m = _ADULT
    if kind in ("servant", "guard", "cupbearer", "baker"):
        D = dict(robe=LINEN, sleeve=skin, sleeve_len=0.0, skin=skin, leg=skin, hem=0.55 if kind != "baker" else 0.62,
                 flare_k=0.8, hem_col=shade(LINEN, -0.10), hem_w=6, ears=False, hat=wig, hat_h=0.16, bare=True,
                 robe_deco=_pleat_deco(shade(LINEN, -0.25), 5))
        belt = _EG_KILT[v % 4]
        collar = None
        apron = None
        strap = None
        if kind == "guard":
            D.update(hat=("custom", lambda R: _nemes(R, LINEN, LAPIS, None, lappet=False, stripes=6) + _eyeliner(R)),
                     hat_h=0.22, sandal=SANDAL_DARK, bare=False)
            apron, strap = shade(belt, 0.2), LEATHER
            m = _metrics(_ADULT, 1.02, 1.04)
        elif kind == "cupbearer":
            collar = (GOLD, LAPIS, CARNELIAN)
            D.update(hem=0.80, bare=False, sandal=SANDAL)
        elif kind == "baker":
            D.update(hat=("custom", lambda R: _bald(R, skin)), hat_h=0.0, hair=None, hem=0.70)
            m = _metrics(_ADULT, 0.98, 1.16)
            apron = "#f2e8d0"
        D["mid"] = _bare_chest(skin, belt, apron=apron, collar=collar, strap=strap)
        if kind == "guard" and spear:
            D["front"] = _spear_front(D)
        return D, m
    if kind == "wise":
        w = _EG_WISE[v % 3]
        D = dict(robe=w["robe"], sleeve=w["robe"], skin=skin, leg=skin, hem=0.97, flare_k=0.9, hem_col=GOLD, hem_w=9,
                 cuff=GOLD, pattern=(w["pat"][0], w["pat"][1], 22), sash=GOLD, sash_tail=True, sandal=SANDAL_DARK,
                 ears=True, hat=("custom", lambda R: _bald(R, skin) + _eyeliner(R)), hat_h=0.0, hair=None,
                 neck_v=GOLD)
        D["mid"] = lambda st: _broad_collar(st, (GOLD, LAPIS, "#e8dcc0"), 0.8)    # noqa: E731
        if v % 3 == 1:
            D["beard"] = ("pointed", "#e4ddd0")
        return D, _metrics(_ADULT, 1.0, 1.0)
    if kind == "potiphar":
        D = dict(robe=LINEN, sleeve=LINEN, skin="#c98f68", leg="#c98f68", hem=0.95, flare_k=1.1, hem_col=CARNELIAN,
                 hem_w=10, cuff=CARNELIAN, sash=CARNELIAN, sash_tail=True, sandal=GOLD_DARK, ears=False,
                 hat=("custom", lambda R: _bob_wig(R, length=0.70) + _eyeliner(R)), hat_h=0.16,
                 robe_deco=_pleat_deco(shade(LINEN, -0.22), 7))
        D["mid"] = lambda st: _broad_collar(st, (GOLD, LAPIS, CARNELIAN), 1.1)     # noqa: E731
        return D, _metrics(_ADULT, 1.02, 1.24)
    # woman
    dress = LINEN
    band = (LAPIS, CARNELIAN, "#3b8b89", GOLD)[v % 4]
    D = dict(robe=dress, sleeve=skin, sleeve_len=0.0, skin=skin, leg=skin, hem=1.0, flare_k=0.55, hem_col=band,
             hem_w=7, sandal=SANDAL, ears=False, sash=band, sash_tail=True,
             hat=("custom", lambda R: _bob_wig(R, length=1.45, band=band) + _eyeliner(R)), hat_h=0.16,
             robe_deco=_pleat_deco(shade(LINEN, -0.2), 5))
    D["mid"] = lambda st: _broad_collar(st, (GOLD, band, "#e8dcc0"), 0.85)        # noqa: E731
    return D, _metrics(_ADULT, 0.95, 0.88)


def egyptian(x, y, scale=1.0, facing=1, kind="servant", variant=0, pose="stand", expr=None, prisoner=False,
             spear=None, item="sack", marks=True):
    """Egyptians (servants, guards, wise men, Potiphar, women, the cupbearer and the baker), see module doc."""
    if kind not in EGYPTIAN_KINDS:
        raise ValueError(f"egyptian: unknown kind {kind!r}; choose from {EGYPTIAN_KINDS}")
    _check_js(pose, EGYPTIAN_POSES + ("walk",), "egyptian")
    _check_js_expr(expr, "egyptian")
    pose = "walk_a" if pose == "walk" else pose
    if spear is None:
        spear = kind == "guard" and pose in ("stand", "walk_a", "walk_b")
    D, m = _egyptian_design(kind, variant, prisoner, spear, pose)
    if pose.startswith("carry"):
        ps = _carry_pose(pose, item)
        b, mi, fr = _carry_hooks(D, pose, item)
        D["behind"], D["mid"], D["front"] = b, _hooks(D.get("mid"), mi), fr
    elif pose == "bow":
        ps = _js_pose("kneel_bow")
        ps["expr"] = "peaceful"
    elif kind == "guard" and spear and pose in ("stand", "walk_a", "walk_b"):
        ps = dict(POSES[_GUARD_ALIAS[pose]])
    elif kind == "guard" and pose in ("lead", "lead_b"):
        ps = _js_pose(pose)
        far = _spear_front(D)

        def spear_far(st):           # the spear in the far hand, behind the body
            st2 = dict(st, arms=[st["arms"][1], st["arms"][0]])
            return far(st2)
        D["behind"] = spear_far
        D["front"] = None
    else:
        ps = _js_pose(pose)
    if pose == "give":
        D["front"] = _keys_front(D) if kind == "potiphar" else (_cup_front(D) if kind == "cupbearer" else None)
    elif pose == "stand" and kind == "cupbearer" and not prisoner:
        ps = _P(arms=(("fk", 14, 8), ("fk", 40, 90)), expr="neutral")
        D["front"] = _cup_front(D)
    elif pose in ("stand", "shrug") and kind == "wise" and int(variant) % 3 == 0 and pose == "stand":
        D["front"] = _scroll_front(D)
    if pose == "shrug" and marks:
        D["front"] = _hooks(D.get("front"), lambda st: _question_mark(st["Hc"], st["m"]["R"]))
    if kind == "potiphar" and pose in ("stand", "walk_a", "walk_b", "talk", "give", "point"):
        ps["expr"] = "happy"
    elif pose in ("stand", "walk_a", "walk_b", "lead", "lead_b") and ps["expr"] == "neutral":
        ps["expr"] = "neutral"
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"egyptian-{kind}{variant}-{pose}")


# ---------------------------------------------------------------- the Ishmaelite traders
TRADER_POSES = ("stand", "walk_a", "walk_b", "talk", "lead", "lead_b", "give", "count", "point")
_TRADERS = [dict(robe="#c9a46a", stripe="#8a5a3a", cloth="#f0e6cc", cord="#3a2a22", skin="#b07a52", beard="#2a201b"),
            dict(robe="#7f9a8a", stripe="#e8d6aa", cloth="#d9534a", cord="#2a201b", skin="#c68a62", beard="#4a3020"),
            dict(robe="#b8674a", stripe="#f0d890", cloth="#efe2c4", cord="#5a3a24", skin="#a46b47", beard="#2a201b")]


def _coins_front(D, n=3):
    def front(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        s = ""
        for k in range(n):
            s += _prp()._coin(W[0] + 6 + 4 * k, W[1] - 10 - 7 * k, 9)
        return s + _fist(W, hr, D["skin"], 0, 2)
    return front


def _pouch_front(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        c = ((W0[0] + W1[0]) / 2, (W0[1] + W1[1]) / 2 + 14)
        s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) scale(0.55)">{_prp()._coin_pouch(open_=True)}</g>'
        s += _prp()._coin(W0[0] + 4, W0[1] - 8, 9)
        return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    return front


def trader(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, marks=True):
    """An Ishmaelite spice trader (Gen 37:25-28), variant 0-2 (see module doc)."""
    _check_js(pose, TRADER_POSES + ("walk",), "trader")
    _check_js_expr(expr, "trader")
    pose = "walk_a" if pose == "walk" else pose
    v = _TRADERS[int(variant) % 3]
    D = dict(robe=v["robe"], sleeve=v["robe"], hem_col=v["stripe"], cuff=v["stripe"], hem_w=10, skin=v["skin"],
             leg=v["skin"], hem=0.94, flare_k=1.0, stripes=(v["stripe"], 26, 7), sash="#8a3c3c", sash_tail=True,
             hair=v["beard"], hat=("custom", lambda R: _trader_cloth(R, v["cloth"], v["cord"])), hat_h=0.12,
             tail=(v["cloth"], None), ears=False, beard=("full", v["beard"]), sandal=SANDAL_DARK)
    ps = _js_pose(pose if pose != "give" else "give")
    if pose == "give":
        ps = _P(t=4, legs=((8, 3), (-7, -3)), arms=(("fk", 12, 6), ("fk", 68, 86)), hands=("fist", "none"), expr="happy")
        D["front"] = _coins_front(D)
    elif pose == "count":
        D["front"] = _pouch_front(D)
    if pose in ("stand", "walk_a", "walk_b", "talk", "lead", "lead_b"):
        ps["expr"] = "happy"
    e = expr or ps["expr"]
    inner, _ = _figure(D, _metrics(_ADULT, 1.0, 1.04), ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"trader{int(variant) % 3}-{pose}")


# ---------------------------------------------------------------- two figures hugging
def hug_pair(x, y, scale=1.0, facing=1, a=None, b=None, gap=95):
    """Two people hugging. a = (fn, kwargs) stands at x facing ``facing``; b = (fn, kwargs) stands gap*scale in
    front of a, facing back. Both get pose='hug' unless their kwargs say otherwise. b is drawn first, then a,
    whose arms come round b's shoulders. Default: Joseph (ruler, tearful) hugging Jacob."""
    a = a or (joseph, dict(attire="ruler", expr="tearful"))
    b = b or (jacob, dict(expr="tearful"))
    sx = 1 if facing >= 0 else -1
    ka, kb = dict(a[1]), dict(b[1])
    ka.setdefault("pose", "hug")
    kb.setdefault("pose", "hug")
    out = b[0](x + sx * gap * scale, y, scale, -sx, **kb)
    out += a[0](x, y, scale, sx, **ka)
    return f'<g data-who="hug_pair">{out}</g>'


# ---------------------------------------------------------------- the modern siblings (child(sibling=...))
SIBLINGS = ("big", "little")
SIBLING_POSES = ("tug", "sulk", "sorry", "hug", "share")
_SIB_POSES = {
    "tug": _P(t=-18, drop=8, legs=(("ik", 40, 0), ("ik", -16, 1)), arms=(("ik", "abs", 74, -108, 1), ("ik", "abs", 58, -102, 1)),
              expr="cross"),
    "sulk": _P(flip=True, h=14, legs=((6, 2), (-5, -2)), arms=(("ik", "torso", -0.15, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
               far_front=True, expr="cross"),
    "sorry": _P(h=20, arms=(("ik", "torso", -1.30, 0.30, -1), ("ik", "torso", -1.30, 0.30, -1)), hands=("none", "fist"),
                expr="sorry"),
    "hug": _P(t=6, h=4, legs=((8, 3), (-7, -3)), arms=(("ik", "abs", 64, -152, 1), ("ik", "abs", 54, -140, 1)),
              hands=("open", "open"), expr="happy"),
    "share": _P(t=4, h=8, arms=(("ik", "body", 44, -36, 1), ("ik", "body", 26, -32, 1)), hands=("none", "none"),
                expr="kind", look=(0.03, 0.04)),
}
SIB_DRESS = "#e8786a"
SIB_SHIRT = "#5fa3c9"
SIB_SHORTS = "#3f5f8a"


def _sister_hair(R, col="#6a3f24"):
    """Big sister: a bouncy ponytail at the back with a yellow ribbon, a side-swept fringe."""
    s = (f'<path d="{smooth_path([(-0.80 * R, -0.62 * R), (-1.30 * R, -0.70 * R), (-1.62 * R, -0.30 * R), (-1.55 * R, 0.30 * R), (-1.30 * R, 0.10 * R), (-1.10 * R, -0.25 * R)])}" '
         f'fill="{col}" {_st(3.2)}/>')
    s += _line(f"M{fmt(-1.25 * R)},{fmt(-0.50 * R)} Q{fmt(-1.45 * R)},{fmt(-0.25 * R)} {fmt(-1.42 * R)},{fmt(0.10 * R)}", w=2.0,
               col=shade(col, 0.3))
    s += _ell(-0.96 * R, -0.62 * R, 0.14 * R, 0.20 * R, "#f2c84b", sw=2.6, extra='transform="rotate(30)"')
    s += _ell(-0.96 * R, -0.62 * R, 0.06 * R, 0.06 * R, shade("#f2c84b", -0.3))
    s += (f'<path d="M{fmt(0.92 * R)},{fmt(-0.42 * R)} Q{fmt(0.55 * R)},{fmt(-0.30 * R)} {fmt(0.15 * R)},{fmt(-0.46 * R)} '
          f'Q{fmt(0.50 * R)},{fmt(-0.70 * R)} {fmt(0.92 * R)},{fmt(-0.42 * R)} Z" fill="{col}" {_st(2.4)}/>')
    return s


def _sibling_design(sibling):
    if sibling == "big":          # big sister (~7): coral dress with a cream collar, ponytail with a yellow ribbon
        c = SIB_DRESS
        D = dict(robe=c, sleeve=c, sleeve_len=0.45, hem_col=shade(c, -0.15), hem_w=7, skin="#f0c09a", leg="#f0c09a",
                 hem=0.56, flare_k=1.25, hair="#6a3f24", hair_style="short", sandal="#d4523f", neck_v="#f6ecd8",
                 hat=("custom", _sister_hair), hat_h=0.1)
        def mid(st):
            tp, m = st["tp"], st["m"]
            p = tp(0.35 * m["ww"], -0.15 * m["T"])
            return (f'<rect x="{fmt(p[0] - 8)}" y="{fmt(p[1] - 7)}" width="16" height="13" rx="3" fill="{shade(c, 0.25)}" '
                    f'{_st(2.2)}/>')
        D["mid"] = mid
        return D, _metrics(_CHILD, 1.07, 1.0)
    c = SIB_SHIRT                # little brother (~4): striped t-shirt, navy shorts, sneakers
    D = dict(robe=c, sleeve=c, sleeve_len=0.42, hem_col=shade(c, -0.12), hem_w=6, skin="#f2c29c", leg="#f2c29c",
             hem=0.30, flare_k=0.9, hair="#8a5a34", hair_style="curly", sandal="#e8e2d6", neck_v=shade(c, 0.35),
             stripes=("#f2c84b", 16, 6))

    def legwear(st, i):
        H, K, A, a1, a2 = st["legs"][i]
        return _tube([H, _lerp(H, K, 0.92)], st["m"]["lw"] + 10, SIB_SHORTS if i else shade(SIB_SHORTS, -0.15), ow=3.2)
    D["legwear"] = legwear
    return D, _metrics(_CHILD, 0.92, 1.0)


def _toy_front(D, kind, pose):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        PR = _prp()
        if pose == "share":       # held out in both hands
            cx, yy = (W0[0] + W1[0]) / 2 + 8, max(W0[1], W1[1]) + (40 if kind == "horse" else 30)
            s = f'<g transform="translate({fmt(cx)},{fmt(yy)}) scale(0.5)">{PR._toy(kind)}</g>'
            return s + _fist(W0, hr, D["skin"], 0, 1) + _fist(W1, hr, D["skin"], 0, 1)
        if pose == "tug":         # gripped by the head / the near side, the toy reaching out in front
            cx, yy = W0[0] + (26 if kind == "horse" else 22), W0[1] + (42 if kind == "horse" else 28)
            s = f'<g transform="translate({fmt(cx)},{fmt(yy)}) scale(0.5)">{PR._toy(kind)}</g>'
            return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
        W = W1                    # other poses: hanging from the near hand / tucked under the arm
        s = f'<g transform="translate({fmt(W[0] + 4)},{fmt(W[1] + 34)}) scale(0.42)">{PR._toy(kind)}</g>'
        return s + _fist(W, hr, D["skin"])
    return front


def _child_joseph(x, y, scale, facing, pose, expr, hood, boots, coat, phase, marks, sibling, toy):
    """child() with the Joseph-film options (sibling outfits, the new poses, the toy)."""
    if pose not in CHILD_POSES + SIBLING_POSES:
        raise ValueError(f"child: unknown pose {pose!r}; choose from {CHILD_POSES + SIBLING_POSES}")
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"child: unknown expr {expr!r}; choose from {tuple(EXPRS)}")
    if sibling is not None and sibling not in SIBLINGS:
        raise ValueError(f"child: unknown sibling {sibling!r}; choose from {SIBLINGS}")
    if toy is not None and toy not in ("horse", "ball"):
        raise ValueError(f"child: toy must be None, 'horse' or 'ball', not {toy!r}")
    if pose == "wave":
        f = 166 + 18 * math.sin(2 * math.pi * phase)
        ps = _P(h=-4, arms=(("fk", 146, f), ("fk", -10, -4)), hands=("open", "fist"), expr="happy")
    elif pose in _SIB_POSES:
        ps = dict(_SIB_POSES[pose])
    else:
        ps = dict(_CH_POSES[pose])
    if sibling is None:
        D, m = _child_design(ps["legs"], hood, boots, coat or CHILD_COAT), _CHILD
    else:
        D, m = _sibling_design(sibling)
    if toy and pose in ("share", "tug", "stand", "walk_a", "walk_b", "sulk"):
        if pose in ("stand", "walk_a", "walk_b"):
            ps["arms"] = (ps["arms"][0], ("fk", 10, 30))
        D["front"] = _toy_front(D, toy, pose)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    if pose == "jump":
        inner = f'<g transform="translate(0,{-CHILD_JUMP})">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"child{'-' + sibling if sibling else ''}-{pose}")


# ======================================================================= Storm film (Mark 4:35-41)
# Jesus, his twelve disciples (Peter, Andrew, James and John are the four fishermen), the Galilean villagers on the
# lakeshore, disciples_group(), and child(outfit='pyjamas') with the night-time poses. Module doc section "STORM FILM".

EXPRS.update({
    "warm":            dict(eyes="dot", brow=(-0.03, 0.02, -0.05), mouth="smile", blush=True),
    "smile":           dict(eyes="arc", brow=(-0.06, 0.03, -0.05), mouth="smile", blush=True),
    "calm":            dict(eyes="down", brow=(-0.04, 0.03, 0.0), mouth="smile"),
    "gentle_question": dict(eyes="dot", brow=(-0.06, 0.02, -0.08), mouth="small_open", blush=True, look=(0.02, 0.0)),
    "command":         dict(eyes="dot", brow=(-0.03, 0.0, -0.06), mouth="call"),
    "panicked":        dict(eyes="fear", brow=(-0.14, 0.06, -0.10), mouth="shout", sweat=3, tremble=True),
    "awed":            dict(eyes="big", brow=(-0.10, 0.03, -0.14), mouth="small_o", look=(0.02, -0.04)),
})
STORM_EXPRESSIONS = ("warm", "smile", "calm", "gentle_question", "command", "panicked", "awed")

JESUS_SKIN = "#c88e66"
JESUS_HAIR = "#4a3122"
JESUS_ROBE = "#f0e6d0"
JESUS_TRIM = "#d9c59c"
JESUS_MANTLE = "#b24f47"
JESUS_SASH = "#c9a25e"
_JESUS_M = _metrics(_ADULT, 1.02, 1.0)


# ---------------------------------------------------------------- beards and headwear (head frame)
def _storm_beard(R, col, kind):
    """'jesus' a short neat rounded beard along the jaw; 'curly' Peter's full curly beard with grey streaks;
    'fisher' a short square fisherman's beard. All three get the default moustache (see _MOUSTACHED)."""
    if kind == "jesus":
        L = 1.13
        pts = [(-0.86 * R, -0.02 * R), (-0.90 * R, 0.52 * R), (-0.60 * R, (L - 0.20) * R), (-0.12 * R, (L - 0.02) * R),
               (0.16 * R, L * R), (0.50 * R, (L - 0.10) * R), (0.80 * R, 0.70 * R), (0.92 * R, 0.50 * R),
               (0.70 * R, 0.62 * R), (0.20 * R, 0.80 * R), (-0.30 * R, 0.70 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        lite = shade(col, 0.22)
        for x0, y0, x1, y1 in ((-0.62, 0.42, -0.50, 0.80), (-0.25, 0.86, -0.12, 1.02), (0.36, 0.86, 0.46, 0.98)):
            s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} Q{fmt((x0 + 0.08) * R)},{fmt((y0 + y1) / 2 * R)} "
                       f"{fmt(x1 * R)},{fmt(y1 * R)}", w=2.0, col=lite, extra='opacity="0.8"')
        return s
    if kind == "curly":
        circ = []
        for i in range(9):
            a = math.radians(178 - i * 21.5)
            rr = 0.98 * R
            cx, cy = 0.05 * R + rr * math.cos(a) * 0.95, 0.40 * R + rr * math.sin(a) * 0.82
            if cy < 0.05 * R:
                continue
            circ.append((cx, cy, (0.24 if i % 2 else 0.21) * R))
        circ += [(-0.78 * R, 0.10 * R, 0.17 * R), (0.86 * R, 0.42 * R, 0.15 * R), (0.12 * R, 1.25 * R, 0.2 * R)]
        s = _union_circles(circ, col, 2.8)
        s += f'<path d="{smooth_path([(-0.62 * R, 0.25 * R), (-0.30 * R, 0.72 * R), (0.20 * R, 0.84 * R), (0.70 * R, 0.66 * R), (0.55 * R, 0.95 * R), (-0.40 * R, 0.95 * R)])}" fill="{col}"/>'
        grey = mix(col, "#ece8e0", 0.72)
        for k, (x, y, r) in enumerate(circ):
            c_ = grey if k % 2 == 1 else shade(col, 0.25)
            s += _line(f"M{fmt(x - 0.45 * r)},{fmt(y + 0.1 * r)} Q{fmt(x - 0.15 * r)},{fmt(y - 0.6 * r)} {fmt(x + 0.4 * r)},"
                       f"{fmt(y - 0.2 * r)}", w=2.2, col=c_)
        return s
    if kind == "fisher":
        L = 1.06
        pts = [(-0.86 * R, 0.0), (-0.90 * R, 0.60 * R), (-0.66 * R, (L - 0.08) * R), (0.10 * R, L * R),
               (0.62 * R, (L - 0.06) * R), (0.86 * R, 0.62 * R), (0.70 * R, 0.66 * R), (0.20 * R, 0.82 * R),
               (-0.30 * R, 0.70 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts, tension=0.8)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.2)
        for x0 in (-0.55, -0.15, 0.30):
            s += _line(f"M{fmt(x0 * R)},{fmt(0.86 * R)} l{fmt(0.03 * R)},{fmt(0.13 * R)}", w=2.0, col=dark)
        return s
    return ""


def _jesus_hair(R):
    """Dark shoulder-length hair: a soft cap with a side part and a wave over the temple; the back hangs behind the
    head (D['long_hair'])."""
    col = JESUS_HAIR
    pts = [(0.93 * R, -0.36 * R), (0.84 * R, -0.84 * R), (0.32 * R, -1.13 * R), (-0.40 * R, -1.11 * R),
           (-0.98 * R, -0.74 * R), (-1.14 * R, -0.08 * R), (-1.13 * R, 0.58 * R), (-1.02 * R, 1.08 * R),
           (-0.80 * R, 1.16 * R), (-0.76 * R, 0.82 * R), (-0.62 * R, 0.46 * R), (-0.58 * R, -0.04 * R),
           (-0.36 * R, -0.40 * R), (0.10 * R, -0.52 * R), (0.52 * R, -0.46 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    lite = shade(col, 0.36)
    s += _line(f"M{fmt(0.20 * R)},{fmt(-1.08 * R)} Q{fmt(0.42 * R)},{fmt(-0.86 * R)} {fmt(0.62 * R)},{fmt(-0.50 * R)}",
               w=2.2, col=lite)
    for x0, y0, x1, y1 in ((-0.30, -0.96, -0.84, -0.30), (-0.62, -0.62, -0.98, 0.70), (0.02, -1.0, -0.40, -0.52),
                           (-0.86, -0.20, -1.02, 1.06)):
        s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} Q{fmt((x0 + x1) / 2 * R - 0.1 * R)},{fmt((y0 + y1) / 2 * R)} "
                   f"{fmt(x1 * R)},{fmt(y1 * R)}", w=2.0, col=lite, extra='opacity="0.85"')
    return s


def _fisher_cloth(R, col, wind=0.0):
    """A fisherman's kerchief: a cloth over the top of the head, tied in a knot at the back with two short tails
    (they stream back in the wind, wind 0..1)."""
    s = ""
    k0 = (-1.02 * R, -0.22 * R)
    for dy0, dx1, dy1 in ((0.0, -0.46, 0.36), (0.06, -0.30, 0.66)):
        a = math.radians(-14 + 70 * (1 - wind) - 8 * wind)
        L = (0.62 if dy0 == 0 else 0.70) * R
        e = (k0[0] - L * math.cos(a) * (1 if dy0 == 0 else 0.85), k0[1] + dy0 * R + L * math.sin(a))
        m = ((k0[0] + e[0]) / 2 + dx1 * 0.1 * R, (k0[1] + e[1]) / 2 - 0.05 * R * wind)
        s += _tube(_spline_pts([k0, m, e], steps=4), 0.15 * R, shade(col, -0.06), ow=2.4)
    pts = [(0.95 * R, -0.36 * R), (0.82 * R, -0.86 * R), (0.25 * R, -1.15 * R), (-0.45 * R, -1.08 * R),
           (-0.98 * R, -0.66 * R), (-1.12 * R, -0.12 * R), (-0.96 * R, 0.10 * R), (-0.64 * R, -0.18 * R),
           (-0.20 * R, -0.48 * R), (0.45 * R, -0.52 * R)]
    s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(-0.20 * R)},{fmt(-1.00 * R)} Q{fmt(-0.70 * R)},{fmt(-0.70 * R)} {fmt(-0.92 * R)},{fmt(-0.24 * R)}",
               w=2.2, col=shade(col, -0.22))
    s += _line(f"M{fmt(0.40 * R)},{fmt(-1.02 * R)} Q{fmt(0.10 * R)},{fmt(-0.80 * R)} {fmt(-0.10 * R)},{fmt(-0.56 * R)}",
               w=2.0, col=shade(col, -0.18), extra='opacity="0.8"')
    s += f'<circle cx="{fmt(k0[0])}" cy="{fmt(k0[1])}" r="{fmt(0.17 * R)}" fill="{shade(col, -0.04)}" {_st(2.6)}/>'
    return s


def _kerchief(col, wind=0.0, extra=None):
    def hat(R):
        return _fisher_cloth(R, col, wind) + (extra(R) if extra else "")
    return hat


# ---------------------------------------------------------------- worn things (body-frame hooks)
def _hem_stripes(col, gap=(14, 24, 34)):
    """Two thin woven stripes just above the hem (the disciples' fishermen's tunics)."""
    def deco(st, polys):
        s = ""
        Hm, um = st["Hm"], st["um"]
        for d0, d1 in ((gap[0], gap[0] + 5), (gap[1], gap[1] + 9)):
            for poly in polys[-1:]:
                s += _poly(_band(poly, Hm, um, -d1, -d0), col, sw=0)
        return s
    return deco


def _rolled_sleeves(col):
    """A rolled band where the short sleeve ends (fishermen roll their sleeves up)."""
    def deco(st, i, Sx, E, W):
        sl = 0.42
        mid = _lerp(Sx, E, min(1.0, sl * 2))
        dv = _nrm(_sub(E, Sx))
        nv = (-dv[1], dv[0])
        aw = st["m"]["aw"]
        a, b = _add(mid, _mul(nv, aw * 0.62)), _sub(mid, _mul(nv, aw * 0.62))
        return _tube([a, b], 7.5, col, ow=2.4)
    return deco


def _mantle_drape(col, wind=0.0, lying=False):
    """Behind the body: the mantle falling from the far shoulder down the back (streams out behind in the wind)."""
    def behind(st):
        m, tp = st["m"], st["tp"]
        if lying:
            return ""
        T, ww, shw = m["T"], m["ww"], m["shw"]
        top0, top1 = tp(-0.15 * ww, T + 4), tp(-1.05 * shw, T - 12)
        L = 0.62 * (m["th"] + m["sh"]) + 0.55 * T
        if st["mode"] == "feet" and not any(len(s_) for s_ in st["robe"][2:]):
            pass
        ang = 4 + 58 * wind                       # 0 hangs down the back, 1 streams back
        L *= 1 - 0.30 * wind
        d = _dv(-ang)
        base = _add(top1, _mul(d, L))
        if base[1] > st["ground"] - 14:            # never below the ground line
            L *= (st["ground"] - 14 - top1[1]) / max(1.0, base[1] - top1[1])
            base = _add(top1, _mul(d, L))
        side = _rot(d, 90)
        w0, w1 = 0.55 * shw, 0.95 * shw
        pts = [top0, top1, _add(_lerp(top1, base, 0.55), _mul(side, -0.10 * w1)), _add(base, _mul(side, -0.40 * w1)),
               _add(_add(base, _mul(side, 0.08 * w1)), _mul(d, -10 * wind)), _add(base, _mul(side, 0.55 * w1)),
               _add(_lerp(top0, base, 0.55), _mul(side, 0.45 * w1))]
        s = f'<path d="{smooth_path(pts, tension=0.75)}" fill="{shade(col, -0.10)}" {_st()}/>'
        for t in (0.35, 0.7):
            a, b = _lerp(top1, _add(base, _mul(side, -0.3 * w1)), t), _lerp(top0, _add(base, _mul(side, 0.45 * w1)), t)
            q = _lerp(a, b, 0.5)
            s += _line(f"M{_pt(_lerp(top1, q, 0.3))} Q{_pt(q)} {_pt(_add(q, _mul(d, 0.25 * L)))}", w=2.2,
                       col=shade(col, -0.28), extra='opacity="0.7"')
        return s
    return behind


def _mantle_band(col, trim):
    """Over the robe: the mantle crossing the chest from the far shoulder down to the near hip, covering the far
    shoulder (clipped to the body)."""
    def mid(st):
        m, tp, pel, f, u = st["m"], st["tp"], st["pel"], st["f"], st["u"]
        T, ww, shw = m["T"], m["ww"], m["shw"]
        A = tp(-0.95 * shw, T - 4)
        B = tp(0.95 * ww, -0.02 * T)
        dv = _nrm(_sub(B, A))
        n = (-dv[1], dv[0])
        c = _lerp(A, B, 0.5)
        s = ""
        polys = [st["robe"][0]]
        lim = ww + 3
        for poly in st["robe"][1:]:
            b = _band(poly, pel, u, -18, 400)
            if len(b) > 2:
                polys.append(b)
        for poly in polys:
            b = _band(poly, c, n, -26, 24)
            if len(b) > 2:
                b = _clip(b, _sub(pel, _mul(f, lim)), f)
            if len(b) > 2:
                b = _clip(b, _add(pel, _mul(f, lim + 4)), _mul(f, -1))
            if len(b) > 2:
                s += _poly(b, col, sw=3.0)
                for off in (-17,):
                    s += _poly(_band(b, c, n, off - 2.5, off + 2.5), trim, sw=0, extra='opacity="0.9"')
        s += _line(f"M{_pt(_add(c, _mul(n, -8)))} Q{_pt(_add(_lerp(A, B, 0.75), _mul(n, -2)))} {_pt(_add(B, _mul(n, -6)))}",
                   w=2.2, col=shade(col, -0.25), extra='opacity="0.7"')
        return s
    return mid


def _blanket(col, trim):
    """Lying down: the mantle drawn over the legs like a blanket (sleep / wake)."""
    def front(st):
        legs = st["legs"]
        pts = []
        for (H, K, A, a1, a2) in legs:
            pts += [H, K, _lerp(K, A, 0.85)]
        pts.append(st["tp"](0.2 * st["m"]["ww"], 0.32 * st["m"]["T"]))
        pts.append(st["tp"](-0.9 * st["m"]["ww"], 0.32 * st["m"]["T"]))
        hull = _hull(pts)
        floor = st["ground"] - OW
        hull = [(x, min(y, floor)) for x, y in hull]
        poly = _rounded(_hull(hull), 18)
        poly = [(x, min(y + 6, floor)) for x, y in poly]
        s = _poly(poly, col, sw=OW)
        ys = [p[1] for p in poly]
        top = min(ys)
        xs = sorted(p[0] for p in poly)
        x0, x1 = xs[0], xs[-1]
        cid = _clip_id("blanket", _d(poly))
        inner = ""
        for k in range(1, 4):
            xx = x0 + (x1 - x0) * k / 4
            inner += _line(f"M{fmt(xx - 10)},{fmt(top)} Q{fmt(xx + 8)},{fmt((top + floor) / 2)} {fmt(xx - 4)},{fmt(floor)}",
                           w=2.4, col=shade(col, -0.22), extra='opacity="0.7"')
        inner += _line(f"M{fmt(x0)},{fmt(floor - 10)} L{fmt(x1)},{fmt(floor - 10)}", w=6, col=trim, extra='opacity="0.9"')
        s += f'<clipPath id="{cid}"><path d="{_d(poly)}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'
        s += _poly(poly, "none", sw=OW)
        return s
    return front


def _soft_glow(level, kind="stand"):
    """A very soft warm light round the whole figure (calm presence; never a halo ring)."""
    def behind(st):
        if level <= 0:
            return ""
        xs = [p[0] for p in st["ext"]]
        ys = [p[1] for p in st["ext"]]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        rx = (max(xs) - min(xs)) * 0.95 + 120
        ry = (max(ys) - min(ys)) * 0.75 + 120
        gid = _clip_id("jglow", round(level, 3), round(cx), round(cy), round(rx), round(ry))
        return (f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">'
                f'<stop offset="0" stop-color="{P["glow"]}" stop-opacity="0.95"/>'
                f'<stop offset="0.45" stop-color="{P["gold"]}" stop-opacity="0.38"/>'
                f'<stop offset="1" stop-color="{P["gold"]}" stop-opacity="0"/></radialGradient></defs>'
                f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="url(#{gid})" '
                f'opacity="{min(1.0, level):.2f}"/>')
    return behind





# ---------------------------------------------------------------- Jesus
JESUS_POSES = ("stand", "walk_a", "walk_b", "sit", "teach", "teach_stand", "sleep", "wake", "stand_command",
               "turn_kind", "bless", "wave", "point", "pray")
_SEAT = dict(lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8)
_JZ = {
    "stand": _P(arms=(("fk", 12, 6), ("fk", -8, -3)), expr="warm"),
    "walk_a": _P(t=3, legs=((24, 8), (-20, -34)), arms=(("fk", -30, -22), ("fk", 22, 36)), expr="warm"),
    "walk_b": _P(t=3, legs=((-20, -34), (24, 8)), arms=(("fk", 26, 40), ("fk", -20, -12)), expr="warm"),
    "sit": _P(t=-2, arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), expr="warm", **_SEAT),
    "teach": _P(t=-2, h=-4, arms=(("ik", "knee", 0, 0.25, 1), ("fk", 56, 122)), hands=("fist", "open"), expr="smile",
                **_SEAT),
    "teach_stand": _P(h=-3, arms=(("fk", 12, 6), ("fk", 34, 96)), hands=("fist", "open"), expr="smile"),
    "sleep": _P(t=-72, h=-6, ground="body", flat_back=True, legs=(("ik", 40, 1), ("ik", 58, 1)),
                arms=(("ik", "pillow", 1.05, 0, 1), ("ik", "pillow", 0.10, 0, 1)), hands=("open", "none"),
                far_front=True, near_hidden=True, tail=(-40, -92), expr="sleepy", marks=("zzz",), hem=0.97, flare=-6),
    "wake": _P(t=-38, h=-14, ground="body", flat_back=True, legs=(("ik", 92, 1), ("ik", 108, 1)),
               arms=(("ik", "ground", -10, 0, -1), ("fk", 36, 70)), hands=("ground", "open"), far_front=False,
               expr="calm", hem=0.97, flare=-6, look=(0.03, -0.03)),
    "stand_command": _P(t=-3, h=-10, legs=((11, 3), (-10, -4)), arms=(("fk", 122, 146), ("fk", -26, -16)),
                        hands=("palm", "open"), expr="command", look=(0.03, -0.05)),
    "turn_kind": _P(t=2, h=8, legs=((8, 3), (-7, -3)), arms=(("fk", 22, 70), ("fk", 30, 82)), hands=("open", "open"),
                    expr="gentle_question"),
    "bless": _P(h=-4, arms=(("fk", 12, 6), ("fk", 80, 138)), hands=("fist", "palm"), expr="kind"),
    "point": _P(h=-6, legs=((6, 2), (-5, -2)), arms=(("fk", 12, 6), ("fk", 96, 100)), hands=("fist", "point"),
                expr="warm", look=(0.03, -0.03)),
    "pray": _P(h=-12, arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)), hands=("none", "pray"),
               expr="peaceful", look=(0.02, -0.05)),
}
JESUS_EXPRESSIONS = ("warm", "kind", "smile", "calm", "sleepy", "gentle_question", "command", "peaceful", "happy")
JESUS_CUSHION_DX = -150        # sleep / wake: the cushion centre is this far from the anchor (toward the head side)


def _jesus_pose(pose, phase):
    if pose == "wave":
        f = 166 + 16 * math.sin(2 * math.pi * phase)
        return _P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 146, f), ("fk", -8, -3)), hands=("open", "fist"),
                  expr="smile")
    return dict(_JZ[pose])


def _wave_marks(st):
    W = st["arms"][0][2]
    s_ = ""
    for k in (0, 1):
        r = 26 + 14 * k
        s_ += _line(f"M{fmt(W[0] + r)},{fmt(W[1] - r * 0.6)} Q{fmt(W[0] + r * 1.15)},{fmt(W[1])} {fmt(W[0] + r)},"
                    f"{fmt(W[1] + r * 0.6)}", w=2.8, col=MARK)
    return s_


def _jesus_design(pose, glow, cushion, wind, mantle):
    lying = pose in ("sleep", "wake")
    D = dict(robe=JESUS_ROBE, sleeve=JESUS_ROBE, hem_col=JESUS_TRIM, hem_w=10, cuff=JESUS_TRIM, skin=JESUS_SKIN,
             leg=JESUS_SKIN, hem=0.93, flare_k=1.0, hair=None, hat=("custom", _jesus_hair), hat_h=0.14,
             beard=("jesus", JESUS_HAIR), ears=False, sash=JESUS_SASH, sash_tail=True,
             neck_v=shade(JESUS_ROBE, -0.12), sandal=SANDAL)
    behind = [_soft_glow(glow)] if glow > 0 else []
    mids, fronts = [], []
    if mantle and not lying:
        behind.append(_mantle_drape(JESUS_MANTLE, wind))
        mids.append(_mantle_band(JESUS_MANTLE, shade(JESUS_MANTLE, 0.30)))
    if lying and mantle:
        fronts.append(_blanket(JESUS_MANTLE, shade(JESUS_MANTLE, 0.30)))
    if pose == "wave":
        fronts.append(_wave_marks)
    D["behind"] = _hooks(*[b for b in behind if b])
    D["mid"] = _hooks(*mids)
    D["front"] = _hooks(*fronts)
    return D


def jesus(x, y, scale=1.0, facing=1, pose="stand", expr=None, glow=0.0, cushion=True, wind=0.0, phase=0.0,
          mantle=True, marks=True):
    """Jesus: a kind, calm man of about thirty (see module doc, 'STORM FILM')."""
    _check_js(pose, JESUS_POSES + ("walk",), "jesus")
    _check_js_expr(expr, "jesus")
    pose = "walk_a" if pose == "walk" else pose
    ps = _jesus_pose(pose, phase)
    D = _jesus_design(pose, _clamp01(glow), cushion, _clamp01(wind), mantle)
    e = expr or ps["expr"]
    inner, bbox = _figure(D, _JESUS_M, ps, e, _fsign(facing), marks)
    if pose in ("sleep", "wake") and cushion:
        inner = f'<g transform="translate({JESUS_CUSHION_DX},0)">{_prp()._boat_cushion()}</g>' + inner
    return _wrap_out(inner, x, y, scale, facing, f"jesus-{pose}")


# ---------------------------------------------------------------- the twelve disciples
DISCIPLE_NAMES = ("Peter", "Andrew", "James", "John", "Philip", "Bartholomew", "Matthew", "Thomas",
                  "James son of Alphaeus", "Thaddaeus", "Simon", "Judas")
DISCIPLE_LOOKS = {"peter": 0, "andrew": 1, "james": 2, "john": 3}
_DISCIPLES = [
    # Peter: sturdy fisherman, grey-streaked curly hair and beard, slate-teal tunic, rust kerchief
    dict(tunic="#3f7282", stripe="#e6c27a", belt="#c0623f", skin="#cf9570", hair="#4a3428", style="curly",
         beard=("curly", "#5e4636"), hat=("kerchief", "#c0623f"), k=1.03, wide=1.18),
    # Andrew: Peter's brother (same skin and hair), short square beard, honey-sand tunic, teal kerchief
    dict(tunic="#c9a86a", stripe="#3f7282", belt="#3f7282", skin="#cf9570", hair="#4a3428", style="curly",
         beard=("fisher", "#4a3428"), hat=("kerchief", "#4f9a94"), k=1.0, wide=1.02),
    # James son of Zebedee: tall, full dark beard, wine tunic, cream kerchief
    dict(tunic="#8b4a5c", stripe="#efe0c0", belt="#e0b25a", skin="#d9a37a", hair="#2a1f1a", style="short",
         beard=("full", "#2a1f1a"), hat=("kerchief", "#ece0c4"), k=1.05, wide=1.0),
    # John: the youngest, beardless, light-brown curls, sage tunic, a thin ochre headband
    dict(tunic="#77a063", stripe="#f0e4c4", belt="#d9a03c", skin="#ebb894", hair="#8a5530", style="curly",
         beard=None, hat=("band", "#d9a03c"), k=0.97, wide=0.94, curls=True),
    dict(tunic="#c4877e", stripe="#f0dcc0", belt="#7a5a8a", skin="#c68a62", hair="#241b17", style="short",
         beard=("short", "#241b17"), hat=("wrap", "#e0b25a", "#a8743c"), k=1.0, wide=1.0),
    dict(tunic="#5f7fa6", stripe="#e8d6aa", belt="#c0623f", skin="#e2a77e", hair="#5a3a24", style="curly",
         beard=("full", "#5a3a24"), hat=("headband", "#c0623f"), k=1.01, wide=1.06),
    dict(tunic="#8f78ad", stripe="#e8c25a", belt="#e8c25a", skin="#dca57c", hair="#3a2a22", style="short",
         beard=("trim", "#3a2a22"), hat=("kerchief", "#efe2c4"), k=0.99, wide=0.98),
    dict(tunic="#7b8a48", stripe="#efe0c0", belt="#a8743c", skin="#9a6342", hair="#1f1915", style="curly",
         beard=("stubble", "#1f1915"), hat=None, k=1.0, wide=1.0),
    dict(tunic="#cdb07f", stripe="#8a5a3a", belt="#8a5a3a", skin="#d39a72", hair="#2a201b", style="short",
         beard=("pointed", "#2a201b"), hat=("wrap", "#4f9a94", "#3b7d7b"), k=1.02, wide=0.98),
    dict(tunic="#9c5a3c", stripe="#f0d890", belt="#d9a03c", skin="#c98f68", hair="#3a2618", style="curly",
         beard=("short", "#3a2618"), hat=("headband", "#d9a03c"), k=0.99, wide=1.04),
    dict(tunic="#6c7a86", stripe="#e6d6b2", belt="#b5553a", skin="#e2a882", hair="#241b17", style="short",
         beard=("full", "#241b17"), hat=("kerchief", "#a8bb8a"), k=1.03, wide=1.06),
    dict(tunic="#b8923a", stripe="#7a3a3a", belt="#7a3a3a", skin="#c68a62", hair="#2f2420", style="curly",
         beard=("short", "#2f2420"), hat=("wrap", "#8a3c4a", "#6a2c3a"), k=1.0, wide=1.0),
]
DISCIPLE_POSES = ("stand", "walk_a", "walk_b", "sit", "row", "pull_rope", "bail", "cling", "scared", "shout",
                  "wake_shake", "wake_shake_low", "wonder", "whisper", "kneel", "wave", "point", "push", "cast_net",
                  "haul_net")
DISCIPLE_EXPRESSIONS = ("happy", "tired", "scared", "panicked", "amazed", "ashamed", "awed", "worried", "shout",
                        "determined", "kind")
BAIL_ITEMS = ("bucket", "bowl")


def _disciple_index(variant):
    if isinstance(variant, str):
        v = DISCIPLE_LOOKS.get(variant.lower())
        if v is None:
            raise ValueError(f"disciples: unknown variant {variant!r}; use 0-11 or one of {tuple(DISCIPLE_LOOKS)}")
        return v
    return int(variant) % 12


def _john_curls(R):
    return _joseph_curls(R, "#8a5530")


def _disciple_design(v, wind=0.0, wet=False):
    d = _DISCIPLES[v]
    tunic = d["tunic"]
    if wet:
        tunic = shade(tunic, -0.16)
    D = dict(robe=tunic, sleeve=tunic, hem_col=shade(tunic, -0.22), hem_w=8, skin=d["skin"], leg=d["skin"], hem=0.60,
             flare_k=0.85, sleeve_len=0.42, sash=d["belt"], sash_tail=True, hair=d["hair"], hair_style=d["style"],
             beard=d["beard"], neck_v=shade(tunic, 0.25), bare=True, robe_deco=_hem_stripes(d["stripe"]),
             arm_deco=_rolled_sleeves(shade(tunic, 0.12)), wet=wet)
    hat = d.get("hat")
    if hat:
        if hat[0] == "kerchief":
            col = shade(hat[1], -0.18) if wet else hat[1]
            D.update(hat=("custom", _kerchief(col, wind)), hat_h=0.16, ears=False)
        elif hat[0] == "band":
            D.update(hat=("custom", lambda R: _john_curls(R) + _headband(R, d["hat"][1], tails=True)), hat_h=0.12,
                     hair=d["hair"])
        else:
            D["hat"] = hat
    elif d.get("curls"):
        D.update(hat=("custom", _john_curls), hat_h=0.12)
    return D, _metrics(_ADULT, d["k"], d["wide"])


# ---- rowing / bailing / net poses (anchor coordinates at scale 1, facing 1)
def _row_pose(phase):
    PR = _prp()
    hx, hy = PR.row_hands(phase)
    a = 2 * math.pi * phase
    return _P(t=2 + 12 * math.cos(a), h=-4 - 6 * math.cos(a), lap=True, legs=((80, 18), (76, 14)), hem=0.97, flare=-8,
              arms=(("ik", "abs", hx + 6, hy - 4, 1), ("ik", "abs", hx, hy, 1)), hands=("fist", "fist"), expr="happy")


def _bail_keys(phase):
    """(t, drop, far hand, near hand, tip) for the bail cycle: 0 scoop low, .35 lift, .65 throw over the side."""
    keys = [(0.0, (38, 30, (96, -70), (78, -64), 0.0)),
            (0.35, (6, 6, (70, -190), (54, -178), 0.05)),
            (0.65, (-6, 0, (132, -262), (116, -250), 1.0)),
            (1.0, (38, 30, (96, -70), (78, -64), 0.0))]
    p = phase % 1.0
    for (p0, k0), (p1, k1) in zip(keys, keys[1:]):
        if p0 <= p <= p1:
            t = (p - p0) / (p1 - p0)
            t = t * t * (3 - 2 * t)
            return tuple(_lerp(a, b, t) if isinstance(a, tuple) else a + (b - a) * t for a, b in zip(k0, k1))
    return keys[0][1]


def _bail_pose(phase):
    t, drop, Wf, Wn, tip = _bail_keys(phase)
    return _P(t=t, h=-6 if t < 20 else 4, drop=drop, legs=(("ik", 34, 1), ("ik", -30, 1)),
              arms=(("ik", "abs", Wf[0], Wf[1], 1), ("ik", "abs", Wn[0], Wn[1], 1)), hands=("fist", "fist"),
              expr="worried"), tip


def _cast_pose(phase):
    """Casting a round net: 0 wind-up (leaning back, the gathered net swung behind), .5 the swing (net at the hip),
    1 release (arms flung forward-up, the net flying open ahead)."""
    p = _clamp01(phase)
    e = p * p * (3 - 2 * p)
    t = -12 + 30 * e
    fa = -62 + 172 * e            # far arm swings from low behind to forward-up
    na = -48 + 150 * e
    return _P(t=t, h=-8 + 4 * e, legs=((22, 6), (-20, -12)), arms=(("fk", fa, fa + 16), ("fk", na, na + 22)),
              hands=("fist", "open" if p > 0.85 else "fist"), expr="happy", look=(0.03, -0.03))


def _haul_pose(phase):
    """Hauling a heavy full net hand over hand (phase 0..1 alternates the hands)."""
    a = math.sin(2 * math.pi * phase)
    return _P(t=-18, drop=16, legs=(("ik", 64, 0), ("ik", -22, 1)),
              arms=(("ik", "abs", 96 + 14 * a, -150 - 22 * a, 1), ("ik", "abs", 84 - 14 * a, -128 + 22 * a, 1)),
              hands=("fist", "fist"), expr="laugh")


_DS = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3)), expr="happy"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -40, -30), ("fk", 26, 42)), expr="happy"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 44), ("fk", -24, -14)), expr="happy"),
    "sit": _P(t=-2, arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), expr="happy", **_SEAT),
    "pull_rope": _P(t=-16, drop=12, legs=(("ik", 52, 0), ("ik", -22, 1)),
                    arms=(("ik", "abs", 76, -306, 1), ("ik", "abs", 58, -246, 1)), expr="worried", look=(0.03, -0.06),
                    h=-10),
    "cling": _P(t=14, h=-4, drop=22, legs=(("ik", 36, 1), ("ik", -26, 1)),
                arms=(("ik", "abs", 84, -262, 1), ("ik", "abs", 80, -206, 1)), hands=("fist", "fist"), expr="scared"),
    "scared": _P(t=-4, legs=((10, 2), (-8, -4)),
                 arms=(("ik", "headw", 1.15, 0.45, 1), ("ik", "headw", -1.15, 0.45, -1)), hands=("open", "open"),
                 expr="scared"),
    "shout": _P(t=6, h=-8, legs=((10, 3), (-8, -3)), arms=(("fk", 112, 134), ("ik", "head", 1.02, 0.52, 1)),
                hands=("open", "open"), expr="shout"),
    "wake_shake": _P(t=18, h=-2, legs=(("ik", 30, 1), ("ik", -24, 1)), drop=8,
                     arms=(("ik", "abs", 122, -246, 1), ("ik", "abs", 100, -232, 1)), hands=("open", "open"),
                     expr="panicked", look=(0.04, 0.03)),
    "wake_shake_low": _P(t=40, h=-12, drop=40, legs=(("ik", 56, 1), ("ik", -26, 1)),
                         arms=(("ik", "abs", 150, -82, 1), ("ik", "abs", 112, -104, 1)), hands=("open", "open"),
                         expr="panicked"),
    "wonder": _P(h=-8, legs=((8, 3), (-7, -3)), arms=(("fk", 40, 118), ("fk", -36, -112)), hands=("open", "open"),
                 expr="amazed", look=(0.02, -0.04)),
    "whisper": dict(POSES["whisper"], expr="awed"),
    "kneel": _P(t=-2, h=-14, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)),
                hands=("none", "pray"), expr="awed", look=(0.02, -0.06), **_KNEEL),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 14, 8), ("fk", 88, 92)), hands=("fist", "point"),
                expr="happy"),
    "push": _P(t=28, drop=24, legs=(("ik", 52, 1), ("ik", -56, 0)), arms=(("fk", 84, 90), ("fk", 78, 86)),
               hands=("palm", "palm"), expr="happy"),
}


def _disciple_pose(pose, phase):
    if pose == "row":
        return _row_pose(phase), None
    if pose == "bail":
        ps, tip = _bail_pose(phase)
        return ps, tip
    if pose == "cast_net":
        return _cast_pose(phase), None
    if pose == "haul_net":
        return _haul_pose(phase), None
    if pose == "wave":
        f = 168 + 18 * math.sin(2 * math.pi * phase)
        return _P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 146, f), ("fk", -8, -3)), hands=("open", "fist"),
                  expr="happy"), None
    return dict(_DS[pose]), None


def _oar_front(D, phase):
    def front(st):
        PR = _prp()
        G = st["ground"]
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        s = PR._oar_svg(phase, (0.0, G))
        return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    return front


def _bail_front(D, phase, item, tip, marks):
    def front(st):
        PR = _prp()
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        c = ((W0[0] + W1[0]) / 2 + 8, (W0[1] + W1[1]) / 2 + 10)
        full = 0.0 if phase % 1.0 < 0.08 else (1.0 if phase % 1.0 < 0.62 else max(0.0, 1 - (phase % 1.0 - 0.62) * 4))
        s = PR._bail_vessel(item, water=full, tip=tip, splash=marks and 0.6 < phase % 1.0 < 0.9)
        s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate({fmt(-70 * tip)})">{s}</g>'
        return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    return front


def _rope_front(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        dv = _nrm(_sub(W0, W1))
        top = _add(W0, _mul(dv, 230))
        tail = [W1, _add(W1, (-14, 40)), _add(W1, (-30, 90)), _add(W1, (-22, 150))]
        s = _tube(_spline_pts(tail, steps=4), 6, _prp().ROPE, ow=2.2)
        s += _tube([_add(W1, _mul(dv, -4)), top], 6, _prp().ROPE, ow=2.2)
        return s + _fist(W1, hr, D["skin"]) + _fist(W0, hr, D["skin"])
    return front


def _cling_front(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        return _fist(W1, hr, D["skin"]) + _fist(W0, hr, D["skin"])
    return front


def _net_cast_front(D, phase):
    def front(st):
        PR = _prp()
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        p = _clamp01(phase)
        if p < 0.85:            # the gathered net hanging from the hands, swinging with the arms
            c = (W0[0], W0[1] + 4)
            s = (f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate({fmt(40 - 70 * p)}) scale(0.9)">'
                 f'{PR._net_bundle()}</g>')
            return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
        k = (p - 0.85) / 0.15
        c = (W0[0] + 150 + 110 * k, W0[1] - 70 + 30 * k)
        s = _tube([W1, _lerp(W1, c, 0.5), c], 3.0, PR.ROPE, ow=1.8)
        s += f'<g transform="translate({fmt(c[0])},{fmt(c[1])})">{PR._net_fly(0.45 + 0.55 * k)}</g>'
        return s
    return front


def _net_haul_front(D, phase):
    def front(st):
        PR = _prp()
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        G = st["ground"]
        end = (190, G - 60)
        s = ""
        for W in (W0, W1):
            s += _tube([W, _lerp(W, end, 0.5), end], 5, PR.ROPE, ow=2.0)
        s += f'<g transform="translate({fmt(end[0] + 20)},{fmt(end[1] - 10)}) scale(0.75)">{PR._net_full(phase)}</g>'
        return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    return front


def _shake_marks(st, phase):
    s = ""
    for (Sx, E, W) in st["arms"][:1]:
        for k in (0, 1):
            r = 18 + 12 * k
            c = (W[0] + 6, W[1] - 4)
            s += _line(f"M{fmt(c[0] - r)},{fmt(c[1] - r * 0.9)} Q{fmt(c[0])},{fmt(c[1] - r * 1.3)} {fmt(c[0] + r)},"
                       f"{fmt(c[1] - r * 0.9)}", w=2.8, col=MARK, extra='opacity="0.85"')
    return s


def disciples(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, phase=0.0, shake=0.0, item="bucket",
              wind=0.0, wet=False, oar=True, net=True, marks=True):
    """One of the twelve disciples (variant 0-11 or 'peter' / 'andrew' / 'james' / 'john'), see module doc."""
    _check_js(pose, DISCIPLE_POSES + ("walk",), "disciples")
    _check_js_expr(expr, "disciples")
    if item not in BAIL_ITEMS:
        raise ValueError(f"disciples: unknown item {item!r}; choose from {BAIL_ITEMS}")
    pose = "walk_a" if pose == "walk" else pose
    v = _disciple_index(variant)
    D, m = _disciple_design(v, _clamp01(wind), wet)
    ps, tip = _disciple_pose(pose, phase)
    fronts = []
    if pose == "row" and oar:
        fronts.append(_oar_front(D, phase))
    elif pose == "bail":
        fronts.append(_bail_front(D, phase, item, tip, marks))
    elif pose == "pull_rope":
        fronts.append(_rope_front(D))
    elif pose == "cling":
        fronts.append(_cling_front(D))
    elif pose == "cast_net" and net:
        fronts.append(_net_cast_front(D, phase))
    elif pose == "haul_net" and net:
        fronts.append(_net_haul_front(D, phase))
    elif pose == "wave" and marks:
        fronts.append(_wave_marks)
    if pose in ("wake_shake", "wake_shake_low") and marks:
        fronts.append(lambda st: _shake_marks(st, phase))
    if pose in ("scared", "cling") and marks and shake:
        fronts.append(lambda st: _tremble_lines(st, shake))
    D["front"] = _hooks(*fronts)
    if v == 3 and ps["expr"] in ("happy",):
        ps["expr"] = "happy"
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    jit = shake if pose in ("scared", "cling") else (phase if pose in ("wake_shake", "wake_shake_low") else 0.0)
    if jit:
        inner = f'<g transform="translate({fmt(3.5 * math.sin(2 * math.pi * jit))},0)">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"disciple{v}-{pose}")


disciple = disciples

# (variant, dx, dy, facing): back row (higher, 0.96 x) first, then the front row - every face shows
_DG = [(5, -330, -34, 1), (9, -165, -34, 1), (8, 0, -36, 1), (10, 165, -34, -1), (11, 330, -34, -1), (4, 480, -30, -1),
       (6, -480, 0, 1), (7, -320, 0, 1), (1, -160, 0, 1), (0, 0, 2, 1), (2, 160, 0, -1), (3, 320, 0, -1)]
DISCIPLES_GROUP_POSES = ("stand", "wonder", "whisper", "scared", "kneel", "wave", "walk_a", "walk_b", "point", "shout",
                         "sit")


def disciples_group(x, y, scale=1.0, facing=1, pose="stand", n=12, expr=None, gap=150, exprs=None, poses=None,
                    phase=0.0, marks=True):
    """Several disciples at once (see module doc): a two-row group, or a line for the walk poses."""
    _check_js(pose, DISCIPLES_GROUP_POSES, "disciples_group")
    sx = 1 if facing >= 0 else -1
    n = max(1, min(12, int(n)))
    out = ""
    if pose.startswith("walk"):
        other = {"walk_a": "walk_b", "walk_b": "walk_a"}[pose]
        for i in reversed(range(n)):
            p_ = pose if i % 2 == 0 else other
            e = exprs[i % len(exprs)] if exprs else expr
            out += disciples(x - sx * i * gap * scale, y, scale, facing, variant=i, pose=p_, expr=e, marks=marks)
        return f'<g data-who="disciples_group-{pose}">{out}</g>'
    members = sorted(_DG, key=lambda g_: (g_[2] > -10, g_[1]))
    members = [g_ for g_ in members if g_[0] < n]
    for i, (v, dx, dy, f) in enumerate(members):
        p_ = poses[v % len(poses)] if poses else pose
        if pose == "whisper":
            p_ = "whisper" if (f > 0) == (v % 2 == 0) else "wonder"
        e = exprs[v % len(exprs)] if exprs else expr
        k = 0.96 if dy < 0 else 1.0
        out += disciples(x + sx * dx * scale, y + dy * scale, scale * k, f * sx, variant=v, pose=p_, expr=e,
                         phase=(phase + 0.13 * v) % 1.0, marks=marks)
    return f'<g data-who="disciples_group-{pose}">{out}</g>'


# ---------------------------------------------------------------- Galilean villagers (the lakeshore crowd)
VILLAGER_KINDS = ("man", "woman", "child", "elder")
VILLAGER_POSES = ("stand", "walk_a", "walk_b", "listen", "sit", "sit_listen", "kneel", "wave", "cheer", "point",
                  "shoulders", "carry", "carry_walk_a", "carry_walk_b", "nod")
_VL = [
    dict(robe="#8f6a9c", trim="#f0d890", skin="#d9a37a", hair="#2f2420", cloth="#efe2c4", veil="#e9d3a8"),
    dict(robe="#4f8a8a", trim="#e6c27a", skin="#c68a62", hair="#241b17", cloth="#d9a03c", veil="#e9b8a8"),
    dict(robe="#c4a25e", trim="#5a6f9a", skin="#e2a882", hair="#4a2f1f", cloth="#e8dcc0", veil="#a8c4d8"),
    dict(robe="#7a8f5a", trim="#e9d6aa", skin="#a46b47", hair="#1f1915", cloth="#b5553a", veil="#f0e0b8"),
    dict(robe="#b5605a", trim="#f0e4c4", skin="#dca57c", hair="#3a2618", cloth="#5f8aa8", veil="#c9b0d9"),
    dict(robe="#5f6f98", trim="#f0d890", skin="#cf9570", hair="#2a201b", cloth="#e0b25a", veil="#f2c4a0"),
]


def _villager_design(kind, variant):
    c = _VL[int(variant) % 6]
    robe = c["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.2), hem_w=9, cuff=shade(robe, -0.2), skin=c["skin"],
             leg=c["skin"], hem=0.92, flare_k=1.0, hair=c["hair"], hair_style="curly",
             robe_deco=_hem_stripes(c["trim"], gap=(16, 26, 36)), sandal=SANDAL)
    m = _ADULT
    if kind == "man":
        D.update(beard=(("full", "short", "fisher", "stubble", "trim", "jesus")[int(variant) % 6], c["hair"]),
                 sash=c["trim"], sash_tail=True)
        if int(variant) % 3 != 2:
            D.update(hat=("headcloth", c["cloth"], shade(c["cloth"], -0.3)), tail=(c["cloth"], shade(c["cloth"], -0.3)),
                     ears=False)
        m = _metrics(_ADULT, 1.0 + 0.015 * (int(variant) % 3 - 1), 1.0 + 0.04 * (int(variant) % 2))
    elif kind == "woman":
        veil = c["veil"]
        D.update(hat=("veil", veil, shade(veil, -0.25)), veil=veil, ears=False, sash=c["trim"], sash_tail=True,
                 hair_style="short")
        m = _metrics(_ADULT, 0.95, 0.92)
    elif kind == "child":
        girl = int(variant) % 2 == 1
        D.update(hem=0.58, flare_k=0.9, sleeve_len=0.55, rope_belt=c["trim"], hair_style="short" if girl else "curly",
                 robe_deco=_hem_stripes(c["trim"], gap=(10, 18, 26)))
        if girl:
            D.update(ponytail=c["hair"], ribbon=c["cloth"])
        m = _CHILD
    else:                       # elder
        D.update(hair="#e4ddd0", beard=("white", "#ece6da"), shawl=c["trim"], shawl_trim=shade(c["trim"], -0.25),
                 brow_w=4.6, brow_col="#9a9088")
        if int(variant) % 2:
            D.update(hat=("wrap", c["cloth"], shade(c["cloth"], -0.25)))
        m = _metrics(_ADULT, 0.97, 1.0)
    return D, m


_VG = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3)), expr="happy"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -40, -30), ("fk", 26, 42)), expr="happy"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 44), ("fk", -24, -14)), expr="happy"),
    "listen": _P(h=-8, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), expr="kind", look=(0.03, -0.04)),
    "sit": _P(t=-3, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)),
              expr="happy", **_SEATED),
    "sit_listen": _P(t=4, h=-10, legs=(("ik", 76, 1), ("ik", 86, 1)),
                     arms=(("ik", "knee", 0, 0.20, 1), ("ik", "head", 0.32, 1.02, 1)), expr="kind",
                     look=(0.03, -0.05), **_SEATED),
    "kneel": _P(t=-2, h=-12, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)),
                hands=("none", "pray"), expr="kind", look=(0.02, -0.05), **_KNEEL),
    "cheer": dict(POSES["cheer"]),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 14, 8), ("fk", 88, 92)), hands=("fist", "point"),
                expr="happy"),
    "shoulders": _P(h=-4, arms=(("fk", 12, 8), ("ik", "headw", -1.02, -0.90, -1)),
                    hands=("fist", "fist"), expr="happy", look=(0.02, -0.03)),
    "nod": _P(h=22, arms=(("fk", 14, 8), ("fk", -8, -3)), expr="kind"),
}


def _villager_pose(pose, phase, kind):
    if pose == "wave":
        f = 168 + 18 * math.sin(2 * math.pi * phase)
        return _P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 146, f), ("fk", -8, -3)), hands=("open", "fist"),
                  expr="happy")
    if pose == "carry":
        return _nh_carry_pose("basket")
    if pose in ("carry_walk_a", "carry_walk_b"):
        return _nh_carry_pose("basket", pose[-1])
    return dict(_VG[pose])


def _rider_child(variant):
    """The little child riding on the father's shoulders: drawn BEHIND the father, the seat hidden behind his head,
    so the child's body and waving arm rise above it (the father's raised hands hold its legs)."""
    def behind(st):
        Hc, R = st["Hc"], st["m"]["R"]
        D, m = _villager_design("child", variant)
        ps = _P(t=-2, h=-6, lap=True, legs=((62, 4), (56, -2)), hem=0.97, flare=-8,
                arms=(("fk", 150, 170), ("fk", 40, 70)), hands=("open", "fist"), expr="laugh")
        saved = dict(_LAST)
        inner, bb = _figure(D, _metrics(_CHILD, 0.86, 1.0), ps, "laugh", 1, True)
        pel = _LAST["pelvis"]
        _LAST.clear()
        _LAST.update(saved)
        tx, ty = Hc[0] - pel[0] - 0.25 * R, Hc[1] + 0.15 * R - pel[1]
        return f'<g transform="translate({fmt(tx)},{fmt(ty)})">{inner}</g>'
    return behind


def villager(x, y, scale=1.0, facing=1, kind="man", variant=0, pose="stand", expr=None, phase=0.0, rider=None,
             marks=True):
    """Galilean villagers on the lakeshore: men, women, children and elders (see module doc, 'STORM FILM')."""
    if kind not in VILLAGER_KINDS:
        raise ValueError(f"villager: unknown kind {kind!r}; choose from {VILLAGER_KINDS}")
    _check_js(pose, VILLAGER_POSES + ("walk",), "villager")
    _check_js_expr(expr, "villager")
    pose = "walk_a" if pose == "walk" else pose
    if pose == "shoulders" and kind not in ("man",):
        raise ValueError("villager: pose 'shoulders' is for kind='man' (a father with a child on his shoulders)")
    D, m = _villager_design(kind, variant)
    ps = _villager_pose(pose, phase, kind)
    fronts = []
    if pose.startswith("carry"):
        b, mi, fr = _carry_hooks(D, "carry", "basket")
        fronts.append(fr)
    if pose == "wave" and marks:
        fronts.append(_wave_marks)
    if pose == "shoulders":
        rv = int(variant) + 1 if rider is None else rider
        D["behind"] = _rider_child(rv)

        D["hat"] = None
        D.pop("tail", None)
        D["ears"] = True
    if kind == "elder" and pose in ("stand", "walk_a", "walk_b", "listen", "nod"):
        ps["t"] = ps["t"] + 8
        if pose != "listen":
            ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
            fronts.insert(0, _cane)
    D["front"] = _hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"villager-{kind}{int(variant) % 6}-{pose}")


# ---------------------------------------------------------------- the modern child at night (child(outfit=...))
STORM_CHILD_POSES = ("hug_pillow", "sit_hug", "pray", "kneel_pray", "sit_pray")
CHILD_OUTFITS = ("pyjamas",)
PYJAMA = "#8fa6d8"
PYJAMA_STAR = "#f4d77a"
_SC_POSES = {
    "hug_pillow": _P(t=4, h=6, legs=((6, 2), (-5, -2)), arms=(("ik", "body", -2, -50, 1), ("ik", "body", 46, -12, 1)),
                     hands=("open", "open"), expr="worried", look=(0.04, 0.0)),
    "sit_hug": _P(t=2, h=8, legs=(("ik", 66, 1), ("ik", 76, 1)),
                  arms=(("ik", "body", 2, -52, 1), ("ik", "body", 46, -16, 1)), hands=("open", "open"),
                  expr="worried", **_SEATED),
    "pray": _P(h=-6, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)), hands=("none", "pray"),
               expr="peaceful", look=(0.02, -0.04)),
    "kneel_pray": dict(POSES["kneel_pray"]),
    "sit_pray": _P(t=-2, h=-4, legs=(("ik", 70, 1), ("ik", 80, 1)),
                   arms=(("ik", "torso", 1.5, 0.66, 1), ("ik", "torso", 1.5, 0.66, 1)), hands=("none", "pray"),
                   expr="peaceful", **_SEATED),
}


def _pyjama_design(base):
    c = PYJAMA
    D = dict(robe=c, sleeve=c, hem_col=shade(c, -0.1), hem_w=6, cuff=shade(c, -0.12), skin="#f0c09a", leg="#f0c09a",
             hem=0.36, flare_k=0.7, hair="#3a2618", hair_style="short", sandal="#f0e6d6", neck_v="#f6ecd8",
             hat=("custom", _pigtails), hat_h=0.12, ears=False, bare=True)

    def stars(st, polys):
        m, tp = st["m"], st["tp"]
        s = ""
        for fx, uy in ((-0.4, 0.75), (0.45, 0.45), (-0.1, 0.15), (0.5, -0.12), (-0.45, -0.18)):
            p = tp(fx * m["ww"], uy * m["T"] if uy > 0 else uy * (m["th"] + m["sh"]) * 0.6)
            s += _star_pts(p, 5.5)
        return s
    D["robe_deco"] = stars

    def legwear(st, i):
        H, K, A, a1, a2 = st["legs"][i]
        col = c if i == 1 else shade(c, -0.12)
        s_ = _tube([H, K, _lerp(K, A, 0.86)], st["m"]["lw"] + 9, col, ow=3.2)
        for t in (0.3, 0.75):
            s_ += _star_pts(_lerp(H, K, t) if t < 0.5 else _lerp(K, A, t - 0.25), 4.5)
        cuff = _lerp(K, A, 0.80)
        dv = _nrm(_sub(A, K))
        nv = (-dv[1], dv[0])
        w = (st["m"]["lw"] + 9) / 2
        s_ += _line(f"M{_pt(_add(cuff, _mul(nv, w)))} L{_pt(_sub(cuff, _mul(nv, w)))}", w=2.2, col=shade(c, -0.3))
        return s_
    D["legwear"] = legwear
    return D


def _star_pts(c, r):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    return _poly(pts, PYJAMA_STAR, sw=0)


def _pigtails(R):
    """The pyjama girl's hair: a soft bob with a side fringe and two little bunches tied with yellow bobbles."""
    col = "#3a2618"
    s = ""
    for (cx, cy) in ((-1.08 * R, 0.10 * R),):
        s += _ell(cx, cy, 0.30 * R, 0.36 * R, col, sw=3.0)
        s += f'<circle cx="{fmt(cx + 0.18 * R)}" cy="{fmt(cy - 0.24 * R)}" r="{fmt(0.09 * R)}" fill="{PYJAMA_STAR}" {_st(2.2)}/>'
    pts = [(0.92 * R, -0.36 * R), (0.80 * R, -0.86 * R), (0.25 * R, -1.12 * R), (-0.45 * R, -1.06 * R),
           (-0.98 * R, -0.66 * R), (-1.10 * R, 0.02 * R), (-0.95 * R, 0.42 * R), (-0.70 * R, 0.30 * R),
           (-0.62 * R, -0.10 * R), (-0.20 * R, -0.42 * R), (0.20 * R, -0.30 * R), (0.55 * R, -0.42 * R)]
    s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
    s += _line(f"M{fmt(0.10 * R)},{fmt(-1.02 * R)} Q{fmt(-0.30 * R)},{fmt(-0.80 * R)} {fmt(-0.70 * R)},{fmt(-0.30 * R)}",
               w=2.0, col=shade(col, 0.3))
    return s


def _pillow_front(D, pose, k=0.52):
    def front(st):
        PR = _prp()
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        c = ((W0[0] + W1[0]) / 2 - 2, (W0[1] + W1[1]) / 2 + 2)
        s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate(-38) scale({k})">{PR._pillow(hug=1.0)}</g>'
        return s + _hand(W0, (0.3, 1.0), "open", D["skin"], hr) + _hand(W1, (0.4, 1.0), "open", D["skin"], hr)
    return front


def _child_storm(x, y, scale, facing, pose, expr, phase, marks, outfit, pillow, sibling, hood, boots, coat):
    if outfit is not None and outfit not in CHILD_OUTFITS:
        raise ValueError(f"child: unknown outfit {outfit!r}; choose from {CHILD_OUTFITS}")
    allp = CHILD_POSES + SIBLING_POSES + STORM_CHILD_POSES
    if pose not in allp:
        raise ValueError(f"child: unknown pose {pose!r}; choose from {allp}")
    _check_js_expr(expr, "child")
    if pose in _SC_POSES:
        ps = dict(_SC_POSES[pose])
    elif pose == "wave":
        f = 166 + 18 * math.sin(2 * math.pi * phase)
        ps = _P(h=-4, arms=(("fk", 146, f), ("fk", -10, -4)), hands=("open", "fist"), expr="happy")
    elif pose in _SIB_POSES:
        ps = dict(_SIB_POSES[pose])
    else:
        ps = dict(_CH_POSES[pose])
    if outfit == "pyjamas":
        D, m = _pyjama_design(ps), _metrics(_CHILD, 1.0, 0.96)
    elif sibling is not None:
        D, m = _sibling_design(sibling)
    else:
        D, m = _child_design(ps["legs"], hood, boots, coat or CHILD_COAT), _CHILD
    if pose in ("hug_pillow", "sit_hug") and pillow:
        D["front"] = _pillow_front(D, pose)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    if pose == "jump":
        inner = f'<g transform="translate(0,{-CHILD_JUMP})">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"child-{outfit or sibling or 'raincoat'}-{pose}")


VILLAGER_CROWD_POSES = ("stand", "listen", "sit", "sit_listen", "wave", "cheer", "walk_a", "walk_b", "nod", "kneel")


def villager_crowd(x, y, scale=1.0, facing=1, n=12, pose="stand", width=900, rows=3, seed=0, poses=None, expr=None,
                   phase=0.0, marks=True):
    """A lakeshore crowd of n villagers (mixed kinds and colours) in up to `rows` rows centred on x (see module doc).
    The front row stands on y; each row behind is 46*scale higher and 6% smaller, drawn first. pose (or the list
    poses, cycled) is given to everyone; walk poses alternate frames so nobody marches in step; children are put in
    the front row; one father in the back carries a child on his shoulders when n >= 8 and pose is stand / listen /
    wave / cheer."""
    _check_js(pose, VILLAGER_CROWD_POSES, "villager_crowd")
    import random as _random
    rng = _random.Random(seed)
    sx = 1 if facing >= 0 else -1
    rows = max(1, int(rows))
    people = []
    kinds = ["child", "woman", "man", "elder", "man", "woman", "child", "man", "woman", "elder", "child", "man"]
    for i in range(int(n)):
        k = kinds[(i + seed) % len(kinds)]
        people.append((k, (i * 5 + seed) % 6))
    people.sort(key=lambda p_: 0 if p_[0] == "child" else 1)          # children to the front
    per = max(1, -(-len(people) // rows))
    out = ""
    shoulders_done = False
    for r in reversed(range(rows)):
        grp = people[r * per:(r + 1) * per]
        if not grp:
            continue
        k_r = scale * (1 - 0.06 * r)
        y_r = y - 46 * scale * r
        for j, (kind, v) in enumerate(grp):
            u = (j + 0.5) / len(grp) - 0.5
            px = x + sx * (u * width * scale + (r % 2) * 40 * scale + rng.uniform(-14, 14) * scale)
            p_ = poses[(j + r) % len(poses)] if poses else pose
            if p_ in ("walk_a", "walk_b") and (j + r) % 2:
                p_ = "walk_b" if p_ == "walk_a" else "walk_a"
            if p_.startswith("walk") or pose in ("listen", "sit_listen", "sit", "kneel", "nod"):
                f_ = sx                    # everybody looks the same way (toward the speaker / where they go)
            else:
                f_ = sx if u < 0 else -sx  # a chatting crowd: the two halves face each other
            if (not shoulders_done and r == rows - 1 and kind == "man" and n >= 8 and
                    p_ in ("stand", "listen", "wave", "cheer")):
                p_, shoulders_done = "shoulders", True
            kw = dict(kind=kind, variant=v, pose=p_, expr=expr, phase=(phase + 0.21 * j) % 1.0, marks=marks)
            out += villager(px, y_r + rng.uniform(-6, 6) * scale, k_r, f_, **kw)
    return f'<g data-who="villager_crowd-{pose}">{out}</g>'


# ======================================================================= Nativity film (Luke 1-2, Matthew 2)
# Mary, Joseph the carpenter, baby_jesus(), toddler_jesus(), the angels and angel_choir(), the shepherds, the wise men,
# the Bethlehem townsfolk and townsfolk_crowd(), and child(outfit='jumper') with the Christmas-tree poses. New designs
# with this film's own palette (starry-night blues, warm lamplight gold, the gold of the star). Module doc section
# "NATIVITY FILM".

EXPRS.update({
    "startled": dict(eyes="big", brow=(-0.10, 0.02, -0.17), mouth="small_open", blush=True, look=(0.03, -0.02)),
    "tender":   dict(eyes="dot", brow=(-0.08, 0.04, -0.04), mouth="smile", blush=True, look=(0.02, 0.07)),
    "joyful":   dict(eyes="arc", brow=(-0.05, 0.02, -0.09), mouth="grin", blush=True),
    "weary":    dict(eyes="droop", brow=(-0.08, 0.04, 0.02), mouth="smile"),
    "sing":     dict(eyes="arc", brow=(-0.06, 0.02, -0.09), mouth="awe", blush=True),
    "proclaim": dict(eyes="dot", brow=(-0.06, 0.02, -0.08), mouth="call", blush=True),
    "hush":     dict(eyes="closed", brow=(-0.05, 0.03, 0.0), mouth="small_o", blush=True),
    "question": dict(eyes="dot", brow=(-0.07, 0.03, -0.12), brow2=(-0.02, -0.02, -0.04), mouth="small_open", blush=True,
                     look=(0.03, -0.03)),
    "thoughtful": dict(eyes="dot", brow=(-0.07, 0.03, -0.07), mouth="smile", blush=True, look=(-0.04, 0.05)),
})
NATIVITY_EXPRESSIONS = ("startled", "tender", "joyful", "weary", "sing", "proclaim", "hush", "question", "thoughtful")
NATIVITY_CHILD_POSES = ("decorate", "place", "kneel_look", "hold_star")
CHILD_OUTFITS = CHILD_OUTFITS + ("jumper",)

# ---------------------------------------------------------------- palette
MARY_SKIN = "#d9a679"
MARY_HAIR = "#2e2019"
MARY_VEIL = "#6f95cf"
MARY_LINING = "#a9c4e8"
MARY_DRESS = "#efdcb4"
MARY_BLUE = "#3f62a2"
MARY_TRIM = "#cf9a4c"
JOSEPH_C_SKIN = "#c48b62"
JOSEPH_C_HAIR = "#35261d"
JOSEPH_C_TUNIC = "#b47a3c"
JOSEPH_C_CLOAK = "#7a5338"
JOSEPH_C_STRIPE = "#ead9b6"
JOSEPH_C_BAND = "#a94f39"
BABY_SKIN = "#e7b189"
BABY_CLOTH = "#f6efdd"
BABY_BAND = "#e3d3b0"
ANGEL_ROBE = "#fbf4e1"
ANGEL_GOLD = "#e9c35c"
ANGEL_WING = "#fbf6e8"
ANGEL_FEATHER = "#e6cf98"
LAMPLIGHT = "#ffd36e"
STAFF_WOOD = "#8f6440"

_MARY_M = _metrics(_ADULT, 0.93, 0.88)
_JOSEPH_C_M = _metrics(_ADULT, 1.01, 1.04)
_TODDLER = dict(R=33, T=38, neck=26, ua=22, fa=19, th=23, sh=21, aw=13, lw=11.5, hr=7.5, fl=16, sw=15, hw=8, ww=18.5,
                shw=20, flare=8, sdrop=6, seat=10, ank=8)


def _nat_expr(expr, who):
    """Nativity functions draw 'tired' as the gentle 'weary' face (droopy lids, a soft smile, no sweat drops)."""
    if expr == "tired":
        return "weary"
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{who}: unknown expr {expr!r}; choose from {tuple(EXPRS)}")
    return expr


def _reanchor(inner, dx, dy):
    """Make the point (dx, dy) (anchor coords of the figure just built) the new anchor; _LAST follows."""
    for k in ("hands", "shoulders", "feet"):
        _LAST[k] = [(p[0] - dx, p[1] - dy) for p in _LAST[k]]
    for k in ("head", "head_top", "pelvis"):
        p = _LAST[k]
        _LAST[k] = (p[0] - dx, p[1] - dy)
    b = _LAST["bbox"]
    _LAST["bbox"] = (b[0] - dx, b[1] - dy, b[2] - dx, b[3] - dy)
    _LAST["pts"] = [(x - dx, y - dy, r) for x, y, r in _LAST["pts"]]
    return f'<g transform="translate({fmt(-dx)},{fmt(-dy)})">{inner}</g>'


def _seat_point(m):
    """The seat contact under the pelvis of the figure just built (anchor coords): for riders / laps."""
    p = _LAST["pelvis"]
    return (p[0], p[1] + 0.5 * m["lw"] + 7)


def _nested(D, m, ps, expr, marks=True):
    """Build a figure inside another figure's hook without disturbing _LAST; returns (inner, bbox, last)."""
    saved = dict(_LAST)
    inner, bb = _figure(D, m, ps, expr, 1, marks)
    last = dict(_LAST)
    _LAST.clear()
    _LAST.update(saved)
    return inner, bb, last


def _glow_disc(c, rx, ry, level, gid_key, col0=None, col1=None):
    """A soft warm radial glow (no ring) centred on c."""
    if level <= 0:
        return ""
    col0, col1 = col0 or P["glow"], col1 or "#ffe6a8"
    gid = _clip_id("nglow", gid_key, round(level, 3), round(c[0]), round(c[1]), round(rx), round(ry), col0, col1)
    return (f'<defs><radialGradient id="{gid}" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="{col0}" stop-opacity="0.95"/>'
            f'<stop offset="0.42" stop-color="{col1}" stop-opacity="0.42"/>'
            f'<stop offset="1" stop-color="{col1}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="url(#{gid})" '
            f'opacity="{min(1.0, level):.2f}"/>')


def _sparkle(c, r, col="#fff6d0", w=0.0):
    """A soft four-pointed sparkle."""
    x, y = c
    d = (f"M{fmt(x)},{fmt(y - r)} Q{fmt(x + r * 0.16)},{fmt(y - r * 0.16)} {fmt(x + r)},{fmt(y)} "
         f"Q{fmt(x + r * 0.16)},{fmt(y + r * 0.16)} {fmt(x)},{fmt(y + r)} Q{fmt(x - r * 0.16)},{fmt(y + r * 0.16)} "
         f"{fmt(x - r)},{fmt(y)} Q{fmt(x - r * 0.16)},{fmt(y - r * 0.16)} {fmt(x)},{fmt(y - r)} Z")
    st = _st(w, shade(col, -0.35)) if w else ""
    return f'<path d="{d}" fill="{col}" {st}/>'


def _lashes(R, kind):
    """Two tiny lashes at the outer eye corners (young women and children of this film)."""
    if kind not in ("dot", "down", "closed", "arc", "big", "droop"):
        return ""
    dy = 0.06 * R if kind in ("closed", "down", "droop") else 0.0
    return (_line(f"M{fmt(-0.22 * R)},{fmt(-0.06 * R + dy)} l{fmt(-0.07 * R)},{fmt(-0.05 * R)}", w=2.2) +
            _line(f"M{fmt(0.52 * R)},{fmt(-0.06 * R + dy)} l{fmt(0.07 * R)},{fmt(-0.05 * R)}", w=2.2))


def _staff_line(x, y_top, y_bot, w=7.5, col=STAFF_WOOD, lean=0.0):
    """A straight walking staff with a rounded knob top and two knots."""
    top, bot = (x + lean, y_top), (x - lean * 0.2, y_bot)
    s = _tube([bot, top], w, col, ow=3.0)
    s += _line(f"M{_pt(_lerp(bot, top, 0.05))} L{_pt(_lerp(bot, top, 0.96))}", w=1.6, col=shade(col, 0.35),
               extra='opacity="0.7"')
    for t in (0.42, 0.7):
        k = _lerp(bot, top, t)
        s += _line(f"M{fmt(k[0] - w / 2)},{fmt(k[1])} q{fmt(w / 2)},{fmt(-3)} {fmt(w)},0", w=1.8, col=shade(col, -0.35))
    s += f'<circle cx="{fmt(top[0])}" cy="{fmt(top[1])}" r="{fmt(w * 0.85)}" fill="{shade(col, 0.1)}" {_st(3.0)}/>'
    return s


# ---------------------------------------------------------------- Mary (head frame)
def _mary_hat(expr):
    E = EXPRS.get(expr, EXPRS["neutral"])

    def hat(R):
        s = _lashes(R, E["eyes"])
        # dark hair showing under the veil: a soft centre-parted fringe and a lock in front of the ear
        hair = [(0.96 * R, -0.30 * R), (0.70 * R, -0.46 * R), (0.32 * R, -0.50 * R), (0.10 * R, -0.42 * R),
                (-0.16 * R, -0.46 * R), (-0.50 * R, -0.30 * R), (-0.62 * R, 0.06 * R), (-0.56 * R, 0.46 * R),
                (-0.70 * R, 0.62 * R), (-0.86 * R, 0.40 * R), (-0.86 * R, -0.30 * R), (-0.30 * R, -0.80 * R),
                (0.55 * R, -0.78 * R)]
        s += f'<path d="{smooth_path(hair)}" fill="{MARY_HAIR}" {_st(3.0)}/>'
        lite = shade(MARY_HAIR, 0.32)
        s += _line(f"M{fmt(0.62 * R)},{fmt(-0.56 * R)} Q{fmt(0.42 * R)},{fmt(-0.50 * R)} {fmt(0.18 * R)},{fmt(-0.50 * R)}",
                   w=1.8, col=lite)
        s += _line(f"M{fmt(-0.12 * R)},{fmt(-0.54 * R)} Q{fmt(-0.46 * R)},{fmt(-0.40 * R)} {fmt(-0.70 * R)},{fmt(0.30 * R)}",
                   w=1.8, col=lite)
        # the soft blue veil: covers the top and back of the head, front edge set back so the hair shows
        veil = [(0.98 * R, -0.46 * R), (0.84 * R, -0.90 * R), (0.25 * R, -1.18 * R), (-0.48 * R, -1.12 * R),
                (-1.02 * R, -0.70 * R), (-1.20 * R, 0.05 * R), (-1.16 * R, 0.72 * R), (-0.86 * R, 0.86 * R),
                (-0.78 * R, 0.30 * R), (-0.74 * R, -0.26 * R), (-0.30 * R, -0.60 * R), (0.40 * R, -0.66 * R)]
        s += f'<path d="{smooth_path(veil)}" fill="{MARY_VEIL}" {_st(3.6)}/>'
        s += _tube(_spline_pts([(1.00 * R, -0.50 * R), (0.45 * R, -0.70 * R), (-0.24 * R, -0.66 * R),
                                (-0.76 * R, -0.30 * R), (-0.84 * R, 0.32 * R), (-0.92 * R, 0.80 * R)]), 0.13 * R,
                   MARY_LINING, ow=2.4)
        fold = shade(MARY_VEIL, -0.22)
        s += _line(f"M{fmt(-0.30 * R)},{fmt(-0.98 * R)} Q{fmt(-0.86 * R)},{fmt(-0.56 * R)} {fmt(-0.98 * R)},{fmt(0.50 * R)}",
                   w=2.2, col=fold)
        s += _line(f"M{fmt(0.30 * R)},{fmt(-1.06 * R)} Q{fmt(-0.10 * R)},{fmt(-0.90 * R)} {fmt(-0.48 * R)},{fmt(-0.70 * R)}",
                   w=2.0, col=shade(MARY_VEIL, 0.25), extra='opacity="0.8"')
        return s
    return hat


def _mary_design(expr):
    return dict(robe=MARY_DRESS, sleeve=MARY_DRESS, hem_col=MARY_TRIM, hem_w=6, cuff=MARY_TRIM, skin=MARY_SKIN,
                leg=MARY_SKIN, hem=0.96, flare_k=1.05, hair=None, hat=("custom", _mary_hat(expr)), hat_h=0.20,
                veil=MARY_VEIL, ears=False, sash=MARY_BLUE, sash_tail=True, neck_v=MARY_TRIM,
                sandal="#9a6a45", brow_w=3.0)


_MSEAT = dict(lap=True, legs=((86, 4), (82, 2)), hem=0.97, flare=-8)
_MY = {
    "stand": _P(arms=(("fk", 10, 6), ("fk", -6, -2)), expr="kind"),
    "walk_a": _P(t=3, legs=((22, 8), (-18, -30)), arms=(("fk", -24, -16), ("fk", 18, 30)), expr="kind"),
    "walk_b": _P(t=3, legs=((-18, -30), (22, 8)), arms=(("fk", 22, 34), ("fk", -16, -8)), expr="kind"),
    "walk_c": _P(t=2, legs=((5, 1), (-8, -16)), arms=(("fk", 4, 8), ("fk", 2, 8)), expr="kind"),
    "startled": _P(t=-7, h=-6, legs=((16, 5), (-20, -12)), arms=(("fk", 40, 112), ("ik", "torso", 0.55, 0.72, 1)),
                   hands=("open", "open"), expr="startled"),
    "bow": _P(t=7, h=24, arms=(("ik", "torso", 1.35, 0.58, 1), ("ik", "torso", 1.35, 0.58, 1)), hands=("none", "pray"),
              expr="calm"),
    "kneel": _P(t=-2, h=10, arms=(("ik", "torso", 1.45, 0.60, 1), ("ik", "torso", 1.45, 0.60, 1)), hands=("none", "pray"),
                expr="tender", **_KNEEL),
    "kneel_up": _P(t=-4, h=-18, arms=(("ik", "torso", 1.45, 0.64, 1), ("ik", "torso", 1.45, 0.64, 1)),
                   hands=("none", "pray"), expr="awed", look=(0.02, -0.06), **_KNEEL),
    "sit": _P(t=-2, arms=(("ik", "knee", 0, 0.28, 1), ("ik", "knee", 1, 0.28, 1)), hands=("open", "open"), expr="kind",
              **_MSEAT),
    "smile_down": _P(h=20, arms=(("ik", "torso", 1.05, 0.22, 1), ("ik", "torso", 1.05, 0.22, 1)), hands=("none", "pray"),
                     expr="tender"),
    "pray": _P(h=-10, arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)), hands=("none", "pray"),
               expr="peaceful", look=(0.02, -0.05)),
    "carry_jar": _P(t=1, arms=(("fk", 10, 6), ("ik", "headw", -1.02, -0.62, -1)), hands=("fist", "open"), expr="kind"),
    "carry_jar_walk_a": _P(t=3, legs=((22, 8), (-18, -30)), arms=(("fk", -24, -16), ("ik", "headw", -1.02, -0.62, -1)),
                           hands=("fist", "open"), expr="kind"),
    "carry_jar_walk_b": _P(t=3, legs=((-18, -30), (22, 8)), arms=(("fk", 22, 34), ("ik", "headw", -1.02, -0.62, -1)),
                           hands=("fist", "open"), expr="kind"),
    "hold_baby": _P(t=2, h=20, arms=(("ik", "abs", 60, -164, 1), ("ik", "abs", 8, -152, 1)), hands=("open", "open"),
                    expr="tender"),
    "sit_baby": _P(t=0, h=20, arms=(("ik", "abs", 64, -124, 1), ("ik", "abs", 12, -112, 1)), hands=("open", "open"),
                   expr="tender", **_MSEAT),
    "lay_baby": _P(t=30, h=12, drop=14, legs=(("ik", 22, 1), ("ik", -26, 1)), reach=1.05,
                   arms=(("ik", "abs", 136, -118, 1), ("ik", "abs", 86, -124, 1)), hands=("open", "open"), expr="tender"),
    "wrap": _P(t=6, h=24, arms=(("ik", "abs", 88, -96, 1), ("ik", "abs", 30, -110, 1)), hands=("open", "fist"),
               expr="tender", **_MSEAT),
    "sit_hold": _P(t=-2, h=8, arms=(("ik", "abs", 66, -150, 1), ("ik", "abs", 40, -118, 1)), hands=("open", "open"),
                   expr="kind", **_MSEAT),
    "question": _P(t=-2, h=-8, legs=((6, 2), (-5, -2)), arms=(("fk", 26, 104), ("ik", "torso", 0.55, 0.72, 1)),
                   hands=("open", "open"), expr="question"),
    "listen_think": _P(t=2, h=16, arms=(("ik", "torso", 1.0, 0.28, 1), ("ik", "torso", 0.62, 0.70, 1)),
                       hands=("none", "open"), expr="thoughtful"),
    "sit_think": _P(t=0, h=16, arms=(("ik", "knee", 0, 0.28, 1), ("ik", "torso", 0.62, 0.70, 1)), hands=("open", "open"),
                    expr="thoughtful", **_MSEAT),
    "ride": _P(t=-3, lap=True, legs=((62, -2), (56, -6)), hem=0.97, flare=-6,
               arms=(("ik", "body", 46, -26, 1), ("ik", "body", 34, -20, 1)), hands=("open", "open"), expr="kind"),
    "ride_baby": _P(t=-2, h=18, lap=True, legs=((62, -2), (56, -6)), hem=0.97, flare=-6,
                    arms=(("ik", "body", 52, -56, 1), ("ik", "body", 2, -44, 1)), hands=("open", "open"), expr="tender"),
}
MARY_POSES = ("stand", "walk", "walk_a", "walk_b", "walk_c", "sweep", "carry_jar", "carry_jar_walk_a", "carry_jar_walk_b",
              "startled", "bow", "kneel", "kneel_up", "pray", "sit", "ride", "ride_baby", "hold_baby", "sit_baby",
              "lay_baby", "wrap", "smile_down", "sit_hold", "question", "listen_think", "sit_think")
MARY_EXPRESSIONS = ("kind", "startled", "calm", "tender", "tired", "joyful", "awed", "question", "thoughtful", "peaceful",
                    "happy", "worried")
MARY_LAY_DX = 112           # lay_baby: the baby is held this far in front of the anchor ...
MARY_LAY_Y = -112           # ... with its underside at this height (put props.manger's bed there)


def _broom_line(phase):
    """Broom handle top T and head point B (anchor coords) for the sweep cycle."""
    s = math.sin(2 * math.pi * phase)
    return (24 + 10 * s, -214), (150 + 38 * s, -6)


def _walk_phase_pose(table, phase, prefix=""):
    """walk + phase 0..1: the planted-foot cycle a (0) - c (.25) - b (.5) - c (.75)."""
    q = int((phase % 1.0) * 4 + 1e-6) % 4
    return dict(table[prefix + ("walk_a", "walk_c", "walk_b", "walk_c")[q]])


def _mary_pose(pose, phase):
    if pose == "walk":
        return _walk_phase_pose(_MY, phase)
    if pose == "sweep":
        T, B = _broom_line(phase)
        hn, hf = _lerp(T, B, 0.06), _lerp(T, B, 0.40)
        return _P(t=10, h=14, legs=((14, 4), (-14, -8)), arms=(("ik", "abs", hf[0], hf[1], 1), ("ik", "abs", hn[0], hn[1], 1)),
                  hands=("fist", "fist"), expr="kind", look=(0.03, 0.06))
    return dict(_MY[pose])


def _broom_front(D, phase, marks):
    def front(st):
        G = st["ground"]
        T, B = _broom_line(phase)
        T, B = (T[0], G + T[1]), (B[0], G + B[1])
        dv = _nrm(_sub(B, T))
        K = _sub(B, _mul(dv, 46))
        s = _tube([_sub(T, _mul(dv, 14)), K], 7, STAFF_WOOD, ow=3.0)
        nv = (-dv[1], dv[0])
        fan = [_add(K, _mul(nv, 9)), _add(_add(B, _mul(nv, 30)), (0, 2)), _add(_add(B, _mul(nv, -26)), (0, 2)),
               _add(K, _mul(nv, -9))]
        fan = [(x, min(y, G - 2)) for x, y in fan]
        straw = "#d9b366"
        s += f'<path d="{smooth_path(fan, tension=0.5)}" fill="{straw}" {_st(3.2)}/>'
        for t in (-0.6, -0.2, 0.2, 0.6):
            a = _add(K, _mul(nv, 6 * t))
            b = _add(_add(B, _mul(nv, 26 * t)), (0, -2))
            s += _line(f"M{_pt(a)} L{_pt((b[0], min(b[1], G - 4)))}", w=1.8, col=shade(straw, -0.3))
        s += _tube([_add(K, _mul(nv, 10)), _add(K, _mul(nv, -10))], 5, P["terracotta"], ow=2.2)
        if marks:
            for k, (dx, dy, r) in enumerate(((-34, -8, 7), (-48, -18, 5), (36, -10, 6))):
                s += _ell(B[0] + dx, G + dy, r * 1.4, r, "#e8dcc4", extra='opacity="0.6"')
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        return s + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    return front


def _water_jar_mid(D, k=0.95):
    def mid(st):
        Sn = st["S"][1]
        c = (Sn[0] - 20, Sn[1] + 2)
        return f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate(-12) scale({k})">{_prp()._water_jar()}</g>'
    return mid


def _baby_hook(state, at, rot=0.0, k=1.0, hands=(), D=None, glow=0.0, cloth=False):
    """Draw the swaddled baby with its anchor at `at` (body coords) rotated `rot`; then redraw the given hands."""
    def hook(st):
        G = st["ground"]
        p = (at[0], G + at[1]) if at[2:] == ("abs",) else (at[0], at[1])     # anchor coords / body coords
        s = ""
        if glow > 0:
            s += _glow_disc(p, 120 * k, 80 * k, glow, "babyheld")
        s += f'<g transform="translate({fmt(p[0])},{fmt(p[1])}) rotate({fmt(rot)}) scale({k})">{_baby_svg(state, cloth=cloth)}</g>'
        for i in hands:
            W = st["arms"][i][2]
            E = st["arms"][i][1]
            s += _hand(W, _nrm(_sub(W, E)), "open", D["skin"], st["m"]["hr"])
        return s
    return hook


def _toddler_on_lap(expr, pose="sit"):
    def mid(st):
        H, K = st["legs"][1][0], st["legs"][1][1]
        lap = _add(_lerp(H, K, 0.58), (0, -0.5 * st["m"]["lw"] - 9))
        inner, bb, last = _toddler_inner(pose, expr or "happy", 0.0, True)
        return f'<g transform="translate({fmt(lap[0])},{fmt(lap[1])})">{inner}</g>'
    return mid


def _bump_mid(D, seated=False):
    """pregnant: a round, gentle belly under the dress, clearly past the body's front line (outline only on the outside),
    an empire sash just above it; seated: a little higher so its round top shows above the lap."""
    def mid(st):
        m, tp = st["m"], st["tp"]
        ww, T = m["ww"], m["T"]
        c = (1.05 * ww, 0.27 * T) if seated else (0.95 * ww, 0.20 * T)
        rf, ru = (1.12 * ww, 0.41 * T) if seated else (1.02 * ww, 0.46 * T)

        def ep(a, k=1.0, kr=1.0):
            r = math.radians(a)
            return tp(c[0] + kr * rf * math.cos(r) * k, c[1] + kr * ru * math.sin(r))
        arc = [ep(a) for a in range(-100, 106, 6)]
        top_u, bot_u = c[1] + ru * math.sin(math.radians(100)), c[1] + ru * math.sin(math.radians(-100))
        fill = arc + [tp(0.05 * ww, top_u), tp(0.05 * ww, bot_u)]
        col = D["robe"]
        s = _poly(fill, col, sw=0)
        # roundness: a soft shadow along the lower front, a highlight on the upper front
        shadow = [ep(a) for a in range(-96, 34, 8)] + [ep(a, kr=0.80) for a in range(26, -90, -8)]
        s += _poly(shadow, shade(col, -0.14), sw=0, extra='opacity="0.55"')
        s += _line(_d([ep(a, kr=0.62) for a in range(10, 74, 8)], closed=False), w=5.0, col=shade(col, 0.5),
                   extra='opacity="0.75"')
        s += _line(_d(arc, closed=False), w=OW)
        # empire sash just above the bump
        for poly in st["robe"][:1]:
            b = _band(poly, st["pel"], st["u"], 0.62 * T, 0.72 * T)
            if len(b) > 2:
                s += _poly(b, D["sash_col"], sw=2.6)
        k0 = tp(0.62 * ww, 0.66 * T)
        s += _tube([k0, tp(0.86 * ww, 0.42 * T)], 6, D["sash_col"], ow=2.4) + _tube([k0, tp(0.66 * ww, 0.38 * T)], 6,
                                                                                     D["sash_col"], ow=2.4)
        s += f'<circle cx="{fmt(k0[0])}" cy="{fmt(k0[1])}" r="6" fill="{D["sash_col"]}" {_st(2.4)}/>'
        return s
    return mid


def mary(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, baby=True, glow=0.0, pregnant=False,
         marks=True):
    """Mary, a kind young woman (about 16-18) of Nazareth (see module doc, 'NATIVITY FILM')."""
    _check_js(pose, MARY_POSES, "mary")
    expr = _nat_expr(expr, "mary")
    ps = _mary_pose(pose, phase)
    e = expr or ps["expr"]
    D = _mary_design(e)
    behind, mid, front = [], [], []
    if glow > 0:
        behind.append(_soft_glow(_clamp01(glow)))
    if pregnant:
        D["sash_col"] = D.pop("sash")
        mid.append(_bump_mid(D, ps["lap"]))
        m_ = _MARY_M
        bump_hand = ("ik", "body", 1.25 * m_["ww"], -0.62 * m_["T"], 1)     # a hand resting on top of the belly
        if pose == "sit":
            ps["arms"], ps["hands"] = (("ik", "knee", 0, 0.28, 1), bump_hand), ("open", "open")
        elif pose == "ride":
            ps["arms"], ps["hands"] = (("ik", "body", 2.6 * m_["ww"], -0.05 * m_["T"], 1), bump_hand), ("open", "open")
    if pose == "sweep":
        front.append(_broom_front(D, phase, marks))
    elif pose.startswith("carry_jar"):
        mid.append(_water_jar_mid(D))
    elif pose in ("hold_baby", "sit_baby", "ride_baby") and baby:
        at = {"hold_baby": (20, -150, "abs"), "sit_baby": (24, -110, "abs"), "ride_baby": (26, -38, "body")}[pose]
        front.append(_baby_hook("held", at, -12, 0.82, hands=(1,), D=D))
    elif pose == "lay_baby" and baby:
        front.append(_baby_hook("in_manger", (MARY_LAY_DX, MARY_LAY_Y, "abs"), -4, 0.86, hands=(0, 1), D=D))
    elif pose == "wrap" and baby:
        mid.append(_baby_hook("wrap", (36, -104, "abs"), 4, 0.86, D=D, cloth=True))
        front.append(_wrap_band(D))
    elif pose == "sit_hold" and baby:
        mid.append(_toddler_on_lap(None, "sit"))
    D["behind"], D["mid"], D["front"] = _hooks(*behind), _hooks(*mid), _hooks(*front)
    m = _MARY_M
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    if pose in ("ride", "ride_baby"):
        sx, sy = _seat_point(m)
        inner = _reanchor(inner, sx, sy)
    return _wrap_out(inner, x, y, scale, facing, f"mary-{pose}")


def _wrap_band(D):
    """wrap: a loose cloth band from the swaddled baby up to Mary's near hand."""
    def front(st):
        W1, hr = st["arms"][1][2], st["m"]["hr"]
        G = st["ground"]
        b0 = (60, G - 104)
        pts = _spline_pts([b0, (52, G - 120), (W1[0] + 6, W1[1] + 14), (W1[0] - 4, W1[1] + 4)], steps=5)
        s = _tube(pts, 9, BABY_CLOTH, ow=2.6)
        s += _line(_d(pts, closed=False), w=1.4, col=BABY_BAND)
        tail = _spline_pts([(W1[0] - 2, W1[1]), (W1[0] - 18, W1[1] + 24), (W1[0] - 12, W1[1] + 48)], steps=4)
        s += _tube(tail, 8, BABY_CLOTH, ow=2.4)
        return s + _fist(W1, hr, D["skin"])
    return front


# ---------------------------------------------------------------- the baby (a swaddled newborn)
def _baby_svg(state="in_manger", hand=False, cloth=False):
    """Swaddled newborn, local: anchor at the bottom centre of the bundle, HEAD ON THE LEFT, ~132 x 62."""
    awake = state == "awake"
    s = ""
    if cloth:                    # a spread cloth under the bundle (wrapping)
        s += f'<path d="{smooth_path([(-80, 2), (-60, -14), (70, -16), (92, 0), (60, 10), (-60, 10)])}" fill="{BABY_CLOTH}" {_st(3.0)}/>'
        s += _line("M-58,4 L76,2", w=1.6, col=BABY_BAND)
    body = [(-40, -54), (-6, -52), (34, -46), (60, -34), (68, -18), (60, -4), (30, 1), (-20, 1), (-52, -6), (-64, -26)]
    bd = smooth_path(body)
    cid = _clip_id("babyb", bd, state)
    s += f'<path d="{bd}" fill="{BABY_CLOTH}" {_st(3.6)}/>'
    bands = ""
    for k, x0 in enumerate((-30, -4, 22, 46)):
        bands += _poly([(x0 - 4, 4), (x0 + 6, 4), (x0 + 22, -58), (x0 + 12, -58)], BABY_BAND, sw=0)
        bands += _line(f"M{fmt(x0 + 1)},4 L{fmt(x0 + 17)},-58", w=1.5, col=shade(BABY_BAND, -0.25))
    bands += _line("M-40,-12 Q10,-4 64,-12", w=2.0, col=shade(BABY_CLOTH, -0.12), extra='opacity="0.8"')
    s += f'<clipPath id="{cid}"><path d="{bd}"/></clipPath><g clip-path="url(#{cid})">{bands}</g>'
    s += f'<path d="{bd}" fill="none" {_st(3.6)}/>'
    # the hood round the face
    s += _ell(-40, -34, 31, 29, BABY_CLOTH, sw=3.4)
    s += _line("M-62,-50 Q-46,-66 -22,-58", w=1.8, col=shade(BABY_CLOTH, -0.14))
    # face (looking up toward the viewer)
    fx, fy = -36, -32
    s += _ell(fx, fy, 21, 20, BABY_SKIN, sw=3.0)
    s += f'<path d="M{fx - 12},{fy - 17} Q{fx - 4},{fy - 26} {fx + 4},{fy - 19} Q{fx + 1},{fy - 14} {fx - 4},{fy - 15} Z" fill="#4a3326" {_st(2.0)}/>'
    ck = mix(BABY_SKIN, P["cheek"], 0.85)
    s += _ell(fx - 11, fy + 6, 5.5, 3.5, ck, extra='opacity="0.85"') + _ell(fx + 12, fy + 6, 5.5, 3.5, ck, extra='opacity="0.85"')
    if awake:
        for ex in (fx - 7, fx + 7):
            s += _ell(ex, fy - 1, 3.1, 3.8, EYE) + f'<circle cx="{fmt(ex - 1)}" cy="{fmt(fy - 2.4)}" r="1.2" fill="{HI}"/>'
        s += _line(f"M{fx - 4},{fy + 9} Q{fx},{fy + 13} {fx + 4},{fy + 9}", w=2.2)
    else:
        for ex in (fx - 7, fx + 7):
            s += _line(f"M{fmt(ex - 4)},{fmt(fy - 1)} Q{fmt(ex)},{fmt(fy + 3)} {fmt(ex + 4)},{fmt(fy - 1)}", w=2.2)
        s += _line(f"M{fx - 3},{fy + 9} Q{fx},{fy + 11} {fx + 3},{fy + 9}", w=2.0)
    s += _ell(fx, fy + 4, 2.4, 1.8, shade(BABY_SKIN, -0.15))
    if awake or hand:            # a tiny hand peeking out of the swaddle by the chin
        s += _ell(fx + 22, fy + 18, 7, 6, BABY_SKIN, sw=2.6)
        s += _line(f"M{fx + 20},{fy + 14} l2,4 M{fx + 24},{fy + 14} l1,4", w=1.4)
    return s


BABY_STATES = ("in_manger", "held", "awake", "wrap")


def baby_jesus(x, y, scale=1.0, facing=1, state="in_manger", hand=False, glow=0.0, marks=True):
    """The newborn Jesus, swaddled in cloth bands (see module doc, 'NATIVITY FILM'). Head on the LEFT for facing=1."""
    if state not in BABY_STATES:
        raise ValueError(f"baby_jesus: unknown state {state!r}; choose from {BABY_STATES}")
    rot = -14 if state == "held" else 0
    s = ""
    if glow > 0:
        s += _glow_disc((0, -30), 130, 90, _clamp01(glow), "baby")
    s += f'<g transform="rotate({rot})">{_baby_svg(state, hand)}</g>' if rot else _baby_svg(state, hand)
    return _wrap_out(s, x, y, scale, facing, f"baby_jesus-{state}")


# ---------------------------------------------------------------- the toddler (Matthew 2: about one or two)
TODDLER_POSES = ("sit", "sit_reach", "sit_wave", "stand", "reach", "wave")
_TD = {
    "sit": _P(t=-2, lap=True, legs=((80, 18), (74, 12)), hem=0.97, flare=-4,
              arms=(("ik", "knee", 0, 0.45, 1), ("ik", "knee", 1, 0.45, 1)), hands=("open", "open"), expr="happy"),
    "sit_reach": _P(t=4, h=-6, lap=True, legs=((80, 18), (74, 12)), hem=0.97, flare=-4,
                    arms=(("fk", 76, 92), ("fk", 70, 86)), hands=("open", "open"), expr="amazed", look=(0.03, 0.0)),
    "sit_wave": _P(t=-2, h=-4, lap=True, legs=((80, 18), (74, 12)), hem=0.97, flare=-4,
                   arms=(("fk", 140, 160), ("ik", "knee", 1, 0.45, 1)), hands=("open", "open"), expr="laugh"),
    "stand": _P(legs=((6, 2), (-6, -2)), arms=(("fk", 22, 30), ("fk", -16, -22)), hands=("open", "open"), expr="happy"),
    "reach": _P(t=6, legs=((10, 3), (-8, -4)), arms=(("fk", 80, 96), ("fk", 74, 90)), hands=("open", "open"),
                expr="amazed"),
    "wave": _P(legs=((6, 2), (-6, -2)), arms=(("fk", 146, 166), ("fk", -16, -22)), hands=("open", "open"), expr="laugh"),
}
TODDLER_TUNIC = "#f3ecd9"


def _toddler_hat(R):
    """Soft dark baby curls."""
    col = "#3a2a20"
    circ = []
    for i in range(9):
        a = math.radians(-22 - i * 21)
        circ.append((R * 1.0 * math.cos(a) - 0.04 * R, R * 0.98 * math.sin(a) + 0.02 * R, (0.26 if i % 2 else 0.22) * R))
    circ += [(-0.15 * R, -0.62 * R, 0.42 * R), (-0.55 * R, -0.35 * R, 0.4 * R)]
    s = _union_circles(circ, col, 2.8)
    s += f'<circle cx="{fmt(0.48 * R)}" cy="{fmt(-0.66 * R)}" r="{fmt(0.13 * R)}" fill="{col}" {_st(2.2)}/>'
    for x, y, r in circ[:7]:
        s += _line(f"M{fmt(x - 0.4 * r)},{fmt(y)} Q{fmt(x)},{fmt(y - 0.6 * r)} {fmt(x + 0.4 * r)},{fmt(y - 0.1 * r)}", w=1.8,
                   col=shade(col, 0.3))
    return s + _ear(R, BABY_SKIN)


def _toddler_design():
    return dict(robe=TODDLER_TUNIC, sleeve=TODDLER_TUNIC, hem_col=shade(MARY_VEIL, 0.2), hem_w=4, skin=BABY_SKIN,
                leg=BABY_SKIN, hem=0.66, flare_k=0.9, sleeve_len=0.6, hair=None, hat=("custom", _toddler_hat), hat_h=0.12,
                ears=False, bare=True, neck_v=shade(MARY_VEIL, 0.2))


def _toddler_inner(pose, expr, phase, marks):
    ps = dict(_TD[pose])
    if pose in ("wave", "sit_wave"):
        f = 166 + 16 * math.sin(2 * math.pi * phase)
        ps["arms"] = (("fk", 146, f), ps["arms"][1])
    D = _toddler_design()
    saved = dict(_LAST)
    inner, bb = _figure(D, _TODDLER, ps, expr, 1, marks)
    if pose.startswith("sit"):
        sx, sy = _seat_point(_TODDLER)
        inner = _reanchor(inner, sx, sy)
    last = dict(_LAST)
    _LAST.clear()
    _LAST.update(saved)
    return inner, bb, last


def toddler_jesus(x, y, scale=1.0, facing=1, pose="sit", expr=None, phase=0.0, glow=0.0, marks=True):
    """Jesus at about one or two (Matthew 2:11), e.g. sitting on Mary's lap (see module doc, 'NATIVITY FILM')."""
    _check_js(pose, TODDLER_POSES, "toddler_jesus")
    expr = _nat_expr(expr, "toddler_jesus")
    e = expr or _TD[pose]["expr"]
    inner, bb, last = _toddler_inner(pose, e, phase, marks)
    _LAST.clear()
    _LAST.update(last)
    if glow > 0:
        inner = _glow_disc((0, -70), 150, 120, _clamp01(glow), "toddler") + inner
    return _wrap_out(inner, x, y, scale, facing, f"toddler_jesus-{pose}")


# ---------------------------------------------------------------- Joseph, Mary's husband (the carpenter)
def _joseph_c_hat(R):
    """Short dark wavy hair with a thin woven rust headband."""
    s = _hair_cap(R, JOSEPH_C_HAIR, "curly", front=-24, back=170, line=-0.40)
    s += _tube(_spline_pts([(0.98 * R, -0.42 * R), (0.45 * R, -0.62 * R), (-0.25 * R, -0.60 * R),
                            (-0.94 * R, -0.28 * R)]), 0.12 * R, JOSEPH_C_BAND, ow=2.4)
    for xx in (-0.55, -0.05, 0.45):
        s += _line(f"M{fmt(xx * R)},{fmt(-0.66 * R + (0.12 if xx < 0 else 0.04) * R * (1 if xx < -0.3 else 0))} l{fmt(0.05 * R)},{fmt(0.08 * R)}",
                   w=1.6, col=shade(JOSEPH_C_BAND, 0.4))
    return s + _ear(R, JOSEPH_C_SKIN)


def _cloak_stripes(st, polys):
    """Vertical stripes down Joseph's open cloak (cream and thin rust on warm brown)."""
    m, tp, pel, f = st["m"], st["tp"], st["pel"], st["f"]
    s = ""
    ww = m["ww"]
    for c0, w0, col in ((-0.86, 5.0, JOSEPH_C_STRIPE), (-0.70, 2.2, JOSEPH_C_BAND), (-0.50, 5.0, JOSEPH_C_STRIPE),
                        (0.70, 5.0, JOSEPH_C_STRIPE), (0.86, 2.2, JOSEPH_C_BAND)):
        for poly in polys:
            s += _poly(_band(poly, pel, f, c0 * ww - w0, c0 * ww + w0), col, sw=0)
    return s


def _joseph_c_design():
    D = dict(robe=JOSEPH_C_CLOAK, sleeve=JOSEPH_C_TUNIC, cuff=shade(JOSEPH_C_TUNIC, -0.2), skin=JOSEPH_C_SKIN,
             leg=JOSEPH_C_SKIN, hem=0.93, hem_col=shade(JOSEPH_C_CLOAK, -0.18), hem_w=9, hair=None,
             hat=("custom", _joseph_c_hat), hat_h=0.12, ears=False, beard=("carpenter", JOSEPH_C_HAIR),
             tunic=JOSEPH_C_TUNIC, rope_belt="#d9b46a", robe_deco=_cloak_stripes, sandal=SANDAL)
    return D


_JC_STAFF_ARM = ("fk", 40, 80)
_JCZ = {
    "stand": _P(arms=(("fk", 12, 6), _JC_STAFF_ARM), expr="warm"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -34, -24), _JC_STAFF_ARM), expr="warm"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 26, 40), _JC_STAFF_ARM), expr="kind"),
    "walk_c": _P(t=3, legs=((5, 1), (-8, -16)), arms=(("fk", 4, 8), _JC_STAFF_ARM), expr="kind"),
    "lead_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", 40, 70), ("fk", -40, -22)), hands=("fist", "fist"),
                 expr="kind"),
    "lead_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 40, 70), ("fk", -40, -22)), hands=("fist", "fist"),
                 expr="kind"),
    "knock": _P(t=4, h=-2, legs=((10, 3), (-8, -4)), arms=(("fk", 70, 150), _JC_STAFF_ARM), hands=("fist", "fist"),
                expr="kind"),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 86, 90), _JC_STAFF_ARM), hands=("point", "fist"), expr="kind"),
    "kneel": _P(t=-2, h=10, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)), hands=("none", "pray"),
                expr="tender", **_KNEEL),
    "watch": _P(t=6, h=14, legs=((8, 3), (-6, -3)), arms=(("ik", "abs", 74, -214, 1), ("ik", "abs", 66, -198, 1)),
                hands=("fist", "fist"), expr="tender"),
    "hold_lamp": _P(h=-4, arms=(("fk", 60, 128), _JC_STAFF_ARM), hands=("open", "fist"), expr="kind"),
    "sit": _P(t=-2, arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), expr="kind", **_SEAT),
    "talk": _P(h=-2, arms=(("fk", 30, 82), _JC_STAFF_ARM), hands=("open", "fist"), expr="kind"),
    "worry": _P(t=4, h=8, arms=(("ik", "head", 0.42, 1.05, 1), _JC_STAFF_ARM), hands=("fist", "fist"), expr="worried"),
    "cheer": dict(POSES["cheer"], expr="joyful"),
}
JOSEPH_CARPENTER_POSES = ("stand", "walk", "walk_a", "walk_b", "walk_c", "lead", "lead_a", "lead_b", "knock", "point",
                          "kneel", "watch", "hold_lamp", "sit", "talk", "worry", "cheer")
JOSEPH_CARPENTER_EXPRESSIONS = ("kind", "worried", "tender", "joyful", "tired", "happy", "awed", "peaceful")
JOSEPH_LEAD_HAND = (-72, -139)      # lead: the near fist holding the donkey's rope (anchor coords, scale 1, facing 1)
_JC_NO_STAFF = ("lead", "lead_a", "lead_b", "kneel", "watch", "sit", "worry", "cheer")


def _joseph_staff(D):
    def front(st):
        W, hr = st["arms"][1][2], st["m"]["hr"]
        top = st["Hc"][1] - 1.35 * st["m"]["R"]
        return _staff_line(W[0] + 1, top, st["ground"] - 3) + _fist(W, hr, D["skin"], 0.5)
    return front


def _watch_staff(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        x = (W0[0] + W1[0]) / 2 + 4
        return (_staff_line(x, min(W0[1], W1[1]) - 18, st["ground"] - 3) + _fist(W0, hr, D["skin"]) +
                _fist(W1, hr, D["skin"]))
    return front


def _lamp_in_hand(D, glow=1.0):
    def front(st):
        W, hr = st["arms"][0][2], st["m"]["hr"]
        s = _glow_disc((W[0] + 12, W[1] - 26), 130, 110, glow, "jlamp", P["glow"], LAMPLIGHT)
        s += f'<g transform="translate({fmt(W[0] - 4)},{fmt(W[1] - 6)}) scale(0.62)">{_prp()._oil_lamp(True, _clip_id("jl", round(W[0]), round(W[1])))}</g>'
        return s + _hand(W, (0.0, 1.0), "open", D["skin"], hr)
    return front


def _knock_marks(st):
    W = st["arms"][0][2]
    s = ""
    for k in (0, 1):
        r = 22 + 13 * k
        s += _line(f"M{fmt(W[0] + r * 0.7)},{fmt(W[1] - r * 0.7)} Q{fmt(W[0] + r * 1.05)},{fmt(W[1])} {fmt(W[0] + r * 0.7)},"
                   f"{fmt(W[1] + r * 0.7)}", w=2.8, col=MARK)
    return s


def joseph_carpenter(x, y, scale=1.0, facing=1, pose="stand", expr=None, phase=0.0, staff=True, lamp=1.0, marks=True):
    """Joseph of Nazareth, Mary's husband, a gentle carpenter (see module doc, 'NATIVITY FILM')."""
    _check_js(pose, JOSEPH_CARPENTER_POSES, "joseph_carpenter")
    expr = _nat_expr(expr, "joseph_carpenter")
    if pose == "walk":
        ps = _walk_phase_pose(_JCZ, phase)
    elif pose == "lead":
        ps = dict(_JCZ["lead_a" if (phase % 1.0) < 0.5 else "lead_b"])
    elif pose == "knock":
        ps = dict(_JCZ["knock"])
        ps["arms"] = (("fk", 70 + 8 * math.cos(2 * math.pi * phase), 150 - 14 * math.cos(2 * math.pi * phase)),
                      ps["arms"][1])
    else:
        ps = dict(_JCZ[pose])
    D = _joseph_c_design()
    fronts = []
    if pose == "watch":
        fronts.append(_watch_staff(D))
    elif staff and pose not in _JC_NO_STAFF:
        fronts.append(_joseph_staff(D))
    elif not staff and pose not in _JC_NO_STAFF:
        ps["arms"] = (ps["arms"][0], ("fk", -8, -3))
    if pose == "hold_lamp":
        fronts.append(_lamp_in_hand(D, _clamp01(lamp)))
    if pose == "knock" and marks and math.cos(2 * math.pi * phase) > 0.3:
        fronts.append(_knock_marks)
    D["front"] = _hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = _figure(D, _JOSEPH_C_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"joseph_carpenter-{pose}")


# ---------------------------------------------------------------- beards of this film (head frame)
_NATIVITY_BEARDS = ("carpenter", "elder_curl", "magus", "magus_short")


def _nativity_beard(R, col, kind):
    """'carpenter' Joseph's short, close-cropped rounded beard with a little texture; 'elder_curl' the old shepherd's
    soft curly white beard; 'magus' a long beard ending in two soft points (the old wise man); 'magus_short' a
    neat short pointed beard."""
    if kind == "carpenter":
        L = 1.04
        pts = [(-0.86 * R, -0.04 * R), (-0.90 * R, 0.50 * R), (-0.62 * R, (L - 0.14) * R), (-0.10 * R, (L + 0.02) * R),
               (0.30 * R, L * R), (0.66 * R, (L - 0.16) * R), (0.90 * R, 0.52 * R), (0.70 * R, 0.62 * R),
               (0.20 * R, 0.80 * R), (-0.30 * R, 0.70 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts, tension=0.85)}" fill="{col}" {_st(3.2)}/>'
        lite = shade(col, 0.28)
        for x0, y0 in ((-0.58, 0.55), (-0.30, 0.86), (0.05, 0.92), (0.40, 0.88), (-0.72, 0.20)):
            s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} q{fmt(0.05 * R)},{fmt(0.05 * R)} {fmt(0.10 * R)},0", w=1.8, col=lite)
        return s
    if kind == "elder_curl":
        circ = []
        for i in range(10):
            a = math.radians(180 - i * 20)
            cx, cy = 0.04 * R + 0.96 * R * math.cos(a) * 0.95, 0.45 * R + 0.96 * R * math.sin(a) * 0.9
            if cy < 0.0:
                continue
            circ.append((cx, cy, (0.25 if i % 2 else 0.22) * R))
        circ += [(-0.84 * R, 0.05 * R, 0.17 * R), (0.88 * R, 0.40 * R, 0.15 * R), (0.10 * R, 1.38 * R, 0.24 * R),
                 (-0.30 * R, 1.30 * R, 0.22 * R), (0.45 * R, 1.25 * R, 0.2 * R)]
        s = _union_circles(circ, col, 2.8)
        s += f'<path d="{smooth_path([(-0.62 * R, 0.25 * R), (-0.30 * R, 0.72 * R), (0.20 * R, 0.84 * R), (0.70 * R, 0.66 * R), (0.55 * R, 1.0 * R), (-0.40 * R, 1.0 * R)])}" fill="{col}"/>'
        for x, y, r in circ:
            s += _line(f"M{fmt(x - 0.45 * r)},{fmt(y + 0.1 * r)} Q{fmt(x - 0.15 * r)},{fmt(y - 0.6 * r)} {fmt(x + 0.4 * r)},"
                       f"{fmt(y - 0.2 * r)}", w=2.0, col=shade(col, -0.12))
        return s
    if kind in ("magus", "magus_short"):
        L = 1.85 if kind == "magus" else 1.38
        pts = [(-0.86 * R, -0.02 * R), (-0.92 * R, 0.58 * R), (-0.66 * R, 1.10 * R), (-0.22 * R, L * R),
               (0.02 * R, (L - 0.20) * R), (0.26 * R, (L + 0.02) * R), (0.62 * R, 1.12 * R), (0.92 * R, 0.55 * R),
               (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R), (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        if kind == "magus_short":
            pts = [(-0.86 * R, -0.02 * R), (-0.90 * R, 0.55 * R), (-0.52 * R, 1.02 * R), (0.10 * R, L * R),
                   (0.60 * R, 1.02 * R), (0.90 * R, 0.55 * R), (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R),
                   (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.18) if col != "#eeeae2" else "#cfc8bc"
        for x0, y0, x1, y1 in ((-0.50, 0.92, -0.30, L - 0.25), (0.00, 0.98, 0.04, L - 0.35), (0.40, 0.95, 0.28, L - 0.35)):
            s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} Q{fmt((x0 + 0.08) * R)},{fmt((y0 + y1) / 2 * R)} {fmt(x1 * R)},{fmt(y1 * R)}",
                       w=2.0, col=dark)
        return s
    return ""


# ---------------------------------------------------------------- the angels (Gabriel, the angel of the shepherds, the choir)
ANGEL_LOOKS = [
    dict(skin="#e9b892", hair="#b98240", style="long"),      # 0 Gabriel: honey-brown shoulder-length waves
    dict(skin="#c68a62", hair="#3a2618", style="curl"),
    dict(skin="#f0c4a0", hair="#dcae5a", style="long"),
    dict(skin="#9a6342", hair="#241b17", style="curl"),
    dict(skin="#dca57c", hair="#6a3f24", style="short"),
    dict(skin="#e2a882", hair="#c9874a", style="curl"),
]
_ANGEL_M = _metrics(_ADULT, 1.06, 0.92, th=70, sh=68, T=112)
ANGEL_POSES = ("stand", "float", "announce", "sing", "point_down", "wings_open", "bless", "kneel")
ANGEL_FLOAT_LIFT = 46       # float: the lowest toe hovers this far above the anchor (+- 6 px bob with phase)
_AZ = {
    "stand": _P(arms=(("fk", 22, 40), ("fk", -14, -24)), hands=("open", "open"), expr="warm"),
    "float": _P(h=-2, legs=((8, 14), (-4, 6)), feet=(64, 70), arms=(("fk", 44, 72), ("fk", -36, -58)),
                hands=("open", "open"), billow=16, expr="warm"),
    "announce": _P(h=-6, arms=(("fk", 146, 164), ("fk", 30, 72)), hands=("palm", "open"), expr="proclaim"),
    "sing": _P(h=-14, arms=(("fk", 118, 140), ("fk", -112, -136)), hands=("open", "open"), expr="sing",
               look=(0.02, -0.06)),
    "point_down": _P(h=8, arms=(("fk", 62, 50), ("fk", -14, -24)), hands=("point", "open"), expr="warm",
                     look=(0.04, 0.06)),
    "wings_open": _P(h=-4, arms=(("fk", 96, 114), ("fk", -92, -110)), hands=("open", "open"), expr="joyful"),
    "bless": _P(h=-4, arms=(("fk", 22, 40), ("fk", 80, 138)), hands=("open", "palm"), expr="warm"),
    "kneel": _P(t=-2, h=6, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)), hands=("none", "pray"),
                expr="peaceful", **_KNEEL),
}
_ANGEL_WINGS = {"stand": 0.45, "float": 0.8, "announce": 0.9, "sing": 0.75, "point_down": 0.7, "wings_open": 1.0,
                "bless": 0.6, "kneel": 0.25}


def _angel_hair(col, style):
    def hat(R):
        lite = shade(col, 0.34)
        if style == "long":
            pts = [(0.94 * R, -0.34 * R), (0.86 * R, -0.86 * R), (0.32 * R, -1.15 * R), (-0.42 * R, -1.12 * R),
                   (-1.00 * R, -0.74 * R), (-1.16 * R, -0.06 * R), (-1.16 * R, 0.60 * R), (-1.04 * R, 1.10 * R),
                   (-0.80 * R, 1.20 * R), (-0.74 * R, 0.84 * R), (-0.62 * R, 0.46 * R), (-0.58 * R, -0.02 * R),
                   (-0.30 * R, -0.42 * R), (0.20 * R, -0.50 * R), (0.56 * R, -0.42 * R)]
            s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
            for x0, y0, x1, y1 in ((0.20, -1.06, 0.62, -0.50), (-0.30, -0.96, -0.86, -0.30), (-0.66, -0.60, -1.02, 0.72),
                                   (-0.90, -0.10, -0.98, 1.06)):
                s += _line(f"M{fmt(x0 * R)},{fmt(y0 * R)} Q{fmt((x0 + x1) / 2 * R - 0.12 * R)},{fmt((y0 + y1) / 2 * R)} "
                           f"{fmt(x1 * R)},{fmt(y1 * R)}", w=2.0, col=lite)
            return s
        if style == "curl":
            circ = []
            for i in range(10):
                a = math.radians(-20 - i * 19)
                circ.append((1.02 * R * math.cos(a), 1.0 * R * math.sin(a) - 0.02 * R, (0.25 if i % 2 else 0.21) * R))
            circ += [(-0.2 * R, -0.62 * R, 0.45 * R), (-0.62 * R, -0.30 * R, 0.42 * R), (-0.9 * R, 0.18 * R, 0.22 * R)]
            s = _union_circles(circ, col, 2.8)
            for x, y, r in circ[:9]:
                s += _line(f"M{fmt(x - 0.4 * r)},{fmt(y)} Q{fmt(x)},{fmt(y - 0.6 * r)} {fmt(x + 0.4 * r)},{fmt(y - 0.1 * r)}",
                           w=1.8, col=lite)
            return s
        return _hair_cap(R, col, "short", front=-26, back=168, line=-0.40)
    return hat


def _wing_shape(L):
    """Wing outline in its own frame: root at (0, 0), spreading along +x, leading edge up (-y)."""
    lead = [(0.0, -0.10 * L), (0.18 * L, -0.40 * L), (0.46 * L, -0.60 * L), (0.78 * L, -0.66 * L), (1.0 * L, -0.54 * L)]
    trail = []
    tips = [(1.02 * L, -0.40 * L), (0.96 * L, -0.20 * L), (0.86 * L, -0.02 * L), (0.72 * L, 0.13 * L), (0.56 * L, 0.24 * L),
            (0.40 * L, 0.29 * L), (0.24 * L, 0.27 * L), (0.10 * L, 0.18 * L)]
    for i, p in enumerate(tips):
        trail.append(p)
        if i < len(tips) - 1:           # a notch between two rounded feather tips
            q = tips[i + 1]
            trail.append(((p[0] + q[0]) / 2 - 0.035 * L, (p[1] + q[1]) / 2 - 0.035 * L))
    return lead + trail + [(0.0, 0.06 * L)]


def _wing_svg(root, L, ang, mirror, col, feather, key):
    """One wing: frame rotated by ang degrees; mirror=-1 spreads it toward -x (the back of a figure facing +x)."""
    def tr(p):
        q = _rot((p[0] * mirror, p[1]), ang * mirror)
        return (root[0] + q[0], root[1] + q[1])
    outl = [tr(p) for p in _wing_shape(L)]
    d = smooth_path(outl, tension=0.7)
    cid = _clip_id("wing", key, round(root[0], 1), round(root[1], 1), round(ang, 2), mirror, round(L))
    inner = ""
    # soft gold warmth toward the tips
    inner += f'<path d="{smooth_path([tr(p) for p in ((0.55 * L, -0.7 * L), (1.2 * L, -0.6 * L), (1.1 * L, 0.2 * L), (0.6 * L, 0.35 * L))])}" fill="{mix(col, ANGEL_GOLD, 0.35)}" opacity="0.45"/>'
    # rows of small covert scallops near the leading edge
    for row, (r0, r1, n) in enumerate(((0.10, 0.74, 6), (0.16, 0.64, 5))):
        y = -0.38 * L + row * 0.21 * L
        d_ = ""
        for i in range(n):
            u0, u1 = r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n
            y0, y1 = (y + 0.14 * L * (u - r0) * (1 - row * 0.4) for u in (u0, u1))
            a, b = tr((u0 * L, y0)), tr((u1 * L, y1))
            c = tr(((u0 + u1) / 2 * L, (y0 + y1) / 2 + 0.075 * L))
            d_ += f"M{_pt(a)} Q{_pt(c)} {_pt(b)} "
        inner += _line(d_, w=2.0, col=feather)
    # long flight feathers: lines from the notches toward the root
    tips = _wing_shape(L)[5:-1]
    for i, p in enumerate(tips):
        if i % 2 == 1:
            a, b = tr(p), tr((p[0] * 0.55, p[1] * 0.55 - 0.08 * L))
            inner += _line(f"M{_pt(a)} L{_pt(b)}", w=2.0, col=feather)
    s = f'<path d="{d}" fill="{col}" {_st(3.6)}/>'
    s += f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{inner}</g>'
    s += f'<path d="{d}" fill="none" {_st(3.6)}/>'
    return s


def _angel_wings(spread, phase, key):
    def behind(st):
        m, tp = st["m"], st["tp"]
        L = 1.62 * m["T"]
        fl = 5 * math.sin(2 * math.pi * phase)
        a = -64 + 96 * spread + fl
        s = _wing_svg(tp(0.18 * m["ww"], m["T"] - 22), L * 0.80, a - 4, 1, shade(ANGEL_WING, -0.07),
                      shade(ANGEL_FEATHER, -0.08), key + "f")
        s += _wing_svg(tp(-0.42 * m["ww"], m["T"] - 26), L, a, -1, ANGEL_WING, ANGEL_FEATHER, key + "n")
        return s
    return behind


def _angel_glow(level, sparkles, phase):
    def behind(st):
        if level <= 0:
            return ""
        m, tp = st["m"], st["tp"]
        c = tp(0, 0.55 * m["T"])
        s = _glow_disc(c, 300, 340, level, "angel")
        if sparkles:
            for k, (dx, dy, r) in enumerate(((-150, -170, 11), (160, -120, 9), (-120, 40, 8), (150, 70, 10), (40, -250, 8),
                                             (-60, 150, 7))):
                tw = 0.65 + 0.35 * math.sin(2 * math.pi * (phase + k * 0.17))
                s += f'<g opacity="{min(1.0, level) * tw:.2f}">{_sparkle((c[0] + dx, c[1] + dy), r * (0.8 + 0.4 * tw))}</g>'
        return s
    return behind


def _angel_design(variant):
    lk = ANGEL_LOOKS[int(variant) % len(ANGEL_LOOKS)]
    D = dict(robe=ANGEL_ROBE, sleeve=ANGEL_ROBE, hem_col=ANGEL_GOLD, hem_w=8, cuff=ANGEL_GOLD, skin=lk["skin"],
             leg=lk["skin"], hem=1.02, flare_k=1.35, hair=None, hat=("custom", _angel_hair(lk["hair"], lk["style"])),
             hat_h=0.14, ears=False, sash=ANGEL_GOLD, sash_tail=True, neck_v=ANGEL_GOLD, bare=True)
    if lk["style"] == "long":
        D["long_hair"] = lk["hair"]
    return D


def angel(x, y, scale=1.0, facing=1, pose="stand", expr=None, variant=0, glow=0.7, wings=None, phase=0.0, lift=None,
          marks=True):
    """An angel of the Lord: a tall, gentle figure of light with soft wings (see module doc, 'NATIVITY FILM')."""
    _check_js(pose, ANGEL_POSES, "angel")
    expr = _nat_expr(expr, "angel")
    ps = dict(_AZ[pose])
    D = _angel_design(variant)
    spread = _clamp01(_ANGEL_WINGS[pose] if wings is None else wings)
    D["behind"] = _hooks(_angel_glow(_clamp01(glow), marks, phase), _angel_wings(spread, phase, f"a{variant}{pose}"))
    e = expr or ps["expr"]
    inner, _ = _figure(D, _ANGEL_M, ps, e, _fsign(facing), marks)
    if pose == "float":
        up = (ANGEL_FLOAT_LIFT if lift is None else lift) + 6 * math.sin(2 * math.pi * phase)
        inner = _reanchor(inner, 0, up)
    elif lift:
        inner = _reanchor(inner, 0, lift)
    return _wrap_out(inner, x, y, scale, facing, f"angel{int(variant) % len(ANGEL_LOOKS)}-{pose}")


ANGEL_CHOIR_POSES = ("sing", "announce", "wings_open", "sing", "float", "sing", "bless", "announce")


def angel_choir(x0, x1, y, n=9, phase=0.0, scale=0.36, rows=2, seed=0, glow=0.6, poses=None, depth=0.28):
    """The heavenly host (Luke 2:13): n smaller angels of light spread over the sky between x0 and x1 (absolute stage
    px), hovering on the line y (the front row's anchors; rows behind are higher and smaller, drawn first). Poses
    cycle through ANGEL_CHOIR_POSES (or the list `poses`); each angel's wings flutter at its own phase, the two halves
    face the middle. See module doc."""
    import random as _random
    rng = _random.Random(seed)
    rows = max(1, int(rows))
    per = max(1, -(-int(n) // rows))
    out = ""
    i = 0
    plist = list(poses) if poses else list(ANGEL_CHOIR_POSES)
    idx = list(range(int(n)))
    for r in reversed(range(rows)):
        grp = idx[r * per:(r + 1) * per]
        if not grp:
            continue
        k = scale * (1 - depth * r / max(1, rows - 1 if rows > 1 else 1))
        yr = y - r * 230 * scale
        for j, gi in enumerate(grp):
            u = (j + 0.5 + (0.5 if r % 2 else 0.0)) / (len(grp) + (0.5 if r % 2 else 0.0))
            px = x0 + (x1 - x0) * u + rng.uniform(-30, 30) * scale
            py = yr + rng.uniform(-50, 50) * scale - 90 * scale * math.sin(math.pi * u)
            p_ = plist[(gi + seed) % len(plist)]
            f_ = 1 if px < (x0 + x1) / 2 else -1
            v = 1 + (gi + seed) % 5
            out += angel(px, py, k * rng.uniform(0.92, 1.06), f_, pose=p_, variant=v, glow=glow,
                         phase=(phase + 0.23 * gi) % 1.0, lift=0, marks=True)
            i += 1
    return f'<g data-who="angel_choir">{out}</g>'


# ---------------------------------------------------------------- the shepherds (Luke 2:8-20)
_SHEPHERDS = [
    dict(tunic="#9a7b55", fleece="#efe5cf", skin="#d29a70", hair="#3a281d", beard=("stubble", "#3a281d"),
         hat=("headcloth", "#7a5d48", "#e8dcc0"), k=1.0, wide=1.02),
    dict(tunic="#7b6e64", fleece="#e9e0d0", skin="#dba783", hair="#e4ddd0", beard=("elder_curl", "#eeeae2"),
         hat=("headcloth", "#e6dcc6", "#6a5240"), k=0.97, wide=1.04, old=True),
    dict(tunic="#b5603e", fleece="#f2e9d6", skin="#e0a77c", hair="#3a2618", beard=None, hat=None, k=1.04, child=True),
    dict(tunic="#6f7d4a", fleece="#d6c3a0", skin="#9a6342", hair="#1f1915", beard=("short", "#1f1915"),
         hat=("headcloth", "#b5553a", "#e0b25a"), k=1.03, wide=1.12),
    dict(tunic="#c4a060", fleece="#7d5f45", skin="#c68a62", hair="#2a1d17", beard=None, hat=("headband", "#d9a03c"),
         k=1.02, wide=0.94),
    dict(tunic="#55607a", fleece="#e6dccb", skin="#cf9570", hair="#241b17", beard=("full", "#241b17"),
         hat=("headcloth", "#3f4f6a", "#c9a46a"), k=1.0, wide=1.05),
]
SHEPHERD_POSES = ("stand", "walk", "walk_a", "walk_b", "run", "run_a", "run_b", "sit", "sit_warm", "sleep", "shield_eyes",
                  "kneel", "point_up", "look_up", "hold_lamb", "cheer", "tell", "lean")
SHEPHERD_EXPRESSIONS = ("sleepy", "scared", "amazed", "joyful", "awed", "happy", "kind", "peaceful")
_CROOK_ARM = ("fk", 40, 80)
_SZ = {
    "stand": _P(arms=(("fk", 14, 8), _CROOK_ARM), expr="kind"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -34, -24), _CROOK_ARM), expr="kind"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 26, 40), _CROOK_ARM), expr="kind"),
    "run_a": dict(POSES["run_a"], expr="joyful"),
    "run_b": dict(POSES["run_b"], expr="joyful"),
    "sit": _P(t=-3, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)),
              expr="kind", **_SEATED),
    "sit_warm": _P(t=4, h=4, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=(("fk", 66, 98), ("fk", 58, 92)),
                   hands=("palm", "palm"), expr="kind", **_SEATED),
    "sleep": dict(POSES["sleep"]),
    "shield_eyes": _P(t=-14, h=-4, drop=10, legs=(("ik", 34, 1), ("ik", -44, 0)),
                      arms=(("ik", "head", 1.36, 0.02, 1), ("fk", -58, -34)), hands=("palm", "open"),
                      far_over_head=True, expr="scared"),
    "kneel": _P(t=-4, h=-14, arms=(("ik", "torso", 1.45, 0.62, 1), ("ik", "torso", 1.45, 0.62, 1)), hands=("none", "pray"),
                expr="awed", look=(0.02, -0.06), **_KNEEL),
    "point_up": _P(h=-18, legs=((5, 2), (-5, -2)), arms=(("fk", 134, 164), ("fk", -10, -4)), hands=("point", "fist"),
                   look=(0.03, -0.10), expr="amazed"),
    "look_up": _P(h=-24, legs=((6, 2), (-5, -2)), arms=(("fk", 30, 70), ("fk", -26, -60)), hands=("open", "open"),
                  look=(0.03, -0.10), expr="amazed"),
    "hold_lamb": _P(t=2, h=10, arms=(("ik", "torso", 2.3, 0.36, 1), ("ik", "torso", 0.9, 0.28, 1)), hands=("open", "open"),
                    expr="happy"),
    "cheer": dict(POSES["cheer"], expr="joyful"),
    "tell": _P(h=-4, legs=((10, 4), (-8, -3)), arms=(("fk", 96, 118), ("fk", -92, -114)), hands=("open", "open"),
               expr="joyful"),
    "lean": _P(t=8, h=12, legs=((8, 3), (-6, -3)), arms=(("ik", "torso", 2.6, 0.88, 1), ("ik", "torso", 2.3, 1.02, 1)),
               hands=("fist", "fist"), expr="kind"),
}
_SH_CROOK = ("stand", "walk_a", "walk_b")


def _fleece_mid(col, belt):
    """A sheepskin vest over the tunic: open at the front, shaggy lower edge, little wool curls; a cord belt."""
    def mid(st):
        m, tp, pel, f, u = st["m"], st["tp"], st["pel"], st["f"], st["u"]
        T, ww = m["T"], m["ww"]
        lo = -0.05 * T if st["mode"] == "seat" else -0.26 * T
        polys = []
        for poly in st["robe"]:
            b = _band(poly, pel, u, lo, T + 30)
            if len(b) > 2:
                b = _clip(b, _sub(pel, _mul(f, ww + 6)), f)
            if len(b) > 2:
                b = _clip(b, _add(pel, _mul(f, 0.36 * ww)), _mul(f, -1))
            if len(b) > 2:
                polys.append(b)
        if not polys:
            return ""
        circ = []
        edge = _band_edge(polys[-1], pel, u, lo + 1)
        if len(edge) == 2:
            a, b = edge
            n = max(3, int(_len(_sub(b, a)) / 9))
            for i in range(n + 1):
                c = _lerp(a, b, i / n)
                circ.append([(c[0] + 6 * math.cos(t_ * math.pi / 4), c[1] + 6 * math.sin(t_ * math.pi / 4)) for t_ in range(8)])
        s = _union(polys + circ, col, ow=3.0)
        cid = _clip_id("fleece", *[_d(p) for p in polys])
        tex = ""
        xs = [p[0] for pl in polys for p in pl]
        ys = [p[1] for pl in polys for p in pl]
        yy = min(ys) + 6
        row = 0
        while yy < max(ys):
            xx = min(xs) + (5 if row % 2 else 0)
            while xx < max(xs):
                tex += f"M{fmt(xx - 3)},{fmt(yy)} q3,-4 6,0 "
                xx += 11
            yy += 9
            row += 1
        s += (f'<clipPath id="{cid}">' + "".join(f'<path d="{_d(p)}"/>' for p in polys) + "</clipPath>"
              f'<g clip-path="url(#{cid})"><path d="{tex}" fill="none" {_st(1.6, shade(col, -0.22))} opacity="0.8"/></g>')
        for poly in polys[:1]:
            ch = _band_edge(poly, pel, f, 0.36 * ww - 1)
            if len(ch) == 2:
                s += _line(_d(ch, closed=False), w=3.0)
        bl = -3 if st["mode"] != "seat" else 6
        for poly in st["robe"][:2]:
            band = _band(poly, pel, u, bl, bl + 8)
            if len(band) > 2:
                band = _clip(band, _sub(pel, _mul(f, ww + 3)), f)
            if len(band) > 2:
                band = _clip(band, _add(pel, _mul(f, ww + 3)), _mul(f, -1))
            if len(band) > 2:
                s += _poly(band, belt, sw=2.2)
        return s
    return mid


def _shepherd_design(v):
    d = _SHEPHERDS[v]
    t = d["tunic"]
    D = dict(robe=t, sleeve=t, hem_col=shade(t, -0.2), hem_w=8, skin=d["skin"], leg=d["skin"], hem=0.62 if not d.get("old") else 0.80,
             flare_k=0.9, sleeve_len=0.75, hair=d["hair"], hair_style="curly", beard=d["beard"], neck_v=shade(t, 0.22),
             sandal=SANDAL)
    if d.get("hat"):
        hat = d["hat"]
        if hat[0] == "headcloth":
            D.update(hat=hat, tail=(hat[1], hat[2]), ears=False)
        else:
            D["hat"] = hat
    if d.get("old"):
        D.update(brow_w=4.6, brow_col="#a39a90")
    if d.get("child"):
        m = _metrics(_CHILD, d["k"], 1.0)
        D.update(hem=0.6, sleeve_len=0.6, hat=("custom", _curly_hat(d["hair"], d["skin"])), hat_h=0.12, ears=False)
    else:
        m = _metrics(_ADULT, d["k"], d.get("wide", 1.0))
    D["mid"] = _fleece_mid(d["fleece"], "#8a6a45")
    return D, m


def _curly_hat(col, skin):
    def hat(R):
        circ = []
        for i in range(9):
            a = math.radians(-22 - i * 21)
            circ.append((1.0 * R * math.cos(a) - 0.04 * R, 0.98 * R * math.sin(a) + 0.02 * R, (0.25 if i % 2 else 0.21) * R))
        circ += [(-0.15 * R, -0.62 * R, 0.42 * R), (-0.55 * R, -0.35 * R, 0.4 * R)]
        s = _union_circles(circ, col, 2.8)
        for x, y, r in circ[:7]:
            s += _line(f"M{fmt(x - 0.4 * r)},{fmt(y)} Q{fmt(x)},{fmt(y - 0.6 * r)} {fmt(x + 0.4 * r)},{fmt(y - 0.1 * r)}",
                       w=1.8, col=shade(col, 0.3))
        return s + _ear(R, skin)
    return hat


def _crook_front(D):
    def front(st):
        W, R = st["arms"][1][2], st["m"]["R"]
        return _crook(W[0] + 2, st["Hc"][1] - 1.5 * R, st["ground"] - 4) + _fist(W, st["m"]["hr"], D["skin"], 0.5)
    return front


def _lean_crook(D):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        x = (W0[0] + W1[0]) / 2 + 2
        return (_crook(x, min(W0[1], W1[1]) - 6, st["ground"] - 4, hook=-1) + _fist(W0, hr, D["skin"]) +
                _fist(W1, hr, D["skin"]))
    return front


def _lamb_front(D, k, variant=0):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        c = ((W0[0] + W1[0]) / 2 + 4, (W0[1] + W1[1]) / 2 + 14 * k)
        s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) scale({k})">{_prp()._sheep(variant, "stand", True)}</g>'
        return s + _hand(W1, (0.3, 1.0), "open", D["skin"], hr) + _hand(W0, (-0.2, 1.0), "open", D["skin"], hr)
    return front


def shepherds(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, phase=0.0, crook=True, lamb=True,
              marks=True):
    """The shepherds in the fields near Bethlehem (see module doc, 'NATIVITY FILM'). shepherd() is the same function."""
    v = int(variant) % len(_SHEPHERDS)
    _check_js(pose, SHEPHERD_POSES, "shepherds")
    expr = _nat_expr(expr, "shepherds")
    if pose == "walk":
        pose = "walk_a" if (phase % 1.0) < 0.5 else "walk_b"
    elif pose == "run":
        pose = "run_a" if (phase % 1.0) < 0.5 else "run_b"
    ps = dict(_SZ[pose])
    D, m = _shepherd_design(v)
    d = _SHEPHERDS[v]
    fronts = []
    if pose in _SH_CROOK:
        if crook:
            fronts.append(_crook_front(D))
        else:
            ps["arms"] = (ps["arms"][0], ("fk", -8, -3))
    elif pose == "lean":
        fronts.append(_lean_crook(D))
    elif pose == "hold_lamb" and lamb:
        fronts.append(_lamb_front(D, 0.46 if d.get("child") else 0.6, v % 4))
    if d.get("old") and pose in ("stand", "walk_a", "walk_b", "lean"):
        ps["t"] = ps["t"] + 6
    D["front"] = _hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"shepherd{v}-{pose}")


shepherd = shepherds


# ---------------------------------------------------------------- the wise men from the East (Matthew 2:1-11)
WISE_MEN_NAMES = ("Melchior", "Caspar", "Balthasar")      # traditional names only (Matthew gives no names or number)
_MAGI = [
    dict(skin="#efc4a0", hair="#e9e4dc", beard=("magus", "#eeeae2"), robe="#9b2f3c", pat=("#efc35a", "dots"),
         cape="#e0a944", hat="crown_cloth", k=0.99, wide=1.04, old=True, gift="gold"),
    dict(skin="#d39a6c", hair="#5a3a24", beard=("stubble", "#5a3a24"), robe="#2f6e5a", pat=("#e8c25a", "diamond"),
         cape="#c9a24a", hat="turban", k=1.03, wide=0.98, gift="frankincense"),
    dict(skin="#7a4a30", hair="#1f1915", beard=("magus_short", "#1f1915"), robe="#5b3a8a", pat=("#f0c75a", "flower"),
         cape="#c4572f", hat="crown_tall", k=1.02, wide=1.08, gift="myrrh"),
]
WISE_MEN_POSES = ("stand", "walk", "walk_a", "walk_b", "ride", "point_up", "look_up", "study", "carry_gift", "present",
                  "kneel_offer", "bow")
WISE_MEN_EXPRESSIONS = ("kind", "awed", "amazed", "joyful", "thoughtful", "peaceful", "happy")


def _magus_hat(kind, skin):
    def hat(R):
        if kind == "crown_cloth":       # a cream head-cloth under a five-pointed gold crown with jewels
            s = _cloth_cap(R, "#f3ead6", edge=GOLD)
            pts = [(-0.86 * R, -0.50 * R), (-0.84 * R, -1.05 * R), (-0.62 * R, -0.80 * R), (-0.38 * R, -1.30 * R),
                   (-0.10 * R, -0.92 * R), (0.18 * R, -1.38 * R), (0.44 * R, -0.92 * R), (0.70 * R, -1.28 * R),
                   (0.86 * R, -0.86 * R), (0.98 * R, -1.10 * R), (0.98 * R, -0.58 * R), (0.10 * R, -0.70 * R)]
            s += f'<path d="M{"L".join(_pt(p) for p in pts)} Z" fill="{GOLD}" {_st(3.0)}/>'
            s += _line(f"M{fmt(-0.86 * R)},{fmt(-0.62 * R)} Q{fmt(0.10 * R)},{fmt(-0.80 * R)} {fmt(0.98 * R)},{fmt(-0.70 * R)}",
                       w=2.4, col=GOLD_DARK)
            for (xx, yy, col) in ((-0.38, -1.30, "#c43c46"), (0.18, -1.38, "#3f6fc0"), (0.70, -1.28, "#c43c46")):
                s += f'<circle cx="{fmt(xx * R)}" cy="{fmt(yy * R)}" r="{fmt(0.08 * R)}" fill="{col}" {_st(1.8)}/>'
            for (xx, col) in ((-0.40, "#3c9a74"), (0.10, "#c43c46"), (0.60, "#3f6fc0")):
                s += f'<circle cx="{fmt(xx * R)}" cy="{fmt(-0.70 * R + abs(xx - 0.1) * 0.05 * R)}" r="{fmt(0.07 * R)}" fill="{col}" {_st(1.6)}/>'
            return s
        if kind == "turban":            # a tall cream-and-gold turban with a green jewel and a little plume
            s = _turban(R, "#f0e2bc", "#3c9a74")
            s += _tube(_spline_pts([(0.62 * R, -1.40 * R), (0.70 * R, -1.80 * R), (0.46 * R, -2.08 * R)], steps=4), 0.12 * R,
                       "#e9c35c", ow=2.2)
            s += _line(f"M{fmt(-0.98 * R)},{fmt(-0.70 * R)} Q{fmt(0.0)},{fmt(-1.10 * R)} {fmt(1.0 * R)},{fmt(-0.66 * R)}", w=3.0,
                       col=GOLD)
            return s
        # crown_tall: a tall rounded cap in warm orange-red with a gold crown band, pearls and a jewel
        cap = [(0.95 * R, -0.42 * R), (0.98 * R, -1.10 * R), (0.70 * R, -1.62 * R), (0.10 * R, -1.80 * R),
               (-0.52 * R, -1.66 * R), (-0.92 * R, -1.18 * R), (-1.02 * R, -0.40 * R), (-0.40 * R, -0.54 * R),
               (0.30 * R, -0.58 * R)]
        s = f'<path d="{smooth_path(cap)}" fill="#c4572f" {_st(3.4)}/>'
        s += _line(f"M{fmt(-0.52 * R)},{fmt(-1.50 * R)} Q{fmt(0.10 * R)},{fmt(-1.66 * R)} {fmt(0.70 * R)},{fmt(-1.46 * R)}",
                   w=2.2, col=shade("#c4572f", 0.3))
        s += _tube(_spline_pts([(1.0 * R, -0.52 * R), (0.40 * R, -0.70 * R), (-0.35 * R, -0.66 * R),
                                (-1.02 * R, -0.46 * R)]), 0.26 * R, GOLD, ow=2.6)
        for xx in (-0.70, -0.30, 0.10, 0.50, 0.86):
            s += f'<circle cx="{fmt(xx * R)}" cy="{fmt(-0.66 * R - (0.04 if -0.4 < xx < 0.6 else 0) * R)}" r="{fmt(0.05 * R)}" fill="#fbf3e0"/>'
        s += _ell(0.62 * R, -0.98 * R, 0.13 * R, 0.16 * R, "#3f6fc0", sw=2.2)
        s += f'<circle cx="{fmt(0.10 * R)}" cy="{fmt(-1.84 * R)}" r="{fmt(0.12 * R)}" fill="{GOLD}" {_st(2.2)}/>'
        return s
    return hat


def _magi_design(v):
    d = _MAGI[v]
    robe = d["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=GOLD, hem_w=12, cuff=GOLD, skin=d["skin"], leg=d["skin"], hem=0.98,
             flare_k=1.15, hair=d["hair"], hair_style="short", beard=d["beard"], hat=("custom", _magus_hat(d["hat"], d["skin"])),
             hat_h={"crown_cloth": 0.40, "turban": 1.10, "crown_tall": 0.86}[d["hat"]], ears=False, sash=GOLD, sash_tail=True,
             pattern=(d["pat"][0], d["pat"][1], 22), collar=GOLD, sandal=GOLD_DARK)
    if d["hat"] == "crown_cloth":
        D["tail"] = ("#f3ead6", GOLD)
    if d.get("old"):
        D.update(brow_w=4.4, brow_col="#b0a89e")
    m = _metrics(_ADULT, d["k"], d["wide"])
    return D, m


_MZ = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3)), expr="kind"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -30, -20), ("fk", 22, 36)), expr="kind"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 26, 40), ("fk", -20, -12)), expr="kind"),
    "ride": _P(t=-2, lap=True, legs=((62, -2), (56, -6)), hem=0.97, flare=-6,
               arms=(("ik", "body", 52, -30, 1), ("ik", "body", 40, -24, 1)), hands=("fist", "fist"), expr="kind"),
    "point_up": _P(h=-20, legs=((5, 2), (-5, -2)), arms=(("fk", 140, 166), ("fk", -10, -4)), hands=("point", "fist"),
                   look=(0.03, -0.10), expr="awed"),
    "look_up": _P(h=-24, arms=(("fk", 24, 56), ("fk", -20, -48)), hands=("open", "open"), look=(0.03, -0.10), expr="amazed"),
    "study": _P(h=16, arms=(("ik", "torso", 2.1, 0.52, 1), ("ik", "torso", 0.6, 0.46, 1)), hands=("fist", "fist"),
                look=(0.03, 0.07), expr="thoughtful"),
    "carry_gift": _P(t=2, h=6, arms=(("ik", "torso", 1.9, 0.42, 1), ("ik", "torso", 1.2, 0.34, 1)), hands=("open", "open"),
                     expr="kind"),
    "present": _P(t=12, h=8, legs=((10, 3), (-8, -3)), arms=(("fk", 60, 78), ("fk", 66, 84)), hands=("open", "open"),
                  expr="joyful"),
    "kneel_offer": _P(t=8, h=4, arms=(("ik", "torso", 3.0, 0.42, 1), ("ik", "torso", 2.4, 0.34, 1)), hands=("open", "open"),
                      expr="joyful", **_KNEEL),
    "bow": _P(t=60, h=28, arms=(("ik", "abs", 132, -6, 1), ("ik", "abs", 116, -6, 1)), hands=("ground", "ground"),
              expr="peaceful", **_KNEEL),
}
_GIFT_HELD = {"carry_gift": 0.62, "present": 0.66, "kneel_offer": 0.66}


def _star_chart_svg():
    """An open star chart: parchment with dotted constellations and one big new star (local centre (0, 0))."""
    s = _poly([(-62, -40), (62, -40), (66, 40), (-62, 40)], PARCH, sw=3.4)
    for x0, x1 in ((-72, -56), (56, 72)):
        s += f'<rect x="{x0}" y="-48" width="{x1 - x0}" height="96" rx="7" fill="{PARCH_ROLL}" {_st(3.0)}/>'
    for pts in (((-44, -22), (-30, -10), (-36, 8), (-18, 18)), ((6, -26), (22, -16), (36, -24), (30, 0)), ((10, 14), (24, 26))):
        s += _line(_d(pts, closed=False), w=1.6, col=P["ink_soft"], extra='stroke-dasharray="3 3"')
        for p in pts:
            s += f'<circle cx="{p[0]}" cy="{p[1]}" r="2.6" fill="{P["ink_soft"]}"/>'
    s += _sparkle((-4, -4), 11, "#e8b33c", 1.4)
    s += _line("M-50,32 L-20,32 M-12,32 L20,32", w=1.6, col=P["ink_soft"], extra='opacity="0.7"')
    return s


def _magi_items(D, pose, gift_kind, gift_open, gift_glow):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        skin = D["skin"]
        if pose == "study":
            c = ((W0[0] + W1[0]) / 2, (W0[1] + W1[1]) / 2 - 4)
            ang = _ang(_sub(W0, W1))
            s = f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate({fmt(ang)}) scale(0.62)">{_star_chart_svg()}</g>'
            return s + _fist(W0, hr, skin) + _fist(W1, hr, skin)
        k = _GIFT_HELD[pose]
        c = ((W0[0] + W1[0]) / 2, max(W0[1], W1[1]) + 10 * k)
        s = (f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) scale({k})">'
             f'{_prp()._gift(gift_kind, gift_open, gift_glow)}</g>')
        return s + _hand(W1, (0.25, 1.0), "open", skin, hr) + _hand(W0, (-0.2, 1.0), "open", skin, hr)
    return front


def wise_men(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, phase=0.0, gift=None, gift_open=0.0,
             gift_glow=0.0, marks=True):
    """The wise men (magi) from the East (see module doc, 'NATIVITY FILM'). wise_man() is the same function."""
    v = int(variant) % len(_MAGI)
    _check_js(pose, WISE_MEN_POSES, "wise_men")
    expr = _nat_expr(expr, "wise_men")
    if pose == "walk":
        pose = "walk_a" if (phase % 1.0) < 0.5 else "walk_b"
    ps = dict(_MZ[pose])
    D, m = _magi_design(v)
    d = _MAGI[v]
    gk = gift or d["gift"]
    if gk not in _prp().GIFT_KINDS:
        raise ValueError(f"wise_men: unknown gift {gk!r}; choose from {_prp().GIFT_KINDS}")
    D["behind"] = _mantle_drape(d["cape"])
    if pose in _GIFT_HELD or pose == "study":
        D["front"] = _magi_items(D, pose, gk, _clamp01(gift_open), _clamp01(gift_glow))
    if d.get("old") and pose in ("stand", "walk_a", "walk_b"):
        ps["t"] = ps["t"] + 4
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    if pose == "ride":
        sx, sy = _seat_point(m)
        inner = _reanchor(inner, sx, sy)
    return _wrap_out(inner, x, y, scale, facing, f"wise_man{v}-{pose}")


wise_man = wise_men


# ---------------------------------------------------------------- the people of Bethlehem (and the herald of the decree)
TOWNSFOLK_KINDS = ("man", "woman", "child", "elder", "traveller", "traveller_woman", "innkeeper", "herald")
TOWNSFOLK_POSES = ("stand", "walk", "walk_a", "walk_b", "talk", "point", "wave", "cheer", "listen", "sit", "carry",
                   "carry_walk_a", "carry_walk_b", "squeeze", "look_around", "shake_head", "read", "announce", "hold_lamp",
                   "sleep")
TOWNSFOLK_ITEMS = ("bundle", "sack", "basket", "jar", "hen", "pots", None)
_TF = [   # robe, trim / embroidery, skin, hair, cloth (head-cloth / veil)
    dict(robe="#4a5a8a", trim="#d9a03c", skin="#d9a37a", hair="#2f2420", cloth="#efe4cc"),
    dict(robe="#a8503a", trim="#e8d6aa", skin="#c68a62", hair="#241b17", cloth="#2f3a5e"),
    dict(robe="#c9a46a", trim="#7a3a3a", skin="#e2a882", hair="#4a2f1f", cloth="#f2e8d4"),
    dict(robe="#7a4a6a", trim="#e0b25a", skin="#a46b47", hair="#1f1915", cloth="#d9c9a0"),
    dict(robe="#6f7a48", trim="#efe0c0", skin="#dca57c", hair="#3a2618", cloth="#a8503a"),
    dict(robe="#3f6f78", trim="#e9c35c", skin="#cf9570", hair="#2a201b", cloth="#ead9b6"),
]
_BETH_DRESS = ("#2f3a5e", "#7a2e36", "#3a2e2a", "#2f4a3a", "#4b3a6a", "#6a3a2a")
_EMB_RED = "#c9483c"
_EMB_GOLD = "#e3b44f"


def _embroidery(st, polys):
    """Bethlehem dress: a cross-stitched chest panel and a stitched band above the hem (red and gold)."""
    m, tp, pel, f, u = st["m"], st["tp"], st["pel"], st["f"], st["u"]
    s = ""
    T, ww = m["T"], m["ww"]
    panel = [tp(-0.15 * ww, T - 4), tp(0.82 * ww, T - 6), tp(0.82 * ww, 0.45 * T), tp(-0.15 * ww, 0.45 * T)]
    s += _poly(panel, _EMB_RED, sw=2.2)
    for j in range(3):
        for i in range(4):
            c = tp((-0.02 + 0.22 * i) * ww, (0.55 + 0.14 * j) * T)
            s += _poly([(c[0], c[1] - 4), (c[0] + 4, c[1]), (c[0], c[1] + 4), (c[0] - 4, c[1])], _EMB_GOLD, sw=0)
    Hm, um = st["Hm"], st["um"]
    for poly in polys[-1:]:
        s += _poly(_band(poly, Hm, um, -30, -18), _EMB_RED, sw=0)
        b = _band(poly, Hm, um, -27, -21)
        s += _poly(b, _EMB_GOLD, sw=0)
    return s


def _townsfolk_design(kind, variant):
    v = int(variant) % 6
    c = _TF[v]
    robe = c["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.2), hem_w=9, cuff=shade(robe, -0.2), skin=c["skin"],
             leg=c["skin"], hem=0.92, flare_k=1.0, hair=c["hair"], hair_style="curly", sandal=SANDAL)
    m = _ADULT
    if kind in ("man", "traveller"):
        D.update(beard=(("full", "short", "fisher", "trim", "stubble", "carpenter")[v], c["hair"]), rope_belt=c["trim"])
        if v % 3 != 1:
            D.update(hat=("headcloth", c["cloth"], "#2a2420"), tail=(c["cloth"], None), ears=False)
        else:
            D.update(hat=("wrap", c["cloth"], c["trim"]))
        if kind == "traveller":
            D.update(robe=shade(robe, -0.06), hem=0.86, robe_deco=_dust_deco(v))
        m = _metrics(_ADULT, 1.0 + 0.015 * (v % 3 - 1), 1.0 + 0.05 * (v % 2))
    elif kind in ("woman", "traveller_woman"):
        dress = _BETH_DRESS[v]
        veil = ("#f2ead8", "#efe4cc", "#e8d8b8", "#f4ecdc", "#ead9c4", "#f0e2c8")[v]
        D.update(robe=dress, sleeve=dress, hem_col=shade(dress, -0.15), cuff=_EMB_RED, hat=("veil", veil, shade(veil, -0.2)),
                 veil=veil, ears=False, hair_style="short", robe_deco=_embroidery, sash=_EMB_GOLD, sash_tail=True)
        m = _metrics(_ADULT, 0.95, 0.92)
    elif kind == "child":
        girl = v % 2 == 1
        D.update(hem=0.6, flare_k=0.9, sleeve_len=0.55, rope_belt=c["trim"], hair_style="short" if girl else "curly")
        if girl:
            D.update(ponytail=c["hair"], ribbon=_EMB_RED, robe=_BETH_DRESS[v], sleeve=_BETH_DRESS[v], cuff=_EMB_RED)
        m = _CHILD
    elif kind == "elder":
        D.update(hair="#e4ddd0", beard=("white", "#ece6da"), shawl=c["trim"], shawl_trim=shade(c["trim"], -0.25), brow_w=4.6,
                 brow_col="#9a9088")
        if v % 2:
            D.update(hat=("wrap", c["cloth"], shade(c["cloth"], -0.25)))
        m = _metrics(_ADULT, 0.97, 1.0)
    elif kind == "innkeeper":        # plump and friendly: rust robe, cream apron, bald with a grey fringe, big moustache
        D.update(robe="#9c4a32", sleeve="#9c4a32", hem_col=shade("#9c4a32", -0.2), cuff="#e8dcc0", hair=None,
                 hat=("custom", _innkeeper_head), hat_h=0.06, ears=False, beard=("captain", "#8a8079"), skin="#d99a72",
                 leg="#d99a72", tunic="#f1e6cc", rope_belt="#6a4a30")
        m = _metrics(_ADULT, 0.98, 1.32)
    elif kind == "herald":           # the emperor's herald: white tunic, red cloak, laced sandals, a scroll
        D.update(robe="#f1e9d6", sleeve="#f1e9d6", hem=0.60, flare_k=0.8, sleeve_len=0.5, hem_col="#b8473c", hem_w=7,
                 beard=None, hair="#3a2a22", hair_style="short", sash="#b8473c", sash_tail=False, skin="#e0a67e",
                 leg="#e0a67e", neck_v=shade("#f1e9d6", -0.12))
        m = _metrics(_ADULT, 1.02, 1.0)
    return D, m


def _innkeeper_head(R):
    s = _aged(R, "#d99a72")
    s += f'<path d="{smooth_path([(-0.78 * R, -0.36 * R), (-1.06 * R, -0.05 * R), (-0.98 * R, 0.42 * R), (-0.70 * R, 0.40 * R), (-0.62 * R, -0.02 * R)])}" fill="#a39a92" {_st(2.8)}/>'
    s += _line(f"M{fmt(-0.30 * R)},{fmt(-0.86 * R)} Q{fmt(0.10 * R)},{fmt(-0.96 * R)} {fmt(0.40 * R)},{fmt(-0.84 * R)}", w=2.4,
               col=HI, extra='opacity="0.6"')
    return s + _ear(R, "#d99a72")


def _red_cloak(st):
    """The herald's red cloak pinned at the far shoulder, falling down his back."""
    return _mantle_drape("#b8473c")(st)


_TZ = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3)), expr="happy"),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -36, -26), ("fk", 24, 40)), expr="happy"),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 26, 42), ("fk", -22, -12)), expr="happy"),
    "talk": _P(h=-2, arms=(("fk", 12, 6), ("fk", 30, 82)), hands=("fist", "open"), expr="happy"),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 14, 8), ("fk", 88, 92)), hands=("fist", "point"), expr="happy"),
    "cheer": dict(POSES["cheer"], expr="joyful"),
    "listen": _P(h=-8, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), expr="kind", look=(0.03, -0.04)),
    "sit": _P(t=-3, legs=(("ik", 80, 1), ("ik", 90, 1)), arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)),
              expr="happy", **_SEATED),
    "squeeze": _P(t=-2, h=4, legs=((4, 1), (-4, -1)), arms=(("fk", 166, 176), ("fk", -164, -176)), hands=("open", "open"),
                  expr="surprised"),
    "look_around": _P(h=-12, legs=((6, 2), (-5, -2)), arms=(("ik", "torso", 1.0, 0.0, -1), ("ik", "torso", -1.0, 0.0, 1)),
                      hands=("fist", "fist"), expr="puzzled", look=(0.04, -0.05)),
    "read": _P(h=14, arms=(("ik", "torso", 2.3, 0.55, 1), ("ik", "torso", 0.6, 0.50, 1)), hands=("fist", "fist"),
               look=(0.03, 0.07), expr="neutral"),
    "announce": _P(t=-3, h=-6, arms=(("fk", 112, 150), ("fk", 70, 120)), hands=("fist", "fist"), expr="call"),
    "hold_lamp": _P(h=-4, arms=(("fk", 60, 128), ("fk", -8, -3)), hands=("open", "fist"), expr="kind"),
    "sleep": dict(POSES["sleep"]),
}


def _shake_pose(phase):
    a = 9 * math.sin(2 * math.pi * phase)
    return _P(t=2, h=a, legs=((6, 2), (-5, -2)), arms=(("fk", 40, 116), ("fk", -26, -100)), hands=("palm", "palm"),
              expr="sorry", marks=("shake",))


def _tf_items(D, pose, item, phase):
    """Hooks for held / carried things (behind, mid, front)."""
    PRm = _prp()
    behind = mid = front = None
    if pose in ("carry", "carry_walk_a", "carry_walk_b", "squeeze"):
        if item == "bundle" and pose != "squeeze":
            def behind(st):           # a cloth bundle on the back, its knot at the near shoulder
                m, tp = st["m"], st["tp"]
                c = tp(-1.05 * m["ww"], 0.70 * m["T"])
                col = "#c9a46a"
                body = smooth_path([(c[0] - 34, c[1] - 30), (c[0] + 10, c[1] - 42), (c[0] + 26, c[1] - 6), (c[0] + 16, c[1] + 40),
                                    (c[0] - 30, c[1] + 44), (c[0] - 46, c[1] + 6)])
                s_ = f'<path d="{body}" fill="{col}" {_st(3.4)}/>'
                s_ += _line(f"M{fmt(c[0] - 34)},{fmt(c[1] + 2)} Q{fmt(c[0] - 10)},{fmt(c[1] + 12)} {fmt(c[0] + 18)},{fmt(c[1] + 4)}",
                            w=2.2, col=shade(col, -0.25))
                s_ += _ell(c[0] + 8, c[1] - 36, 9, 7, shade(col, -0.1), sw=2.6)
                return s_

            def mid(st):
                m, tp = st["m"], st["tp"]
                return _tube([st["S"][1], tp(0.2 * m["ww"], 0.45 * m["T"]), tp(0.85 * m["ww"], 0.05 * m["T"])], 5,
                             "#8a6a45", ow=2.2)
        elif item in ("hen", "pots") or pose == "squeeze":
            def front(st):
                W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
                c = ((W0[0] + W1[0]) / 2, min(W0[1], W1[1]) - 4)
                it = item or "bundle"
                if it == "pots":
                    s_ = f'<g transform="translate({fmt(c[0])},{fmt(c[1] + 4)}) scale(0.62)">{_pot_stack()}</g>'
                elif it == "hen":
                    s_ = f'<g transform="translate({fmt(c[0])},{fmt(c[1] + 6)}) scale(0.7)">{_hen_basket(phase)}</g>'
                else:
                    s_ = f'<g transform="translate({fmt(c[0])},{fmt(c[1] + 8)}) scale(0.55)">{PRm._sack(1.0, "#c9a46a", 2)}</g>'
                return s_ + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
        else:
            b, mi, fr = _nh_items(D, "carry", 0.0, item, False, False, False)
            behind, mid, front = b, mi, fr
    elif pose == "read" or pose == "announce":
        def front(st):
            W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
            c = ((W0[0] + W1[0]) / 2, (W0[1] + W1[1]) / 2)
            ang = _ang(_sub(W0, W1))
            s_ = (f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) rotate({fmt(ang)}) scale({0.36 * _len(_sub(W0, W1)) / 60:.3f},0.5)">'
                  f'{PRm._scroll(True)}</g>')
            return s_ + _fist(W0, hr, D["skin"]) + _fist(W1, hr, D["skin"])
    elif pose == "hold_lamp":
        front = _lamp_in_hand(D, 1.0)
    return behind, mid, front


def _pot_stack():
    """A wobbly comic stack of clay pots and bowls (anchor bottom centre)."""
    s = ""
    y = 0
    for i, (w, h, col) in enumerate(((60, 40, "#c9714a"), (44, 34, "#d98a5a"), (52, 22, "#b8603e"), (30, 30, "#e0a070"))):
        dx = (-4, 5, -3, 4)[i]
        s += f'<path d="M{dx - w / 2},{y - h} Q{dx - w / 2 - 6},{y - h * 0.3} {dx - w / 3},{y} L{dx + w / 3},{y} Q{dx + w / 2 + 6},{y - h * 0.3} {dx + w / 2},{y - h} Z" fill="{col}" {_st(3.0)}/>'
        s += _ell(dx, y - h, w / 2, 5, shade(col, -0.3), sw=2.4)
        s += _line(f"M{dx - w / 2 + 4},{y - h * 0.55} Q{dx},{y - h * 0.4} {dx + w / 2 - 4},{y - h * 0.55}", w=2.0, col=CREAMY)
        y -= h + 2
    return s


CREAMY = "#f3e6c8"


def _hen_basket(phase=0.0):
    """A round basket with a cheerful brown hen in it (anchor bottom centre)."""
    s = f'<path d="M-40,-30 Q-40,0 0,2 Q40,0 40,-30 Z" fill="#c9995a" {_st(3.2)}/>'
    for xx in (-24, -8, 8, 24):
        s += _line(f"M{xx},-28 L{xx * 0.9},-2", w=1.8, col="#9a6a3a")
    s += _line("M-38,-16 Q0,-10 38,-16", w=1.8, col="#9a6a3a")
    hop = -4 * abs(math.sin(2 * math.pi * phase))
    hen = f'<path d="M-26,-30 Q-30,-58 -4,-64 Q14,-90 30,-74 Q40,-62 30,-44 Q24,-30 -26,-30 Z" fill="#b8643a" {_st(3.0)}/>'
    hen += f'<path d="M28,-86 q4,-10 8,-2 q6,-8 8,2 q-6,6 -14,4 Z" fill="#d94a3a" {_st(2.0)}/>'
    hen += f'<path d="M38,-72 L50,-68 L38,-64 Z" fill="#f2b34a" {_st(2.0)}/>'
    hen += f'<circle cx="32" cy="-74" r="2.6" fill="{EYE}"/>'
    hen += _line("M-14,-50 Q0,-40 14,-48", w=2.2, col="#8a4626")
    s = f'<g transform="translate(0,{hop:.1f})">{hen}</g>' + s
    return s


def townsfolk(x, y, scale=1.0, facing=1, kind="man", variant=0, pose="stand", expr=None, phase=0.0, item=None,
              marks=True):
    """The people of Bethlehem: townsfolk, travellers with bundles, the innkeeper, the emperor's herald (see module
    doc, 'NATIVITY FILM')."""
    if kind not in TOWNSFOLK_KINDS:
        raise ValueError(f"townsfolk: unknown kind {kind!r}; choose from {TOWNSFOLK_KINDS}")
    _check_js(pose, TOWNSFOLK_POSES, "townsfolk")
    if item not in TOWNSFOLK_ITEMS:
        raise ValueError(f"townsfolk: unknown item {item!r}; choose from {TOWNSFOLK_ITEMS}")
    expr = _nat_expr(expr, "townsfolk")
    if pose == "walk":
        pose = "walk_a" if (phase % 1.0) < 0.5 else "walk_b"
    if item is None and pose.startswith("carry"):
        item = "bundle" if kind.startswith("traveller") else ("jar" if kind == "woman" else "basket")
    if pose == "shake_head":
        ps = _shake_pose(phase)
    elif pose == "wave":
        f = 168 + 18 * math.sin(2 * math.pi * phase)
        ps = _P(h=-4, legs=((6, 2), (-5, -2)), arms=(("fk", 146, f), ("fk", -8, -3)), hands=("open", "fist"), expr="happy")
    elif pose in ("carry", "carry_walk_a", "carry_walk_b"):
        if item in ("hen", "pots"):
            ps = _P(t=2, legs={"carry": ((3, 1), (-3, -1)), "carry_walk_a": ((24, 8), (-20, -34)),
                               "carry_walk_b": ((-20, -34), (24, 8))}[pose],
                    arms=(("ik", "torso", 1.9, 0.30, 1), ("ik", "torso", 1.0, 0.24, 1)), hands=("none", "none"),
                    expr="happy")
        elif item == "bundle":
            ps = dict(_TZ["stand" if pose == "carry" else pose[6:]])
            ps["arms"] = (ps["arms"][0], ("ik", "torso", -0.1, 0.60, -1))
        else:
            ps = _nh_carry_pose(item, None if pose == "carry" else pose[-1])
    else:
        ps = dict(_TZ[pose])
    D, m = _townsfolk_design(kind, variant)
    b, mi, fr = _tf_items(D, pose, item, phase)
    behind = [b]
    if kind == "herald":
        behind.insert(0, _red_cloak)
    D["behind"], D["mid"] = _hooks(*behind), _hooks(D.get("mid"), mi)
    fronts = [fr]
    if kind == "elder" and pose in ("stand", "walk_a", "walk_b", "listen"):
        ps["t"] = ps["t"] + 8
        if pose != "listen":
            ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
            fronts.insert(0, _cane)
    if kind.startswith("traveller") and pose in ("stand", "walk_a", "walk_b"):
        ps["arms"] = (ps["arms"][0], ("fk", 40, 80))
        fronts.insert(0, _joseph_staff(D))
    if pose == "wave" and marks:
        fronts.append(_wave_marks)
    D["front"] = _hooks(*fronts)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"townsfolk-{kind}{int(variant) % 6}-{pose}")


TOWNSFOLK_CROWD_POSES = ("walk", "stand", "squeeze", "talk", "look_around", "cheer", "listen", "wave")


def townsfolk_crowd(x, y, scale=1.0, facing=1, n=14, pose="walk", width=1200, rows=3, seed=0, phase=0.0, animals=True,
                    busy=1.0, marks=True):
    """A busy Bethlehem street crowd (Luke 2:1-7: everyone travelling to be registered): n people in up to `rows` rows
    centred on x; each row behind is 44*scale higher and 6% smaller. pose='walk' mixes travellers with bundles, women
    with jars, a pot carrier and a hen basket going both ways; 'squeeze' packs them tight with bundles held overhead
    ('as crowded as a station at New Year'); animals adds a laden donkey and a goat. busy 0..1 how many carry things."""
    _check_js(pose, TOWNSFOLK_CROWD_POSES, "townsfolk_crowd")
    import random as _random
    rng = _random.Random(seed)
    sx = 1 if facing >= 0 else -1
    rows = max(1, int(rows))
    kinds = ["traveller", "woman", "man", "traveller_woman", "child", "traveller", "elder", "woman", "traveller", "man",
             "child", "traveller_woman"]
    people = [(kinds[(i + seed) % len(kinds)], (i * 5 + seed) % 6) for i in range(int(n))]
    people.sort(key=lambda p_: 0 if p_[0] == "child" else 1)
    per = max(1, -(-len(people) // rows))
    out = ""
    PRm = _prp()
    for r in reversed(range(rows)):
        grp = people[r * per:(r + 1) * per]
        k_r = scale * (1 - 0.06 * r)
        y_r = y - 44 * scale * r
        if animals and r == min(1, rows - 1):
            ax = x + sx * (width * scale * 0.18 + rng.uniform(-20, 20) * scale)
            out += PRm.donkey(ax, y_r, k_r * 0.92, sx if rng.random() < 0.5 else -sx, pose="walk", phase=phase, sacks=2)
            out += PRm.animal(x - sx * width * scale * 0.32, y_r + 6 * scale, k_r * 0.55, -sx, kind="goat")
        for j, (kind, v) in enumerate(grp):
            u = (j + 0.5) / len(grp) - 0.5
            px = x + sx * (u * width * scale + (r % 2) * 40 * scale + rng.uniform(-16, 16) * scale)
            f_ = sx if (j + r) % 3 else -sx
            ph = (phase + 0.37 * j + 0.5 * r) % 1.0
            item = None
            if pose == "walk":
                carry = rng.random() < busy
                if carry and kind != "child":
                    item = {"traveller": "bundle", "traveller_woman": "bundle", "woman": "jar", "man": "sack",
                            "elder": None}.get(kind)
                    if (j + seed) % 7 == 3:
                        item = "pots"
                    elif (j + seed) % 7 == 5:
                        item = "hen"
                if item:
                    p_ = "carry_walk_a" if ph < 0.5 else "carry_walk_b"
                else:
                    p_ = "walk"
            elif pose == "squeeze":
                p_ = "squeeze" if (j + r) % 2 == 0 and kind != "child" else ("look_around" if kind != "child" else "stand")
                f_ = sx if (j % 2) else -sx
            else:
                p_ = pose
            out += townsfolk(px, y_r + rng.uniform(-5, 5) * scale, k_r, f_, kind=kind, variant=v, pose=p_, phase=ph,
                             item=item, marks=marks)
    return f'<g data-who="townsfolk_crowd-{pose}">{out}</g>'


# ---------------------------------------------------------------- the modern child at the Christmas tree (child(outfit='jumper'))
JUMPER = "#c8443e"
JUMPER_KNIT = "#f4e6cc"
JUMPER_TROUSERS = "#3f6b4a"
JUMPER_SOCKS = "#f1e4d0"
CHILD_ITEMS = ("bauble", "star", "figure", "sheep", "gift", None)
_NC_POSES = {
    "decorate": _P(h=-14, legs=((6, 2), (-5, -2)), arms=(("fk", 128, 150), ("fk", -10, -4)), hands=("fist", "fist"),
                   look=(0.04, -0.08), expr="happy"),
    "place": _P(t=16, h=14, arms=(("fk", 62, 40), ("fk", 56, 34)), hands=("open", "open"), look=(0.03, 0.06), expr="kind",
                **_KNEEL),
    "kneel_look": _P(t=4, h=8, legs=((84, -86), (80, -90)), feet=(100, 100), hem=0.97,
                     arms=(("ik", "knee", 0, 0.15, 1), ("ik", "knee", 1, 0.15, 1)), hands=("open", "open"), expr="amazed",
                     look=(0.04, 0.05)),
    "hold_star": _P(h=-12, legs=((6, 2), (-5, -2)), arms=(("fk", 100, 122), ("fk", 106, 128)), hands=("open", "open"),
                    look=(0.02, -0.08), expr="joyful"),
}


def _jumper_design():
    c = JUMPER
    D = dict(robe=c, sleeve=c, hem_col=JUMPER_KNIT, hem_w=6, cuff=JUMPER_KNIT, skin="#c98c62", leg=JUMPER_SOCKS, hem=0.24,
             flare_k=0.55, hair="#2a1d17", hair_style="curly", hat=("custom", _curly_hat("#2a1d17", "#c98c62")), hat_h=0.12,
             ears=False, bare=True, neck_v=JUMPER_KNIT)

    def knit(st, polys):
        m, tp, pel, u = st["m"], st["tp"], st["pel"], st["u"]
        s = ""
        T = m["T"]
        for poly in polys[:1]:
            s += _poly(_band(poly, pel, u, 0.50 * T, 0.70 * T), JUMPER_KNIT, sw=0)
        for i in range(-3, 4):          # little green trees and red dots in the knitted band
            c0 = tp(i * 0.36 * m["ww"], 0.60 * T)
            s += _poly([(c0[0], c0[1] - 6), (c0[0] + 5, c0[1] + 4), (c0[0] - 5, c0[1] + 4)], JUMPER_TROUSERS, sw=0)
        for i in range(-4, 5):
            c0 = tp((i + 0.5) * 0.36 * m["ww"], 0.20 * T)
            s += _poly([(c0[0], c0[1] - 4), (c0[0] + 4, c0[1]), (c0[0], c0[1] + 4), (c0[0] - 4, c0[1])], JUMPER_KNIT, sw=0)
        return s
    D["robe_deco"] = knit

    def legwear(st, i):
        H, K, A, a1, a2 = st["legs"][i]
        col = JUMPER_TROUSERS if i == 1 else shade(JUMPER_TROUSERS, -0.12)
        s_ = _tube([H, K, _lerp(K, A, 0.84)], st["m"]["lw"] + 8, col, ow=3.2)
        cuff = _lerp(K, A, 0.80)
        dv = _nrm(_sub(A, K))
        nv = (-dv[1], dv[0])
        w = (st["m"]["lw"] + 8) / 2
        s_ += _line(f"M{_pt(_add(cuff, _mul(nv, w)))} L{_pt(_sub(cuff, _mul(nv, w)))}", w=2.2, col=shade(JUMPER_TROUSERS, -0.3))
        return s_
    D["legwear"] = legwear
    return D


def _child_item_front(D, pose, item):
    def front(st):
        W0, W1, hr = st["arms"][0][2], st["arms"][1][2], st["m"]["hr"]
        s = ""
        if pose == "decorate":
            it = item or "bauble"
            if it == "star":
                s += _sparkle((W0[0] + 6, W0[1] - 14), 18, "#f2c94e", 2.4)
            else:
                s += _line(f"M{_pt(W0)} l2,18", w=1.8)
                s += f'<circle cx="{fmt(W0[0] + 2)}" cy="{fmt(W0[1] + 30)}" r="12" fill="#d9453f" {_st(2.8)}/>'
                s += f'<circle cx="{fmt(W0[0] - 2)}" cy="{fmt(W0[1] + 26)}" r="3.5" fill="{HI}" opacity="0.8"/>'
                s += f'<rect x="{fmt(W0[0] - 3)}" y="{fmt(W0[1] + 15)}" width="10" height="6" rx="2" fill="{GOLD}" {_st(1.8)}/>'
            s += _fist(W0, hr, D["skin"])
        elif pose == "place":
            it = item or "figure"
            c = ((W0[0] + W1[0]) / 2, max(W0[1], W1[1]) + 6)
            s += f'<g transform="translate({fmt(c[0])},{fmt(c[1])}) scale(0.55)">{_prp()._nativity_figure(it)}</g>'
            s += _hand(W0, (0.3, 1.0), "open", D["skin"], hr) + _hand(W1, (0.3, 1.0), "open", D["skin"], hr)
        elif pose == "hold_star":
            c = ((W0[0] + W1[0]) / 2 + 14, min(W0[1], W1[1]) - 22)
            s += _glow_disc(c, 70, 70, 0.8, "cstar")
            s += _sparkle(c, 30, "#f2c94e", 3.0)
            s += _hand(W0, (0.5, -0.9), "open", D["skin"], hr) + _hand(W1, (0.3, -1.0), "open", D["skin"], hr)
        return s
    return front


def _child_nativity(x, y, scale, facing, pose, expr, phase, marks, outfit, pillow, sibling, hood, boots, coat, toy, item):
    if outfit is not None and outfit not in CHILD_OUTFITS:
        raise ValueError(f"child: unknown outfit {outfit!r}; choose from {CHILD_OUTFITS}")
    allp = CHILD_POSES + SIBLING_POSES + STORM_CHILD_POSES + NATIVITY_CHILD_POSES
    if pose not in allp:
        raise ValueError(f"child: unknown pose {pose!r}; choose from {allp}")
    if item not in CHILD_ITEMS:
        raise ValueError(f"child: unknown item {item!r}; choose from {CHILD_ITEMS}")
    expr = _nat_expr(expr, "child")
    if pose in _NC_POSES:
        ps = dict(_NC_POSES[pose])
    elif pose in _SC_POSES:
        ps = dict(_SC_POSES[pose])
    elif pose == "wave":
        f = 166 + 18 * math.sin(2 * math.pi * phase)
        ps = _P(h=-4, arms=(("fk", 146, f), ("fk", -10, -4)), hands=("open", "fist"), expr="happy")
    elif pose in _SIB_POSES:
        ps = dict(_SIB_POSES[pose])
    else:
        ps = dict(_CH_POSES[pose])
    if outfit == "jumper":
        D, m = _jumper_design(), _metrics(_CHILD, 1.0, 0.98)
    elif outfit == "pyjamas":
        D, m = _pyjama_design(ps), _metrics(_CHILD, 1.0, 0.96)
    elif sibling is not None:
        D, m = _sibling_design(sibling)
    else:
        D, m = _child_design(ps["legs"], hood, boots, coat or CHILD_COAT), _CHILD
    if pose in NATIVITY_CHILD_POSES:
        D["front"] = _child_item_front(D, pose, item)
    elif pose in ("hug_pillow", "sit_hug") and pillow:
        D["front"] = _pillow_front(D, pose)
    e = expr or ps["expr"]
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    if pose == "jump":
        inner = f'<g transform="translate(0,{-CHILD_JUMP})">{inner}</g>'
    return _wrap_out(inner, x, y, scale, facing, f"child-{outfit or sibling or 'raincoat'}-{pose}")
