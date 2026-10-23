"""The background score for 耶稣降生 (Luke 1:26-38, 2:1-20; Matthew 2:1-11; ~4:57) -- one continuous piece in 12 cues.

Read by audio/score.py when the story is "nativity" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework as the earlier scores (audio/scorekit.py,
audio/scorelib.py): every cue starts at its scene's global start, is planned in whole bars whose tempo follows the
real line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap), never to fixed times.  Where a
continuous tune runs across an unsynced segment boundary (the gift theme in s02 and s12, the shepherds' run in s09)
the boundary is placed for one even tempo.  Hits that show an on-screen action follow the PICTURE: pic() reads the
scene's own sound-effect cues at build time (engine.loader.build_scene(...).sfx_cues) and picks them exactly as
music_check picks a PICTURE_HITS target (the k-th cue of a name from the start of the LINE containing a phrase);
hit() puts a synced accent there on tones of the chord sounding (clearing harp / pizzicato figures within 0.12 s so
it is one clear attack); lead() gives a scene moment's main attack to the picture when the cue falls inside that
moment's own segment (the light in s03, the angels in s07 and s08, the star in s10 and s11, the baby in s06...) and
otherwise accents the cue on its own, so every listed picture hit is always placed.  The narration phrase marks where
the harmony arrives (a 'change' in REQUIRED_HITS); a scene that does not build falls back to the narration.  Cues
in a scene's last second (the last stars in s06, the sign's second sparkle in s07) are accented but not listed: a
re-timed narration can push them past the cue.  syl() times the three gifts on the narrator's own voice.

Colour: a warm carol and lullaby film, unlike the six earlier scores (Jonah's D-major sea, Daniel's Persian court in A
hijaz, David's G pipe tune, Noah's B-flat march, Joseph's D clarinet and Egyptian hijaz, the Storm's Galilean
mixolydian folk).  Home key E-flat major, in 3/4 and 6/8; the instruments are the night's: music box, celesta,
glockenspiel and tubular bells, harp, a recorder (the girl from Nazareth, the shepherds), gentle strings, choir 'aah'
for the angels (General MIDI Choir Aahs) and 'ooh' for the starry night; a radiant D major with trumpet, horns,
trombone, choir, bells and timpani for the heavenly host; for the wise men an English horn over a drone with a
hammered dulcimer and finger cymbals in C dorian, whose notes are E-flat lydian -- the star that rises over the East
shines lydian (with A natural), and when it returns over Bethlehem it shines in plain E-flat (A-flat: home).  The
cosy modern frame (s02, s12) is a music-box waltz with sleigh bells in the narration pauses.  Five General MIDI
voices the shared orchestra does not list are registered here for this story only (_EXTRA): recorder, English horn,
trumpet, dulcimer, tubular bells.  No carol is quoted: every tune below is original; the theme avoids the rising 3-5-8
that opens most of the earlier films' themes.

Themes (q = quarter note)
  The gift theme -- God's gift, Christmas (E-flat, 3/4; its head is the star motif x = sol, mi'. re' mi', a rising
  sixth that twinkles):
     b1 Eb      Bb4 G5. F5            b5 Eb      Bb4 G5. F5
     b2 Eb      G5 Eb5--              b6 Cm      G5 C6--
     b3 Ab      C5 Eb5 Ab5            b7 Ab/C B-flat7  Ab5 G5 F5 D5
     b4 Bb      F5---                 b8 Eb      Eb5---
     x alone: the title (recorder), the star rising (celesta + glockenspiel) and returning, the angels' Gloria (the
     trumpet's sol-mi'), the shepherds' 'Saviour' (horn, in D); the theme on the music box on '圣诞节' (s02), on the
     horn for '他就是天使说的救主' (s09); its climax (b5-b7 + a falling la' sol' fa' | mi' re' do' ti | do') for the
     treasures (s11) and for '耶稣，才是上帝送给全世界最好的礼物' (s12).
  The lullaby -- the manger (E-flat, 6/8; the star motif turned round: mi' re' mi' falling a sixth to sol):
     G5 F5. G5 Bb4. | C5-- Ab4 C5. | Bb4 Eb5. D5 C5. | Bb4--- || G5 F5. G5 Bb4. | C5 Eb5. G5-- | Ab5 G5. F5 D5. | Eb5
     (Eb Ab Eb/Bb-B-flat7 B-flat | Eb Cm Ab-B-flat7 Eb); celesta over a rocking harp; foreshadowed on '他是上帝的儿子'
     (s03) and '小宝宝' (s04); the birth (s06); the sign, in D (s07); '找到了' and Mary pondering (s09); the kneeling
     wise men (s11).
  Mary's theme (A-flat, 3/4, recorder; a nod -- a falling fifth -- and a step up):
     Eb5-- Ab4 | Db5. C5 Db5 | Eb5 C5 Ab4 | Bb4--- || Eb5-- Ab4 | F5. Eb5 Db5 | C5. Bb4 G4 | Ab4  (Ab Db/F Ab Eb ...)
     Nazareth (s03); its close under '我是上帝的使女' is left to the harmony (her voice is thin in 1-4 kHz) and answered
     at once by Joseph's horn with her motif (s04); in E-flat on the road to Bethlehem.
  The shepherds' tune (B-flat, 6/8): D5 Eb5 F5 Bb5. F5 | G5 F5 Eb5 D5. Bb4 | C5 D5 Eb5 F5. A4 | Bb4 F4 Bb4-- ...
     slow, a siciliana on the recorder over a B-flat/F drone in the fields (s07); quick, running to Bethlehem, and
     happy, telling everyone (s09).
  The caravan (C dorian, 2/4, English horn; the raised sixth A over F major, the dorian IV):
     C4. D4 | Eb4 G4 | A4. G4 | F4-- (Cm Cm F F); turned major and led by the star in s11: Eb4. F4 | G4 Bb4 | C5. Bb4 |
     Ab4-- (Eb Eb Ab B-flat7).
  The three gifts (s11): one chime each on the picture's sparkles (else as the narrator names them) over an E-flat
     pedal -- 黄金 the glockenspiel (Eb), 乳香 the celesta and harp (Ab/Eb), 没药 a tubular bell (Bb/Eb).

Cue table (scene: key / meter -- what the music does; picture hits in brackets)
  s01 title     Eb 3/4    x on the recorder, harp, strings, 'ooh' [the title's glint, a celesta step for its first and
                          fourth character, a sparkle]
  s02 question  Eb 3/4    music-box waltz, sleigh bells in the pauses; the question hangs on B-flat7sus4; the gift theme
                          b1-b2 on '圣诞节' (change), b7-b8 to E-flat [an ornament's ping, the cheer, '圣诞节', the tree
                          lights up (the passing re' gives way to its chime), two more sparkles]
  s03 angel     Ab -> C -> Ab   Mary's theme (recorder); D-flat '有一天'; C on '忽然亮起来了' (change; the light on its
                          chime: harp up, bells, glockenspiel and celesta, choir 'aah'); F/C as the angel shines (a
                          bell); A minor, startled (a plucked flick as she jumps); Gabriel over choir and strings (F C/E
                          Dm7 G7sus4 C, the lullaby's head on '他是上帝的儿子'); Mary's question (Am F G, low strings
                          only); Dm7 G7sus4 G7 -> C radiant on '没有做不到的事' (change); F minor and A-flat on '我愿意'
                          (change) [light, angel, jump, the name Jesus, the blessing, Mary's yes]
  s04 journey   Ab -> Bb -> Eb   Joseph: Mary's motif on the horn; B-flat on '那时候' (change): the emperor's little
                          fanfare (trumpet, horns, timpani), then a pizzicato step for each head counted; F7 under the
                          herald's own horn (snare roll, timpani -- no orchestral brass); walking home (pizzicato,
                          clarinet); E-flat on '伯利恒' (change): Mary's theme on the recorder; the lullaby's head on
                          '小宝宝' (change); the long walk, 6/8, the donkey's hooves [Joseph, Mary, the emperor, the first
                          head, the scroll, Bethlehem on the map, the first and last road dots, the road, the baby's
                          heart]
  s05 no room   Bb -> Gm -> Eb   the crowd (busy pizzicato, oboe and clarinet chatter, woodblocks); G minor on '客店里'
                          (change), a lonely bassoon to D7; the deceptive E-flat on '他们只好' (change), warm and humble,
                          hanging on B-flat7sus4 [squeezed in the crowd, the knock at the inn door, the lamp lit]
  s06 birth     Eb 6/8    night (B-flat7sus4); E-flat glowing on '出生了' (change; the glow on the picture's chime); the
                          lullaby on '马利亚用布'; E-flat on '小耶稣睡着了' (change); the stars over E-flat add9 [the glow,
                          the manger, the ox munching (guiro, bassoon), asleep, the first two stars]
  s07 shepherds Bb -> D   the pastoral (recorder siciliana over a drone); A7sus4 on '忽然' (change) and the angel on its
                          chime; D major on '上帝的光' (change, a harp rising with the picture's glow); B minor, afraid;
                          'fear not' (G D/F# Em7 A7sus4); D on '今天，在伯利恒' (change): x on the horn; the lullaby in
                          D for the sign (its entrance a synced attack), half cadence on A [the angel, good news, the
                          Saviour, wrapped in cloths]
  s08 choir     D         B minor on '忽然' (change), the host appears on its chime and multiplies (a celesta step per
                          angel; B minor held, Em7 A7sus4, horns, a timpani roll); A7 '一起赞美上帝'; the Gloria in D in
                          the pause (change: trumpet x, choir, brass, bells, cymbal, timpani -- the film's loudest
                          moment, then held, ducked 10 dB, under the angels' song); G on '在地上' (change); the bells
                          again in the next pause (a synced attack); G on '地上，上帝要把平安' (change): the gift
                          theme's cadence on the horn, landing on D with the picture's 'peace on earth' chime [the
                          host, three angels, glory, peace, heaven, peace on earth]
  s09 visit     D -> Bb -> Eb   the angels go up (harp from the picture's whoosh, choir fading); B-flat glances on
                          '牧羊人你看看我' (change); E-flat F7 '我们快去'; the shepherds' run (change) and search at one
                          tempo; E-flat on '找到了' (change; the lullaby's first note on the picture's sparkle); the gift
                          theme on the horn on '他就是天使说的救主' (change); the shepherds' tune on '牧羊人好开心' (change);
                          A-flat add9, amazed; the lullaby, very soft (E-flat Cm7 B-flat7 E-flat), on '马利亚呢' (change)
                          [the angels leave, found,
                          the Saviour, sent by God, amazed, kept in her heart]
  s10 star      C dorian -> Eb lydian -> C dorian   the East (English horn over a C drone, dulcimer, finger cymbals,
                          celesta stars); B-flat F7sus4 rising (a harp sweep as the picture's star starts to rise);
                          E-flat
                          lydian on '一颗特别的星星' (change; x on celesta and glockenspiel from the picture's chime);
                          F/E-flat sparkle, a horn call on '有一位王出生了', G; the caravan on '他们出发了' (change), its
                          low drum on the camels' steps [the stargazers' star, the star, the king, first and fifth step]
  s11 gifts     Eb        the caravan's tail (G minor); E-flat on '忽然' (change) and x, gold, on the star's chime; the
                          caravan theme in E-flat; A-flat on '停在了' (change; a bell on the picture's sparkle); x bright
                          on '博士们高兴极了' (change); the lullaby as they kneel; the boxes open; the three gifts (A-flat/
                          E-flat on '乳香', change); the gift theme's climax; E-flat on '宝贝' (change: horns, timpani,
                          harp) [the star again, it stops, joy, the boxes, gold, frankincense, myrrh, the treasures]
  s12 end       Eb 3/4    the music-box waltz again; the question '可是你知道吗' (Cm7 B-flat7sus4); the gift theme's
                          climax on '耶稣，才是' (change) to E-flat on '送给了我们' (change); the last question (A-flat add9
                          Gm7 Cm7, the celesta asks); B-flat7sus4 on the end of '你想送给耶稣什么礼物呢' (change), hanging
                          very softly; the final E-flat chord with the end card (x on celesta and music box, sleigh
                          bells), ringing to the end [the gift, Jesus the gift, the best gift, God loves us, a little
                          gift, the end card]

All the music stays under the narration (Seg.duck, low expression levels); under Mary's and the angel's thinner
voices the strings drop to violas and cellos and the melodies step aside (1-4 kHz speech-to-music ratio); the loud
moments live in the pauses and are short and child-safe; the angels' words get only sustained chords.
"""
import numpy as np

from audio.scorekit import PARTS, Part
from audio.scorelib import ChordTones, bassline, broken, drum, gliss, roll, span_end, timp_pitch
from audio.theory import midi

# ------------------------------------------------------------------------------------------- this film's colours
# Five General MIDI voices the shared orchestra (audio/scorekit.PARTS) does not list yet; registered here, for this
# story only, before any cue is written (the MIDI writer, the checks and the bus channel count read PARTS).
_EXTRA = [
    Part("recorder", 0, 74, "wind", -0.12, -3, 60, 98, attack=0.03, jitter=0.008, duck_db=2.5),
    Part("ehorn", 0, 69, "wind", 0.2, 0, 52, 81, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.5),
    Part("tpt", 0, 56, "wind", 0.08, -7, 55, 84, attack=0.03, legato=0.02, jitter=0.008, duck_db=2.5),
    Part("dulcimer", 0, 15, "keys", 0.32, 0, 48, 96, jitter=0.006, duck_db=2.0),
    Part("bells", 0, 14, "keys", 0.12, -7, 60, 84, jitter=0.004, duck_db=2.5),
]
for _p in _EXTRA:
    PARTS.setdefault(_p.name, _p)

# ------------------------------------------------------------------------------------------- themes
GIFT = ["Bb4:1 G5:3/2 F5:1/2", "G5:1 Eb5:2", "C5:1 Eb5:1 Ab5:1", "F5:3",
        "Bb4:1 G5:3/2 F5:1/2", "G5:1 C6:2", "Ab5:1 G5:1/2 F5:1/2 D5:1", "Eb5:3"]
GIFT_PROG = ["Eb:3", "Eb:3", "Ab:3", "Bb:3", "Eb:3", "Cm:3", "Ab/C:1 Bb7:2", "Eb:3"]

LULL = ["G5:1 F5:1/2 G5:1 Bb4:1/2", "C5:3/2 Ab4:1 C5:1/2", "Bb4:1 Eb5:1/2 D5:1 C5:1/2", "Bb4:3",
        "G5:1 F5:1/2 G5:1 Bb4:1/2", "C5:1 Eb5:1/2 G5:3/2", "Ab5:1 G5:1/2 F5:1 D5:1/2", "Eb5:3"]
LULL_PROG = ["Eb:3", "Ab:3", "Eb/Bb:3/2 Bb7:3/2", "Bb:3", "Eb:3", "Cm:3", "Ab:3/2 Bb7:3/2", "Eb:3"]

MARY = ["Eb5:2 Ab4:1", "Db5:3/2 C5:1/2 Db5:1", "Eb5:1 C5:1 Ab4:1", "Bb4:3",
        "Eb5:2 Ab4:1", "F5:3/2 Eb5:1/2 Db5:1", "C5:3/2 Bb4:1/2 G4:1", "Ab4:3"]
MARY_PROG = ["Ab:3", "Db/F:3", "Ab:3", "Eb:3", "Ab:3", "Db/F:3", "Ab/Eb:3/2 Eb7:3/2", "Ab:3"]

SHEP = ["D5:1/2 Eb5:1/2 F5:1/2 Bb5:1 F5:1/2", "G5:1/2 F5:1/2 Eb5:1/2 D5:1 Bb4:1/2",
        "C5:1/2 D5:1/2 Eb5:1/2 F5:1 A4:1/2", "Bb4:1 F4:1/2 Bb4:3/2",
        "D5:1/2 Eb5:1/2 F5:1/2 Bb5:1 F5:1/2", "G5:1/2 Bb5:1/2 G5:1/2 Eb5:1 G5:1/2",
        "F5:1/2 Eb5:1/2 D5:1/2 C5:1 A4:1/2", "Bb4:3"]
SHEP_PROG = ["Bb:3", "Eb:3/2 Bb:3/2", "F7:3", "Bb:3", "Bb:3", "Eb:3", "F7:3", "Bb:3"]
PAST = ["D5:3/4 Eb5:1/4 F5:1/2 Bb5:1 F5:1/2", "G5:3/4 F5:1/4 Eb5:1/2 D5:1 Bb4:1/2",
        "C5:3/4 D5:1/4 Eb5:1/2 F5:1 A4:1/2", "Bb4:3"]
PAST_PROG = ["Bb:3", "Ebadd9/Bb:3/2 Bb:3/2", "F7/Bb:3", "Bb:3"]

CAR = ["C4:3/2 D4:1/2", "Eb4:1 G4:1", "A4:3/2 G4:1/2", "F4:2", "Eb4:1 F4:1/2 Eb4:1/2", "D4:1 Bb3:1", "C4:2"]
CAR_PROG = ["Cm:2", "Cm:2", "F:2", "F:2", "Cm:2", "Gm:2", "Cm:2"]
CAR_MAJ = ["Eb4:3/2 F4:1/2", "G4:1 Bb4:1", "C5:3/2 Bb4:1/2", "Ab4:2"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…—"
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




def _onsets(wav):
    key = str(wav)
    if key in _ONSETS:
        return _ONSETS[key]
    out = None
    try:
        import soundfile as sf
        x, sr = sf.read(str(wav), dtype="float64")
        if x.ndim > 1:
            x = x.mean(axis=1)
        hop = int(0.01 * sr)
        n = len(x) // hop
        db = 10 * np.log10((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
        on = db > max(db.max() - 32.0, -50.0)
        runs, i = [], 0
        while i < n:
            if on[i]:
                j = i
                while j < n and on[j]:
                    j += 1
                if j - i >= 4:
                    runs.append(i)
                i = j
            else:
                i += 1
        out = ([a * 0.01 for a in runs], n * hop / sr)
    except Exception:
        out = None
    _ONSETS[key] = out
    return out


def _align(u, v):
    m, n = len(u), len(v)
    inf = float("inf")
    d = np.full((m + 1, n + 1), inf)
    d[0, :] = 0.0
    for i in range(1, m + 1):
        for j in range(i, n + 1):
            d[i, j] = min(d[i, j - 1] if j - 1 >= i else inf, d[i - 1, j - 1] + (u[i - 1] - v[j - 1]) ** 2)
    out, i, j = [0.0] * m, m, n
    while i > 0:
        if j - 1 >= i and d[i, j] == d[i, j - 1]:
            j -= 1
        else:
            out[i - 1] = v[j - 1]
            i -= 1
            j -= 1
    return out


def syl(c, phrase, n):
    """Cue-relative onsets of the n punctuation groups that start where `phrase` starts, as the narrator speaks
    them (the recorded clip's voice islands matched to the text; the subtitle interpolation as the fallback)."""
    from engine.paths import BUILD

    i = c.find(phrase)
    ln = c.scene["lines"][i]
    units = _units(ln["text"])
    k0 = ln["text"].index(phrase)
    u0 = max(k for k, (p, _) in enumerate(units) if p <= k0)
    interp = [_char_time(ln, p) for p, _ in units]
    times = list(interp)
    on = _onsets(BUILD / ln["wav"]) if ln.get("wav") else None
    if on is not None and len(on[0]) >= len(units) and on[1] > 0:
        scale = (ln["end"] - ln["start"]) / on[1]
        v = [ln["start"] + o * scale for o in on[0]]
        times = [a if abs(a - b) <= 0.5 else b for a, b in zip(_align(interp, v), interp)]
    for k in range(1, len(times)):
        times[k] = max(times[k], times[k - 1] + 0.05)
    n = min(n, len(units) - u0)
    return times[u0:u0 + n]


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


def accent(c, segs, t, what=None, glock=None, celesta=None, harp=None, pluck=None, bells=None, low=None, vel=46):
    """A picture hit at cue-relative time t on tones of the chord sounding there (glock / celesta / harp / pizzicato /
    tubular bell = (lo, hi) ranges: the highest chord tone in range; low=True: a soft low thump); synced if `what`."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if celesta:
        sg.add("celesta", q, _dq(sg, q, 1.0), top(sg, q, *celesta), vel - 6, "arp", "h")
    if harp:
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, *harp), vel, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if bells:
        sg.add("bells", q, _dq(sg, q, 1.0), top(sg, q, *bells), vel - 4, "arp", "h")
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


# ------------------------------------------------------------------------------------------- writing helpers
STR = ["vla", "vln2", "vln1", "vc", "cb"]


def lv(seg, parts, a, b=None, q0=0.0, q1=None):
    """Flat expression (dB) for parts over the segment (or q0..q1), a -> b."""
    seg.expr(parts, [(q0, a), (seg.n_q if q1 is None else q1, a if b is None else b)])


def strings(seg, vel=40, lo=55, hi=72, bass=(41, 53), q0=0.0, q1=None, cb=(29, 41), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vln2", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
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


def sweep(seg, q, dur_s=0.6, lo="Eb4", hi="Eb6", v0=30, v1=46, up=True, part="harp"):
    """A harp glissando over the chord at q."""
    gliss_in(seg, part, q, dur_s, midi(lo), midi(hi), up=up, v0=v0, v1=v1, scale=ChordTones(seg.chord_at(q + 1e-3)))




def troll(seg, q0, q1, pitch, v0, v1, rate=13.0):
    """A timpani roll whose strokes are tuned to the chord at their onset and never ring over a chord change."""
    t0, t1 = seg.t(q0), seg.t(q1)
    n = max(2, int((t1 - t0) * rate))
    for k in range(n):
        tk = t0 + k * (t1 - t0) / n
        qk = seg.q_of(tk)
        dq = min((q1 - q0) / n, span_end(seg, qk + 1e-6) - qk - 0.02)
        if dq < 0.03:
            continue
        v = v0 + (v1 - v0) * k / (n - 1) + (3 if k % 2 else -3)
        seg.add("timp", qk, dq, timp_pitch(seg.chord_at(qk + 1e-3), pitch), v, "timp")


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


def waltz(seg, q0, q1, vel=44, bass=(39, 51), hi=(63, 75), part="harp"):
    """A music-box waltz under the tune: a plucked bass on beat 1, two soft chord tones on beats 2 and 3."""
    q = q0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        beat = int(round((q % seg.bar_q) / seg.beat_q))
        if beat == 0:
            seg.add("pz_lo", q, _dq(seg, q, 1.0), ch.bass_note(*bass), vel, "arp", "s")
        else:
            for p in ch.tones(*hi)[:2]:
                seg.add(part, q, _dq(seg, q, 0.5), p, vel - 10, "arp", "s")
        q += seg.beat_q


def rock(seg, q0, q1, lo=39, hi=51, vel=34, pat=(0, 2, 4, 2, 4, 2), part="harp"):
    """The cradle rocking in 6/8: a harp broken chord in eighths from the bass (only the beats while a line is
    spoken)."""
    broken(seg, part, q0, q1, pat, lo, hi, vel=vel, step=0.5, accent=6, thin=True)


def jingle(seg, q, vel=34, n=3, step=0.125, force=False):
    """A soft shake of the sleigh bells (the cosy Christmas frame) -- only in a narration pause unless forced."""
    if not force and bool(seg.score.speaking(seg.t(q))):
        return
    for k in range(n):
        qq = q + k * step
        if qq < seg.n_q - 0.05:
            drum(seg, qq, 83, vel - 3 * k)


def clipclop(seg, q0, q1, vel=34):
    """The donkey's hooves in 6/8: a high and a low woodblock, long-short."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        drum(seg, q, 76 if k % 2 == 0 else 77, vel - (0 if k % 2 == 0 else 6))
        q += 1.0 if k % 2 == 0 else 0.5
        k += 1


def stars(segs, c, times, lo=79, hi=96, vel=40, glock_every=2, synced=(), what="a star twinkles"):
    """Stars twinkling one by one: a celesta chord tone for each (climbing), a soft glockenspiel on some; the
    picture's stars (in `synced`) a little brighter and synced."""
    prev = lo - 1
    n = 0
    for k, t in enumerate(times):
        seg, q = seg_at(c, segs, t)
        ts = seg.chord_at(q + 1e-3).tones(prev + 1, hi) or seg.chord_at(q + 1e-3).tones(lo, hi)
        p = ts[0]
        prev = p if p < hi - 3 else lo - 1
        pic_star = any(abs(t - x) < 1e-6 for x in synced)
        seg.add("celesta", q, _dq(seg, q, 0.75), p, vel + (8 if pic_star else (k % 3) - 4 * bool(synced)), "arp", "h")
        if pic_star or (glock_every and k % glock_every == 1 and not synced):
            seg.add("glock", q, _dq(seg, q, 0.75), p + 12 if p + 12 <= 103 else p, vel - (2 if pic_star else 8),
                    "arp", "h")
        if pic_star:
            n += 1
            seg.sync(f"{what} ({n})", q, t)


def star_times(c, phrase, t0, t1, n=6, name="sparkle"):
    """(times, picture times) of the twinkles from t0 to t1: the picture's sparkles from the line containing
    `phrase` on, with soft extra ones in between when the picture shows fewer than three; n even steps without it."""
    sp = [t for t in (picture(c, name, c.ls(c.find(phrase)) - 0.3, c.dur - 0.05) or []) if t0 - 0.3 <= t <= t1]
    even = [t0 + 0.12 + k * (t1 - 0.3 - t0) / n for k in range(n)]
    if len(sp) >= 3:
        return sp[:8], sp[:8]
    if sp:
        return sorted(sp + [t for t in even if t > sp[0] and all(abs(t - x) > 0.35 for x in sp)]), sp
    return even, []


def glow(seg, q, vel=44, hi=(84, 96)):
    """A warm glint: a glockenspiel and a celesta chord tone at q."""
    seg.add("glock", q, _dq(seg, q, 1.0), top(seg, q, *hi), vel, "arp", "h")
    seg.add("celesta", q, _dq(seg, q, 1.0), top(seg, q, hi[0] - 12, hi[1] - 12), vel - 6, "arp", "h")


def peal(seg, q, names, vel=44, gap_s=0.16):
    """Tubular bells ringing out a chord, one bell after another (each held to the chord's end)."""
    t0 = seg.t(q)
    for k, nm in enumerate(names):
        qk = seg.q_of(t0 + gap_s * k)
        if qk >= span_end(seg, q + 1e-6) - 0.1:
            break
        seg.add("bells", qk, span_end(seg, q + 1e-6) - qk, nm, vel - 3 * k, "arp", "h")




def clear_near(c, t, win=0.12, roles=("arp",)):
    """Drop this cue's accompaniment onsets (harp and pizzicato figures) within win s of cue-relative time t, so a
    picture accent there is one clear attack."""
    sc = c.score
    ta = c.t0 + t
    sc.notes[:] = [n for n in sc.notes if not (n.seg.cue is c and n.role in roles and abs(n.seg.t(n.q) - ta) < win)]


def hit(c, segs, name, phrase, k, what, clear=True, **kw):
    """The picture cue (name, phrase, k) -- picked as music_check picks a PICTURE_HITS target -- gets an accent on
    the chord sounding there (accent() kwargs), synced; returns its time, or None without the scene / the cue."""
    t = pic(c, name, phrase, k)
    if t is not None:
        if clear:
            clear_near(c, t)
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


def climb(c, segs, times, part="celesta", lo=74, hi=96, vel=40, sync=(), what="", harp=False):
    """One note per picture cue, climbing the chord tones (a celesta step for each pop / sparkle); the cues whose
    index is in `sync` are louder and synced."""
    prev = lo - 1
    for k, t in enumerate(times):
        sg, q = seg_at(c, segs, t)
        ts = sg.chord_at(q + 1e-3).tones(prev + 1, hi) or sg.chord_at(q + 1e-3).tones(lo, hi)
        prev = ts[0]
        loud = k in sync
        sg.add(part, q, _dq(sg, q, 0.5), prev, vel + (10 if loud else 0), "arp", "h")
        if loud:
            if harp:
                sg.add("harp", q, _dq(sg, q, 0.5), prev - 12, vel + 4, "arp", "h")
            sg.sync(f"{what} ({k + 1})", q, t)


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """The star motif -- the gift theme's head, sol mi'. re' | mi' do' -- on the recorder over the harp, soft strings
    and a starry choir 'ooh' (E-flat, 3/4); a glint as the title appears, a celesta step for each title character as
    it pops in, a sparkle at the end (the picture)."""
    c.gain(-12.0)
    s = c.seg(0, c.dur, 2, "3/4", "Eb major", nominal=68, label="title")
    s.duck(1.0)
    s.duck(4.0, parts=["recorder"])
    s.prog("Eb:3 | Eb:3")
    s.mel("recorder", bars(GIFT, 0, 2), vel=46)
    broken(s, "harp", 0, 6, (0, 2, 4, 5, 4, 2), 39, 51, vel=36, thin=True)
    strings(s, vel=42, lo=55, hi=72)
    s.pad("ooh", 3, 58, 74, vel=30, bass_ref=(41, 53))
    s.add("glock", 0, 1, "Bb6", 40, "arp", "h")
    s.add("celesta", 0, 1, "G6", 36, "arp", "h")
    hit(c, (s,), "chime", None, 0, "the title appears (a glint)", glock=(86, 98), celesta=(74, 86), vel=48)
    pops = [pic(c, "pop", "圣经绘本", k) for k in range(4)]
    if None not in pops:                                    # the title's characters pop in one by one
        climb(c, (s,), pops, lo=75, hi=96, vel=40, sync=(0, 3), what="a title character pops in", harp=True)
    hit(c, (s,), "sparkle", None, 0, "the title sparkles", glock=(88, 100), vel=46)
    lv(s, ["recorder"], -15)
    lv(s, ["harp"], -11)
    s.expr(STR, [(0, -17), (1, -14), (6, -14)])
    lv(s, ["ooh"], -22)
    lv(s, ["glock", "celesta"], -12)


def question(c):
    """The modern living room: a music-box waltz in E-flat (pizzicato bass, harp chords, sleigh bells in the pauses);
    a ping as an ornament is hung, a sparkle as the child cheers; the birthday question hangs on B-flat7sus4; the gift
    theme on '圣诞节' (music box, the celesta an octave below, warm strings; the tree lights up with a chime) closing on
    E-flat on '耶稣是怎么出生的'."""
    c.gain(-1.5)
    t_x = c.ls(c.find("圣诞节"))
    t_t = (t_x + c.dur) / 2                                  # the theme's four bars at one tempo
    h = c.seg(0, t_x, 3, "3/4", "Eb major", nominal=88, label="question-home")
    x = c.seg(t_x, t_t, 2, "3/4", "Eb major", nominal=88, label="question-christmas")
    t = c.seg(t_t, c.dur, 2, "3/4", "Eb major", nominal=88, label="question-story")
    segs = (h, x, t)
    for sg in segs:
        sg.duck(1.5)
    h.prog("Eb:3 | Ab:3 | Fm7:3/2 Bb7sus4:3/2")
    x.prog(" | ".join(GIFT_PROG[:2]))
    t.prog(" | ".join(GIFT_PROG[6:8]))
    x.sync("'圣诞节': Christmas -- the gift theme (E-flat)", 0, t_x, kind="change")
    # 'child, what is the best part of your birthday?': the waltz; the question on the music box
    waltz(h, 0, 9, vel=46)
    h.pad(["vla", "vln2"], 2, 58, 72, vel=34, bass_ref=(39, 51))
    h.mel("mbox", "Eb6:1/2 F6:1/2 Ab6:1/2", q=7.5, vel=48)
    jingle(h, 0.0, vel=34)
    jingle(h, qpos(h, c, c.le(0) + 0.1, 6.0, 8.6), vel=32)
    lv(h, ["mbox"], -12)
    lv(h, ["pz_lo", "harp"], -11)
    h.expr(["vla", "vln2"], [(0, -20), (9, -19)])
    # 'Christmas is like everybody celebrating Jesus's birthday': the gift theme
    t_lc = pic(c, "chime", "圣诞节")                         # the tree lights up (picture)
    near_f = t_lc is not None and t_x < t_lc < t_t and abs(x.q_of(c.t0 + t_lc) - 2.5) < 0.3
    head = "Bb4:1 G5:2" if near_f else GIFT[0]               # (the passing re' gives way to the chime)
    for sg, mel in ((x, head + " | " + GIFT[1]), (t, bars(GIFT, 6, 8))):
        sg.mel("mbox", mel, vel=52, transpose=12)
        sg.mel("celesta", mel, vel=40, role="counter")
        waltz(sg, 0, 6, vel=44)
        strings(sg, vel=38, lo=55, hi=72)
        sg.duck(4.0, parts=["mbox", "celesta"])
        lv(sg, ["mbox"], -12)
        lv(sg, ["celesta"], -15)
        lv(sg, ["pz_lo", "harp"], -12)
        lv(sg, STR, -18)
    jingle(t, qpos(t, c, c.le(1) + 0.05, 3.0, 5.6), vel=34)
    hit(c, segs, "pop", None, 0, "an ornament is hung (a ping)", glock=(86, 98), celesta=(79, 91), vel=46)
    hit(c, segs, "sparkle", None, 0, "the child cheers (a sparkle)", glock=(86, 98), vel=46)
    hit(c, segs, "sparkle", "圣诞节", 0, "'圣诞节' (a sparkle)", clear=False, glock=(86, 98), vel=44)
    hit(c, segs, "chime", "圣诞节", 0, "the tree lights up (a chime)", glock=(86, 98), celesta=(74, 86), harp=(67, 79),
        vel=48)
    hit(c, segs, "sparkle", "圣诞节", 2, "a birthday for Jesus (a sparkle)", glock=(88, 100), vel=44)
    hit(c, segs, "sparkle", "圣诞节", 3, "how Jesus was born (a sparkle)", glock=(86, 98), vel=44)
    for sg in segs:
        lv(sg, "hand", -14)
        lv(sg, ["glock"], -12)
    lv(h, ["celesta"], -12)


def angel(c):
    """Nazareth: Mary's theme on the recorder (A-flat, 3/4: sol- do | fa. mi fa | sol mi do | re); '有一天' D-flat,
    the lamp-lit room; '忽然亮起来了' C major -- the light on the picture's chime (harp up, glockenspiel and celesta, a
    bell, choir 'aah', high strings); F/C as the angel stands there (a bell on its sparkle); A minor, startled (a
    plucked flick as she jumps); Gabriel's words over soft choir and strings (F C/E Dm7 G7sus4 C; the lullaby's head on
    the celesta on '他是上帝的儿子'); Mary's question (Am F G, strings only under her voice); G7 -> C, radiant, on
    '没有做不到的事'; F minor on '我是上帝的使女' (strings and harp only under her words) and A-flat on '我愿意'."""
    c.gain(-2.0)
    t_day = c.ls(c.find("有一天"))
    t_light = c.at("忽然亮起来了")
    t_angel = c.at("一位天使")
    t_jump = c.at("马利亚吓了一跳")
    t_g = c.gap(c.find("马利亚，不要怕"))
    t_q = c.gap(c.find("可是，我还没有结婚"))
    t_w = c.gap(c.find("这是上帝要做的事"))
    t_imp = c.at("没有做不到的事")
    t_m = c.gap(c.find("我是上帝的使女"))
    t_yes = c.at("我愿意")
    v = c.seg(0, t_day, 4, "3/4", "Ab major", nominal=79, label="angel-nazareth")
    d = c.seg(t_day, t_light, 1, "3/4", "Ab major", nominal=115, label="angel-one-day")
    li = c.seg(t_light, t_angel, 1, "3/4", "C major", nominal=112, label="angel-light")
    a = c.seg(t_angel, t_jump, 1, "3/4", "C major", nominal=71, label="angel-gabriel")
    j = c.seg(t_jump, t_g, 1, "3/4", "C major", nominal=None, label="angel-startled")        # a held chord
    g = c.seg(t_g, t_q, 4, "3/4", "C major", nominal=80, label="angel-words")
    q = c.seg(t_q, t_w, 2, "3/4", "C major", nominal=80, label="angel-question")
    w = c.seg(t_w, t_imp, 2, "2/4", "C major", nominal=77, label="angel-gods-work")
    i = c.seg(t_imp, t_m, 1, "3/4", "C major", nominal=87, label="angel-nothing-impossible")
    m = c.seg(t_m, t_yes, 2, "3/4", "Ab major", nominal=80, label="angel-handmaid")
    y = c.seg(t_yes, c.dur, 1, "3/4", "Ab major", nominal=150, label="angel-yes")
    segs = (v, d, li, a, j, g, q, w, i, m, y)
    for sg in segs:
        sg.duck(1.5)
    v.prog(" | ".join(MARY_PROG[:4]))
    d.prog("Db:3")
    li.prog("C:3")
    a.prog("F/C:3")
    j.prog("Am:3")
    g.prog("F:3 | C/E:3 | Dm7:3/2 G7sus4:3/2 | C:3")
    q.prog("Am:3 | F:3/2 G:3/2")
    w.prog("Dm7:2 | G7sus4:1 G7:1")
    i.prog("C:3")
    m.prog("Fm:3 | Ab/Eb:3/2 Eb7:3/2")
    y.prog("Ab:3")
    li.sync("'忽然亮起来了': the light (C major)", 0, t_light, kind="change")
    i.sync("'没有做不到的事': nothing is impossible (C, radiant)", 0, t_imp, kind="change")
    y.sync("'我愿意': Mary says yes (A-flat)", 0, t_yes, kind="change")
    # Nazareth: Mary's theme
    v.mel("recorder", bars(MARY, 0, 4), vel=54)
    broken(v, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 44, 56, vel=34, thin=True)
    strings(v, vel=36, lo=55, hi=70)
    v.duck(3.0, parts=["recorder"])
    v.expr(["recorder"], [(0, -18), (1, -15), (12, -15)])
    lv(v, ["harp"], -12)
    v.expr(STR, [(0, -21), (2, -20), (12, -20)])
    # 'one day, in the room...': D-flat, lamp-lit; a harp shiver
    d.pad(["vla", "vln2", "vln1"], 3, 56, 72, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(d, "cb", 29, 41, 34)
    broken(d, "harp", 0, 3, (2, 3, 4, 3, 2, 3), 49, 61, vel=32, step=0.25, thin=True)
    d.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -18), (3, -17)])
    lv(d, ["harp"], -12)
    # the light: C major -- the strings and the choir swell from the word; the light itself on the picture's chime
    t_lc, _ = lead(c, segs, "chime", "有一天", 0, t_light, t_angel - 0.25, "the room fills with light (a chime)",
                   glock=(86, 98), celesta=(74, 86))
    q_lc = qpos(li, c, t_lc, 0.0, li.n_q - 0.05) if t_lc is not None else 0.0
    sweep(li, q_lc + 0.02, 0.55, "C4", "C6", 30, 46)
    glow(li, q_lc, vel=46, hi=(84, 96))
    li.add("bells", q_lc, li.n_q - q_lc, "C5", 38, "arp", "h")
    li.add("pz_cb", q_lc, 1, "C2", 46, "bass", "h")
    if t_lc is not None:
        li.sync("the room fills with light (a chime)", q_lc, t_lc)
    li.pad("choir", 3, 60, 76, vel=40, bass_ref=(48, 60))
    li.pad(["vla", "vln2", "vln1"], 3, 60, 79, vel=38, bass_part="vc", bass_lo=48, bass_hi=60)
    li.add("cb", 0, 3, "C2", 34, "bass")
    li.expr(["choir"], [(0, -24), (1.5, -17), (3, -16)])
    li.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -19), (1.5, -16), (3, -16)])
    lv(li, ["harp", "pz_cb", "bells"], -12)
    # 'an angel stood before her': F/C -- the choir fuller, a harp roll; a bell as the angel shines (picture)
    a.pad("choir", 3, 60, 77, vel=40, bass_ref=(48, 60))
    a.pad(["vla", "vln2", "vln1"], 3, 60, 79, vel=36, bass_part="vc", bass_lo=48, bass_hi=60)
    a.add("cb", 0, 3, "C2", 32, "bass")
    roll_chord(a, 0, 53, 77, vel=40)
    t_an, _ = lead(c, segs, "sparkle", "有一天", 0, t_angel, t_jump - 0.2, "the angel shines (a bell)",
                   glock=(86, 98), celesta=(74, 86))
    if t_an is not None:
        accent(c, (a,), t_an, "the angel shines (a bell)", glock=(86, 98), celesta=(74, 86), bells=(65, 77), vel=48)
    else:
        a.add("bells", 0, 3, "C5", 40, "arp", "h")
    lv(a, ["choir"], -17, -19)
    lv(a, ["vla", "vln2", "vln1", "vc", "cb"], -17, -18)
    lv(a, ["harp"], -12)
    # 'Mary was startled': A minor -- the strings tremble; a plucked flick as she jumps (picture), else on the word
    t_jp, _ = lead(c, segs, "cloth", "有一天", 1, t_jump, t_g - 0.4, "Mary jumps", pluck=(57, 69), vel=46)
    q_jp = qpos(j, c, t_jp, 0.0, j.n_q - 0.3) if t_jp is not None else 0.0
    for k_, dq in enumerate((0.0, 0.125, 0.25)):
        j.add("pz_hi", q_jp + dq, 0.125, top(j, q_jp + dq, 57, 76, k_ - 3), 58 if k_ == 0 else 38, "arp", "s")
    j.add("harp", q_jp, _dq(j, q_jp, 1.0), "E5", 50, "arp", "h")
    j.add("celesta", q_jp, _dq(j, q_jp, 1.0), "A6", 44, "arp", "h")
    if t_jp is not None:
        j.sync("Mary jumps (a plucked flick)", q_jp, t_jp)
    j.pad(["trem_va", "trem_hi", "trem_hi"], 3, 57, 76, vel=36, bass_ref=(33, 45))
    j.add("vc", 0, 3, "A2", 36, "bass")
    j.add("cb", 0, 3, "A1", 34, "bass")
    j.expr(["trem_va", "trem_hi"], [(0, -16), (1, -16), (3, -18)])
    lv(j, ["vc", "cb"], -17)
    lv(j, ["pz_hi", "harp"], -11)
    # Gabriel: soft choir and strings; the lullaby's head on '他是上帝的儿子'
    g.pad("choir", 3, 57, 74, vel=36, bass_ref=(40, 52))
    strings(g, vel=36, lo=57, hi=74, bass=(40, 52), cb=(28, 40))
    broken(g, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 41, 53, vel=30, thin=True)
    g.mel("celesta", "E6:1 D6:1/2 E6:1 G5:1/2", q=9, vel=42)
    g.duck(2.5, parts=["choir"])
    lv(g, ["choir"], -23)
    lv(g, STR, -20)
    lv(g, ["harp"], -14)
    lv(g, ["celesta"], -16)
    hit(c, segs, "sparkle", "马利亚，不要怕", 0, "the name Jesus sparkles", celesta=(79, 91), vel=46)
    # Mary's question: A minor, F, G -- strings and harp only (her voice)
    q.pad(["vla", "vla", "vln2"], 3, 50, 65, vel=34, bass_part="vc", bass_lo=45, bass_hi=57)
    bassline(q, "cb", 33, 45, 32)
    q.duck(3.0)
    q.add("harp", 0, 3, "A3", 34, "arp")
    q.add("harp", 0.05, 2.95, "E4", 32, "arp")
    q.add("harp", 3, 1.5, "C4", 32, "arp")
    q.add("harp", 4.5, 1.5, "B3", 32, "arp")
    lv(q, ["vla", "vln2", "vc", "cb"], -21)
    lv(q, ["harp"], -14)
    # 'this is God's work; nothing is impossible with God': Dm7 G7sus4 G7 -> C radiant
    w.pad("choir", 3, 57, 74, vel=34, bass_ref=(40, 52))
    strings(w, vel=36, lo=57, hi=74, bass=(40, 52), cb=(28, 40))
    w.duck(2.0)
    lv(w, ["choir"], -22, -20)
    w.expr(STR, [(0, -20), (4, -18)])
    hit(c, segs, "chime", "这是上帝要做的事", 0, "the angel's blessing (a chime)", glock=(86, 98), celesta=(74, 86),
        vel=46)
    sweep(i, 0.02, 0.5, "C4", "C6", 30, 44)
    glow(i, 0.0, vel=44)
    i.pad("choir", 3, 57, 74, vel=38, bass_ref=(48, 60))
    i.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=38, bass_part="vc", bass_lo=48, bass_hi=60)
    i.add("cb", 0, 3, "C2", 34, "bass")
    i.add("pz_cb", 0, 1, "C2", 46, "bass", "h")
    i.duck(2.0, parts=["choir"])
    lv(i, ["choir"], -20)
    lv(i, ["vla", "vln2", "vln1", "vc", "cb"], -18, -19)
    lv(i, ["harp", "pz_cb"], -12)
    # 'I am the Lord's servant... let it be as you say': F minor (strings, harp); A-flat on '我愿意'
    m.pad(["vla", "vla", "vln2"], 3, 50, 65, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(m, "cb", 29, 41, 32)
    broken(m, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 41, 53, vel=32, thin=True)
    m.duck(3.0)
    y.duck(3.0)
    lv(m, ["vla", "vln2", "vc", "cb"], -21)
    lv(m, ["harp"], -15)
    roll_chord(y, 0, 44, 60, vel=30)
    y.pad(["vla", "vla", "vln2"], 3, 50, 65, vel=34, bass_part="vc", bass_lo=44, bass_hi=56)
    bassline(y, "cb", 32, 44, 32)
    lv(y, ["harp"], -14)
    lv(y, ["vla", "vln2", "vc", "cb"], -20)
    hit(c, segs, "sparkle", "我是上帝的使女", 0, "Mary's yes (a sparkle)", glock=(86, 98), vel=46)
    for sg in segs:
        lv(sg, ["glock", "celesta", "pz_hi", "pz_cb"], -12)
        if sg not in (li,):
            lv(sg, ["bells"], -12)


def journey(c):
    """Joseph: Mary's motif on the horn (A-flat D-flat/F F7; a pluck as Joseph and then Mary are named); the Roman
    emperor on '那时候' -- a small pompous B-flat fanfare (trumpet, horns, timpani; a glint as he appears), then the
    people counted: a pizzicato step for each head that pops up (the picture); '他下了一道命令' F7 under the herald's
    own horn (a soft snare roll and timpani only); everyone walking home (B-flat, walking pizzicato, the clarinet);
    E-flat on '伯利恒' -- Mary's theme in E-flat on the recorder (the road dots on the map: celesta steps); the
    lullaby's head on the celesta on '小宝宝'; the long walk (6/8, the donkey's hooves) on '他们走啊走'."""
    c.gain(-2.0)
    t_rome = c.at("那时候")
    t_ord = c.gap(c.find("他下了一道命令"))
    t_home = c.at("每个人都要回到")
    t_bl = c.at("伯利恒")
    t_baby = c.at("小宝宝")
    t_walk = c.gap(c.find("他们走啊走"))
    j = c.seg(0, t_rome, 2, "3/4", "Ab major", nominal=98, label="journey-joseph")
    r = c.seg(t_rome, t_ord, 2, "4/4", "Bb major", nominal=92, label="journey-rome")
    o = c.seg(t_ord, t_home, 1, "2/4", "Bb major", nominal=None, label="journey-decree")      # a held roll
    w = c.seg(t_home, t_bl, 4, "2/4", "Bb major", nominal=83, label="journey-everyone")
    b = c.seg(t_bl, t_baby, 4, "3/4", "Eb major", nominal=86, label="journey-bethlehem")
    y = c.seg(t_baby, t_walk, 1, "6/8", "Eb major", nominal=66, label="journey-baby")
    k = c.seg(t_walk, c.dur, 2, "6/8", "Eb major", nominal=92, label="journey-walk")
    segs = (j, r, o, w, b, y, k)
    for sg in segs:
        sg.duck(1.5)
    j.prog("Ab:3 | Db/F:3/2 F7:3/2")
    r.prog("Bb:4 | Eb:2 F7:2")
    o.prog("F7:2")
    w.prog("Bb:2 | F7:2 | Bb:2 | Bb7:2")
    b.prog("Eb:3 | Ab:3 | Eb:3 | Bb:3")
    y.prog("Eb:3")
    k.prog("Eb:3 | Bb:3")
    r.sync("'那时候': the Roman emperor (B-flat)", 0, t_rome, kind="change")
    b.sync("'伯利恒': Bethlehem (E-flat)", 0, t_bl, kind="change")
    y.sync("'小宝宝': the lullaby's head (E-flat)", 0, t_baby, kind="change")
    # Joseph: Mary's motif on the horn
    j.mel("horn", "Eb4:2 Ab3:1 | Db4:3/2 C4:3/2", vel=48)
    strings(j, vel=36, lo=55, hi=70)
    broken(j, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 41, 53, vel=30, thin=True)
    j.duck(2.5, parts=["horn"])
    j.expr(["horn"], [(0, -19), (1, -16), (6, -16)])
    j.expr(STR, [(0, -22), (1.5, -20), (4.5, -20), (6, -18)])
    lv(j, ["harp"], -13)
    hit(c, segs, "pop", None, 0, "Joseph pops up", pluck=(60, 72), celesta=(79, 91), vel=44)
    hit(c, segs, "pop", None, 1, "Mary pops up", pluck=(63, 75), celesta=(82, 94), vel=44)
    # the Roman emperor: a small pompous fanfare; then the people counted
    r.mel("tpt", "F4:3/4 F4:1/4 Bb4:1 D5:3/4 C5:1/4 Bb4:1", vel=50)
    r.pad(["horn", "horn"], 2, 50, 62, vel=40, q1=4, bass_ref=(34, 46))
    r.add("timp", 0, 0.5, "Bb2", 38, "timp", "h")
    r.add("timp", 2, 0.5, "F2", 40, "timp", "h")
    r.add("pz_cb", 0, 1, "Bb1", 38, "bass", "h")
    r.add("pz_lo", 4, 1, "Eb3", 42, "arp", "s")
    r.add("pz_lo", 6, 1, "F2", 42, "arp", "s")
    r.pad(["vla", "vln2"], 2, 58, 72, vel=32, q0=4, bass_ref=(34, 46))
    heads = [pic(c, "pop", None, kk) for kk in range(2, 12)]
    if None not in heads:                                    # one, two, three...: a pluck for each head (picture)
        climb(c, segs, heads, part="pz_hi", lo=62, hi=86, vel=40, sync=(0,), what="a head is counted")
    else:
        prev = 62
        for kk in range(8):
            qq = 4 + 0.5 * kk
            prev = r.chord_at(qq + 1e-3).tones(prev + 1, 90)[0]
            r.add("pz_hi", qq, 0.25, prev, 40 + kk, "arp", "s")
    hit(c, segs, "chime", None, 0, "the emperor appears (a glint)", glock=(86, 98), celesta=(74, 86), vel=46)
    r.duck(3.0, parts=["tpt", "horn"])
    lv(r, ["tpt"], -14)
    lv(r, ["horn"], -18, q1=4)
    lv(r, ["timp", "pz_cb", "pz_hi", "pz_lo"], -10)
    r.expr(["vla", "vln2"], [(4, -20), (8, -19)])
    # 'he gave an order': F7 under the herald's horn -- a soft snare roll, the timpani
    roll(o, 0.1, 1.9, 38, 22, 32, rate=16)
    o.add("timp", 0, 2, "F2", 36, "timp", "h")
    o.pad(["vla", "vln2", "vln1"], 3, 55, 70, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    lv(o, "okit", -12)
    lv(o, ["timp"], -12)
    lv(o, ["vla", "vln2", "vln1", "vc"], -19)
    # everyone goes home to be counted: walking pizzicato, the clarinet
    w.mel("clar", "D5:1 F5:1 | Eb5:1 C5:1 | D5:1 Bb4:1 | Ab4:2", vel=48, art="s")
    for qq in range(8):                                    # walking: the bass, then its fifth
        ch = w.chord_at(qq + 1e-3)
        b0 = ch.bass_note(41, 53)
        w.add("pz_lo", qq, 1, b0 + 7 if qq % 2 and (b0 + 7) % 12 in ch.pcset else b0, 44, "arp", "s")
    w.pad(["vla", "vln2"], 2, 58, 72, vel=32, bass_ref=(34, 46))
    w.duck(2.5, parts=["clar"])
    lv(w, ["clar"], -15)
    w.expr(["pz_lo"], [(0, -13), (1, -9), (8, -9)])
    w.expr(["vla", "vln2"], [(0, -19), (1, -17), (8, -17)])
    hit(c, segs, "sparkle", "他下了一道命令", 0, "the scroll sparkles", glock=(86, 98), vel=44)
    hit(c, segs, "pop", "约瑟的老家", 0, "Bethlehem on the map", celesta=(79, 91), pluck=(62, 74), vel=46)
    # Bethlehem: Mary's theme in E-flat on the recorder
    b.mel("recorder", bars(MARY, 0, 4), vel=50, transpose=-5)
    strings(b, vel=36, lo=55, hi=70)
    broken(b, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 39, 51, vel=30, thin=True)
    b.duck(3.0, parts=["recorder"])
    b.expr(["recorder"], [(0, -17), (1, -14), (12, -14)])
    b.expr(STR, [(0, -21), (1, -20), (12, -20)])
    lv(b, ["harp"], -13)
    dots = [pic(c, "pop", "约瑟的老家", kk) for kk in range(1, 8)]
    if None not in dots:                                   # the road to Bethlehem dotted in (picture)
        climb(c, segs, dots, lo=72, hi=91, vel=34, sync=(0, 6), what="a dot on the road")
    hit(c, segs, "sparkle", "约瑟的老家", 0, "the road is drawn (a sparkle)", glock=(86, 98), vel=44)
    # 'the baby will soon be born': the lullaby's head on the celesta
    y.mel("celesta", LULL[0], vel=46)
    rock(y, 0, 3, vel=32)
    strings(y, vel=34, lo=55, hi=70)
    lv(y, ["celesta"], -13)
    lv(y, ["harp"], -13)
    lv(y, STR, -20)
    hit(c, segs, "sparkle", "这时候", 0, "the baby's heart (a sparkle)", glock=(86, 98), vel=44)
    # 'they walked and walked for many days': the donkey's hooves, the recorder
    k.mel("recorder", "Bb4:1 G4:1/2 Bb4:1 Eb5:1/2 | D5:1 C5:1/2 Bb4:3/2", vel=48)
    clipclop(k, 0, 6, vel=36)
    for qq in (0.0, 1.5, 3.0, 4.5):
        k.add("pz_lo", qq, 1.5, k.chord_at(qq + 1e-3).bass_note(39, 51), 44, "arp", "s")
    k.pad(["vla", "vln2"], 2, 58, 72, vel=32, bass_ref=(39, 51))
    k.duck(2.5, parts=["recorder"])
    lv(k, ["recorder"], -15)
    k.expr(["pz_lo"], [(0, -15), (1.5, -11), (6, -11)])     # the walk eases in
    k.expr("hand", [(0, -19), (1.5, -15), (6, -15)])
    lv(k, ["vla", "vln2"], -20)
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)
        if sg is not y:
            lv(sg, ["celesta"], -12)


def noroom(c):
    """Bethlehem crowded: a busy B-flat scherzando (pizzicato, oboe and clarinet chattering, woodblock ticks);
    '客店里' G minor -- a lonely bassoon falling to D7; the deceptive E-flat on '他们只好' (a humble warm place: low
    strings, harp, a horn), hanging on B-flat7sus4."""
    c.gain(-2.0)
    t_inn = c.gap(c.find("客店里"))
    t_sh = c.gap(c.find("他们只好"))
    a = c.seg(0, t_inn, 4, "4/4", "Bb major", nominal=131, label="noroom-crowd")
    n = c.seg(t_inn, t_sh, 1, "4/4", "G minor+", nominal=77, label="noroom-full")
    s = c.seg(t_sh, c.dur, 2, "3/4", "Eb major", nominal=77, label="noroom-stable")
    segs = (a, n, s)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Bb:4 | Eb:2 F7:2 | Bb:2 Gm:2 | Eb:2 F:2")
    n.prog("Gm:2 Eb:1 D7:1")
    s.prog("Eb:3 | Ab:3/2 Bb7sus4:3/2")
    n.sync("'客店里': no room (G minor)", 0, t_inn, kind="change")
    s.sync("'他们只好': a humble place (E-flat)", 0, t_sh, kind="change")
    # the crowd: pizzicato eighths, chattering winds, ticks
    for qq in np.arange(0, 16, 0.5):
        ch = a.chord_at(qq + 1e-3)
        if qq % 1 == 0:
            a.add("pz_lo", qq, 0.5, ch.bass_note(41, 53) if qq % 2 == 0 else ch.tones(46, 58)[1], 46, "arp", "s")
        else:
            a.add("pz_hi", qq, 0.5, ch.tones(62, 74)[int(qq) % 2], 38, "arp", "s")
    for k_, (part, q0) in enumerate((("oboe", 0.5), ("clar", 2.5), ("oboe", 4.5), ("clar", 6.5), ("oboe", 8.5),
                                     ("clar", 10.5), ("oboe", 12.5))):
        lo, hi = (67, 81) if part == "oboe" else (58, 72)
        for j_ in range(3):
            qq = q0 + 0.25 * j_
            a.add(part, qq, 0.25, top(a, qq, lo, hi, -1 - (j_ + k_) % 3), 46, "arp", "s")
    for qq in np.arange(0.5, 16, 1.0):
        if not bool(a.score.speaking(a.t(qq))):
            drum(a, qq, 76, 36)
    a.pad(["vla", "vln2"], 2, 58, 72, vel=34, bass_ref=(41, 53))
    a.expr(["pz_lo", "pz_hi"], [(0, -21), (3, -10), (16, -10)])      # the crowd fades in with the picture
    a.expr(["oboe", "clar"], [(0, -18), (2, -15), (16, -15)])
    a.expr("hand", [(0, -20), (3, -14), (16, -14)])
    a.expr(["vla", "vln2"], [(0, -21), (2, -19), (16, -19)])
    # 'the inn had no room': G minor, a lonely bassoon
    n.mel("bsn", "Bb3:1 A3:1 G3:1 F#3:1", vel=48)
    n.pad(["vla", "vln2", "vln1"], 3, 55, 70, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(n, "cb", 28, 40, 30)
    lv(n, ["bsn"], -17)
    lv(n, ["vla", "vln2", "vln1", "vc", "cb"], -22)
    # 'so they stayed in a place for animals': E-flat, warm and humble
    s.mel("horn", "G3:3 | Ab3:3", vel=40, role="pad")
    strings(s, vel=36, lo=55, hi=70)
    roll_chord(s, 0, 39, 63, vel=36)
    broken(s, "harp", 1, 6, (0, 2, 4, 2, 4, 2), 39, 51, vel=28, thin=True)
    lv(s, ["horn"], -20)
    lv(s, STR, -19)
    lv(s, ["harp"], -13)
    hit(c, segs, "pop", None, 0, "squeezed in the crowd (a pop)", pluck=(62, 74), celesta=(79, 91), vel=48)
    t_kn = pic(c, "hammer", None)                          # a knock at the inn door (picture)
    if t_kn is not None:
        clear_near(c, t_kn)
        sg, q_kn = accent(c, segs, t_kn, "a knock at the inn door", pluck=(55, 67), vel=46)
        drum(sg, q_kn, 77, 44)
    hit(c, segs, "sparkle", "他们只好", 0, "a lamp is lit in the stable (a sparkle)", glock=(86, 98), vel=44)
    for sg in segs:
        lv(sg, ["glock", "celesta", "pz_hi"], -12)


def birth(c):
    """Night in the stable (B-flat7sus4, harp, soft strings); E-flat glowing on '出生了' (the picture's chime: harp
    roll, glockenspiel and celesta, choir 'ooh'); the lullaby (6/8: mi' re' mi' sol | la - fa la | sol do' ti la | sol)
    on the celesta over the rocking harp on '马利亚用布' (a harp and celesta note as the baby is laid in the manger, a
    soft bassoon munch for the ox); E-flat on '小耶稣睡着了' and the stars twinkling over E-flat add9 (a celesta note
    for each of the picture's stars)."""
    c.gain(-2.0)
    t_born = c.at("出生了")
    t_wrap = c.gap(c.find("马利亚用布"))
    t_sleep = c.ls(c.find("小耶稣睡着了"))
    a = c.seg(0, t_born, 2, "6/8", "Eb major", nominal=99, label="birth-night")
    b = c.seg(t_born, t_wrap, 1, "6/8", "Eb major", nominal=None, label="birth-born")         # a held chord
    l = c.seg(t_wrap, t_sleep, 4, "6/8", "Eb major", nominal=86, label="birth-lullaby")
    z = c.seg(t_sleep, c.dur, 2, "6/8", "Eb major", nominal=75, label="birth-asleep")
    segs = (a, b, l, z)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Bb7sus4:3 | Bb7:3")
    b.prog("Eb:3")
    l.prog(" | ".join(LULL_PROG[:4]))
    z.prog("Eb:3 | Ebadd9:3")
    b.sync("'出生了': Jesus is born (E-flat)", 0, t_born, kind="change")
    z.sync("'小耶稣睡着了': asleep (E-flat)", 0, t_sleep, kind="change")
    # night in the stable
    rock(a, 0, 6, lo=39, hi=51, vel=32)
    a.pad(["vla", "vln2", "vln1"], 3, 56, 70, vel=34, bass_part="vc", bass_lo=46, bass_hi=58)
    a.add("cb", 0, 6, "Bb1", 32, "bass")
    lv(a, ["harp"], -12)
    lv(a, ["vla", "vln2", "vln1", "vc", "cb"], -19)
    # born: E-flat glowing (the picture's chime)
    t_bc, _ = lead(c, segs, "chime", None, 0, t_born, t_wrap - 0.2, "the baby glows (a chime)", glock=(86, 98))
    q_bc = qpos(b, c, t_bc, 0.0, b.n_q - 0.1) if t_bc is not None else 0.0
    roll_chord(b, 0, 39, 70, vel=42)
    glow(b, q_bc, vel=48)
    if t_bc is not None:
        b.sync("the baby glows (a chime)", q_bc, t_bc)
    b.pad("ooh", 3, 58, 74, vel=34, bass_ref=(39, 51))
    strings(b, vel=38, lo=55, hi=72)
    lv(b, ["harp"], -12)
    b.expr(["ooh"], [(0, -24), (3, -20)])
    lv(b, STR, -18)
    # the lullaby
    l.mel("celesta", bars(LULL, 0, 4), vel=48)
    rock(l, 0, 12, vel=32)
    strings(l, vel=34, lo=55, hi=70)
    l.pad("ooh", 3, 58, 72, vel=28, q0=6, bass_ref=(41, 53))
    l.duck(2.5, parts=["celesta"])
    l.expr(["celesta"], [(0, -14), (1.5, -12), (12, -12)])
    lv(l, ["harp"], -13)
    lv(l, STR, -19)
    l.expr(["ooh"], [(6, -26), (12, -23)])
    hit(c, segs, "sparkle", "马利亚用布", 0, "the baby is laid in the manger", celesta=(79, 91), harp=(67, 79), vel=46)
    t_ox = pic(c, "crunch", None)                         # the ox munches the hay (picture): a soft bassoon munch
    if t_ox is not None:
        clear_near(c, t_ox)
        sg, q_ox = seg_at(c, segs, t_ox)
        lo_ = sg.chord_at(q_ox + 1e-3).bass_note(46, 58)
        drum(sg, q_ox, 73, 58)                              # munch: a short guiro scrape, a plucked low note
        sg.add("bsn", q_ox, 0.25, lo_, 54, "arp", "s")
        sg.add("pz_lo", q_ox, 0.25, lo_, 56, "arp", "s")
        q2 = min(q_ox + 0.5, sg.n_q - 0.3)
        drum(sg, q2, 73, 44)
        sg.add("bsn", q2, 0.25, lo_, 44, "arp", "s")
        sg.sync("the ox munches (a guiro, a bassoon)", q_ox, t_ox)
    # asleep; the stars
    z.mel("celesta", LULL[4] + " | Eb5:3", vel=46)
    rock(z, 0, 3, vel=30)
    z.pad(["vla", "vln2", "vln1"], 3, 58, 75, vel=32, bass_part="vc", bass_lo=41, bass_hi=53)
    z.add("cb", 0, 6, "Eb2", 30, "bass")
    z.add("harp", 3, 3, "Eb3", 34, "arp", "h")
    z.add("harp", 3.05, 2.95, "Bb3", 32, "arp")
    hit(c, segs, "sparkle", "小耶稣睡着了", 0, "asleep (a glint)", glock=(86, 98), vel=44)
    times, sp = star_times(c, "小耶稣睡着了", c.at("一闪一闪"), c.dur - 0.25, 5)
    stars(segs, c, times, lo=82, hi=98, vel=40, synced=sp, what="a star twinkles")
    z.duck(2.0, parts=["celesta", "vla", "vln2", "vln1"])
    lv(z, ["celesta"], -14, -15)
    lv(z, ["harp"], -13)
    z.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -21), (6, -23)])
    for sg in segs:
        lv(sg, ["glock", "bsn", "pz_lo"], -12)
        if sg is not l and sg is not z:
            lv(sg, ["celesta"], -12)


def shepherds(c):
    """The shepherds' pastoral (B-flat 6/8 siciliana on the recorder over a B-flat/F drone, harp); A7sus4 on '忽然'
    and the angel on the picture's chime (a harp sweep from its whoosh, a bell, glockenspiel and celesta, timpani; the
    choir 'aah' enters, high tremolo); D major radiant on '上帝的光'; B minor, the shepherds frightened (low tremolo, a
    soft timpani roll); the angel's words over soft choir and strings (G D/F# Em7 A7sus4); the star motif on the horn
    in D on '今天，在伯利恒'; the lullaby's head in D on the celesta for the sign ('你们会看见一个婴孩'), half
    cadence on A; sparkles and a chime where the picture glints."""
    c.gain(-2.0)
    t_sud = c.ls(c.find("忽然"))
    t_light = c.at("上帝的光")
    t_fear = c.at("牧羊人都吓坏了")
    t_np = c.gap(c.find("不要怕"))
    t_today = c.gap(c.find("今天，在伯利恒"))
    t_sign = c.gap(c.find("你们会看见"))
    p = c.seg(0, t_sud, 4, "6/8", "Bb major", nominal=93, label="shepherds-pastoral")
    g = c.seg(t_sud, t_light, 2, "3/4", "D major", nominal=105, label="shepherds-angel")
    li = c.seg(t_light, t_fear, 1, "3/4", "D major", nominal=67, label="shepherds-glory")
    f = c.seg(t_fear, t_np, 1, "3/4", "D major", nominal=90, label="shepherds-afraid")
    s = c.seg(t_np, t_today, 3, "3/4", "D major", nominal=94, label="shepherds-fear-not")
    t = c.seg(t_today, t_sign, 2, "3/4", "D major", nominal=81, label="shepherds-saviour")
    k = c.seg(t_sign, c.dur, 4, "6/8", "D major", nominal=106, label="shepherds-sign")
    segs = (p, g, li, f, s, t, k)
    for sg in segs:
        sg.duck(1.5)
    p.prog(" | ".join(PAST_PROG))
    g.prog("A7sus4:3 | A7:3")
    li.prog("D:3")
    f.prog("Bm:3")
    s.prog("G:3 | D/F#:3 | Em7:3/2 A7sus4:3/2")
    t.prog("D:3 | D/F#:3")
    k.prog("D:3 | G:3 | D/A:3/2 A7:3/2 | A:3")
    g.sync("'忽然': the angel (A7sus4)", 0, t_sud, kind="change")
    li.sync("'上帝的光': the glory of the Lord (D major)", 0, t_light, kind="change")
    t.sync("'今天，在伯利恒': a Saviour is born (D)", 0, t_today, kind="change")
    # the pastoral: the recorder over a drone
    p.mel("recorder", bars(PAST, 0, 4), vel=50)
    p.add("vc", 0, 12, "Bb2", 36, "bass")
    p.add("vla", 0, 12, "F3", 32, "pad", voice="vla.0")
    p.add("cb", 0, 12, "Bb1", 32, "bass")
    rock(p, 0, 12, lo=46, hi=58, vel=32, pat=(2, 3, 4, 3, 4, 3))
    p.duck(3.0, parts=["recorder"])
    p.expr(["recorder"], [(0, -17), (1.5, -13), (12, -13)])
    lv(p, ["vc", "vla", "cb"], -18)
    lv(p, ["harp"], -13)
    # '忽然': the angel -- the choir enters on the word; the attack on the picture's chime (else on the word)
    t_ap, _ = lead(c, segs, "chime", "忽然", 0, t_sud, t_light - 0.6, "the angel appears (a chime)",
                   glock=(86, 98), celesta=(74, 86))
    q_ap = qpos(g, c, t_ap, 0.0, g.n_q - 0.5) if t_ap is not None else 0.0
    t_wh = pic(c, "whoosh", "忽然", lo=t_sud, hi=t_light - 0.6)
    q_wh = qpos(g, c, t_wh, 0.0, q_ap) if t_wh is not None and t_wh <= (t_ap or t_sud) else q_ap
    sweep(g, q_wh + 0.01, 0.6, "A3", "A5", 32, 52)
    g.add("bells", q_ap, 6 - q_ap, "A4", 44, "arp", "h")
    glow(g, q_ap, vel=50, hi=(86, 98))
    g.add("pz_cb", q_ap, 1, "A1", 48, "bass", "h")
    g.add("timp", q_ap, 1, "A2", 42, "timp", "h")
    g.sync("the angel appears (a chime)" if t_ap is not None else "'忽然': the angel appears", q_ap,
           t_ap if t_ap is not None else t_sud)
    g.pad("choir", 3, 57, 74, vel=38, bass_ref=(33, 45))
    g.pad(["trem_va", "trem_hi", "trem_hi"], 3, 62, 81, vel=34, bass_ref=(33, 45))
    g.add("vc", 0, 6, "A2", 34, "bass")
    g.add("cb", 0, 6, "A1", 32, "bass")
    g.expr(["choir"], [(0, -25), (2, -19), (6, -18)])
    g.expr(["trem_va", "trem_hi"], [(0, -23), (3, -20), (6, -19)])
    lv(g, ["vc", "cb"], -19)
    lv(g, ["harp", "pz_cb", "timp", "bells"], -11)
    # '上帝的光': D major, radiant (a harp sweep rising with the picture's glow)
    t_gr = pic(c, "grow", "忽然", lo=t_light - 0.2, hi=t_fear - 0.8)
    q_gr = qpos(li, c, t_gr, 0.0, 1.5) if t_gr is not None else 0.0
    sweep(li, q_gr + 0.02, 0.8, "D4", "D6", 30, 48)
    li.add("bells", 0, 3, "D5", 40, "arp", "h")
    glow(li, 0.0, vel=46)
    li.pad("choir", 3, 60, 77, vel=40, bass_ref=(50, 62))
    li.pad(["vla", "vln2", "vln1"], 3, 62, 81, vel=38, bass_part="vc", bass_lo=50, bass_hi=62)
    li.add("cb", 0, 3, "D2", 34, "bass")
    li.add("pz_cb", 0, 1, "D2", 44, "bass", "h")
    li.add("okit", 0, 2, 57, 28, "perc", "h")
    li.duck(2.0, parts=["choir", "vln1", "vln2", "vla"])
    lv(li, ["choir"], -17)
    lv(li, ["vla", "vln2", "vln1", "vc", "cb"], -17)
    lv(li, ["harp", "pz_cb", "bells"], -12)
    lv(li, "okit", -16)
    # 'the shepherds were terrified': B minor -- low tremolo, a soft timpani roll
    f.pad(["trem_lo", "trem_va", "trem_va"], 3, 50, 66, vel=38, bass_ref=(35, 47))
    f.add("cb", 0, 3, "B1", 34, "bass")
    troll(f, 0.1, 2.9, midi("B2"), 24, 32)
    f.expr(["trem_lo", "trem_va"], [(0, -17), (3, -19)])
    lv(f, ["cb"], -18)
    lv(f, ["timp"], -13)
    # 'fear not: I bring you good news for all people': soft choir and strings
    s.pad("choir", 3, 57, 74, vel=36, bass_ref=(40, 52))
    strings(s, vel=36, lo=57, hi=74, bass=(40, 52), cb=(28, 40))
    broken(s, "harp", 0, 9, (0, 2, 4, 2, 4, 2), 38, 50, vel=30, thin=True)
    s.duck(2.5, parts=["choir"])
    lv(s, ["choir"], -22)
    lv(s, STR, -20)
    lv(s, ["harp"], -13)
    hit(c, segs, "sparkle", "不要怕", 0, "good news for all (a sparkle)", glock=(86, 98), vel=44)
    # 'today in Bethlehem a Saviour is born': the star motif on the horn (D), soft under the angel's voice
    t.mel("horn", bars(GIFT, 0, 2), vel=46, transpose=-13)
    t.pad(["vla", "vla", "vln2"], 3, 50, 66, vel=34, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(t, "cb", 28, 40, 32)
    roll_chord(t, 0, 38, 62, vel=38)
    t.duck(3.0)
    t.duck(5.0, parts=["horn"])
    lv(t, ["horn"], -20)
    t.expr(["vla", "vln2", "vc", "cb"], [(0, -20), (4.5, -20), (6, -17)])     # swelling into the sign
    lv(t, ["harp"], -13)
    hit(c, segs, "chime", "今天，在伯利恒", 0, "the Saviour (a chime)", glock=(86, 98), celesta=(74, 86), vel=46)
    # 'you will find a baby wrapped in cloths, lying in a manger': the lullaby's head in D (the sign)
    k.mel("celesta", bars(LULL, 0, 4), vel=44, transpose=-1)
    rock(k, 0, 12, lo=45, hi=57, vel=30)
    strings(k, vel=34, lo=62, hi=77, bass=(40, 52), cb=(28, 40))
    k.duck(2.5, parts=["celesta"])
    k.expr(["celesta"], [(0, -16), (1.5, -13), (12, -13)])
    k.sync("the sign: the lullaby begins (celesta)", 0, t_sign)
    k.expr(["harp"], [(0, -18), (1.5, -13), (12, -13)])
    k.expr(STR, [(0, -21), (1.5, -20), (12, -20)])
    hit(c, segs, "sparkle", "你们会看见", 0, "wrapped in cloths (a sparkle)", glock=(86, 98), vel=44)
    hit(c, segs, "sparkle", "你们会看见", 1, "the sign (a sparkle)", glock=(86, 98), celesta=(74, 86), vel=44)
    for sg in segs:
        lv(sg, ["glock"], -12)
        if sg is not k:
            lv(sg, ["celesta"], -12)


def choir(c):
    """The heavenly host: '忽然' -- Bm, the angels appear on the picture's chime (bells, harp, glockenspiel; the choir
    enters) and multiply (a celesta step for each new angel; B minor held, Em7 A7sus4, more voices, horns and a
    timpani roll
    growing); A7 on '一起赞美上帝'; the Gloria in D in the pause (trumpet: the star motif's head; horns, trombone, choir
    'aah', bells pealing, timpani, a soft cymbal) -- held, ducked, under the angels' song (a glint on '荣耀'); G, peace,
    on '在地上' (a chime); the bells again in the pause; '就是说' D (a sparkle on '天上'); G on '地上，上帝要把平安'
    -- the gift theme's cadence on the horn, landing on D with the picture's '平安' chime (else half-way)."""
    c.gain(1.0)
    t_sud = c.ls(0)
    t_praise = c.at("一起赞美上帝")
    t_glo = c.gap(c.find("在至高之处"))
    t_peace = c.at("在地上")
    t_exp = c.gap(c.find("就是说"))
    t_earth = c.at("地上，上帝要把平安")
    a0 = c.seg(0, t_sud, 1, "2/4", "D major", nominal=133, label="choir-hush")
    a = c.seg(t_sud, t_praise, 2, "4/4", "D major", nominal=123, label="choir-angels")
    b = c.seg(t_praise, t_glo, 1, "2/4", "D major", nominal=64, label="choir-praise")
    g = c.seg(t_glo, t_peace, 2, "3/4", "D major", nominal=103, label="choir-gloria")
    p = c.seg(t_peace, t_exp, 2, "3/4", "D major", nominal=100, label="choir-peace")
    r = c.seg(t_exp, t_earth, 2, "3/4", "D major", nominal=105, label="choir-heaven")
    t_pe = pic(c, "chime", "就是说")                         # 'peace on earth' (picture): the cadence lands on it
    ok = t_pe is not None and t_earth + 1.45 <= t_pe <= min(c.dur - 1.2, t_earth + 2.5)   # (a G-A7 bar at q 72-124)
    t_d = t_pe if ok else (t_earth + c.dur) / 2
    e = c.seg(t_earth, t_d, 1, "3/4", "D major", nominal=97, label="choir-earth")
    n = c.seg(t_d, c.dur, 1, "3/4", "D major", nominal=None, label="choir-peace-on-earth")   # the held cadence
    segs = (a0, a, b, g, p, r, e, n)
    for sg in segs:
        sg.duck(1.5)
    a.duck(7.0)
    b.duck(7.0)
    g.duck(10.0)
    p.duck(8.0)
    r.duck(5.0)
    e.duck(5.0)
    n.duck(5.0)
    a0.prog("A:2")
    a.prog("Bm:4 | Em7:2 A7sus4:2")
    b.prog("A7:2")
    g.prog("D:3 | Bm:3/2 D/A:3/2")
    p.prog("G:3 | A7sus4:3/2 A7:3/2")
    r.prog("D:3 | Bm7:3/2 A:3/2")
    e.prog("G:1 A7:2")
    n.prog("D:3")
    a.sync("'忽然': the heavenly host (B minor)", 0, t_sud, kind="change")
    g.sync("'在至高之处': the Gloria (D major)", 0, t_glo, kind="change")
    p.sync("'在地上': peace on earth (G)", 0, t_peace, kind="change")
    e.sync("'地上，上帝要把平安': on earth (G)", 0, t_earth, kind="change")
    # the hush before
    a0.pad(["vla", "vln2", "vln1"], 3, 57, 73, vel=32, bass_part="vc", bass_lo=45, bass_hi=57)
    lv(a0, ["vla", "vln2", "vln1", "vc"], -19)
    # the angels appear (the picture's chime, else the word) and multiply (a celesta step for each)
    t_ap, _ = lead(c, segs, "chime", None, 0, t_sud, t_praise - 1.0, "the angels appear (a chime)",
                   glock=(86, 98))
    q_ap = qpos(a, c, t_ap, 0.0, a.n_q - 1.0) if t_ap is not None else 0.0
    t_gr = pic(c, "grow", None, lo=t_sud, hi=t_praise - 1.0)
    q_gr = qpos(a, c, t_gr, 0.0, a.n_q - 1.0) if t_gr is not None else q_ap
    sweep(a, q_gr + 0.02, 0.7, "B3", "B5", 32, 50)
    a.add("bells", q_ap, _dq(a, q_ap, 2.0), "F#5", 44, "arp", "h")
    glow(a, q_ap, vel=50, hi=(83, 95))
    a.add("pz_cb", q_ap, 1, "B1", 48, "bass", "h")
    a.add("timp", q_ap, 1, "B2", 40, "timp", "h")
    a.sync("the angels appear (a chime)" if t_ap is not None else "'忽然': the angels appear", q_ap,
           t_ap if t_ap is not None else t_sud)
    more = [t_ for t_ in (pic(c, "sparkle", None, kk) for kk in range(3)) if t_ is not None]
    if more:
        climb(c, segs, more, lo=79, hi=96, vel=40, sync=tuple(range(len(more))), what="another angel appears")
    a.pad("choir", 3, 57, 76, vel=40, bass_ref=(40, 52))
    strings(a, vel=38, lo=57, hi=76, bass=(40, 52), cb=(28, 40))
    a.pad(["horn", "horn", "horn"], 3, 50, 65, vel=38, q0=4, bass_ref=(40, 52))
    troll(a, 5.0, 7.95, midi("A2"), 18, 30)
    a.expr(["choir"], [(0, -25), (2, -21), (8, -18)])
    a.expr(STR, [(0, -21), (8, -18)])
    a.expr(["horn"], [(4, -26), (8, -20)])
    lv(a, ["harp", "pz_cb", "timp", "bells"], -12)
    # '一起赞美上帝': A7 -- the timpani roll and a soft cymbal growing
    b.pad("choir", 3, 57, 76, vel=40, bass_ref=(33, 45))
    strings(b, vel=40, lo=57, hi=76, bass=(45, 57), cb=(33, 45))
    b.pad(["tbn", "horn", "horn"], 3, 45, 65, vel=40, bass_ref=(33, 45))
    troll(b, 0.0, 1.92, midi("A2"), 26, 40)
    roll(b, 0.2, 1.95, 59, 10, 26, rate=12)
    b.expr(["choir"], [(0, -19), (2, -16)])
    b.expr(STR, [(0, -19), (2, -16)])
    b.expr(["tbn", "horn"], [(0, -21), (2, -17)])
    lv(b, ["timp"], -13)
    lv(b, "okit", -16)
    # the Gloria: the trumpet's head of the star motif, bells, cymbal; held under the angels' song
    g.mel("tpt", "A4:1 F#5:2", vel=54)
    peal(g, 0, ["A5", "F#5", "D5", "A4"], vel=46, gap_s=0.15)
    sweep(g, 0.02, 0.5, "D4", "D6", 32, 46)
    glow(g, 0.0, vel=46)
    g.add("timp", 0, 0.5, "D3", 46, "timp", "h")
    g.add("pz_cb", 0, 1, "D2", 48, "bass", "h")
    g.add("okit", 0, 2, 57, 34, "perc", "h")
    g.pad("choir", 3, 62, 79, vel=42, bass_ref=(40, 52))
    strings(g, vel=40, lo=62, hi=81, bass=(40, 52), cb=(28, 40))
    g.pad(["tbn", "horn", "horn"], 3, 50, 66, vel=40, bass_ref=(40, 52))
    g.expr(["tpt"], [(0, -15), (3, -17)])
    g.expr(["choir"], [(0, -16), (1.5, -18), (6, -19)])
    g.expr(STR, [(0, -16), (1.5, -18), (6, -19)])
    g.expr(["tbn", "horn"], [(0, -17), (1.5, -21), (6, -22)])
    lv(g, ["timp", "pz_cb", "harp", "bells"], -14.5)
    lv(g, "okit", -17.5)
    hit(c, segs, "sparkle", "在至高之处", 0, "glory (a glint)", glock=(86, 98), vel=46)
    # '在地上，平安...': G, softer
    p.pad("choir", 3, 59, 76, vel=38, bass_ref=(43, 55))
    strings(p, vel=38, lo=59, hi=76, bass=(43, 55), cb=(31, 43))
    roll_chord(p, 0, 43, 67, vel=38)
    lv(p, ["choir"], -18, -19)
    lv(p, STR, -17, -18)
    lv(p, ["harp"], -12)
    hit(c, segs, "chime", "在至高之处", 0, "peace (a chime)", celesta=(79, 91), glock=(86, 98), vel=44)
    # '就是说：天上，要赞美上帝！': D, the bells again in the pause
    peal(r, 0, ["F#5", "D5", "A4", "D4"], vel=44, gap_s=0.15)
    glow(r, 0.0, vel=44)
    r.sync("the bells ring again (the pause after the angels' song)", 0, t_exp)
    r.pad("choir", 3, 62, 79, vel=36, bass_ref=(40, 52))
    strings(r, vel=38, lo=60, hi=78, bass=(40, 52), cb=(28, 40))
    broken(r, "harp", 0.5, 6, (0, 2, 4, 2, 4, 2), 38, 50, vel=30, thin=True)
    lv(r, ["choir"], -19)
    lv(r, STR, -17)
    lv(r, ["harp", "bells"], -12)
    hit(c, segs, "sparkle", "就是说", 0, "heaven (a sparkle)", glock=(86, 98), vel=44)
    # '地上，上帝要把平安送给他喜爱的人': G, the gift theme's cadence on the horn (D)
    e.mel("horn", GIFT[6], vel=48, transpose=-13)
    n.mel("horn", GIFT[7], vel=48, transpose=-13)
    roll_chord(e, 0, 43, 67, vel=38)
    roll_chord(n, 0.3, 38, 62, vel=34)
    n.add("pz_cb", 0, 1, "D2", 42, "bass", "h")
    for sg in (e, n):
        strings(sg, vel=38, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
        sg.pad("ooh", 3, 57, 74, vel=30, bass_ref=(43, 55))
        sg.duck(2.5, parts=["horn"])
        lv(sg, ["horn"], -16)
        lv(sg, STR, -18)
        lv(sg, ["ooh"], -22)
        lv(sg, ["harp", "pz_cb"], -12)
    hit(c, segs, "chime", "就是说", 0, "peace on earth (a chime)", celesta=(79, 91), vel=46)
    for sg in segs:
        lv(sg, ["glock", "celesta"], -12)


def visit(c):
    """'天使们回天上去了' (D: harp and celesta rising, the choir fading upward); B-flat on '牧羊人你看看我' -- plucked
    glances; E-flat F7 ('我们快去伯利恒看看吧'); the shepherds' running tune (B-flat 6/8 on the recorder) on
    '他们急急忙忙'; searching (Cm7 B-flat7); E-flat on '找到了' -- the lullaby; the gift theme on the horn on
    '他就是天使说的救主'; the shepherds' tune, happy, on '牧羊人好开心'; A-flat add9 (wonder) and the lullaby,
    very soft, for Mary pondering on '马利亚呢'."""
    c.gain(-2.0)
    t_look = c.at("牧羊人你看看我")
    t_go = c.gap(c.find("我们快去伯利恒看看吧"))
    t_run = c.gap(c.find("他们急急忙忙"))
    t_found = c.at("找到了")
    t_seek = t_run + 2 * (t_found - t_run) / 3              # the run and the search ('找啊找') at one tempo
    t_he = c.gap(c.find("他就是天使说的救主"))
    t_joy = c.gap(c.find("牧羊人好开心"))
    t_won = c.gap(c.find("听见的人"))
    t_mary = c.at("马利亚呢")
    u = c.seg(0, t_look, 2, "3/4", "D major", nominal=122, label="visit-angels-go")
    k = c.seg(t_look, t_go, 2, "2/4", "Bb major", nominal=71, label="visit-glances")
    s = c.seg(t_go, t_run, 2, "6/8", "Bb major", nominal=132, label="visit-lets-go")
    r = c.seg(t_run, t_seek, 2, "6/8", "Bb major", nominal=133, label="visit-run")
    f = c.seg(t_seek, t_found, 1, "6/8", "Bb major", nominal=133, label="visit-search")
    m = c.seg(t_found, t_he, 3, "6/8", "Eb major", nominal=87, label="visit-found")
    h = c.seg(t_he, t_joy, 2, "3/4", "Eb major", nominal=69, label="visit-saviour")
    j = c.seg(t_joy, t_won, 4, "6/8", "Bb major", nominal=117, label="visit-tell")
    w = c.seg(t_won, t_mary, 1, "3/4", "Eb major", nominal=None, label="visit-wonder")        # a held chord
    y = c.seg(t_mary, c.dur, 3, "6/8", "Eb major", nominal=106, rit=0.15, label="visit-mary")
    segs = (u, k, s, r, f, m, h, j, w, y)
    for sg in segs:
        sg.duck(1.5)
    u.prog("D:3 | D:3")
    k.prog("Bb:2 | F7:2")
    s.prog("Eb:3 | F7:3")
    r.prog(" | ".join(SHEP_PROG[:2]))
    f.prog("Cm7:3/2 Bb7:3/2")
    m.prog(" | ".join([LULL_PROG[0], LULL_PROG[1], LULL_PROG[3]]))
    h.prog("Eb:3 | Cm:3")
    j.prog(" | ".join(SHEP_PROG[4:8]))
    w.prog("Abadd9:3")
    y.prog("Eb:3 | Cm7:3/2 Bb7:3/2 | Eb:3")
    k.sync("'牧羊人你看看我': back on earth (B-flat)", 0, t_look, kind="change")
    r.sync("'他们急急忙忙': the shepherds run (B-flat)", 0, t_run, kind="change")
    m.sync("'找到了': found (E-flat)", 0, t_found, kind="change")
    h.sync("'他就是天使说的救主': the Saviour (E-flat)", 0, t_he, kind="change")
    j.sync("'牧羊人好开心': the shepherds tell everyone (B-flat)", 0, t_joy, kind="change")
    y.sync("'马利亚呢': Mary ponders (E-flat)", 0, t_mary, kind="change")
    # the angels go back up to heaven (a harp sweep from the picture's whoosh, a glint on its chime)
    t_up = pic(c, "whoosh", None, lo=0.0, hi=t_look - 1.0)
    sweep(u, qpos(u, c, t_up, 0.0, 3.0) + 0.02 if t_up is not None else 0.02, 0.9, "D4", "D7", 28, 44)
    hit(c, segs, "chime", None, 0, "the angels go back to heaven (a chime)", glock=(86, 98), celesta=(79, 91), vel=46)
    u.mel("celesta", "A5:1 D6:1 F#6:1 | A6:3", vel=40, role="arp")
    u.pad("choir", 3, 62, 79, vel=34, bass_ref=(38, 50))
    u.pad(["vla", "vln2", "vln1"], 3, 62, 81, vel=34, bass_part="vc", bass_lo=50, bass_hi=62)
    u.expr(["choir"], [(0, -19), (6, -24)])
    u.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (6, -18)])
    lv(u, ["harp"], -13)
    lv(u, ["celesta"], -14)
    # 'the shepherds looked at each other': plucked glances
    for qq, hi_ in ((0.0, 70), (0.5, 74), (2.0, 72), (2.5, 69)):
        k.add("pz_hi", qq, 0.25, top(k, qq, 58, hi_), 48, "arp", "s")
    k.add("pz_lo", 0, 1, "Bb2", 36, "arp", "s")
    k.add("pz_lo", 2, 1, "F2", 36, "arp", "s")
    k.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    lv(k, ["pz_hi", "pz_lo"], -9)
    lv(k, ["vla", "vln2", "vln1", "vc"], -17)
    # "let's go to Bethlehem!": E-flat F7, the plucked bass climbing
    for qq, nm in ((0.0, "Eb3"), (1.5, "G3"), (3.0, "F3"), (4.5, "A3")):
        s.add("pz_lo", qq, 1.5, nm, 46, "arp", "s")
    s.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_ref=(39, 51))
    s.mel("recorder", "r:3 | C5:1/2 D5:1/2 Eb5:1/2 F5:3/2", vel=46)
    lv(s, ["pz_lo"], -10)
    s.expr(["vla", "vln2", "vln1"], [(0, -20), (6, -18)])
    lv(s, ["recorder"], -14)
    # the run: the shepherds' tune, quick
    r.mel("recorder", bars(SHEP, 0, 2), vel=50)
    f.mel("recorder", "C5:1/2 D5:1/2 Eb5:1/2 F5:1 Ab4:1/2", vel=48)
    for sg_ in (r, f):
        for qq in np.arange(0, sg_.n_q, 1.5):
            ch = sg_.chord_at(qq + 1e-3)
            sg_.add("pz_lo", qq, 0.5, ch.bass_note(39, 51), 44, "arp", "s")
            sg_.add("pz_hi", qq + 0.5, 0.5, ch.tones(58, 70)[0], 34, "arp", "s")
            sg_.add("pz_hi", qq + 1.0, 0.5, ch.tones(58, 70)[1], 32, "arp", "s")
        sg_.pad(["vla", "vln2"], 2, 58, 72, vel=30, bass_ref=(39, 51))
        lv(sg_, ["pz_lo", "pz_hi"], -12)
        lv(sg_, ["vla", "vln2"], -21)
        lv(sg_, ["recorder"], -14)
    # '找到了': E-flat -- found; the lullaby
    t_fd, _ = lead(c, segs, "sparkle", "他们急急忙忙", 0, t_found, t_found + 0.45, "found (a sparkle)",
                   glock=(86, 98))
    q_fd = qpos(m, c, t_fd, 0.0, 1.4) if t_fd is not None else 0.0
    sweep(m, q_fd + 0.02, 0.5, "Eb4", "Eb6", 30, 48)
    glow(m, q_fd, vel=48)
    if t_fd is not None:
        m.sync("found (a sparkle)", q_fd, t_fd)
    if q_fd < 0.9:                                         # mi' (from the sparkle) re' mi' sol
        m.add("celesta", q_fd, 1.0 - q_fd, "G5", 46, "melody")
    m.mel("celesta", "F5:1/2 G5:1 Bb4:1/2 | " + LULL[1] + " | " + LULL[3], q=1.0, vel=46)
    rock(m, 0, 9, vel=30)
    strings(m, vel=34, lo=55, hi=72)
    m.pad("ooh", 3, 58, 72, vel=28, bass_ref=(41, 53))
    m.duck(2.5, parts=["celesta"])
    lv(m, ["celesta"], -13)
    lv(m, ["harp"], -13)
    lv(m, STR, -20)
    lv(m, ["ooh"], -24)
    # 'he is the Saviour the angel spoke of': the gift theme on the horn
    h.mel("horn", bars(GIFT, 0, 2), vel=48, transpose=-12)
    strings(h, vel=36, lo=55, hi=72)
    roll_chord(h, 0, 39, 63, vel=38)
    h.pad("ooh", 3, 58, 74, vel=30, bass_ref=(41, 53))
    h.duck(3.0, parts=["horn"])
    lv(h, ["horn"], -16)
    lv(h, STR, -20)
    lv(h, ["harp"], -12)
    lv(h, ["ooh"], -23)
    hit(c, segs, "chime", "他就是天使说的救主", 0, "the Saviour (a chime)", glock=(86, 98), celesta=(74, 86), vel=46)
    hit(c, segs, "sparkle", "他就是天使说的救主", 0, "sent by God (a sparkle)", glock=(88, 100), vel=44)
    # 'the shepherds were so happy, they told everyone': the shepherds' tune, a tambourine in the pauses
    j.mel("recorder", bars(SHEP, 4, 8), vel=48)
    for qq in np.arange(0, 12, 1.5):
        ch = j.chord_at(qq + 1e-3)
        j.add("pz_lo", qq, 0.5, ch.bass_note(39, 51), 42, "arp", "s")
        j.add("pz_hi", qq + 0.5, 0.5, ch.tones(58, 70)[0], 32, "arp", "s")
        j.add("pz_hi", qq + 1.0, 0.5, ch.tones(58, 70)[1], 30, "arp", "s")
        if not bool(j.score.speaking(j.t(qq))):
            drum(j, qq, 54, 30)
    j.pad(["vla", "vln2"], 2, 58, 72, vel=30, bass_ref=(39, 51))
    j.duck(2.5, parts=["recorder"])
    lv(j, ["recorder"], -15)
    lv(j, ["pz_lo", "pz_hi"], -12)
    lv(j, "hand", -16)
    lv(j, ["vla", "vln2"], -21)
    # 'all who heard were amazed': A-flat add9, wonder
    roll_chord(w, 0, 44, 70, vel=36)
    w.pad(["vla", "vln2", "vln1"], 3, 58, 75, vel=32, bass_part="vc", bass_lo=44, bass_hi=56)
    w.add("celesta", 1, 2, "Bb5", 34, "arp")
    lv(w, ["harp"], -13)
    lv(w, ["vla", "vln2", "vln1", "vc"], -20)
    lv(w, ["celesta"], -15)
    hit(c, segs, "pop", "听见的人", 0, "everyone is amazed (a pop)", pluck=(62, 74), celesta=(79, 91), vel=46)
    # 'but Mary treasured all these things in her heart': the lullaby, very soft (Cm7, so the picture's heart chime,
    # tuned E-flat from the score, rings on in the next chord)
    y.mel("celesta", "G5:1 F5:1/2 G5:3/2 | C5:1 Eb5:1/2 D5:1 F5:1/2 | Eb5:3", vel=44)
    rock(y, 0, 9, vel=30)
    y.pad(["vla", "vln2", "vln1"], 3, 56, 72, vel=32, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(y, "cb", 29, 41, 30)
    y.duck(2.0, parts=["celesta"])
    lv(y, ["celesta"], -14, -15)
    lv(y, ["harp"], -13)
    y.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -20), (9, -22)])
    t_hc = pic(c, "chime", "听见的人")                       # kept in her heart (picture): a clear glint
    if t_hc is not None:
        clear_near(c, t_hc, win=0.22)
        accent(c, segs, t_hc, "kept in her heart (a chime)", glock=(86, 98), celesta=(74, 86), harp=(62, 74), vel=48)
    for sg in segs:
        lv(sg, ["glock", "pz_hi"], -12)
        if sg not in (u, m, w, y):
            lv(sg, ["celesta"], -12)


def star(c):
    """The East (C dorian: the English horn over a C drone, the dulcimer, a soft finger cymbal; a celesta star where
    the picture's stars sparkle, '研究星星'); B-flat F7sus4, the strings rising (a harp sweep as the picture's star begins
    to rise); E-flat lydian on '一颗特别的星星' -- the star motif on the celesta and glockenspiel from the picture's
    chime (harp up, choir 'ooh'); F/E-flat sparkles and a noble horn call on '有一位王出生了' (a glint on '王'), G;
    the caravan (C dorian 2/4: do. re | me sol | la. sol | fa -- the English horn, the dulcimer, plucked basses, finger
    cymbals; the low drum on the camels' steps) on '他们出发了'."""
    c.gain(-2.0)
    t_stud = c.at("博士，就是")
    t_day = c.gap(c.find("有一天"))
    t_star = c.at("一颗特别的星星")
    t_w = c.gap(c.find("这颗星星告诉我们"))
    t_go = c.gap(c.find("他们出发了"))
    e = c.seg(0, t_stud, 2, "4/4", "C dorian", nominal=107, label="star-east")
    s = c.seg(t_stud, t_day, 2, "4/4", "C dorian", nominal=110, label="star-wise-men")
    d = c.seg(t_day, t_star, 1, "4/4", "C dorian", nominal=82, label="star-one-day")
    t = c.seg(t_star, t_w, 1, "3/4", "Eb lydian", nominal=100, label="star-rises")
    w = c.seg(t_w, t_go, 3, "3/4", "Eb lydian", nominal=99, label="star-king")
    v = c.seg(t_go, c.dur, 4, "2/4", "C dorian", nominal=87, label="star-caravan")
    segs = (e, s, d, t, w, v)
    for sg in segs:
        sg.duck(1.5)
    e.prog("Cm:4 | F/C:4")
    s.prog("Gm/C:4 | Cm:4")
    d.prog("Bb:2 F7sus4:2")
    t.prog("Eb:3")
    w.prog("F/Eb:3 | Eb:3 | G:3@C-melodic")
    v.prog(" | ".join(CAR_PROG[:4]))
    t.sync("'一颗特别的星星': the star (E-flat lydian)", 0, t_star, kind="change")
    v.sync("'他们出发了': the caravan sets off (C dorian)", 0, t_go, kind="change")
    # the East: the English horn over a drone, the dulcimer
    e.mel("ehorn", "G4:2 A4:1 Bb4:1 | A4:2 F4:2", vel=50)
    s.mel("ehorn", "Bb4:2 A4:1 G4:1 | Eb4:2 G4:2", vel=48)
    for sg in (e, s):
        sg.add("vc", 0, 8, "C3", 34, "pad", voice="vc.0")
        sg.add("cb", 0, 8, "C2", 32, "bass")
        broken(sg, "dulcimer", 0, 8, (2, 3, 4, 3), 55, 72, vel=40, step=0.5, thin=True)
        drum(sg, 0, 81, 28)
        drum(sg, 4, 81, 26)
        sg.pad(["vla", "vln2"], 2, 55, 70, vel=30, bass_ref=(36, 48))
        sg.duck(3.0, parts=["ehorn"])
        sg.expr(["ehorn"], [(0, -17 if sg is e else -15), (1, -14), (8, -14)])
        lv(sg, ["vc", "cb"], -19)
        lv(sg, ["dulcimer"], -12)
        lv(sg, "hand", -15)
        lv(sg, ["vla", "vln2"], -21)
    t_s0 = pic(c, "sparkle", None, 0)                       # the stars the wise men study (picture)
    sp = [t_s0] if t_s0 is not None else []
    even = [t_stud + 1.0 + kk * (t_day - 0.4 - t_stud - 1.0) / 4 for kk in range(4)]
    times = sorted(sp + [t_ for t_ in even if all(abs(t_ - x) > 0.4 for x in sp)])
    stars(segs, c, times, lo=79, hi=91, vel=36, glock_every=0, synced=sp, what="a star sparkles over the wise men")
    # 'one day they saw...': B-flat F7sus4 (the mix tunes the rising star's bell from it: E-flat), the strings
    # rising; a harp sweep as the star begins to rise (picture)
    d.pad(["trem_va", "trem_hi", "trem_hi"], 3, 58, 77, vel=34, bass_ref=(41, 53))
    bassline(d, "vc", 41, 53, 34)
    broken(d, "harp", 0, 4, (2, 3, 4, 3), 53, 70, vel=30, step=0.25, thin=True)
    t_gr = pic(c, "grow", "有一天", lo=t_day, hi=t_star + 0.2)
    if t_gr is not None and t_gr < t_star - 0.15:
        q_gr = qpos(d, c, t_gr, 0.0, d.n_q - 0.3)
        sweep(d, q_gr, min(0.9, d.t(d.n_q) - d.t(q_gr) - 0.05), "Bb3", "F6", 26, 44)
    d.duck(3.0)
    d.expr(["trem_va", "trem_hi"], [(0, -23), (4, -20)])
    lv(d, ["vc"], -19)
    lv(d, ["harp"], -15)
    # the star: E-flat lydian -- the star motif from the picture's chime (else on the word), harp up, choir 'ooh'
    t_ch, _ = lead(c, segs, "chime", "有一天", 0, t_star, t_w - 0.9, "the star shines (a chime)",
                   celesta=(79, 91), glock=(86, 98))
    q_ch = qpos(t, c, t_ch, 0.0, 2.6) if t_ch is not None else 0.0
    d1 = min(1.0, (3.0 - q_ch) / 2)                         # sol (on the picture) ... mi'
    t.add("celesta", q_ch, d1, "Bb5", 52, "melody", "h")
    t.add("glock", q_ch, d1, "Bb6", 42, "counter", "h", voice="glock.0")
    t.add("celesta", q_ch + d1, 3.0 - q_ch - d1, "G6", 50, "melody")
    t.add("glock", q_ch + d1, 3.0 - q_ch - d1, "G7", 40, "counter", voice="glock.0")
    if t_ch is not None:
        t.sync("the star shines (a chime)", q_ch, t_ch)
    sweep(t, q_ch + 0.02, 0.5, "Eb4", "Eb6", 32, 50)
    t.pad("ooh", 3, 58, 75, vel=34, bass_ref=(39, 51))
    t.pad(["vla", "vln2", "vln1"], 3, 62, 79, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    t.add("cb", 0, 3, "Eb2", 32, "bass")
    t.add("pz_cb", 0, 1, "Eb2", 44, "bass", "h")
    t.duck(2.5, parts=["celesta", "glock", "vla", "vln2", "vln1", "ooh"])
    lv(t, ["celesta"], -16)
    lv(t, ["glock"], -19)
    lv(t, ["harp", "pz_cb"], -12)
    t.expr(["ooh"], [(0, -24), (3, -20)])
    lv(t, ["vla", "vln2", "vln1", "vc", "cb"], -18)
    # 'this star tells us a king is born -- let us go and worship him': lydian sparkle, a horn call, G
    w.mel("celesta", "A6:1 F6:1 C6:1 | Bb5:3", vel=44)
    w.mel("horn", "r:3 | Bb3:1 Eb4:3/2 F4:1/2 | G4:3", vel=46)
    w.pad("ooh", 3, 58, 75, vel=32, bass_ref=(41, 53), q1=6)
    w.pad(["vla", "vln2", "vln1"], 3, 58, 75, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(w, "cb", 29, 41, 30)
    w.add("timp", 6, 0.5, "G2", 36, "timp", "h")
    w.duck(3.0, parts=["horn"])
    lv(w, ["celesta"], -13)
    lv(w, ["horn"], -16)
    lv(w, ["ooh"], -21, q1=6)
    lv(w, ["vla", "vln2", "vln1", "vc", "cb"], -19)
    lv(w, ["timp"], -13)
    hit(c, segs, "sparkle", "这颗星星告诉我们", 0, "a king is born (a glint)", glock=(86, 98), vel=44)
    # the caravan sets off: plucked basses on the beats, the low drum on the camels' steps (picture)
    v.mel("ehorn", bars(CAR, 0, 4), vel=52)
    steps = [t_ for t_ in (pic(c, "thud", "他们出发了", kk) for kk in range(5)) if t_ is not None]
    for qq in range(8):
        ch = v.chord_at(qq + 1e-3)
        if qq % 2 == 0:
            v.add("pz_lo", qq, 1, ch.bass_note(36, 48), 46, "arp", "s")
            if not steps:
                drum(v, qq, 64, 36)
        else:
            v.add("pz_lo", qq, 1, ch.tones(43, 55)[1], 38, "arp", "s")
            if all(abs(v.t(qq + 0.5) - c.t0 - ts) > 0.25 for ts in steps):   # finger cymbals off the camels' steps
                drum(v, qq + 0.5, 81, 24)
    for kk, ts in enumerate(steps):                         # a camel's step: the low drum, a plucked bass
        clear_near(c, ts)
        sg, q_st = seg_at(c, segs, ts)
        drum(sg, q_st, 64, 46 if kk in (0, 4) else 38)
        sg.add("pz_cb", q_st, _dq(sg, q_st, 0.5), sg.chord_at(q_st + 1e-3).bass_note(29, 41), 46, "bass", "h")
        if kk in (0, 4):
            sg.sync(f"a camel's step ({kk + 1})", q_st, ts)
    broken(v, "dulcimer", 0, 8, (2, 3, 4, 3), 55, 72, vel=38, step=0.5, thin=True)
    v.add("vc", 0, 8, "C3", 32, "pad", voice="vc.0")
    v.pad(["vla", "vln2"], 2, 55, 70, vel=30, bass_ref=(36, 48))
    v.duck(3.0, parts=["ehorn"])
    lv(v, ["ehorn"], -14)
    lv(v, ["pz_lo", "pz_cb"], -11)
    lv(v, "hand", -13)
    lv(v, ["dulcimer"], -13)
    lv(v, ["vc", "vla", "vln2"], -21)
    for sg in segs:
        if sg is not t:
            lv(sg, ["glock"], -12)
        if sg not in (t, w):
            lv(sg, ["celesta"], -12)


def gifts(c):
    """The caravan's tail (G minor); E-flat on '忽然' and the star again, gold (the star motif on the glockenspiel and
    celesta, harp up, choir 'ooh'); the caravan theme turned major on '在前面给他们带路' (the English horn, the
    dulcimer, celesta glints); A-flat on '停在了' -- the star stops (a bell, a harp roll); the star motif, bright, on
    '博士们高兴极了'; the lullaby as they kneel; the treasure boxes (E-flat, harp); a chime for each gift -- 黄金
    the glockenspiel, 乳香 the celesta and harp, 没药 a tubular bell (E-flat, A-flat/E-flat, B-flat/E-flat over a
    pedal); the gift theme's climax on '乳香和没药' and the royal E-flat on '宝贝' (horns, timpani, harp roll)."""
    c.gain(-2.5)
    t_sud = c.ls(0)
    t_lead = c.at("在前面给他们带路")
    t_stop = c.at("停在了")
    t_joy = c.gap(c.find("博士们高兴极了"))
    t_in = c.at("他们走进房子")
    t_open = c.gap(c.find("他们打开宝盒"))
    t_gw = c.at("黄金")
    t_fw = c.at("乳香")
    t_mw = c.at("没药")
    t_say = c.gap(c.find("乳香和没药"))
    t_tre = c.at("宝贝")
    a = c.seg(0, t_sud, 1, "2/4", "C dorian", nominal=133, label="gifts-caravan")
    s = c.seg(t_sud, t_lead, 1, "3/4", "Eb major", nominal=79, label="gifts-star")
    l = c.seg(t_lead, t_stop, 4, "2/4", "Eb major", nominal=94, label="gifts-lead")
    p = c.seg(t_stop, t_joy, 1, "3/4", "Eb major", nominal=78, label="gifts-stops")
    j = c.seg(t_joy, t_in, 1, "3/4", "Eb major", nominal=92, label="gifts-joy")
    k = c.seg(t_in, t_open, 3, "6/8", "Eb major", nominal=92, label="gifts-kneel")
    o = c.seg(t_open, t_gw, 2, "3/4", "Eb major", nominal=91, label="gifts-boxes")
    g = c.seg(t_gw, t_say, 1, "3/4", "Eb major", nominal=65, label="gifts-three")
    r = c.seg(t_say, t_tre, 3, "3/4", "Eb major", nominal=87, label="gifts-precious")
    z = c.seg(t_tre, c.dur, 1, "2/4", "Eb major", nominal=145, label="gifts-king")
    segs = (a, s, l, p, j, k, o, g, r, z)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Gm:2")
    s.prog("Eb:3")
    l.prog("Eb:2 | Eb:2 | Ab:2 | Bb7:2")
    p.prog("Ab:3")
    j.prog("Eb:3")
    k.prog("Eb:3 | Ab:3 | Fm7:3/2 Bb7sus4:3/2")
    o.prog("Eb:3 | Cm7:3/2 Bb7sus4:3/2")
    g_ed = edges48(g, c, [t_fw, t_mw])
    prog48(g, ["Eb", "Ab/Eb", "Bb/Eb"], g_ed)
    r.prog(" | ".join(GIFT_PROG[4:7]))
    z.prog("Eb:2")
    s.sync("'忽然': the star again (E-flat)", 0, t_sud, kind="change")
    p.sync("'停在了': the star stops (A-flat)", 0, t_stop, kind="change")
    j.sync("'博士们高兴极了': joy (E-flat)", 0, t_joy, kind="change")
    g.sync("'乳香': A-flat/E-flat", g_ed[1] / 48, t_fw, kind="change")
    z.sync("'宝贝': the treasures for the king (E-flat)", 0, t_tre, kind="change")
    # the caravan's tail
    a.mel("ehorn", "D4:1 Bb3:1", vel=48)
    a.add("pz_lo", 0, 1, "G2", 42, "arp", "s")
    drum(a, 0, 64, 32)
    a.add("vc", 0, 2, "D3", 30, "pad", voice="vc.0")
    lv(a, ["ehorn"], -13)
    lv(a, ["pz_lo"], -11)
    lv(a, "hand", -15)
    lv(a, ["vc"], -20)
    # the star again: E-flat gold (the picture's chime, else the word)
    t_sc, _ = lead(c, segs, "chime", None, 0, t_sud, t_lead - 0.6, "the star appears again (a chime)",
                   glock=(86, 98), celesta=(74, 86))
    q_sc = qpos(s, c, t_sc, 0.0, 2.6) if t_sc is not None else 0.0
    d1 = min(1.0, (3.0 - q_sc) / 2)                         # sol (on the picture) ... mi'
    s.add("glock", q_sc, d1, "Bb6", 44, "melody", "h")
    s.add("celesta", q_sc, d1, "Bb5", 50, "counter", "h", voice="celesta.0")
    s.add("glock", q_sc + d1, 3.0 - q_sc - d1, "G7", 44, "melody")
    s.add("celesta", q_sc + d1, 3.0 - q_sc - d1, "G6", 48, "counter", voice="celesta.0")
    if t_sc is not None:
        s.sync("the star appears again (a chime)", q_sc, t_sc)
    sweep(s, q_sc + 0.02, 0.55, "Eb4", "Eb6", 34, 52)
    s.pad("ooh", 3, 58, 75, vel=36, bass_ref=(39, 51))
    strings(s, vel=38, lo=60, hi=77)
    s.add("pz_cb", 0, 1, "Eb2", 46, "bass", "h")
    s.duck(2.5, parts=["glock", "celesta", "vla", "vln2", "vln1", "ooh"])
    lv(s, ["glock"], -14)
    lv(s, ["celesta"], -13)
    lv(s, ["harp", "pz_cb"], -12)
    s.expr(["ooh"], [(0, -24), (3, -20)])
    lv(s, STR, -18)
    # 'it went ahead of them, all the way to Bethlehem': the caravan theme in E-flat
    l.mel("ehorn", " | ".join(CAR_MAJ[:3]) + " | Ab4:2", vel=50)
    for qq in range(8):
        ch = l.chord_at(qq + 1e-3)
        l.add("pz_lo", qq, 1, ch.bass_note(39, 51) if qq % 2 == 0 else ch.tones(46, 58)[1], 40, "arp", "s")
        if qq % 2 == 0:
            drum(l, qq, 64, 30)
    broken(l, "dulcimer", 0, 8, (2, 3, 4, 3), 55, 72, vel=36, step=0.5, thin=True)
    l.pad(["vla", "vln2", "vln1"], 3, 58, 75, vel=34, bass_ref=(39, 51))
    for qq in (1.5, 3.5, 5.5):
        if not bool(l.score.speaking(l.t(qq))):
            l.add("celesta", qq, 0.5, top(l, qq, 84, 96), 36, "arp", "h")
    l.duck(3.0, parts=["ehorn"])
    lv(l, ["ehorn"], -14)
    lv(l, ["pz_lo"], -11)
    lv(l, "hand", -15)
    lv(l, ["dulcimer"], -13)
    lv(l, ["vla", "vln2", "vln1"], -20)
    # '...and stopped over a house': A-flat -- the star stops (a bell, a harp roll)
    p.mel("ehorn", "Ab4:3", vel=44)
    roll_chord(p, 0, 44, 72, vel=40)
    t_sp, _ = lead(c, segs, "sparkle", "星星一直走到伯利恒", 0, t_stop, t_stop + 0.6, "the star stops (a bell)",
                   glock=(86, 98))
    q_sp = qpos(p, c, t_sp, 0.0, 2.5) if t_sp is not None else 0.0
    p.add("bells", q_sp, 3 - q_sp, "Eb5", 42, "arp", "h")
    glow(p, q_sp, vel=44)
    if t_sp is not None:
        p.sync("the star stops (a bell)", q_sp, t_sp)
    p.pad("ooh", 3, 58, 75, vel=32, bass_ref=(44, 56))
    p.pad(["vla", "vln2", "vln1"], 3, 58, 75, vel=34, bass_part="vc", bass_lo=44, bass_hi=56)
    p.add("cb", 0, 3, "Ab1", 30, "bass")
    lv(p, ["ehorn"], -17)
    lv(p, ["harp", "bells"], -13)
    lv(p, ["ooh"], -22)
    lv(p, ["vla", "vln2", "vln1", "vc", "cb"], -19)
    # 'the wise men were overjoyed': the star motif, bright
    j.mel("recorder", GIFT[0], vel=48)
    j.mel("celesta", GIFT[0], vel=40, transpose=12, role="counter")
    strings(j, vel=36, lo=57, hi=74)
    waltz(j, 0, 3, vel=40)
    jingle(j, 0, vel=30)
    lv(j, ["recorder"], -15)
    lv(j, ["celesta"], -15)
    lv(j, STR, -19)
    lv(j, ["pz_lo", "harp"], -13)
    lv(j, "hand", -16)
    hit(c, segs, "chime", "博士们高兴极了", 0, "the wise men rejoice (a chime)", glock=(86, 98), vel=46)
    # 'they went in, saw the child with Mary, and knelt': the lullaby
    k.mel("celesta", LULL[0] + " | " + LULL[1] + " | Ab4:1 C5:1/2 Bb4:3/2", vel=44)
    rock(k, 0, 9, vel=30)
    strings(k, vel=34, lo=55, hi=72)
    k.pad("ooh", 3, 58, 72, vel=28, bass_ref=(41, 53))
    k.duck(2.5, parts=["celesta"])
    lv(k, ["celesta"], -13)
    lv(k, ["harp"], -13)
    lv(k, STR, -20)
    lv(k, ["ooh"], -24)
    # 'they opened their treasure boxes': E-flat, harp shimmer
    broken(o, "harp", 0, 6, (2, 3, 4, 5, 4, 3), 51, 70, vel=34, step=0.5, thin=True)
    strings(o, vel=36, lo=57, hi=74)
    o.pad("ooh", 3, 58, 74, vel=30, bass_ref=(41, 53))
    lv(o, ["harp"], -11)
    lv(o, STR, -18)
    lv(o, ["ooh"], -23)
    hit(c, segs, "cloth", "他们打开宝盒", 0, "the treasure boxes open", harp=(62, 74), celesta=(79, 91), vel=46)
    # gold, frankincense, myrrh: a chime for each (the picture's, else as the narrator names them)
    sp = [pic(c, "sparkle", "他们打开宝盒", kk) for kk in range(3)]
    have = None not in sp
    names = syl(c, "黄金", 3)
    spoken = [names[0], names[1], (names[2] + (t_mw - c.at("还有没药"))) if len(names) > 2 else t_mw]
    chimes = sp if have else spoken
    g.add("vc", 0, 3, "Eb3", 32, "pad", voice="vc.0")
    g.add("cb", 0, 3, "Eb2", 30, "bass")
    g.pad(["vla", "vln2", "vln1"], 3, 58, 77, vel=34, bass_ref=(39, 51))
    for kk, (tk, what) in enumerate(zip(chimes, ("gold", "frankincense", "myrrh"))):
        sg, qk = seg_at(c, segs, tk)
        if kk == 0:
            sg.add("glock", qk, _dq(sg, qk, 1.0), top(sg, qk, 86, 98), 52, "arp", "h")
            sg.add("celesta", qk, _dq(sg, qk, 1.0), top(sg, qk, 74, 86), 40, "arp", "h")
        elif kk == 1:
            sg.add("celesta", qk, _dq(sg, qk, 1.0), top(sg, qk, 81, 93), 52, "arp", "h")
            sg.add("harp", qk, _dq(sg, qk, 1.0), top(sg, qk, 67, 79), 50, "arp", "h")
            sg.add("harp", qk, _dq(sg, qk, 1.0), top(sg, qk, 60, 70), 46, "arp", "h")
        else:
            sg.add("bells", qk, _dq(sg, qk, 1.0), top(sg, qk, 62, 74), 48, "arp", "h")
            sg.add("celesta", qk, _dq(sg, qk, 1.0), top(sg, qk, 74, 86), 42, "arp", "h")
            sg.add("pz_cb", qk, _dq(sg, qk, 0.5), sg.chord_at(qk + 1e-3).bass_note(29, 41), 44, "bass", "h")
        sg.sync(f"{('黄金', '乳香', '没药')[kk]}: the {what} shines" + (" (picture)" if have else ""), qk, tk)
    lv(g, ["vc", "cb"], -19)
    lv(g, ["vla", "vln2", "vln1"], -19)
    # 'frankincense and myrrh are precious spices -- treasures for the king': the gift theme's climax
    r.mel("horn", bars(GIFT, 4, 7), vel=48, transpose=-12)
    r.mel("recorder", bars(GIFT, 4, 7), vel=42, role="counter")
    strings(r, vel=38, lo=55, hi=72)
    broken(r, "harp", 0, 9, (0, 2, 4, 2, 4, 2), 39, 51, vel=30, thin=True)
    r.pad("ooh", 3, 58, 74, vel=30, bass_ref=(41, 53))
    r.duck(3.0, parts=["horn", "recorder"])
    lv(r, ["horn"], -17)
    lv(r, ["recorder"], -19)
    lv(r, STR, -20)
    lv(r, ["harp"], -13)
    lv(r, ["ooh"], -22)
    t_fr = pic(c, "grow", "乳香和没药", lo=t_say - 0.2, hi=t_tre - 2.0)   # the fragrance rises (picture)
    if t_fr is not None:
        sg_, q_fr = seg_at(c, segs, t_fr)
        sweep(sg_, q_fr, 0.8, "Eb4", "Eb6", 26, 42)
    hit(c, segs, "chime", "乳香和没药", 0, "treasures for the king (a chime)", celesta=(79, 91), glock=(86, 98), vel=46)
    z.mel("horn", "Eb4:2", vel=46)
    z.mel("recorder", "Eb5:2", vel=42, role="counter")
    roll_chord(z, 0, 39, 70, vel=42)
    z.add("timp", 0, 0.5, "Eb3", 42, "timp", "h")
    z.add("pz_cb", 0, 1, "Eb2", 46, "bass", "h")
    glow(z, 0.0, vel=44)
    strings(z, vel=38, lo=55, hi=74)
    z.pad(["tbn", "horn", "horn"], 3, 46, 63, vel=36, bass_ref=(39, 51))
    lv(z, ["horn", "tbn"], -19)
    lv(z, ["recorder"], -20)
    lv(z, ["harp", "pz_cb", "timp"], -14)
    lv(z, STR, -20)
    for sg in segs:
        if sg is not s:
            lv(sg, ["glock", "bells", "pz_cb"], -12)
        if sg not in (s, j, k):
            lv(sg, ["celesta"], -12)


def end(c):
    """The living room again: the music-box waltz (E-flat, sleigh bells in the pauses); the question on '可是你知道吗'
    (Cm7 B-flat7sus4); the gift theme's climax on '耶稣，才是' (strings, the recorder and celesta, choir 'ooh', harp;
    sol mi'. re' | mi' la' | la' sol' fa' | mi' re' do' ti) and E-flat on '送给了我们'; the last question (A-flat add9,
    Gm7 Cm7, the celesta asks); B-flat7sus4 on the end of '你想送给耶稣什么礼物呢', hanging very softly through the
    pause; the final E-flat chord with the end card (the star motif on the celesta and music box, sleigh bells),
    ringing to the end."""
    c.gain(-2.5)
    t_know = c.at("可是你知道吗")
    t_jesus = c.at("耶稣，才是")
    t_gave = c.at("送给了我们")
    t_love = (t_jesus + t_gave) / 2                         # the climax's four bars at one tempo
    t_q = c.gap(c.find("你想送给耶稣什么礼物呢"))
    t_f = c.le(c.find("你想送给耶稣什么礼物呢"))
    t_raw = pic(c, "chime", "你想送给耶稣什么礼物呢")         # the end card (picture)
    t_card = t_raw if t_raw is not None and t_f + 0.5 <= t_raw <= c.dur - 0.6 else None
    t_fin = t_card if t_card is not None else max(t_f + 0.8, c.dur - 1.3)
    h = c.seg(0, t_know, 2, "3/4", "Eb major", nominal=82, label="end-home")
    q = c.seg(t_know, t_jesus, 1, "3/4", "Eb major", nominal=107, label="end-do-you-know")
    g = c.seg(t_jesus, t_love, 2, "3/4", "Eb major", nominal=90, label="end-gift")
    l = c.seg(t_love, t_gave, 2, "3/4", "Eb major", nominal=90, label="end-love")
    m = c.seg(t_gave, t_q, 1, "3/4", "Eb major", nominal=122, label="end-gave")
    p = c.seg(t_q, t_f, 2, "3/4", "Eb major", nominal=80, label="end-question")
    sp = c.seg(t_f, t_fin, 1, "2/4", "Eb major", nominal=None, label="end-space")
    f = c.seg(t_fin, c.dur, 1, "2/4", "Eb major", nominal=None, rit=0.3, label="end-final-chord")
    segs = (h, q, g, l, m, p, sp, f)
    for sg in (h, q, g, l, m, p):
        sg.duck(1.5)
    h.prog("Eb:3 | Ab:3")
    q.prog("Cm7:3/2 Bb7sus4:3/2")
    g.prog(" | ".join(GIFT_PROG[4:6]))
    l.prog("Ab:3 | Eb/Bb:1 Bb7:2")
    m.prog("Eb:3")
    p.prog("Abadd9:3 | Gm7:3/2 Cm7:3/2")
    sp.prog("Bb7sus4:2")
    f.prog("Eb:2")
    g.sync("'耶稣，才是': the gift theme (E-flat)", 0, t_jesus, kind="change")
    m.sync("'送给了我们': given to us (E-flat)", 0, t_gave, kind="change")
    sp.sync("'你想送给耶稣什么礼物呢': B-flat7sus4, the question hangs", 0, t_f, kind="change")
    f.sync("the final E-flat chord (the end card)", 0, t_fin, kind="change")
    f.sync("the end card: the final chord's harp roll" if t_card is not None else "the final chord: harp roll", 0,
           t_fin)
    # home: the music-box waltz
    waltz(h, 0, 6, vel=46)
    h.mel("mbox", "G6:1 F6:1/2 Eb6:1/2 Bb5:1 | C6:3", vel=48)
    h.pad(["vla", "vln2", "vln1"], 3, 57, 72, vel=34, bass_part="vc", bass_lo=39, bass_hi=51)
    jingle(h, 0.0, vel=32)
    h.duck(3.0, parts=["mbox"])
    lv(h, ["mbox"], -16)
    lv(h, ["pz_lo", "harp"], -11)
    lv(h, ["vla", "vln2", "vln1", "vc"], -19)
    hit(c, segs, "sparkle", None, 0, "the wise men's gift (a sparkle)", glock=(86, 98), vel=44)
    # 'but do you know?': the question
    q.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=46, bass_hi=58)
    q.add("harp", 0, 1.5, "C4", 30, "arp")
    q.add("harp", 1.5, 1.5, "Bb3", 30, "arp")
    q.add("celesta", 1.5, 1.5, "Eb6", 34, "arp")
    lv(q, ["vla", "vln2", "vln1", "vc"], -19)
    lv(q, ["harp"], -14)
    # 'Jesus is God's best gift to the whole world... God loves us, so he gave his Son': the theme's climax
    g.mel("recorder", bars(GIFT, 4, 6), vel=50)
    l.mel("recorder", "C6:1 Bb5:1 Ab5:1 | G5:1 F5:1/2 Eb5:1/2 D5:1", vel=48)
    m.mel("recorder", "Eb5:3", vel=48)
    m.mel("celesta", "Eb6:3", vel=36, role="counter")
    for sg in (g, l, m):
        strings(sg, vel=38, lo=55, hi=72)
        broken(sg, "harp", 0, sg.n_q, (0, 2, 4, 2, 4, 2), 39, 51, vel=30, thin=True)
        sg.pad("ooh", 3, 58, 74, vel=30, bass_ref=(41, 53))
        sg.duck(3.5, parts=["recorder", "celesta"])
        lv(sg, ["recorder"], -18)
        lv(sg, ["celesta"], -17)
        lv(sg, STR, -20)
        lv(sg, ["harp"], -13)
        lv(sg, ["ooh"], -22)
    glow(m, 0.0, vel=44)
    hit(c, segs, "sparkle", "耶稣，才是", 1, "Jesus, the gift (a sparkle)", glock=(86, 98), vel=44)
    hit(c, segs, "chime", "耶稣，才是", 0, "the best gift of all (a chime)", celesta=(79, 91), glock=(86, 98), vel=46)
    hit(c, segs, "sparkle", "上帝爱我们", 0, "God loves us (a sparkle)", glock=(88, 100), vel=44)
    # 'this Christmas, what gift would you like to give Jesus?': very soft; the celesta asks
    p.mel("celesta", "Bb5:1 C6:1 Eb6:1 | D6:3/2 Eb6:3/2", vel=38, role="arp")
    p.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=32, bass_part="vc", bass_lo=43, bass_hi=55)
    bassline(p, "cb", 31, 43, 30)
    p.add("harp", 0, 3, "Ab3", 32, "arp")
    p.add("harp", 3, 1.5, "G3", 32, "arp")
    p.add("harp", 4.5, 1.5, "C3", 32, "arp")
    lv(p, ["celesta"], -14)
    lv(p, ["vla", "vln2", "vln1", "vc", "cb"], -19, -20)
    lv(p, ["harp"], -13)
    hit(c, segs, "pop", "今年圣诞节", 0, "a little gift for Jesus (a pop)", pluck=(62, 74), celesta=(79, 91), vel=44)
    # the space after the question: B-flat7sus4 hanging, very soft
    sp.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=32, bass_part="vc", bass_lo=46, bass_hi=58)
    sp.add("cb", 0, 2, "Bb1", 30, "bass")
    sp.add("harp", 0, 2, "Bb2", 36, "arp", "h")
    sp.add("harp", 0.06, 1.94, "F3", 32, "arp")
    sp.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -20), (1, -21), (2, -22)])
    lv(sp, ["harp"], -13, -14)
    # the final E-flat chord: harp rolled up, the star motif on the celesta and music box, sleigh bells, strings, ooh
    for k_, nm in enumerate(["Eb2", "Bb2", "Eb3", "G3", "Bb3", "Eb4", "G4", "Bb4", "Eb5"]):
        f.add("harp", 0.06 * k_, 2 - 0.06 * k_, nm, 46 - 2 * k_, "arp", "r")
    f.mel("celesta", "Bb5:1/2 G6:3/2", vel=38, art="r", role="arp")
    f.mel("mbox", "Bb6:1/2 G6:3/2", vel=40, art="r", role="arp")
    strings(f, vel=38, lo=55, hi=72, q0=0.25)
    f.pad("ooh", 3, 58, 74, vel=34, q0=0.25, bass_ref=(41, 53))
    jingle(f, 0.5, vel=30, force=True)
    f.expr(["vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -19), (0.5, -18.5), (1.4, -21), (2, -28)])
    f.expr(["harp", "celesta", "mbox", "glock"], [(0, -15), (2, -19)])
    lv(f, "hand", -18)
    if t_card is not None:
        f.add("glock", 0, f.n_q, "Bb6", 40, "arp", "r")
    elif t_raw is not None:                                 # the end card earlier than the space allows: its own glint
        accent(c, segs, t_raw, "the end card (a chime)", celesta=(79, 91), glock=(86, 98), vel=44)
    for sg in (h, q, g, l, m, p, sp):
        lv(sg, "hand", -16)
        if sg in (h, q, sp):
            lv(sg, ["glock", "celesta"], -12)


SCENE_CUES = {
    "s01_title": title, "s02_question": question, "s03_angel": angel, "s04_journey": journey,
    "s05_no_room": noroom, "s06_birth": birth, "s07_shepherds": shepherds, "s08_choir": choir, "s09_visit": visit,
    "s10_star": star, "s11_gifts": gifts, "s12_end": end,
}

# Hit points defined by the narration text (audio/music_check.py REQUIRED_HITS format: (scene, phrase, mode, kind)).
# Where a word is also an on-screen action (the light, the angels, the star) the phrase is where the harmony arrives
# ('change') and the attack follows the picture (PICTURE_HITS).
REQUIRED_HITS = [
    ("s02_question", "圣诞节", "line", "change"),            # Christmas: the gift theme (E-flat)
    ("s03_angel", "忽然亮起来了", "phrase", "change"),        # the light (C major)
    ("s03_angel", "没有做不到的事", "phrase", "change"),      # nothing is impossible (C)
    ("s03_angel", "我愿意", "phrase", "change"),              # Mary says yes (A-flat)
    ("s04_journey", "那时候", "phrase", "change"),            # the Roman emperor (B-flat)
    ("s04_journey", "伯利恒", "phrase", "change"),            # Bethlehem (E-flat)
    ("s04_journey", "小宝宝", "phrase", "change"),            # the lullaby's head
    ("s05_no_room", "客店里", "gap", "change"),               # no room (G minor)
    ("s05_no_room", "他们只好", "gap", "change"),             # a humble warm place (E-flat)
    ("s06_birth", "出生了", "phrase", "change"),              # Jesus is born (E-flat)
    ("s06_birth", "小耶稣睡着了", "line", "change"),          # asleep (E-flat)
    ("s07_shepherds", "忽然", "line", "change"),              # the angel (A7sus4; the attack: picture)
    ("s07_shepherds", "上帝的光", "phrase", "change"),        # the glory (D major)
    ("s07_shepherds", "今天，在伯利恒", "gap", "change"),     # a Saviour is born (D)
    ("s08_choir", "忽然", "line", "change"),                  # the heavenly host (B minor; the attack: picture)
    ("s08_choir", "在至高之处", "gap", "change"),             # the Gloria (D major)
    ("s08_choir", "在地上", "phrase", "change"),              # peace on earth (G)
    ("s08_choir", "地上，上帝要把平安", "phrase", "change"),  # on earth (G)
    ("s09_visit", "牧羊人你看看我", "phrase", "change"),      # back on earth (B-flat)
    ("s09_visit", "他们急急忙忙", "gap", "change"),           # the shepherds run
    ("s09_visit", "找到了", "phrase", "change"),              # found (E-flat)
    ("s09_visit", "他就是天使说的救主", "gap", "change"),     # the Saviour (E-flat)
    ("s09_visit", "牧羊人好开心", "gap", "change"),           # they tell everyone (B-flat)
    ("s09_visit", "马利亚呢", "phrase", "change"),            # Mary ponders (E-flat)
    ("s10_star", "一颗特别的星星", "phrase", "change"),       # the star (E-flat lydian; its motif: picture)
    ("s10_star", "他们出发了", "gap", "change"),              # the caravan (C dorian)
    ("s11_gifts", "忽然", "line", "change"),                  # the star again (E-flat)
    ("s11_gifts", "停在了", "phrase", "change"),              # the star stops (A-flat)
    ("s11_gifts", "博士们高兴极了", "gap", "change"),         # joy (E-flat)
    ("s11_gifts", "乳香", "phrase", "change"),                # frankincense (A-flat/E-flat)
    ("s11_gifts", "宝贝", "phrase", "change"),                # the treasures for the king (E-flat)
    ("s12_end", "耶稣，才是", "phrase", "change"),            # the gift theme (E-flat)
    ("s12_end", "送给了我们", "phrase", "change"),            # given to us (E-flat)
    ("s12_end", "你想送给耶稣什么礼物呢", "end", "change"),   # B-flat7sus4: the question hangs
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or None,
# index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.
PICTURE_HITS = [
    ("s01_title", "chime", None, 0, 0.0, "hit", "the title appears (a glint)"),
    ("s01_title", "pop", "圣经绘本", 0, 0.0, "hit", "title character 1 pops in"),
    ("s01_title", "pop", "圣经绘本", 3, 0.0, "hit", "title character 4 pops in"),
    ("s01_title", "sparkle", None, 0, 0.0, "hit", "the title sparkles"),
    ("s02_question", "pop", None, 0, 0.0, "hit", "an ornament is hung (a ping)"),
    ("s02_question", "sparkle", None, 0, 0.0, "hit", "the child cheers (a sparkle)"),
    ("s02_question", "sparkle", "圣诞节", 0, 0.0, "hit", "'圣诞节' (a sparkle)"),
    ("s02_question", "chime", "圣诞节", 0, 0.0, "hit", "the tree lights up (a chime)"),
    ("s02_question", "sparkle", "圣诞节", 2, 0.0, "hit", "a birthday for Jesus (a sparkle)"),
    ("s02_question", "sparkle", "圣诞节", 3, 0.0, "hit", "how Jesus was born (a sparkle)"),
    ("s03_angel", "chime", "有一天", 0, 0.0, "hit", "the room fills with light ('忽然亮起来了')"),
    ("s03_angel", "sparkle", "有一天", 0, 0.0, "hit", "the angel shines ('一位天使')"),
    ("s03_angel", "cloth", "有一天", 1, 0.0, "hit", "Mary jumps ('吓了一跳')"),
    ("s03_angel", "sparkle", "马利亚，不要怕", 0, 0.0, "hit", "the name Jesus sparkles"),
    ("s03_angel", "chime", "这是上帝要做的事", 0, 0.0, "hit", "the angel's blessing (a chime)"),
    ("s03_angel", "sparkle", "我是上帝的使女", 0, 0.0, "hit", "Mary's yes (a sparkle)"),
    ("s04_journey", "pop", None, 0, 0.0, "hit", "Joseph pops up"),
    ("s04_journey", "pop", None, 1, 0.0, "hit", "Mary pops up"),
    ("s04_journey", "chime", None, 0, 0.0, "hit", "the emperor appears (a glint)"),
    ("s04_journey", "pop", None, 2, 0.0, "hit", "the first head is counted"),
    ("s04_journey", "sparkle", "他下了一道命令", 0, 0.0, "hit", "the scroll sparkles"),
    ("s04_journey", "pop", "约瑟的老家", 0, 0.0, "hit", "Bethlehem on the map"),
    ("s04_journey", "pop", "约瑟的老家", 1, 0.0, "hit", "the first dot on the road"),
    ("s04_journey", "pop", "约瑟的老家", 7, 0.0, "hit", "the last dot on the road"),
    ("s04_journey", "sparkle", "约瑟的老家", 0, 0.0, "hit", "the road is drawn (a sparkle)"),
    ("s04_journey", "sparkle", "这时候", 0, 0.0, "hit", "the baby's heart (a sparkle, '小宝宝')"),
    ("s05_no_room", "pop", None, 0, 0.0, "hit", "squeezed in the crowd (a pop)"),
    ("s05_no_room", "hammer", None, 0, 0.0, "hit", "a knock at the inn door"),
    ("s05_no_room", "sparkle", "他们只好", 0, 0.0, "hit", "a lamp is lit in the stable (a sparkle)"),
    ("s06_birth", "chime", None, 0, 0.0, "hit", "the baby glows ('出生了')"),
    ("s06_birth", "sparkle", "马利亚用布", 0, 0.0, "hit", "the baby is laid in the manger"),
    ("s06_birth", "crunch", None, 0, 0.0, "hit", "the ox munches (a guiro, a bassoon)"),
    ("s06_birth", "sparkle", "小耶稣睡着了", 0, 0.0, "hit", "asleep (a glint)"),
    ("s06_birth", "sparkle", "小耶稣睡着了", 1, 0.0, "hit", "a star twinkles (1)"),
    ("s06_birth", "sparkle", "小耶稣睡着了", 2, 0.0, "hit", "a star twinkles (2)"),
    ("s07_shepherds", "chime", "忽然", 0, 0.0, "hit", "the angel appears ('忽然')"),
    ("s07_shepherds", "sparkle", "不要怕", 0, 0.0, "hit", "good news for all (a sparkle)"),
    ("s07_shepherds", "chime", "今天，在伯利恒", 0, 0.0, "hit", "the Saviour (a chime)"),
    ("s07_shepherds", "sparkle", "你们会看见", 0, 0.0, "hit", "wrapped in cloths (a sparkle)"),
    ("s08_choir", "chime", None, 0, 0.0, "hit", "the heavenly host appears ('忽然')"),
    ("s08_choir", "sparkle", None, 0, 0.0, "hit", "another angel appears (1)"),
    ("s08_choir", "sparkle", None, 1, 0.0, "hit", "another angel appears (2)"),
    ("s08_choir", "sparkle", None, 2, 0.0, "hit", "another angel appears (3)"),
    ("s08_choir", "sparkle", "在至高之处", 0, 0.0, "hit", "glory (a glint)"),
    ("s08_choir", "chime", "在至高之处", 0, 0.0, "hit", "peace (a chime)"),
    ("s08_choir", "sparkle", "就是说", 0, 0.0, "hit", "heaven (a sparkle)"),
    ("s08_choir", "chime", "就是说", 0, 0.0, "hit", "peace on earth (a chime)"),
    ("s09_visit", "chime", None, 0, 0.0, "hit", "the angels go back to heaven (a chime)"),
    ("s09_visit", "sparkle", "他们急急忙忙", 0, 0.0, "hit", "found ('找到了', a sparkle)"),
    ("s09_visit", "chime", "他就是天使说的救主", 0, 0.0, "hit", "the Saviour (a chime)"),
    ("s09_visit", "sparkle", "他就是天使说的救主", 0, 0.0, "hit", "sent by God (a sparkle)"),
    ("s09_visit", "pop", "听见的人", 0, 0.0, "hit", "everyone is amazed (a pop)"),
    ("s09_visit", "chime", "听见的人", 0, 0.0, "hit", "kept in her heart (a chime)"),
    ("s10_star", "sparkle", None, 0, 0.0, "hit", "a star sparkles over the wise men"),
    ("s10_star", "chime", "有一天", 0, 0.0, "hit", "the star shines ('一颗特别的星星')"),
    ("s10_star", "sparkle", "这颗星星告诉我们", 0, 0.0, "hit", "a king is born (a glint)"),
    ("s10_star", "thud", "他们出发了", 0, 0.0, "hit", "a camel's first step"),
    ("s10_star", "thud", "他们出发了", 4, 0.0, "hit", "a camel's fifth step"),
    ("s11_gifts", "chime", None, 0, 0.0, "hit", "the star appears again ('忽然')"),
    ("s11_gifts", "sparkle", "星星一直走到伯利恒", 0, 0.0, "hit", "the star stops ('停在了', a bell)"),
    ("s11_gifts", "chime", "博士们高兴极了", 0, 0.0, "hit", "the wise men rejoice (a chime)"),
    ("s11_gifts", "cloth", "他们打开宝盒", 0, 0.0, "hit", "the treasure boxes open"),
    ("s11_gifts", "sparkle", "他们打开宝盒", 0, 0.0, "hit", "黄金: the gold shines (glockenspiel)"),
    ("s11_gifts", "sparkle", "他们打开宝盒", 1, 0.0, "hit", "乳香: the frankincense shines (celesta, harp)"),
    ("s11_gifts", "sparkle", "他们打开宝盒", 2, 0.0, "hit", "没药: the myrrh shines (a tubular bell)"),
    ("s11_gifts", "chime", "乳香和没药", 0, 0.0, "hit", "treasures for the king (a chime)"),
    ("s12_end", "sparkle", None, 0, 0.0, "hit", "the wise men's gift (a sparkle)"),
    ("s12_end", "sparkle", "耶稣，才是", 1, 0.0, "hit", "Jesus, the gift (a sparkle)"),
    ("s12_end", "chime", "耶稣，才是", 0, 0.0, "hit", "the best gift of all (a chime)"),
    ("s12_end", "sparkle", "上帝爱我们", 0, 0.0, "hit", "God loves us (a sparkle)"),
    ("s12_end", "pop", "今年圣诞节", 0, 0.0, "hit", "a little gift for Jesus (a pop)"),
    ("s12_end", "chime", "你想送给耶稣什么礼物呢", 0, 0.0, "hit", "the end card: the final E-flat chord"),
]
