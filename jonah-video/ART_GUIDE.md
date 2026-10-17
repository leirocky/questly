# Art guide — 约拿的故事 picture-book video

Shared rules for everyone writing `art/characters.py` and `art/scenes/*.py`.
Read `engine/scene.py`, `engine/motion.py`, `engine/fx.py`, `art/style.py` and
`art/characters.py` docstrings for the exact APIs; `art/scenes/s01_title.py` is a
small worked example.

## Look and feel
- A warm, gentle **watercolour / gouache children's picture book** (think classic Bible storybooks for ages 3–8).
  Soft rounded shapes, simple big forms, friendly faces, generous negative space, cosy light.
- Outlines: umber ink (`P["ink"]`), 3–5 px, round joins, always with a wobble filter
  (`filter="wobble"` for big shapes, `"wobble-fine"` for characters/small props, `"wobble-strong"` sparingly).
  Never pure black. Never pure white fills (use `P["foam"]`, `#fffaf0`, cream).
- Colour: use `art.style.P` palette; derive variants with `S.mix()` / `S.shade()`. Each scene has a clear mood palette
  (dawn pastel, storm slate-blue, underwater teal, belly warm-dark, Nineveh sand/terracotta, hot noon ochre, sunset gold).
- Depth: 3–6 planes (sky, far, mid, near, foreground accents) with soft gradients; distant planes lighter and
  less saturated; foreground silhouettes (grass tufts, rocks, rope, leaves) framing the shot help a lot.
- Texture is added automatically: every layer gets a watercolour pass (pigment mottling + edge pooling) and every frame
  gets cream paper grain. Don't add your own noise textures. Text layers should use `wc=0`.
- Detail level: rich enough to feel like a finished book page (small props, windows, plants, birds, waves crests,
  clouds), but readable at a glance by a child. Faces of main characters must be clearly visible.

## God
God is **never** drawn as a person. Show his presence as warm golden light (rays from parting clouds, glow,
sparkles via `FX.sparkles`), and through his voice. Keep it reverent and gentle.

## Characters (from `art/characters.py`)
- **Jonah** — the hero in every scene; must look identical everywhere: ochre-orange robe (`jonah_robe`), teal sash,
  cream head-cloth with brown stripe, short brown beard, round friendly face, dot eyes with highlight, rosy cheeks.
- Sailors, the captain, the king of Nineveh, townspeople (men, women, children, elders), animals, the great fish,
  the ship, the castor plant (蓖麻), the worm, gulls — all from the library so they match across scenes.
- The great fish is a **huge friendly fish** (vertical tail fin, fins, gills, spots, big kind eye), not a scary monster.
- Characters are SVG markup (`<g>`) you place inside `S.svg_doc(...)`. Put each character that moves on its own layer.

## Bible accuracy (Jonah 1–4)
Joppa (约帕) port → ship to Tarshish (他施, westward), away from Nineveh (尼尼微, east). God sends the storm; sailors
are afraid, cry to their gods and throw cargo overboard; Jonah sleeps in the inner part of the ship; the captain wakes
him; they cast lots; the lot falls on Jonah; he tells them to throw him in; the sea calms at once; God appoints a great
fish that swallows him; three days and three nights; he prays; the fish vomits him onto dry land; second call;
Nineveh is a great city; Jonah preaches "forty days"; people believe, fast, wear sackcloth — the king leaves his throne,
puts on sackcloth and sits in ashes; even animals wear sackcloth; God relents. Jonah is angry, sits east of the city
in a little booth; God makes a castor plant (蓖麻, big palm-shaped leaves) grow to shade him; at dawn a worm attacks
it and it withers; a scorching east wind and sun make him faint; God speaks about caring for the plant vs. the city of
120,000 people who cannot tell their right hand from their left, and many animals. Don't add unbiblical events.
Assyrian look for Nineveh: thick mud-brick walls, crenellations, big gates, ziggurat/stepped temple, flat roofs,
date palms; people in long fringed robes, curled beards; the king with a tall crown.

## Frame, timing, motion
- Stage default 2112×1188 (16:9). You may use a larger stage (e.g. 3600×1188 panorama, or 2112×2376 tall) and move the
  camera with `M.cam_keys`. Keep the camera viewport inside the painted area at all times (no empty edges, including
  during shakes, sways and the 0.8 s cross-dissolves at both ends of the scene).
- **Subtitle zone**: the bottom ~150 px of the 1920×1080 output shows subtitles. Keep faces and key action above it.
- Key animation to the narration: `ctx.lines[i].start/.end` (seconds from scene start). Things the narrator describes
  should happen while it is being said (or just before). The first and last ~0.8 s overlap neighbouring scenes in a
  cross-dissolve, so start and end on calm, readable frames.
- Every scene should feel alive the whole time: breathing/bobbing characters, drifting clouds, moving water,
  swaying plants, particles — subtle, not frantic (storm excepted). Prefer eased keyframes (`M.keys`) for actions.
- Line boil (`boil=6`) gives a hand-drawn shimmer; use it on a few small layers at most.
- Performance budget: `python3 tools/preview.py <id> --bench` must report < 450 ms/frame single-threaded.
  Big moving layers and many fx cost the most; flatten static things into one layer.

## Sound effects
Declare sound with `sc.sfx(name, at, dur=..., gain_db=..., pan=...)` using these names (implemented in
`audio/sfx.py`; loops accept any `dur`, one-shots have a natural length when `dur=None`):

| loops (pass `dur`) | one-shots (`dur=None`) |
| --- | --- |
| `waves_calm`, `waves_storm`, `storm_wind`, `rain`, `wind_soft`, `wind_hot`, `ship_creak`, `underwater`, `bubbles`, `heartbeat`, `drip`, `footsteps`, `footsteps_run`, `crowd`, `birds`, `snore`, `heat` | `thunder` (~3.5 s), `splash` (~1.5 s), `splash_small` (~0.8 s), `whoosh` (~0.8 s), `gulp` (~1 s), `spit` (~0.8 s), `thud` (~0.4 s), `chime` (~2.5 s divine shimmer), `sparkle` (~1.2 s), `grow` (~2 s rising), `wither` (~2 s falling), `crunch` (~1.5 s nibbling), `gull` (~1.5 s), `lots` (~1.5 s wooden rattle), `cloth` (~0.8 s), `sheep` (~1 s), `pop` (~0.3 s) |

Ambiences (waves, wind, rain) usually run the whole scene with ~0.8 s fades so they overlap the dissolves;
one-shots (splash, thunder, gulp) go exactly on the visual event. Narration is the priority: keep ambiences at
about −8…−16 dB and one-shots at about −4…−12 dB.

## Verify before you finish
1. `python3 tools/preview.py <id> --lines` and `python3 tools/preview.py <id>` — open the PNGs (Read tool) and look.
2. `python3 tools/preview.py <id> --times ...` around every animated event to check its timing.
3. `python3 tools/preview.py <id> --bench`.
4. Only edit your own file(s). If you think a shared file has a bug, describe it in your final answer instead.
