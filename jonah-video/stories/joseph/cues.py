"""The background score for 约瑟和彩衣 (Genesis 37-50, ~4:25) -- one continuous piece in 14 cues.

Read by audio/score.py when the story is "joseph" (SCENE_CUES); REQUIRED_HITS / PICTURE_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework and orchestra as the Jonah, Daniel, David and Noah
scores (audio/scorekit.py, audio/scorelib.py): every cue starts at its scene's global start, is planned in whole
bars whose tempo follows the real line timings, and is keyed to narration phrases (Cue.find / Cue.at / Cue.gap),
never to fixed times.  Hits that show an on-screen action (the colour bands of the coat, the coat pulled off, the
coins, the gulp of the thin cows, the chariot...) follow the PICTURE where the scene declares a sound-effect cue
for it: picture() reads the scene's own sfx cues at build time (engine.loader.build_scene(...).sfx_cues, the same
source as music_check's PICTURE_HITS), so they move when a scene is edited; the narration phrase then marks where
the harmony arrives (a 'change' in REQUIRED_HITS).  pic() picks a scene's sfx cue exactly as music_check picks a
PICTURE_HITS target (k-th cue of a name from the start of the line containing a phrase), and accent() puts the attack
wherever that cue falls in the cue, on tones of the chord sounding there -- so a hit never drops out or clashes when a
scene is re-timed.  Without a scene that builds, those hits fall back to the narrator's own voice: syl() aligns the
recorded line's voice islands to the punctuation groups of the text (红的、黄的、蓝的、绿的 -> one onset per colour
word) by a monotone least-squares match; the subtitle-chunk interpolation is the fallback when the clip is missing or
does not match.

Themes
  Joseph (D major, 4/4; clarinet or oboe over harp; motif x = the rising 3-5-8 'F# A D', the boy looking up):
     b1 D        F#4 A4 D5--             b5 D        F#4 A4 D5--
     b2 G  A     B4 D5 C#5 E5            b6 G  D/F#  B4 D5 G5. F#5
     b3 Bm G     F#5. E5 D5 B4           b7 Em7 A7   E5 G5 F#5 E5
     b4 Em7 A7   E5. D5 C#5--            b8 D        D5---
     innocent: clarinet + harp (s01, s03, s05 in G walking to his brothers); sad: the minor version, slower, a
     solo oboe (the pit in E minor, the caravan in A minor, the ending's three misfortunes); noble: horns and
     violins (s11, '管理全埃及'); tender and full: violins, horn counter-melody, choir (s13, s14).
  The coat: a sparkling glockenspiel/celesta scale, one note per colour word as the bands appear, D E F# G and
     the A of '好漂亮' (红 D, 黄 Em, 蓝 F#m, 绿 G over a rising bass, D again on '好漂亮'); torn off in s05 it
     falls (G6 E6 C6 G5 over C), and comes back broken in s07 (D5 E5 F5 -- and stops).
  The brothers' jealousy: a sly, grumbling staccato bassoon (low clarinet answering), sliding down chromatically,
     comic, never menacing:  Em  E3 . G3 F#3 F3 E3 B2- | Am B7  A2 . C3 B2 D#3 F#3 A3-.  In s12 the same notes,
     slow and legato (the brothers come tired and hungry); in s13 small and frightened.
  The dream (D major, 6/8, harp and celesta, Dmaj7 Bm7 Gmaj7): the sheaves bow -- a celesta scale falling in
     eighths G6 F#6 E6 | D6 C#6 B5 over G | A7sus4 with a harp glissando down -- onto the glowing sheaf's chord, D
     major lit up (glockenspiel, harp rolled up, choir, a soft timpani touch) on '下拜'; the same gesture and chord
     on '现在真的发生了' in s12.
  The pit and the caravan (A harmonic minor, 4/4 plod): a frame drum DUM . . ka DUM . . ka, plucked basses, camel
     bells (a soft triangle), an oboe with the F-G# augmented second; the twenty pieces of silver (glockenspiel and
     celesta clinks) on F, the Phrygian side of A.
  Jacob's grief: a slow cello lament in D minor (3/4 -> 4/4), the deceptive A7 -> B-flat on '哭了很久很久'.
  Egypt: D hijaz (harp, oboe with the Eb-F# step, a soft frame drum); God with Joseph: warm B-flat chords (choir
     'ooh', strings, horn) on both '上帝(还是)和约瑟同在', and on '是上帝' in prison.
  Pharaoh's dream: the court (D minor, stately horns, Eb Phrygian side); seven fat cows -- a plump tuba/bassoon
     waltz in F (3/4); the thin cows -- a thin staccato violin note for each as it climbs out of the Nile, a thin high
     tremolo, D minor; A on '吃掉了' and gulp-gulp-gulp on the picture (plucked basses, bassoon, woodblock, the first
     with tuba, timpani and bass drum); plenty (D major, harp up, glockenspiel) vs famine (D minor, bare low fifths).
  The ruler: the theme on horns and violins in D on '管理全埃及'; Em7 A7 on '坐上了大马车' (a snare roll, a thump as he
     lands in the chariot); the processional when the horse sets off with the scene's herald's horn (oom-pah, snare,
     timpani, a light flute fanfare; the brass enters with the theme's b2 only after the horn call, so the orchestral
     brass never sits on the sfx shofar); the grain heaped high (a run up into D).

Tonal plan
  s01 title D (theme b1-b2, clarinet; a glint on the coat) -> s02 G 3/4 (a tender question, clarinet) | E minor
  sulk (bassoon) | B minor, the brothers' motif peeks ('被他的哥哥们欺负得好惨') | D on '可是后来' (motif x on the
  horn, harp up) -> s03 D: Jacob (cello melody, twelve harp notes for the twelve sons) | theme b1-b2 (clarinet) |
  Em7 A7 shimmer ('彩色的衣服') | the colours D Em F#m G (red, yellow, blue, green) | D on '好漂亮' | D B7 |
  E minor jealousy on '酸溜溜的' (bassoon), ending on B7 -> s04 D 6/8 dream: night (Dmaj7 Bm7, celesta stars) |
  Gmaj7 Dmaj7 | the sheaf stands up (Em7 A, a rising arpeggio) | circling Bm7, the bow G A7sus4 | D glowing on
  '下拜' | E minor, the brothers angrier (bassoon + trombone, a mock fanfare on C B7) -> s05 G: Joseph walks to his
  brothers (theme b1-b2 in G, walking pizzicato) | E minor plot ('看，那个做梦的来了') | C on '剥下约瑟的彩衣' (the
  coat motif falling) | the dry pit (Am, F B7; hollow) | E minor, the sad motif on the oboe ('哥哥！放我出去')
  -> s06 A harmonic minor caravan (plod, oboe) | Am E | F on '二十块银子' (coins) | Dm Am fading far away -> s07 D
  minor: the broken coat motif (3/4) | the cello lament (Dm A7) | B-flat on '哭了很久很久' -> s08 D hijaz Egypt |
  B-flat on '上帝和约瑟同在' | theme b1-b3 in B-flat (oboe, walking pizzicato: the trusted servant) | D minor on
  '被人冤枉' (falling bass D C Bb A) | B-flat on '上帝还是和约瑟同在' -> s09 G minor prison, Ebmaj7 dreams |
  theme b1-b2 in B-flat (clarinet) ending on F7 | B-flat on '是上帝' -> s10 D minor court (Eb, Gm, A) | F waltz
  (fat cows) | D minor thin cows | A on the gulp '吃掉了' | Gm A7 shrug | D, motif x on the oboe ('有人想起了约瑟') |
  Em7 A7 | D G plenty on '七年大丰收' | D minor famine on '七年大饥荒' | Bb A -> s11 G (God with you) Em7 A7, a timpani
  roll | D noble theme on '管理全埃及' (horns, violins; glints on the ring, the robe and the gold chain) | Em7 A7 on
  '坐上了大马车' | D processional as the horse sets off | G A D, the run up ('像山一样高') -> s12 D minor famine | the brothers' motif slow (Dm Gm Dm A) |
  B-flat on '跪下下拜' (a bow), A | the dream again (Bm7 Gmaj7, the bow G A7sus4) | D glowing on '现在真的发生了'
  -> s13 G Em7 A7sus4 (Joseph cannot hold back) | D, theme b1 in the violins, choir, on '我就是约瑟' | B minor fear
  (tremolo, the motif small) | D A/C# tender ('不要害怕') | G on '可是上帝把它变成了好事' (choir), Em7 A7 | theme
  b5-b7 full (violins, horn, Jacob's cellos) | D on '一家人，又在一起了' (choir 'ah', timpani, harp, glockenspiel)
  -> s14 B minor, E minor, F# (three misfortunes, a low clarinet) | D on '可是他从来没有离开上帝' (choir, theme b1-b2
  on the flute) | the question (Em7 Gmaj7, a celesta) | A7sus4 held softly through the 2 s pause | theme b5-b7 warm
  (clarinet, horn, strings, choir) | the final D major chord on the end of '学会原谅', ringing to the end.

All the music stays under the narration (Seg.duck, low expression levels); the loud moments are short and
child-safe (comic cows and gulp, a warm processional, the forgiveness swelling under the words); God's presence
gets only soft sustained chords.
"""
import re

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
from audio.theory import midi, pc

# ------------------------------------------------------------------------------------------- themes
JOSEPH = ["F#4:1 A4:1 D5:2", "B4:1 D5:1 C#5:1 E5:1", "F#5:3/2 E5:1/2 D5:1 B4:1", "E5:3/2 D5:1/2 C#5:2",
          "F#4:1 A4:1 D5:2", "B4:1 D5:1 G5:3/2 F#5:1/2", "E5:1 G5:1 F#5:1 E5:1", "D5:4"]
JOSEPH_PROG = ["D:4", "G:2 A:2", "Bm:2 G:2", "Em7:2 A7:2", "D:4", "G:2 D/F#:2", "Em7:2 A7:2", "D:4"]

# the brothers' jealousy (E minor; bassoon, staccato)
JEALOUS = ["E3:1/2:s r:1/2 G3:1/2:s F#3:1/2:s F3:1/2:s E3:1/2:s B2:1:s",
           "A2:1/2:s r:1/2 C3:1/2:s B2:1/2:s D#3:1/2:s F#3:1/2:s A3:1:s"]
JEALOUS_PROG = ["Em:4", "Am:2 B7:2"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
_CH = re.compile(r"^([A-G](?:#|b)?)([^/]*)(?:/([A-G](?:#|b)?))?$")


def tprog(spec, k, flats=False):
    """A chord progression transposed by k semitones."""
    names = _FLAT if flats else _SHARP
    out = []
    for tok in spec.split():
        if tok == "|":
            out.append(tok)
            continue
        body, at, sc = tok.partition("@")
        sym, d = body.rsplit(":", 1)
        m = _CH.match(sym)
        new = names[(pc(m.group(1)) + k) % 12] + m.group(2)
        if m.group(3):
            new += "/" + names[(pc(m.group(3)) + k) % 12]
        out.append(f"{new}:{d}" + (at + sc if at else ""))
    return " ".join(out)


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…"
SOUND_CHARS = set()        # this script has no sound words spoken syllable by syllable
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


def accent(c, segs, t, what=None, glock=None, celesta=None, harp=None, pluck=None, low=None, vel=46):
    """A picture hit at cue-relative time t, in whichever of segs it falls: chord tones of the chord sounding there --
    glock / celesta / harp / pluck = (lo, hi) ranges for a glockenspiel, celesta, harp or pizzicato note (the
    highest chord tone in range), low=True a soft thump (timpani, plucked basses, bass drum).  Synced as a hit
    when `what` is given.  Returns (segment, q)."""
    sg, q = seg_at(c, segs, t)
    if glock:
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, *glock), vel, "arp", "h")
    if celesta:
        sg.add("celesta", q, _dq(sg, q, 1.0), top(sg, q, *celesta), vel - 6, "arp", "h")
    if harp:
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, *harp), vel, "arp", "h")
    if pluck:
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, *pluck), vel + 4, "arp", "h")
    if low:
        thump(sg, q, vel=vel + 2)
    if what:
        sg.sync(what, q, t)
    return sg, q


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
STR = ["vla", "vln2", "vln1", "vc", "cb"]


def strings(seg, vel=44, lo=53, hi=72, bass=(41, 53), q0=0.0, q1=None, cb=(29, 41), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vln2", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
            bass_hi=bass[1])
    if cb:
        bassline(seg, "cb", cb[0], cb[1], cb_vel or vel - 2, q0=q0, q1=q1)


def name_of(p):
    from audio.theory import name
    return name(p)


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


def thump(seg, q, vel=50, kit=True):
    """A soft low accent (timpani, plucked basses, a bass drum) on tones common to the chord there and the chord a
    little later."""
    pcs = seg.chord_at(q + 1e-3).pcset & seg.chord_at(min(q + 0.4, seg.n_q - 1e-3)).pcset or \
        seg.chord_at(q + 1e-3).pcset
    seg.add("timp", q, _dq(seg, q, 0.5), [p for p in range(38, 51) if p % 12 in pcs][0], vel, "timp", "h")
    seg.add("pz_cb", q, 0.4, [p for p in range(29, 41) if p % 12 in pcs][0], vel + 2, "bass", "h")
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


def camel(seg, q0, q1, vel=56, bells=True):
    """The camels' plod: a frame drum DUM . . ka DUM . . ka (low drum on the beats 1 and 3, a slap on the
    upbeats), plucked basses on the DUMs, a soft camel bell (triangle) on each bar's first beat."""
    q = q0
    while q < q1 - 1e-6:
        pos = (q - q0) % 4
        if pos in (0, 2):
            drum(seg, q, 45, vel if pos == 0 else vel - 6)
            ch = seg.chord_at(q + 1e-3)
            seg.add("pz_cb", q, _dq(seg, q, 1.0), ch.bass_note(33, 45) if pos == 0 else
                    [p for p in ch.tones(33, 52) if (p - ch.bass) % 12 == 7][0], vel - 4, "bass", "s")
            if pos == 0 and bells:
                drum(seg, q, 81, vel - 32)
        else:
            drum(seg, q, 60, vel - 14)
        q += 1.5 if pos in (0, 2) else 0.5


def clink(seg, q, k, vel=56):
    """A silver coin: a glockenspiel and a celesta chord tone (higher with k), a tiny woodblock tick."""
    ts = seg.chord_at(q + 1e-3).tones(84, 98)
    p = ts[min(k, len(ts) - 1)]
    seg.add("glock", q, _dq(seg, q, 0.5), p, vel - 3 * (k % 2), "arp", "h")
    seg.add("celesta", q, _dq(seg, q, 0.5), p - 12, vel - 10, "arp", "h")
    drum(seg, q, 76, vel - 16)


def jealous(seg, q, k=0, vel=56, part="bsn", transpose=0):
    """The brothers' jealousy: bar k of the sly bassoon motif at q (E minor; transposed)."""
    seg.mel(part, JEALOUS[k], q=q, vel=vel, transpose=transpose)


def bow(seg, q0, vel=44, harp=True, q_end=None):
    """The sheaves bow: a celesta scale falling G6 F#6 E6 D6 C#6 B5 over a 6/8 bar of G | A7sus4 starting at q0 (in
    eighths; squeezed into [q0, q_end] when the picture's bow comes before the bar ends), a harp glissando down with
    it.  The landing A5 on the sheaf's chord is written by glow()."""
    q1 = min(q0 + 3.0, seg.n_q) if q_end is None else max(q0 + 1.2, min(q_end, q0 + 3.0))
    step = (q1 - q0) / 6
    for k, nm in enumerate(["G6", "F#6", "E6", "D6", "C#6", "B5"]):
        seg.add("celesta", q0 + k * step, step, nm, vel, "melody", voice="celesta.0")
    if harp:
        dur = seg.t(q1) - seg.t(q0) - 0.08
        gliss_in(seg, "harp", q0 + 0.1, dur, midi("A4"), midi("G6"), up=False, v0=40, v1=30)


def glow(seg, q=0.0, vel=50, choir=True, land=None):
    """The glowing sheaf: D major lit up -- a harp rolled up, choir 'ooh' and strings from the chord change at q; the
    attack where the sheaves touch down (land = (segment, q), default the change): the celesta lands on A5, a
    glockenspiel D6 + A6, a soft timpani and plucked-bass D -- tones common to the A7sus4 before and the D (the same
    sonority in s04 and at the callback in s12)."""
    lseg, lq = land if land is not None else (seg, q)
    lseg.add("celesta", lq, _dq(lseg, lq, 1.0), "A5", vel - 6, "melody", voice="celesta.0")
    lseg.add("glock", lq, _dq(lseg, lq, 1.0), "D6", vel, "arp", "h")
    lseg.add("glock", lq, _dq(lseg, lq, 1.0), "A6", vel - 6, "arp", "h")
    lseg.add("timp", lq, _dq(lseg, lq, 0.5), "D3", vel - 10, "timp", "h")
    lseg.add("pz_cb", lq, _dq(lseg, lq, 0.5), "D2", vel - 4, "bass", "h")
    if lseg is seg and lq > q + 0.05:                     # the picture's bow comes after the change: hold the D
        seg.add("glock", q, lq - q, "F#6", vel - 12, "arp")
    harp_roll(seg, q, ["D3", "A3", "D4", "F#4", "A4", "D5"], vel=vel - 2)
    if choir:
        seg.pad("ooh", 3, 57, 74, q0=q, vel=40, bass_ref=(38, 50))


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """Joseph's theme b1-b2 on the clarinet over harp and soft strings (D major); a glockenspiel glint on the coat."""
    c.gain(-9.0)
    s = c.seg(0, c.dur, 2, "4/4", "D major", nominal=96, label="title")
    s.duck(1.0)
    s.duck(4.0, parts=["clar"])
    s.prog(" | ".join(JOSEPH_PROG[:2]))
    s.mel("clar", bars(JOSEPH, 0, 2), vel=62)
    broken(s, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 38, 50, vel=42)
    strings(s, vel=46, lo=54, hi=71)
    t_gl = pic(c, "sparkle", "圣经绘本")                  # '彩衣': the coat twinkles (on the picture)
    if t_gl is not None:
        q_gl = qpos(s, c, t_gl)
        s.add("glock", q_gl, _dq(s, q_gl, 1.0), top(s, q_gl, 86, 100), 42, "arp", "h")
        s.sync("the coat twinkles ('彩衣')", q_gl, t_gl)
    else:
        s.add("glock", 2.5, 1.0, "D7", 40, "arp", "r")    # D: in the D and the G chord
    s.expr(["clar"], [(0, -11), (8, -12)])
    s.expr(["harp"], [(0, -9), (8, -10)])
    s.expr(STR, [(0, -16), (1, -12), (8, -12)])
    s.expr(["glock"], [(0, -10), (8, -10)])


def question(c):
    """A tender question (G major, 3/4, clarinet and harp); the sulk (E minor, a long bassoon); the story of a boy
    bullied by his brothers (B minor, their sly motif peeks in); D on '可是后来' (motif x on the horn, harp up)."""
    c.gain(-2.4)
    t_a = c.at("你有没有生过")
    t_s = c.gap(c.find("今天的故事里"))
    t_b = c.at("可是后来")
    a = c.seg(0, t_a, 2, "3/4", "G major", nominal=92, label="question-bullied")
    b = c.seg(t_a, t_s, 2, "3/4", "E minor+", nominal=78, label="question-sulk")
    s = c.seg(t_s, t_b, 2, "4/4", "B minor+", nominal=86, label="question-story")
    h = c.seg(t_b, c.dur, 1, "4/4", "D major", nominal=60, label="question-but")
    for sg in (a, b, s, h):
        sg.duck(1.5)
    a.prog("G:3 | C:3")
    b.prog("Em:3 | C:3/2 B7:3/2")
    s.prog("Bm:4 | Em:2 F#7:2")
    h.prog("D:4")
    h.sync("'可是后来': D major, hope (motif x)", 0, t_b, kind="change")
    # 'have you ever been bullied by your big brothers and sisters?': a gentle clarinet, harp
    a.mel("clar", "B4:3/2 D5:1/2 G4:1 | E5:3/2 C5:1/2 G4:1", vel=56)
    broken(a, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 43, 55, vel=36, thin=True)
    a.pad(["vla", "vln2"], 2, 55, 69, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    a.duck(2.5, parts=["clar", "harp"])
    a.expr(["clar"], [(0, -13), (6, -13)])
    a.expr(["harp"], [(0, -10), (6, -10)])
    a.expr(["vla", "vln2", "vc"], [(0, -18), (1.5, -15), (6, -15)])
    # 'angry with someone for a long, long time?': a sulking bassoon, a pouting clarinet
    b.mel("bsn", "E3:3 | E3:3/2 D#3:3/2", vel=52)
    b.mel("clar", "G4:1 F#4:1/2 E4:3/2 | r:3", vel=50)
    b.pad(["vla", "vln2"], 2, 52, 67, vel=36, bass_ref=(40, 52))
    bassline(b, "cb", 28, 40, 38)
    b.expr(["bsn"], [(0, -12), (6, -12)])
    b.expr(["clar"], [(0, -14), (6, -15)])
    b.expr(["vla", "vln2", "cb"], [(0, -17), (6, -16)])
    # 'in today's story a boy was bullied terribly by his brothers': B minor, their sly motif peeks in
    jealous(s, 0, 0, vel=50, transpose=-5)
    jealous(s, 4, 1, vel=48, transpose=-5)
    s.pad(["vla", "vln2"], 2, 50, 66, vel=34, bass_ref=(35, 47))
    bassline(s, "cb", 31, 43, 36)
    s.expr(["bsn"], [(0, -14), (8, -14)])
    s.expr(["vla", "vln2", "cb"], [(0, -18), (8, -16)])
    # 'but later he did something wonderful': D major, motif x on the horn, a harp sweep up, strings
    h.mel("horn", "F#3:1 A3:1 D4:2", vel=54)
    gliss_in(h, "harp", 0.5, 0.5, midi("D4"), midi("D6"), v0=26, v1=40, scale=ChordTones(h.chord_at(0)))
    h.add("glock", 2, 1, "A6", 34, "arp", "h")
    strings(h, vel=42, lo=54, hi=72)
    h.duck(2.0, parts=["horn"])
    h.expr(["horn"], [(0, -19), (1, -14), (3, -14), (4, -17)])
    h.expr(["harp", "glock"], [(0, -14), (1, -11), (4, -12)])
    h.expr(STR, [(0, -20), (1.5, -15), (3, -15), (4, -18)])
    # the picture: she grabs the toy horse, stumbles back with it; the little storm cloud; the coat's sparkle burst
    segs = (a, b, s, h)
    t_grab = pic(c, "cloth", "小朋友")
    if t_grab is not None:
        sg, q = seg_at(c, segs, t_grab)
        pluck_chord(sg, q, vel=56, lo=59, hi=71)
        drum(sg, q, 77, 50)
        sg.sync("the sister grabs the toy horse", q, t_grab)
    t_fall = pic(c, "thud", "小朋友")
    if t_fall is not None:
        sg, q = seg_at(c, segs, t_fall)
        thump(sg, q, vel=56)
        sg.add("pz_lo", q, _dq(sg, q, 0.5), top(sg, q, 43, 55, 0), 58, "bass", "h")
        sg.sync("she stumbles back hugging it", q, t_fall)
    t_cloud = pic(c, "pop", "小朋友")
    if t_cloud is not None:
        sg, q = seg_at(c, segs, t_cloud)
        sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, 67, 79), 54, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 0.5), top(sg, q, 79, 91), 44, "arp", "h")
        sg.sync("the little storm cloud pops up ('很久很久')", q, t_cloud)
    t_zap = pic(c, "thunder", "小朋友")
    if t_zap is not None:                                # its tiny grumble: a soft timpani roll
        sg, q = seg_at(c, segs, t_zap)
        q1 = min(q + 1.0, span_end(sg, q + 1e-6) - 0.05)
        if q1 > q + 0.3:
            timp_roll(sg, q, q1, midi("E2"), 22, 30)
    t_great = pic(c, "sparkle", "今天的故事里")
    if t_great is not None:
        sg, q = seg_at(c, segs, t_great)
        sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, 86, 98), 46, "arp", "h")
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, 62, 74), 44, "arp", "h")
        sg.sync("the coat's sparkle burst ('很了不起的事')", q, t_great)
    for sg in segs:
        sg.expr(["pz_hi", "pz_lo", "celesta"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["hand", "okit"], [(0, -13), (sg.n_q, -13)])
        sg.expr(["timp", "pz_cb"], [(0, -10), (sg.n_q, -10)])


def coat(c):
    """Jacob and his twelve sons (D major, a warm cello melody, twelve harp notes); Joseph's theme b1-b2 on the
    clarinet ('雅各最疼爱的'); a shimmer for the coat (Em7 A7); the colours: a rising glockenspiel/celesta scale, one
    note per colour as it appears (红 D, 黄 Em, 蓝 F#m, 绿 G over a rising bass), D on '好漂亮'; the brothers frown (D
    B7) and the jealousy motif on '酸溜溜的' (E minor, bassoon), the grumbling question ending on B7."""
    c.gain(-2.4)
    t_j = c.gap(c.find("雅各最疼爱的"))
    t_coat = c.gap(c.find("他给约瑟做了"))
    t_red = c.at("红")
    t_green = c.at("绿")
    t_s = c.gap(c.find("哥哥们看见了"))
    t_sour = c.at("酸溜溜的")
    v_col = syl(c, "红", 5)                                   # 红的 黄的 蓝的 绿的 好漂亮
    pic_bands = [pic(c, "sparkle", "红", k) for k in range(4)]  # the colour bands appearing (picture)
    have_bands = None not in pic_bands
    bands = pic_bands if have_bands else v_col[:4]
    t_wow_pic = pic(c, "chime", "红")                         # '好漂亮': Joseph wears the coat (picture)
    t_wow = t_wow_pic if t_wow_pic is not None else v_col[4]
    t_wow = min(max(t_wow, t_green + 0.45, bands[-1] + 0.3), t_s - 0.75)
    long_wow = t_s - t_wow >= 1.15
    a = c.seg(0, t_j, 2, "4/4", "D major", nominal=72, label="coat-jacob")
    b = c.seg(t_j, t_coat, 2, "4/4", "D major", nominal=104, label="coat-joseph")
    co = c.seg(t_coat, t_red, 1, "4/4", "D major", nominal=76, label="coat-made")
    r = c.seg(t_red, t_wow, 1, "4/4", "D major", nominal=84, label="coat-colours")
    w = c.seg(t_wow, t_s, 1, "2/4" if long_wow else "3/8", "D major", nominal=92 if long_wow else 100,
              label="coat-beautiful")
    f = c.seg(t_s, t_sour, 1, "4/4", "D major", nominal=110, label="coat-frown")
    j = c.seg(t_sour, c.dur, 2, "4/4", "E minor+", nominal=124, label="coat-jealous")
    for sg in (a, b, co, r, w, f, j):
        sg.duck(1.5)
    a.prog("D:4 | Bm:2 A:2")
    b.prog(" | ".join(JOSEPH_PROG[:2]))
    co.prog("Em7:2 A7:2")
    # the colour chords (in 48ths of a quarter): D on the word 红, Em F#m on the bands of 黄 蓝, G on the word 绿
    e1 = min(max(bands[1], t_red + 0.25), t_green - 0.5)
    e2 = min(max(bands[2], e1 + 0.25), t_green - 0.25)
    e1, e2 = min(e1, e2 - 0.2), max(e2, e1 + 0.2)
    qs = [0.0] + [r.q_of(c.t0 + t) for t in (e1, e2, t_green)] + [r.n_q]
    edges = [int(round(q * 48)) for q in qs]
    for k in range(1, len(edges)):
        edges[k] = max(edges[k], edges[k - 1] + 6)
    edges[-1] = int(round(r.n_q * 48))
    r.prog(" ".join(f"{ch}:{edges[k + 1] - edges[k]}/48" for k, ch in enumerate(["D", "Em", "F#m", "G"])))
    w.prog(f"D:{w.n_q:g}")
    f.prog("D:2 B7:2")
    j.prog(" | ".join(JEALOUS_PROG))
    r.sync("'红': the colours begin (D)", 0, t_red, kind="change")
    r.sync("'绿': green (G)", edges[3] / 48, t_green, kind="change")
    j.sync("'酸溜溜的': the brothers' jealousy (E minor)", 0, t_sour, kind="change")
    j.sync("'酸溜溜的': the bassoon's first note", 0, t_sour)
    # long ago there was a father called Jacob, who had twelve sons: a warm cello melody, twelve harp notes
    a.mel("vc", "A3:2 F#3:1 D3:1 | D3:2 E3:2", vel=54)
    a.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=38, bass_ref=(33, 45))
    bassline(a, "cb", 33, 45, 40)
    sons = [pic(c, "pop", "很久以前", k) for k in range(12)]
    if None in sons:                                      # no picture: twelve even steps from '他有十二个儿子'
        t12 = c.at("他有十二个儿子")
        sons = [t12 + k * (t_j - 0.2 - t12) / 12 for k in range(12)]
    prev = 54
    for k, t in enumerate(sons):                          # twelve sons: twelve harp notes up the chord
        sg, q = seg_at(c, (a, b), t)
        ts = sg.chord_at(q + 1e-3).tones(prev + 1, 100) or sg.chord_at(q + 1e-3).tones(55, 100)
        prev = ts[0]
        sg.add("harp", q, _dq(sg, q, 0.5), prev, 54 if k in (0, 11) else 34 + k, "arp", "h")
        if k in (0, 11):                                  # the first son, and little Benjamin: a pluck and a glint
            sg.add("pz_hi", q, _dq(sg, q, 0.25), top(sg, q, 62, 74), 58, "arp", "h")
            if k == 11:
                sg.add("glock", q, _dq(sg, q, 1.0), top(sg, q, 86, 98), 50, "arp", "h")
            if pic(c, "pop", "很久以前", k) is not None:
                sg.sync("son 1 pops up" if k == 0 else "son 12 (Benjamin) pops up", q, t)
    a.duck(2.0, parts=["vc"])
    a.expr(["vc"], [(0, -14), (1, -11), (8, -11)])
    a.expr(["harp", "pz_hi", "glock"], [(0, -11), (8, -11)])
    a.expr(["vla", "vln2", "vln1", "cb"], [(0, -17), (2, -15), (8, -15)])
    # Jacob loved Joseph, his eleventh son, most: Joseph's theme on the clarinet, harp
    b.mel("clar", bars(JOSEPH, 0, 2), vel=58)
    broken(b, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 38, 50, vel=38, thin=True)
    strings(b, vel=40, lo=57, hi=74)
    b.duck(2.5, parts=["clar", "harp"])
    b.expr(["clar"], [(0, -12), (8, -12)])
    b.expr(["harp"], [(0, -10), (8, -10)])
    b.expr(STR, [(0, -15), (8, -15)])
    t_heart = pic(c, "sparkle", "雅各最疼爱的")             # the warm heart over Jacob and Joseph
    if t_heart is not None:
        sg, _ = accent(c, (a, b, co, r, w, f, j), t_heart, "the warm heart ('最疼爱的')", glock=(86, 98),
                       celesta=(74, 86), vel=44)
        sg.expr(["glock", "celesta"], [(0, -11), (sg.n_q, -11)])
    # he made Joseph a coat of many colours: a shimmer (harp sixteenths, celesta, high tremolo)
    broken(co, "harp", 0, 4, (0, 1, 2, 3, 4, 3, 2, 1), 55, 84, vel=34, step=0.25, thin=True)
    co.pad(["trem_va", "trem_hi", "trem_hi"], 3, 57, 77, vel=36, bass_ref=(40, 52))
    co.mel("celesta", "r:1 B5:1 r:1 C#6:1", vel=36, role="arp")
    bassline(co, "cb", 28, 40, 34)
    co.expr(["harp", "celesta"], [(0, -13), (4, -11)])
    co.expr(["trem_va", "trem_hi", "cb"], [(0, -20), (4, -15)])
    # 红、黄、蓝、绿: a note for every colour as its band appears, rising -- each the next chord tone up (D6 E6 F#6 G6
    # over the colour chords), glockenspiel and celesta, a harp and a pizzicato note under it
    words = "红黄蓝绿"
    prev = midi("C#6")
    for k, t in enumerate(bands):
        sg, q = seg_at(c, (co, r, w), t)
        ch = sg.chord_at(q + 1e-3)
        up = [p_ for p_ in ch.tones(prev + 1, prev + 7)] or [max(ch.tones(prev - 7, prev))]
        nm, prev = up[0], up[0]
        sg.add("glock", q, _dq(sg, q, 1.0), nm, 52 + k, "arp", "h")
        sg.add("celesta", q, _dq(sg, q, 1.0), nm - 12, 42 + k, "arp", "h")
        sg.add("harp", q, _dq(sg, q, 1.0), ch.tones(50, 62)[0], 44 + k, "arp", "h")
        sg.add("pz_hi", q, _dq(sg, q, 0.25), ch.tones(62, 74)[-1], 46 + k, "arp", "s")
        if have_bands:
            sg.sync(f"colour {k + 1} ({words[k]})", q, t)
    r.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=40, bass_part="vc", bass_lo=50, bass_hi=62)
    bassline(r, "cb", 38, 50, 40)
    r.expr(["glock"], [(0, -10), (4, -9)])
    r.expr(["celesta", "harp", "pz_hi"], [(0, -11), (4, -10)])
    r.expr(STR, [(0, -16), (4, -13)])
    # '好漂亮!': D major -- the scale's A, a harp sweep, a soft plucked chord, strings
    w.add("glock", 0, w.n_q, "A6", 52, "arp", "h")
    w.add("celesta", 0, w.n_q, "A5", 42, "arp", "h")
    gliss_in(w, "harp", 0, 0.35, midi("D4"), midi("D6"), v0=36, v1=50, scale=ChordTones(w.chord_at(0)))
    pluck_chord(w, 0, vel=54, lo=62, hi=74)
    w.add("pz_cb", 0, 0.5, "D2", 52, "bass", "h")
    strings(w, vel=42, lo=57, hi=76)
    if t_wow_pic is not None and abs(t_wow_pic - t_wow) > 0.01:     # the picture's twirl, away from the D arrival
        accent(c, (co, r, w, f, j), t_wow_pic, "'好漂亮': Joseph wears the coat", glock=(86, 98), pluck=(62, 74))
    else:
        w.sync("'好漂亮': Joseph wears the coat (D major)", 0, t_wow)
    w.expr(["glock", "celesta", "harp", "pz_hi", "pz_cb"], [(0, -10), (w.n_q, -12)])
    w.expr(STR, [(0, -14), (w.n_q, -15)])
    # the brothers saw it: the glow fades (D), B7 creeps in
    f.pad(["vla", "vln2"], 2, 54, 69, vel=36, bass_ref=(35, 47))
    f.mel("pz_lo", "D3:1:s r:1 B2:1:s r:1", vel=48, role="bass")
    f.mel("cb", "D2:2 B1:2", vel=36, role="bass")
    f.expr(["vla", "vln2", "cb"], [(0, -16), (4, -18)])
    f.expr(["pz_lo"], [(0, -12), (4, -12)])
    # their hearts went sour: the jealousy motif (bassoon), plucked basses, a low clarinet's grumbling question
    jealous(j, 0, 0, vel=60)
    j.mel("bsn", JEALOUS[1].replace("A3:1:s", "A3:1"), q=4, vel=58)
    j.mel("pz_cb", "E2:1:s r:1 B1:1:s r:1 | A1:1:s r:1 B1:1:s r:1", vel=54, role="bass")
    j.add("hand", 0, 0.25, 77, 46, "perc", "h")
    j.mel("clar", "r:4 | r:2 D#4:1/2:s F#4:1/2:s A4:1/2:s B4:1/2", vel=50)
    j.pad(["vla", "vln2"], 2, 52, 67, vel=32, bass_ref=(40, 52))
    j.expr(["bsn"], [(0, -12), (6, -12), (8, -16)])
    j.expr(["clar"], [(0, -13), (6, -13), (8, -18)])
    j.expr(["pz_cb", "hand"], [(0, -11), (6, -12), (8, -16)])
    j.expr(["vla", "vln2"], [(0, -15), (6, -15), (8, -14)])


def dream(c):
    """Night (D major 6/8: Dmaj7 Bm7, celesta stars, harp); the dream (Gmaj7 Dmaj7, a celesta melody); the sheaf stands
    up (Em7 A, a rising arpeggio); the others gather round (Bm7, circling) and bow (the celesta scale falling over G
    A7sus4, a harp glissando down) onto the glowing sheaf's chord, D major, on '下拜'; the brothers angrier (E minor,
    the motif on bassoon and trombone, a mock fanfare on '难道你还想做王')."""
    c.gain(-2.6)
    t_d = c.gap(c.find("我梦见"))
    t_up = c.at("我的那一捆站了起来")
    t_round = c.at("你们的麦捆")
    t_bow = c.at("下拜")
    t_ang = c.gap(c.find("哥哥们听了"))
    t_bow_pic = pic(c, "chime", "我梦见")                    # the sheaves bow (picture)
    t_land = t_bow_pic if t_bow_pic is not None and t_bow - 0.45 <= t_bow_pic <= t_ang - 0.1 else None
    a = c.seg(0, t_d, 2, "6/8", "D major", nominal=90, label="dream-night")
    b = c.seg(t_d, t_up, 2, "6/8", "D major", nominal=116, label="dream-field")
    u = c.seg(t_up, t_round, 1, "6/8", "D major", nominal=100, label="dream-stands")
    d = c.seg(t_round, t_bow, 2, "6/8", "D major", nominal=112, label="dream-bow")
    long_glow = t_ang - t_bow >= 0.8
    e = c.seg(t_bow, t_ang, 1, "2/4" if long_glow else "3/8", "D major", nominal=120 if long_glow else 130,
              label="dream-glow")
    g = c.seg(t_ang, c.dur, 3, "4/4", "E minor+", nominal=116, label="dream-angry")
    for sg in (a, b, u, d, e, g):
        sg.duck(1.5)
    a.prog("Dmaj7:3 | Bm7:3")
    b.prog("Gmaj7:3 | Dmaj7:3")
    u.prog("Em7:3/2 A:3/2")
    d.prog("Bm7:3 | G:3/2 A7sus4:3/2")
    e.prog(f"D:{e.n_q:g}")
    g.prog(" | ".join(JEALOUS_PROG) + " | C:2 B7:2")
    e.sync("'下拜': the glowing sheaf (D major)", 0, t_bow, kind="change")
    if t_land is not None:
        sg, q = seg_at(c, (d, e), t_land)
        sg.sync("the sheaves bow (the glow: glockenspiel, celesta)", q, t_land)
    elif t_bow_pic is not None:                           # the picture's bow far from the word: a glint there
        accent(c, (a, b, u, d, e, g), t_bow_pic, "the sheaves bow (a glint)", glock=(86, 98), celesta=(74, 86))
    else:
        e.sync("'下拜': the glow (glockenspiel, harp)", 0, t_bow)
    # one night Joseph had a dream: stars (celesta), a slow harp, soft high strings
    a.mel("celesta", "r:3/2 A6:3/2 | r:3/2 F#6:3/2", vel=36, role="arp")
    broken(a, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    a.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=34, bass_part="vc", bass_lo=38, bass_hi=50)
    a.expr(["celesta"], [(0, -12), (6, -12)])
    a.expr(["harp"], [(0, -10), (1.5, -11), (6, -11)])
    a.expr(["vla", "vln2", "vln1", "vc"], [(0, -14), (2, -17), (6, -17)])
    # 'I dreamed we were binding sheaves in the field': harp rolling in 6/8, a celesta melody
    b.mel("celesta", "F#6:3/2 E6:1/2 D6:1 | C#6:3/2 A5:3/2", vel=42)
    broken(b, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 50, vel=36, thin=True)
    b.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=34, bass_part="vc", bass_lo=38, bass_hi=50)
    b.duck(2.5, parts=["celesta", "harp"])
    b.expr(["celesta"], [(0, -12), (6, -12)])
    b.expr(["harp"], [(0, -11), (6, -11)])
    b.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (6, -17)])
    # 'my sheaf stood up': a rising arpeggio (celesta, pizzicato), a harp sweep up
    u.mel("celesta", "E5:1/2 G5:1/2 B5:1/2 C#6:1/2 E6:1/2 A6:1/2", vel=42)
    gliss_in(u, "harp", 1.5, 0.45, midi("A3"), midi("A5"), v0=30, v1=44, scale=ChordTones(u.chord_at(1.6)))
    u.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    u.duck(2.5, parts=["celesta", "harp"])
    u.expr(["celesta", "harp"], [(0, -12), (3, -11)])
    u.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (3, -16)])
    # 'your sheaves gathered round and bowed down to mine': circling (Bm7), then the bow
    d.mel("celesta", "F#6:1/2 D6:1/2 B5:1/2 D6:1/2 F#6:1/2 A6:1/2", vel=40)
    bow(d, 3.0, vel=44, q_end=None if t_land is None or t_land >= t_bow else d.q_of(c.t0 + t_land))
    d.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_part="vc", bass_lo=43, bass_hi=55)
    d.duck(2.5, parts=["celesta", "harp"])
    d.expr(["celesta", "harp"], [(0, -12), (6, -11)])
    d.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (6, -15)])
    # '下拜!': the glowing sheaf (its attack where the sheaves touch down on the picture)
    glow(e, 0, vel=52, land=None if t_land is None else seg_at(c, (d, e), t_land))
    strings(e, vel=42, lo=57, hi=76)
    e.expr(["celesta", "glock", "harp", "timp", "pz_cb"], [(0, -10), (e.n_q, -12)])
    e.expr(["ooh"], [(0, -16), (e.n_q, -18)])
    e.expr(STR, [(0, -14), (e.n_q, -16)])
    # the brothers were even angrier: the motif on bassoon and trombone, plucked basses; a mock fanfare
    jealous(g, 0, 0, vel=62)
    jealous(g, 4, 1, vel=60)
    g.mel("bsn", "G3:1/2:s G3:1/2:s C4:1:s B3:1/2:s A3:1/2:s B3:1:s", q=8, vel=58)
    g.mel("tbn", "E3:1/2:s r:1/2 G3:1/2:s r:1/2 r:1/2 E3:1/2:s B2:1:s", vel=50)
    g.mel("horn", "r:4 | r:4 | G3:1/2:s G3:1/2:s C4:1 B3:2", vel=48)
    g.mel("pz_cb", "E2:1:s r:1 B1:1:s r:1 | A1:1:s r:1 B1:1:s r:1 | C2:1:s r:1 B1:1:s r:1", vel=54, role="bass")
    g.pad(["trem_va", "trem_va"], 2, 52, 67, vel=34, bass_ref=(35, 47))
    g.add("hand", 0, 0.25, 77, 48, "perc", "h")
    g.sync("the brothers' motif enters (bassoon, pizzicato)", 0, t_ang)
    g.expr(["bsn", "tbn"], [(0, -12), (12, -12)])
    g.expr(["horn"], [(0, -14), (12, -15)])
    g.expr(["pz_cb", "hand"], [(0, -11), (12, -11)])
    g.expr(["trem_va"], [(0, -20), (12, -18)])
    # the picture: the dream bubble opens; the sheaf stands up and glows; the brothers stamp ('更生气了')
    segs = (a, b, u, d, e, g)
    t_bub = pic(c, "chime", "有一天晚上")
    if t_bub is not None:
        sg, q = accent(c, segs, t_bub, "the dream bubble opens", celesta=(79, 93), harp=(62, 74), vel=46)
        gliss_in(sg, "harp", q + 0.1, 0.5, midi("D4"), midi("D6"), v0=26, v1=38, scale=ChordTones(sg.chord_at(q + 1e-3)))
    t_rise = pic(c, "grow", "我梦见")
    if t_rise is not None:
        accent(c, segs, t_rise, "Joseph's sheaf stands up", glock=(81, 93), pluck=(64, 76), vel=46)
    t_shine = pic(c, "sparkle", "我梦见")
    if t_shine is not None:
        accent(c, segs, t_shine, "the sheaf glows", glock=(88, 100), vel=44)
    t_stamp = pic(c, "thud", "哥哥们听了")
    if t_stamp is not None:
        accent(c, segs, t_stamp, "the brothers stamp ('更生气了')", low=True, vel=50)
    for sg in segs:
        sg.expr(["glock", "pz_hi"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])


def pit(c):
    """Joseph walks to his brothers (theme b1-b2 in G, clarinet, walking pizzicato); they see him and plot (E minor,
    the jealousy motif, tremolo); C on '剥下约瑟的彩衣' (the coat motif falling: glockenspiel, celesta, a plucked
    chord); the dry pit (A minor, hollow: low basses, a high thin violin line); '哥哥！放我出去！' -- the sad motif on a
    solo oboe (E minor)."""
    c.gain(-2.2)
    t_see = c.gap(c.find("哥哥们远远看见"))
    t_strip = c.at("剥下约瑟的彩衣")
    t_pit = c.at("把他丢进")
    t_cry = c.gap(c.find("哥哥！放我出去"))
    a = c.seg(0, t_see, 2, "4/4", "G major", nominal=76, label="pit-walk")
    b = c.seg(t_see, t_strip, 3, "4/4", "E minor+", nominal=98, label="pit-plot")
    s = c.seg(t_strip, t_pit, 1, "2/4", "C major", nominal=80, label="pit-coat")
    p = c.seg(t_pit, t_cry, 2, "4/4", "A minor", nominal=96, label="pit-dry")
    e = c.seg(t_cry, c.dur, 1, "2/4", "E minor", nominal=52, label="pit-cry")
    for sg in (a, b, s, p, e):
        sg.duck(1.5)
    a.prog(tprog(" | ".join(JOSEPH_PROG[:2]), 5))
    b.prog(" | ".join(JEALOUS_PROG) + " | Em:2 B7:2")
    s.prog("C:2")
    p.prog("Am:4 | Em:2 B7:2@E-minor+")
    e.prog("Em:2")
    s.sync("'剥下约瑟的彩衣': C (the coat torn off)", 0, t_strip, kind="change")
    # father sent Joseph to see his brothers far away: the theme in G, walking pizzicato
    a.mel("clar", bars(JOSEPH, 0, 2), vel=56, transpose=5)
    walk(a, "pz_lo", 0, 8, 43, 62, vel=50)
    a.pad(["vla", "vln2"], 2, 55, 71, vel=36, bass_ref=(43, 55))
    a.duck(2.5, parts=["clar"])
    a.expr(["clar"], [(0, -13), (8, -13)])
    a.expr(["pz_lo"], [(0, -12), (8, -12)])
    a.expr(["vla", "vln2"], [(0, -18), (8, -17)])
    # the brothers saw him coming: the motif, sneaking pizzicato, tremolo growing; 'look, the dreamer!'
    jealous(b, 0, 0, vel=56)
    jealous(b, 4, 1, vel=54)
    b.mel("bsn", "E3:1/2:s G3:1/2:s B3:1:s D#3:1/2:s F#3:1/2:s A3:1:s", q=8, vel=54)
    b.mel("pz_cb", "E2:1:s r:1 B1:1:s r:1 | A1:1:s r:1 B1:1:s r:1 | E2:1:s r:1 B1:1:s r:1", vel=50, role="bass")
    b.pad(["trem_va", "trem_va"], 2, 52, 67, vel=36, bass_ref=(35, 47))
    b.expr(["bsn"], [(0, -12), (12, -12)])
    b.expr(["pz_cb"], [(0, -12), (12, -12)])
    b.expr(["trem_va"], [(0, -22), (8, -17), (12, -15)])
    # they pulled off his coat: it flies (a swish) and tumbles down (the coat motif falls, C major) onto the grass
    segs = (a, b, s, p, e)
    t_fly = pic(c, "whoosh", "他们剥下")
    t_down = pic(c, "cloth", "他们剥下")
    if t_fly is not None:
        sg, q = seg_at(c, segs, t_fly)
        pluck_chord(sg, q, vel=56, lo=59, hi=71)
        gliss_in(sg, "harp", q + 0.05, 0.4, midi("B3"), midi("B5"), up=False, v0=40, v1=30,
                 scale=ChordTones(sg.chord_at(q + 1e-3)))
        sg.sync("the coat flies (a swish)", q, t_fly)
    inside = t_down is not None and t_strip + 0.3 <= t_down <= t_pit - 0.1
    q_dn = s.q_of(c.t0 + t_down) if inside else 1.5
    step = q_dn / 3
    for k, (g_, c_) in enumerate((("G6", "G5"), ("E6", "E5"), ("C6", "C5"), ("G5", "G4"))):
        q = k * step
        dq = step if k < 3 else s.n_q - q
        s.add("glock", q, dq, g_, 50 - 2 * k, "melody", voice="glock.0")
        s.add("celesta", q, dq, c_, 42 - 2 * k, "melody", voice="celesta.0")
    pluck_chord(s, 0, vel=50, lo=63, hi=75)
    if inside:
        thump(s, q_dn, vel=48)
        s.sync("the coat lands on the grass", q_dn, t_down)
    elif t_down is not None:
        accent(c, segs, t_down, "the coat lands on the grass", low=True, vel=46)
    s.pad(["trem_va", "trem_va"], 2, 52, 67, vel=36, bass_ref=(36, 48))
    s.expr(["glock", "celesta"], [(0, -10), (2, -12)])
    s.expr(["trem_va"], [(0, -15), (2, -17)])
    t_glint = pic(c, "sparkle", "哥哥们远远看见")               # the bright coat far away on the hill path
    if t_glint is not None:
        accent(c, segs, t_glint, "the coat glints far away", glock=(86, 98), vel=42)
    # ...and threw him into a dry, empty pit: hollow (low basses, a thin high violin line, a lone harp note)
    p.mel("cb", "A1:4 | E1:2 B1:2", vel=40, role="bass")
    p.pad(["trem_hi", "trem_hi"], 2, 64, 81, vel=34, bass_ref=(33, 45))
    p.add("harp", 2, 2, "E3", 36, "arp")
    p.add("harp", 6, 2, "D#3", 34, "arp")
    p.mel("oboe", "r:4 | G4:1/2 B4:1/2 E5:1 D#5:2", vel=50)
    p.expr(["oboe"], [(4, -16), (6, -16), (8, -19)])
    p.expr(["cb"], [(0, -14), (8, -15)])
    p.expr(["trem_hi"], [(0, -19), (8, -20)])
    p.expr(["harp"], [(0, -11), (8, -11)])
    t_in = pic(c, "thud", "他们剥下")                        # Joseph lands at the bottom
    if t_in is not None:
        accent(c, segs, t_in, "Joseph lands in the pit", low=True, vel=48)
    t_dust = pic(c, "thud", "他们剥下", 1)                    # he scuffs the dry floor
    if t_dust is not None:
        sg, q = accent(c, segs, t_dust, "he scuffs the dry floor (dust)")
        drum(sg, q, 77, 44)
        sg.add("pz_lo", q, _dq(sg, q, 0.25), top(sg, q, 45, 57, 0), 46, "bass", "h")
    for sg in segs:
        sg.expr(["glock"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["pz_hi", "timp", "pz_cb"], [(0, -10), (sg.n_q, -10)])
        sg.expr(["okit", "hand"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["pz_lo"], [(0, -12), (sg.n_q, -12)])
    # 'brothers! let me out!': the sad motif on a solo oboe
    e.pad(["vla", "vln2"], 2, 48, 64, vel=34, bass_part="vc", bass_lo=40, bass_hi=52)
    e.expr(["vla", "vln2", "vc"], [(0, -14), (2, -16)])


def sold(c):
    """The caravan (A harmonic minor: the camels' plod on a frame drum, plucked basses, camel bells, an oboe with the
    F-G# augmented second); the rope thrown down and Joseph pulled up (Am E, a harp sweep); F on '二十块银子' (a plucked
    chord and the frame drum), then the silver counted out two by two on the picture (a glockenspiel/celesta clink per
    coin, rising) and a glint for the '20' badge; the caravan goes far away (A minor, the plod fading, the sad motif x
    on the oboe)."""
    c.gain(-2.4)
    t_s = c.gap(c.find("哥哥们把约瑟拉上来"))
    t_coin = c.at("二十块银子")
    t_far = c.gap(c.find("约瑟被带到了"))
    a = c.seg(0, t_s, 2, "4/4", "A harmonic", nominal=78, label="sold-caravan")
    b = c.seg(t_s, t_coin, 1, "4/4", "A harmonic", nominal=90, label="sold-pull")
    k = c.seg(t_coin, t_far, 1, "4/4", "A harmonic", nominal=98, label="sold-silver")
    f = c.seg(t_far, c.dur, 1, "4/4", "A harmonic", nominal=64, rit=0.2, label="sold-away")
    for sg in (a, b, k, f):
        sg.duck(1.5)
    a.prog("Am:4 | Dm:2 E:2")
    b.prog("Am:2 E:2")
    k.prog("F:2 E:2")
    f.prog("Am:4")
    k.sync("'二十块银子': F (the price)", 0, t_coin, kind="change")
    k.sync("'二十块银子': the price (plucked chord, frame drum)", 0, t_coin)
    # a line of camels came along, traders going to Egypt: the plod, bells, an oboe
    camel(a, 0, 8, vel=58)
    a.sync("the caravan's first step (frame drum)", 0, 0.0)
    a.mel("oboe", "E5:1 F5:1/2 G#5:1/2 A5:1 G#5:1/2 F5:1/2 | E5:1 D5:1/2 C5:1/2 B4:1 G#4:1", vel=56)
    a.pad(["vla", "vln2"], 2, 52, 69, vel=34, bass_ref=(33, 45))
    a.duck(3.5, parts=["oboe"])
    a.expr(["oboe"], [(0, -15), (8, -15)])
    a.expr(["pz_cb", "hand"], [(0, -13), (8, -13)])
    a.expr(["vla", "vln2"], [(0, -19), (8, -18)])
    # the brothers pulled Joseph up...
    camel(b, 0, 4, vel=54, bells=False)
    b.pad(["vla", "vln2"], 2, 52, 69, vel=34, bass_ref=(33, 45))
    b.expr(["pz_cb", "hand"], [(0, -13), (4, -13)])
    b.expr(["vla", "vln2"], [(0, -18), (4, -18)])
    # ...and sold him for twenty pieces of silver: F, the clinks
    segs = (a, b, k, f)
    coins = [pic(c, "coins", "哥哥们把约瑟拉上来", i_) for i_ in range(5)]
    have = coins[0] is not None
    coins = [t for t in coins if t is not None] if have else [t_coin + 0.15 + 0.25 * i_ for i_ in range(5)]
    for i_, t in enumerate(coins):                        # the silver counted out, two by two up to twenty
        sg, q = seg_at(c, segs, t)
        clink(sg, q, i_, vel=56 + i_)
        if have:
            sg.sync(f"coin {i_ + 1} (counted out)", q, t)
    t_20 = pic(c, "pop", "哥哥们把约瑟拉上来")                  # the '20' badge pops
    if t_20 is not None:
        accent(c, segs, t_20, "the '20' badge", glock=(88, 100), pluck=(64, 76), vel=50)
    t_rope = pic(c, "whoosh", "哥哥们把约瑟拉上来")              # the rope thrown down; Joseph pulled up
    if t_rope is not None:
        sg, q = accent(c, segs, t_rope, "the rope is thrown down", pluck=(57, 69), vel=48)
        gliss_in(sg, "harp", q + 0.05, 0.6, midi("A3"), midi("A5"), v0=28, v1=40, scale=ChordTones(sg.chord_at(q + 1e-3)))
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -10), (sg.n_q, -11)])
        sg.expr(["pz_hi", "harp"], [(0, -12), (sg.n_q, -12)])
    pluck_chord(k, 0, vel=52, lo=57, hi=69)
    k.add("pz_cb", 0, _dq(k, 0, 1.0), "F2", 54, "bass", "s")
    drum(k, 0, 45, 50)
    drum(k, 2, 45, 44)
    k.add("pz_cb", 2, _dq(k, 2, 1.0), "E2", 48, "bass", "s")
    k.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_ref=(40, 52))
    k.expr(["glock", "celesta"], [(0, -10), (4, -11)])
    k.expr(["pz_cb", "pz_hi", "hand"], [(0, -12), (4, -12)])
    k.expr(["vla", "vln2", "vln1"], [(0, -16), (4, -16)])
    # Joseph was taken far, far away to Egypt: the plod fades, the sad motif on the oboe
    camel(f, 0, 4, vel=50, bells=True)
    f.mel("oboe", "C5:1 E5:1 A5:2", vel=50)
    f.pad(["vla", "vln2"], 2, 52, 69, vel=34, bass_ref=(33, 45))
    f.duck(2.5, parts=["oboe"])
    f.expr(["oboe"], [(0, -14), (4, -17)])
    f.expr(["pz_cb", "hand"], [(0, -14), (4, -22)])
    f.expr(["vla", "vln2"], [(0, -18), (4, -20)])


def jacob(c):
    """The torn coat (D minor 3/4: the coat motif on the celesta -- D E F rising to the moment the coat is torn on the
    picture, where it breaks off; a dull pluck, low strings); Judah shows Jacob the coat, Jacob takes it and sinks
    down (soft harp accents); Jacob's grief: the cello lament (Dm A7); the deceptive B-flat on '哭了很久很久' (sobbing
    cellos, choir 'ooh')."""
    c.gain(-3.0)
    t_j = c.gap(c.find("雅各以为"))
    t_cry = c.at("哭了很久很久")
    a = c.seg(0, t_j, 2, "3/4", "D minor+", nominal=66, label="jacob-coat")
    b = c.seg(t_j, t_cry, 1, "4/4", "D minor+", nominal=64, label="jacob-lament")
    s = c.seg(t_cry, c.dur, 1, "2/4", "D minor+", nominal=59, label="jacob-weeps")
    for sg in (a, b, s):
        sg.duck(1.5)
    a.prog("Dm:3 | Gm:3/2 A:3/2")
    b.prog("Dm:2 A7:2")
    s.prog("Bb:2")
    s.sync("'哭了很久很久': B-flat (Jacob weeps)", 0, t_cry, kind="change")
    # the brothers brought the torn, dirty coat home: the coat motif, broken off where the coat is torn (picture)
    segs = (a, b, s)
    t_tear = pic(c, "cloth", "哥哥们把彩衣")
    q_t = a.q_of(c.t0 + t_tear) if t_tear is not None and 0.9 <= t_tear <= t_j - 0.3 else 3.0
    q_t = round(min(q_t, 4.4) * 48) / 48
    for k, nm in enumerate(["D5", "E5", "F5"]):           # D E F rising towards the tear ...
        a.add("celesta", k * q_t / 3, q_t / 3, nm, 40, "melody", voice="celesta.0")
    a.add("celesta", q_t, _dq(a, q_t, 1.5), "G5" if q_t >= 3.0 else "A5", 40, "melody", voice="celesta.0")
    if t_tear is not None:                                # ... and it breaks: a dull pluck, a puff of dust
        sg, q = accent(c, segs, t_tear, "the coat is torn (a puff of dust)", low=True, vel=44)
        sg.add("pz_lo", q, _dq(sg, q, 0.25), top(sg, q, 50, 62, 0), 50, "bass", "h")
    t_show = pic(c, "cloth", "哥哥们把彩衣", 1)               # Judah holds the coat up to Jacob
    if t_show is not None:
        accent(c, segs, t_show, "Judah shows Jacob the coat", harp=(55, 67), pluck=(57, 69), vel=44)
    t_take = pic(c, "cloth", "雅各以为")                     # Jacob takes the coat and sinks down
    if t_take is not None:
        accent(c, segs, t_take, "Jacob takes the coat and sinks down", harp=(50, 62), low=True, vel=42)
    for sg in segs:
        sg.expr(["pz_lo", "pz_hi", "harp"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])
        sg.expr("okit", [(0, -14), (sg.n_q, -14)])
    a.pad(["vla", "vln2"], 2, 50, 65, vel=36, bass_part="vc", bass_lo=38, bass_hi=50)
    a.expr(["celesta"], [(0, -12), (6, -13)])
    a.expr(["vla", "vln2", "vc"], [(0, -20), (2, -16), (6, -16)])
    # Jacob thought a wild animal had eaten Joseph: the cello lament
    b.mel("vc", "A3:1 G3:1/2 F3:1/2 E3:1 C#3:1", vel=56)
    b.pad(["vla", "vln2"], 2, 53, 69, vel=36, bass_ref=(33, 45))
    b.mel("cb", "D2:2 A1:2", vel=38, role="bass")
    b.duck(2.0, parts=["vc"])
    b.expr(["vc"], [(0, -12), (4, -11)])
    b.expr(["vla", "vln2", "cb"], [(0, -17), (4, -16)])
    # ...and he wept for a long, long time: B-flat, the cellos sobbing, choir 'ooh'
    s.mel("vc", "D4:1 C4:1/2 Bb3:1/2", vel=56)
    s.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=38, bass_ref=(34, 46))
    s.pad("ooh", 3, 55, 70, vel=36, bass_ref=(34, 46))
    s.add("cb", 0, 2, "Bb1", 38, "bass")
    s.expr(["vc"], [(0, -12), (2, -13)])
    s.expr(["vla", "vln2", "vln1", "cb"], [(0, -15), (2, -16)])
    s.expr(["ooh"], [(0, -19), (2, -20)])


def egypt(c):
    """Egypt (D hijaz: harp, an oboe with the Eb-F# step, a soft frame drum); B-flat on '上帝和约瑟同在' (God with
    Joseph: choir 'ooh', strings, horn); Joseph's theme b1-b3 in B-flat on the oboe, walking pizzicato (the trusted
    servant); D minor on '被人冤枉' (the falling bass D C Bb A: prison); B-flat again on '上帝还是和约瑟同在'."""
    c.gain(-2.4)
    t_god = c.at("上帝和约瑟同在")
    t_work = c.gap(c.find("约瑟做事很认真"))
    t_wrong = c.at("被人冤枉")
    t_still = c.at("上帝还是和约瑟同在")
    a = c.seg(0, t_god, 1, "4/4", "D hijaz", nominal=64, label="egypt-slave")
    g = c.seg(t_god, t_work, 1, "4/4", "Bb major", nominal=100, label="egypt-god")
    w = c.seg(t_work, t_wrong, 3, "4/4", "Bb major", nominal=96, label="egypt-servant")
    p = c.seg(t_wrong, t_still, 2, "4/4", "D minor+", nominal=104, label="egypt-wronged")
    s = c.seg(t_still, c.dur, 1, "4/4", "Bb major", nominal=85, label="egypt-god-still")
    for sg in (a, g, w, p, s):
        sg.duck(1.5)
    a.prog("D:2 Eb:2")
    g.prog("Bb:4")
    w.prog(tprog(" | ".join(JOSEPH_PROG[:3]), -4, flats=True))
    p.prog("Dm:2 Dm/C:2 | Gm/Bb:2 A:2")
    s.prog("Bb:4")
    g.sync("'上帝和约瑟同在': B-flat (God with Joseph)", 0, t_god, kind="change")
    p.sync("'被人冤枉': D minor (wrongly accused)", 0, t_wrong, kind="change")
    s.sync("'上帝还是和约瑟同在': B-flat again", 0, t_still, kind="change")
    # in Egypt Joseph became a slave: the oboe in D hijaz, harp fifths, a soft frame drum
    a.mel("oboe", "D5:1/2 Eb5:1/2 F#5:1 G5:1 Bb5:1", vel=54)
    for q in (0, 1, 2, 3):
        ch = a.chord_at(q + 1e-3)
        a.add("harp", q, _dq(a, q, 1.0), ch.bass_note(38, 50), 40, "arp")
        a.add("harp", q + 0.5, _dq(a, q + 0.5, 0.5), ch.tones(50, 62)[-1 if q % 2 else 1], 34, "arp")
    for q, key, v in [(0, 45, 48), (1.5, 60, 36), (2, 45, 44), (3, 60, 36), (3.5, 61, 30)]:
        drum(a, q, key, v)
    a.pad(["vla", "vln2"], 2, 50, 67, vel=34, bass_ref=(38, 50))
    a.add("cb", 0, 2, "D2", 36, "bass")
    a.add("cb", 2, 2, "Eb2", 36, "bass")
    a.duck(3.5, parts=["oboe"])
    a.expr(["oboe"], [(0, -16), (4, -16)])
    a.expr(["harp"], [(0, -12), (4, -12)])
    a.expr("hand", [(0, -13), (4, -13)])
    a.expr(["vla", "vln2", "cb"], [(0, -19), (4, -18)])
    # 'but God was with Joseph': warm sustained B-flat (choir 'ooh', strings, a soft horn)
    g.pad("ooh", 3, 55, 72, vel=38, bass_ref=(34, 46))
    strings(g, vel=40, lo=55, hi=74, bass=(46, 58), cb=(34, 46))
    g.add("horn", 0, 4, "F3", 40, "pad", voice="horn.0")
    g.add("horn", 0, 4, "Bb3", 40, "pad", voice="horn.1")
    g.add("harp", 0, 4, "D5", 34, "arp")
    g.duck(2.5)
    g.expr(["ooh"], [(0, -20), (1, -17), (4, -18)])
    g.expr(STR, [(0, -17), (1, -14), (4, -15)])
    g.expr(["horn", "harp"], [(0, -16), (4, -16)])
    # Joseph worked hard; his master trusted him with the whole house: the theme in B-flat (oboe), walking pizzicato
    w.mel("clar", bars(JOSEPH, 0, 3), vel=54, transpose=-4)
    walk(w, "pz_lo", 0, 12, 39, 58, vel=48)
    broken(w, "harp", 0, 12, (0, 2, 4, 2), 46, 58, vel=32, thin=True)
    w.pad(["vla", "vln2"], 2, 55, 70, vel=34, bass_ref=(39, 51))
    for q in range(0, 12, 2):
        drum(w, q, 45, 36)
    w.duck(3.5, parts=["clar", "harp"])
    w.expr(["clar"], [(0, -14), (12, -14)])
    w.expr(["pz_lo", "harp"], [(0, -13), (12, -13)])
    w.expr("hand", [(0, -14), (12, -14)])
    w.expr(["vla", "vln2"], [(0, -18), (12, -18)])
    # later he was wrongly accused and put in prison: D minor, the falling bass, quiet
    p.mel("cb", "D2:2 C2:2 | Bb1:2 A1:2", vel=40, role="bass")
    p.pad(["vla", "vln2", "vln1"], 3, 53, 70, vel=36, bass_ref=(33, 45))
    p.mel("clar", "F4:2 E4:2 | D4:2 C#4:2", vel=46)
    segs = (a, g, w, p, s)
    door = pic(c, "thud", "后来，约瑟被人冤枉")             # the prison gate clangs shut (on the picture)
    if door is not None:
        accent(c, segs, door, "the prison gate clangs shut", low=True, vel=46)
    t_drop = pic(c, "coins", "后来，约瑟被人冤枉")           # the keys fall from his hands: clink
    if t_drop is not None:
        accent(c, segs, t_drop, "the keys fall (clink)", glock=(86, 98), celesta=(74, 86), vel=46)
    p.expr(["cb"], [(0, -14), (8, -15)])
    p.expr(["vla", "vln2", "vln1"], [(0, -16), (8, -18)])
    p.expr(["clar"], [(0, -15), (8, -16)])
    t_sack = pic(c, "thud", "在埃及")                       # he drops the grain sack on the pile (咚)
    if t_sack is not None:
        accent(c, segs, t_sack, "the grain sack drops on the pile", low=True, vel=46)
    for kk in range(2):                                   # the master gives him the keys; he holds them up (jingle)
        t = pic(c, "coins", "约瑟做事很认真", kk)
        if t is not None:
            sg, q = seg_at(c, segs, t)
            clink(sg, q, kk, vel=54)
            sg.sync(f"the keys {'(given)' if kk == 0 else '(held up)'}", q, t)
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -12), (sg.n_q, -12)])
        sg.expr(["okit", "hand"], [(0, -13), (sg.n_q, -13)])
    # 'but even in prison God was still with Joseph': B-flat again
    s.pad("ooh", 3, 55, 72, vel=38, bass_ref=(34, 46))
    strings(s, vel=40, lo=55, hi=74, bass=(46, 58), cb=(34, 46))
    s.add("horn", 0, 4, "F3", 40, "pad", voice="horn.0")
    s.add("horn", 0, 4, "Bb3", 40, "pad", voice="horn.1")
    s.add("harp", 0, 4, "D5", 34, "arp")
    s.duck(2.5)
    s.expr(["ooh"], [(0, -19), (1, -17), (3, -18), (4, -23)])
    s.expr(STR, [(0, -16), (1, -14), (3, -16), (4, -21)])
    s.expr(["horn", "harp"], [(0, -16), (3, -17), (4, -20)])


def prison(c):
    """Prison (G minor, 3/4, quiet low strings); the strange dreams (Ebmaj7: celesta and harp); Joseph explains them:
    the theme b1-b2 in B-flat on the clarinet, ending on F7; B-flat on '是上帝' (choir, strings, harp rolled)."""
    c.gain(-3.0)
    t_solve = c.at("约瑟帮他们解梦")
    t_god = c.at("是上帝")
    a = c.seg(0, t_solve, 2, "3/4", "G minor", nominal=80, label="prison-dreams")
    b = c.seg(t_solve, t_god, 2, "4/4", "Bb major", nominal=82, label="prison-explain")
    s = c.seg(t_god, c.dur, 1, "2/4", "Bb major", nominal=116, label="prison-god")
    for sg in (a, b, s):
        sg.duck(1.5)
    a.prog("Gm:3 | Ebmaj7:3")
    b.prog("Bb:4 | Eb:2 F7:2")
    s.prog("Bb:2")
    s.sync("'是上帝': B-flat (God)", 0, t_god, kind="change")
    # in prison two men had strange dreams: low strings, then a dream shimmer (celesta, harp)
    a.pad(["vla", "vln2"], 2, 50, 67, vel=36, bass_part="vc", bass_lo=43, bass_hi=55)
    a.mel("celesta", "r:3 | D6:1 Bb5:1 G5:1", vel=38, role="arp")
    broken(a, "harp", 3, 6, (0, 2, 4, 6, 4, 2), 39, 51, vel=32, thin=True)
    a.expr(["vla", "vln2", "vc"], [(0, -15), (2, -17), (6, -17)])
    a.expr(["celesta", "harp"], [(0, -12), (6, -12)])
    # Joseph told them what they meant, and it all came true: the theme in B-flat on the clarinet
    b.mel("clar", bars(JOSEPH, 0, 2), vel=54, transpose=-4)
    broken(b, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 46, 58, vel=34, thin=True)
    b.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=34, bass_part="vc", bass_lo=41, bass_hi=53)
    b.duck(3.5, parts=["clar", "harp"])
    b.expr(["clar"], [(0, -13), (4, -14), (5, -19), (8, -19)])
    b.expr(["harp"], [(0, -11), (4, -12), (5, -15), (8, -15)])
    b.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (8, -17)])
    # 'it is not I who can explain dreams -- it is God': B-flat, choir, a harp rolled up
    s.pad("ooh", 3, 55, 72, vel=38, bass_ref=(34, 46))
    strings(s, vel=40, lo=55, hi=74, bass=(46, 58), cb=(34, 46))
    t_light = pic(c, "chime", "能解梦的", lo=t_god - 0.1, hi=c.dur - 0.3)    # he points up: the light glows
    q_l = qpos(s, c, t_light) if t_light is not None else 0.0
    harp_roll(s, q_l, ["Bb2", "F3", "Bb3", "D4", "F4", "Bb4"], vel=42)
    for kk, what in enumerate(("the cupbearer's dream bubble", "the baker's dream bubble")):
        t = pic(c, "pop", "在监牢里", kk)
        if t is not None:
            accent(c, (a, b, s), t, what, celesta=(76 + 3 * kk, 88 + 3 * kk), harp=(64, 76), vel=48)
    t_sun = pic(c, "sparkle", "在监牢里")                    # it all came true: the sunny bubble
    if t_sun is not None:
        accent(c, (a, b, s), t_sun, "it all came true (the sunny bubble)", glock=(86, 98), vel=44)
    for sg in (a, b, s):
        sg.expr(["glock"], [(0, -11), (sg.n_q, -11)])
    s.expr(["ooh"], [(0, -20), (2, -20)])
    s.expr(STR, [(0, -17), (2, -17)])
    s.expr(["harp"], [(0, -13), (2, -13)])


def pharaoh(c):
    """Pharaoh's court (D minor, stately: horns, harp, a slow frame drum; Eb and A at its sides), a strange dream
    (celesta, a glint as the bubble blooms); seven fat cows (an F major waltz: tuba oom, bassoon pah-pah); seven thin
    cows (a thin staccato violin note for each as it climbs out of the river, D minor); A on '吃掉了' and the gulps on
    the picture (plucked basses, bassoon, woodblock; the first with tuba, timpani and bass drum); Pharaoh wakes with a
    start; three wise men shrug (bassoon, Gm A7); the cupbearer's idea (a glint); D on '有人想起了约瑟' (motif x on the
    oboe); God's message (Em7 A7); D on '七年大丰收' (harp up the golden fields, glockenspiel); D minor bare fifths on
    '七年大饥荒'; 'store the grain' (Bb A, steady pizzicato, the sacks thumping into the granary)."""
    c.gain(-2.2)
    t_cows = c.at("七头肥肥的牛")
    t_thin = c.at("被七头瘦瘦的牛")
    t_gulp = c.at("吃掉了")
    t_none = c.gap(c.find("没有人能解"))
    t_jo = c.at("有人想起了约瑟")
    t_say = c.gap(c.find("上帝告诉你"))
    t_plenty = c.at("七年大丰收")
    t_famine = c.at("七年大饥荒")
    t_store = c.at("要趁丰收的时候")
    p = c.seg(0, t_cows, 2, "4/4", "D minor", nominal=88, label="pharaoh-court")
    f = c.seg(t_cows, t_thin, 1, "3/4", "F major", nominal=112, label="pharaoh-fat-cows")
    th = c.seg(t_thin, t_gulp, 1, "3/4", "D minor", nominal=106, label="pharaoh-thin-cows")
    g = c.seg(t_gulp, t_none, 1, "2/4", "D minor+", nominal=102, label="pharaoh-gulp")
    n = c.seg(t_none, t_jo, 1, "4/4", "D minor+", nominal=83, label="pharaoh-shrug")
    j = c.seg(t_jo, t_say, 1, "4/4", "D major", nominal=112, label="pharaoh-joseph")
    y = c.seg(t_say, t_plenty, 1, "4/4", "D major", nominal=110, label="pharaoh-god-says")
    pl = c.seg(t_plenty, t_famine, 1, "4/4", "D major", nominal=112, label="pharaoh-plenty")
    fa = c.seg(t_famine, t_store, 1, "2/4", "D minor", nominal=84, label="pharaoh-famine")
    st = c.seg(t_store, c.dur, 1, "4/4", "D minor+", nominal=72, label="pharaoh-store")
    segs = (p, f, th, g, n, j, y, pl, fa, st)
    for sg in segs:
        sg.duck(1.5)
    p.prog("Dm:2 Eb:2@D-phrygian | Gm:2 A:2@D-harmonic")
    f.prog("F:3")
    th.prog("Dm:3")
    g.prog("A:2@D-harmonic")
    n.prog("Gm:2 A7:2")
    j.prog("D:4")
    y.prog("Em7:2 A7:2")
    pl.prog("D:2 G:2")
    fa.prog("Dm:2")
    st.prog("Bb:2 A:2")
    f.sync("'七头肥肥的牛': the fat cows' waltz (F)", 0, t_cows, kind="change")
    g.sync("'吃掉了': A (the thin cows gulp them down)", 0, t_gulp, kind="change")
    j.sync("'有人想起了约瑟': D major (motif x)", 0, t_jo, kind="change")
    pl.sync("'七年大丰收': plenty (D major)", 0, t_plenty, kind="change")
    fa.sync("'七年大饥荒': famine (D minor, bare)", 0, t_famine, kind="change")
    # two years later Pharaoh, king of Egypt, had a strange dream: the court (horns, harp, frame drum), celesta
    p.pad(["horn", "horn", "horn"], 3, 50, 65, vel=44, bass_ref=(38, 50))
    p.mel("cb", "D2:2 Eb2:2 | G1:2 A1:2", vel=40, role="bass")
    p.mel("vc", "D3:2 Eb3:2 | G2:2 A2:2", vel=40, role="bass")
    for q in (0, 2, 4, 6):
        drum(p, q, 45, 46 if q % 4 == 0 else 40)
        ch = p.chord_at(q + 1e-3)
        p.add("harp", q, _dq(p, q, 2), ch.bass_note(38, 50), 40, "arp")
        p.add("harp", q + 0.05, _dq(p, q + 0.05, 1.95), ch.tones(55, 67)[0], 36, "arp")
    p.mel("celesta", "r:4 | G6:1 D6:1 E6:1 C#6:1", vel=36, role="arp")
    t_bloom = pic(c, "chime", None)                         # the dream bubble blooms (picture)
    if t_bloom is not None:
        accent(c, segs, t_bloom, "the dream bubble blooms", glock=(86, 98), vel=42)
    p.expr(["horn"], [(0, -16), (8, -17)])
    p.expr(["cb", "vc"], [(0, -16), (8, -16)])
    p.expr(["harp", "celesta", "glock"], [(0, -11), (8, -11)])
    p.expr("hand", [(0, -12), (8, -12)])
    # seven fat cows: the plump waltz (tuba oom, bassoon pah-pah)
    f.add("tuba", 0, 1, "F1", 58, "bass", "s")
    for q in (1, 2):
        f.add("bsn", q, 0.5, "A2", 50, "harmony", "s", voice="bsn.0")
        f.add("bsn", q, 0.5, "C3", 50, "harmony", "s", voice="bsn.1")
    f.mel("clar", "C4:1 F4:1/2 A4:1/2 C5:1", vel=48)
    f.pad(["vla", "vln2"], 2, 53, 69, vel=32, bass_ref=(29, 41))
    f.expr(["tuba", "bsn"], [(0, -12), (3, -13)])
    f.expr(["clar"], [(0, -16), (3, -16)])
    f.expr(["vla", "vln2"], [(0, -19), (3, -19)])
    # ...were eaten by seven thin cows: a thin staccato violin note for each as it climbs out of the river
    thin = picture(c, "splash_small", t_thin - 0.3, t_gulp - 0.05) or []
    if len(thin) >= 4:
        lad = ["D5", "F5", "A5", "D6", "F6", "A6", "D7"]
        for k, t in enumerate(thin[:7]):
            q = qpos(th, c, t)
            th.add("vln_mel", q, 0.25, lad[k], 50 + k, "melody", "s")
    else:
        th.mel("vln_mel", "A5:1/2:s F5:1/2:s D5:1/2:s F5:1/2:s A5:1/2:s D6:1/2:s", vel=52)
    th.mel("pz_hi", "D5:1:s A4:1:s F4:1:s", vel=44, role="arp")
    th.pad(["trem_hi", "trem_hi"], 2, 69, 86, vel=34, bass_ref=(38, 50))
    th.expr(["trem_hi"], [(0, -17), (3, -18)])
    th.expr(["vln_mel"], [(0, -12), (3, -12)])
    th.expr(["pz_hi"], [(0, -11), (3, -11)])
    # 吃掉了! gulp-gulp-gulp (on the picture; without it, on the word): plucked basses, bassoon, a woodblock
    gulps = [pic(c, "gulp", None, k) for k in range(4)]
    gulps = [t for t in gulps if t is not None] or [t_gulp + 0.05 + 0.2 * k for k in range(4)]
    low = ["E3", "C#3", "A2", "E2"]
    for k, t in enumerate(gulps[:4]):
        sg, q = seg_at(c, segs, t)
        ch = sg.chord_at(q + 1e-3)
        sg.add("pz_cb", q, _dq(sg, q, 0.25), ch.bass_note(33, 45), (62, 54, 50, 44)[k], "bass", "h")
        nm = low[k] if midi(low[k]) % 12 in ch.pcset else name_of(top(sg, q, 40, 52, 0))
        sg.add("bsn", q, _dq(sg, q, 0.25), nm, (56, 50, 47, 40)[k], "harmony", "s")
        drum(sg, q, 77, (54, 48, 45, 38)[k])          # each gulp a little smaller
        if k == 0:
            sg.add("tuba", q, _dq(sg, q, 0.5), ch.bass_note(29, 41), 58, "bass", "h")
            sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(ch, midi("A2")), 54, "timp", "h")
            sg.add("okit", q, 1, 36, 48, "perc", "h")
        sg.sync(f"gulp {k + 1}", q, t)
    g.pad(["vla", "vln2"], 2, 52, 69, vel=32, bass_ref=(33, 45))
    for sg_ in (th, g):
        sg_.expr(["tuba", "pz_cb", "timp", "bsn"], [(0, -10), (sg_.n_q, -11)])
        sg_.expr(["okit", "hand"], [(0, -12), (sg_.n_q, -12)])
    g.expr(["vla", "vln2"], [(0, -18), (2, -18)])
    # Pharaoh wakes with a start; nobody could explain the dream: three wise men shrug, one after another
    wake = picture(c, "cloth", t_gulp + 0.3, t_none + 0.4) or []
    if wake:                                              # the last rustle before the throne hall: he sits up
        sg, q = seg_at(c, (g, n), wake[-1])
        pluck_chord(sg, q, vel=54, lo=55, hi=67)
        sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(sg.chord_at(q + 1e-3), midi("D3")), 46, "timp", "h")
    cand = [t for t in (picture(c, "cloth", c.ls(c.find("没有人能解")) - 0.3) or []) if t <= c.dur - 0.02][:3]
    shrugs = cand if len(cand) == 3 else [t_none + 0.4, t_none + 0.7, t_none + 1.0]
    for k, t in enumerate(shrugs):                        # each shrug a little higher: 'hm?'
        sg, q = seg_at(c, segs, t)
        sg.add("bsn", q, _dq(sg, q, 0.25), top(sg, q, 50, 60, k), 60 if k == 0 else 52, "harmony", "s")
        sg.add("pz_lo", q, _dq(sg, q, 0.25), top(sg, q, 43, 55, 0), 58 if k == 0 else 48, "bass", "h")
        if k == 0:
            pluck_chord(sg, q, vel=54, lo=55, hi=67)
            if cand:
                sg.sync("the first wise man shrugs", q, t)
    n.mel("bsn", "r:3 E3:1/2:s C#3:1/2:s", vel=50)
    n.pad(["vla", "vln2"], 2, 52, 69, vel=32, bass_ref=(31, 43))
    n.mel("cb", "G1:2 A1:2", vel=36, role="bass")
    t_idea = pic(c, "sparkle", "没有人能解")                  # the cupbearer's idea (a gold star)
    if t_idea is not None:
        accent(c, segs, t_idea, "the cupbearer's idea (a gold star)", glock=(85, 97), vel=46)
    n.expr(["bsn", "pz_lo"], [(0, -12), (4, -12)])
    n.expr(["vla", "vln2", "cb"], [(0, -18), (3, -17), (4, -16)])
    for sg_ in (g, n, j):
        sg_.expr(["glock"], [(0, -11), (sg_.n_q, -11)])
        sg_.expr(["pz_hi", "timp"], [(0, -12), (sg_.n_q, -12)])
    # then someone remembered Joseph: motif x on the oboe, harp
    j.mel("oboe", "F#4:1 A4:1 D5:2", vel=54)
    broken(j, "harp", 1, 4, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    strings(j, vel=38, lo=54, hi=71)
    j.duck(2.5, parts=["oboe", "harp"])
    j.expr(["oboe"], [(0, -18), (1, -14), (3, -14), (4, -16)])
    j.expr(["harp"], [(0, -16), (1, -11), (3, -11), (4, -13)])
    j.expr(STR, [(0, -19), (1, -16), (3, -16), (4, -17)])
    # 'God is telling you': soft pads
    y.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    y.pad("ooh", 3, 55, 70, vel=34, bass_ref=(40, 52))
    y.duck(2.0)
    y.expr(["vla", "vln2", "vln1", "vc"], [(0, -15), (4, -17)])
    y.expr(["ooh"], [(0, -21), (4, -20)])
    # seven years of plenty: bright -- a harp sweep up the golden fields as they pop up, the glockenspiel's glint
    fields = picture(c, "pop", t_plenty - 0.1, t_famine - 0.2) or []
    q0f, q1f = (qpos(pl, c, fields[1] if len(fields) > 2 else fields[0]), qpos(pl, c, fields[-1])) if fields else (0.05, 0.6)
    gliss_in(pl, "harp", q0f, max(0.3, pl.t(q1f) - pl.t(q0f)), midi("D4"), midi("D6"), v0=32, v1=46,
             scale=ChordTones(pl.chord_at(q0f + 1e-3)))
    pluck_chord(pl, 0, vel=50, lo=62, hi=74)
    pl.add("pz_cb", 0, 1, "D2", 50, "bass", "h")
    t_gold = pic(c, "sparkle", "上帝告诉你")
    pl.sync("'七年大丰收': the harvest (plucked chord, plucked bass)", 0, t_plenty)
    if t_gold is not None:
        accent(c, segs, t_gold, "the golden fields glint", glock=(86, 98), vel=46)
    else:
        pl.add("glock", 0, 1, "F#6", 46, "arp", "h")
    pl.add("horn", 0, 2, "A3", 44, "melody")
    pl.add("horn", 2, 2, "B3", 44, "melody")
    strings(pl, vel=40, lo=57, hi=74)
    pl.expr(["glock", "harp", "pz_hi", "pz_cb"], [(0, -10), (4, -11)])
    pl.expr(["horn"], [(0, -14), (4, -14)])
    pl.expr(STR, [(0, -15), (4, -15)])
    # then seven years of famine: bare low fifths, a thin high violin, a soft timpani
    fa.add("cb", 0, 2, "D2", 42, "bass")
    fa.add("vc", 0, 2, "A2", 40, "harmony")
    fa.add("trem_hi", 0, 2, "A5", 36, "pad")
    fa.add("trem_hi", 0, 2, "F5", 34, "pad", voice="trem_hi.1")
    fa.add("timp", 0, 0.5, "D3", 44, "timp", "h")
    fa.expr(["cb", "vc"], [(0, -12), (2, -14)])
    fa.expr(["trem_hi"], [(0, -18), (2, -19)])
    fa.expr(["timp"], [(0, -13), (2, -13)])
    # store up the grain while there is plenty: steady pizzicato steps; the golden row glows; the sacks thump in
    walk(st, "pz_lo", 0, 4, 46, 62, vel=48, step=1.0)
    st.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=34, bass_part="vc", bass_lo=45, bass_hi=58)
    t_row = pic(c, "sparkle", "上帝告诉你", 1)
    if t_row is not None:
        accent(c, segs, t_row, "the golden row glows", glock=(86, 98), vel=42)
    for k in range(2):
        t = pic(c, "thud", "上帝告诉你", k)
        if t is not None:
            accent(c, segs, t, f"sack {k + 1} lands in the granary", low=True, vel=44 + 2 * k)
    st.expr(["pz_lo"], [(0, -13), (4, -12)])
    for sg in (p, j, y, pl, fa, st):
        sg.expr(["glock"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])
    st.expr(["vla", "vln2", "vln1", "vc"], [(0, -17), (4, -15)])


def ruler(c):
    """Pharaoh speaks (G: God with you; Em7 A7, a timpani roll growing); D on '管理全埃及': the noble theme on horns and
    violins (glints on the ring, the robe and the gold chain); Em7 A7 on '坐上了大马车' (a snare roll as he walks out,
    a low thump as he lands in the chariot); the processional when the horse sets off with the herald's horn (snare,
    oom-pah, timpani, a light flute fanfare -- the brass enters with the theme's b2 only after the horn call); the
    grain heaped high like mountains (G A D, a run up, the glint on the top of the heap)."""
    c.gain(-3.0)
    t_rule = c.at("管理全埃及")
    t_chariot = c.at("坐上了大马车")
    t_mount = c.at("粮食堆得像山一样高")
    t_horn = pic(c, "horn", "约瑟穿上了", off=0.1)           # the horse sets off with the herald's horn (picture)
    t_go = min(max(t_horn if t_horn is not None else t_chariot + 1.4, t_chariot + 0.8), t_mount - 3.6)
    a = c.seg(0, t_rule, 2, "4/4", "D major", nominal=88, label="ruler-pharaoh")
    b = c.seg(t_rule, t_chariot, 2, "4/4", "D major", nominal=82, label="ruler-noble")
    k = c.seg(t_chariot, t_go, 1, "2/4", "D major", nominal=86, label="ruler-chariot")
    p = c.seg(t_go, t_mount, 2, "4/4", "D major", nominal=92, label="ruler-procession")
    m = c.seg(t_mount, c.dur, 1, "4/4", "D major", nominal=93, label="ruler-mountain")
    segs = (a, b, k, p, m)
    for sg in segs:
        sg.duck(1.5)
    a.prog("G:4 | Em7:2 A7:2")
    b.prog(" | ".join(JOSEPH_PROG[:2]))
    k.prog("Em7:1 A7:1")
    p.prog("D:4 | G:2 A:2")
    m.prog("G:1 A:1 D:2")
    b.sync("'管理全埃及': the noble theme (D major)", 0, t_rule, kind="change")
    k.sync("'坐上了大马车': Em7 (to the chariot)", 0, t_chariot, kind="change")
    if t_horn is not None and abs(t_horn - t_go) > 0.01:      # the picture's start away from the march's downbeat
        accent(c, segs, t_horn, "the horse sets off with the herald's horn", low=True, vel=50)
    else:
        p.sync("the horse sets off: the processional's first beat", 0, t_go)
    m.sync("'粮食堆得像山一样高': G, the run up", 0, t_mount, kind="change")
    # 'God is with you, no one is wiser than you': soft pads, a timpani roll growing
    a.pad("ooh", 3, 55, 72, vel=36, bass_ref=(43, 55))
    strings(a, vel=40, lo=55, hi=74, bass=(40, 55), cb=(28, 43))
    timp_roll(a, 5.0, 7.95, midi("A2"), 24, 44)
    a.duck(2.0)
    a.expr(["ooh"], [(0, -21), (8, -19)])
    a.expr(STR, [(0, -17), (5, -16), (8, -13)])
    a.expr(["timp"], [(5, -14), (8, -11)])
    # 'I put you in charge of all Egypt!': the theme on horns and violins; glints on the ring, robe and gold chain
    b.mel("horn", bars(JOSEPH, 0, 2), vel=56, transpose=-12)
    b.mel("vln_mel", bars(JOSEPH, 0, 2), vel=50)
    b.add("timp", 0, 0.5, "D3", 50, "timp", "h")
    b.add("okit", 0, 2, 57, 34, "perc", "h")
    gliss_in(b, "harp", 0, 0.4, midi("D4"), midi("D6"), v0=36, v1=50, scale=ChordTones(b.chord_at(0)))
    strings(b, vel=42, lo=55, hi=74)
    glints = [(pic(c, "sparkle", "上帝和你同在"), "the ring's glint ('管理全埃及')")]
    glints += [(pic(c, "sparkle", "约瑟穿上了", kk), what)
               for kk, what in enumerate(("the robes (sparkle burst)", "the gold chain's twinkle"))]
    if all(t is None for t, _ in glints[1:]):              # no picture: on the words
        glints[1:] = [(c.at("漂亮的衣服"), None), (c.at("金链子"), None)]
    for t, what in glints:
        if t is not None:
            accent(c, segs, t, what, glock=(84, 98), vel=42)
    b.duck(3.5, parts=["horn", "vln_mel"])
    b.expr(["horn"], [(0, -12), (8, -13)])
    b.expr(["vln_mel"], [(0, -17), (8, -18)])
    b.expr(["timp", "harp", "glock"], [(0, -10), (8, -11)])
    b.expr("okit", [(0, -14), (8, -14)])
    b.expr(STR, [(0, -16), (8, -16)])
    # he walks out and hops into the great chariot: Em7 A7, a snare roll, a thump as he lands
    t_land = pic(c, "thud", "约瑟穿上了")
    q_end = k.n_q - 0.45 if t_land is None else min(k.n_q - 0.45, max(0.0, k.q_of(c.t0 + t_land) - 0.45))
    if q_end > 0.6:
        roll(k, 0.2, q_end, 38, 18, 30, rate=12)
    k.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=36, bass_part="vc", bass_lo=50, bass_hi=62)
    k.mel("cb", "E2:1 A2:1", vel=38, role="bass")
    if t_land is not None:
        accent(c, segs, t_land, "Joseph lands in the chariot", low=True, vel=48)
    k.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (2, -14)])
    k.expr("okit", [(0, -14), (2, -12)])
    k.expr(["timp", "pz_cb"], [(0, -11), (2, -11)])
    # the horse sets off (the herald's horn on the picture): the processional; the brass enters after the horn call
    p.mel("flute", "A5:1/2 F#5:1/2 D5:1/2 F#5:1/2 A5:1 D6:1 | B5:1 D6:1 C#6:1 E6:1", vel=44)
    p.mel("brass", "r:4 | B4:1 D5:1 C#5:1 E5:1", vel=52)
    oompah(p, 0, 8, vel=50, bass="tuba", blo=33, bhi=45)
    snare(p, 0, 8, vel=30)
    for q in (0, 4):
        p.add("timp", q, 0.5, timp_pitch(p.chord_at(q + 1e-3), midi("D3")), 56 if q == 0 else 44, "timp", "h")
        p.add("okit", q, 1, 36, 54 if q == 0 else 40, "perc", "h")
    pluck_chord(p, 0, vel=56, lo=62, hi=74)
    t_silo = pic(c, "grow", "七年丰收", lo=t_go, hi=t_mount - 0.3)      # the granary silos fill: a harp sweep up
    if t_silo is not None:
        q = qpos(p, c, t_silo)
        gliss_in(p, "harp", q, 0.6, midi("A3"), midi("A5"), v0=28, v1=40, scale=ChordTones(p.chord_at(q + 1e-3)))
    p.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=34, bass_ref=(33, 45))
    p.duck(3.5, parts=["brass", "flute"])
    p.expr(["brass", "flute"], [(0, -15), (8, -16)])
    p.expr(["tuba", "pz_hi"], [(0, -13), (8, -14)])
    p.expr(["timp", "harp"], [(0, -10), (8, -12)])
    p.expr("okit", [(0, -12), (8, -13)])
    p.expr(["vla", "vln2", "vln1"], [(0, -17), (8, -17)])
    # the grain heaped up like mountains: a run up into D, the glint on the top of the heap
    m.mel("vln_mel", "G5:1/4 A5:1/4 B5:1/4 C#6:1/4 A5:1/4 B5:1/4 C#6:1/4 E6:1/4 D6:2", vel=48)
    m.mel("flute", "B5:1 C#6:1 D6:2", vel=44)
    timp_roll(m, 0, 1.9, midi("A2"), 26, 40)
    t_top = pic(c, "sparkle", "七年丰收")
    if t_top is not None:
        sg, q = accent(c, segs, t_top, "the top of the grain mountain glints", glock=(86, 98), vel=42)
        sg.add("timp", q, _dq(sg, q, 0.5), timp_pitch(sg.chord_at(q + 1e-3), midi("D3")), 46, "timp", "h")
    else:
        m.add("timp", 2, 0.5, "D3", 46, "timp", "h")
        m.add("glock", 2, 1, "D7", 42, "arp", "h")
    strings(m, vel=42, lo=57, hi=76)
    m.duck(2.5, parts=["vln_mel", "flute"])
    m.expr(["vln_mel", "flute"], [(0, -17), (4, -17)])
    m.expr(STR, [(0, -15), (4, -14)])
    for sg in segs:
        sg.expr(["glock"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])


def brothers(c):
    """The famine (D minor, bare fifths, an airy flute; a low thump as the empty grain jar topples); the brothers come
    to Egypt: their motif slow and legato, the donkeys' woodblock steps (Dm Gm Dm A); B-flat on '跪下下拜' (a falling
    celesta, two low thumps as they kneel), Joseph knows them (a start: glockenspiel and pizzicato; motif x on the
    oboe over A); the dream again ('你还记得约瑟的梦吗': Bm7 Em7, harp and celesta; the bubble, his sheaf rising, the
    sheaves bowing on the picture) and the bow over G A7sus4 onto the glowing D -- the harmony on '现在真的发生了', the
    attack on the picture's twinkles."""
    c.gain(-2.4)
    t_bro = c.at("约瑟的哥哥们")
    t_bow = c.at("跪下下拜")
    t_ask = c.gap(c.find("小朋友，你还记得"))
    t_real = c.at("现在真的发生了")
    t_true = pic(c, "sparkle", "小朋友，你还记得", 1)          # the brothers dip lower with the sheaves: twinkles
    t_land = t_true if t_true is not None and t_real - 0.45 <= t_true <= c.dur - 0.1 else None
    a = c.seg(0, t_bro, 1, "4/4", "D minor", nominal=95, label="brothers-famine")
    b = c.seg(t_bro, t_bow, 2, "4/4", "D minor+", nominal=84, label="brothers-travel")
    k = c.seg(t_bow, t_ask, 1, "4/4", "D minor+", nominal=67, label="brothers-bow")
    d = c.seg(t_ask, t_real, 3, "6/8", "D major", nominal=96, label="brothers-dream")
    e = c.seg(t_real, c.dur, 1, "2/4", "D major", nominal=63, label="brothers-glow")
    for sg in (a, b, k, d, e):
        sg.duck(1.5)
    a.prog("Dm:4")
    b.prog("Dm:2 Gm:2 | Dm:2 A:2")
    k.prog("Bb:2 A:2")
    d.prog("Bm7:3 | Em7:3 | G:3/2 A7sus4:3/2")
    e.prog("D:2")
    k.sync("'跪下下拜': B-flat (they bow)", 0, t_bow, kind="change")
    e.sync("'现在真的发生了': the glowing sheaf (D major)", 0, t_real, kind="change")
    # then the famine came: bare fifths, an airy flute
    a.add("cb", 0, 4, "D2", 40, "bass")
    a.add("vc", 0, 4, "A2", 38, "harmony")
    a.pad(["trem_hi", "trem_hi"], 2, 62, 77, vel=34, bass_ref=(38, 50))
    a.mel("flute", "F5:2 A5:2", vel=40)
    a.expr(["cb", "vc"], [(0, -16), (4, -15)])
    a.expr(["trem_hi"], [(0, -21), (4, -20)])
    a.expr(["flute"], [(0, -18), (4, -17)])
    # Joseph's brothers had nothing to eat and came to Egypt: their motif, slow and tired; the donkeys' steps
    b.mel("bsn", "D3:1 F3:1/2 E3:1/2 Eb3:1 D3:1 | F3:1 E3:1/2 D3:1/2 C#3:2", vel=52)
    b.mel("pz_cb", "D2:1:s r:1 G1:1:s r:1 | D2:1:s r:1 A1:1:s r:1", vel=46, role="bass")
    for q in range(8):
        drum(b, q + 0.5, 76 if q % 2 == 0 else 77, 34)
    b.pad(["vla", "vln2"], 2, 52, 67, vel=32, bass_ref=(31, 43))
    b.expr(["bsn"], [(0, -12), (8, -12)])
    b.expr(["pz_cb"], [(0, -13), (8, -13)])
    b.expr("hand", [(0, -13), (8, -14)])
    b.expr(["vla", "vln2"], [(0, -19), (8, -18)])
    # they bowed down before Joseph -- but they did not recognise him: a bow (celesta), motif x on the oboe
    k.mel("celesta", "F6:1/2 D6:1/2 Bb5:1", vel=40)
    k.mel("oboe", "r:2 C#5:1 E5:1", vel=48)
    k.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=36, bass_part="vc", bass_lo=45, bass_hi=58)
    k.add("cb", 0, 2, "Bb1", 36, "bass")
    k.add("cb", 2, 2, "A1", 36, "bass")
    k.expr(["celesta"], [(0, -12), (4, -13)])
    k.expr(["oboe"], [(0, -14), (4, -14)])
    k.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (4, -17)])
    # 'do you remember Joseph's dream? his brothers' sheaves bowed down to him...': the dream and the bow
    d.mel("celesta", "F#6:3/2 D6:1/2 B5:1 | B5:3/2 D6:3/2", vel=40)
    broken(d, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    bow(d, 6.0, vel=44, q_end=None if t_land is None or t_land >= t_real else d.q_of(c.t0 + t_land))
    d.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=34, bass_part="vc", bass_lo=43, bass_hi=55)
    d.duck(2.5, parts=["celesta", "harp"])
    d.expr(["celesta", "harp"], [(0, -12), (9, -11)])
    d.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (9, -15)])
    # '...now it really happened!': the glowing sheaf (its attack on the picture's twinkles)
    glow(e, 0, vel=52, land=None if t_land is None else seg_at(c, (d, e), t_land))
    strings(e, vel=42, lo=57, hi=76)
    e.expr(["celesta", "glock", "harp", "timp", "pz_cb"], [(0, -10), (2, -12)])
    e.expr(["ooh"], [(0, -16), (2, -18)])
    e.expr(STR, [(0, -14), (2, -16)])
    # the picture: the empty jar topples; they kneel (two thuds); Joseph starts up; the dream bubble; his sheaf rises;
    # the sheaves bow; the twinkles as it comes true
    segs = (a, b, k, d, e)
    if t_land is not None:
        sg, q = seg_at(c, (d, e), t_land)
        sg.sync("it really happened: the glow (twinkles)", q, t_land)
    elif t_true is not None:
        accent(c, segs, t_true, "it really happened (twinkles)", glock=(86, 98), vel=46)
    else:
        e.sync("'现在真的发生了': the glow (glockenspiel, harp)", 0, t_real)
    t_jar = pic(c, "thud", "后来，饥荒来了")
    if t_jar is not None:
        accent(c, segs, t_jar, "the empty grain jar topples", low=True, vel=46)
    for kk in range(2):
        t = pic(c, "thud", "他们向约瑟跪下", kk)
        if t is not None:
            accent(c, segs, t, f"they kneel ({kk + 1})", low=True, vel=50 - 6 * kk)
    t_start = pic(c, "pop", "他们向约瑟跪下")
    if t_start is not None:
        accent(c, segs, t_start, "Joseph knows them (a start)", glock=(84, 96), pluck=(62, 74), harp=(62, 74), vel=56)
    t_bub = pic(c, "chime", "小朋友，你还记得")
    if t_bub is not None:
        accent(c, segs, t_bub, "the dream bubble rises", celesta=(79, 93), harp=(62, 74), vel=46)
    t_rise = pic(c, "grow", "小朋友，你还记得")
    if t_rise is not None:
        accent(c, segs, t_rise, "Joseph's sheaf stands up and glows", glock=(81, 93), pluck=(64, 76), vel=46)
    t_sbow = pic(c, "sparkle", "小朋友，你还记得")
    if t_sbow is not None:
        accent(c, segs, t_sbow, "the sheaves bow", celesta=(76, 88), vel=46)
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["pz_hi", "harp"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])


def forgive(c):
    """Joseph cannot hold back (G Em7 A7sus4: strings swelling, the violins rising); D on '我就是约瑟': the theme in
    the violins, horn arpeggio, choir (the headcloth flying off on the picture: glockenspiel, pizzicato, harp); B minor
    fear (tremolo, the brothers' motif small; a thump as they jump back); tender (D A/C#: '不要害怕'); G on
    '可是上帝把它变成了好事' (choir; God's light stays a soft swell), Em7 A7; the theme b5-b7 full (violins and clarinet,
    a horn counter-melody; soft harp/celesta touches on the hugs); D on '一家人，又在一起了' (choir 'ah', timpani, harp
    sweep, glockenspiel), with glints for Joseph and Jacob's hug and the family's twinkles on the picture."""
    c.gain(-3.0)
    t_me = c.at("我就是约瑟")
    t_fear = c.gap(c.find("哥哥们吓坏了"))
    t_dont = c.gap(c.find("不要害怕"))
    t_good = c.at("可是上帝把它变成了好事")
    t_hug = c.gap(c.find("约瑟抱住哥哥们"))
    t_fam = c.at("一家人，又在一起了")
    a = c.seg(0, t_me, 2, "4/4", "D major", nominal=100, label="forgive-tears")
    b = c.seg(t_me, t_fear, 1, "4/4", "D major", nominal=85, label="forgive-reveal")
    f = c.seg(t_fear, t_dont, 2, "4/4", "B minor+", nominal=112, label="forgive-fear")
    d = c.seg(t_dont, t_good, 1, "4/4", "D major", nominal=84, label="forgive-dont")
    g = c.seg(t_good, t_hug, 2, "4/4", "D major", nominal=110, label="forgive-good")
    e = c.seg(t_hug, t_fam, 3, "4/4", "D major", nominal=108, label="forgive-hug")
    h = c.seg(t_fam, c.dur, 1, "4/4", "D major", nominal=98, label="forgive-family")
    for sg in (a, b, f, d, g, e, h):
        sg.duck(1.5)
    a.prog("G:4 | Em7:2 A7sus4:1 A7:1")
    b.prog("D:4")
    f.prog("Bm:4 | Em:2 F#:2")
    d.prog("D:2 A/C#:2")
    g.prog("G:4 | Em7:2 A7:2")
    e.prog(" | ".join(JOSEPH_PROG[4:7]))
    h.prog("D:4")
    b.sync("'我就是约瑟': D major, the theme", 0, t_me, kind="change")
    g.sync("'可是上帝把它变成了好事': G (choir)", 0, t_good, kind="change")
    h.sync("'一家人，又在一起了': D major, the family together", 0, t_fam, kind="change")
    # Joseph could not hold back any longer and wept: strings swell, the violins rise
    a.mel("vln_mel", "D5:2 B4:1 D5:1 | E5:2 D5:1 C#5:1", vel=48)
    strings(a, vel=40, lo=55, hi=72, bass=(40, 52), cb=(28, 40))
    a.pad("ooh", 3, 55, 72, vel=34, bass_ref=(40, 52))
    a.duck(2.5, parts=["vln_mel"])
    a.expr(["vln_mel"], [(0, -18), (8, -14)])
    a.expr(STR, [(0, -18), (8, -14)])
    a.expr(["ooh"], [(0, -23), (8, -19)])
    # 'I am Joseph, your brother!': the theme in the violins and horn, choir, a harp sweep
    b.mel("vln_mel", JOSEPH[0], vel=52)
    b.mel("horn", "D3:1 F#3:1 A3:2", vel=48)
    gliss_in(b, "harp", 0, 0.45, midi("D4"), midi("D6"), v0=36, v1=50, scale=ChordTones(b.chord_at(0)))
    b.add("pz_cb", 0, 1, "D2", 50, "bass", "h")
    b.pad("ooh", 3, 57, 74, vel=38, bass_ref=(38, 50))
    strings(b, vel=44, lo=57, hi=74)
    b.duck(4.0, parts=["vln_mel", "horn", "ooh"])
    b.expr(["vln_mel", "horn"], [(0, -14), (4, -15)])
    b.expr(["ooh"], [(0, -17), (4, -18)])
    b.expr(["harp", "pz_cb"], [(0, -10), (4, -11)])
    b.expr(STR, [(0, -14), (4, -15)])
    # the brothers were terrified he would pay them back: tremolo, the motif small and scared
    f.pad(["trem_va", "trem_va", "trem_hi"], 3, 50, 71, vel=40, bass_ref=(35, 47))
    jealous(f, 0, 0, vel=48, transpose=-5)
    f.mel("cb", "B1:4 | E2:2 F#2:2", vel=36, role="bass")
    f.expr(["trem_va", "trem_hi", "cb"], [(0, -19), (8, -17)])
    f.expr(["bsn"], [(0, -15), (8, -15)])
    # 'don't be afraid; you meant to harm me...': tender, soft
    d.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=36, bass_part="vc", bass_lo=37, bass_hi=50)
    d.add("harp", 0, 2, "F#5", 34, "arp")
    d.add("harp", 2, 2, "E5", 32, "arp")
    d.duck(2.0)
    d.expr(["vla", "vln2", "vln1", "vc"], [(0, -18), (4, -18)])
    d.expr(["harp"], [(0, -13), (4, -13)])
    # '...but God turned it into good, and saved many lives': G, warm choir
    g.pad("ooh", 3, 55, 72, vel=38, bass_ref=(40, 52))
    strings(g, vel=40, lo=55, hi=74, bass=(40, 52), cb=(28, 40))
    broken(g, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 43, 55, vel=32, thin=True)
    g.duck(2.5)
    g.expr(["ooh"], [(0, -19), (2, -17), (8, -17)])
    g.expr(STR, [(0, -16), (8, -15)])
    g.expr(["harp"], [(0, -12), (8, -12)])
    # Joseph hugged his brothers and forgave them; then father Jacob came too: the theme b5-b7, full and tender
    e.mel("vln_mel", bars(JOSEPH, 4, 7), vel=54)
    e.mel("clar", bars(JOSEPH, 4, 7), vel=46)
    e.mel("horn", "F#3:4 | G3:2 A3:2 | G3:2 G3:2", vel=44, role="counter")
    broken(e, "harp", 0, 12, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    strings(e, vel=44, lo=55, hi=74)
    e.pad("ooh", 3, 55, 72, vel=36, q0=4, bass_ref=(38, 50))
    e.duck(4.0, parts=["vln_mel", "clar", "horn", "harp", "ooh"])
    e.expr(["vln_mel"], [(0, -15), (1.5, -13), (12, -12)])
    e.expr(["clar"], [(0, -17), (12, -15)])
    e.expr(["horn", "harp"], [(0, -15), (12, -13)])
    e.expr(STR, [(0, -15), (12, -13)])
    e.expr(["ooh"], [(4, -20), (6, -17), (12, -16)])
    # 'a family, together again!': D major -- choir 'ah', timpani, a harp sweep, glockenspiel, the theme's D
    h.mel("vln_mel", "D5:4", vel=54)
    h.mel("clar", "D5:4", vel=46)
    h.add("horn", 0, 4, "F#3", 44, "counter")
    h.pad("choir", 3, 57, 74, vel=42, bass_ref=(38, 50))
    gliss_in(h, "harp", 0, 0.4, midi("D4"), midi("D6"), v0=36, v1=52, scale=ChordTones(h.chord_at(0)))
    h.add("glock", 0, 1, "A6", 44, "arp", "h")
    h.add("timp", 0, 0.5, "D3", 50, "timp", "h")
    h.add("pz_cb", 0, 1, "D2", 52, "bass", "h")
    strings(h, vel=46, lo=57, hi=76)
    h.duck(4.0, parts=["choir", "vln_mel", "clar", "horn"])
    h.expr(["vln_mel", "clar"], [(0, -14), (3, -15), (4, -19)])
    h.expr(["horn"], [(0, -14), (3, -15), (4, -19)])
    h.expr(["choir"], [(0, -17), (3, -18), (4, -22)])
    h.expr(["harp", "glock", "timp", "pz_cb"], [(0, -10), (4, -13)])
    h.expr(STR, [(0, -13), (3, -15), (4, -19)])
    # the picture: the headcloth flies off ('我就是约瑟'); the brothers jump back, scared; the hugs; Joseph and Jacob;
    # the family's twinkles (God's light on '上帝把它变成了好事' stays a soft swell: no attack)
    segs = (a, b, f, d, g, e, h)
    t_cloth = pic(c, "whoosh", "我就是约瑟")
    if t_cloth is not None:
        sg, q = accent(c, segs, t_cloth, "the headcloth flies off ('我就是约瑟')", glock=(86, 98), pluck=(62, 74),
                       harp=(62, 74), vel=58)
        pluck_chord(sg, q, vel=56, lo=50, hi=62, part="pz_lo")
    t_scared = pic(c, "thud", "哥哥们吓坏了")
    if t_scared is not None:
        sg, q = accent(c, segs, t_scared, "the brothers jump back, scared", low=True, vel=48)
        pluck_chord(sg, q, vel=50, lo=59, hi=71)
    for kk, what in enumerate(("he hugs Judah", "he hugs the next brother")):
        t = pic(c, "cloth", "约瑟抱住哥哥们", kk)
        if t is not None:
            accent(c, segs, t, what, harp=(62, 76), celesta=(74, 86), vel=46)
    t_dad = pic(c, "chime", "约瑟抱住哥哥们")
    if t_dad is not None:
        accent(c, segs, t_dad, "Joseph and Jacob hug", glock=(86, 98), celesta=(74, 86), vel=46)
    t_all = pic(c, "sparkle", "约瑟抱住哥哥们")
    if t_all is not None:
        accent(c, segs, t_all, "the family together (twinkles)", glock=(88, 100), vel=46)
    for sg in segs:
        sg.expr(["glock", "celesta"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["pz_hi", "harp"], [(0, -11), (sg.n_q, -11)])
        sg.expr(["timp", "pz_cb"], [(0, -11), (sg.n_q, -11)])
        sg.expr("okit", [(0, -13), (sg.n_q, -13)])


def end(c):
    """Three misfortunes (B minor, E minor, F#7, one per picture panel as it pops onto the string: a low clarinet
    note, a soft pluck); D on '可是他从来没有离开上帝' (choir, the theme b1-b2 on the flute, harp; a glint as the golden
    light fills the panels); the question (Em7 Gmaj7, a celesta), then only a soft A7sus4 held through the 2 s pause;
    the theme b5-b7 warm (clarinet, horn, strings, choir; glints as the siblings hug, Joseph's picture glows and the
    toy is shared); the final D major chord on the end of '学会原谅', ringing to the end (the end card's chime)."""
    c.gain(-2.4)
    t_but = c.at("可是他从来没有离开上帝")
    t_q = c.gap(c.find("小朋友，如果"))
    i_q = c.find("小朋友，如果")
    t_e = max(c.ls(i_q + 1) - 0.4, (c.le(i_q) + c.ls(i_q + 1)) / 2)
    t_f = c.le(c.find("学会原谅"))
    a = c.seg(0, t_but, 3, "2/4", "B minor+", nominal=84, label="end-misfortunes")
    b = c.seg(t_but, t_q, 2, "4/4", "D major", nominal=96, label="end-never-left")
    long_q = t_e - t_q >= 5.0                     # the question and (most of) its 2 s pause
    ask = c.seg(t_q, t_e, 2, "4/4" if long_q else "3/4", "D major", nominal=80 if long_q else 84, label="end-question")
    e = c.seg(t_e, t_f, 3, "4/4", "D major", nominal=100, rit=0.15, label="end-theme")
    f = c.seg(t_f, c.dur, 1, "2/4", "D major", nominal=90, rit=0.3, label="end-final-chord")
    for sg in (a, b, ask, e):
        sg.duck(1.5)
    # three panels pop onto the string, one per misfortune (picture; the narrator's groups without it): Bm Em F#7
    panels = [pic(c, "pop", "约瑟被卖", kk) for kk in range(3)]
    have = None not in panels
    if not have:
        panels = syl(c, "约瑟被卖", 3)
    qp = [qpos(a, c, t, 0.0, a.n_q - 0.3) for t in panels]
    qp[1] = min(max(qp[1], qp[0] + 0.5, 1.0), 4.5)
    qp[2] = min(max(qp[2], qp[1] + 0.75), 5.5)
    qp = [round(q * 48) / 48 for q in qp]                 # on the chords' grid
    edges = [0] + [int(round(q * 48)) for q in qp[1:]] + [int(round(a.n_q * 48))]
    a.prog(" ".join(f"{ch}:{edges[i + 1] - edges[i]}/48" for i, ch in enumerate(["Bm", "Em", "F#7"])))
    b.prog(" | ".join(JOSEPH_PROG[:2]))
    ask.prog("Em7:2 Gmaj7:2 | A7sus4:4" if long_q else "Em7:3/2 Gmaj7:3/2 | A7sus4:3")
    e.prog(" | ".join(JOSEPH_PROG[4:7]))
    f.prog("D:2")
    b.sync("'可是他从来没有离开上帝': D major (God never left him)", 0, t_but, kind="change")
    f.sync("the final D major chord (after '学会原谅')", 0, t_f, kind="change")
    f.sync("the final chord: harp roll", 0, t_f)
    # sold, wrongly accused, put in prison: three soft chords, a low clarinet note, a soft pluck for each panel
    for kk, (q, nm) in enumerate(zip(qp, ["D5", "E5", "C#5"])):
        q_end = qp[kk + 1] if kk < 2 else a.n_q
        a.add("clar", q, q_end - q, nm, 46, "melody")
    for kk, t in enumerate(panels):
        sg, q = seg_at(c, (a, b), t)
        sg.add("pz_hi", q, _dq(sg, q, 0.5), top(sg, q, 62, 74), 62 if kk == 0 else 58, "arp", "h")
        if kk == 0:
            sg.add("celesta", q, _dq(sg, q, 1.0), top(sg, q, 74, 86), 48, "arp", "h")
        sg.add("harp", q, _dq(sg, q, 1.0), top(sg, q, 50, 62, 0), 52, "arp", "h")
        if have:
            sg.sync(f"panel {kk + 1} pops onto the string", q, t)
    a.expr(["pz_hi", "harp", "celesta"], [(0, -10), (6, -10)])
    a.pad(["vla", "vln2", "vln1"], 3, 50, 69, vel=34, bass_part="vc", bass_lo=40, bass_hi=52)
    a.expr(["clar"], [(0, -15), (6, -15)])
    a.expr(["vla", "vln2", "vln1", "vc"], [(0, -16), (6, -17)])
    # but he never left God, and God never left him: D, choir, the theme on the flute
    b.mel("flute", bars(JOSEPH, 0, 2), vel=50, transpose=12)
    broken(b, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    b.pad("ooh", 3, 55, 72, vel=36, bass_ref=(38, 50))
    strings(b, vel=40, lo=55, hi=72)
    b.duck(2.5, parts=["flute", "harp", "ooh"])
    b.expr(["flute"], [(0, -15), (8, -15)])
    b.expr(["harp"], [(0, -11), (8, -11)])
    b.expr(["ooh"], [(0, -20), (8, -19)])
    b.expr(STR, [(0, -16), (8, -16)])
    t_gold = pic(c, "chime", "约瑟被卖")                    # a golden light glows up in every panel
    if t_gold is not None:
        accent(c, (a, b, ask, e, f), t_gold, "the golden light in the panels", glock=(86, 98), celesta=(74, 86),
               vel=44)
    # 'if someone is unkind to you, will you forgive them?': the celesta asks; then only the soft held A7sus4
    ask.mel("celesta", "E6:1 B5:1 D6:1 F#6:1 | E6:2 r:2" if long_q else "E6:3/4 B5:3/4 D6:3/4 F#6:3/4 | E6:3/2 r:3/2",
          vel=40, role="arp")
    ask.pad(["vla", "vln2", "vln1"], 3, 57, 74, vel=34, bass_part="vc", bass_lo=50, bass_hi=62)
    h_ = ask.bar_q / 2
    ask.mel("cb", f"E2:{h_:g} G2:{h_:g} | A2:{ask.bar_q:g}", vel=34, role="bass")
    ask.expr(["celesta"], [(0, -11), (ask.bar_q, -12), (ask.n_q, -15)])
    ask.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (ask.bar_q, -17), (ask.n_q, -18)])
    # 'God can turn bad things into good; we can learn to forgive like Joseph': the theme b5-b7, warm
    e.mel("clar", bars(JOSEPH, 4, 7), vel=56)
    e.mel("horn", "F#3:4 | G3:2 A3:2 | G3:2 G3:2", vel=42, role="counter")
    broken(e, "harp", 0, 12, (0, 2, 4, 6, 4, 2), 38, 50, vel=34, thin=True)
    strings(e, vel=42, lo=55, hi=72)
    e.pad("ooh", 3, 55, 72, vel=36, q0=4, bass_ref=(38, 50))
    e.duck(4.0, parts=["clar", "horn", "harp", "ooh"])
    e.expr(["clar"], [(0, -21), (1.5, -13), (12, -13)])
    e.expr(["horn", "harp"], [(0, -21), (1.5, -14), (12, -14)])
    e.expr(STR, [(0, -20), (1.5, -16), (12, -15)])
    e.expr(["ooh"], [(4, -20), (6, -17), (12, -16)])
    # the picture: they hug (the cloud turns sunny); Joseph hugging his brother glows up; she shares the toy horse
    for nm, kk, part, what in (("sparkle", 0, "glock", "they hug: the cloud turns sunny"),
                               ("chime", 0, "celesta", "the picture of Joseph and his brother glows up"),
                               ("sparkle", 1, "glock", "she shares the toy horse")):
        t = pic(c, nm, "上帝可以", kk)
        if t is not None:
            if part == "glock":
                accent(c, (a, b, ask, e, f), t, what, glock=(86, 98), vel=44)
            else:
                accent(c, (a, b, ask, e, f), t, what, celesta=(76, 88), vel=50)
    # the final D major chord: harp rolled up, the clarinet's D, celesta, strings, ooh -- it rings to the end
    f.mel("clar", "D5:2", vel=52)
    for k_, nm in enumerate(["D2", "A2", "D3", "F#3", "A3", "D4", "F#4", "A4", "D5"]):
        f.add("harp", 0.06 * k_, 2 - 0.06 * k_, nm, 46 - 2 * k_, "arp", "r")
    f.mel("celesta", "A5:1/2 D6:1/2 F#6:1", vel=36, art="r", role="arp")
    strings(f, vel=40, lo=57, hi=72)
    f.pad("ooh", 3, 57, 72, vel=38, bass_ref=(38, 50))
    f.expr(["clar", "vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -15), (0.5, -14.5), (1.4, -17), (2, -26)])
    f.expr(["harp", "celesta"], [(0, -13), (2, -17)])
    t_card = pic(c, "chime", "上帝可以", 1)                 # the end card's chime
    if t_card is not None:
        sg, q = seg_at(c, (a, b, ask, e, f), t_card)
        if sg is f:
            f.add("glock", q, f.n_q - q, "A6", 40, "arp", "r")
            f.sync("the end card", q, t_card)
        else:
            accent(c, (a, b, ask, e, f), t_card, "the end card", glock=(86, 98), vel=40)
    for sg in (a, b, ask, e):
        sg.expr(["glock", "celesta"], [(0, -11), (sg.n_q, -12)])


SCENE_CUES = {
    "s01_title": title, "s02_question": question, "s03_coat": coat, "s04_dream": dream, "s05_pit": pit,
    "s06_sold": sold, "s07_jacob": jacob, "s08_egypt": egypt, "s09_prison": prison, "s10_pharaoh": pharaoh,
    "s11_ruler": ruler, "s12_brothers": brothers, "s13_forgive": forgive, "s14_end": end,
}

# Hit points the score must place, defined by the narration text (audio/music_check.py REQUIRED_HITS format:
# (scene, phrase, mode, kind); mode 'line' / 'gap' / 'phrase' / 'end', kind 'hit' (attack) or 'change' (harmony)).
# Where a word is also an on-screen action (the colour bands, the coins, the gulp...) the phrase is where the harmony
# arrives, and the attacks themselves follow the picture: PICTURE_HITS.
REQUIRED_HITS = [
    ("s02_question", "可是后来", "phrase", "change"),           # hope: D major, motif x
    ("s03_coat", "红", "phrase", "change"),                     # the colours begin (D)
    ("s03_coat", "绿", "phrase", "change"),                     # green (G)
    ("s03_coat", "酸溜溜的", "phrase", "change"),               # the jealousy (E minor)
    ("s03_coat", "酸溜溜的", "phrase", "hit"),                  # ... the bassoon's first note
    ("s04_dream", "下拜", "phrase", "change"),                  # the glowing sheaf (D major)
    ("s05_pit", "剥下约瑟的彩衣", "phrase", "change"),          # the coat torn off (C)
    ("s06_sold", "二十块银子", "phrase", "change"),             # the price (F)
    ("s07_jacob", "哭了很久很久", "phrase", "change"),          # Jacob weeps (B-flat)
    ("s08_egypt", "上帝和约瑟同在", "phrase", "change"),        # God with Joseph (B-flat)
    ("s08_egypt", "被人冤枉", "phrase", "change"),              # wrongly accused (D minor)
    ("s08_egypt", "上帝还是和约瑟同在", "phrase", "change"),    # God still with him (B-flat)
    ("s09_prison", "是上帝", "phrase", "change"),               # it is God (B-flat)
    ("s10_pharaoh", "七头肥肥的牛", "phrase", "change"),        # the fat cows' waltz (F)
    ("s10_pharaoh", "吃掉了", "phrase", "change"),              # A: the thin cows gulp them down (gulps: picture)
    ("s10_pharaoh", "有人想起了约瑟", "phrase", "change"),      # Joseph remembered (D, motif x)
    ("s10_pharaoh", "七年大丰收", "phrase", "change"),          # plenty (D major)
    ("s10_pharaoh", "七年大饥荒", "phrase", "change"),          # famine (D minor, bare)
    ("s11_ruler", "管理全埃及", "phrase", "change"),            # the noble theme (D major)
    ("s11_ruler", "坐上了大马车", "phrase", "change"),          # to the chariot (the procession: picture)
    ("s11_ruler", "粮食堆得像山一样高", "phrase", "change"),    # the grain heaped high
    ("s12_brothers", "跪下下拜", "phrase", "change"),           # they bow (B-flat)
    ("s12_brothers", "现在真的发生了", "phrase", "change"),     # the dream come true (the glowing D)
    ("s13_forgive", "我就是约瑟", "phrase", "change"),          # the reveal (D major, the theme)
    ("s13_forgive", "可是上帝把它变成了好事", "phrase", "change"),  # God turned it to good (G)
    ("s13_forgive", "一家人，又在一起了", "phrase", "change"),  # together again (D major)
    ("s14_end", "可是他从来没有离开上帝", "phrase", "change"),  # God never left him (D)
    ("s14_end", "学会原谅", "end", "change"),                   # the final chord
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or
# None, index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation.  Filled in as the
# scenes are drawn.
PICTURE_HITS = [
    ("s01_title", "sparkle", "圣经绘本", 0, 0.0, "hit", "the coat twinkles ('彩衣')"),
    ("s02_question", "cloth", "小朋友", 0, 0.0, "hit", "the sister grabs the toy horse"),
    ("s02_question", "thud", "小朋友", 0, 0.0, "hit", "she stumbles back hugging it"),
    ("s02_question", "pop", "小朋友", 0, 0.0, "hit", "the little storm cloud pops up ('很久很久')"),
    ("s02_question", "sparkle", "今天的故事里", 0, 0.0, "hit", "the coat's sparkle burst ('很了不起的事')"),
    ("s03_coat", "pop", "很久以前", 0, 0.0, "hit", "son 1 pops up"),
    ("s03_coat", "pop", "很久以前", 11, 0.0, "hit", "son 12 (Benjamin) pops up"),
    ("s03_coat", "sparkle", "雅各最疼爱的", 0, 0.0, "hit", "the warm heart ('最疼爱的')"),
    ("s03_coat", "sparkle", "红", 0, 0.0, "hit", "colour band 1 (红)"),
    ("s03_coat", "sparkle", "红", 1, 0.0, "hit", "colour band 2 (黄)"),
    ("s03_coat", "sparkle", "红", 2, 0.0, "hit", "colour band 3 (蓝)"),
    ("s03_coat", "sparkle", "红", 3, 0.0, "hit", "colour band 4 (绿)"),
    ("s03_coat", "chime", "红", 0, 0.0, "hit", "'好漂亮': Joseph wears the coat (D major)"),
    ("s04_dream", "chime", "有一天晚上", 0, 0.0, "hit", "the dream bubble opens"),
    ("s04_dream", "grow", "我梦见", 0, 0.0, "hit", "Joseph's sheaf stands up"),
    ("s04_dream", "sparkle", "我梦见", 0, 0.0, "hit", "the sheaf glows"),
    ("s04_dream", "chime", "我梦见", 0, 0.0, "hit", "the sheaves bow: the glow"),
    ("s04_dream", "thud", "哥哥们听了", 0, 0.0, "hit", "the brothers stamp ('更生气了')"),
    ("s05_pit", "sparkle", "哥哥们远远看见", 0, 0.0, "hit", "the coat glints far away"),
    ("s05_pit", "whoosh", "他们剥下", 0, 0.0, "hit", "the coat flies (a swish)"),
    ("s05_pit", "cloth", "他们剥下", 0, 0.0, "hit", "the coat lands on the grass"),
    ("s05_pit", "thud", "他们剥下", 0, 0.0, "hit", "Joseph lands in the pit"),
    ("s05_pit", "thud", "他们剥下", 1, 0.0, "hit", "he scuffs the dry floor (dust)"),
    ("s06_sold", "whoosh", "哥哥们把约瑟拉上来", 0, 0.0, "hit", "the rope is thrown down"),
    ("s06_sold", "coins", "哥哥们把约瑟拉上来", 0, 0.0, "hit", "coin 1 (the silver counted out)"),
    ("s06_sold", "coins", "哥哥们把约瑟拉上来", 1, 0.0, "hit", "coin 2"),
    ("s06_sold", "coins", "哥哥们把约瑟拉上来", 2, 0.0, "hit", "coin 3"),
    ("s06_sold", "coins", "哥哥们把约瑟拉上来", 3, 0.0, "hit", "coin 4"),
    ("s06_sold", "coins", "哥哥们把约瑟拉上来", 4, 0.0, "hit", "coin 5"),
    ("s06_sold", "pop", "哥哥们把约瑟拉上来", 0, 0.0, "hit", "the '20' badge pops"),
    ("s07_jacob", "cloth", "哥哥们把彩衣", 0, 0.0, "hit", "the coat is torn (a puff of dust)"),
    ("s07_jacob", "cloth", "哥哥们把彩衣", 1, 0.0, "hit", "Judah shows Jacob the coat"),
    ("s07_jacob", "cloth", "雅各以为", 0, 0.0, "hit", "Jacob takes the coat and sinks down"),
    ("s08_egypt", "thud", "在埃及", 0, 0.0, "hit", "the grain sack drops on the pile (咚)"),
    ("s08_egypt", "coins", "约瑟做事很认真", 0, 0.0, "hit", "the master gives him the keys"),
    ("s08_egypt", "coins", "约瑟做事很认真", 1, 0.0, "hit", "he holds the keys up (jingle)"),
    ("s08_egypt", "coins", "后来，约瑟被人冤枉", 0, 0.0, "hit", "the keys fall (clink)"),
    ("s08_egypt", "thud", "后来，约瑟被人冤枉", 0, 0.0, "hit", "the prison gate clangs shut"),
    ("s09_prison", "pop", "在监牢里", 0, 0.0, "hit", "the cupbearer's dream bubble"),
    ("s09_prison", "pop", "在监牢里", 1, 0.0, "hit", "the baker's dream bubble"),
    ("s09_prison", "sparkle", "在监牢里", 0, 0.0, "hit", "it all came true (the sunny bubble)"),
    ("s10_pharaoh", "chime", None, 0, 0.0, "hit", "the dream bubble blooms"),
    ("s10_pharaoh", "gulp", None, 0, 0.0, "hit", "gulp 1 ('吃掉了')"),
    ("s10_pharaoh", "gulp", None, 1, 0.0, "hit", "gulp 2"),
    ("s10_pharaoh", "gulp", None, 2, 0.0, "hit", "gulp 3"),
    ("s10_pharaoh", "gulp", None, 3, 0.0, "hit", "gulp 4"),
    ("s10_pharaoh", "cloth", "没有人能解", 0, 0.0, "hit", "the first wise man shrugs"),
    ("s10_pharaoh", "sparkle", "没有人能解", 0, 0.0, "hit", "the cupbearer's idea (a gold star)"),
    ("s10_pharaoh", "sparkle", "上帝告诉你", 0, 0.0, "hit", "the golden fields glint ('七年大丰收')"),
    ("s10_pharaoh", "sparkle", "上帝告诉你", 1, 0.0, "hit", "the golden row glows ('要趁丰收的时候')"),
    ("s10_pharaoh", "thud", "上帝告诉你", 0, 0.0, "hit", "sack 1 lands in the granary"),
    ("s10_pharaoh", "thud", "上帝告诉你", 1, 0.0, "hit", "sack 2 lands in the granary"),
    ("s11_ruler", "sparkle", "上帝和你同在", 0, 0.0, "hit", "the ring's glint ('管理全埃及')"),
    ("s11_ruler", "sparkle", "约瑟穿上了", 0, 0.0, "hit", "the robes (sparkle burst)"),
    ("s11_ruler", "sparkle", "约瑟穿上了", 1, 0.0, "hit", "the gold chain's twinkle"),
    ("s11_ruler", "thud", "约瑟穿上了", 0, 0.0, "hit", "Joseph lands in the chariot"),
    ("s11_ruler", "horn", "约瑟穿上了", 0, 0.1, "hit", "the horse sets off with the herald's horn: the processional"),
    ("s11_ruler", "sparkle", "七年丰收", 0, 0.0, "hit", "the top of the grain mountain glints"),
    ("s12_brothers", "thud", "后来，饥荒来了", 0, 0.0, "hit", "the empty grain jar topples"),
    ("s12_brothers", "thud", "他们向约瑟跪下", 0, 0.0, "hit", "they kneel (1)"),
    ("s12_brothers", "thud", "他们向约瑟跪下", 1, 0.0, "hit", "they kneel (2)"),
    ("s12_brothers", "pop", "他们向约瑟跪下", 0, 0.0, "hit", "Joseph knows them (a start)"),
    ("s12_brothers", "chime", "小朋友，你还记得", 0, 0.0, "hit", "the dream bubble rises"),
    ("s12_brothers", "grow", "小朋友，你还记得", 0, 0.0, "hit", "Joseph's sheaf stands up and glows"),
    ("s12_brothers", "sparkle", "小朋友，你还记得", 0, 0.0, "hit", "the sheaves bow"),
    ("s12_brothers", "sparkle", "小朋友，你还记得", 1, 0.0, "hit", "it really happened: the glow (twinkles)"),
    ("s13_forgive", "whoosh", "我就是约瑟", 0, 0.0, "hit", "the headcloth flies off ('我就是约瑟')"),
    ("s13_forgive", "thud", "哥哥们吓坏了", 0, 0.0, "hit", "the brothers jump back, scared"),
    ("s13_forgive", "cloth", "约瑟抱住哥哥们", 0, 0.0, "hit", "he hugs Judah"),
    ("s13_forgive", "cloth", "约瑟抱住哥哥们", 1, 0.0, "hit", "he hugs the next brother"),
    ("s13_forgive", "chime", "约瑟抱住哥哥们", 0, 0.0, "hit", "Joseph and Jacob hug"),
    ("s13_forgive", "sparkle", "约瑟抱住哥哥们", 0, 0.0, "hit", "the family together (twinkles)"),
    ("s14_end", "pop", "约瑟被卖", 0, 0.0, "hit", "panel 1 pops onto the string ('被卖')"),
    ("s14_end", "pop", "约瑟被卖", 1, 0.0, "hit", "panel 2 ('被冤枉')"),
    ("s14_end", "pop", "约瑟被卖", 2, 0.0, "hit", "panel 3 ('被关进监牢')"),
    ("s14_end", "chime", "约瑟被卖", 0, 0.0, "hit", "the golden light in the panels"),
    ("s14_end", "sparkle", "上帝可以", 0, 0.0, "hit", "they hug: the cloud turns sunny"),
    ("s14_end", "chime", "上帝可以", 0, 0.0, "hit", "the picture of Joseph and his brother glows up"),
    ("s14_end", "sparkle", "上帝可以", 1, 0.0, "hit", "she shares the toy horse"),
    ("s14_end", "chime", "上帝可以", 1, 0.0, "hit", "the end card"),
]
