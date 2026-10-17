#!/usr/bin/env bash
# One-time environment setup for the picture-book video pipeline (Ubuntu 24.04 or macOS with Homebrew).
# Installs system packages, Python packages and downloads the offline speech models
# into .cache/models/. Safe to re-run: existing models are skipped.
set -euo pipefail
cd "$(dirname "$0")"

if [ "$(uname)" = "Darwin" ]; then
  command -v brew >/dev/null || { echo "Homebrew is required: https://brew.sh"; exit 1; }
  brew install ffmpeg fluid-synth
  # LXGW WenKai v1.315 — the version Ubuntu ships (later releases renamed Bold to Medium).
  mkdir -p ~/Library/Fonts
  for f in LXGWWenKai-Regular.ttf LXGWWenKai-Bold.ttf LXGWWenKai-Light.ttf; do
    [ -f ~/Library/Fonts/$f ] || [ -f /Library/Fonts/$f ] || curl -sSL --retry 4 -o ~/Library/Fonts/$f \
      "https://github.com/lxgw/LxgwWenKai/releases/download/v1.315/$f"
  done
elif command -v apt-get >/dev/null; then
  SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
  $SUDO apt-get update -q
  DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -q \
    ffmpeg fluidsynth musescore-general-soundfont fluid-soundfont-gm fonts-lxgw-wenkai fonts-noto-cjk
fi

PY=${PYTHON:-python3}
if [ "$(uname)" = "Darwin" ] && [ -z "${VIRTUAL_ENV:-}" ]; then
  # Homebrew's Python refuses system-wide pip installs (PEP 668): use a local venv.
  [ -d .venv ] || python3 -m venv .venv
  PY=.venv/bin/python
fi
$PY -m pip install -q sherpa-onnx==1.13.8 playwright==1.56.0 opencv-python-headless numpy scipy soundfile pyloudnorm \
  pillow mido pypinyin==0.55.0 zstandard   # pinned: lexicons and take cache keys depend on them
# Soundfont: macOS (and Linux without the apt package) gets the same MuseScore General file in .cache/.
[ -f /usr/share/sounds/sf3/MuseScore_General.sf3 ] || $PY tools/fetch_soundfont.py
# Chromium: use a preinstalled Playwright browser if PLAYWRIGHT_BROWSERS_PATH has one, else download it.
if ! ls "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"/chromium-*/chrome-linux*/chrome >/dev/null 2>&1; then
  $PY -m playwright install chromium
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
echo "setup complete — run: $PY build.py all"
if [ "$PY" = .venv/bin/python ]; then echo "(or: source .venv/bin/activate, then python3 build.py all)"; fi
