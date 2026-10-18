"""Shared paths and global video constants."""
import os
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

def _find_font(name):
    """Locate an LXGW WenKai font file on Linux (fonts-lxgw-wenkai) or macOS (brew cask font-lxgw-wenkai)."""
    dirs = [os.environ.get("JONAH_FONT_DIR", ""), "/usr/share/fonts/truetype/lxgw-wenkai",
            str(Path.home() / "Library/Fonts"), "/Library/Fonts", "/opt/homebrew/share/fonts",
            "/usr/local/share/fonts", str(Path.home() / ".local/share/fonts"), "/usr/share/fonts"]
    for d in dirs:
        if d and Path(d).is_dir():
            hit = next(Path(d).rglob(name), None)
            if hit:
                return hit
    return Path("/usr/share/fonts/truetype/lxgw-wenkai") / name   # clear error later if missing


def _find_soundfont():
    """MuseScore General soundfont: $JONAH_SOUNDFONT, the Ubuntu package, or tools/fetch_soundfont.py's copy."""
    for c in (os.environ.get("JONAH_SOUNDFONT", ""), "/usr/share/sounds/sf3/MuseScore_General.sf3",
              str(ROOT / ".cache" / "soundfonts" / "MuseScore_General.sf3")):
        if c and Path(c).exists():
            return Path(c)
    return ROOT / ".cache" / "soundfonts" / "MuseScore_General.sf3"


FONT_REGULAR = _find_font("LXGWWenKai-Regular.ttf")
FONT_BOLD = _find_font("LXGWWenKai-Bold.ttf")
SOUNDFONT = _find_soundfont()


def ensure_dirs():
    for d in (BUILD, CACHE, OUTPUT):
        d.mkdir(parents=True, exist_ok=True)
