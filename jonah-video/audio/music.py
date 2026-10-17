"""Background score renderer: audio/score.py -> MIDI (per bus) -> fluidsynth -> numpy mix.

    python3 build.py music        # build/audio/music.wav + build/preview/music_report.txt / .png

The score is generated from the timeline (scene starts, line timings), rendered with
fluidsynth and MuseScore_General.sf3 (dry), then mixed here: per-bus convolution reverb
(synthetic hall impulse response), an echo line for the celesta drops inside the fish, an
extra dark "cave" reverb during the belly scene, a high-pass, loudness normalisation and a
gentle look-ahead peak limiter.  Output: 48 kHz stereo WAV of exactly timeline['duration'].
"""
import shutil
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import ndimage, signal

from audio import score as score_mod
from audio.scorekit import SR, fluidsynth_render

# bus -> (gain dB, hall send, high-pass Hz)
BUSES = {
    "str_hi": (0.0, 0.42, 30),     # violins, choirs (the string bus is split: 15 MIDI channels per file)
    "str_lo": (0.0, 0.42, 30),     # violas, cellos, basses, pad
    "keys": (-1.0, 0.36, 60),
    "wind": (-1.0, 0.32, 45),
    "pluck": (0.0, 0.24, 40),
    "perc": (-1.0, 0.30, 30),
    "hand": (-2.0, 0.22, 40),
    "echo": (-1.0, 0.55, 80),
}
TARGET_LUFS = -20.0
CEILING = 0.90


def make_ir(rt60, seed, pre=0.02, length=None, dark=1.0):
    """Synthetic stereo hall impulse response with frequency-dependent decay (unit energy)."""
    n = int((length or rt60 * 1.3) * SR)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    f = np.fft.rfftfreq(n, 1 / SR)
    bands = [(0, 200, 1.1), (200, 1200, 1.0), (1200, 4000, 0.72 / dark), (4000, SR / 2, 0.42 / dark)]
    ir = np.zeros((n, 2))
    for ch in range(2):
        spec = np.fft.rfft(rng.standard_normal(n))
        out = np.zeros(n)
        for lo, hi, k in bands:
            band = np.fft.irfft(spec * ((f >= lo) & (f < hi)), n)
            out += band * np.exp(-6.91 * t / (rt60 * k))
        ir[:, ch] = out
    ir *= (1 - np.exp(-t / 0.015))[:, None]                 # diffuse build-up
    for k, (dt, g) in enumerate([(0.011, 0.5), (0.019, 0.38), (0.027, 0.3), (0.041, 0.22)]):
        i = int(dt * SR)
        ir[i, k % 2] += g * 3.0                             # a few early reflections
    ir = np.concatenate([np.zeros((int(pre * SR), 2)), ir])
    return ir / np.sqrt((ir ** 2).sum(axis=0).mean())


def convolve(x, ir):
    return np.stack([signal.fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], axis=1)


def highpass(x, hz, order=2):
    sos = signal.butter(order, hz, "highpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x, axis=0)


def echo(x, delay, fb=0.42, taps=6):
    """Ping-pong echo with progressively darker repeats."""
    y = x.copy()
    d = int(delay * SR)
    sos = signal.butter(1, 2500, "lowpass", fs=SR, output="sos")
    rep = x.copy()
    for k in range(1, taps + 1):
        rep = signal.sosfilt(sos, rep, axis=0) * fb
        shifted = np.zeros_like(x)
        shifted[k * d:] = rep[: len(x) - k * d]
        if k % 2:
            shifted = shifted[:, ::-1]
        y += shifted
    return y


def window_env(n, t0, t1, ramp=0.6):
    t = np.arange(n) / SR
    up = np.clip((t - (t0 - ramp)) / ramp, 0, 1)
    dn = np.clip(((t1 + ramp) - t) / ramp, 0, 1)
    return np.minimum(up, dn)


def limit(x, ceiling=CEILING, release=0.12, stats=None):
    """Look-ahead peak limiter.  stats (dict, optional) receives the pre-limit peak and how much /
    how long it reduced the gain."""
    peak = np.max(np.abs(x), axis=1)
    gain = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    look = int(0.006 * SR)
    gain = ndimage.minimum_filter1d(gain, 2 * look + 1)
    a = np.exp(-1 / (release * SR))
    zi = signal.lfilter_zi([1 - a], [1, -a]) * gain[0]      # start settled (no fade-in at t=0)
    smooth, _ = signal.lfilter([1 - a], [1, -a], gain, zi=zi)
    gain = np.minimum(gain, smooth)
    if stats is not None:
        gr = -20 * np.log10(np.maximum(gain, 1e-9))
        busy = np.nonzero(gr > 1.0)[0]
        stats.update(pre_peak=float(peak.max()), max_gr_db=float(gr.max()),
                     s_over_1db=len(busy) / SR, s_over_0_1db=float((gr > 0.1).sum()) / SR,
                     where=(round(busy[0] / SR, 2), round(busy[-1] / SR, 2)) if len(busy) else None)
    return x * gain[:, None]


def render(timeline, out_path):
    """Compose, render and mix the score. Returns out_path."""
    import pyloudnorm as pyln

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n = int(round(float(timeline["duration"]) * SR))

    sc = score_mod.build(timeline)
    sc.perform()
    work = Path(tempfile.mkdtemp(prefix="music_", dir=out_path.parent))
    try:
        mids = sc.write_midis(work)
        wavs = fluidsynth_render(mids, work)
        stems = {}
        for bus, wp in wavs.items():
            x, sr = sf.read(wp, dtype="float32", always_2d=True)      # float32: a 10-min score has
            assert sr == SR, sr                                          # 8 stems of 29 M frames
            x = x[:n] if len(x) >= n else np.concatenate([x, np.zeros((n - len(x), 2), np.float32)])
            stems[bus] = x
        midi_dir = out_path.parent / "music_midi"
        midi_dir.mkdir(exist_ok=True)
        for mp in mids.values():
            shutil.copy(mp, midi_dir / Path(mp).name)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    hall = make_ir(2.1, seed=11)
    cave = make_ir(3.6, seed=23, pre=0.05, dark=1.8)
    bellies = [c for c in sc.cues if c.mood == "belly"]      # s11 + s12: one dark cave
    cave_env = (window_env(n, min(c.t0 for c in bellies), max(c.t1 for c in bellies))[:, None]
                if bellies else np.zeros((n, 1)))

    dry = np.zeros((n, 2))
    hall_in = np.zeros((n, 2))
    for bus, x in stems.items():
        g_db, send, hp = BUSES.get(bus, (0.0, 0.3, 40))
        x = highpass(x, hp) * 10 ** (g_db / 20)
        if bus == "echo":
            x = echo(x, delay=0.5)
        dry += x
        hall_in += x * send
        del x
    wet = convolve(hall_in, hall)
    del hall_in
    wet += convolve(dry * cave_env * 0.45, cave)
    dry += wet
    del wet
    mix = highpass(dry, 32, order=2)
    del dry

    # tiny de-click fade at the very start; the last chord rings to the end and closes with a
    # raised-cosine fade to silence over the final 0.7 s
    fi, fo = int(0.005 * SR), int(0.7 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix[-fo:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fo)))[:, None]

    meter = pyln.Meter(SR)
    lufs = meter.integrated_loudness(mix)
    mix *= 10 ** ((TARGET_LUFS - lufs) / 20)
    lim = {}
    mix = limit(mix, stats=lim)
    mix = np.nan_to_num(mix).astype(np.float32)
    assert len(mix) == n
    sf.write(out_path, mix, SR, subtype="PCM_24")
    print(f"  music: {n / SR:.3f}s, {meter.integrated_loudness(mix.astype(np.float64)):.1f} LUFS, "
          f"peak {np.abs(mix).max():.3f}, notes {len(sc.notes)}")
    lim_note = (f"limiter: pre-limit peak {lim['pre_peak']:.3f} (ceiling {CEILING}), max gain reduction "
                f"{lim['max_gr_db']:.1f} dB, {lim['s_over_1db']:.2f} s above 1 dB / {lim['s_over_0_1db']:.2f} s above "
                f"0.1 dB of reduction" + (f" (between {lim['where'][0]} and {lim['where'][1]} s)" if lim["where"] else ""))
    print(f"  {lim_note}")

    from audio import music_check
    music_check.report(sc, out_path, stems, timeline, notes=[lim_note])
    return out_path


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from engine.loader import load_timeline
    from engine.paths import BUILD

    render(load_timeline(), BUILD / "audio" / "music.wav")
