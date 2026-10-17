"""Score framework: parts, segments with tempo maps, chord tracks, notes -> MIDI -> fluidsynth.

All musical positions are in quarter notes (``q``) relative to the start of a segment.
Each segment owns an exact time map from q to absolute seconds on the film timeline, so a
segment of N bars always fills exactly the window it is given (tempo = N bars / window).
"""
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

import mido
import numpy as np

from audio.theory import Chord, Scale, midi, voice_lead

SOUNDFONT = "/usr/share/sounds/sf3/MuseScore_General.sf3"
SR = 48000
PPQ = 960
TEMPO_US = 500000                      # fixed MIDI tempo: 1 tick = 1/1920 s
TICKS_PER_S = PPQ * 1e6 / TEMPO_US

METERS = {  # meter -> (bar length in q, beat length in q)
    "4/4": (4.0, 1.0), "3/4": (3.0, 1.0), "2/4": (2.0, 1.0),
    "6/8": (3.0, 1.5), "3/8": (1.5, 1.5), "12/8": (6.0, 1.5),
}


@dataclass
class Part:
    name: str
    bank: int
    prog: int
    bus: str
    pan: float = 0.0
    gain_db: float = -4.0
    lo: int = 21
    hi: int = 108
    attack: float = 0.0        # onset pre-roll (s) for slow-speaking samples
    legato: float = 0.0        # overlap added to note ends (s)
    duck_db: float = 2.5       # expression dip while narration is spoken
    jitter: float = 0.008      # timing humanisation (s, sigma)
    drum: bool = False


PARTS = {p.name: p for p in [
    # keyboards / tuned percussion / harp
    Part("mbox", 0, 10, "keys", 0.15, 0, 60, 100, jitter=0.006, duck_db=2.5),
    Part("celesta", 0, 8, "keys", -0.2, 0, 60, 108, jitter=0.007, duck_db=2.5),
    Part("glock", 0, 9, "keys", 0.3, -3, 72, 108, jitter=0.005, duck_db=2.5),
    Part("harp", 0, 46, "keys", -0.35, -4, 24, 103, jitter=0.006, duck_db=2.0),
    Part("piano", 0, 0, "keys", 0.05, -1, 21, 108, jitter=0.007, duck_db=2.0),
    # bowed strings (section banks of MuseScore General); low parts stay near the centre
    Part("vln1", 20, 49, "str_hi", -0.45, -6, 55, 100, attack=0.12, legato=0.04, jitter=0.010, duck_db=1.5),
    Part("vln2", 25, 49, "str_hi", -0.2, -7, 55, 96, attack=0.12, legato=0.04, jitter=0.010, duck_db=1.5),
    Part("vla", 30, 49, "str_lo", 0.15, -7, 48, 88, attack=0.11, legato=0.04, jitter=0.010, duck_db=1.5),
    Part("vc", 40, 49, "str_lo", 0.25, -7, 36, 76, attack=0.14, legato=0.04, jitter=0.010, duck_db=1.5),
    Part("cb", 50, 49, "str_lo", 0.12, -9, 28, 60, attack=0.13, legato=0.04, jitter=0.010, duck_db=1.0),
    Part("vln_mel", 20, 48, "str_hi", -0.3, -1, 55, 100, attack=0.05, legato=0.03, jitter=0.008, duck_db=2.5),
    Part("vc_fast", 40, 48, "str_lo", 0.2, -4, 36, 76, attack=0.04, legato=0.02, jitter=0.006, duck_db=1.5),
    Part("cb_fast", 50, 48, "str_lo", 0.1, -5, 28, 60, attack=0.04, legato=0.02, jitter=0.006, duck_db=1.0),
    Part("trem_hi", 20, 44, "str_hi", -0.35, -6, 55, 100, attack=0.06, legato=0.03, jitter=0.010, duck_db=1.5),
    Part("trem_va", 30, 44, "str_lo", 0.1, -6, 48, 88, attack=0.06, legato=0.03, jitter=0.010, duck_db=1.5),
    Part("trem_lo", 40, 44, "str_lo", 0.25, -6, 36, 76, attack=0.06, legato=0.03, jitter=0.010, duck_db=1.5),
    Part("choir", 0, 52, "str_hi", 0.0, -7, 48, 81, attack=0.16, legato=0.05, jitter=0.012, duck_db=2.0),
    Part("ooh", 0, 53, "str_hi", 0.1, -8, 52, 81, attack=0.18, legato=0.05, jitter=0.0, duck_db=1.5),
    Part("pad", 0, 89, "str_lo", 0.0, -10, 36, 84, attack=0.25, legato=0.10, jitter=0.0, duck_db=1.0),
    Part("contrab", 0, 43, "str_lo", 0.1, -6, 28, 60, attack=0.03, jitter=0.006, duck_db=1.0),
    # plucked
    Part("pz_hi", 20, 45, "pluck", -0.35, -3, 55, 100, jitter=0.007, duck_db=2.0),
    Part("pz_lo", 40, 45, "pluck", 0.2, -5, 36, 76, jitter=0.006, duck_db=1.5),
    Part("pz_cb", 50, 45, "pluck", 0.12, -6, 28, 60, jitter=0.006, duck_db=1.0),
    Part("guitar", 0, 24, "pluck", -0.25, -5, 40, 84, jitter=0.008, duck_db=2.0),
    # winds and brass
    Part("flute", 0, 73, "wind", -0.15, -2, 60, 96, attack=0.03, jitter=0.008, duck_db=2.5),
    Part("oboe", 0, 68, "wind", 0.1, -3, 58, 91, attack=0.03, jitter=0.008, duck_db=2.5),
    Part("clar", 0, 71, "wind", 0.2, -1, 50, 91, attack=0.02, jitter=0.008, duck_db=2.5),
    Part("bsn", 0, 70, "wind", -0.1, -3, 34, 75, attack=0.02, jitter=0.008, duck_db=2.0),
    Part("horn", 0, 60, "wind", -0.1, -4, 41, 77, attack=0.04, legato=0.03, jitter=0.010, duck_db=2.0),
    Part("tbn", 0, 57, "wind", 0.15, -12, 40, 72, attack=0.03, legato=0.03, jitter=0.010, duck_db=2.0),
    Part("tuba", 0, 58, "wind", 0.1, -9, 28, 60, attack=0.02, legato=0.02, jitter=0.006, duck_db=1.5),
    Part("brass", 0, 61, "wind", 0.0, -11, 40, 84, attack=0.06, legato=0.03, jitter=0.010, duck_db=2.0),
    # percussion
    Part("timp", 0, 47, "perc", 0.05, -8, 38, 60, jitter=0.004, duck_db=2.0),
    Part("okit", 128, 48, "perc", 0.0, -8, 0, 127, jitter=0.004, drum=True, duck_db=1.0),
    Part("hand", 128, 0, "hand", 0.1, -6, 0, 127, jitter=0.005, drum=True, duck_db=2.0),
    # echoing celesta drops inside the fish (own bus gets a delay line)
    Part("echo_cel", 0, 8, "echo", 0.0, -4, 60, 108, jitter=0.0, duck_db=1.0),
]}

ROLE_STRICT = {"pad", "bass", "arp", "harmony", "timp"}   # must be chord tones


@dataclass
class Note:
    part: str
    pitch: int
    vel: float
    seg: "Seg"
    q: float
    dq: float
    role: str = "melody"
    art: str = ""             # s = staccato, S = very short, l = legato, h = hit (no jitter), r = let ring
    tag: str = ""
    voice: str = ""           # voice id for voice-leading checks ("part.k"); set by add/mel/pad
    t: float = 0.0
    d: float = 0.0
    q_abs_end: float = field(default=0.0, repr=False)


def _parse_dur(s):
    return float(Fraction(s))


class Seg:
    """A stretch of music in one meter whose bars exactly fill [t0, t1] (absolute seconds)."""

    def __init__(self, cue, t0, t1, bars, meter, scale, nominal=None, rit=0.0, rit_q=None, label=""):
        self.cue, self.score = cue, cue.score
        self.t0, self.t1 = float(t0), float(t1)
        self.meter = meter
        self.bar_q, self.beat_q = METERS[meter]
        self.bars = bars
        self.n_q = bars * self.bar_q
        self.scale = Scale(scale)
        self.label = label
        self.chords = []           # (q0, q1, Chord, local Scale or None)
        self.local_scales = []     # (q0, q1, Scale)
        res = 1 / 96
        grid = np.arange(0, self.n_q + res / 2, res)
        w = np.ones(len(grid) - 1)
        if rit:
            rq = rit_q or self.bar_q
            x = np.clip((grid[:-1] - (self.n_q - rq)) / rq, 0, 1)
            w *= 1 + rit * x ** 1.5
        cum = np.concatenate([[0.0], np.cumsum(w)])
        cum *= (self.t1 - self.t0) / cum[-1]
        self._grid, self._cum = grid, cum
        self.sec_per_q0 = cum[1] / grid[1]
        self.sec_per_q1 = (cum[-1] - cum[-2]) / (grid[-1] - grid[-2])
        self.tempo = 60.0 * self.n_q / (self.t1 - self.t0)
        self.nominal = nominal
        cue.segs.append(self)

    # --------------------------------------------------------------- time
    def t(self, q):
        if q < 0:
            return self.t0 + q * self.sec_per_q0
        if q > self.n_q:
            return self.t1 + (q - self.n_q) * self.sec_per_q1
        return self.t0 + float(np.interp(q, self._grid, self._cum))

    def q_of(self, t):
        """Inverse map (absolute seconds -> q)."""
        return float(np.interp(t - self.t0, self._cum, self._grid))

    def bar(self, i, beat=0.0):
        return i * self.bar_q + beat

    # --------------------------------------------------------------- harmony
    def prog(self, spec, q=0.0):
        pos = q
        for tok in spec.split():
            if tok == "|":
                assert abs(pos / self.bar_q - round(pos / self.bar_q)) < 1e-6, (self.label, spec, pos)
                continue
            body, _, sc = tok.partition("@")
            sym, d = body.rsplit(":", 1)
            d = _parse_dur(d)
            local = Scale(sc.replace("-", " ")) if sc else None
            self.chords.append((pos, pos + d, Chord(sym), local))
            pos += d
        assert pos <= self.n_q + 1e-6, (self.label, "progression longer than segment", pos, self.n_q)
        return pos

    def chord_at(self, q):
        for q0, q1, ch, _ in self.chords:
            if q0 - 1e-6 <= q < q1 - 1e-6:
                return ch
        if self.chords and q >= self.chords[-1][1] - 1e-6:
            return self.chords[-1][2]
        return None

    def scales_at(self, q):
        out = [self.scale]
        for q0, q1, ch, local in self.chords:
            if local is not None and q0 - 1e-6 <= q < q1 - 1e-6:
                out.append(local)
        for q0, q1, sc in self.local_scales:
            if q0 - 1e-6 <= q < q1 - 1e-6:
                out.append(sc)
        return out

    def chord_spans(self, q0=0.0, q1=None):
        q1 = self.n_q if q1 is None else q1
        return [(max(a, q0), min(b, q1), ch) for a, b, ch, _ in self.chords if b > q0 + 1e-6 and a < q1 - 1e-6]

    # --------------------------------------------------------------- notes
    def add(self, part, q, dq, pitch, vel, role="melody", art="", tag="", voice=None):
        if isinstance(pitch, str):
            pitch = midi(pitch)
        n = Note(part, int(pitch), float(vel), self, float(q), float(dq), role, art, tag,
                 voice=voice or f"{part}.0")
        self.score.notes.append(n)
        return n

    def mel(self, part, spec, q=0.0, vel=80, role="melody", art="", transpose=0, tag="", accent=10):
        """Parse 'F#5:1 E5:1/2 r:1/2 [D4,F#4]:3 | ...' (durations in quarter notes).

        Optional third field = flags: s staccato, S very short, a accent, p soft, l legato, h hit."""
        pos = q
        out = []
        for tok in spec.split():
            if tok == "|":
                assert abs(pos / self.bar_q - round(pos / self.bar_q)) < 1e-6, (self.label, part, spec, pos)
                continue
            fields = tok.split(":")
            p, d = fields[0], _parse_dur(fields[1])
            flags = (fields[2] if len(fields) > 2 else "") + art
            if p != "r":
                v = vel + (accent if "a" in flags else 0) - (14 if "p" in flags else 0)
                pitches = sorted(midi(nm) + transpose for nm in p.strip("[]").split(","))
                for k, pch in enumerate(pitches):
                    out.append(self.add(part, pos, d, pch, v, role, flags.replace("a", "").replace("p", ""),
                                        tag, voice=f"{part}.{k}"))
            pos += d
        return out

    def expr(self, parts, points):
        """Expression automation: points [(q, dB)] (0 dB = CC11 127)."""
        for p in ([parts] if isinstance(parts, str) else parts):
            for q, db in points:
                self.score.expr[p].append((self.t(q), float(db)))

    def sync(self, label, q, target_rel):
        """Record a hit point: musical position q should land at cue-relative time target_rel."""
        self.score.syncs.append((self.cue.id, label, self.cue.t0 + target_rel, self.t(q)))

    # --------------------------------------------------------------- generators
    def pad(self, parts, n, lo, hi, q0=0.0, q1=None, vel=60, role="pad", bass_part=None, bass_lo=28,
            bass_hi=52, tops=None, center=None, prev=None, tie=True, art="", bass_vel=None, bass_ref=None,
            family=None, link=True):
        """Voice-led sustained chords.  parts: one part for all voices or a list (bottom -> top).

        bass_ref=(lo, hi): another part plays the bass there; use it for chord coverage and
        parallel-motion checks without writing bass notes.
        Continuity: unless prev= is given, the last voicing of the same instrument family (strings,
        tremolo strings, choir, brass, ...) is used as prev when it ended where this one starts,
        so voice-leading (and parallel checks against the bass) also run across segment and cue
        boundaries."""
        spans = self.chord_spans(q0, q1)
        chords = [c for _, _, c in spans]
        if bass_part or bass_ref:
            blo, bhi = (bass_lo, bass_hi) if bass_part else bass_ref
            basses = [c.bass_note(blo, bhi) for c in chords]
        else:
            basses = None
        plist = list(parts) if isinstance(parts, (list, tuple)) else [parts] * n
        fam = family or _family(plist)
        vids, seen = [], Counter()
        for pt in plist:
            vids.append(f"{pt}.{seen[pt]}")
            seen[pt] += 1
        prev_bass = None
        if prev is None and link:
            last = self.score.last_voicing.get(fam)
            if last is not None and abs(last[0] - self.t(spans[0][0])) < 0.35 and len(last[1]) >= n:
                prev, prev_bass = tuple(sorted(last[1])[:n]), last[2]      # lowest voices continue
        own = set(vids) | ({f"{bass_part}.0"} if bass_part else set())
        guides = self.score.guides_at([self.t(a) for a, _, _ in spans], own)
        vs = voice_lead(chords, n, lo, hi, basses=basses, center=center, prev=prev, tops=tops,
                        prev_bass=prev_bass, guides=guides)
        self.score.voicings.append((f"{self.label}:{'/'.join(plist)}", [c.sym for c in chords], vs, basses))
        self.score.last_voicing[fam] = (self.t(spans[-1][1]), vs[-1], basses[-1] if basses else None)
        notes = []
        for v in range(n):
            cur = None
            for (a, b, _), voicing in zip(spans, vs):
                p = voicing[v]
                if tie and cur is not None and cur.pitch == p and abs(cur.q + cur.dq - a) < 1e-6:
                    cur.dq = b - cur.q
                    continue
                cur = self.add(plist[v], a, b - a, p, vel, role, art, voice=vids[v])
                notes.append(cur)
        if bass_part:
            cur = None
            for (a, b, _), p in zip(spans, basses):
                if tie and cur is not None and cur.pitch == p and abs(cur.q + cur.dq - a) < 1e-6:
                    cur.dq = b - cur.q
                    continue
                cur = self.add(bass_part, a, b - a, p, bass_vel or vel, "bass", art)
        return vs


_FAMILIES = [("str", {"vla", "vln1", "vln2", "vc"}), ("trem", {"trem_hi", "trem_va", "trem_lo"}),
             ("brass", {"tbn", "brass", "horn", "tuba"})]


def _family(plist):
    for fam, members in _FAMILIES:
        if set(plist) <= members:
            return fam
    return plist[0]


class Cue:
    def __init__(self, score, scene, t1):
        self.score = score
        self.scene = scene
        self.id = scene["id"]
        self.mood = scene["mood"]
        self.t0 = float(scene["start"])
        self.t1 = float(t1)
        self.dur = self.t1 - self.t0
        self.lines = [(float(l["start"]), float(l["end"])) for l in scene["lines"]]
        self.segs = []
        score.cues.append(self)

    def seg(self, r0, r1, bars, meter, scale, **kw):
        return Seg(self, self.t0 + r0, self.t0 + r1, bars, meter, scale, **kw)

    def ls(self, i):
        return self.lines[i][0]

    def le(self, i):
        return self.lines[i][1]

    def gap(self, i):
        """Middle of the pause before line i (cue-relative): where musical changes should land."""
        return (self.lines[i - 1][1] + self.lines[i][0]) / 2 if i > 0 else self.lines[0][0] / 2

    def pauses(self, min_len=0.22):
        """Pauses between consecutive lines of this cue: [(start, end)] cue-relative."""
        return [(a[1], b[0]) for a, b in zip(self.lines, self.lines[1:]) if b[0] - a[1] >= min_len]

    def pause_or_gap(self, i, min_len=0.25):
        """The pause before line i (cue-relative (start, end)); if it is shorter than min_len, a
        min_len window centred on it (fills then overlap the line edges slightly instead of
        crashing when narration pauses are tightened)."""
        if i <= 0:
            a, b = max(0.0, self.lines[0][0] - min_len), self.lines[0][0]
        else:
            a, b = self.lines[i - 1][1], self.lines[i][0]
        if b - a >= min_len:
            return a, b
        m = (a + b) / 2
        return m - min_len / 2, m + min_len / 2


class Score:
    def __init__(self, timeline):
        self.tl = timeline
        self.duration = float(timeline["duration"])
        self.notes = []
        self.cues = []
        self.expr = defaultdict(list)
        self.syncs = []
        self.voicings = []         # (label, chord symbols, voicings, bass pitches) from Seg.pad
        self.last_voicing = {}     # family -> (end time s, last voicing, last bass) for pad continuity
        self.guide_notes = None    # voice -> [(t0, t1, pitch, role)] from a previous build pass
        self.speech_iv = []
        for s in timeline["scenes"]:
            for ln in s["lines"]:
                self.speech_iv.append((s["start"] + ln["start"], s["start"] + ln["end"]))
        self.speech_iv.sort()
        # phrases: lines separated by less than MERGE_GAP s count as one stretch of speech, so the
        # music does not pump in every short breath between lines
        self.phrases = []
        for a, b in self.speech_iv:
            if self.phrases and a - self.phrases[-1][1] < self.MERGE_GAP:
                self.phrases[-1][1] = max(self.phrases[-1][1], b)
            else:
                self.phrases.append([a, b])

    def guides_at(self, times, own):
        """For each time: [(pitch before, pitch at, fifths_only)] of the other voices of the previous
        build pass that have an onset exactly there (and were sounding just before)."""
        out = [[] for _ in times]
        if not self.guide_notes:
            return out
        import bisect
        for vid, (onsets, lst) in self.guide_notes.items():
            if vid in own:
                continue
            for k, tk in enumerate(times):
                i = bisect.bisect_left(onsets, tk - 2e-3)
                if i >= len(lst) or abs(lst[i][0] - tk) >= 2e-3 or i == 0:
                    continue
                at, before = lst[i], lst[i - 1]
                if before[1] < tk - 0.15:
                    continue
                out[k].append((before[2], at[2], at[3] == "pad" and before[3] == "pad"))
        return out

    def guide_index(self, roles=("melody", "counter", "pad", "bass", "harmony")):
        idx = defaultdict(list)
        for n in self.notes:
            if PARTS[n.part].drum or n.role not in roles:
                continue
            idx[n.voice].append((n.seg.t(n.q), n.seg.t(n.q + n.dq), n.pitch, n.role))
        out = {}
        for vid, lst in idx.items():
            lst.sort()
            out[vid] = ([x[0] for x in lst], lst)
        return out

    MERGE_GAP = 0.5
    ATTACK = 0.35
    RELEASE = 0.7

    def speech(self, t):
        """Narration activity 0..1 over merged phrases: a smooth 0.35 s rise that reaches 1 as the
        first line starts, a 0.7 s release after the last one (used for ducking and softening)."""
        t = np.asarray(t, float)
        out = np.zeros_like(t)
        for a, b in self.phrases:
            up = np.clip((t - (a - self.ATTACK)) / self.ATTACK, 0, 1)
            dn = np.clip(((b + self.RELEASE) - t) / self.RELEASE, 0, 1)
            x = np.minimum(up, dn)
            out = np.maximum(out, x * x * (3 - 2 * x))
        return out

    def speaking(self, t):
        """True while a line is actually being spoken (no merging, no ramps) -- for analysis."""
        t = np.asarray(t, float)
        out = np.zeros(t.shape, bool)
        for a, b in self.speech_iv:
            out |= (t >= a) & (t < b)
        return out

    # --------------------------------------------------------------- performance
    def perform(self, seed=7):
        """Resolve q -> seconds, apply articulation, humanisation, attack compensation."""
        rng = np.random.default_rng(seed)
        self.notes.sort(key=lambda n: (n.seg.t(n.q), n.part, n.pitch))
        groups = defaultdict(list)
        for n in self.notes:
            groups[(n.part, id(n.seg))].append(n.pitch)
        contour = {k: float(np.median(v)) for k, v in groups.items()}
        for n in self.notes:
            p = PARTS[n.part]
            t_on = n.seg.t(n.q)
            t_off = n.seg.t(n.q + n.dq)
            d = t_off - t_on
            if "S" in n.art:
                d = min(d * 0.3, 0.09)
            elif "s" in n.art:
                d = min(d * 0.5, 0.22)
            elif "r" in n.art:
                d = d + 0.6
            else:
                d = d + p.legato + (0.04 if "l" in n.art else 0.0)
            jit = 0.0 if "h" in n.art else float(np.clip(rng.normal(0, p.jitter), -2.5 * p.jitter, 2.5 * p.jitter))
            t_on = t_on + jit - p.attack
            if t_on < 0:
                d += t_on
                t_on = 0.0
            n.t, n.d = t_on, max(0.03, d)
            # velocity humanisation and gentle speech-aware softening of foreground parts
            v = n.vel + rng.normal(0, 3.0)
            pos = n.q % n.seg.bar_q
            if abs(pos) < 1e-6:
                v += 4.0
            elif abs(pos % n.seg.beat_q) < 1e-6:
                v += 1.5
            if n.role in ("melody", "counter"):
                v += 0.6 * (n.pitch - contour[(n.part, id(n.seg))])      # higher notes lean forward
            if n.role in ("melody", "counter", "arp", "gliss", "fx"):
                v -= 4.0 * float(self.speech(n.seg.t(n.q)))
            n.vel = float(np.clip(v, 12, 127))
        # avoid overlapping identical pitches in the same part (re-trigger cleanly)
        by = defaultdict(list)
        for n in self.notes:
            by[(n.part, n.pitch)].append(n)
        for lst in by.values():
            lst.sort(key=lambda n: n.t)
            for a, b in zip(lst, lst[1:]):
                if a.t + a.d > b.t - 0.012:
                    a.d = max(0.03, b.t - 0.012 - a.t)

    def expression_curve(self, part, t):
        pts = sorted(self.expr.get(part, []))
        if pts:
            ts, dbs = zip(*pts)
            db = np.interp(t, ts, dbs)
        else:
            db = np.full_like(t, -3.0)
        db = db - PARTS[part].duck_db * self.speech(t)
        return np.minimum(db, 0.0)

    # --------------------------------------------------------------- MIDI
    def write_midis(self, out_dir):
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        buses = defaultdict(list)
        for n in self.notes:
            buses[PARTS[n.part].bus].append(n)
        paths = {}
        for bus, notes in buses.items():
            paths[bus] = out_dir / f"music_{bus}.mid"
            self._write_bus(notes, paths[bus])
        return paths

    def _write_bus(self, notes, path):
        parts = sorted({n.part for n in notes}, key=lambda p: min(n.t for n in notes if n.part == p))
        chans, nxt = {}, 0
        for p in parts:
            if PARTS[p].drum:
                chans[p] = 9
                continue
            if nxt == 9:
                nxt += 1
            assert nxt < 16, f"too many parts on one bus: {parts}"
            chans[p] = nxt
            nxt += 1
        ev = []   # (tick, order, msg)
        tk = lambda t: int(round(t * TICKS_PER_S))
        for p in parts:
            pd, ch = PARTS[p], chans[p]
            if not pd.drum:
                ev.append((0, 0, mido.Message("control_change", channel=ch, control=0, value=pd.bank)))
            ev.append((0, 1, mido.Message("program_change", channel=ch, program=pd.prog)))
            vol = int(np.clip(round(127 * 10 ** (pd.gain_db / 40)), 1, 127))
            ev.append((0, 2, mido.Message("control_change", channel=ch, control=7, value=vol)))
            ev.append((0, 2, mido.Message("control_change", channel=ch, control=10,
                                          value=int(np.clip(round(64 + 63 * pd.pan), 0, 127)))))
            ev.append((0, 2, mido.Message("control_change", channel=ch, control=91, value=0)))
            ev.append((0, 2, mido.Message("control_change", channel=ch, control=93, value=0)))
            pn = [n for n in notes if n.part == p]
            t_a = max(0.0, min(n.t for n in pn) - 0.5)
            t_b = max(n.t + n.d for n in pn) + 2.0
            ts = np.arange(t_a, t_b, 0.02)
            cc = np.clip(np.round(127 * 10 ** (self.expression_curve(p, ts) / 40)), 1, 127).astype(int)
            last = None
            for t, v in zip(ts, cc):
                if last is None or abs(v - last) >= 1:
                    ev.append((tk(t), 1, mido.Message("control_change", channel=ch, control=11, value=int(v))))
                    last = v
            for n in pn:
                vel = int(np.clip(round(n.vel), 1, 127))
                ev.append((tk(n.t), 2, mido.Message("note_on", channel=ch, note=n.pitch, velocity=vel)))
                ev.append((tk(n.t + n.d), 0, mido.Message("note_off", channel=ch, note=n.pitch, velocity=0)))
        ev.append((tk(self.duration + 4.0), 3, mido.Message("control_change", channel=0, control=11, value=1)))
        ev.sort(key=lambda e: (e[0], e[1]))
        mid = mido.MidiFile(ticks_per_beat=PPQ)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        tr.append(mido.MetaMessage("set_tempo", tempo=TEMPO_US, time=0))
        last = 0
        for t, _, m in ev:
            m.time = t - last
            last = t
            tr.append(m)
        mid.save(path)


def fluidsynth_render(mid_paths, out_dir, gain=0.5):
    """Render each MIDI file to a float WAV in parallel. Returns {key: wav_path}."""
    procs, outs = [], {}
    for key, mp in mid_paths.items():
        wav = Path(out_dir) / f"{Path(mp).stem}.wav"
        outs[key] = wav
        cmd = ["fluidsynth", "-ni", "-q", "-R", "0", "-C", "0", "-g", str(gain), "-r", str(SR),
               "-O", "float", "-T", "wav", "-o", "synth.polyphony=1024", "-F", str(wav), SOUNDFONT, str(mp)]
        procs.append((key, subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)))
    for key, pr in procs:
        _, err = pr.communicate()
        if pr.returncode != 0 or not outs[key].exists():
            raise RuntimeError(f"fluidsynth failed for {key}: {err.decode()[-500:]}")
    return outs
