export const meta = {
  name: 'jonah-characters',
  description: 'Build the shared picture-book character and prop libraries for the Jonah video, then critique and polish them',
  phases: [
    { title: 'Build', detail: 'people library and props/creatures library in parallel' },
    { title: 'Review', detail: 'independent visual critique of each character sheet' },
    { title: 'Polish', detail: 'apply the critique' },
  ],
}

const ROOT = '/home/user/questly/jonah-video'
const COMMON = `
Project: ${ROOT} — a ~2:19 Chinese picture-book style video of the Bible story of Jonah (Python pipeline, already working).
Read first: ${ROOT}/ART_GUIDE.md, ${ROOT}/art/style.py (palette P, svg_doc, filters wobble/wobble-fine, helpers), ${ROOT}/engine/raster.py and ${ROOT}/engine/watercolor.py (how SVG becomes watercolour images), ${ROOT}/art/scenes/s01_title.py (example).
Environment: python3 with numpy, pillow, opencv, playwright (Chromium at /opt/pw-browsers) installed; run commands from ${ROOT}. Rasterise SVG with engine.raster.rasterize(svg_string, w, h) and engine.watercolor.watercolor(img, seed=...) so you see exactly what the film shows. Look at your PNGs with the Read tool and iterate until they look like a finished, charming children's Bible picture book (ages 3-8): warm, soft, rounded, friendly faces, readable silhouettes, consistent ink outlines (art.style.INK, 3-5 px at scale 1, round joins), never pure black or pure white.
Output format of every drawing function: SVG markup string (a <g>...</g>, NO <svg> wrapper) to be placed inside art.style.svg_doc(...). Signature style: fn(x, y, scale=1.0, facing=1, **options). (x, y) is the anchor in stage pixels; facing=1 faces/moves right, -1 mirrors to face left. Wrap each character in a group with filter="url(#wobble-fine)" (props too). Keep shapes simple and bold — they are rendered at stage size 2112x1188 and shown at 1920x1080.
Document in the module docstring, for EVERY public function: signature, anchor point, approximate bounding box at scale=1 relative to the anchor (left, top, right, bottom in px), and the list of poses/options. Scene authors will rely on that docstring alone.
Only create/edit the files named in your task (you may append new generic helper functions at the END of art/style.py without changing existing ones). Do not touch other files.`

const TASKS = [
  {
    key: 'people',
    prompt: `${COMMON}

YOUR TASK: create ${ROOT}/art/characters.py — the PEOPLE library — and ${ROOT}/tools/character_sheet.py which renders labelled contact sheets of every function/pose/expression on a cream paper background to ${ROOT}/build/preview/characters_*.png (use engine.raster + engine.watercolor; a few sheets, each <= 2400 px wide).

Proportions: picture-book style ~3.5-4 heads tall; adult standing height ~330 px at scale=1, child ~220 px. Anchor = bottom centre between the feet (ground contact point) for every person, in every pose (for lying/sitting/kneeling poses it is still the ground contact point under the body centre).
Faces: round, big dot eyes with a tiny highlight, simple brows, small nose, rosy cheeks (P['cheek']), clear mouth shapes. Expressions must read instantly.

Functions:
1. jonah(x, y, scale=1.0, facing=1, pose='stand', expr='neutral', wet=False)
   Design (must be identical in every pose): ochre-orange robe P['jonah_robe'] with darker hem P['jonah_robe_dark'], teal sash P['jonah_sash'], cream head-cloth P['headcloth'] with a brown stripe band P['headcloth_stripe'] hanging behind the neck, short brown beard P['beard'], skin P['skin'], brown sandals. Kind, slightly worried everyman prophet.
   poses: stand, walk_a, walk_b (two stride frames for a walk cycle), run_a, run_b (two run frames), sleep (lying on his side, eyes closed, hands under cheek), kneel_pray (kneeling, hands together, head tilted up), sit (sitting on the ground), sit_sulk (sitting, arms crossed), sit_faint (slumped, head drooping, fanning hand), sit_happy (sitting, relaxed, arms open), preach (standing, one arm raised high, mouth open), point, arms_up, fall (tumbling through the air, arms and legs out), float (underwater, arms spread, hair/cloth floating), refuse (body turned away, hand raised palm-out, shaking head), confess (hand on chest, head bowed), listen (standing/looking up, hand cupped near ear), wake (sitting up, rubbing eyes).
   expr: neutral, happy, sad, scared, angry, surprised, sleepy (closed eyes), peaceful (closed eyes, gentle smile), dizzy (spiral eyes), shout (open mouth), sorry.
   wet=True: dripping, a bit of green seaweed on his head-cloth.
2. sailor(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr='neutral') — variants 0-3 differ in striped tunic colours (blue/cream, red/cream, teal/cream, ochre/brown), headband/cap, beard/no beard, hair, skin tones (varied, respectful). poses: stand, scared (hands up by face), throw (both arms raised high as if heaving something overboard), carry (arms forward low, bent knees), pray (both hands raised to the sky), point, pull (hauling a rope, leaning back), lift (both hands above head, together with others lifting a person).
3. captain(x, y, scale=1.0, facing=1, pose='stand', expr='neutral') — bigger, grey beard, red cap, blue coat over tunic. poses: stand, wake (leaning forward, one hand reaching down to shake someone), point, worried (hands on head).
4. king(x, y, scale=1.0, facing=1, pose='stand', attire='royal', expr='neutral') — Assyrian king of Nineveh: curled black beard and hair (Assyrian style, gentle not scary), tall cylindrical gold crown (P['crown']), purple fringed robe P['royal']. attire='sackcloth': crown removed, rough burlap sack robe P['sackcloth'] with rope belt, grey ash smudges. poses: stand, sit_throne (seated; include an optional simple throne via throne=True), sit_ashes (sitting on the ground, head bowed, hands on knees), kneel_pray, remove_crown (holding the crown in both hands).
5. citizen(x, y, scale=1.0, facing=1, kind='man', variant=0, pose='stand', attire='normal', expr='neutral') — Nineveh townspeople. kind: man, woman, child, elder. variant 0-3 colours (sand, terracotta, olive, indigo) with simple Mesopotamian robes, shawls, curled beards for men. attire='sackcloth' as above. poses: stand, walk, listen (turned toward a speaker, hand to ear/chin), kneel_pray, point, sad (head bowed), cheer (arms up, for children playing).

Iterate visually (several rounds). Check: no broken joints, limbs attached, hands visible, head/body overlap correct, outlines consistent, Jonah recognisable in every pose at small sizes (render one sheet also at scale 0.45 to check readability), facing=-1 works. Return a concise summary of the API (signatures, anchors, bounding boxes, poses) and the sheet paths.`,
  },
  {
    key: 'props',
    prompt: `${COMMON}

YOUR TASK: create ${ROOT}/art/props.py — the CREATURES, VEHICLES, PLANTS, BUILDINGS and PROPS library — and ${ROOT}/tools/props_sheet.py which renders labelled contact sheets of every function/option on a cream paper background to ${ROOT}/build/preview/props_*.png (use engine.raster + engine.watercolor; a few sheets, each <= 2400 px wide).
Scale reference: an adult person is ~330 px tall at scale=1 (Jonah, drawn by a separate library in art/characters.py).

Functions (anchor in brackets):
1. fish(x, y, scale=1.0, facing=1, mouth=0.0, eye='open', tail=0.0, blush=True) [body centre] — THE GREAT FISH: a huge, friendly fish ~1300 px long at scale 1 (big enough to swallow a man): rounded body, vertical tail fin (it is a fish, not a whale), dorsal and pectoral fins, gill line, scales hinted with soft arcs, spots P['fish_spot'], blue body P['fish'] with light belly P['fish_belly'] and darker back P['fish_dark'], one big kind eye with highlight, gentle smile. mouth 0..1 opens the jaw wide (at 1 a dark mouth P['mouth_inside'] big enough to swallow a person, with a tongue); eye: open, closed, happy (^ arc), surprised; tail -1..1 bends the tail fin up/down for swimming animation. Must look good at all mouth values (animators will render several frames).
2. ship(x, y, scale=1.0, facing=1, sail='full', cutaway=False, lantern=True) [hull waterline centre] — ancient Phoenician-style wooden merchant ship ~1000 px long at scale 1: curved hull with planks (P['wood'] tones), raised bow/stern (stern curling), one mast, square sail P['sail'] with terracotta stripes P['sail_stripe'], rigging, rail, a row of round shields or rope, oars optional. sail: full (billowing), furled, torn (storm). cutaway=True shows the hull in cross-section like a dollhouse: a below-deck hold with cargo sacks/jars, a little bed area, a hanging lantern — and document the stage-space rectangle of that interior (relative to the anchor) so scene authors can place sleeping Jonah inside.
3. Props: crate(x, y, scale=1.0, rot=0) [centre], jar(...) [centre, amphora], sack(...) [bottom centre], lots_jar(x, y, scale) [bottom centre] plus lot(x, y, scale=1.0, rot=0, marked=False) [centre, a small wooden stick/pebble; marked=True has a glowing mark], lantern(x, y, scale) [top hook], rope_coil, scroll, booth(x, y, scale=1.0) [bottom centre: Jonah's simple shelter of sticks with a cloth roof, Jonah 4:5], throne(x, y, scale) [bottom centre], ash_pile(x, y, scale).
4. Plants: castor_plant(x, y, scale=1.0, growth=1.0, wither=0.0, bite=0.0) [ground/root point] — the 蓖麻 (Ricinus communis): thick reddish-green stem P['leaf_dark'], very large palm-shaped (palmate) leaves with 7-9 pointed lobes P['leaf'], a few spiky red seed clusters; growth 0 = small sprout, 0.5 = waist high, 1 = taller than a standing man with leaves forming a shade canopy above and to one side (document where the shade falls); wither 0..1 turns leaves yellow-brown P['leaf_dry'] -> P['leaf_dead'], curling and drooping; bite 0..1 shows a nibbled notch in the stem. Must look good at intermediate values (animators will render frames 0, 0.25, 0.5, 0.75, 1). palm_tree(x, y, scale, lean=0) [base], olive_tree(x, y, scale) [base], bush(x, y, scale, variant) [base], grass_tuft(x, y, scale, variant) [base], seaweed(x, y, scale, variant) [base], reeds.
5. Creatures: worm(x, y, scale=1.0, facing=1, chomp=0.0) [bottom centre; small cute green-pink caterpillar-like worm ~60 px long, chomp opens its mouth], gull(x, y, scale=1.0, facing=1, wing=0.0) [body centre; wing -1..1 flap position], small_fish(x, y, scale, facing, color) [centre], dove(x, y, scale, facing, wing), animal(x, y, scale=1.0, facing=1, kind='sheep', sackcloth=False) [bottom centre; kinds: sheep, goat, cow, donkey, camel — cute rounded picture-book animals; sackcloth=True drapes a little burlap blanket on them (Jonah 3:8)].
6. Buildings: house(x, y, scale=1.0, variant=0) [bottom centre; flat-roof mud-brick Middle-Eastern house with small dark windows, door, maybe stairs to the roof; variants differ], city_wall(x0, x1, y, height=260, gate=None) [ground line; Assyrian crenellated mud-brick wall from x0 to x1; gate=(gx, width) adds an arched gate with tall doors], ziggurat(x, y, scale) [bottom centre; stepped temple tower], nineveh_skyline(x0, x1, y, scale=1.0, seed=0) [ground line; a dense distant city panorama of walls, houses, towers, palms for far backgrounds], harbor_dock(x0, x1, y) [deck level; wooden pier with posts], signpost(x, y, scale, left_text, right_text) [base; two wooden arrow boards with Chinese text in LXGW WenKai, e.g. '尼尼微' and '他施'].

Iterate visually (several rounds). Check proportions relative to a 330 px person, consistent outlines, appeal, intermediate parameter values (fish mouth 0/0.33/0.66/1, plant growth/wither series), facing=-1 works. Return a concise summary of the API (signatures, anchors, bounding boxes, options; the ship cutaway interior rectangle; the plant shade region) and the sheet paths.`,
  },
]

const BUILD = { type: 'object', properties: { summary: { type: 'string' }, api: { type: 'string' }, sheets: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } }, required: ['summary', 'api', 'sheets'] }
const REVIEW = { type: 'object', properties: { verdict: { type: 'string', enum: ['good', 'needs_fixes'] }, issues: { type: 'array', items: { type: 'object', properties: { severity: { type: 'string', enum: ['high', 'medium', 'low'] }, item: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['severity', 'item', 'problem', 'fix'] } } }, required: ['verdict', 'issues'] }
const FIX = { type: 'object', properties: { summary: { type: 'string' }, api: { type: 'string' }, sheets: { type: 'array', items: { type: 'string' } }, unresolved: { type: 'string' } }, required: ['summary', 'api', 'sheets'] }

const results = await pipeline(
  TASKS,
  t => agent(t.prompt, { label: `build:${t.key}`, phase: 'Build', schema: BUILD }),
  (built, t) => agent(`${COMMON}

YOUR TASK: you are an independent art director reviewing the ${t.key === 'people' ? 'people library art/characters.py' : 'props/creatures library art/props.py'} that another artist just made for this film. Do NOT edit any files.
Their summary: ${JSON.stringify(built)}
Re-render the sheets yourself (python3 tools/${t.key === 'people' ? 'character_sheet.py' : 'props_sheet.py'}), then look carefully at every image with the Read tool, and read the code/docstring.
Judge against the ART_GUIDE and this brief:
${t.prompt.split('YOUR TASK:')[1]}
Look for: anatomy/assembly errors (detached limbs, floating parts, wrong overlaps, hands missing), poses that don't read, inconsistent design between poses (Jonah must be identical), off-model colours, harsh or scary looks, outlines too thin/thick, missing functions/options/poses from the brief, broken facing=-1 mirroring, intermediate parameter values that look wrong, docstring missing anchors/bounding boxes, anything unbiblical or culturally insensitive, and overall appeal versus a professionally illustrated children's picture book. Be specific and actionable; list every real problem, ranked.`, { label: `review:${t.key}`, phase: 'Review', schema: REVIEW }),
  (review, t) => agent(`${COMMON}

YOUR TASK: polish ${t.key === 'people' ? 'art/characters.py (and tools/character_sheet.py)' : 'art/props.py (and tools/props_sheet.py)'} — fix every high and medium issue from the art director's review below, and low ones when cheap. Keep the public API backward compatible (same function names/params); extend it if the review asks for something missing. Re-render the sheets and look at them to confirm each fix. Make sure the module docstring documents every function's signature, anchor, bounding box at scale 1 and options accurately.
Original brief:
${t.prompt.split('YOUR TASK:')[1]}
Review: ${JSON.stringify(review)}
Return the final API summary.`, { label: `polish:${t.key}`, phase: 'Polish', schema: FIX }),
)
return results
