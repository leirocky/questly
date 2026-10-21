"""The background score for 挪亚方舟 (Genesis 6-9, ~4:29) -- one continuous piece in 14 cues.

Read by audio/score.py when the story is "noah" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework and orchestra as the Jonah, Daniel and David scores
(audio/scorekit.py, audio/scorelib.py): every cue starts at its scene's global start, is planned in whole bars
whose tempo follows the real line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap), never
to fixed times.  Hits that show an on-screen action (the elephants' stomps, the rabbits' hops, the saw and the
hammer, the door, the colours of the rainbow...) follow the PICTURE where the scene declares a sound-effect cue for
it: picture() reads the scene's own sfx cues at build time (engine.loader.build_scene(...).sfx_cues, the same
source as music_check's PICTURE_HITS), so they move when a scene is edited; the narration phrase then marks where
the harmony arrives (a 'change' in REQUIRED_HITS).  Without a scene that builds, those hits fall back to the
narrator's own voice: syl() aligns the recorded line's voice islands to the text (punctuation groups, with the
sound words 咚 扑扑扑 蹦蹦蹦 嘎吱嘎吱 叮叮当当 滴答 split into syllables) by a monotone least-squares match, so a hit
lands on the spoken 咚, not on a character interpolation that can be 0.2 s off; the subtitle-chunk interpolation
is the fallback when the clip is missing or does not match.

Themes
  Noah (F major, 4/4, a hymn -- horn or clarinet over strings; motif x = the steady rise 3-5-8 'A C F'):
     b1 F        A4 C5 F5--            b5 F        A4 C5 F5--
     b2 C  F     E5 D5 C5--            b6 Dm Bb    F5 E5 D5 C5
     b3 Bb F     D5 Bb4 C5 A4          b7 Gm C7    Bb4 D5 C5 Bb4
     b4 Gm C     G4 A4 G4--            b8 F        A4------
  The building (C major): a busy pizzicato ostinato with woodblock ticks; the saw on 嘎吱嘎吱 (guiro strokes, cello
     and bassoon pushing and pulling: low on 嘎, high on 吱); the hammer on 叮叮当当 (glockenspiel + celesta +
     woodblock: two high 'ting's, two lower 'tang's); the ark 'growing' (the ostinato climbs a register every bar
     over a rising bass C-D-E-F, a horn rising in long notes; three glockenspiel steps on '它有三层'); days
     passing (glockenspiel sun / celesta moon); a G7 run up into the C major cheer on '造好了'.
  The animal parade (B-flat major march, 4/4; instruments join as the animals arrive -- a horn call 'here they
     come', tuba + timpani + bass drum stomps on the elephants' 咚 咚 咚, flute flutters on the birds' 扑扑扑, a comic
     low-brass roar on 嗷呜, pizzicato hops on the rabbits' 蹦蹦蹦, then the march two by two: the tune in thirds,
     flute over clarinet):
     b1 Bb   F4 Bb4 D5 Bb4 F5- D5-       b3 Bb Eb  D5 F5 Bb5- G5 Eb5 G5-
     b2 F7   Eb5 C5 A4 C5 F5- Eb5-       b4 F  Bb  F5- C5- Bb4--
  The flood (D minor): drip pizzicato and celesta on 滴答, rolling strings and timpani on 哗啦啦, a rising bass with a
     horn in tenths on '越涨越高', a deceptive A7 -> B-flat lift as the ark floats ('方舟浮起来了', 6/8 rocking), the
     mountains covered (big, warm, never a stinger), a hushed close on '都不见了'.
  Inside the ark: a B-flat lullaby in 3/4 (celesta and harp, soft pizzicato raindrops on the roof), Noah's motif
     on the horn and a choir 'ooh' on '可是上帝一直记得挪亚'.
  The dove (F major, 6/8 flute): out (rising arpeggio), searching, back home to F -- twice (the second time it
     comes home on a glowing D major chord for the olive leaf); the third time the melody flies up and ends open,
     on the ninth of a B-flat add9 chord: it does not come back, hopeful.
  The rainbow (F major): a rising glockenspiel/celesta/harp scale, one note per colour band as it appears on the
     picture (红 F 橙 G 黄 A 绿 Bb 青 C 蓝 D 紫 E; the narrator's colour words without the scene), over a bass falling
     in thirds (F | Dm | Bb | Gm | C); the radiant tutti with choir 'ah', cymbal and timpani on F on '好漂亮啊'.

Tonal plan
  s01 title F (Noah b1-b2, clarinet, harp; a rainbow glint) -> s02 F, raindrops on the window (pizzicato,
  celesta) | D minor rolling swell on '哗啦啦' | F, the story (oboe), harp up to C on '四十天' -> s03 D minor 'long
  ago' (oboe, 3/4) | the quarrel (grumpy staccato bassoon, pushes and grabs, a clarinet squabble on A7) | G minor
  on '上帝看见了', a single celesta tear, half cadence on A -> s04 B-flat C ('可是，有一个人不一样') | F major,
  Noah's theme on the horn on '他的名字叫挪亚' (b1-b3, walking pizzicato: he walks with God) | b4-b5 on the
  clarinet, three harp plucks for 闪、含、雅弗 -> s05 B-flat: the golden light ('有一天') | God speaks: soft pads only
  (B-flat Gm Eb F; choir 'ooh', strings) | '一只大船？' a bassoon question (Dm Am), a far-away flute on '好远好远'
  | Noah obeys: theme b7-b8 on the horn (Gm C7 F), steady pizzicato steps on '一样一样' -> s06 C major building
  (ostinato, saw, hammer, growing, days, G7 run) | C major cheer on '造好了' -> s07 B-flat march: horn call, F7
  walk, the stomps on B-flat, birds (Eb Bb), the lion (Gm Eb, roar), the rabbits (Bb F), the march two by two
  (b1-b3), the food (Eb Bb Gm C7 -> F: the march modulates to F) -> s08 F: the family's eight steps (theme b1-b2,
  clarinet, walking pizzicato) | B-flat swell (God's hand: choir, harp) | F on '把门关上了', the gentle thunk
  on the door, a warm held chord -> s09 D minor: seven soft ticks ('七天以后') | drips on A | the pour on D minor
  | rising (Dm C/E F Gm A7) | B-flat 6/8 float | Dm Bb the mountains | Gm Dm hushed -> s10 B-flat lullaby 3/4 | Eb
  on '可是上帝一直记得挪亚' -> s11 the wind (Dm Gm) | the water goes down (a clarinet scale down over Bb F/A) |
  Ararat (C) | dove 1 out (F Bb Dm Gm C), home on F ('又飞回来了') | dove 2, D major on '橄榄叶' (Gm C F: '水退了')
  | dove 3 out, flies away: C -> B-flat add9, open -> s12 B-flat: God speaks (soft pads, Eb F) | '门打开了' the
  burst: the parade theme returns (brass, flutes, timpani, cymbal), hops, flutters, a run | Noah's theme on the
  horn at the altar (F) | plagal amen on '感谢上帝' (B-flat F) -> s13 F: God's covenant (soft pads) | the
  rainbow in the clouds (B-flat over C, harp shimmer) | the colours | the radiant tutti on '好漂亮啊' | God's
  promise (soft pads, Bb Gm C) -> s14 F: Noah's theme b1-b2 (flute, harp) | b5-b7 (clarinet, horn, strings,
  choir) | the parade's head on the celesta (so many animals) | the question (B-flat, C sus4, very soft) | the
  final F chord on the end of the question, ringing through the closing pause to the end.

All the music stays under the narration (Seg.duck, low expression levels); the loud moments are short and
child-safe (cheers, comic stomps and roars, a big warm flood without stingers); God's voice lines get only soft
sustained pads.
"""
from fractions import Fraction

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
    timp_roll,
)
from audio.theory import midi

# ------------------------------------------------------------------------------------------- themes
NOAH = ["A4:1 C5:1 F5:2", "E5:1 D5:1 C5:2", "D5:1 Bb4:1 C5:1 A4:1", "G4:1 A4:1 G4:2",
        "A4:1 C5:1 F5:2", "F5:1 E5:1 D5:1 C5:1", "Bb4:1 D5:1 C5:1 Bb4:1", "A4:4"]
NOAH_PROG = ["F:4", "C:2 F:2", "Bb:2 F:2", "Gm:2 C:2", "F:4", "Dm:2 Bb:2", "Gm:2 C7:2", "F:4"]

PARADE = ["F4:1/2 Bb4:1/2 D5:1/2 Bb4:1/2 F5:1 D5:1", "Eb5:1/2 C5:1/2 A4:1/2 C5:1/2 F5:1 Eb5:1",
          "D5:1/2 F5:1/2 Bb5:1 G5:1/2 Eb5:1/2 G5:1", "F5:1 C5:1 Bb4:2"]
PARADE_PROG = ["Bb:4", "F7:4", "Bb:2 Eb:2", "F:2 Bb:2"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…"
SOUND_CHARS = set("咚扑蹦滴答嘎吱叮当")      # sound words that are spoken (and hit) syllable by syllable
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
    """The groups of an utterance, with the sound words (咚, 扑扑扑, 嘎吱嘎吱...) split into their syllables."""
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
    """Cue-relative onsets of the n narration units (groups; sound words split into syllables) that start where
    `phrase` starts, as the narrator actually speaks them: the recorded clip's voice islands matched to the text
    in order (least squares against the subtitle-chunk interpolation); a unit whose match is more than 0.5 s off,
    or a clip that is missing or has too few islands, keeps the interpolation."""
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


def picture(c, name, t0=-1e9, t1=1e9):
    """Cue-relative times of this scene's own sound-effect cues called `name` between t0 and t1.  The scene
    authors key them to the animation, so a hit that shows an action follows the PICTURE: read at build time
    from the scene code, as music_check reads PICTURE_HITS.  None when the scene does not build (the caller then
    falls back to the narration)."""
    key = (c.id, round(c.t0, 4), tuple(c.lines))
    if key not in _PICTURE:
        try:
            from engine.loader import build_scene
            _PICTURE[key] = [(x["name"], float(x["at"])) for x in build_scene(c.id, c.score.tl).sfx_cues]
        except Exception:
            _PICTURE[key] = None
    cues = _PICTURE[key]
    if cues is None:
        return None
    return sorted(t for nm, t in cues if nm == name and t0 <= t <= t1)


def on_picture(c, name, t0, t1, n, fallback):
    """The first n picture cues `name` in [t0, t1] if the scene shows at least n of them, else fallback()."""
    ts = picture(c, name, t0, t1)
    return ts[:n] if ts is not None and len(ts) >= n else list(fallback())[:n]


def seg_at(c, segs, t):
    """(segment, q) of cue-relative time t among segs (a hit that lands in a neighbouring segment takes its chord)."""
    for sg in segs:
        if sg.t0 - 1e-6 <= c.t0 + t < sg.t1 - 1e-6:
            return sg, min(max(sg.q_of(c.t0 + t), 0.0), sg.n_q - 1e-3)
    sg = segs[0] if c.t0 + t < segs[0].t0 else segs[-1]
    return sg, (0.0 if sg is segs[0] and c.t0 + t < sg.t0 else sg.n_q - 0.1)


def qpos(seg, c, t, lo=0.0, hi=None):
    """q of cue-relative time t in seg, clamped to [lo, hi] (hi default: just before the segment end)."""
    hi = seg.n_q - 0.1 if hi is None else hi
    return min(max(seg.q_of(c.t0 + t), lo), hi)


# ------------------------------------------------------------------------------------------- helpers
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
    ch = seg.chord_at(q + 1e-3)
    for k, p in enumerate(ch.tones(lo, hi)[:n]):
        seg.add(part, q, _dq(seg, q, 0.5), p, vel, "harmony", "h", voice=f"{part}.{k}")


def thirds(seg, part, spec, q=0.0, vel=58, art=""):
    """A second voice for a tune of chord tones: the chord tone 3-9 semitones below each note (two by two)."""
    pos = q
    for tok in spec.split():
        if tok == "|":
            continue
        f = tok.split(":")
        d = float(Fraction(f[1]))
        flags = (f[2] if len(f) > 2 else "") + art
        if f[0] != "r":
            p = midi(f[0])
            ch = seg.chord_at(pos + 1e-3)
            cand = ch.tones(p - 9, p - 3)
            if cand:
                seg.add(part, pos, d, max(cand), vel, "harmony", flags.replace("a", "").replace("p", ""))
        pos += d


def walk(seg, part, q0, q1, lo, hi, vel=52, step=1.0, art="s", role="bass"):
    """Walking chord-tone steps (root, third, fifth, third...) on every `step` q."""
    q, k, last = q0, 0, None
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        if ch is not last:
            k = 0
        last = ch
        lad = [p for p in range(ch.bass_note(lo, hi), hi + 1) if p % 12 in ch.pcset]
        seg.add(part, q, min(step, q1 - q), lad[[0, 1, 2, 1][k % 4] if len(lad) > 2 else 0], vel, role, art)
        q += step
        k += 1


def oompah(seg, q0, q1, vel=54, bass="pz_cb", chord="pz_hi", lo=55, hi=67, blo=29, bhi=41):
    """March accompaniment: plucked basses on the strong beats, a short plucked chord on the off-beats."""
    q = q0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        beat = int(round((q % seg.bar_q) / seg.beat_q))
        if beat % 2 == 0:
            b = ch.bass_note(blo, bhi)
            if beat % 4 == 2 and seg.bar_q >= 4:
                fifth = [p for p in ch.tones(blo, bhi + 7) if (p - b) % 12 == 7]
                b = fifth[0] if fifth else b
            seg.add(bass, q, _dq(seg, q, seg.beat_q), b, vel, "bass", "s")
        else:
            for k, p in enumerate(ch.tones(lo, hi)[:3]):
                seg.add(chord, q, _dq(seg, q, 0.5), p, vel - 8, "harmony", "s", voice=f"{chord}.{k}")
        q += seg.beat_q


def snare(seg, q0, q1, vel=34, every=1.0, offset=1.0):
    """A soft concert snare on the off-beats (orchestral kit), a tiny ruff before each."""
    q = q0 + offset
    while q < q1 - 1e-6:
        seg.add("okit", q - 0.125, 0.1, 38, vel - 10, "perc", "h")
        seg.add("okit", q, 0.25, 38, vel, "perc", "h")
        q += 2 * every


def drops(seg, q0, q1, pos, lo=74, hi=88, vel=40, parts=("pz_hi", "celesta")):
    """Raindrops: short plucks / celesta drops at the given q offsets (chord tones high up, alternating)."""
    for k, dq in enumerate(pos):
        q = q0 + dq
        if q >= q1 - 1e-6:
            break
        ts = seg.chord_at(q + 1e-3).tones(lo, hi)
        p = ts[(k * 2 + 1) % len(ts)]
        part = parts[k % len(parts)]
        seg.add(part, q, _dq(seg, q, 0.25), p, vel - (6 if part == "celesta" else 0), "arp", "s")


def stomp(seg, q, vel=64, kit=True):
    """An elephant's stomp: timpani and plucked basses on the chord's bass, tuba, a concert bass drum."""
    ch = seg.chord_at(q + 1e-3)
    seg.add("timp", q, _dq(seg, q, 0.5), timp_pitch(ch, midi("Bb2")), vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q, 0.5), ch.bass_note(29, 41), vel - 2, "bass", "h")
    seg.add("tuba", q, _dq(seg, q, 0.5), ch.bass_note(29, 41), vel - 8, "bass", "h")
    if kit:
        seg.add("okit", q, 1, 36, vel - 8, "perc", "h")


def flutter(seg, q, vel=56, n=3, lo=82, hi=96):
    """A bird's flap: a quick flute flourish up the chord (and a celesta glint)."""
    for k in range(n):
        qq = q + 0.12 * k
        ts = seg.chord_at(qq + 1e-3).tones(lo, hi)
        seg.add("flute", qq, min(0.12, max(0.05, span_end(seg, qq + 1e-6) - qq)), ts[min(k, len(ts) - 1)],
                vel - 2 * k, "arp", "h" if k == 0 else "s")
    ts = seg.chord_at(q + 1e-3).tones(lo, hi)
    seg.add("celesta", q, _dq(seg, q, 0.25), ts[min(n, len(ts) - 1)], vel - 10, "arp", "h")


def hop(seg, q, k, vel=60):
    """A rabbit's hop: a pizzicato chord tone (climbing with k), a high woodblock."""
    ts = seg.chord_at(q + 1e-3).tones(65, 84)
    seg.add("pz_hi", q, _dq(seg, q, 0.25), ts[min(k, len(ts) - 1)], vel + 2 * k, "arp", "h")
    drum(seg, q, 76, vel - 6)


def thump(seg, q, vel=50, sync=None, t=None, kit=True):
    """A soft low accent (timpani, plucked basses, a bass drum) on tones common to the chord there and the chord
    a little later (it may sit just before a chord change)."""
    pcs = seg.chord_at(q + 1e-3).pcset & seg.chord_at(min(q + 0.4, seg.n_q - 1e-3)).pcset or seg.chord_at(q + 1e-3).pcset
    seg.add("timp", q, _dq(seg, q, 0.5), [p for p in range(38, 51) if p % 12 in pcs][0], vel, "timp", "h")
    seg.add("pz_cb", q, 0.4, [p for p in range(29, 41) if p % 12 in pcs][0], vel + 2, "bass", "h")
    if kit:
        seg.add("okit", q, 1, 36, vel - 8, "perc", "h")
    if sync:
        seg.sync(sync, q, t)


def gliss_in(seg, part, q, dur_s, lo, hi, **kw):
    """A harp glissando that stays inside its segment (shortened to the room left; none if under 0.12 s)."""
    room = seg.t(seg.n_q) - seg.t(q) - 0.03
    if room >= 0.12:
        gliss(seg, part, q, min(dur_s, room), lo, hi, **kw)


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """Noah's theme b1-b2 on the clarinet over harp and soft strings (F major); a glockenspiel glint (the rainbow
    on the title page)."""
    c.gain(-8.5)
    s = c.seg(0, c.dur, 2, "4/4", "F major", nominal=100, label="title")
    s.duck(1.0)
    s.duck(3.0, parts=["clar"])
    s.prog(" | ".join(NOAH_PROG[:2]))
    s.mel("clar", bars(NOAH, 0, 2), vel=62)
    broken(s, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 41, 53, vel=42)
    s.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=46, bass_part="vc", bass_lo=41, bass_hi=53)
    bassline(s, "cb", 29, 41, 40)
    glint = picture(c, "sparkle", 0.5, c.dur - 0.5)
    q_gl = min(max(s.q_of(c.t0 + glint[0]), 4.0), 7.5) if glint else 6.5
    s.add("glock", q_gl, _dq(s, q_gl, 1.0), "C7", 40, "arp", "r")          # C: in both the C and the F chord
    s.expr(["clar"], [(0, -9), (8, -10)])
    s.expr(["harp"], [(0, -8), (8, -9)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (1, -12), (8, -12)])
    s.expr(["glock"], [(0, -10), (8, -10)])


def rain(c):
    """Raindrops on the window (F major: pizzicato and celesta drops, soft strings) under the question; the rain
    pours on '哗啦啦' (D minor: rolling cellos, tremolo, a timpani roll, a harp sweep down on each 哗啦啦); the
    story begins (F, an oboe), a harp sweep up to C on '四十天'."""
    c.gain(-2.2)
    t_w = c.at("哗啦啦")
    t_s = c.gap(c.find("今天的故事里"))
    pours = on_picture(c, "splash_small", c.ls(0) - 0.3, c.le(0) + 0.3, 2, lambda: syl(c, "哗啦啦", 2))
    t_40 = on_picture(c, "sparkle", c.ls(1), c.dur, 1, lambda: [c.at("四十天")])[0]
    a = c.seg(0, t_w, 2, "4/4", "F major", nominal=100, label="rain-window")
    w = c.seg(t_w, t_s, 1, "4/4", "D minor", nominal=112, label="rain-pour")
    s = c.seg(t_s, c.dur, 3, "4/4", "F major", nominal=94, label="rain-story")
    for sg in (a, w, s):
        sg.duck(1.5)
    a.prog("F:2 Dm:2 | Bb:2 C:2")
    w.prog("Dm:2 Bb:2")
    s.prog("F:4 | Dm:2 Bb:2 | Gm:2 C:2")
    w.sync("'哗啦啦': the rain pours (D minor)", 0, t_w, kind="change")
    # 'have you ever seen very, very heavy rain?': drops on the window
    drops(a, 0, 8, [0.5, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 5.75, 6.5, 7.25, 7.75], vel=44)
    a.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_part="vc", bass_lo=41, bass_hi=53)
    a.expr(["pz_hi", "celesta"], [(0, -10), (8, -9)])
    a.expr(["vla", "vln2", "vc"], [(0, -18), (2, -15), (8, -14)])
    # 哗啦啦，哗啦啦: rolling cellos, tremolo, a harp sweep down on each, a soft timpani roll
    broken(w, "vc_fast", 0, 4, (0, 1, 2, 1), 38, 62, vel=50, step=0.25, accent=6, ring=False, art="s", role="arp")
    w.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 74, vel=48, bass_ref=(38, 50))
    bassline(w, "cb", 28, 40, 44)
    timp_roll(w, 0, 3.9, midi("D2"), 26, 40)
    for i_, t in enumerate(pours):
        sg, q = seg_at(c, (a, w, s), t)
        gliss_in(sg, "harp", q, 0.45, midi("D4"), midi("D6"), up=False, v0=46, v1=56,
              scale=ChordTones(sg.chord_at(q + 1e-3)))
        sg.add("pz_cb", q, _dq(sg, q, 0.5), sg.chord_at(q + 1e-3).bass_note(29, 41), 64, "bass", "h")
        sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(sg.chord_at(q + 1e-3), midi("D2")), 58, "timp", "h")
        pluck_chord(sg, q, vel=62, lo=62, hi=74)
        sg.add("okit", q, 1, 36, 48, "perc", "h")
        sg.sync(f"'哗啦啦' {i_ + 1} (the big drops)", q, t)
    w.expr(["vc_fast"], [(0, -16), (2, -14), (4, -15)])
    w.expr(["trem_va", "trem_hi", "cb"], [(0, -16), (1.5, -11), (4, -13)])
    w.expr(["timp", "harp", "pz_cb", "pz_hi"], [(0, -10), (4, -10)])
    w.expr("okit", [(0, -12), (4, -12)])
    # 'in today's story it rained and rained -- for how long? forty whole days!': the oboe, harp, strings
    s.mel("oboe", "C5:1 A4:1 C5:2 | F5:1 E5:1 D5:1 F5:1 | Bb4:1 D5:1 E5:1 C5:1", vel=54)
    broken(s, "harp", 0, s.n_q, (0, 2, 4, 2), 41, 53, vel=36, thin=True)
    strings(s, vel=40, lo=53, hi=70)
    q40 = qpos(s, c, t_40, 0.0, s.n_q - 0.3)
    gliss_in(s, "harp", q40, 0.4, midi("C4"), midi("C6"), v0=32, v1=48, scale=ChordTones(s.chord_at(q40 + 1e-3)))
    s.add("glock", q40, _dq(s, q40, 1.0), top(s, q40, 84, 96), 40, "arp", "h")
    s.duck(2.5, parts=["oboe", "harp"])
    s.expr(["oboe"], [(0, -12), (12, -12)])
    s.expr(["harp", "glock"], [(0, -9), (12, -10)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (12, -15)])


def world(c):
    """Long ago (D minor, an oboe in 3/4, harp); the quarrel (a grumpy staccato bassoon, pushes and grabs, a
    clarinet squabble on '天天吵架'); God is sad: G minor on '上帝看见了', a single celesta tear, half cadence on A."""
    c.gain(-2.6)
    t_q = c.at("他们不听")
    t_s = c.gap(c.find("上帝看见了"))
    push, grab = on_picture(c, "whoosh", c.ls(0) - 0.3, c.le(0), 2, lambda: syl(c, "你推我", 2))
    t_tear = on_picture(c, "drip", c.ls(1), c.dur, 1, lambda: [None])[0]
    a = c.seg(0, t_q, 2, "3/4", "D minor", nominal=84, label="world-long-ago")
    q = c.seg(t_q, t_s, 2, "4/4", "D minor+", nominal=96, label="world-quarrel")
    s = c.seg(t_s, c.dur, 1, "4/4", "D minor+", nominal=78, label="world-sorrow")
    for sg in (a, q, s):
        sg.duck(1.5)
    a.prog("Dm:3 | Bb:3")
    q.prog("Dm:2 A:2 | Dm:2 A7:2")
    s.prog("Gm:2 A:2")
    s.sync("'上帝看见了': God is sad (G minor)", 0, t_s, kind="change")
    # long, long ago: an oboe, harp
    a.mel("oboe", "A4:2 D5:1 | F5:2 D5:1", vel=54)
    broken(a, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 50, vel=36, thin=True)
    a.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_part="vc", bass_lo=38, bass_hi=50)
    a.duck(2.5, parts=["oboe"])
    a.expr(["oboe"], [(0, -12), (6, -12)])
    a.expr(["harp"], [(0, -9), (6, -10)])
    a.expr(["vla", "vln2", "vc"], [(0, -16), (6, -15)])
    # pushing and grabbing, quarrelling every day: a grumpy bassoon, plucked basses
    q.mel("bsn", "D3:1/2:s A2:1/2:s D3:1/2:s r:1/2 C#3:1/2:s E3:1/2:s A2:1 | "
                 "D3:1/2:s F3:1/2:s A3:1/2:s r:1/2 G3:1/2:s E3:1/2:s C#3:1/2:s A2:1/2:s", vel=58)
    q.mel("pz_cb", "D2:1 r:1 A1:1 r:1 | D2:1 r:1 A1:1 r:1", vel=52, role="bass")
    q.pad(["vla", "vln2"], 2, 52, 67, vel=36, bass_ref=(33, 45))
    for lbl, t in (("push ('你推我')", push), ("grab ('我抢你')", grab)):   # a shove and a grab
        sg, qq = seg_at(c, (a, q), t)
        drum(sg, qq, 77, 58)
        pluck_chord(sg, qq, vel=56, lo=57, hi=69)
        sg.add("okit", qq, 1, 36, 40, "perc", "h")
        sg.sync(lbl, qq, t)
    q.mel("clar", "E5:1/4 C#5:1/4 E5:1/4 C#5:1/4 G5:1/4 E5:1/4 C#5:1/4 A4:1/4", q=6, vel=50, art="s")
    q.expr(["bsn"], [(0, -11), (8, -11)])
    q.expr(["clar"], [(0, -14), (8, -16)])
    q.expr(["pz_cb", "pz_hi", "vla", "vln2"], [(0, -13), (8, -13)])
    q.expr(["hand", "okit"], [(0, -12), (8, -12)])
    # God saw it and was very sad: soft strings, a single falling tear (celesta)
    strings(s, vel=40, lo=55, hi=70, bass=(43, 55), cb=(31, 43))
    q_t = 2.5 if t_tear is None else min(max(qpos(s, c, t_tear), 2.0), s.n_q - 0.5)
    s.add("celesta", q_t, s.n_q - q_t, "A5", 40, "arp")
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -11), (2, -14), (4, -18)])
    s.expr(["celesta"], [(0, -10), (4, -10)])


def noah(c):
    """'But one man was different' (B-flat, C); Noah's theme on the horn as his name is said (F major), b2-b3 with
    walking pizzicato (he walks with God); b4-b5 on the clarinet, three harp plucks for his sons 闪、含、雅弗."""
    c.gain(-2.2)
    t_n = c.at("他的名字叫挪亚")
    t_l = c.gap(c.find("挪亚爱上帝"))
    t_s = c.gap(c.find("挪亚有三个儿子"))
    a = c.seg(0, t_n, 1, "4/4", "F major", nominal=92, label="noah-but")
    n = c.seg(t_n, t_l, 1, "4/4", "F major", nominal=96, label="noah-name")
    w = c.seg(t_l, t_s, 2, "4/4", "F major", nominal=90, label="noah-walks")
    s = c.seg(t_s, c.dur, 2, "4/4", "F major", nominal=96, label="noah-sons")
    for sg in (a, n, w, s):
        sg.duck(1.5)
    a.prog("Bb:2 C:2")
    n.prog(NOAH_PROG[0])
    w.prog(" | ".join(NOAH_PROG[1:3]))
    s.prog(" | ".join(NOAH_PROG[3:5]))
    n.sync("'他的名字叫挪亚': Noah's theme (F major)", 0, t_n, kind="change")
    # but there was one man who was different: a lift (harp, clarinet rising)
    a.mel("clar", "D5:2 E5:2", vel=50)
    gliss_in(a, "harp", 0.25, 0.5, midi("Bb3"), midi("Bb5"), v0=30, v1=44, scale=ChordTones(a.chord_at(0)))
    strings(a, vel=40, lo=53, hi=70)
    a.expr(["clar"], [(0, -14), (4, -12)])
    a.expr(["harp"], [(0, -10), (4, -10)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (4, -14)])
    # his name was Noah: the theme on the horn
    n.mel("horn", NOAH[0], vel=58, transpose=-12)
    broken(n, "harp", 0, 4, (0, 2, 4, 6, 4, 2), 41, 53, vel=38, thin=True)
    strings(n, vel=42, lo=55, hi=72)
    n.duck(2.0, parts=["horn"])
    n.expr(["horn"], [(0, -11), (4, -11)])
    n.expr(["harp"], [(0, -9), (4, -9)])
    n.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (4, -13)])
    # Noah loved God, listened to him, walked with him every day: b2-b3, walking pizzicato
    w.mel("horn", bars(NOAH, 1, 3), vel=58, transpose=-12)
    walk(w, "pz_lo", 0, 8, 41, 60, vel=52)
    w.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=40, bass_ref=(41, 53))
    w.duck(2.0, parts=["horn"])
    w.expr(["horn"], [(0, -11), (8, -11)])
    w.expr(["pz_lo"], [(0, -11), (8, -11)])
    w.expr(["vla", "vln2", "vln1"], [(0, -15), (8, -15)])
    # Noah had three sons, Shem, Ham and Japheth: b4-b5 on the clarinet, a pluck for every name
    s.mel("clar", bars(NOAH, 3, 5), vel=56)
    strings(s, vel=40, lo=53, hi=70)
    names = on_picture(c, "pop", c.ls(2) - 0.3, c.dur, 3, lambda: [c.at("闪"), c.at("含"), c.at("雅弗")])
    for k, t in enumerate(names):
        sg, q = seg_at(c, (a, n, w, s), t)
        sg.add("harp", q, _dq(sg, q, 0.75), top(sg, q, 72 + 3 * k, 76 + 4 * k, 0), 50 + 2 * k, "arp", "h")
        sg.add("glock", q, _dq(sg, q, 0.5), top(sg, q, 84 + 3 * k, 88 + 4 * k, 0), 42 + 2 * k, "arp", "h")
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, 60 + 3 * k, 64 + 4 * k, 0), 50, "arp", "h")
        sg.sync(f"son {k + 1} ({'闪含雅弗'[k] if k < 2 else '雅弗'})", q, t)
    s.duck(2.0, parts=["clar"])
    s.expr(["clar"], [(0, -12), (8, -12)])
    s.expr(["harp", "glock", "pz_hi"], [(0, -10), (8, -10)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -15)])


def command(c):
    """'One day' (B-flat, the golden light: harp, celesta); God speaks -- soft pads only (B-flat Gm Eb F; choir
    'ooh', strings); Noah wonders: a bassoon question on '一只大船？', a far-away flute on '好远好远'; Noah obeys:
    Noah's theme b7-b8 on the horn (Gm C7 F), steady pizzicato steps on '一样一样'."""
    c.gain(-1.4)
    t_g = c.gap(c.find("挪亚，地上"))
    t_h = c.gap(c.find("挪亚心想"))
    t_o = c.gap(c.find("可是，挪亚还是"))
    a = c.seg(0, t_g, 1, "4/4", "Bb major", nominal=72, label="command-one-day")
    g = c.seg(t_g, t_h, 4, "4/4", "Bb major", nominal=58, label="command-god")
    h = c.seg(t_h, t_o, 2, "4/4", "F major", nominal=74, label="command-boat")
    o = c.seg(t_o, c.dur, 2, "4/4", "F major", nominal=90, label="command-obeys")
    for sg in (a, g, h, o):
        sg.duck(1.5)
    a.prog("Bb:4")
    g.prog("Bb:4 | Gm:4 | Eb:4 | F:4")
    h.prog("Dm:2 Am:2 | Bb:2 C:2")
    o.prog(" | ".join(NOAH_PROG[6:8]))
    o.sync("'可是，挪亚还是…': Noah obeys (his theme, G minor)", 0, t_o, kind="change")
    # one day, God said to Noah: a golden shimmer
    gliss_in(a, "harp", 0.5, 0.6, midi("F3"), midi("F6"), v0=28, v1=42, scale=ChordTones(a.chord_at(0)))
    a.mel("celesta", "r:1 D6:1 F6:1 Bb6:1", vel=36, role="arp")
    a.pad(["vla", "vln2", "vln1"], 3, 58, 74, vel=38, bass_part="vc", bass_lo=46, bass_hi=58)
    a.expr(["harp", "celesta"], [(0, -11), (4, -12)])
    a.expr(["vla", "vln2", "vln1", "vc"], [(0, -14), (4, -16)])
    # God speaks: only soft sustained pads (choir 'ooh', high strings)
    g.pad("ooh", 3, 55, 72, vel=38, bass_ref=(39, 51))
    g.pad(["vla", "vln2", "vln1"], 3, 58, 76, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    g.duck(3.0)
    g.expr(["ooh"], [(0, -22), (2, -19), (16, -19)])
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (16, -18)])
    # 'A big boat? But the sea is so far away!': a bassoon question, a far-away flute
    h.mel("bsn", "r:1 D3:1/2:s F3:1/2:s A3:1/2:s r:1/2 C4:1/2:s E4:1/2:s", vel=56)
    h.mel("flute", "r:4 | F5:2 E5:1 G5:1", vel=44)
    h.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    h.duck(2.0, parts=["bsn", "flute"])
    h.expr(["bsn"], [(0, -11), (8, -11)])
    h.expr(["flute"], [(0, -16), (4, -14), (8, -15)])
    h.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (8, -17)])
    # but Noah did everything just as God said, one thing after another: b7-b8 on the horn, steady steps
    o.mel("horn", bars(NOAH, 6, 8), vel=58, transpose=-12)
    walk(o, "pz_lo", 0, 4, 43, 62, vel=50)
    o.add("pz_lo", 4, 1, "F2", 48, "bass", "s")
    broken(o, "harp", 4, 8, (0, 2, 4, 6, 4, 2), 41, 53, vel=36, thin=True)
    strings(o, vel=40, lo=53, hi=70)
    o.duck(2.0, parts=["horn"])
    o.expr(["horn"], [(0, -11), (8, -12)])
    o.expr(["pz_lo", "harp"], [(0, -11), (8, -11)])
    o.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -15)])


def build(c):
    """The building (C major): the busy ostinato; the saw on 嘎吱嘎吱 (guiro, cellos and bassoon pushing and
    pulling); the hammer on 叮叮当当 (glockenspiel, celesta, woodblock); the ark growing (the ostinato climbing,
    a horn rising, three steps on '三层'); days passing (sun and moon); a G7 run into the cheer on '造好了'."""
    c.gain(-2.0)
    t_saw = c.at("锯木头")
    t_nail = c.at("钉钉子")
    t_g = c.gap(c.find("方舟好长好长"))
    t_d = c.gap(c.find("他们造啊造"))
    t_f = c.gap(c.find("终于"))
    t_done = c.at("造好了")
    v_saw = syl(c, "嘎吱嘎吱", 4)
    v_nail = syl(c, "叮叮当当", 4)
    strokes = on_picture(c, "ship_creak", c.ls(0) - 0.3, t_nail, 2, lambda: [v_saw[0], v_saw[2]])
    pull = min(0.24, max(0.12, v_saw[1] - v_saw[0]))           # 嘎 push on the stroke, 吱 pull just after
    nxt = strokes[1:] + [t_nail]
    saws = sorted(strokes + [min(t + pull, t2 - 0.1) for t, t2 in zip(strokes, nxt)])
    nails = on_picture(c, "coins", c.ls(0) - 0.3, c.le(0) + 0.4, 4, lambda: v_nail)
    a = c.seg(0, t_saw, 2, "4/4", "C major", nominal=126, label="build-start")
    s = c.seg(t_saw, t_nail, 1, "4/4", "C major", nominal=96, label="build-saw")
    n = c.seg(t_nail, t_g, 1, "4/4", "C major", nominal=90, label="build-nails")
    g = c.seg(t_g, t_d, 4, "4/4", "C major", nominal=100, label="build-grow")
    d = c.seg(t_d, t_f, 2, "4/4", "C major", nominal=116, label="build-days")
    f = c.seg(t_f, t_done, 1, "2/4", "C major", nominal=74, label="build-last")
    k = c.seg(t_done, c.dur, 1, "2/4", "C major", nominal=90, label="build-done")
    for sg in (a, s, n, g, d, f, k):
        sg.duck(1.5)
    a.prog("C:4 | G:2 C:2")
    s.prog("C:4")
    n.prog("C:2 G:2")
    g.prog("C:4 | Dm:2 G:2 | Em:2 Am:2 | F:2 G:2")
    d.prog("Am:2 F:2 | Dm:2 G:2")
    f.prog("G7:2")
    k.prog("C:2")
    k.sync("'造好了': the ark is finished (C major)", 0, t_done, kind="change")
    k.sync("'造好了': the cheer (timpani, cymbal)", 0, t_done)
    segs = (a, s, n, g, d, f, k)
    # Noah and his sons start building: the ostinato, a cheerful clarinet, a bouncy bassoon, woodblock ticks
    broken(a, "pz_hi", 0, 8, (0, 1, 2, 1), 60, 76, vel=48, step=0.5, ring=False, art="s")
    a.mel("bsn", "C3:1/2:s r:1/2 G2:1/2:s r:1/2 C3:1/2:s r:1/2 E3:1/2:s r:1/2 | "
                 "G2:1/2:s r:1/2 D3:1/2:s r:1/2 C3:1/2:s r:1/2 G2:1/2:s r:1/2", vel=56)
    a.mel("clar", "G4:1/2 C5:1/2 E5:1/2 G5:1/2 E5:1 C5:1 | D5:1/2 B4:1/2 G4:1 C5:2", vel=54)
    for q in range(8):
        drum(a, q, 76, 36 if q % 2 else 42)
    a.pad(["vla", "vln2"], 2, 55, 72, vel=36, bass_ref=(36, 48))
    a.duck(2.0, parts=["clar"])
    a.expr(["pz_hi", "bsn"], [(0, -12), (6, -12), (8, -14)])
    a.expr(["clar"], [(0, -13), (6, -13), (8, -16)])
    a.expr(["vla", "vln2"], [(0, -16), (8, -16)])
    a.expr("hand", [(0, -11), (8, -11)])
    # 锯木头，嘎吱嘎吱: the saw (a guiro stroke, a cello / bassoon push on 嘎, a pull on 吱)
    broken(s, "pz_hi", 0, 4, (0, 1, 2, 1), 60, 76, vel=42, step=0.5, ring=False, art="s", thin=True)
    s.pad(["vla", "vln2"], 2, 55, 72, vel=34, bass_ref=(36, 48))
    s.mel("pz_cb", "C2:1:s G1:1:s C2:1:s G1:1:s", vel=48, role="bass")
    for i_, t in enumerate(saws):
        sg, q = seg_at(c, segs, t)
        push = i_ % 2 == 0
        ch = sg.chord_at(q + 1e-3)
        drum(sg, q, 74 if push else 73, 70 if push else 56)
        p = ch.bass_note(48, 60) if push else ch.tones(52, 60)[-1]
        sg.add("vc_fast", q, _dq(sg, q, 0.25), p, 62 if push else 54, "bass", "h")
        sg.add("bsn", q, _dq(sg, q, 0.25), p - 12, 58 if push else 50, "bass", "h")
        if push:
            sg.add("pz_lo", q, _dq(sg, q, 0.25), p - 12, 60, "bass", "h")
            sg.sync(f"saw stroke {i_ // 2 + 1} ('嘎吱')", q, t)
    s.expr(["pz_hi", "pz_cb"], [(0, -11), (4, -11)])
    s.expr(["vc_fast", "bsn", "pz_lo"], [(0, -12), (4, -12)])
    s.expr(["vla", "vln2"], [(0, -15), (4, -15)])
    s.expr("hand", [(0, -10), (4, -10)])
    # 钉钉子，叮叮当当: the hammer (two high 'ting's, two lower 'tang's)
    broken(n, "pz_hi", 0, 4, (0, 1, 2, 1), 60, 76, vel=42, step=0.5, ring=False, art="s", thin=True)
    n.pad(["vla", "vln2"], 2, 55, 72, vel=36, bass_ref=(36, 48))
    bassline(n, "pz_cb", 31, 43, 46, art="s")
    for i_, t in enumerate(nails):
        sg, q = seg_at(c, segs, t)
        ting = i_ < 2
        p = top(sg, q, 84, 91) if ting else top(sg, q, 84, 91, 0)
        sg.add("glock", q, _dq(sg, q, 0.5), p, 58 if i_ % 2 == 0 else 50, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 0.5), p - 12, 48, "arp", "h")
        drum(sg, q, 76 if ting else 77, 60 if i_ % 2 == 0 else 52)
        sg.sync(f"hammer {i_ + 1} ('{'叮' if ting else '当'}')", q, t)
    n.expr(["pz_hi", "pz_cb"], [(0, -11), (4, -12)])
    n.expr(["glock", "celesta"], [(0, -11), (4, -11)])
    n.expr(["vla", "vln2"], [(0, -15), (2.5, -15), (4, -12)])
    n.expr("hand", [(0, -10), (4, -10)])
    # so long, longer than a football field! three decks, a door, a window: the ark grows
    for b in range(4):
        broken(g, "pz_hi", 4 * b, 4 * b + 4, (0, 1, 2, 1), 60 + 2 * b, 77 + 2 * b, vel=44 + 2 * b, step=0.5,
               ring=False, art="s", thin=True)
    g.mel("horn", "E4:4 | F4:2 G4:2 | G4:2 A4:2 | A4:2 B4:2", vel=52)
    g.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=38, bass_ref=(36, 48))
    bassline(g, "cb", 28, 40, 40)
    t3 = c.at("它有三层")
    for j in range(3):                                   # three decks: three glockenspiel steps up
        q = qpos(g, c, t3 + 0.28 * j, 0.0, g.n_q - 0.5)
        ts = g.chord_at(q + 1e-3).tones(79, 96)
        g.add("glock", q, _dq(g, q, 0.5), ts[min(j, len(ts) - 1)], 40 + 2 * j, "arp", "h")
    for q in range(0, 16, 2):
        drum(g, q, 76, 34)
    g.duck(2.0, parts=["horn"])
    g.expr(["pz_hi"], [(0, -14), (16, -11)])
    g.expr(["horn"], [(0, -20), (1.5, -15), (16, -12)])
    g.expr(["vla", "vln2", "vln1", "cb"], [(0, -13), (1.5, -16), (16, -14)])
    g.expr(["glock"], [(0, -10), (16, -10)])
    g.expr("hand", [(0, -13), (16, -13)])
    # they built and built, day after day: sun (glockenspiel) and moon (celesta), the hammer ticking on
    broken(d, "pz_hi", 0, 8, (0, 1, 2, 1), 64, 81, vel=46, step=0.5, ring=False, art="s", thin=True)
    for q in (0, 4):
        d.add("glock", q, _dq(d, q, 1.0), top(d, q, 84, 96), 38, "arp", "h")
        d.add("celesta", q + 2, _dq(d, q + 2, 1.0), top(d, q + 2, 72, 84, 0), 36, "arp")
    for q in range(8):
        drum(d, q, 76 if q % 2 == 0 else 77, 36)
    d.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=38, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(d, "cb", 28, 40, 38)
    d.expr(["pz_hi", "glock", "celesta"], [(0, -12), (8, -12)])
    d.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -14)])
    d.expr("hand", [(0, -13), (8, -13)])
    # 'at last' -- a run up over G7 and a timpani roll...
    f.mel("flute", "G5:1/4 A5:1/4 B5:1/4 C6:1/4 D6:1/4 E6:1/4 F6:1/4 G6:1/4", vel=48, art="s")
    f.mel("clar", "G4:1/4 A4:1/4 B4:1/4 C5:1/4 D5:1/4 E5:1/4 F5:1/4 G5:1/4", vel=48, art="s")
    timp_roll(f, 0, 1.9, midi("G2"), 26, 44)
    f.pad(["vla", "vln2", "vln1"], 3, 55, 76, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    f.expr(["flute", "clar"], [(0, -15), (2, -13)])
    f.expr(["timp"], [(0, -13), (2, -12)])
    f.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (2, -13)])
    # '...the ark is finished!': the cheer, C major (timpani, cymbal, horns, glockenspiel, a harp sweep)
    k.add("timp", 0, 0.5, "C3", 54, "timp", "h")
    k.add("okit", 0, 2, 57, 40, "perc", "h")
    k.add("pz_cb", 0, 0.5, "C2", 60, "bass", "h")
    k.add("glock", 0, 1, "C7", 46, "arp", "h")
    pluck_chord(k, 0, vel=58, lo=60, hi=72)
    gliss_in(k, "harp", 0, 0.35, midi("C4"), midi("C6"), v0=36, v1=50, scale=ChordTones(k.chord_at(0)))
    for j, nm in enumerate(["C4", "E4", "G4"]):
        k.add("horn", 0, 2, nm, 54, "pad", voice=f"horn.{j}")
    k.mel("flute", "E6:2", vel=50)
    strings(k, vel=44, lo=55, hi=76, bass=(36, 48), cb=(28, 40))
    k.duck(3.0)
    k.expr(["timp", "pz_cb", "pz_hi", "glock", "harp"], [(0, -12), (2, -13)])
    k.expr(["horn", "flute"], [(0, -14), (2, -15)])
    k.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (2, -15)])
    k.expr("okit", [(0, -12), (2, -12)])


def animals(c):
    """The animal parade (B-flat march): the horn call 'here they come'; the elephants (an F7 walk, the stomps on
    B-flat: tuba, timpani, bass drum on each 咚); the birds (flute flutters on 扑扑扑); the lion (G minor, the comic
    low-brass roar on 嗷呜); the rabbits (pizzicato hops on 蹦蹦蹦); the march two by two (the tune in thirds);
    the food (lighter, an oboe; Eb Bb Gm C7 -> F, the march modulating into the next page's key)."""
    c.gain(-2.2)
    t_e = c.gap(c.find("大象来了"))
    t_dong = c.at("咚，咚，咚")
    t_b = c.at("小鸟飞来了")
    t_l = c.at("狮子来了")
    t_roar = c.at("嗷呜")
    t_r = c.at("小兔子跳来了")
    t_m = c.gap(c.find("它们都是两个两个来的"))
    t_f = c.gap(c.find("挪亚还在方舟里"))
    i_b = c.find("大象来了")
    # the picture's cues on the big line (as PICTURE_HITS counts them): thud x3 (the stomps), whoosh x3 (the flaps)
    # and a fourth whoosh (the roar), pop x3 (the hops); each falls back to the narrator's voice
    wh = picture(c, "whoosh", c.ls(i_b) - 0.3, c.le(i_b) + 0.3) or []
    dongs = on_picture(c, "thud", c.ls(i_b) - 0.3, t_b, 3, lambda: syl(c, "咚，咚，咚", 3))
    puffs = wh[:3] if len(wh) >= 4 else syl(c, "扑扑扑", 3)
    t_roar_pic = wh[3] if len(wh) >= 4 else t_roar
    hops = on_picture(c, "pop", c.ls(i_b) - 0.3, c.le(i_b) + 0.4, 3, lambda: syl(c, "蹦蹦蹦", 3))
    i = c.seg(0, t_e, 1, "4/4", "Bb major", nominal=84, label="animals-here")
    e = c.seg(t_e, t_dong, 1, "2/4", "Bb major", nominal=88, label="animals-elephants")
    E = c.seg(t_dong, t_b, 1, "2/4", "Bb major", nominal=106, label="animals-stomps")
    b = c.seg(t_b, t_l, 1, "4/4", "Bb major", nominal=104, label="animals-birds")
    lion = c.seg(t_l, t_r, 1, "4/4", "Bb major", nominal=116, label="animals-lion")
    r = c.seg(t_r, t_m, 1, "4/4", "Bb major", nominal=92, label="animals-rabbits")
    m = c.seg(t_m, t_f, 3, "4/4", "Bb major", nominal=116, label="animals-march")
    f = c.seg(t_f, c.dur, 3, "4/4", "Bb major", nominal=116, label="animals-food")
    segs = (i, e, E, b, lion, r, m, f)
    for sg in segs:
        sg.duck(1.5)
    i.prog("Bb:4")
    e.prog("F7:2")
    E.prog("Bb:2")
    b.prog("Eb:2 Bb:2")
    e_r = min(max(int(round(lion.q_of(c.t0 + t_roar) * 48)), 12), int(lion.n_q * 48) - 12)
    lion.prog(f"Gm:{e_r}/48 Eb:{int(lion.n_q * 48) - e_r}/48")
    r.prog("Bb:2 F:2")
    m.prog(" | ".join(PARADE_PROG[:3]))
    f.prog("Eb:2 Bb:2 | Gm:2 C7:2@F-major | F:4@F-major")
    E.sync("'咚，咚，咚': the elephants (B-flat)", 0, t_dong, kind="change")
    lion.sync("'嗷呜': E-flat (the roar)", e_r / 48, t_roar, kind="change")
    m.sync("'两个两个': the march two by two", 0, t_m, kind="change")
    # 'and then -- the animals came!': a horn call, a snare roll, plucked oom-pah
    i.mel("horn", "F4:1 Bb4:1 D5:2", vel=56)
    oompah(i, 0, 4, vel=50)
    roll(i, 2, 3.9, 38, 16, 34, rate=12)
    i.pad(["vla", "vln2"], 2, 58, 74, vel=36, bass_ref=(34, 46))
    i.expr(["horn"], [(0, -12), (4, -11)])
    i.expr(["pz_cb", "pz_hi", "vla", "vln2"], [(0, -14), (4, -14)])
    i.expr("okit", [(0, -14), (4, -12)])
    # the elephants come: a heavy walk (tuba, bassoon) -- and 咚，咚，咚: three stomps
    e.mel("tuba", "F1:1 A1:1", vel=56)
    e.mel("bsn", "C3:1 Eb3:1", vel=50)
    e.pad(["vla", "vln2"], 2, 57, 72, vel=34, bass_ref=(29, 41))
    e.expr(["tuba", "bsn"], [(0, -11), (2, -11)])
    e.expr(["vla", "vln2"], [(0, -15), (2, -15)])
    for i_, t in enumerate(dongs):
        sg, q = seg_at(c, segs, t)
        stomp(sg, q, vel=60 + 3 * i_)
        sg.sync(f"stomp {i_ + 1} ('咚')", q, t)
    E.pad(["vla", "vln2"], 2, 58, 74, vel=36, bass_ref=(34, 46))
    E.expr(["timp", "pz_cb", "tuba"], [(0, -8), (2, -9)])
    E.expr("okit", [(0, -8), (2, -9)])
    E.expr(["vla", "vln2"], [(0, -15), (2, -15)])
    # the little birds fly in: 扑扑扑 -- flute flutters
    oompah(b, 0, 4, vel=46)
    b.pad(["vla", "vln2", "vln1"], 3, 60, 79, vel=34, bass_ref=(34, 46))
    for i_, t in enumerate(puffs):
        sg, q = seg_at(c, segs, t)
        flutter(sg, q, vel=56 + 2 * i_)
        sg.sync(f"flap {i_ + 1} ('扑')", q, t)
    b.expr(["flute", "celesta"], [(0, -12), (4, -12)])
    b.expr(["pz_cb", "pz_hi"], [(0, -12), (4, -13)])
    b.expr(["vla", "vln2", "vln1"], [(0, -14), (4, -16)])
    # the lion comes: a prowl (low pizzicato) -- 嗷呜! the comic roar (trombones, tuba, bassoon, timpani)
    for q in range(4):                                    # a prowl: low plucks, root and fifth of the chord
        ch = lion.chord_at(q + 1e-3)
        lion.add("pz_lo", q, _dq(lion, q, 0.5), ch.tones(43, 55)[0 if q % 2 == 0 else -1], 54, "bass", "s")
    lion.pad(["trem_va", "trem_va"], 2, 55, 70, vel=36, bass_ref=(31, 43))
    # the roar sits on the tones G and B-flat, common to the G minor before it and the E-flat it lands on
    q_r = qpos(lion, c, t_roar_pic, 0.0, 3.0)
    pcs = lion.chord_at(q_r + 1e-3).pcset & lion.chord_at(e_r / 48 + 1e-3).pcset
    roar = [p for p in range(46, 63) if p % 12 in pcs][:3]
    for j, p in enumerate(roar):
        lion.add("tbn", q_r, 1.0, p, 62, "harmony", "h", voice=f"tbn.{j}")
    low = [p for p in range(31, 47) if p % 12 in pcs]
    lion.add("tuba", q_r, 0.5, low[-1], 62, "bass", "h")
    q2 = q_r + 0.5
    second = lion.chord_at(q2 + 1e-3).bass_note(31, 43) if q2 >= e_r / 48 else low[0]
    lion.add("tuba", q2, _dq(lion, q2, 1.0), second, 56, "bass")      # ...rrrooar: down onto the E-flat
    bassline(lion, "cb", 31, 43, 46)
    lion.add("bsn", q_r, 1.0, low[-1] + 12 if low[-1] + 12 <= 60 else low[-1], 58, "bass", "h")
    lion.add("timp", q_r, 0.5, [p for p in range(38, 51) if p % 12 in pcs][0], 58, "timp", "h")
    lion.add("okit", q_r, 1, 36, 52, "perc", "h")
    lion.sync("the lion's roar (on the picture)", q_r, t_roar_pic)
    lion.expr(["tbn"], [(0, -14), (4, -15)])
    lion.expr(["tuba", "bsn", "timp", "pz_lo"], [(0, -13), (4, -13)])
    lion.expr(["trem_va"], [(0, -18), (4, -17)])
    lion.expr(["cb"], [(0, -14), (4, -12)])
    # the little rabbits hop in: 蹦蹦蹦 -- pizzicato hops
    oompah(r, 0, 4, vel=46)
    r.pad(["vla", "vln2"], 2, 58, 74, vel=34, bass_ref=(34, 46))
    for i_, t in enumerate(hops):
        sg, q = seg_at(c, segs, t)
        hop(sg, q, i_, vel=60)
        sg.sync(f"hop {i_ + 1} ('蹦')", q, t)
    r.expr(["pz_hi"], [(0, -10), (4, -10)])
    r.expr(["pz_cb"], [(0, -12), (4, -13)])
    r.expr(["vla", "vln2"], [(0, -14), (4, -16)])
    r.expr("hand", [(0, -9), (4, -9)])
    # two by two, a male and a female, in a line into the ark: the march in thirds
    tune = bars(PARADE, 0, 3)
    m.mel("flute", tune, vel=56)
    thirds(m, "clar", tune, vel=52)
    oompah(m, 0, 12, vel=50, bass="tuba")
    snare(m, 0, 12, vel=30)
    for q in (0, 4, 8):
        m.add("okit", q, 1, 36, 46 if q == 0 else 40, "perc", "h")
    m.sync("the march's first downbeat (bass drum, tuba)", 0, t_m)
    m.pad(["vla", "vln2"], 2, 55, 70, vel=34, bass_ref=(34, 46))
    m.duck(3.5, parts=["flute", "clar"])
    m.expr(["flute", "clar"], [(0, -17), (1, -13.5), (12, -13.5)])
    m.expr(["tuba", "pz_hi"], [(0, -13), (12, -13)])
    m.expr("okit", [(0, -12), (12, -12)])
    m.expr(["vla", "vln2"], [(0, -17), (12, -17)])
    # Noah filled the ark with food for people and animals: lighter (oboe, bassoon), on to F
    f.mel("oboe", "Eb5:1 G5:1 F5:1 D5:1 | Bb4:1 D5:1 E5:1 G5:1 | F5:4", vel=52)
    oompah(f, 0, 8, vel=46, bass="pz_cb")
    f.mel("bsn", "r:8 | F3:2 C3:2", vel=46, role="bass")
    snare(f, 0, 8, vel=26)
    f.pad(["vla", "vln2"], 2, 55, 70, vel=34, bass_ref=(29, 41))
    f.add("cb", 8, 4, "F1", 36, "bass")
    f.duck(2.5, parts=["oboe"])
    f.expr(["oboe"], [(0, -12), (12, -13)])
    f.expr(["pz_cb", "pz_hi", "bsn"], [(0, -14), (12, -15)])
    f.expr("okit", [(0, -14), (8, -16)])
    f.expr(["vla", "vln2", "cb"], [(0, -17), (12, -17)])


def door(c):
    """The family's eight steps up the ramp (Noah's theme b1-b2, clarinet, walking pizzicato, F); God's hand (a
    B-flat swell: choir, harp); F on '把门关上了', the gentle low thunk on the door, a warm held chord."""
    c.gain(-2.4)
    t_d = c.gap(c.find("然后，上帝亲手"))
    t_s = c.at("把门关上了")
    t_thunk = on_picture(c, "thud", t_s - 0.3, c.dur - 0.2, 1, lambda: [c.at("关上了")])[0]
    a = c.seg(0, t_d, 2, "4/4", "F major", nominal=104, label="door-family")
    d = c.seg(t_d, t_s, 1, "3/4", "F major", nominal=88, label="door-god")
    s = c.seg(t_s, c.dur, 1, "2/4", "F major", nominal=70, label="door-shut")
    for sg in (a, d, s):
        sg.duck(1.5)
    a.prog(" | ".join(NOAH_PROG[:2]))
    d.prog("Bb:3")
    s.prog("F:2")
    s.sync("'把门关上了': the warm F major chord", 0, t_s, kind="change")
    # Noah's family of eight walked into the ark too: eight steps, the theme on the clarinet
    a.mel("clar", bars(NOAH, 0, 2), vel=54)
    walk(a, "pz_lo", 0, 8, 41, 60, vel=50)
    a.pad(["vla", "vln2"], 2, 55, 70, vel=36, bass_ref=(41, 53))
    a.duck(2.0, parts=["clar"])
    a.expr(["clar"], [(0, -13), (8, -13)])
    a.expr(["pz_lo"], [(0, -11), (8, -11)])
    a.expr(["vla", "vln2"], [(0, -17), (8, -17)])
    # then God himself...: a swell (choir 'ooh', strings), a harp sweep up
    d.pad("ooh", 3, 58, 74, vel=40, bass_ref=(34, 46))
    strings(d, vel=38, lo=58, hi=74, bass=(46, 58), cb=(34, 46))
    gliss_in(d, "harp", 0.5, 0.7, midi("F3"), midi("F6"), v0=28, v1=44, scale=ChordTones(d.chord_at(0)))
    d.expr(["ooh"], [(0, -22), (3, -16)])
    d.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -17), (3, -13)])
    d.expr(["harp"], [(0, -11), (3, -11)])
    # ...shut the door: a gentle low thunk (on the picture), a warm held F major chord
    sg, q = seg_at(c, (d, s), t_thunk)
    ch = sg.chord_at(q + 1e-3)
    sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(ch, midi("F2")), 54, "timp", "h")
    sg.add("pz_cb", q, _dq(sg, q, 0.5), ch.bass_note(29, 41), 56, "bass", "h")
    sg.add("okit", q, 1, 36, 44, "perc", "h")
    sg.sync("the door shuts (a gentle low thunk)", q, t_thunk)
    for j, nm in enumerate(["F3", "A3", "C4"]):
        s.add("horn", 0, 2, nm, 46, "pad", voice=f"horn.{j}")
    s.pad("ooh", 3, 57, 72, vel=40, bass_ref=(41, 53))
    strings(s, vel=42, lo=57, hi=72)
    s.expr(["horn"], [(0, -14), (1.2, -17), (2, -21)])
    s.expr(["ooh"], [(0, -15), (1.2, -18), (2, -22)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -12), (1.2, -15), (2, -19)])
    s.expr(["timp", "pz_cb"], [(0, -9), (2, -9)])
    s.expr("okit", [(0, -12), (2, -12)])


def flood(c):
    """Seven soft ticks (D minor); the drips on 滴答 (pizzicato and celesta over A); the pour on '哗啦啦' (D minor:
    rolling cellos, tremolo, timpani, harp sweeps); the water rising (Dm C/E F Gm A7, a horn in tenths over the
    rising bass, the timpani growing); the ark floats on '方舟浮起来了' (deceptive A7 -> B-flat, 6/8 rocking); the
    mountains covered (big, warm); a hushed close on '外面的一切，都不见了'."""
    c.gain(-1.6)
    t_d = c.at("滴答")
    t_w = c.at("哗啦啦")
    t_r = c.gap(c.find("大雨下了"))
    t_f = c.at("方舟浮起来了")
    t_m = c.gap(c.find("大水盖过了"))
    t_h = c.at("外面的一切")
    v_drip = syl(c, "滴答", 4)
    d_pic = picture(c, "drip", c.ls(0) - 0.3, t_w + 0.3) or []
    if len(d_pic) >= 2:                                   # the picture's drop on each 滴 (答 follows as spoken)
        drip = sorted(d_pic[:2] + [t + (v_drip[1] - v_drip[0]) for t in d_pic[:2]])
    else:
        drip = v_drip
    t_thunder = on_picture(c, "thunder", c.ls(0) - 0.3, c.le(0) + 0.3, 1, lambda: [None])[0]
    rises = picture(c, "splash", c.ls(1) - 0.3, c.le(1)) or []
    pours = syl(c, "哗啦啦", 2)
    a = c.seg(0, t_d, 1, "4/4", "D minor", nominal=80, label="flood-seven-days")
    d = c.seg(t_d, t_w, 1, "2/4", "D minor+", nominal=80, label="flood-drips")
    w = c.seg(t_w, t_r, 1, "4/4", "D minor", nominal=118, label="flood-pour")
    r = c.seg(t_r, t_f, 2, "4/4", "D minor+", nominal=88, label="flood-rising")
    fl = c.seg(t_f, t_m, 2, "6/8", "Bb major", nominal=100, label="flood-float")
    m = c.seg(t_m, t_h, 1, "4/4", "D minor", nominal=94, label="flood-mountains")
    h = c.seg(t_h, c.dur, 1, "4/4", "D minor", nominal=100, label="flood-gone")
    h.hush = True
    segs = (a, d, w, r, fl, m, h)
    for sg in segs:
        sg.duck(1.5)
    a.prog("Dm:4")
    d.prog("A:2")
    w.prog("Dm:2 Bb:2")
    r.prog("Dm:2 C/E:2 | F:2 Gm:1 A7:1")
    fl.prog("Bb:3 | Gm:3")
    m.prog("Dm:2 Bb:2")
    h.prog("Gm:2 Dm:2")
    w.sync("'哗啦啦': the pour (D minor)", 0, t_w, kind="change")
    fl.sync("'方舟浮起来了': the ark floats (B-flat)", 0, t_f, kind="change")
    # seven days later, it began to rain: seven soft ticks, clouds (low tremolo)
    for j in range(7):
        q = 0.5 + 0.5 * j
        a.add("pz_hi" if j % 2 == 0 else "celesta", q, 0.25, top(a, q, 69, 86, 1 + (j % 2)), 40, "arp", "s")
    a.pad(["trem_va", "trem_va"], 2, 50, 65, vel=38, bass_ref=(38, 50))
    a.add("cb", 0, 4, "D2", 38, "bass")
    a.expr(["pz_hi", "celesta"], [(0, -12), (4, -12)])
    a.expr(["trem_va", "cb"], [(0, -15), (4, -15)])
    # 滴答，滴答: drips (pizzicato and celesta), high and then lower
    for i_, t in enumerate(drip):
        sg, q = seg_at(c, segs, t)
        hi_ = i_ % 2 == 0
        ts = sg.chord_at(q + 1e-3).tones(76, 90)
        p = ts[-1] if hi_ else ts[max(0, len(ts) - 3)]
        sg.add("pz_hi", q, _dq(sg, q, 0.25), p, 62 if hi_ else 54, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 0.25), p, 50 if hi_ else 44, "arp", "h")
        if hi_:
            sg.sync(f"drip {i_ // 2 + 1} ('滴')", q, t)
    if t_thunder is not None:                             # a distant rumble on the picture's thunder
        sg, q = seg_at(c, segs, t_thunder)
        thump(sg, q, vel=50, sync="thunder (a soft rumble)", t=t_thunder)
    for k, t in enumerate(rises[:2]):                     # the water rises: a low accent on each surge
        sg, q = seg_at(c, segs, t)
        thump(sg, q, vel=60 + 4 * k, sync=f"the water rises {k + 1}", t=t)
        pluck_chord(sg, q, vel=58 + 2 * k, lo=55, hi=67)
    d.pad(["trem_va", "trem_va"], 2, 52, 69, vel=36, bass_ref=(33, 45))
    d.add("cb", 0, 2, "A1", 38, "bass")
    d.expr(["pz_hi", "celesta"], [(0, -8), (2, -8)])
    for sg in (d, w, r):
        sg.expr("okit", [(0, -12), (sg.n_q, -12)])
    d.expr(["trem_va", "cb"], [(0, -17), (2, -15)])
    # 哗啦啦，哗啦啦: rolling cellos, tremolo, a timpani roll, harp sweeps down
    broken(w, "vc_fast", 0, 4, (0, 1, 2, 1), 38, 62, vel=54, step=0.25, accent=6, ring=False, art="s", role="arp")
    w.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 74, vel=50, bass_ref=(34, 46))
    bassline(w, "cb", 28, 40, 46)
    timp_roll(w, 0, 3.9, midi("D2"), 30, 46)
    for t in pours:
        q = qpos(w, c, t, 0.0, 3.5)
        gliss_in(w, "harp", q, 0.45, midi("D4"), midi("D6"), up=False, v0=46, v1=58,
              scale=ChordTones(w.chord_at(q + 1e-3)))
    w.expr(["vc_fast"], [(0, -11), (4, -11)])
    w.expr(["trem_va", "trem_hi", "cb"], [(0, -12), (4, -12)])
    w.expr(["timp", "harp"], [(0, -11), (4, -11)])
    # it rained forty days and forty nights, the water rose higher and higher
    broken(r, "vc_fast", 0, 8, (0, 1, 2, 1), 38, 62, vel=52, step=0.25, accent=6, ring=False, art="s", role="arp")
    r.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 76, vel=48, bass_ref=(38, 50))
    bassline(r, "cb", 38, 50, 44)
    r.mel("horn", "F4:2 G4:2 | A4:2 Bb4:1 C#5:1", vel=54)
    q_roll = max(4.0, max((qpos(r, c, t) for t in rises[:2]), default=0.0) + 0.6)
    if q_roll < 7.4:
        timp_roll(r, q_roll, 7.9, midi("D2"), 28, 48)
    r.duck(2.0, parts=["horn"])
    r.expr(["vc_fast"], [(0, -12), (8, -10)])
    r.expr(["trem_va", "trem_hi", "cb"], [(0, -14), (8, -11)])
    r.expr(["horn"], [(0, -13), (8, -11)])
    r.expr(["timp", "pz_cb", "pz_hi"], [(0, -10), (8, -10)])
    # the ark lifted and floated, on and on: B-flat, 6/8 rocking
    fl.mel("clar", "D5:1 C5:1/2 D5:1 F5:1/2 | G5:1 F5:1/2 D5:3/2", vel=56)
    broken(fl, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 46, 58, vel=40, thin=True)
    fl.mel("pz_lo", "Bb2:3/2 D3:3/2 | G2:3/2 D2:3/2", vel=52, role="bass")
    fl.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=40, bass_ref=(38, 50))
    fl.duck(2.0, parts=["clar", "harp"])
    fl.expr(["clar"], [(0, -12), (6, -12)])
    fl.expr(["harp", "pz_lo"], [(0, -10), (6, -10)])
    fl.expr(["vla", "vln2", "vln1"], [(0, -14), (6, -14)])
    # the water covered the highest mountains: big and warm (rolling strings, timpani, low brass)
    broken(m, "vc_fast", 0, 4, (0, 1, 2, 1), 38, 62, vel=54, step=0.25, accent=6, ring=False, art="s", role="arp")
    m.pad(["trem_va", "trem_va", "trem_hi"], 3, 52, 76, vel=50, bass_ref=(34, 46))
    m.pad(["tbn", "tbn", "horn"], 3, 50, 67, vel=46, bass_ref=(34, 46))
    bassline(m, "cb", 28, 40, 46)
    timp_roll(m, 0, 3.9, midi("D2"), 40, 34)
    m.expr(["vc_fast"], [(0, -11), (2.5, -12), (4, -17)])
    m.expr(["trem_va", "trem_hi", "cb"], [(0, -12), (2.5, -13), (4, -16)])
    m.expr(["tbn", "horn"], [(0, -16), (1.5, -12), (3, -15), (4, -20)])
    m.expr(["timp"], [(0, -11), (4, -13)])
    # everything outside was gone: hushed (high tremolo, a low D)
    h.pad(["trem_hi", "trem_hi"], 2, 62, 77, vel=36, bass_ref=(38, 50))
    h.add("cb", 0, 4, "D2", 36, "bass")
    h.add("celesta", 2, 2, "A5", 34, "arp")
    h.expr(["trem_hi", "cb"], [(0, -16), (4, -20)])
    h.expr(["celesta"], [(0, -14), (4, -15)])


def inside(c):
    """Inside the ark: a B-flat lullaby in 3/4 (celesta, harp, pizzicato raindrops on the roof, a little wind on
    '外面风很大'); E-flat on '可是上帝一直记得挪亚': Noah's motif on the horn, a choir 'ooh'."""
    c.gain(-3.0)
    t_g = c.at("可是上帝一直记得挪亚")
    a = c.seg(0, t_g, 4, "3/4", "Bb major", nominal=84, label="inside-lullaby")
    g = c.seg(t_g, c.dur, 2, "3/4", "Bb major", nominal=72, rit=0.15, label="inside-remembers")
    for sg in (a, g):
        sg.duck(1.5)
    a.prog("Bb:3 | Eb:3 | Bb:3 | F:3")
    g.prog("Eb:3 | Bb:3")
    g.sync("'可是上帝一直记得挪亚': E-flat, Noah's motif", 0, t_g, kind="change")
    # everyone safe and sound inside: the lullaby (celesta, harp), rain on the roof
    a.mel("celesta", "F5:2 D5:1 | Eb5:2 G5:1 | F5:1 D5:1 Bb4:1 | C5:3", vel=46)
    broken(a, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 46, 58, vel=36, thin=True)
    drops(a, 0, 12, [0.75, 2.5, 3.75, 5.5, 6.25, 7.5, 8.75, 10.5, 11.25], lo=79, hi=91, vel=36,
          parts=("pz_hi",))
    a.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    a.pad(["trem_va", "trem_va"], 2, 50, 65, vel=34, q0=6, bass_ref=(39, 51))
    a.duck(2.0, parts=["celesta", "harp"])
    a.expr(["celesta"], [(0, -18), (1.5, -10), (12, -10)])
    a.expr(["harp"], [(0, -18), (1.5, -10), (12, -10)])
    a.expr(["pz_hi"], [(0, -14), (12, -14)])
    a.expr(["vla", "vln2", "vln1", "vc"], [(0, -22), (2, -16), (12, -16)])
    a.expr(["trem_va"], [(6, -24), (9, -17), (12, -20)])
    # but God remembered Noah, and every animal in the ark: the horn, a choir 'ooh', the lullaby goes on
    g.mel("horn", "G3:1 Bb3:1 Eb4:1 | D4:3", vel=54)
    g.mel("celesta", "G5:2 Eb5:1 | D5:3", vel=42)
    g.pad("ooh", 3, 55, 70, vel=38, bass_ref=(39, 51))
    broken(g, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 39, 51, vel=36, thin=True)
    g.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    g.duck(2.5, parts=["horn", "ooh"])
    g.expr(["horn"], [(0, -12), (6, -13)])
    g.expr(["celesta", "harp"], [(0, -11), (6, -12)])
    g.expr(["ooh"], [(0, -20), (2, -17), (6, -18)])
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -15), (6, -16)])


def dove(c):
    """The wind (Dm Gm: harp sweeps, tremolo, an airy flute); the water goes down (a clarinet scale down over
    B-flat, F/A); the ark rests on Ararat (C: a soft settle); the dove (F, 6/8 flute): out and searching, home on
    F on '又飞回来了'; out again, home on a glowing D major chord for '橄榄叶', Gm C F on '水退了'; the third time it
    flies up and away -- C, then B-flat add9 with the flute held on the ninth: open, hopeful."""
    c.gain(-2.4)
    t_r = c.at("水慢慢地")
    t_s = c.at("方舟停在了")
    t_1 = c.gap(c.find("挪亚打开窗户"))
    t_b1 = c.at("又飞回来了")
    t_2 = c.gap(c.find("过了七天"))
    t_leaf = c.at("橄榄叶")
    t_3 = c.gap(c.find("又过了七天"))
    t_n = c.at("这一次")
    t_settle = on_picture(c, "thud", t_s - 0.3, c.le(0) + 0.5, 1, lambda: [None])[0]
    ticks = [t for t in (picture(c, "pop", c.ls(2) - 0.3, c.dur) or [])]          # seven days pass (twice)
    w = c.seg(0, t_r, 1, "4/4", "F major", nominal=72, label="dove-wind")
    r = c.seg(t_r, t_s, 1, "4/4", "F major", nominal=104, label="dove-recede")
    s = c.seg(t_s, t_1, 1, "4/4", "F major", nominal=88, label="dove-ararat")
    o1 = c.seg(t_1, t_b1, 4, "6/8", "F major", nominal=116, label="dove-1-out")
    b1 = c.seg(t_b1, t_2, 1, "6/8", "F major", nominal=116, label="dove-1-home")
    o2 = c.seg(t_2, t_leaf, 5, "6/8", "F major", nominal=116, label="dove-2")
    lf = c.seg(t_leaf, t_3, 3, "6/8", "F major", nominal=116, label="dove-leaf")
    o3 = c.seg(t_3, t_n, 2, "6/8", "F major", nominal=104, label="dove-3-out")
    n = c.seg(t_n, c.dur, 2, "6/8", "F major", nominal=116, label="dove-3-gone")
    for sg in (w, r, s, o1, b1, o2, lf, o3, n):
        sg.duck(1.5)
    w.prog("Dm:2 Gm:2")
    r.prog("Bb:2 F/A:2")
    s.prog("C:4")
    o1.prog("F:3 | Bb:3 | Dm:3/2 Gm:3/2 | C:3")
    b1.prog("F:3")
    o2.prog("F:3 | Bb:3 | F:3 | Gm:3/2 C:3/2 | C:3")
    lf.prog("D:3@D-major | Gm:3/2 C:3/2 | F:3")
    o3.prog("F:3 | Bb:3")
    n.prog("C:3 | Bbadd9:3")
    b1.sync("'又飞回来了': the dove comes home (F)", 0, t_b1, kind="change")
    lf.sync("'橄榄叶': the olive leaf (D major)", 0, t_leaf, kind="change")
    n.sync("'这一次': the last flight (C)", 0, t_n, kind="change")
    # God sent a wind over the earth: harp sweeps up and down, tremolo swelling, an airy flute
    gliss_in(w, "harp", 0.25, 0.8, midi("D3"), midi("D6"), v0=28, v1=42, scale=ChordTones(w.chord_at(0)))
    gliss_in(w, "harp", 2.25, 0.8, midi("G5"), midi("G3"), up=False, v0=40, v1=28, scale=ChordTones(w.chord_at(2)))
    w.mel("flute", "A5:2 Bb5:2", vel=44)
    w.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 72, vel=40, bass_ref=(38, 50))
    bassline(w, "cb", 31, 43, 36)
    w.expr(["harp"], [(0, -11), (4, -11)])
    w.expr(["flute"], [(0, -17), (2, -14), (4, -15)])
    w.expr(["trem_va", "trem_hi", "cb"], [(0, -20), (2, -15), (4, -17)])
    # the water slowly went down: a clarinet scale down
    r.mel("clar", "F5:1/2 E5:1/2 D5:1/2 C5:1/2 Bb4:1/2 A4:1/2 G4:1/2 F4:1/2", vel=52)
    r.pad(["vla", "vln2"], 2, 55, 70, vel=36, bass_part="vc", bass_lo=45, bass_hi=57)
    r.expr(["clar"], [(0, -12), (4, -13)])
    r.expr(["vla", "vln2", "vc"], [(0, -16), (4, -16)])
    # the ark came to rest on the mountains of Ararat: a soft settle, open fifths in the horn
    q_st = 0.5 if t_settle is None else qpos(s, c, t_settle, 0.0, 3.0)
    s.add("timp", q_st, 0.5, "C3", 50, "timp", "h")
    s.add("pz_cb", q_st, 0.5, "C2", 54, "bass", "h")
    s.add("okit", q_st, 1, 36, 36, "perc", "h")
    if t_settle is not None:
        s.sync("the ark settles on Ararat", q_st, t_settle)
    for j, nm in enumerate(["C3", "G3"]):
        s.add("horn", 0, 4, nm, 44, "pad", voice=f"horn.{j}")
    s.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=36, bass_part="vc", bass_lo=36, bass_hi=48)
    s.expr(["horn"], [(0, -18), (2, -14), (4, -15)])
    s.expr(["timp", "pz_cb"], [(0, -12), (4, -12)])
    s.expr("okit", [(0, -12), (4, -12)])
    s.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (4, -15)])
    for t in ticks:                                       # the days tick by: soft celesta ticks on the picture
        sg, q = seg_at(c, (o1, b1, o2, lf, o3, n), t)
        sg.add("celesta", q, _dq(sg, q, 0.25), top(sg, q, 84, 91, 0), 30, "arp", "s")
    # the first dove: out (a rising arpeggio), searching, home again
    o1.mel("flute", "C5:1 F5:1/2 A5:1 C6:1/2 | D6:3/2 Bb5:1 F5:1/2 | F5:1 A5:1/2 G5:1 Bb5:1/2 | "
                    "C6:1 Bb5:1/2 G5:1 E5:1/2", vel=56)
    broken(o1, "harp", 0, 12, (0, 2, 4, 2, 4, 2), 41, 53, vel=36, thin=True)
    o1.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    b1.mel("flute", "A5:1 G5:1/2 F5:3/2", vel=54)
    b1.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=38, bass_part="vc", bass_lo=41, bass_hi=53)
    b1.add("harp", 0, 3, "F3", 42, "arp")
    b1.add("harp", 0.1, 2.9, "C4", 40, "arp")
    for sg, nq in ((o1, 12), (b1, 3)):
        sg.duck(3.5, parts=["flute", "harp"])
        sg.expr(["flute"], [(0, -12), (nq, -12)])
        sg.expr(["harp"], [(0, -10), (nq, -10)])
        sg.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (nq, -16)])
    # seven days later, again; back in the evening -- with a fresh olive leaf!
    o2.mel("flute", "C5:1 F5:1/2 A5:1 C6:1/2 | D6:3/2 Bb5:3/2 | A5:1 G5:1/2 F5:3/2 | Bb5:1 A5:1/2 G5:1 E5:1/2 | "
                    "G5:3", vel=54)
    broken(o2, "harp", 0, 15, (0, 2, 4, 2, 4, 2), 41, 53, vel=36, thin=True)
    o2.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    for q, nm in ((6.0, "F6"), (7.5, "C7")):              # evening: a celesta star
        o2.add("celesta", q, 1.0, nm, 32, "arp")
    o2.duck(4.0, parts=["flute", "harp"])
    o2.expr(["flute"], [(0, -13), (15, -13)])
    o2.expr(["harp", "celesta"], [(0, -10), (15, -10)])
    o2.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (15, -16)])
    # the leaf: D major glowing (flute, glockenspiel, harp sweep), then Gm C F -- the waters were gone!
    lf.mel("flute", "F#5:1 A5:1/2 D6:3/2 | Bb5:1 G5:1/2 G5:1 E5:1/2 | F5:3", vel=56)
    gliss_in(lf, "harp", 0, 0.5, midi("D4"), midi("D6"), v0=34, v1=50, scale=ChordTones(lf.chord_at(0)))
    lf.add("glock", 0, 1.5, "F#6", 46, "arp", "h")
    lf.add("celesta", 0.5, 1.0, "A6", 38, "arp")
    lf.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=40, bass_part="vc", bass_lo=40, bass_hi=52)
    lf.pad("ooh", 3, 57, 74, vel=36, bass_ref=(38, 50))
    bassline(lf, "cb", 28, 40, 38)
    broken(lf, "harp", 3, 9, (0, 2, 4, 2, 4, 2), 41, 53, vel=36, thin=True)
    lf.duck(4.0, parts=["flute", "harp", "glock"])
    lf.expr(["flute"], [(0, -12), (9, -13)])
    lf.expr(["harp", "glock", "celesta"], [(0, -9), (9, -10)])
    lf.expr(["ooh"], [(0, -20), (1.5, -17), (9, -19)])
    lf.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (9, -15)])
    # seven more days: the third flight out...
    o3.mel("flute", "C5:1 F5:1/2 A5:1 C6:1/2 | D6:3", vel=54)
    broken(o3, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 41, 53, vel=36, thin=True)
    o3.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    o3.duck(4.0, parts=["flute", "harp"])
    o3.expr(["flute"], [(0, -13), (6, -13)])
    o3.expr(["harp"], [(0, -10), (6, -10)])
    o3.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (6, -16)])
    # ...and this time the dove did not come back: up and away, the melody ends open (B-flat add9, on the 9th)
    n.mel("flute", "G5:1 C6:1/2 E6:3/2 | D6:3/2 C6:3/2", vel=52)
    n.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_part="vc", bass_lo=46, bass_hi=58)
    n.add("cb", 0, 3, "C2", 34, "bass")
    n.add("cb", 3, 3, "Bb1", 34, "bass")
    n.add("harp", 3, 3, "Bb2", 38, "arp")
    n.add("harp", 3.12, 2.88, "F3", 36, "arp")
    n.add("harp", 3.24, 2.76, "D4", 34, "arp")
    n.add("celesta", 4.5, 1.5, "C7", 30, "arp")
    n.duck(4.0, parts=["flute"])
    n.expr(["flute"], [(0, -14), (4.5, -14), (6, -18)])
    n.expr(["harp", "celesta"], [(0, -11), (6, -12)])
    n.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (6, -18)])


def out(c):
    """God speaks (B-flat, then soft pads only: Eb F); '门打开了' -- the burst: the parade theme returns in full
    (brass, flute and clarinet in thirds, tuba, snare, timpani, cymbal, harp sweep), a hop, a flap and a run on
    '有的跳，有的飞，有的跑'; Noah's altar: his theme on the horn (F); the plagal amen on '感谢上帝' (B-flat, F)."""
    c.gain(-2.2)
    t_g = c.gap(c.find("你和你的家人，还有"))
    t_o = c.at("门打开了")
    t_t = c.gap(c.find("挪亚做的第一件事"))
    t_a = c.at("感谢上帝")
    t_open = on_picture(c, "ship_creak", t_o - 0.3, t_o + 0.5, 1, lambda: [t_o])[0]
    i_o = c.find("门打开了")
    v_j = [t + 0.25 for t in syl(c, "有的跳", 3)]          # 跳 / 飞 / 跑 (just after each 有的)
    jumps = [on_picture(c, nm, c.ls(i_o) - 0.3, c.le(i_o), 1, lambda k=k: [v_j[k]])[0]
             for k, nm in enumerate(("pop", "whoosh", "footsteps_run"))]
    stones = picture(c, "thud", c.ls(i_o + 1) - 0.3, c.dur) or []
    n = c.seg(0, t_g, 1, "4/4", "Bb major", nominal=86, label="out-god-speaks")
    g = c.seg(t_g, t_o, 2, "4/4", "Bb major", nominal=75, label="out-god")
    o = c.seg(t_o, t_t, 4, "4/4", "Bb major", nominal=118, label="out-parade")
    t = c.seg(t_t, t_a, 2, "4/4", "F major", nominal=112, label="out-altar")
    a = c.seg(t_a, c.dur, 1, "2/4", "F major", nominal=88, label="out-thanks")
    for sg in (n, g, o, t, a):
        sg.duck(1.5)
    n.prog("Bb:4")
    g.prog("Eb:4 | F:4")
    o.prog(" | ".join(PARADE_PROG))
    t.prog(" | ".join(NOAH_PROG[:2]))
    a.prog("Bb:1 F:1")
    o.sync("'门打开了': the parade returns (B-flat)", 0, t_o, kind="change")
    a.sync("'感谢上帝': the amen (B-flat)", 0, t_a, kind="change")
    # God said to Noah: a soft harp, strings
    broken(n, "harp", 0, 4, (0, 2, 4, 6), 46, 58, vel=34, thin=True)
    n.pad(["vla", "vln2", "vln1"], 3, 58, 74, vel=36, bass_part="vc", bass_lo=46, bass_hi=58)
    n.expr(["harp"], [(0, -12), (4, -13)])
    n.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (4, -17)])
    # 'come out, you and your family, and all the animals': soft pads only
    g.pad("ooh", 3, 55, 72, vel=38, bass_ref=(39, 51))
    g.pad(["vla", "vln2", "vln1"], 3, 58, 76, vel=36, bass_part="vc", bass_lo=39, bass_hi=51)
    g.duck(3.0)
    g.expr(["ooh"], [(0, -22), (2, -19), (8, -19)])
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (8, -17)])
    # the door opened! the burst, and the parade theme in full
    sg, q0 = seg_at(c, (g, o), t_open)
    sg.add("timp", q0, _dq(sg, q0, 0.5), timp_pitch(sg.chord_at(q0 + 1e-3), midi("Bb2")), 56, "timp", "h")
    sg.add("okit", q0, 2, 57, 42, "perc", "h")
    sg.add("glock", q0, _dq(sg, q0, 1.0), top(sg, q0, 86, 98), 46, "arp", "h")
    pluck_chord(sg, q0, vel=58, lo=58, hi=70)
    sg.sync("the door opens (on the picture)", q0, t_open)
    gliss_in(o, "harp", 0, 0.35, midi("Bb3"), midi("Bb5"), v0=36, v1=50, scale=ChordTones(o.chord_at(0)))
    tune = bars(PARADE, 0, 4)
    o.mel("brass", tune, vel=54)
    o.mel("flute", tune, vel=54)
    thirds(o, "clar", tune, vel=50)
    oompah(o, 0, 16, vel=50, bass="tuba")
    snare(o, 0, 16, vel=28)
    for q in (4, 8, 12):
        o.add("okit", q, 1, 36, 38, "perc", "h")
    o.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=38, bass_ref=(34, 46))
    labels = ("hop", "flap", "run")
    for k, tj in enumerate(jumps):
        qj = qpos(o, c, tj, 0.0, o.n_q - 0.6)
        if labels[k] == "hop":
            hop(o, qj, 1, vel=52)
        elif labels[k] == "flap":
            flutter(o, qj, vel=50)
        else:
            for j in range(4):
                qq = qj + 0.125 * j
                o.add("pz_hi", qq, 0.125, o.chord_at(qq + 1e-3).tones(67, 84)[j], 46 + 2 * j, "arp", "s")
    o.duck(3.0, parts=["brass", "flute", "clar"])
    o.expr(["brass", "flute", "clar"], [(0, -11), (16, -12)])
    o.expr(["tuba", "pz_hi"], [(0, -12), (16, -13)])
    o.expr(["timp", "glock", "harp", "pz_hi"], [(0, -9), (16, -11)])
    o.expr("okit", [(0, -10), (16, -12)])
    o.expr("hand", [(0, -10), (16, -10)])
    o.expr(["vla", "vln2", "vln1"], [(0, -15), (16, -15)])
    # Noah's first thing: an altar to thank God -- his theme on the horn
    t.mel("horn", bars(NOAH, 0, 2), vel=56, transpose=-12)
    strings(t, vel=40, lo=55, hi=72)
    broken(t, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 41, 53, vel=36, thin=True)
    for k, ts_ in enumerate(stones[:4]):                   # the altar's stones, one by one (on the picture)
        sg, q = seg_at(c, (o, t, a), ts_)
        ch = sg.chord_at(q + 1e-3)
        sg.add("pz_lo", q, _dq(sg, q, 0.5), ch.bass_note(41, 53), 54, "bass", "h")
        sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(ch, midi("F2")), 46, "timp", "h")
        drum(sg, q, 77, 48)
        sg.sync(f"altar stone {k + 1}", q, ts_)
    t.duck(2.0, parts=["horn"])
    t.expr(["pz_lo", "timp"], [(0, -10), (8, -10)])
    t.expr("hand", [(0, -11), (8, -11)])
    t.expr(["horn"], [(0, -12), (8, -12)])
    t.expr(["harp"], [(0, -10), (8, -10)])
    t.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -15)])
    # '感谢上帝': amen (B-flat, F) -- the horn, a choir 'ooh'
    a.mel("horn", "D4:1 C4:1", vel=52)
    a.pad("ooh", 3, 57, 72, vel=40, bass_ref=(41, 53))
    strings(a, vel=42, lo=57, hi=72)
    a.expr(["horn"], [(0, -12), (1.2, -14), (2, -17)])
    a.expr(["ooh"], [(0, -16), (1.2, -18), (2, -20)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (1.2, -15), (2, -17)])


def rainbow(c):
    """God's covenant (soft pads, F); the rainbow in the clouds (B-flat over C, harp shimmer); the colours: a rising
    scale, one note per colour band as it appears on the picture (the scene's sparkle on each band; the narrator's
    colour words without the scene), glockenspiel, celesta, harp, pizzicato, over a bass falling in thirds (F | Dm |
    Bb | Gm | C: F arrives with the word 红, Dm Bb Gm with the bands of 黄 绿 蓝, C with the word 紫); the radiant tutti
    on '好漂亮啊' (on the picture's chime: choir 'ah', brass, cymbal, timpani, F); God's promise (soft pads)."""
    c.gain(-2.2)
    t_p = c.gap(c.find("上帝把一道彩虹"))
    words = ["红", "橙", "黄", "绿", "青", "蓝", "紫"]
    t_c = {w_: c.at(w_) for w_ in words}
    t_red = t_c["红"]
    v_col = syl(c, "红", 8)
    i_c = c.find("红")
    bands = on_picture(c, "sparkle", c.ls(i_c) - 0.3, c.le(i_c), 7, lambda: v_col[:7])
    bands = [max(b_, t_red + 0.02) for b_ in bands]
    t_wow = on_picture(c, "chime", bands[-1] + 0.1, c.le(i_c) + 0.3, 1, lambda: [v_col[7]])[0]
    t_wow = min(max(t_wow, t_c["紫"] + 0.35, bands[-1] + 0.25), c.le(i_c) - 0.2)
    t_e = c.gap(c.find("每次看见彩虹"))
    g = c.seg(0, t_p, 2, "4/4", "F major", nominal=72, label="rainbow-covenant")
    p = c.seg(t_p, t_red, 1, "4/4", "F major", nominal=66, label="rainbow-clouds")
    r = c.seg(t_red, t_wow, 1, "4/4", "F major", nominal=80, label="rainbow-colours")
    long_wow = t_e - t_wow >= 1.15
    t = c.seg(t_wow, t_e, 1, "2/4" if long_wow else "3/8", "F major", nominal=88 if long_wow else 100,
              label="rainbow-radiant")
    e = c.seg(t_e, c.dur, 2, "4/4", "F major", nominal=96, label="rainbow-promise")
    for sg in (g, p, r, t, e):
        sg.duck(1.5)
    g.prog("F:4 | Dm:2 Bb:2")
    p.prog("Bb/C:2 C:2")
    # the colour chords (in 48ths of a quarter): F on the word 红, Dm Bb Gm on the bands of 黄 绿 蓝, C on the word 紫
    qs = [0.0] + [r.q_of(c.t0 + t) for t in (bands[2], bands[3], bands[5], t_c["紫"])] + [r.n_q]
    edges = [int(round(q * 48)) for q in qs]
    for k in range(1, len(edges)):
        edges[k] = max(edges[k], edges[k - 1] + 6)
    edges[-1] = int(round(r.n_q * 48))
    chords = ["F", "Dm", "Bb", "Gm", "C"]
    r.prog(" ".join(f"{ch}:{edges[k + 1] - edges[k]}/48" for k, ch in enumerate(chords)))
    t.prog("F:2" if long_wow else "F:3/2")
    e.prog("Bb:4 | Gm:2 C:2")
    r.sync("'红': the rainbow begins (F)", 0, t_red, kind="change")
    r.sync("'紫': the last colour (C)", edges[4] / 48, t_c["紫"], kind="change")
    t.sync("'好漂亮啊': the radiant tutti (F)", 0, t_wow)
    # 'I make a covenant with you: never again a flood': soft pads only
    g.pad("ooh", 3, 57, 74, vel=36, bass_ref=(41, 53))
    g.pad(["vla", "vln2", "vln1"], 3, 60, 77, vel=36, bass_part="vc", bass_lo=41, bass_hi=53)
    g.duck(3.0)
    g.expr(["ooh"], [(0, -20), (2, -19), (8, -19)])
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -15), (2, -18), (8, -18)])
    # God put a rainbow in the clouds: a harp shimmer over C, high tremolo
    broken(p, "harp", 0, 4, (0, 1, 2, 3, 4, 3, 2, 1), 58, 82, vel=34, step=0.25, thin=True)
    p.pad(["trem_va", "trem_hi", "trem_hi"], 3, 60, 79, vel=38, bass_ref=(36, 48))
    p.add("cb", 0, 4, "C2", 36, "bass")
    p.expr(["harp"], [(0, -19), (1, -14), (4, -11)])
    p.expr(["trem_va", "trem_hi", "cb"], [(0, -23), (4, -15)])
    # 红、橙、黄、绿、青、蓝、紫: a note for every colour, rising
    scale_up = ["F5", "G5", "A5", "Bb5", "C6", "D6", "E6"]
    q_col = [qpos(r, c, bands[k], 0.0, r.n_q - 0.15) for k in range(7)]
    for k in range(1, 7):
        q_col[k] = max(q_col[k], q_col[k - 1] + 0.12)
    for k in range(7):
        r.sync(f"colour {k + 1} ({words[k]})", q_col[k], bands[k])
    for k, (q, nm) in enumerate(zip(q_col, scale_up)):
        end = q_col[k + 1] if k + 1 < 7 else r.n_q
        if midi(nm) % 12 in r.chord_at(q + 1e-3).pcset:         # a chord tone stops with its chord
            end = min(end, span_end(r, q + 1e-6))
        r.add("glock", q, end - q, nm, 50 + k, "melody", "h")
        r.add("celesta", q, end - q, midi(nm) - 12, 42 + k, "melody", "h")
        ch = r.chord_at(q + 1e-3)
        r.add("harp", q, _dq(r, q, end - q), ch.tones(53, 67)[0], 42 + k, "arp", "h")
        r.add("pz_hi", q, _dq(r, q, 0.25), ch.tones(60, 72)[-1], 44 + k, "arp", "s")
    r.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=40, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(r, "cb", 28, 40, 40)
    r.expr(["glock"], [(0, -10), (4, -9)])
    r.expr(["celesta", "harp", "pz_hi"], [(0, -11), (4, -10)])
    r.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (4, -13)])
    # '好漂亮啊!': the radiant tutti (choir 'ah', brass, strings, timpani, cymbal, harp sweep, glockenspiel)
    t.add("timp", 0, 0.5, "F2", 52, "timp", "h")
    t.add("okit", 0, t.n_q, 57, 40, "perc", "h")
    t.add("glock", 0, 1, "F6", 50, "arp", "h")
    t.add("pz_cb", 0, 0.5, "F1", 56, "bass", "h")
    gliss_in(t, "harp", 0, 0.35, midi("F4"), midi("F6"), v0=38, v1=52, scale=ChordTones(t.chord_at(0)))
    t.pad("choir", 3, 57, 74, vel=44, bass_ref=(41, 53))
    t.pad(["brass", "brass", "brass"], 3, 53, 70, vel=44, bass_ref=(41, 53))
    t.add("vln_mel", 0, t.n_q, "F5", 52, "melody")
    strings(t, vel=44, lo=57, hi=77)
    t.duck(3.0, parts=["choir", "brass", "vln_mel"])
    t.expr(["choir"], [(0, -14), (t.n_q, -13)])
    t.expr(["brass", "vln_mel"], [(0, -12), (t.n_q, -13)])
    t.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -12), (t.n_q, -12)])
    t.expr(["timp", "glock", "harp", "pz_cb"], [(0, -8), (t.n_q, -10)])
    # 'whenever I see the rainbow, I will remember my promise': soft pads only
    e.pad("ooh", 3, 57, 74, vel=36, bass_ref=(36, 48))
    e.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(e, "cb", 28, 40, 34)
    e.duck(3.0)
    e.expr(["ooh"], [(0, -17), (2, -19), (8, -20)])
    e.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (2, -16), (8, -16)])


def end(c):
    """Noah's theme b1-b2 (flute, harp) for the child after the rain; b5-b7 warm (clarinet, horn, strings, choir
    'ooh') on God's faithfulness; the parade's head on the celesta (so many animals); the question (B-flat, C sus4,
    very soft); the final F chord at the end of the question, ringing through the closing pause to the end."""
    c.gain(-2.6)
    t_b = c.gap(c.find("上帝说过的话"))
    t_q = c.gap(c.find("对了"))
    t_w = c.at("你最喜欢")
    t_f = c.le(c.find("你最喜欢"))
    splashes = picture(c, "splash_small", c.ls(0) - 0.3, c.le(0)) or []
    pops = picture(c, "pop", c.ls(2) - 0.3, t_f) or []
    t_chime = on_picture(c, "chime", t_f, c.dur, 1, lambda: [None])[0]
    a = c.seg(0, t_b, 2, "4/4", "F major", nominal=76, label="end-rainbow")
    b = c.seg(t_b, t_q, 3, "4/4", "F major", nominal=100, label="end-promise")
    q = c.seg(t_q, t_w, 1, "4/4", "F major", nominal=88, label="end-animals")
    w = c.seg(t_w, t_f, 1, "4/4", "F major", nominal=110, label="end-question")
    f = c.seg(t_f, c.dur, 1, "2/4", "F major", nominal=90, rit=0.3, label="end-final-chord")
    for sg in (a, b, q, w):
        sg.duck(1.5)
    a.prog(" | ".join(NOAH_PROG[:2]))
    b.prog(" | ".join(NOAH_PROG[4:7]))
    q.prog("F:4")
    w.prog("Bb:2 Csus4:2")
    f.prog("F:2")
    f.sync("the final F major chord (after the question)", 0, t_f, kind="change")
    f.sync("the final chord: harp roll", 0, t_f)
    # next time you see a rainbow after the rain: the theme on the flute, harp
    a.mel("flute", bars(NOAH, 0, 2), vel=54)
    broken(a, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 41, 53, vel=38, thin=True)
    strings(a, vel=40, lo=55, hi=72)
    a.duck(2.5, parts=["flute", "harp"])
    a.expr(["flute"], [(0, -19), (1.5, -14.5), (8, -14.5)])
    a.expr(["harp"], [(0, -17), (1.5, -11), (8, -11)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -19), (2, -15), (8, -15)])
    for k, t in enumerate(splashes[:2]):                  # splish, splash: the child jumps in the puddle
        sg, qs = seg_at(c, (a, b), t)
        sg.add("pz_hi", qs, _dq(sg, qs, 0.25), top(sg, qs, 72, 84), 56, "arp", "h")
        sg.add("celesta", qs, _dq(sg, qs, 0.25), top(sg, qs, 84, 96), 46, "arp", "h")
        sg.add("pz_lo", qs, _dq(sg, qs, 0.25), sg.chord_at(qs + 1e-3).bass_note(41, 53), 50, "bass", "h")
        sg.sync(f"puddle splash {k + 1}", qs, t)
    a.expr(["pz_hi", "celesta", "pz_lo"], [(0, -12), (8, -13)])
    # what God says, he will do; God remembers you, just as he remembered Noah: b5-b7, warm
    b.mel("clar", bars(NOAH, 4, 7), vel=56)
    b.mel("horn", "F3:4 | F3:2 F3:2 | G3:2 G3:2", vel=44, role="counter")
    broken(b, "harp", 0, 12, (0, 2, 4, 6, 4, 2), 41, 53, vel=36, thin=True)
    strings(b, vel=42, lo=55, hi=72)
    b.pad("ooh", 3, 55, 72, vel=36, q0=4, bass_ref=(41, 53))
    b.duck(3.0, parts=["clar", "horn", "harp", "ooh"])
    b.expr(["clar"], [(0, -16), (1.5, -12), (12, -12)])
    b.expr(["horn", "harp"], [(0, -16), (1.5, -13), (12, -13)])
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (1.5, -14), (12, -14)])
    b.expr(["ooh"], [(4, -20), (6, -17), (12, -17)])
    # 'so many animals in the ark...': the parade's head, small, on the celesta and pizzicato
    q.mel("celesta", "C5:1/2 F5:1/2 A5:1/2 F5:1/2 C6:1 A5:1", vel=42, role="arp")
    q.mel("pz_lo", "F2:1:s r:1 C3:1:s r:1", vel=44, role="bass")
    q.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    q.expr(["celesta"], [(0, -12), (4, -13)])
    q.expr(["pz_lo"], [(0, -12), (4, -12)])
    q.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (4, -17)])
    for t in pops:                                         # the animals pop up, one after another
        sg, qp = seg_at(c, (q, w), t)
        sg.add("celesta", qp, _dq(sg, qp, 0.25), top(sg, qp, 81, 93, 0), 32, "arp", "s")
    # '...which one do you like best?': a very soft question
    w.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    w.add("cb", 0, 2, "Bb1", 32, "bass")
    w.add("cb", 2, 2, "C2", 32, "bass")
    w.add("harp", 0, 2, "D5", 34, "arp")
    w.add("harp", 2, 2, "G5", 34, "arp")
    w.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -17), (4, -18)])
    w.expr(["harp"], [(0, -13), (4, -13)])
    # the final F major chord rings through the closing pause: harp rolled up, flute, celesta, strings, ooh
    f.add("flute", 0, 2, "A5", 50, "melody")
    for k_, nm in enumerate(["F2", "C3", "F3", "A3", "C4", "F4", "A4", "C5", "F5"]):
        f.add("harp", 0.06 * k_, 2 - 0.06 * k_, nm, 46 - 2 * k_, "arp", "r")
    f.mel("celesta", "C6:1/2 F6:1/2 A6:1", vel=36, art="r", role="arp")
    if t_chime is not None and f.q_of(c.t0 + t_chime) < f.n_q - 0.3:      # the rainbow's chime
        f.add("glock", f.q_of(c.t0 + t_chime), 0.5, "C7", 34, "arp", "r")
    strings(f, vel=40, lo=57, hi=72)
    f.pad("ooh", 3, 57, 72, vel=38, bass_ref=(41, 53))
    f.expr(["flute", "vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -15), (0.5, -14.5), (1.4, -17), (2, -26)])
    f.expr(["harp", "celesta", "glock"], [(0, -13), (2, -17)])


SCENE_CUES = {
    "s01_title": title, "s02_rain": rain, "s03_world": world, "s04_noah": noah, "s05_command": command,
    "s06_build": build, "s07_animals": animals, "s08_door": door, "s09_flood": flood, "s10_inside": inside,
    "s11_dove": dove, "s12_out": out, "s13_rainbow": rainbow, "s14_end": end,
}

# Hit points the score must place, defined by the narration text (audio/music_check.py REQUIRED_HITS format:
# (scene, phrase, mode, kind); mode 'line' / 'gap' / 'phrase' / 'end', kind 'hit' (attack) or 'change' (harmony)).
# Where a sound word is also an on-screen action (the elephants' 咚s, the rabbits' hops, the saw and the hammer,
# the door) the phrase is where the harmony arrives, and the attacks themselves follow the picture: PICTURE_HITS.
REQUIRED_HITS = [
    ("s02_rain", "哗啦啦", "phrase", "change"),                 # the rain pours (D minor)
    ("s03_world", "上帝看见了", "gap", "change"),               # God is sad (G minor)
    ("s04_noah", "他的名字叫挪亚", "phrase", "change"),         # Noah's theme (F major)
    ("s05_command", "可是，挪亚还是", "gap", "change"),          # Noah obeys (his theme)
    ("s06_build", "造好了", "phrase", "change"),                # the ark is finished (C major)
    ("s07_animals", "咚，咚，咚", "phrase", "change"),           # the elephants (B-flat; the stomps: picture / voice)
    ("s07_animals", "嗷呜", "phrase", "change"),                # the lion's roar: E-flat (the attack: picture)
    ("s07_animals", "它们都是两个两个来的", "gap", "change"),    # the march two by two
    ("s08_door", "把门关上了", "phrase", "change"),             # God shuts the door: the warm chord (thunk: picture)
    ("s09_flood", "哗啦啦", "phrase", "change"),                # the pour (D minor)
    ("s09_flood", "方舟浮起来了", "phrase", "change"),          # the ark floats (B-flat)
    ("s10_inside", "可是上帝一直记得挪亚", "phrase", "change"),  # God remembers (E-flat)
    ("s11_dove", "又飞回来了", "phrase", "change"),             # the first dove comes home (F)
    ("s11_dove", "橄榄叶", "phrase", "change"),                 # the olive leaf (D major)
    ("s11_dove", "这一次", "phrase", "change"),                 # the last flight (open ending)
    ("s12_out", "门打开了", "phrase", "change"),                # the door opens: the parade returns (B-flat)
    ("s12_out", "感谢上帝", "phrase", "change"),                # the amen
    ("s13_rainbow", "红", "phrase", "change"),                  # the rainbow begins (F; the bands: picture)
    ("s13_rainbow", "紫", "phrase", "change"),                  # the last colour (C)
    ("s14_end", "你最喜欢哪一种呢", "end", "change"),           # the final chord, after the question
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or
# None, index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.  Filled in as the
# scenes are drawn (see the report in the hand-off).
PICTURE_HITS = [
    ("s02_rain", "splash_small", "小朋友", 0, 0.0, "hit", "'哗啦啦' 1: the big drops"),
    ("s02_rain", "splash_small", "小朋友", 1, 0.0, "hit", "'哗啦啦' 2"),
    ("s03_world", "whoosh", "他们不听", 0, 0.0, "hit", "the push ('你推我')"),
    ("s03_world", "whoosh", "他们不听", 1, 0.0, "hit", "the grab ('我抢你')"),
    ("s04_noah", "pop", "挪亚有三个儿子", 0, 0.0, "hit", "Shem"),
    ("s04_noah", "pop", "挪亚有三个儿子", 1, 0.0, "hit", "Ham"),
    ("s04_noah", "pop", "挪亚有三个儿子", 2, 0.0, "hit", "Japheth"),
    ("s06_build", "ship_creak", "锯木头", 0, 0.0, "hit", "saw stroke 1 ('嘎吱')"),
    ("s06_build", "ship_creak", "锯木头", 1, 0.0, "hit", "saw stroke 2 ('嘎吱')"),
    ("s06_build", "coins", "钉钉子", 0, 0.0, "hit", "hammer '叮'"),
    ("s06_build", "coins", "钉钉子", 1, 0.0, "hit", "hammer '叮'"),
    ("s06_build", "coins", "钉钉子", 2, 0.0, "hit", "hammer '当'"),
    ("s06_build", "coins", "钉钉子", 3, 0.0, "hit", "hammer '当'"),
    ("s07_animals", "thud", "大象来了", 0, 0.0, "hit", "elephant stomp 1 ('咚')"),
    ("s07_animals", "thud", "大象来了", 1, 0.0, "hit", "elephant stomp 2 ('咚')"),
    ("s07_animals", "thud", "大象来了", 2, 0.0, "hit", "elephant stomp 3 ('咚')"),
    ("s07_animals", "whoosh", "小鸟飞来了", 0, 0.0, "hit", "flap 1 ('扑')"),
    ("s07_animals", "whoosh", "小鸟飞来了", 1, 0.0, "hit", "flap 2 ('扑')"),
    ("s07_animals", "whoosh", "小鸟飞来了", 2, 0.0, "hit", "flap 3 ('扑')"),
    ("s07_animals", "whoosh", "小鸟飞来了", 3, 0.0, "hit", "the lion's roar ('嗷呜')"),
    ("s07_animals", "pop", "小兔子跳来了", 0, 0.0, "hit", "hop 1 ('蹦')"),
    ("s07_animals", "pop", "小兔子跳来了", 1, 0.0, "hit", "hop 2 ('蹦')"),
    ("s07_animals", "pop", "小兔子跳来了", 2, 0.0, "hit", "hop 3 ('蹦')"),
    ("s11_dove", "thud", "方舟停在了", 0, 0.0, "hit", "the ark settles on Ararat"),
    ("s08_door", "thud", "把门关上了", 0, 0.0, "hit", "the door shuts (a gentle low thunk)"),
    ("s09_flood", "drip", "滴答", 0, 0.0, "hit", "drip 1 ('滴')"),
    ("s09_flood", "drip", "滴答", 1, 0.0, "hit", "drip 2 ('滴')"),
    ("s09_flood", "thunder", "七天以后", 0, 0.0, "hit", "thunder (a soft rumble)"),
    ("s09_flood", "splash", "大雨下了", 0, 0.0, "hit", "the water rises 1"),
    ("s09_flood", "splash", "大雨下了", 1, 0.0, "hit", "the water rises 2"),
    ("s12_out", "ship_creak", "门打开了", 0, 0.0, "hit", "the door opens"),
    ("s12_out", "thud", "挪亚做的第一件事", 0, 0.0, "hit", "altar stone 1"),
    ("s12_out", "thud", "挪亚做的第一件事", 1, 0.0, "hit", "altar stone 2"),
    ("s12_out", "thud", "挪亚做的第一件事", 2, 0.0, "hit", "altar stone 3"),
    ("s12_out", "thud", "挪亚做的第一件事", 3, 0.0, "hit", "altar stone 4"),
    ("s13_rainbow", "sparkle", "红", 0, 0.0, "hit", "colour band 1 (红)"),
    ("s13_rainbow", "sparkle", "红", 1, 0.0, "hit", "colour band 2 (橙)"),
    ("s13_rainbow", "sparkle", "红", 2, 0.0, "hit", "colour band 3 (黄)"),
    ("s13_rainbow", "sparkle", "红", 3, 0.0, "hit", "colour band 4 (绿)"),
    ("s13_rainbow", "sparkle", "红", 4, 0.0, "hit", "colour band 5 (青)"),
    ("s13_rainbow", "sparkle", "红", 5, 0.0, "hit", "colour band 6 (蓝)"),
    ("s13_rainbow", "sparkle", "红", 6, 0.0, "hit", "colour band 7 (紫)"),
    ("s13_rainbow", "chime", "红", 0, 0.0, "hit", "'好漂亮啊': the radiant tutti"),
    ("s14_end", "splash_small", "小朋友", 0, 0.0, "hit", "puddle splash 1"),
    ("s14_end", "splash_small", "小朋友", 1, 0.0, "hit", "puddle splash 2"),
]
