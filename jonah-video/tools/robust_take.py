"""Retake one line (delete its .cache/tts wav and takes/ flac first, or this overwrites the cache). Generate takes of one line until the raw clip passes every check AND the processed line (as the voice stage makes
it) is heard with every name right, by toneless pinyin; save it to the line's cache path.
PB_STORY=<story> .venv/bin/python tools/robust_take.py <story> <speaker> 'text' [--exact] [--context] [--speed S]"""
import sys; sys.path.insert(0, '.')
import numpy as np, soundfile as sf, voice.tts as T
from scipy import signal
spk, text = sys.argv[2], sys.argv[3]; v = T.VOICES[spk]
exact = '--exact' in sys.argv   # also: the processed line's toneless pinyin must equal the script's (星 heard as 心)
speed = float(sys.argv[sys.argv.index('--speed') + 1]) if '--speed' in sys.argv else None   # e.g. 0.85: slow a rushed line
context = '--context' in sys.argv   # also: names heard right with the neighbouring finished lines around it (撒该 can
                                    # pass alone and turn into 撒呆 between its neighbours)
from pypinyin import lazy_pinyin
path = T._cache_path(text, v, T._relevant_entries(text, T._zipvoice_content().splitlines()))
tts = T._engine("zipvoice"); px, psr, pt = T._prompt(v)
def processed(x, sr):
    y = T.resample(T.trim(x, sr), sr)
    y = signal.sosfiltfilt(T._DC_SOS, T.soften_onsets(y, T.SR)).astype(np.float32)
    if v.get("stretch_pauses"):
        y = T.stretch_pauses(y, T.SR, text)
    return T.loudness_normalize(T.apply_fx(y, T.SR, v["fx"]), T.SR, T.TARGET_LUFS + v["gain_db"])
def neighbours():
    """(text, wav, gap before) of the finished lines before and after this one in the story's timeline."""
    import json
    tl = json.load(open(T.BUILD / "timeline.json"))
    flat = [(s["start"] + l["start"], s["start"] + l["end"], l) for s in tl["scenes"] for l in s["lines"]]
    i = next(k for k, f in enumerate(flat) if f[2]["text"] == text)
    def load(k):
        a, b, l = flat[k]
        x, _ = sf.read(T.BUILD / l["wav"], dtype="float32")
        return l["text"], x
    prev = load(i - 1) if i > 0 else None
    nxt = load(i + 1) if i + 1 < len(flat) else None
    g0 = flat[i][0] - flat[i - 1][1] if prev else 0
    g1 = flat[i + 1][0] - flat[i][1] if nxt else 0
    return prev, nxt, min(g0, 1.0), min(g1, 1.0)
NB = neighbours() if context else None
def in_context(y):
    """What the recogniser hears of this line when it sits between its neighbours: only the tokens timed inside
    this line's span count, so a weak name in a neighbour does not fail this take."""
    prev, nxt, g0, g1 = NB
    pad = np.zeros(int(0.3 * T.SR), np.float32)
    parts = [pad]
    if prev:
        parts += [prev[1], np.zeros(int(g0 * T.SR), np.float32)]
    t0 = sum(len(p) for p in parts) / T.SR
    parts.append(y)
    t1 = t0 + len(y) / T.SR
    if nxt:
        parts += [np.zeros(int(g1 * T.SR), np.float32), nxt[1]]
    parts.append(pad)
    _, toks, ts = T.asr(np.concatenate(parts), T.SR)
    return "".join(tk for tk, t in zip(toks, ts) if t0 - 0.1 <= t <= t1 + 0.05)
def heard(y, sr):
    yp = np.concatenate([np.zeros(int(.3 * sr), np.float32), y, np.zeros(int(.3 * sr), np.float32)])
    return T.asr(yp, sr)[0]
base = speed or v["speed"]
for n, (spd, steps) in enumerate([(base, 8), (base, 12), (base - .03, 8), (base + .03, 12),
                                  (base, 16), (base, 10)] * 3):
    a = tts.generate(T.tts_text(text, "zipvoice"), pt, px.tolist(), psr, spd, steps)
    x = np.asarray(a.samples, np.float32); sr = a.sample_rate
    bad, err = T._take_score(text, x, sr)
    h2 = heard(processed(x, sr), T.SR)
    ok = not bad and not T._misheard_name(text, h2) and (not exact or lazy_pinyin(T._norm(h2)) == lazy_pinyin(T._norm(text)))
    if ok and context:
        hc = in_context(processed(x, sr))
        ok = not T._misheard_name(text, hc)
        h2 += ' | in context: ' + hc
    print(n, spd, steps, round(err, 3), "BAD" if bad else "", h2, "OK" if ok else "", flush=True)
    if ok:
        sf.write(path, x, sr); print("saved", path); break
