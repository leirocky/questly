"""Retake one line (delete its .cache/tts wav and takes/ flac first, or this overwrites the cache). Generate takes of one line until the raw clip passes every check AND the processed line (as the voice stage makes
it) is heard with every name right, by toneless pinyin; save it to the line's cache path.
PB_STORY=<story> .venv/bin/python tools/robust_take.py <story> <speaker> 'text'"""
import sys; sys.path.insert(0, '.')
import numpy as np, soundfile as sf, voice.tts as T
from scipy import signal
spk, text = sys.argv[2], sys.argv[3]; v = T.VOICES[spk]
path = T._cache_path(text, v, T._relevant_entries(text, T._zipvoice_content().splitlines()))
tts = T._engine("zipvoice"); px, psr, pt = T._prompt(v)
def processed(x, sr):
    y = T.resample(T.trim(x, sr), sr)
    y = signal.sosfiltfilt(T._DC_SOS, T.soften_onsets(y, T.SR)).astype(np.float32)
    if v.get("stretch_pauses"):
        y = T.stretch_pauses(y, T.SR, text)
    return T.loudness_normalize(T.apply_fx(y, T.SR, v["fx"]), T.SR, T.TARGET_LUFS + v["gain_db"])
def heard(y, sr):
    yp = np.concatenate([np.zeros(int(.3 * sr), np.float32), y, np.zeros(int(.3 * sr), np.float32)])
    return T.asr(yp, sr)[0]
for n, (spd, steps) in enumerate([(v["speed"], 8), (v["speed"], 12), (v["speed"] - .03, 8), (v["speed"] + .03, 12),
                                  (v["speed"], 16), (v["speed"], 10)] * 3):
    a = tts.generate(T.tts_text(text, "zipvoice"), pt, px.tolist(), psr, spd, steps)
    x = np.asarray(a.samples, np.float32); sr = a.sample_rate
    bad, err = T._take_score(text, x, sr)
    h2 = heard(processed(x, sr), T.SR)
    ok = not bad and not T._misheard_name(text, h2)
    print(n, spd, steps, round(err, 3), "BAD" if bad else "", h2, "OK" if ok else "", flush=True)
    if ok:
        sf.write(path, x, sr); print("saved", path); break
