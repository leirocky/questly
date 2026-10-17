"""Automated checks of the rendered score -> build/preview/music_report.txt + music_spectrogram.png.

Harmony check: every pitched note is tested against its segment's scale(s) and the chord that is
sounding.  Harmonic roles (pad, bass, arp, harmony, timpani) must be chord tones for every chord
they sound through.  Melodic roles may use non-chord tones only when they behave like real
non-chord tones (passing, neighbour, suspension, appoggiatura, anticipation, escape, or short
unaccented notes); chromatic notes are allowed only as chromatic passing/neighbour notes.
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


def check_harmony(sc):
    stats = Counter()
    viol = []
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


def check_clashes(sc, min_overlap=0.3, min_dur=0.4):
    """Sustained minor-second / minor-ninth collisions between simultaneously sounding notes.

    Returns (unexpected, expected): 'expected' ones involve a classified non-chord tone
    (passing note, suspension, ...) or a glissando, i.e. dissonance that resolves by design."""
    notes = sorted([n for n in sc.notes if not PARTS[n.part].drum and n.role != "perc"], key=lambda n: n.t)
    out, exp = [], []
    active = []
    for n in notes:
        active = [a for a in active if a.t + a.d > n.t + min_overlap]
        for a in active:
            iv = abs(a.pitch - n.pitch)
            if iv in (1, 13) and min(a.d, n.d) >= min_dur:
                ov = min(a.t + a.d, n.t + n.d) - n.t
                if ov >= min_overlap:
                    (exp if (getattr(a, "nct", None) or getattr(n, "nct", None)) else out).append((a, n, ov))
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
                  ({"mbox"}, {"celesta"}), ({"celesta"}, {"vln_mel", "glock", "piano"})]
# intended parallel fifths (stylistic planing): (segment label, part set A, part set B)
PLANING_OK = [("call-God", {"choir"}, STRING_PARTS)]


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
                elif kind == "fifths" and any(lbl == a1[3].seg.label == b1[3].seg.label and _pair_ok(pa, pb, [(X, Y)])
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
    normalised to MUSIC_LUFS and ducked by MUSIC_DUCK_DB with mix.speech_envelope(voice).

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
    env = mixmod.speech_envelope(voice.astype(np.float32)).astype(np.float64)
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
STORM_OVER_MEDIAN = 6.0  # dB, the storm may be at most this much louder (RMS) than the median cue
STORM_PEAK_OVER_MEDIAN = 5.0   # dB, the storm-peak segment (hit + horn call) vs the median cue
PEAK_WINDOW_OVER_MEDIAN = 10.0  # dB, loudest 400 ms of the score vs its median 400 ms level


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

    # ---------------------------------------------------------------- per-scene levels
    w("PER-SCENE LEVELS (cue window = scene start -> next scene start; 'speech' = while a line is spoken)")
    w(f"{'scene':12s} {'mood':8s} {'start':>7s} {'len':>6s} {'RMS dB':>7s} {'peak dB':>8s} "
      f"{'speech RMS':>10s} {'gap RMS':>8s} {'L-R dB':>7s} {'onsets/s speech':>16s} {'gaps':>6s}")
    speech = sc.speaking(np.arange(len(x)) / sr)
    rows = []
    for c in sc.cues:
        a, b = int(c.t0 * sr), int(c.t1 * sr)
        seg = mono[a:b]
        sp = speech[a:b]
        r = _rms_db(x[a:b])
        rs = _rms_db(seg[sp]) if sp.sum() > sr * 0.3 else float("nan")
        rg = _rms_db(seg[~sp]) if (~sp).sum() > sr * 0.3 else float("nan")
        lr = _rms_db(x[a:b, 0]) - _rms_db(x[a:b, 1])
        ds, dg = onset_density(sc, c)
        rows.append((c, r))
        w(f"{c.id:12s} {c.mood:8s} {c.t0:7.2f} {c.dur:6.2f} {r:7.1f} {20 * np.log10(np.abs(x[a:b]).max()):8.1f} "
          f"{rs:10.1f} {rg:8.1f} {lr:7.1f} {ds:16.1f} {dg:6.1f}")
    w("")
    loud = max(rows, key=lambda r: r[1])[0].mood
    quiet = min(rows, key=lambda r: r[1])[0].mood
    med = float(np.median([r for _, r in rows]))
    storm_r = next((r for c, r in rows if c.mood == "storm"), float("nan"))
    w(f"loudest cue: {loud}, quietest cue: {quiet}; median cue RMS {med:.1f} dB, "
      f"storm {storm_r:.1f} dB = median {storm_r - med:+.1f} dB")
    checks.append(("storm is the loudest cue", loud == "storm", loud))
    checks.append(("belly is the quietest cue", quiet == "belly", quiet))
    checks.append((f"storm no more than {STORM_OVER_MEDIAN:.0f} dB above the median cue",
                   storm_r - med <= STORM_OVER_MEDIAN, f"{storm_r - med:+.1f} dB"))
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
        lifts[cue.mood].append(_rms_db(gi) - _rms_db(si))
    allv = [v for vs in lifts.values() for v in vs]
    for c in sc.cues:
        vs = lifts.get(c.mood, [])
        if vs:
            w(f"  {c.mood:8s} pauses {len(vs):2d}  median lift {np.median(vs):+5.1f} dB  (min {min(vs):+5.1f}, max {max(vs):+5.1f})")
    if allv:
        w(f"  all pauses: {len(allv)}, median lift {np.median(allv):+.1f} dB, 75th pct {np.percentile(allv, 75):+.1f} dB, "
          f"max {max(allv):+.1f} dB")
    w("")

    # ---------------------------------------------------------------- speech-to-music ratio in the mix
    smr = line_smr(timeline, x, sr, Path(wav_path).parent / "voice.wav")
    w(f"SPEECH-TO-MUSIC RATIO per line (simulated mix.py: music -> -27 LUFS, ducked 7 dB under speech; "
      f"active-speech frames; FAIL below {SMR_MIN:.0f} dB broadband)")
    if smr is None:
        w("  SKIPPED: build/audio/voice.wav not found")
        checks.append(("speech-to-music ratio >= 15 dB on every line", None, "voice.wav missing"))
    else:
        w(f"  {'scene':12s} {'line':>4s} {'SMR':>6s} {'1-4kHz':>7s} {'worst 200ms':>11s}  text")
        fails = []
        for sid, i, text, r, rb, rw in smr:
            flag = "  FAIL" if r < SMR_MIN else ""
            if flag:
                fails.append(f"{sid} L{i} {r:.1f}")
            w(f"  {sid:12s} {i:4d} {r:6.1f} {rb:7.1f} {rw:11.1f}  {text}{flag}")
        vals = [r for *_, r, rb, rw in smr]
        w(f"  min {min(vals):.1f} dB, median {np.median(vals):.1f} dB")
        checks.append((f"speech-to-music ratio >= {SMR_MIN:.0f} dB on every line", not fails,
                       f"min {min(vals):.1f} dB" + (f"; fails {fails}" if fails else "")))
    w("")

    # ---------------------------------------------------------------- spectral balance
    w("SPECTRAL BALANCE per cue (band energy relative to the cue total, dB)")
    bands = [(20, 150), (150, 600), (600, 2500), (2500, 6000), (6000, 20000)]

    def spec_row(seg):
        F = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        tot = F.sum() + 1e-20
        return [10 * np.log10(F[(fr >= a) & (fr < b)].sum() / tot + 1e-12) for a, b in bands], (F * fr).sum() / tot

    w(f"  {'cue':8s} " + " ".join(f"{f'{a}-{b}':>10s}" for a, b in bands) + "   centroid")
    for c in sc.cues:
        vals, cen = spec_row(mono[int(c.t0 * sr):int(c.t1 * sr)])
        w(f"  {c.mood:8s} " + " ".join(f"{v:10.1f}" for v in vals) + f"   {cen:7.0f} Hz")
    w("")
    w("SEGMENT LEVELS (RMS dB and 2.5-6 kHz share of each musical segment)")
    for c in sc.cues:
        for sg_ in c.segs:
            seg = mono[int(sg_.t0 * sr):int(sg_.t1 * sr)]
            vals, cen = spec_row(seg)
            w(f"  {sg_.label:24s} {sg_.t0:8.2f}-{sg_.t1:8.2f}  RMS {_rms_db(seg):6.1f} dB  2.5-6k {vals[3]:6.1f} dB  "
              f"centroid {cen:6.0f} Hz")
            if sg_.label == "vine-heat":
                checks.append(("vine-heat audible (RMS >= -33 dB) and not shrill (2.5-6k share < -10 dB)",
                               _rms_db(seg) >= -33 and vals[3] < -10, f"RMS {_rms_db(seg):.1f} dB, 2.5-6k {vals[3]:.1f} dB"))
            if sg_.label == "storm-peak":
                checks.append((f"storm-peak segment no more than {STORM_PEAK_OVER_MEDIAN:.0f} dB above the median cue",
                               _rms_db(seg) - med <= STORM_PEAK_OVER_MEDIAN, f"{_rms_db(seg) - med:+.1f} dB"))
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
    w(f"  sustained m2/m9 against non-chord tones that resolve (passing/suspension/gliss, by design): {len(expected)}")
    w(f"  UNEXPECTED sustained m2/m9 clashes (overlap >= 0.3 s, both notes >= 0.4 s): {len(clashes)}")
    for a, b2, ov in clashes[:40]:
        w(f"    ~ {a.t:7.2f}s {a.part}:{name(a.pitch)} ({a.role}) vs {b2.part}:{name(b2.pitch)} ({b2.role}) "
          f"overlap {ov:.2f}s")
    rng = check_ranges(sc)
    w(f"  notes outside instrument range: {len(rng)}")
    for n in rng[:20]:
        w(f"    ! {n.seg.cue.id} {n.part} {name(n.pitch)}")
    checks.append(("harmony: every note in scale / chord or a resolved non-chord tone", not viol, f"{len(viol)} violations"))
    checks.append(("no unexpected sustained m2/m9 clashes", not clashes, f"{len(clashes)}"))
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
            mel[(n.seg.cue.mood, n.part)].append(n)
    order = {c.mood: k for k, c in enumerate(sc.cues)}
    for (mood, part), lst in sorted(mel.items(), key=lambda kv: order[kv[0][0]]):
        lst.sort(key=lambda n: n.seg.t(n.q))
        ps = [n.pitch for n in lst]
        ivs = [abs(b - a) for a, b in zip(ps, ps[1:])]
        if not ivs:
            continue
        steps = sum(1 for v in ivs if v <= 2) / len(ivs)
        w(f"  {mood:8s} {part:9s} notes {len(ps):3d}  range {name(min(ps))}-{name(max(ps))} ({max(ps) - min(ps):2d} st)"
          f"  largest leap {max(ivs):2d} st  stepwise {100 * steps:3.0f}%")
    w("")

    # ---------------------------------------------------------------- orchestration summary
    w("ORCHESTRATION (notes per part per cue)")
    per = defaultdict(Counter)
    for n in sc.notes:
        per[n.seg.cue.mood][n.part] += 1
    for c in sc.cues:
        w(f"  {c.mood:8s} " + ", ".join(f"{p} {k}" for p, k in sorted(per[c.mood].items(), key=lambda kv: -kv[1])))
    w("")
    w("BUS LEVELS (dry stems, RMS dB per cue)")
    w("  " + " ".join(f"{b:>7s}" for b in stems) + "   cue")
    for c in sc.cues:
        a, b = int(c.t0 * sr), int(c.t1 * sr)
        w("  " + " ".join(f"{_rms_db(st[a:b]):7.1f}" for st in stems.values()) + f"   {c.mood}")

    head = ["MUSIC REPORT — 约拿的故事 background score", "", "SUMMARY"]
    for nm, ok_, det in checks:
        head.append(f"  [{'PASS' if ok_ else ('SKIP' if ok_ is None else 'FAIL')}] {nm}: {det}")
    head.append("")
    text = "\n".join(head + L) + "\n"
    (out_dir / "music_report.txt").write_text(text)
    n_fail = sum(1 for _, ok_, _ in checks if ok_ is False)
    print(f"  report: {out_dir / 'music_report.txt'} ({n_fail} failed checks; {len(viol)} harmony violations, "
          f"{len(gbad)} global parallels)")
    _spectrogram(mono, sr, sc, out_dir / "music_spectrogram.png")
    return text


def _spectrogram(mono, sr, sc, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  (matplotlib missing: no spectrogram)")
        return
    from scipy import signal as sg
    f, t, S = sg.stft(mono, fs=sr, nperseg=4096, noverlap=4096 - 1024)
    db = 20 * np.log10(np.abs(S) + 1e-9)
    db -= db.max()
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(22, 9), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    keep = (f >= 30) & (f <= 12000)
    ax.pcolormesh(t, f[keep], db[keep], vmin=-90, vmax=0, cmap="magma", shading="auto")
    ax.set_yscale("log")
    ax.set_ylim(30, 12000)
    ax.set_ylabel("Hz")
    hop = int(0.05 * sr)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, "same"))[::hop]
    te = np.arange(len(env)) * 0.05
    ax2.plot(te, 20 * np.log10(env + 1e-9), lw=0.7, color="#333")
    for a, b in sc.speech_iv:
        ax2.axvspan(a, b, color="#9ecae1", alpha=0.35, lw=0)
    ax2.set_ylim(-70, 0)
    ax2.set_ylabel("RMS dB (blue = narration)")
    ax2.set_xlabel("seconds")
    for c in sc.cues:
        for a_ in (ax, ax2):
            a_.axvline(c.t0, color="cyan", lw=1.0)
        ax.text(c.t0 + 0.2, 9000, c.mood, color="white", fontsize=10, va="top")
        for s in c.segs[1:]:
            ax.axvline(s.t0, color="white", lw=0.5, ls=":")
    for cid, label, target, actual, kind in sc.syncs:
        ax2.plot([actual], [-5], "v" if kind == "hit" else "D", color="crimson", ms=5)
    ax.set_title("Background score — spectrogram (cyan = scene starts, dotted = hit-point segments)")
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)
    print(f"  spectrogram: {path}")
