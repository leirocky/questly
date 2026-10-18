"""Render every scene to build/video/<id>.mp4 in parallel, skipping unchanged scenes."""
import hashlib
import re
import multiprocessing as mp
import time
from pathlib import Path

from engine import compositor, raster
from engine.loader import build_scene, load_timeline, scene_ids
from engine.paths import BUILD, ROOT, SCENES_DIR

# Files whose changes invalidate every rendered scene.
_SHARED = ["engine/compositor.py", "engine/motion.py", "engine/fx.py", "engine/scene.py", "engine/watercolor.py",
           "engine/raster.py", "art/style.py", "art/characters.py"]


def _imports(sid):
    src = (SCENES_DIR / f"{sid}.py").read_text()
    deps = set(re.findall(r"(?:art|stories\.\w+)\.scenes\.(s\d\d_\w+)", src))
    deps |= {m for line in re.findall(r"from (?:art|stories\.\w+)\.scenes import ([^\n]+)", src) for m in re.findall(r"s\d\d_\w+", line)}
    return deps


def _scene_deps(sid, tl):
    """v2 scene files a scene depends on: its neighbours, whose first/last frames it matches across the
    dissolves (often by copying their constants or building them), and every scene those import."""
    ids = [s["id"] for s in tl["scenes"]]
    k = ids.index(sid)
    deps, todo = set(), list(ids[max(0, k - 1):k + 2]) + sorted(_imports(sid))
    while todo:
        d = todo.pop()
        if d not in deps and (SCENES_DIR / f"{d}.py").exists():
            deps.add(d)
            todo += sorted(_imports(d))
    return sorted(deps)


def _scene_hash(sid, tl):
    h = hashlib.sha1()
    v1 = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "art" / "scenes_v1").glob("*.py"))
    deps = [str((SCENES_DIR / f"{d}.py").relative_to(ROOT)) for d in _scene_deps(sid, tl)]
    for rel in _SHARED + ["art/props.py", "art/characters.py"] + v1 + deps:
        p = ROOT / rel
        if p.exists():
            h.update(p.read_bytes())
    entry = next(s for s in tl["scenes"] if s["id"] == sid)
    # the transition into a scene is applied when the film is assembled, not when the scene is drawn
    h.update(repr(sorted((k, str(v)) for k, v in entry.items() if k != "transition")).encode())
    return h.hexdigest()


def _prepare_one(sid):
    """Rasterise + watercolour all layers of one scene (fills the disk caches)."""
    compositor.prepare(build_scene(sid))
    raster.close()
    return sid


def _render_one(sid):
    import cv2

    cv2.setNumThreads(1)
    t0 = time.time()
    tl = load_timeline()
    out = BUILD / "video" / f"{sid}.mp4"
    compositor.render_video(build_scene(sid, tl), out)
    (BUILD / "video" / f"{sid}.hash").write_text(_scene_hash(sid, tl))
    return sid, time.time() - t0


def render_all(ids=None, jobs=3, force=False):
    tl = load_timeline()
    ids = ids or scene_ids(tl)
    (BUILD / "video").mkdir(parents=True, exist_ok=True)
    todo = []
    for sid in ids:
        hp = BUILD / "video" / f"{sid}.hash"
        if not force and hp.exists() and (BUILD / "video" / f"{sid}.mp4").exists() \
                and hp.read_text() == _scene_hash(sid, tl):
            print(f"  {sid}: up to date")
            continue
        todo.append(sid)
    if not todo:
        return
    # Rasterise sequentially (one Chromium), then composite in parallel processes.
    for sid in todo:
        _prepare_one(sid)
        print(f"  {sid}: layers ready")
    ctx = mp.get_context("spawn")
    with ctx.Pool(min(jobs, len(todo))) as pool:
        for sid, dt in pool.imap_unordered(_render_one, todo):
            print(f"  {sid}: rendered in {dt:.0f}s")


def video_paths(tl=None):
    tl = tl or load_timeline()
    return [Path(BUILD / "video" / f"{s['id']}.mp4") for s in tl["scenes"]]
