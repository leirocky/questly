"""The background score for 约拿的故事 (v2) — one continuous piece in 24 cues (~10 minutes).

Every cue starts exactly at its scene's global start (inside the 1 s cross-dissolve) and is
planned in bars whose tempo is derived from the scene's real line timings.  Hit points are found
from the narration text (`Cue.find` / `Cue.at` locate the utterance or the word inside it), never
from fixed line indices or durations.  The cues live in audio/cues_[a-e].py; shared writing
helpers in audio/scorelib.py; the framework (segments, tempo maps, voice-leading, MIDI) in
audio/scorekit.py.

Tonal plan (hand-offs by common tone or dominant -> tonic):

  s01 title D 6/8 (Jonah theme b1-b2) -> s02 call D (theme b3-b7, shimmer, God's choir on bVI over
  a D pedal, a first hijaz glimpse of Nineveh) -> s03 flee D dorian (run / tiptoe question / Joppa /
  ship, scale run) -> s04 storm D minor (build, peak hit, cargo, sleeping Jonah) -> s05 hold D minor
  6/8 (muffled, rocking) -> urgent pulse -> s06 lots (ticking council, rattle, ping, questions,
  Jonah's theme on the horn in D major, fear, diminished stinger) -> s07 waves 6/8 -> lament ->
  s08 rowing strokes (D minor, Neapolitan Eb climb, crash) -> hushed prayer -> s09 storm reprise,
  splash, sudden D major calm, plagal hymn -> s10 sinking Dmaj7-Bm7, the great-fish motif, gulp
  D-C#-B -> s11 B minor belly (warm G for '别怕', heartbeat, prayer) -> s12 sinking lament bass,
  deceptive V-VI turn to G on '想起了耶和华', rise, radiant D on '救恩属于耶和华' -> s13 shore G
  (fish motif in G, pop, sunny Jonah motif) -> s14 the second call (same shimmer and God's chords),
  Jonah's theme walking -> s15 Nineveh D hijaz (maqsum), 'forty days' -> s16 G minor guess, Eb
  surprise, humble G minor -> s17 king: sarabande G-F-Eb-D, herald horn, processional decree, Bb
  hope, half cadence -> s18 mercy G major -> s19 happy G, grumpy G minor bassoon, tender Eb, the
  flight recalled, God's question (call chords in G) -> s20 booth G (plucked) -> s21 night, plant
  grows (bVI-bVII-I), shade, waltz -> s22 dawn, worm (chromatic pizzicato), heat (open fifths, wind),
  hush, stubborn stomps -> s23 lesson G 6/8 (theme on piano, ends on A7) -> s24 end: Bm7-Gmaj7-
  Em7-A7sus4 question, then the theme in D, warm and full, final D chord ringing to the end.

The Jonah theme (D major, 6/8, q = quarter note):
  b1 D  F#5:1 E5:1/2 D5:1 A4:1/2        motif x (3-2-1-5, lilting long-short)
  b2 G  B4:1 D5:1/2 G5:1 F#5:1/2        motif y (rising arpeggio)
  b3 Em7|A7  E5:3/2 C#5:1 D5:1/2
  b4 A  E5:5/2 A4:1/2                   half cadence + pickup
  b5 = b1,  b6 G  B4:1 D5:1/2 G5:1 B5:1/2,  b7 D/A|A7  A5:1 F#5:1/2 E5:1 C#5:1/2,  b8 D  D5:3
"""
from audio import cues_a, cues_b, cues_c, cues_d, cues_e
from audio.scorekit import Cue, PhraseNotFound, Score

SCENE_CUES = {
    "s01_title": cues_a.title, "s02_call": cues_a.call, "s03_flee": cues_a.flee, "s04_storm": cues_a.storm,
    "s05_captain": cues_b.captain, "s06_lots": cues_b.lots, "s07_confess": cues_b.confess, "s08_row": cues_b.row,
    "s09_overboard": cues_c.overboard, "s10_swallow": cues_c.swallow, "s11_belly": cues_c.belly,
    "s12_deep": cues_c.deep, "s13_shore": cues_c.shore,
    "s14_again": cues_d.again, "s15_city": cues_d.city, "s16_believe": cues_d.believe, "s17_king": cues_d.king,
    "s18_mercy": cues_d.mercy,
    "s19_angry": cues_e.angry, "s20_booth": cues_e.booth, "s21_vine": cues_e.vine, "s22_worm": cues_e.worm,
    "s23_lesson": cues_e.lesson, "s24_end": cues_e.end,
}


def build(timeline, passes=3):
    """Compose the score.  Pads are voice-led against the complete score of the previous pass
    (melodies, counter-melodies, basses and other pads written anywhere in the cue), so they avoid
    parallel fifths/octaves with lines that are written after them; the passes are deterministic.

    A scene this score does not know (renamed or new) gets a soft generic pad in its mood's key
    instead of breaking the build."""
    guides = None
    for _ in range(passes):
        sc = Score(timeline)
        sc.guide_notes = guides
        scenes = timeline["scenes"]
        for i, s in enumerate(scenes):
            t1 = scenes[i + 1]["start"] if i + 1 < len(scenes) else timeline["duration"]
            fn = SCENE_CUES.get(s["id"], cues_e.generic)
            cue = Cue(sc, s, t1)
            try:
                fn(cue)
            except PhraseNotFound:
                if fn is cues_e.generic:
                    raise
                # a phrase this cue listens for is missing (the narration was rewritten): drop the
                # half-written cue and fall back to the generic one
                sc.notes[:] = [n for n in sc.notes if n.seg.cue is not cue]
                sc.syncs[:] = [x for x in sc.syncs if x[0] != cue.id]
                cue.segs.clear()
                print(f"  score: {s['id']}: narration phrase not found, using a generic cue")
                cues_e.generic(cue)
        guides = sc.guide_index()
    return sc
