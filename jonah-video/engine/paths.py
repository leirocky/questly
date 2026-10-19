"""Shared paths and global video constants."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache"         # downloaded models + raster/TTS caches, shared by all stories (git-ignored)
MODELS = CACHE / "models"
OUTPUT = ROOT / "output"

# Story project (python3 build.py --story <name>, or PB_STORY): "jonah" is the original layout (story.py,
# art/scenes/, voice/takes/, build/); any other story lives in stories/<name>/ (story.py, scenes/, takes/)
# and builds into build/<name>/. Engine, art library, voices and audio code are shared.
STORY = os.environ.get("PB_STORY", "jonah")
if STORY == "jonah":
    PROJECT = ROOT
    SCENES_DIR, SCENES_PKG = ROOT / "art" / "scenes", "art.scenes"
    TAKES = ROOT / "voice" / "takes"
    BUILD = ROOT / "build"      # regenerated intermediates (git-ignored)
else:
    PROJECT = ROOT / "stories" / STORY
    SCENES_DIR, SCENES_PKG = PROJECT / "scenes", f"stories.{STORY}.scenes"
    TAKES = PROJECT / "takes"
    BUILD = ROOT / "build" / STORY
OUT_NAME = f"{STORY}_story.mp4"


def load_story():
    """The current story's story.py as the module ``story``."""
    import importlib.util
    import sys

    if "story" not in sys.modules or getattr(sys.modules["story"], "__file__", "") != str(PROJECT / "story.py"):
        spec = importlib.util.spec_from_file_location("story", PROJECT / "story.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["story"] = mod
        spec.loader.exec_module(mod)
    return sys.modules["story"]

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
