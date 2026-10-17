# 约拿的故事 — picture-book video (work in progress)

A ~2-minute Chinese picture-book style video of the Book of Jonah with narration,
background music and sound effects. Everything for it lives in this folder and is
independent of the Questly app.

## Status

Done:
- `story.py` — narration script (Jonah 1–4, 13 scenes); polyphonic characters checked against the TTS lexicons.
- `voice/tts.py` — offline TTS via sherpa-onnx (narrator: matcha zh-baker; God: Kokoro v1.1-zh speaker 101 with reverb;
  Jonah: Kokoro speaker 95). Builds `build/timeline.json` (currently ~137 s) and `build/audio/voice.wav`.
- `engine/` — SVG layers rasterised by headless Chromium, watercolour + paper texture, OpenCV compositor with
  motions, camera, fx (rain, lightning, bubbles, sparkles...), subtitles; parallel scene rendering (`engine/render.py`).
- `art/style.py` — palette and SVG helpers; `art/scenes/s01_title.py` — title page.
- `tools/preview.py` — render stills / contact sheet / clip of one scene.

Not done yet: `art/characters.py`, scenes s02–s13, `audio/` (music, sfx, mix), final assembly (`build.py`), output video.

## Requirements (Ubuntu 24.04)

    apt-get install fluidsynth musescore-general-soundfont fonts-lxgw-wenkai fonts-noto-cjk ffmpeg
    pip install sherpa-onnx playwright==1.56.0 opencv-python-headless numpy scipy soundfile pyloudnorm pillow mido

Chromium comes from Playwright (`PLAYWRIGHT_BROWSERS_PATH`, default `/opt/pw-browsers`).
TTS models go in `.cache/models/` (from https://github.com/k2-fsa/sherpa-onnx/releases):
`tts-models/kokoro-multi-lang-v1_1.tar.bz2`, `tts-models/matcha-icefall-zh-baker.tar.bz2`,
`vocoder-models/vocos-22khz-univ.onnx`; optional ASR check model
`asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2`.

## Usage so far

    cd jonah-video
    python3 voice/tts.py                 # voices + timeline
    python3 tools/preview.py s01_title   # stills + contact sheet in build/preview/
