"""Are the names heard right in the finished mix?  The last gate after voice, music and mix.

tools/name_check.py hears the clean voice lines; but music can mask a weak initial even 15-24 dB under the voice
(撒该 came back 撒呆 in the mix while the clean voice was right).  This cuts every line with a NO_BREAK name out of
build/<story>/audio/mix.wav (else voice.wav) with several paddings and asks the recogniser each time; a line fails
when its name is misheard (toneless pinyin, voice/tts.py _misheard_name) at any padding.

    PB_STORY=zacchaeus .venv/bin/python tools/mix_name_check.py [--stem voice|mix]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json  # noqa: E402

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from scipy.signal import resample_poly  # noqa: E402

import voice.tts as T  # noqa: E402

PADS = (0.0, 0.15, 0.3, 0.5, 0.8, 1.2)    # seconds of real mix kept around the line


def main():
    stem = sys.argv[sys.argv.index("--stem") + 1] if "--stem" in sys.argv else "mix"
    path = T.BUILD / "audio" / f"{stem}.wav"
    x, sr = sf.read(path, dtype="float32", always_2d=True)
    x = x.mean(1)
    if sr != 16000:
        x = resample_poly(x, 16000, sr).astype(np.float32)
        sr = 16000
    tl = json.load(open(T.BUILD / "timeline.json"))
    bad = 0
    for s in tl["scenes"]:
        for i, ln in enumerate(s["lines"]):
            if not any(w in T._norm(ln["text"]) for w in T.NO_BREAK):
                continue
            a, b = s["start"] + ln["start"], s["start"] + ln["end"]
            miss = []
            for p in PADS:
                seg = x[max(0, int((a - p) * sr)):int((b + p) * sr)]
                seg = np.concatenate([np.zeros(4800, np.float32), seg, np.zeros(4800, np.float32)])
                h = T.asr(seg, sr)[0]
                if T._misheard_name(ln["text"], h):
                    miss.append(f"{p}:{h[:16]}")
            if miss:
                bad += 1
                print(f"  {s['id']} L{i} at {a:.2f}s ({len(miss)}/{len(PADS)}): " + " | ".join(miss))
    print(f"{stem}: {bad} line(s) with a misheard name")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
