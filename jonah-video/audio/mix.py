"""Final audio mix: narration + ducked music + scene sound effects.

Inputs   build/audio/voice.wav (mono, from voice/tts.py)
         build/audio/music.wav (stereo, from audio/music.py)
         SFX cues declared by each scene (Scene.sfx), synthesised by audio/sfx.py
Output   build/audio/mix.wav (48 kHz stereo, -16 LUFS integrated, true peak <= -1.7 dBTP so the AAC 160k encode
         stays <= -1 dBTP)
         build/audio/stem_music.wav, stem_sfx.wav (for inspection)
         build/audio/speech_report.txt (speech-band margins per line, true peak, one-shot lift, duck swings, where
         the music bed breathes), build/audio/oneshot_report.txt (every one-shot's lift over its bed / bed + music)

Ducking under the narration (one speech envelope, two time constants):
  * the music and the ambience beds follow the BED envelope (bed_envelope): which pauses it holds is decided
    by the TIMELINE, not by the voice energy -- every line counts as speech, and so does every gap between
    lines shorter than BED_ENV['line_bridge'] s (sentence pauses ~0.63-0.86 s and scene changes ~1.19-1.22 s
    in this film), so the duck holds through all of them however quietly a line begins or ends; it breathes
    up along a slow raised cosine only in the longer pauses (here the 1.49 s after the title and the 2.5 s
    rest in s24), so the music no longer swells in every breath or at every scene change;
  * one-shot effects follow the FX envelope (fast; short gaps only), so an on-picture action placed in a pause
    is heard; under speech they duck as deep as the beds (SFX_DUCK_DB = ONESHOT_DUCK_DB) and stay above them;
  * a cue with ``duck_db`` set (Scene.sfx(..., duck_db=-3)) is ducked by that amount instead, on its own
    pre-ducked bus (same envelope as its kind).
"""
import zlib

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import ndimage, signal

from engine.loader import build_scene, load_timeline
from engine.paths import BUILD, SR

MUSIC_LUFS = -27.0      # music bed loudness before ducking (narration clips sit at -20 LUFS)
MUSIC_DUCK_DB = -7.0    # extra attenuation while someone is speaking
SFX_DUCK_DB = -9.0      # ambience loops under speech
ONESHOT_DUCK_DB = -9.0  # one-shot effects under speech: as deep as the beds, so an action stays above its bed
SPEECH_MARGIN_DB = 12.0  # narration must stay at least this far above music + sfx on every line
FINAL_LUFS = -16.0
KEY_ONESHOTS = ("splash", "thunder", "gulp", "horn", "thud", "crunch", "spit", "hammer")
TP_CEILING_DB = -1.7    # true-peak ceiling of mix.wav: the AAC 160k encode adds ~0.3-0.6 dB of overshoot (measured
                        # +0.4 dB on this film: -1.5 dBTP -> -1.1 dBTP), so this keeps the delivery <= -1.1 dBTP
# envelope time constants (s): raised-cosine attack ending at each speech onset (look-ahead), hold, raised-cosine
# release; pauses shorter than `bridge` (on the voice energy) count as speech.  The BED envelope is driven by the
# line timings instead (`line_bridge`): pauses measured on the voice energy run longer than the timeline's and
# vary with how softly a line starts (scene changes, 1.19-1.22 s by the timeline, measure 1.24-1.50 s on the
# voice: s10 -> s11 '大鱼的肚子里' starts at -44..-62 dB), so no energy threshold separates them reliably from
# the 1.49 s title pause.  line_bridge = 1.35 s sits half-way between the longest scene change (1.22 s) and the
# title pause (1.49 s); `bridge` is then only the fallback without a timeline (the energy bridges blips < 0.3 s)
BED_ENV = dict(attack=0.15, hold=0.1, release=1.3, bridge=1.45, line_bridge=1.35)
FX_ENV = dict(attack=0.08, hold=0.0, release=0.7, bridge=0.25)
BLIP = 0.3              # with line timings, energy-only bridging is limited to blips this short


def _to_stereo(x):
    return np.stack([x, x], axis=1) if x.ndim == 1 else x[:, :2]


def _fit(x, n):
    if len(x) >= n:
        return x[:n]
    pad = np.zeros((n - len(x),) + x.shape[1:], x.dtype)
    return np.concatenate([x, pad])


def collect_cues(tl):
    cues = []
    for s in tl["scenes"]:
        sc = build_scene(s["id"], tl)
        for c in sc.sfx_cues:
            c = dict(c)
            c["t"] = s["start"] + c["at"]
            c["scene"] = s["id"]
            cues.append(c)
    return cues


def _duck(env, db):
    return (10 ** (db * env / 20)).astype(np.float32)


def render_sfx(tl, cues, n, envs=None):
    """Synthesise and place every cue.  Returns (loops, oneshots, pre) -- the two buses still to be ducked, and
    {kind: bus} of the cues with their own ``duck_db``, already ducked by it with envs[kind] (when envs is None
    they go to their kind's bus)."""
    from audio import sfx

    loops = np.zeros((n, 2), np.float32)
    oneshots = np.zeros((n, 2), np.float32)
    pre = {}
    for c in cues:
        seed = zlib.crc32(f"{c['scene']}:{c['name']}:{c['at']}".encode()) & 0xFFFF
        x = sfx.make(c["name"], c["dur"], SR, seed=seed, **c["params"])
        x = _to_stereo(np.asarray(x, np.float32))
        if c["dur"] is not None:
            x = _fit(x, int(c["dur"] * SR))
        m = len(x)
        if m == 0:
            continue
        fi, fo = int(c["fade_in"] * SR), int(c["fade_out"] * SR)
        env = np.ones(m, np.float32)
        if fi > 0:
            env[:min(fi, m)] = np.linspace(0, 1, min(fi, m))
        if fo > 0:
            env[-min(fo, m):] *= np.linspace(1, 0, min(fo, m))
        g = 10 ** (c["gain_db"] / 20)
        pan = max(-1.0, min(1.0, c["pan"]))
        a = (pan + 1) * np.pi / 4
        x = x * env[:, None] * g * np.array([np.cos(a), np.sin(a)], np.float32) * np.sqrt(2)
        start = int(round(c["t"] * SR))
        if start < 0:
            x, start = x[-start:], 0
        end = min(n, start + len(x))
        if end <= start:
            continue
        kind = sfx.NAMES[c["name"]][0]
        if c.get("duck_db") is not None and envs is not None:
            if kind not in pre:
                pre[kind] = np.zeros((n, 2), np.float32)
            pre[kind][start:end] += x[: end - start] * _duck(envs[kind][start:end], float(c["duck_db"]))[:, None]
        else:
            (oneshots if kind == "oneshot" else loops)[start:end] += x[: end - start]
    return loops, oneshots, pre


def line_intervals(tl):
    """Sorted global (start, end) s of every narration line."""
    return sorted((s["start"] + ln["start"], s["start"] + ln["end"]) for s in tl["scenes"] for ln in s["lines"])


def held_stretches(lines, gap):
    """Narration stretches: lines less than ``gap`` s apart merged into one [start, end]."""
    out = []
    for a, b in sorted(lines):
        if out and a - out[-1][1] < gap:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def speech_envelope(voice, attack=BED_ENV["attack"], hold=BED_ENV["hold"], release=BED_ENV["release"],
                    bridge=BED_ENV["bridge"], thresh_db=-42, lines=None, line_bridge=None):
    """0..1 envelope of the narration (10 ms frames, interpolated to samples).

    Frames above thresh_db are speech.  With ``lines`` (global (start, end) s of the narration lines) and
    ``line_bridge``, every line and every gap between lines shorter than line_bridge also count as speech
    (the timeline decides which pauses are held; the voice energy only adds what lies outside the lines) and
    energy-only pauses are filled up to BLIP s; without lines, pauses shorter than ``bridge`` s are filled.
    The envelope rises along a raised cosine over ``attack`` s that ends exactly at each speech onset
    (look-ahead: fully ducked when the word starts), holds ``hold`` s after the speech and falls along a raised
    cosine over ``release`` s.  bed_envelope() gives the BED envelope (music, ambience); one-shots use FX_ENV."""
    fr = 0.01
    hop = int(fr * SR)
    nh = len(voice) // hop + 1
    v = _fit(voice, nh * hop).reshape(nh, hop)
    db = 10 * np.log10(np.mean(v.astype(np.float64) ** 2, axis=1) + 1e-12)
    active = db > thresh_db
    if lines is not None and line_bridge is not None:
        for a, b in held_stretches(lines, line_bridge):
            active[max(0, int(np.floor(a / fr))): min(nh, int(np.ceil(b / fr)) + 1)] = True
        bridge = min(bridge, BLIP)
    # bridge: fill every pause (inactive run between two active frames) shorter than `bridge`
    idx = np.nonzero(active)[0]
    if len(idx) > 1:
        gaps = np.diff(idx) - 1
        for i in np.nonzero((gaps > 0) & (gaps * fr < bridge))[0]:
            active[idx[i] + 1: idx[i + 1]] = True
    k = np.arange(nh)
    big = 10 ** 9
    last = np.maximum.accumulate(np.where(active, k, -big))           # most recent active frame
    nxt = np.minimum.accumulate(np.where(active, k, big)[::-1])[::-1]  # next active frame
    d_prev = (k - last) * fr
    d_next = (nxt - k) * fr

    def rc(x):              # raised cosine 1 -> 0 for x in 0..1, 0 beyond
        return np.where(x <= 0, 1.0, np.where(x >= 1, 0.0, 0.5 * (1 + np.cos(np.pi * np.clip(x, 0, 1)))))

    up = rc(d_next / max(attack, fr))
    dn = rc((d_prev - hold) / max(release, fr))
    env = np.maximum(up, dn)
    env[active] = 1.0
    return np.interp(np.arange(len(voice)) / hop, k, env).astype(np.float32)


def bed_envelope(voice, tl):
    """The BED envelope (music and ambience beds): held through every timeline gap < BED_ENV['line_bridge']."""
    return speech_envelope(voice, lines=line_intervals(tl), **BED_ENV)


def _rms_db(x):
    return 10 * np.log10(np.mean(np.square(x, dtype=np.float64)) + 1e-12)


def protect_speech(tl, voice, music, sfx, target_db=SPEECH_MARGIN_DB, ramp=0.25):
    """Extra, smoothly ramped background attenuation on any line where the background
    (music + sfx) is less than ``target_db`` below the narration. Returns new stems + report."""
    n = len(voice)
    gain_db = np.zeros(n, np.float32)
    rows = []
    # Measure in the speech band (300-4000 Hz): that is what small speakers reproduce and what
    # carries intelligibility, so bass-heavy voices or rumbling effects can't pass on full-band RMS.
    band = signal.butter(4, [300, 4000], "bandpass", fs=SR, output="sos")
    v_band = signal.sosfiltfilt(band, voice)
    bg_band = signal.sosfiltfilt(band, (music + sfx).mean(axis=1))
    for s in tl["scenes"]:
        for i, ln in enumerate(s["lines"]):
            a = int((s["start"] + ln["start"]) * SR)
            b = min(n, int((s["start"] + ln["end"]) * SR))
            if b <= a:
                continue
            v = _rms_db(v_band[a:b])
            bg = _rms_db(bg_band[a:b])
            need = min(0.0, (v - bg) - target_db)          # negative dB if background too loud
            if need < 0:
                gain_db[a:b] = np.minimum(gain_db[a:b], need)
            rows.append((s["id"], i, v - bg, need))
    # Smooth the gain curve so cuts ramp in/out over ``ramp`` seconds (and start slightly early).
    k = int(ramp * SR)
    g = ndimage.minimum_filter1d(gain_db, k)
    g = ndimage.uniform_filter1d(g, 2 * k)
    gl = (10 ** (g / 20)).astype(np.float32)[:, None]
    lines = [f"speech-to-background target {target_db:.0f} dB (300-4000 Hz band)"]
    for sid, i, m, need in rows:
        lines.append(f"{sid:12s} line {i}: {m:5.1f} dB" + (f"  -> background cut {need:.1f} dB" if need < 0 else ""))
    music, sfx = music * gl, sfx * gl
    bg_band = bg_band * gl[:, 0]
    after = []
    for s in tl["scenes"]:
        for ln in s["lines"]:
            a, b = int((s["start"] + ln["start"]) * SR), min(n, int((s["start"] + ln["end"]) * SR))
            if b > a:
                after.append(_rms_db(v_band[a:b]) - _rms_db(bg_band[a:b]))
    worst = min(r[2] for r in rows)
    lines.append(f"worst before protection {worst:.1f} dB; lines adjusted {sum(1 for r in rows if r[3] < 0)}; "
                 f"worst after {min(after):.1f} dB")
    return music, sfx, "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------- true-peak limiter

def true_peak(x, os=4, block=1 << 18):
    """Per-sample true-peak magnitude: max over the channels of the ``os``-times oversampled signal between
    each sample and the next (polyphase FIR interpolation, processed in blocks)."""
    x = x if x.ndim == 2 else x[:, None]
    n = len(x)
    out = np.empty(n, np.float32)
    pad = 64
    for a in range(0, n, block):
        b = min(n, a + block)
        a0, b0 = max(0, a - pad), min(n, b + pad)
        y = signal.resample_poly(x[a0:b0].astype(np.float64), os, 1, axis=0)
        m = np.abs(y).max(axis=1).reshape(-1, os).max(axis=1)
        out[a:b] = m[a - a0: a - a0 + (b - a)]
    return out


def _gain_reduction(need, look, hold, release, block=24):
    """Gain reduction (dB) >= need (dB) at every sample: a raised-cosine fall over ~2 x ``look`` s that ends
    at each over (look-ahead), then ``hold`` s and a raised-cosine recovery over ``release`` s."""
    la = max(1, int(look * SR))
    # attack: max over +-la, smoothed by a Hann window of the same span -> S-shaped ramps of 2*la; the window
    # around an over only sees values >= its need, so the result still covers it
    r1 = ndimage.maximum_filter1d(need, 2 * la + 1)
    w = np.hanning(2 * la + 3)[1:-1]
    r2 = signal.oaconvolve(r1, w / w.sum(), mode="same").astype(np.float32)
    r2 = np.maximum(r2, 0)
    # hold + raised-cosine release, on 0.5 ms blocks (max per block), back to samples by linear interpolation
    # between conservative block edges
    nb = -(-len(r2) // block)
    rb = _fit(r2, nb * block).reshape(nb, block).max(axis=1)
    h, r = int(round(hold * SR / block)), max(1, int(round(release * SR / block)))
    rel = rb.copy()
    for d in range(1, h + r + 1):
        c = 1.0 if d <= h else 0.5 * (1 + np.cos(np.pi * (d - h) / r))
        np.maximum(rel[d:], rb[:-d] * c, out=rel[d:])
    edges = np.maximum(np.concatenate([[rel[0]], rel]), np.concatenate([rel, [rel[-1]]]))   # nb + 1 edges
    ri = np.interp(np.arange(len(r2)) / block, np.arange(nb + 1), edges).astype(np.float32)
    return np.maximum(r2, ri)


def limit(x, ceiling_db=TP_CEILING_DB, look=0.0025, hold=0.005, release=0.08, passes=4):
    """True-peak look-ahead limiter (4x oversampled detection, raised-cosine attack and release).  Returns the
    limited signal and stats (true peak before / after, max gain reduction, seconds with > 0.5 dB of it)."""
    ceiling = 10 ** (ceiling_db / 20)
    gr_tot = np.zeros(len(x), np.float32)
    tp0 = None
    for _ in range(passes):
        tp = true_peak(x)
        if tp0 is None:
            tp0 = float(tp.max())
        need = np.maximum(0.0, 20 * np.log10(np.maximum(tp, 1e-9) / ceiling)).astype(np.float32)
        if need.max() <= 0.002:
            break
        gr = _gain_reduction(need + 0.02 * (need > 0), look, hold, release)
        gr_tot += gr
        x = x * (10 ** (-gr / 20))[:, None]
    tp1 = float(true_peak(x).max())
    stats = dict(tp_in_db=20 * np.log10(tp0), tp_out_db=20 * np.log10(tp1), max_gr_db=float(gr_tot.max()),
                 s_over_0_5db=float((gr_tot > 0.5).sum()) / SR)
    return x, stats


def loudness(x):
    return pyln.Meter(SR).integrated_loudness(x.astype(np.float64))


# ---------------------------------------------------------------------------------------- diagnostics

def oneshot_lift(cues, oneshots, beds, music=None, win=0.3, hop=0.05):
    """For every one-shot cue: its ducked bus level in its loudest 300 ms (within its first second) minus the
    ducked ambience beds over the same window (dB), and minus beds + ducked music.  Returns
    [(t, scene, name, lift over the beds, lift over beds + music or nan)] (no bed: skipped)."""
    from audio import sfx

    out = []
    w, hp = int(win * SR), int(hop * SR)
    for c in cues:
        if sfx.NAMES[c["name"]][0] != "oneshot":
            continue
        a = int(c["t"] * SR)
        L = min(1.0, c["dur"] or sfx.NAMES[c["name"]][1])
        best = None
        for s in range(a, a + max(hp, int(L * SR) - w + 1), hp):
            if s < 0 or s + w > len(oneshots):
                continue
            lv = _rms_db(oneshots[s:s + w])
            if best is None or lv > best[0]:
                best = (lv, s)
        if best is None:
            continue
        bed = _rms_db(beds[best[1]:best[1] + w])
        if bed < -75:
            continue
        bm = (best[0] - _rms_db(beds[best[1]:best[1] + w] + music[best[1]:best[1] + w])) if music is not None \
            else float("nan")
        out.append((c["t"], c["scene"], c["name"], best[0] - bed, bm))
    return out


def duck_swings(gain_db, tl, min_db=3.0, merge=BED_ENV["line_bridge"], fr=0.01):
    """Swings (> min_db rises that fall back) of a duck-gain curve (dB, one value per fr s) inside stretches of
    continuous narration (lines < merge s apart).  Returns (count, minutes)."""
    st = held_stretches(line_intervals(tl), merge)
    cnt, tot = 0, 0.0
    for a, b in st:
        seg = gain_db[int(a / fr):int(b / fr)]
        if len(seg) < 3:
            continue
        pk, _ = signal.find_peaks(seg, prominence=min_db)
        cnt += len(pk)
        tot += b - a
    return cnt, tot / 60


def bed_breaths(gain_db, tl, min_db=1.0, fr=0.01):
    """Every pause between lines where the bed duck (dB curve, one value per fr s) releases by more than min_db:
    [(pause start s, pause length s, rise dB)] -- where the music is allowed to breathe."""
    iv = line_intervals(tl)
    floor = float(gain_db.min())
    out = []
    for (a0, a1), (b0, b1) in zip(iv, iv[1:]):
        seg = gain_db[int(a1 / fr):int(b0 / fr) + 1]
        if len(seg) and seg.max() - floor > min_db:
            out.append((a1, b0 - a1, float(seg.max() - floor)))
    return out


def mix():
    tl = load_timeline()
    total = tl["duration"]
    n = int(total * SR)
    voice, sr = sf.read(BUILD / "audio" / "voice.wav", dtype="float32")
    assert sr == SR
    voice = _fit(voice, n)

    music_path = BUILD / "audio" / "music.wav"
    if music_path.exists():
        music, sr = sf.read(music_path, dtype="float32")
        assert sr == SR
        music = _fit(_to_stereo(music), n)
        lm = loudness(music)
        if np.isfinite(lm):
            music *= 10 ** ((MUSIC_LUFS - lm) / 20)
    else:
        print("  (no music.wav — mixing without music)")
        music = np.zeros((n, 2), np.float32)

    env_bed = bed_envelope(voice, tl)
    env_fx = speech_envelope(voice, **FX_ENV)
    cues = collect_cues(tl)
    loops, oneshots, pre = render_sfx(tl, cues, n, envs={"loop": env_bed, "oneshot": env_fx})
    music_d = music * _duck(env_bed, MUSIC_DUCK_DB)[:, None]
    loops *= _duck(env_bed, SFX_DUCK_DB)[:, None]
    oneshots *= _duck(env_fx, ONESHOT_DUCK_DB)[:, None]
    for kind, bus in pre.items():           # cues with their own duck_db, already ducked
        (oneshots if kind == "oneshot" else loops)[:] += bus
    del pre
    lift = oneshot_lift(cues, oneshots, loops, music_d)
    sfx_d = loops + oneshots
    del loops, oneshots
    music_d, sfx_d, report = protect_speech(tl, voice, music_d, sfx_d)

    out = _to_stereo(voice) + music_d + sfx_d
    # Gentle fade in/out of the whole film.
    fi, fo = int(0.5 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]
    out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    out = signal.sosfiltfilt(signal.butter(2, 20, "highpass", fs=SR, output="sos"), out, axis=0)  # DC/infrasound
    # loudness to FINAL_LUFS, then the true-peak limiter; repeat the gain if limiting moved the loudness
    out *= 10 ** ((FINAL_LUFS - loudness(out)) / 20)
    for _ in range(3):
        lim, st = limit(out)
        lo = loudness(lim)
        if abs(lo - FINAL_LUFS) <= 0.05:
            break
        out *= 10 ** ((FINAL_LUFS - lo) / 20)
    out = lim.astype(np.float32)
    del lim

    lifts = np.array([x[3] for x in lift]) if lift else np.array([np.nan])
    duck_of = {(c["t"], c["name"]): c.get("duck_db") for c in cues}
    from audio import picture
    doubled = {(sid, nm) for sid, nm, *_ in picture.EVENTS.values()}     # the score hits these on the same frame
    rows = sorted(((t, sid, nm, a, b, duck_of.get((t, nm)), (sid, nm) in doubled) for t, sid, nm, a, b in lift),
                  key=lambda r: r[3])
    weak = [r for r in rows if r[2] in KEY_ONESHOTS][:10]
    (BUILD / "audio" / "oneshot_report.txt").write_text(
        "one-shot cues, weakest first: time s, scene, cue, loudest 300 ms of the ducked one-shot bus over the ducked "
        "beds / over beds + ducked music (dB), the cue's own duck_db; * = the score hits the same picture event "
        "(audio/picture.py), so its 'music' is that hit\n" + "".join(
            f"{t:8.2f}  {sid:14s} {nm:13s} {a:+6.1f} / {b:+6.1f}" + (f"  duck_db {d:g}" if d is not None else "")
            + ("  *" if dbl else "") + "\n" for t, sid, nm, a, b, d, dbl in rows))
    g_bed = MUSIC_DUCK_DB * env_bed[::int(0.01 * SR)]
    sw_after = duck_swings(g_bed, tl)
    breaths = bed_breaths(g_bed, tl)
    iv = line_intervals(tl)
    gaps = np.array([b0 - a1 for (a0, a1), (b0, b1) in zip(iv, iv[1:])])
    report += (f"true peak: {st['tp_in_db']:.2f} dBTP before the limiter, {st['tp_out_db']:.2f} dBTP after (ceiling "
               f"{TP_CEILING_DB} dBTP, 4x oversampled); max gain reduction {st['max_gr_db']:.1f} dB, "
               f"{st['s_over_0_5db']:.2f} s above 0.5 dB\n"
               f"integrated loudness {loudness(out):.2f} LUFS (target {FINAL_LUFS})\n"
               f"one-shot effects vs their ambience beds (loudest 300 ms, ducked): median lift {np.nanmedian(lifts):+.1f} dB, "
               f"25th pct {np.nanpercentile(lifts, 25):+.1f} dB, {int((lifts < 3).sum())} of {len(lift)} cues below +3 dB\n"
               f"weakest key one-shots ({', '.join(KEY_ONESHOTS)}) over their beds / over beds + music (dB; * = the "
               f"score hits the same frame; all cues in oneshot_report.txt; scene authors can raise gain_db or set "
               f"duck_db): " + ", ".join(
                   f"{sid} {nm} {t:.2f} s {a:+.1f}/{b:+.1f}" + (f" [duck_db {d:g}]" if d is not None else "")
                   + ("*" if dbl else "") for t, sid, nm, a, b, d, dbl in weak) + "\n"
               f"music duck swings > 3 dB inside continuous narration: {sw_after[0]} in {sw_after[1]:.1f} min "
               f"({sw_after[0] / max(sw_after[1], 1e-9):.2f}/min)\n"
               f"music bed held through {int((gaps < BED_ENV['line_bridge']).sum())} of {len(gaps)} pauses between lines "
               f"(timeline gap < {BED_ENV['line_bridge']} s); it breathes (duck release > 1 dB) in {len(breaths)}: "
               + ", ".join(f"{a:.2f} s ({d:.2f} s pause, +{r:.1f} dB)" for a, d, r in breaths) + "\n")
    (BUILD / "audio" / "speech_report.txt").write_text(report)
    sf.write(BUILD / "audio" / "stem_music.wav", music_d, SR)
    sf.write(BUILD / "audio" / "stem_sfx.wav", sfx_d, SR)
    sf.write(BUILD / "audio" / "mix.wav", out, SR)
    print(f"  mix: {total:.2f}s, {loudness(out):.1f} LUFS, sample peak {np.abs(out).max():.3f}, "
          f"true peak {st['tp_out_db']:.2f} dBTP")
    return BUILD / "audio" / "mix.wav"


if __name__ == "__main__":
    mix()
