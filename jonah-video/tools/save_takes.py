"""Commit the approved narration takes: copy the raw TTS takes used by the last voice build into
voice/takes/<key>.flac (lossless) and delete takes the script no longer uses.

TTS takes are stochastic (Matcha samples noise; ZipVoice is retried until ASR agrees), so a fresh
machine would otherwise synthesise different takes from the same script. voice/tts.py reads
voice/takes/ before synthesising, so with these files `python3 build.py voice` reproduces the
approved narration anywhere. Run after `python3 build.py voice` + `check` look right.
Usage: python3 tools/save_takes.py
"""
import os
import sys
from pathlib import Path

if "--story" in sys.argv:                      # python3 tools/save_takes.py --story daniel
    os.environ["PB_STORY"] = sys.argv[sys.argv.index("--story") + 1]

import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.paths import BUILD, CACHE, TAKES  # noqa: E402



def main():
    listing = BUILD / "voice" / "takes.txt"
    if not listing.exists():
        raise SystemExit("run `python3 build.py voice` first")
    keys = [k for k in listing.read_text().split() if k]
    TAKES.mkdir(parents=True, exist_ok=True)
    added = 0
    for k in keys:
        out = TAKES / f"{k}.flac"
        if out.exists():
            continue
        x, sr = sf.read(CACHE / "tts" / f"{k}.wav", dtype="float32")
        sf.write(out, x, sr, subtype="PCM_16")   # the cache WAVs are 16-bit: bit-exact
        added += 1
    stale = [p for p in TAKES.glob("*.flac") if p.stem not in set(keys)]
    for p in stale:
        p.unlink()
    size = sum(p.stat().st_size for p in TAKES.glob("*.flac")) / 1e6
    print(f"{len(keys)} takes ({added} new, {len(stale)} removed), {size:.1f} MB in {TAKES}")


if __name__ == "__main__":
    main()
