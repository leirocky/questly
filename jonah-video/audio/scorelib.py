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
