"""The background score for 约拿的故事 — one continuous piece in 13 cues.

Every cue starts exactly at its scene's global start and is planned in bars whose tempo is
derived from the scene's real line timings (hit points such as the storm peak, the calm sea,
the gulp, God's mercy are segment boundaries).  Tonal plan (all hand-offs by common tone or
dominant -> tonic):

  title D major 6/8 (Jonah theme) -> call D major + bVI/bVII mixture -> flee D dorian
  -> storm D minor -> lots D minor (lament bass) -> fish D minor -> D major (calm)
  -> belly B minor -> D major (prayer, = V of G) -> shore G major -> nineveh D hijaz (= V of g)
  -> repent G minor -> G major (mercy, half cadence) -> vine G minor/Eb-F-G/G waltz/chromatic/D
  -> lesson G major 6/8 (theme on piano, ends on A7) -> end D major 6/8 (theme, final cadence)

The Jonah theme (D major, 6/8, q = quarter note):
  b1 D  F#5:1 E5:1/2 D5:1 A4:1/2        motif x (3-2-1-5, lilting long-short)
  b2 G  B4:1 D5:1/2 G5:1 F#5:1/2        motif y (rising arpeggio)
  b3 Em7|A7  E5:3/2 C#5:1 D5:1/2
  b4 A  E5:5/2 A4:1/2                   half cadence + pickup
  b5 = b1,  b6 G  B4:1 D5:1/2 G5:1 B5:1/2,  b7 D/A|A7  A5:1 F#5:1/2 E5:1 C#5:1/2,  b8 D  D5:3
"""
import numpy as np

from audio.scorekit import Cue, Score
from audio.theory import midi

STR_UP = ["vla", "vln2", "vln1"]


# ----------------------------------------------------------------------------- helpers
def ladder(ch, lo, hi, top=108):
    b = ch.bass_note(lo, hi)
    return [p for p in range(b, top + 1) if p % 12 in ch.pcset]


def span_end(seg, q):
    for a, b, _, _ in seg.chords:
        if a - 1e-6 <= q < b - 1e-6:
            return b
    return seg.n_q


def broken(seg, part, q0, q1, pat, lo, hi, vel=52, step=0.5, accent=8, role="arp", art="", top=108,
           restart=True, ring=True, thin=False):
    """Broken-chord figure: pat indexes the chord-tone ladder that starts at the chord's bass.

    With ring=True each note sustains until the chord changes (harp/pedal style), never across it.
    thin=True: while a line is being spoken only the beats are played (e.g. dotted-quarter pulses in
    6/8); the full figure returns in the pauses."""
    q, i, last = q0, 0, None
    while q < q1 - 1e-6:
        ch = seg.chord_at(q)
        if restart and ch is not last:
            i = 0
        last = ch
        if thin and abs((q + 1e-6) % seg.beat_q) > 2e-6 and bool(seg.score.speaking(seg.t(q))):
            q += step
            i += 1
            continue
        lad = ladder(ch, lo, hi, top)
        k = pat[i % len(pat)]
        p = lad[min(k, len(lad) - 1)]
        dq = min(span_end(seg, q), q1) - q if ring else step
        seg.add(part, q, dq, p, vel + (accent if i % len(pat) == 0 else 0), role, art)
        q += step
        i += 1


def drop_spoken(notes, pre=0.08):
    """Remove the given notes whose onset falls while a line is spoken (or just before one)."""
    if not notes:
        return []
    sc = notes[0].seg.score
    gone = {id(n) for n in notes if sc.speaking(np.array([n.seg.t(n.q), n.seg.t(n.q) + pre])).any()}
    sc.notes[:] = [n for n in sc.notes if id(n) not in gone]
    return [n for n in notes if id(n) not in gone]


def gliss(seg, part, q0, dur_s, lo, hi, up=True, v0=40, v1=70, scale=None):
    """Harp glissando over the segment scale (or an explicit Scale) taking dur_s seconds."""
    sc = scale or seg.scale
    notes = sc.degree_pitches(lo, hi)
    if not up:
        notes = notes[::-1]
    t0 = seg.t(q0)
    n = len(notes)
    for k, p in enumerate(notes):
        x = k / max(1, n - 1)
        tk = t0 + dur_s * (x ** 0.9)
        v = v0 + (v1 - v0) * (1 - (2 * x - 1) ** 2) if v1 > v0 else v0
        seg.add(part, seg.q_of(tk), 0.1, p, v, "gliss", "h")


def timp_roll(seg, q0, q1, pitch, v0, v1, rate=13.0):
    t0, t1 = seg.t(q0), seg.t(q1)
    n = max(2, int((t1 - t0) * rate))
    for k in range(n):
        tk = t0 + k * (t1 - t0) / n
        v = v0 + (v1 - v0) * k / (n - 1) + (3 if k % 2 else -3)
        seg.add("timp", seg.q_of(tk), (q1 - q0) / n, pitch, v, "timp")


def fill(cue, part, pause, n=3, lo=72, hi=96, vel=48, up=True, frac=0.85):
    """A soft chord-tone figure inside a narration pause (cue-relative (start, end))."""
    a, b = pause
    t0 = cue.t0 + a + 0.03
    seg = next(sg for sg in cue.segs if sg.t0 <= t0 < sg.t1)
    dt = (b - a) * frac / n
    ch = seg.chord_at(seg.q_of(t0))
    tones = ch.tones(lo, hi)
    start = len(tones) // 3
    pick = tones[start:start + n] if up else tones[start:start + n][::-1]
    for k, pch in enumerate(pick):
        tk = t0 + k * dt
        if tk >= seg.t1 - 0.02:
            break
        qk = seg.q_of(tk)
        if seg.chord_at(qk) is not ch:
            break
        seg.add(part, qk, span_end(seg, qk) - qk, pch, vel + 4 * k, "arp")


def drum(seg, q, key, vel, part="hand"):
    seg.add(part, q, 0.25, key, vel, "perc")


# ----------------------------------------------------------------------------- cues
def title(c):
    """Jonah theme, b1-b2: music box over harp and soft strings (D major, 6/8)."""
    s = c.seg(0, c.dur, 2, "6/8", "D major", nominal=84, label="title")
    s.prog("D:3 | G:3")
    s.mel("mbox", "F#6:1 E6:1/2 D6:1 A5:1/2 | B5:1 D6:1/2 G6:1 F#6:1/2", vel=92)
    s.mel("celesta", "F#5:1 E5:1/2 D5:1 A4:1/2 | B4:1 D5:1/2 G5:1 F#5:1/2", vel=56)
    broken(s, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 49, vel=46)
    s.pad(["vla", "vln2", "vln2"], 3, 54, 69, bass_part="vc", bass_lo=38, bass_hi=50, vel=50)
    s.expr(["vla", "vln2", "vc"], [(0, -16), (1.5, -7), (6, -6)])
    s.expr(["mbox", "celesta", "harp"], [(0, -2), (6, -3)])


def call(c):
    tB, tC = c.ls(1), c.gap(2)       # the A4 pickup of the theme sits in the pause before line 1
    # b3-b4 of the theme continue under "long ago there was a prophet named Jonah"
    a = c.seg(0, tB, 2, "6/8", "D major", nominal=84, label="call-theme")
    a.prog("Em7:3/2 A7:3/2 | Asus4:3/2 A:3/2")
    a.mel("celesta", "E5:3/2 C#5:1 D5:1/2 | E5:5/2 A4:1/2", vel=84)
    broken(a, "harp", 0, 6, (0, 2, 4, 5, 4, 2), 38, 49, vel=46)
    a.pad(["vla", "vln2", "vln2"], 3, 52, 69, bass_part="vc", bass_lo=38, bass_hi=50, vel=50)
    a.expr(["vla", "vln2", "vc", "celesta", "harp"], [(0, -6), (6, -7)])
    # "God said to him:" -- the theme resolves to D(add9); harp shimmer rises
    b = c.seg(tB, tC, 1, "3/8", "D major", nominal=76, label="call-shimmer")     # a held breath
    b.prog("Dadd9:3/2")
    b.mel("celesta", "F#5:3/2", vel=76)
    for k, nm in enumerate(["D4", "A4", "E5", "F#5", "A5", "D6"]):
        b.add("harp", k * 0.25, 1.5 - k * 0.25, nm, 42 + k, "arp")
    b.pad(["vla", "vln2", "vln2"], 3, 52, 69, bass_part="cb", bass_lo=38, bass_hi=50, vel=48)
    b.add("vc", 0, 1.5, "D3", 46, "bass")
    b.expr(["vla", "vln2", "vc", "cb"], [(0, -8), (1.5, -6)])
    # God speaks: choir enters on bVI over a D pedal, bVII -> I, minor iv, half cadence
    g = c.seg(tC, c.dur, 4, "6/8", "D major", nominal=82, rit=0.12, label="call-God")
    g.prog("Bb/D:3@D-minor | C/D:3/2@D-mixolydian D:3/2 | Gm/D:3@D-minor | Asus4:3/2 A:3/2")
    g.sync("choir enters with God's voice", 0, c.gap(2))
    tops = [midi(x) for x in ("D5", "E5", "F#5", "G5", "E5", "E5")]
    g.pad("choir", 3, 57, 79, vel=62, tops=tops, bass_ref=(33, 44))
    g.pad(["vla", "vln2", "vln2"], 3, 50, 67, vel=50, bass_ref=(33, 44))
    for q0, q1, ch in g.chord_spans():
        if ch.sym.startswith("A"):
            g.add("cb", q0, q1 - q0, "A1", 50, "bass")
            g.add("vc", q0, q1 - q0, "A2", 48, "bass")
        else:
            g.add("cb", q0, q1 - q0, "D2", 50, "bass")
            g.add("vc", q0, q1 - q0, "D3", 46, "bass")
    broken(g, "harp", 0, 12, (0, 1, 2, 3, 4, 5), 50, 61, vel=46, accent=6)
    fill(c, "celesta", c.pause_or_gap(3), n=3, lo=74, hi=91, vel=50)    # between God's two sentences
    g.expr("choir", [(0, -16), (1.5, -6), (6, -5), (9, -7), (12, -9)])
    g.expr(["vla", "vln2", "vc", "cb"], [(0, -6), (6, -5), (12, -8)])
    g.expr("harp", [(0, -5), (12, -6)])
    g.add("bsn", 11.5, 0.5, "A2", 62, "melody", "s")       # anacrusis into the flight (V -> i)


def flee(c):
    f = c.seg(0, c.dur, 5, "4/4", "D dorian", nominal=148, label="flee")
    f.prog("Dm:4 | G:4 | Dm:4 | C:4 | A7:4@D-melodic")
    f.mel("bsn", "D3:1/2:s F3:1/2:s A3:1/2:s r:1/2 G3:1/2:s F3:1/2:s E3:1/2:s D3:1/2:s | "
                 "B2:1/2:s D3:1/2:s G3:1/2:s r:1/2 A3:1/2:s B3:1/2:s A3:1/2:s G3:1/2:s", vel=72)
    f.mel("clar", "r:4 | r:4 | D5:1/2:s F5:1/2:s A5:1/2:s r:1/2 G5:1/2:s F5:1/2:s E5:1/2:s D5:1/2:s | "
                  "C5:1/2:s E5:1/2:s G5:1/2:s r:1/2 F5:1/2:s E5:1/2:s D5:1/2:s C5:1/2:s", vel=78)
    # the run under "想要躲开上帝。" stays soft; the storm's downbeat right after the line is the arrival
    f.mel("bsn", "A2:1/2 B2:1/2 C#3:1/2 D3:1/2 E3:1/2 F3:1/2 G3:1/2 A3:1/2:a", q=16, vel=62)
    f.mel("clar", "A4:1/2 B4:1/2 C#5:1/2 D5:1/2 E5:1/2 F5:1/2 G5:1/2 A5:1/2:a", q=16, vel=60)
    f.mel("pz_lo", " ".join(["D3:1/2 A2:1/2"] * 4) + " | " + " ".join(["G2:1/2 D3:1/2"] * 4) + " | "
          + " ".join(["D3:1/2 A2:1/2"] * 4) + " | " + " ".join(["C3:1/2 G2:1/2"] * 4) + " | "
          + "A2:1/2 E3:1/2 A2:1/2 E3:1/2 A2:1/2 C#3:1/2 E3:1/2 G3:1/2", vel=64, role="bass")
    f.mel("pz_cb", "D2:1 r:1 A1:1 r:1 | G1:1 r:1 D2:1 r:1 | D2:1 r:1 A1:1 r:1 | C2:1 r:1 G1:1 r:1 | "
                   "A1:1 r:1 A1:1 r:1", vel=70, role="bass")
    up = {"Dm": "[F4,A4,D5]", "G": "[G4,B4,D5]", "C": "[G4,C5,E5]", "A7": "[G4,C#5,E5]"}
    for bar, sym in enumerate(["Dm", "G", "Dm", "C", "A7"]):
        f.mel("pz_hi", " ".join([f"r:1/2 {up[sym]}:1/2"] * 4), q=bar * 4, vel=48, role="harmony")
    f.expr(["bsn", "clar"], [(0, -4), (20, -4)])
    f.expr(["pz_lo", "pz_cb", "pz_hi"], [(0, -3), (16, -4), (20, -4)])


def storm(c):
    """D minor, fastest and loudest cue -- but the loud moments live in the narration pauses:
    sforzando hit before '船几乎要被打破了！', subito piano under it, a surge and the horn call in
    the pause before line 2, receding under it, hush for the sleeping Jonah."""
    t_hit = (c.le(0) + c.ls(1)) / 2          # the gap before "船几乎要被打破了！"
    t_sleep = c.gap(3)                       # before "约拿却躺在船舱底下，呼呼大睡。"
    s1 = c.seg(0, t_hit, 2, "4/4", "D minor", nominal=160, label="storm-build")
    s2 = c.seg(t_hit, t_sleep, 4, "4/4", "D minor", nominal=168, label="storm-peak")
    s3 = c.seg(t_sleep, c.dur, 2, "4/4", "D minor", nominal=160, rit=0.15, label="storm-sleep")
    s1.prog("Dm:4 | Gm/Bb:2 A:2@D-harmonic")
    s2.prog("Dm:4 | Bb:4 | Gm:2 A:2@D-harmonic | Dm:2 A7:2@D-harmonic")
    s3.prog("Dm:4 | Gm/D:2 Dm:2")
    s2.sync("storm peak (orchestra hit, in the pause)", 0, t_hit)
    q_le0 = s1.q_of(c.t0 + c.le(0))
    q_le1, q_gap2, q_ls2 = (s2.q_of(c.t0 + x) for x in (c.le(1), c.gap(2), c.ls(2)))
    q_call = 5.5                                        # horn pickup: inside the pause before line 2

    # tremolo strings (the bass is played by cb_fast: bass_ref keeps the voicing clear of it)
    s1.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 50, 81, vel=74, center=66, bass_ref=(28, 40))
    s2.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 50, 81, vel=80, center=67, bass_ref=(28, 40))
    s3.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=50, bass_ref=(36, 47))
    # low strings: rolling eighths (cellos) and roots (basses)
    for seg in (s1, s2):
        for q0, q1, ch in seg.chord_spans():
            b = ch.bass_note(36, 47)
            fifth = b + 7 if (b + 7) % 12 in ch.pcset else b + 12
            q = q0
            k = 0
            while q < q1 - 1e-6:
                p = [b, fifth, b + 12, fifth][k % 4]
                seg.add("vc_fast", q, 0.5, p, 74 + (8 if k % 4 == 0 else 0), "bass", "s")
                q += 0.5
                k += 1
            seg.add("cb_fast", q0, q1 - q0, ch.bass_note(28, 40), 78, "bass")
    s3.add("cb", 0, 8, "D2", 46, "bass")
    # low brass: rising line under line 0 (soft), swells only in the pauses
    s1.mel("tbn", "D3:2 E3:1 F3:1 | G3:2 A3:2", vel=68)
    s1.mel("tuba", "D2:4 | Bb1:2 A1:2", vel=72, role="bass")
    s2.pad(["tbn", "tbn", "brass"], 3, 50, 70, vel=80, center=60, bass_ref=(28, 40))
    s2.mel("tuba", "D2:4 | Bb1:4 | G1:2 A1:2 | D2:2 A1:2", vel=80, role="bass")
    s2.mel("horn", "r:4 | r:3/2 A4:1/2 D5:1 F5:1 | G5:1 F5:1 E5:2 | F5:2 E5:2", vel=84)
    # timpani: hit on the storm downbeat, soft roll under line 0, crescendo roll in the pause into the hit
    s1.add("timp", 0, 1, "D2", 92, "timp", "h")      # answers the flight's run
    timp_roll(s1, 1, 4, midi("D2"), 34, 48)
    timp_roll(s1, 4, 6, midi("D2"), 46, 56)
    timp_roll(s1, 6, max(6.5, q_le0 - 0.3), midi("A2"), 56, 66)
    timp_roll(s1, max(6.5, q_le0 - 0.3), 8, midi("A2"), 80, 98)
    s2.add("timp", 0, 1, "D2", 100, "timp", "h")
    timp_roll(s2, 1, 4.5, midi("D2"), 40, 52)
    s2.add("timp", q_call + 0.5, 1, "D2", 84, "timp", "h")
    s2.mel("timp", "G2:1 r:1 A2:1 r:1 | D2:1 r:1 A2:1 A2:1", q=8, vel=58, role="timp")
    timp_roll(s3, 0, 6, midi("D2"), 40, 22)
    s2.add("okit", 0, 1, 36, 88, "perc", "h")           # concert bass drum on the peak
    s2.add("okit", 0, 2, 57, 62, "perc", "h")           # soft cymbal crash
    for k in range(10):                                 # suspended-cymbal swell into the peak
        s1.add("okit", 6 + k * 0.2, 0.2, 59, 16 + k * 4, "perc")
    # Jonah sleeps: the theme head in D minor on clarinet, a low bassoon sigh
    s3.mel("clar", "F4:3/2 E4:1/2 D4:3/2 A3:1/2 | D4:4", vel=58)
    s3.mel("bsn", "A2:4 | Bb2:2 A2:2", vel=50)
    # dynamics: soft build under line 0 -> surge in the pause -> sfz hit, subito piano under line 1
    # -> surge + horn call in the pause -> receding under line 2 -> hush
    for p in ("trem_hi", "trem_va", "vc_fast", "cb_fast", "tbn", "tuba", "horn", "brass", "timp"):
        s1.expr(p, [(0, -3), (1, -13), (max(1.5, q_le0 - 0.3), -9), (8, -1)])
        s2.expr(p, [(0, 0), (0.4, -9), (q_le1, -9), (q_gap2, -2), (q_ls2, -7), (16, -11)])
    s3.expr(["trem_lo", "trem_va", "cb", "clar", "bsn", "timp"], [(0, -9), (8, -11)])


def lots(c):
    s = c.seg(0, c.dur, 4, "4/4", "D minor", nominal=80, rit=0.1, label="lots")
    # lament bass D-C-Bb-A under a chain of clarinet 4-3 suspensions
    s.prog("Dsus2:2 Dm:2 | Csus4:2 Am/C:2 | Gm/Bb:4 | Asus4:2 A:2@D-harmonic")
    s.mel("clar", "r:2 F4:4 E4:4 D4:4 C#4:2", vel=66)
    s.mel("cb", "D2:4 | C2:4 | Bb1:4 | A1:4", vel=48, role="bass")
    s.mel("vc", "D3:4 | C3:4 | Bb2:4 | A2:4", vel=44, role="bass")
    s.pad(["vla", "vln2", "vln1"], 3, 55, 77, vel=38, center=66, bass_ref=(33, 44))
    s.mel("pz_lo", "r:1 D3:1 r:1 D3:1 | r:1 C3:1 r:1 C3:1 | r:1 Bb2:1 r:1 Bb2:1 | r:1 A2:1 r:1 A2:1",
          vel=36, role="bass")
    # the lot falls on Jonah: a small bell-like ping on the nearest eighth
    q = s.q_of(c.t0 + c.gap(1))
    e = span_end(s, q)
    s.add("harp", q, e - q, "G5", 56, "arp")
    s.add("harp", q, e - q, "C5", 50, "arp")
    s.add("celesta", q, e - q, "G5", 48, "arp")
    s.sync("lot falls (ping)", q, c.gap(1))
    for i in (2, 3):                               # faint echoes of the ping before Jonah speaks
        fill(c, "celesta", c.pause_or_gap(i), n=2, lo=67, hi=84, vel=40, up=False)
    s.expr(["vla", "vln2", "vln1", "vc", "cb", "pz_lo"], [(0, -10), (8, -7), (12, -7), (16, -10)])
    s.expr("clar", [(0, -6), (8, -5), (12, -5), (16, -7)])   # the 4-3 suspension chain stays in front


def fish(c):
    t_calm, t_gulp = c.le(0), c.gap(2)
    a = c.seg(0, t_calm, 2, "4/4", "D minor", nominal=116, label="fish-storm")
    b = c.seg(t_calm, t_gulp, 1, "4/4", "D major", nominal=104, label="fish-calm")
    g = c.seg(t_gulp, c.dur, 1, "3/4", "D major", nominal=90, rit=0.35, label="fish-gulp")
    a.prog("Dm:4 | Bb:2 A7:2@D-harmonic")
    b.prog("D:2 G/D:1 D:1")
    g.prog("D:1 A/C#:1 Bm:1@B-minor")
    b.sync("sea calm: D major + harp glissando", 0, t_calm)
    g.sync("gulp accent", 0, t_gulp)
    # storm reprise (they throw Jonah in), calming during "海立刻平静了"
    a.pad(["trem_va", "trem_hi", "trem_hi"], 3, 52, 77, vel=64, bass_ref=(28, 40))
    for q0, q1, ch in a.chord_spans():
        bnote = ch.bass_note(36, 47)
        for k in range(int(round((q1 - q0) / 0.5))):
            a.add("vc_fast", q0 + k * 0.5, 0.5, [bnote, bnote + 7, bnote + 12, bnote + 7][k % 4], 66, "bass", "s")
        a.add("cb", q0, q1 - q0, ch.bass_note(28, 40), 56, "bass")
    timp_roll(a, 0, 3, midi("D2"), 44, 70)
    a.mel("timp", "r:3 D2:1 | r:4", vel=76, role="timp")
    a.mel("horn", "D4:4 | D4:2 C#4:2", vel=64)
    a.expr(["trem_va", "trem_hi", "vc_fast", "cb", "horn", "timp"], [(0, -8), (3, -6), (4, -8), (8, -16)])
    # calm: D major strings + rising harp glissando exactly on the end of the line
    gliss(b, "harp", 0, 0.65, midi("D3"), midi("D6"), v0=36, v1=72)
    b.pad(["vla", "vln2", "vln1"], 3, 57, 78, vel=54, bass_part="vc", bass_lo=38, bass_hi=50)
    b.add("cb", 0, 4, "D2", 48, "bass")
    # the great fish: tuba + contrabass, doubled four octaves up by glockenspiel
    b.mel("tuba", "r:1/2 D2:1/2:s F#2:1/2:s A2:1/2:s B2:1 A2:1/2:s F#2:1/2:s", vel=86)
    b.mel("contrab", "r:1/2 D2:1/2:s F#2:1/2:s A2:1/2:s B2:1 A2:1/2:s F#2:1/2:s", vel=66)
    b.mel("glock", "r:1/2 D6:1/2 F#6:1/2 A6:1/2 B6:1 A6:1/2 F#6:1/2", vel=68)
    b.sync("fish motif enters", 0.5, c.ls(1))
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -9), (1, -6), (4, -7)])
    b.expr(["tuba", "contrab", "glock", "harp"], [(0, -4), (4, -4)])
    # gulp: small accent, then the bass sinks D-C#-B into the dark belly
    g.mel("tuba", "D2:1:a C#2:1 B1:1", vel=92, role="bass")
    g.mel("contrab", "D2:1:a C#2:1 B1:1", vel=72, role="bass")
    g.add("timp", 0, 0.5, "D2", 88, "timp", "h")
    g.add("pz_lo", 0, 0.5, "D3", 84, "bass", "h")
    g.add("pz_cb", 0, 0.5, "D2", 90, "bass", "h")
    g.mel("glock", "A6:1/2 D6:1/2", vel=70)
    g.pad(["vla", "vln2", "vln1"], 3, 54, 74, vel=46, bass_ref=(35, 47))
    g.expr(["vla", "vln2", "vln1", "tuba", "contrab"], [(0, -6), (3, -14)])


def belly(c):
    tp, ts = c.gap(2), c.gap(3)
    a = c.seg(0, tp, 2, "3/4", "B minor", nominal=60, label="belly-dark")
    b = c.seg(tp, ts, 1, "4/4", "D major", nominal=60, label="belly-prayer")
    e = c.seg(ts, c.dur, 1, "2/4", "D major", nominal=60, label="belly-salvation")
    a.prog("Bm:3 | Em/B:3")
    b.prog("G:2 Em7:1 A:1")
    e.prog("D:2")
    b.sync("hopeful turn (choir) on Jonah's prayer", 0, tp)
    e.sync("D major swell on '救恩属于耶和华'", 0, ts)
    # darkness: warm pad, low drone, sparse echoing celesta drops
    a.pad("pad", 3, 50, 69, vel=60, bass_ref=(35, 47))
    a.add("cb", 0, 6, "B1", 54, "bass")
    a.mel("vc", "F#2:3 | G2:3", vel=44, role="bass")
    for q, nm in [(0.5, "F#6"), (1.75, "D6"), (4.5, "E6"), (5.5, "B5")]:
        a.add("echo_cel", q, 0.5, nm, 62, "melody", "r")
    fill(c, "echo_cel", c.pause_or_gap(1), n=2, lo=79, hi=93, vel=60, up=False)   # a drop in the pause
    a.expr(["pad", "cb", "vc"], [(0, -12), (6, -12)])
    a.expr("echo_cel", [(0, -4), (6, -4)])
    # prayer: the pad brightens, choir enters, strings join
    b.pad("pad", 3, 50, 69, vel=60, bass_ref=(40, 52))
    b.pad("choir", 3, 57, 76, vel=58, tops=[midi("B4"), midi("B4"), midi("C#5")], bass_ref=(40, 52))
    b.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=44, bass_part="vc", bass_lo=40, bass_hi=52)
    b.mel("cb", "G1:2 E1:1 A1:1", vel=50, role="bass")
    b.add("harp", 0, 2, "G3", 42, "arp")
    b.add("harp", 0.5, 1.5, "D4", 40, "arp")
    b.add("harp", 1.0, 1.0, "B4", 40, "arp")
    b.expr(["pad", "choir", "vla", "vln2", "vln1", "vc", "cb"], [(0, -18), (2, -12), (4, -10)])
    # salvation: D major, choir and strings swell (V of the shore's G major)
    # V -> I with the cellos rising A2 -> D3 alongside the basses (A1 -> D2); every pad continues
    # from its own voicing in b, checked against that bass
    e.pad("pad", 3, 50, 69, vel=60, bass_ref=(48, 60))
    e.pad("choir", 3, 57, 76, vel=66, tops=[midi("D5")], bass_ref=(48, 60))
    e.pad(["vla", "vln2", "vln1"], 3, 55, 78, vel=54, bass_part="vc", bass_lo=48, bass_hi=60)
    e.add("cb", 0, 2, "D2", 54, "bass")
    broken(e, "harp", 0, 2, (0, 2, 4, 5, 6, 7, 8, 9), 38, 49, vel=42, step=0.25)
    e.expr(["pad", "choir", "vla", "vln2", "vln1", "vc", "cb"], [(0, -10), (1, -7), (2, -9)])


def shore(c):
    s = c.seg(0, c.dur, 4, "2/4", "G major", nominal=108, label="shore")
    s.prog("G:2 | C:2 | G/D:1 D7:1 | D7:2")
    # the Jonah motif (3-2-1-5) made bouncy: he is safe on dry land
    s.mel("flute", "B5:1/2:s A5:1/4:s G5:1/4:s D5:1/2:s G5:1/2:s | C6:1/2:s B5:1/4:s C6:1/4:s G5:1/2:s E5:1/2:s | "
                   "B5:1/2:s G5:1/2:s A5:1/2:s F#5:1/2:s | C6:1/4:s B5:1/4:s A5:1/2:s F#5:1/2 D5:1/2", vel=84)
    s.mel("glock", "B6:1 r:1 | C7:1 r:1 | B6:1 A6:1 | C7:1 r:1", vel=64)
    s.mel("pz_lo", "G2:1/2 r:1/2 D3:1/2 r:1/2 | C3:1/2 r:1/2 G2:1/2 r:1/2 | D3:1/2 r:1/2 D2:1/2 r:1/2 | "
                   "D2:1/2 r:1/2 A2:1/2 r:1/2", vel=72, role="bass")
    s.mel("pz_hi", "r:1/2 [G4,B4,D5]:1/2 r:1/2 [G4,B4,D5]:1/2 | r:1/2 [G4,C5,E5]:1/2 r:1/2 [G4,C5,E5]:1/2 | "
                   "r:1/2 [G4,B4,D5]:1/2 r:1/2 [F#4,A4,C5]:1/2 | r:1/2 [F#4,A4,C5]:1/2 r:1/2 [F#4,A4,C5]:1/2",
          vel=56, role="harmony")
    s.expr(["flute", "glock", "pz_lo", "pz_hi"], [(0, -3), (8, -3)])


def nineveh(c):
    t40 = c.gap(2)
    a = c.seg(0, t40, 3, "4/4", "D hijaz", nominal=96, label="nineveh-walk")
    b = c.seg(t40, c.dur, 1, "4/4", "D hijaz", nominal=66, rit=0.15, label="nineveh-forty-days")
    a.prog("D:4 | Gm:2 Cm:2 | Eb:2 D:2")
    b.prog("Gm/D:2 D:2")
    b.sync("solemn chord under 'forty days'", 0, t40)
    a.mel("oboe", "A5:3/2 Bb5:1/2 A5:1 G5:1/2 F#5:1/2 | G5:1 A5:1/2 Bb5:1/2 C6:1 Bb5:1/2 A5:1/2 | "
                  "G5:1 F#5:1/2 Eb5:1/2 D5:2", vel=82)
    a.mel("guitar", "D3:1/2 D3:1/4 Eb3:1/4 F#3:1/2 G3:1/2 A3:1/2 G3:1/4 F#3:1/4 Eb3:1/2 D3:1/2 | "
                    "G2:1/2 D3:1/4 G3:1/4 Bb3:1/2 A3:1/2 C3:1/2 G3:1/4 C4:1/4 Eb4:1/2 C4:1/2 | "
                    "Eb3:1/2 Bb2:1/4 Eb3:1/4 G3:1/2 F#3:1/2 D3:1/2 A2:1/4 D3:1/4 F#3:1/2 Eb3:1/4 D3:1/4",
          vel=70, role="counter")
    a.mel("pz_cb", "D2:1 A1:1 D2:1 A1:1 | G1:1 D2:1 C2:1 G1:1 | Eb2:1 Bb1:1 D2:1 A1:1", vel=72, role="bass")
    # maqsum: DUM tek . tek DUM . tek ka-ka  (+ light tambourine)
    for bar in range(3):
        o = bar * 4
        for q, key, v in [(0, 45, 92), (0, 64, 70), (0.5, 60, 62), (1.5, 60, 70), (2, 45, 84), (2, 64, 64),
                          (3, 60, 66), (3.5, 61, 52), (3.75, 61, 44)]:
            drum(a, o + q, key, v)
        for q in (0.5, 1.5, 2.5, 3.5):
            drum(a, o + q, 54, 34)
    a.expr(["oboe", "guitar", "pz_cb", "hand"], [(0, -5), (12, -5)])
    # "forty days": sustained solemn chord, slow low drum
    b.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=56, bass_part="vc", bass_lo=43, bass_hi=55)
    b.add("cb", 0, 4, "D2", 56, "bass")
    b.pad("horn", 2, 50, 66, vel=60, bass_ref=(43, 55))
    drum(b, 0, 45, 70)
    drum(b, 2, 45, 56)
    b.expr(["vla", "vln2", "vln1", "vc", "cb", "horn"], [(0, -12), (1.5, -5), (4, -9)])


def repent(c):
    tm = c.gap(2)
    a = c.seg(0, tm, 2, "4/4", "G minor+", nominal=74, label="repent-solemn")
    t_b2 = tm + (c.dur - tm) * 4 / 6
    b1 = c.seg(tm, t_b2, 1, "4/4", "G major", nominal=76, label="repent-mercy")
    b2 = c.seg(t_b2, c.dur, 1, "2/4", "G major", nominal=76, rit=0.2, label="repent-half-cadence")
    a.prog("Gm:2 Eb:2 | Cm:2 D:2")
    b1.prog("G:2 Em:2")
    b2.prog("C:1 D:1")
    b1.sync("mercy: G major", 0, tm)
    va = a.pad("choir", 3, 55, 76, vel=58, tops=[midi(x) for x in ("D5", "Eb5", "Eb5", "D5")], bass_ref=(43, 55))
    a.pad(["vla", "vln2"], 2, 53, 70, vel=48, bass_part="vc", bass_lo=43, bass_hi=55)
    a.mel("cb", "G1:2 Eb2:2 | C2:2 D2:2", vel=52, role="bass")
    vb = b1.pad("choir", 3, 55, 76, vel=62, tops=[midi("D5"), midi("E5")], prev=va[-1], bass_ref=(43, 55))
    b2.pad("choir", 3, 55, 78, vel=60, tops=[midi("E5"), midi("F#5")], prev=vb[-1], bass_ref=(43, 55))
    for seg in (b1, b2):
        seg.pad(["vla", "vln2"], 2, 53, 70, vel=52, bass_part="vc", bass_lo=43, bass_hi=55)
    b1.mel("cb", "G1:2 E2:2", vel=52, role="bass")
    b2.mel("cb", "C2:1 D2:1", vel=52, role="bass")
    b1.mel("vln_mel", "B5:3/2 A5:1/2 G5:2", vel=64)
    b2.mel("vln_mel", "G5:1 F#5:1", vel=64)        # not G5-A5 over C2-D2 (outer-voice fifths)
    broken(b1, "harp", 0, 4, (0, 2, 3, 4, 5, 6, 5, 4), 43, 54, vel=46)
    broken(b2, "harp", 0, 2, (0, 2, 3, 4), 36, 50, vel=44)
    b1.mel("celesta", "r:1/2 B6:1/2 r:1 r:1/2 G6:1/2 r:1", vel=40)
    b2.add("bsn", 1.5, 0.5, "D3", 56, "melody", "s")       # grumpy pickup into the vine
    fill(c, "harp", c.pause_or_gap(1), n=3, lo=62, hi=82, vel=44)
    fill(c, "celesta", c.pause_or_gap(len(c.lines) - 1), n=3, lo=79, hi=96, vel=44)
    a.expr(["choir", "vla", "vln2", "vc", "cb"], [(0, -12), (4, -8), (8, -6)])
    b1.expr(["choir", "vla", "vln2", "vc", "cb", "vln_mel", "harp", "celesta"], [(0, -6), (4, -5)])
    b2.expr(["choir", "vla", "vln2", "vc", "cb", "vln_mel", "harp"], [(0, -5), (2, -9)])


def vine(c):
    t_grow, t_worm, t_heat = c.gap(1), c.gap(3), c.gap(4)
    # the waltz (two quick bars of 3/4) starts when "...为他遮阴" has ended -- never before, so the
    # growth music is not cut off while the growth is narrated -- and at the latest in the pause
    # before "约拿非常喜乐"
    t_waltz = min(max(t_worm - 6 * 60 / 190, t_grow + 2.4, c.le(1)), c.gap(2))
    v0 = c.seg(0, t_grow, 3, "2/4", "G minor", nominal=84, label="vine-grumpy")
    v1 = c.seg(t_grow, t_waltz, 2, "3/4", "G minor", nominal=120, label="vine-grow")
    v2 = c.seg(t_waltz, t_worm, 2, "3/4", "G major", nominal=195, label="vine-waltz")
    v3 = c.seg(t_worm, t_heat, 2, "4/4", "G minor", nominal=130, label="vine-worm")
    v4 = c.seg(t_heat, c.dur, 1, "4/4", "D mixolydian", nominal=66, label="vine-heat")
    v0.prog("Gm:2 | Cm7:2 | D7:2@G-harmonic")
    v1.prog("Eb:3 | F:3/2 G:3/2@G-major")
    v2.prog("G:3 | D7:3")
    v3.prog("Gm:4 | D7:2@G-harmonic D:2@G-harmonic")
    v4.prog("Dsus2:4")
    v1.sync("plant grows: rising arpeggios", 0, t_grow)
    v2.sync("happy waltz", 0, t_waltz)
    v3.sync("worm: chromatic pizzicato", 0, t_worm)
    v4.sync("heat: harmonics + slow drum", 0, t_heat)
    # grumpy Jonah: staccato bassoon grumble over stomping pizzicato
    v0.mel("bsn", "G2:3/4:s D3:1/4:s Bb2:1/2:s G2:1/2:s | Eb3:1/2:s D3:1/4:s C3:1/4:s Bb2:1/2:s G2:1/2:s | "
                  "F#2:1/2:s A2:1/4:s C3:1/4:s D3:1/2:a r:1/2", vel=76)
    v0.mel("pz_cb", "G1:1/2:a r:1/2 G1:1/2 r:1/2 | C2:1/2:a r:1/2 C2:1/2 r:1/2 | D2:1/2:a r:1/2 D2:1/2 r:1/2",
           vel=74, role="bass")
    v0.mel("pz_lo", "r:1/2 [G2,D3]:1/2 r:1/2 [G2,D3]:1/2 | r:1/2 [C3,G3]:1/2 r:1/2 [C3,G3]:1/2 | "
                    "r:1/2 [D3,A3]:1/2 r:1/2 [D3,C4]:1/2", vel=54, role="harmony")
    v0.expr(["bsn", "pz_cb", "pz_lo"], [(0, -4), (6, -4)])
    # the plant grows: rising harp + celesta arpeggios over swelling strings (bVI - bVII - I)
    broken(v1, "harp", 0, 6, tuple(range(12)), 39, 50, vel=48, step=0.25, accent=4, restart=True)
    for q0, q1, ch in v1.chord_spans():
        lad = [p for p in ch.tones(72, 100)]
        n = int(round((q1 - q0) / 0.25))
        for k in range(n):
            v1.add("celesta", q0 + k * 0.25, q1 - q0 - k * 0.25, lad[min(k, len(lad) - 1)], 48 + 2 * k, "arp")
    v1.pad(["vla", "vln2", "vln1"], 3, 58, 79, vel=50, bass_part="vc", bass_lo=48, bass_hi=60)
    v1.mel("cb", "Eb2:3 | F2:3/2 G2:3/2", vel=50, role="bass")
    v1.add("glock", 4.5, 1.5, "G6", 54, "arp", "r")
    v1.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (6, -5)])
    v1.expr(["harp", "celesta"], [(0, -6), (6, -3)])
    # "约拿非常喜乐": a happy little waltz
    v2.mel("flute", "D5:1 G5:1/2 A5:1/2 B5:1 | C6:1 B5:1/2 A5:1/2 F#5:1", vel=72)
    v2.mel("glock", "G6:1 r:2 | F#6:1 r:2", vel=48)
    v2.mel("pz_lo", "G2:1 r:2 | D2:1 r:2", vel=70, role="bass")
    v2.mel("pz_hi", "r:1 [B3,D4,G4]:1 [B3,D4,G4]:1 | r:1 [A3,C4,F#4]:1 [A3,C4,F#4]:1", vel=52, role="harmony")
    v2.expr(["flute", "glock", "pz_lo", "pz_hi"], [(0, -3), (6, -3)])
    # the worm: descending chromatic pizzicato, the plant withers onto D
    v3.mel("pz_hi", "D5:1/2 C#5:1/2 C5:1/2 B4:1/2 Bb4:1/2 A4:1/2 Ab4:1/2 G4:1/2 | "
                    "F#4:1/2 F4:1/2 E4:1/2 Eb4:1/2 D4:2", vel=66, role="chromatic")
    v3.mel("pz_lo", "G2:1 r:1 D3:1 r:1 | D2:2 r:2", vel=60, role="bass")
    v3.mel("clar", "Bb3:4 | A3:4", vel=44)
    v3.expr(["pz_hi", "pz_lo", "clar"], [(0, -4), (8, -9)])
    # heat: a thin, airy open fifth (violins E5/A5 at low expression, a hushed 'ooh' choir on D4/A4),
    # basses on D, and a slow, soft, dry low drum
    v4.add("vln1", 0, 4, "E5", 58, "pad", voice="vln1.0")
    v4.add("vln1", 0, 4, "A5", 60, "pad", voice="vln1.1")
    v4.add("ooh", 0, 4, "D4", 54, "pad", voice="ooh.0")
    v4.add("ooh", 0, 4, "A4", 52, "pad", voice="ooh.1")
    v4.add("cb", 0, 4, "D2", 48, "bass")
    drum(v4, 0, 45, 64)
    drum(v4, 2, 45, 56)
    drum(v4, 3.5, 61, 34)
    v4.add("piano", 3.5, 0.5, "D5", 54, "melody")          # the theme's anacrusis returns
    v4.expr(["vln1", "ooh", "cb"], [(0, -10), (1.5, -7), (3.5, -6), (4, -6)])


def lesson(c):
    s = c.seg(0, c.dur, 6, "6/8", "G major", nominal=72, rit=0.3, rit_q=3, label="lesson")
    s.prog("G:3 | C:3 | Am7:3/2 D7:3/2 | Dsus4:3/2 D:3/2 | G:3 | C:3/2 A7:3/2@D-major")
    # the Jonah theme in G, slowly, on piano; ends on the 7th of A7 (a question)
    s.mel("piano", "B5:1 A5:1/2 G5:1 D5:1/2 | E5:1 G5:1/2 C6:1 B5:1/2 | A5:3/2 F#5:1 G5:1/2 | "
                   "A5:5/2 D5:1/2 | B5:1 A5:1/2 G5:1 D5:1/2 | E5:1 G5:1/2 A5:1/2 G5:1", vel=66)
    # God is speaking almost throughout: dotted-quarter pulses under the words, full eighths in pauses
    broken(s, "piano", 0, 18, (0, 2, 4, 5, 4, 2), 43, 54, vel=34, accent=6, role="arp", thin=True)
    s.pad(["vla", "vln2", "vln2"], 3, 52, 71, vel=48, bass_part="vc", bass_lo=43, bass_hi=55)
    s.mel("cb", "G1:3 | C2:3 | A1:3/2 D2:3/2 | D2:3 | G1:3 | C2:3/2 A1:3/2", vel=46, role="bass")
    s.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (3, -8), (12, -6), (18, -8)])
    s.expr("piano", [(0, -7), (3, -3), (15, -3), (18, -5)])


def end(c):
    t_cad = min(c.le(len(c.lines) - 1) + 0.03, c.dur - 2.0)
    a = c.seg(0, t_cad, 3, "6/8", "D major", nominal=78, rit=0.12, label="end-theme")
    b = c.seg(t_cad, c.dur, 1, "6/8", "D major", nominal=56, label="end-final-chord")
    a.prog("D:3 | G:3 | D/A:3/2 A7:3/2")
    b.prog("D:3")
    b.sync("final D major cadence", 0, t_cad)
    # the theme on violins, kept gentle under the two closing lines; the celesta doubles it only
    # where nobody speaks, and returns for the fills and the cadence
    a.mel("vln_mel", "F#5:1 E5:1/2 D5:1 A4:1/2 | B4:1 D5:1/2 G5:1 B5:1/2 | A5:1 F#5:1/2 E5:1 C#5:1/2", vel=76)
    b.add("vln_mel", 0, 3, "D5", 80, "melody")
    drop_spoken(a.mel("celesta", "F#6:1 E6:1/2 D6:1 A5:1/2 | B5:1 D6:1/2 G6:1 B6:1/2 | A6:1 F#6:1/2 E6:1 C#6:1/2",
                      vel=56))
    b.mel("celesta", "D6:1 r:1/2 F#6:1/2 A6:1/2 D7:1/2", vel=50, art="r")
    a.mel("horn", "A4:3 | G4:3/2 B4:3/2 | F#4:3/2 G4:3/2", vel=56, role="counter")
    b.add("horn", 0, 3, "F#4", 66, "counter")
    broken(a, "harp", 0, 9, (0, 2, 4, 6, 4, 2), 38, 49, vel=46, thin=True)
    fill(c, "celesta", c.pause_or_gap(1), n=3, lo=86, hi=100, vel=46)
    for k, nm in enumerate(["D2", "A2", "D3", "F#3", "A3", "D4", "F#4", "A4", "D5"]):
        b.add("harp", 0.12 * k, 3, nm, 58 - 2 * k, "arp", "r")
    a.pad(["vla", "vln2", "vln2"], 3, 52, 71, vel=56, bass_part="vc", bass_lo=43, bass_hi=55)
    b.pad(["vla", "vln2", "vln2"], 3, 54, 71, vel=56, bass_part="vc", bass_lo=43, bass_hi=55)
    a.mel("cb", "D2:3 | G1:3 | A1:3", vel=54, role="bass")
    b.add("cb", 0, 3, "D2", 56, "bass")
    # no crescendo under the closing line: the swell belongs to the final chord alone
    q_le1 = a.q_of(c.t0 + c.le(len(c.lines) - 1))
    a.expr(["vla", "vln2", "vc", "cb", "vln_mel", "horn"], [(0, -8), (min(q_le1, 8.9), -8), (9, -5)])
    b.expr(["vla", "vln2", "vc", "cb", "vln_mel", "horn"], [(0, -4), (0.75, -1), (1.5, -2), (3, -24)])
    a.expr(["harp", "celesta"], [(0, -4), (9, -3)])
    b.expr(["harp", "celesta"], [(0, -3), (3, -6)])


CUES = {"title": title, "call": call, "flee": flee, "storm": storm, "lots": lots, "fish": fish,
        "belly": belly, "shore": shore, "nineveh": nineveh, "repent": repent, "vine": vine,
        "lesson": lesson, "end": end}


def build(timeline, passes=3):
    """Compose the score.  Pads are voice-led against the complete score of the previous pass
    (melodies, counter-melodies, basses and other pads written anywhere in the cue), so they avoid
    parallel fifths/octaves with lines that are written after them; the passes are deterministic."""
    guides = None
    for _ in range(passes):
        sc = Score(timeline)
        sc.guide_notes = guides
        scenes = timeline["scenes"]
        for i, s in enumerate(scenes):
            t1 = scenes[i + 1]["start"] if i + 1 < len(scenes) else timeline["duration"]
            CUES[s["mood"]](Cue(sc, s, t1))
        guides = sc.guide_index()
    return sc
