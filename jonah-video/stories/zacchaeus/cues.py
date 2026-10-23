"""The background score for 撒该爬上桑树 (Luke 19:1-10; ~3:55) -- one continuous piece in 11 cues.

Read by audio/score.py when the story is "zacchaeus" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework as the earlier scores (audio/scorekit.py,
audio/scorelib.py): every cue starts at its scene's global start, is planned in whole bars whose tempo follows the
real line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap), never to fixed times.  Hits that
show an on-screen action follow the PICTURE: picture() / pic() read the scene's own sound-effect cues at build time
(engine.loader.build_scene(...).sfx_cues) and pick them exactly as music_check picks a PICTURE_HITS target; hit() and
accent() put the attack wherever the cue falls, on tones of the chord sounding there, lead() gives a moment's main
attack to the picture when it falls inside that moment's own segment (the title's ta-da, the idea, the arrival at the
top of the tree), and climb() gives each of a row of pops one note, climbing.  A scene that does not build (yet) falls
back to the narrator's voice: syl() / chars() measure the punctuation groups (and the characters inside them) in the
recorded clip the way the scenes do (stories/noah/scenes/s01_title.py voice_marks), scaled to the line's length in the
timeline -- the two 跳 of s04, the five 爬 of s05, the coins of s08.  audio/music.py writes the chord at every moment
to harmony.json and audio/mix.py tunes the scenes' chimes, sparkles and grows to it, so the chord under every one of
those cues below is chosen for the bells too (a sus chord rings its bells a whole step lower).

Colour: a bouncy street comedy, unlike the eight earlier scores (Jonah's D-major sea, Daniel's Persian court in A
hijaz, David's G pipe tune, Noah's F hymn and B-flat march, Joseph's D clarinet, the Storm's Galilean mixolydian folk,
the Nativity's E-flat carols and music box, the Lost Sheep's A-major pastoral with mandolin and pennywhistle).  Home
key B-flat major (a home key no film has used), mostly in a quick 2/4: Zacchaeus's little steps on a staccato bassoon
and pizzicato, his perky voice on the clarinet, his smugness on a Harmon-muted trumpet, the jumps, ideas and climbs on
a xylophone; Jericho is a koto played like a qanun (its street tune leans on the flat sixth and flat second as
chromatic neighbours), a darbuka (low conga 'doum', high bongo 'tek'), hand-claps and a marimba off-beat.  The
frustration is a comic G minor (a ticking clock of woodblocks, the wall of low brass); the crowd grumbles on low
woodwinds in G minor.  The call is warm E-flat strings and horn; the brave promise a trumpet march; salvation a
chromatic-mediant lift to a radiant D major (trumpet, horns, choir, harp, glockenspiel, timpani) where a pan flute
recalls the shepherd for a moment; the golden evening is his own tune, sung by the horn, back in B-flat.  The modern
frame (s02, s11) is a cosy F major on marimba, nylon guitar and soft strings.  Six General MIDI voices the shared
orchestra does not list are registered here for this story only (_EXTRA): xylophone, marimba, Harmon-mute trumpet,
trumpet, koto, pan flute.  Every tune below is original; none opens with the rising 3-5-8 of the earlier themes, and
the well-known children's 'wee little man' song is not quoted (no sol-sol-mi openings).

Themes (q = quarter note)
  Zacchaeus (B-flat, 2/4; mi fa fi sol | do' . sol mi | fa re ti re | do -- a little man creeping up on tiptoe, a pop
  and a cheeky zig-zag home):
     b1 Bb   D5 Eb5 E5 F5       b2 Bb   Bb5 . F5 D5       b3 F7   Eb5 C5 A4 C5       b4 Bb   Bb4
     perky on the clarinet (the title s01; '名叫撒该' s03; the joy of s06), its head questioning ('也想看看' s04, in C
     minor for '耶稣认识我' s06), fast on the xylophone as he scampers (s05), an octave higher on flute and xylophone in
     the tree ('嘿嘿，这下看得清清楚楚了' s05), in F on the bassoon for the frame (s02), in D in s09.
  The call -- Zacchaeus's tune made warm and lyrical when Jesus calls him (4/4; mi fa fi sol-- | do'. ti la sol | ...):
     D5:1 Eb5:1/2 E5:1/2 F5:2 | Bb5:3/2 A5:1/2 G5:1 F5:1 | Eb5:1 D5:1/2 C5:1/2 F5:1 A4:1 | Bb4  (Bb | Gm Eb | Cm7 F7 |
     Bb); the horn under '撒该，快下来' (s06), in E-flat for '可是耶稣，还是愿意' (s07), on the clarinet in D for
     '撒该也是上帝家里的人' (s09), on the marimba in F for '耶稣知道撒该的名字，也知道你的名字' (s11).
  The brave march -- the same tune with dotted steps, on the trumpet, for the promise (s08).
  The generous song -- after salvation the tune sings, diatonic and broad (2/4; mi . fa sol | do'. ti | la sol fa |
     sol-- | la sol fa | mi re do | re. ti | do): the golden evening on the horn (s10), its head in F for
     '他也想住进你的心里' (s11).
  The Jericho street tune (B-flat, 2/4, koto; sol le sol mi do | re mi re do | ...: the flat sixth and flat second as
     chromatic neighbours give the qanun its accent): the town (s03), the news running through the crowd (s04).
  The shepherd's echo -- an original two-bar pan-flute call in D, 6/8 (sol la sol mi do | re mi re do), for
     '就像牧羊人，去找走丢的小羊' (s09); the Lost Sheep's tunes are not quoted.

Cue table (scene: key / meter -- what the music does; picture hits in brackets)
  s01 title     B-flat 2/4  a bar of little steps (bassoon, pizzicato, the marimba's off-beat, the darbuka), then
                            Zacchaeus's tune on the clarinet; the B-flat ta-da arrives with the finished title [he peeks
                            out of the leaves (a xylophone grace), the ribbon (a glint), a xylophone step climbing for
                            each of the six title characters, F5 Bb5 C6 Eb6 F6 A6, the ta-da on the sparkle]
  s02 question  F 2/4       the frame (marimba, guitar, strings): his tune's creep on the marimba; Gm7 C7sus4 on
                            '什么都看不见' (change), hanging through the pause (a guitar heartbeat); F on '今天' (change):
                            his tune small, on the bassoon, in F; B-flat on '可是，他想了一个好办法' (change), C7; F on
                            '好办法' (change and a plucked hit), the guitar rolling on and the marimba waving through
                            the tail into the page turn [two hops (a xylophone hop each), back on his heels (a low
                            pluck), dad lifts him (a xylophone run up), the boy up and beaming (a xylophone ping)]
  s03 jericho   B-flat 2/4 -> G minor -> E-flat   the street tune on the koto (marimba, pizzicato, darbuka, a qanun
                            flourish); his tune on '城里住着一个人' (change); a mock-imperial muted-trumpet fanfare on
                            '收税的人，就是' (change); his smug strut on '撒该管着好多' (change), a muted-trumpet 'heh-heh'
                            after '他很有钱'; G minor on '可是，大家都不喜欢撒该' (change): a sneaky clarinet, tiptoe
                            pizzicato; E-flat on '大家看见撒该' (change), a lonely clarinet to F7 [he counts his coins (a
                            clink), the emperor's coin (a timpani and a glint), three coins on the heap, the chest
                            overflows (a bling and the coins glittering up), he hops off his stool, he snatches an extra
                            coin (a sly grace), into his pouch (a plink)]
  s04 crowd     B-flat -> G minor 2/4   the news: the street tune, claps, a xylophone scamper; his head questioning
                            on '撒该也想看看' (change); G minor on '撒该心想' (change): a ticking clock of woodblocks;
                            E-flat on '可是，撒该的个子太矮了' (change), a bassoon plunk; G minor on '他跳呀跳' (change):
                            a xylophone glissando up on each jump that falls back, a bassoon 'nope'; C minor on '他踮起脚'
                            (change): a clarinet slide up the chord, a wobbling trill, the fall; G minor on '前面的人'
                            (change): a wall of low brass; G minor on '他想挤进去' (change): pushing pizzicato, the thud
                            of the elbow; G minor on '撒该急得团团转' (change): a circling figure; E-flat add9 on '小朋友，
                            你猜' (change); F7sus4 at the end of the question (change), hanging through the 1.5 s
                            guess: the koto rolls it, the marimba ticks while he thinks, and his tune's creep (E-flat,
                            E, F) rises on the clarinet as the idea comes [the thought bubble (a pluck), its '?' (a
                            plucked question), the two jumps (take-off, glissando, landing), the elbow (a thud), three
                            thinking dots (three xylophone notes climbing)]
  s05 tree      B-flat 2/4 -> E-flat 4/4 -> B-flat   F7sus4 held (the clarinet's F still hanging); the idea sting on
                            '有了' (change; the hit on the picture's light bulb); the scamper (his tune fast on the
                            xylophone over a running bassoon, woodblock feet) that screeches to a halt; E-flat on
                            '那里有一棵大大的桑树' (change): the tree on the horn; B-flat on '撒该爬呀爬' (change): one step up for
                            each climbing stage, D Eb F A over a rising bass B-flat C D F; B-flat high on the hoist onto
                            the sitting branch (a picture change); his tune an octave higher on flute and xylophone on
                            '嘿嘿' (change) [the light bulb, the halt (a plucked stop), the low branches glow (a glint),
                            hands on the fork (a run up), climbing stages 1 and 4, the hoist, he settles (a pluck), the
                            twig pushed aside (a muted-trumpet giggle)]
  s06 call      B-flat 2/4 -> E-flat -> C minor -> B-flat   the procession (soft pizzicato, harp, the darbuka's slow
                            taps); a hush on '停住了' (hit: a last pluck, the harp ringing, one string chord); warm E-flat
                            add9 on '他抬起头' (change); the call on the horn on '撒该，快下来' (change); G7 on '撒该吓了
                            一跳' (change); C minor on '耶稣认识我' (change), his head questioning to F7sus4; B-flat on
                            '他高兴极了' (change): a falling scale as he slides down the trunk, then his tune's pop and
                            zig-zag home, with claps [the jolt (a xylophone boing, a vibraslap) and the branch wobbling
                            (a koto tremolo), both arms up (a xylophone chord), he lands (a plucked plop), 'come!' (a
                            glint)]
  s07 grumble   G minor 2/4 -> E-flat   the low woodwind mutter over low pizzicato and tremolo; 'hmph' on '哼' (hit
                            and change: bassoon, muted trumpet, pizzicato, a guiro); G minor on '大家都说撒该是个坏人'
                            (change); the deceptive E-flat on '可是耶稣' (change): the call, warm on the horn, to F7
                            [Jesus's hand on his shoulder (a harp note), the gate opens with warm light (a harp and a
                            glint)]
  s08 promise   B-flat 2/4  the house (marimba, guitar); nervous (tiptoe pizzicato, a trembling clarinet, a snare roll);
                            the brave march on the trumpet on '主啊' (change); ta-da at the end of '我就还他四倍' (hit); the
                            glosses on '一半，就是' and '四倍，就是' (changes) with clear plucks [he stands up (a pluck), he
                            hops down (a soft thump), the money chest opens (a glint), the first card (a pluck), ten coins
                            in a row (a koto ripple of ten), two piles of five (two plucked chords), one pile to the poor
                            (a harp glint), a heart (a glint), the second card, one coin (one low pluck), four coins
                            popping out (four plucks climbing)]
  s09 saved     B-flat 2/4 -> D major   '耶稣笑了'; A7sus4 on '今天，救恩到了这一家' (change, a timpani roll); the
                            radiant D major on '救恩' (change; trumpet, horns, choir, strings, harp, glockenspiel, timpani
                            on the picture's light); B minor on '就是说' (change), the call on the clarinet in D; G on
                            '我来' (change); D on '撒该想看看耶稣' (change): his perky head in D; G on '原来耶稣也在找撒该'
                            (change): the call answering on the horn; D on '就像牧羊人' (change): the shepherd's echo on
                            the pan flute over a drone [Jesus smiles (a glint), the light, a heart rises over Zacchaeus
                            (a glint), the picture of the tree pops up (a pluck), the moonlit hills (a harp glint)]
  s10 heart     B-flat 2/4  the golden evening: the generous song on the horn over harp, strings and a shimmering koto
                            [a coin for the widow and four for the farmer (koto plucks), the hearts (glints)]
  s11 end       F 4/4 -> 2/4   the call on the marimba ('耶稣知道撒该的名字，也知道你的名字'); G minor 7 on '不管别人'
                            (change); F on '他也想住进你的心里' (change), the generous song's head; B-flat on '小朋友，如果
                            耶稣今天' (change), very soft; C7sus4 at the end of '你想对他说什么呢' (change), hanging through
                            the answer pause; the final F chord on the end card [the heart on '爱' and on '心' (glints),
                            the end card]

All the music stays under the narration (Seg.duck, low expression levels, melodies ducked further, accompaniment
figures thinned to the beats while a line is spoken); the loud moments (the ta-da, the idea, the top of the tree, the
radiant D) live in the pauses and are short and child-safe; the frustration stays comic, never anxious.
"""
import numpy as np

from audio.scorekit import PARTS, Part
from audio.scorelib import ChordTones, bassline, broken, drum, gliss, span_end
from audio.theory import midi

# ------------------------------------------------------------------------------------------- this film's colours
# General MIDI voices the shared orchestra (audio/scorekit.PARTS) does not list; registered here, for this story only,
# before any cue is written (the MIDI writer, the checks and the bus channel count read PARTS).
_EXTRA = [
    Part("xylo", 0, 13, "keys", 0.22, -5, 65, 103, jitter=0.004, duck_db=3.0),
    Part("marimba", 0, 12, "keys", -0.18, -2, 45, 96, jitter=0.006, duck_db=2.0),
    Part("mtpt", 0, 59, "wind", 0.12, -6, 54, 82, attack=0.02, jitter=0.007, duck_db=3.0),
    Part("tpt", 0, 56, "wind", 0.06, -8, 55, 84, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.5),
    Part("koto", 0, 107, "pluck", -0.32, -3, 48, 91, jitter=0.006, duck_db=2.0),
    Part("panflute", 0, 75, "wind", -0.1, -4, 60, 96, attack=0.03, jitter=0.008, duck_db=2.5),
]
for _p in _EXTRA:
    PARTS.setdefault(_p.name, _p)

# ------------------------------------------------------------------------------------------- themes (q = quarter)
# Zacchaeus (B-flat, 2/4): mi fa fi sol | do' . sol mi | fa re ti re | do
Z = ["D5:1/2 Eb5:1/2 E5:1/2 F5:1/2", "Bb5:1/2:s r:1/2 F5:1/2:s D5:1/2:s", "Eb5:1/2 C5:1/2 A4:1/2 C5:1/2",
     "Bb4:1:s r:1"]
Z_PROG = ["Bb:2", "Bb:2", "F7:2", "Bb:2"]
# the call (4/4): his tune made lyrical
CALL = ["D5:1 Eb5:1/2 E5:1/2 F5:2", "Bb5:3/2 A5:1/2 G5:1 F5:1", "Eb5:1 D5:1/2 C5:1/2 F5:1 A4:1", "Bb4:4"]
CALL_PROG = ["Bb:4", "Gm:2 Eb:2", "Cm7:2 F7:2", "Bb:4"]
# the generous song (2/4): mi . fa sol | do'. ti | la sol fa | sol -- | la sol fa | mi re do | re. ti | do
GEN = ["D5:1 Eb5:1/2 F5:1/2", "Bb5:3/2 A5:1/2", "G5:1 F5:1/2 Eb5:1/2", "F5:2", "G5:1 F5:1/2 Eb5:1/2",
       "D5:1 C5:1/2 Bb4:1/2", "C5:3/2 A4:1/2", "Bb4:2"]
GEN_PROG = ["Bb:2", "Eb:2", "Cm7:2", "F7sus4:1 F7:1", "Eb:2", "Bb/F:2", "F7:2", "Bb:2"]
# the Jericho street tune (B-flat, 2/4, koto): sol le sol mi do | re mi re do | ...
JER = ["F5:1/2 Gb5:1/4 F5:1/4 D5:1/2 Bb4:1/2", "C5:1/2 D5:1/4 C5:1/4 Bb4:1", "G5:1/2 Ab5:1/4 G5:1/4 Eb5:1/2 C5:1/2",
       "D5:1/2 C5:1/2 A4:1", "F5:1/2 Gb5:1/4 F5:1/4 D5:1/2 Bb4:1/2", "D5:1/2 Eb5:1/4 D5:1/4 Bb4:1/2 G4:1/2",
       "G5:1/2 Eb5:1/2 F5:1/4 Eb5:1/4 C5:1/4 A4:1/4", "Bb4:1 r:1"]
JER_PROG = ["Bb:2", "Bb:2", "Cm7:2", "F7:2", "Bb:2", "Gm:2", "Eb:1 F7:1", "Bb:1 F7:1"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…—"
SOUND_CHARS = set()


def _groups(text):
    """[(char index, text)] of the punctuation-separated groups of an utterance."""
    out, cur, start = [], "", 0
    for k, ch in enumerate(text):
        if ch in PUNCT:
            if cur:
                out.append((start, cur))
                cur = ""
        else:
            if not cur:
                start = k
            cur += ch
    if cur:
        out.append((start, cur))
    return out


def _units(text):
    out = []
    for k, g in _groups(text):
        if len(g) > 1 and all(ch in SOUND_CHARS for ch in g):
            out += [(k + j, ch) for j, ch in enumerate(g)]
        else:
            out.append((k, g))
    return out


def _char_time(ln, k):
    """Cue-relative time of character k of a line (Cue.at's chunk interpolation)."""
    chunks = ln.get("chunks") or [{"text": ln["text"], "start": ln["start"], "end": ln["end"]}]
    pos = 0
    for ch in chunks:
        txt = ch["text"]
        j = ln["text"].find(txt, pos)
        j = pos if j < 0 else j
        if j <= k <= j + len(txt):
            w = lambda s: sum(0.5 if c_ in "，。！？：；、" else 1.0 for c_ in s)
            return float(ch["start"] + w(txt[:k - j]) / max(1e-9, w(txt)) * (ch["end"] - ch["start"]))
        pos = j + len(txt)
    return float(ln["start"])


_SEGS = {}


def _clip_segments(wav):
    """(speech segments [(start, end)] in s from the clip start, clip length): 10 ms frames above 5 % of the peak RMS,
    gaps under 50 ms merged, islands under 30 ms dropped -- the way the scenes measure the voice
    (stories/noah/scenes/s01_title.py voice_marks); None without the clip."""
    key = str(wav)
    if key in _SEGS:
        return _SEGS[key]
    out = None
    try:
        import soundfile as sf
        x, sr = sf.read(str(wav), dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        hop = int(sr * 0.01)
        n = len(x) // hop
        e = np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1))
        on = e / max(1e-6, float(e.max())) > 0.05
        segs, st = [], None
        for i, v in enumerate(on):
            if v and st is None:
                st = i
            if not v and st is not None:
                segs.append([st, i])
                st = None
        if st is not None:
            segs.append([st, n])
        merged = []
        for a_, b_ in segs:
            if merged and a_ - merged[-1][1] < 5:
                merged[-1][1] = b_
            elif b_ - a_ >= 3:
                merged.append([a_, b_])
        out = ([(a_ * 0.01, b_ * 0.01) for a_, b_ in merged], n * hop / sr)
    except Exception:
        out = None
    _SEGS[key] = out
    return out


def _prop(t0, t1, groups):
    n = sum(len(g) for g in groups) + 0.5 * (len(groups) - 1)
    out, acc = [], 0.0
    for g in groups:
        a_ = t0 + (t1 - t0) * acc / n
        acc += len(g)
        out.append((a_, t0 + (t1 - t0) * acc / n))
        acc += 0.5
    return out


def _voice_groups(c, i):
    """[(group, start, end)] of the punctuation groups of line i (cue-relative), measured in the voice clip: the subtitle
    chunks are the anchors; inside a chunk the group boundaries are the clip's pauses that best match the character
    estimate, longer pauses preferred (the scenes' voice_marks method, scaled to the line's length in this timeline);
    proportional inside the chunk without the clip."""
    import itertools
    from engine.paths import BUILD

    ln = c.scene["lines"][i]
    clip = _clip_segments(BUILD / ln["wav"]) if ln.get("wav") else None
    segs = []
    if clip and clip[1] > 0:
        f = (ln["end"] - ln["start"]) / clip[1]
        segs = [(ln["start"] + a_ * f, ln["start"] + b_ * f) for a_, b_ in clip[0]]
    chunks = ln.get("chunks") or [{"text": ln["text"], "start": ln["start"], "end": ln["end"]}]
    out = []
    for ci, ch in enumerate(chunks):
        groups = [g for _, g in _groups(ch["text"])]
        if not groups:
            continue
        lo = ch["start"] - 0.25
        hi = chunks[ci + 1]["start"] - 0.1 if ci + 1 < len(chunks) else ch["end"] + 0.3
        mine = [sg for sg in segs if lo <= (sg[0] + sg[1]) / 2 <= hi]
        if not mine:
            out += [(g, a_, b_) for g, (a_, b_) in zip(groups, _prop(ch["start"], ch["end"], groups))]
            continue
        s0, s1 = mine[0][0], mine[-1][1]
        if len(groups) == 1:
            out.append((groups[0], s0, s1))
            continue
        est = _prop(s0, s1, groups)
        gaps = [(k, mine[k][1], mine[k + 1][0]) for k in range(len(mine) - 1)]
        k = len(groups) - 1
        best = None
        if len(gaps) >= k:
            for combo in itertools.combinations(gaps, k):
                cost = sum(abs((ga + gb) / 2 - (est[j][1] + est[j + 1][0]) / 2) - 2.0 * min(gb - ga, 0.35)
                           for j, (_, ga, gb) in enumerate(combo))
                if best is None or cost < best[0]:
                    best = (cost, combo)
        if best is None:
            out += [(g, a_, b_) for g, (a_, b_) in zip(groups, est)]
            continue
        cuts = [g[0] for g in best[1]]
        st = 0
        for j, g in enumerate(groups):
            en = cuts[j] if j < k else len(mine) - 1
            out.append((g, mine[st][0], mine[en][1]))
            st = en + 1
    return out


def syl(c, phrase, n):
    """Cue-relative onsets of the n punctuation groups that start where `phrase` starts, as the speaker says them
    (_voice_groups; the subtitle interpolation when the clip's groups do not match the text)."""
    i = c.find(phrase)
    ln = c.scene["lines"][i]
    units = _units(ln["text"])
    k0 = ln["text"].index(phrase)
    u0 = max(k for k, (p, _) in enumerate(units) if p <= k0)
    vg = _voice_groups(c, i)
    if len(vg) == len(units):
        times = [a_ for _, a_, _ in vg]
        p0, g0 = units[u0]
        if k0 > p0:                                            # the phrase starts inside its group
            times[u0] = vg[u0][1] + (k0 - p0) / max(1, len(g0)) * (vg[u0][2] - vg[u0][1])
    else:
        times = [_char_time(ln, p) for p, _ in units]
    for k in range(1, len(times)):
        times[k] = max(times[k], times[k - 1] + 0.05)
    n = min(n, len(units) - u0)
    return times[u0:u0 + n]


def voice_at(c, phrase):
    """Cue-relative time where `phrase` is spoken (syl)."""
    return syl(c, phrase, 1)[0]


def chars(c, phrase, ch):
    """Cue-relative onsets of every character `ch` in the line containing `phrase`, as the speaker says them: the
    measured punctuation groups (_voice_groups) divided evenly among their characters (the subtitle interpolation when
    the clip's groups do not match the text)."""
    i = c.find(phrase)
    ln = c.scene["lines"][i]
    text = ln["text"]
    vg = _voice_groups(c, i)
    units = _groups(text)
    out = []
    if len(vg) == len(units):
        for (p, g), (_, a_, b_) in zip(units, vg):
            for j, x in enumerate(g):
                if x == ch:
                    out.append(a_ + j / len(g) * (b_ - a_))
    else:
        out = [_char_time(ln, k) for k, x in enumerate(text) if x == ch]
    return out


# ------------------------------------------------------------------------------------------- the picture
_PICTURE = {}


def _forget_voice_marks(sid):
    """Scene helpers may cache voice marks by (scene id, line index): forget this scene's, so a re-timed timeline
    (audio/test_score.py) builds the scene for that timeline."""
    import sys
    for name, mod in list(sys.modules.items()):
        cache = getattr(mod, "_SEG_CACHE", None) if name.startswith("stories.") else None
        if isinstance(cache, dict):
            for key in [k for k in cache if isinstance(k, tuple) and k and k[0] == sid]:
                del cache[key]


def picture(c, name, t0=-1e9, t1=1e9):
    """Cue-relative times of this scene's own sound-effect cues called `name` between t0 and t1 (read at build time
    from the scene code, as music_check reads PICTURE_HITS); None when the scene does not build (yet)."""
    tl = c.score.tl
    key = (round(c.t0, 4), tuple(c.lines), id(tl), float(tl["duration"]))
    if c.id not in _PICTURE or _PICTURE[c.id][0] != key:
        try:
            from engine.loader import build_scene
            _forget_voice_marks(c.id)
            _PICTURE[c.id] = (key, [(x["name"], float(x["at"])) for x in build_scene(c.id, tl).sfx_cues])
        except Exception:
            _PICTURE[c.id] = (key, None)
    cues = _PICTURE[c.id][1]
    if cues is None:
        return None
    return sorted(t for nm, t in cues if nm == name and t0 <= t <= t1)


def pic(c, name, phrase, k=0, off=0.0, lo=None, hi=None):
    """The k-th picture cue `name` from the start of the line containing `phrase` (minus 0.3 s; None: from the scene
    start) plus off -- chosen as music_check.picture_targets chooses a PICTURE_HITS target -- or None (no scene, no
    such cue, or outside [lo, hi]; default: inside this cue)."""
    t0 = c.ls(c.find(phrase)) - 0.3 if phrase else -1e9
    ts = picture(c, name, t0)
    if not ts or k >= len(ts):
        return None
    t = ts[k] + off
    lo = 0.02 if lo is None else lo
    hi = c.dur - 0.02 if hi is None else hi
    return t if lo <= t <= hi else None


def pics(c, name, t0=-1e9, t1=1e9):
    """picture() inside this cue ([] without the scene)."""
    return [t for t in (picture(c, name, t0, t1) or []) if 0.02 <= t <= c.dur - 0.02]


def seg_at(c, segs, t):
    """(segment, q) of cue-relative time t among segs (a hit a hair before a chord change takes the new chord)."""
    for sg in segs:
        if sg.t0 - 1e-6 <= c.t0 + t < sg.t1 - 1e-6:
            q = min(max(sg.q_of(c.t0 + t), 0.0), sg.n_q - 1e-3)
            se = span_end(sg, q + 1e-6)
            if se - q < 0.04 and se < sg.n_q - 1e-3:
                q = se
            return sg, q
    sg = segs[0] if c.t0 + t < segs[0].t0 else segs[-1]
    return sg, (0.0 if sg is segs[0] and c.t0 + t < sg.t0 else sg.n_q - 0.1)


def accent(c, segs, t, what=None, glock=None, xylo=None, koto=None, pluck=None, marim=None, harp=None, low=None,
           block=None, vel=46):
    """A picture hit at cue-relative time t on tones of the chord sounding there (glock / xylophone / koto / pizzicato /
    marimba / harp = (lo, hi) ranges: the highest chord tone in range; low=True: a soft low thump; block: a woodblock
    or hand-drum key); synced if `what`."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if xylo:
        sg.add("xylo", q, _dq(sg, q, 0.5), top(sg, q, *xylo), vel, "arp", "h")
    if koto:
        sg.add("koto", q, _dq(sg, q, 0.75), top(sg, q, *koto), vel + 2, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if marim:
        sg.add("marimba", q, _dq(sg, q, 0.75), top(sg, q, *marim), vel, "arp", "h")
    if harp:
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, *harp), vel, "arp", "h")
    if low:
        thump(sg, q, vel=vel + 2)
    if block:
        drum(sg, q, block, vel - 6)
    if what:
        sg.sync(what, q, t)
    return sg, q


def qpos(seg, c, t, lo=0.0, hi=None):
    hi = seg.n_q - 0.1 if hi is None else hi
    return min(max(seg.q_of(c.t0 + t), lo), hi)


def edges48(seg, c, times, min_gap=6):
    end = int(round(seg.n_q * 48))
    out = [0]
    for t in times:
        e = int(round(seg.q_of(c.t0 + t) * 48))
        out.append(max(e, out[-1] + min_gap))
    out.append(end)
    for k in range(len(out) - 2, 0, -1):
        out[k] = min(out[k], out[k + 1] - min_gap)
    return out


def prog48(seg, chords, edges):
    seg.prog(" ".join(f"{ch}:{edges[k + 1] - edges[k]}/48" for k, ch in enumerate(chords)))


def clear_near(c, t, win=0.12, roles=("arp",)):
    """Drop this cue's accompaniment onsets (plucked and broken-chord figures) within win s of cue-relative time t,
    so a picture accent there is one clear attack."""
    sc = c.score
    ta = c.t0 + t
    sc.notes[:] = [n for n in sc.notes if not (n.seg.cue is c and n.role in roles and abs(n.seg.t(n.q) - ta) < win)]


def hit(c, segs, name, phrase, k, what, clear=True, win=0.12, **kw):
    """The picture cue (name, phrase, k) -- picked as music_check picks a PICTURE_HITS target -- gets an accent on
    the chord sounding there (accent() kwargs), synced; returns its time, or None without the scene / the cue."""
    t = pic(c, name, phrase, k)
    if t is not None:
        if clear:
            clear_near(c, t, win=win)
        accent(c, segs, t, what, **kw)
    return t


def lead(c, segs, name, phrase, k, lo, hi, what, **kw):
    """The picture cue (name, phrase, k): (time, True) when it lies in [lo, hi] -- the caller puts its main attack
    there and syncs it --; (None, False) without it; when it exists outside the window it gets its own synced accent
    (accent() kwargs) and (None, False) is returned, so every listed picture hit is always placed."""
    t = pic(c, name, phrase, k)
    if t is None:
        return None, False
    if lo <= t <= hi:
        return t, True
    clear_near(c, t)
    accent(c, segs, t, what, **kw)
    return None, False


def climb(c, segs, times, part="xylo", lo=69, hi=94, vel=40, sync=(), what="", glock=True, pz=False):
    """One note per picture cue, climbing the chord tones (a pluck for each pop); those whose index is in `sync` are
    louder and synced."""
    prev = lo - 1
    for k, t in enumerate(times):
        sg, q = seg_at(c, segs, t)
        ts = sg.chord_at(q + 1e-3).tones(prev + 1, hi) or sg.chord_at(q + 1e-3).tones(lo, hi)
        prev = ts[0]
        loud = k in sync
        sg.add(part, q, _dq(sg, q, 0.5), prev, vel + (8 if loud else 0), "arp", "h")
        if pz and 55 <= prev - 12 <= 100:
            sg.add("pz_hi", q, _dq(sg, q, 0.25), prev - 12, vel, "arp", "h")
        if loud:
            if glock and prev + 12 <= 105:
                sg.add("glock", q, _dq(sg, q, 0.5), prev + 12, vel - 4, "arp", "h")
            sg.sync(f"{what} ({k + 1})", q, t)


# ------------------------------------------------------------------------------------------- writing helpers
STR = ["vla", "vln2", "vln1", "vc", "cb"]


def lv(seg, parts, a, b=None, q0=0.0, q1=None):
    """Flat expression (dB) for parts over the segment (or q0..q1), a -> b."""
    seg.expr(parts, [(q0, a), (seg.n_q if q1 is None else q1, a if b is None else b)])


def strings(seg, vel=40, lo=50, hi=69, bass=(41, 53), q0=0.0, q1=None, cb=(29, 41), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vla", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
            bass_hi=bass[1])
    if cb:
        bassline(seg, "cb", cb[0], cb[1], cb_vel or vel - 2, q0=q0, q1=q1)


def _dq(seg, q, dq):
    return max(0.1, min(dq, span_end(seg, q + 1e-6) - q, seg.n_q - q))


def top(seg, q, lo, hi, k=-1):
    ts = seg.chord_at(q + 1e-3).tones(lo, hi)
    return ts[max(-len(ts), min(k, len(ts) - 1))]


def thump(seg, q, vel=50, kit=True):
    pcs = seg.chord_at(q + 0.02).pcset & seg.chord_at(min(q + 0.4, seg.n_q - 1e-3)).pcset or \
        seg.chord_at(q + 0.02).pcset
    seg.add("timp", q, _dq(seg, q + 0.02, 0.5), [p for p in range(38, 51) if p % 12 in pcs][0], vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q + 0.02, 0.4), [p for p in range(29, 41) if p % 12 in pcs][0], vel + 2, "bass", "h")
    if kit:
        seg.add("okit", q, 1, 36, vel - 8, "perc", "h")


def gliss_in(seg, part, q, dur_s, lo, hi, **kw):
    room = seg.t(seg.n_q) - seg.t(q) - 0.03
    if room >= 0.12:
        gliss(seg, part, q, min(dur_s, room), lo, hi, **kw)


def sweep(seg, q, dur_s=0.6, lo="A4", hi="A6", v0=30, v1=46, up=True, part="xylo"):
    """A glissando (xylophone, harp, koto) over the chord at q."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1, scale=ChordTones(seg.chord_at(q + 1e-3)))


def scale_run(seg, q, dur_s=0.45, lo="Bb4", hi="Bb5", v0=30, v1=44, up=True, part="koto"):
    """A run up (or down) the segment's scale -- the koto's qanun flourish, a clarinet slide."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1)


def roll_chord(seg, q, lo, hi, vel=46, gap_s=0.05, part="marimba", n=6):
    """The chord at q rolled up from its lowest tone in [lo, hi] (n notes), each held to the chord's end."""
    ts = []
    for p in seg.chord_at(q + 1e-3).tones(lo, hi):
        if not ts or p - ts[-1] >= 3:
            ts.append(p)
    ts = ts[:n]
    t0 = seg.t(q)
    for k, p in enumerate(ts):
        qk = seg.q_of(t0 + gap_s * k)
        if qk >= span_end(seg, q + 1e-6) - 0.05:
            break
        seg.add(part, qk, span_end(seg, q + 1e-6) - qk, p, vel - 2 * k, "arp")


def _alt_bass(ch, lo, hi):
    """The chord's other bass note for an oom-pah: its fifth (or its root under an inversion) near the bass."""
    b0 = ch.bass_note(lo, hi)
    for pc_ in ((ch.root + 7) % 12, ch.root):
        cand = [p for p in range(lo, hi + 6) if p % 12 == pc_ and p != b0]
        if cand:
            return min(cand, key=lambda p: abs(p - b0))
    return b0


def oom(seg, q0, q1, vel=40, bass=(33, 45), hi=(58, 70), n=3, bpart="pz_cb", cpart="marimba", lively=False):
    """The street's oom-pah: a plucked bass on every beat (the chord's bass, then its fifth while the chord stays), the
    marimba's chord on the off-beat (2/4: the 'and'; lively: the 'and' and the 'a'); 4/4: every beat."""
    beat = seg.beat_q
    offs = ((0.5, 0.75) if lively else (0.5,)) if seg.meter in ("2/4", "4/4") else (1.0,)
    q, k, last = q0, 0, None
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        k = 0 if ch is not last else k + 1
        p = ch.bass_note(*bass) if k % 2 == 0 else _alt_bass(ch, *bass)
        seg.add(bpart, q, _dq(seg, q, beat * 0.6), p, vel, "arp", "s")
        for off in offs:
            qq = q + off
            if qq < q1 - 1e-6 and cpart and not (off == 0.75 and bool(seg.score.speaking(seg.t(qq)))):
                for pt in seg.chord_at(qq + 1e-3).tones(*hi)[:n]:
                    seg.add(cpart, qq, _dq(seg, qq, 0.25), pt, vel - 8, "arp", "s")
        last = ch
        q += beat


def steps(seg, q0, q1, vel=38, lo=46, hi=62, pat=(0, 2, 1, 2), part="bsn", thin=True):
    """Zacchaeus's little steps: staccato bassoon eighths on the chord's bass, fifth and third (only the beats while a
    line is spoken)."""
    broken(seg, part, q0, q1, pat, lo, hi, vel=vel, step=0.5, art="s", ring=False, thin=thin, accent=4)


def darbuka(seg, q0, q1, vel=32, sparse=False):
    """The Jericho darbuka (2/4): DOUM . tek . | DOUM tek-tek tek (low conga, high bongo); only the beats while a line is
    spoken; sparse: DOUM . . . tek . . ."""
    pat = ((0.0, 64, 0), (1.0, 60, -6)) if sparse else \
        ((0.0, 64, 0), (0.5, 60, -7), (1.0, 64, -4), (1.25, 60, -10), (1.5, 60, -6))
    bar = 2.0
    b = int(q0 // bar)
    while b * bar < q1 - 1e-6:
        for off, key, dv in pat:
            q = b * bar + off
            if q0 - 1e-6 <= q < q1 - 1e-6:
                on_beat = abs((q + 1e-6) % 1.0) < 2e-6
                if not on_beat and bool(seg.score.speaking(seg.t(q))):
                    continue
                drum(seg, q, key, vel + dv)
        b += 1


def claps(seg, q0, q1, vel=30, offs=(1.0,), every=1.0):
    """Hand-claps (beat 2 of the 2/4 bar, or the given off-sets) in the pauses only."""
    b = int(q0 // 2.0)
    while b * 2.0 < q1 - 1e-6:
        for off in offs:
            q = b * 2.0 + off
            if q0 - 1e-6 <= q < q1 - 1e-6 and not bool(seg.score.speaking(seg.t(q))):
                drum(seg, q, 39, vel)
        b += 1


def tick(seg, q0, q1, vel=28, step=0.5):
    """A clock: high and low woodblocks alternating (tick-tock)."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        drum(seg, q, 76 if k % 2 == 0 else 77, vel - (0 if k % 2 == 0 else 4))
        q += step
        k += 1


def run(seg, part, q0, notes, step, vel=40, role="melody", art=""):
    """A quick scale run: the given pitches, one every `step` q from q0."""
    out = []
    for k, nm in enumerate(notes):
        q = q0 + k * step
        if q < seg.n_q - 1e-6:
            out.append(seg.add(part, q, min(step, seg.n_q - q), nm, vel + k, role, art))
    return out


def trem(seg, part, q0, q1, pitch, vel, rate=0.125, role="arp", alt=None):
    """A plucked tremolo (koto, xylophone): the same note re-struck every `rate` q (alternating with `alt`)."""
    pitch = midi(pitch) if isinstance(pitch, str) else pitch
    alt = midi(alt) if isinstance(alt, str) else alt
    q, k = q0, 0
    while q < q1 - 1e-6:
        p = alt if (alt is not None and k % 2) else pitch
        seg.add(part, q, min(rate, q1 - q), p, vel + (3 if k % 2 == 0 else -3), role)
        q += rate
        k += 1


def jump(c, segs, t, t_land=None, vel=42, what=None):
    """The jump-and-fall gag: a woodblock and a pizzicato pluck on the take-off, a xylophone glissando up the chord,
    two notes falling back and a soft low plop as he lands (on the picture's landing when given)."""
    sg, q = seg_at(c, segs, t)
    ch = sg.chord_at(q + 1e-3)
    p0 = top(sg, q, 67, 74)
    sg.add("pz_hi", q, _dq(sg, q, 0.25), p0, vel + 4, "arp", "h")
    sg.add("xylo", q, _dq(sg, q, 0.25), p0, vel, "arp", "h")
    drum(sg, q, 76, vel - 4)
    t_land = t + 0.34 if t_land is None else t_land
    up = max(0.1, min(0.18, (t_land - t) * 0.45))
    gliss_in(sg, "xylo", q + 0.02, up, p0 + 1, 98, up=True, v0=vel - 10, v1=vel, scale=ChordTones(ch))
    prev = 94
    for k in range(2):
        tk = t + up + 0.05 + 0.06 * k
        if tk > t_land - 0.03:
            break
        sg2, q2 = seg_at(c, segs, tk)
        ts = [p for p in sg2.chord_at(q2 + 1e-3).tones(79, 93) if p < prev]
        if sg2 is sg and ts:
            prev = ts[-1]
            sg.add("xylo", q2, _dq(sg, q2, 0.25), prev, vel - 4 - 3 * k, "arp", "S")
    sg3, q3 = seg_at(c, segs, t_land)
    sg3.add("pz_lo", q3, _dq(sg3, q3, 0.25), sg3.chord_at(q3 + 1e-3).bass_note(43, 55), vel - 4, "arp", "s")
    if what:
        sg.sync(what, q, t)


def pick_times(times, lo, hi, n=None):
    out = [t for t in (times or []) if lo <= t <= hi]
    return out[:n] if n else out


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """The title (B-flat, 2/4): a bar of little steps (bassoon, pizzicato, the marimba's off-beat, the darbuka), then
    Zacchaeus's tune on the clarinet; the picture: a xylophone grace as he peeks out of the leaves, a glint for the
    ribbon, a xylophone step climbing for each of the six title characters, and the ta-da (xylophone, glockenspiel,
    pizzicato, the koto's flourish before it) on the finished title's sparkle."""
    c.gain(-6.0)
    s = c.seg(0, c.dur, 5, "2/4", "Bb major", nominal=101, label="title")
    segs = (s,)
    s.duck(1.5)
    s.duck(3.0, parts=["clar", "xylo", "koto"])
    # the ta-da on the finished title (the picture's sparkle): the B-flat arrives with it
    t_sp = pic(c, "sparkle", None, 0)
    ok = t_sp is not None and s.t(7.4) - c.t0 <= t_sp <= s.t(9.0) - c.t0
    q_td = qpos(s, c, t_sp, 7.4, 9.0) if ok else 8.0
    q_b = min(q_td, 8.0)
    f7 = int(round((q_b - 6.0) * 48))
    s.prog(f"Bb:2 | Bb:2 | Bb:2 | F7:{f7}/48 Bb:{192 - f7}/48")
    s.mel("clar", "r:2 | " + bars(Z, 0, 3) + " | Bb4:2", vel=50)
    steps(s, 0, min(8.0, q_b), vel=36)
    oom(s, 0, min(8.0, q_b), vel=36)
    darbuka(s, 0, 8, vel=30)
    s.pad(["vla", "vla", "vln1"], 3, 55, 74, vel=30, bass_ref=(33, 45))
    if t_sp is not None and not ok:
        accent(c, segs, t_sp, "the title sparkles (a glint)", glock=(86, 98), vel=44)
    for nm in ("Bb5", "D6"):
        s.add("xylo", q_td, _dq(s, q_td, 1.0), nm, 46, "arp", "h")
    s.add("glock", q_td, _dq(s, q_td, 1.5), "F6", 42, "arp", "h")
    for nm in ("Bb3", "F4", "D5"):
        s.add("pz_hi", q_td, _dq(s, q_td, 0.5), nm, 46, "arp", "h")
    s.add("pz_cb", q_td, _dq(s, q_td, 0.5), "Bb1", 46, "bass", "h")
    roll_chord(s, q_td + 0.08, 58, 82, vel=38, part="marimba", n=5)
    drum(s, q_td, 81, 30)
    s.sync("ta-da: the finished title" + (" (picture)" if ok else ""), q_td, s.t(q_td) - c.t0)
    # he peeks out of the leaves: a xylophone grace; the ribbon unfurls: a glint
    t_pk = pic(c, "pop", None, 0)
    if t_pk is not None and t_pk < 2.6:
        clear_near(c, t_pk)
        sg_, q_p = accent(c, segs, t_pk, "Zacchaeus peeks out (a xylophone grace)", xylo=(82, 89), vel=44)
        g = q_p - 0.12
        if g > 0:
            sg_.add("xylo", g, 0.1, top(sg_, q_p, 82, 89) - 2, 34, "fx", "S")
    hit(c, segs, "chime", None, 0, "the ribbon unfurls (a glint)", glock=(86, 98), vel=42)
    t_ch = pic(c, "chime", None, 0)
    pops = pics(c, "pop", (t_ch + 0.2) if t_ch is not None else 2.0, s.t(q_td) - c.t0 - 0.1)
    if pops:
        for t_ in pops:
            clear_near(c, t_)
        climb(c, segs, pops, part="xylo", lo=77, hi=94, vel=42, sync=(0, len(pops) - 1),
              what="a title character pops in", glock=True)
    lv(s, ["clar"], -16)
    lv(s, ["bsn"], -17)
    lv(s, ["pz_cb"], -13)
    lv(s, ["marimba"], -19)
    lv(s, ["xylo"], -15)
    lv(s, ["koto"], -15)
    lv(s, "hand", -18)
    lv(s, ["pz_hi"], -13)
    lv(s, ["glock"], -13)
    s.expr(["vla", "vln1"], [(0, -25), (2, -23), (10, -22)])


def question(c):
    """The modern frame (F major, 2/4): marimba, nylon guitar and soft strings, a xylophone hop for each of the boy's
    hops and a low pluck as he drops back on his heels; Gm7 and a hanging C7sus4 on '什么都看不见'; F on '今天':
    Zacchaeus's tune small, on the bassoon, in F ('有一个人也是这样'); B-flat on '可是，他想了一个好办法', C7 under dad's lift
    (a xylophone run up on the picture), and F on '好办法' with a xylophone ping as the boy is up and beaming."""
    c.gain(-4.5)
    t_q = c.at("什么都看不见")
    t_today = c.ls(c.find("今天"))
    t_idea = c.at("可是，他想了一个好办法")
    t_good = c.at("好办法")
    a = c.seg(0, t_q, 3, "2/4", "F major", nominal=88, label="question-crowd")
    h = c.seg(t_q, t_today, 1, "2/4", "F major", nominal=None, label="question-see")         # the question hangs
    t = c.seg(t_today, t_idea, 3, "2/4", "F major", nominal=100, label="question-today")
    i = c.seg(t_idea, t_good, 1, "2/4", "F major", nominal=None, label="question-but")
    g = c.seg(t_good, c.dur, 1, "2/4", "F major", nominal=None, label="question-idea")
    segs = (a, h, t, i, g)
    for sg in segs:
        sg.duck(1.5)
    a.prog("F:2 | Am7:2 | Dm7:2")
    h.prog("Gm7:1 C7sus4:1")
    t.prog("F:2 | F:2 | C7:2")
    i.prog("Bb:1 C7:1")
    g.prog("F:2")
    h.sync("'什么都看不见': the question (Gm7)", 0, t_q, kind="change")
    t.sync("'今天': the story begins (F)", 0, t_today, kind="change")
    i.sync("'可是，他想了一个好办法' (B-flat)", 0, t_idea, kind="change")
    g.sync("'好办法': the idea (F)", 0, t_good, kind="change")
    # 'child, have you ever been stuck behind the grown-ups?': the cosy frame
    a.mel("marimba", "A4:1 Bb4:1/2 B4:1/2 | C5:2 | F5:2", vel=48)
    broken(a, "guitar", 0, 6, (0, 2, 1, 2), 41, 57, vel=34, thin=True)
    a.pad(["vla", "vla", "vln1"], 3, 50, 67, vel=30, bass_ref=(41, 53))
    bassline(a, "vc", 41, 53, 30)
    a.duck(2.5, parts=["marimba"])
    lv(a, ["marimba"], -14)
    lv(a, ["guitar"], -13)
    a.expr(["vla", "vln1", "vc"], [(0, -24), (2, -22), (6, -22)])
    hops = pick_times(pics(c, "thud"), 0.0, t_q - 0.1, 2)
    for k_, t_ in enumerate(hops):                           # the boy hops (a xylophone hop and a pluck)
        clear_near(c, t_)
        accent(c, segs, t_, f"the boy hops ({k_ + 1})", xylo=(77, 86), pluck=(55, 64), block=76, vel=44)
    # 'can't see anything?': Gm7, then C7sus4 hangs through the pause (a guitar heartbeat, the marimba asks)
    h.mel("marimba", "r:1/2 D5:1/2 C5:1", vel=40)
    t_heel = pick_times(pics(c, "thud"), t_q - 0.1, t_today - 0.1, 1)
    if t_heel:                                               # back on his heels, pouting: a soft low pluck
        accent(c, segs, t_heel[0], "back on his heels (a low pluck)", pluck=(55, 62), block=77, vel=40)
    for k_ in range(8):
        h.add("guitar", 0.25 * k_, 0.25, top(h, 0.25 * k_, 43, 57, -1 - k_ % 2), 30 + (4 if k_ % 2 == 0 else 0),
              "arp", "s")
    h.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_part="vc", bass_lo=41, bass_hi=53)
    lv(h, ["marimba"], -15)
    lv(h, ["guitar"], -13)
    h.expr(["vla", "vln1", "vc"], [(0, -20), (2, -20)])
    # 'today's story has someone just like that': Zacchaeus's tune, small, on the bassoon (in F)
    t.mel("bsn", "A3:1/2 Bb3:1/2 B3:1/2 C4:1/2 | F4:1/2:s r:1/2 C4:1/2:s A3:1/2:s | Bb3:1/2 G3:1/2 E3:1/2 G3:1/2",
          vel=46)
    oom(t, 0, 6, vel=32, bass=(29, 41), hi=(57, 69), cpart="marimba")
    t.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=28, bass_ref=(29, 41))
    t.duck(2.0, parts=["bsn"])
    lv(t, ["bsn"], -15)
    lv(t, ["pz_cb"], -13)
    lv(t, ["marimba"], -20)
    t.expr(["vla", "vln1"], [(0, -23), (6, -23)])
    # 'but he thought of a good idea!': B-flat, C7 ... F on '好办法'
    i.mel("bsn", "F3:1/2:s r:1/2 E3:1", vel=40)
    i.pad(["vla", "vla", "vln1"], 3, 52, 70, vel=30, bass_part="vc", bass_lo=41, bass_hi=53)
    i.add("pz_cb", 0, 0.5, "Bb1", 40, "bass", "s")
    i.add("pz_cb", 1, 0.5, "C2", 40, "bass", "s")
    lv(i, ["bsn"], -16)
    lv(i, ["pz_cb"], -13)
    i.expr(["vla", "vln1", "vc"], [(0, -23), (2, -21)])
    t_up_, ok_up = lead(c, segs, "sparkle", "可是，他想了一个好办法", 0, t_good - 0.05, g.t(1.6) - c.t0,
                        "the boy is up (a glint)", glock=(86, 98), vel=40)
    q_up = qpos(g, c, t_up_, 0.0, 1.6) if ok_up else 0.0
    g.add("xylo", q_up, _dq(g, q_up, 1.0), "C6", 46, "arp", "h")
    g.add("xylo", q_up, _dq(g, q_up, 1.0), "F6", 44, "arp", "h")
    g.add("glock", q_up, _dq(g, q_up, 1.5), "A6", 38, "arp", "h")
    if ok_up:
        g.sync("the boy is up and beaming (a xylophone ping)", q_up, t_up_)
    g.add("pz_cb", 0, 1, "F1", 42, "bass", "h")
    roll_chord(g, 0.1, 57, 81, vel=38, part="marimba", n=5)
    drum(g, q_up, 81, 28)
    g.add("pz_hi", 0, 0.5, "C4", 40, "arp", "h")
    g.add("pz_hi", 0, 0.5, "A4", 40, "arp", "h")
    g.sync("'好办法': the idea (F)", 0, t_good)
    g.pad(["vla", "vla", "vln1"], 3, 52, 72, vel=30, bass_part="vc", bass_lo=41, bass_hi=53)
    g.add("bsn", 0, 0.5, "F3", 40, "melody", "s")
    q_ar = min(max(q_up + 0.5, 0.75), 1.25)                  # after the ping: the guitar rolls on, the marimba waves
    broken(g, "guitar", q_ar, 2.0, (0, 2, 4, 2, 4, 2), 41, 64, vel=28, step=0.25, ring=False)
    for k_, nm in enumerate(("A4", "C5", "F5")):
        qq = q_ar + 0.25 + 0.2 * k_
        if qq < 1.9:
            g.add("marimba", qq, 2.0 - qq, nm, 32 + 2 * k_, "arp")
    lv(g, ["guitar"], -15)
    lv(g, ["xylo"], -14)
    lv(g, ["glock"], -14)
    lv(g, ["pz_cb"], -13)
    lv(g, ["marimba"], -17)
    lv(g, ["bsn"], -16)
    g.expr(["vla", "vln1", "vc"], [(0, -21), (2, -22)])
    t_lift = pic(c, "whoosh", None, 0)
    if t_lift is not None:                                   # dad lifts the child onto his shoulders: a run up
        sg_, q_l = seg_at(c, segs, t_lift)
        clear_near(c, t_lift)
        sweep(sg_, q_l, 0.4, "F5", "F6", 30, 42, part="xylo")
        sg_.add("pz_hi", q_l, _dq(sg_, q_l, 0.25), top(sg_, q_l, 60, 72), 44, "arp", "h")
        sg_.sync("dad lifts the child (a run up)", q_l, t_lift)
    t_pt = pic(c, "pop", "可是，他想了一个好办法", 0)
    if t_pt is not None:                                     # he points at the parade (the cue's last moment)
        accent(c, segs, t_pt, None, glock=(86, 98), vel=34)
    for sg in segs:
        lv(sg, "hand", -18)
        lv(sg, ["pz_hi"], -13)
        if sg is not g:
            lv(sg, ["xylo", "glock"], -15)


def jericho(c):
    """Jericho (B-flat, 2/4): the street tune on the koto over the marimba's off-beat, plucked basses, a darbuka and soft
    strings; Zacchaeus's tune on the clarinet on '城里住着一个人' (bassoon steps, a clink for the coins on the picture);
    a mock-imperial fanfare on the muted trumpet for the Roman emperor ('收税的人，就是', E-flat), coins clinking for
    '向大家收钱的人'; his smug strut on '撒该管着好多' (muted trumpet), a glockenspiel 'bling' and the coins glittering up
    (a xylophone glissando) as his chest overflows on '他很有钱', a muted-trumpet 'heh-heh' after it; G minor on
    '可是，大家都不喜欢撒该': a sneaky clarinet over tiptoe pizzicato, a pluck as he hops off his stool, a sly grace as he
    snatches an extra coin, a plink as it goes into his pouch; E-flat on '大家看见撒该': everyone steps away, a lonely
    clarinet to F7."""
    c.gain(-3.0)
    t_z = c.gap(c.find("城里住着一个人"))
    t_r = c.gap(c.find("收税的人，就是"))
    t_m = c.gap(c.find("撒该管着好多"))
    t_u = c.gap(c.find("可是，大家都不喜欢撒该"))
    t_a = c.gap(c.find("大家看见撒该"))
    j = c.seg(0, t_z, 8, "2/4", "Bb major", nominal=107, label="jericho-town")
    z = c.seg(t_z, t_r, 5, "2/4", "Bb major", nominal=102, label="jericho-zacchaeus")
    r = c.seg(t_r, t_m, 5, "2/4", "Bb major", nominal=114, label="jericho-rome")
    m = c.seg(t_m, t_u, 4, "2/4", "Bb major", nominal=108, label="jericho-rich")
    u = c.seg(t_u, t_a, 6, "2/4", "Bb major", nominal=94, label="jericho-disliked")
    a = c.seg(t_a, c.dur, 3, "2/4", "Bb major", nominal=96, label="jericho-alone")
    segs = (j, z, r, m, u, a)
    for sg in segs:
        sg.duck(1.5)
    j.prog(" | ".join(JER_PROG))
    z.prog("Bb:2 | " + " | ".join(Z_PROG))
    r.prog("Eb:2 | Bb/D:2 | Cm:1 F7:1 | Bb:2 | F7:2")
    m.prog("Bb:2 | Eb:2 | F7:2 | Bb:2")
    u.prog("Gm:2 | Cm:2 | D7:2@G-harmonic | Gm:2 | Cm:1 D7:1@G-harmonic | Gm:2")
    a.prog("Eb:2 | Cm7:2 | F7sus4:1 F7:1")
    z.sync("'城里住着一个人': Zacchaeus's tune (B-flat)", 0, t_z, kind="change")
    r.sync("'收税的人，就是': the Roman emperor (E-flat)", 0, t_r, kind="change")
    m.sync("'撒该管着好多': the smug strut (B-flat)", 0, t_m, kind="change")
    u.sync("'可是，大家都不喜欢撒该': G minor", 0, t_u, kind="change")
    a.sync("'大家看见撒该': everyone steps away (E-flat)", 0, t_a, kind="change")
    # 'one day Jesus passed through a town called Jericho; tall palms everywhere': the street tune
    j.mel("koto", bars(JER, 0, 8), vel=50)
    oom(j, 0, 16, vel=36)
    darbuka(j, 0, 16, vel=32)
    j.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    sweep(j, 15.0, 0.45, "F4", "Eb5", 28, 36, part="koto")        # a qanun flourish on the last F7, into his steps
    j.duck(7.5, parts=["koto"])
    j.duck(3.5, parts=["marimba"])
    j.expr(["koto"], [(0, -19), (1.5, -15), (16, -15)])
    j.expr(["pz_cb"], [(0, -19), (1.5, -13), (16, -13)])
    j.expr(["marimba"], [(0, -25), (1.5, -20), (16, -20)])
    j.expr("hand", [(0, -26), (1.5, -21), (16, -21)])
    j.expr(["vla", "vln1"], [(0, -26), (2, -24), (16, -24)])
    # 'in the town lived a man called Zacchaeus; he was a tax collector': his steps, then his tune
    z.mel("clar", "r:2 | " + bars(Z, 0, 3) + " | Bb4:2", vel=50)
    steps(z, 0, 10, vel=38)
    oom(z, 0, 10, vel=32, cpart="marimba")
    lv(z, ["marimba"], -22)
    z.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    z.duck(4.5, parts=["clar"])
    z.duck(2.5, parts=["marimba", "bsn"])
    lv(z, ["clar"], -16)
    z.expr(["bsn"], [(0, -22), (1, -16), (10, -16)])
    z.expr(["pz_cb"], [(0, -19), (1, -14), (10, -14)])
    z.expr(["vla", "vln1"], [(0, -25), (10, -25)])
    i_tax = c.find("城里住着一个人")
    coins = pick_times(pics(c, "coins"), c.ls(i_tax) - 0.3, c.le(i_tax) + 0.4, 1)
    for t_ in coins:                                         # he counts his coins: a clink
        clear_near(c, t_)
        accent(c, segs, t_, "he counts his coins (a clink)", glock=(86, 98), vel=40)
    # 'tax collectors collected money for the Roman emperor': a mock-imperial muted trumpet, a snare, a timpani
    r.mel("mtpt", "Bb4:3/4 Bb4:1/4 Eb5:1/2 G5:1/2 | F5:3/4 D5:1/4 Bb4:1 | C5:1/2 Eb5:1/2 F5:1/2 A4:1/2 | "
                  "Bb4:1/2:s r:3/2 | r:1 F4:1/4 G4:1/4 A4:1/4 C5:1/4", vel=50)
    r.add("timp", 0, 1, "Eb3", 34, "timp", "h")
    for q_ in (0.0, 0.75, 2.0, 2.75, 4.0):
        drum(r, q_, 38, 26 if q_ == 0.0 else 30, part="okit")
    oom(r, 0, 10, vel=34, cpart="marimba")
    r.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    i_rm = c.find("收税的人，就是")
    hit(c, segs, "pop", "收税的人，就是", 0, "the emperor's coin (a timpani and a glint)", glock=(86, 98), low=True,
        vel=40)
    cs_ = pick_times(pics(c, "coins"), c.ls(i_rm) - 0.3, c.le(i_rm) + 0.5)
    rc = next(([a_, b_, d_] for a_, b_, d_ in zip(cs_, cs_[1:], cs_[2:]) if d_ - a_ < 0.7), [])
    if rc:
        for k_, t_ in enumerate(rc):
            clear_near(c, t_)
            accent(c, segs, t_, "three coins on the heap" if k_ == 0 else None, glock=(86, 98), koto=(70, 82), vel=38)
    else:
        for q_ in (6.5, 7.5, 8.5):
            if not bool(r.score.speaking(r.t(q_))):
                r.add("glock", q_, 0.5, top(r, q_, 86, 98), 34, "arp", "h")
    r.duck(2.5, parts=["mtpt"])
    lv(r, ["mtpt"], -17)
    lv(r, ["timp"], -16)
    lv(r, "okit", -21)
    lv(r, ["pz_cb"], -14)
    lv(r, ["marimba"], -21)
    r.expr(["vla", "vln1"], [(0, -25), (10, -25)])
    # 'Zacchaeus was the boss of many tax collectors; he was rich!': the smug strut, the coins glitter up
    m.mel("mtpt", "F4:1/2:s Bb4:1/2:s D5:1/2:s F5:1/2:s | G5:1 Eb5:1/2 G5:1/2 | F5:1/2 Eb5:1/2 C5:1/2 A4:1/2", vel=48)
    steps(m, 0, 8, vel=36)
    oom(m, 0, 8, vel=32, cpart="marimba")
    m.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    i_m = c.find("撒该管着好多")
    t_ov = pic(c, "sparkle", "撒该管着好多", 0)
    if t_ov is not None and not (m.t0 - c.t0 + 0.1 <= t_ov <= m.t1 - c.t0 - 0.4):
        clear_near(c, t_ov)
        accent(c, segs, t_ov, "the chest overflows (a glint)", glock=(86, 98), vel=42)
        t_ov = None
    t_rich = t_ov if t_ov is not None else c.le(i_m) + 0.05
    sg_, q_rich = seg_at(c, segs, t_rich)
    if sg_ is m:                                             # the chest overflows: a bling, the coins glitter up
        clear_near(c, t_rich, win=0.2)
        m.add("glock", q_rich, _dq(m, q_rich, 1.0), top(m, q_rich, 86, 98), 44, "arp", "h")
        m.add("xylo", q_rich, _dq(m, q_rich, 0.25), top(m, q_rich, 77, 86), 44, "arp", "h")
        sweep(m, q_rich + 0.1, 0.35, "F5", "F7", 30, 42, part="xylo")
        m.sync("'他很有钱！': the chest overflows (a bling, the coins glitter)" + (" (picture)" if t_ov is not None else ""),
               q_rich, t_rich)
    t_hh = c.le(i_m) + 0.08
    sg_, q_hh = seg_at(c, segs, t_hh)
    if sg_ is m:
        for k_, nm in enumerate(("D5", "Bb4")):              # heh-heh
            qq = min(q_hh + 0.25 * k_, m.n_q - 0.15)
            m.add("mtpt", qq, 0.2, nm, 44 - 2 * k_, "arp", "S")
    m.duck(2.5, parts=["mtpt"])
    m.expr(["mtpt"], [(0, -21), (1, -17), (8, -17)])
    lv(m, ["bsn"], -17)
    lv(m, ["xylo"], -16)
    lv(m, ["glock"], -14)
    lv(m, ["pz_cb"], -14)
    lv(m, ["marimba"], -21)
    m.expr(["vla", "vln1"], [(0, -25), (8, -25)])
    # 'but nobody liked him: he took too much money and put it in his own pocket': G minor, sneaky
    u.mel("clar", "G4:1/2 A4:1/2 Bb4:1/2 G4:1/2 | C5:1/2 Bb4:1/2 A4:1/2 G4:1/2 | F#4:1/2 A4:1/2 C5:1/2 A4:1/2 | "
                  "G4:1 D4:1 | Eb4:1/2 G4:1/2 F#4:1/2 A4:1/2", vel=46, art="s")
    u.mel("clar", "r:10 | G4:2", vel=42)
    for q_ in np.arange(0, 12, 0.5):                         # tiptoe pizzicato
        ch = u.chord_at(q_ + 1e-3)
        if abs(q_ % 1.0) < 1e-6:
            u.add("pz_lo", q_, 0.5, ch.bass_note(43, 55), 38, "arp", "s")
        elif not bool(u.score.speaking(u.t(q_))):
            u.add("pz_hi", q_, 0.25, ch.tones(62, 74)[int(q_ * 2) % 2], 30, "arp", "S")
    u.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(43, 55))
    i_pk = c.find("可是，大家都不喜欢撒该")
    hit(c, segs, "pop", "可是，大家都不喜欢撒该", 0, "he hops off his stool (a pluck)", pluck=(55, 67), xylo=(74, 86),
        vel=40)
    pk = pick_times(pics(c, "coins"), c.ls(i_pk) - 0.3, c.le(i_pk) + 0.4)
    if len(pk) >= 3:                                         # he snatches an extra coin: a sly grace
        clear_near(c, pk[1])
        sg_, q_sn = accent(c, segs, pk[1], "he snatches an extra coin (a sly grace)", xylo=(79, 91), pluck=(62, 74),
                           block=76, vel=46)
        if q_sn > 0.15:
            sg_.add("xylo", q_sn - 0.12, 0.1, top(sg_, q_sn, 79, 91) - 2, 32, "fx", "S")
    t_pk = pk[-1] if pk else None
    if t_pk is not None:                                     # into his pouch: a plink
        clear_near(c, t_pk)
        accent(c, segs, t_pk, "into his pouch (a plink)", xylo=(79, 91), pluck=(55, 67), vel=40)
    u.duck(2.5, parts=["clar"])
    u.expr(["clar"], [(0, -21), (1, -16), (12, -16)])
    u.expr(["pz_lo"], [(0, -19), (1, -14), (12, -14)])
    lv(u, ["pz_hi"], -15)
    u.expr(["vla", "vln1"], [(0, -24), (12, -24)])
    # 'when people saw Zacchaeus they stayed far away': E-flat, a lonely clarinet, F7
    a.mel("clar", "G4:1 Eb4:1 | G4:1/2 F4:1/2 Eb4:1 | F4:2", vel=44)
    for q_ in (0.0, 1.0, 2.0, 3.0):
        a.add("pz_lo", q_, 0.5, a.chord_at(q_ + 1e-3).bass_note(43, 55), 34 - 2 * int(q_), "arp", "s")
    a.add("pz_lo", 4.0, 1.0, "F2", 34, "arp", "s")
    a.add("pz_lo", 5.0, 1.0, "C3", 32, "arp", "s")
    a.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_part="vc", bass_lo=41, bass_hi=53)
    a.expr(["clar"], [(0, -20), (1, -16), (6, -16)])
    lv(a, ["pz_lo"], -15)
    a.expr(["vla", "vln1", "vc"], [(0, -27), (1.5, -23), (6, -22)])
    for sg in segs:
        lv(sg, ["glock"], -14)
        lv(sg, ["pz_hi"], -14)


def crowd(c):
    """'Jesus is coming!' (B-flat, 2/4): the street tune on the koto and the clarinet, claps and the darbuka, a
    scamper up to F7; Zacchaeus's head questioning on '撒该也想看看'; G minor on '撒该心想': a ticking clock; E-flat on
    '可是，撒该的个子太矮了' (a bassoon plunk); G minor on '他跳呀跳': a xylophone glissando up on each 跳 that falls
    back, a bassoon 'nope'; C minor on '他踮起脚': a clarinet slide up, a wobbling trill on tiptoe, the fall on
    '还是看不见'; G minor on '前面的人': a wall of low brass, a woodblock bonk on the back of a head; G minor on
    '他想挤进去': pushing pizzicato and the thud of the elbow; G minor on '撒该急得团团转': a circling figure; E-flat add9
    on '小朋友，你猜' with three xylophone notes climbing as his three thinking dots rise (a pluck for the thought bubble
    and its '?' earlier on); F7sus4 at the end of the question, hanging through the guess without dead air: the koto
    rolls it, the marimba ticks while he thinks, and his tune's creep (E-flat, E, F) rises on the clarinet as the idea
    comes -- s05 pops it."""
    c.gain(-3.0)
    t_w = c.gap(c.find("撒该也想看看"))
    t_x = c.gap(c.find("撒该心想"))
    t_s = c.gap(c.find("可是，撒该的个子太矮了"))
    t_j = c.at("他跳呀跳")
    t_t = c.at("他踮起脚")
    t_wall = c.gap(c.find("前面的人"))
    t_sq = c.gap(c.find("他想挤进去"))
    t_sp = c.at("撒该急得团团转")
    t_q = c.gap(c.find("小朋友，你猜"))
    t_qe = c.le(c.find("小朋友，你猜"))
    n = c.seg(0, t_w, 6, "2/4", "Bb major", nominal=123, label="crowd-news")
    w = c.seg(t_w, t_x, 4, "2/4", "Bb major", nominal=118, label="crowd-wants")
    x = c.seg(t_x, t_s, 6, "2/4", "Bb major", nominal=103, label="crowd-chance")
    s = c.seg(t_s, t_j, 2, "2/4", "Bb major", nominal=90, label="crowd-short")
    jm = c.seg(t_j, t_t, 2, "2/4", "Bb major", nominal=100, label="crowd-jump")
    tp = c.seg(t_t, t_wall, 2, "2/4", "Bb major", nominal=100, label="crowd-tiptoe")
    wl = c.seg(t_wall, t_sq, 4, "2/4", "Bb major", nominal=82, label="crowd-wall")
    sq = c.seg(t_sq, t_sp, 3, "2/4", "Bb major", nominal=108, label="crowd-squeeze")
    sp = c.seg(t_sp, t_q, 2, "2/4", "Bb major", nominal=120, label="crowd-spin")
    q = c.seg(t_q, t_qe, 2, "2/4", "Bb major", nominal=None, label="crowd-question")      # the question
    gs = c.seg(t_qe, c.dur, 1, "2/4", "Bb major", nominal=None, label="crowd-guess")       # the guess hangs
    segs = (n, w, x, s, jm, tp, wl, sq, sp, q, gs)
    for sg in segs:
        sg.duck(1.5)
    n.prog("Bb:2 | Bb:2 | Cm7:2 | F7:2 | Bb:2 | F7:2")
    w.prog("Bb:2 | Bb:2 | Eb:2 | F7sus4:2")
    x.prog("Gm:2 | Gm:2 | Eb:2 | Cm:2 | D7sus4:1@G-harmonic D7:1@G-harmonic | D7:2@G-harmonic")
    s.prog("Eb:2 | Cm:1 D7:1@G-harmonic")
    jm.prog("Gm:1 Eb:1 | Cm:1 D7:1@G-harmonic")
    tp.prog("Cm:2 | D7:2@G-harmonic")
    wl.prog("Gm:2 | Eb:2 | Cm:2 | D:2@G-harmonic")
    sq.prog("Gm:2 | Cm:2 | D7:2@G-harmonic")
    sp.prog("Gm:1 D7:1@G-harmonic | Gm:1 D7:1@G-harmonic")
    q.prog("Ebadd9:2 | Ebadd9:2")
    gs.prog("F7sus4:2")
    w.sync("'撒该也想看看': he wants to see too (B-flat)", 0, t_w, kind="change")
    x.sync("'撒该心想': no other chance (G minor)", 0, t_x, kind="change")
    s.sync("'可是，撒该的个子太矮了': too short (E-flat)", 0, t_s, kind="change")
    jm.sync("'他跳呀跳': the jumps (G minor)", 0, t_j, kind="change")
    tp.sync("'他踮起脚': on tiptoe (C minor)", 0, t_t, kind="change")
    wl.sync("'前面的人': the wall (G minor)", 0, t_wall, kind="change")
    sq.sync("'他想挤进去': squeezing (G minor)", 0, t_sq, kind="change")
    sp.sync("'撒该急得团团转': round and round (G minor)", 0, t_sp, kind="change")
    q.sync("'小朋友，你猜': the question (E-flat add9)", 0, t_q, kind="change")
    gs.sync("the guess: F7sus4 hangs", 0, t_qe, kind="change")
    # 'Jesus is coming! everyone ran into the street': the street tune, claps, a scamper
    n.mel("koto", bars(JER, 0, 4), vel=48)
    n.mel("clar", bars(JER, 0, 4), vel=40, transpose=-12, role="fx")
    run(n, "xylo", 8.0, ["Bb5", "C6", "D6", "Eb6", "F6", "G6", "A6", "Bb6"], 0.25, vel=34, role="melody", art="s")
    run(n, "xylo", 10.0, ["A6", "F6", "Eb6", "C6"], 0.5, vel=36, role="melody", art="s")
    oom(n, 0, 12, vel=36, lively=True)
    darbuka(n, 0, 12, vel=32)
    claps(n, 0, 12, vel=30, offs=(0.5, 1.5))
    n.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    n.duck(4.5, parts=["koto", "clar", "xylo"])
    n.expr(["koto"], [(0, -17), (1, -14), (12, -14)])
    lv(n, ["clar"], -20)
    lv(n, ["xylo"], -17)
    lv(n, ["pz_cb"], -13)
    lv(n, ["marimba"], -20)
    lv(n, "hand", -17)
    n.expr(["vla", "vln1"], [(0, -25), (12, -24)])
    # 'Zacchaeus wanted to see what Jesus was like too': his head, questioning
    w.mel("clar", bars(Z, 0, 2) + " | Eb5:1/2 G5:1/2 Bb5:1/2 G5:1/2 | F5:2", vel=48)
    steps(w, 0, 8, vel=34)
    oom(w, 0, 8, vel=30, cpart="marimba")
    w.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    w.duck(4.5, parts=["clar"])
    w.expr(["clar"], [(0, -21), (1, -16), (8, -16)])
    w.expr(["bsn"], [(0, -22), (1, -17), (8, -17)])
    lv(w, ["pz_cb"], -14)
    lv(w, ["marimba"], -21)
    w.expr(["vla", "vln1"], [(0, -25), (8, -24)])
    # 'Jesus is only passing through; if I don't see him today there won't be another chance!': a ticking clock
    x.mel("clar", "G4:1/2 A4:1/2 Bb4:1/2 G4:1/2 | D5:1 Bb4:1 | Eb5:1/2 D5:1/2 C5:1/2 Bb4:1/2 | C5:1/2 Eb5:1/2 G5:1 | "
                  "A5:1 F#5:1 | D5:1/2 F#5:1/2 A5:1/2 C6:1/2", vel=44)
    tick(x, 0, 12, vel=28)
    for q_ in range(12):
        x.add("pz_lo", q_, 0.5, x.chord_at(q_ + 1e-3).bass_note(43, 55), 36, "arp", "s")
    x.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 69, vel=28, q0=8, bass_ref=(43, 55))
    x.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, q1=8, bass_ref=(43, 55))
    hit(c, segs, "pop", "撒该心想", 0, "a thought bubble opens (a xylophone pluck)", xylo=(74, 86), vel=38)
    hit(c, segs, "pop", "撒该心想", 1, "a big '?' in the bubble (a plucked question)", xylo=(79, 91), pluck=(62, 74),
        vel=40)
    x.duck(4.5, parts=["clar"])
    lv(x, ["clar"], -17)
    lv(x, "hand", -20)
    lv(x, ["pz_lo"], -14)
    x.expr(["vla", "vln1"], [(0, -25), (8, -24)])
    x.expr(["trem_va", "trem_hi"], [(8, -25), (12, -22)])
    # 'but Zacchaeus was too short!': E-flat, a bassoon plunk down
    s.mel("bsn", "Bb3:1/2:s G3:1/2:s Eb3:1 | Eb3:1 F#3:1", vel=46)
    s.add("xylo", 0.5, 0.25, "Bb6", 32, "arp", "S")
    s.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=39, bass_hi=51)
    s.expr(["bsn"], [(0, -21), (1, -15), (4, -15)])
    lv(s, ["xylo"], -17)
    s.expr(["vla", "vln1", "vc"], [(0, -27), (1, -24), (4, -23)])
    # 'he jumped and jumped -- couldn't see': a glissando up on each 跳 that falls back; a bassoon 'nope'
    jumps = pick_times(pics(c, "whoosh"), t_j - 0.15, t_t - 0.2, 2)
    lands = [t_ for t_ in (pick_times(pics(c, "thud"), t_j - 0.1, t_t + 0.2) or [])]
    pic_j = len(jumps) == 2
    if not pic_j:
        jumps = chars(c, "他跳呀跳", "跳")[:2]
    for t_ in jumps:
        clear_near(c, t_, win=0.12)
    for k_, t_ in enumerate(jumps):
        land = next((x for x in lands if t_ + 0.12 < x < t_ + 0.7), None) if pic_j else None
        jump(c, segs, t_, land, vel=42, what=f"跳 {k_ + 1}: a jump (xylophone up)" + (" (picture)" if pic_j else ""))
    t_no = voice_at(c, "看不见")
    sg_, q_no = seg_at(c, segs, t_no)
    if sg_ is jm and q_no < jm.n_q - 0.6:
        jm.add("bsn", q_no, 0.5, top(jm, q_no, 43, 50), 44, "melody", "s")
        jm.add("bsn", q_no + 0.5, 0.5, jm.chord_at(q_no + 0.51).bass_note(36, 48), 42, "melody", "s")
    jm.add("pz_lo", 0, 0.5, "G2", 36, "arp", "s")
    jm.add("bsn", 0, 0.9, "G2", 38, "melody")
    jm.add("bsn", 0, 0.9, "D3", 34, "harmony")
    jm.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=39, bass_hi=51)
    lv(jm, ["bsn"], -15)
    lv(jm, ["xylo"], -15)
    lv(jm, ["pz_hi"], -13)
    lv(jm, ["pz_lo"], -14)
    jm.add("marimba", 0, 1.0, "Bb3", 34, "arp")
    jm.expr(["vla", "vln1", "vc"], [(0, -20), (1, -24), (4, -24)])
    lv(jm, ["marimba"], -18)
    # 'he stood on tiptoe -- still couldn't see!': a clarinet slide up, a wobbling trill, the fall
    t_tip = pic(c, "cloth", "他跳呀跳", 0, lo=t_t - 0.1, hi=t_t + 0.8)
    q_s = qpos(tp, c, t_tip, 0.0, 1.0) if t_tip is not None else 0.0
    sweep(tp, q_s, 0.4, "G4", "G5", 28, 40, part="clar")
    trem(tp, "clar", q_s + 0.75, 2.0, "G5", 36, rate=0.125, role="fx", alt="F5")
    tp.add("clar", 2.0, 0.75, "A5", 36, "fx")
    t_still = voice_at(c, "还是看不见")
    q_f = qpos(tp, c, t_still, 2.75, 3.5)
    scale_run(tp, q_f, 0.35, "D4", "A5", 36, 28, up=False, part="clar")
    tp.add("bsn", q_f + 0.25, 0.5, "D3", 42, "melody", "s")
    tp.add("pz_lo", q_f + 0.25, 0.5, "D3", 38, "arp", "s")
    drum(tp, q_f + 0.25, 77, 30)
    tp.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 69, vel=26, bass_ref=(43, 55))
    bassline(tp, "vc", 38, 50, 28)
    tp.sync("'他踮起脚': the slide up" + (" (picture)" if t_tip is not None else ""), q_s, tp.t(q_s) - c.t0) \
        if t_tip is not None else None
    lv(tp, ["clar"], -18)
    lv(tp, ["bsn"], -15)
    lv(tp, ["pz_lo"], -14)
    lv(tp, "hand", -19)
    tp.expr(["trem_va", "trem_hi"], [(0, -26), (4, -24)])
    lv(tp, ["vc"], -23)
    # 'the people in front were like a tall wall; he saw only the backs of their heads': a wall of low brass
    for q_ in range(8):
        ch = wl.chord_at(q_ + 1e-3)
        wl.add("tuba", q_, 0.5, ch.bass_note(31, 43), 40, "arp", "s")
    wl.pad(["tbn", "tbn", "horn"], 3, 46, 62, vel=34, bass_ref=(31, 43))
    wl.mel("bsn", "r:1 G3:1/4 A3:1/4 Bb3:1/2 | r:1 G3:1/4 Bb3:1/4 Eb4:1/2 | r:1 C4:1/4 D4:1/4 Eb4:1/2 | r:1 "
                  "F#3:1/2 A3:1/2", vel=40, art="s")
    i_bk = c.find("前面的人")
    bonk = pick_times(pics(c, "thud"), c.ls(i_bk) - 0.3, c.le(i_bk) + 0.3, 1) or \
        pick_times(pics(c, "pop"), c.ls(i_bk) - 0.3, c.le(i_bk) + 0.3, 1)
    if bonk:
        clear_near(c, bonk[0])
        sg_, q_b = accent(c, segs, bonk[0], "the back of a head (a woodblock bonk)", xylo=(70, 79), vel=40)
        drum(sg_, q_b, 77, 36)
    else:
        t_bk = voice_at(c, "撒该只看见别人的后脑勺") + 0.1
        sg_, q_b = seg_at(c, segs, t_bk)
        drum(sg_, q_b, 77, 30)
    wl.duck(2.0, parts=["tbn", "horn", "tuba"])
    wl.expr(["tbn", "horn"], [(0, -25), (8, -24)])
    lv(wl, ["tuba"], -19)
    lv(wl, ["bsn"], -16)
    # 'he tried to squeeze in, but nobody let him': pushing pizzicato, the thud of the elbow
    for q_ in np.arange(0, 6, 0.5):
        ch = sq.chord_at(q_ + 1e-3)
        sq.add("pz_lo", q_, 0.25, ch.bass_note(43, 55), 34 + int(q_ * 2), "arp", "S")
        if abs(q_ % 1.0) > 1e-6 and not bool(sq.score.speaking(sq.t(q_))):
            sq.add("pz_hi", q_, 0.25, ch.tones(60, 72)[0], 30, "arp", "S")
    sq.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_ref=(43, 55))
    i_sq = c.find("他想挤进去")
    elbow = pick_times(pics(c, "thud"), c.ls(i_sq) - 0.3, t_sp - 0.15, 1)
    pic_e = bool(elbow)
    t_el = elbow[0] if elbow else voice_at(c, "大家都不让他")
    clear_near(c, t_el, win=0.2)
    sg_, q_e = accent(c, segs, t_el, None, low=True, pluck=(55, 62), vel=44)
    drum(sg_, q_e, 58, 26)
    sg_.sync("the elbow bump (a thud)" + (" (picture)" if pic_e else ""), q_e, t_el)
    lv(sq, ["pz_lo"], -14)
    lv(sq, ["pz_hi"], -15)
    sq.expr(["vla", "vln1"], [(0, -25), (6, -24)])
    # 'Zacchaeus went round and round': a circling figure (clarinet, xylophone)
    circ = "Bb4:1/4 C5:1/4 D5:1/4 C5:1/4 A4:1/4 Bb4:1/4 C5:1/4 Bb4:1/4"
    sp.mel("clar", circ + " | " + circ, vel=42)
    sp.mel("xylo", circ + " | " + circ, vel=34, transpose=24, role="fx")
    for q_ in np.arange(0, 4, 0.5):
        sp.add("pz_lo", q_, 0.5, sp.chord_at(q_ + 1e-3).bass_note(43, 55), 34, "arp", "s")
    sp.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_ref=(43, 55))
    sp.duck(2.5, parts=["clar", "xylo"])
    lv(sp, ["clar"], -17)
    lv(sp, ["xylo"], -19)
    lv(sp, ["pz_lo"], -14)
    sp.expr(["vla", "vln1"], [(0, -25), (4, -24)])
    # 'child, can you guess what good idea Zacchaeus thought of?': E-flat add9 under the question, the three thinking
    # dots climbing on the xylophone; then the guess: F7sus4 hangs in the pause -- the koto rolls it, the marimba ticks
    # while he thinks, and his tune's creep (E-flat, E, F) rises on the clarinet as the idea comes (s05 pops it)
    q.pad(["vla", "vla", "vln1"], 3, 53, 74, vel=30, bass_part="vc", bass_lo=39, bass_hi=53)
    roll_chord(q, 0.05, 55, 79, vel=34, part="koto", n=5)
    dots = pick_times(pics(c, "pop"), t_q, c.dur - 0.05, 3)
    if len(dots) == 3:                                       # three thinking dots rise: three notes climbing
        for t_ in dots:
            clear_near(c, t_, win=0.25)
        climb(c, segs, dots, part="xylo", lo=76, hi=91, vel=54, sync=(0, 2), what="a thinking dot rises", glock=False,
              pz=True)
    else:
        for k_, nm in enumerate(("Bb5", "D6", "F6")):
            q.add("xylo", 2.0 + 0.5 * k_, 0.5, nm, 34 + 2 * k_, "arp")
    lv(q, ["koto"], -17)
    lv(q, ["xylo"], -14)
    q.expr(["vla", "vln1", "vc"], [(0, -22), (4, -21)])
    gs.pad(["vla", "vla", "vln1"], 3, 53, 74, vel=30, bass_part="vc", bass_lo=39, bass_hi=53)
    roll_chord(gs, 0.04, 53, 77, vel=34, part="koto", n=5)
    for q_, nm in ((0.5, "C5"), (0.9, "Bb4"), (1.3, "C5")):  # thinking: tick, tock, tick
        gs.add("marimba", q_, 0.3, nm, 34, "arp", "s")
    gs.mel("clar", "r:3/2 Eb5:1/6 E5:1/6 F5:1/6", vel=40)
    lv(gs, ["koto"], -17)
    lv(gs, ["marimba"], -17)
    gs.expr(["clar"], [(0, -21), (2, -18)])
    gs.expr(["vla", "vln1", "vc"], [(0, -21), (2, -20)])
    for sg in segs:
        lv(sg, ["glock"], -14)
        lv(sg, ["pz_hi"], -14)
        if sg not in (n, x, tp):
            lv(sg, "hand", -18)


def tree(c):
    """'有了！' -- the idea sting on the picture's light bulb (B-flat: xylophone, glockenspiel, pizzicato, a triangle)
    after the held F7sus4; the scamper (his tune fast on the xylophone over a running bassoon, woodblock feet, the
    darbuka) that screeches to a halt at the tree (a xylophone glissando down, a plucked stop); the big tree on the horn
    in E-flat ('那里有一棵大大的桑树', low strings for the thick branches, a glint as the low limbs glow, a run up as his
    hands reach the fork); '撒该爬呀爬' -- one step up for each climbing stage (xylophone, koto, pizzicato: D Eb F A)
    over a rising bass B-flat C D F; the hoist onto the sitting branch lands on B-flat (a xylophone run, glockenspiel,
    flute, plucked chords, a cymbal breath); he settles (a soft pluck); his tune an octave higher on flute and
    xylophone on '嘿嘿' (a muted-trumpet giggle on the two giggle bobs)."""
    c.gain(-3.0)
    t_idea = c.ls(0)
    t_run = c.at("撒该往前跑")
    t_tree = c.gap(c.find("那里有一棵大大的桑树"))
    i_cl = c.find("撒该爬呀爬")
    t_climb = c.gap(i_cl)
    t_hee = c.gap(c.find("嘿嘿"))
    # the climbing stages and the hoist: the picture's cloth cues (the k-th from the climbing line), else the voice's 爬
    cl_pic = pick_times(pics(c, "cloth"), c.ls(i_cl) - 0.3, t_hee - 0.3)
    pic_c = len(cl_pic) >= 5
    if pic_c:
        pa, t_top = cl_pic[:4], cl_pic[4]
    else:
        pa_v = chars(c, "撒该爬呀爬", "爬")
        pa, t_top = pa_v[:4], (pa_v[4] if len(pa_v) >= 5 else syl(c, "爬上了桑树", 1)[0])
    t_top = min(max(t_top, t_climb + 1.2), t_hee - 0.5)
    pa = [t_ for t_ in pa if t_climb + 0.05 < t_ < t_top - 0.15]
    h = c.seg(0, t_idea, 1, "2/4", "Bb major", nominal=None, label="tree-guess")
    i = c.seg(t_idea, t_run, 1, "2/4", "Bb major", nominal=None, label="tree-idea")
    r = c.seg(t_run, t_tree, 5, "2/4", "Bb major", nominal=144, label="tree-run")
    b = c.seg(t_tree, t_climb, 2, "4/4", "Eb major", nominal=75, label="tree-tree")
    cl = c.seg(t_climb, t_top, 2, "2/4", "Bb major", nominal=76, label="tree-climb")
    tp = c.seg(t_top, t_hee, 1, "2/4", "Bb major", nominal=None, label="tree-top")
    e = c.seg(t_hee, c.dur, 4, "2/4", "Bb major", nominal=127, label="tree-hehe")
    segs = (h, i, r, b, cl, tp, e)
    for sg in segs:
        sg.duck(1.5)
    h.prog("F7sus4:2")
    i.prog("Bb:2")
    r.prog("Bb:2 | Bb:2 | F7:2 | Bb:2 | F7:2")
    b.prog("Eb:2 Ab:2 | Cm7:2 F7sus4:1 F7:1")
    if len(pa) >= 2:
        prog48(cl, ["Bb", "Cm7", "Bb/D", "F7"][:len(pa)], edges48(cl, c, pa[1:]))
    else:
        cl.prog("Bb:2 | Bb/D:2 | F7:2")
    tp.prog("Bb:1 F7:1")
    e.prog(" | ".join(Z_PROG))
    i.sync("'有了！': the idea (B-flat)", 0, t_idea, kind="change")
    b.sync("'那里有一棵大大的桑树': the tree (E-flat)", 0, t_tree, kind="change")
    cl.sync("'撒该爬呀爬': the climb (B-flat)", 0, t_climb, kind="change")
    tp.sync("the hoist onto the branch (B-flat)" + (" (picture)" if pic_c else ""), 0, t_top, kind="change")
    e.sync("'嘿嘿': his tune in the tree (B-flat)", 0, t_hee, kind="change")
    # the question still hangs (F7sus4)
    h.pad(["vla", "vla", "vln1"], 3, 53, 74, vel=30, bass_part="vc", bass_lo=39, bass_hi=53)
    roll_chord(h, 0.0, 53, 77, vel=28, part="koto", n=5)
    h.add("clar", 0.0, 2.0, "F5", 36, "melody")
    h.add("xylo", 1.0, 1.0, "C6", 30, "arp")
    lv(h, ["clar"], -19)
    lv(h, ["koto"], -17)
    lv(h, ["xylo"], -18)
    h.expr(["vla", "vln1", "vc"], [(0, -21), (2, -21)])
    # '有了！': the idea sting -- on the picture's light bulb when it comes with the word
    t_bulb = None
    for nm in ("pop", "sparkle", "chime"):
        tb = pic(c, nm, None, 0, lo=t_idea - 0.12, hi=t_idea + 0.35)
        if tb is not None:
            t_bulb = (nm, tb)
            break
    q_i = qpos(i, c, t_bulb[1], 0.0, 0.6) if t_bulb else 0.0
    for nm in ("Bb5", "D6", "F6"):
        i.add("xylo", q_i, _dq(i, q_i, 1.0), nm, 48, "arp", "h")
    i.add("glock", q_i, _dq(i, q_i, 2.0), "Bb6", 44, "arp", "h")
    for nm in ("Bb3", "F4", "D5"):
        i.add("pz_hi", q_i, _dq(i, q_i, 0.5), nm, 48, "arp", "h")
    i.add("pz_cb", q_i, _dq(i, q_i, 0.5), "Bb1", 46, "bass", "h")
    drum(i, q_i, 81, 34)
    drum(i, q_i, 76, 34)
    i.sync("'有了！': the idea sting" + (f" (picture {t_bulb[0]})" if t_bulb else ""), q_i, i.t(q_i) - c.t0)
    i.pad(["vla", "vla", "vln1"], 3, 53, 74, vel=32, bass_part="vc", bass_lo=39, bass_hi=53)
    lv(i, ["xylo"], -13)
    lv(i, ["glock"], -13)
    lv(i, ["pz_hi", "pz_cb"], -12)
    i.expr(["vla", "vln1", "vc"], [(0, -20), (2, -22)])
    # 'he ran ahead to the road Jesus would pass': the scamper ... and the halt at the tree
    r.mel("bsn", "Bb2:1/2 C3:1/2 D3:1/2 Eb3:1/2 | F3:1/2 Eb3:1/2 D3:1/2 C3:1/2 | F3:1/2 Eb3:1/2 C3:1/2 A2:1/2 | "
                 "Bb2:1/2 C3:1/2 D3:1/2 F3:1/2", vel=44, art="s")
    r.mel("xylo", bars(Z, 0, 3) + " | Bb5:1/2:s D6:1/2:s F6:1/2:s D6:1/2:s", vel=38, role="fx")
    tick(r, 0, 8, vel=26, step=0.5)
    darbuka(r, 0, 8, vel=30)
    for q_ in range(8):
        r.add("pz_cb", q_, 0.4, r.chord_at(q_ + 1e-3).bass_note(33, 45), 38, "arp", "s")
    r.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=26, bass_ref=(33, 45))
    i_run = c.find("有了")
    t_wh = pic(c, "whoosh", "有了", 0, lo=r.t(7.0) - c.t0, hi=r.t(9.6) - c.t0)
    t_halt = pic(c, "thud", "有了", 0)
    pic_h = t_halt is not None and r.t(7.0) - c.t0 <= t_halt <= r.t(9.8) - c.t0
    if t_halt is not None and not pic_h:
        clear_near(c, t_halt)
        accent(c, segs, t_halt, "he screeches to a halt (a pluck)", pluck=(55, 67), block=77, vel=44)
    if not pic_h:
        t_halt = r.t(8.25) - c.t0
    if t_wh is None or t_wh > t_halt - 0.05:
        t_wh = t_halt - 0.12
    q_wh = qpos(r, c, t_wh, 8.0, 9.5)
    sweep(r, q_wh, 0.12, "C6", "F6", 36, 30, up=False, part="xylo")
    clear_near(c, t_halt)
    sg_, q_h = seg_at(c, segs, t_halt)
    ch_h = sg_.chord_at(q_h + 1e-3)
    for pt in (ch_h.bass_note(41, 53), _alt_bass(ch_h, 41, 53)):
        sg_.add("pz_lo", q_h, _dq(sg_, q_h, 0.5), pt, 46, "arp", "h")
    for pt in ch_h.tones(63, 70)[-2:]:
        sg_.add("pz_hi", q_h, _dq(sg_, q_h, 0.5), pt, 42, "arp", "h")
    drum(sg_, q_h, 77, 36)
    if pic_h:
        sg_.sync("he screeches to a halt at the tree (a plucked stop)", q_h, t_halt)
    lv(r, ["bsn"], -15)
    lv(r, ["xylo"], -18)
    lv(r, "hand", -20)
    lv(r, ["pz_cb"], -14)
    lv(r, ["pz_lo"], -13)
    r.duck(2.5, parts=["xylo"])
    r.duck(2.0)
    r.expr(["vla", "vln1"], [(0, -25), (10, -23)])
    # 'there stood a big sycamore-fig; its branches low and thick, just right for climbing': the tree on the horn
    b.mel("horn", "Eb4:1 G4:1/2 Bb4:1/2 C5:3/2 Bb4:1/2 | Ab4:1 G4:1 F4:2", vel=50)
    strings(b, vel=36, lo=51, hi=70, bass=(40, 52), cb=(28, 40))
    broken(b, "harp", 0, 8, (0, 2, 4, 2), 51, 75, vel=32, thin=True)
    hit(c, segs, "sparkle", "那里有一棵大大的桑树", 0, "the low branches glow (a glint)", glock=(86, 98), vel=40)
    t_fork = pic(c, "cloth", "那里有一棵大大的桑树", 0)
    if t_fork is not None and not (b.t(7.0) - c.t0 <= t_fork <= b.t(7.4) - c.t0):
        clear_near(c, t_fork)
        accent(c, segs, t_fork, "hands on the fork (a pluck)", pluck=(55, 67), xylo=(77, 89), vel=42)
        t_fork = None
    q_fk = qpos(b, c, t_fork, 7.0, 7.4) if t_fork is not None else 7.0
    if t_fork is not None:
        clear_near(c, t_fork)
    run(b, "xylo", q_fk, ["F5", "A5", "C6", "Eb6"], min(0.15, (8.0 - q_fk) / 4), vel=34, role="arp", art="h")
    b.add("pz_hi", q_fk, _dq(b, q_fk, 0.25), "F4", 44, "arp", "h")
    drum(b, q_fk, 76, 34)
    if t_fork is not None:
        b.sync("hands on the fork (a run up)", q_fk, t_fork)
    b.duck(6.5, parts=["horn"])
    b.duck(2.5, parts=STR + ["harp"])
    b.expr(["horn"], [(0, -24), (1.2, -17), (8, -17)])
    b.expr(["harp"], [(0, -23), (1.2, -17), (8, -17)])
    lv(b, ["xylo"], -16)
    b.expr(STR, [(0, -27), (1.5, -21), (8, -21)])
    # 'Zacchaeus climbed and climbed': one step up for each stage over a rising bass, D Eb F A
    prev = 73
    for k_, t_ in enumerate(pa):
        sg_, q_c = seg_at(c, segs, t_)
        ts = sg_.chord_at(q_c + 1e-3).tones(prev + 1, 84)
        prev = ts[0]
        clear_near(c, t_)
        sg_.add("xylo", q_c, _dq(sg_, q_c, 0.5), prev, 42 + 2 * k_, "arp", "h")
        sg_.add("koto", q_c, _dq(sg_, q_c, 0.75), prev - 12, 40 + 2 * k_, "arp", "h")
        sg_.add("pz_lo", q_c, _dq(sg_, q_c, 0.5), sg_.chord_at(q_c + 1e-3).bass_note(41, 53), 40, "arp", "s")
        if k_ in (0, len(pa) - 1):
            sg_.sync(f"climbing stage {k_ + 1}: a step up" + (" (picture)" if pic_c else ""), q_c, t_)
    cl.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_part="vc", bass_lo=41, bass_hi=53)
    cl.duck(2.0)
    lv(cl, ["xylo"], -15)
    lv(cl, ["koto"], -15)
    lv(cl, ["pz_lo"], -13)
    cl.expr(["vla", "vln1", "vc"], [(0, -24), (6, -21)])
    # the hoist onto the sitting branch: B-flat high -- a run up, glockenspiel, flute, plucked chords, a cymbal breath
    sweep(tp, 0.0, 0.25, "Bb5", "Bb6", 34, 44, part="xylo")
    tp.add("glock", 0, 1.0, "D7", 42, "arp", "h")
    tp.add("flute", 0, 1.0, "Bb5", 40, "melody")
    tp.add("flute", 1.0, 1.0, "A5", 34, "melody")
    for nm in ("Bb3", "F4", "D5", "F5"):
        tp.add("pz_hi", 0, 0.5, nm, 46, "arp", "h")
    for nm in ("D6", "F6"):
        tp.add("xylo", 0, 0.5, nm, 44, "arp", "h")
    roll_chord(tp, 0.06, 58, 77, vel=40, part="koto", n=4)
    tp.add("pz_cb", 0, 0.5, "Bb1", 44, "bass", "h")
    tp.add("okit", 0, 1, 57, 24, "perc", "h")
    tp.sync("the hoist onto the sitting branch" + (" (picture)" if pic_c else ""), 0, t_top)
    strings(tp, vel=34, lo=55, hi=74, bass=(40, 52), cb=None)
    t_set = pic(c, "pop", "撒该爬呀爬", 0, lo=t_top + 0.2, hi=t_hee - 0.1)
    if t_set is not None:                                    # he settles on the branch: a soft pluck
        clear_near(c, t_set)
        accent(c, segs, t_set, "he settles on the branch (a pluck)", koto=(65, 77), pluck=(57, 69), vel=40)
    lv(tp, ["xylo"], -14)
    lv(tp, ["glock"], -13)
    lv(tp, ["flute"], -18)
    lv(tp, ["koto"], -16)
    lv(tp, ["pz_hi", "pz_cb"], -12)
    lv(tp, "okit", -20)
    tp.expr(["vla", "vln1", "vc"], [(0, -21), (2, -22)])
    # 'hee hee, now I can see everything!': his tune an octave higher, flute and xylophone; a muted-trumpet giggle
    e.mel("flute", bars(Z, 0, 4), vel=44, transpose=12)
    e.mel("xylo", bars(Z, 0, 4), vel=36, transpose=12, role="fx")
    steps(e, 0, 8, vel=32, lo=50, hi=65)
    oom(e, 0, 8, vel=30, hi=(62, 74), cpart="marimba")
    e.pad(["vla", "vla", "vln1"], 3, 55, 74, vel=26, bass_ref=(33, 45))
    i_he = c.find("嘿嘿")
    t_tw = pic(c, "cloth", "嘿嘿", 0, lo=c.ls(i_he) - 0.3, hi=c.ls(i_he) + 0.5)
    t_he = t_tw if t_tw is not None else c.ls(i_he) + 0.05
    sg_, q_he = seg_at(c, segs, t_he)
    if sg_ is e:
        clear_near(c, t_he)
        for k_, nm in enumerate(("F5", "D5")):
            e.add("mtpt", q_he + 0.25 * k_, 0.2, nm, 42 - 2 * k_, "arp", "S")
        e.add("xylo", q_he, _dq(e, q_he, 0.25), top(e, q_he, 82, 94), 42, "arp", "h")
        e.add("pz_hi", q_he, _dq(e, q_he, 0.25), top(e, q_he, 62, 74), 42, "arp", "h")
        drum(e, q_he, 76, 34)
        if t_tw is not None:
            e.sync("'嘿嘿': the twig pushed aside (a muted-trumpet giggle)", q_he, t_tw)
    e.duck(5.0, parts=["flute", "xylo"])
    e.expr(["flute"], [(0, -22), (1, -18), (8, -18)])
    e.expr(["xylo"], [(0, -23), (1, -19), (8, -19)])
    e.expr(["bsn"], [(0, -22), (1, -18), (8, -18)])
    lv(e, ["mtpt"], -18)
    e.expr(["pz_cb"], [(0, -18), (1, -14), (8, -14)])
    e.expr(["marimba"], [(0, -25), (1, -21), (8, -21)])
    e.expr(["vla", "vln1"], [(0, -25), (8, -24)])
    for sg in segs:
        lv(sg, ["pz_hi"], -13)
        if sg not in (r,):
            lv(sg, "hand", -18)


def call(c):
    """The procession (B-flat, 2/4: soft pizzicato steps, harp, the darbuka's slow taps); a hush on '停住了' (a last
    pluck, a triangle, one high string note); warm E-flat add9 on '他抬起头' (strings swelling, the harp rolled); the
    call on the horn under '撒该，快下来' (his tune made lyrical, B-flat); G7 on '他吓了一跳': the jolt (a xylophone
    'boing', a vibraslap) and the branch wobbling (a koto tremolo); C minor on '耶稣认识我': his head questioning on the
    clarinet, A-flat, F7sus4; B-flat on '他高兴极了': a xylophone chord as his arms go up, a falling scale as he slides
    down the trunk (a plucked plop as he lands), then his tune's pop and zig-zag home, with claps."""
    c.gain(-3.0)
    t_stop = c.at("停住了")
    t_up = c.at("他抬起头")
    t_call = c.gap(c.find("撒该，快下来"))
    t_jolt = c.gap(c.find("他吓了一跳"))
    t_ques = c.gap(c.find("耶稣认识我"))
    t_joy = c.gap(c.find("他高兴极了"))
    w = c.seg(0, t_stop, 2, "2/4", "Bb major", nominal=86, label="call-walk")
    st = c.seg(t_stop, t_up, 1, "2/4", "Bb major", nominal=None, label="call-stop")         # the hush
    u = c.seg(t_up, t_call, 2, "2/4", "Bb major", nominal=78, label="call-look")
    k = c.seg(t_call, t_jolt, 2, "4/4", "Bb major", nominal=104, label="call-call")
    jl = c.seg(t_jolt, t_ques, 2, "2/4", "Bb major", nominal=None, label="call-jolt")              # held
    qu = c.seg(t_ques, t_joy, 4, "2/4", "Bb major", nominal=114, label="call-question")
    j = c.seg(t_joy, c.dur, 6, "2/4", "Bb major", nominal=123, label="call-joy")
    segs = (w, st, u, k, jl, qu, j)
    for sg in segs:
        sg.duck(1.5)
    w.prog("Bb:2 | Eb/Bb:1 Bb:1")
    st.prog("Bb:2")
    u.prog("Ebadd9:2 | Cm7:1 F7sus4:1")
    k.prog("Bb:4 | Gm:2 F7sus4:1 F7:1")
    jl.prog("G7:2@C-harmonic | G7:2@C-harmonic")
    qu.prog("Cm:2 | Cm:2 | Ab:2@C-minor | F7sus4:2")
    j.prog("Bb:2 | Eb:1 F7:1 | " + " | ".join(Z_PROG))
    st.sync("'停住了': he stops (a hush)", 0, t_stop)
    u.sync("'他抬起头': warm E-flat", 0, t_up, kind="change")
    k.sync("'撒该，快下来': the call (B-flat)", 0, t_call, kind="change")
    jl.sync("'他吓了一跳': G7", 0, t_jolt, kind="change")
    qu.sync("'耶稣认识我': C minor", 0, t_ques, kind="change")
    j.sync("'他高兴极了': joy (B-flat)", 0, t_joy, kind="change")
    # 'Jesus came to the sycamore': the procession, soft
    for q_ in range(4):
        w.add("pz_lo", q_, 0.5, w.chord_at(q_ + 1e-3).bass_note(46, 58) if q_ % 2 == 0 else
              _alt_bass(w.chord_at(q_ + 1e-3), 46, 58), 36, "arp", "s")
    broken(w, "harp", 0, 4, (0, 2, 4, 2), 58, 77, vel=30, thin=True)
    darbuka(w, 1, 4, vel=26, sparse=True)
    w.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(46, 58))
    w.expr(["pz_lo"], [(0, -20), (1, -14), (4, -14)])
    w.expr(["harp"], [(0, -23), (1, -17), (4, -17)])
    lv(w, "hand", -19)
    w.expr(["vla", "vln1"], [(0, -25), (4, -24)])
    # '... and stopped': a last pluck, a triangle; one high string note holds
    st.add("pz_lo", 0, 0.5, "Bb2", 28, "arp", "h")
    st.add("harp", 0, 2, "F5", 33, "arp", "r")
    st.add("harp", 0, 2, "Bb5", 29, "arp", "r")
    st.add("harp", 0, 2, "Bb3", 31, "arp", "r")
    st.add("vc", 0, 2, "Bb2", 26, "bass")
    st.add("vln1", 0, 2, "F5", 29, "pad")
    st.add("vla", 0, 2, "D5", 27, "pad")
    st.add("vla", 0, 2, "Bb4", 27, "pad")
    lv(st, ["pz_lo"], -14)
    lv(st, ["harp"], -15)
    st.expr(["vla", "vln1", "vc"], [(0, -22), (2, -22)])
    # 'he looked up at Zacchaeus and said': warm E-flat, the strings swell, the harp rolled
    strings(u, vel=34, lo=53, hi=72, bass=(40, 52), cb=(28, 40))
    roll_chord(u, 0.05, 51, 79, vel=29, part="harp", n=6)
    u.mel("horn", "r:2 | Eb4:1 F4:1", vel=34)
    u.expr(STR, [(0, -23), (2.0, -20), (4, -21)])
    lv(u, ["harp"], -16)
    lv(u, ["horn"], -22)
    # 'Zacchaeus, come down quickly! today I must stay at your house': the call on the horn
    k.mel("horn", "D4:1 Eb4:1/2 E4:1/2 F4:2 | Bb4:3/2 A4:1/2 G4:1 F4:1", vel=48)
    strings(k, vel=34, lo=53, hi=72, bass=(40, 52), cb=(28, 40))
    broken(k, "harp", 0, 8, (0, 2, 4, 2), 51, 75, vel=30, thin=True)
    k.duck(5.0, parts=["horn"])
    k.duck(1.5, parts=STR + ["harp"])
    k.expr(["horn"], [(0, -23), (1.2, -18), (8, -18)])
    lv(k, ["harp"], -17)
    k.expr(STR, [(0, -21), (8, -22)])
    # 'Zacchaeus jumped': G7, the jolt, the branch wobbles
    t_j = voice_at(c, "他吓了一跳")
    t_xia = chars(c, "他吓了一跳", "吓")
    t_x = t_xia[0] if t_xia else t_j + 0.3
    wob = pick_times(pics(c, "whoosh"), t_jolt - 0.2, t_ques - 0.2) or \
        pick_times(pics(c, "cloth"), t_jolt - 0.2, t_ques - 0.2)
    t_jo = wob[0] if wob else t_x
    clear_near(c, t_jo, win=0.2)
    sg_, q_j = seg_at(c, segs, t_jo)
    sg_.add("xylo", q_j, _dq(sg_, q_j, 0.25), top(sg_, q_j, 67, 74), 44, "arp", "h")
    sg_.add("pz_hi", q_j, _dq(sg_, q_j, 0.25), top(sg_, q_j, 55, 67), 46, "arp", "h")
    gliss_in(sg_, "xylo", q_j + 0.02, 0.18, top(sg_, q_j, 67, 74) + 1, 95, up=True, v0=34, v1=44,
             scale=ChordTones(sg_.chord_at(q_j + 1e-3)))
    drum(sg_, q_j, 58, 26)
    sg_.sync("the jolt (a xylophone boing)" + (" (picture)" if wob else ""), q_j, t_jo)
    q_w = min(q_j + 0.5, jl.n_q - 1.0) if sg_ is jl else 1.0
    trem(jl, "koto", q_w, min(q_w + 1.5, jl.n_q - 0.25), "B4", 34, rate=0.125, role="arp", alt="D5")
    jl.pad(["trem_va", "trem_va", "trem_hi"], 3, 53, 71, vel=28, bass_part="vc", bass_lo=43, bass_hi=55)
    roll_chord(jl, 0.0, 55, 74, vel=32, part="harp", n=4)
    lv(jl, ["xylo"], -15)
    lv(jl, ["pz_hi"], -13)
    lv(jl, ["koto"], -18)
    lv(jl, "hand", -20)
    jl.expr(["trem_va", "trem_hi", "vc"], [(0, -22), (4, -23)])
    lv(jl, ["harp"], -16)
    # 'Jesus knows me? he wants to come to my house?': his head questioning in C minor, A-flat, F7sus4
    qu.mel("clar", "Eb5:1/2 F5:1/2 F#5:1/2 G5:1/2 | C6:1/2:s r:1/2 G5:1/2:s Eb5:1/2:s | C6:1/2 Ab5:1/2 Eb5:1/2 Ab5:1/2 | "
                   "Bb5:2", vel=44)
    for q_ in range(8):
        qu.add("pz_lo", q_, 0.5, qu.chord_at(q_ + 1e-3).bass_note(41, 53), 34, "arp", "s")
    qu.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(41, 53))
    qu.duck(5.0, parts=["clar"])
    qu.expr(["clar"], [(0, -22), (1, -17), (8, -17)])
    qu.expr(["pz_lo"], [(0, -18), (1, -14), (8, -14)])
    qu.expr(["vla", "vln1"], [(0, -28), (1.5, -25), (8, -23)])
    # 'he was so happy; he climbed down quickly and welcomed Jesus with joy': a run down the tree, his tune, claps
    t_jb, okj = lead(c, segs, "sparkle", "他高兴极了", 0, t_joy - 0.1, j.t(1.6) - c.t0, "arms up (a glint)",
                     glock=(86, 98), vel=40)
    q_jb = qpos(j, c, t_jb, 0.0, 1.6) if okj else 0.0
    j.add("xylo", q_jb, _dq(j, q_jb, 1.0), "D6", 44, "arp", "h")
    j.add("xylo", q_jb, _dq(j, q_jb, 1.0), "F6", 42, "arp", "h")
    j.add("glock", q_jb, _dq(j, q_jb, 1.0), "Bb6", 38, "arp", "h")
    if okj:
        j.sync("both arms up, bouncing (a xylophone chord)", q_jb, t_jb)
    slide = "Bb5:1/4 A5:1/4 G5:1/4 F5:1/4 Eb5:1/4 D5:1/4 C5:1/4 Bb4:1/4"     # down the trunk, then home
    j.mel("clar", "r:4 | " + slide + " | " + bars(Z, 1, 4), vel=48)
    j.mel("xylo", "r:4 | " + slide + " | " + bars(Z, 1, 4), vel=34, transpose=12, role="fx")
    i_jy = c.find("他高兴极了")
    t_ld = pic(c, "thud", "他高兴极了", 0)
    if t_ld is not None:                                     # he lands at the foot of the tree: a plucked plop
        clear_near(c, t_ld)
        sg_, q_ld = accent(c, segs, t_ld, "he lands (a plucked plop)", pluck=(55, 67), vel=42)
        drum(sg_, q_ld, 77, 32)
    t_cm = pic(c, "chime", "他高兴极了", 0)
    if t_cm is not None and t_cm < c.dur - 0.5:              # 'come!' -- a glint
        accent(c, segs, t_cm, None, glock=(86, 98), vel=34)
    oom(j, 0, 12, vel=34, cpart="marimba")
    darbuka(j, 0, 12, vel=30)
    claps(j, 4, 12, vel=30)
    j.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    j.duck(2.5, parts=["clar", "xylo"])
    lv(j, ["clar"], -16)
    lv(j, ["xylo"], -17)
    lv(j, ["glock"], -14)
    lv(j, ["pz_cb"], -13)
    lv(j, ["marimba"], -20)
    lv(j, "hand", -18)
    j.expr(["vla", "vln1"], [(0, -24), (12, -24)])
    for sg in segs:
        lv(sg, ["pz_hi"], -13)


def grumble(c):
    """The crowd grumbles (G minor, 2/4): a muttering bassoon over low pizzicato and soft low tremolo (a whisper on
    '小声说'); 'hmph!' on '哼' (bassoon, muted trumpet, low pizzicato, a guiro scrape) and the grumble goes on to D7;
    G minor on '大家都说撒该是个坏人'; the deceptive E-flat on '可是耶稣' -- the call, warm on the horn, to F7 (a harp note as
    Jesus lays his hand on Zacchaeus's shoulder, a harp and a glint as the gate opens with warm light)."""
    c.gain(-3.5)
    t_hm = c.ls(c.find("哼"))
    t_b = c.gap(c.find("大家都说撒该是个坏人"))
    t_j = c.at("可是耶稣")
    m = c.seg(0, t_hm, 4, "2/4", "Bb major", nominal=96, label="grumble-mutter")
    h = c.seg(t_hm, t_b, 3, "2/4", "Bb major", nominal=102, label="grumble-hmph")
    b = c.seg(t_b, t_j, 3, "2/4", "Bb major", nominal=109, label="grumble-bad")
    j = c.seg(t_j, c.dur, 3, "2/4", "Bb major", nominal=106, label="grumble-but")
    segs = (m, h, b, j)
    for sg in segs:
        sg.duck(1.5)
    m.prog("Gm:2 | Cm:2 | Gm:2 | D7:2@G-harmonic")
    h.prog("Gm:2 | Eb:2 | D7:2@G-harmonic")
    b.prog("Gm:2 | Cm:2 | D7sus4:1@G-harmonic D7:1@G-harmonic")
    j.prog("Eb:2 | Bb/D:2 | Cm7:1 F7:1")
    h.sync("'哼': hmph (G minor)", 0, t_hm, kind="change")
    b.sync("'大家都说撒该是个坏人' (G minor)", 0, t_b, kind="change")
    j.sync("'可是耶稣': but Jesus (E-flat)", 0, t_j, kind="change")
    mutter = ("G2:1/4 G2:1/4 A2:1/4 Bb2:1/4 A2:1/2 G2:1/2 | C3:1/4 C3:1/4 D3:1/4 Eb3:1/4 D3:1/2 C3:1/2 | "
              "G2:1/4 G2:1/4 A2:1/4 Bb2:1/4 A2:1/2 G2:1/2 | D3:1/4 D3:1/4 Eb3:1/4 D3:1/4 C3:1/2 A2:1/2")
    # 'everyone saw it and was unhappy; they whispered': the mutter
    m.mel("bsn", mutter, vel=44, art="s")
    for q_ in range(8):
        m.add("pz_lo", q_, 0.5, m.chord_at(q_ + 1e-3).bass_note(43, 55), 34, "arp", "s")
    m.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 67, vel=26, bass_ref=(43, 55))
    m.duck(2.0, parts=["bsn"])
    lv(m, ["bsn"], -15)
    lv(m, ["pz_lo"], -14)
    m.expr(["trem_va", "trem_hi"], [(0, -27), (8, -24)])
    # 'hmph! why would Jesus stay with a bad man?': the hmph, then the grumble, D7
    h.add("bsn", 0, 0.5, "G2", 50, "melody", "s")
    h.add("mtpt", 0, 0.5, "G3", 46, "arp", "s")
    h.add("pz_lo", 0, 0.5, "G2", 46, "arp", "h")
    h.add("pz_cb", 0, 0.5, "G1", 44, "bass", "h")
    for nm in ("Bb3", "D4"):
        h.add("pz_hi" if midi(nm) >= 55 else "pz_lo", 0, 0.5, nm, 40, "arp", "h")
    drum(h, 0, 73, 30)
    h.sync("'哼': hmph (bassoon, muted trumpet, pizzicato)", 0, t_hm)
    h.mel("bsn", "r:1 Bb2:1/4 Bb2:1/4 C3:1/4 Bb2:1/4 | G2:1/4 G2:1/4 Bb2:1/4 C3:1/4 Eb3:1/2 Bb2:1/2 | "
                 "A2:1/4 A2:1/4 C3:1/4 A2:1/4", vel=42, art="s")
    h.mel("bsn", "r:5 D3:1", vel=38)
    for q_ in range(1, 6):
        h.add("pz_lo", q_, 0.5, h.chord_at(q_ + 1e-3).bass_note(43, 55), 32, "arp", "s")
    h.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 67, vel=26, bass_ref=(43, 55))
    h.duck(2.5, parts=["bsn"])
    lv(h, ["bsn"], -15)
    lv(h, ["mtpt"], -17)
    lv(h, ["pz_lo", "pz_cb", "pz_hi"], -13)
    lv(h, "hand", -18)
    h.expr(["trem_va", "trem_hi"], [(0, -25), (6, -24)])
    # 'everyone said Zacchaeus was a bad man': the mutter, sulky
    b.add("pz_lo", 0, 0.5, "G2", 30, "arp", "h")
    for nm in ("Bb3", "D4"):
        b.add("pz_hi", 0, 0.5, nm, 30, "arp", "h")
    b.mel("bsn", "G2:1/4 G2:1/4 Bb2:1/4 G2:1/4 D3:1/2 G2:1/2 | C3:1/4 C3:1/4 D3:1/4 Eb3:1/4 D3:1/2 C3:1/2 | "
                 "D3:1 C3:1/2 A2:1/2", vel=42, art="s")
    for q_ in range(6):
        b.add("pz_lo", q_, 0.5, b.chord_at(q_ + 1e-3).bass_note(43, 55), 32, "arp", "s")
    b.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 67, vel=26, bass_ref=(43, 55))
    b.duck(2.0, parts=["bsn"])
    lv(b, ["pz_lo"], -15)
    lv(b, ["pz_hi"], -17)
    b.expr(["trem_va", "trem_hi"], [(0, -24), (6, -25)])
    b.expr(["bsn"], [(0, -22), (1.5, -16), (6, -16)])
    # 'but Jesus still wanted to go to his house': the deceptive E-flat, the call on the horn, warm strings, F7
    j.mel("horn", "G4:1 Ab4:1/2 A4:1/2 | Bb4:2 | C5:1 A4:1", vel=46)
    strings(j, vel=34, lo=53, hi=72, bass=(40, 52), cb=(28, 40))
    roll_chord(j, 0.05, 51, 75, vel=32, part="harp", n=5)
    t_hd = pic(c, "cloth", "可是耶稣", 1)
    if t_hd is not None and t_hd < c.dur - 0.4:              # Jesus's kind hand on his shoulder: a soft harp note
        accent(c, segs, t_hd, None, harp=(65, 77), vel=34)
    hit(c, segs, "chime", "可是耶稣", 0, "the gate opens, warm light (a harp and a glint)", harp=(72, 84), glock=(86, 98),
        vel=40)
    j.duck(3.0, parts=["horn"])
    j.expr(["horn"], [(0, -20), (1, -18), (6, -18)])
    lv(j, ["harp"], -16)
    lv(j, ["glock"], -14)
    j.expr(STR, [(0, -23), (1, -20), (6, -21)])


def promise(c):
    """Zacchaeus's house (B-flat, 2/4): marimba, guitar and soft strings; nervous as he stands up (tiptoe pizzicato,
    a trembling clarinet, a pluck as he stands and a soft thump as he hops down, a snare roll); the brave march on the
    trumpet on '主啊' (his tune with dotted steps, horn, pizzicato, a light snare and timpani), a glint as the money chest
    opens; ta-da at the end of '我就还他四倍' (trumpet, horns, timpani, a cymbal breath, glockenspiel); the glosses with
    clear plucks: the card pops up, ten coins drop in a row (a koto ripple of ten), two piles of five (two plucked
    chords), one pile to the poor (a harp glint); the second card, one coin (one low pluck), and four coins popping out
    one by one (four plucks climbing) to F7."""
    c.gain(-3.0)
    t_n = voice_at(c, "撒该站起来")
    t_f = c.gap(c.find("主啊"))
    t_td = c.le(c.find("我就还他四倍"))
    t_g1 = c.ls(c.find("一半，就是"))
    t_g2 = c.ls(c.find("四倍，就是"))
    h = c.seg(0, t_n, 2, "2/4", "Bb major", nominal=98, label="promise-house")
    n = c.seg(t_n, t_f, 2, "2/4", "Bb major", nominal=92, label="promise-nervous")
    f = c.seg(t_f, t_td, 8, "2/4", "Bb major", nominal=109, label="promise-march")
    td = c.seg(t_td, t_g1, 1, "2/4", "Bb major", nominal=None, label="promise-tada")
    g1 = c.seg(t_g1, t_g2, 4, "2/4", "Bb major", nominal=108, label="promise-half")
    g2 = c.seg(t_g2, c.dur, 4, "2/4", "Bb major", nominal=106, label="promise-four")
    segs = (h, n, f, td, g1, g2)
    for sg in segs:
        sg.duck(1.5)
    h.prog("Bb:2 | Eb:1 F7:1")
    n.prog("Gm:1 Cm:1 | F7sus4:1 F7:1")
    f.prog("Bb:2 | Bb:2 | Eb:2 | F:2 | Gm:1 Eb:1 | Bb/F:1 F7:1 | Eb:1 F7:1 | F7sus4:1 F7:1")
    td.prog("Bb:2")
    g1.prog("Eb:2 | Bb/D:2 | Cm7:1 F7:1 | Bb:2")
    g2.prog("Eb:2 | Bb/D:2 | Gm:1 C7:1 | F7:2")
    f.sync("'主啊': the brave march (B-flat)", 0, t_f, kind="change")
    td.sync("'我就还他四倍': ta-da", 0, t_td)
    g1.sync("'一半，就是': the first gloss (E-flat)", 0, t_g1, kind="change")
    g2.sync("'四倍，就是': the second gloss (E-flat)", 0, t_g2, kind="change")
    # 'in Zacchaeus's house': marimba, guitar, soft strings
    roll_chord(h, 0.0, 58, 77, vel=34, part="marimba", n=4)
    broken(h, "guitar", 0, 4, (0, 2, 1, 2), 46, 62, vel=32, thin=True)
    h.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_part="vc", bass_lo=39, bass_hi=51)
    h.expr(["marimba"], [(0, -24), (1, -19), (4, -19)])
    h.expr(["guitar"], [(0, -19), (1, -14), (4, -14)])
    h.expr(["vla", "vln1", "vc"], [(0, -27), (1, -24), (4, -24)])
    # 'Zacchaeus stood up and said to Jesus': nervous -- tiptoe pizzicato, a trembling clarinet, a snare roll
    for q_ in np.arange(0, 4, 0.25):
        if not bool(n.score.speaking(n.t(q_))) or abs(q_ % 1.0) < 1e-6:
            n.add("pz_hi", q_, 0.25, n.chord_at(q_ + 1e-3).tones(58, 70)[int(q_ * 4) % 2], 30, "arp", "S")
    trem(n, "clar", 0.0, 1.75, "D5", 30, rate=0.125, role="fx", alt="Eb5")
    trem(n, "clar", 2.0, 3.75, "C5", 30, rate=0.125, role="fx", alt="Bb4")
    for k_, q_ in enumerate(np.arange(2.0, 4.0, 1 / 12)):
        n.add("okit", q_, 1 / 12, 38, 18 + k_, "perc")
    n.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=26, bass_part="vc", bass_lo=41, bass_hi=53)
    hit(c, segs, "cloth", None, 0, "he stands up (a pluck)", pluck=(58, 70), marim=(70, 82), vel=40)
    hit(c, segs, "thud", None, 0, "he hops down (a soft thump)", low=True, pluck=(55, 67), block=77, vel=40)
    lv(n, ["pz_hi"], -14)
    lv(n, ["clar"], -21)
    n.expr("okit", [(2, -26), (4, -19)])
    n.expr(["vla", "vln1", "vc"], [(0, -21), (4, -22)])
    # 'Lord, I will give half of my money to the poor! if I took too much from anyone, I will pay back four times!'
    march = ("D5:3/4 Eb5:1/4 E5:1/2 F5:1/2 | Bb5:1 F5:1/2 D5:1/2 | Eb5:3/4 F5:1/4 G5:1/2 Bb5:1/2 | A5:1 F5:1 | "
             "G5:3/4 F5:1/4 Eb5:1/2 G5:1/2 | F5:3/4 D5:1/4 C5:1/2 Eb5:1/2 | Eb5:1/2 G5:1/2 F5:1/2 A5:1/2 | F5:1 A5:1")
    f.mel("tpt", march, vel=48)
    f.mel("horn", march, vel=40, transpose=-12, role="fx")
    for q_ in range(16):
        ch = f.chord_at(q_ + 1e-3)
        f.add("pz_cb", q_, 0.5, ch.bass_note(33, 45) if q_ % 2 == 0 else _alt_bass(ch, 33, 45), 36, "arp", "s")
        if not bool(f.score.speaking(f.t(q_ + 0.5))):
            for pt in f.chord_at(q_ + 0.51).tones(58, 70)[:3]:
                f.add("marimba", q_ + 0.5, 0.25, pt, 28, "arp", "s")
    for q_ in range(0, 16, 2):
        drum(f, q_, 38, 24, part="okit")
        f.add("timp", q_, 0.5, "Bb2" if f.chord_at(q_ + 1e-3).root == 10 else
              [p for p in range(38, 51) if p % 12 in f.chord_at(q_ + 1e-3).pcset][0], 34, "timp", "h")
    f.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=28, bass_ref=(33, 45))
    hit(c, segs, "sparkle", "主啊", 0, "the money chest opens (a glint)", glock=(86, 98), vel=40)
    f.duck(3.0, parts=["tpt", "horn"])
    lv(f, ["tpt"], -20)
    lv(f, ["horn"], -23)
    lv(f, ["pz_cb"], -14)
    lv(f, ["marimba"], -22)
    lv(f, "okit", -24)
    lv(f, ["timp"], -19)
    f.expr(["vla", "vln1"], [(0, -25), (16, -24)])
    # ta-da: the promise made
    td.add("tpt", 0, 2, "Bb5", 46, "melody")
    td.add("horn", 0, 2, "F4", 40, "melody")
    td.add("horn", 0, 2, "D4", 38, "harmony")
    td.add("timp", 0, 1, "Bb2", 44, "timp", "h")
    td.add("pz_cb", 0, 1, "Bb1", 46, "bass", "h")
    td.add("glock", 0, 1.5, "D7", 40, "arp", "h")
    td.add("okit", 0, 2, 57, 24, "perc", "h")
    for nm in ("Bb3", "F4", "D5"):
        td.add("pz_hi", 0, 0.5, nm, 44, "arp", "h")
    td.pad(["vla", "vla", "vln1"], 3, 53, 74, vel=30, bass_part="vc", bass_lo=39, bass_hi=51)
    lv(td, ["tpt"], -18)
    lv(td, ["horn"], -21)
    lv(td, ["timp"], -15)
    lv(td, ["pz_cb", "pz_hi"], -12)
    lv(td, ["glock"], -13)
    lv(td, "okit", -21)
    td.expr(["vla", "vln1", "vc"], [(0, -21), (2, -22)])
    # 'half: if you have ten coins, five go to the poor!'
    for sg in (g1, g2):
        oom(sg, 0, 8, vel=30, bass=(33, 45), cpart="marimba")
        sg.pad(["vla", "vla", "vln1"], 3, 53, 72, vel=26, bass_ref=(33, 45))
        lv(sg, ["pz_cb"], -15)
        lv(sg, ["marimba"], -23)
        sg.expr(["vla", "vln1"], [(0, -25), (8, -25)])
    hit(c, segs, "pop", "一半，就是", 0, "the first card pops up (a pluck)", koto=(70, 82), marim=(74, 86), vel=40)
    i_h = c.find("一半，就是")
    ch10 = pick_times(pics(c, "coins"), c.ls(i_h) - 0.3, c.le(i_h) + 0.6)
    pic_h = len(ch10) >= 2
    t_ten = ch10[0] if pic_h else (chars(c, "一半，就是", "十") or [voice_at(c, "就是有十块钱") + 0.4])[0]
    t_two = ch10[1] if pic_h else (chars(c, "一半，就是", "五") or [voice_at(c, "分五块给穷人") + 0.2])[0]
    t_bowl = ch10[2] if len(ch10) >= 3 else None
    # ten coins drop in a row: a koto ripple of ten, climbing
    clear_near(c, t_ten, win=0.5)
    sg_, q_t = seg_at(c, segs, t_ten)
    ladder_ = sg_.chord_at(q_t + 1e-3).tones(62, 86)[:10]
    for k_, p in enumerate(ladder_):
        sg2, q2 = seg_at(c, segs, t_ten + 0.045 * k_)
        sg2.add("koto", q2, _dq(sg2, q2, 0.5), p, 38 + k_, "arp", "h" if k_ == 0 else "")
    sg_.add("xylo", q_t, _dq(sg_, q_t, 0.25), ladder_[0] + 12, 36, "arp", "h")
    sg_.sync("ten coins drop in a row (a koto ripple)" + (" (picture)" if pic_h else ""), q_t, t_ten)
    # two piles of five: two plucked chords, low and high
    clear_near(c, t_two, win=0.2)
    sg_, q_2 = seg_at(c, segs, t_two)
    for k_, (lo_, hi_) in enumerate(((58, 70), (70, 82))):
        sg2, q2 = seg_at(c, segs, t_two + 0.16 * k_)
        for pt in sg2.chord_at(q2 + 1e-3).tones(lo_, hi_)[:3]:
            sg2.add("koto", q2, _dq(sg2, q2, 0.5), pt, 42, "arp", "h")
        sg2.add("pz_hi", q2, _dq(sg2, q2, 0.25), sg2.chord_at(q2 + 1e-3).tones(lo_, hi_)[0], 40, "arp", "h")
    sg_.sync("two piles of five (two plucked chords)" + (" (picture)" if pic_h else ""), q_2, t_two)
    if t_bowl is not None:
        accent(c, segs, t_bowl, "one pile to the poor (a harp glint)", harp=(77, 89), vel=38)
    hit(c, segs, "sparkle", "一半，就是", 0, "a heart for the poor (a glint)", glock=(86, 98), vel=38)
    # 'four times: if you took one coin too many, give back four!'
    hit(c, segs, "pop", "四倍，就是", 0, "the second card pops up (a pluck)", koto=(70, 82), marim=(74, 86), vel=40)
    i_4 = c.find("四倍，就是")
    one = pick_times(pics(c, "coins"), c.ls(i_4) - 0.3, c.dur)
    t_one = one[0] if one else (chars(c, "四倍，就是", "一") or [voice_at(c, "就是多收了一块钱") + 0.5])[0]
    clear_near(c, t_one, win=0.2)
    accent(c, segs, t_one, "one coin (one low pluck)" + (" (picture)" if one else ""), koto=(58, 65), pluck=(55, 62),
           vel=42)
    four = pick_times(pics(c, "pop"), t_one + 0.3, c.dur, 4)
    pic_4 = len(four) >= 1
    if not pic_4:
        t4 = (chars(c, "四倍，就是", "四") or [voice_at(c, "要还四块钱")])[-1]
        four = [t_ for t_ in (t4 + 0.25 * k_ for k_ in range(4)) if t_ < c.dur - 0.12]
    for t_ in four:
        clear_near(c, t_)
    climb(c, segs, four, part="koto", lo=64, hi=88, vel=40, sync=(0, len(four) - 1) if pic_4 else (),
          what="four coins pop out", glock=False, pz=True)
    for sg in (g1, g2):
        sg.duck(2.0, parts=["koto", "marimba"])
    for sg in segs:
        lv(sg, ["koto"], -15)
        lv(sg, ["xylo"], -16)
        lv(sg, ["harp"], -16)
        if sg is not td:
            lv(sg, ["glock"], -14)
            lv(sg, ["pz_hi"], -13)


def saved(c):
    """'耶稣笑了' (B-flat, warm strings, harp, the marimba); A7sus4 on '今天，' (a timpani roll, the strings rising);
    the radiant D major on '救恩' -- trumpet, horns, strings, choir 'aah', a harp glissando, glockenspiel, timpani, a
    cymbal breath (on the picture's light when it comes with the word); B minor on '就是说' -- the call on the clarinet
    in D ('撒该也是上帝家里的人'); G on '我来' (soft strings, harp, a horn); D on '撒该想看看耶稣': his perky head on the
    clarinet in D; G on '原来耶稣也在找撒该': the call answering on the horn; D on '就像牧羊人': the shepherd's echo on the
    pan flute over a drone."""
    c.gain(-2.5)
    t_s2 = c.gap(c.find("今天，救恩到了这一家"))
    t_jy = c.at("救恩")
    t_m = c.gap(c.find("就是说"))
    t_l = c.gap(c.find("我来"))
    t_f = c.gap(c.find("撒该想看看耶稣"))
    t_also = c.at("原来耶稣也在找撒该")
    t_sh = c.at("就像牧羊人")
    s1 = c.seg(0, t_s2, 2, "2/4", "Bb major", nominal=82, label="saved-smile")
    s2 = c.seg(t_s2, t_jy, 1, "2/4", "Bb major", nominal=None, label="saved-today")
    r = c.seg(t_jy, t_m, 1, "4/4", "D major", nominal=None, label="saved-salvation")
    m = c.seg(t_m, t_l, 2, "4/4", "D major", nominal=78, label="saved-family")
    lo_ = c.seg(t_l, t_f, 2, "4/4", "D major", nominal=96, label="saved-lost")
    f1 = c.seg(t_f, t_also, 2, "2/4", "D major", nominal=94, label="saved-see")
    f2 = c.seg(t_also, t_sh, 2, "2/4", "D major", nominal=88, label="saved-found")
    p = c.seg(t_sh, c.dur, 2, "6/8", "D major", nominal=108, label="saved-shepherd")
    segs = (s1, s2, r, m, lo_, f1, f2, p)
    for sg in segs:
        sg.duck(1.5)
    s1.prog("Bb:2 | Gm7:2")
    s2.prog("A7sus4:2@D-major")
    r.prog("D:4")
    m.prog("Bm:2 D/A:2 | G:2 A7:2")
    lo_.prog("G:2 D/F#:2 | Em7:2 A7:2")
    f1.prog("D:2 | D:2")
    f2.prog("G:2 | Em7:1 A7:1")
    p.prog("D:3 | G/D:3/2 D:3/2")
    s2.sync("'今天，': A7sus4", 0, t_s2, kind="change")
    r.sync("'救恩': salvation (radiant D major)", 0, t_jy, kind="change")
    m.sync("'就是说': B minor", 0, t_m, kind="change")
    lo_.sync("'我来': G", 0, t_l, kind="change")
    f1.sync("'撒该想看看耶稣': D", 0, t_f, kind="change")
    f2.sync("'原来耶稣也在找撒该': G", 0, t_also, kind="change")
    p.sync("'就像牧羊人': the shepherd's echo (D)", 0, t_sh, kind="change")
    # 'Jesus smiled and said': warm strings, harp, the marimba
    strings(s1, vel=32, lo=53, hi=72, bass=(40, 52), cb=(28, 40))
    broken(s1, "harp", 0, 4, (0, 2, 4, 2), 51, 77, vel=30, thin=True)
    roll_chord(s1, 0.0, 58, 77, vel=30, part="marimba", n=4)
    hit(c, segs, "sparkle", None, 0, "Jesus smiles (a glint)", glock=(86, 98), vel=38)
    s1.expr(STR, [(0, -24), (4, -22)])
    lv(s1, ["harp"], -17)
    lv(s1, ["marimba"], -20)
    # 'today': A7sus4, a timpani roll, the strings rising
    strings(s2, vel=34, lo=55, hi=76, bass=(40, 52), cb=(28, 40))
    for k_, q_ in enumerate(np.arange(0, 2, 1 / 8)):
        s2.add("timp", q_, 1 / 8, "A2", 22 + 2 * k_, "timp")
    s2.expr(STR, [(0, -22), (2, -18)])
    lv(s2, ["timp"], -18)
    # 'salvation has come to this house!': the radiant D major
    t_lt, okl = lead(c, segs, "chime", None, 0, t_jy - 0.05, r.t(1.5) - c.t0, "the light (a glint)", glock=(86, 98),
                     vel=42)
    if not okl:
        t_lt, okl = lead(c, segs, "sparkle", None, 0, t_jy - 0.05, r.t(1.5) - c.t0, "the light (a glint)",
                         glock=(86, 98), vel=42)
    q_l = qpos(r, c, t_lt, 0.0, 1.5) if okl else 0.0
    strings(r, vel=40, lo=57, hi=78, bass=(40, 52), cb=(28, 40))
    r.pad(["horn", "horn", "horn"], 3, 50, 69, vel=40, bass_ref=(38, 50))
    r.pad("choir", 3, 57, 74, vel=34, bass_ref=(38, 50))
    r.add("tpt", 0, 4, "A5", 44, "melody")
    r.add("timp", q_l, _dq(r, q_l, 1.5), "D3", 44, "timp", "h")
    r.add("pz_cb", q_l, _dq(r, q_l, 1.0), "D2", 46, "bass", "h")
    r.add("okit", q_l, 2, 57, 26, "perc", "h")
    r.add("glock", q_l, _dq(r, q_l, 2.0), "F#6", 44, "arp", "h")
    r.add("glock", q_l, _dq(r, q_l, 2.0), "D7", 38, "arp", "h")
    sweep(r, q_l + 0.02, 0.6, "D4", "D6", 26, 38, part="harp")
    if okl:
        r.sync("salvation: the light (picture)", q_l, t_lt)
    r.duck(6.0)
    r.expr(STR, [(0, -21), (1, -17), (4, -18)])
    r.expr(["horn"], [(0, -24), (1, -19), (4, -20)])
    r.expr(["choir"], [(0, -27), (1.5, -22), (4, -22)])
    lv(r, ["tpt"], -19)
    lv(r, ["timp", "pz_cb"], -13)
    lv(r, "okit", -20)
    lv(r, ["glock"], -13)
    lv(r, ["harp"], -15)
    # 'that is: God saved Zacchaeus! Zacchaeus belongs to God's family too': the call on the clarinet, in D
    m.mel("clar", "F#5:1 G5:1/2 G#5:1/2 A5:2 | D6:3/2 C#6:1/2 B5:1 A5:1", vel=46)
    strings(m, vel=34, lo=54, hi=74, bass=(40, 52), cb=(28, 40))
    broken(m, "harp", 0, 8, (0, 2, 4, 2), 50, 74, vel=30, thin=True)
    hit(c, segs, "sparkle", "就是说", 0, "a heart rises over him (a glint)", glock=(86, 98), vel=38)
    m.duck(5.5, parts=["clar"])
    m.duck(1.5, parts=STR + ["harp"])
    m.expr(["clar"], [(0, -20), (1, -17), (8, -17)])
    lv(m, ["harp"], -18)
    m.expr(STR, [(0, -22), (8, -23)])
    # 'I came to find the lost and bring them home': soft strings, harp, a horn answering in the pause
    strings(lo_, vel=32, lo=54, hi=74, bass=(40, 52), cb=(28, 40))
    broken(lo_, "harp", 0, 8, (0, 2, 4, 2), 50, 74, vel=28, thin=True)
    lo_.mel("horn", "r:6 C#4:1 E4:1", vel=40)
    lo_.duck(2.5)
    lo_.expr(STR, [(0, -22), (8, -22)])
    lv(lo_, ["harp"], -17)
    lv(lo_, ["horn"], -21)
    # 'Zacchaeus wanted to see Jesus': his perky head on the clarinet, in D
    f1.mel("clar", "F#5:1/2 G5:1/2 G#5:1/2 A5:1/2 | D6:1/2:s r:1/2 A5:1/2:s F#5:1/2", vel=44)
    for q_ in range(4):
        f1.add("pz_lo", q_, 0.5, f1.chord_at(q_ + 1e-3).bass_note(38, 50) if q_ % 2 == 0 else
               _alt_bass(f1.chord_at(q_ + 1e-3), 38, 50), 32, "arp", "s")
    f1.pad(["vla", "vla", "vln1"], 3, 54, 74, vel=28, bass_ref=(38, 50))
    hit(c, segs, "pop", "撒该想看看耶稣", 0, "the picture of the tree pops up (a pluck)", pluck=(62, 74), xylo=(74, 86),
        block=76, vel=44)
    f1.duck(1.5, parts=["clar"])
    lv(f1, ["clar"], -16)
    lv(f1, ["pz_lo"], -13)
    f1.expr(["vla", "vln1"], [(0, -24), (2.5, -23), (4, -20)])
    # '... and Jesus was looking for Zacchaeus too!': the call answering on the horn, warm strings
    f2.mel("horn", "B4:1 A4:1/2 B4:1/2 | D5:1 C#5:1", vel=46)
    strings(f2, vel=34, lo=54, hi=74, bass=(40, 52), cb=(28, 40))
    roll_chord(f2, 0.05, 50, 74, vel=24, part="harp", n=5)
    f2.add("pz_lo", 0, 0.5, "G2", 34, "arp", "s")             # the bows take a moment: a soft plucked G carries the beat
    for nm in ("D4", "G4"):
        f2.add("pz_hi", 0, 0.5, nm, 30, "arp", "s")
    lv(f2, ["pz_lo", "pz_hi"], -15)
    f2.duck(3.0, parts=["horn"])
    f2.expr(["horn"], [(0, -28), (1.5, -20), (4, -19)])
    f2.expr(["harp"], [(0, -23), (1.5, -17), (4, -17)])
    f2.expr(["vla", "vln1"], [(0, -22), (1.5, -20), (4, -20)])
    f2.expr(["vc", "cb"], [(0, -28), (1.5, -20), (4, -20)])
    # 'like a shepherd looking for his lost lamb': the pan flute over a drone
    p.mel("panflute", "A5:1/2 B5:1/2 A5:1/2 F#5:1 D5:1/2 | E5:1/2 F#5:1/2 E5:1/2 D5:3/2", vel=44)
    p.add("vc", 0, 6, "D2", 30, "bass")
    p.pad(["vla", "vla", "vln1"], 3, 54, 74, vel=26, bass_ref=(38, 50))
    broken(p, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 50, 74, vel=26, thin=True)
    hit(c, segs, "sparkle", "撒该想看看耶稣", 0, "the moonlit hills (a harp glint)", harp=(74, 86), glock=(86, 98), vel=38)
    t_lamb = pic(c, "sheep", "撒该想看看耶稣", 0)
    if t_lamb is not None and t_lamb < c.dur - 0.3:          # the lamb nuzzles him (a harp note; the cue's last second)
        accent(c, segs, t_lamb, None, harp=(74, 86), vel=32)
    p.duck(2.5, parts=["panflute"])
    p.expr(["panflute"], [(0, -20), (1, -17), (6, -17)])
    lv(p, ["vc"], -22)
    lv(p, ["harp"], -18)
    p.expr(["vla", "vln1"], [(0, -24), (6, -24)])
    for sg in segs:
        if sg is not r:
            lv(sg, ["glock"], -14)


def heart(c):
    """The golden evening (B-flat, 2/4): the generous song -- Zacchaeus's tune, now broad and diatonic -- on the horn
    over harp, warm strings, plucked basses and a shimmering koto, cadencing as the scene ends."""
    c.gain(-4.0)
    s = c.seg(0, c.dur, 8, "2/4", "Bb major", nominal=100, label="heart-song")
    s.duck(1.5)
    s.prog(" | ".join(GEN_PROG))
    s.mel("horn", bars(GEN, 0, 8), vel=50, transpose=-12)
    strings(s, vel=34, lo=53, hi=74, bass=(39, 51), cb=None)
    broken(s, "harp", 0, 16, (0, 2, 4, 2), 51, 77, vel=30, thin=True)
    for q_ in range(0, 16):
        if not bool(s.score.speaking(s.t(q_ + 0.5))):
            s.add("koto", q_ + 0.5, 0.5, top(s, q_ + 0.5, 77, 89), 28, "arp", "s")
    s.duck(6.0, parts=["horn"])
    s.duck(2.0, parts=STR + ["harp"])
    s.expr(["horn"], [(0, -20), (1, -17), (16, -17)])
    lv(s, ["harp"], -17)
    lv(s, ["koto"], -19)
    s.expr(STR, [(0, -23), (2, -21), (16, -21)])
    hit(c, (s,), "coins", None, 0, "a coin for the widow (a koto pluck)", koto=(70, 82), vel=38)
    hit(c, (s,), "coins", None, 1, "four coins for the farmer (a koto pluck)", koto=(70, 82), vel=38)
    hit(c, (s,), "sparkle", None, 0, "a heart over Zacchaeus (a glint)", glock=(86, 98), vel=38)
    hit(c, (s,), "sparkle", None, 1, "hearts over everyone (a glint)", glock=(86, 98), vel=36)
    lv(s, ["glock"], -14)


def end(c):
    """The modern frame again (F major): the call on the marimba ('耶稣知道撒该的名字，也知道你的名字'; guitar, soft
    strings); G minor 7 on '不管别人' (tender); F on '他也想住进你的心里' -- the generous song's head; B-flat on
    '小朋友，如果耶稣今天到你家来', very soft; C7sus4 at the end of '你想对他说什么呢', hanging through the answer pause
    (a guitar, the marimba asks once); the final F chord on the end card (marimba, guitar, glockenspiel together, then
    rolled), ringing to the end."""
    c.gain(-3.5)
    t_l = c.gap(c.find("不管别人"))
    t_h = c.at("他也想住进你的心里")
    t_q = c.gap(c.find("小朋友，如果耶稣今天"))
    t_f = c.le(c.find("你想对他说什么呢"))
    t_raw = pic(c, "chime", "你想对他说什么呢")
    t_card = t_raw if t_raw is not None and t_f + 0.5 <= t_raw <= c.dur - 0.6 else None
    t_fin = t_card if t_card is not None else max(t_f + 0.8, c.dur - 2.6)
    n = c.seg(0, t_l, 2, "4/4", "F major", nominal=91, label="end-name")
    l = c.seg(t_l, t_h, 3, "2/4", "F major", nominal=98, label="end-love")
    h = c.seg(t_h, t_q, 2, "2/4", "F major", nominal=107, label="end-heart")
    q = c.seg(t_q, t_f, 4, "2/4", "F major", nominal=94, label="end-question")
    sp = c.seg(t_f, t_fin, 1, "2/4", "F major", nominal=None, label="end-space")
    f = c.seg(t_fin, c.dur, 1, "2/4", "F major", nominal=None, rit=0.3, label="end-final-chord")
    segs = (n, l, h, q, sp, f)
    for sg in (n, l, h, q):
        sg.duck(1.5)
    n.prog("F:4 | Dm:2 Bb:2")
    l.prog("Gm7:2 | Am7:2 | Bb:1 C7:1")
    h.prog("F:2 | Dm:1 C7:1")
    q.prog("Bb/D:2 | F/A:2 | Dm7:2 | Gm7:2")
    sp.prog("C7sus4:2")
    f.prog("F:2")
    l.sync("'不管别人': tender (G minor 7)", 0, t_l, kind="change")
    h.sync("'他也想住进你的心里': home (F)", 0, t_h, kind="change")
    q.sync("'小朋友，如果耶稣今天': the last question (B-flat)", 0, t_q, kind="change")
    sp.sync("'你想对他说什么呢': C7sus4, the question hangs", 0, t_f, kind="change")
    f.sync("the final F chord (the end card)", 0, t_fin, kind="change")
    f.sync("the end card: the final chord" if t_card is not None else "the final chord", 0, t_fin)
    # 'child, Jesus knew Zacchaeus's name, and he knows yours too': the call on the marimba
    n.mel("marimba", "A4:1 Bb4:1/2 B4:1/2 C5:2 | F5:3/2 E5:1/2 D5:2", vel=50)
    broken(n, "guitar", 0, 8, (0, 2, 1, 2), 41, 57, vel=32, thin=True)
    n.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=38, bass_hi=50)
    n.duck(4.0, parts=["marimba"])
    n.duck(1.5, parts=["guitar", "vla", "vln1", "vc"])
    n.expr(["marimba"], [(0, -16), (1, -13), (8, -13)])
    lv(n, ["guitar"], -13)
    n.expr(["vla", "vln1", "vc"], [(0, -24), (8, -23)])
    # 'whether others like you or not, Jesus loves you': tender
    l.mel("marimba", "Bb4:1 A4:1/2 G4:1/2 | C5:1 Bb4:1/2 A4:1/2 | D5:1 E5:1", vel=46)
    broken(l, "guitar", 0, 6, (0, 2, 1, 2), 41, 57, vel=30, thin=True)
    l.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=38, bass_hi=50)
    hit(c, segs, "chime", "不管别人", 0, "a heart pops up on '爱' (a glint)", glock=(86, 98), vel=38)
    l.duck(4.0, parts=["marimba"])
    l.expr(["marimba"], [(0, -19), (1, -14), (6, -14)])
    l.expr(["guitar"], [(0, -18), (1, -13), (6, -13)])
    l.expr(["vla", "vln1", "vc"], [(0, -23), (6, -22)])
    # 'he wants to live in your heart too': F, the generous song's head
    h.mel("marimba", "A4:1 Bb4:1/2 C5:1/2 | F5:3/2 E5:1/2", vel=48)
    broken(h, "guitar", 0, 4, (0, 2, 1, 2), 41, 57, vel=30, thin=True)
    strings(h, vel=32, lo=50, hi=71, bass=(41, 53), cb=(29, 41))
    hit(c, segs, "sparkle", "他也想住进你的心里", 0, "a heart (a glint)", glock=(86, 98), vel=38)
    h.duck(2.5, parts=["marimba"])
    h.expr(["marimba"], [(0, -21), (1, -14), (4, -14)])
    h.expr(["guitar"], [(0, -18), (1, -13), (4, -13)])
    h.expr(STR, [(0, -27), (1, -22), (4, -21)])
    # 'child, if Jesus came to your home today, what would you say to him?': very soft
    q.mel("marimba", "F5:1 D5:1 | C5:1 A4:1 | D5:1 C5:1/2 A4:1/2 | Bb4:2", vel=42)
    broken(q, "guitar", 0, 8, (0, 2, 1, 2), 41, 57, vel=28, thin=True)
    q.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_part="vc", bass_lo=38, bass_hi=50)
    q.duck(2.0)
    lv(q, ["marimba"], -16)
    lv(q, ["guitar"], -14)
    q.expr(["vla", "vln1", "vc"], [(0, -23), (8, -24)])
    # the space after the question: C7sus4 hanging, very soft; the marimba asks once
    sp.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_part="vc", bass_lo=36, bass_hi=48)
    sp.add("guitar", 0, 2, "C3", 30, "arp", "h")
    sp.add("guitar", 0.06, 1.94, "G3", 26, "arp")
    sp.add("marimba", 0.75, 1.25, "G5", 30, "arp")
    sp.expr(["vla", "vln1", "vc"], [(0, -23), (1, -25), (2, -27)])
    lv(sp, ["guitar"], -15)
    lv(sp, ["marimba"], -17)
    # the final F chord on the end card: marimba, guitar and glockenspiel together, then rolled; strings
    for nm in ("F2", "C3", "A3"):
        f.add("guitar", 0, 2, nm, 42, "arp", "r")
    for nm in ("F4", "C5"):
        f.add("marimba", 0, 2, nm, 44, "arp", "r")
    f.add("glock", 0, 1.5, "A6", 34, "arp", "r")
    f.add("xylo", 0, 0.5, "F6", 30, "arp", "h")
    for k_, nm in enumerate(["A4", "C5", "F5", "A5", "C6"]):
        f.add("marimba", 0.15 + 0.06 * k_, 1.85 - 0.06 * k_, nm, 34 - 2 * k_, "arp", "r")
    strings(f, vel=30, lo=50, hi=69, bass=(41, 53), cb=(29, 41), q0=0.25)
    f.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -25), (0.5, -24), (1.4, -26), (2, -31)])
    f.expr(["guitar", "marimba", "glock", "xylo"], [(0, -19), (2, -23)])
    if t_card is None and t_raw is not None:
        accent(c, segs, t_raw, "the end card (a glint)", glock=(86, 98), vel=38)
    for sg in segs:
        if sg not in (f, sp):
            lv(sg, ["glock", "pz_hi"], -14)


SCENE_CUES = {
    "s01_title": title, "s02_question": question, "s03_jericho": jericho, "s04_crowd": crowd, "s05_tree": tree,
    "s06_call": call, "s07_grumble": grumble, "s08_promise": promise, "s09_saved": saved, "s10_heart": heart,
    "s11_end": end,
}

# Hit points defined by the narration text (audio/music_check.py REQUIRED_HITS format: (scene, phrase, mode, kind)).
REQUIRED_HITS = [
    ("s02_question", "什么都看不见", "phrase", "change"),           # the question (Gm7)
    ("s02_question", "今天", "line", "change"),                     # the story begins (F)
    ("s02_question", "可是，他想了一个好办法", "phrase", "change"),  # B-flat
    ("s02_question", "好办法", "phrase", "hit"),                    # the idea (a xylophone ping)
    ("s03_jericho", "城里住着一个人", "gap", "change"),             # Zacchaeus's tune (B-flat)
    ("s03_jericho", "收税的人，就是", "gap", "change"),             # the Roman emperor (E-flat)
    ("s03_jericho", "撒该管着好多", "gap", "change"),               # the smug strut (B-flat)
    ("s03_jericho", "可是，大家都不喜欢撒该", "gap", "change"),     # G minor
    ("s03_jericho", "大家看见撒该", "gap", "change"),               # everyone steps away (E-flat)
    ("s04_crowd", "撒该也想看看", "gap", "change"),                 # he wants to see too (B-flat)
    ("s04_crowd", "撒该心想", "gap", "change"),                     # no other chance (G minor)
    ("s04_crowd", "可是，撒该的个子太矮了", "gap", "change"),       # too short (E-flat)
    ("s04_crowd", "他跳呀跳", "phrase", "change"),                  # the jumps (G minor)
    ("s04_crowd", "他踮起脚", "phrase", "change"),                  # on tiptoe (C minor)
    ("s04_crowd", "前面的人", "gap", "change"),                     # the wall (G minor)
    ("s04_crowd", "他想挤进去", "gap", "change"),                   # squeezing (G minor)
    ("s04_crowd", "撒该急得团团转", "phrase", "change"),            # round and round (G minor)
    ("s04_crowd", "小朋友，你猜", "gap", "change"),                 # the question (E-flat add9)
    ("s04_crowd", "小朋友，你猜", "end", "change"),                 # the guess: F7sus4 hangs through the pause
    ("s05_tree", "有了", "line", "change"),                         # the idea (B-flat)
    ("s05_tree", "那里有一棵大大的桑树", "gap", "change"),          # the tree (E-flat)
    ("s05_tree", "撒该爬呀爬", "gap", "change"),                    # the climb (B-flat)
    ("s05_tree", "嘿嘿", "gap", "change"),                          # his tune in the tree (B-flat)
    ("s06_call", "停住了", "phrase", "hit"),                        # the hush
    ("s06_call", "他抬起头", "phrase", "change"),                   # warm E-flat
    ("s06_call", "撒该，快下来", "gap", "change"),                  # the call (B-flat)
    ("s06_call", "他吓了一跳", "gap", "change"),                  # G7
    ("s06_call", "耶稣认识我", "gap", "change"),                    # C minor
    ("s06_call", "他高兴极了", "gap", "change"),                    # joy (B-flat)
    ("s07_grumble", "哼", "line", "hit"),                           # hmph!
    ("s07_grumble", "哼", "line", "change"),                        # G minor
    ("s07_grumble", "大家都说撒该是个坏人", "gap", "change"),       # G minor
    ("s07_grumble", "可是耶稣", "phrase", "change"),                # the deceptive E-flat
    ("s08_promise", "主啊", "gap", "change"),                       # the brave march (B-flat)
    ("s08_promise", "我就还他四倍", "end", "hit"),                  # ta-da
    ("s08_promise", "一半，就是", "line", "change"),                # the first gloss (E-flat)
    ("s08_promise", "四倍，就是", "line", "change"),                # the second gloss (E-flat)
    ("s09_saved", "今天，救恩到了这一家", "gap", "change"),         # A7sus4
    ("s09_saved", "救恩", "phrase", "change"),                      # the radiant D major
    ("s09_saved", "就是说", "gap", "change"),                       # B minor
    ("s09_saved", "我来", "gap", "change"),                         # G
    ("s09_saved", "撒该想看看耶稣", "gap", "change"),               # D
    ("s09_saved", "原来耶稣也在找撒该", "phrase", "change"),        # G
    ("s09_saved", "就像牧羊人", "phrase", "change"),                # the shepherd's echo (D)
    ("s11_end", "不管别人", "gap", "change"),                       # tender (G minor 7)
    ("s11_end", "他也想住进你的心里", "phrase", "change"),          # home (F)
    ("s11_end", "小朋友，如果耶稣今天", "gap", "change"),           # the last question (B-flat)
    ("s11_end", "你想对他说什么呢", "end", "change"),               # C7sus4: the question hangs
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or None,
# index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.  Cues in a scene's last
# second (the boy pointing in s02, the gate's light in s07, the coins' last pops in s08, the lamb in s09) are accented
# but not listed: a re-timed narration can push them past the cue.
PICTURE_HITS = [
    ("s01_title", "pop", None, 0, 0.0, "hit", "Zacchaeus peeks out of the leaves (a xylophone grace)"),
    ("s01_title", "chime", None, 0, 0.0, "hit", "the ribbon unfurls (a glint)"),
    ("s01_title", "pop", None, 1, 0.0, "hit", "title character 1 pops in (a xylophone step)"),
    ("s01_title", "pop", None, 6, 0.0, "hit", "title character 6 pops in (a xylophone step)"),
    ("s01_title", "sparkle", None, 0, 0.0, "hit", "the finished title: ta-da (B-flat arrives with it)"),
    ("s02_question", "thud", None, 0, 0.0, "hit", "the boy hops (1)"),
    ("s02_question", "thud", None, 1, 0.0, "hit", "the boy hops (2)"),
    ("s02_question", "thud", None, 2, 0.0, "hit", "back on his heels, pouting (a low pluck)"),
    ("s02_question", "whoosh", None, 0, 0.0, "hit", "dad lifts him onto his shoulders (a xylophone run up)"),
    ("s03_jericho", "coins", "城里住着一个人", 0, 0.0, "hit", "he counts his coins (a clink)"),
    ("s03_jericho", "pop", "收税的人，就是", 0, 0.0, "hit", "the emperor's coin (a timpani and a glint)"),
    ("s03_jericho", "sparkle", "撒该管着好多", 0, 0.0, "hit", "'他很有钱': the chest overflows (a bling, coins glitter up)"),
    ("s03_jericho", "pop", "可是，大家都不喜欢撒该", 0, 0.0, "hit", "he hops off his stool (a pluck)"),
    ("s03_jericho", "coins", "可是，大家都不喜欢撒该", 1, 0.0, "hit", "he snatches an extra coin (a sly grace)"),
    ("s03_jericho", "coins", "可是，大家都不喜欢撒该", 2, 0.0, "hit", "into his pouch (a plink)"),
    ("s04_crowd", "pop", "撒该心想", 0, 0.0, "hit", "a thought bubble opens (a xylophone pluck)"),
    ("s04_crowd", "pop", "撒该心想", 1, 0.0, "hit", "a big '?' in the bubble (a plucked question)"),
    ("s04_crowd", "whoosh", "他跳呀跳", 0, 0.0, "hit", "跳 1: a xylophone glissando up that falls back"),
    ("s04_crowd", "whoosh", "他跳呀跳", 1, 0.0, "hit", "跳 2: a xylophone glissando up that falls back"),
    ("s04_crowd", "thud", "他想挤进去", 0, 0.0, "hit", "the elbow bump (a thud)"),
    ("s04_crowd", "pop", "小朋友，你猜", 0, 0.0, "hit", "the first thinking dot rises (a soft xylophone note)"),
    ("s04_crowd", "pop", "小朋友，你猜", 2, 0.0, "hit", "the third thinking dot (the notes climb)"),
    ("s05_tree", "pop", None, 0, 0.0, "hit", "'有了！': the light bulb (the idea sting)"),
    ("s05_tree", "thud", "有了", 0, 0.0, "hit", "he screeches to a halt at the tree (a plucked stop)"),
    ("s05_tree", "sparkle", "那里有一棵大大的桑树", 0, 0.0, "hit", "the low branches glow (a glint)"),
    ("s05_tree", "cloth", "那里有一棵大大的桑树", 0, 0.0, "hit", "hands on the fork (a run up)"),
    ("s05_tree", "cloth", "撒该爬呀爬", 0, 0.0, "hit", "climbing stage 1 (a step up)"),
    ("s05_tree", "cloth", "撒该爬呀爬", 3, 0.0, "hit", "climbing stage 4 (a step up, on F7)"),
    ("s05_tree", "cloth", "撒该爬呀爬", 4, 0.0, "hit", "the hoist onto the sitting branch"),
    ("s05_tree", "cloth", "撒该爬呀爬", 4, 0.0, "change", "the hoist: B-flat at the top of the tree"),
    ("s05_tree", "cloth", "嘿嘿", 0, 0.0, "hit", "'嘿嘿': the twig pushed aside (a muted-trumpet giggle)"),
    ("s06_call", "whoosh", "他吓了一跳", 0, 0.0, "hit", "the jolt (a xylophone boing)"),
    ("s06_call", "sparkle", "他高兴极了", 0, 0.0, "hit", "both arms up, bouncing (a xylophone chord)"),
    ("s06_call", "thud", "他高兴极了", 0, 0.0, "hit", "he lands at the foot of the tree (a plucked plop)"),
    ("s08_promise", "cloth", None, 0, 0.0, "hit", "he stands up (a pluck)"),
    ("s08_promise", "thud", None, 0, 0.0, "hit", "he hops down (a soft thump)"),
    ("s08_promise", "sparkle", "主啊", 0, 0.0, "hit", "the money chest opens (a glint)"),
    ("s08_promise", "pop", "一半，就是", 0, 0.0, "hit", "the first card pops up (a pluck)"),
    ("s08_promise", "coins", "一半，就是", 0, 0.0, "hit", "ten coins drop in a row (a koto ripple of ten)"),
    ("s08_promise", "coins", "一半，就是", 1, 0.0, "hit", "two piles of five (two plucked chords)"),
    ("s08_promise", "coins", "一半，就是", 2, 0.0, "hit", "one pile to the poor (a harp glint)"),
    ("s08_promise", "sparkle", "一半，就是", 0, 0.0, "hit", "a heart for the poor (a glint)"),
    ("s08_promise", "pop", "四倍，就是", 0, 0.0, "hit", "the second card pops up (a pluck)"),
    ("s08_promise", "coins", "四倍，就是", 0, 0.0, "hit", "one coin (one low pluck)"),
    ("s08_promise", "pop", "四倍，就是", 1, 0.0, "hit", "the first of four coins pops out (four plucks climb)"),
    ("s09_saved", "sparkle", None, 0, 0.0, "hit", "Jesus smiles (a glint)"),
    ("s09_saved", "chime", None, 0, 0.0, "hit", "'救恩': the light fills the room (the radiant D major)"),
    ("s09_saved", "sparkle", "就是说", 0, 0.0, "hit", "a heart rises over him (a glint)"),
    ("s09_saved", "pop", "撒该想看看耶稣", 0, 0.0, "hit", "the picture of the tree pops up (a pluck)"),
    ("s09_saved", "sparkle", "撒该想看看耶稣", 0, 0.0, "hit", "the moonlit hills (a harp glint)"),
    ("s10_heart", "coins", None, 0, 0.0, "hit", "a coin for the widow (a koto pluck)"),
    ("s10_heart", "coins", None, 1, 0.0, "hit", "four coins for the farmer (a koto pluck)"),
    ("s10_heart", "sparkle", None, 0, 0.0, "hit", "a heart over Zacchaeus (a glint)"),
    ("s10_heart", "sparkle", None, 1, 0.0, "hit", "hearts over everyone (a glint)"),
    ("s11_end", "chime", "不管别人", 0, 0.0, "hit", "a heart pops up on '爱' (a glint)"),
    ("s11_end", "sparkle", "他也想住进你的心里", 0, 0.0, "hit", "the second heart on '心' (a glint)"),
    ("s11_end", "chime", "你想对他说什么呢", 0, 0.0, "hit", "the end card: the final F chord"),
]
