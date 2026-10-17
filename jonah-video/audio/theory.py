"""Small music-theory toolkit for the score: pitches, scales, chords, voice-leading.

Pitches are MIDI numbers (C4 = 60).  Pitch classes are 0..11 (C = 0).
"""
import itertools
import re

import numpy as np

_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_ACC = {"": 0, "#": 1, "##": 2, "b": -1, "bb": -2}
_NOTE_RE = re.compile(r"^([A-G])(##|#|bb|b)?(-?\d+)$")
_PC_RE = re.compile(r"^([A-G])(##|#|bb|b)?$")
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def pc(name):
    m = _PC_RE.match(name)
    if not m:
        raise ValueError(f"bad pitch class {name!r}")
    return (_PC[m.group(1)] + _ACC[m.group(2) or ""]) % 12


def midi(name):
    m = _NOTE_RE.match(name)
    if not m:
        raise ValueError(f"bad note {name!r}")
    return 12 * (int(m.group(3)) + 1) + _PC[m.group(1)] + _ACC[m.group(2) or ""]


def name(p):
    return f"{NAMES[p % 12]}{p // 12 - 1}"


MODES = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
    "harmonic": (0, 2, 3, 5, 7, 8, 11),
    "melodic": (0, 2, 3, 5, 7, 9, 11),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
    "lydian": (0, 2, 4, 6, 7, 9, 11),
    "hijaz": (0, 1, 4, 5, 7, 8, 10),          # phrygian dominant
    "minor+": (0, 2, 3, 5, 7, 8, 10, 11),     # natural minor plus leading tone
}


class Scale:
    def __init__(self, spec):
        tonic, mode = spec.split()
        self.spec = spec
        self.tonic = pc(tonic)
        self.mode = mode
        self.pcs = frozenset((self.tonic + i) % 12 for i in MODES[mode])

    def __contains__(self, p):
        return p % 12 in self.pcs

    def degree_pitches(self, lo, hi):
        return [p for p in range(lo, hi + 1) if p % 12 in self.pcs]

    def __repr__(self):
        return f"Scale({self.spec})"


# Intervals listed in order of importance: root, third/sus, fifth, seventh, extensions.
QUALITIES = {
    "": (0, 4, 7), "m": (0, 3, 7), "dim": (0, 3, 6), "aug": (0, 4, 8),
    "7": (0, 4, 10, 7), "maj7": (0, 4, 11, 7), "m7": (0, 3, 10, 7), "m7b5": (0, 3, 6, 10),
    "dim7": (0, 3, 6, 9), "sus4": (0, 5, 7), "sus2": (0, 2, 7), "7sus4": (0, 5, 10, 7),
    "add9": (0, 4, 2, 7), "madd9": (0, 3, 2, 7), "6": (0, 4, 9, 7), "m6": (0, 3, 9, 7),
    "5": (0, 7), "maj9": (0, 4, 11, 2, 7),
}
_CHORD_RE = re.compile(r"^([A-G](?:#|b)?)([^/]*)(?:/([A-G](?:#|b)?))?$")


class Chord:
    def __init__(self, sym):
        m = _CHORD_RE.match(sym)
        if not m or m.group(2) not in QUALITIES:
            raise ValueError(f"bad chord {sym!r}")
        self.sym = sym
        self.root = pc(m.group(1))
        self.quality = m.group(2)
        ivs = QUALITIES[self.quality]
        self.pcs = tuple((self.root + i) % 12 for i in ivs)
        self.upper = frozenset(self.pcs)          # the chord proper (used for voicing)
        self.bass = pc(m.group(3)) if m.group(3) else self.root
        self.pedal = self.bass not in self.upper  # e.g. C/D: D is a pedal under a C triad
        self.pcset = self.upper | {self.bass}     # tones that are consonant with this sonority
        # Tones a complete voicing must contain (the fifth may be omitted when a 7th/9th is present).
        need = [self.pcs[0], self.pcs[1]] if len(self.pcs) > 1 else [self.pcs[0]]
        if len(ivs) >= 4 or self.quality in ("add9", "madd9", "6", "m6"):
            need.append(self.pcs[2])
        if self.quality in ("", "m", "dim", "aug", "sus4", "sus2", "5", "m7b5", "dim7"):
            need = list(self.pcs)
        self.need = frozenset(need)
        self.third = self.pcs[1] if ivs[1] in (3, 4) else None

    def tones(self, lo, hi):
        return [p for p in range(lo, hi + 1) if p % 12 in self.pcset]

    def bass_note(self, lo, hi):
        """Lowest bass pitch of the chord's bass pitch-class in [lo, hi]."""
        for p in range(lo, hi + 1):
            if p % 12 == self.bass:
                return p
        raise ValueError(f"no bass for {self.sym} in {lo}..{hi}")

    def __repr__(self):
        return f"Chord({self.sym})"


# ----------------------------------------------------------------------------- voice-leading
def _candidates(ch, n, lo, hi, bass_pc=None, max_gap=12, top=None):
    pitches = [p for p in range(lo, hi + 1) if p % 12 in ch.upper]
    root_third = frozenset(x for x in (ch.pcs[0], ch.third) if x is not None)
    for gap, need in ((max_gap, ch.need), (max_gap + 7, ch.need), (max_gap + 7, root_third)):
        out = []
        for combo in itertools.combinations(pitches, n):
            if top is not None and combo[-1] != top:
                continue
            if any(b - a > gap for a, b in zip(combo, combo[1:])):
                continue
            pcs = {p % 12 for p in combo}
            if bass_pc is not None:
                pcs.add(bass_pc)
            if not need <= pcs:
                continue
            out.append(combo)
        if out:
            return out
    return []


def _static_cost(V, ch, center, bass):
    """V: (K, n) candidate voicings.  Lower is better."""
    K, n = V.shape
    cost = np.abs(V.mean(axis=1) - center) * 0.12
    full = np.concatenate([np.full((K, 1), bass), V], axis=1) if bass is not None else V
    m = full.shape[1]
    for i in range(m):
        for j in range(i + 1, m):
            iv = np.abs(full[:, j] - full[:, i])
            cost += np.where((iv == 1) | (iv == 13), 8.0, 0.0)          # m2 / m9 clash
            cost += np.where(iv == 0, 6.0, 0.0)                          # unison doubling
            low = np.minimum(full[:, i], full[:, j])
            cost += np.where((iv < 5) & (low < 52), 2.0, 0.0)            # muddy low thirds
    if ch.third is not None:
        thirds = (V % 12 == ch.third).sum(axis=1)
        cost += np.where(thirds > 1, 2.5, 0.0)
    return cost


def _trans_cost(A, B, bass_a, bass_b):
    """Pairwise transition costs (Ka, Kb)."""
    motion = np.abs(A[:, None, :] - B[None, :, :])
    cost = motion.sum(axis=2).astype(float)
    cost += (motion > 7).sum(axis=2) * 3.0
    Af = A if bass_a is None else np.concatenate([np.full((len(A), 1), bass_a), A], axis=1)
    Bf = B if bass_b is None else np.concatenate([np.full((len(B), 1), bass_b), B], axis=1)
    m = Af.shape[1]
    for i in range(m):
        for j in range(i + 1, m):
            ia = (Af[:, j] - Af[:, i])[:, None]
            ib = (Bf[:, j] - Bf[:, i])[None, :]
            di = np.sign(Bf[None, :, i] - Af[:, None, i])
            dj = np.sign(Bf[None, :, j] - Af[:, None, j])
            moving = (di != 0) & (di == dj)
            perfect = ((ia % 12 == 0) & (ib % 12 == 0)) | ((ia % 12 == 7) & (ib % 12 == 7))
            cost += np.where(moving & perfect, 40.0, 0.0)
    return cost


def _guide_cost(A, B, guides):
    """Parallel P5/P8 (similar motion) between candidate voices and guide lines at one chord change.

    guides: [(pitch before, pitch at the change, fifths_only)] of other parts that move there."""
    cost = np.zeros((len(A), len(B)))
    for gb, ga, fifths_only in guides:
        dg = np.sign(ga - gb)
        if dg == 0:
            continue
        moving = np.sign(B[None, :, :] - A[:, None, :]) == dg
        ib = (np.abs(A - gb) % 12)[:, None, :]
        ia = (np.abs(B - ga) % 12)[None, :, :]
        perfect = (ib == ia) & ((ib == 7) | ((ib == 0) & (not fifths_only)))
        cost += (moving & perfect).sum(axis=2) * 40.0
    return cost


def voice_lead(chords, n, lo, hi, basses=None, center=None, prev=None, tops=None, max_gap=12, prev_bass=None,
               guides=None):
    """Choose smooth voicings (Viterbi) for a chord sequence.

    chords  list of Chord
    n       number of upper voices
    basses  optional list of bass pitches (part of coverage and parallel checks)
    prev    optional voicing that precedes the sequence (for continuity)
    prev_bass  bass pitch under prev (parallels against the bass are then checked at the join)
    guides  optional list (one per chord) of [(before, at, fifths_only)]: other lines (melody,
            counter-melody, basses, other pads) that move at that chord change; the voicing avoids
            parallel fifths/octaves with them (fifths only for doubling pads)
    tops    optional list of forced top pitches (None entries are free)
    """
    center = center if center is not None else (lo + hi) / 2
    basses = basses or [None] * len(chords)
    tops = tops or [None] * len(chords)
    cands, costs = [], []
    for ch, b, tp in zip(chords, basses, tops):
        c = _candidates(ch, n, lo, hi, None if b is None else b % 12, max_gap, tp)
        if not c:
            raise ValueError(f"no voicing for {ch.sym} n={n} in {lo}..{hi}")
        V = np.array(c)
        cands.append(V)
        costs.append(_static_cost(V, ch, center, b))
    score = costs[0].copy()
    guides = guides or [[] for _ in chords]
    if prev is not None:
        P = np.array([prev])
        pb = prev_bass if (prev_bass is not None and basses[0] is not None) else None
        score += _trans_cost(P, cands[0], pb, basses[0] if pb is not None else None)[0]
        score += _guide_cost(P, cands[0], guides[0])[0]
    back = []
    for k in range(1, len(chords)):
        tc = _trans_cost(cands[k - 1], cands[k], basses[k - 1], basses[k])
        if guides[k]:
            tc = tc + _guide_cost(cands[k - 1], cands[k], guides[k])
        tot = score[:, None] + tc
        bi = tot.argmin(axis=0)
        back.append(bi)
        score = tot[bi, np.arange(tot.shape[1])] + costs[k]
    idx = [int(score.argmin())]
    for bi in reversed(back):
        idx.append(int(bi[idx[-1]]))
    idx.reverse()
    return [tuple(int(x) for x in cands[k][i]) for k, i in enumerate(idx)]


def parallels(seq_a, seq_b):
    """Count parallel perfect fifths/octaves between two voices given as pitch lists (same length)."""
    bad = []
    for k in range(1, len(seq_a)):
        a0, a1, b0, b1 = seq_a[k - 1], seq_a[k], seq_b[k - 1], seq_b[k]
        if None in (a0, a1, b0, b1):
            continue
        da, db = np.sign(a1 - a0), np.sign(b1 - b0)
        if da == 0 or da != db:
            continue
        i0, i1 = abs(b0 - a0) % 12, abs(b1 - a1) % 12
        if i0 == i1 and i0 in (0, 7):
            bad.append(k)
    return bad
