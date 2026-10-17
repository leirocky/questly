"""Shared paths and global video constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"          # regenerated intermediates (git-ignored)
CACHE = ROOT / ".cache"         # downloaded models + raster cache (git-ignored)
MODELS = CACHE / "models"
OUTPUT = ROOT / "output"

FPS = 30
OUT_W, OUT_H = 1920, 1080       # final video size
STAGE_W, STAGE_H = 2112, 1188   # default illustration canvas (1.1x frame, room for camera moves)
SR = 48000                      # audio sample rate

FONT_DIR = Path("/usr/share/fonts/truetype/lxgw-wenkai")
FONT_REGULAR = FONT_DIR / "LXGWWenKai-Regular.ttf"
FONT_BOLD = FONT_DIR / "LXGWWenKai-Bold.ttf"


def ensure_dirs():
    for d in (BUILD, CACHE, OUTPUT):
        d.mkdir(parents=True, exist_ok=True)
