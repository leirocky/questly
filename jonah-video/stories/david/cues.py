"""The background score for 大卫和歌利亚 (1 Samuel 17, ~5:53) -- one continuous piece in 14 cues.

Read by audio/score.py when the story is "david" (SCENE_CUES); REQUIRED_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework and orchestra as the Jonah and Daniel scores
(audio/scorekit.py, audio/scorelib.py): every cue starts at its scene's global start, is planned in whole
bars whose tempo follows the real line timings, and is keyed to narration phrases (Cue.find / Cue.at /
Cue.gap), never to fixed times.  Hits that show an on-screen action -- the giant's footfalls (s02, s04, s07,
s12), the armour's 哐当 (s09), the stones dropping into the bag (s10), and the helmet/sword clanks, glints, the
log, the sling's test swings -- follow the PICTURE: picture() reads the scene's own sound-effect cues at build
time (engine.loader.build_scene(...).sfx_cues, the same source as music_check's PICTURE_HITS), so they move when
a scene is edited; the narration phrase then marks where the harmony arrives (a 'change' in REQUIRED_HITS).
Without a scene that builds, those hits fall back to the narrator's own voice: voice_times() reads the recorded
line (its pause-separated voice islands matched to the punctuation groups of the text; character interpolation
if the clip is missing or does not match).  group_times() keeps a phrase's Cue.at anchor with the narrator's
spacing ('转啊转，转啊转', '早上喊，晚上喊').

Themes
  David, the shepherd boy (G major, 4/4; a pipe tune -- flute or clarinet over plucked harp; motif x = the
  bouncing 3-5-3-1-5 'B D B G D', motif y = the rising answer 'E G E' that reaches up a step each time):
     b1 G        B4 D5 B4 G4 D5          b5 G        B4 D5 B4 G4 D5
     b2 C  G     E5 G5 E5 D5 B4          b6 C  G     E5 G5 E5 D5 G5
     b3 Am D7    C5 E5 C5 A4 C5          b7 C  D7    E5 G5 E5 F#5 A5
     b4 G  D     B4 G4 A4--              b8 G        G5---
  Goliath (G minor -- the same G, the other mode; tuba and bassoon in unison, big timpani / bass-drum stomps,
     heavy but a little comic):  Gm  G2 G2 Bb2 A2 G2 | D  F#2 G2 A2 D2 | Gm  G2 G2 Bb2 C3 D3 | Cm D  Eb3 C3 D3
  Israel's fear (E minor): tremolo strings, a clarinet shiver (the top chord tone trembling with its upper
     neighbour) and knocking knees (two woodblocks).
  The armour: comic clanks (woodblocks + low pizzicato + bassoon) as the helmet, the mail and the sword go on
     and on each 哐当, a wobbly chromatic bassoon on '哎呀，太重了'.
  The stones: five plucks counting up G-A-B-C-D (pizzicato + harp, glockenspiel on the fifth) over a falling
     bass G-F#-E-C-D, home to G on '都放进口袋里'.
  The sling: a circling harp/flute whirl rising on '转啊转' (3/4, a beat for every turn of the strap on the
     picture; suspended cymbal swelling), the whoosh on '嗖'
     (harp glissando, flute run, plucked chord), a 'bonk' on '正好打中' (woodblock, glockenspiel, timpani,
     celesta stars), the giant's fall (tuba + bassoon sliding down chromatically D3 -> A2) and the big low
     hit on '咚！巨人扑倒' (timpani, bass drum, tuba, plucked basses on G).

Tonal plan
  s01 title G (David b1-b2, flute; a far-off soft double timpani step and a glint) -> s02 G, the question
  (clarinet, harp, a soft thunder roll on the picture's thunder) | E minor fear (tremolo, shiver, knees) |
  G minor on '是一个巨人' and the giant's two footfalls -> s03 E minor horn call 'long ago' | G major on
  Israel's hill | Eb (a trombone chord), then G minor with Goliath's head, on '非利士人站在那边' | D, the
  valley with its brook (V of G minor) -> s04 G minor camp (tremolo, timpani growing, his approaching steps)
  | G minor on '咚！咚！咚！' and the three stomps on the picture | Goliath's theme b1-b2 (a
  clarinet run up on '好高好高') | b3-b4 with brass clanks on the bronze helmet and armour, a wooden thunk on
  '大木头' | his challenge (sparse: timpani steps, soft tremolo) | E minor fear | '连扫罗王': a drooping
  bassoon, half cadence on D -> s05 the day counter: G morning (flute bird), G minor shout (tuba) | E minor
  evening, G minor shout | morning, evening, forty days (G / E minor, tuba honks) | E minor 'nobody dared',
  ii-V into G -> s06 Bethlehem: David's theme b1-b4 (flute, harp) | father Jesse: b5-b8 on the horn over dark,
  soft strings (his voice is dull in the 1-4 kHz band, so the music under it stays dark and soft) | walking
  pizzicato and the oboe | a harp sweep on '出发了' -> s07 arrival (b1, clarinet) darkening to Eb-D |
  Goliath's shout (hit, his theme) | the soldiers run (G melodic-minor scurry) | David asks (b1 + b7, a
  question on D7) | Eliab cross (E minor, grumpy bassoon) | David's simple answer (harp and strings only) ->
  s08 Saul's tent (E minor horn, timpani) | David brave (b1-b2, horn) | '你？' a plucked double take, Goliath
  on the tuba | the lion (G minor pizzicato pounce) | the bear (Eb waddle) | the rescue (running cellos, b1 +
  b7) | faith (b5 b7 b8, horn, choir) | Saul's blessing (plagal C-G, harp) -> s09 the fitting (a little march)
  | clanks on the three pieces | the first steps | 哐当 哐当 | '哎呀': the wobble down onto D7 | '这些我穿不惯'
  (bassoon) | free again (b1, flute, harp sweep) -> s10 the brook (harp ripples) | the counting | the sling
  (circling harp) | '又快又远': a flute run up and a harp sweep on D -> s11 G minor: Goliath sees him | the
  laugh on '哈哈大笑' (ho-ho-hooo) | his mockery (theme) | David answers (b1, horn, G major) | '万军之耶和华'
  (choir) | the build (b5 and b7 on the horn, choir, a held D with a timpani roll; soft under David's words) ->
  s12 Goliath walks (G minor stomps) | David runs (G major, b1 + b7) | the stone in the sling (D pedal) |
  '转啊转' the whirl (G C D D7) | '嗖' | '正好打中' bonk + the fall over D7 | '咚！' the big low G minor hit,
  dust settling -> s13 the Philistines see (deflated bassoon) | they flee (scurry onto D7) | '欢呼' David's
  theme in full (brass, violins, horn, choir 'ah', timpani, glockenspiel; G major -- under the narration, so
  bright rather than loud) -> s14 under the stars: David's theme slow (flute, harp, celesta) | the question
  (Em C Dsus4; the 2 s pause after it keeps only the soft Dsus4) | b5-b7 warm (clarinet, horn, strings,
  choir) | the final G major chord on '和我在一起', ringing to the end.

All the music stays under the narration (Seg.duck, low expression levels); the loud moments are short and
child-safe (comic stomps and bonks, no stingers; the fall is a cartoon slide, the big 咚 a warm low thud).
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
    timp_roll,
)
from audio.theory import midi

# ------------------------------------------------------------------------------------------- themes
DAVID = ["B4:1 D5:1/2 B4:1/2 G4:1 D5:1", "E5:1 G5:1/2 E5:1/2 D5:1 B4:1", "C5:1 E5:1/2 C5:1/2 A4:1 C5:1",
         "B4:1 G4:1 A4:2", "B4:1 D5:1/2 B4:1/2 G4:1 D5:1", "E5:1 G5:1/2 E5:1/2 D5:1 G5:1",
         "E5:1 G5:1/2 E5:1/2 F#5:1 A5:1", "G5:4"]
DAVID_PROG = ["G:4", "C:2 G:2", "Am:2 D7:2", "G:2 D:2", "G:4", "C:2 G:2", "C:2 D7:2", "G:4"]

GOLIATH = ["G2:1 G2:1 Bb2:1 A2:1/2 G2:1/2", "F#2:1 G2:1/2 A2:1/2 D2:2", "G2:1 G2:1 Bb2:1 C3:1/2 D3:1/2",
           "Eb3:1 C3:1 D3:2"]
GOLIATH_PROG = ["Gm:4", "D:4", "Gm:4", "Cm:2 D:2"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- narration timing
PUNCT = "，。！？：；、…"
_ISLANDS = {}


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


def _voice_islands(wav, n_groups):
    """Onsets (s into the clip) of its pause-separated voice islands, for the widest pause threshold that
    yields exactly n_groups islands (None if none does or the clip is missing)."""
    key = (str(wav), n_groups)
    if key in _ISLANDS:
        return _ISLANDS[key]
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
                runs.append([i, j])
                i = j
            else:
                i += 1
        for gap in (0.25, 0.2, 0.16, 0.12, 0.09, 0.07, 0.05, 0.04, 0.03, 0.02):
            merged = []
            for a, b in runs:
                if merged and (a - merged[-1][1]) * 0.01 < gap:
                    merged[-1][1] = b
                else:
                    merged.append([a, b])
            merged = [r for r in merged if (r[1] - r[0]) * 0.01 >= 0.05]
            if len(merged) == n_groups:
                out = [a * 0.01 for a, _ in merged], n * hop / sr
                break
    except Exception:
        out = None
    _ISLANDS[key] = out
    return out


def group_times(c, phrase, n):
    """Cue-relative times of the n punctuation groups of the narration that start where `phrase` starts
    (e.g. '咚！咚！咚！' -> the three 咚).  The first is Cue.at(phrase), the anchor every hit point uses; the
    spacing of the others is the narrator's own, read from the recorded clip (voice islands matched to the
    text's groups) -- or, without a usable clip, the subtitle-chunk character interpolation."""
    from engine.paths import BUILD

    i = c.find(phrase)
    ln = c.scene["lines"][i]
    t0 = c.at(phrase)
    grp = _groups(ln["text"])
    k0 = ln["text"].index(phrase)
    g0 = max(k for k, (p, _) in enumerate(grp) if p <= k0)
    n = min(n, len(grp) - g0)
    isl = _voice_islands(BUILD / ln["wav"], len(grp)) if ln.get("wav") else None
    if isl is not None:
        onsets, clip = isl
        scale = (ln["end"] - ln["start"]) / clip
        return [t0 + (onsets[g0 + k] - onsets[g0]) * scale for k in range(n)]
    base = _char_time(ln, grp[g0][0])
    return [t0 + _char_time(ln, grp[g0 + k][0]) - base for k in range(n)]


def voice_times(c, phrase, n):
    """Cue-relative onsets of the n punctuation groups starting at `phrase` as the narrator actually speaks them
    (the clip's voice islands); the subtitle-chunk interpolation without a usable clip."""
    from engine.paths import BUILD

    ln = c.scene["lines"][c.find(phrase)]
    grp = _groups(ln["text"])
    k0 = ln["text"].index(phrase)
    g0 = max(k for k, (p, _) in enumerate(grp) if p <= k0)
    n = min(n, len(grp) - g0)
    isl = _voice_islands(BUILD / ln["wav"], len(grp)) if ln.get("wav") else None
    if isl is not None:
        onsets, clip = isl
        scale = (ln["end"] - ln["start"]) / clip
        return [ln["start"] + onsets[g0 + k] * scale for k in range(n)]
    return [_char_time(ln, grp[g0 + k][0]) for k in range(n)]


_PICTURE = {}


def picture(c, name, t0=-1e9, t1=1e9):
    """Cue-relative times of this scene's own sound-effect cues called `name` between t0 and t1.  The scene
    authors key them to the animation (footfalls, clanks, the stones dropping into the bag...), so a hit that
    shows an action follows the PICTURE: read at build time from the scene code, as music_check reads
    PICTURE_HITS.  None when the scene does not build (the caller then falls back to the narration)."""
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


def seg_at(c, segs, t):
    """(segment, q) of cue-relative time t among segs (a hit that lands in a neighbouring segment takes its chord)."""
    for sg in segs:
        if sg.t0 - 1e-6 <= c.t0 + t < sg.t1 - 1e-6:
            return sg, min(max(sg.q_of(c.t0 + t), 0.0), sg.n_q - 0.1)
    sg = segs[0] if c.t0 + t < segs[0].t0 else segs[-1]
    return sg, (0.0 if sg is segs[0] and c.t0 + t < sg.t0 else sg.n_q - 0.1)


def on_picture(c, name, t0, t1, n, fallback):
    """The first n picture cues `name` in [t0, t1] if the scene shows at least n of them, else fallback()."""
    ts = picture(c, name, t0, t1)
    return ts[:n] if ts is not None and len(ts) >= n else list(fallback())[:n]


# ------------------------------------------------------------------------------------------- helpers
def strings(seg, vel=44, lo=53, hi=72, bass=(40, 51), q0=0.0, q1=None, cb=(28, 39), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vln2", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
            bass_hi=bass[1])
    if cb:
        bassline(seg, "cb", cb[0], cb[1], cb_vel or vel - 2, q0=q0, q1=q1)


def _dq(seg, q, dq):
    """dq, shortened so the note ends with its chord."""
    return max(0.1, min(dq, span_end(seg, q + 1e-6) - q, seg.n_q - q))


def stomp(seg, q, vel=66, bass=None, kit=True, timp=True):
    """A giant's step: timpani and plucked basses on the chord's bass (or `bass`), a concert bass drum."""
    ch = seg.chord_at(q + 1e-3)
    b = midi(bass) if isinstance(bass, str) else (bass or ch.bass_note(28, 40))
    if timp:
        seg.add("timp", q, _dq(seg, q, 0.5), timp_pitch(ch, midi("G2")), vel, "timp", "h")
    seg.add("pz_cb", q, _dq(seg, q, 0.5), b, vel - 2, "bass", "h")
    if kit:
        seg.add("okit", q, 1, 36, vel - 8, "perc", "h")


def clank(seg, q, vel=64, low=True, ting=False):
    """Comic armour clank: two woodblocks at once, a low pluck, optionally a glockenspiel 'ting'."""
    ch = seg.chord_at(q + 1e-3)
    drum(seg, q, 76, vel)
    drum(seg, q, 77, vel - 6)
    if low:
        seg.add("pz_lo", q, _dq(seg, q, 0.5), ch.bass_note(40, 51), vel - 4, "bass", "h")
    if ting:
        seg.add("glock", q, _dq(seg, q, 0.5), max(ch.tones(84, 96)), vel - 10, "arp", "h")


def pluck_chord(seg, q, vel=60, lo=55, hi=67, part="pz_hi"):
    ch = seg.chord_at(q + 1e-3)
    for k, p in enumerate(ch.tones(lo, hi)[:3]):
        seg.add(part, q, _dq(seg, q, 0.5), p, vel, "harmony", "h", voice=f"{part}.{k}")


def knees(seg, q0, q1, vel=40, step=0.5):
    """Knocking knees: two woodblocks alternating softly."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        drum(seg, q, 76 if k % 2 == 0 else 77, vel - (4 if k % 2 else 0))
        q += step
        k += 1


def shiver(seg, part, q0, q1, lo, hi, vel=52):
    """A trembling figure: the chord's top tone and its upper neighbour in sixteenths (one shiver per beat,
    the neighbour never on a strong beat)."""
    q = q0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-3)
        p = max(ch.tones(lo, hi))
        up = p + 1 if (p + 1) in seg.scale else p + 2
        for k, pp in enumerate((p, up, p, up)):
            seg.add(part, q + 0.25 * k, 0.25, pp, vel - (6 if k % 2 else 0), "melody", "s")
        q += 1.0


def ripple(seg, q0, q1, lo=55, hi=79, vel=40, step=0.25, part="harp"):
    """The brook: harp sixteenths rippling up and down the chord."""
    broken(seg, part, q0, q1, (0, 2, 4, 3, 5, 4, 2, 1), lo, hi, vel=vel, step=step, accent=4, thin=True)


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """David's theme b1-b2 on the flute over harp and soft strings (G major); far off, two soft timpani steps."""
    c.gain(-5.0)
    s = c.seg(0, c.dur, 2, "4/4", "G major", nominal=96, label="title")
    s.duck(1.0)
    s.prog(" | ".join(DAVID_PROG[:2]))
    s.mel("flute", bars(DAVID, 0, 2), vel=62)
    broken(s, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 43, 55, vel=42)
    s.pad(["vla", "vln2", "vln1"], 3, 55, 71, vel=46, bass_part="vc", bass_lo=43, bass_hi=55)
    s.add("cb", 0, 8, "G1", 40, "bass")
    s.add("timp", 6, 0.5, "G2", 34, "timp", "h")          # the far-off helmet: two soft steps
    s.add("timp", 7, 0.5, "G2", 30, "timp", "h")
    glint = picture(c, "sparkle", 1.0, c.dur - 1.0)        # ...and its glint (on the picture's sparkle)
    q_gl = min(max(s.q_of(c.t0 + glint[0]), 4.0), 7.0) if glint else 6.5
    s.add("glock", q_gl, _dq(s, q_gl, 1.0), "G6", 40, "arp", "r")         # G: in both the C and the G chord
    s.expr(["flute"], [(0, -9), (8, -10)])
    s.expr(["harp"], [(0, -8), (8, -9)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (1, -12), (8, -12)])
    s.expr(["timp", "glock"], [(0, -10), (8, -10)])


def afraid(c):
    """The question to the child (G major, clarinet, harp; a soft thunder roll on '打雷'); a crowd of frightened
    people (E minor: tremolo, a clarinet shiver, knocking knees); the giant (G minor on '是一个巨人', his two
    footfalls on the picture)."""
    c.gain(-1.6)
    t_g = c.gap(c.find("今天的故事里"))
    t_j = c.at("是一个巨人")
    t_th = on_picture(c, "thunder", 0, c.le(0), 1, lambda: [c.at("打雷")])[0]
    steps = on_picture(c, "thud", t_j - 0.3, c.dur - 0.15, 2, lambda: [c.at("巨人"), c.at("巨人") + 0.4])
    a = c.seg(0, t_g, 2, "4/4", "G major", nominal=70, label="afraid-question")
    b = c.seg(t_g, t_j, 2, "4/4", "E minor+", nominal=84, label="afraid-crowd")
    j = c.seg(t_j, c.dur, 1, "2/4", "G minor", nominal=76, label="afraid-giant")
    for sg in (a, b, j):
        sg.duck(1.5)
    a.prog("G:2 Em:2 | Am:2 D:2")
    b.prog("Em:4 | C:2 D:2")
    j.prog("Gm:2")
    j.sync("'是一个巨人': G minor (the giant)", 0, t_j, kind="change")
    # 'have you ever been afraid? of thunder, of a dark room?'
    a.mel("clar", "D5:1 B4:1 G4:1 B4:1 | A4:1 C5:1 D5:2", vel=58)
    broken(a, "harp", 0, 8, (0, 2, 4, 2), 43, 55, vel=38, thin=True)
    a.pad(["vla", "vln2"], 2, 55, 69, vel=42, bass_part="vc", bass_lo=40, bass_hi=52)
    q_th = min(max(a.q_of(c.t0 + t_th), 0.5), 6.0)
    timp_roll(a, q_th, q_th + 1.5, midi("A2"), 22, 34)
    a.duck(2.5, parts=["clar", "harp"])
    a.expr(["clar"], [(0, -12), (8, -12)])
    a.expr(["harp"], [(0, -9), (8, -10)])
    a.expr(["vla", "vln2", "vc"], [(0, -16), (1, -13), (8, -13)])
    a.expr(["timp"], [(0, -12), (8, -12)])
    # 'a whole crowd of people, all terribly afraid': tremolo, the shiver, knocking knees
    b.pad(["trem_va", "trem_va", "trem_hi"], 3, 48, 69, vel=48, bass_ref=(40, 52))
    b.mel("cb", "E2:4 | C2:2 D2:2", vel=42, role="bass")
    shiver(b, "clar", 1, 7, 70, 76, vel=54)
    knees(b, 0.5, 7.5, vel=36)
    b.expr(["trem_va", "cb"], [(0, -18), (2, -14), (8, -13)])
    b.expr(["clar"], [(0, -13), (8, -13)])
    b.expr("hand", [(0, -12), (8, -12)])
    # 'what they feared was a giant!': G minor; the giant's two footfalls on the picture (timpani, bass drum,
    # tuba and plucked basses on G)
    for i_, t in enumerate(steps):
        sg, q = seg_at(c, (b, j), t)
        stomp(sg, q, vel=62 + 3 * i_)
        sg.add("tuba", q, _dq(sg, q, 0.5), sg.chord_at(q + 1e-3).bass_note(28, 40), 54 + 2 * i_, "bass", "h")
        sg.sync(f"the giant's footfall {i_ + 1}", q, t)
    j.add("bsn", 0, 2, "Bb2", 48, "harmony")
    j.pad(["trem_va", "trem_va"], 2, 48, 64, vel=44, bass_ref=(31, 43))
    j.add("cb", 0, 2, "G1", 44, "bass")
    j.expr(["tuba", "timp", "pz_cb"], [(0, -8), (2, -9)])
    j.expr(["bsn"], [(0, -12), (2, -14)])
    j.expr(["trem_va", "cb"], [(0, -12), (2, -15)])


def valley(c):
    """'Long ago' (E minor horn call over timpani); Israel's hill (G major); the Philistines' hill (G minor,
    Goliath's head on the tuba) on '非利士人站在那边'; the valley between (D, a brook in the harp)."""
    c.gain(-3.6)
    t_i = c.at("以色列人站在这边")
    t_p = c.at("非利士人站在那边")
    t_v = c.at("中间隔着")
    a = c.seg(0, t_i, 2, "4/4", "E minor", nominal=86, label="valley-long-ago")
    b = c.seg(t_i, t_p, 1, "4/4", "G major", nominal=116, label="valley-israel")
    p = c.seg(t_p, t_v, 1, "4/4", "G minor", nominal=88, label="valley-philistines")
    v = c.seg(t_v, c.dur, 1, "2/4", "D major", nominal=62, label="valley-brook")
    for sg in (a, b, p, v):
        sg.duck(1.5)
    a.prog("Em:4 | C:2 D:2")
    b.prog("G:4")
    p.prog("Eb:2 Gm:2")
    v.prog("D:2")
    p.sync("the Philistines' hill: E-flat, G minor ('非利士人站在那边')", 0, t_p, kind="change")
    # long ago, Israel and the Philistines were about to go to war: a horn call over soft timpani
    a.mel("horn", "E3:1 B3:1 E4:2 | E4:1 G4:1 F#4:2", vel=58)
    a.pad(["vla", "vln2"], 2, 52, 67, vel=42, bass_part="vc", bass_lo=36, bass_hi=48)
    a.mel("cb", "E2:4 | C2:2 D2:2", vel=42, role="bass")
    for q, nm in ((0, "E2"), (2, "B2"), (4, "C3"), (6, "D3")):
        a.add("timp", q, 0.5, nm, 38, "timp")
    a.duck(2.5, parts=["horn"])
    a.expr(["horn"], [(0, -11), (8, -11)])
    a.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (8, -13)])
    a.expr(["timp"], [(0, -12), (8, -12)])
    # the Israelites on this hill: G major, bright (flute, plucked strings)
    b.mel("flute", "D5:1/2 G5:1/2 B5:1 G5:2", vel=56)
    b.pad(["vla", "vln2"], 2, 55, 71, vel=44, bass_part="vc", bass_lo=43, bass_hi=55)
    b.add("cb", 0, 4, "G2", 42, "bass")
    pluck_chord(b, 0, vel=50)
    b.expr(["flute"], [(0, -11), (4, -11)])
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (4, -13)])
    # the Philistines on that hill: G minor, Goliath's head motif (tuba + bassoon), low strings
    p.mel("tuba", GOLIATH[0], vel=56)
    p.mel("bsn", GOLIATH[0], vel=54)
    p.pad(["vla", "vln2"], 2, 55, 70, vel=44, bass_part="vc", bass_lo=36, bass_hi=48)
    p.mel("cb", "Eb2:2 G2:2", vel=42, role="bass")
    p.add("timp", 0, 0.5, "G2", 40, "timp", "h")
    for k_, nm in enumerate(["Eb3", "G3", "Bb3"]):
        p.add("tbn", 0, 2, nm, 50, "pad", voice=f"tbn.{k_}")
    p.expr(["tbn"], [(0, -10), (2, -14)])
    p.expr(["tuba", "bsn"], [(0, -10), (4, -10)])
    p.expr(["vla", "vln2", "vln1", "vc", "cb", "timp"], [(0, -13), (4, -13)])
    # a valley in between, a little brook: D (the giant's dominant), harp ripples
    ripple(v, 0, 2, 50, 74, vel=36)
    v.pad(["vla", "vln2"], 2, 54, 69, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    v.add("cb", 0, 2, "D3", 40, "bass")
    v.expr(["harp"], [(0, -9), (2, -11)])
    v.expr(["vla", "vln2", "vc", "cb"], [(0, -13), (2, -15)])


def giant(c):
    """The Philistine camp (G minor, low tremolo, timpani growing); the three stomps on '咚！咚！咚！';
    Goliath's theme (b1-b2, a clarinet run up on '好高好高'); b3-b4 with bronze clanks; his challenge (sparse
    steps); Israel's fear (E minor); '连扫罗王' -- a drooping bassoon, half cadence on D."""
    c.gain(-1.0)
    t_dong = c.at("咚！咚！咚！")
    t_n = c.gap(c.find("他的名字叫歌利亚"))
    t_m = c.gap(c.find("他戴着铜头盔"))
    t_g = c.gap(c.find("以色列人听着"))
    t_f = c.gap(c.find("以色列人听了"))
    t_k = c.at("连扫罗王")
    # the three stomps and Goliath's approaching steps follow the picture (the scene's thuds); without it,
    # the stomps sit on the spoken 咚s
    t_st = on_picture(c, "thud", t_dong - 0.3, c.le(0) + 0.3, 3, lambda: voice_times(c, "咚！咚！咚！", 3))
    approach = picture(c, "thud", c.ls(0) - 0.3, t_dong - 0.3) or []
    a = c.seg(0, t_dong, 2, "4/4", "G minor", nominal=104, label="giant-camp")
    s = c.seg(t_dong, t_n, 1, "4/4", "G minor", nominal=128, label="giant-stomps")
    n = c.seg(t_n, t_m, 2, "4/4", "G minor+", nominal=70, label="giant-name")
    n.gain(-1.5)
    m = c.seg(t_m, t_g, 2, "4/4", "G minor+", nominal=70, label="giant-armour")
    m.gain(-1.0)
    g = c.seg(t_g, t_f, 3, "4/4", "G minor+", nominal=66, label="giant-challenge")
    f = c.seg(t_f, t_k, 2, "4/4", "E minor+", nominal=132, label="giant-fear")
    k = c.seg(t_k, c.dur, 1, "4/4", "G major", nominal=86, label="giant-saul")
    for sg in (a, s, n, m, g, f, k):
        sg.duck(1.5)
    a.prog("Gm:4 | Eb:2 D:2")
    s.prog("Gm:4")
    n.prog(" | ".join(GOLIATH_PROG[:2]))
    m.prog(" | ".join(GOLIATH_PROG[2:4]))
    g.prog("Gm:4 | Eb:4 | Cm:2 D:2")
    f.prog("Em:4 | Em:2 B7:2")
    k.prog("C:2 D:2")
    # out of the Philistine camp came a man...: tremolo, his footsteps coming closer (plucked basses, a soft
    # bass drum -- on the picture's steps, else a plod), the timpani growing into the dominant
    a.pad(["trem_va", "trem_va", "trem_hi"], 3, 48, 67, vel=48, bass_ref=(31, 43))
    if approach:
        for i_, t in enumerate(approach):
            sg, q = seg_at(c, (a, s), t)
            stomp(sg, q, vel=48 + 3 * i_, timp=False)
    else:
        a.mel("pz_cb", "G1:1 r:1 G1:1 r:1 | Eb2:1 r:1 D2:1 r:1", vel=58, role="bass")
    timp_roll(a, 4, 7.9, midi("D2"), 24, 46)
    a.expr(["trem_va"], [(0, -18), (4, -14), (8, -12)])
    a.expr(["pz_cb", "timp", "okit"], [(0, -9), (8, -9)])
    # 咚！咚！咚！ -- G minor as he steps out, and three giant stomps
    s.sync("'咚！咚！咚！': G minor (Goliath steps out)", 0, t_dong, kind="change")
    s.add("bsn", 0, 4, "Bb2", 46, "harmony")
    for i_, t in enumerate(t_st):
        sg, q = seg_at(c, (a, s, n), t)
        stomp(sg, q, vel=60 + 3 * i_)
        sg.add("tuba", q, _dq(sg, q, 0.5), sg.chord_at(q + 1e-3).bass_note(28, 40), 54 + 2 * i_, "bass", "h")
        sg.sync(f"stomp {i_ + 1} ('咚')", q, t)
    s.expr(["bsn"], [(0, -13), (4, -14)])
    s.pad(["trem_va", "trem_va"], 2, 48, 64, vel=44, bass_ref=(31, 43))
    s.add("cb", 0, 4, "G1", 42, "bass")
    s.expr(["trem_va", "cb"], [(0, -13), (4, -13)])
    s.expr(["timp", "pz_cb", "tuba"], [(0, -6), (4, -6)])
    # his name was Goliath, so tall, so tall: Goliath's theme b1-b2 (tuba + bassoon), soft steps; the clarinet
    # climbs on '好高好高'
    n.mel("tuba", bars(GOLIATH, 0, 2), vel=60)
    n.mel("bsn", bars(GOLIATH, 0, 2), vel=58)
    n.add("cb", 0, 4, "G1", 42, "bass")
    for q in (0, 2, 4, 6):
        n.add("timp", q, 0.5, "G2" if q < 4 else "D2", 42 if q % 4 == 0 else 36, "timp")
    n.pad(["vla", "vln2"], 2, 50, 65, vel=40, bass_ref=(31, 43))
    t_tall = c.at("好高好高")
    q_tall = min(max(round(n.q_of(c.t0 + t_tall) * 2) / 2, 0.0), 2.0)
    n.mel("clar", "G4:1/4 A4:1/4 Bb4:1/4 C5:1/4 D5:1/4 Eb5:1/4 F5:1/4 G5:1/4", q=q_tall, vel=50, art="s")
    n.duck(2.0, parts=["tuba", "bsn", "clar"])
    n.expr(["tuba", "bsn"], [(0, -14), (1, -10), (8, -10)])
    n.expr(["clar"], [(0, -12), (8, -12)])
    n.expr(["cb", "timp", "vla", "vln2"], [(0, -13), (8, -13)])
    # a bronze helmet, bronze armour, a spear as thick as a log: b3-b4, brass clanks, a wooden thunk
    m.mel("tuba", bars(GOLIATH, 2, 4), vel=60)
    m.mel("bsn", bars(GOLIATH, 2, 4), vel=58)
    m.mel("cb", "G1:4 | C2:2 r:2", vel=42, role="bass")
    for part, spec in (("vla", "G3:4 | G3:2 F#3:2"), ("vln2", "Bb3:4 | C4:2 A3:2")):
        m.mel(part, spec, vel=40, role="pad")
    glints = on_picture(c, "sparkle", c.ls(2) - 0.3, c.le(2), 2, lambda: [c.at("铜头盔"), c.at("铜盔甲")])
    for t in glints:                                # the helmet and the armour glint on the picture
        q = min(m.q_of(c.t0 + t), m.n_q - 0.5)
        ch = m.chord_at(q + 1e-3)
        for k_, p_ in enumerate(ch.tones(52, 64)[:3]):
            m.add("tbn", q, _dq(m, q, 0.5), p_, 56, "harmony", "h", voice=f"tbn.{k_}")
        m.add("glock", q, _dq(m, q, 0.5), max(ch.tones(84, 96)), 44, "arp", "h")
    t_log = on_picture(c, "pop", c.at("粗得像") - 0.3, c.le(2) + 0.3, 1, lambda: [c.at("大木头")])[0]
    q_log = min(m.q_of(c.t0 + t_log), m.n_q - 0.5)
    drum(m, q_log, 77, 56)
    m.add("pz_cb", q_log, _dq(m, q_log, 0.5), m.chord_at(q_log + 1e-3).bass_note(28, 40), 56, "bass", "h")
    m.duck(3.0, parts=["tuba", "bsn"])
    m.expr(["tuba", "bsn"], [(0, -12), (8, -12)])
    m.expr(["tbn", "glock"], [(0, -11), (8, -11)])
    m.expr(["cb", "vla", "vln2", "pz_cb"], [(0, -13), (8, -13)])
    # 'Israel, listen! Send a man out to fight me!...': under his big voice only the giant's slow steps
    for q in range(0, 12, 4):
        stomp(g, q, vel=50, kit=q % 8 == 0)
    g.pad(["trem_va", "trem_hi"], 2, 55, 72, vel=40, bass_ref=(31, 43))
    g.mel("cb", "G1:4 | Eb2:4 | C2:2 D2:2", vel=40, role="bass")
    g.mel("tuba", "r:4 | r:4 | r:2 D2:2", vel=48, role="counter")
    g.expr(["trem_va", "trem_hi", "cb"], [(0, -18), (12, -16)])
    g.expr(["timp", "pz_cb", "tuba"], [(0, -12), (12, -12)])
    # the Israelites' legs went weak: E minor tremolo, the clarinet's shiver, knocking knees
    f.sync("Israel's fear (E minor)", 0, t_f, kind="change")
    f.pad(["trem_va", "trem_va", "trem_hi"], 3, 48, 69, vel=48, bass_ref=(40, 52))
    f.mel("cb", "E2:4 | E2:2 B1:2", vel=42, role="bass")
    shiver(f, "clar", 0, 8, 70, 76, vel=54)
    knees(f, 0.5, 8, vel=38)
    f.expr(["trem_va", "cb"], [(0, -14), (8, -13)])
    f.expr(["clar"], [(0, -13), (8, -13)])
    f.expr("hand", [(0, -12), (8, -12)])
    # not even King Saul dared to go out: a drooping bassoon, half cadence on D
    k.mel("bsn", "G3:1 E3:1 F#3:1 D3:1", vel=56)
    k.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    k.mel("cb", "C2:2 D2:2", vel=40, role="bass")
    k.expr(["bsn"], [(0, -11), (3, -12), (4, -14)])
    k.expr(["vla", "vln2", "vc", "cb"], [(0, -13), (3, -13), (4, -15)])   # ease into the next page


def forty(c):
    """The day counter: morning (G, a flute bird, a glockenspiel sunrise) and Goliath's shout (G minor tuba);
    evening (E minor, celesta) and the shout again; morning, evening, forty days (tuba honks); 'nobody dared'
    (E minor tremolo), ii-V into G."""
    c.gain(-1.0)
    t_e = c.at("到了晚上")
    t_c = c.gap(c.find("早上喊"))
    t_d = c.gap(c.find("可是以色列人里"))
    a = c.seg(0, t_e, 1, "4/4", "G major", nominal=64, label="forty-morning")
    b = c.seg(t_e, t_c, 1, "4/4", "E minor", nominal=98, label="forty-evening")
    r = c.seg(t_c, t_d, 2, "4/4", "G major", nominal=107, label="forty-days")
    d = c.seg(t_d, c.dur, 2, "4/4", "E minor", nominal=108, label="forty-nobody")
    for sg in (a, b, r, d):
        sg.duck(1.5)
    a.prog("G:3 Gm:1")
    b.prog("Em:3 Gm:1")
    r.prog("G:2 Em:2 | C:2 D:2")
    d.prog("Em:4 | Am:2 D:2")
    # morning: the sun comes up (glockenspiel, flute bird); 'Goliath came to shout again' (tuba)
    a.mel("flute", "r:1/2 D6:1/4 B5:1/4 D6:1/2 r:2", vel=52)
    a.add("glock", 0, 1, "G6", 32, "arp", "r")
    a.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=42, bass_part="vc", bass_lo=43, bass_hi=55)
    a.add("cb", 0, 4, "G1", 40, "bass")
    a.mel("tuba", "r:3 G2:1/2:s D2:1/2:s", vel=58)
    a.expr(["flute", "glock"], [(0, -15), (4, -14)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (1, -13), (4, -13)])
    a.expr(["tuba"], [(0, -10), (4, -10)])
    # evening: E minor, a celesta star; and again he shouts
    b.mel("celesta", "B5:1 G5:1 E5:1 r:1", vel=44, role="arp")
    b.pad(["vla", "vln2", "vln1"], 3, 52, 71, vel=42, bass_part="vc", bass_lo=43, bass_hi=55)
    b.add("cb", 0, 3, "E2", 40, "bass")
    b.add("cb", 3, 1, "G1", 40, "bass")
    b.mel("tuba", "r:3 G2:1/2:s D2:1/2:s", vel=58)
    b.expr(["celesta"], [(0, -9), (4, -9)])
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (4, -14)])
    b.expr(["tuba"], [(0, -10), (4, -10)])
    # morning shout, evening shout, forty days: the days tick by (plucks), a tuba honk on each shout
    for q in np.arange(0, 8, 0.5):
        ch = r.chord_at(q + 1e-3)
        r.add("pz_hi", q, 0.5, max(ch.tones(67, 79)), 46 if q % 1 else 52, "arp", "s")
    for t in group_times(c, "早上喊", 2):
        q = min(max(round(r.q_of(c.t0 + t) * 2) / 2, 0.0), r.n_q - 0.5)
        r.add("tuba", q, 0.5, r.chord_at(q + 1e-3).bass_note(38, 50), 56, "bass", "s")
    r.pad(["vla", "vln2"], 2, 52, 69, vel=40, bass_part="vc", bass_lo=40, bass_hi=52)
    bassline(r, "cb", 28, 40, 40)
    r.expr(["pz_hi"], [(0, -11), (8, -11)])
    r.expr(["tuba"], [(0, -10), (8, -10)])
    r.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (8, -14)])
    # but not one of the Israelites dared to come out: tremolo, a timid clarinet sinking; ii-V into G
    d.pad(["trem_va", "trem_va", "trem_hi"], 3, 48, 69, vel=46, bass_ref=(40, 52))
    d.mel("clar", "B4:2 G4:1 E4:1 | E4:1 C4:1 D4:2", vel=52)
    d.mel("cb", "E2:4 | A1:2 D2:2", vel=40, role="bass")
    d.expr(["trem_va", "cb"], [(0, -15), (8, -15)])
    d.expr(["clar"], [(0, -13), (8, -13)])


def shepherd(c):
    """Bethlehem: David's theme b1-b4 (the shepherd's pipe: flute over harp); father Jesse (b5-b8 on the
    clarinet, horn, warm strings); off he goes (walking pizzicato, oboe, a harp sweep on '出发了')."""
    c.gain(-2.0)
    t_j = c.gap(c.find("有一天"))
    t_o = c.gap(c.find("大卫一大早"))
    t_go = c.at("出发了")
    a = c.seg(0, t_j, 4, "4/4", "G major", nominal=78, label="shepherd-theme")
    j = c.seg(t_j, t_o, 4, "4/4", "G major", nominal=90, label="shepherd-jesse")
    o = c.seg(t_o, t_go, 2, "4/4", "G major", nominal=112, label="shepherd-walk")
    g = c.seg(t_go, c.dur, 1, "2/4", "G major", nominal=108, label="shepherd-off")
    for sg in (a, j, o, g):
        sg.duck(1.5)
    a.prog(" | ".join(DAVID_PROG[:4]))
    j.prog(" | ".join(DAVID_PROG[4:8]))
    o.prog("G:4 | C:2 D:2")
    g.prog("G:2")
    # on the green hills of Bethlehem, a shepherd boy named David: the theme on the flute (his pipe)
    a.mel("flute", bars(DAVID, 0, 4), vel=62)
    broken(a, "harp", 0, a.n_q, (0, 2, 4, 6, 4, 2), 43, 55, vel=40, thin=True)
    strings(a, vel=42, lo=55, hi=71, bass=(43, 55), cb=(31, 43))
    a.duck(2.5, parts=["flute", "harp"])
    a.expr(["flute"], [(0, -11), (16, -11)])
    a.expr(["harp"], [(0, -8), (16, -9)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (2, -13), (16, -13)])
    # his father Jesse: the theme's second half on the clarinet, a warm horn below
    j.mel("horn", bars(DAVID, 4, 8), vel=56, transpose=-12)
    j.pad(["vla", "vla", "vln2"], 3, 50, 66, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    bassline(j, "cb", 31, 43, 40)
    j.duck(8.0)
    j.duck(3.0, parts=["horn"])
    j.expr(["horn"], [(0, -13), (16, -13)])
    j.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (16, -14)])
    # up early, the sheep handed over, and off he goes: walking pizzicato, the theme's head on the oboe
    o.mel("pz_lo", "G2:1 B2:1 D3:1 B2:1 | C3:1 E3:1 D3:1 A2:1", vel=58, role="bass")
    o.mel("oboe", "B4:1 D5:1/2 B4:1/2 G4:1 D5:1 | E5:1 G5:1/2 E5:1/2 F#5:1 A5:1", vel=54, art="s")
    o.pad(["vla", "vln2"], 2, 52, 67, vel=38, bass_ref=(43, 55))
    o.expr(["pz_lo"], [(0, -9), (8, -9)])
    o.expr(["oboe"], [(0, -12), (8, -12)])
    o.expr(["vla", "vln2"], [(0, -15), (8, -15)])
    # '出发了': a harp sweep up and a glockenspiel 'ting'
    g.sync("'出发了' (harp sweep)", 0, t_go)
    gliss(g, "harp", 0, 0.35, midi("G3"), midi("G6"), v0=34, v1=50, scale=ChordTones(g.chord_at(0)))
    g.add("glock", 0, 1, "D7", 44, "arp", "h")
    pluck_chord(g, 0, vel=56, lo=55, hi=67)
    g.add("pz_cb", 0, 0.5, "G1", 58, "bass", "h")
    g.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    g.expr(["harp", "glock"], [(0, -9), (2, -10)])
    g.expr(["vla", "vln2", "vln1", "vc"], [(0, -14), (2, -15)])


def camp(c):
    """The camp: David arrives (b1, clarinet) and the sky darkens (Eb-D); Goliath's shout (a hit, his theme);
    the soldiers run (a G minor scurry); David asks (b1 + b7, a question on D); Eliab is cross (E minor,
    grumpy bassoon); David's simple answer."""
    c.gain(-1.5)
    t_g = c.gap(c.find("胆小鬼们"))
    t_r = c.gap(c.find("转身就跑"))
    t_d = c.gap(c.find("这个人是谁"))
    t_e = c.gap(c.find("以利押听见了"))
    t_i = c.gap(c.find("我又做了什么"))
    a = c.seg(0, t_g, 2, "4/4", "G major", nominal=84, label="camp-arrive")
    g = c.seg(t_g, t_r, 1, "4/4", "G minor", nominal=66, label="camp-goliath")
    r = c.seg(t_r, t_d, 2, "4/4", "G melodic", nominal=98, label="camp-run")
    d = c.seg(t_d, t_e, 2, "4/4", "G major", nominal=84, label="camp-david-asks")
    e = c.seg(t_e, t_i, 3, "4/4", "E minor", nominal=70, label="camp-eliab")
    i = c.seg(t_i, c.dur, 1, "4/4", "G major", nominal=60, label="camp-answer")
    for sg in (a, g, r, d, e, i):
        sg.duck(1.5)
    a.prog("G:4 | Eb:2 D:2")
    g.prog("Gm:4")
    r.prog("Gm:4 | D:4")
    d.prog("G:4 | C:2 D7:2")
    e.prog("Em:4 | Am:4 | Am:2 D:2")
    i.prog("G:2 D:2")
    g.sync("Goliath's voice booms (his theme, a stomp)", 0, t_g)
    g.gain(-3.0)
    i_g = c.find("胆小鬼们")
    far = picture(c, "thud", c.ls(0), c.ls(i_g) - 0.3) or []     # his booming steps, heard from afar
    near = picture(c, "thud", c.ls(i_g) - 0.3, t_r - 0.3) or []  # ...and as he shouts
    # David arrives with his basket (the theme's head, clarinet) -- and hears a huge voice (Eb, D)
    a.mel("clar", DAVID[0] + " | G4:2 F#4:2", vel=58)
    a.pad(["vla", "vln2"], 2, 55, 69, vel=40, bass_part="vc", bass_lo=38, bass_hi=50)
    a.mel("trem_va", "r:4 | G3:2 A3:2", vel=44, role="pad")
    a.add("trem_va", 4, 2, "Bb3", 44, "pad", voice="trem_va.1")
    a.add("trem_va", 6, 2, "D4", 44, "pad", voice="trem_va.1")
    broken(a, "harp", 0, 4, (0, 2, 4, 2), 43, 55, vel=36, thin=True)
    a.expr(["clar"], [(0, -12), (8, -12)])
    a.expr(["vla", "vln2", "vc", "harp"], [(0, -14), (8, -14)])
    a.expr(["trem_va"], [(4, -20), (8, -12)])
    for t in far:
        sg, q = seg_at(c, (a, g), t)
        stomp(sg, q, vel=46, kit=True)
    a.expr(["timp", "pz_cb", "okit"], [(0, -10), (8, -10)])
    # 'Cowards! Who dares come out and fight me?': a stomp and Goliath's theme, slow and heavy
    stomp(g, 0, vel=64, bass="G1")
    g.mel("tuba", GOLIATH[0], vel=58)
    g.mel("bsn", GOLIATH[0], vel=56)
    g.add("cb", 0, 4, "G1", 42, "bass")
    for i_, t in enumerate(near):
        sg, q = seg_at(c, (a, g, r), t)
        stomp(sg, q, vel=58, kit=True)
        sg.sync(f"Goliath's step {i_ + 1}", q, t)
    if not near:
        g.add("timp", 2, 0.5, "G2", 44, "timp")
    for k_, p_ in enumerate(g.chord_at(0).tones(50, 62)[:3]):
        g.add("tbn", 0, 1, p_, 54, "harmony", "h", voice=f"tbn.{k_}")
    g.pad(["trem_va", "trem_hi"], 2, 55, 70, vel=40, bass_ref=(31, 43))
    g.duck(2.0, parts=["tuba", "bsn"])
    g.expr(["tuba", "bsn"], [(0, -9), (4, -11)])
    g.expr(["tbn"], [(0, -9), (4, -12)])
    g.expr(["cb", "trem_va", "trem_hi"], [(0, -14), (4, -15)])
    # the soldiers see Goliath and run: a scurry (clarinet + bassoon), plucked basses
    run = ("D5:1/2 C5:1/2 Bb4:1/2 A4:1/2 G4:1/2 F#4:1/2 G4:1/2 A4:1/2 | "
           "F#4:1/2 G4:1/2 A4:1/2 G4:1/2 F#4:1/2 E4:1/2 D4:1")
    toks = run.split()                                  # staccato, the last note held into David's question
    run = " ".join(t if t == "|" or k_ == len(toks) - 1 else t + ":s" for k_, t in enumerate(toks))
    r.mel("clar", run, vel=60)
    r.mel("bsn", run, vel=56, transpose=-12)
    r.pad(["trem_va", "trem_va"], 2, 55, 67, vel=40, bass_ref=(31, 43))
    r.expr(["trem_va"], [(0, -18), (8, -14)])
    r.mel("pz_cb", "G1:1 D2:1 G1:1 D2:1 | D2:1 A1:1 D2:2", vel=56, role="bass")
    r.expr(["clar", "bsn"], [(0, -12), (8, -11)])
    r.expr(["pz_cb"], [(0, -9), (8, -9)])
    # 'Who is this man? How dare he defy the armies of the living God?': the theme, a question on D7
    d.mel("flute", DAVID[0] + " | " + DAVID[6], vel=58)
    broken(d, "harp", 0, 8, (0, 2, 4, 2), 43, 55, vel=36, thin=True)
    d.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    d.duck(6.0, parts=["flute", "harp"])
    d.expr(["flute"], [(0, -16), (1, -12), (8, -12)])
    d.expr(["vla", "vln2", "vln1", "vc", "harp"], [(0, -18), (1, -14), (8, -14)])
    # his eldest brother Eliab, cross: a grumpy bassoon in E minor, plucked strings
    e.mel("bsn", "E3:1/2:s r:1/2 E3:1/2:s G3:1/2:s B2:1 r:1 | A2:1/2:s r:1/2 C3:1/2:s E3:1/2:s A2:1 r:1 | "
                 "C3:1/2:s B2:1/2:s A2:1 F#2:1 A2:1", vel=60)
    e.mel("pz_cb", "E2:1 r:1 B1:1 r:1 | A1:1 r:1 E2:1 r:1 | A1:1 r:1 D2:1 r:1", vel=54, role="bass")
    e.pad(["vla", "vln2"], 2, 52, 67, vel=38, bass_ref=(28, 40))
    e.expr(["bsn"], [(0, -11), (12, -11)])
    e.expr(["pz_cb", "vla", "vln2"], [(0, -13), (12, -13)])
    # 'What have I done now? I was only asking.': simple and light (flute, harp)
    broken(i, "harp", 0, 4, (0, 2, 4, 2), 43, 55, vel=36, thin=True)
    i.pad(["vla", "vln2"], 2, 55, 69, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    i.expr(["vla", "vln2", "vc", "harp"], [(0, -13), (4, -15)])


def saul(c):
    """Saul's tent (E minor horn, soft timpani); David brave (b1-b2, horn, G major); '你？' -- a double take,
    Goliath on the tuba; the lion (a G minor pizzicato pounce); the bear (an Eb waddle); the rescue (running
    cellos, b1 + b7); faith (b5-b8, horn and choir); Saul's blessing (plagal C-G, harp)."""
    c.gain(-1.6)
    t_b = c.gap(c.find("王啊"))
    t_k = c.gap(c.find("你还是个孩子"))
    t_l = c.gap(c.find("有狮子来抓小羊"))
    t_br = c.at("也有熊来抓小羊")
    t_rs = c.at("我就去追")
    t_f = c.gap(c.find("上帝救我脱离"))
    t_bl = c.gap(c.find("好吧，你去吧"))
    a = c.seg(0, t_b, 2, "4/4", "E minor", nominal=68, label="saul-tent")
    b = c.seg(t_b, t_k, 2, "4/4", "G major", nominal=82, label="saul-david")
    k = c.seg(t_k, t_l, 2, "4/4", "E minor+", nominal=68, label="saul-you")
    l = c.seg(t_l, t_br, 2, "4/4", "G minor+", nominal=108, label="saul-lion")
    br = c.seg(t_br, t_rs, 1, "4/4", "G minor", nominal=104, label="saul-bear")
    rs = c.seg(t_rs, t_f, 2, "4/4", "G major", nominal=112, label="saul-rescue")
    f = c.seg(t_f, t_bl, 3, "4/4", "G major", nominal=92, label="saul-faith")
    bl = c.seg(t_bl, c.dur, 1, "4/4", "G major", nominal=58, rit=0.15, label="saul-blessing")
    for sg in (a, b, k, l, br, rs, f, bl):
        sg.duck(1.5)
    a.prog("Em:2 C:2 | Am:2 D:2")
    b.prog(" | ".join(DAVID_PROG[:2]))
    k.prog("Em:4 | Gm:2 D:2")
    l.prog("Gm:4 | Cm:2 D:2")
    br.prog("Eb:2 D:2")
    rs.prog("G:4 | C:2 D7:2")
    f.prog(" | ".join([DAVID_PROG[4], DAVID_PROG[6], DAVID_PROG[7]]))
    bl.prog("C:2 G:2")
    # King Saul's tent: a stately, worried horn over soft timpani and low strings
    a.mel("horn", "B3:2 C4:1 B3:1 | A3:1 C4:1 A3:2", vel=54)
    strings(a, vel=40, lo=52, hi=67, bass=(40, 52), cb=(28, 40))
    for q, nm in ((0, "E2"), (4, "A2")):
        a.add("timp", q, 0.5, nm, 36, "timp")
    a.duck(2.5, parts=["horn"])
    a.expr(["horn"], [(0, -12), (8, -12)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb", "timp"], [(0, -14), (8, -14)])
    # 'O king, nobody needs to be afraid. I will go and fight the giant!': David's theme on the horn
    b.mel("horn", bars(DAVID, 0, 2), vel=58, transpose=-12)
    broken(b, "harp", 0, 8, (0, 2, 4, 2), 43, 55, vel=36, thin=True)
    strings(b, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    b.duck(2.5, parts=["horn", "harp"])
    b.expr(["horn"], [(0, -12), (8, -11)])
    b.expr(["vla", "vln2", "vln1", "vc", "cb", "harp"], [(0, -14), (8, -13)])
    # 'You? You are only a boy!' (a plucked double take) '...he has been a warrior since his youth' (tuba)
    pluck_chord(k, 0, vel=58, lo=59, hi=71)
    k.add("pz_cb", 0, 0.5, "E2", 58, "bass", "h")
    k.mel("bsn", "r:1/2 E3:1/4:s G3:1/4:s B3:1/2:s r:5/2", vel=56)
    k.mel("tuba", "r:4 | G2:1 Bb2:1 A2:1 D2:1", vel=54)
    k.pad(["vla", "vln2"], 2, 52, 67, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    k.add("cb", 0, 4, "E2", 40, "bass")
    k.add("cb", 4, 2, "G1", 40, "bass")
    k.add("cb", 6, 2, "D2", 40, "bass")
    k.expr(["bsn", "tuba"], [(0, -10), (8, -11)])
    k.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (8, -14)])
    # the lion came to take a lamb: a pizzicato pounce, a soft growl in the bassoon, tremolo
    l.mel("pz_lo", "G2:1/2:s r:1/2 D3:1/2:s r:1/2 G2:1/2:s Bb2:1/2:s D3:1 | C3:1/2:s r:1/2 Eb3:1/2:s r:1/2 D3:1 A2:1",
          vel=60, role="bass")
    l.mel("bsn", "r:2 G2:1 Bb2:1/2 A2:1/2 | G2:2 F#2:2", vel=52)
    l.pad(["trem_va", "trem_hi"], 2, 55, 70, vel=42, bass_ref=(31, 43))
    timp_roll(l, 6, 7.8, midi("D2"), 24, 30)                    # on the D chord only
    l.expr(["pz_lo"], [(0, -9), (8, -9)])
    l.expr(["bsn"], [(0, -11), (8, -11)])
    l.expr(["trem_va", "timp"], [(0, -16), (8, -14)])
    # ...and a bear: the tuba waddles (Eb, D)
    br.mel("tuba", "Eb2:1 Bb1:1 D2:1 A1:1", vel=56)
    br.mel("bsn", "G3:1/2:s r:1/2 Eb3:1/2:s r:1/2 F#3:1/2:s r:1/2 D3:1/2:s r:1/2", vel=50)
    br.pad(["vla", "vln2"], 2, 52, 67, vel=36, bass_ref=(34, 46))
    br.expr(["tuba", "bsn"], [(0, -10), (4, -10)])
    br.expr(["vla", "vln2"], [(0, -12), (4, -12)])
    # 'I went after them and saved the lamb from their mouths': running cellos, the theme (flute)
    for q0, q1, ch in rs.chord_spans():
        root = ch.bass_note(43, 54)
        fifth = root + 7 if (root + 7) % 12 in ch.pcset else root + 12
        q, k_ = q0, 0
        while q < q1 - 1e-6:
            rs.add("vc_fast", q, 0.5, [root, fifth][k_ % 2], 56 + (6 if k_ % 4 == 0 else 0), "bass", "s")
            q += 0.5
            k_ += 1
        rs.add("cb_fast", q0, q1 - q0, ch.bass_note(31, 43), 50, "bass")
    rs.mel("flute", DAVID[0] + " | " + DAVID[6], vel=58)
    rs.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=38, bass_ref=(43, 54))
    rs.duck(2.5, parts=["flute"])
    rs.expr(["vc_fast", "cb_fast"], [(0, -18), (1.5, -13), (8, -12)])
    rs.expr(["flute"], [(0, -15), (1, -12), (8, -11)])
    rs.expr(["vla", "vln2", "vln1"], [(0, -16), (8, -15)])
    # 'God saved me from the lion and the bear, he will save me from this giant!': b5-b8, horn and choir
    f.mel("horn", " | ".join([DAVID[4], DAVID[6], DAVID[7]]), vel=58, transpose=-12)
    f.pad("ooh", 3, 55, 74, vel=42, bass_ref=(43, 55))
    broken(f, "harp", 0, f.n_q, (0, 2, 4, 6, 4, 2), 43, 55, vel=36, thin=True)
    strings(f, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    f.duck(5.0)
    f.duck(7.0, parts=["horn", "harp", "ooh"])
    f.expr(["horn"], [(0, -12), (12, -11)])
    f.expr(["ooh"], [(0, -20), (4, -17), (12, -16)])
    f.expr(["harp"], [(0, -9), (12, -9)])
    f.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (12, -13)])
    # 'Go, and the LORD be with you!': a plagal blessing, harp
    for k_, nm in enumerate(["C3", "G3", "C4", "E4", "G4"]):
        bl.add("harp", 0.15 * k_, 2 - 0.15 * k_, nm, 42 - 2 * k_, "arp")
    for k_, nm in enumerate(["G2", "D3", "G3", "B3", "D4"]):
        bl.add("harp", 2 + 0.15 * k_, 2 - 0.15 * k_, nm, 42 - 2 * k_, "arp")
    strings(bl, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    bl.pad("ooh", 3, 55, 72, vel=40, bass_ref=(43, 55))
    bl.expr(["vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -14), (4, -15)])
    bl.expr(["harp"], [(0, -9), (4, -10)])


def armor(c):
    """Comic: the fitting (a little march); clanks on the helmet, the coat of mail and the sword; the first
    steps; '哐当，哐当' (woodblocks, low pizzicato, bassoon); '哎呀' -- the wobble down; '这些我穿不惯' (clarinet);
    free again (the theme's head, flute, harp sweep)."""
    c.gain(-1.6)
    t_d = c.at("头上戴上")
    t_w = c.gap(c.find("大卫试着走了几步"))
    t_k = c.at("哐当，哐当")
    t_x = c.gap(c.find("这些我穿不惯"))
    t_f = c.gap(c.find("大卫就把盔甲"))
    # the picture: a thud as the helmet and as the sword go on (the mail jingles in between), a thud on each
    # 哐当, a whoosh as he wobbles ('哎呀') and as the armour comes off -- the narration where it is missing
    put = picture(c, "thud", t_d - 0.3, c.le(0) + 0.3)
    helmet, sword = (put[0], put[-1]) if put and len(put) >= 2 else (c.at("铜头盔"), c.at("大刀"))
    mail = on_picture(c, "coins", helmet + 0.4, sword - 0.4, 1, lambda: [c.at("铠甲")])[0]
    v_cl = voice_times(c, "哐当，哐当", 3)
    clanks = on_picture(c, "thud", c.ls(1) - 0.3, c.le(1), 2, lambda: v_cl[:2])
    t_oops = on_picture(c, "whoosh", clanks[-1] + 0.3, c.le(1), 1, lambda: v_cl[2:])[0]
    t_off = on_picture(c, "whoosh", c.ls(3) - 0.3, c.dur - 0.5, 1, lambda: [t_f])[0]
    a = c.seg(0, t_d, 2, "4/4", "G major", nominal=114, label="armor-fitting")
    d = c.seg(t_d, t_w, 2, "4/4", "G major", nominal=80, label="armor-pieces")
    w = c.seg(t_w, t_k, 1, "4/4", "G major", nominal=103, label="armor-steps")
    k = c.seg(t_k, t_oops, 1, "4/4", "G major", nominal=136, label="armor-clank")
    o = c.seg(t_oops, t_x, 1, "4/4", "G major", nominal=84, label="armor-wobble")
    x = c.seg(t_x, t_f, 1, "4/4", "G major", nominal=120, label="armor-not-used")
    f = c.seg(t_f, c.dur, 1, "4/4", "G major", nominal=72, label="armor-free")
    for sg in (a, d, w, k, o, x, f):
        sg.duck(1.5)
    a.prog("G:4 | D:2 G:2")
    d.prog("G:4 | D:2 G:2")
    w.prog("G:2 D:2")
    k.prog("G:4")
    k.sync("'哐当': back on G as the clanking starts", 0, t_k, kind="change")
    o.prog("C:2 D7:2")
    x.prog("G:2 D7:2")
    f.prog("G:4")
    # King Saul puts his own armour on David: a pompous little march (bassoon, plucked strings)
    a.mel("bsn", "G3:1/2:s B3:1/2:s D4:1/2:s B3:1/2:s G3:1 D3:1 | A3:1/2:s F#3:1/2:s D3:1 G3:2", vel=58)
    a.mel("pz_cb", "G1:1 r:1 D2:1 r:1 | D2:1 r:1 G1:1 r:1", vel=54, role="bass")
    a.pad(["vla", "vln2"], 2, 55, 69, vel=38, bass_ref=(31, 43))
    a.expr(["bsn"], [(0, -11), (8, -11)])
    a.expr(["pz_cb", "vla", "vln2"], [(0, -13), (8, -13)])
    # a bronze helmet (ting), a coat of mail (clank), a big sword at his side (a heavier clank)
    d.mel("pz_cb", "G1:1 r:1 D2:1 r:1 | D2:1 r:1 G1:1 r:1", vel=50, role="bass")
    d.pad(["vla", "vln2"], 2, 55, 69, vel=36, bass_ref=(31, 43))
    for lbl, t, kw in (("the helmet", helmet, dict(vel=58, low=False, ting=True)),
                       ("the coat of mail", mail, dict(vel=62)), ("the sword", sword, dict(vel=66, ting=True))):
        q = min(max(d.q_of(c.t0 + t), 0.0), d.n_q - 0.1)
        clank(d, q, **kw)
        d.sync(f"clank: {lbl}", q, t)
    d.expr(["pz_cb", "vla", "vln2"], [(0, -13), (8, -13)])
    d.expr(["pz_lo", "glock"], [(0, -8), (8, -8)])
    d.expr("hand", [(0, -8), (8, -8)])
    # David tries a few steps: heavy tiptoes
    w.mel("pz_lo", "G2:1/2:s r:1/2 D2:1/2:s r:1/2 D2:1/2:s r:1/2 A2:1/2:s r:1/2", vel=54, role="bass")
    w.pad(["vla", "vln2"], 2, 55, 69, vel=36, bass_ref=(38, 50))
    w.expr(["pz_lo", "vla", "vln2"], [(0, -12), (4, -12)])
    # 哐当，哐当: clank! clank! (woodblocks, a low pluck, the bassoon stumbling)
    for i_, t in enumerate(clanks):
        sg, q = seg_at(c, (w, k, o), t)
        ch = sg.chord_at(q + 1e-3)
        clank(sg, q, vel=56 + 2 * i_)
        sg.add("pz_cb", q, _dq(sg, q, 0.5), ch.bass_note(28, 40), 62, "bass", "h")
        sg.add("bsn", q, _dq(sg, q, 1.75), ch.tones(43, 55)[-1 if i_ == 0 else 0], 58, "melody")
        sg.sync(f"'哐当' {i_ + 1} (clank)", q, t)
    k.pad(["vla", "vln2"], 2, 55, 69, vel=36, bass_ref=(31, 43))
    k.expr(["pz_lo", "pz_cb", "bsn"], [(0, -7), (4, -7)])
    k.expr("hand", [(0, -6), (4, -6)])
    k.expr(["vla", "vln2"], [(0, -11), (4, -11)])
    # '哎呀，太重了，根本走不动！': the bassoon wobbles down chromatically onto the dominant
    o.mel("bsn", "G3:1/2 F#3:1/2 F3:1/2 E3:1/2 Eb3:1/2 D3:1/2 C3:1", vel=56)
    o.mel("pz_cb", "C2:1/2:s r:3/2 D2:1/2:s r:3/2", vel=52, role="bass")
    o.pad(["vla", "vln2"], 2, 54, 69, vel=36, bass_ref=(36, 50))
    o.expr(["bsn"], [(0, -13), (0.5, -10), (4, -11)])
    o.expr(["pz_cb", "vla", "vln2"], [(0, -13), (4, -13)])
    # 'I'm not used to these.' -- simply (clarinet)
    x.mel("bsn", "B3:1 G3:1 C4:1 A3:1", vel=54)
    x.pad(["vla", "vln2"], 2, 55, 69, vel=36, bass_part="vc", bass_lo=43, bass_hi=55)
    x.expr(["bsn"], [(0, -12), (4, -12)])
    x.expr(["vla", "vln2", "vc"], [(0, -15), (4, -15)])
    # he takes it all off -- himself again: the theme's head on the flute, a harp sweep
    f.mel("flute", DAVID[0], vel=56)
    q_off = min(max(f.q_of(c.t0 + t_off), 0.0), 3.0)             # the armour comes off (the picture's whoosh)
    gliss(f, "harp", q_off, 0.4, midi("G3"), midi("G6"), v0=30, v1=44, scale=ChordTones(f.chord_at(0)))
    f.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    f.add("cb", 0, 4, "G1", 38, "bass")
    f.expr(["flute", "harp"], [(0, -11), (4, -12)])
    f.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (4, -15)])


def stones(c):
    """The brook (harp ripples, G major); five plucks counting up G-A-B-C-D on '一块……五块' over a falling bass
    G-F#-E-C-D, home to G on '都放进口袋里'; the sling (a circling harp, a flute run up on '又快又远'), D."""
    c.gain(-1.8)
    t_n = c.at("一块")
    t_sl = c.gap(c.find("他手里还拿着"))
    # the stones drop into the bag on the picture (its pops; the spoken counts without it), the bag sparkles on
    # '都放进口袋里'; the sling's test swings (whooshes) start the run on '又快又远'
    pops = [max(t, t_n) for t in on_picture(c, "pop", t_n - 0.3, c.le(1) + 0.3, 5, lambda: voice_times(c, "一块", 5))]
    t_bag = on_picture(c, "sparkle", pops[-1] + 0.2, min(c.le(1) + 0.6, t_sl - 0.3), 1,
                       lambda: voice_times(c, "一块", 6)[5:])[0]
    swings = picture(c, "whoosh", c.ls(2), c.dur - 0.5) or []
    t_far = swings[0] if swings else c.at("又快又远")
    long_far = c.dur - t_far > 2.0
    a = c.seg(0, t_n, 3, "4/4", "G major", nominal=90, label="stones-brook")
    n = c.seg(t_n, t_sl, 2, "4/4", "G major", nominal=82, label="stones-count")
    s = c.seg(t_sl, t_far, 2, "4/4", "G major", nominal=64, label="stones-sling")
    r = c.seg(t_far, c.dur, 1, "4/4" if long_far else "2/4", "D major", nominal=88 if long_far else 80,
              label="stones-far")
    for sg in (a, n, s, r):
        sg.duck(1.5)
    a.prog("G:4 | C:2 G:2 | Am:2 D:2")
    qs = [min(round(n.q_of(c.t0 + t) * 48) / 48, n.n_q - 0.25) for t in pops + [t_bag]]
    chords = ["G", "D/F#", "Em", "C", "D", "G"]
    edges = [0] + [int(round(q * 48)) for q in qs[1:]] + [int(round(n.n_q * 48))]
    n.prog(" ".join(f"{ch}:{edges[k + 1] - edges[k]}/48" for k, ch in enumerate(chords)))
    n.sync("'一块': home to G as the counting starts", 0, t_n, kind="change")
    s.prog("G:4 | C:2 Em:2")
    r.prog("D:4" if long_far else "D:2")
    # David takes his shepherd's staff and goes down to the brook: harp ripples, a soft flute
    ripple(a, 0, a.n_q, 55, 79, vel=36)
    a.mel("flute", "r:4 | E5:1 G5:1/2 E5:1/2 D5:1 B4:1 | C5:1 E5:1/2 C5:1/2 A4:2", vel=52)
    a.pad(["vla", "vla", "vln2"], 3, 50, 67, vel=36, bass_part="vc", bass_lo=43, bass_hi=55)
    bassline(a, "cb", 31, 43, 38)
    a.duck(2.0, parts=["flute", "harp"])
    a.expr(["harp"], [(0, -10), (12, -10)])
    a.expr(["flute"], [(0, -12), (12, -12)])
    a.expr(["vla", "vln2", "vc", "cb"], [(0, -15), (12, -15)])
    # one, two, three, four, five: a pluck for every stone, counting up; into the bag: G
    for k, (q, nm) in enumerate(zip(qs, ["G4", "A4", "B4", "C5", "D5"])):
        n.add("pz_hi", q, _dq(n, q, 1.0), nm, 62 + 2 * k, "harmony", "h")
        n.add("harp", q, _dq(n, q, 1.0), nm, 50 + 2 * k, "arp", "h")
        n.add("pz_cb", q, _dq(n, q, 0.5), n.chord_at(q + 1e-3).bass_note(36, 48), 54, "bass", "h")
        n.sync(f"stone {k + 1}", q, pops[k])
    n.add("glock", qs[4], _dq(n, qs[4], 1.0), "D6", 46, "arp", "h")
    q5 = qs[5]
    n.sync("into the bag (G)", q5, t_bag)
    n.add("pz_cb", q5, _dq(n, q5, 0.5), "G2", 58, "bass", "h")
    pluck_chord(n, q5, vel=58, lo=55, hi=67)
    for k_, nm in enumerate(["G3", "B3", "D4", "G4"]):
        n.add("harp", q5 + 0.08 * k_, _dq(n, q5, 1.5) - 0.08 * k_, nm, 44, "arp")
    n.pad(["vla", "vln2"], 2, 52, 66, vel=36, bass_part="vc", bass_lo=40, bass_hi=52)
    n.expr(["pz_hi", "harp", "pz_cb", "glock"], [(0, -9), (8, -9)])
    n.expr(["vla", "vln2", "vc"], [(0, -12), (8, -12)])
    # the sling, a long strap that throws stones fast and far: a circling harp; a flute run up on '又快又远'
    broken(s, "harp", 0, s.n_q, (0, 1, 2, 3, 2, 1), 50, 74, vel=36, thin=True)
    s.mel("flute", "r:4 | E5:1 G5:1/2 E5:1/2 G5:1 B5:1", vel=48)
    s.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    bassline(s, "cb", 31, 43, 38)
    # '...又快又远': fast and far -- the flute runs up, the harp sweeps (D, the dominant of the fight)
    r.mel("flute", f"D5:1/8 E5:1/8 F#5:1/8 G5:1/8 A5:1/8 B5:1/8 C#6:1/8 D6:1/8 D6:{int(r.n_q) - 1}", vel=50)
    for t in swings[1:]:                                   # the strap whirls again: a plucked 'whish' each time
        q = r.q_of(c.t0 + t)
        if 0.9 <= q <= r.n_q - 0.25:
            r.add("pz_hi", q, _dq(r, q, 0.5), max(r.chord_at(q + 1e-3).tones(62, 74)), 50, "arp", "s")
    gliss(r, "harp", 0, 0.45, midi("D4"), midi("D6"), v0=30, v1=44, scale=ChordTones(r.chord_at(0)))
    r.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=38, bass_part="vc", bass_lo=38, bass_hi=50)
    r.add("cb", 0, r.n_q, "D2", 38, "bass")
    r.expr(["flute", "harp", "pz_hi"], [(0, -12), (r.n_q, -12)])
    r.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (r.n_q, -14)])
    s.duck(2.0, parts=["flute", "harp"])
    s.expr(["harp"], [(0, -10), (8, -10)])
    s.expr(["flute"], [(0, -12), (8, -12)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -14)])


def face(c):
    """Goliath sees David (G minor); the laugh on '哈哈大笑' (ho-ho-ho, tuba + bassoon + timpani); his mockery
    (the theme, soft under his voice); David answers (b1 on the horn, G major); '万军之耶和华的名' (choir);
    the build (b5-b7 and a held D with a timpani roll) into the fight."""
    c.gain(-1.9)
    t_h = c.at("哈哈大笑")
    t_m = c.gap(c.find("你拿着棍子"))
    t_d = c.gap(c.find("你来打我"))
    t_n = c.at("我来打你")
    t_w = c.gap(c.find("今天，我要让"))
    a = c.seg(0, t_h, 1, "4/4", "G minor", nominal=73, label="face-sees")
    h = c.seg(t_h, t_m, 1, "3/4", "G minor", nominal=128, label="face-laugh")
    m = c.seg(t_m, t_d, 2, "4/4", "G minor+", nominal=66, label="face-mock")
    d = c.seg(t_d, t_n, 1, "4/4", "G major", nominal=80, label="face-david")
    n = c.seg(t_n, t_w, 1, "4/4", "G major", nominal=58, label="face-lord")
    w = c.seg(t_w, c.dur, 3, "4/4", "G major", nominal=80, label="face-build")
    for sg in (a, h, m, d, n, w):
        sg.duck(1.5)
    a.prog("Gm:4")
    h.prog("Gm:3")
    m.prog("Gm:4 | Cm:2 D:2")
    d.prog("G:4")
    n.prog("C:2 D7:2")
    w.prog("G:4 | C:2 D7:2 | D:4")
    h.sync("'哈哈大笑' (ho-ho-ho)", 0, t_h)
    d.sync("David answers (G major)", 0, t_d, kind="change")
    # Goliath sees the boy coming: his theme's head, soft, a low tremolo
    a.mel("tuba", GOLIATH[0], vel=54)
    a.pad(["trem_va", "trem_va"], 2, 48, 64, vel=42, bass_ref=(31, 43))
    a.add("cb", 0, 4, "G1", 40, "bass")
    a.expr(["tuba"], [(0, -11), (4, -11)])
    a.expr(["trem_va", "cb"], [(0, -16), (4, -14)])
    # ho! ho! ho!
    for k_, nm in enumerate(["D3", "Bb2", "G2"]):
        held = k_ == 2                                  # the last 'ho' is a long, satisfied one
        h.add("tuba", k_, 1.0 if held else 0.5, nm, 64 - 4 * k_, "melody", "" if held else "s")
        h.add("bsn", k_, 1.0 if held else 0.5, nm, 62 - 4 * k_, "melody", "" if held else "s")
        h.add("pz_lo", k_, 0.5, nm, 60 - 4 * k_, "harmony", "h")
        h.add("timp", k_, 0.5, timp_pitch(h.chord_at(k_), midi(nm) if midi(nm) >= 38 else midi("G2")),
              58 - 6 * k_, "timp", "h")
    pluck_chord(h, 0, vel=62, lo=55, hi=67)
    drum(h, 0, 41, 62)
    h.add("cb", 0, 3, "G1", 40, "bass")
    drum(h, 1, 41, 54)
    h.sync("ho 2", 1, h.t(1) - c.t0)
    h.expr(["tuba", "bsn", "pz_lo", "timp"], [(0, -7), (3, -8)])
    # 'Am I a dog, that you come at me with a stick? ...': his theme, low and soft under his voice
    m.mel("tuba", " | ".join([GOLIATH[0], GOLIATH[3]]), vel=56)
    m.mel("bsn", " | ".join([GOLIATH[0], GOLIATH[3]]), vel=52)
    m.add("cb", 0, 4, "G1", 40, "bass")
    m.add("cb", 4, 2, "C2", 40, "bass")
    stomp(m, 4, vel=46, kit=False, bass="C2")
    m.pad(["trem_va", "trem_hi"], 2, 55, 70, vel=38, bass_ref=(31, 43))
    m.duck(2.5, parts=["tuba", "bsn"])
    m.expr(["tuba", "bsn"], [(0, -14), (1, -12), (8, -12)])
    m.expr(["cb", "timp", "pz_cb", "trem_va", "trem_hi"], [(0, -15), (8, -15)])
    # 'You come with sword and spear -- ': David's theme on the horn, steady
    d.mel("horn", DAVID[0], vel=58, transpose=-12)
    d.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=42, bass_part="vc", bass_lo=43, bass_hi=55)
    d.add("cb", 0, 4, "G1", 40, "bass")
    d.add("timp", 0, 0.5, "G2", 40, "timp")
    d.duck(2.5, parts=["horn"])
    d.expr(["horn"], [(0, -12), (4, -12)])
    d.expr(["vla", "vln2", "vln1", "vc", "cb", "timp"], [(0, -14), (4, -14)])
    # '-- I come in the name of the LORD of hosts!': the choir enters, the theme goes on
    n.mel("horn", DAVID[6], vel=58, transpose=-12)
    n.pad("choir", 3, 55, 72, vel=44, bass_ref=(43, 55))
    strings(n, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    n.duck(3.0, parts=["horn", "choir"])
    n.expr(["horn"], [(0, -12), (4, -11)])
    n.expr(["choir"], [(0, -20), (2, -15), (4, -14)])
    n.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (4, -13)])
    # 'Today the whole world will know there is a God in Israel! The battle is the LORD's!': b5-b7 grow, D held
    w.mel("horn", DAVID[4] + " | " + DAVID[6], vel=58, transpose=-12)
    w.pad("choir", 3, 55, 74, vel=44, bass_ref=(43, 55))
    strings(w, vel=44, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    for q in (0, 4):
        w.add("timp", q, 0.5, timp_pitch(w.chord_at(q), midi("G2")), 40, "timp")
    timp_roll(w, 8, 11.8, midi("D2"), 28, 52)
    w.duck(4.5)
    w.duck(6.0, parts=["horn", "choir"])
    w.expr(["horn"], [(0, -13), (8, -11), (12, -10)])
    w.expr(["choir"], [(0, -20), (6, -17), (12, -16)])
    w.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (8, -12), (12, -11)])
    w.expr(["timp"], [(0, -12), (12, -9)])


def sling(c):
    """Goliath walks (G minor stomps); David runs (G major, b1 + b7, running cellos); the stone into the sling
    (D pedal, tiptoe); '转啊转' the whirl (circling harp and flute rising, suspended cymbal); '嗖' the whoosh;
    '正好打中' the bonk and the giant's fall (a chromatic slide in tuba and bassoon over D7); '咚！' the big
    low hit on G minor, the dust settling."""
    c.gain(-3.5)
    t_r = c.at("大卫不但没有跑")
    t_p = c.gap(c.find("他从口袋里"))
    tz = group_times(c, "转啊转", 2)
    t_sou = c.at("嗖")
    t_hit = c.at("正好打中")
    t_dong = c.at("咚！巨人扑倒")
    steps = picture(c, "thud", c.ls(0) - 0.3, t_p - 0.3)          # Goliath's steps on the picture
    a = c.seg(0, t_r, 1, "4/4", "G minor", nominal=74, label="sling-goliath")
    r = c.seg(t_r, t_p, 2, "4/4", "G major", nominal=111, label="sling-run")
    p = c.seg(t_p, tz[0], 2, "4/4", "G major", nominal=112, label="sling-stone")
    z = c.seg(tz[0], t_sou, 2, "3/4", "G major", nominal=121, label="sling-whirl")   # a beat per turn
    f = c.seg(t_sou, t_hit, 1, "4/4", "G major", nominal=113, label="sling-whoosh")
    h = c.seg(t_hit, t_dong, 1, "4/4", "G major", nominal=83, label="sling-fall")
    d = c.seg(t_dong, c.dur, 1, "4/4", "G minor", nominal=60, label="sling-thud")
    for sg in (a, r, p, z, f, h, d):
        sg.duck(1.5)
    a.prog("Gm:4")
    r.prog("G:4 | C:2 D7:2")
    p.prog("D:4 | Dsus4:2 D:2")
    z.prog("G:3/2 C:3/2 | D:3/2 D7:3/2")
    f.prog("G:4")
    h.prog("D7:4")
    d.prog("Gm:4")
    z.sync("'转啊转': the whirl (G major)", 0, tz[0], kind="change")
    f.sync("'嗖' (whoosh)", 0, t_sou)
    h.sync("'正好打中' (bonk)", 0, t_hit)
    d.sync("'咚！' the giant falls (big low hit)", 0, t_dong)
    # Goliath comes at David: his theme; a stomp on each of his steps (the picture's), else on every beat
    a.mel("tuba", GOLIATH[0], vel=58)
    a.mel("bsn", GOLIATH[0], vel=54)
    if steps:
        for i_, t in enumerate(steps):
            sg, q = seg_at(c, (a, r, p), t)
            stomp(sg, q, vel=56 + 2 * i_, kit=True)
            sg.sync(f"Goliath's step {i_ + 1}", q, t)
    else:
        for q in (0, 1, 2, 3):
            stomp(a, q, vel=52 + (4 if q % 2 == 0 else 0), kit=q % 2 == 0, bass="G1")
    a.pad(["trem_va", "trem_va"], 2, 48, 64, vel=42, bass_ref=(31, 43))
    a.expr(["tuba", "bsn"], [(0, -10), (4, -10)])
    a.expr(["timp", "pz_cb"], [(0, -9), (4, -9)])
    a.expr(["trem_va"], [(0, -15), (4, -13)])
    # David doesn't run away -- he runs toward him!: running cellos, the theme on the flute
    for q0, q1, ch in r.chord_spans():
        root = ch.bass_note(43, 54)
        fifth = root + 7 if (root + 7) % 12 in ch.pcset else root + 12
        q, k_ = q0, 0
        while q < q1 - 1e-6:
            r.add("vc_fast", q, 0.5, [root, fifth][k_ % 2], 58 + (6 if k_ % 4 == 0 else 0), "bass", "s")
            q += 0.5
            k_ += 1
        r.add("cb_fast", q0, q1 - q0, ch.bass_note(31, 43), 50, "bass")
    r.mel("flute", DAVID[0] + " | " + DAVID[6], vel=60)
    r.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 76, vel=40, bass_ref=(43, 54))
    r.duck(2.0, parts=["flute"])
    r.expr(["vc_fast", "cb_fast"], [(0, -12), (8, -11)])
    r.expr(["flute"], [(0, -11), (8, -10)])
    r.expr(["trem_va", "trem_hi"], [(0, -18), (8, -15)])
    # a stone from his bag into the sling: tiptoe plucks over a D pedal, a held breath
    for q in np.arange(0, 8, 0.5):
        ch = p.chord_at(q + 1e-3)
        p.add("pz_hi", q, 0.5, max(ch.tones(62, 74)) if q % 1 else min(ch.tones(62, 74)), 48, "arp", "s")
    p.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 76, vel=40, bass_ref=(38, 50))
    p.add("cb", 0, 8, "D2", 42, "bass")
    p.expr(["pz_hi"], [(0, -11), (8, -10)])
    p.expr(["trem_va", "trem_hi", "cb"], [(0, -17), (8, -14)])
    # 转啊转，转啊转: round and round -- the harp and flute circle, rising; a suspended cymbal swells
    broken(z, "harp", 0, 5.5, (0, 1, 2, 3), 55, 79, vel=44, step=0.25, accent=6, restart=False)
    q2 = min(max(z.q_of(c.t0 + tz[1]), 1.5), 4.5)
    q2 = round(q2 * 4) / 4
    for q0, q1, ch in z.chord_spans(q2, 5.5):
        lad = ch.tones(72, 91)
        q, k_ = q0, 0
        while q < q1 - 1e-6:
            z.add("flute", q, 0.25, lad[min(k_ % 4 + (1 if q >= 4.5 else 0), len(lad) - 1)], 50, "arp", "s")
            q += 0.25
            k_ += 1
    z.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 79, vel=46, bass_ref=(38, 50))
    bassline(z, "cb", 31, 43, 44)
    roll(z, 0, 5.9, 59, 14, 40, rate=12)
    z.expr(["harp", "flute"], [(0, -12), (6, -8)])
    z.expr(["trem_va", "trem_hi", "cb"], [(0, -16), (6, -10)])
    # 嗖！ the stone flies: harp glissando, a flute run, a plucked chord, a high glockenspiel
    gliss(f, "harp", 0, 0.3, midi("G4"), midi("G6"), v0=46, v1=60, scale=ChordTones(f.chord_at(0)))
    pluck_chord(f, 0, vel=70, lo=62, hi=74)
    f.add("pz_cb", 0, 0.5, "G1", 64, "bass", "h")
    f.add("pz_lo", 0, 0.5, "G2", 62, "bass", "h")
    f.add("okit", 0, 1, 57, 50, "perc", "h")
    drum(f, 0, 54, 56)
    f.add("glock", 0, 1, "G6", 50, "arp", "h")
    f.mel("flute", "G5:1/4 A5:1/4 B5:1/4 C6:1/4 D6:1", vel=54)
    f.pad(["trem_va", "trem_hi", "trem_hi"], 3, 55, 76, vel=42, bass_ref=(31, 43))
    f.expr(["flute", "glock", "harp", "pz_hi", "pz_cb", "pz_lo"], [(0, -7), (4, -10)])
    f.expr(["trem_va", "trem_hi"], [(0, -13), (4, -15)])
    f.expr("hand", [(0, -8), (4, -8)])
    # 正好打中: bonk! (woodblock, glockenspiel, timpani) -- stars -- and the giant topples (a chromatic slide)
    drum(h, 0, 76, 70)
    h.add("glock", 0, 1, "A6", 50, "arp", "h")
    h.add("timp", 0, 0.5, "D2", 58, "timp", "h")
    h.add("pz_lo", 0, 0.5, "D3", 58, "bass", "h")
    h.add("celesta", 0.25, 0.25, "F#6", 44, "arp", "s")
    h.add("celesta", 0.5, 0.25, "A6", 42, "arp", "s")
    fall = "r:1 D3:1/2 C#3:1/2 C3:1/2 B2:1/2 Bb2:1/2 A2:1/2"
    h.mel("tuba", fall, vel=58)
    h.mel("bsn", fall, vel=56)
    h.pad(["trem_va", "trem_va"], 2, 48, 66, vel=42, bass_ref=(38, 50))
    h.expr(["tuba", "bsn"], [(0, -12), (4, -9)])
    h.expr(["glock", "celesta", "pz_lo", "timp"], [(0, -8), (4, -8)])
    h.expr(["trem_va"], [(0, -15), (4, -13)])
    h.expr("hand", [(0, -6), (4, -6)])
    # 咚！ the giant falls flat: a big warm low hit on G, then the dust settles
    d.add("timp", 0, 1, "G2", 68, "timp", "h")
    d.add("okit", 0, 1, 36, 68, "perc", "h")
    d.add("tuba", 0, 2, "G1", 60, "bass", "h")
    d.add("pz_cb", 0, 0.5, "G1", 68, "bass", "h")
    d.add("pz_lo", 0, 0.5, "G2", 62, "bass", "h")
    d.add("okit", 0, 2, 57, 44, "perc", "h")
    d.mel("bsn", "r:2 D3:1/2 Bb2:1/2 G2:1", vel=48)
    d.pad(["trem_va", "trem_va"], 2, 48, 64, vel=42, bass_ref=(31, 43))
    d.add("cb", 0, 4, "G1", 44, "bass")
    d.add("celesta", 2.5, 0.5, "D6", 38, "arp", "r")
    d.expr(["timp", "tuba", "pz_cb", "pz_lo"], [(0, -5), (4, -9)])
    d.expr(["bsn", "celesta"], [(0, -12), (4, -12)])
    d.expr(["trem_va", "cb"], [(0, -16), (1, -13), (4, -15)])


def victory(c):
    """The Philistines see their champion down (Goliath's theme deflated on the bassoon) and flee (a G minor
    scurry onto D7); '欢呼' -- David's theme in full: brass, violins, choir 'ah', timpani, glockenspiel (G)."""
    c.gain(-2.0)
    t_r = c.at("吓得转身就逃")
    t_v = c.at("欢呼")
    a = c.seg(0, t_r, 2, "4/4", "G minor+", nominal=103, label="victory-see")
    r = c.seg(t_r, t_v, 1, "4/4", "G melodic", nominal=75, label="victory-flee")
    v = c.seg(t_v, c.dur, 2, "4/4", "G major", nominal=104, label="victory-cheer")
    for sg in (a, r, v):
        sg.duck(1.5)
    a.prog("Gm:4 | D:4")
    r.prog("Gm:2 D7:2")
    v.prog("G:4 | C:2 D7:2")
    v.sync("'欢呼': David's theme in full (G major)", 0, t_v, kind="change")
    v.gain(-1.8)
    # their mightiest warrior is down: Goliath's theme, deflated (bassoon), a low tremolo
    a.mel("bsn", "D3:1 Bb2:1 G2:2 | F#2:1 A2:1 D2:2", vel=56)
    a.pad(["trem_va", "trem_va"], 2, 48, 64, vel=40, bass_ref=(31, 43))
    a.mel("cb", "G1:4 | D2:4", vel=40, role="bass")
    a.expr(["bsn"], [(0, -10), (8, -11)])
    a.expr(["trem_va", "cb"], [(0, -16), (8, -15)])
    # ...they turn and run!: a scurry down (clarinet + bassoon in sixteenths)
    run = ("D5:1/4 C5:1/4 Bb4:1/4 A4:1/4 G4:1/4 F#4:1/4 G4:1/4 A4:1/4 "
           "C5:1/4 A4:1/4 F#4:1/4 E4:1/4 D4:1/4 C4:1/4 A3:1/4 D4:1/4")
    r.mel("clar", run, vel=58, art="s")
    r.mel("bsn", run, vel=54, art="s", transpose=-12)
    r.mel("pz_cb", "G1:1 D2:1 D2:1 A1:1", vel=56, role="bass")
    r.pad(["trem_va", "trem_hi"], 2, 55, 72, vel=40, bass_ref=(31, 43))
    r.expr(["clar", "bsn"], [(0, -11), (4, -10)])
    r.expr(["pz_cb"], [(0, -9), (4, -9)])
    r.expr(["trem_va", "trem_hi"], [(0, -16), (4, -12)])
    # Israel cheers!: David's theme, bright -- brass and violins, choir 'ah', timpani, glockenspiel
    theme = DAVID[0] + " | " + DAVID[6]
    v.mel("brass", theme, vel=58)
    v.mel("vln_mel", theme, vel=56)
    v.mel("horn", theme, vel=52, transpose=-12)
    v.pad("choir", 3, 55, 74, vel=46, bass_ref=(43, 55))
    strings(v, vel=44, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    broken(v, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 43, 55, vel=40, thin=True)
    for q in (0, 2, 4, 6):
        v.add("timp", q, 0.5, timp_pitch(v.chord_at(q), midi("G2")), 52 if q % 4 == 0 else 44, "timp", "h")
    v.add("glock", 0, 1, "B6", 46, "arp", "h")
    v.add("okit", 0, 2, 57, 40, "perc", "h")
    v.duck(3.0, parts=["brass", "vln_mel", "horn", "choir"])
    v.expr(["brass", "vln_mel", "horn"], [(0, -11), (8, -10)])
    v.expr(["choir"], [(0, -16), (2, -12), (8, -12)])
    v.expr(["vla", "vln2", "vln1", "vc", "cb", "harp"], [(0, -12), (8, -12)])
    v.expr(["timp", "glock"], [(0, -9), (8, -9)])


def end(c):
    """Under the stars: David's theme slow (flute, harp, celesta); the question (Em C Dsus4 -- the 2 s pause
    after it keeps only the soft Dsus4); b5-b7 warm (clarinet, strings, choir); the final G major chord on
    '和我在一起', ringing to the end."""
    c.gain(-2.2)
    t_q = c.gap(c.find("小朋友，你心里"))
    t_e = c.gap(c.find("下次害怕的时候"))
    t_f = c.at("和我在一起")
    a = c.seg(0, t_q, 2, "4/4", "G major", nominal=56, label="end-stars")
    q = c.seg(t_q, t_e, 2, "4/4", "G major", nominal=98, label="end-question")
    e = c.seg(t_e, t_f, 3, "4/4", "G major", nominal=93, rit=0.15, label="end-theme")
    f = c.seg(t_f, c.dur, 1, "4/4", "G major", nominal=88, rit=0.3, label="end-final-chord")
    for sg in (a, q, e):
        sg.duck(1.5)
    a.prog(" | ".join(DAVID_PROG[:2]))
    q.prog("Em:2 C:2 | Dsus4:4")
    e.prog(" | ".join(DAVID_PROG[4:7]))
    f.prog("G:4")
    f.sync("the final G major chord: '和我在一起'", 0, t_f, kind="change")
    # evening on the hill, the first stars: the theme slowly (flute), harp, celesta
    a.mel("flute", bars(DAVID, 0, 2), vel=56)
    broken(a, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 43, 55, vel=38, thin=True)
    strings(a, vel=40, lo=55, hi=71, bass=(43, 55), cb=(31, 43))
    a.add("celesta", 2.5, 0.5, "D6", 38, "arp", "r")
    a.add("celesta", 7.5, 0.5, "B5", 36, "arp", "r")
    a.duck(2.5, parts=["flute", "harp"])
    a.expr(["flute"], [(0, -12), (8, -12)])
    a.expr(["harp", "celesta"], [(0, -9), (8, -10)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (8, -15)])
    # 'is there a giant in your heart that frightens you?' -- the celesta asks; then only a soft held chord
    q.mel("celesta", "E6:1 B5:1 C6:1 G5:1 | A5:2 D6:2", vel=42, role="arp")
    q.pad(["vla", "vln2", "vln1"], 3, 55, 71, vel=38, bass_part="vc", bass_lo=43, bass_hi=55)
    q.mel("cb", "E2:2 C2:2 | D2:4", vel=36, role="bass")
    q.expr(["celesta"], [(0, -10), (4, -10), (8, -14)])
    q.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (4, -15), (8, -18)])
    # 'next time you are afraid, you can say like David: God, I believe you are with me': b5-b7, warm
    e.mel("clar", bars(DAVID, 4, 7), vel=58)
    e.mel("horn", "G3:4 | G3:2 B3:2 | C4:2 C4:2", vel=44, role="counter")
    broken(e, "harp", 0, e.n_q, (0, 2, 4, 6, 4, 2), 43, 55, vel=38, thin=True)
    strings(e, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    e.pad("ooh", 3, 55, 72, vel=38, q0=4, bass_ref=(43, 55))
    e.duck(3.0, parts=["clar", "horn", "harp", "ooh"])
    e.expr(["clar"], [(0, -20), (1.5, -13), (12, -12)])
    e.expr(["horn", "harp"], [(0, -20), (1.5, -14), (12, -13)])
    e.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -19), (1.5, -14), (12, -13)])
    e.expr(["ooh"], [(4, -20), (6, -16), (12, -15)])
    # '...和我在一起': the G major chord, harp rolled up, celesta stars, flute on G -- it rings to the end
    f.add("flute", 0, 4, "G5", 54, "melody")
    for k_, nm in enumerate(["G2", "D3", "G3", "B3", "D4", "G4", "B4", "D5", "G5"]):
        f.add("harp", 0.12 * k_, 4 - 0.12 * k_, nm, 48 - 2 * k_, "arp", "r")
    f.mel("celesta", "D6:1 G6:1 B6:1 D7:1", vel=40, art="r", role="arp")
    strings(f, vel=42, lo=55, hi=72, bass=(43, 55), cb=(31, 43))
    f.pad("ooh", 3, 55, 72, vel=40, bass_ref=(43, 55))
    f.expr(["flute", "vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -14), (1, -13.5), (2.5, -15.5), (4, -26)])
    f.expr(["harp", "celesta"], [(0, -12), (4, -15)])


SCENE_CUES = {
    "s01_title": title, "s02_afraid": afraid, "s03_valley": valley, "s04_giant": giant, "s05_forty": forty,
    "s06_shepherd": shepherd, "s07_camp": camp, "s08_saul": saul, "s09_armor": armor, "s10_stones": stones,
    "s11_face": face, "s12_sling": sling, "s13_victory": victory, "s14_end": end,
}

# Hit points the score must place, defined by the narration text (audio/music_check.py REQUIRED_HITS format:
# (scene, phrase, mode, kind); mode 'line' / 'gap' / 'phrase' / 'end', kind 'hit' (attack) or 'change' (harmony)).
# Where a sound word is also an on-screen action (Goliath's 咚s, the armour's 哐当, the stones dropping into the
# bag) the phrase is where the harmony arrives, and the attacks themselves follow the picture: PICTURE_HITS.
REQUIRED_HITS = [
    ("s02_afraid", "是一个巨人", "phrase", "change"),           # G minor: the giant (his footfalls: picture)
    ("s03_valley", "非利士人站在那边", "phrase", "change"),     # the Philistines' hill (E-flat, G minor)
    ("s04_giant", "咚！咚！咚！", "phrase", "change"),          # Goliath steps out (G minor; the stomps: picture)
    ("s04_giant", "以色列人听了", "gap", "change"),             # Israel's fear (E minor)
    ("s07_camp", "胆小鬼们", "gap", "hit"),                     # Goliath's voice booms
    ("s09_armor", "哐当", "phrase", "change"),                  # the clanking starts (the clanks: picture)
    ("s10_stones", "一块", "phrase", "change"),                 # the counting starts (the five plucks: picture)
    ("s11_face", "哈哈大笑", "phrase", "hit"),                  # the giant laughs
    ("s11_face", "你来打我", "gap", "change"),                  # David answers (G major)
    ("s12_sling", "转啊转", "phrase", "change"),                # the whirl
    ("s12_sling", "嗖", "phrase", "hit"),                       # whoosh
    ("s12_sling", "正好打中", "phrase", "hit"),                 # bonk
    ("s12_sling", "咚！巨人扑倒", "phrase", "hit"),             # the giant falls
    ("s13_victory", "欢呼", "phrase", "change"),                # David's theme in full
    ("s14_end", "和我在一起", "phrase", "change"),              # the final chord
]

# Hit points defined by the PICTURE (music_check.PICTURE_HITS format: (scene, sfx cue name, from-line phrase or
# None, index, offset s, kind, what)): the scenes' own sound-effect cues, keyed to the animation (and, for the
# 咚s and the counting, to the narrator's voice).  The index counts that cue from the start of the line containing
# the phrase (minus 0.3 s); s04's line starts with three softer approach steps, so its 咚 stomps are #3-#5.
PICTURE_HITS = [
    ("s02_afraid", "thud", "是一个巨人", 0, 0.0, "hit", "the giant's first footfall"),
    ("s02_afraid", "thud", "是一个巨人", 1, 0.0, "hit", "the giant's second footfall"),
    ("s04_giant", "thud", "咚！咚！咚！", 3, 0.0, "hit", "stomp 1 ('咚')"),
    ("s04_giant", "thud", "咚！咚！咚！", 4, 0.0, "hit", "stomp 2 ('咚')"),
    ("s04_giant", "thud", "咚！咚！咚！", 5, 0.0, "hit", "stomp 3 ('咚')"),
    ("s07_camp", "thud", "胆小鬼们", 0, 0.0, "hit", "Goliath's step as he shouts"),
    ("s07_camp", "thud", "胆小鬼们", 1, 0.0, "hit", "Goliath's second step"),
    ("s09_armor", "thud", "哐当", 0, 0.0, "hit", "'哐当' 1 (clank)"),
    ("s09_armor", "thud", "哐当", 1, 0.0, "hit", "'哐当' 2 (clank)"),
    ("s10_stones", "pop", "一块", 0, 0.0, "hit", "stone 1"),
    ("s10_stones", "pop", "一块", 1, 0.0, "hit", "stone 2"),
    ("s10_stones", "pop", "一块", 2, 0.0, "hit", "stone 3"),
    ("s10_stones", "pop", "一块", 3, 0.0, "hit", "stone 4"),
    ("s10_stones", "pop", "一块", 4, 0.0, "hit", "stone 5"),
    ("s12_sling", "thud", "歌利亚朝大卫走过来", 0, 0.0, "hit", "Goliath's step 1"),
    ("s12_sling", "thud", "歌利亚朝大卫走过来", 1, 0.0, "hit", "Goliath's step 2"),
    ("s12_sling", "thud", "歌利亚朝大卫走过来", 2, 0.0, "hit", "Goliath's step 3"),
]
