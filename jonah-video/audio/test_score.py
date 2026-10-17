"""Robustness tests of the score generator against re-timed narration (no audio rendering).

    python3 -m audio.test_score          # from the project root; or: python3 -m pytest audio/test_score.py

The score reads every scene start and line timing from the timeline, so a TTS re-trim, a new
narrator or a LINE_GAP change must not break `build.py music`.  Each variant re-times
build/timeline.json the way voice/tts.py lays scenes out (lead-in, lines, pauses, tail, scenes
overlapping by the cross-dissolve) -- uniformly (all pauses set to one length, all lines scaled
alike) and non-uniformly (every pause scaled by its own random factor 0.3-1.6, every line by
0.85-1.2, several seeds) -- and checks:
  * the score builds (no crash when pauses shrink below the fill / pause helpers' minimum),
  * every cue's segments tile its window exactly and every hit point lies inside its cue,
  * every required hit point (music_check.REQUIRED_HITS, defined by the narration text) is placed,
  * no segment tempo strays more than 35 % from its nominal tempo,
  * harmony (incl. let-ring / echo tails): 0 violations, notes inside instrument ranges, 0 parallel
    fifths/octaves (whole score),
  * each MIDI bus fits in 15 melodic channels.
"""
import copy
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from audio import music_check, score
from audio.scorekit import PARTS

VARIANTS = [  # (label, pause between lines in s or None = as built, speech-length factor)
    ("as built", None, 1.0),
    ("pauses 0.15 s", 0.15, 1.0),
    ("pauses 0.20 s", 0.20, 1.0),
    ("pauses 0.50 s", 0.50, 1.0),
    ("speech x0.9", None, 0.9),
    ("speech x1.1", None, 1.1),
    ("pauses 0.15 s, speech x1.1", 0.15, 1.1),
]
JITTER_SEEDS = (1, 2, 3, 4, 5, 6)      # non-uniform variants: each pause x0.3-1.6, each line x0.85-1.2
MAX_TEMPO_DEV = 0.35


def retime(tl, gap=None, speech=1.0, seed=None):
    """Copy of the timeline with every line's length scaled by `speech` and the pauses between lines
    set to `gap` (None keeps them); lead-ins and tails are kept, scenes overlap by the cross-dissolve.
    seed: non-uniform instead -- every pause scaled by its own factor in 0.3..1.6 and every line by
    its own factor in 0.85..1.2."""
    tl = copy.deepcopy(tl)
    rnd = random.Random(seed) if seed is not None else None
    t_scene = 0.0
    for sc in tl["scenes"]:
        lines = sc["lines"]
        tail = sc["duration"] - lines[-1]["end"]
        gaps = [b["start"] - a["end"] for a, b in zip(lines, lines[1:])] + [0.0]
        cur = lines[0]["start"]
        for ln, g in zip(lines, gaps):
            f = rnd.uniform(0.85, 1.2) if rnd else speech
            length = (ln["end"] - ln["start"]) * f
            old = ln["start"]
            ln["start"], ln["end"] = round(cur, 3), round(cur + length, 3)
            for ch in ln.get("chunks") or []:          # word timings move with their line
                ch["start"] = round(cur + (ch["start"] - old) * f, 3)
                ch["end"] = round(cur + (ch["end"] - old) * f, 3)
            if rnd:
                g = g * rnd.uniform(0.3, 1.6)
            cur = ln["end"] + (gap if gap is not None else g)
        sc["duration"] = round(lines[-1]["end"] + tail, 3)
        sc["start"] = round(t_scene, 3)
        t_scene += sc["duration"] - tl["xfade"]
    last = tl["scenes"][-1]
    tl["duration"] = round(last["start"] + last["duration"], 3)
    return tl


def check_variant(tl):
    """Build the score for a timeline and return a list of problems (empty = OK)."""
    problems = []
    sc = score.build(tl)
    for c in sc.cues:
        segs = c.segs
        if abs(segs[0].t0 - c.t0) > 1e-6 or abs(segs[-1].t1 - c.t1) > 1e-6:
            problems.append(f"{c.id}: segments do not fill the cue window")
        for a, b in zip(segs, segs[1:]):
            if abs(a.t1 - b.t0) > 1e-6:
                problems.append(f"{c.id}: gap/overlap between {a.label} and {b.label}")
            if b.t1 - b.t0 <= 0.05:
                problems.append(f"{c.id}: segment {b.label} has no room ({b.t1 - b.t0:.3f} s)")
        for s in segs:
            if s.nominal and abs(s.tempo / s.nominal - 1) > MAX_TEMPO_DEV:
                problems.append(f"{s.label}: tempo {s.tempo:.0f} vs nominal {s.nominal} "
                                f"({100 * (s.tempo / s.nominal - 1):+.0f} %)")
    cue_win = {c.id: (c.t0, c.t1) for c in sc.cues}
    for cid, label, target, actual, kind in sc.syncs:
        a, b = cue_win[cid]
        if not (a - 1e-6 <= target <= b + 1e-6 and a - 1e-6 <= actual <= b + 1e-6):
            problems.append(f"{cid}: hit point '{label}' outside its cue")
    for sid, ph, mode, kind, target, got in music_check.required_hits(sc, tl):
        if got is None:
            problems.append(f"required hit point missing or moved: {sid} {kind} '{ph}' ({mode}) at {target:.3f} s")
    sc.perform()                                   # rendered durations: let-ring and echo tails
    _, viol = music_check.check_harmony(sc)
    problems += [f"harmony: {msg}" for _, msg in viol[:5]]
    problems += [f"range: {n.seg.cue.id} {n.part} {n.pitch}" for n in music_check.check_ranges(sc)[:5]]
    bad, _ = music_check.check_parallels_global(sc)
    problems += [f"parallel {k} at {t:.2f}s {va}/{vb}" for t, _, _, k, va, vb, *_ in bad[:5]]
    buses = defaultdict(set)
    for n in sc.notes:
        if not PARTS[n.part].drum:
            buses[PARTS[n.part].bus].add(n.part)
    problems += [f"bus {b} needs {len(p)} channels" for b, p in buses.items() if len(p) > 15]
    return problems, sc


def _timeline():
    import json
    import os
    if os.environ.get("SCORE_TIMELINE"):            # test against a saved snapshot
        return json.loads(Path(os.environ["SCORE_TIMELINE"]).read_text())
    from engine.loader import load_timeline
    return load_timeline()


def variants(tl):
    """[(label, re-timed timeline)]: the uniform variants and the non-uniform jitter seeds."""
    out = [(label, retime(tl, gap, speech)) for label, gap, speech in VARIANTS]
    return out + [(f"jitter seed {k}", retime(tl, seed=k)) for k in JITTER_SEEDS]


def test_variants():
    failures = {}
    for label, t2 in variants(_timeline()):
        problems, _ = check_variant(t2)
        if problems:
            failures[label] = problems
    assert not failures, failures


def main():
    tl = _timeline()
    n_fail = 0
    cases = variants(tl)
    for label, t2 in cases:
        problems, sc = check_variant(t2)
        devs = [100 * (s.tempo / s.nominal - 1) for c in sc.cues for s in c.segs if s.nominal]
        print(f"  {label:28s} duration {t2['duration']:7.2f}s  notes {len(sc.notes):5d}  "
              f"tempo dev {min(devs):+4.0f}..{max(devs):+4.0f} %  -> {'OK' if not problems else 'FAIL'}")
        for p in problems:
            print(f"      ! {p}")
        n_fail += bool(problems)
    print(f"{len(cases) - n_fail}/{len(cases)} timeline variants OK")
    return n_fail


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
