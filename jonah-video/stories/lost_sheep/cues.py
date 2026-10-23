"""The background score for 迷失的羊 (Luke 15:1-7 with Matthew 18:12-14; ~4:02) -- one continuous piece in 12 cues.

Read by audio/score.py when the story is "lost_sheep" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework as the earlier scores (audio/scorekit.py,
audio/scorelib.py): every cue starts at its scene's global start, is planned in whole bars whose tempo follows the
real line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap), never to fixed times.  Hits that
show an on-screen action follow the PICTURE: picture() / pic() read the scene's own sound-effect cues at build time
(engine.loader.build_scene(...).sfx_cues) and pick them exactly as music_check picks a PICTURE_HITS target; hit() and
accent() put the attack wherever the cue falls, on tones of the chord sounding there, and lead() gives a moment's main
attack to the picture when it falls inside that moment's segment (the found arrival, the hug, heaven's light).  A
scene that does not build falls back to the narrator's voice: syl() / voice_at() measure the punctuation groups in
the recorded clip the way the scenes do (stories/noah/scenes/s01_title.py voice_marks: chunk anchors, then the pauses
that best match the character estimate), scaled to the line's length in the timeline -- the 咦 of s05 and s06, the
bleats of s07 and s09, the numbers of s06.  Phrases whose subtitle interpolation is off the voice (咦, 大家都不见了,
还是九十九只) follow the voice or the picture and are not REQUIRED_HITS.

Colour: a sunny pastoral folk film, unlike the seven earlier scores (Jonah's D-major sea, Daniel's Persian court in A
hijaz, David's G pipe tune, Noah's B-flat march, Joseph's D clarinet, the Storm's Galilean mixolydian folk, the
Nativity's E-flat carols and music box).  Jesus's story lives in A major (unused as a home key so far), in 6/8 and
2/4: a pennywhistle on the tunes, a squeezebox (accordion) oom-pah, a plucked mandolin, pizzicato basses, two
woodblocks for little hooves, and the lamb's own bell (General MIDI Tinker Bell); its night is F-sharp minor
(ocarina owl, soft tremolo, the hills echoing on the echo line).  The outer story sits a fifth lower, in D major: the
courtyard meal with a bandoneon, a nylon guitar and a tambourine (B minor and a stiff bassoon for the Pharisees),
and the modern child's lullaby on a kalimba over the guitar.  The village party is a jig (musette accordion, fiddle,
whistle, tambourine, claps).  Ten General MIDI voices the shared orchestra does not list are registered here for this
story only (_EXTRA): whistle, ocarina, accordion, Italian musette accordion, bandoneon, mandolin, kalimba, tinkle
(the bell), fiddle, and an ocarina and a whistle on the echo bus.  Every tune below is original; none opens with the
rising 3-5-8 of the earlier themes, and the Nativity's sol-mi' and Jonah's 3-2-1-5 are avoided.

Themes (q = quarter note)
  The shepherd's song (A major, 6/8; mi fa sol do' | re' do' ti sol -- a stepwise climb and a leap up the hill):
     b1 A      C#5 D5. E5 A5.        b5 A        C#5 D5. E5 A5.
     b2 E/G#   B5 A5. G#5 E5.        b6 D        A5 B5. A5 F#5.
     b3 F#m    F#5 E5. F#5 A5.       b7 D E7     F#5 A5. G#5 B5.
     b4 E      G#5 F#5. E5--         b8 A        A5---
     (the bass falls A G# F# E under b1-b4).  Whistle over the flock (s05), walking home (s09), the dance (s10);
     on the bandoneon in D for Jesus at the table (s03 '可是耶稣很欢迎他们', s11 -- Jesus is the shepherd); the head
     in D on the ocarina at sunset and on the whistle as he sets off (s06), on the kalimba for '上帝就像这个牧羊人'
     (s12); in F-sharp minor, dotted, as the shepherd whistles to keep going at night (s08: A B C# F# | G# F# E# C# |
     D C# D F# | E# D C#), and back in A major for '一定要找到它'.
  The lamb (A major, 6/8, mandolin with its bell): do mi re do sol, | la, do ti, re -- a skip about and a question:
     A5 C#6 B5 A5 E5 | F#5 A5. G#5 B5  (A | D E).  Curious in s05 (wandering up into D on '越走越远'), small and
     alone in F-sharp minor (F#5 A5 G#5 F#5 C#5 | D5 F#5. E#5 G#5) at '大家都不见了' and at dusk (s07), in B minor
     on its bell for '少了一只小羊' (s06), joyful in A when it is found and lifted to the high A (s09), high and
     bright for heaven's joy (s11).
  The lullaby (D major, 6/8, kalimba) -- the lamb's motif slowed: the child is the little lamb:
     D5 F#5 E5 D5 A4 | B4 D5. C#5 E5 | G5 F#5 E5 D5 B4 | C#5 D5 E5 A4--  (D | G A | G | A); the frame (s02, s12).
  The counting game (s06, 2/4): one pluck per number as it pops up, climbing the D major scale from D4 (一 两 三 and
     a fourth over a falling bass D C# B G), on up with the quick pops (数啊数), 97 98 99 = A5 B5 C#6 over D G A --
     and the hundredth note, the high D, never comes: A7/G hangs on '咦？'; the recount runs up twice as fast and
     lands on C#6 again with the big '99'; then a deflating bassoon and trombone (wah wah wah waaah) and the
     deceptive B minor on '少了一只小羊'.  When the lamb is found (s09) the mandolin finally runs up to the top A.
  The Pharisees (B minor, 2/4): a stiff staccato bassoon strut over marching pizzicato; the 'hmph' on 哼.

Cue table (scene: key / meter -- what the music does; picture hits in brackets)
  s01 title     A 6/8     the shepherd's song's head (whistle), mandolin, oom-pah, soft strings, the bell on the
                          last chord [the lamb's bleat, the title's glint, a mandolin step for title characters 1 and 4,
                          two sparkles]
  s02 question  D 6/8     the lullaby (kalimba, guitar); B minor on '找不到爸爸妈妈'; Em7 A7sus4 with a guitar
                          heartbeat, hanging through the pause; D on '今天' (change); the lamb's motif and its bell on
                          '故事里...走丢的小家伙' [the child, mum gone, the hug (a kalimba roll), the toy lamb's bell]
  s03 meal      D 2/4 -> E minor -> B minor -> D 6/8 -> B minor   the courtyard table song (bandoneon, guitar
                          oom-pah, tambourine); E minor on '来的人里' (change): a sly clarinet; B minor on '还有一些人'
                          (change): a lonely bandoneon sigh to A7; the shepherd's song in D on '可是耶稣很欢迎他们'
                          (change); B minor on '旁边站着几个法利赛人' (change): the bassoon strut; E minor on
                          '他们皱着眉头' (change): tremolo, tiptoe pizzicato; the 'hmph' on '哼' (hit), F#7 left hanging
                          [the six coins stacking up (a glockenspiel clink climbing for each), bread broken, the table
                          laughs (tambourine, a strum)]
  s04 story     G 6/8 -> D -> E7sus4   the deceptive G (kindness after F#7), the mandolin's tremolo rising; D on
                          '如果你有一百只羊' (change), strings under Jesus's voice, a run up for the hundred; E7sus4 on
                          '你会怎么做呢' (change), hanging into the page turn [the page pops open (a glint), a sheep in
                          the page (its bell), '丢了一只' (one bell note falling away), the page's whoosh (a run up),
                          a last glint]
  s05 flock     A 6/8     E7sus4 held through the page turn; the shepherd's song on '耶稣的故事里' (change); the
                          whole flock on '一百只羊' (change: strings, tremolo, a run up on E7); the morning walk on
                          '每天早上' (change: the song on the mandolin, woodblock hooves); the lamb's motif on
                          '有一只小羊' (change), up into D, a flute butterfly; E7sus4 on '一抬头' (change), a plucked
                          '咦？'; F-sharp minor and the bell alone on '大家都不见了' [he loves each one, a bleat of the
                          hundred (its bell), morning, a grazing bleat, the lamb's bell, the landing, 咦, everyone gone]
  s06 count     D 6/8 -> 2/4 -> B minor -> D 6/8   sunset (ocarina, the song in D, to A7); the counting game (above)
                          -- changes on '一只，两只', '数啊数，数啊数', '九十七', '数啊数……还是', '少了一只小羊'; E minor
                          and A on '我的小羊呢' (change: the horn rising); the song on the whistle on
                          '牧羊人把九十九只羊' (change) to C#7sus4 C#7 [the lamb's bell far away, the first count, 97,
                          99, '我再数一遍' (a plucked upbeat), the first quick recount pop, the big 99, '我要去找它']
  s07 alone     F# minor 6/8   the lamb's motif in minor on its bell (a celesta below), high strings; Bm7 on
                          '天黑了' (change), the wind's glissando on the picture's first gust, an owl (ocarina, hoo --
                          hoo) in the pause; F-sharp minor on '小羊好害怕' (change), a soft tremolo, each bleat echoed
                          by the hills (ocarina on the echo line); C#7 [the lamb alone (its bell)]
  s08 search    F# minor 2/4 -> A   the steady walk (pizzicato steps, mandolin off-beats) and the shepherd
                          whistling his song in minor; D A on '小羊！小羊！' (change), his call echoed by the hills in
                          the pause (whistle on the echo line, C#6 A5); the walk again, darker, on '找啊找' (change);
                          A major hope on '可是牧羊人一直找' (change), a rising bass D E F#m E [the first and fourth
                          stepping stones, the thorny bushes, he stops, determined]
  s09 found     A 6/8     a hush on '忽然' (change: E7sus4, high strings, far echoes of the bleats, then the bell
                          answers the lamb); F-sharp minor on '在一块大石头后面' (change), the bell trembling, a run up
                          the scale; A major on '找到了' (change; the arrival on the picture's sparkle: strings,
                          horns, accordion, timpani, a cymbal breath, glockenspiel, the bell, the whistle's high A --
                          the film's loudest three seconds); D on '牧羊人一点也没生气' (change), the lamb's motif
                          joyful, lifted to the high A on the shoulders; the song's cadence on '找到你了' (change),
                          hooves walking home [the bell answers, found, a bleat, the moon, onto his shoulders]
  s10 party     A 6/8 jig the vamp, the knock and the doors; the song on the musette on '和我一起高兴吧' (change);
                          the dance on '大家都好开心' (change: whistle, fiddle, musette, oom-pa-pa, tambourine, claps,
                          the bell) [the knock, two doors, '找到了！' cheered (a glint, tambourine)]
  s11 meaning   D 6/8     the courtyard (guitar, bandoneon); Jesus's words in B minor on '一个做错事的人' (change);
                          D on '天上也会这样' (change): heaven's light on the picture's chime (harp, high strings, choir
                          'ooh', glockenspiel, the bell high); the shepherd's song on the bandoneon on
                          '耶稣和这些人一起吃饭' (change); its second phrase, warm and full, on '在上帝眼里' (change),
                          cadencing in D [the page in his hands, heaven, '欢欢喜喜', like the shepherd, the lost lamb's
                          bell, in God's eyes, the first and sixth hearts popping up (a mandolin climb), '失去']
  s12 end       D 6/8     the song's head on the kalimba; the lullaby with the bell on '你，就是' (change); B minor on
                          '如果你做错了事' (change, the lamb's motif in minor); D on '我想回到你身边' (change); G on the
                          last question (change), very soft; A7sus4 at the end of '你想对牧羊人说什么呢' (change),
                          hanging; the final D chord on the end card (kalimba, guitar and bell together, then rolled)
                          [the toy lamb squeezed (its bell), God comes to find you, the toy lamb lifted, the end card]

All the music stays under the narration (Seg.duck, low expression levels, melodies ducked further); entrances fade in
over their first beat where a bass or a whistle would otherwise jump out; the loud moments (the found arrival, the
dance) live in the pauses and are short and child-safe; the night never turns frightening.
"""
import numpy as np

from audio.scorekit import PARTS, Part
from audio.scorelib import ChordTones, bassline, broken, drum, gliss, span_end
from audio.theory import midi

# ------------------------------------------------------------------------------------------- this film's colours
# General MIDI voices the shared orchestra (audio/scorekit.PARTS) does not list; registered here, for this story only,
# before any cue is written (the MIDI writer, the checks and the bus channel count read PARTS).
_EXTRA = [
    Part("whistle", 0, 78, "wind", -0.15, -6, 67, 98, attack=0.02, jitter=0.007, duck_db=2.5),
    Part("ocarina", 0, 79, "wind", 0.12, -3, 57, 91, attack=0.03, jitter=0.008, duck_db=2.5),
    Part("accordion", 0, 21, "wind", 0.22, -9, 41, 89, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.0),
    Part("musette", 8, 21, "wind", -0.22, -9, 53, 93, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.5),
    Part("bandoneon", 0, 23, "wind", -0.18, -7, 41, 86, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.0),
    Part("mandolin", 16, 25, "pluck", 0.3, -3, 55, 93, jitter=0.006, duck_db=2.0),
    Part("kalimba", 0, 108, "keys", -0.12, -1, 57, 96, jitter=0.006, duck_db=2.0),
    Part("tinkle", 0, 112, "keys", 0.28, -6, 72, 100, jitter=0.004, duck_db=2.5),
    Part("fiddle", 0, 110, "str_hi", 0.25, -6, 55, 96, attack=0.04, legato=0.02, jitter=0.008, duck_db=2.5),
    Part("echo_oca", 0, 79, "echo", 0.0, -5, 57, 91, jitter=0.0, duck_db=1.0),
    Part("echo_whis", 0, 78, "echo", 0.0, -8, 67, 98, jitter=0.0, duck_db=1.0),
]
for _p in _EXTRA:
    PARTS.setdefault(_p.name, _p)

# ------------------------------------------------------------------------------------------- themes (q = quarter)
# the shepherd's song (A major, 6/8): mi fa sol do' | re' do' ti sol | la sol la do' | ti la sol | ...
SHEP = ["C#5:1 D5:1/2 E5:1 A5:1/2", "B5:1 A5:1/2 G#5:1 E5:1/2", "F#5:1 E5:1/2 F#5:1 A5:1/2", "G#5:1 F#5:1/2 E5:3/2",
        "C#5:1 D5:1/2 E5:1 A5:1/2", "A5:1 B5:1/2 A5:1 F#5:1/2", "F#5:1 A5:1/2 G#5:1 B5:1/2", "A5:3"]
SHEP_PROG = ["A:3", "E/G#:3", "F#m:3", "E:3", "A:3", "D:3", "D:3/2 E7:3/2", "A:3"]
# the lamb (A major, 6/8; with its bell): do mi re do sol, | la, do ti, re -- a skip about, and a question
LAMB = ["A5:1/2 C#6:1/2 B5:1/2 A5:1 E5:1/2", "F#5:1/2 A5:1 G#5:1/2 B5:1"]
LAMB_PROG = ["A:3", "D:3/2 E:3/2"]
LAMB_MIN = ["F#5:1/2 A5:1/2 G#5:1/2 F#5:1 C#5:1/2", "D5:1/2 F#5:1 E#5:1/2 G#5:1"]        # small, at dusk
LAMB_MIN_PROG = ["F#m:3", "D:3/2 C#7:3/2"]
# the lullaby of the modern frame (D major, 6/8) -- the lamb's motif slowed: the child is the little lamb
LULL = ["D5:1/2 F#5:1/2 E5:1/2 D5:1 A4:1/2", "B4:1/2 D5:1 C#5:1/2 E5:1", "G5:1/2 F#5:1/2 E5:1/2 D5:1 B4:1/2",
        "C#5:1/2 D5:1/2 E5:1/2 A4:3/2", "D5:1/2 F#5:1/2 E5:1/2 D5:1 A4:1/2", "B4:1/2 D5:1/2 G5:1/2 F#5:1 E5:1/2",
        "E5:1/2 G5:1/2 F#5:1/2 E5:1 C#5:1/2", "D5:3"]
LULL_PROG = ["D:3", "G:3/2 A:3/2", "G:3", "A:3", "D:3", "G:3/2 D/F#:3/2", "Em7:3/2 A7:3/2", "D:3"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…—"          # the dashes of 咩——咩—— separate the two bleats
SOUND_CHARS = set()
_ONSETS = {}


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
        times = []
        for (p, g), (_, a_, b_) in zip(units, vg):
            times.append(a_)
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


def seg_at(c, segs, t):
    """(segment, q) of cue-relative time t among segs (a hit a hair before a chord change takes the new chord)."""
    for sg in segs:
        if sg.t0 - 1e-6 <= c.t0 + t < sg.t1 - 1e-6:
            q = min(max(sg.q_of(c.t0 + t), 0.0), sg.n_q - 1e-3)
            se = span_end(sg, q + 1e-6)
            if se - q < 0.01 and se < sg.n_q - 1e-3:
                q = se
            return sg, q
    sg = segs[0] if c.t0 + t < segs[0].t0 else segs[-1]
    return sg, (0.0 if sg is segs[0] and c.t0 + t < sg.t0 else sg.n_q - 0.1)


def accent(c, segs, t, what=None, glock=None, celesta=None, pluck=None, mando=None, bell=None, low=None, vel=46):
    """A picture hit at cue-relative time t on tones of the chord sounding there (glock / celesta / pizzicato /
    mandolin / the lamb's bell = (lo, hi) ranges: the highest chord tone in range; low=True: a soft low thump);
    synced if `what`."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if celesta:
        sg.add("celesta", q, _dq(sg, q, 1.0), top(sg, q, *celesta), vel - 6, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if mando:
        sg.add("mandolin", q, _dq(sg, q, 0.5), top(sg, q, *mando), vel + 2, "arp", "h")
    if bell:
        sg.add("tinkle", q, _dq(sg, q, 0.75), top(sg, q, *bell), vel - 2, "arp", "h")
    if low:
        thump(sg, q, vel=vel + 2)
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
    accent(c, segs, t, what, **kw)
    return None, False


def climb(c, segs, times, part="mandolin", lo=69, hi=91, vel=40, sync=(), what="", glock=True):
    """One note per picture cue, climbing the chord tones (a pluck for each pop); those whose index is in `sync` are
    louder and synced."""
    prev = lo - 1
    for k, t in enumerate(times):
        sg, q = seg_at(c, segs, t)
        ts = sg.chord_at(q + 1e-3).tones(prev + 1, hi) or sg.chord_at(q + 1e-3).tones(lo, hi)
        prev = ts[0]
        loud = k in sync
        sg.add(part, q, _dq(sg, q, 0.5), prev, vel + (8 if loud else 0), "arp", "h")
        if loud:
            if glock and prev + 12 <= 105:
                sg.add("glock", q, _dq(sg, q, 0.5), prev + 12, vel, "arp", "h")
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


def sweep(seg, q, dur_s=0.6, lo="A4", hi="A6", v0=30, v1=46, up=True, part="harp"):
    """A glissando (harp, or the mandolin's strummed run) over the chord at q."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1, scale=ChordTones(seg.chord_at(q + 1e-3)))


def roll_chord(seg, q, lo, hi, vel=46, gap_s=0.05, part="kalimba", n=6):
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


def oom(seg, q0, q1, vel=40, bass=(40, 52), hi=(57, 69), n=3, bpart="pz_lo", cpart="accordion", lively=False):
    """The village oom-pah: a plucked bass on every beat (the chord's bass, then its fifth while the chord stays), the
    accordion's chord on the off-beat (2/4: the 'and'; 6/8: the third eighth of each beat, both the second and the
    third when lively)."""
    beat = seg.beat_q
    offs = (0.5,) if seg.meter == "2/4" else ((0.5, 1.0) if lively else (1.0,))
    q, k, last = q0, 0, None
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        k = 0 if ch is not last else k + 1
        p = ch.bass_note(*bass) if k % 2 == 0 else _alt_bass(ch, *bass)
        seg.add(bpart, q, _dq(seg, q, beat * 0.6), p, vel, "arp", "s")
        for off in offs:
            qq = q + off
            if qq < q1 - 1e-6 and cpart:
                for pt in seg.chord_at(qq + 1e-3).tones(*hi)[:n]:
                    seg.add(cpart, qq, _dq(seg, qq, 0.4), pt, vel - 8, "arp", "s")
        last = ch
        q += beat


def clop(seg, q0, q1, vel=30, quiet_under_speech=True):
    """The flock's little hooves: a high and a low woodblock (6/8: a lilting tik . tok tik . tok; 2/4: on the beats);
    only the beats while a line is spoken."""
    pat = ((0.0, 76, 0), (1.0, 77, -6), (1.5, 76, -2), (2.5, 77, -6)) if seg.meter == "6/8" else \
        ((0.0, 76, 0), (1.0, 77, -4))
    bar = seg.bar_q
    b = int(q0 // bar)
    while b * bar < q1 - 1e-6:
        for off, key, dv in pat:
            q = b * bar + off
            if q0 - 1e-6 <= q < q1 - 1e-6:
                on_beat = abs((q + 1e-6) % seg.beat_q) < 2e-6
                if quiet_under_speech and not on_beat and bool(seg.score.speaking(seg.t(q))):
                    continue
                drum(seg, q, key, vel + dv)
        b += 1


def bell(seg, q, vel=40, lo=84, hi=98, n=2, gap=0.125):
    """The lamb's little bell: n quick chord tones falling from the highest in [lo, hi] (a tinkle)."""
    ts = seg.chord_at(q + 1e-3).tones(lo, hi)[::-1][:n]
    for k, p in enumerate(ts):
        qq = q + k * gap
        if qq < seg.n_q - 0.05:
            seg.add("tinkle", qq, _dq(seg, qq, 0.75), p, vel - 4 * k, "arp", "h" if k == 0 else "")


def trem(seg, part, q0, q1, pitch, vel, rate=0.125, role="arp"):
    """A mandolin tremolo: the same note re-plucked every `rate` q."""
    pitch = midi(pitch) if isinstance(pitch, str) else pitch
    q, k = q0, 0
    while q < q1 - 1e-6:
        seg.add(part, q, min(rate, q1 - q), pitch, vel + (3 if k % 2 == 0 else -3), role)
        q += rate
        k += 1


def count_pluck(sg, q, p, vel=50, glock=True, block=True):
    """One sheep counted: a mandolin and pizzicato pluck (and a glockenspiel ping two octaves up, a woodblock tick)."""
    sg.add("mandolin", q, _dq(sg, q, 0.5), p, vel, "arp", "h")
    sg.add("pz_hi", q, _dq(sg, q, 0.5), p, vel - 6, "arp", "h")
    if glock:
        g = p + 24 if p + 24 <= 105 else p + 12
        sg.add("glock", q, _dq(sg, q, 0.5), g, vel - 10, "arp", "h")
    if block:
        drum(sg, q, 76, vel - 16)


def run(seg, part, q0, notes, step, vel=40, role="melody", art=""):
    """A quick scale run: the given pitches, one every `step` q from q0."""
    out = []
    for k, nm in enumerate(notes):
        q = q0 + k * step
        if q < seg.n_q - 1e-6:
            out.append(seg.add(part, q, min(step, seg.n_q - q), nm, vel + k, role, art))
    return out


def echo_call(c, segs, t, names, gap_s, part="echo_oca", vel=44, dur_s=0.32):
    """A call that the hills echo back: the notes on the echo bus (0.5 s ping-pong repeats), from cue-relative t."""
    for k, nm in enumerate(names):
        sg, q = seg_at(c, segs, t + k * gap_s)
        q1 = sg.q_of(sg.t(q) + dur_s)
        sg.add(part, q, max(0.1, min(q1 - q, sg.n_q - q)), nm, vel - 3 * k, "arp", "h")


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """The spring hillside: the shepherd's song (whistle) over the mandolin, the accordion's oom-pah and soft
    strings (A major, 6/8), the lamb's bell on the last chord; the picture: the lamb's bleat (its bell), the title's
    glint, a mandolin step for each title character as it pops in, two sparkles."""
    c.gain(-8.5)
    s = c.seg(0, c.dur, 3, "6/8", "A major", nominal=120, label="title")
    s.duck(1.5)
    s.duck(3.5, parts=["whistle"])
    s.prog("A:3 | E/G#:3 | A:3")
    s.mel("whistle", SHEP[0] + " | B5:1 A5:1/2 G#5:1 B5:1/2 | A5:3", vel=46)
    broken(s, "mandolin", 0, 9, (0, 1, 2, 1, 2, 1), 62, 76, vel=38, thin=True)
    oom(s, 0, 9, vel=38, bass=(45, 57), hi=(57, 69))
    strings(s, vel=34, lo=55, hi=76, bass=(40, 52), cb=(28, 40))
    bell(s, 6.0, vel=42)
    segs = (s,)
    hit(c, segs, "chime", None, 0, "the title appears (a glint)", glock=(86, 98), vel=46)
    pops = [pic(c, "pop", None, k) for k in range(4)]
    if None not in pops:
        climb(c, segs, pops, part="mandolin", lo=69, hi=88, vel=44, sync=(0, 3), what="a title character pops in")
    hit(c, segs, "sparkle", None, 0, "the title sparkles", glock=(88, 100), vel=44)
    hit(c, segs, "sparkle", None, 1, "the title sparkles again", clear=False, glock=(86, 98), vel=40)
    hit(c, segs, "sheep", None, 0, "the little lamb bleats (its bell)", bell=(84, 98), vel=44)
    lv(s, ["whistle"], -15)
    lv(s, ["mandolin"], -13)
    lv(s, ["pz_lo"], -12)
    lv(s, ["accordion"], -20)
    s.expr(STR, [(0, -24), (1.5, -21), (9, -21)])
    lv(s, ["tinkle", "glock"], -12)


def question(c):
    """The modern frame: the lullaby on the kalimba over a nylon guitar and soft strings (D major, 6/8; its head is the
    lamb's motif), a glint for the child; B minor on '找不到爸爸妈妈' (a pluck as mum is gone); the worry
    ('心里是不是好着急') hangs on Em7 A7sus4 with a guitar heartbeat; D warm on '今天', a kalimba roll and the bell on
    the hug (the picture); the lamb's motif on '故事里，也有一个走丢的小家伙', the bell as the child hugs the toy lamb."""
    c.gain(-4.5)
    t_worry = c.at("心里是不是好着急")
    t_today = c.ls(c.find("今天"))
    h = c.seg(0, t_worry, 3, "6/8", "D major", nominal=97, label="question-lost")
    w = c.seg(t_worry, t_today, 1, "6/8", "D major", nominal=None, label="question-worry")       # a held question
    t = c.seg(t_today, c.dur, 3, "6/8", "D major", nominal=87, label="question-today")
    segs = (h, w, t)
    for sg in segs:
        sg.duck(1.5)
    h.prog("D:3 | G:3/2 A:3/2 | Bm:3")
    w.prog("Em7:3/2 A7sus4:3/2")
    t.prog("D:3 | D:3 | G:3/2 A:3/2")
    t.sync("'今天': the story begins (D)", 0, t_today, kind="change")
    # 'child, have you ever been lost?': the lullaby
    h.mel("kalimba", LULL[0] + " | " + LULL[1] + " | B4:1/2 D5:1/2 F#5:1/2 E5:1 D5:1/2", vel=50)
    broken(h, "guitar", 0, 9, (0, 2, 4, 2, 4, 2), 50, 62, vel=34, thin=True)
    h.pad(["vla", "vla", "vln1"], 3, 50, 67, vel=32, bass_ref=(40, 52))
    bassline(h, "vc", 40, 52, 32)
    h.duck(3.0, parts=["kalimba"])
    h.expr(["kalimba"], [(0, -15), (1.5, -13), (9, -13)])
    h.expr(["guitar"], [(0, -14), (1.5, -12), (9, -12)])
    h.expr(["vla", "vln1", "vc"], [(0, -22), (3, -21), (9, -20)])
    hit(c, segs, "sparkle", None, 0, "the child (a glint)", glock=(86, 98), vel=42)
    hit(c, segs, "pop", None, 0, "mum is gone (a pluck)", pluck=(59, 71), mando=(62, 74), vel=42)
    # 'are you worried?': a guitar heartbeat, the question hangs
    for k_ in range(6):
        q_ = 0.5 * k_
        w.add("guitar", q_, 0.5, top(w, q_, 52, 64), 34 + (4 if k_ % 3 == 0 else 0), "arp", "s")
    w.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    w.add("kalimba", 1.5, 1.5, "D6", 38, "arp")
    lv(w, ["guitar"], -12)
    lv(w, ["kalimba"], -14)
    w.expr(["vla", "vln1", "vc"], [(0, -20), (1.5, -20), (3, -21)])
    # 'today Jesus tells a story; in it there is a little one who got lost too': D warm -- the hug (a kalimba roll and
    # the bell, on the picture), the lamb's motif, the bell again for the toy lamb
    t_hug, ok = lead(c, segs, "cloth", None, 0, t_today - 0.05, t.t(2.6) - c.t0, "the hug (a pluck)",
                     pluck=(62, 74), vel=42)
    q_h = qpos(t, c, t_hug, 0.0, 2.6) if ok else 0.0
    roll_chord(t, q_h, 57, 81, vel=40 if ok else 34, part="kalimba")
    bell(t, q_h + 0.25, vel=36)
    if ok:
        t.sync("the hug (a kalimba roll)", q_h, t_hug)
    t.mel("kalimba", "r:3 | " + LULL[0] + " | " + LULL[1], vel=48)
    broken(t, "guitar", 0.5, 9, (0, 2, 4, 2, 4, 2), 50, 62, vel=32, thin=True)
    strings(t, vel=34, lo=50, hi=67, bass=(40, 52), cb=None)
    t.duck(3.0, parts=["kalimba"])
    lv(t, ["kalimba"], -12)
    lv(t, ["guitar"], -12)
    t.expr(STR, [(0, -21), (1.0, -19), (9, -20)])
    lv(t, ["tinkle"], -14)
    hit(c, segs, "sparkle", "今天", 0, "the toy lamb (its bell)", bell=(84, 98), vel=42)
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)


def meal(c):
    """The courtyard (D major, 2/4): a table song on the bandoneon over a guitar oom-pah and a light tambourine;
    E minor on '来的人里' -- the tax collectors' sly clarinet, a glockenspiel clink climbing for each coin the picture
    stacks up; B minor on '还有一些人', a lonely bandoneon sigh to A7; the shepherd's song (6/8, bandoneon) on
    '可是耶稣很欢迎他们' -- Jesus is the shepherd (a pluck as bread is broken, tambourine and a strum as the table
    laughs); B minor on '旁边站着几个法利赛人': a stiff staccato bassoon; a whisper (tremolo, tiptoe pizzicato) on
    '他们皱着眉头'; the 'hmph' on '哼' (bassoon, low pizzicato, guitar, a short bandoneon chord) and F#7 left hanging."""
    c.gain(-2.5)
    t_tax = c.gap(c.find("来的人里"))
    t_sin = c.gap(c.find("还有一些人"))
    t_wel = c.gap(c.find("可是耶稣很欢迎他们"))
    t_ph = c.gap(c.find("旁边站着几个法利赛人"))
    t_wh = c.at("他们皱着眉头")
    t_hm = c.ls(c.find("哼"))
    a = c.seg(0, t_tax, 4, "2/4", "D major", nominal=118, label="meal-crowd")
    b = c.seg(t_tax, t_sin, 5, "2/4", "E harmonic", nominal=111, label="meal-tax")
    s = c.seg(t_sin, t_wel, 4, "2/4", "D major", nominal=89, label="meal-sinners")
    w = c.seg(t_wel, t_ph, 3, "6/8", "D major", nominal=122, label="meal-welcome")
    p = c.seg(t_ph, t_wh, 6, "2/4", "B harmonic", nominal=101, label="meal-pharisees")
    z = c.seg(t_wh, t_hm, 3, "2/4", "B harmonic", nominal=112, label="meal-whisper")
    g = c.seg(t_hm, c.dur, 3, "2/4", "B harmonic", nominal=95, label="meal-hmph")
    segs = (a, b, s, w, p, z, g)
    for sg in segs:
        sg.duck(1.5)
    a.prog("D:2 | G:2 | A:2 | D:2")
    b.prog("Em:2 | Em:2 | Am:2 | B7:2 | Em:2")
    s.prog("Bm:2 | G:2 | Em7:2 | A7sus4:1 A7:1")
    w.prog("D:3 | A/C#:3 | G:3/2 A7:3/2")
    p.prog("Bm:2 | F#7:2 | Bm:2 | Em:2 | F#7:2 | Bm:2")
    z.prog("Em:2 | Em:2 | F#7:2")
    g.prog("Bm:2 | Em:2 | F#7:2")
    b.sync("'来的人里': the tax collectors (E minor)", 0, t_tax, kind="change")
    s.sync("'还有一些人': nobody liked them (B minor)", 0, t_sin, kind="change")
    w.sync("'可是耶稣很欢迎他们': the shepherd's song (D)", 0, t_wel, kind="change")
    p.sync("'旁边站着几个法利赛人': the Pharisees (B minor)", 0, t_ph, kind="change")
    z.sync("'他们皱着眉头': whispering (E minor)", 0, t_wh, kind="change")
    # the courtyard: a table song, a guitar oom-pah, a light tambourine in the pauses
    a.mel("bandoneon", "A4:1/2 B4:1/2 A4:1/2 F#4:1/2 | G4:1/2 B4:1/2 D5:1 | C#5:1/2 B4:1/2 A4:1/2 G4:1/2 | F#4:2",
          vel=46)
    oom(a, 0, 8, vel=40, bass=(40, 52), hi=(54, 66), cpart="guitar")
    a.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(40, 52))
    for q_ in np.arange(0.5, 8, 1.0):
        if not bool(a.score.speaking(a.t(q_))):
            drum(a, q_, 54, 30)
    a.duck(3.0, parts=["bandoneon"])
    a.expr(["bandoneon"], [(0, -19), (1, -16), (8, -16)])
    lv(a, ["pz_lo", "guitar"], -12)
    lv(a, "hand", -17)
    lv(a, ["vla", "vln2", "vln1"], -22)
    # 'the tax collectors, who took too much money': a sly staccato clarinet, tiptoe pizzicato, a coin glint
    b.mel("clar", "E4:1/2 G4:1/2 F#4:1/2 E4:1/2 | B4:1/2 r:1/2 B3:1/2 r:1/2 | A4:1/2 C5:1/2 B4:1/2 A4:1/2 | "
                  "D#4:1/2 F#4:1/2 A4:1 | G4:1 E4:1", vel=46, art="s")
    for q_ in range(10):
        ch = b.chord_at(q_ + 1e-3)
        b.add("pz_lo", q_, 0.5, ch.bass_note(40, 52) if q_ % 2 == 0 else _alt_bass(ch, 40, 52), 40, "arp", "s")
        b.add("pz_hi", q_ + 0.5, 0.5, ch.tones(59, 71)[q_ % 2], 32, "arp", "s")
    b.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(40, 52))
    i_tax = c.find("来的人里")
    coins = picture(c, "coins", c.ls(i_tax) - 0.3, c.le(i_tax) + 1.0) or []
    if coins:                                                # the coins stack up: a clink for each, climbing
        for t_ in coins:
            clear_near(c, t_)
        climb(c, segs, coins, part="glock", lo=83, hi=100, vel=38, sync=(0, len(coins) - 1),
              what="a coin on the stack", glock=False)
    else:
        b.add("glock", 2.0, 0.5, "B6", 40, "arp", "h")
    b.duck(2.5, parts=["clar"])
    lv(b, ["clar"], -16)
    lv(b, ["pz_lo", "pz_hi"], -12)
    lv(b, ["glock"], -13)
    lv(b, ["vla", "vln2", "vln1"], -23)
    # 'and people who had done many wrong things; nobody liked them': a lonely bandoneon sigh
    s.mel("bandoneon", "D5:1 C#5:1 | B4:2 | G4:1 F#4:1 | E4:1 C#4:1", vel=44)
    broken(s, "guitar", 0, 8, (0, 2, 4, 2), 47, 59, vel=30, thin=True)
    s.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    s.duck(2.5, parts=["bandoneon"])
    s.expr(["bandoneon"], [(0, -22), (1, -17), (8, -17)])
    s.expr(["guitar"], [(0, -17), (1, -13), (8, -13)])
    lv(s, ["vla", "vln2", "vln1", "vc"], -21)
    # 'but Jesus welcomed them and ate with them': the shepherd's song on the bandoneon (6/8), warm strings
    w.mel("bandoneon", "F#4:1 G4:1/2 A4:1 D5:1/2 | E5:1 D5:1/2 C#5:1 A4:1/2 | B4:1 D5:1/2 C#5:1 E5:1/2", vel=50)
    broken(w, "guitar", 0, 9, (0, 2, 4, 2, 4, 2), 50, 62, vel=34, thin=True)
    strings(w, vel=36, lo=50, hi=69, bass=(40, 52), cb=(28, 40))
    for q_ in (1.0, 2.5, 4.0, 5.5, 7.0, 8.5):
        if not bool(w.score.speaking(w.t(q_))):
            drum(w, q_, 54, 30)
    w.duck(3.0, parts=["bandoneon"])
    w.expr(["bandoneon"], [(0, -16), (1.5, -14), (9, -14)])
    lv(w, ["guitar"], -12)
    w.expr(STR, [(0, -21), (1.5, -19), (9, -19)])
    lv(w, "hand", -17)
    hit(c, segs, "crunch", "可是耶稣很欢迎他们", 0, "bread is broken (a pluck)", pluck=(62, 74), mando=(62, 74),
        vel=48)
    t_ch = pic(c, "cheer", "可是耶稣很欢迎他们")
    if t_ch is not None:                                     # everyone at the table laughs: tambourine and a strum
        clear_near(c, t_ch)
        sg_, q_c = seg_at(c, segs, t_ch)
        drum(sg_, q_c, 54, 40)
        for k_, pt in enumerate(sg_.chord_at(q_c + 1e-3).tones(52, 67)[:4]):
            sg_.add("guitar", q_c + 0.04 * k_, _dq(sg_, q_c + 0.04 * k_, 1.0), pt, 40 - k_, "arp", "h" if k_ == 0 else "")
        sg_.sync("the table laughs (tambourine, a strum)", q_c, t_ch)
    # the Pharisees: a stiff staccato bassoon over marching pizzicato
    p.mel("bsn", "B2:3/4 C#3:1/4 D3:1/2 B2:1/2 | F#3:1 F#2:1 | D3:3/4 E3:1/4 F#3:1/2 D3:1/2 | G3:1 E3:1 | "
                 "A#2:1/2 C#3:1/2 E3:1/2 C#3:1/2 | B2:1 r:1", vel=50, art="s")
    for q_ in range(12):
        ch = p.chord_at(q_ + 1e-3)
        p.add("pz_lo", q_, 0.5, ch.bass_note(42, 54), 40, "arp", "s")
    p.pad("bandoneon", 3, 50, 64, vel=34, bass_ref=(42, 54))
    p.pad(["vla", "vla", "vln1"], 3, 50, 66, vel=28, bass_ref=(42, 54))
    p.duck(2.5, parts=["bsn"])
    lv(p, ["bsn"], -14)
    lv(p, ["pz_lo"], -12)
    lv(p, ["bandoneon"], -22)
    lv(p, ["vla", "vln2", "vln1"], -24)
    # 'they frowned and whispered': tremolo and tiptoe pizzicato
    z.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 69, vel=32, bass_ref=(40, 52))
    for q_ in np.arange(0, 6, 0.5):
        z.add("pz_hi", q_, 0.25, top(z, q_, 55, 71, -1 - int(q_ * 2) % 3), 32, "arp", "S")
    z.add("cb", 0, 6, "E2", 30, "bass")
    z.expr(["trem_va", "trem_hi"], [(0, -24), (6, -22)])
    lv(z, ["pz_hi"], -12)
    lv(z, ["cb"], -21)
    # 'hmph!': bassoon, low pizzicato and a short bandoneon chord on the word; then the question, F#7 left hanging
    g.add("bsn", 0, 0.5, "B2", 48, "melody", "s")
    g.add("pz_lo", 0, 0.5, "B2", 44, "arp", "h")
    g.add("pz_cb", 0, 0.5, "B1", 42, "bass", "h")
    for nm in ("D4", "F#4", "B4"):
        g.add("bandoneon", 0, 0.5, nm, 38, "arp", "s")
    for nm in ("B2", "F#3", "B3"):
        g.add("guitar", 0, 0.5, nm, 40, "arp", "h")
    drum(g, 0, 77, 34)
    g.sync("'哼': hmph (bassoon, pizzicato, bandoneon)", 0, t_hm)
    g.pad(["vla", "vla", "vln1"], 3, 50, 65, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    g.add("bsn", 4, 2, "C#3", 40, "melody")
    g.duck(3.0)
    lv(g, ["bsn"], -14)
    lv(g, ["pz_lo", "pz_cb"], -11)
    lv(g, ["bandoneon"], -17)
    lv(g, ["guitar"], -13)
    lv(g, "hand", -17)
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (6, -20)])


def story(c):
    """Jesus answers kindly: the deceptive G after the Pharisees' F#7 (6/8; guitar, strings, a soft bandoneon), the
    mandolin's tremolo rising (D/F# Em7 A7); D on '如果你有一百只羊' (strings only under his voice; a glint as the story
    page pops open, a quick run up the mandolin for the hundred, a sheep's bell, one bell note falling away as one
    is lost); E7sus4 on '你会怎么做呢' -- the question hangs into the page turn (a run up on the page's whoosh, a
    last glint)."""
    c.gain(-2.5)
    t_q = c.gap(c.find("如果你有一百只羊"))
    t_hang = c.at("你会怎么做呢")
    a = c.seg(0, t_q, 3, "6/8", "G major", nominal=118, label="story-kind")
    b = c.seg(t_q, t_hang, 2, "6/8", "D major", nominal=103, label="story-question")
    h = c.seg(t_hang, c.dur, 1, "6/8", "A major", nominal=None, label="story-hang")             # a held question
    segs = (a, b, h)
    for sg in segs:
        sg.duck(1.5)
    a.prog("G:3 | D/F#:3 | Em7:3/2 A7:3/2")
    b.prog("D:3 | G:3")
    h.prog("E7sus4:3")
    a.sync("'耶稣听见了': kindly (G, after F#7)", 0, 0.0, kind="change")
    b.sync("'如果你有一百只羊': the question (D)", 0, t_q, kind="change")
    h.sync("'你会怎么做呢': the question hangs (E7sus4)", 0, t_hang, kind="change")
    # 'Jesus heard, and told them a story': warm G, the guitar; the mandolin's tremolo rises with the story page
    broken(a, "guitar", 0, 9, (0, 2, 4, 5, 4, 2), 43, 62, vel=34, thin=True)
    strings(a, vel=36, lo=50, hi=69, bass=(40, 52), cb=(28, 40))
    a.pad("bandoneon", 3, 55, 67, vel=32, q1=6, bass_ref=(40, 52))
    trem(a, "mandolin", 6.0, 7.5, "B4", 30)
    trem(a, "mandolin", 7.5, 9.0, "C#5", 32)
    a.expr(["mandolin"], [(6, -22), (9, -17)])
    lv(a, ["guitar"], -12)
    a.expr(STR, [(0, -22), (1.5, -19), (9, -20)])
    lv(a, ["bandoneon"], -22, q1=6)
    hit(c, segs, "chime", None, 0, "the story page pops open (a glint)", glock=(86, 98), celesta=(79, 91), vel=46)
    # 'if you had a hundred sheep and lost one': strings under his voice; the hundred (a run), one bell falls away
    b.pad(["vla", "vla", "vln1"], 3, 50, 66, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(b, "cb", 28, 40, 30)
    t_100 = c.at("一百只羊")
    q_100 = qpos(b, c, t_100 + 0.15, 0.0, 2.0)
    run(b, "mandolin", q_100, ["D5", "E5", "F#5", "G5", "A5", "B5", "C#6", "D6"], 0.125, vel=30, role="melody")
    baa = picture(c, "sheep", c.ls(c.find("如果你有一百只羊")) - 0.3) or []
    if len(baa) >= 2:                                       # a sheep in the page (its bell), then one wanders off
        accent(c, segs, baa[0], "a sheep in the story page (its bell)", bell=(84, 98), vel=36)
        sg_, q_l = seg_at(c, segs, baa[1])
        sg_.add("tinkle", q_l, _dq(sg_, q_l, 3.0), top(sg_, q_l, 79, 86), 38, "arp", "h")
        sg_.sync("'丢了一只': one bell note falls away", q_l, baa[1])
    else:
        t_lost = voice_at(c, "丢了一只")
        q_lost = qpos(b, c, t_lost, 3.0, 5.4)
        b.add("tinkle", q_lost, 6 - q_lost, "B5", 38, "arp", "h")
    b.duck(3.0)
    b.expr(STR, [(0, -19), (1.5, -22), (6, -21)])
    lv(b, ["mandolin"], -15)
    lv(b, ["tinkle"], -13)
    # 'what would you do?': E7sus4 hangs (into the page turn)
    h.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    trem(h, "mandolin", 0, 3, "B4", 28)
    h.add("tinkle", 0.5, 2.5, "E6", 34, "arp")
    t_wh = pic(c, "whoosh", "如果你有一百只羊", 0)
    if t_wh is not None:                                     # the page whooshes open into the story: a run up
        sg_, q_w = seg_at(c, segs, t_wh)
        if sg_ is h:
            run(h, "mandolin", q_w, ["E5", "A5", "B5", "D6", "E6"], 0.12, vel=34, role="arp")
            h.sync("the page whooshes into the story (a run up)", q_w, t_wh)
        else:
            accent(c, segs, t_wh, "the page whooshes (a pluck)", mando=(74, 88), vel=40)
    hit(c, segs, "sparkle", "你会怎么做呢", 1, "the story page glints", glock=(86, 98), vel=38)
    h.expr(["vla", "vln2", "vln1", "vc"], [(0, -21), (3, -22)])
    lv(h, ["mandolin"], -18)
    lv(h, ["tinkle"], -15)
    for sg in segs:
        lv(sg, ["glock"], -12)


def flock(c):
    """Jesus's story begins (A major, 6/8): the page turn holds the question's E7sus4, the shepherd's song lands on A at
    '耶稣的故事里' (whistle, mandolin, the accordion's oom-pah, pizzicato; a pluck as he loves each one); '一百只羊' --
    the whole flock (strings, a mandolin tremolo, the song's second phrase, a little bell for every bleat in the
    picture, a run up the scale on E7); '每天早上' -- the walk to the grass (the song on the mandolin, the hooves on two
    woodblocks; a glint of morning); '有一只小羊' -- the lamb's motif (mandolin with its bell), wandering up into D on
    '越走越远', a nibble, a flute butterfly; '一抬头' -- E7sus4 hangs, a plucked '咦？'; F# minor on '大家都不见了',
    the bell's motif small and alone (the picture's bell sparkles: the landing, 咦, 大家都不见了)."""
    c.gain(-2.5)
    t_sh = c.ls(0)
    t_100 = c.ls(c.find("一百只羊，好多好多"))
    t_mo = c.gap(c.find("每天早上"))
    t_lamb = c.gap(c.find("有一只小羊"))
    t_up = c.at("一抬头")
    sp4 = picture(c, "sparkle", c.ls(c.find("一抬头")) - 0.3) or []
    t_yi = sp4[1] if len(sp4) >= 3 else voice_at(c, "咦")
    t_gone = sp4[2] if len(sp4) >= 3 else voice_at(c, "大家都不见了")
    t_gone = min(max(t_gone, t_up + 0.6), c.dur - 0.8)
    p = c.seg(0, t_sh, 1, "2/4", "A major", nominal=None, label="flock-page")             # the question held
    s = c.seg(t_sh, t_100, 4, "6/8", "A major", nominal=107, label="flock-shepherd")
    d = c.seg(t_100, t_mo, 3, "6/8", "A major", nominal=120, label="flock-hundred")
    m = c.seg(t_mo, t_lamb, 3, "6/8", "A major", nominal=100, label="flock-morning")
    l = c.seg(t_lamb, t_up, 5, "6/8", "A major", nominal=112, label="flock-lamb")
    u = c.seg(t_up, t_gone, 1, "6/8", "A major", nominal=None, label="flock-look-up")       # a held '咦？'
    g = c.seg(t_gone, c.dur, 1, "6/8", "F# minor+", nominal=None, label="flock-gone")
    segs = (p, s, d, m, l, u, g)
    for sg in segs:
        sg.duck(1.5)
    p.prog("E7sus4:2")
    s.prog(" | ".join(SHEP_PROG[:4]))
    d.prog("A:3 | D:3 | E7:3")
    m.prog("A:3 | E/G#:3 | E:3")
    l.prog("A:3 | D:3/2 E:3/2 | D:3 | G:3/2 A:3/2 | Bm7:3")
    u.prog("E7sus4:3")
    g.prog("F#m:3")
    s.sync("'耶稣的故事里': the shepherd's song (A)", 0, t_sh, kind="change")
    d.sync("'一百只羊': the whole flock (A)", 0, t_100, kind="change")
    m.sync("'每天早上': the morning walk (A)", 0, t_mo, kind="change")
    l.sync("'有一只小羊': the lamb's motif (A)", 0, t_lamb, kind="change")
    u.sync("'一抬头': the lamb looks up (E7sus4)", 0, t_up, kind="change")
    g.sync("'大家都不见了': everyone is gone (F# minor)", 0, t_gone, kind="change")
    # the page turn: the question's E7sus4 held; a mandolin run up into the spring hills
    p.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    p.pad("accordion", 3, 57, 69, vel=30, bass_ref=(40, 52))
    trem(p, "mandolin", 0, 1.0, "B4", 28)
    run(p, "mandolin", 1.0, ["E5", "A5", "B5", "D6", "E6"], 0.2, vel=32, role="arp")
    p.expr(["vla", "vln1", "vc"], [(0, -21), (2, -19)])
    lv(p, ["accordion"], -22)
    lv(p, ["mandolin"], -17)
    # the shepherd and his hundred sheep: the song on the whistle
    s.mel("whistle", bars(SHEP, 0, 4), vel=48)
    broken(s, "mandolin", 0, 12, (0, 1, 2, 1, 2, 1), 62, 76, vel=36, thin=True)
    oom(s, 0, 12, vel=38, bass=(40, 52), hi=(57, 69))
    s.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(40, 52))
    s.duck(3.0, parts=["whistle"])
    s.expr(["whistle"], [(0, -19), (1.5, -16), (12, -16)])
    s.expr(["mandolin"], [(0, -20), (1.5, -16), (12, -16)])
    s.expr(["pz_lo"], [(0, -17), (1.5, -14), (12, -14)])
    s.expr(["accordion"], [(0, -24), (1.5, -21), (12, -21)])
    s.expr(["vla", "vln1"], [(0, -20), (3, -23), (12, -23)])
    hit(c, segs, "pop", None, 0, "he loves every one (a pluck)", mando=(74, 88), glock=(86, 98), vel=42)
    # 'a hundred sheep, so many, all over the hillside': the whole flock; a little bell for each bleat
    d.mel("whistle", SHEP[4] + " | " + SHEP[5] + " | G#5:3/2 B5:3/2", vel=48)
    run(d, "mandolin", 6.0, ["E5", "F#5", "G#5", "A5", "B5", "C#6", "D6", "E6"], 0.25, vel=34, role="melody")
    d.add("mandolin", 8.0, 1.0, "E6", 38, "melody")
    trem(d, "mandolin", 0, 6, "A4", 26, role="arp")
    oom(d, 0, 9, vel=38, bass=(40, 52), hi=(57, 69), lively=True)
    strings(d, vel=34, lo=50, hi=71, bass=(40, 52), cb=(28, 40))
    baas = picture(c, "sheep", c.ls(c.find("一百只羊，好多好多")) - 0.3, t_mo) or []
    if baas:
        for k_, tb in enumerate(baas[:4]):
            sg_, q_b = seg_at(c, segs, tb)
            bell(sg_, q_b, vel=38 - 2 * k_)
            if k_ == 0:
                sg_.sync("a sheep bleats (its bell)", q_b, tb)
    else:
        bell(d, 0.0, vel=38)
        for k_, q_ in enumerate((1.5, 3.0, 4.5)):
            if not bool(d.score.speaking(d.t(q_) + 0.05)):
                bell(d, q_, vel=36 - 2 * k_)
    d.duck(4.0, parts=["whistle"])
    d.expr(["whistle"], [(0, -17), (9, -16)])
    lv(d, ["mandolin"], -17)
    lv(d, ["pz_lo"], -14)
    lv(d, ["accordion"], -22)
    d.expr(STR, [(0, -23), (6, -22), (9, -21)])
    lv(d, ["tinkle"], -14)
    # 'every morning the shepherd leads the flock to the grass': the song on the mandolin, the little hooves
    m.mel("mandolin", SHEP[0] + " | " + SHEP[1] + " | " + SHEP[3], vel=44)
    oom(m, 0, 9, vel=36, bass=(40, 52), hi=(57, 69))
    clop(m, 0, 9, vel=30)
    m.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(40, 52))
    m.duck(2.5, parts=["mandolin"])
    lv(m, ["mandolin"], -14)
    lv(m, ["pz_lo"], -13)
    lv(m, ["accordion"], -22)
    lv(m, "hand", -16)
    lv(m, ["vla", "vln1"], -23)
    hit(c, segs, "sparkle", "每天早上", 0, "morning (a glint)", glock=(86, 98), vel=40)
    hit(c, segs, "sheep", "每天早上", 0, "a sheep bleats (its bell)", bell=(84, 98), vel=40)
    # 'one little lamb nibbled and wandered, further and further': the lamb's motif with its bell
    lamb = bars(LAMB, 0, 2) + " | D6:1/2 F#6:1/2 E6:1/2 D6:1 A5:1/2 | B5:1/2 D6:1 C#6:1/2 E6:1"
    l.mel("mandolin", lamb, vel=46)
    l.mel("tinkle", lamb, vel=40, role="fx")
    oom(l, 0, 12, vel=34, bass=(40, 52), hi=(57, 69))
    l.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    l.mel("flute", "r:12 | B5:1/4 D6:1/4 F#6:1/4 D6:1/4 B5:1/4 A5:1/4 B5:1/4 D6:1/4 F#6:1/2 A5:1/2", vel=40,
          role="counter")
    l.add("pz_lo", 12, 1.5, "B2", 34, "arp", "s")
    l.duck(2.5, parts=["mandolin", "tinkle", "flute"])
    l.expr(["mandolin"], [(0, -18), (1.5, -15), (6, -15), (12, -18)])
    l.expr(["tinkle"], [(0, -20), (1.5, -17), (6, -17), (12, -20)])
    lv(l, ["flute"], -18)
    lv(l, ["pz_lo"], -13)
    lv(l, ["accordion"], -22)
    l.expr(["vla", "vln1"], [(0, -23), (15, -24)])
    hit(c, segs, "sparkle", "有一只小羊", 0, "the lamb's bell (on the picture)", bell=(84, 98), vel=40)
    t_nib = pic(c, "crunch", "有一只小羊")
    if t_nib is not None:                                    # nibbling: two soft plucks
        clear_near(c, t_nib)
        sg_, q_n = accent(c, segs, t_nib, None, pluck=(62, 74), vel=38)
        q2 = min(q_n + 0.25, sg_.n_q - 0.1)
        sg_.add("pz_hi", q2, _dq(sg_, q2, 0.25), top(sg_, q2, 62, 74), 34, "arp", "S")
    # 'it looked up -- huh?': E7sus4 hangs; the lamb lands (its bell) and a plucked question on 咦
    u.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    if len(sp4) >= 3:
        accent(c, segs, sp4[0], "the lamb lands (its bell)", bell=(84, 98), vel=38)
    sg_, q_yi = seg_at(c, segs, t_yi)
    if sg_ is u:
        u.add("mandolin", q_yi, _dq(u, q_yi, 1.0), "B5", 44, "arp", "h")
        u.add("tinkle", q_yi, _dq(u, q_yi, 1.0), "E6", 38, "arp", "h")
        u.sync("'咦？' (a plucked question)" + (" (picture)" if len(sp4) >= 3 else ""), q_yi, t_yi)
    u.expr(["vla", "vln1", "vc"], [(0, -21), (3, -22)])
    lv(u, ["mandolin"], -15)
    lv(u, ["tinkle"], -14)
    # 'everyone was gone!': F# minor, the bell's motif small and alone
    g.mel("tinkle", LAMB_MIN[0], vel=40)
    g.add("tinkle", 0, 0.5, "C#6", 34, "arp", "h")
    g.sync("everyone is gone (the bell)" + (" (picture)" if len(sp4) >= 3 else ""), 0, t_gone)
    g.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=30, bass_part="vc", bass_lo=42, bass_hi=54)
    lv(g, ["tinkle"], -14)
    g.expr(["vla", "vln1", "vc"], [(0, -20), (3, -21)])
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)


def count(c):
    """Sunset (D major, 6/8): the shepherd's song on the ocarina, the accordion and warm strings, to A7 (the lamb's bell
    far away on the picture); then the counting game in 2/4 -- a pluck (mandolin, pizzicato, a glockenspiel ping, a
    woodblock tick) on each number as it pops up, climbing the D major scale over a falling bass (一 D, 两 A/C#, 三 Bm,
    and a fourth G); '数啊数' runs on up, one note per pop (A4 ... G5 over G A A7); 97, 98, 99 climb A5 B5 C#6 over D G
    A -- and the hundredth note, the high D, never comes: on the spoken '咦？' the bass slips to G (A7/G) under the held
    C#, a plucked tritone; an upbeat as he decides to count again; the recount on '数啊数……' is twice as fast (a pluck
    on each quick pop, D/F# G A7) and lands on C#6 again with the big '99' bubble -- then the deflation (bassoon and
    trombone: wah wah wah waaah); the deceptive B minor on '少了一只小羊' (tremolo, the lamb's motif in B minor on its
    bell); '我的小羊呢' E minor and A (the horn rising, a glint as he resolves to go); '牧羊人把九十九只羊' -- the
    shepherd's song in D on the whistle, B minor, C#7sus4 C#7 (V of F# minor)."""
    c.gain(-2.5)
    i1 = c.find("一只，两只")
    i9 = c.find("九十七")
    i4 = c.find("数啊数……还是")
    t_one = c.gap(i1)
    t_run = c.gap(c.find("数啊数，数啊数"))
    t_97 = c.gap(i9)
    t_huh = syl(c, "九十七", 4)[3]                            # the spoken 咦 (0.2 s before its subtitle estimate)
    t_re = c.gap(i4)
    t_miss = c.at("少了一只小羊")
    t_my = c.gap(c.find("我的小羊呢"))
    t_go = c.gap(c.find("牧羊人把九十九只羊"))
    pops = picture(c, "pop") or []
    slow = [t_ for t_ in pops if c.ls(i1) - 0.3 <= t_ < t_run]
    fast = [t_ for t_ in pops if t_run <= t_ < t_97]
    nines = [t_ for t_ in pops if c.ls(i9) - 0.3 <= t_ < t_huh - 0.1][:3]
    rec = [t_ for t_ in pops if c.ls(i4) - 0.3 <= t_ < t_miss]
    pic_one = len(slow) >= 3
    one = slow[:4] if pic_one else syl(c, "一只", 3)
    ninety = nines if len(nines) == 3 else syl(c, "九十七", 3)
    t_99 = rec[-1] if len(rec) >= 2 else voice_at(c, "九十九只")
    jabs = rec[:-1] if len(rec) >= 2 else []
    t_99 = min(max(t_99, t_re + 0.6), t_miss - 0.5)
    su = c.seg(0, t_one, 3, "6/8", "D major", nominal=82, label="count-sunset")
    o = c.seg(t_one, t_run, 3, "2/4", "D major", nominal=116, label="count-one")
    r = c.seg(t_run, t_97, 3, "2/4", "D major", nominal=120, label="count-run")
    n = c.seg(t_97, t_huh, 3, "2/4", "D major", nominal=118, label="count-ninety")
    h = c.seg(t_huh, t_re, 1, "2/4", "D major", nominal=None, label="count-huh")              # held: 咦？
    rc = c.seg(t_re, t_99, 2, "2/4", "D major", nominal=None, label="count-recount")
    st = c.seg(t_99, t_miss, 1, "2/4", "D major", nominal=None, label="count-still")
    w = c.seg(t_miss, t_my, 1, "6/8", "B minor", nominal=96, label="count-missing")
    y = c.seg(t_my, t_go, 2, "6/8", "D major", nominal=105, label="count-my-lamb")
    g = c.seg(t_go, c.dur, 3, "6/8", "D major", nominal=97, label="count-sets-off")
    segs = (su, o, r, n, h, rc, st, w, y, g)
    for sg in segs:
        sg.duck(1.5)
    su.prog("D:3 | G:3 | Em7:3/2 A7:3/2")
    if len(one) >= 4 and one[3] < t_run - 0.15:
        prog48(o, ["D", "A/C#", "Bm", "G"], edges48(o, c, one[1:4]))
    else:
        one = one[:3]
        prog48(o, ["D", "A/C#", "Bm"], edges48(o, c, one[1:3]))
    r.prog("A:2 | A:2 | A7:2")
    prog48(n, ["D", "G", "A"], edges48(n, c, ninety[1:3]))
    h.prog("A7/G:2")
    if len(jabs) >= 5:
        prog48(rc, ["D/F#", "G", "A7"], edges48(rc, c, [jabs[2], jabs[4]]))
    else:
        rc.prog("D/F#:1 G:1 | A7:2")
    st.prog("A7:2")
    w.prog("Bm:3")
    y.prog("Em:3 | A:3")
    g.prog("D:3 | Bm:3 | C#7sus4:3/2@F#-harmonic C#7:3/2@F#-harmonic")
    o.sync("'一只，两只，三只': the count begins (D)", 0, t_one, kind="change")
    r.sync("'数啊数': counting on (A)", 0, t_run, kind="change")
    n.sync("'九十七': ninety-seven (D)", 0, t_97, kind="change")
    h.sync("'咦？': the hundredth never comes (A7/G)", 0, t_huh, kind="change")
    rc.sync("'数啊数……': the recount (D/F#)", 0, t_re, kind="change")
    w.sync("'少了一只小羊': one is missing (B minor)", 0, t_miss, kind="change")
    y.sync("'我的小羊呢': where is my lamb? (E minor)", 0, t_my, kind="change")
    g.sync("'牧羊人把九十九只羊': he sets off (D)", 0, t_go, kind="change")
    # sunset: the shepherd's song on the ocarina, warm strings, the accordion; the lamb's bell far away
    su.mel("ocarina", "F#5:1 G5:1/2 A5:1 D6:1/2 | B5:1 A5:1/2 G5:1 D5:1/2 | E5:3/2 C#5:3/2", vel=44)
    strings(su, vel=34, lo=50, hi=69, bass=(40, 52), cb=None)
    su.pad("accordion", 3, 57, 69, vel=30, bass_ref=(40, 52))
    broken(su, "mandolin", 1.5, 9, (0, 1, 2, 1, 2, 1), 62, 76, vel=28, thin=True)
    su.duck(3.5, parts=["ocarina"])
    su.expr(["ocarina"], [(0, -26), (1.5, -19), (9, -18)])
    su.expr(STR, [(0, -24), (1.5, -23), (9, -22)])
    su.expr(["accordion"], [(0, -27), (1.5, -24), (9, -24)])
    lv(su, ["mandolin"], -19)
    hit(c, segs, "sparkle", None, 0, "the lamb far away (its bell)", bell=(84, 98), vel=38)
    lv(su, ["tinkle"], -15)
    # 'one, two, three...': a pluck for each number, climbing over a falling bass; the sheep go by (the accordion)
    o.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(31, 43))
    bassline(o, "pz_cb", 31, 43, 42, role="arp")
    for q_ in np.arange(0.5, 6, 1.0):
        for pt in o.chord_at(q_ + 1e-3).tones(57, 69)[:3]:
            o.add("accordion", q_, _dq(o, q_, 0.4), pt, 28, "arp", "s")
    for k_, (t_, nm) in enumerate(zip(one, ("D4", "E4", "F#4", "G4"))):
        sg_, q_ = seg_at(c, segs, t_)
        count_pluck(sg_, q_, midi(nm), vel=48 + 2 * k_, glock=k_ < 3)
        sg_.sync(f"count {k_ + 1} (a pluck)" + (" (picture)" if pic_one else ""), q_, t_)
    lv(o, ["vla", "vln1"], -21)
    lv(o, ["pz_cb"], -12)
    lv(o, ["accordion"], -23)
    # 'counting, counting...': the run, one note (and a woodblock tick) for every sheep counted
    run_notes = ["A4", "B4", "C#5", "D5", "E5", "F#5", "G5"]
    if len(fast) >= 7:
        t_fast = fast[:7]
    else:
        t_fast = [r.t(0.84 + 0.62 * k_) - c.t0 for k_ in range(7)]
    for k_, (t_, nm) in enumerate(zip(t_fast, run_notes)):
        sg_, q_ = seg_at(c, segs, t_)
        sg_.add("mandolin", q_, _dq(sg_, q_, 0.5), nm, 34 + 2 * k_, "melody", "s")
        sg_.add("pz_hi", q_, _dq(sg_, q_, 0.5), nm, 28 + 2 * k_, "melody", "s")
        drum(sg_, q_, 76 if k_ % 2 == 0 else 77, 30)
        if k_ == 0 and len(fast) >= 7:
            sg_.sync("'数啊数': the counting runs on (picture)", q_, t_)
    if len(fast) >= 8:                                       # ninety-six: a tick (its note would repeat G)
        sg_, q_ = seg_at(c, segs, fast[7])
        drum(sg_, q_, 76, 32)
    oom(r, 0, 6, vel=32, bass=(40, 52), hi=(57, 69))
    for pt in ("A3", "C#4", "E4"):                           # the A arrives with '数啊数' (the run starts on the pops)
        r.add("accordion", 0, 1.0, pt, 34, "arp")
    r.add("pz_cb", 0, 0.5, "A1", 42, "bass", "h")
    r.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    lv(r, ["mandolin"], -15)
    lv(r, ["pz_hi"], -16)
    lv(r, ["pz_lo", "pz_cb"], -14)
    r.expr(["accordion"], [(0, -21), (1, -24), (6, -24)])
    lv(r, "hand", -18)
    lv(r, ["vla", "vln1"], -23)
    # '97, 98, 99...': A5 B5 C#6 over D G A -- each louder; the strings lean in
    for k_, (t_, nm) in enumerate(zip(ninety, ("A5", "B5", "C#6"))):
        sg_, q_ = seg_at(c, segs, t_)
        count_pluck(sg_, q_, midi(nm), vel=46 + 3 * k_)
        if k_ == 2:
            sg_.add("whistle", q_, sg_.n_q - q_, nm, 40, "melody")
        if k_ in (0, 2):
            sg_.sync(f"'{('九十七', '九十八', '九十九')[k_]}' (a pluck)" + (" (picture)" if len(nines) == 3 else ""),
                     q_, t_)
    n.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    n.expr(["vla", "vln1", "vc"], [(0, -24), (6, -20)])
    lv(n, ["whistle"], -18)
    # 'huh? why only ninety-nine? I'll count again!': the bass slips to G under the held C#; a plucked tritone on 咦;
    # an upbeat as he decides to count again
    h.add("whistle", 0, 2, "C#6", 36, "melody")
    h.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    h.add("bsn", 0, 0.5, "G3", 38, "melody", "s")
    h.add("pz_cb", 0, 0.5, "G2", 38, "bass", "h")
    h.add("mandolin", 0, 0.5, "G5", 40, "arp", "h")
    h.add("mandolin", 0, 0.5, "C#6", 38, "arp", "h")
    h.add("pz_hi", 0, 0.5, "G5", 34, "arp", "h")
    h.sync("'咦？' (a plucked tritone)", 0, t_huh)
    t_ag = pic(c, "cloth", "九十七", 0)
    if t_ag is not None:                                     # 'I'll count again!': a little plucked upbeat
        sg_, q_ag = seg_at(c, segs, t_ag)
        for k_, pt in enumerate(sg_.chord_at(q_ag + 1e-3).tones(57, 69)[:3]):
            qq = min(q_ag + 0.125 * k_, sg_.n_q - 0.15)
            sg_.add("pz_hi", qq, _dq(sg_, qq, 0.125), pt, 40 + 3 * k_, "arp", "S")
        sg_.add("mandolin", q_ag, _dq(sg_, q_ag, 0.25), top(sg_, q_ag, 62, 69), 40, "arp", "h")
        sg_.sync("'我再数一遍' (a plucked upbeat)", q_ag, t_ag)
    lv(h, ["whistle"], -19)
    lv(h, ["bsn"], -14)
    lv(h, ["pz_cb"], -13)
    h.expr(["vla", "vln1", "vc"], [(0, -17), (1, -19), (2, -23)])
    # the recount: twice as fast, a pluck on each quick pop, a run up -- and C#6 again with the big '99'
    if len(jabs) >= 3:
        jn = ["D4", "A4", "B4", "D5", "E5"][:len(jabs)]
        for k_, (t_, nm) in enumerate(zip(jabs, jn)):
            sg_, q_ = seg_at(c, segs, t_)
            sg_.add("mandolin", q_, _dq(sg_, q_, 0.25), nm, 40 + 2 * k_, "arp", "h")
            sg_.add("pz_hi", q_, _dq(sg_, q_, 0.25), nm, 34 + 2 * k_, "arp", "h")
            drum(sg_, q_, 76 if k_ % 2 == 0 else 77, 28)
            if k_ == 0:
                sg_.sync("the recount: the first quick pop", q_, t_)
        q5 = rc.q_of(c.t0 + jabs[-1])
        tail = ["F#5", "G5", "A5", "B5"]
        step = max(0.08, (rc.n_q - q5) / (len(tail) + 1))
        for k_, nm in enumerate(tail):
            qq = q5 + step * (k_ + 1)
            if qq < rc.n_q - 0.05:
                rc.add("mandolin", qq, min(step, rc.n_q - qq), nm, 40 + 2 * k_, "melody", "s")
    else:
        re_notes = ["D4", "E4", "F#4", "G4", "A4", "B4", "C#5", "D5", "E5", "F#5", "G5", "A5", "B5"]
        for k_, nm in enumerate(re_notes):
            q_ = 0.25 * k_ + 0.5
            if q_ < rc.n_q - 0.1:
                rc.add("mandolin", q_, 0.25, nm, 38 + k_, "melody", "s")
                rc.add("pz_hi", q_, 0.25, nm, 32 + k_, "melody", "s")
                drum(rc, q_, 76 if k_ % 2 == 0 else 77, 26)
    rc.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    bassline(rc, "pz_lo", 40, 52, 38, role="arp")
    lv(rc, ["mandolin"], -18)
    lv(rc, ["pz_hi"], -19)
    lv(rc, ["pz_lo"], -14)
    lv(rc, "hand", -19)
    lv(rc, ["vla", "vln1"], -24)
    # 'still ninety-nine!': C#6 again on the big '99', then the deflation -- bassoon and trombone, wah wah wah waaah
    st.add("mandolin", 0, 0.5, "C#6", 50, "arp", "h")
    st.add("pz_hi", 0, 0.5, "C#6", 44, "arp", "h")
    st.add("glock", 0, 0.5, "C#7", 38, "arp", "h")
    st.add("whistle", 0, 0.5, "C#6", 38, "arp")
    st.sync("'还是九十九只': C#6 again, the big 99" + (" (picture)" if jabs else ""), 0, t_99)
    for part, vel in (("bsn", 52), ("tbn", 46)):
        st.mel(part, "r:1/2 G3:1/3 F#3:1/3 F3:1/3 E3:1/2", vel=vel)
    st.add("pz_lo", 0.5, 0.5, "A2", 44, "arp", "h")
    st.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=26, bass_ref=(45, 57))
    lv(st, ["mandolin", "pz_hi"], -15)
    lv(st, ["whistle"], -19)
    lv(st, ["bsn"], -16)
    lv(st, ["tbn"], -20)
    lv(st, ["pz_lo"], -13)
    lv(st, ["vla", "vln1"], -25)
    # 'one little lamb is missing!': the deceptive B minor -- tremolo, the lamb's motif on its bell in B minor
    w.mel("tinkle", "B5:1 D6:1/2 B5:1 F#5:1/2", vel=40)
    w.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 71, vel=32, bass_ref=(47, 59))
    w.add("vc", 0, 3, "B2", 34, "bass")
    w.add("pz_lo", 0, 1, "B2", 46, "arp", "h")
    w.add("pz_lo", 0, 1, "F#3", 40, "arp", "h")
    lv(w, ["tinkle"], -15)
    w.expr(["trem_va", "trem_hi"], [(0, -20), (3, -22)])
    lv(w, ["vc"], -19)
    lv(w, ["pz_lo"], -12)
    # 'where is my lamb? I'll go and find it!': E minor, A; the horn rising; a glint as he resolves to go
    y.mel("horn", "E4:1 F#4:1/2 G4:1 B4:1/2 | A4:1 B4:1/2 C#5:1 E5:1/2", vel=46)
    strings(y, vel=34, lo=50, hi=69, bass=(40, 52), cb=(28, 40))
    y.duck(3.0, parts=["horn"])
    lv(y, ["horn"], -18)
    y.expr(STR, [(0, -22), (6, -20)])
    hit(c, segs, "sparkle", "我的小羊呢", 0, "I'll go and find it (a glint)", glock=(86, 98), vel=42)
    # 'he left the ninety-nine on the hillside and went to find the one': the shepherd's song on the whistle
    g.mel("whistle", "F#5:1 G5:1/2 A5:1 D6:1/2 | B5:1 A5:1/2 F#5:1 D5:1/2 | F#5:3/2 E#5:3/2", vel=44)
    oom(g, 0, 9, vel=34, bass=(37, 49), hi=(57, 69))
    g.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(37, 49))
    g.duck(3.5, parts=["whistle"])
    lv(g, ["whistle"], -17)
    lv(g, ["pz_lo"], -13)
    lv(g, ["accordion"], -23)
    g.expr(["vla", "vln1"], [(0, -22), (9, -21)])
    for sg in segs:
        lv(sg, ["glock"], -12)


def alone(c):
    """Dusk on the rocky slope (F# minor, 6/8): the lamb's motif in minor, small, on its bell (a celesta below) over
    soft high strings and a low cello; Bm7 on '天黑了' -- the wind swells on '呼呼' (strings, a soft harp glissando), an
    owl (the ocarina, hoo -- hoo) in the pause; F# minor on '小羊好害怕' (a soft tremolo -- it trembles) and each 咩 (the
    narrator's, or the picture's bleats) echoed back by the hills (the ocarina on the echo line); C#7 at the end."""
    c.gain(-3.0)
    t_dark = c.at("天黑了")
    t_bl = c.gap(c.find("小羊好害怕"))
    d = c.seg(0, t_dark, 2, "6/8", "F# harmonic", nominal=94, label="alone-dusk")
    n = c.seg(t_dark, t_bl, 1, "6/8", "F# harmonic", nominal=75, label="alone-night")
    b = c.seg(t_bl, c.dur, 2, "6/8", "F# harmonic", nominal=100, label="alone-bleat")
    segs = (d, n, b)
    for sg in segs:
        sg.duck(1.5)
    d.prog(" | ".join(LAMB_MIN_PROG))
    n.prog("Bm7:3")
    b.prog("F#m:3 | F#m:3/2 C#7:3/2")
    n.sync("'天黑了': night falls (Bm7)", 0, t_dark, kind="change")
    b.sync("'小羊好害怕': afraid (F# minor)", 0, t_bl, kind="change")
    # 'meanwhile the little lamb was alone on the hill': its motif, small, in minor
    d.mel("tinkle", bars(LAMB_MIN, 0, 2), vel=40)
    d.mel("celesta", bars(LAMB_MIN, 0, 2), vel=32, transpose=-12, role="fx")
    d.pad(["vla", "vla", "vln1"], 3, 57, 76, vel=30, bass_part="vc", bass_lo=37, bass_hi=49)
    d.duck(2.5, parts=["tinkle", "celesta"])
    hit(c, segs, "sparkle", None, 0, "the lamb alone (its bell)", clear=False, bell=(84, 98), vel=38)
    lv(d, ["tinkle"], -14)
    lv(d, ["celesta"], -16)
    d.expr(["vla", "vln1", "vc"], [(0, -22), (6, -22)])
    # 'night fell, the wind blew': Bm7; the wind on 呼呼; an owl in the pause
    n.pad(["vla", "vla", "vln1"], 3, 57, 76, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    t_wind = pic(c, "whoosh", None, 0, lo=0.0, hi=n.t(2.6) - c.t0) or voice_at(c, "呼呼")
    q_w = qpos(n, c, t_wind, 0.0, 2.0)
    sweep(n, q_w, 0.8, "B3", "F#5", 24, 36, part="harp")
    n.expr(["vla", "vln1", "vc"], [(0, -22), (q_w, -22), (min(q_w + 0.8, 2.6), -18), (3, -21)])
    lv(n, ["harp"], -16)
    t_owl = c.le(0) + 0.06
    sg_, q_o = seg_at(c, segs, t_owl)
    sg_.add("ocarina", q_o, _dq(sg_, q_o, 0.6), "A4", 40, "arp")
    sg2, q_o2 = seg_at(c, segs, t_owl + 0.42)
    sg2.add("ocarina", q_o2, _dq(sg2, q_o2, 0.8), "F#4", 38, "arp")
    for sg in segs:
        lv(sg, ["ocarina"], -14)
    # 'the lamb was so afraid, it called: baa -- baa --': F# minor, a soft tremolo; each bleat echoed by the hills
    b.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 71, vel=30, bass_ref=(42, 54))
    bassline(b, "vc", 42, 54, 30)
    baa = picture(c, "sheep", c.ls(c.find("小羊好害怕")) - 0.3) or []
    bleats = baa[:2] if len(baa) >= 2 else syl(c, "咩——咩——", 2)
    for k_, tb in enumerate(bleats):
        echo_call(c, segs, min(tb + 0.4, c.dur - 0.12), ["C#6"], 0.0, part="echo_oca", vel=32 - 4 * k_, dur_s=0.3)
    b.expr(["trem_va", "trem_hi"], [(0, -22), (6, -23)])
    b.expr(["vc"], [(0, -22), (6, -23)])
    for sg in segs:
        lv(sg, ["echo_oca"], -17)


def search(c):
    """The search at night (2/4, a steady walk): pizzicato steps, the mandolin's off-beats, soft strings, and the
    shepherd whistling his song in F# minor to keep going (A B C# F# | G# F# E# C# ...); a pluck on each stepping stone
    as he crosses the stream (the picture); '小羊！小羊！' -- he stops and calls (D, A: held strings and a mandolin
    tremolo), and in the pause the hills echo his call (the whistle, C#6 A5, on the echo line); '找啊找' -- the walk
    again, darker (C#7, Bm) but never frightening, a pluck in the thorny bushes; '可是牧羊人一直找' -- A major hope: a
    rising bass D E F#m E under the song's head, landing on E (V of A)."""
    c.gain(-2.5)
    t_call = c.gap(c.find("小羊！小羊！"))
    t_seek = c.gap(c.find("找啊找"))
    t_det = c.gap(c.find("可是牧羊人一直找"))
    w = c.seg(0, t_call, 6, "2/4", "F# harmonic", nominal=108, label="search-walk")
    k = c.seg(t_call, t_seek, 3, "2/4", "A major", nominal=94, label="search-call")
    s = c.seg(t_seek, t_det, 5, "2/4", "F# harmonic", nominal=101, label="search-seek")
    d = c.seg(t_det, c.dur, 4, "2/4", "A major", nominal=91, label="search-determined")
    segs = (w, k, s, d)
    for sg in segs:
        sg.duck(1.5)
    walk = "A4:3/4 B4:1/4 C#5:1/2 F#5:1/2 | G#5:3/4 F#5:1/4 E#5:1/2 C#5:1/2 | " \
           "D5:3/4 C#5:1/4 D5:1/2 F#5:1/2 | E#5:3/4 D5:1/4 C#5:1"
    w.prog("F#m:2 | F#m:2 | F#m:2 | C#7:2 | Bm:2 | C#7:2")
    k.prog("D:2 | A:2 | A:2")
    s.prog("F#m:2 | F#m:2 | C#7:2 | Bm:2 | C#7:2")
    d.prog("D:2 | E:2 | F#m7:2 | E:2")
    k.sync("'小羊！小羊！': he calls (D)", 0, t_call, kind="change")
    s.sync("'找啊找': searching on (F# minor)", 0, t_seek, kind="change")
    d.sync("'可是牧羊人一直找': he never gives up (D)", 0, t_det, kind="change")

    def steps(sg, q0, q1, vel=40):
        for q_ in np.arange(q0, q1, 1.0):
            ch = sg.chord_at(q_ + 1e-3)
            p_ = ch.bass_note(37, 49) if int(q_) % 2 == 0 else _alt_bass(ch, 37, 49)
            sg.add("pz_lo", q_, 0.5, p_, vel, "arp", "s")
            for pt in ch.tones(61, 71)[:2]:
                sg.add("mandolin", q_ + 0.5, 0.25, pt, vel - 10, "arp", "s")

    # over high hills, along a winding path, across a stream: the walk, the shepherd's song in minor
    steps(w, 0, 12)
    w.mel("whistle", "r:2 | r:2 | " + walk, vel=44)
    w.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_ref=(37, 49))
    w.duck(3.0, parts=["whistle"])
    lv(w, ["whistle"], -16)
    w.expr(["pz_lo"], [(0, -16), (2, -13), (12, -12)])
    w.expr(["mandolin"], [(0, -21), (2, -17), (12, -17)])
    w.expr(["vla", "vln1"], [(0, -20), (2, -22), (12, -22)])
    i0 = c.find("跨过一条小河")
    stones = [t_ for t_ in (picture(c, "splash_small", c.ls(i0) - 0.3, c.le(i0) + 0.6) or [])][:4]
    if len(stones) >= 2:
        prev = 61
        for kk, ts in enumerate(stones):
            clear_near(c, ts)
            sg_, q_s = seg_at(c, segs, ts)
            pts = sg_.chord_at(q_s + 1e-3).tones(prev + 1, 81) or sg_.chord_at(q_s + 1e-3).tones(62, 81)
            prev = pts[0]
            sg_.add("pz_hi", q_s, _dq(sg_, q_s, 0.25), prev, 46, "arp", "h")
            sg_.add("mandolin", q_s, _dq(sg_, q_s, 0.25), prev, 42, "arp", "h")
            if kk in (0, len(stones) - 1):
                sg_.sync(f"a stepping stone ({kk + 1})", q_s, ts)
    # 'little lamb! where are you?': he stops and calls; the hills echo his call in the pause
    k.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    trem(k, "mandolin", 0, 6, "A4", 26)
    k.duck(2.5)
    k.expr(["vla", "vln1", "vc"], [(0, -21), (6, -22)])
    lv(k, ["mandolin"], -19)
    i_call = c.find("小羊！小羊！")
    a_, b_ = c.pause_after(i_call)
    echo_call(c, segs, a_ + 0.06, ["C#6", "A5"], min(0.3, max(0.12, (b_ - a_) * 0.4)), part="echo_whis", vel=44,
              dur_s=0.28)
    for sg in segs:
        lv(sg, ["echo_whis"], -12)
    # 'searching, searching; darker and darker, the path harder and harder': the walk again, darker
    steps(s, 0, 10)
    s.mel("whistle", "r:2 | " + walk, vel=42)
    s.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(37, 49))
    s.duck(3.0, parts=["whistle"])
    lv(s, ["whistle"], -17)
    lv(s, ["pz_lo"], -12)
    lv(s, ["mandolin"], -17)
    s.expr(["vla", "vln1"], [(0, -23), (10, -21)])
    hit(c, segs, "cloth", "找啊找", 0, "the thorny bushes (a pluck)", win=0.2, pluck=(59, 71), mando=(62, 74), vel=42)
    # 'but the shepherd kept on searching -- he would find it!': A major hope, a rising bass
    d.mel("whistle", "A4:3/4 B4:1/4 C#5:1/2 F#5:1/2 | E5:3/4 F#5:1/4 E5:1/2 G#4:1/2 | C#5:3/4 D5:1/4 E5:1/2 A5:1/2 | "
                     "G#5:1 B5:1", vel=46)
    steps(d, 0, 8, vel=42)
    strings(d, vel=34, lo=50, hi=71, bass=(40, 52), cb=(28, 40))
    d.duck(3.0, parts=["whistle"])
    d.expr(["whistle"], [(0, -17), (8, -16)])
    lv(d, ["pz_lo"], -11)
    lv(d, ["mandolin"], -16)
    d.expr(STR, [(0, -22), (6, -20), (8, -20)])
    hit(c, segs, "cloth", "可是牧羊人一直找", 0, "he stops, determined (a pluck)", pluck=(59, 71), vel=42)
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)


def found(c):
    """'忽然' -- a hush (E7sus4, high strings); far echoes of the narrator's 咩, then the lamb's bell answers its real
    bleat (the picture); F# minor on '在一块大石头后面' (a soft tremolo, the bell trembling), D E7 and a run up the A
    major scale -- the note the count never reached; A major on '找到了': the big warm arrival on the picture's sparkle
    (strings, horns, accordion, timpani, a cymbal breath, glockenspiel and the bell; the whistle on the high A); D on
    '牧羊人一点也没生气' (the bell as the lamb bleats), the lamb's motif turned major and joyful (whistle and bell, the
    accordion's oom-pah), a glint as the moon comes out, lifted up to the high A as he puts it on his shoulders; '找到你了'
    -- the shepherd's song's cadence, walking home (woodblock hooves)."""
    c.gain(-2.0)
    t_sud = c.ls(0)
    t_rock = c.gap(c.find("在一块大石头后面"))
    t_fd = c.at("找到了")
    t_kind = c.gap(c.find("牧羊人一点也没生气"))
    t_home = c.gap(c.find("找到你了"))
    p = c.seg(0, t_sud, 1, "2/4", "A major", nominal=None, label="found-still")
    h = c.seg(t_sud, t_rock, 2, "6/8", "A major", nominal=111, label="found-hear")
    r = c.seg(t_rock, t_fd, 2, "6/8", "A major", nominal=89, label="found-rock")
    j = c.seg(t_fd, t_kind, 1, "6/8", "A major", nominal=None, label="found-found")          # the arrival held
    k = c.seg(t_kind, t_home, 4, "6/8", "A major", nominal=113, label="found-carry")
    o = c.seg(t_home, c.dur, 2, "6/8", "A major", nominal=119, label="found-home")
    segs = (p, h, r, j, k, o)
    for sg in segs:
        sg.duck(1.5)
    p.prog("E:2")
    h.prog("E7sus4:3 | E7sus4:3")
    r.prog("F#m:3 | D:3/2 E7:3/2")
    j.prog("A:3")
    k.prog("D:3 | A:3 | D:3/2 E:3/2 | A:3")
    o.prog("D:3/2 E7:3/2 | A:3")
    h.sync("'忽然': he hears something (E7sus4)", 0, t_sud, kind="change")
    r.sync("'在一块大石头后面': behind a big rock (F# minor)", 0, t_rock, kind="change")
    j.sync("'找到了': found! (A major)", 0, t_fd, kind="change")
    k.sync("'牧羊人一点也没生气': not angry at all (D)", 0, t_kind, kind="change")
    o.sync("'找到你了': homeward (D)", 0, t_home, kind="change")
    # the walk's E rings on, fading into the hush
    p.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    p.add("pz_lo", 0, 1, "E2", 34, "arp", "s")
    p.expr(["vla", "vln1", "vc"], [(0, -19), (2, -23)])
    lv(p, ["pz_lo"], -14)
    # 'suddenly he heard: baa -- baa --': a hush; far echoes of the bleats, then the lamb's bell answers its bleat
    h.pad(["trem_hi", "trem_hi", "trem_hi"], 3, 69, 83, vel=28, bass_ref=(40, 52))
    h.add("vc", 0, 6, "E2", 28, "bass")
    for k_, tb in enumerate(syl(c, "咩——咩——", 2)):
        echo_call(c, segs, tb + 0.3, ["A5"], 0.0, part="echo_oca", vel=34 - 3 * k_, dur_s=0.25)
    t_bl = pic(c, "sheep", "忽然", 0)
    t_bell = t_bl if t_bl is not None else syl(c, "咩——咩——", 2)[1] + 0.45
    sg_, q_b = seg_at(c, segs, t_bell)
    bell(sg_, q_b, vel=44, lo=83, hi=95)
    sg_.sync("the lamb's bell answers its bleat" + (" (picture)" if t_bl is not None else ""), q_b, t_bell)
    h.expr(["trem_hi"], [(0, -26), (6, -24)])
    lv(h, ["vc"], -22)
    for sg in segs:
        lv(sg, ["echo_oca"], -13)
    # 'behind a big rock, the little lamb was shivering with cold': a soft tremolo, the bell trembling; a run up
    r.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 71, vel=30, bass_ref=(40, 52))
    bassline(r, "vc", 40, 52, 30)
    for q_ in np.arange(0, 3, 0.25):
        r.add("tinkle", q_, 0.25, "C#6" if int(q_ * 4) % 2 == 0 else "A5", 30, "arp", "S")
    run(r, "mandolin", 4.5, ["E5", "F#5", "G#5", "A5", "B5", "C#6", "D6", "E6", "G#6"], 1 / 6, vel=34,
        role="melody")
    r.expr(["trem_va", "trem_hi"], [(0, -23), (3, -22), (6, -19)])
    lv(r, ["vc"], -21)
    lv(r, ["tinkle"], -17)
    lv(r, ["mandolin"], -15)
    for sg in (p, h, r):
        lv(sg, ["tinkle"], -13 if sg is h else -17)
    # 'found!': A major -- the big warm arrival (on the picture's sparkle), the high A, bells
    t_fp, _ = lead(c, segs, "sparkle", "在一块大石头后面", 0, t_fd, t_fd + 0.6, "found (a sparkle)",
                   glock=(86, 98))
    q_f = qpos(j, c, t_fp, 0.0, 1.2) if t_fp is not None else 0.0
    j.add("whistle", 0, 3, "A5", 48, "melody")
    j.add("mandolin", 0, 3, "A5", 46, "melody")
    j.add("glock", q_f, _dq(j, q_f, 3.0), "A6", 46, "arp", "h")
    j.add("glock", q_f, _dq(j, q_f, 3.0), "E6", 40, "arp", "h")
    bell(j, q_f + 0.5, vel=40)
    j.add("timp", 0, 1.5, "A2", 44, "timp", "h")
    j.add("pz_cb", 0, 1, "A1", 50, "bass", "h")
    j.add("okit", 0, 2, 57, 28, "perc", "h")
    if t_fp is not None:
        j.sync("found (a sparkle)", q_f, t_fp)
    strings(j, vel=40, lo=55, hi=76, bass=(40, 52), cb=(28, 40))
    j.pad(["horn", "horn", "horn"], 3, 52, 67, vel=40, bass_ref=(40, 52))
    j.pad("accordion", 3, 57, 69, vel=36, bass_ref=(40, 52))
    j.duck(3.0)
    lv(j, ["whistle"], -15)
    lv(j, ["mandolin"], -15)
    lv(j, ["glock", "tinkle"], -12)
    lv(j, ["timp", "pz_cb"], -12)
    lv(j, "okit", -18)
    j.expr(STR, [(0, -19), (1.5, -16), (3, -17)])
    j.expr(["horn"], [(0, -22), (1.5, -18), (3, -19)])
    lv(j, ["accordion"], -21)
    # 'the shepherd was not angry at all; joyfully he lifted the lamb onto his shoulders': the lamb's motif, joyful
    k.mel("accordion", "A4:3/2 F#4:1 D4:1/2", vel=40)
    k.mel("whistle", "r:3 | " + bars(LAMB, 0, 2), vel=46)
    k.mel("tinkle", "r:3 | " + bars(LAMB, 0, 2), vel=36, role="fx")
    t_on = pic(c, "cloth", "牧羊人一点也没生气", 2)
    q_on = qpos(k, c, t_on, 9.0, 10.5) if t_on is not None else 9.0
    for kk, nm in enumerate(("A5", "C#6", "E6", "A6")):
        qq = q_on + 0.5 * kk
        dur = 0.5 if kk < 3 else 12.0 - qq
        k.add("whistle", qq, dur, nm, 46 + kk, "melody", "h" if kk == 0 else "")
        k.add("tinkle", qq, dur, nm, 34 + kk, "fx", "h" if kk == 0 else "")
    if t_on is not None and abs(k.t(q_on) - c.t0 - t_on) < 0.03:
        k.sync("onto his shoulders (the lift)", q_on, t_on)
    elif t_on is not None:
        accent(c, segs, t_on, "onto his shoulders (a pluck)", mando=(76, 88), vel=42)
    oom(k, 3, 12, vel=34, bass=(40, 52), hi=(57, 69))
    k.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    broken(k, "mandolin", 0, 12, (0, 1, 2, 1, 2, 1), 62, 76, vel=30, thin=True)
    k.duck(3.5, parts=["whistle", "tinkle"])
    lv(k, ["accordion"], -18, q1=3)
    lv(k, ["accordion"], -23, q0=3)
    k.expr(["whistle"], [(0, -17), (12, -15)])
    k.expr(["tinkle"], [(0, -19), (12, -17)])
    lv(k, ["pz_lo"], -13)
    lv(k, ["mandolin"], -18)
    k.expr(["vla", "vln1", "vc"], [(0, -21), (12, -21)])
    hit(c, segs, "sheep", "牧羊人一点也没生气", 0, "the lamb bleats (its bell)", bell=(84, 98), vel=40)
    hit(c, segs, "sparkle", "牧羊人一点也没生气", 0, "the moon comes out (a glint)", glock=(86, 98), celesta=(74, 86),
        vel=42)
    # 'found you! let's go home!': the shepherd's song's cadence, walking home
    o.mel("whistle", SHEP[6] + " | " + SHEP[7], vel=44)
    oom(o, 0, 6, vel=34, bass=(40, 52), hi=(57, 69))
    clop(o, 0, 6, vel=30)
    o.pad(["vla", "vla", "vln1"], 3, 50, 71, vel=30, bass_ref=(40, 52))
    o.duck(3.0, parts=["whistle"])
    lv(o, ["whistle"], -16)
    lv(o, ["pz_lo"], -13)
    lv(o, ["accordion"], -22)
    lv(o, "hand", -16)
    o.expr(["vla", "vln1"], [(0, -21), (6, -20)])
    for sg in segs:
        if sg is not j:
            lv(sg, ["glock", "celesta"], -12)
        lv(sg, ["pz_hi"], -12)


def party(c):
    """The village at night (A major jig, 6/8): a plucked vamp, the knock answered by a pluck and a woodblock, a pluck
    as each neighbour's door opens; the shepherd's song on the musette and the mandolin under '和我一起高兴吧' (a glint
    and the tambourine as '找到了' is cheered); the dance on '大家都好开心' -- whistle, fiddle and musette on the tune,
    the accordion's oom-pa-pa, tambourine and claps, the lamb's bell -- ending on A."""
    c.gain(-2.0)
    t_call = c.gap(c.find("和我一起高兴吧"))
    t_all = c.gap(c.find("大家都好开心"))
    k = c.seg(0, t_call, 4, "6/8", "A major", nominal=142, label="party-knock")
    h = c.seg(t_call, t_all, 4, "6/8", "A major", nominal=153, label="party-call")
    d = c.seg(t_all, c.dur, 4, "6/8", "A major", nominal=152, label="party-dance")
    segs = (k, h, d)
    for sg in segs:
        sg.duck(1.5)
    k.prog("A:3 | D:3 | A:3 | E7:3")
    h.prog(" | ".join(SHEP_PROG[:4]))
    d.prog(" | ".join(SHEP_PROG[4:8]))
    h.sync("'和我一起高兴吧': the dance begins (A)", 0, t_call, kind="change")
    d.sync("'大家都好开心': everyone dances (A)", 0, t_all, kind="change")
    # 'back home, he called his friends and neighbours': the vamp; the knocks answered
    oom(k, 0, 12, vel=36, bass=(40, 52), hi=(57, 69), cpart="guitar")
    k.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    knocks = [t_ for t_ in (pic(c, "hammer", None, kk) for kk in range(4)) if t_ is not None]
    for kk, tk in enumerate(knocks):
        clear_near(c, tk)
        sg_, q_k = accent(c, segs, tk, f"a knock on a door ({kk + 1})" if kk == 0 else None, pluck=(62, 74), vel=42)
        drum(sg_, q_k, 77, 40)
    for kk in range(2):                                      # the neighbours' doors open
        hit(c, segs, "cloth", None, kk, f"a door opens ({kk + 1})", mando=(69, 81) if kk == 0 else (74, 86), vel=40)
    k.expr(["pz_lo", "guitar"], [(0, -15), (3, -13), (12, -12)])
    k.expr(["vla", "vln2", "vln1"], [(0, -24), (12, -22)])
    # 'be happy with me! the sheep I lost is found!': the tune on the musette and the mandolin
    h.mel("musette", bars(SHEP, 0, 4), vel=44)
    h.mel("mandolin", bars(SHEP, 0, 4), vel=40, role="fx")
    oom(h, 0, 12, vel=36, bass=(40, 52), hi=(57, 69), lively=True)
    strings(h, vel=28, lo=50, hi=69, bass=(40, 52), cb=(28, 40))
    h.duck(3.0, parts=["musette", "mandolin"])
    h.expr(["musette"], [(0, -23), (1.5, -18), (12, -18)])
    h.expr(["mandolin"], [(0, -21), (1.5, -16), (12, -16)])
    lv(h, ["pz_lo"], -12)
    h.expr(["accordion"], [(0, -25), (1.5, -22), (12, -22)])
    h.expr(STR, [(0, -24), (12, -21)])
    # 'everyone was so happy, singing and celebrating': the dance
    d.mel("whistle", bars(SHEP, 4, 8), vel=48)
    d.mel("fiddle", bars(SHEP, 4, 8), vel=42, transpose=-12, role="fx")
    d.mel("musette", bars(SHEP, 4, 8), vel=40, role="fx")
    oom(d, 0, 12, vel=36, bass=(40, 52), hi=(57, 69), lively=True)
    strings(d, vel=30, lo=50, hi=71, bass=(40, 52), cb=None)
    for q_ in np.arange(1.5, 12, 1.5):
        drum(d, q_, 54, 34 if q_ % 3 == 0 else 28)
        if q_ % 3 == 1.5:
            drum(d, q_, 39, 30)
    bell(d, 9.0, vel=42)
    d.duck(3.0, parts=["whistle", "fiddle", "musette"])
    d.expr(["whistle"], [(0, -22), (1.5, -17), (12, -16)])
    d.expr(["fiddle"], [(0, -24), (1.5, -19), (12, -19)])
    d.expr(["musette"], [(0, -25), (1.5, -20), (12, -20)])
    d.expr(["pz_lo"], [(0, -17), (1.5, -12), (12, -12)])
    d.expr(["accordion"], [(0, -24), (1.5, -21), (12, -21)])
    d.expr(STR, [(0, -21), (12, -20)])
    lv(d, "hand", -16)
    lv(d, ["tinkle"], -12)
    t_sp = pic(c, "sparkle", "和我一起高兴吧")
    if t_sp is not None:                                     # '找到了!' -- the neighbours cheer: tambourine and a glint
        clear_near(c, t_sp)
        sg_, q_s = accent(c, segs, t_sp, "'找到了！' -- everyone cheers (a glint, tambourine)", glock=(86, 98), vel=44)
        drum(sg_, q_s, 54, 36)
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)


def meaning(c):
    """Back in the courtyard (D major, 6/8): guitar and bandoneon, a glint as the story page lands in Jesus's hands;
    his words over soft strings (B minor, G, A); D on '天上也会这样' -- heaven's joy on the picture's chime: a harp
    glissando, high strings, a choir 'ooh', the glockenspiel and the lamb's bell high and bright; the shepherd's song on
    the bandoneon on '耶稣和这些人一起吃饭' (Jesus is the shepherd), the lost lamb's bell; D on '在上帝眼里': the song's
    second phrase, warm and full (strings, horn, accordion, whistle), a mandolin step for each heart that pops up over
    the people, cadencing in D on '失去'."""
    c.gain(-2.0)
    t_w = c.gap(c.find("一个做错事的人"))
    t_hv = c.at("天上也会这样")
    t_like = c.gap(c.find("耶稣和这些人一起吃饭"))
    t_tr = c.gap(c.find("在上帝眼里"))
    a = c.seg(0, t_w, 2, "6/8", "D major", nominal=113, label="meaning-told")
    b = c.seg(t_w, t_hv, 2, "6/8", "D major", nominal=91, label="meaning-words")
    v = c.seg(t_hv, t_like, 2, "6/8", "D major", nominal=93, label="meaning-heaven")
    l = c.seg(t_like, t_tr, 4, "6/8", "D major", nominal=114, label="meaning-like")
    t = c.seg(t_tr, c.dur, 4, "6/8", "D major", nominal=120, label="meaning-treasure")
    segs = (a, b, v, l, t)
    for sg in segs:
        sg.duck(1.5)
    a.prog("D:3 | Em7:3/2 A7:3/2")
    b.prog("Bm:3 | G:3/2 A:3/2")
    v.prog("D:3 | G:3/2 A:3/2")
    l.prog("D:3 | A/C#:3 | Bm:3 | A:3")
    t.prog("D:3 | G:3 | G:3/2 A7:3/2 | D:3")
    a.sync("'讲完故事': back in the courtyard (D)", 0, 0.0, kind="change")
    b.sync("'一个做错事的人': Jesus's words (B minor)", 0, t_w, kind="change")
    v.sync("'天上也会这样': heaven's joy (D)", 0, t_hv, kind="change")
    l.sync("'耶稣和这些人一起吃饭': the shepherd's song (D)", 0, t_like, kind="change")
    t.sync("'在上帝眼里': every one is precious (D)", 0, t_tr, kind="change")
    # 'when the story was over, Jesus said': the courtyard again
    broken(a, "guitar", 0, 6, (0, 2, 4, 2, 4, 2), 50, 62, vel=34, thin=True)
    a.pad("bandoneon", 3, 54, 67, vel=34, bass_ref=(40, 52))
    a.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    lv(a, ["guitar"], -12)
    lv(a, ["bandoneon"], -21)
    lv(a, ["vla", "vln2", "vln1"], -23)
    hit(c, segs, "sparkle", None, 0, "the story page lands in his hands (a glint)", glock=(86, 98), vel=42)
    # 'when one who did wrong comes back to God': soft strings under his voice
    b.pad(["vla", "vla", "vln1"], 3, 50, 66, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(b, "cb", 28, 40, 28)
    broken(b, "guitar", 0, 6, (0, 2, 4, 2, 4, 2), 47, 59, vel=28, thin=True)
    b.duck(2.5)
    b.expr(STR, [(0, -22), (6, -21)])
    lv(b, ["guitar"], -14)
    # 'heaven celebrates like this, with joy!': light -- harp, high strings, choir 'ooh', glockenspiel, the bell
    t_hc, okh = lead(c, segs, "chime", "一个做错事的人", 0, t_hv, v.t(2.0) - c.t0, "heaven (a glint)",
                     glock=(86, 98), vel=42)
    q_hc = qpos(v, c, t_hc, 0.0, 2.0) if okh else 0.0
    sweep(v, q_hc + 0.02, 0.7, "D4", "D6", 24, 34, part="harp")
    v.pad(["vla", "vla", "vln1"], 3, 62, 81, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    v.pad("ooh", 3, 60, 76, vel=28, bass_ref=(40, 52))
    v.mel("tinkle", "D6:1/2 F#6:1/2 E6:1/2 D6:1 A5:1/2 | B5:1/2 D6:1 C#6:1/2 E6:1", vel=38)
    v.add("glock", q_hc, _dq(v, q_hc, 1.5), "F#6", 46, "arp", "h")
    v.add("celesta", q_hc, _dq(v, q_hc, 1.5), "A5", 40, "arp", "h")
    v.sync("heaven's light (harp, glockenspiel)" + (" (picture)" if okh else ""), q_hc, t_hc if okh else t_hv)
    v.add("glock", 3.0, 1.5, "D7", 34, "arp", "h")
    v.duck(2.5, parts=["tinkle", "ooh", "vln1", "vln2", "vla"])
    lv(v, ["harp"], -14)
    v.expr(["vla", "vln2", "vln1", "vc"], [(0, -22), (1.5, -19), (6, -19)])
    v.expr(["ooh"], [(0, -27), (2, -23), (6, -23)])
    lv(v, ["tinkle"], -14)
    hit(c, segs, "sparkle", "一个做错事的人", 0, "'欢欢喜喜' (a sparkle)", glock=(88, 100), vel=40)
    # 'Jesus eating with these people is like the shepherd looking for his lost lamb': the song on the bandoneon
    l.mel("bandoneon", "F#4:1 G4:1/2 A4:1 D5:1/2 | E5:1 D5:1/2 C#5:1 A4:1/2 | B4:1 A4:1/2 B4:1 D5:1/2 | "
                       "C#5:1 B4:1/2 A4:3/2", vel=48)
    broken(l, "guitar", 0, 12, (0, 2, 4, 2, 4, 2), 50, 62, vel=32, thin=True)
    l.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_ref=(40, 52))
    bassline(l, "vc", 40, 52, 30)
    t_lb = pic(c, "sheep", "耶稣和这些人一起吃饭")
    if t_lb is not None:                                     # '走丢的小羊': the lamb's bell
        accent(c, segs, t_lb, "the lost lamb (its bell)", bell=(84, 98), vel=38)
    else:
        for q_ in (4.5, 10.5):
            if not bool(l.score.speaking(l.t(q_))):
                bell(l, q_, vel=36)
    hit(c, segs, "pop", "耶稣和这些人一起吃饭", 0, "like the shepherd (a pluck)", mando=(69, 81), vel=38)
    l.duck(3.0, parts=["bandoneon"])
    l.expr(["bandoneon"], [(0, -20), (1.5, -15), (12, -15)])
    l.expr(["guitar"], [(0, -17), (1.5, -13), (12, -13)])
    l.expr(["vla", "vln2", "vln1", "vc"], [(0, -23), (12, -21)])
    lv(l, ["tinkle"], -13)
    # 'in God's eyes every one is precious; God does not want to lose a single one!': warm and full
    t.mel("whistle", "F#5:1 G5:1/2 A5:1 D6:1/2 | D6:1 E6:1/2 D6:1 B5:1/2 | B5:1 D6:1/2 C#6:1 E6:1/2 | D6:3", vel=46)
    t.mel("horn", "F#4:1 G4:1/2 A4:1 D5:1/2 | D5:1 E5:1/2 D5:1 B4:1/2 | B4:1 D5:1/2 C#5:1 E5:1/2 | D5:3", vel=42,
          role="fx")
    oom(t, 0, 12, vel=34, bass=(40, 52), hi=(57, 69))
    strings(t, vel=36, lo=50, hi=71, bass=(40, 52), cb=(28, 40))
    t.duck(4.5, parts=["whistle", "horn", "accordion"])
    t.expr(["whistle"], [(0, -22), (9, -20), (12, -19)])
    t.expr(["horn"], [(0, -21), (12, -18)])
    lv(t, ["pz_lo"], -12)
    lv(t, ["accordion"], -24)
    t.expr(STR, [(0, -22), (9, -19), (12, -19)])
    hit(c, segs, "chime", "在上帝眼里", 0, "in God's eyes (a glint)", glock=(86, 98), celesta=(74, 86), vel=40)
    hearts = [t_ for t_ in (picture(c, "pop", c.ls(c.find("在上帝眼里")) - 0.3) or [])][:6]
    if len(hearts) >= 2:                                     # '每一个人都是宝贝': a heart pops up over each person
        for t_ in hearts:
            clear_near(c, t_)
        climb(c, segs, hearts, part="mandolin", lo=69, hi=93, vel=30, sync=(0, len(hearts) - 1),
              what="a heart pops up", glock=False)
    hit(c, segs, "sparkle", "在上帝眼里", 0, "'失去': not one lost (a glint)", glock=(86, 98), vel=40)
    for sg in segs:
        lv(sg, ["glock"], -12)


def end(c):
    """The modern frame again (D major, 6/8): the shepherd's song's head on the kalimba ('上帝就像这个牧羊人'; a glint as
    the picture-book shepherd appears); D on '你，就是' -- the lullaby, which is the lamb's motif, on the kalimba with the
    lamb's bell as the child squeezes the toy lamb (the child is the little lamb); a glint on '上帝都会来找你'; B minor on
    '如果你做错了事' (the lamb's motif in minor; Em7, A7sus4 A7 under '对不起'); D warm on '我想回到你身边'; G on the last
    question, very soft (D/F#, Bm7); A7sus4 at the end of '你想对牧羊人说什么呢', hanging through the pause; the final D
    chord on the end card (kalimba, guitar and bell together, then rolled), ringing to the end."""
    c.gain(-3.0)
    t_you = c.at("你，就是")
    t_sorry = c.ls(c.find("如果你做错了事"))
    t_back = c.at("我想回到你身边")
    t_q = c.gap(c.find("小朋友，如果你是那只小羊"))
    t_f = c.le(c.find("你想对牧羊人说什么呢"))
    t_raw = pic(c, "chime", "你想对牧羊人说什么呢")
    t_card = t_raw if t_raw is not None and t_f + 0.5 <= t_raw <= c.dur - 0.6 else None
    t_fin = t_card if t_card is not None else max(t_f + 0.8, c.dur - 1.3)
    s = c.seg(0, t_you, 2, "6/8", "D major", nominal=91, label="end-shepherd")
    l = c.seg(t_you, t_sorry, 4, "6/8", "D major", nominal=104, label="end-lamb")
    o = c.seg(t_sorry, t_back, 3, "6/8", "D major", nominal=96, label="end-sorry")
    h = c.seg(t_back, t_q, 1, "6/8", "D major", nominal=87, label="end-home")
    q = c.seg(t_q, t_f, 3, "6/8", "D major", nominal=77, label="end-question")
    sp = c.seg(t_f, t_fin, 1, "2/4", "D major", nominal=None, label="end-space")
    f = c.seg(t_fin, c.dur, 1, "2/4", "D major", nominal=None, rit=0.3, label="end-final-chord")
    segs = (s, l, o, h, q, sp, f)
    for sg in (s, l, o, h, q):
        sg.duck(1.5)
    s.prog("D:3 | A/C#:3")
    l.prog(" | ".join(LULL_PROG[:4]))
    o.prog("Bm:3 | Em7:3 | A7sus4:3/2 A7:3/2")
    h.prog("D:3")
    q.prog("G:3 | D/F#:3 | Bm7:3")
    sp.prog("A7sus4:2")
    f.prog("D:2")
    l.sync("'你，就是': you are the little lamb (D)", 0, t_you, kind="change")
    o.sync("'如果你做错了事': if you did wrong (B minor)", 0, t_sorry, kind="change")
    h.sync("'我想回到你身边': back home (D)", 0, t_back, kind="change")
    q.sync("'小朋友，如果你是那只小羊': the last question (G)", 0, t_q, kind="change")
    sp.sync("'你想对牧羊人说什么呢': A7sus4, the question hangs", 0, t_f, kind="change")
    f.sync("the final D chord (the end card)", 0, t_fin, kind="change")
    f.sync("the end card: the final chord" if t_card is not None else "the final chord", 0, t_fin)
    # 'child, God is like this shepherd': the song's head on the kalimba
    s.mel("kalimba", "F#5:1 G5:1/2 A5:1 D6:1/2 | E6:1 D6:1/2 C#6:1 A5:1/2", vel=48)
    broken(s, "guitar", 0, 6, (0, 2, 4, 2, 4, 2), 50, 62, vel=32, thin=True)
    s.pad(["vla", "vla", "vln1"], 3, 50, 67, vel=28, bass_ref=(37, 49))
    bassline(s, "vc", 37, 49, 30)
    s.duck(3.0, parts=["kalimba"])
    lv(s, ["kalimba"], -13)
    lv(s, ["guitar"], -12)
    s.expr(["vla", "vln1", "vc"], [(0, -22), (6, -21)])
    # 'you are his precious little lamb; however far you go, God will come and find you': the lullaby and the bell
    l.mel("kalimba", bars(LULL, 0, 4), vel=48)
    t_sq = pic(c, "pop", "小朋友，上帝就像")
    if t_sq is not None:                                     # the child squeezes the toy lamb: its bell
        accent(c, segs, t_sq, "the toy lamb squeezed (its bell)", bell=(84, 98), vel=42)
    else:
        bell(l, 0.0, vel=38)
    broken(l, "guitar", 0, 12, (0, 2, 4, 2, 4, 2), 50, 62, vel=32, thin=True)
    strings(l, vel=32, lo=50, hi=67, bass=(40, 52), cb=None)
    l.duck(3.0, parts=["kalimba"])
    l.expr(["kalimba"], [(0, -16), (1.5, -13), (12, -13)])
    l.expr(["guitar"], [(0, -16), (1.5, -12), (12, -12)])
    l.expr(STR, [(0, -21), (12, -21)])
    hit(c, segs, "sparkle", "不管你走多远", 0, "God will come and find you (a glint)", glock=(86, 98), vel=40)
    # 'if you did wrong, don't be afraid; you can tell God: I'm sorry': B minor, tender
    o.mel("kalimba", "D5:1/2 F#5:1/2 E5:1/2 D5:1 B4:1/2 | G5:1 F#5:1/2 E5:1 B4:1/2 | D5:3/2 C#5:3/2", vel=44)
    broken(o, "guitar", 0, 9, (0, 2, 4, 2, 4, 2), 47, 59, vel=30, thin=True)
    o.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=30, bass_part="vc", bass_lo=40, bass_hi=52)
    o.duck(3.0, parts=["kalimba"])
    lv(o, ["kalimba"], -14)
    lv(o, ["guitar"], -13)
    o.expr(["vla", "vln1", "vc"], [(0, -22), (9, -21)])
    # 'I want to come back to you': D, warm
    roll_chord(h, 0, 57, 81, vel=30, part="kalimba")
    h.mel("kalimba", "r:3/2 F#5:1 A5:1/2", vel=38, role="counter")
    strings(h, vel=34, lo=50, hi=71, bass=(40, 52), cb=(28, 40))
    bell(h, 1.5, vel=34)
    lv(h, ["kalimba"], -14)
    h.expr(STR, [(0, -19), (1.5, -19), (3, -20)])
    # 'if you were that lamb, what would you say to the shepherd when he found you?': very soft
    q.mel("kalimba", "B4:1/2 D5:1/2 G5:1/2 F#5:1 E5:1/2 | D5:1/2 F#5:1/2 A5:1/2 G5:1 F#5:1/2 | "
                     "D5:1/2 F#5:1/2 E5:1/2 D5:3/2", vel=42)
    broken(q, "guitar", 0, 9, (0, 2, 4, 2, 4, 2), 43, 59, vel=28, thin=True)
    q.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=40, bass_hi=52)
    q.duck(2.5)
    lv(q, ["kalimba"], -15)
    lv(q, ["guitar"], -14)
    q.expr(["vla", "vln1", "vc"], [(0, -22), (9, -23)])
    hit(c, segs, "pop", "小朋友，如果你是那只小羊", 0, "the toy lamb lifted (a pluck)", pluck=(62, 74), vel=36)
    # the space after the question: A7sus4 hanging, very soft; the bell asks once
    sp.pad(["vla", "vla", "vln1"], 3, 50, 69, vel=28, bass_part="vc", bass_lo=40, bass_hi=52)
    sp.add("guitar", 0, 2, "A2", 32, "arp", "h")
    sp.add("guitar", 0.06, 1.94, "E3", 28, "arp")
    sp.add("tinkle", 0.5, 1.5, "E6", 30, "arp")
    sp.expr(["vla", "vln1", "vc"], [(0, -22), (1, -24), (2, -26)])
    lv(sp, ["guitar"], -15)
    lv(sp, ["tinkle"], -18)
    # the final D chord on the end card: kalimba, guitar and bell together, then rolled up; strings
    for nm in ("D3", "A3", "F#4"):
        f.add("guitar", 0, 2, nm, 44, "arp", "r")
    for nm in ("D5", "A5"):
        f.add("kalimba", 0, 2, nm, 46, "arp", "r")
    f.add("tinkle", 0, 1.5, "F#6", 40, "arp", "r")
    f.add("glock", 0, 1.5, "D7", 34, "arp", "r")
    for k_, nm in enumerate(["A4", "D5", "F#5", "A5", "D6"]):
        f.add("kalimba", 0.4 + 0.08 * k_, 1.6 - 0.08 * k_, nm, 34 - 2 * k_, "arp", "r")
    strings(f, vel=32, lo=50, hi=69, bass=(40, 52), cb=(28, 40), q0=0.25)
    f.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -23), (0.5, -22), (1.4, -24), (2, -30)])
    f.expr(["guitar", "kalimba", "tinkle", "glock"], [(0, -16), (2, -21)])
    if t_card is None and t_raw is not None:                # the end card earlier than the space allows
        accent(c, segs, t_raw, "the end card (a glint)", glock=(86, 98), vel=40)
    for sg in segs:
        if sg not in (f, sp):
            lv(sg, ["glock", "pz_hi", "tinkle"], -13)


SCENE_CUES = {
    "s01_title": title, "s02_question": question, "s03_meal": meal, "s04_story": story, "s05_flock": flock,
    "s06_count": count, "s07_alone": alone, "s08_search": search, "s09_found": found, "s10_party": party,
    "s11_meaning": meaning, "s12_end": end,
}

# Hit points defined by the narration text (audio/music_check.py REQUIRED_HITS format: (scene, phrase, mode, kind)).
REQUIRED_HITS = [
    ("s02_question", "今天", "line", "change"),                    # the story begins (D)
    ("s03_meal", "来的人里", "gap", "change"),                      # the tax collectors (E minor)
    ("s03_meal", "还有一些人", "gap", "change"),                    # nobody liked them (B minor)
    ("s03_meal", "可是耶稣很欢迎他们", "gap", "change"),            # the shepherd's song in the courtyard (D)
    ("s03_meal", "旁边站着几个法利赛人", "gap", "change"),          # the Pharisees (B minor)
    ("s03_meal", "他们皱着眉头", "phrase", "change"),               # whispering (E minor)
    ("s03_meal", "哼", "line", "hit"),                              # hmph!
    ("s04_story", "如果你有一百只羊", "gap", "change"),             # Jesus's question (D)
    ("s04_story", "你会怎么做呢", "phrase", "change"),              # the question hangs (E7sus4)
    ("s05_flock", "耶稣的故事里", "line", "change"),                # the shepherd's song (A)
    ("s05_flock", "一百只羊，好多好多", "line", "change"),          # the whole flock (A)
    ("s05_flock", "每天早上", "gap", "change"),                     # the morning walk (A)
    ("s05_flock", "有一只小羊", "gap", "change"),                   # the lamb's motif (A)
    ("s05_flock", "一抬头", "phrase", "change"),                    # it looks up (E7sus4)
    ("s06_count", "一只，两只", "gap", "change"),                   # the count begins (D)
    ("s06_count", "数啊数，数啊数", "gap", "change"),               # counting on (G)
    ("s06_count", "九十七", "gap", "change"),                       # ninety-seven (D)
    ("s06_count", "数啊数……还是", "gap", "change"),                 # the recount (D)
    ("s06_count", "少了一只小羊", "phrase", "change"),              # one is missing (B minor)
    ("s06_count", "我的小羊呢", "gap", "change"),                   # where is my lamb? (E minor)
    ("s06_count", "牧羊人把九十九只羊", "gap", "change"),           # he sets off (D)
    ("s07_alone", "天黑了", "phrase", "change"),                    # night falls (Bm7)
    ("s07_alone", "小羊好害怕", "gap", "change"),                   # afraid (F# minor)
    ("s08_search", "小羊！小羊！", "gap", "change"),                # he calls (D)
    ("s08_search", "找啊找", "gap", "change"),                      # searching on (F# minor)
    ("s08_search", "可是牧羊人一直找", "gap", "change"),            # he never gives up (D, rising)
    ("s09_found", "忽然", "line", "change"),                        # a hush (E7sus4)
    ("s09_found", "在一块大石头后面", "gap", "change"),             # behind a big rock (F# minor)
    ("s09_found", "找到了", "phrase", "change"),                    # found! (A major)
    ("s09_found", "牧羊人一点也没生气", "gap", "change"),           # not angry at all (D)
    ("s09_found", "找到你了", "gap", "change"),                     # homeward (D)
    ("s10_party", "和我一起高兴吧", "gap", "change"),               # the dance begins (A)
    ("s10_party", "大家都好开心", "gap", "change"),                 # everyone dances (A)
    ("s11_meaning", "一个做错事的人", "gap", "change"),             # Jesus's words (B minor)
    ("s11_meaning", "天上也会这样", "phrase", "change"),            # heaven's joy (D)
    ("s11_meaning", "耶稣和这些人一起吃饭", "gap", "change"),       # the shepherd's song (D)
    ("s11_meaning", "在上帝眼里", "gap", "change"),                 # every one is precious (D)
    ("s12_end", "你，就是", "phrase", "change"),                    # you are the little lamb (D)
    ("s12_end", "如果你做错了事", "line", "change"),                # if you did wrong (B minor)
    ("s12_end", "我想回到你身边", "phrase", "change"),              # back home (D)
    ("s12_end", "小朋友，如果你是那只小羊", "gap", "change"),       # the last question (G)
    ("s12_end", "你想对牧羊人说什么呢", "end", "change"),           # A7sus4: the question hangs
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or None,
# index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.
PICTURE_HITS = [
    ("s01_title", "sheep", None, 0, 0.0, "hit", "the little lamb bleats (its bell)"),
    ("s01_title", "chime", None, 0, 0.0, "hit", "the title appears (a glint)"),
    ("s01_title", "pop", None, 0, 0.0, "hit", "title character 1 pops in (a mandolin step)"),
    ("s01_title", "pop", None, 3, 0.0, "hit", "title character 4 pops in (a mandolin step)"),
    ("s01_title", "sparkle", None, 0, 0.0, "hit", "the title sparkles"),
    ("s01_title", "sparkle", None, 1, 0.0, "hit", "the title sparkles again"),
    ("s02_question", "sparkle", None, 0, 0.0, "hit", "the child (a glint)"),
    ("s02_question", "pop", None, 0, 0.0, "hit", "mum is gone (a pluck)"),
    ("s02_question", "cloth", None, 0, 0.0, "hit", "the hug (a kalimba roll and the bell)"),
    ("s02_question", "sparkle", "今天", 0, 0.0, "hit", "the toy lamb (its bell)"),
    ("s03_meal", "coins", "来的人里", 0, 0.0, "hit", "the first coin on the stack"),
    ("s03_meal", "coins", "来的人里", 5, 0.0, "hit", "the sixth coin on the stack"),
    ("s03_meal", "crunch", "可是耶稣很欢迎他们", 0, 0.0, "hit", "bread is broken (a pluck)"),
    ("s03_meal", "cheer", "可是耶稣很欢迎他们", 0, 0.0, "hit", "the table laughs (tambourine, a strum)"),
    ("s04_story", "chime", None, 0, 0.0, "hit", "the story page pops open (a glint)"),
    ("s04_story", "sheep", "如果你有一百只羊", 0, 0.0, "hit", "a sheep in the story page (its bell)"),
    ("s04_story", "sheep", "如果你有一百只羊", 1, 0.0, "hit", "'丢了一只': one bell note falls away"),
    ("s04_story", "whoosh", "如果你有一百只羊", 0, 0.0, "hit", "the page whooshes into the story (a run up)"),
    ("s04_story", "sparkle", "如果你有一百只羊", 1, 0.0, "hit", "the story page glints"),
    ("s05_flock", "pop", None, 0, 0.0, "hit", "he loves every one (a pluck)"),
    ("s05_flock", "sheep", "一百只羊，好多好多", 0, 0.0, "hit", "a sheep of the hundred bleats (its bell)"),
    ("s05_flock", "sparkle", "每天早上", 0, 0.0, "hit", "morning (a glint)"),
    ("s05_flock", "sheep", "每天早上", 0, 0.0, "hit", "a grazing sheep bleats (its bell)"),
    ("s05_flock", "sparkle", "有一只小羊", 0, 0.0, "hit", "the little lamb's bell"),
    ("s05_flock", "sparkle", "一抬头", 0, 0.0, "hit", "the lamb lands (its bell)"),
    ("s05_flock", "sparkle", "一抬头", 1, 0.0, "hit", "'咦？' (a plucked question)"),
    ("s05_flock", "sparkle", "一抬头", 2, 0.0, "hit", "'大家都不见了': F# minor, the bell alone"),
    ("s06_count", "sparkle", None, 0, 0.0, "hit", "the lamb far away (its bell)"),
    ("s06_count", "pop", "一只，两只", 0, 0.0, "hit", "'一只': the first sheep counted (a pluck)"),
    ("s06_count", "pop", "九十七", 0, 0.0, "hit", "'九十七' (a pluck)"),
    ("s06_count", "pop", "九十七", 2, 0.0, "hit", "'九十九' (a pluck, C#6 held)"),
    ("s06_count", "cloth", "九十七", 0, 0.0, "hit", "'我再数一遍' (a plucked upbeat)"),
    ("s06_count", "pop", "数啊数……还是", 0, 0.0, "hit", "the recount: the first quick pop"),
    ("s06_count", "pop", "数啊数……还是", 5, 0.0, "hit", "'还是九十九只': C#6 again on the big 99, then wah wah"),
    ("s06_count", "sparkle", "我的小羊呢", 0, 0.0, "hit", "'我要去找它' (a glint)"),
    ("s07_alone", "sparkle", None, 0, 0.0, "hit", "the lamb alone (its bell)"),
    ("s08_search", "splash_small", "跨过一条小河", 0, 0.0, "hit", "the first stepping stone (a pluck)"),
    ("s08_search", "splash_small", "跨过一条小河", 3, 0.0, "hit", "the fourth stepping stone (a pluck)"),
    ("s08_search", "cloth", "找啊找", 0, 0.0, "hit", "into the thorny bushes (a pluck)"),
    ("s08_search", "cloth", "可是牧羊人一直找", 0, 0.0, "hit", "he stops, determined (a pluck)"),
    ("s09_found", "sheep", "忽然", 0, 0.0, "hit", "the lamb's bell answers its bleat"),
    ("s09_found", "sparkle", "在一块大石头后面", 0, 0.0, "hit", "found ('找到了': A major on the sparkle)"),
    ("s09_found", "sheep", "牧羊人一点也没生气", 0, 0.0, "hit", "the lamb bleats (its bell)"),
    ("s09_found", "sparkle", "牧羊人一点也没生气", 0, 0.0, "hit", "the moon comes out (a glint)"),
    ("s09_found", "cloth", "牧羊人一点也没生气", 2, 0.0, "hit", "onto his shoulders (the lift to the high A)"),
    ("s10_party", "hammer", None, 0, 0.0, "hit", "a knock on a door"),
    ("s10_party", "cloth", None, 0, 0.0, "hit", "a door opens (1)"),
    ("s10_party", "cloth", None, 1, 0.0, "hit", "a door opens (2)"),
    ("s10_party", "sparkle", "和我一起高兴吧", 0, 0.0, "hit", "'找到了！' -- everyone cheers (a glint, tambourine)"),
    ("s11_meaning", "sparkle", None, 0, 0.0, "hit", "the story page lands in his hands (a glint)"),
    ("s11_meaning", "chime", "一个做错事的人", 0, 0.0, "hit", "heaven's light on the chime (harp, glockenspiel)"),
    ("s11_meaning", "sparkle", "一个做错事的人", 0, 0.0, "hit", "'欢欢喜喜' (a sparkle)"),
    ("s11_meaning", "pop", "耶稣和这些人一起吃饭", 0, 0.0, "hit", "like the shepherd (a pluck)"),
    ("s11_meaning", "sheep", "耶稣和这些人一起吃饭", 0, 0.0, "hit", "the lost lamb (its bell)"),
    ("s11_meaning", "chime", "在上帝眼里", 0, 0.0, "hit", "in God's eyes (a glint)"),
    ("s11_meaning", "pop", "在上帝眼里", 0, 0.0, "hit", "a heart pops up (1)"),
    ("s11_meaning", "pop", "在上帝眼里", 5, 0.0, "hit", "a heart pops up (6)"),
    ("s11_meaning", "sparkle", "在上帝眼里", 0, 0.0, "hit", "'失去': not one lost (a glint)"),
    ("s12_end", "pop", "小朋友，上帝就像", 0, 0.0, "hit", "the toy lamb squeezed (its bell)"),
    ("s12_end", "sparkle", "不管你走多远", 0, 0.0, "hit", "God will come and find you (a glint)"),
    ("s12_end", "pop", "小朋友，如果你是那只小羊", 0, 0.0, "hit", "the toy lamb lifted (a pluck)"),
    ("s12_end", "chime", "你想对牧羊人说什么呢", 0, 0.0, "hit", "the end card: the final D chord"),
]
