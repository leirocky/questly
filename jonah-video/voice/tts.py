"""Offline Chinese text-to-speech for every story line, plus the master timeline.

Engines (sherpa-onnx, models downloaded by setup.sh into .cache/models):
  * matcha-icefall-zh-baker + vocos vocoder  -> narrator (clear female voice)
  * kokoro-multi-lang-v1_1 (Kokoro 82M v1.1-zh) -> God (deep male) and Jonah (male)

Outputs
  build/voice/lines/<scene>_<n>.wav   processed 48 kHz mono clip per line
  build/audio/voice.wav               all lines placed on the global timeline
  build/timeline.json                 scene and line timing (seconds, frame aligned)
"""
import hashlib
import json
import re
import sys
from math import gcd

import numpy as np
import soundfile as sf
from scipy import signal

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import story  # noqa: E402
from engine.paths import BUILD, CACHE, FPS, MODELS, SR, ensure_dirs  # noqa: E402

VOICES = {
    "N": {"engine": "matcha", "sid": 0, "speed": 1.05, "fx": None, "gain_db": 0.0},
    "G": {"engine": "kokoro", "sid": 101, "speed": 1.0, "fx": "divine", "gain_db": 0.0},
    "J": {"engine": "kokoro", "sid": 95, "speed": 1.08, "fx": None, "gain_db": 0.0},
}
# Per-scene overrides of a speaker's effect (Jonah praying inside the fish).
SCENE_FX = {("s07_belly", "J"): "cave"}

TARGET_LUFS = -20.0  # per-clip loudness before the final mix

_engines = {}


def _engine(name):
    import sherpa_onnx as so

    if name in _engines:
        return _engines[name]
    if name == "matcha":
        d = MODELS / "matcha-icefall-zh-baker"
        cfg = so.OfflineTtsConfig(
            model=so.OfflineTtsModelConfig(
                matcha=so.OfflineTtsMatchaModelConfig(
                    acoustic_model=str(d / "model-steps-3.onnx"),
                    vocoder=str(MODELS / "vocos-22khz-univ.onnx"),
                    lexicon=str(d / "lexicon.txt"),
                    tokens=str(d / "tokens.txt"),
                    dict_dir=str(d / "dict"),
                ),
                num_threads=4,
            ),
            rule_fsts=f"{d}/phone.fst,{d}/date.fst,{d}/number.fst",
        )
    elif name == "kokoro":
        d = MODELS / "kokoro-multi-lang-v1_1"
        cfg = so.OfflineTtsConfig(
            model=so.OfflineTtsModelConfig(
                kokoro=so.OfflineTtsKokoroModelConfig(
                    model=str(d / "model.onnx"),
                    voices=str(d / "voices.bin"),
                    tokens=str(d / "tokens.txt"),
                    data_dir=str(d / "espeak-ng-data"),
                    dict_dir=str(d / "dict"),
                    lexicon=f"{d}/lexicon-us-en.txt,{d}/lexicon-zh.txt",
                ),
                num_threads=4,
            ),
            rule_fsts=f"{d}/phone-zh.fst,{d}/date-zh.fst,{d}/number-zh.fst",
        )
    else:
        raise ValueError(name)
    _engines[name] = so.OfflineTts(cfg)
    return _engines[name]


def tts_text(text, engine):
    """Normalise punctuation the front ends would otherwise read aloud."""
    t = re.sub(r"[“”‘’\"'《》「」]", "", text)
    t = t.replace("：", "，").replace("；", "，").replace("…", "。").replace("——", "，")
    if engine == "kokoro":
        t = t.replace("、", "，")
    return t


def synth_raw(text, voice):
    """Synthesize (cached) and return float32 mono at the engine's sample rate."""
    key = hashlib.sha1(json.dumps([text, voice["engine"], voice["sid"], voice["speed"]]).encode()).hexdigest()[:16]
    path = CACHE / "tts" / f"{key}.wav"
    if path.exists():
        x, sr = sf.read(path, dtype="float32")
        return x, sr
    path.parent.mkdir(parents=True, exist_ok=True)
    tts = _engine(voice["engine"])
    a = tts.generate(tts_text(text, voice["engine"]), sid=voice["sid"], speed=voice["speed"])
    x = np.asarray(a.samples, dtype=np.float32)
    sf.write(path, x, a.sample_rate)
    return x, a.sample_rate


def resample(x, sr_in, sr_out=SR):
    if sr_in == sr_out:
        return x
    g = gcd(sr_in, sr_out)
    return signal.resample_poly(x, sr_out // g, sr_in // g).astype(np.float32)


def trim(x, sr, thresh_db=-42, pad_s=0.04):
    """Trim leading/trailing silence using a 10 ms RMS envelope."""
    hop = int(sr * 0.01)
    n = len(x) // hop
    if n == 0:
        return x
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms / (rms.max() + 1e-12))
    idx = np.where(db > thresh_db)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] * hop - int(pad_s * sr))
    b = min(len(x), (idx[-1] + 1) * hop + int(pad_s * sr))
    y = x[a:b].copy()
    f = int(0.01 * sr)
    y[:f] *= np.linspace(0, 1, f)
    y[-f:] *= np.linspace(1, 0, f)
    return y


def _reverb_ir(sr, seconds, decay, lowpass_hz, seed, predelay_s=0.0):
    rng = np.random.default_rng(seed)
    n = int(sr * seconds)
    t = np.arange(n) / sr
    ir = rng.standard_normal(n) * np.exp(-t * decay)
    b, a = signal.butter(2, lowpass_hz / (sr / 2), "low")
    ir = signal.lfilter(b, a, ir)
    ir = np.concatenate([np.zeros(int(predelay_s * sr)), ir])
    return (ir / np.sqrt(np.sum(ir**2))).astype(np.float32)


def apply_fx(x, sr, fx):
    """Return float32 mono with a gentle effect; tail is appended, so clips get longer."""
    if fx is None:
        return x
    if fx == "divine":
        # Warm, softly echoing voice from heaven: low-shelf warmth + airy hall reverb.
        ir = _reverb_ir(sr, 2.2, 3.2, 5000, seed=7, predelay_s=0.035)
        wet = signal.fftconvolve(x, ir)[: len(x) + int(1.2 * sr)]
        dry = np.concatenate([x, np.zeros(len(wet) - len(x), np.float32)])
        b, a = signal.butter(2, 220 / (sr / 2), "low")
        warm = signal.lfilter(b, a, dry)
        return (dry + 0.35 * warm + 0.30 * wet).astype(np.float32)
    if fx == "cave":
        # Inside the fish: muffled, boomy, short dense reverb.
        b, a = signal.butter(4, 2600 / (sr / 2), "low")
        muff = signal.lfilter(b, a, x)
        ir = _reverb_ir(sr, 1.4, 4.5, 1800, seed=11, predelay_s=0.02)
        wet = signal.fftconvolve(muff, ir)[: len(x) + int(0.9 * sr)]
        dry = np.concatenate([muff, np.zeros(len(wet) - len(x), np.float32)])
        return (0.85 * dry + 0.45 * wet).astype(np.float32)
    raise ValueError(fx)


def loudness_normalize(x, sr, target=TARGET_LUFS):
    import pyloudnorm as pyln

    meter = pyln.Meter(sr)
    lufs = meter.integrated_loudness(x.astype(np.float64)) if len(x) > sr * 0.45 else -30.0
    if not np.isfinite(lufs):
        return x
    y = x * 10 ** ((target - lufs) / 20)
    peak = np.abs(y).max()
    if peak > 0.89:
        y *= 0.89 / peak
    return y.astype(np.float32)


def frames(t):
    """Round seconds to the nearest whole video frame."""
    return round(t * FPS) / FPS


def build():
    ensure_dirs()
    out_lines = BUILD / "voice" / "lines"
    out_lines.mkdir(parents=True, exist_ok=True)
    (BUILD / "audio").mkdir(parents=True, exist_ok=True)

    scenes = []
    t_scene = 0.0
    for i, sc in enumerate(story.SCENES):
        lead = sc.get("lead_in", story.LEAD_IN)
        tail = sc.get("tail", story.TAIL)
        cur = lead
        lines = []
        for j, ln in enumerate(sc["lines"]):
            spk, text = ln[0], ln[1]
            pause = ln[2] if len(ln) > 2 else story.LINE_GAP
            v = VOICES[spk]
            x, sr = synth_raw(text, v)
            x = resample(trim(x, sr), sr)
            speech_len = len(x) / SR
            fx = SCENE_FX.get((sc["id"], spk), v["fx"])
            x = loudness_normalize(apply_fx(x, SR, fx), SR, TARGET_LUFS + v["gain_db"])
            name = f"{sc['id']}_{j:02d}.wav"
            sf.write(out_lines / name, x, SR)
            start = frames(cur)
            lines.append({
                "speaker": spk, "text": text, "wav": f"voice/lines/{name}",
                "start": start, "end": round(start + speech_len, 3), "fx": fx,
            })
            cur = start + speech_len + pause
        dur = frames(lines[-1]["end"] + tail)
        scenes.append({"id": sc["id"], "mood": sc["mood"], "note": sc["note"],
                       "start": frames(t_scene), "duration": dur, "lines": lines})
        t_scene = frames(t_scene + dur - story.XFADE)

    total = frames(scenes[-1]["start"] + scenes[-1]["duration"])
    timeline = {"fps": FPS, "xfade": story.XFADE, "duration": total, "title": story.TITLE,
                "subtitle": story.SUBTITLE, "scenes": scenes}
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1))

    # Place every line on one mono voice track.
    track = np.zeros(int((total + 3) * SR), np.float32)
    for sc in scenes:
        for ln in sc["lines"]:
            x, _ = sf.read(BUILD / ln["wav"], dtype="float32")
            a = int(round((sc["start"] + ln["start"]) * SR))
            track[a:a + len(x)] += x
    track = track[: int(total * SR)]
    sf.write(BUILD / "audio" / "voice.wav", track, SR)

    for sc in scenes:
        print(f"{sc['id']:12s} start={sc['start']:7.2f}s dur={sc['duration']:6.2f}s lines={len(sc['lines'])}")
    print(f"TOTAL {total:.2f}s")
    return timeline


if __name__ == "__main__":
    build()
