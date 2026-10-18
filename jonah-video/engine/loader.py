"""Load the timeline and build Scene objects from art/scenes/<id>.py."""
import importlib
import json

from engine.paths import BUILD, SCENES_PKG
from engine.scene import SceneContext


def load_timeline():
    path = BUILD / "timeline.json"
    if not path.exists():
        raise SystemExit(f"{path} missing — run: python3 build.py voice")
    return json.loads(path.read_text())


def scene_ids(timeline=None):
    tl = timeline or load_timeline()
    return [s["id"] for s in tl["scenes"]]


def context(scene_id, timeline=None):
    tl = timeline or load_timeline()
    for s in tl["scenes"]:
        if s["id"] == scene_id:
            return SceneContext.from_timeline(s)
    raise KeyError(scene_id)


def build_scene(scene_id, timeline=None):
    mod = importlib.import_module(f"{SCENES_PKG}.{scene_id}")
    importlib.reload(mod)
    return mod.build(context(scene_id, timeline))
