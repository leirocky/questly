"""Automated checks of the rendered score -> build/preview/music_report.txt + music_spectrogram.png.

Harmony check: every pitched note is tested against its segment's scale(s) and the chord that is
sounding.  Harmonic roles (pad, bass, arp, harmony, timpani) must be chord tones for every chord
they sound through.  Melodic roles may use non-chord tones only when they behave like real
non-chord tones (passing, neighbour, suspension, appoggiatura, anticipation, escape, or short
unaccented notes); chromatic notes are allowed only as chromatic passing/neighbour notes.  Notes
are also judged by how long they really sound: a let-ring note (+0.6 s) or a celesta drop on the
echo bus (+1.5 s of repeats) must not ring on over a chord that does not contain it.

Levels are K-weighted (ITU-R BS.1770 LUFS, pyloudnorm): integrated loudness per cue and per
storm section, and short-term (3 s) loudness for the loudest moment of every cue.

Story projects: the hit-point lists and the level checks below (storm loudest, belly quietest, ...) are the
Jonah film's.  For another story (engine.paths.STORY != "jonah") the hit points come from the story's own
stories/<name>/cues.py (REQUIRED_HITS, optional PICTURE_HITS; none if absent), the Jonah level checks are
skipped (a general "no cue far above the median cue" check replaces them) and every general check stays:
duration, clipping, cue tiling, hand-offs, silences, speech-to-music ratio, hit audibility, harmony, clashes,
ranges, parallels.  The report goes to <the story's BUILD>/preview/.
"""
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import soundfile as sf

from audio.scorekit import PARTS, ROLE_STRICT
from audio.theory import name, parallels

STRONG = {"4/4": (0.0, 2.0), "3/4": (0.0,), "2/4": (0.0,), "6/8": (0.0, 1.5), "3/8": (0.0,), "12/8": (0.0, 3.0)}
MELODIC = {"melody", "counter", "chromatic", "fx"}


def _is_step(a, b, scales):
    d = abs(a - b)
    if d in (1, 2):
        return True
    if d == 3:   # augmented second between adjacent degrees (hijaz / harmonic minor)
        lo, hi = min(a, b), max(a, b)
        return any(lo in s and hi in s and not any((p in s) for p in range(lo + 1, hi)) for s in scales)
    return False


def _overlapping_chords(n):
    q0, q1 = n.q, n.q + n.dq
    out = []
    for a, b, ch, _ in n.seg.chords:
        ov = min(b, q1) - max(a, q0)
        if ov > 1e-6:
            out.append((max(a, q0), ov, ch))
    return out


ECHO_TAIL = 1.5      # s of audible repeats on the echo bus (music.py: 0.5 s ping-pong, -7.5 dB per repeat)


def sounding_end(n):
    """When a performed note stops sounding: its rendered end (articulation, let-ring) plus the
    echo bus's repeats."""
    return n.t + n.d + (ECHO_TAIL if PARTS[n.part].bus == "echo" else 0.0)


def chord_timeline(sc):
    """[(t0, t1, Chord)] of the whole score in time order."""
    out = [(s_.t(a), s_.t(b), ch) for c in sc.cues for s_ in c.segs for a, b, ch, _ in s_.chords]
    out.sort(key=lambda x: x[0])
    return out


def chords_between(timeline, t0, t1, min_ov=0.0):
    """[(overlap s, Chord)] of the chords sounding between t0 and t1."""
    import bisect
    starts = [x[0] for x in timeline]
    i = max(0, bisect.bisect_right(starts, t0) - 1)
    out = []
    while i < len(timeline) and timeline[i][0] < t1:
        a, b, ch = timeline[i]
        ov = min(b, t1) - max(a, t0)
        if ov > min_ov:
            out.append((ov, ch))
        i += 1
    return out


def check_harmony(sc):
    stats = Counter()
    viol = []
    ctl = chord_timeline(sc)
    # ring and echo tails: what still sounds after the written end must fit the chords it meets
    for n in sc.notes:
        if PARTS[n.part].drum or n.role in ("perc", "gliss"):
            continue
        tw, te = n.seg.t(n.q + n.dq), sounding_end(n)
        if te - tw <= 0.15:
            continue
        stats["notes with a let-ring / echo tail"] += 1
        bad = sorted({ch.sym for ov, ch in chords_between(ctl, tw, te, 0.15) if n.pitch % 12 not in ch.pcset})
        if bad:
            viol.append((n, f"{n.seg.cue.id}/{n.seg.label} q={n.q:.2f} {n.part} {name(n.pitch)} ({n.role}): its "
                            f"{'echo' if PARTS[n.part].bus == 'echo' else 'let-ring'} tail ({te - tw:.1f} s) rings on "
                            f"over {bad}"))
    lines = defaultdict(list)
    for n in sc.notes:
        if PARTS[n.part].drum or n.role == "perc":
            continue
        lines[(n.part, n.role in MELODIC)].append(n)
    for lst in lines.values():
        lst.sort(key=lambda n: (n.seg.t(n.q), -n.pitch))
    neighbours = {}
    for (part, melodic), lst in lines.items():
        if not melodic:
            continue
        for i, n in enumerate(lst):
            t = n.seg.t(n.q)
            prev = lst[i - 1] if i > 0 else None
            nxt = lst[i + 1] if i + 1 < len(lst) else None
            if prev is not None and t - prev.seg.t(prev.q + prev.dq) > 0.6:
                prev = None
            if nxt is not None and nxt.seg.t(nxt.q) - n.seg.t(n.q + n.dq) > 0.6:
                nxt = None
            neighbours[id(n)] = (prev, nxt)

    for n in sc.notes:
        if PARTS[n.part].drum or n.role == "perc":
            continue
        stats["notes"] += 1
        scales = n.seg.scales_at(n.q)
        in_scale = any(n.pitch in s for s in scales)
        chords = _overlapping_chords(n)
        if not chords:
            viol.append((n, f"{n.seg.cue.id}/{n.seg.label} q={n.q:.2f} {n.part} {name(n.pitch)}: no chord defined"))
            continue
        ch0 = n.seg.chord_at(n.q)
        is_ct = n.pitch % 12 in ch0.pcset
        where = f"{n.seg.cue.id}/{n.seg.label} bar {int(n.q // n.seg.bar_q) + 1} beat {n.q % n.seg.bar_q + 1:.2f}"
        desc = f"{where} {n.part:8s} {name(n.pitch):4s} over {ch0.sym:7s} ({n.role})"
        if n.role == "gliss":
            n.nct = "gliss"
            stats["gliss (scale only)"] += 1
            if not in_scale:
                viol.append((n, desc + " glissando note outside scale"))
            continue
        if n.role in ROLE_STRICT:
            bad = [c.sym for _, ov, c in chords if n.pitch % 12 not in c.pcset and ov > 0.12]
            if n.role == "timp" and not is_ct and ch0.sym not in bad:      # roll strokes are short:
                bad.append(ch0.sym)                                         # judge them at the onset
            if bad:
                viol.append((n, desc + f" harmonic-role note not in chord(s) {bad}"))
            else:
                stats["chord tone (harmonic role)"] += 1
            continue
        # melodic roles -----------------------------------------------------
        prev, nxt = neighbours.get(id(n), (None, None))
        pp = prev.pitch if prev else None
        np_ = nxt.pitch if nxt else None
        if is_ct:
            stats["chord tone (melodic)"] += 1
            # held into a chord where it does not belong -> must resolve by step (suspension)
            for q, ov, c in chords[1:]:
                if n.pitch % 12 not in c.pcset and ov > 0.3 * n.seg.beat_q:
                    if np_ is not None and _is_step(n.pitch, np_, scales):
                        stats["suspension (held over chord change)"] += 1
                    else:
                        viol.append((n, desc + f" held over {c.sym} without resolution"))
            continue
        strong = any(abs((n.q % n.seg.bar_q) - s) < 1e-6 for s in STRONG[n.seg.meter])
        short = n.dq <= 0.5 * n.seg.beat_q + 1e-6
        kind = None
        if not in_scale:
            if pp is not None and np_ is not None and abs(pp - n.pitch) == 1 and abs(n.pitch - np_) == 1 \
                    and (pp - n.pitch) * (n.pitch - np_) > 0:
                kind = "chromatic passing"
            elif pp is not None and pp == np_ and abs(pp - n.pitch) == 1:
                kind = "chromatic neighbour"
            if kind is None:
                viol.append((n, desc + " OUT OF SCALE and not a chord tone"))
                continue
        else:
            sp = pp is not None and _is_step(pp, n.pitch, scales)
            sn = np_ is not None and _is_step(n.pitch, np_, scales)
            if sp and sn and (pp - n.pitch) * (n.pitch - np_) > 0:
                kind = "passing"
            elif sp and sn and pp == np_:
                kind = "neighbour"
            elif pp == n.pitch and sn:
                kind = "suspension"
            elif sn and pp is not None and not sp and np_ is not None and \
                    nxt.seg.chord_at(nxt.q) is not None and np_ % 12 in nxt.seg.chord_at(nxt.q).pcset:
                kind = "appoggiatura"
            elif np_ == n.pitch and nxt.seg.chord_at(nxt.q) is not None and \
                    np_ % 12 in nxt.seg.chord_at(nxt.q).pcset:
                kind = "anticipation"
            elif sp and np_ is not None and not sn and (pp - n.pitch) * (n.pitch - np_) < 0:
                kind = "escape tone"
            elif short and not strong:
                kind = "short unaccented"
        if kind is None:
            viol.append((n, desc + f" unresolved non-chord tone (prev {name(pp) if pp else '-'}, "
                                   f"next {name(np_) if np_ else '-'})"))
        else:
            n.nct = kind
            stats[f"non-chord tone: {kind}"] += 1
    return stats, viol


CLASH_IVS = (1, 13, 25, 11, 23)     # minor 2nd / 9th / 16th, major 7th / 14th


def check_clashes(sc, min_overlap=0.3, min_dur=0.4):
    """Sustained minor-second-class (m2, m9, m16) and major-seventh-class (M7, M14) collisions
    between notes that really sound together (rendered durations, let-ring and echo tails).

    Returns (unexpected, expected).  Expected: a classified non-chord tone (passing note,
    suspension, ...) or glissando is involved; or a pedal chord's bass against its upper chord
    (Eb/D); or, wider than a semitone, two tones of the declared chord (a maj7 chord's M7)."""
    ctl = chord_timeline(sc)
    notes = sorted([n for n in sc.notes if not PARTS[n.part].drum and n.role != "perc"], key=lambda n: n.t)
    out, exp = [], []
    active = []
    for n in notes:
        active = [a for a in active if sounding_end(a) > n.t + min_overlap]
        for a in active:
            iv = abs(a.pitch - n.pitch)
            if iv not in CLASH_IVS or min(sounding_end(a) - a.t, sounding_end(n) - n.t) < min_dur:
                continue
            t1 = min(sounding_end(a), sounding_end(n))
            ov = t1 - n.t
            if ov < min_overlap:
                continue
            t0 = max(a.seg.t(a.q), n.seg.t(n.q))          # written onsets (strings are pre-rolled)
            chs = [ch for _, ch in chords_between(ctl, t0, t1, 0.2)]
            pa, pb = a.pitch % 12, n.pitch % 12
            pedal = any(ch.pedal and ({pa, pb} & {ch.bass}) and ({pa, pb} - {ch.bass}) <= ch.upper for ch in chs)
            declared = iv > 1 and chs and all(pa in ch.pcset and pb in ch.pcset for ch in chs)
            if getattr(a, "nct", None) or getattr(n, "nct", None) or pedal or declared:
                exp.append((a, n, ov))
            else:
                out.append((a, n, ov))
        active.append(n)
    return out, exp


def check_ranges(sc):
    bad = []
    for n in sc.notes:
        p = PARTS[n.part]
        if not p.drum and not (p.lo <= n.pitch <= p.hi):
            bad.append(n)
    return bad


VL_ROLES = {"melody", "counter", "pad", "bass", "harmony"}
BASS_PARTS = {"vc", "cb", "vc_fast", "cb_fast", "contrab", "tuba", "pz_lo", "pz_cb", "trem_lo"}
STRING_PARTS = {"vla", "vln1", "vln2", "vc", "cb", "pad", "ooh", "trem_hi", "trem_va", "trem_lo"}
# intended octave doublings (octave/unison parallels between these are orchestration, not voice-leading)
DOUBLING_PAIRS = [(BASS_PARTS, BASS_PARTS), ({"choir"}, STRING_PARTS), ({"glock"}, {"tuba", "contrab"}),
                  ({"mbox"}, {"celesta"}), ({"celesta"}, {"vln_mel", "glock", "piano"}), ({"glock"}, {"flute"})]
# intended parallel fifths (stylistic planing): (segment label, part set A, part set B)
PLANING_OK = [("call-God", {"choir"}, STRING_PARTS), ("angry-question", {"choir"}, STRING_PARTS)]   # label prefix


def _sounding(lst, onsets, t):
    """Note of a voice sounding at time t (latest onset <= t that has not ended)."""
    import bisect
    i = bisect.bisect_right(onsets, t + 1e-4) - 1
    while i >= 0:
        t0, t1, p, n = lst[i]
        if t1 > t + 1e-3:
            return lst[i]
        if t - t0 > 8.0:
            break
        i -= 1
    return None


def _pair_ok(pa, pb, pairs):
    return any((pa in A and pb in B) or (pb in A and pa in B) for A, B in pairs)


def check_parallels_global(sc):
    """Consecutive perfect fifths / octaves in similar motion between ANY two voices of the score
    (melody, counter-melody, pads, basses, chordal parts), across segment and cue boundaries.

    Returns (violations, accepted); each item (time, cue, label, kind, voice a, voice b, a0, a1, b0, b1).
    Octaves between doubling pairs (bass section, choir/strings, glock/tuba...) and between two
    voices that double each other (>= 60% octaves/unisons in that cue) are accepted, as is the
    deliberate planing listed in PLANING_OK."""
    lines = defaultdict(list)
    for n in sc.notes:
        if PARTS[n.part].drum or n.role not in VL_ROLES:
            continue
        lines[n.voice or n.part].append((n.seg.t(n.q), n.seg.t(n.q + n.dq), n.pitch, n))
    for v in lines.values():
        v.sort(key=lambda x: (x[0], x[2]))
    onsets = {v: [x[0] for x in lst] for v, lst in lines.items()}
    vids = sorted(lines)
    bad, ok = [], []
    for i, va in enumerate(vids):
        A = lines[va]
        for vb in vids[i + 1:]:
            B = lines[vb]
            if A[-1][1] < B[0][0] or B[-1][1] < A[0][0]:
                continue
            events = sorted({x[0] for x in A} | {x[0] for x in B})
            seq = [(t, _sounding(A, onsets[va], t), _sounding(B, onsets[vb], t)) for t in events]
            # doubling share per cue
            dbl = defaultdict(lambda: [0, 0])
            for t, na, nb in seq:
                if na and nb:
                    d = dbl[na[3].seg.cue.id]
                    d[1] += 1
                    d[0] += abs(na[2] - nb[2]) % 12 == 0
            for (t0, a0, b0), (t1, a1, b1) in zip(seq, seq[1:]):
                if None in (a0, b0, a1, b1) or (a0 is a1 and b0 is b1):
                    continue
                da, db = a1[2] - a0[2], b1[2] - b0[2]
                if da == 0 or db == 0 or (da > 0) != (db > 0):
                    continue
                i0, i1 = abs(a0[2] - b0[2]) % 12, abs(a1[2] - b1[2]) % 12
                if i0 != i1 or i0 not in (0, 7):
                    continue
                if a0[1] < t1 - 0.15 or b0[1] < t1 - 0.15:      # not connected (a rest in between)
                    continue
                pa, pb = a1[3].part, b1[3].part
                kind = "octaves" if i0 == 0 else "fifths"
                both_pads = a1[3].role == b1[3].role == "pad" and _pad_family(pa) != _pad_family(pb)
                cue = a1[3].seg.cue.id
                item = (t1, cue, a1[3].seg.label, kind, va, vb, a0[2], a1[2], b0[2], b1[2])
                d = dbl[cue]
                if kind == "octaves" and (_pair_ok(pa, pb, DOUBLING_PAIRS) or both_pads
                                          or (d[1] >= 3 and d[0] / d[1] >= 0.6)):
                    ok.append(item + ("doubling",))
                elif kind == "fifths" and a1[3].seg.label == b1[3].seg.label and any(
                        a1[3].seg.label.startswith(lbl) and _pair_ok(pa, pb, [(X, Y)])
                                              for lbl, X, Y in PLANING_OK):
                    ok.append(item + ("planing",))
                else:
                    bad.append(item)
            # a doubled bass that splits into contrary motion (e.g. cellos up a fourth while the
            # basses fall a fifth) blurs the bass line and traps the inner voices
            if not (lines[va][0][3].part in BASS_PARTS and B[0][3].part in BASS_PARTS):
                continue
            for (t0, a0, b0), (t1, a1, b1) in zip(seq, seq[1:]):
                if None in (a0, b0, a1, b1) or a0 is a1 or b0 is b1:
                    continue
                if min(a0[1] - a0[0], b0[1] - b0[0], a1[1] - a1[0], b1[1] - b1[0]) < 0.4:
                    continue
                if a0[1] < t1 - 0.15 or b0[1] < t1 - 0.15:
                    continue
                if abs(a0[2] - b0[2]) % 12 == 0 and (a1[2] - a0[2]) * (b1[2] - b0[2]) < 0:
                    bad.append((t1, a1[3].seg.cue.id, a1[3].seg.label, "split bass", va, vb,
                                a0[2], a1[2], b0[2], b1[2]))
    bad.sort()
    ok.sort()
    return bad, ok


def _pad_family(part):
    for fam, members in (("str", {"vla", "vln1", "vln2", "vc", "cb"}), ("trem", {"trem_hi", "trem_va", "trem_lo"}),
                         ("brass", {"tbn", "brass", "horn", "tuba"})):
        if part in members:
            return fam
    return part


def line_smr(timeline, music, sr, voice_path):
    """Speech-to-music ratio of every narration line in a simulation of audio/mix.py: music is
    normalised to MUSIC_LUFS and ducked by MUSIC_DUCK_DB with mix.bed_envelope(voice, timeline) (as the mix).

    Returns rows (scene, line index, text, broadband SMR, 1-4 kHz SMR, worst 200 ms SMR) over the
    frames where the voice is active, or None when voice.wav is missing."""
    import pyloudnorm as pyln
    from scipy import signal as sg

    from audio import mix as mixmod

    if not Path(voice_path).exists():
        return None
    voice, vsr = sf.read(voice_path, dtype="float64")
    assert vsr == sr
    if voice.ndim > 1:
        voice = voice.mean(axis=1)
    n = len(music)
    voice = voice[:n] if len(voice) >= n else np.concatenate([voice, np.zeros(n - len(voice))])
    lm = pyln.Meter(sr).integrated_loudness(music)
    m = music * 10 ** ((mixmod.MUSIC_LUFS - lm) / 20)
    env = mixmod.bed_envelope(voice.astype(np.float32), timeline).astype(np.float64)
    m = m * 10 ** (mixmod.MUSIC_DUCK_DB * env / 20)[:, None]
    sos = sg.butter(4, [1000, 4000], "bandpass", fs=sr, output="sos")
    hop = int(0.02 * sr)

    def frames(x):
        k = len(x) // hop
        return x[:k * hop].reshape(k, hop).mean(axis=1)

    V, Mu = frames(voice ** 2), frames((m ** 2).mean(axis=1))
    VB, MB = frames(sg.sosfilt(sos, voice) ** 2), frames((sg.sosfilt(sos, m, axis=0) ** 2).mean(axis=1))
    rows = []
    for s in timeline["scenes"]:
        for i, ln in enumerate(s["lines"]):
            a, b = int((s["start"] + ln["start"]) / 0.02), int((s["start"] + ln["end"]) / 0.02)
            vd = 10 * np.log10(V[a:b] + 1e-15)
            act = vd > max(-42.0, np.percentile(vd, 95) - 25)
            smr = 10 * np.log10(V[a:b][act].sum() / (Mu[a:b][act].sum() + 1e-20))
            smrb = 10 * np.log10(VB[a:b][act].sum() / (MB[a:b][act].sum() + 1e-20))
            worst = []
            for k in range(a, b - 10):
                ac = act[k - a:k - a + 10]
                if ac.mean() >= 0.7:
                    worst.append(10 * np.log10(V[k:k + 10][ac].sum() / (Mu[k:k + 10][ac].sum() + 1e-20)))
            rows.append((s["id"], i, ln["text"], smr, smrb, min(worst) if worst else float("nan")))
    return rows


def sync_onsets(sc, stems, sr, search=0.15):
    """Audible onset at every 'hit' sync: spectral flux of the summed dry stems around the target.
    Returns rows (cue, label, target, structural time, onset offset s, prominence)."""
    from scipy import signal as sg

    tot = sum(stems.values()).mean(axis=1)
    hop, win = int(0.005 * sr), 2048
    rows = []
    for cid, label, target, actual, kind in sc.syncs:
        if kind != "hit":
            continue
        a, b = int((target - 1.2) * sr), int((target + 1.2) * sr)
        a0, b0 = max(0, a - win), min(len(tot), b + win)
        _, ts, S = sg.stft(tot[a0:b0], fs=sr, nperseg=win, noverlap=win - hop, boundary=None, padded=False)
        L = np.log10(np.abs(S) + 1e-6)
        flux = np.maximum(0, np.diff(L, axis=1)).sum(axis=0)
        tf = a0 / sr + ts[1:]                      # frame centre times
        near = np.abs(tf - target) <= search
        if not near.any():
            continue
        k = np.argmax(np.where(near, flux, -1))
        prom = flux[k] / (np.median(flux) + 1e-9)
        rows.append((cid, label, target, actual, tf[k] - target, prom))
    return rows


def _chord_at_time(sc, t):
    for c in sc.cues:
        for s in c.segs:
            if s.t0 - 1e-6 <= t < s.t1:
                return s.chord_at(s.q_of(t))
    return None


def sync_changes(sc, mono, sr, pre=(-0.7, -0.2), post=(0.2, 0.7)):
    """Audible harmonic arrival at every 'change' sync, measured on the final (reverberant) mix.

    Chroma (magnitude spectrum 65-2100 Hz folded onto pitch classes, normalised per frame) gives
    d(t) = share of the pitch classes only in the new chord - share of those only in the old chord.
    Change = mean d after (+0.2..+0.7 s) - mean d before (-0.7..-0.2 s); arrival = first time
    from -0.4 s on where the smoothed d passes the midpoint and stays there for 150 ms.
    Returns rows (cue, label, target, old chord, new chord, change, arrival offset s)."""
    from scipy import signal as sg

    win, hop = 8192, int(0.01 * sr)
    rows = []
    for cid, label, target, actual, kind in sc.syncs:
        if kind != "change":
            continue
        old, new = _chord_at_time(sc, target - 0.05), _chord_at_time(sc, target + 0.05)
        a, b = int((target - 1.3) * sr), int((target + 1.3) * sr)
        f, ts, S = sg.stft(mono[max(0, a):b], fs=sr, nperseg=win, noverlap=win - hop, boundary=None, padded=False)
        ts = ts + max(0, a) / sr - target
        keep = (f >= 65) & (f <= 2100)
        pcs = np.round(12 * np.log2(f[keep] / 440.0) + 69).astype(int) % 12
        mag = np.abs(S[keep])
        chroma = np.zeros((12, mag.shape[1]))
        for p in range(12):
            chroma[p] = mag[pcs == p].sum(axis=0)
        chroma /= chroma.sum(axis=0, keepdims=True) + 1e-12
        new_only = sorted(new.pcset - old.pcset)
        old_only = sorted(old.pcset - new.pcset)
        d = chroma[new_only].sum(axis=0) - chroma[old_only].sum(axis=0)
        d = np.convolve(d, np.ones(5) / 5, "same")
        before = d[(ts >= pre[0]) & (ts <= pre[1])].mean()
        after = d[(ts >= post[0]) & (ts <= post[1])].mean()
        mid = (before + after) / 2
        arr = float("nan")
        hold = int(0.15 / 0.01)
        for i in np.nonzero(ts >= -0.4)[0]:
            if i + hold < len(d) and (d[i:i + hold] >= mid).all():
                arr = float(ts[i])
                break
        rows.append((cid, label, target, old.sym, new.sym, after - before, arr))
    return rows


def onset_density(sc, cue):
    """Pitched note onsets per second while lines are spoken vs. in the pauses of this cue."""
    on = np.array([n.seg.t(n.q) for n in sc.notes if n.seg.cue is cue and not PARTS[n.part].drum
                   and n.role not in ("gliss",)])
    if len(on) == 0:
        return float("nan"), float("nan")
    sp = sc.speaking(on)
    grid = np.arange(cue.t0, cue.t1, 0.01)
    gs = sc.speaking(grid)
    ts, tg = gs.sum() * 0.01, (~gs).sum() * 0.01
    return (sp.sum() / ts if ts > 0.3 else float("nan")), ((~sp).sum() / tg if tg > 0.3 else float("nan"))


def _rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


SMR_MIN = 15.0          # dB, broadband speech-to-music ratio per line in the simulated mix
SMR_BAND_MIN = 12.0     # dB, the same in the 1-4 kHz band that carries most of the intelligibility
STORM_OVER_MEDIAN = 6.0  # LU, the storm section may be at most this much louder than the median cue
STORM_LEAD = 1.5        # LU, every storm section must be at least this much louder than every non-storm cue
STORM_ST_LEAD = 0.5     # LU, the storm's loudest 3 s must beat every other cue's loudest 3 s by this much
STORM_PEAK_OVER_MEDIAN = 5.0   # LU, the storm-peak segment (hit + horn call) vs the median cue
PEAK_WINDOW_OVER_MEDIAN = 10.0  # dB, loudest 400 ms of the score vs its median 400 ms level


HANDOFF_DB = 8.0       # dB, largest level step between two adjacent 250 ms windows at a scene or segment start
HANDOFF_WIN = 0.25     # s


# ITU-R BS.1770 K-weighting at 48 kHz (high shelf + RLB high-pass)
_K_SOS = np.array([[1.53512485958697, -2.69169618940638, 1.19839281085285, 1.0, -1.69065929318241, 0.73248077421585],
                   [1.0, -2.0, 1.0, 1.0, -1.99004745483398, 0.99007225036621]])


def k_weighted_power(x, sr):
    """Per-sample K-weighted power summed over the channels (BS.1770, 48 kHz)."""
    from scipy import signal as sg
    assert sr == 48000, "K-weighting coefficients are for 48 kHz"
    y = sg.sosfilt(_K_SOS, x, axis=0)
    return (y ** 2).sum(axis=1) if y.ndim > 1 else y ** 2


def integrated_lufs(x, sr):
    """Gated integrated loudness (LUFS) of a stretch of audio (>= 0.4 s)."""
    import pyloudnorm as pyln
    if len(x) < int(0.4 * sr):
        return float("nan")
    v = pyln.Meter(sr).integrated_loudness(x)
    return float(v) if np.isfinite(v) else float("nan")


def short_term(power, sr, win=3.0, hop=0.1):
    """Short-term loudness (3 s windows, LUFS) every hop s: (window centre times, values)."""
    cs = np.concatenate([[0.0], np.cumsum(power)])
    w, h = int(win * sr), int(hop * sr)
    st = np.arange(0, len(power) - w, h)
    return (st + w / 2) / sr, -0.691 + 10 * np.log10((cs[st + w] - cs[st]) / w + 1e-15)


def storm_sections(sc):
    """{cue id: [(t0, t1)]} of every storm cue without its deliberately hushed close (Seg.hush)."""
    out = {}
    for c in sc.cues:
        if c.mood == "storm":
            out[c.id] = [(s_.t0, s_.t1) for s_ in c.segs if not s_.hush]
    return out


def handoff_steps(mono, sr, sc, boundaries, win=HANDOFF_WIN, hop=0.05):
    """Largest level step between adjacent `win` windows around each boundary (t, span after it).
    Not counted: steps within 0.3 s of a 'hit' sync (an intended attack), and drops within 0.4 s
    of the start of a spoken line (the designed speech ducking engaging).
    Returns [(t boundary, label, step dB, at s)]."""
    cs = np.concatenate([[0.0], np.cumsum(mono ** 2)])
    n = int(win * sr)
    hits = np.array([actual for _, _, _, actual, kind in sc.syncs if kind == "hit"] or [-99.0])
    onsets = np.array([a for a, _ in sc.speech_iv] or [-99.0])

    def lvl(t):
        a = int(t * sr)
        if a < 0 or a + n > len(mono):
            return float("nan")
        return 10 * np.log10((cs[a + n] - cs[a]) / n + 1e-12)

    out = []
    for t0, span, label in boundaries:
        best = (0.0, t0)
        for t in np.arange(t0 - win, t0 + span, hop):
            if np.abs(hits - t).min() <= 0.3:
                continue
            d = lvl(t) - lvl(t - win)
            if d < 0 and np.abs(onsets - t).min() <= 0.4:
                continue
            if np.isfinite(d) and abs(d) > abs(best[0]):
                best = (d, t)
        out.append((t0, label, best[0], best[1]))
    return out

# Hit points the v2 score must place, defined by the narration text: (scene, phrase, mode, kind)
#   mode 'line'   = start of the utterance containing the phrase
#        'gap'    = middle of the pause before that utterance
#        'phrase' = where the phrase itself is spoken (subtitle-chunk timing, interpolated by characters)
#        'end'    = end of that utterance
# (the s08 wave crash, the s09 splash, the s10 gulp, the s17 horn blow and Jonah's stamps in s22 illustrate
# on-screen actions: they are PICTURE_HITS below)
REQUIRED_HITS = [
    ("s02_call", "你起来", "gap", "change"),                  # God speaks: the choir enters
    ("s04_storm", "大浪一个接着一个", "gap", "hit"),           # storm peak
    ("s06_lots", "抽中的正是约拿", "phrase", "hit"),           # the lot falls on Jonah
    ("s09_overboard", "海就平静了", "line", "change"),         # sudden calm
    ("s10_swallow", "安排好了一条大鱼", "gap", "hit"),         # the great-fish motif
    ("s12_deep", "想起了耶和华", "phrase", "change"),          # the turning point
    ("s12_deep", "救恩属于耶和华", "phrase", "change"),        # radiant major
    ("s14_again", "你起来", "gap", "change"),                 # the second call echoes the first
    ("s15_city", "再过四十天", "gap", "hit"),                  # forty days
    ("s16_believe", "竟然都相信了上帝", "phrase", "change"),    # surprise belief
    ("s17_king", "国王又派人在全城宣告", "gap", "hit"),         # the king commands: the herald section
    ("s19_angry", "只有约拿", "phrase", "hit"),                # grumpy bassoon
    ("s19_angry", "又慈爱", "gap", "change"),                  # tender under God's kindness
    ("s21_vine", "一夜之间", "phrase", "hit"),                 # the plant grows
    ("s21_vine", "非常非常高兴", "gap", "hit"),                # happy waltz
    ("s22_worm", "小虫子", "phrase", "hit"),                   # the little worm
    ("s22_worm", "咬了蓖麻", "phrase", "hit"),                 # the worm bites
    ("s24_end", "连我们不喜欢的人", "end", "hit"),              # final cadence
]


# Hit points defined by the PICTURE (an on-screen action the score illustrates; a hit there must follow the
# animation, not the narration word).  Targets come from the scenes' own sound-effect cues, which the scene
# authors key to the animation (engine.loader.build_scene(sid).sfx_cues), independently of the score code:
# (scene, sfx cue name, from-line phrase or None, index, offset s, kind, what)
#   the index counts the cues of that name in time order (from the start of the line containing the phrase,
#   minus 0.3 s, when a phrase is given); the target is that cue's time + offset
PICTURE_HITS = [
    ("s08_row", "splash", None, 0, 0.0, "hit", "the wave slams into the ship (the waves win)"),
    ("s09_overboard", "splash", None, 0, 0.02, "hit", "Jonah hits the water (the scene's splash cue is 0.02 s early)"),
    ("s10_swallow", "gulp", None, 0, 0.32, "hit", "the fish's mouth snaps shut (half-way through the close)"),
    ("s17_king", "horn", None, 0, 0.0, "hit", "the messenger blows the horn"),
    ("s22_worm", "thud", "我气极了", 0, 0.0, "hit", "Jonah stamps on '对！'"),
    ("s22_worm", "thud", "我气极了", 1, 0.0, "hit", "Jonah stamps on '我就是生气！'"),
    ("s22_worm", "thud", "我气极了", 2, 0.0, "hit", "Jonah stamps on '我气极了！'"),
]


def is_jonah():
    from engine import paths
    return paths.STORY == "jonah"


def hit_lists():
    """(required hits, picture hits) of the current story: Jonah's lists above, or the story's cues.py
    REQUIRED_HITS / PICTURE_HITS (same formats; empty when not given)."""
    if is_jonah():
        return REQUIRED_HITS, PICTURE_HITS
    from audio import score
    mod = score.story_cues()
    return list(getattr(mod, "REQUIRED_HITS", [])), list(getattr(mod, "PICTURE_HITS", []))


def story_title():
    if is_jonah():
        return "约拿的故事"
    from engine.paths import STORY, load_story
    try:
        return getattr(load_story(), "TITLE", STORY)
    except Exception:
        return STORY


def picture_targets(timeline, hits=None):
    """[(scene, label, kind, scene-relative target s or None, note)] for PICTURE_HITS (or `hits`)."""
    from engine.loader import build_scene

    by_id = {s_["id"]: s_ for s_ in timeline["scenes"]}
    cues, out = {}, []
    for sid, cue_name, phrase, k, off, kind, what in (PICTURE_HITS if hits is None else hits):
        label = f"sfx '{cue_name}' #{k}" + (f" from '{phrase}'" if phrase else "") + (f" {off:+.2f}s" if off else "")
        if sid not in by_id:
            continue
        if sid not in cues:
            try:
                cues[sid] = build_scene(sid, timeline).sfx_cues
            except Exception as e:
                cues[sid] = e
        if isinstance(cues[sid], Exception):
            out.append((sid, label, kind, None, f"scene does not build: {cues[sid]}"))
            continue
        t_from = -1e9
        if phrase:
            ln = next((l_ for l_ in by_id[sid]["lines"] if phrase in l_["text"]), None)
            if ln is None:
                out.append((sid, label, kind, None, f"no line contains {phrase!r}"))
                continue
            t_from = ln["start"] - 0.3
        ts = sorted(float(c_["at"]) for c_ in cues[sid] if c_["name"] == cue_name and float(c_["at"]) >= t_from)
        out.append((sid, label, kind, ts[k] + off if k < len(ts) else None,
                    what if k < len(ts) else f"no cue ({what})"))
    return out


def phrase_time(scene, phrase, mode):
    """Scene-relative time of a phrase in the narration (see REQUIRED_HITS)."""
    lines = scene["lines"]
    i = next(k for k, ln in enumerate(lines) if phrase in ln["text"])
    ln = lines[i]
    if mode == "line":
        return ln["start"]
    if mode == "end":
        return ln["end"]
    if mode == "gap":
        return (lines[i - 1]["end"] + ln["start"]) / 2 if i > 0 else ln["start"] / 2
    k0 = ln["text"].index(phrase)
    wgt = lambda t: sum(0.5 if ch in "，。！？：；、" else 1.0 for ch in t)
    pos = 0
    for ch in ln.get("chunks") or [{"text": ln["text"], "start": ln["start"], "end": ln["end"]}]:
        j = ln["text"].find(ch["text"], pos)
        j = pos if j < 0 else j
        if j <= k0 <= j + len(ch["text"]):
            return ch["start"] + wgt(ch["text"][:k0 - j]) / max(1e-9, wgt(ch["text"])) * (ch["end"] - ch["start"])
        pos = j + len(ch["text"])
    return ln["start"]


def required_hits(sc, timeline, tol=0.05, picture=True):
    """[(scene, phrase, mode, kind, target abs s, (sync abs s, label) or None)]; picture hits (PICTURE_HITS)
    have mode 'picture' and the sfx cue as 'phrase'.  A picture hit whose scene does not build or whose cue
    is gone has no target to check: it is listed with got = 'n/a' instead."""
    out = []
    by_id = {s_["id"]: s_ for s_ in timeline["scenes"]}

    def placed(sid, kind, target):
        cands = [(actual, label) for cid, label, tg, actual, k in sc.syncs
                 if cid == sid and k == kind and abs(actual - target) <= tol]
        return min(cands, key=lambda x: abs(x[0] - target)) if cands else None

    req, pic = hit_lists()
    for sid, ph, mode, kind in req:
        s_ = by_id.get(sid)
        if s_ is None or not any(ph in ln["text"] for ln in s_["lines"]):
            out.append((sid, ph, mode, kind, float("nan"), None))
            continue
        target = s_["start"] + phrase_time(s_, ph, mode)
        out.append((sid, ph, mode, kind, target, placed(sid, kind, target)))
    if picture:
        for sid, label, kind, t_rel, note in picture_targets(timeline, pic):
            if t_rel is None:
                out.append((sid, label, "picture", kind, float("nan"), ("n/a", note)))
                continue
            target = by_id[sid]["start"] + t_rel
            out.append((sid, label, "picture", kind, target, placed(sid, kind, target)))
    return out


def _jonah_level_checks(checks, loud_c, lufs, lead, top_other, storm_st, other_st, quiet_c, quiet_seg, sec_lufs,
                        seg_lufs, med):
    """The Jonah film's dynamic plan: the storm is the loudest music, the belly the quietest."""
    checks.append(("a storm cue (s04 storm or s08 rowing) is the loudest cue (integrated LUFS)", loud_c.mood == "storm",
                   f"{loud_c.id} {lufs[loud_c.id]:.1f} LUFS"))
    checks.append((f"every storm section (hushed close excluded) >= {STORM_LEAD} LU above every non-storm cue",
                   bool(lead) and min(lead.values()) >= STORM_LEAD,
                   ", ".join(f"{cid} {v:+.1f} LU vs {top_other}" for cid, v in lead.items())))
    checks.append((f"the storm's loudest 3 s beat every other cue's loudest 3 s by >= {STORM_ST_LEAD} LU (finale included)",
                   storm_st[0] - other_st[0][0] >= STORM_ST_LEAD,
                   f"storm {storm_st[0]:.1f} at {storm_st[1]:.1f} s vs {other_st[1]} {other_st[0][0]:.1f} at "
                   f"{other_st[0][1]:.1f} s ({storm_st[0] - other_st[0][0]:+.1f} LU)"))
    checks.append(("belly (or the end's open question) is the quietest (LUFS)", quiet_c.mood == "belly"
                   or quiet_seg == "end-question", f"quietest cue {quiet_c.id}, quietest segment {quiet_seg}"))
    worst_storm = max(sec_lufs.values(), default=float("nan"))
    checks.append((f"storm no more than {STORM_OVER_MEDIAN:.0f} LU above the median cue",
                   worst_storm - med <= STORM_OVER_MEDIAN, f"{worst_storm - med:+.1f} LU"))
    if "storm-peak" in seg_lufs:
        checks.append((f"storm-peak segment no more than {STORM_PEAK_OVER_MEDIAN:.0f} LU above the median cue",
                       seg_lufs["storm-peak"] - med <= STORM_PEAK_OVER_MEDIAN, f"{seg_lufs['storm-peak'] - med:+.1f} LU"))


def report(sc, wav_path, stems, timeline, out_dir=None, notes=()):
    out_dir = Path(out_dir or Path(wav_path).parent.parent / "preview")
    out_dir.mkdir(parents=True, exist_ok=True)
    x, sr = sf.read(wav_path, dtype="float64", always_2d=True)
    n_exp = int(round(float(timeline["duration"]) * sr))
    mono = x.mean(axis=1)
    checks = []                     # (name, ok, detail)
    L = []
    w = L.append
    peak = np.abs(x).max()
    n_nan = int(np.isnan(x).sum())
    checks.append(("exact duration", len(x) == n_exp, f"{len(x)} samples, expected {n_exp}"))
    checks.append(("peak < 0.99, no NaN", peak < 0.99 and n_nan == 0, f"peak {peak:.4f}, NaN {n_nan}"))
    w(f"file: {wav_path}")
    w(f"duration: {len(x) / sr:.4f} s ({len(x)} samples, expected {n_exp}) -> "
      f"{'OK' if len(x) == n_exp else 'MISMATCH'}")
    w(f"sample rate {sr}, channels {x.shape[1]}, NaN: {n_nan}, "
      f"peak {peak:.4f} ({20 * np.log10(peak):.2f} dBFS), samples >= 0.99: {int((np.abs(x) >= 0.99).sum())}")
    try:
        import pyloudnorm as pyln
        w(f"integrated loudness: {pyln.Meter(sr).integrated_loudness(x):.1f} LUFS")
    except Exception:
        pass
    w(f"DC offset L/R: {x[:, 0].mean():.2e} / {x[:, 1].mean():.2e}")
    for nt in notes:
        w(nt)
    hd = int(0.3 * sr)
    w(f"first 0.3 s RMS {_rms_db(x[:hd]):.1f} dB (start of the title downbeat), "
      f"last 50 ms RMS {_rms_db(x[-int(0.05 * sr):]):.1f} dB, last sample {np.abs(x[-1]).max():.2e}")
    w("")

    # ---------------------------------------------------------------- cue structure (v2 timeline)
    probs = []
    scenes = timeline["scenes"]
    if [c.id for c in sc.cues] != [s_["id"] for s_ in scenes]:
        probs.append("cue list differs from the scene list")
    for i, (c, s_) in enumerate(zip(sc.cues, scenes)):
        t1 = scenes[i + 1]["start"] if i + 1 < len(scenes) else float(timeline["duration"])
        if abs(c.t0 - s_["start"]) > 1e-6 or abs(c.t1 - t1) > 1e-6:
            probs.append(f"{c.id}: cue window {c.t0:.3f}-{c.t1:.3f} != scene {s_['start']:.3f}-{t1:.3f}")
        if not c.segs or abs(c.segs[0].t0 - c.t0) > 1e-6 or abs(c.segs[-1].t1 - c.t1) > 1e-6:
            probs.append(f"{c.id}: segments do not fill the cue")
        for a_, b_ in zip(c.segs, c.segs[1:]):
            if abs(a_.t1 - b_.t0) > 1e-6:
                probs.append(f"{c.id}: gap/overlap between {a_.label} and {b_.label}")
    checks.append((f"all {len(scenes)} scenes have a cue starting at the scene's global start; segments tile it",
                   not probs, "; ".join(probs[:4]) or f"{len(sc.cues)} cues, {sum(len(c.segs) for c in sc.cues)} segments"))
    hits = required_hits(sc, timeline)
    miss = [f"{sid} '{ph}'" for sid, ph, mode, kind, target, got in hits if got is None]
    na = [f"{sid} {ph} ({got[1]})" for sid, ph, mode, kind, target, got in hits if got and got[0] == "n/a"]
    w("REQUIRED HIT POINTS (target computed here, independently of the score code, from the timeline text and")
    w("subtitle-chunk timings -- or, for 'picture' hits, from the scenes' own sound-effect cues, which follow the")
    w("animation; the score must place a sync of that kind within 50 ms of it)")
    for sid, ph, mode, kind, target, got in hits:
        if got and got[0] == "n/a":
            w(f"  {sid:14s} {kind:6s} {mode:10s} {ph}  n/a: {got[1]}")
            continue
        w(f"  {sid:14s} {kind:6s} {mode:10s} '{ph}'  target {target:8.3f}s  "
          + (f"score {got[1]!r} at {got[0]:8.3f}s ({1000 * (got[0] - target):+.0f} ms)" if got else "MISSING"))
    checks.append(("required hit points placed (narration text: calm, turn, salvation, herald, waltz...; picture: "
                   "the wave hit, the splash, the gulp, the horn blow, Jonah's stamps)" if is_jonah() else
                   "required hit points placed (the story's REQUIRED_HITS / PICTURE_HITS)", not miss,
                   (", ".join(miss) or f"all {len(hits) - len(na)}") + (f"; not checkable: {na}" if na else "")))
    w("")

    # ---------------------------------------------------------------- per-scene levels
    w("PER-SCENE LEVELS (cue window = scene start -> next scene start; 'speech' = while a line is spoken;")
    w("LUFS = gated integrated K-weighted loudness of the cue; ST max = its loudest 3 s window, short-term LUFS)")
    w(f"{'scene':14s} {'mood':8s} {'start':>7s} {'len':>6s} {'LUFS':>6s} {'ST max':>7s} {'at':>7s} {'RMS dB':>7s} "
      f"{'peak dB':>8s} {'speech RMS':>10s} {'gap RMS':>8s} {'L-R dB':>7s} {'onsets/s speech':>16s} {'gaps':>6s}")
    speech = sc.speaking(np.arange(len(x)) / sr)
    st_t, st_l = short_term(k_weighted_power(x, sr), sr)
    lufs, st_max = {}, {}
    for c in sc.cues:
        a, b = int(c.t0 * sr), int(c.t1 * sr)
        seg = mono[a:b]
        sp = speech[a:b]
        r = _rms_db(x[a:b])
        rs = _rms_db(seg[sp]) if sp.sum() > sr * 0.3 else float("nan")
        rg = _rms_db(seg[~sp]) if (~sp).sum() > sr * 0.3 else float("nan")
        lr = _rms_db(x[a:b, 0]) - _rms_db(x[a:b, 1])
        ds, dg = onset_density(sc, c)
        lufs[c.id] = integrated_lufs(x[a:b], sr)
        k = (st_t >= c.t0) & (st_t < c.t1)
        j = int(np.argmax(np.where(k, st_l, -np.inf)))
        st_max[c.id] = (float(st_l[j]), float(st_t[j])) if k.any() else (float("nan"), c.t0)
        w(f"{c.id:14s} {c.mood:8s} {c.t0:7.2f} {c.dur:6.2f} {lufs[c.id]:6.1f} {st_max[c.id][0]:7.1f} "
          f"{st_max[c.id][1]:7.1f} {r:7.1f} {20 * np.log10(np.abs(x[a:b]).max()):8.1f} "
          f"{rs:10.1f} {rg:8.1f} {lr:7.1f} {ds:16.1f} {dg:6.1f}")
    w("")
    by_id = {c.id: c for c in sc.cues}
    med = float(np.nanmedian(list(lufs.values())))
    loud_c = by_id[max(lufs, key=lambda k_: lufs[k_])]
    quiet_c = by_id[min(lufs, key=lambda k_: lufs[k_])]
    seg_lufs = {sg_.label: integrated_lufs(x[int(sg_.t0 * sr):int(sg_.t1 * sr)], sr) for c in sc.cues for sg_ in c.segs}
    seg_lufs = {k_: v for k_, v in seg_lufs.items() if np.isfinite(v)}
    quiet_seg = min(seg_lufs, key=seg_lufs.get)
    sections = storm_sections(sc)
    sec_lufs = {cid: integrated_lufs(np.concatenate([x[int(a_ * sr):int(b_ * sr)] for a_, b_ in iv]), sr)
                for cid, iv in sections.items()}
    others = {cid: v for cid, v in lufs.items() if by_id[cid].mood != "storm"}
    top_other = max(others, key=others.get) if others else None
    w(f"loudest cue: {loud_c.id} ({loud_c.mood}) {lufs[loud_c.id]:.1f} LUFS, quietest cue: {quiet_c.id} ({quiet_c.mood}) "
      f"{lufs[quiet_c.id]:.1f} LUFS, quietest segment: {quiet_seg} ({seg_lufs[quiet_seg]:.1f} LUFS); median cue "
      f"{med:.1f} LUFS; loudest non-storm cue {top_other} {others.get(top_other, float('nan')):.1f} LUFS")
    lead = {cid: v - others[top_other] for cid, v in sec_lufs.items()} if others else {}
    for cid, v in sec_lufs.items():
        w(f"storm section {cid} (without its hushed close): {v:.1f} LUFS = median {v - med:+.1f} LU, loudest non-storm "
          f"cue {lead[cid]:+.1f} LU")
    storm_st = max((st_max[cid] for cid in sections), default=(float("nan"), 0.0))
    other_st = max(((v, cid) for cid, v in st_max.items() if by_id[cid].mood != "storm"),
                   default=((float("nan"), 0.0), ""))
    w(f"loudest 3 s: storm {storm_st[0]:.1f} LUFS at {storm_st[1]:.1f} s; loudest other cue {other_st[1]} "
      f"{other_st[0][0]:.1f} LUFS at {other_st[0][1]:.1f} s")
    if is_jonah():
        _jonah_level_checks(checks, loud_c, lufs, lead, top_other, storm_st, other_st, quiet_c, quiet_seg, sec_lufs,
                            seg_lufs, med)
    else:                       # the Jonah film's dynamic plan (storm loudest, belly quietest) is its own
        top = max(lufs, key=lambda k_: lufs[k_])
        checks.append((f"no cue more than {STORM_OVER_MEDIAN:.0f} LU above the median cue",
                       lufs[top] - med <= STORM_OVER_MEDIAN, f"loudest {top} {lufs[top] - med:+.1f} LU"))
    # hand-offs and entrances: adjacent 250 ms windows across every scene start (through the 1 s
    # dissolve) and every segment start
    bounds = ([(c.t0, 1.25, c.id) for c in sc.cues[1:]]
              + [(sg_.t0, 0.5, sg_.label) for c in sc.cues for sg_ in c.segs[1:]])
    steps = handoff_steps(mono, sr, sc, bounds)
    big = [f"{lbl} {d:+.1f} dB at {at:.2f} s" for t0, lbl, d, at in steps if abs(d) > HANDOFF_DB]
    w(f"HAND-OFFS (largest step between adjacent {int(HANDOFF_WIN * 1000)} ms windows at each scene start, through the "
      f"dissolve, and at each segment start; steps within 0.3 s of an attack sync, and drops as a line starts "
      f"(the speech ducking), excluded):")
    w("  " + ", ".join(f"{lbl[:16]} {d:+.1f}" for t0, lbl, d, at in steps))
    checks.append((f"smooth hand-offs and entrances (no step > {HANDOFF_DB:.0f} dB between adjacent "
                   f"{int(HANDOFF_WIN * 1000)} ms windows)", not big,
                   ", ".join(big) or f"max {max(abs(d) for _, _, d, _ in steps):.1f} dB"))
    gaps = []
    hop = int(0.05 * sr)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, "same"))[::hop]
    edb = 20 * np.log10(env + 1e-9)
    ref = np.percentile(edb, 95)
    silent = edb < ref - 45
    run = 0
    for i, s_ in enumerate(silent[:-int(1.0 / 0.05)]):       # the final fade-out is not a dead silence
        run = run + 1 if s_ else 0
        if run == int(0.5 / 0.05):
            gaps.append(round(i * 0.05, 2))
    w(f"dead silences (> 0.5 s more than 45 dB below the 95th-percentile level): {len(gaps)} {gaps[:10]}")
    checks.append(("no dead silences", not gaps, str(gaps[:5])))
    w("")
    w("NARRATION PAUSES: music level in each pause between lines vs. the 0.6 s of speech on either side")
    w("  (speech envelope merges lines < 0.5 s apart, so short breaths no longer pump; fills are written)")
    lifts = defaultdict(list)
    iv = sorted(sc.speech_iv)
    for (a0, b0), (a1, b1) in zip(iv, iv[1:]):
        g0, g1 = b0, a1
        if g1 - g0 < 0.2:
            continue
        gi = mono[int(g0 * sr):int(g1 * sr)]
        si = np.concatenate([mono[int(max(a0, g0 - 0.6) * sr):int(g0 * sr)], mono[int(g1 * sr):int(min(b1, g1 + 0.6) * sr)]])
        cue = next(c for c in sc.cues if c.t0 <= (g0 + g1) / 2 < c.t1)
        lifts[cue.id].append(_rms_db(gi) - _rms_db(si))
    allv = [v for vs in lifts.values() for v in vs]
    for c in sc.cues:
        vs = lifts.get(c.id, [])
        if vs:
            w(f"  {c.id:14s} pauses {len(vs):2d}  median lift {np.median(vs):+5.1f} dB  (min {min(vs):+5.1f}, max {max(vs):+5.1f})")
    if allv:
        w(f"  all pauses: {len(allv)}, median lift {np.median(allv):+.1f} dB, 75th pct {np.percentile(allv, 75):+.1f} dB, "
          f"max {max(allv):+.1f} dB")
    w("")

    # ---------------------------------------------------------------- speech-to-music ratio in the mix
    smr = line_smr(timeline, x, sr, Path(wav_path).parent / "voice.wav")
    w(f"SPEECH-TO-MUSIC RATIO per line (simulated mix.py: music -> -27 LUFS, ducked 7 dB under speech; "
      f"active-speech frames; FAIL below {SMR_MIN:.0f} dB broadband or {SMR_BAND_MIN:.0f} dB in 1-4 kHz)")
    if smr is None:
        w("  SKIPPED: build/audio/voice.wav not found")
        checks.append(("speech-to-music ratio >= 15 dB on every line", None, "voice.wav missing"))
    else:
        w(f"  {'scene':12s} {'line':>4s} {'SMR':>6s} {'1-4kHz':>7s} {'worst 200ms':>11s}  text")
        fails, fails_b = [], []
        for sid, i, text, r, rb, rw in smr:
            flag = "  FAIL" if r < SMR_MIN else ""
            if flag:
                fails.append(f"{sid} L{i} {r:.1f}")
            if rb < SMR_BAND_MIN:
                fails_b.append(f"{sid} L{i} {rb:.1f}")
                flag += "  FAIL(1-4k)"
            w(f"  {sid:12s} {i:4d} {r:6.1f} {rb:7.1f} {rw:11.1f}  {text}{flag}")
        vals = [r for *_, r, rb, rw in smr]
        vb = [rb for *_, r, rb, rw in smr]
        w(f"  min {min(vals):.1f} dB, median {np.median(vals):.1f} dB; 1-4 kHz min {min(vb):.1f} dB, median "
          f"{np.median(vb):.1f} dB")
        checks.append((f"speech-to-music ratio >= {SMR_MIN:.0f} dB on every line", not fails,
                       f"min {min(vals):.1f} dB" + (f"; fails {fails}" if fails else "")))
        checks.append((f"speech-to-music ratio in the 1-4 kHz band >= {SMR_BAND_MIN:.0f} dB on every line", not fails_b,
                       f"min {min(vb):.1f} dB" + (f"; fails {fails_b}" if fails_b else "")))
    w("")

    # ---------------------------------------------------------------- spectral balance
    w("SPECTRAL BALANCE per cue (band energy relative to the cue total, dB)")
    bands = [(20, 150), (150, 600), (600, 2500), (2500, 6000), (6000, 20000)]

    def spec_row(seg):
        F = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        tot = F.sum() + 1e-20
        return [10 * np.log10(F[(fr >= a) & (fr < b)].sum() / tot + 1e-12) for a, b in bands], (F * fr).sum() / tot

    w(f"  {'cue':14s} " + " ".join(f"{f'{a}-{b}':>10s}" for a, b in bands) + "   centroid")
    for c in sc.cues:
        vals, cen = spec_row(mono[int(c.t0 * sr):int(c.t1 * sr)])
        w(f"  {c.id:14s} " + " ".join(f"{v:10.1f}" for v in vals) + f"   {cen:7.0f} Hz")
    w("")
    w("SEGMENT LEVELS (RMS dB and 2.5-6 kHz share of each musical segment)")
    for c in sc.cues:
        for sg_ in c.segs:
            seg = mono[int(sg_.t0 * sr):int(sg_.t1 * sr)]
            vals, cen = spec_row(seg)
            w(f"  {sg_.label:24s} {sg_.t0:8.2f}-{sg_.t1:8.2f}  RMS {_rms_db(seg):6.1f} dB  2.5-6k {vals[3]:6.1f} dB  "
              f"centroid {cen:6.0f} Hz")
            if sg_.label == "worm-heat":
                checks.append(("worm-heat audible (RMS >= -33 dB) and not shrill (2.5-6k share < -10 dB)",
                               _rms_db(seg) >= -33 and vals[3] < -10, f"RMS {_rms_db(seg):.1f} dB, 2.5-6k {vals[3]:.1f} dB"))
    # the biggest short-term jump: loudest 400 ms window vs the film's median 400 ms level
    win, hop_ = int(0.4 * sr), int(0.05 * sr)
    cs = np.concatenate([[0.0], np.cumsum(mono ** 2)])
    starts = np.arange(0, len(mono) - win, hop_)
    pw = (cs[starts + win] - cs[starts]) / win
    pdb = 10 * np.log10(pw + 1e-12)
    k_max = int(np.argmax(pdb))
    w(f"  loudest 400 ms window at {k_max * 0.05:.2f} s: {pdb[k_max] - np.median(pdb):+.1f} dB above the film's median "
      f"400 ms level ({pdb[k_max]:.1f} vs {np.median(pdb):.1f} dB); 99th percentile "
      f"{np.percentile(pdb, 99) - np.median(pdb):+.1f} dB")
    checks.append((f"loudest 400 ms window no more than {PEAK_WINDOW_OVER_MEDIAN:.0f} dB above the median",
                   pdb[k_max] - np.median(pdb) <= PEAK_WINDOW_OVER_MEDIAN,
                   f"{pdb[k_max] - np.median(pdb):+.1f} dB at {k_max * 0.05:.2f} s"))
    w("")

    # ---------------------------------------------------------------- tempo map
    w("TEMPO MAP (segments are whole bars fitted exactly to their scene windows)")
    for c in sc.cues:
        for s_ in c.segs:
            dev = (s_.tempo / s_.nominal - 1) * 100 if s_.nominal else 0.0
            w(f"  {s_.label:24s} {s_.meter:4s} bars {s_.bars:<4g} {s_.t0:8.3f}-{s_.t1:8.3f}  "
              f"q={s_.tempo:6.1f} (nominal {s_.nominal}, {dev:+5.1f}%)  key {s_.scale.spec}"
              + ("   <-- tempo far from nominal: revisit bar count" if abs(dev) > 15 else ""))
    w("")
    w("HIT POINTS. 'structural' = where the score places the event (segment boundaries, so 0 ms by")
    w("construction -- not evidence).  Audible evidence from the rendered audio:")
    w("  attacks ('hit'): strongest spectral-flux onset in the dry stems within +-150 ms of the target, with")
    w("    its prominence (peak / median flux over +-1.2 s); FAIL if off by > 80 ms or prominence < 2.")
    w("  harmonic arrivals ('change', swells whose strings/choir are pre-rolled, so an onset test does not")
    w("    apply): chroma share of the new chord's own pitch classes minus the old chord's, after vs before")
    w("    (final mix); FAIL if the change is < 0.08 or it arrives outside -150..+350 ms.")
    structural = {(cid, label): actual for cid, label, target, actual, kind in sc.syncs}
    weak = []
    for cid, label, target, actual, off, prom in sync_onsets(sc, stems, sr):
        bad_ = abs(off) > 0.08 or prom < 2.0
        if bad_:
            weak.append(f"{cid}:{label}")
        w(f"  hit    {cid:12s} {label:44s} {target:8.3f}s  structural {1000 * (actual - target):+6.1f} ms  "
          f"onset {1000 * off:+6.1f} ms  prominence {prom:5.1f}{'  FAIL' if bad_ else ''}")
    for cid, label, target, old, new, chg, arr in sync_changes(sc, mono, sr):
        bad_ = not (chg >= 0.08 and -0.15 <= arr <= 0.35)
        if bad_:
            weak.append(f"{cid}:{label}")
        w(f"  change {cid:12s} {label:44s} {target:8.3f}s  structural "
          f"{1000 * (structural[(cid, label)] - target):+6.1f} ms  {old}->{new}: chroma change {chg:+.2f}, "
          f"arrives {1000 * arr:+6.0f} ms{'  FAIL' if bad_ else ''}")
    checks.append(("hit points audible (attacks: onset within 80 ms; arrivals: harmony changes on time)",
                   not weak, ", ".join(weak) or f"all {len(sc.syncs)}"))
    w("")

    # ---------------------------------------------------------------- harmony
    stats, viol = check_harmony(sc)
    w("HARMONY CHECK (every pitched note vs. its cue scale and the active chord)")
    for k, v in sorted(stats.items()):
        w(f"  {k:40s} {v}")
    w(f"  VIOLATIONS: {len(viol)}")
    for n, msg in viol[:200]:
        w(f"    ! {msg}")
    clashes, expected = check_clashes(sc)
    w(f"  sustained m2/m9/m16/M7/M14 explained by design (resolving non-chord tones, glissandi, pedal chords, "
      f"maj7 chord tones): {len(expected)}")
    w(f"  UNEXPECTED sustained m2/m9/m16/M7/M14 clashes (rendered durations incl. let-ring and echo tails; overlap "
      f">= 0.3 s, both notes >= 0.4 s): {len(clashes)}")
    for a, b2, ov in clashes[:40]:
        w(f"    ~ {a.t:7.2f}s {a.part}:{name(a.pitch)} ({a.role}) vs {b2.part}:{name(b2.pitch)} ({b2.role}) "
          f"overlap {ov:.2f}s")
    rng = check_ranges(sc)
    w(f"  notes outside instrument range: {len(rng)}")
    for n in rng[:20]:
        w(f"    ! {n.seg.cue.id} {n.part} {name(n.pitch)}")
    checks.append(("harmony: every note in scale / chord or a resolved non-chord tone", not viol, f"{len(viol)} violations"))
    checks.append(("no unexpected sustained m2/m9/m16/M7/M14 clashes (incl. ring and echo tails)", not clashes,
                   f"{len(clashes)}"))
    checks.append(("all notes inside instrument ranges", not rng, f"{len(rng)}"))
    w("")

    # ---------------------------------------------------------------- voice-leading
    n_par, n_pairs, bad = 0, 0, []
    for label, syms, vs, basses in sc.voicings:
        cols = [list(v) for v in zip(*vs)]
        if basses:
            cols = [list(basses)] + cols
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                n_pairs += 1
                ks = parallels(cols[i], cols[j])
                n_par += len(ks)
                bad += [f"{label} {syms[k - 1]}->{syms[k]} voices {i}/{j}" for k in ks]
    w(f"VOICE-LEADING inside each voice-led pad ({len(sc.voicings)} passages, {n_pairs} voice pairs)")
    w(f"  parallel perfect fifths/octaves: {n_par}")
    for b_ in bad[:20]:
        w(f"    ! {b_}")
    gbad, gok = check_parallels_global(sc)
    w("VOICE-LEADING across the whole score (every pair of melody/counter/pad/bass/chordal voices, at every")
    w("shared onset, across segment and cue joins; consecutive P5/P8 in similar motion)")
    w(f"  violations: {len(gbad)}")
    for t, cue, lbl, kind, va, vb, a0, a1, b0, b1 in gbad[:60]:
        w(f"    ! {t:7.2f}s {lbl:22s} {kind:7s} {va} {name(a0)}->{name(a1)}  vs  {vb} {name(b0)}->{name(b1)}")
    kinds = Counter(item[-1] for item in gok)
    w(f"  accepted: {len(gok)} ({', '.join(f'{k} {v}' for k, v in kinds.items()) or 'none'}): intended octave doublings "
      f"and the call-God planing")
    for t, cue, lbl, kind, va, vb, a0, a1, b0, b1, why in [g for g in gok if g[-1] == "planing"][:10]:
        w(f"    = {t:7.2f}s {lbl:22s} {kind:7s} {va} {name(a0)}->{name(a1)}  vs  {vb} {name(b0)}->{name(b1)}  ({why})")
    checks.append(("no parallel fifths/octaves (pads + whole score)", n_par == 0 and not gbad,
                   f"pads {n_par}, global {len(gbad)}"))
    w("")

    # ---------------------------------------------------------------- melodies
    w("MELODIES (melody-role lines per cue: range, largest leap, share of stepwise motion)")
    mel = defaultdict(list)
    for n in sc.notes:
        if n.role == "melody" and not PARTS[n.part].drum:
            mel[(n.seg.cue.id, n.part)].append(n)
    order = {c.id: k for k, c in enumerate(sc.cues)}
    for (mood, part), lst in sorted(mel.items(), key=lambda kv: order[kv[0][0]]):
        lst.sort(key=lambda n: n.seg.t(n.q))
        ps = [n.pitch for n in lst]
        ivs = [abs(b - a) for a, b in zip(ps, ps[1:])]
        if not ivs:
            continue
        steps = sum(1 for v in ivs if v <= 2) / len(ivs)
        w(f"  {mood:14s} {part:9s} notes {len(ps):3d}  range {name(min(ps))}-{name(max(ps))} ({max(ps) - min(ps):2d} st)"
          f"  largest leap {max(ivs):2d} st  stepwise {100 * steps:3.0f}%")
    w("")

    # ---------------------------------------------------------------- orchestration summary
    w("ORCHESTRATION (notes per part per cue)")
    per = defaultdict(Counter)
    for n in sc.notes:
        per[n.seg.cue.id][n.part] += 1
    for c in sc.cues:
        w(f"  {c.id:14s} " + ", ".join(f"{p} {k}" for p, k in sorted(per[c.id].items(), key=lambda kv: -kv[1])))
    w("")
    w("BUS LEVELS (dry stems, RMS dB per cue)")
    w("  " + " ".join(f"{b:>7s}" for b in stems) + "   cue")
    for c in sc.cues:
        a, b = int(c.t0 * sr), int(c.t1 * sr)
        w("  " + " ".join(f"{_rms_db(st[a:b]):7.1f}" for st in stems.values()) + f"   {c.id}")

    head = [f"MUSIC REPORT — {story_title()} background score ({len(sc.cues)} cues, {sc.duration:.1f} s)", "", "SUMMARY"]
    for nm, ok_, det in checks:
        head.append(f"  [{'PASS' if ok_ else ('SKIP' if ok_ is None else 'FAIL')}] {nm}: {det}")
    head.append("")
    text = "\n".join(head + L) + "\n"
    (out_dir / "music_report.txt").write_text(text)
    n_fail = sum(1 for _, ok_, _ in checks if ok_ is not None and not ok_)
    print(f"  report: {out_dir / 'music_report.txt'} ({n_fail} failed checks; {len(viol)} harmony violations, "
          f"{len(gbad)} global parallels)")
    _spectrogram(mono, sr, sc, out_dir / "music_spectrogram.png")
    return text


def _spectrogram(mono, sr, sc, path, rows=4):
    """Spectrogram + level curve in `rows` stacked strips (cyan = scene starts with id and mood,
    dotted = segment boundaries, blue = narration, red markers = hit points)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (matplotlib missing: no spectrogram)")
        return
    from scipy import signal as sg
    f, t, S = sg.stft(mono, fs=sr, nperseg=4096, noverlap=4096 - 2048)
    db = 20 * np.log10(np.abs(S) + 1e-9)
    db -= db.max()
    keep = (f >= 30) & (f <= 12000)
    hop = int(0.05 * sr)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, "same"))[::hop]
    te = np.arange(len(env)) * 0.05
    total = len(mono) / sr
    span = total / rows
    fig, axes = plt.subplots(2 * rows, 1, figsize=(26, 5.2 * rows),
                             gridspec_kw={"height_ratios": [3, 1] * rows})
    for r in range(rows):
        ax, ax2 = axes[2 * r], axes[2 * r + 1]
        lo, hi = r * span, (r + 1) * span
        m = (t >= lo - 1) & (t <= hi + 1)
        ax.pcolormesh(t[m], f[keep], db[keep][:, m], vmin=-90, vmax=0, cmap="magma", shading="auto")
        ax.set_yscale("log")
        ax.set_ylim(30, 12000)
        ax.set_xlim(lo, hi)
        ax.set_ylabel("Hz")
        me = (te >= lo) & (te <= hi)
        ax2.plot(te[me], 20 * np.log10(env[me] + 1e-9), lw=0.7, color="#333")
        for a_, b_ in sc.speech_iv:
            if b_ > lo and a_ < hi:
                ax2.axvspan(a_, b_, color="#9ecae1", alpha=0.35, lw=0)
        ax2.set_ylim(-70, 0)
        ax2.set_xlim(lo, hi)
        ax2.set_ylabel("RMS dB")
        for c in sc.cues:
            if lo - 1 <= c.t0 <= hi:
                for a_ in (ax, ax2):
                    a_.axvline(c.t0, color="cyan", lw=1.2)
                ax.text(c.t0 + 0.3, 9000, f"{c.id[:3]} {c.mood}", color="white", fontsize=11, va="top",
                        fontweight="bold")
            for sg_ in c.segs[1:]:
                if lo <= sg_.t0 <= hi:
                    ax.axvline(sg_.t0, color="white", lw=0.6, ls=":")
                    ax.text(sg_.t0 + 0.2, 40, sg_.label.split("-", 1)[-1], color="white", fontsize=7, rotation=90,
                            va="bottom")
        for cid, label, target, actual, kind in sc.syncs:
            if lo <= actual <= hi:
                ax2.plot([actual], [-5], "v" if kind == "hit" else "D", color="crimson", ms=6)
    axes[0].set_title("Background score - spectrogram (cyan = scene starts, dotted = segments, "
                      "blue = narration, red = hit points)")
    axes[-1].set_xlabel("seconds")
    fig.tight_layout()
    fig.savefig(path, dpi=55)
    plt.close(fig)
    print(f"  spectrogram: {path}")
