#!/usr/bin/env bash
# One-time environment setup for the picture-book video pipeline (Ubuntu 24.04).
# Installs system packages, Python packages and downloads the offline speech models
# into .cache/models/. Safe to re-run: existing models are skipped.
set -euo pipefail
cd "$(dirname "$0")"

if command -v apt-get >/dev/null; then
  SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
  $SUDO apt-get update -q
  DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -q \
    ffmpeg fluidsynth musescore-general-soundfont fluid-soundfont-gm fonts-lxgw-wenkai fonts-noto-cjk
fi

pip install -q sherpa-onnx playwright==1.56.0 opencv-python-headless numpy scipy soundfile pyloudnorm \
  pillow mido pypinyin
# Chromium: use a preinstalled Playwright browser if PLAYWRIGHT_BROWSERS_PATH has one, else download it.
if ! ls "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"/chromium-*/chrome-linux*/chrome >/dev/null 2>&1; then
  python3 -m playwright install chromium
fi

M=.cache/models
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
mkdir -p "$M"
fetch_tar() {  # $1 = release path, $2 = directory it unpacks to
  if [ ! -d "$M/$2" ]; then
    echo "downloading $2"
    curl -sSL --retry 4 -o "$M/tmp.tar.bz2" "$R/$1" && tar xjf "$M/tmp.tar.bz2" -C "$M" && rm "$M/tmp.tar.bz2"
  fi
}
fetch_file() {  # $1 = release path, $2 = file name
  [ -f "$M/$2" ] || { echo "downloading $2"; curl -sSL --retry 4 -o "$M/$2" "$R/$1"; }
}
fetch_tar tts-models/matcha-icefall-zh-baker.tar.bz2 matcha-icefall-zh-baker
fetch_tar tts-models/kokoro-multi-lang-v1_1.tar.bz2 kokoro-multi-lang-v1_1
fetch_tar tts-models/sherpa-onnx-zipvoice-distill-zh-en-emilia.tar.bz2 sherpa-onnx-zipvoice-distill-zh-en-emilia
fetch_tar asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2 \
  sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17
fetch_file vocoder-models/vocos-22khz-univ.onnx vocos-22khz-univ.onnx
fetch_file vocoder-models/vocos_24khz.onnx vocos_24khz.onnx
echo "setup complete — run: python3 build.py all"
