"""Shared writing helpers for the cue modules (audio/cues_*.py)."""
import numpy as np

from audio.theory import midi

STR_UP = ["vla", "vln2", "vln1"]


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
    thin=True: while a line is being spoken only the beats are played; the full figure returns in
    the pauses."""
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


class ChordTones:
    """A 'scale' of one chord's tones: gliss(..., scale=ChordTones(ch)) sweeps an arpeggio (a harp glissando
    with the pedals set to the chord)."""

    def __init__(self, ch):
        self.pcs = frozenset(ch.pcset)

    def degree_pitches(self, lo, hi):
        return [p for p in range(lo, hi + 1) if p % 12 in self.pcs]


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


def timp_pitch(ch, pitch, lo=38, hi=57):
    """pitch if it belongs to the chord, else the chord's bass (or nearest chord tone) in the drum range."""
    if pitch % 12 in ch.pcset:
        return pitch
    bass = [p for p in range(lo, hi + 1) if p % 12 == ch.bass]
    pool = bass or [p for p in range(lo, hi + 1) if p % 12 in ch.pcset]
    return min(pool, key=lambda p: abs(p - pitch))


def timp_roll(seg, q0, q1, pitch, v0, v1, rate=13.0):
    """Timpani roll; across a chord change it re-tunes to a tone of the new chord (its bass if possible)."""
    t0, t1 = seg.t(q0), seg.t(q1)
    n = max(2, int((t1 - t0) * rate))
    for k in range(n):
        tk = t0 + k * (t1 - t0) / n
        v = v0 + (v1 - v0) * k / (n - 1) + (3 if k % 2 else -3)
        qk = seg.q_of(tk)
        seg.add("timp", qk, (q1 - q0) / n, timp_pitch(seg.chord_at(qk + 1e-3), pitch), v, "timp")


def roll(seg, q0, q1, key, v0, v1, part="okit", rate=14.0, accel=1.0):
    """Unpitched roll / rattle from q0 to q1 (accel > 1: strokes get denser towards the end)."""
    t0, t1 = seg.t(q0), seg.t(q1)
    n = max(2, int((t1 - t0) * rate))
    for k in range(n):
        x = k / n
        tk = t0 + (t1 - t0) * (x ** accel)
        v = v0 + (v1 - v0) * k / (n - 1) + (2 if k % 2 else -2)
        seg.add(part, seg.q_of(tk), 0.1, key, v, "perc")


def fill(cue, part, pause, n=3, lo=72, hi=96, vel=48, up=True, frac=0.85):
    """A soft chord-tone figure inside a narration pause (cue-relative (start, end))."""
    a, b = pause
    t0 = cue.t0 + a + 0.03
    seg = next((sg for sg in cue.segs if sg.t0 <= t0 < sg.t1), None)
    if seg is None:
        return
    dt = (b - a) * frac / n
    ch = seg.chord_at(seg.q_of(t0))
    tones = ch.tones(lo, hi)
    start = len(tones) // 3
    pick = tones[start:start + n] if up else tones[start:start + n][::-1]
    echo = part == "echo_cel"
    for k, pch in enumerate(pick):
        tk = t0 + k * dt
        if tk >= seg.t1 - 0.02:
            break
        qk = seg.q_of(tk)
        if seg.chord_at(qk) is not ch:
            break
        dq = span_end(seg, qk) - qk
        if echo and not _tail_fits(seg, qk, dq, pch, ECHO_TAIL):
            # the echo would ring on into the next chord: use a tone the two chords share
            alt = [p for p in tones if _tail_fits(seg, qk, dq, p, ECHO_TAIL)]
            if not alt:
                continue
            pch = min(alt, key=lambda p: abs(p - pch))
        seg.add(part, qk, dq, pch, vel + 4 * k, "arp")


def drum(seg, q, key, vel, part="hand"):
    seg.add(part, q, 0.25, key, vel, "perc")


def bassline(seg, part, lo, hi, vel, q0=0.0, q1=None, art="", tie=True, role="bass"):
    """Chord basses (lowest bass pitch-class in [lo, hi]) for every chord span; repeated pitches tie."""
    cur = None
    out = []
    for a, b, ch in seg.chord_spans(q0, q1):
        p = ch.bass_note(lo, hi)
        if tie and cur is not None and cur.pitch == p and abs(cur.q + cur.dq - a) < 1e-6:
            cur.dq = b - cur.q
            continue
        cur = seg.add(part, a, b - a, p, vel, role, art)
        out.append(cur)
    return out


def pulse(seg, part, q0, q1, step, vel, lo, hi, idx=0, art="s", role="arp", accent=0, every=None):
    """Repeated chord tone (ladder index idx from the bass in [lo, hi]) every `step` q."""
    q, k = q0, 0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q)
        lad = ladder(ch, lo, hi)
        v = vel + (accent if every and k % every == 0 else 0)
        seg.add(part, q, step, lad[min(idx, len(lad) - 1)], v, role, art)
        q += step
        k += 1


def sustain_q(seg, t_rel_cue):
    """q inside seg of a cue-relative time."""
    return seg.q_of(seg.cue.t0 + t_rel_cue)


def tops(*names):
    return [midi(x) for x in names]


ECHO_TAIL = 1.5      # s: the echo bus (music.py, 0.5 s ping-pong) repeats a note for about this long
RING = 0.6           # s: a let-ring ('r') note sounds this long past its written end (Score.perform)


def _tail_fits(seg, q, dq, pitch, tail):
    """True when a note at q (dq quarters + tail seconds of ring/echo) sounds only over chords of
    this cue that contain its pitch class."""
    t_a, t_b = seg.t(q), seg.t(q + dq) + tail
    if t_b > seg.cue.t1 - 0.05:              # the next cue's harmony is not known yet
        return False
    for sg in seg.cue.segs:
        for a, b, ch, _ in sg.chords:
            ov = min(sg.t(b), t_b) - max(sg.t(a), t_a)
            if ov > 0.05 and pitch % 12 not in ch.pcset:
                return False
    return True


def echo_drop(seg, q, pitch, vel, dq=0.5, art="r", part="echo_cel", earliest=None):
    """An echoing celesta drop at q, or at the latest quarter-step before it (down to `earliest`,
    default q - 2) whose ring and echo tail stay over chords containing the pitch; else none."""
    pitch = midi(pitch) if isinstance(pitch, str) else int(pitch)
    tail = (ECHO_TAIL if part == "echo_cel" else 0.0) + (RING if "r" in art else 0.0)
    lo = max(0.0, q - 2.0 if earliest is None else earliest)
    qq = q
    while qq >= lo - 1e-9:
        if _tail_fits(seg, qq, dq, pitch, tail):
            return seg.add(part, qq, dq, pitch, vel, "arp", art)
        qq -= 0.25
    return None
