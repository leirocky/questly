"""The background score for 耶稣平静风浪 (Mark 4:35-41 with its setting, ~3:45) -- one continuous piece in 15 cues.

Read by audio/score.py when the story is "storm" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework and orchestra as the Jonah, Daniel, David, Noah and
Joseph scores (audio/scorekit.py, audio/scorelib.py): every cue starts at its scene's global start, is planned in
whole bars whose tempo follows the real line timings, and is keyed to narration phrases (Cue.find / Cue.at /
Cue.gap), never to fixed times.  Hits that show an on-screen action follow the PICTURE where the scene declares a
sound-effect cue for it: picture() reads the scene's own sfx cues at build time (engine.loader.build_scene(...)
.sfx_cues, the same source as music_check's PICTURE_HITS), so they move when a scene is edited; the narration phrase
then marks where the harmony arrives (a 'change' in REQUIRED_HITS).  pic() picks a scene's sfx cue exactly as
music_check picks a PICTURE_HITS target, and accent() puts the attack wherever that cue falls in the cue, on tones of
the chord sounding there; the picture moves a segment boundary only where that keeps the plan sound (else the
boundary stays on the narration and the picture gets its own accent).  Spoken sound words are found on the narrator's
own voice: syl() aligns the recorded line's voice islands to the text (punctuation groups; the dashes of 呼—— count as
punctuation) by a monotone least-squares match, with the subtitle-chunk interpolation as the fallback.  The scenes
put 哗 on the voice (their splashes) while the subtitle interpolation of '哗啦！哗啦！' falls on 啦: the splash follows
the picture, the narration phrase gets the spray; the first 呼 sits half-way between the picture's whoosh and the
spoken 呼 (two frames apart).

Colour: a Galilean folk feel, unlike the five earlier films -- modal major (G mixolydian, D mixolydian: the flat
seventh, I-bVII-IV-I), an oud-like plucked line (the nylon guitar doubling the wooden flute an octave below, in
heterophony), harp, a soft frame drum; the storm in G minor with rolling strings, low brass and timpani; the calm in
G major and the warm E-flat of Jesus's presence (bVI) when he wakes and when the moon comes out.  Wonder and questions
sit on open add9 / sus colours (Cadd9, Ebadd9, Fadd9, D7sus4, A7sus4), never a semitone inside a voicing.

Themes
  Jesus (G mixolydian, 3/4; flute with the guitar an octave below, over harp; motif x = the rising triad B D G):
     b1 G   B4 D5 G5           b5 G   B4 D5 G5
     b2 F   A5. G5 F5          b6 Em  B5. A5 G5
     b3 C   E5 G5 C5           b7 F   F5 G5 A5
     b4 G   D5--               b8 G   G5--      (b7 rises F G A: the bass moves F -> G against it)
     gentle in the title, on the shore, in the gentle question (s12) and the ending; in D, bright and full, at dawn
     (s14); his motif in E-flat on the horn when he wakes (s11) and in G when the disciples understand (s13).
  The fishermen's barcarolle (D mixolydian, 6/8: the rowing rhythm -- plucked basses on the dotted-quarter beats, a
     frame drum DUM . ka DUM . ka, the guitar rocking; clarinet over a D drone: D | G/D | C/D | D):
     F#4 A4. D5 A4. | B4 G4. B4 D5. | E5 D5. C5 E5. | D5-- A4--   (b5-b8: F#4 A4 D5 F#5 | G5 F#5 E5 D5 | E5 G5 E5 C5 |
     D5); in G when the boat sets out in the evening (s07); frantic, in G minor, in the panic (s09).
  The mustard seed (C major, 3/4, a music box over a pizzicato waltz): F, tiny and high, on '最小最小的种子', a pling on
     each sparkle of the seed; then each 长 a step up -- 长 Dm7, 长 Em7, 长得 F, 所有的菜 G, 都大 C (music box D6 E6 F6
     G6 C7 over a climbing bass, on the picture's growth); C on '做窝', the birds' flute trill as they land.
  The lullaby (G major, 6/8; celesta and harp, then the flute): D5 B4. D5 B4. | E5 G5. E5 C5. | E5 D5. C5 A4. |
     B4 A4. A4-- (G C Am7 D) ... | D5 C5. A4 F#4. | G4 (D7 G); a tiny warm island of it inside the storm (s10).
  The storm (G minor): a single gust on '忽然', a gust on each 呼, rolling cellos, tremolo, low brass and timpani, a
     timpani stroke and a soft cymbal on each wave, a splash on each 哗 (bass drum, timpani, cymbal, a harp sweep down)
     and a spray on 啦; the water rising (G A Bb C D); big but warm -- no clusters, no stingers.

Tonal plan
  s01 title G (Jesus b1-b2, flute + guitar; a glint as the title appears, a celesta note for each character of the
  title as it pops in, a far-off timpani roll on F with the clouds' thunder) -> s02 E minor night (harp, a gust on
  '很大很大的风', a gust on 呼呼, two knocks as the window rattles: Am B7), the question (C Am7), G 6/8 on '今天的故事里'
  (the boat; a chime as the book opens), E minor on '遇到了好大好大的风浪' (rolling cellos, two splashes) -> s03 D:
  morning | G on '十二个好朋友' (Jesus b1-b2, twelve harp notes rising, one per friend as each pops up) | D mixolydian
  barcarolle on '他们当中' (a pluck for 彼得、安得烈、雅各、约翰 as each pops up, a harp sweep for the net and a pluck as it
  lands) | b5-b8, the fish spots on the map, a little gust with the wind sign, D -> s04 G: Jesus b1-b4 (the crowd:
  choir 'ooh') | b7-b8 F G (Jesus steps into the boat) | Cadd9 G hush on '大家都安安静静地听' (a celesta peeks: the
  children) -> s05 C music box | F, tiny | the seed planted (C, low) | 长啊长 Dm7 Em7 F G C | F, C on '做窝' (the
  birds) | F G7 C, a smile -> s06 C sunset hymn (C G/B Am7 F: horns and strings) | G on '我们渡到湖的那一边去吧'
  (Jesus b1, C D; the boat pushed off) -> s07 G barcarolle (the boat sets out) | Em Am7 D (tired; he lies down) | the
  lullaby on '睡着了' | 摇啊摇 (G C D7, flute; the boat creaks) | Em7 Cadd9 stars on '星星一颗一颗地亮起来了' (a celesta
  note for each star) -> s08 G minor storm: a gust on '忽然' | 呼 呼 (two gusts) | rolling Gm Eb Cm D | waves, one by
  one | splashes on 哗 哗, the water rising (Gm F/A Gm/Bb Cm D) -> s09 G minor panic (staccato ostinato, the barcarolle
  frantic on the clarinet; a glint of the calm fishing days that pops; two big waves; a swell in the pause) | the stab
  on '抓紧' (Gm), bailing (Cm D; a scoop on each splash) | the water rising (Gm Ab F/A Gm/Bb G/B Cm) | rocking and
  sinking (Cm Gm/Bb Ab D, 6/8; the boat dips) -> s10 D | the lullaby island in G on '可是，耶稣还在睡觉' (his warm glow)
  | the storm returns (Gm Eb Cm D ... Am7b5; they shake him, a wave) | D7 held on '你不管吗' -> s11 D7 | E-flat on
  '耶稣醒了' (his motif on the horn; he stands up), Cm | Ab Am7b5, the last surge (he raises his hand), falling back for
  a breath | D on '住了吧' (the storm stops dead) | G on '静了吧' (stillness: G Cadd9/G G) | E-flat radiant on
  '月亮出来了' (high strings, choir 'ooh', the moon's chime, celesta stars) -> s12 G: Jesus b1-b2 soft (he turns to
  them) | C Am7 D7sus4 (his question) -> s13 Cadd9 Am7 D7sus4 (wonder) | Ebadd9 on '这到底是谁' (open) | Fadd9 C/E |
  Am7 D7sus4 D7 | G on '耶稣不只是他们的好老师' (his motif on the horn; he glows) -> s14 D barcarolle at dawn (the boat
  reaches the shore) | the theme in D, bright and full, on '太阳出来了' (the sunrise chime, the water sparkles) | b3-b4,
  then Bm7 Gadd9 A7sus4 ('到底是谁呢？', question marks) -> s15 Em7 Cadd9 Am7 (the question, space in the pause) | G on
  '他就是耶稣' (Jesus b1-b4) | b5-b8 warm (clarinet, horn, strings, choir; she folds her hands) | Cadd9 Em7 (the last
  question) | D7sus4 on the end of '想对耶稣说什么呢', hanging very softly through the pause | the final G major chord
  with the end card, ringing to the end.

All the music stays under the narration (Seg.duck, low expression levels); the storm's weight lives in the pauses and
in the hits; its loud moments are short and child-safe; Jesus's words get only soft sustained chords (the two
arrivals under '住了吧！静了吧！' are ducked, the storm falling back just before them).
"""
import numpy as np

from audio.scorelib import (
    ChordTones,
    bassline,
    broken,
    drum,
    gliss,
    roll,
    span_end,
    timp_pitch,
)
from audio.theory import midi

# ------------------------------------------------------------------------------------------- themes
JESUS = ["B4:1 D5:1 G5:1", "A5:3/2 G5:1/2 F5:1", "E5:1 G5:1 C5:1", "D5:3",
         "B4:1 D5:1 G5:1", "B5:3/2 A5:1/2 G5:1", "F5:1 G5:1 A5:1", "G5:3"]
JESUS_PROG = ["G:3", "F:3", "C:3", "G:3", "G:3", "Em:3", "F:3", "G:3"]

BOAT = ["F#4:1 A4:1/2 D5:1 A4:1/2", "B4:1 G4:1/2 B4:1 D5:1/2", "E5:1 D5:1/2 C5:1 E5:1/2", "D5:3/2 A4:3/2",
        "F#4:1 A4:1/2 D5:1 F#5:1/2", "G5:1 F#5:1/2 E5:1 D5:1/2", "E5:1 G5:1/2 E5:1 C5:1/2", "D5:3"]
BOAT_PROG = ["D:3", "G/D:3", "C/D:3", "D:3", "D:3", "G/D:3", "C/D:3", "D:3"]

LULL = ["D5:1 B4:1/2 D5:1 B4:1/2", "E5:1 G5:1/2 E5:1 C5:1/2", "E5:1 D5:1/2 C5:1 A4:1/2", "B4:1 A4:1/2 A4:3/2",
        "D5:1 B4:1/2 D5:1 G5:1/2", "G5:1 E5:1/2 C5:1 E5:1/2", "D5:1 C5:1/2 A4:1 F#4:1/2", "G4:3"]
LULL_PROG = ["G:3", "C:3", "Am7:3", "D:3", "G:3", "C:3", "D7:3", "G:3"]

MBOX = ["E6:1 D6:1/2 E6:1/2 G6:1", "F6:1 D6:1 B5:1", "C6:1 E6:1 G6:1", "C6:3"]
MBOX_PROG = ["C:3", "G7:3", "C:3", "C:3"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…—"          # the dashes of 呼—— separate the spoken sound syllables
SOUND_CHARS = set()                # no sound word here is spoken syllable by syllable inside one group
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
    """The groups of an utterance (sound words split into their syllables)."""
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


def char_at(c, phrase, k):
    """Cue-relative time of the k-th character of `phrase` in the narration (Cue.at's interpolation)."""
    i = c.find(phrase)
    ln = c.scene["lines"][i]
    return _char_time(ln, ln["text"].index(phrase) + k)


def _onsets(wav):
    """(onsets s into the clip of its voice islands -- runs of 10 ms frames within 32 dB of the loudest, at least
    40 ms long --, clip length s), or None if the clip cannot be read."""
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
    """Monotone assignment of every expected time u[i] to a distinct island onset v[j] (both sorted) with the
    least sum of squared distances (len(v) >= len(u))."""
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
    """Cue-relative onsets of the n narration units (punctuation groups) that start where `phrase` starts, as the
    narrator actually speaks them: the recorded clip's voice islands matched to the text in order (least squares
    against the subtitle-chunk interpolation); a unit whose match is more than 0.5 s off, or a clip that is missing
    or has too few islands, keeps the interpolation."""
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


_PICTURE = {}


def _forget_voice_marks(sid):
    """The storm scenes time their actions with a shared scene helper (stories/noah/scenes/s01_title.voice_marks)
    whose cache keys each line's voice marks by (scene id, line index) only, not by the timeline: in one process a
    re-timed timeline (audio/test_score.py) would get the marks of the first one.  Forget this scene's marks (the
    timeline-independent clip analyses, keyed by path, stay) so the scene is built for the timeline being scored."""
    import sys
    for name, mod in list(sys.modules.items()):
        cache = getattr(mod, "_SEG_CACHE", None) if name.startswith("stories.") else None
        if isinstance(cache, dict):
            for key in [k for k in cache if isinstance(k, tuple) and k and k[0] == sid]:
                del cache[key]


def picture(c, name, t0=-1e9, t1=1e9):
    """Cue-relative times of this scene's own sound-effect cues called `name` between t0 and t1.  The scene
    authors key them to the animation, so a hit that shows an action follows the PICTURE: read at build time
    from the scene code, as music_check reads PICTURE_HITS.  None when the scene does not build (the caller then
    falls back to the narration)."""
    tl = c.score.tl
    key = (round(c.t0, 4), tuple(c.lines), id(tl), float(tl["duration"]))
    if c.id not in _PICTURE or _PICTURE[c.id][0] != key:      # a new timeline: build the scene for it
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
    """The k-th picture cue `name` from the start of the line containing `phrase` (minus 0.3 s; phrase None: from the
    scene start) plus off -- chosen exactly as music_check.picture_targets chooses a PICTURE_HITS target -- or None
    when the scene does not build, has no such cue, or the cue lies outside [lo, hi] (default: inside this cue,
    just inside its end)."""
    t0 = c.ls(c.find(phrase)) - 0.3 if phrase else -1e9
    ts = picture(c, name, t0)
    if not ts or k >= len(ts):
        return None
    t = ts[k] + off
    lo = 0.02 if lo is None else lo
    hi = c.dur - 0.02 if hi is None else hi
    return t if lo <= t <= hi else None


def near(c, name, t, tol=0.5):
    """The picture cue `name` nearest to cue-relative time t if one lies within tol s of it, else t."""
    ts = picture(c, name, t - tol, t + tol)
    return min(ts, key=lambda x: abs(x - t)) if ts else t


def accent(c, segs, t, what=None, glock=None, celesta=None, harp=None, pluck=None, guitar=None, low=None, vel=46):
    """A picture hit at cue-relative time t, in whichever of segs it falls: chord tones of the chord sounding there --
    glock / celesta / harp / pluck / guitar = (lo, hi) ranges for a glockenspiel, celesta, harp, pizzicato or guitar
    note (the highest chord tone in range), low=True a soft thump (timpani, plucked basses, bass drum).  Synced as a
    hit when `what` is given.  Returns (segment, q)."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if celesta:
        sg.add("celesta", q, _dq(sg, q, 1.0), top(sg, q, *celesta), vel - 6, "arp", "h")
    if harp:
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, *harp), vel, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if guitar:
        sg.add("guitar", q, _dq(sg, q, 0.5), top(sg, q, *guitar), vel + 4, "arp", "h")
    if low:
        thump(sg, q, vel=vel + 2)
    if what:
        sg.sync(what, q, t)
    return sg, q


def seg_at(c, segs, t):
    """(segment, q) of cue-relative time t among segs (a hit that lands in a neighbouring segment takes its chord)."""
    for sg in segs:
        if sg.t0 - 1e-6 <= c.t0 + t < sg.t1 - 1e-6:
            q = min(max(sg.q_of(c.t0 + t), 0.0), sg.n_q - 1e-3)
            se = span_end(sg, q + 1e-6)
            if se - q < 0.01 and se < sg.n_q - 1e-3:         # a hair before a chord change: on the new chord
                q = se
            return sg, q
    sg = segs[0] if c.t0 + t < segs[0].t0 else segs[-1]
    return sg, (0.0 if sg is segs[0] and c.t0 + t < sg.t0 else sg.n_q - 0.1)


def qpos(seg, c, t, lo=0.0, hi=None):
    """q of cue-relative time t in seg, clamped to [lo, hi] (hi default: just before the segment end)."""
    hi = seg.n_q - 0.1 if hi is None else hi
    return min(max(seg.q_of(c.t0 + t), lo), hi)


def edges48(seg, c, times, min_gap=6):
    """Chord edges (in 48ths of a quarter) at the given cue-relative times inside seg: [0, ..., n_q*48], each at
    least min_gap 48ths after the previous one (and before the end)."""
    end = int(round(seg.n_q * 48))
    out = [0]
    for t in times:
        e = int(round(seg.q_of(c.t0 + t) * 48))
        out.append(max(e, out[-1] + min_gap))
    out.append(end)
    for k in range(len(out) - 2, 0, -1):                 # squeeze back from the end if needed
        out[k] = min(out[k], out[k + 1] - min_gap)
    return out


def prog48(seg, chords, edges):
    seg.prog(" ".join(f"{ch}:{edges[k + 1] - edges[k]}/48" for k, ch in enumerate(chords)))


# ------------------------------------------------------------------------------------------- helpers
STR = ["vla", "vln2", "vln1", "vc", "cb"]
TREM = ["trem_va", "trem_hi", "trem_lo"]


def strings(seg, vel=44, lo=53, hi=72, bass=(41, 53), q0=0.0, q1=None, cb=(29, 41), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vln2", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
            bass_hi=bass[1])
    if cb:
        bassline(seg, "cb", cb[0], cb[1], cb_vel or vel - 2, q0=q0, q1=q1)


def _dq(seg, q, dq):
    """dq, shortened so the note ends with its chord."""
    return max(0.1, min(dq, span_end(seg, q + 1e-6) - q, seg.n_q - q))


def top(seg, q, lo, hi, k=-1):
    """A chord tone of the chord at q in [lo, hi] (k=-1: the highest)."""
    ts = seg.chord_at(q + 1e-3).tones(lo, hi)
    return ts[max(-len(ts), min(k, len(ts) - 1))]


def pluck_chord(seg, q, vel=60, lo=55, hi=67, part="pz_hi", n=3):
    """A short plucked chord (an accent: chord tones, not a voice-led part)."""
    ch = seg.chord_at(q + 1e-3)
    for k, p in enumerate(ch.tones(lo, hi)[:n]):
        seg.add(part, q, _dq(seg, q, 0.5), p, vel, "arp", "h", voice=f"{part}.{k}")


def thump(seg, q, vel=50, kit=True):
    """A soft low accent (timpani, plucked basses, a bass drum) on tones common to the chord there and the chord a
    little later (each note ends with its chord)."""
    pcs = seg.chord_at(q + 0.02).pcset & seg.chord_at(min(q + 0.4, seg.n_q - 1e-3)).pcset or \
        seg.chord_at(q + 0.02).pcset
    seg.add("timp", q, _dq(seg, q + 0.02, 0.5), [p for p in range(38, 51) if p % 12 in pcs][0], vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q + 0.02, 0.4), [p for p in range(29, 41) if p % 12 in pcs][0], vel + 2, "bass", "h")
    if kit:
        seg.add("okit", q, 1, 36, vel - 8, "perc", "h")


def gliss_in(seg, part, q, dur_s, lo, hi, **kw):
    """A harp glissando that stays inside its segment (shortened to the room left; none if under 0.12 s)."""
    room = seg.t(seg.n_q) - seg.t(q) - 0.03
    if room >= 0.12:
        gliss(seg, part, q, min(dur_s, room), lo, hi, **kw)


def harp_roll(seg, q, names, vel=46, gap_s=0.06, art=""):
    """A harp chord rolled up from the bottom (one note every gap_s seconds), each held to the chord's end."""
    t0 = seg.t(q)
    for k, nm in enumerate(names):
        qk = seg.q_of(t0 + gap_s * k)
        if qk >= span_end(seg, q + 1e-6) - 0.05:
            break
        seg.add("harp", qk, span_end(seg, q + 1e-6) - qk, nm, vel - 2 * k, "arp", art)


def troll(seg, q0, q1, pitch, v0, v1, rate=13.0):
    """A timpani roll (as scorelib.timp_roll) whose strokes never ring over a chord change: each stroke is tuned to the
    chord at its onset (its bass if possible) and clipped at that chord's end."""
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


def theme(seg, a, b, q=0.0, vel=58, transpose=0, part="flute", oud=True, oud_vel=None):
    """Bars a..b of Jesus's theme on `part`, the guitar an octave below (the oud-like heterophony)."""
    seg.mel(part, bars(JESUS, a, b), q=q, vel=vel, transpose=transpose)
    if oud:
        seg.mel("guitar", bars(JESUS, a, b), q=q, vel=oud_vel or vel - 8, transpose=transpose - 12, role="counter")


def guitar(seg, q0, q1, pat=(0, 2, 3, 4, 3, 2), lo=43, hi=55, vel=42, step=0.5, thin=True):
    """The guitar rocking under a tune: broken chord tones from the bass (ringing until the chord changes)."""
    broken(seg, "guitar", q0, q1, pat, lo, hi, vel=vel, step=step, accent=6, thin=thin, top=84)


def oars(seg, q0, q1, vel=50, lo=38, hi=50, part="pz_lo"):
    """The oars: a plucked bass on every dotted-quarter beat of 6/8 (the chord's bass, its upper octave on the second
    beat of the bar)."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        b = ch.bass_note(lo, hi)
        p = b + 12 if k % 2 else b
        seg.add(part, q, _dq(seg, q, 1.5), p, vel - (6 if k % 2 else 0), "arp", "s")
        q += 1.5
        k += 1


def frame68(seg, q0, q1, vel=44, light=True):
    """A soft frame drum in 6/8: DUM . ka DUM . ka (a low conga on the dotted-quarter beats, a bongo 'ka' on the third
    and sixth eighths); the 'ka's only in the narration pauses when light."""
    sc = seg.score
    for bar in range(int(q0 // 3), int(np.ceil(q1 / 3 - 1e-9))):
        o = bar * 3
        for dq, key, v, lt in ((0.0, 64, 0, False), (1.0, 60, -14, True), (1.5, 64, -8, False), (2.5, 60, -14, True)):
            qq = o + dq
            if not (q0 - 1e-6 <= qq < q1 - 1e-6):
                continue
            if lt and light and bool(sc.speaking(seg.t(qq))):
                continue
            drum(seg, qq, key, vel + v)


def waltz(seg, q0, q1, vel=46, bass=(43, 55), hi=(64, 76), part="harp"):
    """A music-box waltz under the tune: a plucked bass on beat 1, two soft chords on beats 2 and 3."""
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


def rolling(seg, q0=0.0, q1=None, vel=52, lo=36, hi=60, step=0.5, part="vc_fast"):
    """Cellos rolling in eighths (bass, fifth, octave, fifth), staccato."""
    broken(seg, part, q0, seg.n_q if q1 is None else q1, (0, 2, 3, 2), lo, hi, vel=vel, step=step, accent=6,
           ring=False, art="s", role="arp")


def gust(seg, q, dur_s=0.55, vel=50, lo=55, hi=84, attack=True, back=True, cym=None):
    """A gust of wind: a harp glissando up the chord (and back down), with a soft attack (a plucked low note, a soft
    timpani touch, a plucked chord; cym: a soft cymbal touch at that velocity) where it starts."""
    ch = seg.chord_at(q + 1e-3)
    if cym:
        seg.add("okit", q, 1, 57, cym, "perc", "h")
    if attack:
        seg.add("pz_lo", q, _dq(seg, q, 0.5), ch.bass_note(38, 50), vel + 4, "bass", "h")
        seg.add("pz_cb", q, _dq(seg, q, 0.5), ch.bass_note(31, 43), vel + 4, "bass", "h")
        seg.add("timp", q, _dq(seg, q, 0.5), timp_pitch(ch, ch.bass_note(38, 50)), vel - 2, "timp", "h")
        pluck_chord(seg, q, vel=vel, lo=55, hi=67)
    gliss_in(seg, "harp", q + 0.02, dur_s, lo, hi, up=True, v0=vel - 14, v1=vel, scale=ChordTones(ch))
    q_top = seg.q_of(seg.t(q) + dur_s + 0.03)
    if back and q_top < seg.n_q - 0.2:
        gliss_in(seg, "harp", q_top, dur_s * 1.2, lo, hi, up=False, v0=vel - 6, v1=vel - 18,
                 scale=ChordTones(seg.chord_at(q_top + 1e-3)))


def splash(seg, q, vel=62, cym=True):
    """A wave splashing into the boat: timpani, plucked basses, a concert bass drum, a soft cymbal, a plucked chord
    and a harp sweep down."""
    ch = seg.chord_at(q + 1e-3)
    seg.add("timp", q, _dq(seg, q, 0.5), timp_pitch(ch, ch.bass_note(38, 50)), vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q, 0.5), ch.bass_note(31, 43), vel + 2, "bass", "h")
    seg.add("pz_lo", q, _dq(seg, q, 0.5), ch.bass_note(43, 55), vel - 2, "bass", "h")
    seg.add("okit", q, 1, 36, vel - 4, "perc", "h")
    if cym:
        seg.add("okit", q, 2, 57, vel - 18, "perc", "h")
    pluck_chord(seg, q, vel=vel - 2, lo=55, hi=67)
    gliss_in(seg, "harp", q + 0.03, 0.4, midi("C4"), midi("C6"), up=False, v0=vel - 6, v1=vel - 16,
             scale=ChordTones(ch))


def stab(seg, q, vel=62, dq=0.5, brass=True, kit=True):
    """A short tutti chord (the shout '抓紧', the storm's last chord): timpani, plucked basses and chord, a bass drum,
    horns and trombones staccato."""
    ch = seg.chord_at(q + 1e-3)
    seg.add("timp", q, _dq(seg, q, 0.5), timp_pitch(ch, ch.bass_note(38, 50)), vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q, 0.5), ch.bass_note(31, 43), vel + 2, "bass", "h")
    seg.add("pz_lo", q, _dq(seg, q, 0.5), ch.bass_note(43, 55), vel, "bass", "h")
    pluck_chord(seg, q, vel=vel, lo=55, hi=67)
    if kit:
        seg.add("okit", q, 1, 36, vel - 4, "perc", "h")
    if brass:
        for k, p in enumerate(ch.tones(50, 62)[:3]):
            seg.add("horn", q, _dq(seg, q, dq), p, vel - 6, "harmony", "hs", voice=f"horn.{k + 4}")
        seg.add("tbn", q, _dq(seg, q, dq), ch.bass_note(40, 52), vel - 6, "harmony", "hs", voice="tbn.4")


def stars(segs, c, times, lo=79, hi=96, vel=40, glock_every=2, synced=(), what="a star comes out"):
    """The stars coming out one by one: a celesta chord tone for each (climbing), a soft glockenspiel on some; the
    stars at the times in `synced` (the picture's) are a little brighter (a glockenspiel with each) and synced."""
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


def star_times(c, phrase, t0, t1, n=6):
    """(times, picture times) of the stars from t0 to t1: the picture's sparkles from the line containing `phrase` on
    (as music_check picks them), with soft extra stars in between when the picture shows fewer than three; n even steps
    without the picture."""
    sp = picture(c, "sparkle", c.ls(c.find(phrase)) - 0.3, c.dur - 0.05) or []
    even = [t0 + 0.12 + k * (t1 - 0.3 - t0) / n for k in range(n)]
    if len(sp) >= 3:
        return sp[:8], sp[:8]
    if sp:
        return sorted(sp + [t for t in even if t > sp[0] and all(abs(t - x) > 0.35 for x in sp)]), sp
    return even, []


def trill(seg, part, q, dq, lo_name, hi_name, vel=50, step=0.125):
    """A bird's trill: the chord tone and its upper neighbour alternating every `step` q, inside dq, ending on the
    chord tone (a single chirp on the chord tone when there is no room for three notes)."""
    a, b = midi(lo_name), midi(hi_name)
    n = max(1, int(dq / step + 1e-6))
    if n % 2 == 0:
        n -= 1
    if n < 3:
        n = 1
    for k in range(n):
        seg.add(part, q + k * step, step, a if k % 2 == 0 else b, vel - (k % 2) * 4, "melody", "h" if k == 0 else "")


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """Jesus's theme b1-b2 (G mixolydian, 3/4): the wooden flute with the oud-like guitar an octave below, harp, soft
    strings; a glint as the title appears; far away a soft timpani roll on F (the clouds over the hills)."""
    c.gain(-10.5)
    s = c.seg(0, c.dur, 2, "3/4", "G mixolydian", nominal=78, label="title")
    s.duck(1.0)
    s.duck(4.0, parts=["flute", "guitar"])
    s.prog(" | ".join(JESUS_PROG[:2]))
    theme(s, 0, 2, vel=60)
    broken(s, "harp", 0, 6, (0, 2, 4, 5, 4, 2), 43, 55, vel=38)
    strings(s, vel=44, lo=55, hi=71)
    t_th = pic(c, "thunder", None)                         # the far-off storm clouds (picture)
    q_th = qpos(s, c, t_th, 3.0, 5.4) if t_th is not None else 4.0
    troll(s, q_th, 5.9, midi("F2"), 18, 27)
    t_gl = pic(c, "chime", None)                           # the title appears (picture)
    if t_gl is not None:
        accent(c, (s,), t_gl, "the title appears (a glint)", glock=(86, 98), celesta=(74, 86), vel=44)
    letters = [pic(c, "pop", "圣经绘本", k) for k in range(6)]   # the title's characters pop in one by one
    if None not in letters:
        prev = 64
        for k, t in enumerate(letters):                     # a celesta note for each, climbing the chord
            q = qpos(s, c, t)
            ts = s.chord_at(q + 1e-3).tones(prev + 1, 96) or s.chord_at(q + 1e-3).tones(65, 96)
            prev = ts[0]
            edge = k in (0, 5)                               # the first and the last ring out a little more
            s.add("celesta", q, _dq(s, q, 0.5), prev, 52 if edge else 38, "arp", "h")
            s.add("harp", q, _dq(s, q, 0.5), prev - 12, 48 if edge else 32, "arp", "h")
            if edge:
                s.add("glock", q, _dq(s, q, 0.5), prev + 12 if prev + 12 <= 103 else prev, 44, "arp", "h")
                s.sync(f"title character {k + 1} pops in", q, t)
    t_sp = pic(c, "sparkle", None)                         # the title sparkles
    if t_sp is not None:
        accent(c, (s,), t_sp, "the title sparkles", glock=(88, 100), vel=44)
    s.expr(["flute"], [(0, -12), (6, -12)])
    s.expr(["guitar"], [(0, -13), (6, -13)])
    s.expr(["harp"], [(0, -10), (6, -10)])
    s.expr(STR, [(0, -16), (1, -12), (6, -12)])
    s.expr(["timp"], [(0, -14), (6, -12)])
    s.expr(["glock", "celesta"], [(0, -11), (6, -11)])


def wind(c):
    """Night (E minor 3/4: harp, soft strings, a gust on '很大很大的风'); the wind blows: gusts on 呼呼, two knocks on
    哐哐 (Am B7); the gentle question (C Am7, a low clarinet); the boat on '今天的故事里' (G 6/8, the barcarolle head on
    the clarinet, the oars); the storm previewed on '好大好大的风浪' (E minor: rolling cellos, tremolo, a timpani
    roll, a horn)."""
    c.gain(-2.6)
    t_wind = c.at("风呼呼地吹")
    t_af = c.at("你会不会害怕")
    t_s = c.gap(c.find("今天的故事里"))
    t_big = c.at("遇到了好大好大的风浪")
    a = c.seg(0, t_wind, 2, "3/4", "E minor", nominal=82, label="wind-night")
    w = c.seg(t_wind, t_af, 1, "4/4", "E minor+", nominal=78, label="wind-gusts")
    q = c.seg(t_af, t_s, 1, "2/4", "E minor", nominal=66, label="wind-afraid")
    s = c.seg(t_s, t_big, 2, "6/8", "G major", nominal=104, label="wind-boat")
    b = c.seg(t_big, c.dur, 1, "4/4", "E minor+", nominal=93, label="wind-waves")
    segs = (a, w, q, s, b)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Em:3 | C:3")
    w.prog("Am:2 B7:2")
    q.prog("C:1 Am7:1")
    s.prog("G:3 | D:3")
    b.prog("Em:2 C:1 B7:1")
    s.sync("'今天的故事里': the boat (G)", 0, t_s, kind="change")
    b.sync("'好大好大的风浪': the storm previewed (E minor)", 0, t_big, kind="change")
    # 'have you ever met a very, very big wind?': night -- a slow harp, soft strings, a gust
    broken(a, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 40, 52, vel=36, thin=True)
    a.pad(["vla", "vln2"], 2, 52, 67, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    a.pad(["trem_va", "trem_va"], 2, 55, 69, vel=32, bass_ref=(40, 52))
    t_g = c.at("很大很大的风")
    gust(a, qpos(a, c, t_g, 0.5, 4.5), dur_s=0.6, vel=40, lo=52, hi=76, attack=False)
    a.expr(["harp"], [(0, -12), (6, -12)])
    a.expr(["vla", "vln2", "vc"], [(0, -20), (1.5, -17), (6, -17)])
    a.expr(["trem_va"], [(0, -24), (qpos(a, c, t_g), -21), (qpos(a, c, t_g) + 1.5, -15), (6, -20)])
    # 'the wind goes whoo-whoo, the window rattles': gusts on 呼呼, two knocks on 哐哐
    t_hu = char_at(c, "风呼呼地吹", 1)
    q_hu = qpos(w, c, t_hu, 0.0, 1.5)
    gust(w, q_hu, dur_s=0.5, vel=38, lo=52, hi=79, attack=False)
    w.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 72, vel=36, bass_ref=(33, 45))
    bassline(w, "cb", 28, 40, 36)
    knocks = [pic(c, "hammer", "小朋友", k) for k in range(2)]   # the window rattles (picture), else on 哐哐
    have = None not in knocks
    if not have:
        knocks = [char_at(c, "哐哐", k) for k in range(2)]
    for k, tk in enumerate(knocks):
        sg, qk = seg_at(c, segs, tk)
        drum(sg, qk, 76, 56 - 6 * k)
        sg.add("pz_hi", qk, _dq(sg, qk, 0.25), top(sg, qk, 59, 71), 56 - 6 * k, "arp", "h")
        sg.add("pz_lo", qk, _dq(sg, qk, 0.25), sg.chord_at(qk + 1e-3).bass_note(40, 52), 50 - 4 * k, "arp", "h")
        if have:
            sg.sync(f"the window rattles ('哐' {k + 1})", qk, tk)
    w.expr(["trem_va", "trem_hi", "cb"], [(0, -20), (q_hu + 0.6, -16), (2, -17), (4, -19)])
    w.expr(["harp"], [(0, -12), (4, -12)])
    w.expr("hand", [(0, -13), (4, -13)])
    # 'would you be scared?': a gentle question (a low clarinet, soft strings)
    q.mel("clar", "G4:1 A4:1", vel=48)
    q.pad(["vla", "vln2"], 2, 52, 67, vel=38, bass_part="vc", bass_lo=45, bass_hi=57)
    q.add("harp", 0, 1, "E4", 34, "arp")
    q.add("harp", 1, 1, "E4", 32, "arp")
    q.expr(["clar"], [(0, -16), (2, -16)])
    q.expr(["vla", "vln2", "vc"], [(0, -17), (2, -16)])
    q.expr(["harp"], [(0, -13), (2, -13)])
    # 'in today's story a group of people in a boat...': the barcarolle head (G), the oars
    s.mel("clar", "B4:1 D5:1/2 G5:1 B4:1/2 | F#5:1 E5:1/2 D5:1 A4:1/2", vel=52)
    oars(s, 0, 6, vel=50)
    guitar(s, 0, 6, vel=40)
    frame68(s, 0, 6, vel=40)
    s.pad(["vla", "vln2"], 2, 55, 69, vel=34, bass_ref=(43, 55))
    s.add("harp", 0, 1.5, "G3", 36, "arp", "h")
    s.add("harp", 0.03, 1.47, "D4", 34, "arp", "h")
    s.add("harp", 0.06, 1.44, "B4", 33, "arp", "h")
    t_page = pic(c, "chime", "今天的故事里")                  # the picture book opens (picture)
    if t_page is not None:
        accent(c, segs, t_page, "the story book opens (a chime)", glock=(86, 98), celesta=(74, 86), vel=44)
    s.duck(3.0, parts=["clar", "guitar"])
    s.expr(["clar"], [(0, -18), (1.5, -14), (6, -14)])
    s.expr(["pz_lo", "guitar", "harp"], [(0, -16), (1.5, -12), (6, -12)])
    s.expr("hand", [(0, -18), (1.5, -14), (6, -14)])
    s.expr(["vla", "vln2"], [(0, -19), (6, -19)])
    # '...met a big, big wind and waves': the storm previewed -- rolling cellos, tremolo swelling, a timpani roll
    rolling(b, 0, 4, vel=48, lo=40, hi=64)
    b.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 71, vel=40, bass_ref=(40, 52))
    bassline(b, "cb", 28, 40, 40)
    b.add("timp", 0, 0.5, "E2", 48, "timp", "h")
    b.add("pz_cb", 0, 0.5, "E2", 52, "bass", "h")
    b.add("harp", 0, 2, "E3", 44, "arp", "h")
    troll(b, 0.5, 3.9, midi("E2"), 22, 32, rate=9)
    b.mel("horn", "E3:2 E3:1 D#3:1", vel=44)
    b.expr(["vc_fast"], [(0, -17), (2, -15), (4, -19)])
    b.expr(["trem_va", "trem_hi", "cb"], [(0, -19), (2.5, -15), (4, -19)])
    b.expr(["horn"], [(0, -19), (2.5, -15), (4, -20)])
    b.expr(["harp"], [(0, -12), (4, -14)])
    for k in range(2):                                     # the waves splash up in the picture
        t = pic(c, "splash", "今天的故事里", k)
        if t is not None:
            sg, q = seg_at(c, segs, t)
            splash(sg, q, vel=52 + 2 * k, cym=False)
            sg.sync(f"a wave splashes up ({k + 1})", q, t)
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["pz_hi", "pz_lo", "pz_cb", "timp"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])


def friends(c):
    """Morning on the lake (D); G on '十二个好朋友': Jesus b1-b2 (flute + guitar) and twelve harp notes rising, one per
    friend (on the picture's pops); the fishermen's barcarolle on '他们当中' (D mixolydian 6/8: clarinet, the oars, a
    frame drum; four plucks for the four names, a harp sweep for the net); b5-b8 and a little gust on '起风'."""
    c.gain(-2.4)
    t12 = c.at("十二个好朋友")
    t_f = c.gap(c.find("他们当中"))
    t_k = c.gap(c.find("他们最熟悉"))
    m = c.seg(0, t12, 1, "2/4", "D mixolydian", nominal=80, label="friends-morning")
    j = c.seg(t12, t_f, 2, "3/4", "G mixolydian", nominal=128, label="friends-twelve")
    f = c.seg(t_f, t_k, 6, "6/8", "D mixolydian", nominal=110, label="friends-fishermen")
    d = c.seg(t_k, c.dur, 4, "6/8", "D mixolydian", nominal=114, label="friends-lake")
    segs = (m, j, f, d)
    for sg in segs:
        sg.duck(1.5)
    m.prog("D:2")
    j.prog(" | ".join(JESUS_PROG[:2]))
    f.prog(" | ".join(BOAT_PROG[:3] + ["D:3"] + BOAT_PROG[5:7]))
    d.prog(" | ".join(BOAT_PROG[4:8]))
    j.sync("'十二个好朋友': Jesus and his friends (G)", 0, t12, kind="change")
    f.sync("'他们当中': the fishermen's barcarolle (D)", 0, t_f, kind="change")
    # morning on the lake: a harp sweep up, soft strings
    gliss_in(m, "harp", 0.1, 0.6, midi("D4"), midi("D6"), v0=28, v1=40, scale=ChordTones(m.chord_at(0)))
    m.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=36, bass_part="vc", bass_lo=38, bass_hi=50)
    m.expr(["harp"], [(0, -12), (2, -12)])
    m.expr(["vla", "vln2", "vln1", "vc"], [(0, -20), (2, -17)])
    # 'Jesus had twelve good friends, his disciples': the theme, twelve harp notes rising
    theme(j, 0, 2, vel=54)
    j.pad(["vla", "vln2"], 2, 55, 71, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(j, "cb", 29, 41, 34)
    pops = [pic(c, "pop", "耶稣有十二个好朋友", k) for k in range(12)]
    have = None not in pops
    if not have:                                           # no picture: twelve even steps from the phrase
        pops = [t12 + k * (t_f - 0.25 - t12) / 12 for k in range(12)]
    prev = 54
    for k, t in enumerate(pops):
        sg, q = seg_at(c, segs, t)
        ts = sg.chord_at(q + 1e-3).tones(prev + 1, 100) or sg.chord_at(q + 1e-3).tones(55, 100)
        prev = ts[0]
        sg.add("harp", q, _dq(sg, q, 0.5), prev, 50 if k in (0, 11) else 36 + k, "arp", "h")
        if k in (0, 11):
            sg.add("guitar", q, _dq(sg, q, 0.25), top(sg, q, 55, 67), 54, "arp", "h")
            sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, 67, 79), 54, "arp", "h")
            sg.add("celesta", q, _dq(sg, q, 0.5), top(sg, q, 79, 91), 44, "arp", "h")
            if k == 11:
                sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, 86, 98), 44, "arp", "h")
            if have:
                sg.sync("friend 1 pops up" if k == 0 else "friend 12 pops up", q, t)
    j.duck(4.0, parts=["flute", "guitar"])
    j.duck(2.5, parts=["harp", "celesta", "glock", "pz_hi"])
    j.expr(["flute"], [(0, -14), (6, -14)])
    j.expr(["guitar"], [(0, -14), (6, -14)])
    j.expr(["harp", "glock", "celesta"], [(0, -11), (6, -11)])
    for sg in (m, j):
        sg.expr(["pz_hi"], [(0, -11), (sg.n_q, -11)])
    j.expr(["vla", "vln2", "vc", "cb"], [(0, -19), (6, -18)])
    # 'some of them were fishermen... casting their nets on the Sea of Galilee': the barcarolle, the oars
    f.mel("clar", bars(BOAT, 0, 4) + " | " + bars(BOAT, 5, 7), vel=54)
    oars(f, 0, 18, vel=50)
    guitar(f, 0, 18, vel=40)
    frame68(f, 0, 18, vel=40)
    f.pad(["vla", "vln2"], 2, 55, 69, vel=34, bass_ref=(38, 50))
    f.add("cb", 0, 18, "D2", 34, "bass")
    t_fish = pic(c, "sparkle", "他们当中")                   # the fishermen light up (picture)
    if t_fish is not None:
        accent(c, segs, t_fish, "the fishermen light up", glock=(86, 98), harp=(67, 79), vel=44)
    names = syl(c, "彼得", 3) + [char_at(c, "约翰", 0)]       # 彼得、安得烈、雅各 和 约翰 (as spoken)
    n_pic = [pic(c, "pop", "他们当中", k) for k in range(4, 8)]  # ... or as each pops up in the picture
    have = None not in n_pic
    for k, t in enumerate(n_pic if have else names):       # one pluck for each name, climbing
        sg, q = seg_at(c, segs, t)
        sg.add("guitar", q, _dq(sg, q, 0.5), top(sg, q, 62 + 2 * k, 70 + 2 * k), 58, "arp", "h")
        sg.add("harp", q, _dq(sg, q, 0.5), top(sg, q, 74 + 2 * k, 84 + 2 * k), 50, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 0.5), top(sg, q, 79 + 2 * k, 91 + 2 * k), 44, "arp", "h")
        if have:
            sg.sync(f"{('彼得', '安得烈', '雅各', '约翰')[k]} pops up", q, t)
    t_net = near(c, "whoosh", c.at("撒网"), 0.8)               # the net flies out (picture, else the word)
    sg, q = seg_at(c, segs, t_net)
    gliss_in(sg, "harp", q, 0.5, midi("D4"), midi("D6"), v0=30, v1=46, scale=ChordTones(sg.chord_at(q + 1e-3)))
    t_in = pic(c, "splash", "以前每天")                       # the net lands in the water (picture)
    if t_in is not None:
        sg, q = accent(c, segs, t_in, "the net lands in the water", pluck=(62, 74), vel=46)
        sg.add("pz_cb", q, _dq(sg, q, 0.5), sg.chord_at(q + 1e-3).bass_note(29, 41), 50, "bass", "h")
    f.duck(2.5, parts=["clar", "guitar"])
    f.expr(["clar"], [(0, -15), (18, -15)])
    f.expr(["pz_lo", "guitar"], [(0, -13), (18, -13)])
    f.expr(["harp"], [(0, -12), (18, -12)])
    f.expr("hand", [(0, -15), (18, -15)])
    f.expr(["vla", "vln2", "cb"], [(0, -20), (18, -20)])
    # 'they knew this lake best: where the fish are, when the wind comes': b5-b8, a little gust on '起风'
    d.mel("clar", bars(BOAT, 4, 8), vel=52)
    oars(d, 0, 12, vel=48)
    guitar(d, 0, 12, vel=40)
    frame68(d, 0, 12, vel=40)
    d.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=34, bass_ref=(38, 50))
    d.add("cb", 0, 12, "D2", 34, "bass")
    spots = [pic(c, "pop", "他们最熟悉", k) for k in range(4)]   # the fish spots pop up on the map (picture)
    if None not in spots:
        prev = 76
        for k, t in enumerate(spots):
            sg, q = seg_at(c, segs, t)
            ts = sg.chord_at(q + 1e-3).tones(prev + 1, 96) or sg.chord_at(q + 1e-3).tones(77, 96)
            prev = ts[0]
            sg.add("celesta", q, _dq(sg, q, 0.5), prev, 46 + k, "arp", "h")
            if k == 0:
                sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, 67, 79), 50, "arp", "h")
                sg.sync("a fish spot pops up on the map", q, t)
    t_wind = pic(c, "wind_soft", "他们最熟悉") or c.at("起风")    # the little wind sign (picture), else '起风'
    gust(d, qpos(d, c, t_wind, 0.0, 10.5), dur_s=0.45, vel=40, lo=55, hi=79, attack=False)
    t_ch = pic(c, "chime", "他们最熟悉")                      # '他们都知道' (picture)
    if t_ch is not None:
        accent(c, segs, t_ch, "they know the lake (a chime)", glock=(86, 98), celesta=(74, 86), vel=44)
    for sg in (f, d):
        sg.expr(["glock", "celesta", "pz_hi"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["pz_cb"], [(0, -12), (sg.n_q, -12)])
    d.duck(2.5, parts=["clar", "guitar"])
    d.expr(["clar"], [(0, -15), (12, -15)])
    d.expr(["pz_lo", "guitar"], [(0, -13), (12, -13)])
    d.expr(["harp"], [(0, -12), (12, -12)])
    d.expr("hand", [(0, -15), (12, -15)])
    d.expr(["vla", "vln2", "vln1", "cb"], [(0, -20), (12, -19)])


def shore(c):
    """Jesus teaches by the lake: his theme b1-b4 (G mixolydian: flute + guitar, harp; the crowd -- a soft choir
    'ooh'); b7-b8 (F G) as he sits in the boat; the hush on '大家都安安静静地听' (Cadd9 G: harp, high strings, a
    celesta peeks -- the children)."""
    c.gain(-2.6)
    t_sit = c.at("人太多了")
    t_h = c.gap(c.find("大家都安安静静地听"))
    a = c.seg(0, t_sit, 4, "3/4", "G mixolydian", nominal=122, label="shore-teaching")
    b = c.seg(t_sit, t_h, 2, "3/4", "G mixolydian", nominal=96, label="shore-boat")
    h = c.seg(t_h, c.dur, 2, "3/4", "G mixolydian", nominal=72, label="shore-hush")
    segs = (a, b, h)
    for sg in segs:
        sg.duck(1.5)
    a.prog(" | ".join(JESUS_PROG[:4]))
    b.prog(" | ".join(JESUS_PROG[6:8]))
    h.prog("Cadd9:3 | G:3")
    h.sync("'大家都安安静静地听': the hush (Cadd9)", 0, t_h, kind="change")
    theme(a, 0, 4, vel=54)
    broken(a, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 43, 55, vel=34, thin=True)
    strings(a, vel=38, lo=55, hi=71)
    a.pad("ooh", 3, 55, 70, vel=32, q0=6, bass_ref=(41, 55))
    a.duck(4.0, parts=["flute", "guitar"])
    a.duck(2.5, parts=["harp", "ooh"])
    a.expr(["flute"], [(0, -14), (12, -14)])
    a.expr(["guitar"], [(0, -14), (12, -14)])
    a.expr(["harp"], [(0, -12), (12, -12)])
    a.expr(STR, [(0, -19), (12, -18)])
    a.expr(["ooh"], [(6, -24), (9, -20), (11, -21), (12, -26)])
    # 'there were so many that Jesus sat in a boat to tell his stories': b7-b8, the boat rocking (harp)
    theme(b, 6, 8, vel=52)
    broken(b, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 41, 53, vel=34, thin=True)
    strings(b, vel=38, lo=55, hi=71)
    b.duck(2.5, parts=["flute", "guitar"])
    b.expr(["flute"], [(0, -14), (6, -15)])
    b.expr(["guitar"], [(0, -14), (6, -15)])
    b.expr(["harp"], [(0, -12), (6, -12)])
    b.expr(STR, [(0, -18), (6, -19)])
    # 'everyone listened quietly, even the children': the hush -- harp, high strings, a celesta peeks
    roll_chord(h, 0, 48, 72, vel=44)
    h.pad(["vla", "vln2", "vln1"], 3, 59, 76, vel=34, bass_part="vc", bass_lo=43, bass_hi=55)
    h.mel("celesta", "G5:1 C6:1 E6:1 | D6:3", vel=36, role="arp")
    h.expr(["harp"], [(0, -11), (6, -12)])
    h.expr(["vla", "vln2", "vln1", "vc"], [(0, -19), (6, -20)])
    h.expr(["celesta"], [(0, -13), (6, -14)])
    t_step = pic(c, "splash_small", "人太多了")              # Jesus steps into the boat (picture)
    if t_step is not None:
        accent(c, segs, t_step, "Jesus steps into the boat", glock=(84, 96), harp=(62, 74), pluck=(62, 74), low=True,
               vel=50)
    for sg in segs:
        sg.expr(["pz_hi", "glock"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])


def seed(c):
    """The mustard seed, a music-box miniature (C major 3/4: music box and celesta over a pizzicato-harp waltz); F,
    tiny and high, on '最小最小的种子', a pling on each sparkle of the seed (the picture; else on each 最小); the seed
    planted (a low C as it pops into the earth, drops of rain); 长啊长 -- each 长 a step up (Dm7 Em7 F G, the music box
    D6 E6 F6 G6 over a climbing bass; the third step on the picture's growth), C, big, on '都大' (the attack on the
    big tree's sparkle); the branches (F) and C on '做窝', the birds' flute trill as they land (the picture's pops);
    the nods and a smile (F G7 C)."""
    c.gain(-0.8)
    t_s = c.gap(c.find("芥菜种"))
    t_small = c.at("最小最小的种子")
    t_plant = c.at("可是种在地里")
    t_grow = c.at("长啊长")
    t_branch = c.at("连小鸟")
    t_nest = c.at("做窝")
    t_e = c.gap(c.find("大家听了"))
    g0 = pic(c, "grow", "芥菜种", 0)
    sprout = g0 is not None and -0.045 <= g0 - t_grow <= 0.0  # the sprout grows (picture) just before '长啊长':
    t_gs = g0 if sprout else t_grow                          # the first step starts on the picture
    a = c.seg(0, t_s, 4, "3/4", "C major", nominal=136, label="seed-music-box")
    sm = c.seg(t_s, t_plant, 2, "3/4", "C major", nominal=112, label="seed-tiny")
    p = c.seg(t_plant, t_gs, 1, "3/4", "C major", nominal=84, label="seed-planted")
    g = c.seg(t_gs, t_branch, 1, "4/4", "C major", nominal=84, label="seed-grows")
    b = c.seg(t_branch, t_e, 2, "3/4", "C major", nominal=102, label="seed-birds")
    e = c.seg(t_e, c.dur, 2, "3/4", "C major", nominal=114, label="seed-smile")
    segs = (a, sm, p, g, b, e)
    for sg in segs:
        sg.duck(1.5)
    a.prog(" | ".join(MBOX_PROG))
    sm_ed = edges48(sm, c, [t_small])
    prog48(sm, ["C", "F"], sm_ed)
    p.prog("C:3")
    # 长 啊 长 / 长得 (the picture's growth) / 所有的菜 / 都大: each 长 a step up
    t_g2 = char_at(c, "长啊长", 2)
    t_all = c.at("所有的菜")
    t_big = c.at("都大")
    g1 = pic(c, "grow", "芥菜种", 1)
    pic_g1 = g1 is not None and t_g2 + 0.15 < g1 < t_all - 0.15
    t_g3 = g1 if pic_g1 else c.at("长得比所有的菜都大")
    ed = edges48(g, c, [t_g2, t_g3, t_all, t_big])
    prog48(g, ["Dm7", "Em7", "F", "G", "C"], ed)
    b_ed = edges48(b, c, [t_nest])
    prog48(b, ["F", "C"], b_ed)
    e.prog("F:3/2 G7:3/2 | C:3")
    sm.sync("'最小最小的种子': F (tiny, high)", sm_ed[1] / 48, t_small, kind="change")
    g.sync("'长啊长': the seed grows (Dm7, a step up)", 0, t_grow, kind="change")
    b.sync("'做窝': C (the birds' nest)", b_ed[1] / 48, t_nest, kind="change")
    # 'that day Jesus told a story of a tiny seed': the music box, a pizzicato-harp waltz
    a.mel("mbox", bars(MBOX, 0, 4), vel=54)
    a.mel("celesta", bars(MBOX, 0, 4), vel=40, transpose=-12, role="counter")
    waltz(a, 0, 12, vel=44)
    a.pad(["vla", "vln2"], 2, 60, 74, vel=32, bass_ref=(43, 55))
    t_page = pic(c, "chime", "那天")                        # the story's picture appears
    if t_page is not None:
        accent(c, segs, t_page, "the story picture appears (a chime)", glock=(86, 98), vel=46)
    a.duck(2.5, parts=["mbox", "celesta"])
    a.expr(["mbox"], [(0, -13), (12, -13)])
    a.expr(["celesta"], [(0, -15), (12, -15)])
    a.expr(["pz_lo", "harp"], [(0, -13), (12, -13)])
    a.expr(["vla", "vln2"], [(0, -21), (12, -21)])
    # 'the mustard seed is the smallest of all seeds': tiny -- high and thin; a pling on each sparkle of the seed
    sm.pad(["vln2", "vln1"], 2, 67, 84, vel=30, bass_ref=(48, 60))
    roll_chord(sm, sm_ed[1] / 48, 65, 84, vel=36, n=3)
    pl = [pic(c, "sparkle", "芥菜种", k) for k in range(2)]
    have = None not in pl and all(t_s <= t <= t_plant - 0.1 for t in pl)
    for k, t in enumerate(pl if have else (t_small, char_at(c, "最小最小的种子", 2))):
        sg, q = seg_at(c, segs, t)
        nm = top(sg, q, 91, 98)
        sg.add("mbox", q, _dq(sg, q, 1.0), nm, 58 - 4 * k, "arp", "h")
        sg.add("glock", q, _dq(sg, q, 1.0), nm, 46 - 4 * k, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 1.0), nm - 12, 42 - 4 * k, "arp", "h")
        if have:
            sg.sync(f"the tiny seed sparkles ({k + 1})", q, t)
        elif k == 0:
            sg.sync("'最小最小的种子': a tiny pling", q, t)
    sm.expr(["vln2", "vln1"], [(0, -22), (6, -22)])
    sm.expr(["harp"], [(0, -14), (6, -14)])
    # 'but planted in the ground': the seed pops into the earth -- a low soft C; drops of rain
    t_pop0 = pic(c, "pop", "芥菜种", 0)
    t_plop = t_pop0 if t_pop0 is not None and t_plant <= t_pop0 <= t_gs - 0.2 else None
    if t_pop0 is not None and t_plop is None:               # the picture's pop elsewhere: an accent there
        accent(c, segs, t_pop0, "the seed goes into the earth (a low C)", celesta=(72, 84), pluck=(48, 60), vel=48)
    q_pl = qpos(p, c, t_plop, 0.0, 2.6) if t_plop is not None else 0.0
    p.add("pz_cb", q_pl, _dq(p, q_pl, 1.0), "C2", 48, "bass", "h")
    p.add("harp", q_pl, p.n_q - q_pl, "C2", 42, "arp", "h")
    p.add("harp", q_pl + 0.05, p.n_q - q_pl - 0.05, "G2", 38, "arp")
    p.add("timp", q_pl, _dq(p, q_pl, 0.5), "C3", 36, "timp", "h")
    p.add("celesta", q_pl, _dq(p, q_pl, 0.5), "C6", 40, "arp", "h")
    if t_plop is not None or t_pop0 is None:
        p.sync("the seed goes into the earth (a low C)", q_pl, t_plop if t_plop is not None else t_plant)
    p.pad(["vla", "vln2"], 2, 55, 67, vel=36, bass_part="vc", bass_lo=36, bass_hi=48)
    t_rain = pic(c, "rain", "芥菜种", 0, lo=t_plant, hi=t_gs - 0.3)
    q_r = qpos(p, c, t_rain, 0.3, 2.0) if t_rain is not None else 1.0
    for k in range(3):                                     # rain on the seed: soft drops
        dq = q_r + 0.375 * k
        if dq < p.n_q - 0.2:
            p.add("celesta", dq, _dq(p, dq, 0.5), top(p, dq, 76, 88, -1 - k), 34, "arp", "s")
    p.expr(["pz_cb", "harp", "timp"], [(0, -12), (3, -12)])
    p.expr(["celesta"], [(0, -14), (3, -14)])
    p.expr(["vla", "vln2", "vc"], [(0, -20), (3, -18)])
    # 长啊长 ... 长得比所有的菜都大: each 长 a step up, then big on '都大'
    steps = [("D6", "D3"), ("E6", "E3"), ("F6", "F3"), ("G6", "G3")]
    for k, (hi_, lo_) in enumerate(steps):
        q = ed[k] / 48
        dq = (ed[k + 1] - ed[k]) / 48
        g.add("mbox", q, dq, hi_, 48 + 3 * k, "arp", "h")
        g.add("celesta", q, dq, midi(hi_) - 12, 36 + 2 * k, "arp", "h")
        g.add("pz_lo", q, min(dq, 0.75), lo_, 46 + 3 * k, "bass", "h")
    if sprout:
        g.sync("the sprout grows (picture)", 0, g0)
    elif g0 is not None:
        accent(c, segs, g0, "the sprout grows (picture)", glock=(86, 98), vel=46)
    if pic_g1:
        g.sync("the plant grows up (picture)", ed[2] / 48, g1)
    elif g1 is not None:
        accent(c, segs, g1, "the plant grows up (picture)", glock=(86, 98), celesta=(74, 86), vel=48)
    q_c = ed[4] / 48
    t_spk = pic(c, "sparkle", "芥菜种", 2)                    # the big tree glows (picture)
    t_ce = g.t(q_c) - c.t0                                 # the C edge ('都大')
    t_tree = t_spk if t_spk is not None and t_ce <= t_spk <= t_branch - 0.15 else None
    q_big = qpos(g, c, t_tree, q_c, g.n_q - 0.15) if t_tree is not None else q_c
    g.add("mbox", q_big, g.n_q - q_big, "C7", 60, "arp", "h")
    g.add("glock", q_big, g.n_q - q_big, "C7", 48, "arp", "h")
    g.add("pz_cb", q_big, _dq(g, q_big, 0.5), "C2", 56, "bass", "h")
    g.add("timp", q_big, _dq(g, q_big, 0.5), "C3", 46, "timp", "h")
    gliss_in(g, "harp", q_big, 0.4, midi("C4"), midi("C6"), v0=34, v1=48, scale=ChordTones(g.chord_at(q_big + 1e-3)))
    g.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_ref=(38, 50))
    g.add("horn", q_c, g.n_q - q_c, "E4", 42, "pad", voice="horn.0")
    g.add("horn", q_c, g.n_q - q_c, "G3", 42, "pad", voice="horn.1")
    g.sync("the big tree (sparkle)" if t_tree is not None else "'都大': big (C)", q_big,
           t_tree if t_tree is not None else t_big)
    if t_spk is not None and t_tree is None:
        accent(c, segs, t_spk, "the big tree (sparkle)", glock=(86, 98), vel=50)
    g.expr(["mbox", "celesta", "glock"], [(0, -12), (4, -11)])
    g.expr(["pz_lo", "pz_cb", "timp", "harp"], [(0, -12), (4, -11)])
    g.expr(["vla", "vln2", "vln1"], [(0, -20), (q_c, -17), (4, -16)])
    g.expr(["horn"], [(0, -18), (4, -17)])
    # 'even the birds can nest in its branches': warm strings; C on '做窝', the birds' trill as they land
    strings(b, vel=36, lo=55, hi=74, bass=(41, 53), cb=(29, 41))
    broken(b, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 41, 53, vel=34, thin=True)
    t_bird = c.at("小鸟")
    q_bd = qpos(b, c, t_bird, 0.0, min(2.2, b_ed[1] / 48 - 0.6))
    for k in range(3):                                     # a little bird flies in: a flute flick up the chord
        qq = q_bd + 0.125 * k
        b.add("flute", qq, 0.125 if k < 2 else 0.25, top(b, qq, 77, 89, k - 3), 48 - 2 * k, "melody",
              "h" if k == 0 else "")
    birds = [t for t in (pic(c, "pop", "芥菜种", k) for k in (1, 2, 3)) if t is not None]
    have = bool(birds)
    lands = birds if have else [t_nest]
    sg, q_n = seg_at(c, segs, lands[0])
    q_end = min(sg.q_of(c.t0 + lands[-1]) + 0.75, span_end(sg, q_n + 1e-6) - 0.05, sg.n_q - 0.3)
    ch = sg.chord_at(q_n + 1e-3)
    t_lo = max(ch.tones(86, 93))                          # the bird: the highest chord tone near G6 ...
    t_hi = min(p_ for p_ in range(t_lo + 1, t_lo + 3) if any(p_ in sc_ for sc_ in sg.scales_at(q_n)))   # ... and its
    from audio.theory import name as _nm                  # upper neighbour in the scale
    trill(sg, "flute", q_n, q_end - q_n, _nm(t_lo), _nm(t_hi), vel=52)
    for k, t in enumerate(lands):                          # each bird lands in the nest
        sg_k, q_k = seg_at(c, segs, t)
        sg_k.add("celesta", q_k, _dq(sg_k, q_k, 0.5), top(sg_k, q_k, 84, 96, -1 - (k % 2)), 50 - 4 * k, "arp", "h")
        if k == 0:
            sg_k.add("pz_hi", q_k, _dq(sg_k, q_k, 0.25), top(sg_k, q_k, 72, 84), 54, "arp", "h")
            sg_k.add("harp", q_k, _dq(sg_k, q_k, 0.5), top(sg_k, q_k, 67, 79), 48, "arp", "h")
            sg_k.sync("a bird lands in the nest (trill)" if have else "'做窝': the birds' trill (flute)", q_k, t)
    b.expr(["flute"], [(0, -14), (6, -14)])
    b.expr(STR, [(0, -20), (6, -19)])
    b.expr(["harp", "celesta"], [(0, -12), (6, -12)])
    # 'everyone nodded and smiled': the music box again, the nods, a smile
    e.mel("mbox", "A5:1 C6:1/2 B5:1/2 D6:1 | C6:3", vel=52)
    waltz(e, 0, 6, vel=42)
    e.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=32, bass_ref=(41, 53))
    t_smile = c.at("笑了")
    sg, q = seg_at(c, segs, t_smile)
    sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, 84, 96), 44, "arp", "h")
    e.expr(["mbox"], [(0, -14), (6, -15)])
    e.expr(["pz_lo", "harp"], [(0, -13), (6, -14)])
    e.expr(["vla", "vln2", "vln1"], [(0, -21), (6, -22)])
    for sg in segs:
        sg.expr(["glock"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["pz_hi"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])


def evening(c):
    """Sunset: an evening hymn in C (C G/B Am7 F: horns and strings, a guitar chord, the light going gold); G on
    '我们渡到湖的那一边去吧' -- Jesus b1 on the flute and guitar, a harp sweep across the lake, C D."""
    c.gain(-2.6)
    t_j = c.gap(c.find("我们渡到湖的那一边去吧"))
    a = c.seg(0, t_j, 1, "4/4", "C major", nominal=60, label="evening-sunset")
    j = c.seg(t_j, c.dur, 2, "3/4", "G mixolydian", nominal=104, label="evening-across")
    for sg in (a, j):
        sg.duck(1.5)
    a.prog("C:1 G/B:1 Am7:1 F:1")
    j.prog("G:3 | C:3/2 D:3/2@G-major")
    j.sync("'我们渡到湖的那一边去吧': G (Jesus)", 0, t_j, kind="change")
    # 'it was getting dark': the evening hymn (horns, strings)
    a.pad(["horn", "horn", "horn"], 3, 50, 65, vel=42, bass_ref=(33, 48))
    a.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(a, "cb", 28, 40, 34)
    for q in range(4):
        roll_chord(a, q, 43, 64, vel=36, gap_s=0.04, part="guitar", n=4)
    a.expr(["horn"], [(0, -26), (1, -18), (2, -16), (4, -17)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -26), (1, -19), (2, -17), (4, -18)])
    a.expr(["guitar"], [(0, -22), (1, -15), (4, -15)])
    # 'let us go over to the other side': Jesus b1, a harp sweep across the lake
    theme(j, 0, 1, vel=52)
    j.mel("flute", "E5:3/2 F#5:3/2", q=3, vel=50)
    j.mel("guitar", "E4:3/2 F#4:3/2", q=3, vel=44, role="counter")
    roll_chord(j, 0, 43, 67, vel=44)
    gliss_in(j, "harp", 3.0, 0.7, midi("C4"), midi("C6"), v0=28, v1=42, scale=ChordTones(j.chord_at(3.01)))
    strings(j, vel=36, lo=55, hi=71)
    t_push = pic(c, "thud", "我们渡到湖的那一边去吧")         # the boat is pushed off (picture)
    if t_push is not None:
        accent(c, (a, j), t_push, "the boat is pushed off", harp=(62, 74), pluck=(62, 74), low=True, vel=48)
    j.duck(3.0, parts=["flute", "guitar"])
    j.expr(["flute", "guitar"], [(0, -15), (6, -16)])
    j.expr(["harp"], [(0, -12), (6, -12)])
    j.expr(STR, [(0, -19), (6, -19)])
    for sg in (a, j):
        sg.expr(["pz_hi", "timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])


def sleep(c):
    """The boat sets out (the barcarolle in G 6/8, the oars); Jesus tired (Em Am7 D, the clarinet slowing); the lullaby
    on '睡着了' (celesta and harp, G C Am7 D); 摇啊摇 (G C D7, the flute, the boat rocking); the stars on
    '星星一颗一颗地亮起来了' (Em7 Cadd9: a celesta note for each star), ringing into the dark."""
    c.gain(-1.8)
    t_t = c.at("耶稣累了一整天")
    t_sl = c.at("睡着了")
    t_r = c.gap(c.find("小船在湖上"))
    t_st = c.at("星星一颗一颗地亮起来了")
    r = c.seg(0, t_t, 2, "6/8", "G major", nominal=116, label="sleep-row")
    t = c.seg(t_t, t_sl, 2, "6/8", "G major", nominal=96, rit=0.15, label="sleep-tired")
    lu = c.seg(t_sl, t_r, 4, "6/8", "G major", nominal=122, label="sleep-lullaby")
    s = c.seg(t_r, t_st, 3, "6/8", "G major", nominal=126, label="sleep-rocking")
    st = c.seg(t_st, c.dur, 2, "6/8", "G major", nominal=118, label="sleep-stars")
    segs = (r, t, lu, s, st)
    for sg in segs:
        sg.duck(1.5)
    r.prog("G:3 | C/G:3")
    t.prog("Em:3 | Am7:3/2 D:3/2")
    lu.prog(" | ".join(LULL_PROG[:4]))
    s.prog(" | ".join(LULL_PROG[4:7]))
    st.prog("Em7:3 | Cadd9:3")
    lu.sync("'睡着了': the lullaby (G)", 0, t_sl, kind="change")
    st.sync("'星星一颗一颗地亮起来了': the stars (Em7)", 0, t_st, kind="change")
    # 'the disciples rowed the boat out': the barcarolle in G, the oars
    r.mel("clar", "B4:1 D5:1/2 G5:3/2 | E5:1 C5:1/2 E5:1 G5:1/2", vel=52)
    oars(r, 0, 6, vel=50)
    guitar(r, 0, 6, vel=40)
    frame68(r, 0, 6, vel=38)
    r.pad(["vla", "vln2"], 2, 55, 69, vel=34, bass_ref=(43, 55))
    r.duck(2.5, parts=["clar", "guitar"])
    r.expr(["clar"], [(0, -15), (6, -15)])
    r.expr(["pz_lo", "guitar"], [(0, -17), (1.5, -13), (6, -13)])
    r.expr("hand", [(0, -19), (1.5, -15), (6, -16)])
    r.expr(["vla", "vln2"], [(0, -20), (6, -20)])
    # 'Jesus was tired after a long day; at the back of the boat, on a cushion...': slowing
    t.mel("clar", "B4:3/2 G4:3/2 | C5:3/2 A4:1 F#4:1/2", vel=48)
    broken(t, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 40, 52, vel=34, thin=True)
    t.pad(["vla", "vln2", "vln1"], 3, 55, 71, vel=34, bass_part="vc", bass_lo=40, bass_hi=52)
    t.duck(2.5, parts=["clar"])
    t.expr(["clar"], [(0, -15), (6, -15)])
    t.expr(["harp"], [(0, -12), (6, -12)])
    t.expr(["vla", "vln2", "vln1", "vc"], [(0, -20), (6, -19)])
    # '...fell asleep': the lullaby (celesta, harp, soft strings, the boat rocking)
    lu.mel("celesta", bars(LULL, 0, 4), vel=46)
    broken(lu, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 43, 55, vel=34, thin=True)
    lu.pad(["vla", "vln2", "vln1"], 3, 55, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    lu.add("pz_cb", 0, 1.5, "G2", 38, "bass", "h")
    lu.duck(2.5, parts=["celesta", "harp"])
    lu.expr(["celesta"], [(0, -16), (1.5, -13), (12, -13)])
    lu.expr(["harp", "pz_cb"], [(0, -14), (1.5, -12), (12, -12)])
    lu.expr(["vla", "vln2", "vln1", "vc"], [(0, -20), (12, -20)])
    # 'the little boat rocked gently on the lake': the lullaby on the flute, the rocking
    s.mel("flute", bars(LULL, 4, 7), vel=48)
    guitar(s, 0, 9, pat=(0, 2, 4, 2, 4, 2), lo=43, hi=55, vel=38)
    s.pad(["vla", "vln2", "vln1"], 3, 55, 71, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    s.duck(2.5, parts=["flute", "guitar"])
    s.expr(["flute"], [(0, -20), (1.5, -15), (9, -15)])
    s.expr(["guitar"], [(0, -19), (1.5, -14), (9, -14)])
    s.expr(["vla", "vln2", "vln1", "vc"], [(0, -20), (9, -20)])
    # 'the stars came out one by one': a celesta note for each star, soft high strings, ringing into the dark
    times, sp = star_times(c, "星星一颗一颗地亮起来了", t_st, c.dur - 0.3, 6)
    stars(segs, c, times, lo=79, hi=96, vel=40, synced=sp, what="a star comes out")
    t_off = pic(c, "thud", "门徒们把船划开了")                # the boat pushes off (picture)
    if t_off is not None:
        accent(c, segs, t_off, "the boat pushes off", harp=(62, 74), low=True, vel=46)
    t_lie = pic(c, "cloth", "门徒们把船划开了", 1)            # Jesus lies down on the cushion (picture)
    if t_lie is not None:
        accent(c, segs, t_lie, "Jesus lies down to sleep", celesta=(79, 91), harp=(67, 79), vel=48)
    for t_cr in picture(c, "ship_creak", t_st - 3.0, t_st) or []:   # the boat creaks as it rocks: a low pluck
        sg, q_cr = seg_at(c, segs, t_cr)
        sg.add("guitar", q_cr, _dq(sg, q_cr, 0.75), sg.chord_at(q_cr + 1e-3).bass_note(40, 52), 40, "arp", "h")
    for sg in segs:
        sg.expr(["timp", "pz_cb", "pz_hi"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])
        sg.expr(["glock", "celesta"], [(0, -12), (sg.n_q, -12)])
    st.pad(["vla", "vln2", "vln1"], 3, 59, 76, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    st.add("harp", 0, 3, "E3", 40, "arp", "h")
    st.add("harp", 0.05, 2.95, "B3", 38, "arp")
    st.add("harp", 3, 3, "C3", 38, "arp")
    st.add("harp", 3.05, 2.95, "G3", 36, "arp")
    st.expr(["harp"], [(0, -12), (6, -14)])
    st.expr(["vla", "vln2", "vln1", "vc"], [(0, -21), (6, -24)])


def storm(c):
    """The storm (G minor): out of the dark a gust on '忽然' (a plucked low G, timpani, a harp sweep, the tremolo
    swelling); a gust on each 呼 (bigger); the clouds race in -- rolling cellos, tremolo, low brass, a timpani roll
    (Gm Eb Cm D), the surge in the pause; the waves (low brass swells); a splash on each 哗啦 (bass drum, timpani,
    soft cymbal, a harp sweep down) where the narrator says 哗 (the picture's splashes), a spray on 啦, and the water
    rising (Gm F/A Gm/Bb Cm D).  The gusts and splashes follow the picture's whooshes and splashes where the scene
    has them (the first gust half-way between the picture and the spoken 呼, which lie a few frames apart)."""
    c.gain(-2.8)
    t_hu = c.at("呼——呼——")
    t_cloud = c.at("乌云跑过来")
    t_w = c.gap(c.find("浪一个接一个"))
    t_sp = c.at("哗啦！哗啦！")
    hu = syl(c, "呼——呼——", 2)
    wa = syl(c, "哗啦！哗啦！", 2)
    p_gust = [pic(c, "whoosh", None, k) for k in range(3)]   # 忽然, 呼, 呼 (picture)
    p_hu1 = p_gust[1] if p_gust[1] is not None and abs(p_gust[1] - t_hu) <= 0.09 else None
    t_g1 = (t_hu + p_hu1) / 2 if p_hu1 is not None else t_hu
    p_hu2 = p_gust[2] if p_gust[2] is not None and t_g1 + 0.25 <= p_gust[2] <= t_cloud - 0.25 else None
    hu2 = p_hu2 if p_hu2 is not None else min(max(hu[1] if len(hu) > 1 else t_hu + 0.6, t_g1 + 0.35), t_cloud - 0.25)
    p_sp = [pic(c, "splash", "浪一个接一个", k) for k in range(2)]  # the splashes on 哗 (picture), else as spoken
    sp1 = p_sp[0] if p_sp[0] is not None else min(wa[0], t_sp)
    sp2 = p_sp[1] if p_sp[1] is not None else (wa[1] if len(wa) > 1 and wa[1] >= sp1 + 0.4 else c.at("哗啦！船里"))
    # the water pours in from the first splash on, if that leaves the waves room (else from the phrase)
    t_s = sp1 if t_w + 2.3 <= sp1 <= t_sp + 0.3 else t_sp
    g = c.seg(0, t_g1, 1, "4/4", "G minor", nominal=80, label="storm-gust")
    h = c.seg(t_g1, t_cloud, 1, "2/4", "G minor", nominal=92, label="storm-whoo")
    r = c.seg(t_cloud, t_w, 2, "4/4", "G minor+", nominal=160, label="storm-clouds")
    w = c.seg(t_w, t_s, 2, "4/4", "G minor+", nominal=164, label="storm-waves")
    s = c.seg(t_s, c.dur, 2, "4/4", "G minor+", nominal=124, label="storm-splash")
    segs = (g, h, r, w, s)
    g.duck(2.0)
    h.duck(2.5)
    r.duck(5.5)
    for sg in (w, s):
        sg.duck(6.5)
    g.prog("Gm:4")
    h.prog("Gm:2")
    r.prog("Gm:2 Eb:2 | Cm:2 D:2")
    w.prog("Gm:2 Eb:2 | Cm:2 D7:2")
    s.prog("Gm:2 F/A:2 | Gm/Bb:1 Cm:1 D:2")
    # out of the dark: a low murmur; '忽然': the first gust
    t0 = c.ls(0)
    q0 = qpos(g, c, t0, 0.3, 3.2)
    g.add("trem_lo", 0, 4, "G2", 40, "pad", voice="trem_lo.0")
    g.add("trem_va", 0, 4, "D3", 38, "pad", voice="trem_va.0")
    g.add("cb", 0, 4, "G1", 38, "bass")
    gust(g, q0, dur_s=0.7, vel=52, lo=50, hi=79)
    g.add("okit", q0, 1, 36, 44, "perc", "h")
    g.sync("'忽然': a sudden gust", q0, t0)
    if p_gust[0] is not None and abs(p_gust[0] - t0) <= 0.04:
        g.sync("the first gust (picture)", q0, p_gust[0])
    elif p_gust[0] is not None:
        accent(c, segs, p_gust[0], "the first gust (picture)", pluck=(55, 67), harp=(67, 79), vel=50)
    g.expr(["trem_lo", "trem_va", "cb"], [(0, -26), (q0, -22), (q0 + 1.2, -17), (4, -16)])
    g.expr(["harp", "pz_lo", "pz_cb", "pz_hi", "timp"], [(0, -11), (4, -11)])
    g.expr("okit", [(0, -13), (4, -13)])
    # 呼 —— 呼 ——: a gust on each, the second bigger
    h.add("trem_lo", 0, 2, "G2", 44, "pad", voice="trem_lo.0")
    h.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 74, vel=42, bass_ref=(31, 43))
    h.add("cb", 0, 2, "G1", 42, "bass")
    q2 = qpos(h, c, hu2, 0.35, 1.7)
    dur1 = max(0.12, min(0.45, h.t(q2) - h.t(0) - 0.12))   # the first sweep ends before the second 呼
    gust(h, 0, dur_s=dur1, vel=50, lo=52, hi=81, back=False, cym=40)
    gust(h, q2, dur_s=0.45, vel=60, lo=55, hi=84, back=False, cym=46)
    h.sync("'呼': gust 1", 0, t_hu)
    if p_hu1 is not None:
        h.sync("the wind whooshes (picture)", 0, p_hu1)
    elif p_gust[1] is not None and abs(p_gust[1] - hu2) > 0.15:   # the picture's whoosh away from both gusts
        accent(c, segs, p_gust[1], "the wind whooshes (picture)", pluck=(55, 67), harp=(67, 79), vel=50)
    h.sync("the second gust (picture)" if p_hu2 is not None else "'呼': gust 2", q2, hu2)
    if p_gust[2] is not None and p_hu2 is None:
        accent(c, segs, p_gust[2], "the second gust (picture)", pluck=(55, 67), harp=(67, 79), vel=52)
    h.mel("horn", f"D4:{q2:.6f} G4:{2 - q2:.6f}", vel=48, role="pad")
    h.expr(["trem_lo", "trem_va", "trem_hi", "cb"], [(0, -18), (q2, -16), (2, -14)])
    h.expr(["horn"], [(0, -21), (q2, -18), (2, -16)])
    h.expr(["harp", "pz_lo", "pz_cb", "pz_hi", "timp"], [(0, -10), (2, -10)])
    h.expr("okit", [(0, -12), (2, -12)])
    # 'the dark clouds raced in and covered the moon': rolling cellos, tremolo, low brass, a timpani roll
    q_le0 = r.q_of(c.t0 + c.le(0))
    for sg, v in ((r, 56), (w, 56)):
        rolling(sg, 0, 8, vel=v, lo=36, hi=60)
        sg.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 76, vel=50, bass_ref=(28, 40))
        bassline(sg, "cb_fast", 28, 40, 54)
        sg.pad(["tbn", "tbn", "horn"], 3, 46, 65, vel=50, bass_ref=(28, 40))
    troll(r, 0, min(7.7, max(1.0, q_le0 - 0.2)), midi("G2"), 30, 44)
    if q_le0 < 7.0:
        troll(r, q_le0, 7.85, midi("D2"), 44, 62)
        roll(r, q_le0, 7.9, 59, 14, 34, rate=12)               # a soft suspended cymbal into the waves
    r.add("timp", 0, 0.5, "G2", 50, "timp", "h")
    r.add("pz_cb", 0, 0.5, "G1", 52, "bass", "h")
    loud = ["vc_fast", "cb_fast", "trem_va", "trem_hi", "tbn", "horn", "timp"]
    for p in loud:
        brass = p in ("tbn", "horn")
        r.expr(p, [(0, -15 if brass else -13), (max(0.5, q_le0 - 0.6), -16 if brass else -14),
                   (min(7.6, q_le0 + 0.4), -9 if brass else -8), (8, -8 if brass else -7)])
    r.expr("okit", [(0, -14), (8, -12)])
    # 'wave after wave crashed into the boat': the waves -- a low brass swell for each
    w.add("timp", 0, 0.5, "G2", 54, "timp", "h")
    w.add("okit", 0, 1, 36, 44, "perc", "h")
    waves = [t for t in (pic(c, "splash_small", "浪一个接一个", k) for k in range(3)) if t is not None]
    if not waves:                                          # no picture: the timpani rolls under the waves
        troll(w, 0.5, 3.8, midi("G2"), 30, 42)
        troll(w, 4.2, 7.8, midi("D2"), 32, 48)
    q_ls1 = w.q_of(c.t0 + c.ls(1))
    for p in loud:
        brass = p in ("tbn", "horn")
        pts = [(0, -8 if not brass else -9), (max(0.3, q_ls1), -14 if not brass else -16)]
        pts += [(2.5, -15 if not brass else -14), (4, -14 if not brass else -16), (6.5, -14 if not brass else -14),
                (8, -14 if not brass else -16)]
        w.expr(p, pts)
    w.expr("okit", [(0, -12), (8, -12)])
    for k, t in enumerate(waves):                          # wave after wave breaks over the side (picture)
        sg, q = seg_at(c, segs, t)
        ch = sg.chord_at(q + 1e-3)
        pluck_chord(sg, q, vel=58 + 2 * k, lo=55, hi=67)
        sg.add("pz_cb", q, _dq(sg, q, 0.5), ch.bass_note(31, 43), 56 + 2 * k, "bass", "h")
        sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(ch, ch.bass_note(38, 50)), 52 + 2 * k, "timp", "h")
        sg.add("okit", q, 1, 57, 40 + 2 * k, "perc", "h")
        gliss_in(sg, "harp", q + 0.02, 0.3, midi("G4"), midi("G6"), up=False, v0=46, v1=36, scale=ChordTones(ch))
        sg.sync(f"a wave breaks over the side ({k + 1})", q, t)
    # 哗啦！哗啦！: a splash on each 哗 (the picture), a spray on 啦; the water in the boat rising
    rolling(s, 0, 8, vel=54, lo=36, hi=60)
    s.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 76, vel=48, bass_ref=(28, 40))
    bassline(s, "cb_fast", 28, 40, 54)
    s.mel("horn", "D4:2 C4:2 | D4:1 Eb4:1 F#4:2", vel=50)
    s.mel("tbn", "Bb3:2 A3:2 | G3:1 G3:1 F#3:2", vel=46)
    for k, t in enumerate((sp1, sp2)):                     # a splash on each 哗
        sg, q = seg_at(c, segs, t)
        splash(sg, q, vel=64 + 2 * k)
        pic_k = p_sp[k] is not None and t == p_sp[k]
        sg.sync(f"the wave splashes in ('哗' {k + 1})" if pic_k else f"'哗啦': splash {k + 1}", q, t)
        if not pic_k and k == 0 and abs(t - t_sp) <= 0.04:
            sg.sync("'哗啦': the splash", q, t_sp)
    if min(abs(t_sp - sp1), abs(t_sp - sp2)) > 0.04:       # 啦: the spray (the phrase as the subtitles time it)
        sg, q_la = seg_at(c, segs, t_sp)
        pluck_chord(sg, q_la, vel=60, lo=62, hi=74)
        sg.add("pz_lo", q_la, _dq(sg, q_la, 0.25), sg.chord_at(q_la + 1e-3).bass_note(43, 55), 56, "arp", "h")
        sg.add("celesta", q_la, _dq(sg, q_la, 0.5), top(sg, q_la, 79, 91), 50, "arp", "h")
        sg.add("okit", q_la, 1, 57, 38, "perc", "h")
        gliss_in(sg, "harp", q_la + 0.02, 0.35, midi("D5"), midi("D7"), up=False, v0=46, v1=36,
                 scale=ChordTones(sg.chord_at(q_la + 1e-3)))
        sg.sync("'哗啦': the spray on 啦", q_la, t_sp)
    troll(s, 4.2, 7.85, midi("D2"), 30, 46)
    for p in ["vc_fast", "cb_fast", "trem_va", "trem_hi", "timp"]:
        s.expr(p, [(0, -11), (2.5, -15), (8, -13)])
    s.expr(["horn", "tbn"], [(0, -16), (4, -15), (8, -12)])
    s.expr(["harp", "pz_lo", "pz_cb", "pz_hi"], [(0, -9), (8, -10)])
    s.expr("okit", [(0, -11), (8, -12)])
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -12), (sg.n_q, -12)])
    for sg in (r, w):
        sg.expr(["harp", "pz_hi", "pz_cb"], [(0, -10), (sg.n_q, -10)])


def scared(c):
    """Panic (G minor, fast 4/4): a staccato ostinato in the cellos, the barcarolle frantic on the clarinet, woodblock
    ticks, a swell in the pause (low brass, a timpani roll); the stab on '抓紧' (Gm), bailing (Cm D: scoops); the water
    rising -- a chromatic bass G Ab A Bb B C under the scoops; rocking and sinking (6/8: Cm Gm/Bb Ab D, harp sweeps up
    and down, a falling horn)."""
    c.gain(-3.2)
    t_grab = c.at("抓紧")
    t_b = c.gap(c.find("他们拼命地舀水"))
    t_rock = c.at("小船摇来摇去")
    a = c.seg(0, t_grab, 5, "4/4", "G minor+", nominal=148, label="scared-panic")
    z = c.seg(t_grab, t_b, 3, "2/4", "G minor+", nominal=146, label="scared-grab")
    b = c.seg(t_b, t_rock, 3, "4/4", "G minor+", nominal=164, label="scared-bail")
    k = c.seg(t_rock, c.dur, 2, "6/8", "G minor+", nominal=94, label="scared-sinking")
    segs = (a, z, b, k)
    for sg in segs:
        sg.duck(4.0)
    a.prog("Gm:4 | Eb:4 | Cm:2 D:2 | Gm:2 Eb:2 | Cm:2 D7:2")
    z.prog("Gm:2 | Cm:2 | D:2")
    b.prog("Gm:2 Ab:2@G-phrygian | F/A:2 Gm/Bb:2 | G/B:2@C-harmonic Cm:2")
    k.prog("Cm:3/2 Gm/Bb:3/2 | Ab:3/2@G-phrygian D:3/2")
    # 'the disciples were terrified; many were fishermen, but they had never seen such a storm!'
    q_br = 19.7                                            # the swell draws breath just before '抓紧'
    rolling(a, 0, q_br, vel=52, lo=36, hi=60)
    a.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 72, q1=q_br, vel=44, bass_ref=(28, 40))
    bassline(a, "cb", 28, 40, 44, q1=q_br)
    a.mel("clar", "r:4 | G4:1/2 Bb4:1/2 Eb5:1/2 Bb4:1/2 G4:1/2 Bb4:1/2 G4:1 | "
                  "C5:1/2 Eb5:1/2 G5:1/2 Eb5:1/2 D5:1/2 F#5:1/2 A5:1/2 F#5:1/2 | "
                  "G5:1/2 D5:1/2 Bb4:1/2 D5:1/2 G5:1/2 Eb5:1/2 Bb4:1/2 G4:1/2 | "
                  "C5:1/2 Eb5:1/2 G5:1/2 Eb5:1/2 F#5:1 r:1", vel=52)
    for q in np.arange(0.5, 20, 1.0):                      # woodblock ticks on the off-beats (in the pauses)
        if not bool(a.score.speaking(a.t(q))):
            drum(a, q, 76, 40)
    q_le = a.q_of(c.t0 + c.le(0))
    a.pad(["tbn", "tbn", "horn"], 3, 46, 65, q0=16, q1=q_br, vel=50, bass_ref=(28, 40))
    troll(a, max(12.0, min(17.0, q_le - 1.0)), 19.45, midi("D2"), 30, 58)
    a.expr(["vc_fast"], [(0, -13), (max(0.5, q_le - 0.5), -13), (min(19.5, q_le + 0.3), -13), (20, -13)])
    a.expr(["trem_va", "trem_hi", "cb"], [(0, -15), (max(0.5, q_le - 0.5), -15), (min(19.5, q_le + 0.3), -13),
                                          (20, -13)])
    a.expr(["clar"], [(0, -15), (20, -15)])
    a.expr(["tbn", "horn"], [(16, -18), (max(16.5, q_le), -16), (min(19.6, q_le + 0.5), -14), (20, -14)])
    a.expr(["timp"], [(0, -12), (20, -9)])
    a.expr("hand", [(0, -14), (20, -14)])
    t_mem = pic(c, "chime", "门徒们吓坏了")                   # a memory of calm fishing days (picture) ...
    if t_mem is not None:
        accent(c, segs, t_mem, "a memory of calm fishing (a chime)", celesta=(79, 91), harp=(67, 79), glock=(86, 98),
               vel=48)
    t_pop = pic(c, "pop", "门徒们吓坏了")                     # ... that pops: back in the storm
    if t_pop is not None:
        sg, q = accent(c, segs, t_pop, "the memory pops (back in the storm)", pluck=(60, 72), vel=50)
        drum(sg, q, 76, 50)
    for k_ in range(2):                                    # two big waves (picture)
        t = pic(c, "splash", "门徒们吓坏了", k_, hi=t_grab - 0.3)
        if t is not None:
            sg, q = seg_at(c, segs, t)
            splash(sg, q, vel=56 + 2 * k_, cym=True)
            sg.sync(f"a big wave ({k_ + 1})", q, t)
    scoops = [t for t in (pic(c, "splash_small", "抓紧", k_) for k_ in range(5)) if t is not None]
    # '抓紧！快把水舀出去！': the stab (Gm), bailing (scoops: on the picture's splashes, else on the beats)
    stab(z, 0, vel=56)
    z.sync("'抓紧': the stab (G minor)", 0, t_grab)
    rolling(z, 0.5, 6, vel=50, lo=36, hi=60)
    z.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 72, q0=0.5, vel=42, bass_ref=(28, 40))
    bassline(z, "cb", 28, 40, 42)
    def scoop(sg, q, vel=50):
        """A scoop of water thrown out: a quick pluck up the chord, a woodblock tick."""
        for j, dq in enumerate((0.0, 0.125, 0.25)):
            qq = min(q + dq, sg.n_q - 0.13)
            sg.add("pz_hi", qq, 0.125, top(sg, qq, 60, 79, j - 3), vel + 4 * (j == 0) + 2 * j, "arp", "s")
        drum(sg, q, 76, vel - 4)

    if len(scoops) >= 3:
        for k_, t in enumerate(scoops):
            sg, q = seg_at(c, segs, t)
            scoop(sg, q, vel=54)
            sg.sync(f"a scoop of water ({k_ + 1})", q, t)
    else:
        for q in (2.0, 3.0, 4.0, 5.0):
            scoop(z, q)
    z.expr(["vc_fast", "trem_va", "trem_hi", "cb"], [(0, -14), (6, -14)])
    z.expr(["timp", "horn", "tbn"], [(0, -9), (6, -11)])
    # 'they bailed with all their might, but the water kept rising': the chromatic rising bass, scoops, ticks
    rolling(b, 0, 12, vel=52, lo=36, hi=62)
    b.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 72, vel=44, bass_ref=(28, 44))
    bassline(b, "cb", 28, 44, 44)
    if len(scoops) < 3:
        for q in np.arange(1.0, 12, 2.0):
            scoop(b, q, vel=48)
    b.mel("horn", "Bb3:2 C4:2 | F4:2 G4:2 | G4:2 G4:2", vel=46, role="melody")
    b.expr(["vc_fast", "trem_va", "trem_hi", "cb"], [(0, -15), (12, -13)])
    b.expr(["horn"], [(0, -19), (12, -16)])
    # 'the boat rocked to and fro, as if it would sink': rocking, falling
    for q, up in ((0.0, True), (1.5, False), (3.0, True), (4.5, False)):
        ch = k.chord_at(q + 1e-3)
        gliss_in(k, "harp", q + 0.02, 0.5, midi("C4"), midi("C6"), up=up, v0=40, v1=50, scale=ChordTones(ch))
    k.mel("vc", "C3:3/2 Bb2:3/2 | Ab2:3/2 D3:3/2", vel=54, role="bass")
    k.mel("cb", "C2:3/2 Bb1:3/2 | Ab1:3/2 D2:3/2", vel=50, role="bass")
    k.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 72, vel=44, bass_ref=(32, 44))
    k.mel("horn", "Eb4:3/2 D4:3/2 | C4:3/2 A3:3/2", vel=48)
    troll(k, 4.6, 5.9, midi("D2"), 30, 42)
    k.expr(["vc", "cb", "trem_va", "trem_hi"], [(0, -14), (6, -15)])
    k.expr(["horn"], [(0, -16), (6, -16)])
    k.expr(["harp", "timp"], [(0, -10), (6, -12)])
    t_dip = pic(c, "splash", "小船摇来摇去")                  # the boat dips into a wave (picture)
    if t_dip is not None:
        sg, q = accent(c, segs, t_dip, "the boat dips into a wave", pluck=(55, 67), harp=(55, 67), low=True, vel=56)
        sg.add("pz_lo", q, _dq(sg, q, 0.25), sg.chord_at(q + 1e-3).bass_note(43, 55), 56, "arp", "h")
    for sg in segs:
        sg.expr(["pz_hi", "pz_cb", "pz_lo", "celesta", "glock"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -12), (sg.n_q, -12)])
    for sg in (z, b, k):
        sg.expr("hand", [(0, -14), (sg.n_q, -14)])


def wake(c):
    """The storm's tail (D); the lullaby island on '可是，耶稣还在睡觉' (G major: celesta, harp, soft high strings, a far
    low murmur of the storm); the storm returns as they wake him (G minor: rolling cellos, low tremolo, low brass);
    D7 held on '你不管吗' (the question: tremolo, a horn, a timpani roll)."""
    c.gain(-2.0)
    t_i = c.ls(0)
    t_wk = c.at("门徒们赶快叫醒他")
    t_care = c.at("你不管吗")
    d = c.seg(0, t_i, 1, "2/4", "G minor+", nominal=132, label="wake-tail")
    i = c.seg(t_i, t_wk, 2, "6/8", "G major", nominal=146, label="wake-island")
    w = c.seg(t_wk, t_care, 4, "4/4", "G minor+", nominal=168, label="wake-storm")
    q = c.seg(t_care, c.dur, 1, "2/4", "G minor+", nominal=90, label="wake-care")
    segs = (d, i, w, q)
    for sg in segs:
        sg.duck(2.5)
    w.duck(4.0)
    d.prog("D:2")
    i.prog(" | ".join(LULL_PROG[:2]))
    w.prog("Gm:2 Eb:2 | Cm:2 D:2 | Gm:2 Eb:2 | Cm:2 Am7b5:2")
    q.prog("D7:2")
    i.sync("'可是，耶稣还在睡觉': the lullaby island (G)", 0, t_i, kind="change")
    q.sync("'你不管吗': D7 (the question)", 0, t_care, kind="change")
    # the storm's tail through the dissolve
    d.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 69, vel=40, bass_ref=(38, 50))
    d.add("cb", 0, 2, "D2", 40, "bass")
    troll(d, 0, 1.9, midi("D2"), 36, 24)
    d.expr(["trem_va", "trem_hi", "cb", "timp"], [(0, -14), (2, -15)])
    # 'but Jesus was still asleep': the lullaby, a tiny warm island inside the storm
    i.mel("celesta", bars(LULL, 0, 2), vel=46)
    broken(i, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 43, 55, vel=32, thin=True)
    i.pad(["vla", "vln2", "vln1"], 3, 59, 76, vel=34, bass_part="vc", bass_lo=43, bass_hi=55)
    i.add("trem_lo", 0, 6, "G2", 30, "pad", voice="trem_lo.0")
    i.add("pz_cb", 0, 1.5, "G2", 32, "bass", "h")
    i.expr(["celesta"], [(0, -17), (1.5, -12), (6, -12)])
    i.expr(["harp", "pz_cb"], [(0, -17), (1.5, -12), (6, -12)])
    i.expr(["vla", "vln2", "vln1", "vc"], [(0, -23), (1.5, -20), (6, -20)])
    i.expr(["trem_lo"], [(0, -22), (6, -20)])
    # 'the disciples hurried to wake him: Teacher! Teacher! we are drowning!': the storm returns (kept low: words)
    rolling(w, 0, 16, vel=52, lo=36, hi=57)
    w.pad(["trem_va", "trem_va", "trem_va"], 3, 48, 65, vel=44, bass_ref=(28, 40))
    bassline(w, "cb", 28, 40, 44)
    w.pad(["tbn", "tbn", "horn"], 3, 43, 60, vel=44, bass_ref=(28, 40))
    w.add("timp", 0, 0.5, "G2", 50, "timp", "h")
    troll(w, 0.5, 7.8, midi("G2"), 28, 40)
    troll(w, 8.2, 15.8, midi("G2"), 28, 40)
    q_l1 = w.q_of(c.t0 + c.ls(1))
    for p in ["vc_fast", "trem_va", "cb", "tbn", "horn", "timp"]:
        w.expr(p, [(0, -15), (max(0.5, q_l1 - 1.0), -13), (max(0.6, q_l1), -16), (16, -16)])
    for k_ in range(2):                                    # they shake him: 'Teacher! Teacher!' (picture)
        t_sh = pic(c, "cloth", "老师", k_)
        if t_sh is not None:
            sg, q_sh = accent(c, segs, t_sh, f"they shake him ({k_ + 1})", pluck=(55, 67), vel=50)
            drum(sg, q_sh, 76, 46)
    t_wave = pic(c, "splash", "老师")                         # a wave crashes over the side (picture)
    if t_wave is not None:
        sg, q_wv = seg_at(c, segs, t_wave)
        splash(sg, q_wv, vel=54, cym=True)
        sg.sync("a wave crashes over the side", q_wv, t_wave)
    t_glow = pic(c, "chime", "可是", hi=t_wk)                 # the warm glow around the sleeping Jesus (picture)
    if t_glow is not None:
        accent(c, segs, t_glow, "the warm glow around the sleeping Jesus", celesta=(79, 91), glock=(86, 98),
               harp=(67, 79), vel=56)
    # '...don't you care?': D7 held -- tremolo, a horn, a timpani roll
    q.pad(["trem_va", "trem_va", "trem_va"], 3, 48, 65, vel=42, bass_ref=(38, 50))
    q.add("cb", 0, 2, "D2", 42, "bass")
    q.add("horn", 0, 2, "F#3", 42, "melody")
    q.add("pz_cb", 0, 0.5, "D2", 50, "bass", "h")
    q.add("pz_lo", 0, 0.5, "A2", 46, "bass", "h")
    roll_chord(q, 0, 50, 66, vel=44, n=4)
    troll(q, 0.3, 1.9, midi("D2"), 30, 40)
    q.expr(["trem_va", "cb"], [(0, -16), (2, -13)])
    q.expr(["horn"], [(0, -17), (2, -14)])
    q.expr(["pz_cb", "pz_lo", "harp", "timp"], [(0, -11), (2, -12)])
    for sg in segs:
        sg.expr(["pz_hi", "pz_lo", "pz_cb", "celesta", "glock", "harp"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])
        sg.expr("hand", [(0, -14), (sg.n_q, -14)])


def calm(c):
    """D7 still hanging; E-flat on '耶稣醒了' (his motif on the horn, a harp roll; Cm '站起来'); the storm's last surge
    (Ab Am7b5: rolling, tremolo, a timpani roll stopping just short); D on '住了吧' -- one strong short chord, and the
    storm stops dead; G on '静了吧' -- the second arrival (harp, plucked basses, a soft timpani) leading into stillness
    (G Cadd9/G G: very soft high strings, a slow harp); E-flat radiant on '月亮出来了' (high strings, choir 'ooh', a
    harp sweep), celesta stars on '星星又亮了'."""
    c.gain(-3.0)
    t_e = c.ls(0)
    t_say = c.at("对着风和海说")
    t_z = c.at("住了吧")
    t_j = c.at("静了吧")
    t_moon = c.at("月亮出来了")
    t_star = c.at("星星又亮了")
    d = c.seg(0, t_e, 1, "2/4", "G minor+", nominal=132, label="calm-question")
    e = c.seg(t_e, t_say, 1, "4/4", "G minor+", nominal=124, label="calm-wakes")
    s = c.seg(t_say, t_z, 1, "4/4", "G minor+", nominal=114, label="calm-surge")
    z = c.seg(t_z, t_j, 1, "3/8", "G minor+", nominal=144, label="calm-be-still")
    j = c.seg(t_j, t_moon, 3, "4/4", "G major", nominal=103, label="calm-stillness")
    m = c.seg(t_moon, c.dur, 2, "3/4", "Eb major", nominal=126, label="calm-moon")
    segs = (d, e, s, z, j, m)
    for sg in (d, e, s):
        sg.duck(2.5)
    z.duck(8.0)                                            # the two arrivals sit under Jesus's words
    j.duck(6.0)
    m.duck(1.5)
    d.prog("D7:2")
    e.prog("Eb:2 Cm:2")
    s.prog("Ab:2@G-phrygian Am7b5:2")
    z.prog("D:3/2")
    j.prog("G:4 | Cadd9/G:4 | G:4")
    m.prog("Eb:3 | Ebadd9:3")
    e.sync("'耶稣醒了': E-flat (Jesus wakes)", 0, t_e, kind="change")
    m.sync("'月亮出来了': the moon (E-flat, radiant)", 0, t_moon, kind="change")
    # the question still hanging
    d.pad(["trem_lo", "trem_va", "trem_va"], 3, 43, 65, vel=38, bass_ref=(38, 50))
    d.add("cb", 0, 2, "D2", 38, "bass")
    d.add("horn", 0, 2, "F#3", 38, "melody")
    d.expr(["trem_lo", "trem_va", "cb", "horn"], [(0, -14), (2, -16)])
    # 'Jesus woke and stood up': E-flat, his motif on the horn (the storm murmurs on, low)
    e.mel("horn", "G3:1 Bb3:1 Eb4:2", vel=52)
    roll_chord(e, 0, 39, 63, vel=44)
    e.pad(["vla", "vln2", "vln1"], 3, 55, 70, vel=36, bass_part="vc", bass_lo=36, bass_hi=51)
    e.add("trem_lo", 0, 4, "G2", 34, "pad", voice="trem_lo.0")
    e.add("pz_cb", 0, 0.5, "Eb2", 50, "bass", "h")
    e.expr(["horn"], [(0, -15), (4, -14)])
    e.expr(["harp", "pz_cb"], [(0, -11), (4, -12)])
    e.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (4, -16)])
    e.expr(["trem_lo"], [(0, -20), (4, -16)])
    # '...and spoke to the wind and the sea': the last surge (rolling, tremolo, a timpani roll stopping just short)
    q_le = s.q_of(c.t0 + c.le(0))
    q_br = 3.65                                            # the storm draws breath just before '住了吧'
    rolling(s, 0, q_br, vel=54, lo=36, hi=60)
    s.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 72, q1=q_br, vel=46, bass_ref=(32, 45))
    bassline(s, "cb", 32, 45, 46, q1=q_br)
    s.pad(["tbn", "tbn", "horn"], 3, 44, 63, q1=q_br, vel=46, bass_ref=(32, 45))
    troll(s, 0.2, 3.75, midi("A2"), 28, 46, rate=10)
    for p in ["vc_fast", "trem_va", "trem_hi", "cb", "tbn", "horn", "timp"]:
        s.expr(p, [(0, -16), (max(0.3, q_le - 0.3), -15), (min(3.0, q_le + 0.3), -13), (3.35, -14), (q_br, -21),
                   (4, -21)])
    s.expr("okit", [(0, -14), (4, -12)])
    # '住了吧！': D -- one strong short chord; the storm stops dead
    stab(z, 0, vel=58, dq=0.75, kit=False)
    z.pad(["vla", "vln2", "vln1"], 3, 50, 74, vel=48, art="s", bass_part="vc", bass_lo=38, bass_hi=50)
    z.sync("'住了吧': the storm stops (D)", 0, t_z)
    z.expr(["vla", "vln2", "vln1", "vc"], [(0, -12), (1.5, -14)])
    z.expr(["timp", "pz_cb", "pz_lo", "pz_hi", "horn", "tbn"], [(0, -9), (1.5, -10)])
    z.expr("okit", [(0, -11), (1.5, -12)])
    # '静了吧！': G -- the second arrival, into stillness
    j.add("pz_cb", 0, 1, "G2", 46, "bass", "h")
    j.add("timp", 0, 1, "G2", 34, "timp", "h")
    pluck_chord(j, 0, vel=56, lo=59, hi=71)
    for k_, nm in enumerate(["G3", "B3", "D4", "G4"]):              # the harp chord at once, then rolled on up
        j.add("harp", 0, 4, nm, 52, "arp", "h", voice=f"harp.{k_}")
    harp_roll(j, 0.25, ["B4", "D5", "G5"], vel=44)
    j.add("glock", 0, 2, "B6", 46, "arp", "h")
    j.add("celesta", 0, 2, "G6", 40, "arp", "h")
    j.sync("'静了吧': stillness (G)", 0, t_j)
    j.pad(["vla", "vln2", "vln1"], 3, 59, 79, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    j.add("cb", 0, 12, "G1", 34, "bass")
    broken(j, "harp", 4, 12, (0, 2, 4, 5, 4, 2), 43, 55, vel=30, thin=True)
    j.mel("celesta", "r:4 | E6:2 D6:2 | D6:2 B5:2", vel=32, role="arp")
    j.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (2, -19), (12, -20)])
    j.expr(["harp", "pz_cb", "timp", "glock", "pz_hi"], [(0, -10), (4, -13), (12, -13)])
    j.expr(["celesta"], [(0, -12), (2, -15), (12, -15)])
    # 'the moon came out, and the stars shone again': E-flat, radiant -- high strings, choir 'ooh', celesta stars
    gliss_in(m, "harp", 0.05, 0.5, midi("Eb4"), midi("Eb6"), v0=30, v1=42, scale=ChordTones(m.chord_at(0)))
    m.add("pz_cb", 0, 1, "Eb2", 42, "bass", "h")
    m.pad(["vla", "vln2", "vln1"], 3, 63, 84, vel=40, bass_part="vc", bass_lo=51, bass_hi=63)
    m.add("cb", 0, 6, "Eb2", 36, "bass")
    m.pad("ooh", 3, 58, 75, vel=36, bass_ref=(51, 63))
    times, sp = star_times(c, "星星又亮了", t_star, c.dur - 0.25, 5)
    stars(segs, c, times, lo=82, hi=98, vel=42, synced=sp, what="the stars shine again")
    for nm, phrase, k_, what, kw in (("cloth", "耶稣醒了", 0, "Jesus stands up",
                                     dict(pluck=(55, 67), harp=(62, 74), low=True)),
                                    ("chime", "耶稣醒了", 0, "Jesus raises his hand (a chime)",
                                     dict(celesta=(79, 91), glock=(86, 98))),
                                    ("chime", "风立刻停了", 0, "the moon appears (a chime)",
                                     dict(celesta=(79, 91), glock=(86, 98)))):
        t = pic(c, nm, phrase, k_)
        if t is not None and not (t_z - 0.3 <= t <= t_j + 0.3):       # nothing on top of the two arrivals
            accent(c, segs, t, what, vel=50, **kw)
    for sg in segs:
        sg.expr(["pz_hi", "celesta", "glock"], [(0, -12), (sg.n_q, -12)])
    m.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -20), (1.5, -15), (6, -15)])
    m.expr(["ooh"], [(0, -24), (1.5, -18), (6, -18)])
    m.expr(["harp", "pz_cb"], [(0, -11), (6, -12)])


def question(c):
    """Jesus turns to them, gently: his theme b1-b2 soft (G mixolydian: clarinet and guitar, harp); his question (C
    Am7 D7sus4: soft strings, the harp)."""
    c.gain(-2.2)
    t_q = c.gap(c.find("你们为什么这样害怕呢"))
    a = c.seg(0, t_q, 2, "3/4", "G mixolydian", nominal=84, label="question-turns")
    q = c.seg(t_q, c.dur, 2, "3/4", "G mixolydian", nominal=80, label="question-asks")
    for sg in (a, q):
        sg.duck(1.5)
    a.prog(" | ".join(JESUS_PROG[:2]))
    q.prog("C:3 | Am7:3/2 D7sus4:3/2")
    q.sync("'你们为什么这样害怕呢': his question (C)", 0, t_q, kind="change")
    theme(a, 0, 2, vel=50, part="clar")
    broken(a, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 43, 55, vel=34, thin=True)
    strings(a, vel=36, lo=55, hi=71)
    a.duck(5.0, parts=["clar", "guitar"])
    a.expr(["clar", "guitar"], [(0, -15), (6, -16)])
    a.expr(["harp"], [(0, -12), (6, -12)])
    a.expr(STR, [(0, -19), (6, -19)])
    roll_chord(q, 0, 48, 72, vel=42)
    q.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=45, bass_hi=57)
    q.add("cb", 0, 3, "C2", 32, "bass")
    q.add("cb", 3, 1.5, "A1", 32, "bass")
    q.add("cb", 4.5, 1.5, "D2", 32, "bass")
    q.add("harp", 3, 1.5, "E5", 32, "arp")
    q.add("harp", 4.5, 1.5, "A4", 32, "arp")
    q.expr(["harp"], [(0, -12), (6, -13)])
    q.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -19), (6, -20)])
    t_turn = pic(c, "cloth", "耶稣转过身来")                  # Jesus turns to them (picture)
    if t_turn is not None:
        accent(c, (a, q), t_turn, "Jesus turns to them", harp=(55, 67), pluck=(55, 67), vel=50)
    t_spk = pic(c, "sparkle", "你们为什么这样害怕呢")          # a gentle sparkle as he asks (picture)
    if t_spk is not None:
        accent(c, (a, q), t_spk, "a gentle sparkle", glock=(86, 98), vel=46)
    for sg in (a, q):
        sg.expr(["celesta", "glock"], [(0, -12), (sg.n_q, -12)])


def who(c):
    """Wonder and awe (Cadd9 Am7 D7sus4: harp shimmering, celesta, high tremolo, choir 'ooh'); E-flat add9 on
    '这到底是谁' (open, questioning: a harp roll, strings, horns); Fadd9 C/E ('连风和海都听他的话'); Am7 D7sus4 D7; G on
    '耶稣不只是他们的好老师' -- his motif on the horn, a harp sweep, strings and choir."""
    c.gain(-2.0)
    t_who = c.at("这到底是谁")
    t_wind = c.at("连风和海")
    t_d = c.gap(c.find("这一天"))
    t_j = c.at("耶稣不只是他们的好老师")
    a = c.seg(0, t_who, 2, "4/4", "G major", nominal=94, label="who-wonder")
    b = c.seg(t_who, t_wind, 1, "2/4", "Bb major", nominal=90, label="who-who")
    w = c.seg(t_wind, t_d, 1, "4/4", "C major", nominal=98, label="who-obey")
    d = c.seg(t_d, t_j, 1, "4/4", "G major", nominal=82, label="who-knew")
    e = c.seg(t_j, c.dur, 1, "4/4", "G major", nominal=92, label="who-jesus")
    segs = (a, b, w, d, e)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Cadd9:4 | Am7:2 D7sus4:2")
    b.prog("Ebadd9:2")
    w.prog("Fadd9:2 C/E:2")
    d.prog("Am7:2 D7sus4:1 D7:1")
    e.prog("G:4")
    b.sync("'这到底是谁': E-flat add9 (open)", 0, t_who, kind="change")
    e.sync("'耶稣不只是他们的好老师': G (his motif)", 0, t_j, kind="change")
    # 'amazed and in awe, they said to one another': shimmering
    broken(a, "harp", 0, 8, (2, 3, 5, 3), 48, 60, vel=30, step=0.25, thin=True)
    a.pad(["trem_hi", "trem_hi"], 2, 67, 84, vel=30, bass_ref=(43, 55))
    a.pad("ooh", 3, 57, 72, vel=30, bass_part="vc", bass_lo=43, bass_hi=55)
    a.mel("celesta", "r:1 G5:1 r:1 E6:1 | r:1 C6:1 r:1 D6:1", vel=34, role="arp")
    a.expr(["harp"], [(0, -14), (8, -14)])
    a.expr(["trem_hi"], [(0, -24), (8, -22)])
    a.expr(["ooh", "vc"], [(0, -22), (8, -20)])
    a.expr(["celesta"], [(0, -14), (8, -14)])
    # '这到底是谁？': open, questioning -- E-flat major 7
    harp_roll(b, 0, ["Eb2", "Bb2", "G3", "Bb3", "F4", "G4"], vel=46)
    b.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    b.pad("ooh", 3, 57, 74, vel=32, bass_ref=(39, 51))
    b.add("pz_cb", 0, 1, "Eb2", 48, "bass", "h")
    b.expr(["harp", "pz_cb"], [(0, -11), (2, -12)])
    b.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (2, -18)])
    b.expr(["ooh"], [(0, -21), (2, -21)])
    # '连风和海都听他的话！'
    w.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=36, bass_part="vc", bass_lo=40, bass_hi=53)
    w.pad("ooh", 3, 57, 74, vel=32, bass_ref=(40, 53))
    bassline(w, "cb", 28, 41, 34)
    w.add("harp", 0, 2, "G4", 34, "arp")
    w.add("harp", 2, 2, "G4", 32, "arp")
    w.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -18), (4, -19)])
    w.expr(["ooh"], [(0, -21), (4, -22)])
    w.expr(["harp"], [(0, -13), (4, -13)])
    # 'that day the disciples understood': a hymn (strings, horns)
    d.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(d, "cb", 28, 40, 34)
    d.pad(["horn", "horn"], 2, 50, 65, vel=36, bass_ref=(38, 50))
    d.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -18), (4, -18)])
    d.expr(["horn"], [(0, -20), (4, -19)])
    # 'Jesus was not only their good teacher': G -- his motif on the horn, a harp sweep, strings, choir
    e.mel("horn", "B3:1 D4:1 G4:2", vel=50)
    t_glow = pic(c, "chime", "这一天")                        # Jesus glows (picture)
    if t_glow is not None and t_j - 0.1 <= t_glow <= c.dur - 0.5:   # with the G arrival: the sweep there
        q_gl = qpos(e, c, t_glow, 0.0, 3.0)
        gliss_in(e, "harp", q_gl, 0.45, midi("G3"), midi("G5"), v0=30, v1=42,
                 scale=ChordTones(e.chord_at(q_gl + 1e-3)))
        e.add("pz_cb", q_gl, _dq(e, q_gl, 1.0), "G2", 44, "bass", "h")
        e.add("glock", q_gl, _dq(e, q_gl, 1.0), "B6", 44, "arp", "h")
        e.add("celesta", q_gl, _dq(e, q_gl, 1.0), "G6", 40, "arp", "h")
        e.sync("Jesus glows (a chime)", q_gl, t_glow)
    else:
        gliss_in(e, "harp", 0, 0.45, midi("G3"), midi("G5"), v0=30, v1=42, scale=ChordTones(e.chord_at(0)))
        e.add("pz_cb", 0, 1, "G2", 44, "bass", "h")
        if t_glow is not None:
            accent(c, segs, t_glow, "Jesus glows (a chime)", glock=(86, 98), celesta=(74, 86), vel=48)
    t_tw = pic(c, "sparkle", "这一天")                       # a twinkle around him (picture)
    if t_tw is not None:
        accent(c, segs, t_tw, "a twinkle around Jesus", glock=(88, 100), vel=46)
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -12), (sg.n_q, -12)])
    strings(e, vel=40, lo=57, hi=74)
    e.pad("ooh", 3, 57, 74, vel=34, bass_ref=(43, 55))
    e.duck(2.5, parts=["horn", "ooh"])
    e.expr(["horn"], [(0, -14), (4, -16)])
    e.expr(["harp", "pz_cb"], [(0, -11), (4, -12)])
    e.expr(STR, [(0, -16), (4, -18)])
    e.expr(["ooh"], [(0, -20), (4, -21)])


def arrive(c):
    """Dawn: the barcarolle in D on the flute (D G/D D C/D), the oars, the boat reaching the shore; the theme in D,
    bright and full, on '太阳出来了' (violins and flute, the guitar, a horn, strings, a harp sweep, glockenspiel
    sparkles); b3-b4, then the question ('到底是谁呢？': Bm7 Gadd9 A7sus4)."""
    c.gain(-2.4)
    t_sun = c.at("太阳出来了")
    t_e = c.gap(c.find("门徒们一边走下船"))
    a = c.seg(0, t_sun, 4, "6/8", "D mixolydian", nominal=120, label="arrive-dawn")
    s = c.seg(t_sun, t_e, 2, "3/4", "D mixolydian", nominal=126, label="arrive-sun")
    e = c.seg(t_e, c.dur, 4, "3/4", "D mixolydian", nominal=120, label="arrive-wonder")
    segs = (a, s, e)
    for sg in segs:
        sg.duck(1.5)
    a.prog("D:3 | G/D:3 | D:3 | C/D:3")
    s.prog("D:3 | C:3")
    e.prog("G:3 | D:3 | Bm7:3 | Gadd9:3/2 A7sus4:3/2@D-major")
    s.sync("'太阳出来了': the theme in full (D)", 0, t_sun, kind="change")
    # 'next morning the little boat came safely to the other side': the barcarolle at dawn
    a.mel("flute", " | ".join([BOAT[0], BOAT[1], BOAT[3], BOAT[2]]), vel=50, transpose=12)
    oars(a, 0, 12, vel=44)
    guitar(a, 0, 12, vel=38)
    a.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_ref=(38, 50))
    a.add("cb", 0, 12, "D2", 32, "bass")
    t_land = pic(c, "thud", "第二天早上")                     # the boat touches the shore (picture)
    if t_land is not None:
        accent(c, segs, t_land, "the boat reaches the shore", low=True, harp=(62, 74), vel=46)
    a.duck(5.0, parts=["flute", "guitar"])
    a.expr(["flute"], [(0, -16), (12, -15)])
    a.expr(["pz_lo", "guitar"], [(0, -14), (12, -13)])
    a.expr(["vla", "vln2", "vln1", "cb"], [(0, -21), (12, -20)])
    # 'the sun came up, the water sparkled': the theme in D, bright and full
    theme(s, 0, 2, vel=54, transpose=7)
    s.mel("vln_mel", bars(JESUS, 0, 2), vel=46, transpose=7)
    s.mel("horn", "F#3:3 | G3:3", vel=44, role="counter")
    gliss_in(s, "harp", 0, 0.45, midi("D4"), midi("D6"), v0=34, v1=50, scale=ChordTones(s.chord_at(0)))
    s.add("pz_cb", 0, 1, "D2", 50, "bass", "h")
    s.add("timp", 0, 0.5, "D3", 40, "timp", "h")
    broken(s, "harp", 1, 6, (0, 2, 4, 5, 4, 2), 38, 50, vel=34, thin=True)
    strings(s, vel=42, lo=57, hi=76, bass=(43, 55), cb=(31, 43))
    t_rise = pic(c, "chime", "第二天早上")                    # the sun comes up (picture)
    if t_rise is not None:
        accent(c, segs, t_rise, "the sun comes up (a chime)", celesta=(79, 91), vel=50)
    t_gl = c.at("湖水亮晶晶的")
    sp = [t for t in (pic(c, "sparkle", "第二天早上", k) for k in range(2)) if t is not None]
    glints = sp or [t_gl, t_gl + 0.35]
    for k, t in enumerate(glints[:3]):                     # the water sparkles
        sg, q = seg_at(c, segs, t)
        sg.add("glock", q, _dq(sg, q, 0.75), top(sg, q, 86, 100, -1 - (k % 2)), 48 - 2 * k, "arp", "h")
        if sp:
            sg.sync(f"the water sparkles ({k + 1})", q, t)
    s.duck(5.5, parts=["flute", "guitar", "vln_mel", "horn"])
    s.duck(2.5, parts=["glock", "harp"])
    s.expr(["flute", "vln_mel"], [(0, -15), (6, -15)])
    s.expr(["guitar", "horn"], [(0, -15), (6, -15)])
    s.expr(["harp", "pz_cb", "timp"], [(0, -10), (6, -11)])
    s.expr(STR, [(0, -16), (6, -16)])
    # 'the disciples stepped out, still wondering: Jesus -- who is he?': b3-b4, then the question
    theme(e, 2, 4, vel=50, transpose=7)
    e.mel("flute", "A5:1 B5:1 D6:1 | B5:3/2 D6:3/2", q=6, vel=48)
    e.mel("guitar", "A4:1 B4:1 D5:1 | B4:3/2 D5:3/2", q=6, vel=42, role="counter")
    broken(e, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 38, 50, vel=32, thin=True)
    strings(e, vel=38, lo=57, hi=74, bass=(43, 55), cb=(31, 43))
    e.duck(6.0, parts=["flute", "guitar"])
    e.duck(2.5, parts=["harp"])
    e.expr(["flute", "guitar"], [(0, -15), (12, -16)])
    e.expr(["harp"], [(0, -12), (12, -13)])
    e.expr(STR, [(0, -17), (12, -19)])
    for k in range(2):                                     # question marks pop up over the disciples (picture)
        t = pic(c, "pop", "门徒们一边走下船", k)
        if t is not None:
            sg, q = accent(c, segs, t, f"a question mark pops up ({k + 1})", celesta=(79 + 3 * k, 93 + 3 * k),
                           pluck=(67, 79), vel=48)
    for sg in segs:
        sg.expr(["glock", "celesta", "pz_hi"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])


def end(c):
    """The question to the child (Em7 Cadd9 Am7: a celesta, then only soft strings through the pause); G on
    '他就是耶稣' -- Jesus's theme b1-b4 (flute and guitar, harp, strings); b5-b8 warm (clarinet, a horn
    counter-melody, strings, choir 'ooh'); the last question (Cadd9 Em7, very soft); D7sus4 on the end of
    '想对耶稣说什么呢', hanging very softly through the pause (space for the child's answer); the final G major chord
    at the end, with the end card (the picture's chime; else as the scene's tail begins), ringing to the end."""
    c.gain(-2.6)
    t_he = c.at("他就是耶稣")
    t_p = c.gap(c.find("下次你害怕的时候"))
    t_q = c.gap(c.find("小朋友，你害怕的时候"))
    t_f = c.le(c.find("想对耶稣说什么呢"))
    t_card = pic(c, "chime", "小朋友，你害怕的时候", lo=t_f + 0.8, hi=c.dur - 0.6)    # the end card (picture)
    t_fin = t_card if t_card is not None else max(t_f + 0.8, c.dur - 1.3)
    a = c.seg(0, t_he, 2, "3/4", "G major", nominal=86, label="end-who")
    g = c.seg(t_he, t_p, 4, "3/4", "G mixolydian", nominal=124, label="end-jesus")
    p = c.seg(t_p, t_q, 4, "3/4", "G mixolydian", nominal=108, label="end-pray")
    q = c.seg(t_q, t_f, 2, "3/4", "G major", nominal=84, label="end-question")
    sp = c.seg(t_f, t_fin, 1, "2/4", "G major", nominal=58, label="end-space")
    f = c.seg(t_fin, c.dur, 1, "2/4", "G major", nominal=90, rit=0.3, label="end-final-chord")
    for sg in (a, g, p, q):
        sg.duck(1.5)
    a.prog("Em7:3 | Cadd9:3/2 Am7:3/2")
    g.prog(" | ".join(JESUS_PROG[:4]))
    p.prog(" | ".join(JESUS_PROG[4:8]))
    q.prog("Cadd9:3 | Em7:3")
    sp.prog("D7sus4:2")
    f.prog("G:2")
    g.sync("'他就是耶稣': G (Jesus's theme)", 0, t_he, kind="change")
    sp.sync("'想对耶稣说什么呢': D7sus4, the question hangs", 0, t_f, kind="change")
    f.sync("the final G major chord (the end card)", 0, t_fin, kind="change")
    f.sync("the end card: the final chord's harp roll" if t_card is not None else "the final chord: harp roll", 0,
           t_fin)
    # 'child, do you know who he is?': a celesta asks; then only soft strings in the pause
    a.mel("celesta", "B5:1 E6:1 D6:1 | E6:3/2 r:3/2", vel=38, role="arp")
    a.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(a, "cb", 28, 40, 34)
    a.add("harp", 0, 3, "E3", 34, "arp")
    a.add("harp", 3, 1.5, "C3", 32, "arp")
    a.expr(["celesta"], [(0, -13), (6, -15)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -18), (3, -17), (6, -17)])
    a.expr(["harp"], [(0, -13), (6, -14)])
    # 'he is Jesus, the Son of God; even the wind and the sea obey him': the theme
    theme(g, 0, 4, vel=52)
    broken(g, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 43, 55, vel=34, thin=True)
    roll_chord(g, 0, 43, 67, vel=38)
    strings(g, vel=38, lo=55, hi=71)
    g.duck(3.5, parts=["flute", "guitar"])
    g.expr(["flute", "guitar"], [(0, -19), (1.5, -15), (12, -15)])
    g.expr(["harp"], [(0, -15), (1.5, -12), (12, -12)])
    g.expr(STR, [(0, -19), (1.5, -18), (12, -17)])
    # 'next time you are afraid, remember Jesus is with you; you can pray to him': b5-b8, warm
    p.mel("clar", bars(JESUS, 4, 8), vel=52)
    p.mel("horn", "G3:3 | G3:3 | A3:3 | B3:3", vel=40, role="counter")
    broken(p, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 43, 55, vel=32, thin=True)
    strings(p, vel=38, lo=55, hi=72)
    p.pad("ooh", 3, 57, 72, vel=32, q0=3, bass_ref=(40, 55))
    p.duck(3.0, parts=["clar", "horn", "ooh"])
    p.expr(["clar"], [(0, -15), (12, -15)])
    p.expr(["horn"], [(0, -18), (12, -17)])
    p.expr(["harp"], [(0, -12), (12, -12)])
    p.expr(STR, [(0, -18), (12, -17)])
    p.expr(["ooh"], [(3, -24), (6, -20), (12, -20)])
    # 'child, when you are afraid, what would you like to say to Jesus?': very soft
    q.mel("celesta", "G5:1 D6:1 E6:1 | B5:3/2 D6:3/2", vel=36, role="arp")
    q.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=32, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(q, "cb", 28, 40, 30)
    q.add("harp", 0, 3, "E4", 32, "arp")
    q.add("harp", 3, 3, "G3", 30, "arp")
    q.expr(["celesta"], [(0, -14), (6, -16)])
    q.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -19), (6, -20)])
    q.expr(["harp"], [(0, -13), (6, -14)])
    # the space after the question: D7sus4 hanging, very soft (a low harp D as it begins)
    sp.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=30, bass_part="vc", bass_lo=50, bass_hi=62)
    sp.add("cb", 0, 2, "D2", 28, "bass")
    sp.add("harp", 0, 2, "D3", 36, "arp", "h")
    sp.add("harp", 0.06, 1.94, "A3", 32, "arp")
    sp.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -20), (1, -22), (2, -23)])
    sp.expr(["harp"], [(0, -13), (2, -15)])
    # the final G major chord: harp rolled up, the flute's G, celesta, strings, ooh -- ringing to the end
    f.mel("flute", "G5:2", vel=50)
    for k_, nm in enumerate(["G2", "D3", "G3", "B3", "D4", "G4", "B4", "D5", "G5"]):
        f.add("harp", 0.06 * k_, 2 - 0.06 * k_, nm, 46 - 2 * k_, "arp", "r")
    f.mel("celesta", "D6:1/2 G6:1/2 B6:1", vel=36, art="r", role="arp")
    strings(f, vel=40, lo=57, hi=72, q0=0.25)
    f.pad("ooh", 3, 57, 72, vel=38, q0=0.25, bass_ref=(43, 55))
    f.expr(["flute", "vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -17), (0.5, -16.5), (1.4, -19), (2, -27)])
    f.expr(["harp", "celesta", "glock"], [(0, -14), (2, -18)])
    # the picture: the picture-book corner appears; Jesus's picture glows; the glints; a gust at the window; she folds
    # her hands; a little speech bubble; the end card's chime in the final chord
    segs = (a, g, p, q, sp, f)
    for nm, phrase, what, kw in (("chime", "小朋友，你知道", "the picture-book corner appears (a chime)",
                                  dict(celesta=(79, 91), harp=(67, 79))),
                                 ("sparkle", "他就是耶稣", "Jesus's picture glows", dict(glock=(86, 98))),
                                 ("chime", "他就是耶稣", "'都听耶稣的话' (a chime)", dict(celesta=(79, 91))),
                                 ("sparkle", "下次你害怕的时候", "'记得耶稣就在你身边' (a glint)", dict(glock=(86, 98))),
                                 ("cloth", "下次你害怕的时候", "she folds her hands to pray",
                                  dict(harp=(62, 74), celesta=(79, 91), pluck=(60, 72))),
                                 ("pop", "小朋友，你害怕的时候", "a little speech bubble",
                                  dict(celesta=(79, 91), glock=(86, 98), pluck=(67, 79)))):
        t = pic(c, nm, phrase)
        if t is not None and (t_card is None or t < t_card - 0.2):
            accent(c, segs, t, what, vel=52 if nm in ("cloth", "pop") else 48, **kw)
    t_gust = pic(c, "whoosh", "下次你害怕的时候")             # the wind outside the window
    if t_gust is not None:
        sg, q_g = seg_at(c, segs, t_gust)
        gust(sg, q_g, dur_s=0.4, vel=34, lo=55, hi=79, attack=False, back=False)
    if t_card is not None:                                  # the end card's chime rings in the final chord
        f.add("glock", 0, f.n_q, "B6", 40, "arp", "r")
    for sg in segs:
        sg.expr(["glock", "pz_hi"], [(0, -12), (sg.n_q, -12)])


SCENE_CUES = {
    "s01_title": title, "s02_wind": wind, "s03_friends": friends, "s04_shore": shore, "s05_seed": seed,
    "s06_evening": evening, "s07_sleep": sleep, "s08_storm": storm, "s09_scared": scared, "s10_wake": wake,
    "s11_calm": calm, "s12_question": question, "s13_who": who, "s14_arrive": arrive, "s15_end": end,
}

# Hit points the score must place, defined by the narration text (audio/music_check.py REQUIRED_HITS format:
# (scene, phrase, mode, kind); mode 'line' / 'gap' / 'phrase' / 'end', kind 'hit' (attack) or 'change' (harmony)).
# Where a word is also an on-screen action (the twelve friends popping up...) the phrase is where the harmony
# arrives, and the attacks themselves follow the picture: PICTURE_HITS.
REQUIRED_HITS = [
    ("s02_wind", "今天的故事里", "gap", "change"),               # the boat (G)
    ("s02_wind", "遇到了好大好大的风浪", "phrase", "change"),    # the storm previewed (E minor)
    ("s03_friends", "十二个好朋友", "phrase", "change"),         # Jesus and his friends (G; the pops: picture)
    ("s03_friends", "他们当中", "gap", "change"),                # the fishermen's barcarolle (D)
    ("s04_shore", "大家都安安静静地听", "gap", "change"),        # the hush (Cadd9)
    ("s05_seed", "最小最小的种子", "phrase", "change"),          # F, tiny and high (the plings: picture)
    ("s05_seed", "长啊长", "phrase", "change"),                  # the seed grows, a step up (Dm7)
    ("s05_seed", "做窝", "phrase", "change"),                    # C, the nest (the birds' trill: picture)
    ("s06_evening", "我们渡到湖的那一边去吧", "gap", "change"),  # Jesus: let us go across (G)
    ("s07_sleep", "睡着了", "phrase", "change"),                 # the lullaby (G)
    ("s07_sleep", "星星一颗一颗地亮起来了", "phrase", "change"),  # the stars (Em7)
    ("s08_storm", "忽然", "line", "hit"),                        # a sudden gust
    ("s08_storm", "呼——呼——", "phrase", "hit"),                  # the first gust of 呼
    ("s08_storm", "哗啦！哗啦！", "phrase", "hit"),              # the first splash
    ("s09_scared", "抓紧", "phrase", "hit"),                     # the stab
    ("s10_wake", "耶稣还在睡觉", "line", "change"),              # the lullaby island (G)
    ("s10_wake", "你不管吗", "phrase", "change"),                # D7, the question
    ("s11_calm", "耶稣醒了", "line", "change"),                  # Jesus wakes (E-flat)
    ("s11_calm", "住了吧", "phrase", "hit"),                     # the storm stops (D)
    ("s11_calm", "静了吧", "phrase", "hit"),                     # stillness (G)
    ("s11_calm", "月亮出来了", "phrase", "change"),              # the moon (E-flat, radiant)
    ("s12_question", "你们为什么这样害怕呢", "gap", "change"),    # his question (C)
    ("s13_who", "这到底是谁", "phrase", "change"),               # who is this? (E-flat add9, open)
    ("s13_who", "耶稣不只是他们的好老师", "phrase", "change"),    # G, his motif
    ("s14_arrive", "太阳出来了", "phrase", "change"),            # the theme in full (D)
    ("s15_end", "他就是耶稣", "phrase", "change"),               # G, Jesus's theme
    ("s15_end", "想对耶稣说什么呢", "end", "change"),            # D7sus4: the question hangs (the final chord: picture)
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or
# None, index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation (all 15 scenes).
PICTURE_HITS = [
    ("s01_title", "chime", None, 0, 0.0, "hit", "the title appears (a glint)"),
    ("s01_title", "pop", "圣经绘本", 0, 0.0, "hit", "title character 1 pops in"),
    ("s01_title", "pop", "圣经绘本", 5, 0.0, "hit", "title character 6 pops in"),
    ("s01_title", "sparkle", None, 0, 0.0, "hit", "the title sparkles"),
    ("s02_wind", "hammer", "小朋友", 0, 0.0, "hit", "the window rattles ('哐' 1)"),
    ("s02_wind", "hammer", "小朋友", 1, 0.0, "hit", "the window rattles ('哐' 2)"),
    ("s02_wind", "chime", "今天的故事里", 0, 0.0, "hit", "the story book opens (a chime)"),
    ("s02_wind", "splash", "今天的故事里", 0, 0.0, "hit", "a wave splashes up (1)"),
    ("s02_wind", "splash", "今天的故事里", 1, 0.0, "hit", "a wave splashes up (2)"),
    ("s03_friends", "pop", "耶稣有十二个好朋友", 0, 0.0, "hit", "friend 1 pops up"),
    ("s03_friends", "pop", "耶稣有十二个好朋友", 11, 0.0, "hit", "friend 12 pops up"),
    ("s03_friends", "sparkle", "他们当中", 0, 0.0, "hit", "the fishermen light up"),
    ("s03_friends", "pop", "他们当中", 4, 0.0, "hit", "彼得 pops up"),
    ("s03_friends", "pop", "他们当中", 5, 0.0, "hit", "安得烈 pops up"),
    ("s03_friends", "pop", "他们当中", 6, 0.0, "hit", "雅各 pops up"),
    ("s03_friends", "pop", "他们当中", 7, 0.0, "hit", "约翰 pops up"),
    ("s03_friends", "splash", "以前每天", 0, 0.0, "hit", "the net lands in the water"),
    ("s03_friends", "pop", "他们最熟悉", 0, 0.0, "hit", "a fish spot pops up on the map"),
    ("s03_friends", "chime", "他们最熟悉", 0, 0.0, "hit", "they know the lake (a chime)"),
    ("s04_shore", "splash_small", "人太多了", 0, 0.0, "hit", "Jesus steps into the boat"),
    ("s05_seed", "chime", "那天", 0, 0.0, "hit", "the story picture appears (a chime)"),
    ("s05_seed", "sparkle", "芥菜种", 0, 0.0, "hit", "the tiny seed sparkles (1) ('最小')"),
    ("s05_seed", "sparkle", "芥菜种", 1, 0.0, "hit", "the tiny seed sparkles (2) ('最小')"),
    ("s05_seed", "pop", "芥菜种", 0, 0.0, "hit", "the seed goes into the earth (a low C)"),
    ("s05_seed", "grow", "芥菜种", 0, 0.0, "hit", "the sprout grows ('长啊长', the first step)"),
    ("s05_seed", "grow", "芥菜种", 1, 0.0, "hit", "the plant grows up (the third step)"),
    ("s05_seed", "sparkle", "芥菜种", 2, 0.0, "hit", "the big tree ('都大', C)"),
    ("s05_seed", "pop", "芥菜种", 1, 0.0, "hit", "a bird lands in the nest (the trill, '做窝')"),
    ("s06_evening", "thud", "我们渡到湖的那一边去吧", 0, 0.0, "hit", "the boat is pushed off"),
    ("s07_sleep", "thud", "门徒们把船划开了", 0, 0.0, "hit", "the boat pushes off"),
    ("s07_sleep", "cloth", "门徒们把船划开了", 1, 0.0, "hit", "Jesus lies down to sleep"),
    ("s07_sleep", "sparkle", "星星一颗一颗地亮起来了", 0, 0.0, "hit", "a star comes out (1)"),
    ("s07_sleep", "sparkle", "星星一颗一颗地亮起来了", 1, 0.0, "hit", "a star comes out (2)"),
    ("s08_storm", "whoosh", None, 0, 0.0, "hit", "the first gust ('忽然')"),
    ("s08_storm", "whoosh", None, 1, 0.0, "hit", "the wind whooshes (the first '呼')"),
    ("s08_storm", "whoosh", None, 2, 0.0, "hit", "the second gust (the second '呼')"),
    ("s08_storm", "splash_small", "浪一个接一个", 0, 0.0, "hit", "a wave breaks over the side (1)"),
    ("s08_storm", "splash_small", "浪一个接一个", 1, 0.0, "hit", "a wave breaks over the side (2)"),
    ("s08_storm", "splash_small", "浪一个接一个", 2, 0.0, "hit", "a wave breaks over the side (3)"),
    ("s08_storm", "splash", "浪一个接一个", 0, 0.0, "hit", "the wave splashes in ('哗' 1)"),
    ("s08_storm", "splash", "浪一个接一个", 1, 0.0, "hit", "the wave splashes in ('哗' 2)"),
    ("s09_scared", "chime", "门徒们吓坏了", 0, 0.0, "hit", "a memory of calm fishing (a chime)"),
    ("s09_scared", "pop", "门徒们吓坏了", 0, 0.0, "hit", "the memory pops (back in the storm)"),
    ("s09_scared", "splash", "门徒们吓坏了", 0, 0.0, "hit", "a big wave (1)"),
    ("s09_scared", "splash", "门徒们吓坏了", 1, 0.0, "hit", "a big wave (2)"),
    ("s09_scared", "splash_small", "抓紧", 0, 0.0, "hit", "a scoop of water (1)"),
    ("s09_scared", "splash_small", "抓紧", 1, 0.0, "hit", "a scoop of water (2)"),
    ("s09_scared", "splash_small", "抓紧", 2, 0.0, "hit", "a scoop of water (3)"),
    ("s09_scared", "splash_small", "抓紧", 3, 0.0, "hit", "a scoop of water (4)"),
    ("s09_scared", "splash_small", "抓紧", 4, 0.0, "hit", "a scoop of water (5)"),
    ("s09_scared", "splash", "小船摇来摇去", 0, 0.0, "hit", "the boat dips into a wave"),
    ("s10_wake", "chime", "可是", 0, 0.0, "hit", "the warm glow around the sleeping Jesus"),
    ("s10_wake", "cloth", "老师", 0, 0.0, "hit", "they shake him (1)"),
    ("s10_wake", "cloth", "老师", 1, 0.0, "hit", "they shake him (2)"),
    ("s10_wake", "splash", "老师", 0, 0.0, "hit", "a wave crashes over the side"),
    ("s11_calm", "cloth", "耶稣醒了", 0, 0.0, "hit", "Jesus stands up"),
    ("s11_calm", "chime", "耶稣醒了", 0, 0.0, "hit", "Jesus raises his hand (a chime)"),
    ("s11_calm", "chime", "风立刻停了", 0, 0.0, "hit", "the moon appears (a chime)"),
    ("s11_calm", "sparkle", "星星又亮了", 0, 0.0, "hit", "the stars shine again"),
    ("s12_question", "cloth", "耶稣转过身来", 0, 0.0, "hit", "Jesus turns to them"),
    ("s12_question", "sparkle", "你们为什么这样害怕呢", 0, 0.0, "hit", "a gentle sparkle"),
    ("s13_who", "chime", "这一天", 0, 0.0, "hit", "Jesus glows (a chime, '耶稣不只是他们的好老师')"),
    ("s13_who", "sparkle", "这一天", 0, 0.0, "hit", "a twinkle around Jesus"),
    ("s14_arrive", "thud", "第二天早上", 0, 0.0, "hit", "the boat reaches the shore"),
    ("s14_arrive", "chime", "第二天早上", 0, 0.0, "hit", "the sun comes up (a chime)"),
    ("s14_arrive", "sparkle", "第二天早上", 0, 0.0, "hit", "the water sparkles (1)"),
    ("s14_arrive", "sparkle", "第二天早上", 1, 0.0, "hit", "the water sparkles (2)"),
    ("s14_arrive", "pop", "门徒们一边走下船", 0, 0.0, "hit", "a question mark pops up (1)"),
    ("s14_arrive", "pop", "门徒们一边走下船", 1, 0.0, "hit", "a question mark pops up (2)"),
    ("s15_end", "chime", "小朋友，你知道", 0, 0.0, "hit", "the picture-book corner appears (a chime)"),
    ("s15_end", "sparkle", "他就是耶稣", 0, 0.0, "hit", "Jesus's picture glows"),
    ("s15_end", "chime", "他就是耶稣", 0, 0.0, "hit", "'都听耶稣的话' (a chime)"),
    ("s15_end", "sparkle", "下次你害怕的时候", 0, 0.0, "hit", "'记得耶稣就在你身边' (a glint)"),
    ("s15_end", "cloth", "下次你害怕的时候", 0, 0.0, "hit", "she folds her hands to pray"),
    ("s15_end", "pop", "小朋友，你害怕的时候", 0, 0.0, "hit", "a little speech bubble"),
    ("s15_end", "chime", "小朋友，你害怕的时候", 0, 0.0, "hit", "the end card: the final G major chord"),
]
