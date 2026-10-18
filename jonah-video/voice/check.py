"""Verify the narration: transcribe every clip with an offline ASR model and compare to the script.

Character error rate is computed after mapping known homophones (尼尼威/尼尼微 ...),
since the recogniser cannot know biblical names. Polyphonic readings must be
checked against the lexicons separately (see story.py notes).
Usage: python3 voice/check.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine.loader import load_timeline  # noqa: E402
from engine.paths import BUILD, MODELS  # noqa: E402

HOMOPHONES = {"威": "微", "维": "微", "师": "施", "实": "施", "哪": "拿", "纳": "拿", "地": "帝", "他": "它",
              "颗": "棵", "哭": "枯", "坐": "座", "莱": "来", "进": "禁", "亡": "王"}


def norm(s):
    s = re.sub(r"[^一-鿿0-9]", "", s)
    return s.replace("40", "四十").replace("12万", "十二万")


def cer(ref, hyp):
    ref, hyp = norm(ref), norm(hyp)
    hyp = "".join(HOMOPHONES.get(c, c) if c not in ref else c for c in hyp)
    dp = list(range(len(hyp) + 1))
    for i in range(1, len(ref) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(hyp) + 1):
            cur = dp[j]
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (ref[i - 1] != hyp[j - 1]))
            prev = cur
    return dp[-1] / max(1, len(ref))


def main():
    import sherpa_onnx as so

    d = MODELS / "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17"
    if not d.exists():
        raise SystemExit(f"ASR model missing: {d}")
    rec = so.OfflineRecognizer.from_sense_voice(model=str(d / "model.int8.onnx"), tokens=str(d / "tokens.txt"),
                                                language="zh", use_itn=True, num_threads=4)
    tl = load_timeline()
    worst = 0.0
    total = []
    for s in tl["scenes"]:
        for ln in s["lines"]:
            x, sr = sf.read(BUILD / ln["wav"], dtype="float32")
            pad = np.zeros(int(0.3 * sr), np.float32)   # the recogniser is unreliable on a word at sample 0
            x = np.concatenate([pad, x, pad])
            st = rec.create_stream()
            st.accept_waveform(sr, x)
            rec.decode_stream(st)
            hyp = st.result.text
            e = cer(ln["text"], hyp)
            total.append(e)
            worst = max(worst, e)
            flag = "  <-- check" if e > 0.15 else ""
            print(f"{s['id']:11s} {ln['speaker']} cer={e:.2f} {ln['text']} | {hyp}{flag}")
    print(f"mean CER {np.mean(total):.3f}, worst {worst:.2f}, lines {len(total)}")


if __name__ == "__main__":
    main()
