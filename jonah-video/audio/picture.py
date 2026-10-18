"""Picture hit points for the score: on-screen actions that a cue illustrates with an accent.

A score hit that shows an action (a wave slamming into the ship, a mouth snapping shut, a horn being
blown, a foot stamping) must land on the PICTURE, not on the narration word that names it.  The scene
authors key their sound-effect cues to the animation, so the times are read at build time from the
scenes' own cues (``engine.loader.build_scene(sid, timeline).sfx_cues``, picked by cue name and order)
and the score follows later scene edits.  If a scene does not build or the cue is gone, the scene's own
narration formula (copied from the scene code) is used instead.

    events(timeline) -> {key: [scene-relative seconds, ...]}

  s08_row:wave_hit       the huge wave slams into the bow (the scene's 'splash' cue = T_HIT)
  s09_overboard:impact   Jonah hits the water: the scene's 'splash' cue + 0.02 s (it puts the cue at t_impact - 0.02)
  s10_swallow:mouth_shut the fish's mouth snaps shut: halfway through its close, 0.32 s after the 'gulp'
                         cue (which the scene puts on the lunge, 0.05 s after it starts)
  s17_king:horn_blow     the messenger blows the horn (the scene's first 'horn' cue = t_blow)
  s22_worm:stomps        Jonah's stamps in his closing outburst: the 'thud' cues from the start of the line
                         containing '我气极了' on (up to three)
"""
import math

PUNCT = "，。！？：；、,.!?:;…"


def _line(scene, phrase):
    for ln in scene["lines"]:
        if phrase in ln["text"]:
            return ln
    return None


def _chunk_start(ln, phrases):
    for ph in phrases:
        for c in ln.get("chunks") or []:
            if ph in c["text"]:
                return c["start"]
    return None


def _share(ln, phrase, punct_w=0.0, strip=False):
    """Chunk start + the phrase's share of the chunk by characters (punctuation weighs punct_w)."""
    for c in ln.get("chunks") or [{"text": ln["text"], "start": ln["start"], "end": ln["end"]}]:
        txt = c["text"]
        i = txt.find(phrase)
        if i < 0:
            continue
        body = txt.rstrip(PUNCT) if strip else txt
        w = lambda s: sum(punct_w if ch in PUNCT else 1.0 for ch in s)
        return c["start"] + (c["end"] - c["start"]) * w(txt[:i]) / max(1e-9, w(body))
    return ln["start"]


def _snap(t, fps=30):
    return (math.floor(t * fps) + 0.5) / fps


# ------------------------------------------------------------------ fallbacks (the scenes' own formulas)

def _fb_wave_hit(s):
    ln = s["lines"][1] if len(s["lines"]) > 1 else s["lines"][0]
    t_fail = _chunk_start(ln, ["都没有办法", "没有办法"])
    if t_fail is None:
        t_fail = ln["start"] + 0.6 * (ln["end"] - ln["start"])
    return [t_fail + 0.12]


def _dips(path):
    """Low-energy stretches (>= 40 ms) inside a voice take, s from its start (as art/scenes/s09_overboard.py)."""
    try:
        import numpy as np
        import soundfile as sf
        x, sr = sf.read(str(path), dtype="float32")
    except Exception:
        return []
    if x.ndim == 2:
        x = x.mean(axis=1)
    hop = sr // 100
    nb = len(x) // hop
    if nb < 10:
        return []
    e = np.sqrt((x[:nb * hop] ** 2).reshape(nb, hop).mean(axis=1))
    e = np.convolve(e, np.ones(3) / 3, mode="same")
    low = e < 0.06 * e.max()
    out, i = [], 0
    while i < nb:
        if low[i]:
            j = i
            while j < nb and low[j]:
                j += 1
            if j - i >= 4 and i > 0 and j < nb:
                out.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    return out


def _snapped(s, i, phrase, default):
    """The scene's Cues.at: a phrase inside a chunk is placed by its characters and snapped to the end of the
    best nearby dip in the line's voice take (build/voice/lines/<scene>_<i>.wav)."""
    from engine.paths import BUILD

    ln = s["lines"][i]
    if phrase not in ln["text"]:
        return default
    for c in ln.get("chunks") or [{"text": ln["text"], "start": ln["start"], "end": ln["end"]}]:
        k = c["text"].find(phrase)
        if k < 0:
            continue
        if not any(ch not in PUNCT for ch in c["text"][:k]):
            return c["start"]
        est = _share(ln, phrase)
        best, score = None, -1.0
        for a, b in _dips(BUILD / "voice" / "lines" / f"{s['id']}_{i:02d}.wav"):
            a, b = ln["start"] + a, ln["start"] + b
            if c["start"] < a and b < c["end"] and abs(b - est) < 0.45:
                sc_ = (b - a) - 0.15 * abs(b - est)
                if sc_ > score:
                    best, score = b, sc_
        return best if best is not None else est
    return default


def _fb_impact(s):
    """s09: the lifters' timing from the narration (the scene's own formula: t_impact = t_launch + 0.72)."""
    ln = s["lines"][0]
    at = lambda ph, default: _snapped(s, 0, ph, default)
    t_grab = max(at("他们", ln["start"] + 0.7) + 0.12, ln["start"] + 0.02 + 0.75)
    t_lift = max(at("抬起来", ln["start"] + 1.8) - 0.12, t_grab + 0.5)
    t_heave0 = max(at("扔进", ln["start"] + 2.6) - 0.3, t_lift + 0.34 + 0.2)
    return [t_heave0 + 0.52 + 0.72]


def _fb_mouth_shut(s):
    ln = _line(s, "一口") or s["lines"][-1]
    t_open0 = max(_share(ln, "张开大嘴") - 0.1, ln["start"] + 0.6) if "张开大嘴" in ln["text"] else ln["start"] + 0.6
    t_surge0 = max(_share(ln, "一口") + 0.08, t_open0 + 0.85 + 0.3)
    return [t_surge0 + 0.37]


def _fb_horn_blow(s):
    ln = _line(s, "全城宣告")
    if ln is None:
        return []
    c1 = (ln.get("chunks") or [ln])[0]["start"]
    t_go = _snap(c1 + 0.55)
    return [_snap(_snap(t_go + 7 * 0.25) + 0.12) + 0.18]


def _fb_stomps(s):
    ln = _line(s, "我气极了")
    if ln is None:
        return []
    out = [ln["start"] + 0.02]                                     # '对！'
    if "我就是" in ln["text"]:
        out.append(_share(ln, "我就是", punct_w=1.5, strip=True) + 0.25)    # stamps on '我就是生气！'
    t_hmph = _chunk_start(ln, ["我气极了"])
    out.append((ln["start"] if t_hmph is None else t_hmph) + 0.32)     # '我气极了！'
    return sorted(out)


# key: (scene, sfx cue name, picker(scene, cue times) -> [times], offset s, fallback)
def _first(s, ts):
    return ts[:1]


def _from_line(phrase, n=3, early=0.3):
    def pick(s, ts):
        ln = _line(s, phrase)
        if ln is None:
            return []
        return [t for t in ts if t >= ln["start"] - early][:n]
    return pick


EVENTS = {
    "s08_row:wave_hit": ("s08_row", "splash", _first, 0.0, _fb_wave_hit),
    "s09_overboard:impact": ("s09_overboard", "splash", _first, 0.02, _fb_impact),
    "s10_swallow:mouth_shut": ("s10_swallow", "gulp", _first, 0.32, _fb_mouth_shut),
    "s17_king:horn_blow": ("s17_king", "horn", _first, 0.0, _fb_horn_blow),
    "s22_worm:stomps": ("s22_worm", "thud", _from_line("我气极了"), 0.0, _fb_stomps),
}


def events(timeline, verbose=True):
    """{key: [scene-relative s]} for every EVENTS entry whose scene is in the timeline; 'source' notes in
    events['_source'] ({key: 'sfx' | 'fallback: <reason>'})."""
    from engine.loader import build_scene

    by_id = {s["id"]: s for s in timeline["scenes"]}
    out, src, built = {}, {}, {}
    for key, (sid, name, pick, off, fallback) in EVENTS.items():
        s = by_id.get(sid)
        if s is None:
            continue
        why = None
        if sid not in built:
            try:
                built[sid] = build_scene(sid, timeline).sfx_cues
            except Exception as e:                      # a scene mid-edit must not break the music build
                built[sid] = e
        cues = built[sid]
        if isinstance(cues, Exception):
            why = f"scene does not build ({type(cues).__name__}: {cues})"
        else:
            ts = pick(s, sorted(float(c["at"]) for c in cues if c["name"] == name))
            if ts:
                out[key] = [t + off for t in ts]
                src[key] = "sfx"
                continue
            why = f"no '{name}' cue"
        try:
            out[key] = list(fallback(s))
        except Exception as e:
            out[key] = []
            why += f"; fallback failed ({e})"
        src[key] = f"fallback: {why}"
        if verbose:
            print(f"  score: {key}: {why}; using the scene's narration formula")
    out["_source"] = src
    return out
