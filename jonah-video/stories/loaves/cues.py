"""The background score for 五饼二鱼 (John 6:1-14 / Mark 6:30-44; ~4:11) -- one continuous piece in 9 cues.

Read by audio/score.py when the story is "loaves" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework as the earlier scores (audio/scorekit.py,
audio/scorelib.py): every cue starts at its scene's global start, is planned in whole bars whose tempo follows the real
line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap), never to fixed times.  Hits that show an
on-screen action follow the PICTURE: picture() / pic() read the scene's own sound-effect cues at build time
(engine.loader.build_scene(...).sfx_cues) and pick them exactly as music_check picks a PICTURE_HITS target; hit() and
accent() put the attack wherever the cue falls, on tones of the chord sounding there; tune() puts a tune's notes on a
row of pops (the five loaves and two fish, the twelve friends, the tiny bites, the twelve baskets), climb() a climbing
pluck on each; lead() gives a moment's main attack to the picture when it falls inside that moment (the Amen's light,
the boy's smile).  A listed picture cue always gets its synced accent wherever it falls; only the extra gesture (a
sweep, the cadence) depends on where.  Fast rows (pops 0.13 s apart) sync only their well-separated ends: the onset
check cannot tell neighbours apart.  A scene that does not build falls back to the narrator's voice: syl() / span() /
chars() measure the punctuation groups in the recorded clip the way the scenes do (stories/noah/scenes/s01_title.py
voice_marks), scaled to the line's length in the timeline.  audio/music.py writes the chord at every moment to
harmony.json and audio/mix.py tunes the scenes' chimes, sparkles and grows to it, so the chord under every one of those
cues is a plain major or dominant chord where possible (a sus chord rings its bells a whole step lower; a minor chord
rings its relative major); mix.py also dips the music 8 dB under every name (耶稣, 门徒, 腓力, 安得烈, 牧羊人).

Colour: a warm, generous picnic on the hillside, unlike the nine earlier scores (Jonah's D-major sea, Daniel's Persian
court in A hijaz, David's G pipe tune, Noah's F hymn and B-flat march, Joseph's D clarinet, the Storm's Galilean
mixolydian folk, the Nativity's E-flat carols and music box, the Lost Sheep's A-major pastoral with whistle, mandolin and
accordion, Zacchaeus's B-flat street comedy).  Home key E major (no film has used it), mostly in a broad, rocking 6/8:
a singing solo cello (General MIDI Cello, not the section) for the hillside song -- Jesus's warmth and care -- over harp
and nylon-guitar arpeggios rocking up and down the chord, a soft hand drum (DUM . ta TUM . ta on the congas), an oboe
for worry and for the sheep without a shepherd, a flute for the sunset and the view from above, full strings and a horn
when the hillside fills and the baskets overflow.  The boy is a kalimba: a few bright, plucked notes, small at first,
that grow -- passed to the celesta, the harp, the guitar and the cello, multiplied in a round, and climbing into twelve
baskets.  The crowd's race along the shore is a quick 2/4 of running pizzicato, a shaker and claps against the boat's
long, gliding violin notes; Philip's worry and the tummies' rumble are on the bassoon (and a tuba).  The blessing is a
hush and a table-grace 'Amen' (A over E -> E, choir 'ooh' then 'aah', light only).  Under Jesus's own lines the cello
steps back (the harp carries the motif, the cello answers in the pause): a male voice and a cello share a register.
The modern frame (s02, s09) is a picnic in the park in A major: a mellow grand piano and a ukulele.  Four General MIDI
voices the shared orchestra does not list are registered here for this story only (_EXTRA): solo cello, kalimba,
ukulele (bank 8) and mellow grand piano (bank 8).  Every tune below is original; none opens with the rising 3-5-8 of the
earlier themes, the Lost Sheep's shepherd's song (mi fa sol do') and Zacchaeus's mi fa fi sol are avoided, and the
sheep without a shepherd get their own oboe phrase, no quotation.

Themes (q = quarter note)
  The boy (E, 6/8, kalimba; do mi re fa mi | sol -- do --: seven notes, his five loaves and two fish):
     b1 E A/C#   E5 G#5 F#5 A5 . G#5        b2 B7/D# E   B5 . . E5 . .
     (the bass climbs E C# D# E, so the cadence never doubles the tune in octaves).  The title, '今天的故事里' (s02);
     far off on the celesta when Jesus already knows (s04); the boy brought in, counted on the five loaves and two
     fish, counted again tiny, and handed to the cello -- Jesus's hands -- (s05); alone on the harp as Jesus takes the
     bread, passed on the guitar, multiplied in a round on the kalimba, the celesta and the harp (s07); counted in
     wonder on the celesta, and his smile (s08); counted tiny in A and multiplying on the kalimba (s09).
  The hillside song (E, 6/8, solo cello; the boy's five notes widened -- do sol fa la | sol . mi do | fa la sol fa |
     mi . re . | do sol fa la | do' . la sol | re fa mi re | do):
     b1 E A  E4 B4 A4 C#5     b2 E/G#  B4. G#4 E4     b3 A  A4 C#5 B4 A4     b4 E/B B7  G#4. F#4.
     b5 E A  E4 B4 A4 C#5     b6 C#m   E5. C#5 B4     b7 F#m7 B7  F#4 A4 G#4 F#4     b8 E  E4---
     Its head asks the frame's question on the piano in A (s02), opens the story on the cello (s02), sings love for the
     crowd (s03), answers '你们给他们吃吧' on the harp (s04) and '你们有多少饼' in A (s05), fills the hillside -- b1-b3 on
     the cello, b5-b8 in full strings, violins and horn (s06) -- the twelfth basket and the praise (s08), and the
     ending (s09: b1-b2, then b3 b4 b7 b8 home on '他也会照顾你').
  The twelve friends' walk (E, 2/4, oboe; do ti do mi | (twelve friends pop in) | sol fa mi re | re --), the busy tune
     (E, 2/4, flute; people coming and going in sixteenths) and the race (running pizzicato; the boat's long notes
     E4 ... D#4 ... F#4 on the violins; the flute running up past them) (s03).
  Counting games: twelve steps up the scale for the twelve friends (E5 ... B6, celesta and pizzicato, s03); four
     plucked steps that stall and a bassoon head-shake for Philip's fingers (s04); the boy's seven notes on the five
     loaves and two fish (s05, s08, s09); five tiny bites falling C#6 B5 A5 G#5 F#5 (s04); the leftovers gathered
     (pizzicato up the A chord) and twelve baskets -- a run up the scale A4 ... D#6 over B7 on the first eleven and the
     high E, the full cadence, on the twelfth (s08).

Cue table (scene: key / meter -- what the music does; picture hits in brackets)
  s01 title     E 6/8       the boy's theme on the kalimba over a harp roll, the guitar and the hand drum; sol held
                            as the title is read; the ta-da (do) on the finished title [the ribbon (a glint), the four
                            title characters (the celesta climbing), the basket's glow, the title's sparkle (ta-da, E)]
  s02 question  A 6/8 -> E  the picnic: the hillside head on the mellow piano over the ukulele, Bm7 E7sus4 hanging on
                            '分给好朋友？'; E on '今天的故事里' (change): the boy's theme on the kalimba; A on '可是，耶稣用这
                            一点点饭' (change): the hillside head on the cello; E on '让好多好多人都吃饱了' (change), a harp
                            sweep [the lunchbox opens (a pluck), the lunch (a glint), pops (harp), the half shared (a
                            pluck), the bite (a pizzicato crunch), both smile (a glint, the kalimba rolls)]
  s03 crowd     E 2/4 -> A 6/8 -> C#m/E 2/4 -> E 6/8 -> F#m -> A/E   the walk on the oboe with the twelve friends'
                            climb; busy, busy on '有一天' (change); the quiet place on '我们到安静的地方' (change: A, the
                            harp under Jesus, the cello answering); the boat glides; the deceptive C-sharp minor on '可是，
                            好多人看见了' (change): the race; the ta-da as '比船还先到了' ends (hit, change E); the cello's love;
                            the lone oboe on '他们就像一群没有牧羊人的羊' (change), hanging on B7sus4/F#; '耶稣就给大家讲上帝的事'
                            (change): the cello, healing glints [the twelve friends (first and last), the boat pushes off
                            (a harp sweep), the crowd sees them (a pluck), Jesus steps ashore (a harp note), his heart (a
                            glint), the flock (a harp note), the healing (a glint and the celesta)]
  s04 evening   E -> C#m 2/4 -> E -> G#7 -> A -> E -> C#m   the sunset on the flute; the rumble on '咕噜咕噜' (bassoon
                            and tuba wobbling on C-sharp, on the picture's bubbles); worry on '这里什么吃的都没有' (change:
                            oboe, tremolo, ticking pizzicato); E on '你们给他们吃吧' (change, the harp); G-sharp 7 on '门徒们吓了
                            一跳' (change) and the jolt; A on '耶稣又问腓力' (change), hanging on B7sus4; E on '耶稣这样问'
                            (change); the boy's theme far off on the celesta on '其实，耶稣自己早就知道' (change); Philip's
                            fingers on '腓力掰着手指' (change): plucked steps that stall, a head-shake; the bassoon's sigh on
                            '就算花好多好多钱买饼' (change) to G-sharp 7 [the jolt (whoosh), he already knows (a glint), the
                            money (a clink), five tiny bites (the celesta falling)]
  s05 boy       A -> F#m 2/4 -> E   the hillside head in A on the harp (the deceptive answer to Philip's G-sharp 7);
                            the search on '门徒们找啊找' (change), a ping on '这时候'; E on '彼得的兄弟安得烈' (change, a
                            strum): the boy's theme on the kalimba; the counting game on '这里有个小孩子' (change: A, then E
                            under the count); C-sharp minor on '可是，这么多人' (change), the oboe; '五个饼，两条鱼，只够'
                            (change): the count, tiny; '可是，小男孩把他带的饭' (change): his theme on the cello, home to E
                            [the five loaves and two fish (first, fifth, seventh), the lunch handed over (kalimba and
                            harp); the chime as Jesus takes it is accented but not listed (the scene's last half second)]
  s06 sit       E 6/8       harp, guitar and a flute bird for '叫大家都坐下来吧'; the hillside song on the cello on
                            '那里有好多青草' (change), the rows sitting down (harp and pizzicato, climbing, on the picture's
                            rustles); '有的一百个人一组' (change); the garden from above on '从高处看' (change: A, the flute
                            high over harp and celesta); the song in full strings, violins and horn on '光是男人' (change)
                            [a hundred (a big low chord), fifty (a light high chord), the view rises (a harp sweep), the
                            little gardens (a glint), the hillside fills (the celesta sweeps up), five thousand (a
                            timpani), a child (a kalimba ping)]
  s07 bless     E 6/8       the hush: the boy's theme alone on the harp; '抬头望着天' (change): high strings, a choir
                            'ooh' on A over E; the Amen on '感谢上帝' (change): E, choir 'aah', glockenspiel and harp on the
                            light; '然后，他把饼掰开' (change: A): the bread breaks (a harp cascade, a pizzicato chord), the
                            choir fading; '门徒再分给大家' (change): his five notes on the guitar, the fish on celesta and
                            pizzicato, to B7; the round on '分啊分' (change): his theme in canon over E and A/E, the kalimba,
                            the celesta a bar later, the harp a bar after that (the kalimba then a third higher), the
                            guitar and pizzicato joining; abundance
                            on '大家想吃多少' (change): la do' ti on the violins and cello, the horn, sweeps up A and B7 -- do'
                            arrives with the next page [he looks up (a glint), the light (the Amen), the bread breaks, the
                            shares (pizzicato climbing; first and fourth listed)]
  s08 baskets   E 6/8 -> A -> 2/4 -> E   do' resolves with the page, a contented bassoon (mi re do); A on '把剩下的碎块'
                            (change, the cello); '门徒们去收' (change): the gathering, the run, the twelfth basket's full
                            cadence (hit, change E); the hillside song in full strings and horn; wonder on '大家都好惊讶'
                            (change): the boy's seven notes on the celesta, hanging on B7sus4; the song on the horn on '大家
                            都说' (change), to a half cadence; his theme on the kalimba on '小男孩看着满满的篮子' (change)
                            [the twelfth basket (hit and change), the boy smiles (a glint)]
  s09 end       A 6/8 -> E  the frame: his seven notes in A on the kalimba (the picture's loaves and fish), three tiny
                            notes for '一点点', the ukulele and the piano; E on '可是在耶稣手里' (change): the hillside song
                            on the cello, the kalimba climbing as it multiplies; '耶稣看见大家饿了' (change): the song home
                            on '他也会照顾你'; A on '小朋友，你有什么好东西' (change), very soft; B7sus4 at the end of the question
                            (change), hanging through the answer pause (the kalimba asks once); the final E chord on the
                            end card [the first loaf and second fish, in Jesus's hands (a glint), it multiplies (first and
                            last), he will care for you (a glint), the end card]

All the music stays under the narration (Seg.duck, low expression levels, melodies ducked further, accompaniment
figures thinned to the beats while a line is spoken); melodic entrances at segment starts are eased in (ease()); the
loud moments (the ta-da, the race's arrival, a hundred, five thousand, the twelfth basket) live in the pauses or on
the picture, short and child-safe; the worry stays gentle and the rumble comic.
"""
import numpy as np

from audio.scorekit import PARTS, Part
from audio.scorelib import ChordTones, bassline, broken, drum, gliss, span_end
from audio.theory import midi

# ------------------------------------------------------------------------------------------- this film's colours
# General MIDI voices the shared orchestra (audio/scorekit.PARTS) does not list; registered here, for this story only,
# before any cue is written (the MIDI writer, the checks and the bus channel count read PARTS).
_EXTRA = [
    Part("cello", 0, 42, "str_lo", 0.18, -3, 36, 76, attack=0.08, legato=0.04, jitter=0.009, duck_db=2.5),
    Part("kalimba", 0, 108, "keys", -0.12, -1, 57, 96, jitter=0.006, duck_db=2.0),
    Part("uke", 8, 24, "pluck", -0.22, -4, 55, 84, jitter=0.008, duck_db=2.0),
    Part("mpiano", 8, 0, "keys", 0.06, -3, 36, 96, jitter=0.007, duck_db=2.0),
]
for _p in _EXTRA:
    PARTS.setdefault(_p.name, _p)

# ------------------------------------------------------------------------------------------- themes (q = quarter)
# the boy's theme (E, 6/8): do mi re fa mi | sol -- do -- : five notes and two, his five loaves and two fish
BOY = ["E5:1/2 G#5:1/2 F#5:1/2 A5:1 G#5:1/2", "B5:3/2 E5:3/2"]
BOY_PROG = ["E:3/2 A/C#:3/2", "B7/D#:3/2 E:3/2"]
BOY_NOTES = ["E5", "G#5", "F#5", "A5", "G#5", "B5", "E5"]
# the hillside song (E, 6/8): the boy's five notes widened -- do sol fa la | sol . mi do | fa la sol fa | mi . re . |
# do sol fa la | do' . la sol | re fa mi re | do
HILL = ["E4:1 B4:1/2 A4:1 C#5:1/2", "B4:3/2 G#4:1 E4:1/2", "A4:1 C#5:1/2 B4:1 A4:1/2", "G#4:3/2 F#4:3/2",
        "E4:1 B4:1/2 A4:1 C#5:1/2", "E5:3/2 C#5:1 B4:1/2", "F#4:1 A4:1/2 G#4:1 F#4:1/2", "E4:3"]
HILL_PROG = ["E:3/2 A:3/2", "E/G#:3", "A:3", "E/B:3/2 B7:3/2", "E:3/2 A:3/2", "C#m:3", "F#m7:3/2 B7:3/2", "E:3"]
# the twelve friends' walk (E, 2/4): do ti do mi | fa mi fa la | sol fa mi re | do
WALK = ["E5:1/2 D#5:1/2 E5:1/2 G#5:1/2", "A5:1/2 G#5:1/2 A5:1/2 C#6:1/2", "B5:1/2 A5:1/2 G#5:1/2 F#5:1/2",
        "F#5:2"]
WALK_PROG = ["E:2", "A:2", "E/B:1 B7:1", "B7:2"]
# busy, busy (E, 2/4): people coming and going
BUSY = ["E5:1/4 F#5:1/4 G#5:1/4 E5:1/4 B5:1/2 G#5:1/2", "A5:1/4 G#5:1/4 F#5:1/4 A5:1/4 C#6:1/2 A5:1/2",
        "B5:1/4 A5:1/4 G#5:1/4 F#5:1/4 D#5:1/2 F#5:1/2", "E5:1/2 B4:1/2 E5:1/2 r:1/2",
        "E5:1/4 F#5:1/4 G#5:1/4 E5:1/4 B5:1/2 G#5:1/2", "C#6:1/4 B5:1/4 A5:1/4 B5:1/4 G#5:1/2 E5:1/2",
        "F#5:1/4 A5:1/4 C#6:1/4 A5:1/4 B5:1/2 D#5:1/2", "E5:1/2 G#5:1/4 F#5:1/4 E5:1/2 r:1/2"]
BUSY_PROG = ["E:2", "A:2", "B7:2", "E:2", "E:2", "C#m:2", "F#m7:1 B7:1", "E:2"]


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


def span(c, phrase):
    """(start, end) of the punctuation group that holds `phrase`, as the speaker says it (cue-relative)."""
    i = c.find(phrase)
    ln = c.scene["lines"][i]
    k0 = ln["text"].index(phrase)
    units = _groups(ln["text"])
    u0 = max(k for k, (p, _) in enumerate(units) if p <= k0)
    vg = _voice_groups(c, i)
    if len(vg) == len(units):
        return vg[u0][1], vg[u0][2]
    p0, g0 = units[u0]
    return _char_time(ln, p0), _char_time(ln, p0 + len(g0))


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


def accent(c, segs, t, what=None, glock=None, celesta=None, kal=None, harp=None, pluck=None, guitar=None, low=None,
           block=None, vel=46):
    """A picture hit at cue-relative time t on tones of the chord sounding there (glock / celesta / kalimba / harp /
    pizzicato / guitar = (lo, hi) ranges: the highest chord tone in range; low=True: a soft low thump; block: a hand
    drum key); synced if `what`."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if celesta:
        sg.add("celesta", q, _dq(sg, q, 0.75), top(sg, q, *celesta), vel, "arp", "h")
    if kal:
        sg.add("kalimba", q, _dq(sg, q, 0.75), top(sg, q, *kal), vel + 2, "arp", "h")
    if harp:
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, *harp), vel, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if guitar:
        sg.add("guitar", q, _dq(sg, q, 0.5), top(sg, q, *guitar), vel + 2, "arp", "h")
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


def climb(c, segs, times, part="celesta", lo=69, hi=94, vel=40, sync=(), what="", glock=True, pz=False):
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


def follow(c, segs, name, t0, t1, skip=(), what=None, sync=(), **kw):
    """Every picture cue `name` between cue-relative t0 and t1 (except times in `skip`) gets a soft accent on the
    chord sounding there (accent() kwargs); those whose index is in `sync` are synced as `what (k)`.  Returns the
    times."""
    out = []
    for k, t in enumerate(pics(c, name, t0, t1)):
        if any(abs(t - s_) < 0.05 for s_ in skip):
            continue
        clear_near(c, t)
        accent(c, segs, t, f"{what} ({k + 1})" if what and k in sync else None, **kw)
        out.append(t)
    return out


def tune(c, segs, times, notes, part="kalimba", vel=44, role="fx", art="", what=None, sync=(), glock=None,
         clear=True, last=1.0):
    """A tune whose notes fall at given cue-relative times (the picture's pops, or the narrator's syllables): each note
    held until the next one (the last for a quarter); those whose index is in `sync` are synced as `what (k)`;
    glock: double the notes two octaves up (or one) on the glockenspiel at those indices."""
    out = []
    for k, (t, nm) in enumerate(zip(times, notes)):
        sg, q = seg_at(c, segs, t)
        if k + 1 < len(times):
            sg2, q2 = seg_at(c, segs, times[k + 1])
            dq = (q2 - q) if sg2 is sg else (sg.n_q - q)
        else:
            dq = last
        dq = max(0.1, min(dq, sg.n_q - q))
        p = midi(nm) if isinstance(nm, str) else nm
        if clear:
            clear_near(c, t, win=0.1)
        out.append(sg.add(part, q, dq, p, vel + (6 if k in sync else 0), role, art or ("h" if k in sync else "")))
        if glock is not None and k in glock:
            g = p + 24 if p + 24 <= 105 else p + 12
            sg.add("glock", q, _dq(sg, q, 0.5), g, vel - 10, "arp", "h")
        if what and k in sync:
            sg.sync(f"{what} ({k + 1})", q, t)
    return out


# ------------------------------------------------------------------------------------------- writing helpers
STR = ["vla", "vln2", "vln1", "vc", "cb"]


def lv(seg, parts, a, b=None, q0=0.0, q1=None):
    """Flat expression (dB) for parts over the segment (or q0..q1), a -> b."""
    seg.expr(parts, [(q0, a), (seg.n_q if q1 is None else q1, a if b is None else b)])


def ease(seg, parts, a, drop=6.0, over=1.0, b=None):
    """An entrance eased in: parts start `drop` dB under their level a and reach it after `over` q (then a -> b to the
    segment's end), so a new tune at a segment start does not jump out."""
    seg.expr(parts, [(0.0, a - drop), (min(over, seg.n_q), a), (seg.n_q, a if b is None else b)])


def strings(seg, vel=40, lo=50, hi=69, bass=(40, 52), q0=0.0, q1=None, cb=(28, 40), cb_vel=None):
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


def sweep(seg, q, dur_s=0.6, lo="E4", hi="E6", v0=30, v1=46, up=True, part="harp"):
    """A glissando (harp, celesta, kalimba) over the chord at q."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1, scale=ChordTones(seg.chord_at(q + 1e-3)))


def scale_run(seg, q, dur_s=0.45, lo="E5", hi="E6", v0=30, v1=44, up=True, part="flute"):
    """A run up (or down) the segment's scale."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1)


def roll_chord(seg, q, lo, hi, vel=46, gap_s=0.05, part="harp", n=6):
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


def strum(seg, q, lo, hi, vel=40, part="guitar", gap_s=0.03, n=5, down=True, dq=None, art=""):
    """A quick strum of the chord at q (n tones in [lo, hi], low to high or high to low)."""
    ts = seg.chord_at(q + 1e-3).tones(lo, hi)
    picked = []
    for p in ts:
        if not picked or p - picked[-1] >= 3:
            picked.append(p)
    picked = picked[:n]
    if not down:
        picked = picked[::-1]
    t0 = seg.t(q)
    end = span_end(seg, q + 1e-6) if dq is None else min(q + dq, span_end(seg, q + 1e-6))
    for k, p in enumerate(picked):
        qk = seg.q_of(t0 + gap_s * k)
        if qk >= end - 0.05:
            break
        seg.add(part, qk, end - qk, p, vel - k, "arp", art)


def _alt_bass(ch, lo, hi):
    """The chord's other bass note: its fifth (or its root under an inversion) near the bass."""
    b0 = ch.bass_note(lo, hi)
    for pc_ in ((ch.root + 7) % 12, ch.root):
        cand = [p for p in range(lo, hi + 6) if p % 12 == pc_ and p != b0]
        if cand:
            return min(cand, key=lambda p: abs(p - b0))
    return b0


def oom(seg, q0, q1, vel=40, bass=(40, 52), hi=(56, 68), n=3, bpart="pz_lo", cpart="guitar"):
    """A walking oom-pah (2/4): a plucked bass on every beat (the chord's bass, then its fifth while the chord stays),
    the chord on the off-beat."""
    beat = seg.beat_q
    q, k, last = q0, 0, None
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        k = 0 if ch is not last else k + 1
        p = ch.bass_note(*bass) if k % 2 == 0 else _alt_bass(ch, *bass)
        seg.add(bpart, q, _dq(seg, q, beat * 0.6), p, vel, "arp", "s")
        qq = q + beat / 2
        if qq < q1 - 1e-6 and cpart:
            for pt in seg.chord_at(qq + 1e-3).tones(*hi)[:n]:
                seg.add(cpart, qq, _dq(seg, qq, 0.25), pt, vel - 8, "arp", "s")
        last = ch
        q += beat


def rock(seg, q0, q1, part="harp", lo=40, hi=64, vel=32, pat=(0, 2, 4, 2, 4, 2), thin=True, ring=True):
    """The hillside's rocking 6/8 arpeggio (harp or guitar): six eighths up and down the chord from its bass; only the
    beats while a line is spoken (thin)."""
    broken(seg, part, q0, q1, pat, lo, hi, vel=vel, step=0.5, thin=thin, ring=ring)


def hdrum(seg, q0, q1, vel=30, light=True):
    """The soft hand drum: 6/8 DUM . ta TUM . ta (a low conga on the dotted-quarter beats, a muted high conga on the
    third and sixth eighths, an open one on the second beat); 2/4 DUM ta TUM ta; the 'ta's only in the pauses when
    light."""
    pat = ((0.0, 64, 0, False), (1.0, 62, -12, True), (1.5, 63, -6, False), (2.5, 62, -12, True)) \
        if seg.meter == "6/8" else ((0.0, 64, 0, False), (0.5, 62, -12, True), (1.0, 63, -6, False),
                                    (1.5, 62, -12, True))
    bar = seg.bar_q
    sc = seg.score
    for b in range(int(q0 // bar), int(np.ceil(q1 / bar - 1e-9))):
        for off, key, dv, lt in pat:
            q = b * bar + off
            if not (q0 - 1e-6 <= q < q1 - 1e-6):
                continue
            if lt and light and bool(sc.speaking(seg.t(q))):
                continue
            drum(seg, q, key, vel + dv)


def claps(seg, q0, q1, vel=30, offs=(1.0,)):
    """Hand-claps (beat 2 of the 2/4 bar, or the given off-sets) in the pauses only."""
    b = int(q0 // 2.0)
    while b * 2.0 < q1 - 1e-6:
        for off in offs:
            q = b * 2.0 + off
            if q0 - 1e-6 <= q < q1 - 1e-6 and not bool(seg.score.speaking(seg.t(q))):
                drum(seg, q, 39, vel)
        b += 1


def feet(seg, q0, q1, vel=34, lo=52, hi=71, step=0.5, rise=0):
    """Running feet: staccato pizzicato on every `step` q, the chord's bass on the beat and its upper tones between
    (climbing `rise` semitones over the span)."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        r = int(round(rise * (q - q0) / max(1e-6, q1 - q0)))
        on_beat = abs((q + 1e-6) % seg.beat_q) < 2e-6
        if on_beat:
            seg.add("pz_lo", q, _dq(seg, q, step), ch.bass_note(40, 52), vel, "arp", "s")
        else:
            ts = ch.tones(lo + r, hi + r)
            seg.add("pz_hi", q, _dq(seg, q, step), ts[k % len(ts)], vel - 4, "arp", "S")
        q += step
        k += 1


def run(seg, part, q0, notes, step, vel=40, role="melody", art=""):
    """A quick run: the given pitches, one every `step` q from q0."""
    out = []
    for k, nm in enumerate(notes):
        q = q0 + k * step
        if q < seg.n_q - 1e-6:
            out.append(seg.add(part, q, min(step, seg.n_q - q), nm, vel + k, role, art))
    return out


def trem(seg, part, q0, q1, pitch, vel, rate=0.125, role="arp", alt=None):
    """A plucked tremolo: the same note re-struck every `rate` q (alternating with `alt`)."""
    pitch = midi(pitch) if isinstance(pitch, str) else pitch
    alt = midi(alt) if isinstance(alt, str) else alt
    q, k = q0, 0
    while q < q1 - 1e-6:
        p = alt if (alt is not None and k % 2) else pitch
        seg.add(part, q, min(rate, q1 - q), p, vel + (3 if k % 2 == 0 else -3), role)
        q += rate
        k += 1


def pick_times(times, lo, hi, n=None):
    out = [t for t in (times or []) if lo <= t <= hi]
    return out[:n] if n else out


def spread(t0, t1, n):
    """n times evenly from t0 to t1 (both included)."""
    if n <= 1:
        return [t0]
    return [t0 + (t1 - t0) * k / (n - 1) for k in range(n)]


def count_times(c, phrase, ch_list, t_lo, t_hi):
    """Times of the narrator's syllables `ch_list` (characters of the line with `phrase`, in order), kept inside
    [t_lo, t_hi] and at least 0.08 s apart."""
    out, used = [], {}
    for ch in ch_list:
        ts = chars(c, phrase, ch)
        k = used.get(ch, 0)
        used[ch] = k + 1
        if k < len(ts):
            out.append(ts[k])
    out = [min(max(t, t_lo), t_hi) for t in out]
    for k in range(1, len(out)):
        out[k] = max(out[k], out[k - 1] + 0.08)
    return out


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """The title (E, 6/8): the boy's theme on the kalimba over a harp roll, the guitar and the hand drum -- do mi re fa mi,
    and sol held as the title is read -- the ta-da (do: kalimba, glockenspiel, harp, pizzicato) on the finished title's
    sparkle; a glint for the ribbon, the celesta climbing as the four title characters pop in."""
    c.gain(-6.0)
    t_sp = pic(c, "sparkle", None, 1)
    t_fb = c.le(0) + 0.15
    t_td = t_sp if t_sp is not None and c.le(0) - 0.5 <= t_sp <= c.dur - 1.0 else min(t_fb, c.dur - 1.0)
    s = c.seg(0, t_td, 2, "6/8", "E major", nominal=None, label="title-boy")
    d = c.seg(t_td, c.dur, 1, "6/8", "E major", nominal=None, label="title-tada")
    segs = (s, d)
    for sg in segs:
        sg.duck(1.5)
    s.duck(3.0, parts=["kalimba"])
    s.prog("E:3/2 A:3/2 | B7:3")
    d.prog("E:3")
    d.sync("ta-da: the finished title (E)" + (" (picture)" if t_sp is not None else ""), 0, t_td, kind="change")
    # the boy's theme: do mi re fa mi | sol --- (held as the title is read)
    s.mel("kalimba", "E5:1/2 G#5:1/2 F#5:1/2 A5:3/2 | B5:3", vel=50)
    roll_chord(s, 0.0, 45, 68, vel=30, part="harp", n=4)
    rock(s, 1.5, 6.0, part="guitar", lo=40, hi=64, vel=30)
    s.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    hdrum(s, 1.5, 6, vel=28)
    sweep(s, 4.5, 0.5, "B4", "B6", 24, 34, part="harp")             # the fish note rises into the ta-da
    # ta-da: do -- kalimba (E5 + E6), glockenspiel, harp rolled, pizzicato chord, a soft low conga
    for nm in ("E5", "E6"):
        d.add("kalimba", 0, 1.5, nm, 50, "arp", "h")
    d.add("glock", 0, 1.5, "G#6", 40, "arp", "h")
    for nm in ("E3", "B3", "G#4"):
        d.add("pz_lo" if nm == "E3" else "pz_hi", 0, 0.5, nm, 44, "arp", "h")
    d.add("pz_cb", 0, 0.5, "E2", 44, "bass", "h")
    roll_chord(d, 0.1, 52, 83, vel=36, part="harp", n=5)
    d.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    drum(d, 0, 64, 30)
    d.sync("ta-da: the finished title" + (" (picture)" if t_sp is not None else ""), 0, t_td)
    # the picture: the ribbon (a glint); the four title characters pop in (the celesta climbing)
    hit(c, segs, "chime", None, 0, "the ribbon unfurls (a glint)", glock=(86, 98), harp=(76, 88), vel=48)
    pops = pick_times(pics(c, "pop"), 0.3, t_td - 0.1)
    if pops:
        for t_ in pops:
            clear_near(c, t_)
        climb(c, segs, pops, part="celesta", lo=83, hi=98, vel=38, sync=(0, len(pops) - 1),
              what="a title character pops in", glock=False)
    t_bs = pic(c, "sparkle", None, 0)
    if t_bs is not None and t_bs < t_td - 0.15:                 # the basket glows (a soft glint)
        accent(c, segs, t_bs, None, glock=(86, 98), vel=32)
    for sg in segs:
        lv(sg, ["kalimba"], -13)
        lv(sg, ["harp"], -15)
        lv(sg, ["guitar"], -17)
        lv(sg, "hand", -20)
        lv(sg, ["pz_hi", "pz_cb"], -13)
        lv(sg, ["glock", "celesta"], -14)
    s.expr(["vla", "vln1", "vc"], [(0, -27), (1.5, -24), (6, -23)])
    d.expr(["vla", "vln1", "vc"], [(0, -22), (3, -22)])


def question(c):
    """The modern frame (A major, 6/8): a picnic in the park -- a mellow piano over the ukulele's strum and soft strings;
    the hillside song's head on the piano asks '分给好朋友？' (Bm7 E7sus4 hanging through the pause); E major on '今天的
    故事里' (change): the boy's theme, small, on the kalimba; A on '可是，耶稣用这一点点饭' (change): the hillside song's
    head on the cello; E on '让好多好多人都吃饱了' (change): the song's second bar, a harp sweep, and the kalimba rolling
    up as the children smile (the picture), blooming into the page turn."""
    c.gain(-4.5)
    t_today = c.ls(c.find("今天的故事里"))
    t_but = c.at("可是，耶稣用这一点点饭")
    t_many = c.at("让好多好多人都吃饱了")
    a = c.seg(0, t_today, 2, "6/8", "A major", nominal=66, label="question-share")
    t = c.seg(t_today, t_but, 2, "6/8", "E major", nominal=76, label="question-today")
    b = c.seg(t_but, t_many, 1, "6/8", "E major", nominal=None, label="question-but")
    m = c.seg(t_many, c.dur, 1, "6/8", "E major", nominal=None, label="question-many")
    segs = (a, t, b, m)
    for sg in segs:
        sg.duck(1.5)
    a.prog("A:3/2 D:3/2 | Bm7:3/2 E7sus4:3/2")
    t.prog(" | ".join(BOY_PROG))
    b.prog("A:3")
    m.prog("E:3")
    t.sync("'今天的故事里': the story begins (E)", 0, t_today, kind="change")
    b.sync("'可是，耶稣用这一点点饭' (A)", 0, t_but, kind="change")
    m.sync("'让好多好多人都吃饱了': E", 0, t_many, kind="change")
    # 'child, have you ever shared something yummy with a friend?': the piano, the ukulele, soft strings
    a.mel("mpiano", "A4:1 E5:1/2 D5:1 F#5:1/2 | D5:3/2 E5:3/2", vel=46)
    for q_ in (0.0, 1.5, 3.0, 4.5):                       # the ukulele: down . up down . up
        strum(a, q_, 57, 76, vel=34, part="uke", n=4, dq=1.0)
        if not bool(a.score.speaking(a.t(q_ + 1.0))):
            strum(a, q_ + 1.0, 57, 76, vel=28, part="uke", n=3, down=False, dq=0.5)
    a.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=38, bass_hi=50)
    a.duck(2.5, parts=["mpiano"])
    a.expr(["mpiano"], [(0, -20), (1.5, -14), (6, -13)])
    a.expr(["uke"], [(0, -24), (1.5, -16), (6, -15)])
    a.expr(["vla", "vln1", "vc"], [(0, -26), (2, -23), (6, -22)])
    # 'today's story has a little boy who brought only a little lunch': the boy's theme on the kalimba (E)
    t.mel("kalimba", bars(BOY, 0, 2), vel=46)
    rock(t, 0, 6, part="harp", lo=40, hi=64, vel=28)
    t.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=28, bass_ref=(40, 52))
    bassline(t, "vc", 40, 52, 28)
    t.duck(2.5, parts=["kalimba"])
    ease(t, ["kalimba"], -14)
    lv(t, ["harp"], -17)
    t.expr(["vla", "vln1", "vc"], [(0, -24), (6, -22)])
    # 'but with this little lunch Jesus ...': the hillside song's head on the cello
    b.mel("cello", HILL[0], vel=48)
    rock(b, 0, 3, part="harp", lo=40, hi=64, vel=28)
    b.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=28, bass_ref=(40, 52))
    bassline(b, "vc", 40, 52, 28)
    b.duck(2.5, parts=["cello"])
    b.expr(["cello"], [(0, -21), (1.0, -15), (3, -15)])
    lv(b, ["harp"], -17)
    b.expr(["vla", "vln1", "vc"], [(0, -24), (3, -22)])
    # '... filled ever so many people!': E -- the song's second bar, a harp sweep, strings opening out
    m.mel("cello", HILL[1], vel=46)
    strings(m, vel=32, lo=52, hi=74, bass=(40, 52), cb=(28, 40))
    sweep(m, 0.05, 0.6, "E4", "E6", 24, 36, part="harp")
    m.duck(2.5, parts=["cello"])
    lv(m, ["cello"], -16)
    lv(m, ["harp"], -16)
    lv(m, ["kalimba"], -17)
    m.expr(STR, [(0, -25), (1.5, -22), (3, -23)])
    # the picture: the lunchbox opens (a pluck and a glint), the friend, the half shared, the bite, the smile
    hit(c, segs, "cloth", None, 0, "the lunchbox opens (a soft pluck)", pluck=(60, 72), vel=36)
    hit(c, segs, "sparkle", None, 0, "the lunch inside (a glint)", glock=(86, 98), vel=36)
    follow(c, segs, "pop", 0.3, c.dur - 0.3, harp=(71, 83), glock=(86, 98), vel=30)
    hit(c, segs, "crunch", None, 0, "a bite (a pizzicato crunch)", win=0.25, pluck=(60, 72), guitar=(52, 64),
        harp=(64, 76), vel=50)
    hit(c, segs, "sparkle", None, 1, "a glint", glock=(86, 98), vel=34)
    hit(c, segs, "cloth", None, 1, "the half is shared (a pluck)", pluck=(60, 72), kal=(76, 88), harp=(64, 76), vel=44)
    t_sm = hit(c, segs, "chime", None, 0, "both smile (a glint)", glock=(86, 98), kal=(76, 91), vel=40)
    sg_, q_sm = seg_at(c, segs, t_sm if t_sm is not None else m.t(1.5) - c.t0)
    roll_chord(sg_, q_sm + 0.08, 64, 88, vel=28, part="kalimba", n=4)
    for sg in segs:
        lv(sg, ["glock", "celesta"], -14)
        lv(sg, ["pz_hi"], -14)


def crowd(c):
    """Busy days (E, 2/4) -> the quiet place (A, 6/8) -> the race along the shore (C-sharp minor -> E, 2/4) -> love
    (E, 6/8) -> sheep without a shepherd (F-sharp minor) -> teaching and healing (A -> E).  The twelve friends' walk on
    the oboe over the guitar's oom-pah and the hand drum, the twelve popping in as twelve steps up the scale (celesta
    and pizzicato); busy, busy on '有一天' (change): the flute's chatter, pizzicato, claps; '我们到安静的地方' (change): A
    major, the harp under Jesus's line, the cello answering in the pause; the boat glides (a harp sweep as it pushes off,
    the violins); the deceptive C-sharp minor on '可是，好多人看见了' (change): running pizzicato feet, a shaker, claps,
    the boat's long notes on the violins; the feet climb and the flute runs up past them, and the E ta-da lands as
    '比船还先到了' ends (hit); the hillside song on the cello, tender, on '耶稣下了船'; a lone oboe over a drone on
    '他们就像一群没有牧羊人的羊' (change), hanging on B7sus4/F#; '耶稣就给大家讲上帝的事' (change): the cello, healing glints
    on the picture's chime and sparkle, a celesta sweep on '还把生病的人都治好了'."""
    c.gain(-3.5)
    t_busy = c.gap(c.find("有一天"))
    t_rest = c.gap(c.find("我们到安静的地方"))
    t_saw = c.at("可是，好多人看见了")
    i_run = c.find("比船还先到了")
    t_arr = c.le(i_run)
    t_sheep = c.at("他们就像一群没有牧羊人的羊")
    t_heal = c.gap(c.find("耶稣就给大家讲上帝的事"))
    w = c.seg(0, t_busy, 4, "2/4", "E major", nominal=104, label="crowd-friends")
    b = c.seg(t_busy, t_rest, 8, "2/4", "E major", nominal=128, label="crowd-busy")
    r = c.seg(t_rest, t_saw, 3, "6/8", "E major", nominal=76, label="crowd-rest")
    n = c.seg(t_saw, t_arr, 10, "2/4", "E major", nominal=150, label="crowd-run")
    lov = c.seg(t_arr, t_sheep, 2, "6/8", "E major", nominal=66, label="crowd-love")
    sh = c.seg(t_sheep, t_heal, 2, "6/8", "E major", nominal=78, label="crowd-sheep")
    h = c.seg(t_heal, c.dur, 2, "6/8", "E major", nominal=70, label="crowd-heal")
    segs = (w, b, r, n, lov, sh, h)
    for sg in segs:
        sg.duck(1.5)
    w.prog(" | ".join(WALK_PROG))
    b.prog(" | ".join(BUSY_PROG))
    r.prog("A:3 | E/G#:3 | F#m7:3/2 B7sus4:3/2")
    n.prog("C#m:2 | A:2 | E:2 | B7:2 | E:2 | A:2 | E:2 | A:2 | F#m7:2 | B7:2")
    lov.prog("E:3/2 A:3/2 | E/G#:3")
    sh.prog("F#m:3 | B7sus4/F#:3")
    h.prog("A:3/2 B7:3/2 | E:3")
    b.sync("'有一天': busy, busy (E)", 0, t_busy, kind="change")
    r.sync("'我们到安静的地方': the quiet place (A)", 0, t_rest, kind="change")
    n.sync("'可是，好多人看见了': the crowd sees them (C-sharp minor)", 0, t_saw, kind="change")
    lov.sync("'比船还先到了': they got there first! (E)", 0, t_arr, kind="change")
    sh.sync("'他们就像一群没有牧羊人的羊': sheep without a shepherd (F-sharp minor)", 0, t_sheep, kind="change")
    h.sync("'耶稣就给大家讲上帝的事': teaching (A)", 0, t_heal, kind="change")
    # 'Jesus had twelve good friends, called disciples': the walk on the oboe (a call, and an answer left open), the
    # guitar's oom-pah, the hand drum; between them the twelve friends pop in -- twelve steps up the scale on the
    # celesta and pizzicato (the picture's pops, or spread over '十二个好朋友')
    w.mel("oboe", WALK[0] + " | r:2 | r:2 | " + WALK[3], vel=48)
    i_tw = c.find("耶稣有十二个好朋友")
    twelve = pick_times(pics(c, "pop"), c.ls(i_tw) - 0.3, c.le(i_tw) + 0.3)
    on_pic = len(twelve) >= 12
    if on_pic:
        twelve = twelve[:12]
    else:
        g0, g1 = span(c, "耶稣有十二个好朋友")
        twelve = spread(g0 + 0.25 * (g1 - g0), g1, 12)
    if not on_pic:
        twelve = [t_ for t_ in twelve if w.t(1.0) - c.t0 <= t_ <= w.t(6.4) - c.t0]
    steps12 = ["E5", "F#5", "G#5", "A5", "B5", "C#6", "D#6", "E6", "F#6", "G#6", "A6", "B6"]
    if twelve:
        tune(c, segs, twelve, steps12[:len(twelve)], part="celesta", vel=40, role="fx", art="", last=0.5,
             what="a friend pops in" + (" (picture)" if on_pic else ""), sync=(0, len(twelve) - 1) if on_pic else (),
             glock=(0, len(twelve) - 1) if len(twelve) == 12 else None)
        tune(c, segs, twelve, [midi(x) - 12 for x in steps12[:len(twelve)]], part="pz_hi", vel=36, role="fx",
             art="S", last=0.5, clear=False)
    oom(w, 0, 8, vel=34, bass=(40, 52), hi=(56, 68), cpart="guitar")
    hdrum(w, 0, 8, vel=28)
    w.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_ref=(40, 52))
    w.duck(3.0, parts=["oboe"])
    w.expr(["oboe"], [(0, -20), (1, -16), (8, -16)])
    lv(w, ["pz_lo"], -14)
    lv(w, ["guitar"], -18)
    lv(w, "hand", -21)
    lv(w, ["celesta"], -19)
    lv(w, ["pz_hi"], -17)
    lv(w, ["glock"], -18)
    w.expr(["vla", "vln1"], [(0, -27), (8, -26)])
    # 'one day they were so busy, no time even to eat': busy, busy
    b.mel("flute", bars(BUSY, 0, 8), vel=44)
    oom(b, 0, 16, vel=34, bass=(40, 52), hi=(56, 68), cpart="guitar")
    hdrum(b, 0, 16, vel=28)
    claps(b, 0, 16, vel=28, offs=(1.0,))
    b.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_ref=(40, 52))
    b.duck(4.5, parts=["flute"])
    b.expr(["flute"], [(0, -21), (1, -17), (16, -17)])
    lv(b, ["pz_lo"], -14)
    lv(b, ["guitar"], -18)
    lv(b, "hand", -21)
    b.expr(["vla", "vln1"], [(0, -27), (16, -26)])
    # 'let's go to a quiet place and rest a while': A major, the harp, the cello; the boat glides off (E)
    r.mel("harp", "C#5:3/2 B4:1 A4:1/2 | B4:3/2 r:3/2", vel=38)
    r.mel("cello", "r:3 | r:3/2 G#3:1 E3:1/2 | F#3:3/2 r:3/2", vel=46)
    rock(r, 0, 9, part="harp", lo=40, hi=59, vel=28)
    strings(r, vel=30, lo=52, hi=71, bass=(40, 52), cb=None)
    r.mel("vln_mel", "r:6 | E5:3/2 F#5:3/2", vel=34, role="counter")
    t_boat = pic(c, "splash_small", "他们坐船", 0)
    if t_boat is not None:                                  # the boat pushes off: a harp sweep
        clear_near(c, t_boat, win=0.25, roles=("arp", "perc"))
        sg_, q_bt = accent(c, segs, t_boat, "the boat pushes off (a harp sweep)", harp=(52, 64), pluck=(57, 69),
                           glock=(86, 98), vel=48)
        sweep(sg_, q_bt + 0.05, 0.7, "E4", "E6", 24, 34, part="harp")
    r.duck(2.5, parts=["cello", "vln_mel"])
    ease(r, ["cello"], -16)
    lv(r, ["vln_mel"], -21)
    ease(r, ["harp"], -16)
    r.expr(STR, [(0, -24), (9, -23)])
    # 'but lots of people saw them, and ran and ran along the shore -- and got there before the boat!'
    feet(n, 0, 12, vel=36, lo=56, hi=71, step=0.5)
    feet(n, 12, 20, vel=38, lo=59, hi=76, step=0.25, rise=7)
    for q_ in np.arange(0, 20, 0.5):                         # a shaker for the feet
        drum(n, q_, 70, 26 if abs(q_ % 1.0) < 1e-6 else 20)
    claps(n, 0, 20, vel=28, offs=(1.0,))
    hdrum(n, 0, 20, vel=26)
    n.mel("vln_mel", "E4:2 | E4:2 | E4:2 | D#4:2 | E4:2 | E4:2 | E4:2 | E4:2 | F#4:2 | F#4:2", vel=34,
          role="counter")
    n.mel("flute", "r:2 | r:2 | r:2 | r:2 | E5:1/2 G#5:1/2 B5:1/2 G#5:1/2 | A5:1/2 C#6:1/2 E6:1/2 C#6:1/2 | "
                   "B5:1/4 C#6:1/4 B5:1/4 A5:1/4 G#5:1/2 B5:1/2 | C#6:1/4 B5:1/4 A5:1/4 G#5:1/4 A5:1/2 C#6:1/2 | "
                   "A5:1/4 B5:1/4 C#6:1/4 E6:1/4 F#6:1/2 E6:1/2 | D#6:1/4 E6:1/4 F#6:1/4 A6:1/4 B6:1", vel=40)
    n.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_ref=(40, 52))
    hit(c, segs, "pop", "他们坐船", 0, "the crowd sees them (a pluck)", pluck=(60, 72), glock=(86, 98), vel=42)
    n.duck(3.0, parts=["flute", "vln_mel"])
    n.expr(["flute"], [(0, -22), (8, -19), (20, -16)])
    n.expr(["vln_mel"], [(0, -24), (20, -20)])
    n.expr(["pz_lo", "pz_hi"], [(0, -16), (12, -14), (20, -12)])
    lv(n, "hand", -22)
    n.expr(["vla"], [(0, -27), (20, -25)])
    # the ta-da as the crowd beats the boat (E: pizzicato, glockenspiel, harp, a soft timpani)
    for nm in ("E3", "B3", "G#4", "E5"):
        lov.add("pz_lo" if nm == "E3" else "pz_hi", 0, 0.5, nm, 46, "arp", "h")
    lov.add("pz_cb", 0, 0.5, "E2", 46, "bass", "h")
    lov.add("glock", 0, 1.0, "B6", 40, "arp", "h")
    lov.add("timp", 0, 0.5, "E3", 34, "timp", "h")
    drum(lov, 0, 39, 30)
    lov.sync("'比船还先到了': ta-da", 0, t_arr)
    # 'Jesus got off the boat and saw so many people; his heart was full of love for them': the hillside song, tender
    lov.mel("cello", "r:3/2 E4:1 B4:1/2 | B4:3/2 G#4:1 E4:1/2", vel=46)
    rock(lov, 1.5, 6, part="harp", lo=40, hi=64, vel=28)
    strings(lov, vel=30, lo=52, hi=71, bass=(40, 52), cb=None, q0=0.5)
    hit(c, segs, "splash_small", "耶稣下了船", 0, "Jesus steps ashore (a harp note)", win=0.2, harp=(64, 76),
        pluck=(57, 69), vel=46)
    hit(c, segs, "chime", "耶稣下了船", 0, "his heart is full of love (a glint)", glock=(86, 98), celesta=(76, 88),
        vel=42)
    lov.duck(2.5, parts=["cello"])
    lv(lov, ["cello"], -15)
    lv(lov, ["harp"], -17)
    lv(lov, ["pz_hi", "pz_cb", "timp"], -13)
    lv(lov, "hand", -20)
    lov.expr(STR, [(0, -28), (1.5, -24), (6, -23)])
    # 'like sheep without a shepherd, not knowing where to go': a lone oboe over a drone, hanging
    sh.mel("oboe", "C#5:3/2 B4:1/2 A4:1/2 B4:1/2 | E4:1 F#4:1/2 A4:3/2", vel=44)
    sh.add("vc", 0, 6, "F#2", 30, "bass")
    sh.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=26, bass_ref=(40, 52))
    t_sp_ = pic(c, "pop", "耶稣下了船", 0)
    if t_sp_ is not None and t_sheep - 0.2 < t_sp_ < t_heal:                # the flock appears (a soft harp note)
        accent(c, segs, t_sp_, None, harp=(64, 76), vel=32)
    sh.duck(2.5, parts=["oboe"])
    sh.expr(["oboe"], [(0, -20), (1, -16), (6, -16)])
    lv(sh, ["vc"], -23)
    sh.expr(["vla", "vln1"], [(0, -26), (6, -25)])
    # 'Jesus taught them about God, and healed all the sick': the cello, glints for every healing
    h.mel("cello", "A4:1 C#5:1/2 B4:1 A4:1/2 | G#4:3", vel=46)
    rock(h, 0, 6, part="harp", lo=40, hi=66, vel=28)
    strings(h, vel=30, lo=52, hi=71, bass=(40, 52), cb=(28, 40))
    h.duck(3.5, parts=["cello"])
    h.expr(["cello"], [(0, -16), (4.0, -16), (6, -21)])
    lv(h, ["harp"], -18)
    h.expr(STR, [(0, -25), (6, -24)])
    t_well = voice_at(c, "还把生病的人都治好了")
    sg_, q_w = seg_at(c, segs, t_well)
    if sg_ is h and q_w < h.n_q - 1.0:
        sweep(h, q_w, 0.6, "E5", "E7", 22, 32, part="celesta")
    hit(c, segs, "chime", "耶稣就给大家讲上帝的事", 0, "the sick are healed (a glint)", glock=(86, 98), vel=40)
    hit(c, segs, "sparkle", "耶稣就给大家讲上帝的事", 0, "healing sparkles (the celesta)", clear=False,
        celesta=(76, 88), vel=36)
    follow(c, segs, "sparkle", t_heal - 0.3, c.dur - 0.05, skip=[pic(c, "sparkle", "耶稣就给大家讲上帝的事", 0) or -9],
           glock=(86, 98), celesta=(76, 88), vel=32)
    for sg in segs:
        if sg is not w:
            lv(sg, ["glock", "celesta", "kalimba"], -15)


def evening(c):
    """Evening and worry (E -> C-sharp minor).  The sun goes down on a falling flute (E, C-sharp minor 7); the tummies
    rumble on '咕噜咕噜' (a bassoon and tuba wobble on C-sharp, starting on the picture's bubbles); the disciples' worry in
    C-sharp minor on '这里什么吃的都没有' (change: tremolo strings, an anxious oboe, a ticking pizzicato); E on '你们给他们吃
    吧' (change): the hillside song's head on the harp; G-sharp 7 on '门徒们吓了一跳' (change) and the jolt on the picture;
    the question on '耶稣又问腓力' (change: A, the cello under the narrator, the harp under Jesus, hanging on B7sus4); E on
    '耶稣这样问' (change), warm; '其实，耶稣自己早就知道' (change): the boy's theme, far off, on the celesta -- he already
    knows (a glint on the picture); Philip counts on his fingers on '腓力掰着手指' (change): plucked steps that stall, a
    head-shake; '就算花好多好多钱' (change): the bassoon's sigh, falling to G-sharp 7, a clink for the money and five tiny
    bites falling on the celesta (the picture)."""
    c.gain(-3.5)
    t_worry = c.gap(c.find("这里什么吃的都没有"))
    t_calm = c.gap(c.find("你们给他们吃吧"))
    t_jump = c.gap(c.find("门徒们吓了一跳"))
    t_ask = c.at("耶稣又问腓力")
    t_know = c.gap(c.find("耶稣这样问"))
    t_knew = c.at("其实，耶稣自己早就知道")
    t_count = c.gap(c.find("腓力掰着手指"))
    t_money = c.gap(c.find("就算花好多好多钱买饼"))
    k = c.seg(0, t_worry, 3, "6/8", "E major", nominal=78, label="evening-dusk")
    wr = c.seg(t_worry, t_calm, 5, "2/4", "E major", nominal=80, label="evening-worry")
    cm = c.seg(t_calm, t_jump, 1, "6/8", "E major", nominal=None, label="evening-calm")
    jp = c.seg(t_jump, t_ask, 1, "2/4", "C# harmonic", nominal=None, label="evening-jump")
    ak = c.seg(t_ask, t_know, 2, "6/8", "E major", nominal=62, label="evening-ask")
    kn = c.seg(t_know, t_knew, 2, "6/8", "E major", nominal=84, label="evening-know")
    kw = c.seg(t_knew, t_count, 2, "6/8", "E major", nominal=98, label="evening-knew")
    ct = c.seg(t_count, t_money, 2, "2/4", "E major", nominal=None, label="evening-count")
    mo = c.seg(t_money, c.dur, 4, "2/4", "E major", nominal=72, label="evening-money")
    segs = (k, wr, cm, jp, ak, kn, kw, ct, mo)
    for sg in segs:
        sg.duck(1.5)
    k.prog("E:3 | C#m7:3 | F#m7:3/2 G#7:3/2@C#-harmonic")
    wr.prog("C#m:2 | A:1 F#m:1 | G#7:2@C#-harmonic | C#m:1 A:1 | B7sus4:1 B7:1")
    cm.prog("E:3/2 A:3/2")
    jp.prog("G#7:1 C#m:1")
    ak.prog("A:3 | F#m7:3/2 B7sus4:3/2")
    kn.prog("E:3 | A:3/2 B7sus4:3/2")
    kw.prog(" | ".join(BOY_PROG))
    ct.prog("C#m:2 | G#7sus4:1 G#7:1@C#-harmonic")
    mo.prog("A:2 | E/G#:2 | F#m:2 | G#7:2@C#-harmonic")
    wr.sync("'这里什么吃的都没有': worry (C-sharp minor)", 0, t_worry, kind="change")
    cm.sync("'你们给他们吃吧': E", 0, t_calm, kind="change")
    jp.sync("'门徒们吓了一跳': G-sharp 7", 0, t_jump, kind="change")
    ak.sync("'耶稣又问腓力': the question (A)", 0, t_ask, kind="change")
    kn.sync("'耶稣这样问': E", 0, t_know, kind="change")
    kw.sync("'其实，耶稣自己早就知道': the boy's theme, far off (E)", 0, t_knew, kind="change")
    ct.sync("'腓力掰着手指': Philip counts (C-sharp minor)", 0, t_count, kind="change")
    mo.sync("'就算花好多好多钱买饼': not enough (A)", 0, t_money, kind="change")
    # 'it was getting dark; everyone's tummy went rumble rumble': the sun goes down on the flute
    k.mel("flute", "B5:3/2 A5:1/2 G#5:1/2 F#5:1/2 | E5:3 | C#5:3/2 B#4:3/2", vel=42)
    rock(k, 0, 9, part="harp", lo=40, hi=64, vel=28)
    strings(k, vel=28, lo=52, hi=71, bass=(37, 49), cb=None)
    k.duck(2.5, parts=["flute"])
    k.expr(["flute"], [(0, -20), (1, -17), (9, -18)])
    lv(k, ["harp"], -17)
    k.expr(STR, [(0, -25), (9, -24)])
    # the rumble: gu-lu-gu-lu (bassoon and tuba wobbling on C-sharp), jiao (the low C-sharp)
    g0, g1 = span(c, "咕噜咕噜叫")
    t_bub = pic(c, "bubbles", None, 0)                      # the picture's rumble starts the wobble when it is near
    if t_bub is not None and g0 - 0.35 <= t_bub <= g0 + 0.5:
        g1, g0 = g1 + (t_bub - g0), t_bub
    rumble = spread(g0, g0 + 0.82 * (g1 - g0), 5)
    tune(c, segs, rumble, ["C#3", "D3", "C#3", "C3", "C#3"], part="bsn", vel=48, role="fx", art="", clear=False)
    tune(c, segs, rumble, ["C#2", "D2", "C#2", "C2", "C#2"], part="tuba", vel=44, role="fx", art="", clear=False)
    lv(k, ["bsn"], -18)
    lv(k, ["tuba"], -19)
    # 'there's nothing to eat here, and it's late; send them to the villages to buy food!': worry
    wr.mel("oboe", "G#4:1/2 A4:1/2 G#4:1/2 E4:1/2 | C#5:1/2 B4:1/2 A4:1/2 F#4:1/2 | B#4:1/2 D#5:1/2 F#5:1/2 D#5:1/2 | "
                   "E5:1/2 C#5:1/2 E5:1/2 A4:1/2 | B4:1 A4:1", vel=42)
    wr.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 69, vel=28, bass_ref=(37, 49))
    for q_ in np.arange(0, 10, 0.5):                         # a ticking pizzicato
        ch = wr.chord_at(q_ + 1e-3)
        if abs(q_ % 1.0) < 1e-6:
            wr.add("pz_lo", q_, 0.5, ch.bass_note(37, 49), 36, "arp", "s")
        elif not bool(wr.score.speaking(wr.t(q_))):
            wr.add("pz_hi", q_, 0.25, ch.tones(61, 73)[0], 28, "arp", "S")
    wr.duck(2.5, parts=["oboe"])
    wr.expr(["oboe"], [(0, -21), (1, -17), (10, -17)])
    wr.expr(["trem_va", "trem_hi"], [(0, -27), (10, -25)])
    lv(wr, ["pz_lo"], -15)
    lv(wr, ["pz_hi"], -16)
    # 'you give them something to eat': E, the hillside song's head on the cello
    cm.mel("harp", HILL[0], vel=42, transpose=12)
    roll_chord(cm, 0.0, 40, 64, vel=28, part="harp", n=4)
    strings(cm, vel=30, lo=52, hi=71, bass=(40, 52), cb=None)
    lv(cm, ["harp"], -16)
    cm.expr(STR, [(0, -25), (3, -23)])
    # 'the disciples were startled': a jolt (pizzicato and a flute flick up), Jesus asks Philip
    t_jp = pic(c, "whoosh", "门徒们吓了一跳", 0)
    t_j = t_jp if t_jp is not None else min(max(voice_at(c, "门徒们吓了一跳") + 0.45, t_jump + 0.1), t_ask - 0.25)
    sg_, q_j = seg_at(c, segs, t_j)
    clear_near(c, t_j)
    sg_.add("pz_hi", q_j, _dq(sg_, q_j, 0.25), top(sg_, q_j, 60, 72), 46, "arp", "h")
    sg_.add("pz_lo", q_j, _dq(sg_, q_j, 0.25), sg_.chord_at(q_j + 1e-3).bass_note(37, 49), 44, "arp", "h")
    if sg_ is jp:
        sweep(jp, q_j + 0.02, 0.18, "C#5", "C#6", 30, 40, part="flute")
    sg_.sync("'吓了一跳': the jolt" + (" (picture)" if t_jp is not None else ""), q_j, t_j)
    jp.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=26, bass_part="vc", bass_lo=37, bass_hi=49)
    lv(jp, ["pz_hi", "pz_lo"], -14)
    lv(jp, ["flute"], -18)
    jp.expr(["vla", "vln1", "vc"], [(0, -25), (2, -22)])
    # 'where shall we buy bread for all these people?': A, hanging on B7sus4
    ak.mel("cello", "C#4:3/2 E4:1 r:1/2 | r:3", vel=44)
    ak.mel("harp", "r:3 | C#5:3/2 E5:3/2", vel=36)
    rock(ak, 0, 6, part="harp", lo=40, hi=59, vel=26)
    ak.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=28, bass_part="vc", bass_lo=40, bass_hi=52)
    ak.duck(2.0, parts=["cello"])
    ease(ak, ["cello"], -16, drop=9, over=1.5)
    ease(ak, ["harp"], -17, drop=9, over=1.5)
    ak.expr(["vla", "vln1", "vc"], [(0, -25), (6, -23)])
    # 'Jesus asked to see what Philip would say': warm E
    rock(kn, 0, 6, part="harp", lo=40, hi=66, vel=28)
    strings(kn, vel=28, lo=52, hi=71, bass=(40, 52), cb=None)
    kn.mel("cello", "G#3:3/2 B3:1 E4:1/2 | C#4:3/2 B3:3/2", vel=40)
    kn.duck(2.5, parts=["cello"])
    lv(kn, ["cello"], -20)
    lv(kn, ["harp"], -19)
    kn.expr(STR, [(0, -26), (6, -25)])
    # 'in fact Jesus already knew what he would do': the boy's theme, far off, on the celesta
    kw.mel("celesta", bars(BOY, 0, 2), vel=40, transpose=12)
    rock(kw, 0, 6, part="harp", lo=40, hi=66, vel=26)
    kw.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    hit(c, segs, "chime", "耶稣这样问", 0, "he already knows (a glint)", glock=(86, 98), vel=40)
    kw.duck(3.0, parts=["celesta"])
    ease(kw, ["celesta"], -19, drop=5)
    lv(kw, ["harp"], -21)
    kw.expr(["vla", "vln1", "vc"], [(0, -26), (6, -24)])
    # 'Philip counted on his fingers and shook his head': plucked steps that stall, a head-shake
    ct.pad(["vla", "vla", "vln1"], 3, 50, 68, vel=24, bass_part="vc", bass_lo=37, bass_hi=49)
    fing = pick_times(pics(c, "pop"), t_count, t_money)
    t_shake = voice_at(c, "摇摇头说")
    if len(fing) >= 4:
        steps_t = fing[:4]
    else:
        steps_t = [ct.t(q_) - c.t0 for q_ in (0.0, 0.5, 1.0, 1.5)]
    steps_t = [t_ for t_ in steps_t if t_count - 1e-6 <= t_ < t_money - 0.6]
    tune(c, segs, steps_t, ["C#4", "D#4", "E4", "F#4"][:len(steps_t)], part="pz_hi", vel=44, role="fx",
         art="s", last=0.5, what="Philip counts a finger" if len(fing) >= 4 else None, sync=(0, 3) if len(fing) >= 4 else ())
    stall = [ct.t(2.0) - c.t0, ct.t(2.5) - c.t0]
    tune(c, segs, stall, ["G#4", "G#4"], part="pz_hi", vel=40, role="fx", art="s")
    sh_t = max(t_shake, ct.t(3.0) - c.t0)
    shake = [sh_t + 0.2 * j for j in range(4)]
    shake = [t_ for t_ in shake if t_ < t_money - 0.1]
    tune(c, segs, shake, ["A3", "G#3", "A3", "G#3"][:len(shake)], part="bsn", vel=40, role="fx", art="s")
    ct.duck(1.5, parts=["pz_hi"])
    lv(ct, ["pz_hi"], -14)
    lv(ct, ["bsn"], -17)
    ct.expr(["vla", "vln1", "vc"], [(0, -26), (4, -25)])
    # 'even lots and lots of money wouldn't buy enough for everyone to have a little bite!': the bassoon's sigh
    mo.mel("bsn", "C#4:1/2 E4:1/2 A4:1/2 G#4:1/2 | B4:1 G#4:1/2 E4:1/2 | F#4:1 E4:1/2 D#4:1/2 | B#3:1 G#3:1", vel=44)
    mo.pad(["vla", "vla", "vln1"], 3, 50, 68, vel=26, bass_part="vc", bass_lo=37, bass_hi=49)
    for q_ in np.arange(0, 8, 1.0):
        mo.add("pz_lo", q_, 0.5, mo.chord_at(q_ + 1e-3).bass_note(37, 49), 32, "arp", "s")
    mo.duck(2.5, parts=["bsn"])
    mo.expr(["bsn"], [(0, -20), (1, -16), (8, -17)])
    lv(mo, ["pz_lo"], -15)
    mo.expr(["vla", "vln1", "vc"], [(0, -26), (8, -24)])
    follow(c, segs, "coins", t_money - 0.3, c.dur - 0.05, what="lots and lots of money (a clink)", sync=(0,),
           glock=(86, 98), vel=40)
    t_th = pic(c, "pop", "就算花好多好多钱买饼", 0)            # a thought of money (a soft pluck)
    if t_th is not None and t_th < c.ls(c.find("就算花好多好多钱买饼")) + 0.8:
        accent(c, segs, t_th, None, pluck=(60, 72), vel=34)
    bites = pick_times(pics(c, "pop"), c.at("也不够每个人吃一小口") - 0.6, c.dur - 0.3)
    if len(bites) >= 5:                                     # five tiny bites: the celesta falls, F-sharp minor
        tune(c, segs, bites[:5], ["C#6", "B5", "A5", "G#5", "F#5"], part="celesta", vel=40, role="fx", art="",
             last=0.5, what="a tiny bite each", sync=(0, 4))
        lv(mo, ["celesta"], -16)
        t_sk = pic(c, "sparkle", "就算花好多好多钱买饼", 0)
        if t_sk is not None and t_sk > bites[4] + 0.2:
            accent(c, segs, t_sk, None, glock=(86, 98), vel=32)
    for sg in segs:
        lv(sg, ["glock", "celesta"], -15)


def boy(c):
    """The boy (A -> E).  '你们有多少饼？' -- the hillside song's head in A on the harp (the deceptive answer to Philip's
    G-sharp 7); the search on '门徒们找啊找' (change: F-sharp minor, tiptoe pizzicato, a flute peeking); a ping as he is
    found on '这时候'; E on '彼得的兄弟安得烈' (change): a harp roll, and the boy's theme on the kalimba as he is brought
    in; the counting game on '这里有个小孩子' (change): five notes for the five loaves and two for the fish, on the picture
    (or on the voice); C-sharp minor on '可是，这么多人' (change), hanging on B7sus4; '五个饼，两条鱼' (change): the count
    again, tiny; A on '可是，小男孩把他带的饭' (change): his theme handed to the cello -- Jesus takes it -- warm, home to E."""
    c.gain(-3.5)
    t_find = c.gap(c.find("门徒们找啊找"))
    t_and = c.at("彼得的兄弟安得烈")
    t_cnt = c.gap(c.find("这里有个小孩子"))
    t_doubt = c.at("可是，这么多人")
    t_give = c.gap(c.find("五个饼，两条鱼，只够"))
    t_gift = c.at("可是，小男孩把他带的饭")
    j = c.seg(0, t_find, 2, "6/8", "A major", nominal=None, label="boy-jesus")
    f = c.seg(t_find, t_and, 3, "2/4", "E major", nominal=None, label="boy-search")
    a = c.seg(t_and, t_cnt, 3, "6/8", "E major", nominal=None, label="boy-andrew")
    n = c.seg(t_cnt, t_doubt, 2, "6/8", "E major", nominal=None, label="boy-count")
    d = c.seg(t_doubt, t_give, 2, "6/8", "E major", nominal=None, label="boy-doubt")
    g = c.seg(t_give, t_gift, 2, "6/8", "E major", nominal=None, label="boy-small")
    h = c.seg(t_gift, c.dur, 2, "6/8", "E major", nominal=None, label="boy-gift")
    segs = (j, f, a, n, d, g, h)
    for sg in segs:
        sg.duck(1.5)
    j.prog("A:3/2 D:3/2 | A/C#:3")
    f.prog("F#m:2 | C#m:2 | B7:2")
    a.prog("E:3 | " + " | ".join(BOY_PROG))
    n.prog("A:3 | E:3")
    d.prog("C#m:3 | F#m7:3/2 B7sus4:3/2")
    g.prog("E:3 | F#m7:3/2 B7:3/2")
    h.prog(" | ".join(BOY_PROG))
    f.sync("'门徒们找啊找': the search (F-sharp minor)", 0, t_find, kind="change")
    a.sync("'彼得的兄弟安得烈': Andrew brings the boy (E)", 0, t_and, kind="change")
    n.sync("'这里有个小孩子': the counting game (E)", 0, t_cnt, kind="change")
    d.sync("'可是，这么多人': C-sharp minor", 0, t_doubt, kind="change")
    g.sync("'五个饼，两条鱼，只够': E, tiny", 0, t_give, kind="change")
    h.sync("'可是，小男孩把他带的饭': the gift (E)", 0, t_gift, kind="change")
    # 'how many loaves do you have? go and see': the hillside song's head in A on the cello
    j.mel("harp", "A4:1 E5:1/2 D5:1 F#5:1/2 | E5:3/2 C#5:1 A4:1/2", vel=42)
    rock(j, 0, 6, part="guitar", lo=45, hi=64, vel=26)
    j.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=28, bass_part="vc", bass_lo=40, bass_hi=52)
    lv(j, ["harp"], -16)
    lv(j, ["guitar"], -19)
    j.expr(["vla", "vln1", "vc"], [(0, -26), (6, -24)])
    # 'they looked and looked': tiptoe pizzicato, a flute peeking in the pauses; a ping on '这时候'
    for q_ in np.arange(0, 6, 0.5):
        ch = f.chord_at(q_ + 1e-3)
        if abs(q_ % 1.0) < 1e-6:
            f.add("pz_lo", q_, 0.5, ch.bass_note(40, 52), 34, "arp", "s")
        else:
            f.add("pz_hi", q_, 0.25, ch.tones(61, 73)[int(q_ * 2) % 2], 30, "arp", "S")
    f.mel("flute", "r:1 C#6:1/4 A5:1/4 r:1/2 | r:1 G#5:1/4 E5:1/4 r:1/2 | r:2", vel=36)
    f.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=24, bass_ref=(40, 52))
    t_now = voice_at(c, "这时候")
    sg_, q_n = seg_at(c, segs, t_now)
    if sg_ is f:
        clear_near(c, t_now)
        f.add("kalimba", q_n, _dq(f, q_n, 1.0), top(f, q_n, 76, 88), 44, "arp", "h")
        f.add("glock", q_n, _dq(f, q_n, 1.0), top(f, q_n, 86, 98), 36, "arp", "h")
        f.sync("'这时候': there he is (a ping)", q_n, t_now)
    lv(f, ["pz_lo", "pz_hi"], -15)
    lv(f, ["flute"], -19)
    lv(f, ["kalimba"], -15)
    f.expr(["vla", "vln1"], [(0, -27), (6, -25)])
    # 'Peter's brother Andrew brought a little boy': E, a harp roll, the boy's theme on the kalimba
    clear_near(c, t_and - 0.15, win=0.2)
    roll_chord(a, 0.0, 40, 71, vel=40, part="harp", n=6)
    strum(a, 0.0, 52, 71, vel=44, part="guitar", n=4, dq=1.5)
    a.add("pz_lo", 0, 0.5, "E2", 48, "arp", "h")
    for nm in ("B3", "G#4"):
        a.add("pz_hi", 0, 0.5, nm, 44, "arp", "h")
    a.sync("'彼得的兄弟安得烈': Andrew brings the boy (a strum)", 0, t_and)
    a.mel("kalimba", "r:3 | " + bars(BOY, 0, 2), vel=50)
    rock(a, 1.5, 9, part="guitar", lo=40, hi=64, vel=28)
    strings(a, vel=28, lo=52, hi=71, bass=(40, 52), cb=None)
    hdrum(a, 3, 9, vel=26)
    a.duck(2.5, parts=["kalimba"])
    lv(a, ["kalimba"], -13)
    lv(a, ["harp"], -16)
    lv(a, ["guitar"], -18)
    lv(a, "hand", -21)
    a.expr(STR, [(0, -21), (1.5, -24), (9, -23)])
    lv(a, ["pz_lo", "pz_hi"], -13)
    # 'here's a little boy with five barley loaves and two little fish': the counting game, on the picture or the voice
    i_a = c.find("这里有个小孩子")
    pops = pick_times(pics(c, "pop"), c.ls(i_a) - 0.3, t_doubt - 0.1)
    if len(pops) >= 7:
        times, on_pic = pops[:7], True
    else:
        times, on_pic = count_times(c, "这里有个小孩子", list("五个大麦饼两鱼"), t_cnt + 0.1, t_doubt - 0.15), False
    n.chords.clear()                                         # Andrew's warm A, then E under the counting
    prog48(n, ["A", "E"], edges48(n, c, [times[0] - 0.2]))
    tune(c, segs, times, BOY_NOTES, part="kalimba", vel=46, role="fx",
         what="a loaf / a fish is counted" + (" (picture)" if on_pic else ""), sync=(0, 4, 6),
         glock=(4, 6))
    rock(n, 0, 6, part="harp", lo=40, hi=64, vel=24)
    n.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    lv(n, ["kalimba"], -15)
    lv(n, ["glock"], -18)
    lv(n, ["harp"], -18)
    n.expr(["vla", "vln1", "vc"], [(0, -26), (6, -24)])
    # 'but with so many people, how can this little bit be enough?': C-sharp minor, hanging
    d.mel("oboe", "E5:3/2 D#5:1/2 C#5:1 | A4:3/2 B4:3/2", vel=42)
    d.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=26, bass_part="vc", bass_lo=37, bass_hi=49)
    rock(d, 0, 6, part="harp", lo=37, hi=61, vel=24)
    d.duck(2.5, parts=["oboe"])
    ease(d, ["oboe"], -17, drop=7)
    ease(d, ["harp"], -18)
    d.expr(["vla", "vln1", "vc"], [(0, -26), (6, -24)])
    # 'five loaves, two fish -- just enough for one little boy': the count again, tiny and quick
    o5, o2 = syl(c, "五个饼，两条鱼，只够", 2)
    small = [o5 + 0.15 * k for k in range(5)] + [o2, o2 + 0.3]
    small = [min(t_, g.t(2.6) - c.t0) for t_ in small]
    for k_ in range(1, len(small)):
        small[k_] = max(small[k_], small[k_ - 1] + 0.08)
    tune(c, segs, small, BOY_NOTES, part="kalimba", vel=36, role="fx", clear=False)
    g.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    roll_chord(g, 0.0, 40, 68, vel=28, part="harp", n=5)
    for q_ in (3.0, 4.5):
        g.add("harp", q_, 1.5, top(g, q_, 52, 64), 26, "arp")
    rock(g, 3.0, 6.0, part="harp", lo=40, hi=64, vel=24)
    lv(g, ["kalimba"], -18)
    lv(g, ["harp"], -18)
    g.expr(["vla", "vln1", "vc"], [(0, -24), (6, -24)])
    # 'but the boy gave his lunch to Jesus': his theme in Jesus's hands -- the cello -- warm strings, home to E
    h.mel("cello", bars(BOY, 0, 2), vel=48, transpose=-24)
    h.mel("kalimba", "r:3 | r:3/2 E6:3/2", vel=38)
    strings(h, vel=30, lo=52, hi=73, bass=(40, 52), cb=(28, 40))
    rock(h, 0, 6, part="harp", lo=40, hi=68, vel=28)
    h.duck(2.5, parts=["cello"])
    h.expr(["cello"], [(0, -20), (1.0, -14), (4.5, -14), (6, -19)])
    h.expr(["kalimba"], [(0, -17), (4.5, -17), (6, -21)])
    ease(h, ["harp"], -16, drop=9, over=1.5)
    h.expr(STR, [(0, -28), (1.5, -24), (4.5, -22), (6, -24)])
    hit(c, segs, "cloth", "可是，小男孩把他带的饭", 0, "the boy hands over his lunch (a kalimba and harp)", win=0.15,
        harp=(64, 76), kal=(76, 91), pluck=(60, 72), vel=44)
    hit(c, segs, "chime", "五个饼，两条鱼，只够", 0, "Jesus takes the lunch (a glint)", clear=False, glock=(86, 98),
        vel=40)
    t_by = pic(c, "pop", "五个饼，两条鱼，只够", 1)
    if t_by is not None and t_by < t_gift - 0.3:
        accent(c, segs, t_by, None, harp=(64, 76), vel=30)
    for sg in segs:
        if sg is not n:
            lv(sg, ["glock", "celesta"], -14)


def sit(c):
    """The hillside (E, 6/8).  Jesus: '叫大家都坐下来吧' (harp, guitar, a flute bird); the hillside song on the cello on
    '那里有好多青草' (change), rows of plucks as the groups sit down in rows; '有的一百个人一组' (change): a big low plucked
    chord for the hundred, a light high one for the fifty; the garden seen from above on '从高处看' (change: A, a flute
    high over harp and celesta, little gardens twinkling); '光是男人，就有五千个' (change): the song in full strings with
    a horn, a timpani on '五千', the kalimba for the mothers and children, home to E on '整个山坡'."""
    c.gain(-3.5)
    t_grass = c.gap(c.find("那里有好多青草"))
    t_hund = c.at("有的一百个人一组")
    t_high = c.gap(c.find("从高处看"))
    t_full = c.gap(c.find("光是男人"))
    i0 = c.seg(0, t_grass, 3, "6/8", "E major", nominal=None, label="sit-jesus")
    gr = c.seg(t_grass, t_hund, 3, "6/8", "E major", nominal=None, label="sit-grass")
    hu = c.seg(t_hund, t_high, 2, "6/8", "E major", nominal=None, label="sit-groups")
    ga = c.seg(t_high, t_full, 3, "6/8", "E major", nominal=None, label="sit-garden")
    fu = c.seg(t_full, c.dur, 4, "6/8", "E major", nominal=None, label="sit-full")
    segs = (i0, gr, hu, ga, fu)
    for sg in segs:
        sg.duck(1.5)
    i0.prog("E:3 | A:3 | B7sus4:3/2 B7:3/2")
    gr.prog(" | ".join(HILL_PROG[0:3]))
    hu.prog(HILL_PROG[3] + " | E:3")
    ga.prog("A:3 | E/G#:3 | F#m7:3/2 B7sus4:3/2")
    fu.prog(" | ".join(HILL_PROG[4:8]))
    gr.sync("'那里有好多青草': the hillside song (E)", 0, t_grass, kind="change")
    hu.sync("'有的一百个人一组': the groups (E/B)", 0, t_hund, kind="change")
    ga.sync("'从高处看': from above (A)", 0, t_high, kind="change")
    fu.sync("'光是男人，就有五千个': the whole hillside (E)", 0, t_full, kind="change")
    # 'Jesus said to the disciples: have everyone sit down': harp, guitar, a flute bird
    rock(i0, 0, 9, part="harp", lo=40, hi=66, vel=28)
    rock(i0, 0, 9, part="guitar", lo=40, hi=59, vel=26, pat=(0, 1, 2, 1, 2, 1))
    i0.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    i0.mel("flute", "r:3/2 B5:1/4 C#6:1/4 B5:1 | r:3 | r:3/2 F#5:1/4 A5:1/4 F#5:1", vel=34)
    hdrum(i0, 0, 9, vel=24)
    i0.expr(["harp"], [(0, -15), (3, -17), (9, -17)])
    lv(i0, ["guitar"], -19)
    lv(i0, ["flute"], -21)
    lv(i0, "hand", -22)
    i0.expr(["vla", "vln1", "vc"], [(0, -23), (9, -24)])
    # 'there was lots of green grass; everyone sat down in rows and groups': the hillside song on the cello
    gr.mel("cello", bars(HILL, 0, 3), vel=48)
    rock(gr, 0, 9, part="harp", lo=40, hi=66, vel=28)
    strings(gr, vel=28, lo=52, hi=71, bass=(40, 52), cb=(28, 40))
    hdrum(gr, 0, 9, vel=24)
    gr.duck(3.0, parts=["cello"])
    ease(gr, ["cello"], -15, drop=7)
    ease(gr, ["harp"], -18)
    lv(gr, "hand", -22)
    gr.expr(STR, [(0, -25), (9, -23)])
    rows = pick_times(pics(c, "cloth"), c.at("大家一排一排") - 0.3, t_hund - 0.15)
    if rows:
        for t_ in rows:
            clear_near(c, t_)
        for t_ in rows:
            clear_near(c, t_, win=0.15, roles=("arp", "perc"))
        climb(c, segs, rows, part="harp", lo=64, hi=86, vel=40, glock=False, pz=True)
    # 'some groups of a hundred, some of fifty': a big low plucked chord, a light high one
    p100, p50 = pic(c, "pop", "有的一百个人一组", 0), pic(c, "pop", "有的一百个人一组", 1)
    t_100 = [p100] if p100 is not None else chars(c, "有的一百个人一组", "百")
    t_50 = [p50] if p50 is not None else chars(c, "有的一百个人一组", "十")
    hu.mel("cello", HILL[3] + " | E4:3", vel=46)
    rock(hu, 0, 6, part="harp", lo=40, hi=66, vel=26)
    strings(hu, vel=28, lo=52, hi=71, bass=(40, 52), cb=(28, 40))
    hu.duck(3.0, parts=["cello"])
    lv(hu, ["cello"], -16)
    lv(hu, ["harp"], -19)
    lv(hu, ["pz_lo", "pz_hi", "pz_cb", "kalimba"], -14)
    lv(hu, "hand", -21)
    hu.expr(STR, [(0, -25), (6, -23)])
    for t_l, big in ((t_100[0] if t_100 else None, True), (t_50[0] if t_50 else None, False)):
        if t_l is None:
            continue
        sg_, q_ = seg_at(c, segs, t_l)
        clear_near(c, t_l, win=0.2, roles=("arp", "perc"))
        if big:
            for p in sg_.chord_at(q_ + 1e-3).tones(40, 59)[:4]:
                sg_.add("pz_lo" if p < 55 else "pz_hi", q_, _dq(sg_, q_, 0.5), p, 50, "arp", "h")
            thump(sg_, q_, vel=46, kit=False)
            sg_.add("harp", q_, _dq(sg_, q_, 1.0), sg_.chord_at(q_ + 1e-3).bass_note(28, 40), 44, "arp", "h")
            sg_.add("glock", q_, _dq(sg_, q_, 1.0), top(sg_, q_, 86, 98), 40, "arp", "h")
            drum(sg_, q_, 64, 34)
            sg_.sync("'一百': a hundred (a big low chord)", q_, t_l)
        else:
            for p in sg_.chord_at(q_ + 1e-3).tones(71, 88)[-3:]:
                sg_.add("kalimba", q_, _dq(sg_, q_, 0.5), p, 40, "arp", "h")
            sg_.add("pz_hi", q_, _dq(sg_, q_, 0.25), top(sg_, q_, 64, 76), 40, "arp", "h")
            sg_.sync("'五十': fifty (a light high chord)", q_, t_l)
    # 'seen from high above, the groups look like little gardens': A, the flute high over harp and celesta
    ga.mel("flute", "C#6:3/2 B5:1 C#6:1/2 | B5:3/2 G#5:3/2 | A5:1 F#5:1/2 E5:3/2", vel=40)
    broken(ga, "celesta", 0, 9, (0, 1, 2, 3, 2, 1), 76, 96, vel=26, step=0.5, thin=True, ring=False)
    rock(ga, 0, 9, part="harp", lo=45, hi=71, vel=26)
    ga.pad(["vla", "vla", "vln1"], 3, 55, 74, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    ga.duck(2.5, parts=["flute", "celesta"])
    ga.expr(["flute"], [(0, -20), (1, -16), (9, -16)])
    lv(ga, ["celesta"], -19)
    lv(ga, ["harp"], -17)
    ga.expr(["vla", "vln1", "vc"], [(0, -25), (9, -23)])
    t_up = pic(c, "whoosh", "那里有好多青草", 0)
    if t_up is not None:                                    # the camera rises: a harp sweep into the view
        accent(c, segs, t_up, "the view rises (a harp sweep)", harp=(57, 69), vel=42)
        sg2, q2 = seg_at(c, segs, t_up + 0.03)
        sweep(sg2, q2 + 0.03, 0.7, "A4", "A6", 24, 34, part="harp")
    hit(c, segs, "chime", "从高处看", 0, "the little gardens glow (a glint)", glock=(86, 98), vel=40)
    follow(c, segs, "pop", t_high, t_full, celesta=(84, 96), vel=32)
    follow(c, segs, "sparkle", t_high, t_full, glock=(86, 98), vel=32)
    # 'five thousand men! and lots of mums and children; the whole hillside full': the song in full strings
    fu.mel("vln_mel", bars(HILL, 4, 8), vel=40, transpose=12)
    fu.mel("cello", bars(HILL, 4, 8), vel=44)
    fu.mel("horn", "G#3:3/2 A3:3/2 | G#3:3 | A3:3/2 A3:3/2 | G#3:3", vel=38, role="counter")
    strings(fu, vel=32, lo=52, hi=72, bass=(40, 52), cb=(28, 40))
    rock(fu, 0, 12, part="harp", lo=40, hi=68, vel=28)
    hdrum(fu, 0, 12, vel=26)
    fu.duck(4.0, parts=["vln_mel", "cello", "horn"])
    fu.expr(["vln_mel"], [(0, -23), (1, -19), (9.5, -18), (12, -24)])
    fu.expr(["cello"], [(0, -21), (1, -17), (9.5, -17), (12, -23)])
    fu.expr(["horn"], [(0, -21), (9.5, -21), (12, -27)])
    lv(fu, ["harp"], -16)
    lv(fu, "hand", -21)
    fu.expr(STR, [(0, -25), (6, -22), (10.5, -21), (12, -24)])
    t_5k = voice_at(c, "就有五千个")
    t_5p = pic(c, "sparkle", "光是男人", 0)
    on_5p = t_5p is not None and t_5k - 0.3 <= t_5p <= t_5k + 1.6
    if on_5p:
        t_5k = t_5p
    elif t_5p is not None:
        accent(c, segs, t_5p, "five thousand (a glint)", glock=(86, 98), celesta=(76, 88), vel=40)
    sg_, q_5 = seg_at(c, segs, t_5k)
    if sg_ is fu:
        clear_near(c, t_5k, win=0.3, roles=("arp", "perc"))
        thump(fu, q_5, vel=48, kit=False)
        for p in fu.chord_at(q_5 + 1e-3).tones(52, 71)[:4]:
            fu.add("pz_lo" if p < 55 else "pz_hi", q_5, _dq(fu, q_5, 0.5), p, 50, "arp", "h")
        fu.add("glock", q_5, _dq(fu, q_5, 1.0), top(fu, q_5, 86, 98), 40, "arp", "h")
        roll_chord(fu, q_5 + 0.05, 40, 64, vel=30, part="harp", n=4)
        fu.sync("'五千个': five thousand (a timpani)" + (" (picture)" if on_5p else ""), q_5, t_5k)
    t_ch = pic(c, "chime", "光是男人", 0)
    if t_ch is not None and abs(t_ch - t_5k) > 0.12:
        accent(c, segs, t_ch, None, glock=(86, 98), vel=32)
    t_gw = pic(c, "grow", "光是男人", 0)
    if t_gw is not None:                                    # the hillside fills: the celesta sweeps up
        sg_, q_g = accent(c, segs, t_gw, "the hillside fills (the celesta sweeps up)", celesta=(76, 88), vel=40)
        sweep(sg_, q_g + 0.05, 0.8, "E5", "E7", 22, 32, part="celesta")
    t_kid = pic(c, "pop", "光是男人", 0)
    t_kids = voice_at(c, "还有好多妈妈和小朋友")
    sg_, q_k = seg_at(c, segs, t_kids)
    if t_kid is not None:
        hit(c, segs, "pop", "光是男人", 0, "a child pops up (a kalimba ping)", kal=(79, 91), glock=(86, 98), vel=40)
    elif sg_ is fu:
        for k_, off in enumerate((0.0, 0.25, 0.5)):
            qq = q_k + off
            if qq < fu.n_q - 0.3:
                fu.add("kalimba", qq, _dq(fu, qq, 0.25), fu.chord_at(qq + 1e-3).tones(76, 91)[k_ % 3], 34, "arp",
                       "s")
    lv(fu, ["timp", "pz_cb", "pz_lo", "pz_hi"], -13)
    lv(fu, "okit", -19)
    lv(fu, ["kalimba"], -16)
    for sg in segs:
        lv(sg, ["glock", "celesta"], -15)


def bless(c):
    """The miracle (E, 6/8).  A hush: the five loaves and two fish in Jesus's hands -- the boy's theme on the harp, alone;
    '抬头望着天' (change): high strings rise and a choir 'ooh' on A over E; the Amen on '感谢上帝' (change): E major, choir
    'aah', harp glissando and glockenspiel on the picture's light; '然后，他把饼掰开' (change): the bread breaks (a harp
    cascade, a pizzicato chord); '门徒再分给大家' (change): his five notes passed on to the guitar, the fish on the
    pizzicato and celesta for '鱼也是这样' (to B7); '分啊分' (change): the round -- his theme in canon over E and A/E, the
    kalimba, then the celesta, then the harp, the guitar strumming and the pizzicato joining bar by bar; '大家想吃多少'
    (change): abundance -- the violins and the cello sing la do' ti, the horn, the kalimba and harp sweeping up A and B7,
    and the tonic E arrives with the next page."""
    c.gain(-3.0)
    t_look = c.at("抬头望着天")
    t_thx = c.at("感谢上帝")
    t_brk = c.gap(c.find("然后，他把饼掰开"))
    t_share = c.at("门徒再分给大家")
    t_round = c.gap(c.find("分啊分"))
    t_all = c.at("大家想吃多少")
    tk = c.seg(0, t_look, 2, "6/8", "E major", nominal=None, label="bless-take")
    lk = c.seg(t_look, t_thx, 1, "6/8", "E major", nominal=None, label="bless-look")
    th = c.seg(t_thx, t_brk, 1, "6/8", "E major", nominal=None, label="bless-thanks")
    br = c.seg(t_brk, t_share, 2, "6/8", "E major", nominal=None, label="bless-break")
    sh = c.seg(t_share, t_round, 2, "6/8", "E major", nominal=None, label="bless-share")
    rd = c.seg(t_round, t_all, 3, "6/8", "E major", nominal=None, label="bless-round")
    pl = c.seg(t_all, c.dur, 1, "6/8", "E major", nominal=None, label="bless-plenty")
    segs = (tk, lk, th, br, sh, rd, pl)
    for sg in (tk, lk, br, sh, rd, pl):
        sg.duck(1.5)
    tk.prog(" | ".join(BOY_PROG))
    lk.prog("Aadd9/E:3")
    th.prog("E:3")
    br.prog("A:3 | E/G#:3/2 F#m7:3/2")
    sh.prog(BOY_PROG[0] + " | B7/D#:3")
    rd.prog("E:3/2 A/E:3/2 | E:3/2 A/E:3/2 | E:3/2 E/G#:3/2")
    pl.prog("A:3/2 B7:3/2")
    lk.sync("'抬头望着天': he looks up (A over E)", 0, t_look, kind="change")
    th.sync("'感谢上帝': the Amen (E)", 0, t_thx, kind="change")
    br.sync("'然后，他把饼掰开': the bread is broken (A)", 0, t_brk, kind="change")
    sh.sync("'门徒再分给大家': passed on (E)", 0, t_share, kind="change")
    rd.sync("'分啊分': the round (E)", 0, t_round, kind="change")
    pl.sync("'大家想吃多少': abundance (A)", 0, t_all, kind="change")
    # 'Jesus took the five loaves and two fish': a hush -- the boy's theme on the harp, alone, over soft strings
    tk.mel("harp", bars(BOY, 0, 2), vel=40, transpose=-12)
    tk.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=24, bass_part="vc", bass_lo=40, bass_hi=52)
    lv(tk, ["harp"], -15)
    tk.expr(["vla", "vln1", "vc"], [(0, -26), (6, -26)])
    # 'looked up to heaven': high strings rise, a choir 'ooh'
    lk.pad(["vla", "vln2", "vln1"], 3, 61, 81, vel=28, bass_part="vc", bass_lo=40, bass_hi=52)
    lk.pad("ooh", 3, 57, 76, vel=28, bass_ref=(40, 52))
    lk.expr(["vla", "vln2", "vln1", "vc"], [(0, -28), (3, -21)])
    lk.expr(["ooh"], [(0, -30), (3, -22)])
    # 'and gave thanks to God': the Amen -- E, choir 'aah', harp glissando, glockenspiel (on the picture's light)
    t_up = pic(c, "chime", "抬头望着天", 0)
    k_l = 1 if t_up is not None and t_up < t_thx - 0.2 else 0
    if k_l:                                                 # he looks up to heaven: a glint over the rising strings
        accent(c, segs, t_up, "he looks up to heaven (a glint)", glock=(86, 98), celesta=(76, 88), vel=42)
    t_lt, okl = lead(c, segs, "chime", "抬头望着天", k_l, t_thx - 0.1, th.t(1.5) - c.t0, "the light (a glint)",
                     glock=(86, 98), vel=40)
    q_l = qpos(th, c, t_lt, 0.0, 1.5) if okl else 0.0
    th.pad(["vla", "vln2", "vln1"], 3, 59, 80, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    th.pad("choir", 3, 56, 76, vel=30, bass_ref=(40, 52))
    bassline(th, "cb", 28, 40, 28)
    th.add("glock", q_l, _dq(th, q_l, 2.0), "G#6", 40, "arp", "h")
    th.add("glock", q_l, _dq(th, q_l, 2.0), "E7", 34, "arp", "h")
    th.add("harp", q_l, _dq(th, q_l, 2.0), "E3", 36, "arp", "h")
    sweep(th, q_l + 0.02, 0.6, "E4", "E6", 24, 36, part="harp")
    if okl:
        th.sync("the light (picture)", q_l, t_lt)
    th.expr(["vla", "vln2", "vln1", "vc"], [(0, -21), (1, -19), (3, -22)])
    th.expr(["cb"], [(0, -24), (3, -25)])
    th.expr(["choir"], [(0, -24), (1, -20), (3, -23)])
    lv(th, ["glock"], -14)
    lv(th, ["harp"], -15)
    # 'then he broke the bread and gave it to the disciples': the bread breaks (a harp cascade, a pizzicato chord)
    t_bk = pic(c, "crunch", "然后，他把饼掰开", 0) or pic(c, "cloth", "然后，他把饼掰开", 0)
    t_b = t_bk if t_bk is not None else min(max(voice_at(c, "他把饼掰开") + 0.55, t_brk + 0.2), t_share - 0.5)
    sg_, q_b = seg_at(c, segs, t_b)
    br.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    br.pad("choir", 3, 56, 76, q0=0.0, q1=3.0, vel=26, bass_ref=(40, 52))  # the Amen fades into the breaking
    br.expr(["choir"], [(0, -24), (3, -34)])
    clear_near(c, t_b, win=0.2)
    for p_ in sg_.chord_at(q_b + 1e-3).tones(45, 69)[::2][:3]:
        sg_.add("pz_lo" if p_ < 55 else "pz_hi", q_b, _dq(sg_, q_b, 0.25), p_, 44, "arp", "h")
    sweep(sg_, q_b + 0.02, 0.45, "E6", "E4", 34, 26, up=False, part="harp")
    sg_.sync("'掰开': the bread breaks" + (" (picture)" if t_bk is not None else ""), q_b, t_b)
    br.mel("kalimba", "r:3 | E5:1/2 G#5:1/2 F#5:1/2 A5:3/2", vel=40)
    lv(br, ["pz_hi"], -14)
    lv(br, ["harp"], -16)
    lv(br, ["kalimba"], -15)
    br.expr(["vla", "vln1", "vc"], [(0, -25), (6, -24)])
    # 'the disciples passed it to everyone; the fish too': five notes on the guitar, the fish on pizzicato and celesta
    sh.mel("guitar", BOY[0], vel=44, transpose=-12)
    sh.mel("celesta", "r:3 | B5:3/2 F#5:3/2", vel=38)
    for nm, q_ in (("B3", 3.0), ("F#4", 4.5)):
        sh.add("pz_hi", q_, 0.5, nm, 40, "arp", "s")
    sh.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    rock(sh, 0, 6, part="harp", lo=40, hi=64, vel=24)
    sh.duck(2.0, parts=["guitar", "celesta"])
    ease(sh, ["guitar"], -15, drop=7)
    lv(sh, ["celesta"], -16)
    lv(sh, ["pz_hi"], -15)
    lv(sh, ["harp"], -18)
    sh.expr(["vla", "vln1", "vc"], [(0, -25), (6, -24)])
    # 'shared and shared -- the bread never ran out, nor the fish': the round, his theme in canon, bar by bar
    rd.mel("kalimba", bars(BOY, 0, 2) + " | G#5:1/2 B5:1/2 A5:1/2 C#6:1 B5:1/2", vel=46)   # bar 3: his motif a
    # third higher (growing), in thirds and tenths over the harp's entry
    rd.mel("celesta", "r:3 | " + bars(BOY, 0, 2), vel=40, transpose=12, role="fx")
    rd.mel("harp", "r:3 | r:3 | " + BOY[0], vel=40, transpose=-12, role="fx")
    for q_ in np.arange(0, 9, 1.5):                          # the guitar strums from bar 2
        if q_ >= 3.0:
            strum(rd, q_, 52, 71, vel=32, part="guitar", n=4, dq=1.0)
    for q_ in np.arange(6.0, 9.0, 0.5):                      # the pizzicato joins in bar 3
        rd.add("pz_lo" if abs(q_ % 1.5) < 1e-6 else "pz_hi", q_, 0.25,
               rd.chord_at(q_ + 1e-3).bass_note(40, 52) if abs(q_ % 1.5) < 1e-6 else
               rd.chord_at(q_ + 1e-3).tones(56, 68)[int(q_ * 2) % 3], 34, "arp", "s")
    rd.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    hdrum(rd, 3.0, 9.0, vel=26)
    rd.duck(3.0, parts=["kalimba", "celesta", "harp"])
    rd.expr(["kalimba"], [(0, -20), (1.0, -15), (9, -13)])
    rd.expr(["celesta"], [(3, -19), (9, -16)])
    rd.expr(["harp"], [(6, -18), (9, -16)])
    rd.expr(["guitar"], [(3, -20), (9, -17)])
    lv(rd, ["pz_lo", "pz_hi"], -16)
    lv(rd, "hand", -22)
    rd.expr(["vla", "vln1", "vc"], [(0, -26), (9, -22)])
    # 'everyone ate as much as they wanted': abundance -- la do' ti on the violins and cello, the horn, sweeps up
    pl.mel("vln_mel", "C#5:1 E5:1/2 D#5:3/2", vel=42, transpose=12)
    pl.mel("cello", "C#5:1 E5:1/2 D#5:3/2", vel=44, transpose=-12)
    pl.mel("horn", "E4:3/2 D#4:3/2", vel=38, role="counter")
    strings(pl, vel=32, lo=52, hi=73, bass=(40, 52), cb=(28, 40))
    sweep(pl, 0.05, 0.5, "A4", "A6", 24, 34, part="harp")
    sweep(pl, 1.55, 0.5, "B4", "B6", 26, 36, part="kalimba")
    pl.duck(3.0, parts=["vln_mel", "cello", "horn"])
    pl.expr(["vln_mel"], [(0, -21), (3, -19)])
    pl.expr(["cello"], [(0, -20), (3, -18)])
    pl.expr(["horn"], [(0, -24), (3, -21)])
    pl.expr(STR, [(0, -24), (3, -21)])
    lv(pl, ["harp", "kalimba"], -16)
    t_fish = pic(c, "crunch", "然后，他把饼掰开", 1)
    if t_fish is not None and t_fish < t_round:
        accent(c, segs, t_fish, None, pluck=(55, 67), vel=36)
    shares = pick_times(pics(c, "pop"), t_round - 0.3, t_all)
    if shares:                                              # each share: a pizzicato pluck climbing the chord
        climb(c, segs, shares, part="pz_hi", lo=59, hi=76, vel=42, sync=(0, len(shares) - 1),
              what="a share", glock=False)
    follow(c, segs, "sparkle", t_share - 0.3, c.dur - 0.1, glock=(86, 98), vel=32)
    t_eat = pic(c, "crunch", "分啊分", 0)
    if t_eat is not None:                                   # everyone eats (a soft pluck)
        accent(c, segs, t_eat, None, pluck=(60, 72), vel=34)
    for sg in segs:
        if sg not in (rd, th, sh):
            lv(sg, ["glock", "celesta"], -14)


def baskets(c):
    """Twelve baskets (E).  Full and content: the E of abundance lands with the page, a contented bassoon, harp and
    pizzicato (6/8), the abundance's ti resolving to do' on the violins and cello; A on '把剩下的碎块' (change): the
    cello; '门徒们去收' (change): the leftovers gathered (pizzicato climbing the A chord on the picture's rustles), then
    the twelve baskets -- on the picture a quick run up the scale A4 ... D#6 over B7 (kalimba, glockenspiel) on the first
    eleven pops and the high E, the warm full cadence, on the twelfth (without it eleven slower steps over a rising A,
    E/G#, F#m7, B7 and the cadence at '比原来的五个饼'), timpani and tremolo strings swelling; the hillside song in full
    strings and horn; wonder on '大家都好惊讶' (change): the boy's theme counted on the celesta over E/G#, hanging on
    B7sus4; '大家都说' (change): the song on the horn, to a half cadence; '小男孩看着满满的篮子' (change): his theme on the
    kalimba, a glint as he smiles (the picture's chime)."""
    c.gain(-3.0)
    t_jesus = c.gap(c.find("把剩下的碎块"))
    t_gath = c.gap(c.find("门徒们去收"))
    t_full = c.at("比原来的五个饼")
    t_wow = c.gap(c.find("大家都好惊讶"))
    # the twelve baskets: the picture's twelve pops (the twelfth is the cadence), else spread from the first 收
    i_g = c.find("门徒们去收")
    bk = pick_times(pics(c, "pop"), c.ls(i_g) - 0.3, c.le(i_g))
    on_pic = len(bk) >= 12 and t_gath + 0.6 < bk[11] < t_wow - 0.6
    if on_pic:
        t_full = bk[11]
    t_say = c.gap(c.find("大家都说"))
    t_boy = c.at("小男孩看着满满的篮子")
    fd = c.seg(0, t_jesus, 2, "6/8", "E major", nominal=None, label="baskets-fed")
    js = c.seg(t_jesus, t_gath, 2, "6/8", "E major", nominal=None, label="baskets-jesus")
    ga = c.seg(t_gath, t_full, 3, "2/4", "E major", nominal=None, label="baskets-gather")
    fl = c.seg(t_full, t_wow, 1, "6/8", "E major", nominal=None, label="baskets-full")
    wo = c.seg(t_wow, t_say, 3, "6/8", "E major", nominal=None, label="baskets-wonder")
    sy = c.seg(t_say, t_boy, 2, "6/8", "E major", nominal=None, label="baskets-praise")
    bo = c.seg(t_boy, c.dur, 2, "6/8", "E major", nominal=None, label="baskets-smile")
    segs = (fd, js, ga, fl, wo, sy, bo)
    for sg in segs:
        sg.duck(1.5)
    fd.prog("E:3 | C#m7:3/2 B7sus4:3/2")
    js.prog("A:3 | E/G#:3/2 E7:3/2@A-major")
    # the climb: on the picture, A while the leftovers are gathered and a quick run up over B7 on the first eleven
    # baskets; without it eleven slower steps from the first 收 over a rising A, E/G#, F#m7, B7
    t_c0 = voice_at(c, "收啊收")
    if on_pic:
        steps_t = bk[:11]
    else:
        steps_t = spread(t_c0, t_full - (t_full - t_c0) / 11.0, 11)
    steps_t = [min(max(t_, t_gath + 0.1), t_full - 0.05) for t_ in steps_t]
    for k_ in range(1, len(steps_t)):
        steps_t[k_] = max(steps_t[k_], steps_t[k_ - 1] + 0.05)
    if on_pic:
        prog48(ga, ["A", "B7"], edges48(ga, c, [steps_t[0] - 0.15]))
    else:
        prog48(ga, ["A", "E/G#", "F#m7", "B7"], edges48(ga, c, [steps_t[4], steps_t[8], steps_t[10]]))
    fl.prog("E:3")
    wo.prog("A:3 | E/G#:3 | F#m7:3/2 B7sus4:3/2")
    sy.prog(HILL_PROG[0] + " | " + HILL_PROG[3])
    bo.prog(" | ".join(BOY_PROG))
    js.sync("'把剩下的碎块': A", 0, t_jesus, kind="change")
    ga.sync("'门徒们去收': the gathering (A)", 0, t_gath, kind="change")
    fl.sync("twelve baskets full (E)" + (" (picture)" if on_pic else ""), 0, t_full, kind="change")
    wo.sync("'大家都好惊讶': wonder (A)", 0, t_wow, kind="change")
    sy.sync("'大家都说': the song (E)", 0, t_say, kind="change")
    bo.sync("'小男孩看着满满的篮子': the boy's theme (E)", 0, t_boy, kind="change")
    # 'everyone ate until they were full': E with the page, a contented bassoon, harp, pizzicato
    fd.mel("vln_mel", "E6:3 | r:3", vel=36)                 # la do' ti -- do': the abundance resolves with the page
    fd.mel("cello", "E4:3 | r:3", vel=40)
    fd.expr(["vln_mel"], [(0, -21), (3, -28)])
    fd.expr(["cello"], [(0, -20), (3, -27)])
    fd.mel("bsn", "G#3:1 F#3:1/2 E3:3/2 | r:3/2 F#3:3/2", vel=42)
    rock(fd, 0, 6, part="harp", lo=40, hi=66, vel=28)
    strings(fd, vel=30, lo=52, hi=73, bass=(40, 52), cb=(28, 40))
    for q_ in (0.0, 1.5, 3.0, 4.5):
        fd.add("pz_lo", q_, 0.5, fd.chord_at(q_ + 1e-3).bass_note(40, 52), 32, "arp", "s")
    fd.duck(2.0, parts=["bsn"])
    fd.expr(["bsn"], [(0, -19), (1, -16), (6, -17)])
    lv(fd, ["harp"], -17)
    lv(fd, ["pz_lo"], -15)
    fd.expr(STR, [(0, -22), (1.5, -23), (6, -24)])
    follow(c, segs, "pop", 0.1, t_jesus - 0.2, pluck=(52, 64), vel=30)
    # 'gather the leftovers, let nothing be wasted': A, the cello
    js.mel("cello", "A4:1 C#5:1/2 B4:1 A4:1/2 | B4:3/2 G#4:1 D5:1/2", vel=44)
    rock(js, 0, 6, part="harp", lo=40, hi=66, vel=26)
    strings(js, vel=28, lo=52, hi=71, bass=(40, 52), cb=None)
    js.duck(2.0, parts=["cello"])
    lv(js, ["cello"], -15)
    lv(js, ["harp"], -17)
    js.expr(STR, [(0, -25), (6, -24)])
    # 'they gathered and gathered ... twelve baskets full!': the climb, eleven steps -- the twelfth is the cadence
    climb_n = ["A4", "B4", "C#5", "D#5", "E5", "F#5", "G#5", "A5", "B5", "C#6", "D#6"]
    tune(c, segs, steps_t, climb_n, part="kalimba", vel=42, role="fx",
         what=None if on_pic else "a basket is filled", sync=() if on_pic else (0, 5, 10),
         glock=(0, 3, 7) if on_pic else (0, 2, 4, 6, 9, 10))
    gath = pick_times(pics(c, "crunch"), t_gath, steps_t[0] - 0.2)
    if gath:                                                # the leftovers gathered: pizzicato climbing the A chord
        for t_ in gath:
            clear_near(c, t_)
        climb(c, segs, gath, part="pz_hi", lo=57, hi=81, vel=40, glock=False)
    ga.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 74, vel=28, bass_ref=(40, 52))
    bassline(ga, "vc", 40, 52, 30)
    bassline(ga, "pz_cb", 28, 40, 34)
    q_t0 = ga.q_of(c.t0 + steps_t[6])
    for k_, q_ in enumerate(np.arange(q_t0, ga.n_q - 0.05, 1 / 8)):     # a timpani roll swelling to the twelfth
        ch = ga.chord_at(q_ + 1e-3)
        ga.add("timp", q_, max(0.05, min(1 / 8, span_end(ga, q_ + 1e-6) - q_ - 0.01)),
               [p for p in range(40, 53) if p % 12 in ch.pcset][0], 20 + k_ * 0.6, "timp")
    ga.expr(["trem_va", "trem_hi"], [(0, -27), (ga.n_q, -20)])
    ga.expr(["vc"], [(0, -26), (ga.n_q, -21)])
    lv(ga, ["pz_cb"], -15)
    ga.expr(["timp"], [(0, -24), (ga.n_q, -17)])
    lv(ga, ["kalimba"], -12)
    # 'more than the five loaves they started with!': the twelfth step -- E, full strings, horn, the song
    t_12 = None
    clear_near(c, t_full - 0.06, win=0.1, roles=("fx",))
    fl.add("kalimba", 0, 1.5, "E6", 50, "arp", "h")
    fl.add("glock", 0, 1.5, "E7", 44, "arp", "h")
    for nm in ("E3", "B3", "G#4"):
        fl.add("pz_lo" if nm == "E3" else "pz_hi", 0, 0.5, nm, 48, "arp", "h")
    fl.add("okit", 0, 1, 57, 24, "perc", "h")
    fl.add("timp", 0, 1.0, "E3", 40, "timp", "h")
    fl.add("pz_cb", 0, 1.0, "E1", 44, "bass", "h")
    fl.sync("the twelfth basket: the full cadence (E)" + (" (picture)" if on_pic else ""), 0, t_full)
    for t_ in pick_times(pics(c, "pop"), t_full + 0.3, t_wow - 0.2):     # the loaves compared (soft glints)
        accent(c, segs, t_, None, celesta=(79, 91), vel=30)
    if t_12 is not None and abs(t_12 - t_full) > 0.12:
        accent(c, segs, t_12, "the twelfth basket (a glint)", glock=(86, 98), vel=38)
    fl.mel("vln_mel", HILL[4], vel=42, transpose=12)
    fl.mel("cello", HILL[4], vel=44)
    fl.mel("horn", "G#3:3", vel=38, role="counter")
    strings(fl, vel=34, lo=52, hi=73, bass=(40, 52), cb=(28, 40))
    sweep(fl, 0.05, 0.6, "E4", "E6", 26, 38, part="harp")
    fl.duck(3.0, parts=["vln_mel", "cello", "horn"])
    fl.expr(["vln_mel"], [(0, -19), (3, -17)])
    fl.expr(["cello"], [(0, -18), (3, -16)])
    lv(fl, ["horn"], -20)
    fl.expr(STR, [(0, -19), (3, -21)])
    lv(fl, ["kalimba"], -12)
    lv(fl, ["timp", "pz_cb", "pz_lo", "pz_hi"], -13)
    lv(fl, "okit", -21)
    lv(fl, ["harp"], -16)
    # 'everyone was amazed: five loaves and two fish -- how could they fill so many?': the count on the celesta
    o5, o2 = syl(c, "五个饼、两条鱼", 2)
    wow_t = [o5 + 0.15 * k for k in range(5)] + [o2, o2 + 0.3]
    q_hi = wo.n_q - 3.2
    wow_t = [min(t_, wo.t(q_hi) - c.t0) for t_ in wow_t]
    for k_ in range(1, len(wow_t)):
        wow_t[k_] = max(wow_t[k_], wow_t[k_ - 1] + 0.08)
    e0 = max(wow_t[0] - 0.12, wo.t(0.3) - c.t0)
    e1 = wow_t[-1] + 0.45
    t_q = c.at("怎么能让这么多人吃饱呢")
    wo.chords.clear()
    prog48(wo, ["A", "E/G#", "F#m7", "B7sus4"], edges48(wo, c, [e0, max(e1, e0 + 0.5), max(t_q + 0.9, e1 + 0.6)]))
    tune(c, segs, wow_t, [midi(x) + 12 for x in BOY_NOTES], part="celesta", vel=40, role="fx", clear=False)
    wo.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    rock(wo, 0, 9, part="harp", lo=40, hi=66, vel=24)
    lv(wo, ["celesta"], -15)
    lv(wo, ["harp"], -18)
    wo.expr(["vla", "vln1", "vc"], [(0, -25), (9, -23)])
    # 'everyone said: Jesus must be sent by God!': the song on the horn, warm strings
    sy.mel("horn", HILL[0] + " | " + HILL[3], vel=46)
    strings(sy, vel=30, lo=52, hi=71, bass=(40, 52), cb=(28, 40))
    rock(sy, 0, 6, part="harp", lo=40, hi=66, vel=26)
    hdrum(sy, 0, 6, vel=24)
    sy.duck(2.5, parts=["horn"])
    sy.expr(["horn"], [(0, -21), (1, -17), (6, -17)])
    lv(sy, ["harp"], -17)
    lv(sy, "hand", -22)
    sy.expr(STR, [(0, -24), (6, -22)])
    # 'the little boy looked at the full baskets, and smiled': his theme on the kalimba, a glint as he smiles
    bo.mel("kalimba", bars(BOY, 0, 2), vel=48)
    rock(bo, 0, 6, part="guitar", lo=40, hi=64, vel=26)
    bo.pad(["vla", "vla", "vln1"], 3, 52, 71, vel=26, bass_part="vc", bass_lo=40, bass_hi=52)
    bo.duck(2.5, parts=["kalimba"])
    lv(bo, ["kalimba"], -13)
    lv(bo, ["guitar"], -18)
    bo.expr(["vla", "vln1", "vc"], [(0, -25), (6, -23)])
    t_sm, ok_sm = lead(c, segs, "chime", "大家都说", 0, bo.t(3.5) - c.t0, c.dur - 0.15,
                       "the boy smiles (a glint)", glock=(86, 98), vel=38)
    if ok_sm:
        sg_, q_s = seg_at(c, segs, t_sm)
        sg_.add("glock", q_s, _dq(sg_, q_s, 1.0), top(sg_, q_s, 86, 98), 38, "arp", "h")
        sg_.sync("the boy smiles (a glint)", q_s, t_sm)
    else:
        bo.add("glock", 4.5, 1.5, "G#6", 34, "arp", "h")
    for sg in segs:
        lv(sg, ["glock", "celesta"], -14)


def end(c):
    """The modern frame again (A -> E).  '五个饼、两条鱼' -- the boy's theme counted, tiny, on the kalimba in A, three tiny
    notes for '一点点', over the ukulele and the piano; E on '可是在耶稣手里' (change): the hillside song on the cello,
    strings opening, a harp sweep on '好多好多'; '耶稣看见大家饿了' (change): the song's second half -- home on '他也会照顾
    你'; A on '小朋友，你有什么好东西' (change), very soft; B7sus4 at the end of the question (change), hanging through
    the answer pause (the kalimba asks once); the final E chord on the end card."""
    c.gain(-3.5)
    t_lot = c.at("可是在耶稣手里")
    t_care = c.gap(c.find("耶稣看见大家饿了"))
    t_q = c.gap(c.find("小朋友，你有什么好东西"))
    t_f = c.le(c.find("小朋友，你有什么好东西"))
    t_raw = pic(c, "chime", "小朋友，你有什么好东西")
    t_card = t_raw if t_raw is not None and t_f + 0.5 <= t_raw <= c.dur - 0.6 else None
    t_fin = t_card if t_card is not None else max(t_f + 0.8, c.dur - 2.8)
    sm = c.seg(0, t_lot, 3, "6/8", "A major", nominal=None, label="end-little")
    lt = c.seg(t_lot, t_care, 2, "6/8", "E major", nominal=None, label="end-lots")
    ca = c.seg(t_care, t_q, 4, "6/8", "E major", nominal=None, label="end-care")
    q = c.seg(t_q, t_f, 2, "6/8", "E major", nominal=None, label="end-question")
    sp = c.seg(t_f, t_fin, 1, "6/8", "E major", nominal=None, label="end-space")
    f = c.seg(t_fin, c.dur, 1, "6/8", "E major", nominal=None, rit=0.3, label="end-final-chord")
    segs = (sm, lt, ca, q, sp, f)
    for sg in (sm, lt, ca, q):
        sg.duck(1.5)
    sm.prog("A:3 | A:3 | Bm7:3/2 E7sus4:3/2")
    lt.prog(" | ".join(HILL_PROG[0:2]))
    ca.prog("A:3 | E/B:3/2 B7:3/2 | F#m7:3/2 B7:3/2 | E:3")
    q.prog("A:3 | F#m:3")
    sp.prog("B7sus4:3")
    f.prog("E:3")
    lt.sync("'可是在耶稣手里': E", 0, t_lot, kind="change")
    ca.sync("'耶稣看见大家饿了': A", 0, t_care, kind="change")
    q.sync("'小朋友，你有什么好东西': the last question (A)", 0, t_q, kind="change")
    sp.sync("'可以分给别人呢': B7sus4, the question hangs", 0, t_f, kind="change")
    f.sync("the final E chord (the end card)", 0, t_fin, kind="change")
    f.sync("the end card: the final chord" if t_card is not None else "the final chord", 0, t_fin)
    # 'child, five loaves and two fish look like only a little': the count on the kalimba in A, '一点点' tiny
    i_s = c.find("五个饼、两条鱼")
    pp = pick_times(pics(c, "pop"), c.ls(i_s) - 0.3, c.at("看起来只有一点点"))
    on_pp = len(pp) >= 7
    if on_pp:                                               # the picture's loaves (the first five) and fish (the last two)
        cnt = pp[:5] + pp[-2:]
    else:
        o5, o2 = syl(c, "五个饼、两条鱼", 2)
        cnt = [o5 + 0.15 * k for k in range(5)] + [o2, o2 + 0.3]
    cnt = [min(t_, sm.t(5.6) - c.t0) for t_ in cnt]
    for k_ in range(1, len(cnt)):
        cnt[k_] = max(cnt[k_], cnt[k_ - 1] + 0.08)
    tune(c, segs, cnt, [midi(x) - 7 for x in BOY_NOTES], part="kalimba", vel=42, role="fx", clear=False,
         what="a loaf / a fish (picture)" if on_pp else None, sync=(0, 6) if on_pp else ())
    for t_ in (pp[5:-2] if on_pp else []):                  # the basket between them (a soft harp note)
        accent(c, segs, t_, None, harp=(64, 76), vel=30)
    t_dd = voice_at(c, "看起来只有一点点") + 0.55
    sg_, q_d = seg_at(c, segs, t_dd)
    if sg_ is sm:
        for k_ in range(3):
            qq = q_d + 0.25 * k_
            if qq < sm.n_q - 0.2:
                sm.add("kalimba", qq, 0.25, sm.chord_at(qq + 1e-3).tones(84, 96)[-1 - k_ % 2], 32, "arp", "S")
    for q_ in np.arange(0, 9, 1.5):                          # the ukulele
        strum(sm, q_, 57, 76, vel=32, part="uke", n=4, dq=1.0)
        if not bool(sm.score.speaking(sm.t(q_ + 1.0))):
            strum(sm, q_ + 1.0, 57, 76, vel=26, part="uke", n=3, down=False, dq=0.5)
    sm.mel("mpiano", "r:3 | r:3 | D5:3/2 E5:3/2", vel=40)
    sm.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_part="vc", bass_lo=38, bass_hi=50)
    lv(sm, ["kalimba"], -15)
    sm.expr(["uke"], [(0, -23), (1.5, -16), (9, -15)])
    lv(sm, ["mpiano"], -16)
    sm.expr(["vla", "vln1", "vc"], [(0, -27), (9, -24)])
    # 'but in Jesus's hands a little can become lots and lots!': E, the hillside song on the cello, strings open out
    lt.mel("cello", bars(HILL, 0, 2), vel=48)
    strings(lt, vel=30, lo=52, hi=73, bass=(40, 52), cb=(28, 40))
    rock(lt, 0, 6, part="harp", lo=40, hi=66, vel=28)
    hit(c, segs, "chime", "可是在耶稣手里", 0, "in Jesus's hands (a glint)", glock=(86, 98), vel=40)
    many = pick_times(pics(c, "pop"), c.at("可是在耶稣手里"), t_care)
    if len(many) >= 3:                                      # a little becomes lots: the kalimba climbs on each pop
        for t_ in many:
            clear_near(c, t_)
        climb(c, segs, many, part="kalimba", lo=76, hi=93, vel=40, sync=(0, len(many) - 1),
              what="it multiplies", glock=True)
        t_gl = pic(c, "sparkle", "可是在耶稣手里", 0)
        if t_gl is not None and t_gl > many[-1] + 0.15:
            accent(c, segs, t_gl, None, glock=(86, 98), vel=34)
    else:
        t_lots = voice_at(c, "一点点也能变成好多好多") + 0.9
        sg_, q_o = seg_at(c, segs, t_lots)
        if sg_ is lt:
            sweep(lt, q_o, 0.6, "E5", "E7", 22, 32, part="celesta")
    lt.duck(2.5, parts=["cello"])
    lt.expr(["cello"], [(0, -20), (1.0, -14), (6, -14)])
    lv(lt, ["harp"], -16)
    lt.expr(STR, [(0, -25), (6, -22)])
    # 'Jesus saw they were hungry; he loved them and cared for them; he knows what you need, and he will care for you'
    ca.mel("cello", HILL[2] + " | " + HILL[3] + " | " + HILL[6] + " | " + HILL[7], vel=46)
    strings(ca, vel=30, lo=52, hi=72, bass=(40, 52), cb=(28, 40))
    rock(ca, 0, 12, part="harp", lo=40, hi=66, vel=26)
    follow(c, segs, "sparkle", t_care, t_q, glock=(86, 98), vel=32)
    hit(c, segs, "chime", "耶稣看见大家饿了", 0, "he will care for you (a glint)", glock=(86, 98), harp=(71, 83),
        vel=40)
    ca.duck(3.0, parts=["cello"])
    lv(ca, ["cello"], -16)
    lv(ca, ["harp"], -17)
    ca.expr(STR, [(0, -25), (12, -25)])
    # 'child, what good thing could you share with someone?': very soft -- the ukulele, the piano
    for q_ in np.arange(0, 6, 1.5):
        strum(q, q_, 57, 76, vel=28, part="uke", n=4, dq=1.0)
    q.mel("mpiano", "C#5:3/2 B4:1 A4:1/2 | A4:3/2 C#5:3/2", vel=38)
    q.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=24, bass_part="vc", bass_lo=40, bass_hi=52)
    q.duck(2.0)
    lv(q, ["uke"], -17)
    lv(q, ["mpiano"], -17)
    q.expr(["vla", "vln1", "vc"], [(0, -25), (6, -26)])
    # the answer pause: B7sus4 hanging; the kalimba asks once
    sp.pad(["vla", "vla", "vln1"], 3, 52, 69, vel=24, bass_part="vc", bass_lo=40, bass_hi=52)
    strum(sp, 0.0, 59, 71, vel=24, part="uke", n=3, gap_s=0.06)
    sp.mel("kalimba", "r:1 E5:1/2 F#5:1/2 A5:1", vel=32)
    sp.expr(["vla", "vln1", "vc"], [(0, -23), (1.5, -24), (3, -25)])
    sp.expr(["uke"], [(0, -21), (3, -19)])
    lv(sp, ["kalimba"], -21)
    # the final E chord on the end card: the kalimba rolled up, harp, glockenspiel, the cello's low E, strings
    for k_, nm in enumerate(["E5", "G#5", "B5", "E6"]):
        f.add("kalimba", 0.06 * k_, 3 - 0.06 * k_, nm, 40 - 2 * k_, "arp", "r")
    roll_chord(f, 0.0, 40, 76, vel=34, part="harp", n=6)
    f.add("glock", 0, 2.0, "G#6", 32, "arp", "r")
    f.add("cello", 0, 3, "E3", 36, "harmony")
    strings(f, vel=28, lo=52, hi=71, bass=(40, 52), cb=(28, 40), q0=0.25)
    f.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -25), (0.75, -24), (2, -27), (3, -32)])
    f.expr(["kalimba", "harp", "glock"], [(0, -16), (3, -21)])
    lv(f, ["cello"], -20)
    if t_card is None and t_raw is not None:
        accent(c, segs, t_raw, "the end card (a glint)", glock=(86, 98), vel=36)
    for sg in segs:
        if sg not in (f, sp):
            lv(sg, ["glock", "celesta"], -14)


SCENE_CUES = {
    "s01_title": title, "s02_question": question, "s03_crowd": crowd, "s04_evening": evening, "s05_boy": boy,
    "s06_sit": sit, "s07_bless": bless, "s08_baskets": baskets, "s09_end": end,
}

# Hit points defined by the narration text (audio/music_check.py REQUIRED_HITS format: (scene, phrase, mode, kind)).
REQUIRED_HITS = [
    ("s02_question", "今天的故事里", "line", "change"),               # the story begins (E)
    ("s02_question", "可是，耶稣用这一点点饭", "phrase", "change"),   # C-sharp minor
    ("s02_question", "让好多好多人都吃饱了", "phrase", "change"),     # E
    ("s03_crowd", "有一天", "gap", "change"),                         # busy, busy
    ("s03_crowd", "我们到安静的地方", "gap", "change"),               # the quiet place (A)
    ("s03_crowd", "可是，好多人看见了", "phrase", "change"),          # the crowd sees them (C-sharp minor)
    ("s03_crowd", "比船还先到了", "end", "hit"),                      # ta-da: they got there first
    ("s03_crowd", "比船还先到了", "end", "change"),                   # E
    ("s03_crowd", "他们就像一群没有牧羊人的羊", "phrase", "change"),  # sheep without a shepherd
    ("s03_crowd", "耶稣就给大家讲上帝的事", "gap", "change"),         # teaching and healing
    ("s04_evening", "这里什么吃的都没有", "gap", "change"),           # worry (C-sharp minor)
    ("s04_evening", "你们给他们吃吧", "gap", "change"),               # E
    ("s04_evening", "门徒们吓了一跳", "gap", "change"),               # the startle
    ("s04_evening", "耶稣又问腓力", "phrase", "change"),              # the question (A)
    ("s04_evening", "耶稣这样问", "gap", "change"),                   # E
    ("s04_evening", "其实，耶稣自己早就知道", "phrase", "change"),    # the boy's theme, far off
    ("s04_evening", "腓力掰着手指", "gap", "change"),                 # Philip counts
    ("s04_evening", "就算花好多好多钱买饼", "gap", "change"),         # not enough
    ("s05_boy", "门徒们找啊找", "gap", "change"),                     # the search
    ("s05_boy", "彼得的兄弟安得烈", "phrase", "change"),              # Andrew brings the boy (E)
    ("s05_boy", "这里有个小孩子", "gap", "change"),                   # the counting game
    ("s05_boy", "可是，这么多人", "phrase", "change"),                # C-sharp minor
    ("s05_boy", "五个饼，两条鱼，只够", "gap", "change"),             # tiny
    ("s05_boy", "可是，小男孩把他带的饭", "phrase", "change"),        # the gift
    ("s06_sit", "那里有好多青草", "gap", "change"),                   # the hillside song
    ("s06_sit", "有的一百个人一组", "phrase", "change"),              # the groups
    ("s06_sit", "从高处看", "gap", "change"),                         # from above (A)
    ("s06_sit", "光是男人", "gap", "change"),                         # the whole hillside
    ("s07_bless", "抬头望着天", "phrase", "change"),                  # he looks up
    ("s07_bless", "感谢上帝", "phrase", "change"),                    # the Amen
    ("s07_bless", "然后，他把饼掰开", "gap", "change"),               # the breaking
    ("s07_bless", "门徒再分给大家", "phrase", "change"),              # passed on
    ("s07_bless", "分啊分", "gap", "change"),                         # the round
    ("s07_bless", "大家想吃多少", "phrase", "change"),                # abundance
    ("s08_baskets", "把剩下的碎块", "gap", "change"),                 # A
    ("s08_baskets", "门徒们去收", "gap", "change"),                   # the gathering
    ("s08_baskets", "大家都好惊讶", "gap", "change"),                 # wonder
    ("s08_baskets", "大家都说", "gap", "change"),                     # the song on the horn
    ("s08_baskets", "小男孩看着满满的篮子", "phrase", "change"),      # the boy's theme
    ("s09_end", "可是在耶稣手里", "phrase", "change"),                # E
    ("s09_end", "耶稣看见大家饿了", "gap", "change"),                 # the song's second half
    ("s09_end", "小朋友，你有什么好东西", "gap", "change"),           # the last question
    ("s09_end", "小朋友，你有什么好东西", "end", "change"),           # B7sus4: the question hangs
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or None,
# index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.
PICTURE_HITS = [
    ("s01_title", "chime", None, 0, 0.0, "hit", "the ribbon unfurls (a glint)"),
    ("s01_title", "pop", None, 0, 0.0, "hit", "title character 1 pops in (the celesta climbs)"),
    ("s01_title", "pop", None, 3, 0.0, "hit", "title character 4 pops in"),
    ("s01_title", "sparkle", None, 1, 0.0, "hit", "the finished title: ta-da"),
    ("s01_title", "sparkle", None, 1, 0.0, "change", "the finished title: E arrives with it"),
    ("s02_question", "cloth", None, 0, 0.0, "hit", "the lunchbox opens (a soft pluck)"),
    ("s02_question", "sparkle", None, 0, 0.0, "hit", "the lunch inside (a glint)"),
    ("s02_question", "sparkle", None, 1, 0.0, "hit", "a glint"),
    ("s02_question", "cloth", None, 1, 0.0, "hit", "the half is shared (a pluck)"),
    ("s02_question", "crunch", None, 0, 0.0, "hit", "a bite (a pizzicato crunch)"),
    ("s02_question", "chime", None, 0, 0.0, "hit", "both smile (a glint, the kalimba rolls)"),
    ("s03_crowd", "pop", "耶稣有十二个好朋友", 0, 0.0, "hit", "the first of the twelve friends pops in"),
    ("s03_crowd", "pop", "耶稣有十二个好朋友", 11, 0.0, "hit", "the twelfth friend (the climb's top)"),
    ("s03_crowd", "splash_small", "他们坐船", 0, 0.0, "hit", "the boat pushes off (a harp sweep)"),
    ("s03_crowd", "pop", "他们坐船", 0, 0.0, "hit", "the crowd sees them (a pluck)"),
    ("s03_crowd", "splash_small", "耶稣下了船", 0, 0.0, "hit", "Jesus steps ashore (a harp note)"),
    ("s03_crowd", "chime", "耶稣下了船", 0, 0.0, "hit", "his heart is full of love (a glint)"),
    ("s03_crowd", "chime", "耶稣就给大家讲上帝的事", 0, 0.0, "hit", "the sick are healed (a glint)"),
    ("s03_crowd", "sparkle", "耶稣就给大家讲上帝的事", 0, 0.0, "hit", "healing sparkles (the celesta)"),
    ("s04_evening", "whoosh", "门徒们吓了一跳", 0, 0.0, "hit", "the disciples jump (a jolt)"),
    ("s04_evening", "chime", "耶稣这样问", 0, 0.0, "hit", "he already knows (a glint)"),
    ("s04_evening", "coins", "就算花好多好多钱买饼", 0, 0.0, "hit", "lots and lots of money (a clink)"),
    ("s04_evening", "pop", "就算花好多好多钱买饼", 1, 0.0, "hit", "the first tiny bite (the celesta falls)"),
    ("s04_evening", "pop", "就算花好多好多钱买饼", 5, 0.0, "hit", "the fifth tiny bite"),
    ("s05_boy", "pop", "这里有个小孩子", 0, 0.0, "hit", "the first loaf is counted"),
    ("s05_boy", "pop", "这里有个小孩子", 4, 0.0, "hit", "the fifth loaf"),
    ("s05_boy", "pop", "这里有个小孩子", 6, 0.0, "hit", "the second fish"),
    ("s05_boy", "cloth", "可是，小男孩把他带的饭", 0, 0.0, "hit", "the boy hands over his lunch"),
    ("s06_sit", "pop", "有的一百个人一组", 0, 0.0, "hit", "a group of a hundred (a big low chord)"),
    ("s06_sit", "pop", "有的一百个人一组", 1, 0.0, "hit", "a group of fifty (a light high chord)"),
    ("s06_sit", "whoosh", "那里有好多青草", 0, 0.0, "hit", "the view rises (a harp sweep)"),
    ("s06_sit", "chime", "从高处看", 0, 0.0, "hit", "the little gardens glow (a glint)"),
    ("s06_sit", "grow", "光是男人", 0, 0.0, "hit", "the hillside fills (the celesta sweeps up)"),
    ("s06_sit", "sparkle", "光是男人", 0, 0.0, "hit", "five thousand (a timpani)"),
    ("s06_sit", "pop", "光是男人", 0, 0.0, "hit", "a child pops up (a kalimba ping)"),
    ("s07_bless", "chime", "抬头望着天", 0, 0.0, "hit", "he looks up to heaven (a glint)"),
    ("s07_bless", "chime", "抬头望着天", 1, 0.0, "hit", "the light: the Amen"),
    ("s07_bless", "crunch", "然后，他把饼掰开", 0, 0.0, "hit", "the bread is broken (a harp cascade)"),
    ("s07_bless", "pop", "分啊分", 0, 0.0, "hit", "the first share (a pluck)"),
    ("s07_bless", "pop", "分啊分", 3, 0.0, "hit", "the fourth share, the celesta joins the round"),
    ("s08_baskets", "pop", "门徒们去收", 11, 0.0, "hit", "the twelfth basket: the full cadence"),
    ("s08_baskets", "pop", "门徒们去收", 11, 0.0, "change", "the twelfth basket: E"),
    ("s08_baskets", "chime", "大家都说", 0, 0.0, "hit", "the boy smiles (a glint)"),
    ("s09_end", "pop", "五个饼、两条鱼", 0, 0.0, "hit", "the first loaf (the kalimba, in A)"),
    ("s09_end", "pop", "五个饼、两条鱼", 7, 0.0, "hit", "the second fish"),
    ("s09_end", "chime", "可是在耶稣手里", 0, 0.0, "hit", "in Jesus's hands (a glint)"),
    ("s09_end", "pop", "五个饼、两条鱼", 8, 0.0, "hit", "it multiplies (the kalimba climbs)"),
    ("s09_end", "pop", "五个饼、两条鱼", 11, 0.0, "hit", "it multiplies: the top"),
    ("s09_end", "chime", "耶稣看见大家饿了", 0, 0.0, "hit", "he will care for you (a glint)"),
    ("s09_end", "chime", "小朋友，你有什么好东西", 0, 0.0, "hit", "the end card: the final E chord"),
]
