"""Final audio mix: narration + ducked music + scene sound effects.

Inputs   build/audio/voice.wav (mono, from voice/tts.py)
         build/audio/music.wav (stereo, from audio/music.py)
         SFX cues declared by each scene (Scene.sfx), synthesised by audio/sfx.py
Output   build/audio/mix.wav (48 kHz stereo, -16 LUFS integrated, peaks <= -1 dBFS)
         build/audio/stem_music.wav, stem_sfx.wav (for inspection)
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
SFX_DUCK_DB = -6.0
SPEECH_MARGIN_DB = 12.0  # narration must stay at least this far above music + sfx on every line
FINAL_LUFS = -16.0
CEILING = 0.89          # ~ -1 dBFS


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


def render_sfx(tl, cues, n):
    from audio import sfx

    out = np.zeros((n, 2), np.float32)
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
        if end > start:
            out[start:end] += x[: end - start]
    return out


def speech_envelope(voice, attack=0.08, release=0.7, thresh_db=-42):
    """0..1 envelope that rises shortly *before* speech and relaxes after it."""
    hop = int(0.01 * SR)
    nh = len(voice) // hop + 1
    v = _fit(voice, nh * hop).reshape(nh, hop)
    db = 10 * np.log10(np.mean(v ** 2, axis=1) + 1e-12)
    active = (db > thresh_db).astype(np.float32)
    active = ndimage.maximum_filter1d(active, int(0.25 / 0.01))       # bridge short pauses
    active = np.roll(active, -int(attack / 0.01))                     # look ahead
    a_up, a_dn = 1 - np.exp(-1 / (attack / 0.01)), 1 - np.exp(-1 / (release / 0.01))
    env = np.zeros(nh, np.float32)
    e = 0.0
    for i in range(nh):
        k = a_up if active[i] > e else a_dn
        e += k * (active[i] - e)
        env[i] = e
    return np.interp(np.arange(len(voice)) / hop, np.arange(nh), env).astype(np.float32)


def _rms_db(x):
    return 10 * np.log10(np.mean(np.square(x, dtype=np.float64)) + 1e-12)


def protect_speech(tl, voice, music, sfx, target_db=SPEECH_MARGIN_DB, ramp=0.25):
    """Extra, smoothly ramped background attenuation on any line where the background
    (music + sfx) is less than ``target_db`` below the narration. Returns new stems + report."""
    n = len(voice)
    gain_db = np.zeros(n, np.float32)
    rows = []
    for s in tl["scenes"]:
        for i, ln in enumerate(s["lines"]):
            a = int((s["start"] + ln["start"]) * SR)
            b = min(n, int((s["start"] + ln["end"]) * SR))
            if b <= a:
                continue
            v = _rms_db(voice[a:b])
            bg = _rms_db(music[a:b] + sfx[a:b])
            need = min(0.0, (v - bg) - target_db)          # negative dB if background too loud
            if need < 0:
                gain_db[a:b] = np.minimum(gain_db[a:b], need)
            rows.append((s["id"], i, v - bg, need))
    # Smooth the gain curve so cuts ramp in/out over ``ramp`` seconds (and start slightly early).
    k = int(ramp * SR)
    g = ndimage.minimum_filter1d(gain_db, k)
    g = ndimage.uniform_filter1d(g, 2 * k)
    gl = (10 ** (g / 20)).astype(np.float32)[:, None]
    lines = [f"speech-to-background target {target_db:.0f} dB"]
    for sid, i, m, need in rows:
        lines.append(f"{sid:12s} line {i}: {m:5.1f} dB" + (f"  -> background cut {need:.1f} dB" if need < 0 else ""))
    music, sfx = music * gl, sfx * gl
    after = []
    for s in tl["scenes"]:
        for ln in s["lines"]:
            a, b = int((s["start"] + ln["start"]) * SR), min(n, int((s["start"] + ln["end"]) * SR))
            if b > a:
                after.append(_rms_db(voice[a:b]) - _rms_db(music[a:b] + sfx[a:b]))
    worst = min(r[2] for r in rows)
    lines.append(f"worst before protection {worst:.1f} dB; lines adjusted {sum(1 for r in rows if r[3] < 0)}; "
                 f"worst after {min(after):.1f} dB")
    return music, sfx, "\n".join(lines) + "\n"


def limit(x, ceiling=CEILING, release=0.08):
    """Look-ahead peak limiter (5 ms)."""
    peak = np.max(np.abs(x), axis=1)
    gain = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    look = int(0.005 * SR)
    gain = ndimage.minimum_filter1d(gain, 2 * look + 1)
    b, a = [1 - np.exp(-1 / (release * SR))], [1, -np.exp(-1 / (release * SR))]
    smooth = signal.lfilter(b, a, gain)
    gain = np.minimum(gain, smooth)
    return x * gain[:, None]


def loudness(x):
    return pyln.Meter(SR).integrated_loudness(x.astype(np.float64))


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

    sfx = render_sfx(tl, collect_cues(tl), n)
    env = speech_envelope(voice)[:, None]
    music_d = music * 10 ** (MUSIC_DUCK_DB * env / 20)
    sfx_d = sfx * 10 ** (SFX_DUCK_DB * env / 20)
    music_d, sfx_d, report = protect_speech(tl, voice, music_d, sfx_d)
    (BUILD / "audio" / "speech_report.txt").write_text(report)

    out = _to_stereo(voice) + music_d + sfx_d
    # Gentle fade in/out of the whole film.
    fi, fo = int(0.5 * SR), int(2.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]
    out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    lo = loudness(out)
    out *= 10 ** ((FINAL_LUFS - lo) / 20)
    out = limit(out).astype(np.float32)

    sf.write(BUILD / "audio" / "stem_music.wav", music_d, SR)
    sf.write(BUILD / "audio" / "stem_sfx.wav", sfx_d, SR)
    sf.write(BUILD / "audio" / "mix.wav", out, SR)
    print(f"  mix: {total:.2f}s, {loudness(out):.1f} LUFS, peak {np.abs(out).max():.3f}")
    return BUILD / "audio" / "mix.wav"


if __name__ == "__main__":
    mix()
