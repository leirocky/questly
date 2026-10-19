"""Build the Jonah picture-book video.

  python3 build.py all                 # voice -> music -> video -> mix -> assemble
  python3 build.py voice               # TTS clips + build/timeline.json + voice.wav
  python3 build.py check               # ASR round-trip of every narration clip
  python3 build.py music               # audio/music.py -> build/audio/music.wav
  python3 build.py video [--scenes s04_storm,s05_lots] [--jobs 3] [--force]
  python3 build.py mix                 # voice + music + sfx -> build/audio/mix.wav
  python3 build.py assemble            # -> output/jonah_story.mp4
  add --story daniel to build stories/daniel/ instead (-> build/daniel/, output/daniel_story.mp4)
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["all", "voice", "check", "music", "video", "mix", "assemble"])
    ap.add_argument("--scenes", default=None)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--story", default=None, help="story project: jonah (default) or stories/<name>/")
    a = ap.parse_args()
    if a.story:
        os.environ["PB_STORY"] = a.story       # read by engine.paths, imported below
    t0 = time.time()
    stages = ["voice", "music", "video", "mix", "assemble"] if a.stage == "all" else [a.stage]
    for st in stages:
        print(f"== {st}")
        if st == "voice":
            from voice import tts
            tts.build()
        elif st == "check":
            from voice import check
            check.main()
        elif st == "music":
            from audio import music
            from engine.loader import load_timeline
            from engine.paths import BUILD
            music.render(load_timeline(), BUILD / "audio" / "music.wav")
        elif st == "video":
            from engine import render
            render.render_all(a.scenes.split(",") if a.scenes else None, jobs=a.jobs, force=a.force)
        elif st == "mix":
            from audio import mix
            mix.mix()
        elif st == "assemble":
            from engine import assemble
            assemble.assemble()
    print(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
