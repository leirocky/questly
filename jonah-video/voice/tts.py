"""Offline Chinese text-to-speech for every story utterance, plus the master timeline.

Engines (sherpa-onnx, models in .cache/models — see README):
  * matcha-icefall-zh-baker + vocos-22khz   -> narrator (clear female voice)
  * ZipVoice (distill, zh-en, Emilia)       -> God, Jonah, captain, sailors, king. Zero-shot: each male
    voice takes its timbre from a short Kokoro v1.1-zh prompt clip, while ZipVoice (trained on natural
    conversational speech) supplies the prosody and pauses.
  Both front ends get pronunciation lexicons generated from the script (voice/lexicons.py): readings in
  context plus tone sandhi, so polyphones follow their words.
  * Kokoro v1.1-zh                          -> optional direct engine for the male voices (MALE_ENGINE).

Each utterance is synthesised whole, checked by ASR (retried with other settings when it misreads),
and cut into subtitle chunks at punctuation, timed from the recogniser's per-character timestamps.

Outputs
  build/voice/lines/<scene>_<n>.wav   processed 48 kHz mono clip per utterance
  build/audio/voice.wav               all lines placed on the global timeline
  build/timeline.json                 scene, line and subtitle-chunk timing (seconds, frame aligned)
"""
import hashlib
import json
import re
import sys
from math import gcd

import numpy as np
import soundfile as sf
from scipy import ndimage, signal

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import story  # noqa: E402
from engine.paths import BUILD, CACHE, FPS, MODELS, SR, ensure_dirs  # noqa: E402

MALE_ENGINE = "zipvoice"   # "zipvoice" or "kokoro" for the male speakers

VOICES = {
    "N": {"engine": "matcha", "sid": 0, "speed": 0.85, "fx": None, "gain_db": 0.0},
    "G": {"engine": MALE_ENGINE, "sid": 101, "speed": 0.9, "fx": "divine", "gain_db": 0.0},
    "J": {"engine": MALE_ENGINE, "sid": 91, "speed": 0.95, "fx": None, "gain_db": 0.0},
    "C": {"engine": MALE_ENGINE, "sid": 88, "speed": 0.95, "fx": None, "gain_db": 0.0},
    "S": {"engine": MALE_ENGINE, "sid": 95, "speed": 1.0, "fx": None, "gain_db": 0.0},
    "K": {"engine": MALE_ENGINE, "sid": 100, "speed": 0.9, "fx": None, "gain_db": 0.0},
}
# Kokoro prompt sentences that give each ZipVoice male voice its timbre.
PROMPTS = {
    101: "我是创造天地的上帝，我爱这世上所有的人，也爱一切的生命。",
    91: "我是约拿，我是一个先知，我的家在以色列的一个小村庄里。",
    88: "我是这条船的船长，我在海上航行了很多很多年。",
    95: "我们是船上的水手，每天都在海上拉绳子，划船，搬货物。",
    100: "我是尼尼微的国王，我住在一座很大很大的城里。",
}
# Per-scene overrides of a speaker's effect (Jonah praying inside the fish).
SCENE_FX = {("s11_belly", "J"): "cave", ("s12_deep", "J"): "cave"}
CER_RETRY = 0.10   # re-synthesise a ZipVoice utterance when ASR disagrees more than this
NARRATOR_CER_OK = 0.06

TARGET_LUFS = -20.0  # per-clip loudness before the final mix
_DC_SOS = signal.butter(2, 40, "highpass", fs=SR, output="sos")

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
                    lexicon=str(_narrator_lexicon()[0]),
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
    elif name == "zipvoice":
        d = MODELS / "sherpa-onnx-zipvoice-distill-zh-en-emilia"
        lex = _zipvoice_lexicon()
        cfg = so.OfflineTtsConfig(
            model=so.OfflineTtsModelConfig(
                zipvoice=so.OfflineTtsZipvoiceModelConfig(
                    tokens=str(d / "tokens.txt"), encoder=str(d / "text_encoder.onnx"),
                    decoder=str(d / "fm_decoder.onnx"), vocoder=str(MODELS / "vocos_24khz.onnx"),
                    data_dir=str(d / "espeak-ng-data"), lexicon=str(lex), guidance_scale=3.0,
                ),
                num_threads=4,
            ),
        )
    else:
        raise ValueError(name)
    _engines[name] = so.OfflineTts(cfg)
    return _engines[name]


def _engine_texts():
    from voice import lexicons as LX

    n, z = LX.texts_by_engine(story.SCENES, [k for k, v in VOICES.items() if v["engine"] == "matcha"])
    return n, z + list(PROMPTS.values())


def _narrator_lexicon():
    """(path, version) of the narrator lexicon: matcha's own merged with script-specific fixes."""
    from voice import lexicons as LX

    if "narrator" not in _lex:
        _lex["narrator"] = LX.narrator_lexicon(_engine_texts()[0])
    return _lex["narrator"]


def _zipvoice_content():
    from voice import lexicons as LX

    if "zv" not in _lex:
        _lex["zv"] = LX.zipvoice_content(_engine_texts()[1])
    return _lex["zv"]


def _zipvoice_lexicon():
    content = _zipvoice_content()
    tokens = MODELS / "sherpa-onnx-zipvoice-distill-zh-en-emilia" / "tokens.txt"
    valid = {line.split("\t")[0] for line in open(tokens, encoding="utf-8")}
    bad = [ln for ln in content.splitlines() if any(t not in valid for t in ln.split()[1:])]
    if bad:
        raise ValueError(f"ZipVoice lexicon has tokens the model does not know: {bad[:5]}")
    path = CACHE / "zipvoice_lexicon.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


_lex = {}
_asr = None


def asr(x, sr):
    """Recognise speech; returns (text, tokens, token start times in s)."""
    global _asr
    import sherpa_onnx as so

    if _asr is None:
        d = MODELS / "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17"
        _asr = so.OfflineRecognizer.from_sense_voice(model=str(d / "model.int8.onnx"), tokens=str(d / "tokens.txt"),
                                                     language="zh", use_itn=False, num_threads=4)
    st = _asr.create_stream()
    st.accept_waveform(sr, np.asarray(x, np.float32))
    _asr.decode_stream(st)
    r = st.result
    return r.text, list(r.tokens), list(r.timestamps)


def tts_text(text, engine):
    """Normalise punctuation the front ends would otherwise read aloud."""
    t = re.sub(r"[“”‘’\"'《》「」]", "", text)
    t = t.replace("：", "，").replace("；", "，").replace("…", "。").replace("——", "，")
    if engine in ("kokoro", "zipvoice"):
        t = t.replace("、", "，")
    return t


def _prompt(sid):
    """Kokoro clip that gives a ZipVoice male voice its timbre (DC-free, cached)."""
    text = PROMPTS[sid]
    x, sr = synth_raw(text, {"engine": "kokoro", "sid": sid, "speed": 0.9})
    x = signal.sosfiltfilt(signal.butter(2, 40, "highpass", fs=sr, output="sos"), soften_onsets(x, sr))
    return np.asarray(x, np.float32), sr, text


def _cache_path(text, voice, extra=""):
    key = hashlib.sha1(json.dumps([text, voice["engine"], voice["sid"], voice["speed"], extra]).encode()).hexdigest()[:16]
    return CACHE / "tts" / f"{key}.wav"


def _relevant_entries(text, lines):
    """Hash of the lexicon entries that can apply to this text, so editing one line of the script
    only re-synthesises the lines whose pronunciation could change."""
    rel = sorted(ln for ln in lines if ln.split(" ", 1)[0] in text)
    return hashlib.sha1("\n".join(rel).encode()).hexdigest()[:12]


def synth_raw(text, voice):
    """Synthesize (cached) and return float32 mono at the engine's sample rate."""
    extra = ""
    if voice["engine"] == "zipvoice":
        extra = _relevant_entries(text, _zipvoice_content().splitlines())
    elif voice["engine"] == "matcha":
        from voice import lexicons as LX
        extra = _relevant_entries(text, [f"{w} {' '.join(s)}" for w, s in
                                         LX.narrator_additions(_engine_texts()[0]).items()])
    path = _cache_path(text, voice, extra)
    if path.exists():
        x, sr = sf.read(path, dtype="float32")
        return x, sr
    path.parent.mkdir(parents=True, exist_ok=True)
    tts = _engine(voice["engine"])
    if voice["engine"] == "zipvoice":
        px, psr, ptext = _prompt(voice["sid"])
        best = None
        # Flow matching can occasionally slur a word: verify with ASR and try other settings.
        for spd, steps in ((voice["speed"], 8), (voice["speed"], 12), (voice["speed"] - 0.04, 8),
                           (voice["speed"] + 0.04, 12)):
            a = tts.generate(tts_text(text, "zipvoice"), ptext, px.tolist(), psr, spd, steps)
            x = np.asarray(a.samples, dtype=np.float32)
            err = _cer(text, asr(x, a.sample_rate)[0])
            if best is None or err < best[0]:
                best = (err, x, a.sample_rate)
            if err <= CER_RETRY:
                break
        err, x, sr = best
        if err > CER_RETRY:
            print(f"  WARNING ASR mismatch {err:.2f} for: {text}")
        sf.write(path, x, sr)
        return x, sr
    if voice["engine"] == "matcha":
        # Matcha samples noise, so takes differ: keep the first take ASR agrees with (or the best of 5).
        best = None
        for _ in range(5):
            a = tts.generate(tts_text(text, "matcha"), sid=voice["sid"], speed=voice["speed"])
            x = np.asarray(a.samples, dtype=np.float32)
            err = _cer(text, asr(x, a.sample_rate)[0])
            if best is None or err < best[0]:
                best = (err, x, a.sample_rate)
            if err <= NARRATOR_CER_OK:
                break
        err, x, sr = best
        if err > NARRATOR_CER_OK:
            print(f"  WARNING ASR mismatch {err:.2f} for: {text}")
        sf.write(path, x, sr)
        return x, sr
    a = tts.generate(tts_text(text, voice["engine"]), sid=voice["sid"], speed=voice["speed"])
    x = np.asarray(a.samples, dtype=np.float32)
    sf.write(path, x, a.sample_rate)
    return x, a.sample_rate


_HOMOPHONES = {"威": "微", "师": "施", "实": "施", "哪": "拿", "纳": "拿", "地": "帝", "他": "它", "她": "它",
               "颗": "棵", "莱": "来", "进": "禁", "亡": "王"}


def _norm(s):
    return re.sub(r"[^\u4e00-\u9fff]", "", s)


def _cer(ref, hyp):
    ref, hyp = _norm(ref), _norm(hyp)
    hyp = "".join(c if c in ref else _HOMOPHONES.get(c, c) for c in hyp)
    dp = list(range(len(hyp) + 1))
    for i in range(1, len(ref) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(hyp) + 1):
            cur = dp[j]
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (ref[i - 1] != hyp[j - 1]))
            prev = cur
    return dp[-1] / max(1, len(ref))


SUB_MAX = 16   # max Chinese characters per subtitle chunk


def subtitle_chunks(text):
    """Split an utterance at punctuation into readable subtitle chunks (<= SUB_MAX characters)."""
    clauses = re.findall(r"[^，。！？；：、]+[，。！？；：、]*", text)
    chunks, cur = [], ""
    for c in clauses:
        n_cur, n_c = len(_norm(cur)), len(_norm(c))
        if cur and (n_cur + n_c > SUB_MAX or (cur[-1] in "。！？" and n_cur >= 6)):
            chunks.append(cur)
            cur = ""
        cur += c
    if cur:
        chunks.append(cur)
    return chunks


def chunk_times(text, chunks, x, sr, dur):
    """Start/end of each chunk (seconds within the clip) from ASR per-character timestamps."""
    import difflib

    ref = _norm(text)
    _, toks, ts = asr(x, sr)
    hyp = "".join(toks)
    # map reference char index -> time via aligned tokens, interpolate the rest
    anchors = {}
    tok_starts = []
    pos = 0
    for t, tm in zip(toks, ts):
        tok_starts.append((pos, tm))
        pos += len(t)
    hyp_time = {}
    for p, tm in tok_starts:
        hyp_time[p] = tm
    sm = difflib.SequenceMatcher(None, hyp, ref, autojunk=False)
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            if a + k in hyp_time:
                anchors[b + k] = hyp_time[a + k]
    if len(anchors) < 2:
        anchors = {0: 0.0, len(ref): dur}
    xs = sorted(anchors)
    def t_of(i):
        return float(np.interp(i, xs, [anchors[k] for k in xs]))
    out, idx = [], 0
    starts = []
    for c in chunks:
        starts.append(max(0.0, t_of(idx) - 0.12))
        idx += len(_norm(c))
    for k, c in enumerate(chunks):
        end = starts[k + 1] - 0.04 if k + 1 < len(chunks) else dur
        out.append({"text": c, "start": round(starts[k], 3), "end": round(max(end, starts[k] + 0.4), 3)})
    return out


def soften_onsets(x, sr, ramp_s=0.005, silent=0.0015, jump=0.003):
    """Fade in over ``ramp_s`` wherever the signal jumps straight out of silence.

    Kokoro starts each phrase with a one-sample step to a DC offset; even after the high-pass
    that step leaves a sub-millisecond broadband tick just before the voice.
    """
    y = x.copy()
    r, w = int(ramp_s * sr), int(0.005 * sr)
    last = -10 ** 9
    for c in np.where(np.abs(np.diff(x)) > jump)[0]:
        if c - last < 2 * r:
            continue
        pre = x[max(0, c - w):c]
        if len(pre) == 0 or np.sqrt(np.mean(pre ** 2)) >= silent:
            continue
        a, b = c + 1, min(len(y), c + 1 + r)
        y[a:b] *= 0.5 - 0.5 * np.cos(np.pi * np.arange(1, b - a + 1) / r)
        last = c
    return y.astype(np.float32)


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


def _rbj(kind, sr, f0, gain_db, q=0.7071):
    """RBJ audio-EQ-cookbook biquad coefficients (b, a) for a low shelf (S=1) or peaking filter."""
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / sr
    cw, sw = np.cos(w), np.sin(w)
    if kind == "lowshelf":
        alpha = sw / 2 * np.sqrt(2)
        k = 2 * np.sqrt(A) * alpha
        b = [A * ((A + 1) - (A - 1) * cw + k), 2 * A * ((A - 1) - (A + 1) * cw), A * ((A + 1) - (A - 1) * cw - k)]
        a = [(A + 1) + (A - 1) * cw + k, -2 * ((A - 1) + (A + 1) * cw), (A + 1) + (A - 1) * cw - k]
    elif kind == "peak":
        alpha = sw / (2 * q)
        b = [1 + alpha * A, -2 * cw, 1 - alpha * A]
        a = [1 + alpha / A, -2 * cw, 1 - alpha / A]
    else:
        raise ValueError(kind)
    return np.array(b) / a[0], np.array(a) / a[0]


def _biquad(y, ba):
    return signal.lfilter(ba[0], ba[1], y)


def apply_fx(x, sr, fx):
    """Return float32 mono with a gentle effect; tail is appended, so clips get longer."""
    if fx is None:
        return x
    if fx == "divine":
        # Softly echoing voice from heaven: airy hall reverb, with EQ that moves the deep
        # voice's energy out of the bass so it stays clear on phone/tablet speakers.
        ir = _reverb_ir(sr, 1.8, 4.2, 5000, seed=7, predelay_s=0.035)
        wet = signal.fftconvolve(x, ir)[: len(x) + int(1.0 * sr)]
        dry = np.concatenate([x, np.zeros(len(wet) - len(x), np.float32)])
        y = dry + 0.17 * wet
        y = signal.sosfilt(signal.butter(2, 90, "highpass", fs=sr, output="sos"), y)
        y = _biquad(y, _rbj("lowshelf", sr, 200, -6.0))
        y = _biquad(y, _rbj("peak", sr, 2500, 2.0, q=1.0))
        return y.astype(np.float32)
    if fx == "cave":
        # Inside the fish: muffled, boomy, short dense reverb.
        b, a = signal.butter(2, 4200 / (sr / 2), "low")
        muff = signal.lfilter(b, a, x)
        ir = _reverb_ir(sr, 1.4, 4.5, 1800, seed=11, predelay_s=0.02)
        wet = signal.fftconvolve(muff, ir)[: len(x) + int(0.9 * sr)]
        dry = np.concatenate([muff, np.zeros(len(wet) - len(x), np.float32)])
        return (0.9 * dry + 0.22 * wet).astype(np.float32)
    raise ValueError(fx)


def loudness_normalize(x, sr, target=TARGET_LUFS):
    import pyloudnorm as pyln

    meter = pyln.Meter(sr)
    lufs = meter.integrated_loudness(x.astype(np.float64)) if len(x) > sr * 0.45 else -30.0
    if not np.isfinite(lufs):
        return x
    y = x * 10 ** ((target - lufs) / 20)
    # 5 ms look-ahead peak limiter (instead of scaling the whole clip down for one peak),
    # so every clip actually reaches its loudness target.
    ceiling, look = 0.89, int(0.005 * sr)
    g = np.minimum(1.0, ceiling / np.maximum(np.abs(y), 1e-9))
    g = ndimage.minimum_filter1d(g, 2 * look + 1)
    g = ndimage.uniform_filter1d(g, look)
    return np.clip(y * g, -ceiling, ceiling).astype(np.float32)


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
            nxt = sc["lines"][j + 1][0] if j + 1 < len(sc["lines"]) else spk
            pause = ln[2] if len(ln) > 2 else (story.SPEAKER_GAP if nxt != spk else story.LINE_GAP)
            v = VOICES[spk]
            x, sr = synth_raw(text, v)
            x = resample(trim(x, sr), sr)
            if v["engine"] in ("kokoro", "zipvoice"):
                # Remove any DC offset / infrasonic pulse and onset ticks, zero-phase.
                x = signal.sosfiltfilt(_DC_SOS, soften_onsets(x, SR)).astype(np.float32)
            speech_len = len(x) / SR
            chunks = chunk_times(text, subtitle_chunks(text), x, SR, speech_len)
            fx = SCENE_FX.get((sc["id"], spk), v["fx"])
            x = loudness_normalize(apply_fx(x, SR, fx), SR, TARGET_LUFS + v["gain_db"])
            name = f"{sc['id']}_{j:02d}.wav"
            sf.write(out_lines / name, x, SR)
            start = frames(cur)
            lines.append({
                "speaker": spk, "text": text, "wav": f"voice/lines/{name}",
                "start": start, "end": round(start + speech_len, 3), "fx": fx,
                "chunks": [{**c, "start": round(start + c["start"], 3), "end": round(start + c["end"], 3)}
                           for c in chunks],
            })
            cur = start + speech_len + pause
        dur = frames(lines[-1]["end"] + tail)
        scenes.append({"id": sc["id"], "mood": sc["mood"], "note": sc["note"],
                       "transition": sc.get("transition", "fade"),
                       "start": frames(t_scene), "duration": dur, "lines": lines})
        t_scene = frames(t_scene + dur - story.XFADE)
        print(f"  {sc['id']:14s} {dur:6.2f}s", flush=True)

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
