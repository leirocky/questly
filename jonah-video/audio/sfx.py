"""Procedural sound-effect library for 约拿的故事: every sound is synthesised from code (no samples).

API (used by audio/mix.py, keep exactly):

    make(name, dur, sr=48000, seed=0, **params) -> np.float32 array, shape (n, 2)
    NAMES = {name: (kind, default_dur_seconds, description)}       kind: 'loop' | 'oneshot'

Loops      ``dur`` is required (0.5 s .. 40 s+; ``None`` falls back to the default). The result is a seamless
           circular loop: every component is periodic in ``dur`` (periodic random LFOs, events wrapped around the
           end, reverb tails folded back to the start, noise beds cross-faded at the seam), and the loop is rotated
           so it starts and ends on a quiet near-zero sample, so there is no click at either end or at the seam.
           Integrated loudness is LOOP_LUFS[name] (about -25..-20 LUFS), measured on the render itself. For
           renders shorter than REF_DUR the gain is additionally held within LOOP_CLAMP[name] dB of the gain a
           REF_DUR render of the same seed needs, so a short sparse loop (one creak, one snore) is not boosted
           wildly while dense beds (waves, wind, rain) simply follow their own content.
One-shots  ``dur=None`` gives the natural length (NAMES default); generators render their decay/reverb tail in
           full and it is then fitted into the natural length with a smooth exponential end fade (END_FADE).
           A given ``dur`` trims (15 ms fade) or pads with silence; a negative ``dur`` gives an empty array.
           Level: the loudest 400 ms window (momentary max, BS.1770) is ONESHOT_LUFS[name] (about -14 LUFS),
           with sample peak kept inside PEAK_RANGE (0.5..0.7); transient-heavy sounds get a gentle look-ahead
           limiter (at most ONESHOT_LIMIT[name] dB) so they can reach that loudness within the peak ceiling.
           Mostly centred.
Stereo     Event pans are stratified (alternating / spread slots) and every render is rebalanced so the L/R
           energy differs by at most BALANCE_DB.

Deterministic for (name, dur, sr, seed, params); different seeds give different variations. Unknown names raise
ValueError. Unknown params are ignored with a warning; supported params are listed in PARAMS (every effect also
accepts ``width``: stereo width multiplier, 1 = as designed, 0 = mono) and clamped to PARAM_RANGE.

Character: a soft, warm children's picture book (cartoony for gulp, spit, snore, pop and the oars' plunks), never
harsh. Everything is high-passed at 35 Hz and gently low-passed where the material allows; low thumps (heartbeat,
thud) carry saturated harmonics and a 250-600 Hz knock so they survive phone-sized speakers.

Verify with ``python3 tools/sfx_audition.py`` (WAVs, spectrogram grid, level / seam report).
"""
import warnings
import zlib

import numpy as np
from scipy import ndimage, signal
from scipy.interpolate import CubicSpline

TAU = 2 * np.pi
REF_DUR = 8.0          # loops shorter than this are levelled against a render of this length

NAMES = {
    # ---- loops (dur always given)
    "waves_calm": ("loop", 16.0, "gentle lapping sea, soft surf swells every few seconds"),
    "waves_storm": ("loop", 16.0, "heavy crashing waves over a deep roar"),
    "storm_wind": ("loop", 16.0, "howling, gusting storm wind with soft whistles"),
    "rain": ("loop", 12.0, "heavy rain hiss with droplet texture"),
    "wind_soft": ("loop", 16.0, "light breeze with a little leaf rustle"),
    "wind_hot": ("loop", 16.0, "dry gusty desert wind with sand hiss"),
    "ship_creak": ("loop", 16.0, "wooden hull creaks, rope groans and knocks, irregular"),
    "underwater": ("loop", 16.0, "muffled low underwater ambience with distant rumble"),
    "bubbles": ("loop", 12.0, "bubble bloops in small rising clusters"),
    "heartbeat": ("loop", 12.0, "slow deep soft lub-dub inside the great fish, ~50 bpm"),
    "drip": ("loop", 16.0, "cave-like water drips with echo"),
    "footsteps": ("loop", 8.0, "walking on dirt, ~2 steps/s"),
    "footsteps_run": ("loop", 6.0, "running on dirt, ~4 steps/s"),
    "crowd": ("loop", 16.0, "distant murmuring market crowd, no intelligible words"),
    "birds": ("loop", 16.0, "sparse songbird chirps"),
    "snore": ("loop", 10.5, "cartoon snore: inhale rasp + whistling exhale, ~3.5 s cycle"),
    "heat": ("loop", 16.0, "soft cicada-like heat buzz"),
    "oars": ("loop", 14.0, "rowing: oar dip/splash, pull swirl and wooden oarlock creak, ~1 stroke per 1.4 s"),
    "fire": ("loop", 16.0, "small altar fire: soft crackle and gentle flame whoosh"),
    "night": ("loop", 16.0, "soft crickets and a faint night breeze, very calm"),
    "cheer": ("loop", 16.0, "joyful distant crowd: happy voices swelling up, a few claps, no intelligible words"),
    # ---- one-shots (dur=None -> natural length)
    "thunder": ("oneshot", 3.6, "crack + long deep rolling rumble, not ear-splitting"),
    "splash": ("oneshot", 1.5, "big body splash with falling droplets"),
    "splash_small": ("oneshot", 0.9, "crate plopping into water"),
    "whoosh": ("oneshot", 1.0, "soft swish (~0.7 s) + a breath of air"),
    "gulp": ("oneshot", 1.1, "big cartoon gulp: low sweep + wet pop"),
    "spit": ("oneshot", 0.85, "cartoon 'ptooey': big bloop expelling + wet splatter"),
    "thud": ("oneshot", 0.45, "soft landing on sand"),
    "chime": ("oneshot", 2.6, "warm divine shimmer: celesta major chord + airy sparkle"),
    "sparkle": ("oneshot", 1.2, "magical glitter"),
    "grow": ("oneshot", 2.1, "rising magical sweep with twinkles, blooming into a bell"),
    "wither": ("oneshot", 2.0, "descending dry rustle / deflate"),
    "crunch": ("oneshot", 1.5, "small nibbling crunches"),
    "gull": ("oneshot", 1.5, "seagull calls"),
    "lots": ("oneshot", 1.5, "wooden sticks rattling in a jar, then one dropping"),
    "cloth": ("oneshot", 0.9, "fabric rustle"),
    "sheep": ("oneshot", 1.1, "gentle sheep 'baa'"),
    "pop": ("oneshot", 0.35, "light pop"),
    "coins": ("oneshot", 0.8, "a few small coins clinking into a hand"),
    "horn": ("oneshot", 2.2, "herald's ram's horn (shofar) call: three warm brassy notes, not shrill"),
    "hammer": ("oneshot", 1.5, "a few wooden mallet knocks on a stake / pole, small wood resonance"),
    "rooster": ("oneshot", 1.7, "gentle, friendly rooster crow at dawn (~1.1 s cock-a-doodle-doo + soft tail)"),
}

LOOP_LUFS = {
    "waves_calm": -22.0, "waves_storm": -20.5, "storm_wind": -21.0, "rain": -22.0, "wind_soft": -23.5,
    "wind_hot": -22.0, "ship_creak": -23.0, "underwater": -22.5, "bubbles": -23.0, "heartbeat": -22.0,
    "drip": -23.0, "footsteps": -22.0, "footsteps_run": -21.5, "crowd": -23.0, "birds": -23.0, "snore": -22.0,
    "heat": -25.0,          # 2.5-4 kHz is where (children's) ears are most sensitive: a little lower on purpose
    "oars": -22.5, "fire": -23.0, "cheer": -22.0,
    "night": -24.0,         # very calm; the crickets sit in the sensitive 3-4 kHz band too
}

# Short renders (< REF_DUR): allowed deviation (cut dB, boost dB) of the self-measured gain from the gain of a
# REF_DUR render of the same seed. Dense beds follow their own content; sparse event loops are held close.
_DENSE = (12.0, 12.0)
_SPARSE = (6.0, 4.0)
LOOP_CLAMP = {
    "waves_calm": _DENSE, "waves_storm": _DENSE, "storm_wind": _DENSE, "rain": _DENSE, "wind_soft": _DENSE,
    "wind_hot": _DENSE, "underwater": _DENSE, "crowd": _DENSE, "heat": _DENSE, "heartbeat": _DENSE,
    "footsteps": _DENSE, "footsteps_run": _DENSE, "snore": _DENSE,
    "oars": _DENSE, "fire": _DENSE, "night": _DENSE, "cheer": _DENSE,
    "ship_creak": _SPARSE, "bubbles": _SPARSE, "drip": _SPARSE, "birds": _SPARSE,
}

# One-shot level: momentary-max loudness target (loudest 400 ms window, LUFS) and the allowed sample-peak range.
ONESHOT_LUFS = {k: -14.0 for k, v in NAMES.items() if v[0] == "oneshot"}
PEAK_RANGE = (0.5, 0.7)
# Max gain reduction (dB) of the transient limiter used to reach ONESHOT_LUFS within the peak ceiling.
ONESHOT_LIMIT = {k: 3.0 for k in ONESHOT_LUFS}
ONESHOT_LIMIT.update({"thud": 8.0, "pop": 5.0, "crunch": 6.0, "lots": 6.0, "splash_small": 5.0, "cloth": 4.0,
                      "spit": 4.0, "splash": 4.0, "coins": 5.0, "hammer": 6.0})
BALANCE_DB = 1.0         # max L/R energy difference after rebalancing
# Length (s) of the exponential end fade that fits a one-shot's rendered tail into its natural length.
END_FADE = {k: min(0.25, 0.3 * NAMES[k][1]) for k in ONESHOT_LUFS}


# Optional per-effect params and their defaults (``width`` is accepted everywhere).
PARAMS = {
    "waves_calm": {"density": 1.0}, "waves_storm": {"density": 1.0}, "rain": {"density": 1.0},
    "ship_creak": {"density": 1.0}, "bubbles": {"density": 1.0}, "drip": {"density": 1.0},
    "crowd": {"density": 1.0}, "birds": {"density": 1.0},
    "heartbeat": {"bpm": 50.0}, "footsteps": {"rate": 2.0}, "footsteps_run": {"rate": 4.0},
    "snore": {"cycle": 3.5}, "oars": {"cycle": 1.4},
    "fire": {"density": 1.0}, "night": {"density": 1.0}, "cheer": {"density": 1.0},
    "chime": {"root": 72}, "sparkle": {"root": 79}, "grow": {"root": 67},
    "sheep": {"pitch": 1.0}, "gull": {"pitch": 1.0, "calls": None},
    "horn": {"pitch": 1.0}, "rooster": {"pitch": 1.0},
}
# Numeric params are clamped into these ranges (0 / negative values would divide by zero or make no sense).
PARAM_RANGE = {"density": (0.05, 8.0), "bpm": (20.0, 200.0), "rate": (0.5, 8.0), "cycle": (0.5, 20.0),
               "root": (36.0, 96.0), "pitch": (0.25, 4.0), "calls": (0, 6), "width": (0.0, 2.0)}

# Final filtering per effect: (high-pass Hz, low-pass Hz or None).
_FINISH = {
    "waves_calm": (35, 9000), "waves_storm": (40, 6500), "storm_wind": (35, 7500), "rain": (35, 8500),
    "wind_soft": (35, 7000), "wind_hot": (35, 7000), "ship_creak": (40, 4500), "underwater": (40, 2500),
    "bubbles": (35, 5000), "heartbeat": (45, 1500), "drip": (35, 6000), "footsteps": (35, 7000),
    "footsteps_run": (35, 7000), "crowd": (35, 4000), "birds": (35, 7000), "snore": (35, 4500),
    "heat": (35, 5000), "oars": (35, 7000), "fire": (40, 6500), "night": (35, 6000), "cheer": (40, 5000),
    "thunder": (40, 5000), "splash": (35, 8000), "splash_small": (35, 8000), "whoosh": (35, 7000),
    "gulp": (35, 6000), "spit": (35, 7000), "thud": (40, 6000), "chime": (35, 10000), "sparkle": (35, 8000),
    "grow": (35, 9000), "wither": (35, 7500), "crunch": (35, 7000), "gull": (35, 6500), "lots": (35, 8000),
    "cloth": (35, 7000), "sheep": (35, 6000), "pop": (35, 8000),
    "coins": (35, 7500), "horn": (40, 4500), "hammer": (40, 7000), "rooster": (35, 5000),
}

_DEBUG = None      # tools/sfx_audition.py --debug sets a list here to collect component levels (strings)


def _dbg(label, x):
    if _DEBUG is not None:
        x = np.asarray(x, float)
        rms = np.sqrt(np.mean(x ** 2)) if x.size else 0.0
        pk = np.abs(x).max() if x.size else 0.0
        _DEBUG.append(f"[{label:<16}] rms {20 * np.log10(rms + 1e-12):6.1f} dB  "
                      f"peak {20 * np.log10(pk + 1e-12):6.1f} dB"
                      "  (pre-normalisation)")


def _dbg_vs(label, layer, bed, lo, hi, sr, win=0.05, top=0.05):
    """--debug: band-limited level of a detail layer against the bed in the layer's loudest 50 ms windows."""
    if _DEBUG is None:
        return

    def lev(x):
        x = _stereo(x).mean(axis=1)
        y = _fft_shape(x, sr, lambda f: _bpm(f, lo, hi, 4))
        k = int(win * sr)
        nw = len(y) // k
        return 10 * np.log10(np.mean(y[:nw * k].reshape(nw, k) ** 2, axis=1) + 1e-20)

    a, b = lev(layer), lev(bed)
    sel = np.argsort(a)[-max(1, int(top * len(a))):]
    d = a[sel] - b[sel]
    _DEBUG.append(f"[{label:<16}] {lo}-{hi} Hz, loudest {100 * top:.0f}% of 50 ms windows: layer - bed "
                  f"median {np.median(d):+5.1f} dB, max {d.max():+5.1f} dB")


# =========================================================================================== public entry point
def make(name, dur, sr=48000, seed=0, **params):
    """Synthesise sound effect ``name``; returns float32 (n, 2). See module docstring."""
    if name not in NAMES:
        raise ValueError(f"unknown sound effect {name!r}; known: {', '.join(sorted(NAMES))}")
    kind, default, _ = NAMES[name]
    sr = int(sr)
    allowed = set(PARAMS.get(name, {})) | {"width"}
    unknown = sorted(set(params) - allowed)
    if unknown:
        warnings.warn(f"sfx {name!r}: ignoring unknown params {unknown} (supported: {sorted(allowed)})",
                      stacklevel=2)
    p = {"width": 1.0, **PARAMS.get(name, {})}
    p.update({k: v for k, v in params.items() if k in allowed and v is not None})
    for k, (lo, hi) in PARAM_RANGE.items():
        if k in p and p[k] is not None:
            p[k] = type(lo)(min(max(float(p[k]), lo), hi))
    if kind == "loop":
        T = float(default if dur is None else dur)
        n = int(round(T * sr))
        if n <= 0:
            return np.zeros((0, 2), np.float32)
        x = _render_loop(name, n, sr, seed, p)
    else:
        x = _render_oneshot(name, sr, seed, p)
        if dur is not None:
            x = _fit_len(x, max(0, int(round(float(dur) * sr))), sr)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    return np.ascontiguousarray(x, dtype=np.float32)


def _render_loop(name, n, sr, seed, p):
    m = max(n, int(0.25 * sr))
    x = _rotate_quiet(_balance(_loop_core(name, m, sr, seed, p)), sr)
    target = LOOP_LUFS[name]
    g = target - _lufs(_tile(x, sr), sr)
    nref = int(round(REF_DUR * sr))
    if m < nref:
        g_ref = target - _lufs(_balance(_loop_core(name, nref, sr, seed, p)), sr)
        if np.isfinite(g_ref):
            cut, boost = LOOP_CLAMP[name]
            g = float(np.clip(g, g_ref - cut, g_ref + boost)) if np.isfinite(g) else g_ref
    if np.isfinite(g):
        x = x * 10 ** (g / 20)
    x = _softknee(x, 0.7, 0.9)             # only touches rare transient peaks (footsteps, creaks)
    if m != n:                    # below the documented range: cut and fade (not seamless)
        x = _fade(x[:n], sr, 0.004, 0.004)
    return x


def _tile(x, sr, T=0.6):
    """A loop shorter than T seconds repeated (it is circular) so it can be loudness-measured."""
    k = int(np.ceil(T * sr / max(len(x), 1)))
    return np.tile(x, (k, 1)) if k > 1 else x


def _loop_core(name, n, sr, seed, p):
    rng = _rng(name, seed)
    x = _stereo(_LOOPS[name](rng, n, sr, p))
    hp, lp = _FINISH[name]
    x = _fft_shape(x, sr, lambda f: _hpm(f, hp, 4) * (_lpm(f, lp, 2) if lp else 1.0))
    return _width(x, p["width"])


def _render_oneshot(name, sr, seed, p):
    rng = _rng(name, seed)
    x = _stereo(_ONESHOTS[name](rng, sr, p))          # may run past the natural length (decay / reverb tail)
    hp, lp = _FINISH[name]
    x = _filt(x, "hp", hp, sr, 4)
    if lp:
        x = _filt(x, "lp", lp, sr, 2)
    x = _width(x, p["width"])
    L = int(round(NAMES[name][1] * sr))
    x = _fit_len(x, L, sr, fade=END_FADE[name], curve="exp")
    x = _balance(_fade(x, sr, 0.002, 0.0))
    return _level_oneshot(x, sr, ONESHOT_LUFS[name], ONESHOT_LIMIT[name])


def _level_oneshot(x, sr, target, max_gr):
    """Gain to the momentary-max target; transient limiting (<= max_gr dB) if the peak ceiling is in the way."""
    lo, hi = PEAK_RANGE
    pk = np.abs(x).max()
    if pk <= 0:
        return x
    floor = pk * 10 ** (-max_gr / 20)
    for _ in range(3):
        g = 10 ** ((target - _mom_max(x, sr)) / 20)
        if g * pk <= hi * 1.001 or pk <= floor * 1.01:
            break
        x = _limit(x, max(hi / g, floor), sr)
        pk = np.abs(x).max()
    g = 10 ** ((target - _mom_max(x, sr)) / 20)
    return x * float(np.clip(g, lo / pk, hi / pk))


# =========================================================================================== small helpers
def _rng(name, seed):
    return np.random.default_rng([zlib.crc32(name.encode()), int(seed) & 0xFFFFFFFF])


def _stereo(x):
    x = np.asarray(x, float)
    return np.stack([x, x], 1) if x.ndim == 1 else x[:, :2]


def _width(x, w):
    if w == 1.0:
        return x
    mid, side = (x[:, 0] + x[:, 1]) / 2, (x[:, 0] - x[:, 1]) / 2 * w
    return np.stack([mid + side, mid - side], 1)


def _pan(p):
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    return np.array([np.cos(a), np.sin(a)]) * np.sqrt(2)


def _fade(x, sr, fi, fo):
    x = x.copy()
    for sec, sl in ((fi, 1), (fo, -1)):
        k = min(len(x), int(sec * sr))
        if k > 1:
            r = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
            if sl == 1:
                x[:k] *= r[:, None] if x.ndim == 2 else r
            else:
                x[-k:] *= r[::-1, None] if x.ndim == 2 else r[::-1]
    return x


def _fit_len(x, m, sr, fade=0.015, curve="cos"):
    """Trim to m samples (end fade) or pad with silence. curve='exp': (1-u)*exp(-4u) end fade, which steepens a
    ringing tail the way a damper would instead of chopping it."""
    m = max(0, int(m))
    if len(x) < m:
        return np.concatenate([x, np.zeros((m - len(x),) + x.shape[1:], x.dtype)])
    if curve != "exp":
        return _fade(x[:m], sr, 0.0, min(fade, m / sr / 4))
    y = x[:m].copy()
    k = min(m, int(fade * sr))
    if k > 1:
        u = np.arange(k) / (k - 1)
        g = (1 - u) * np.exp(-4 * u)
        y[-k:] *= g[:, None] if y.ndim == 2 else g
    return y


# ---- loudness (ITU-R BS.1770 / EBU R128; matches pyloudnorm's integrated loudness)
_KW = {}


def _kweight(x, sr):
    if sr not in _KW:
        import pyloudnorm as pyln
        _KW[sr] = [(f.b, f.a) for f in pyln.Meter(sr)._filters.values()]
    y = np.asarray(x, np.float64)
    for b, a in _KW[sr]:
        y = signal.lfilter(b, a, y, axis=0)
    return y


def _block_power(x, sr, block=0.4, hop=0.1):
    """Channel-summed mean square of K-weighted x in blocks of ``block`` s every ``hop`` s (block layout as in
    pyloudnorm, including its partial last block, so both meters agree)."""
    y = _stereo(_kweight(x, sr))
    n = len(y)
    e = np.concatenate([[0.0], np.cumsum(np.sum(y ** 2, axis=1))])
    B = block * sr
    if n < B:
        return np.array([e[-1] / B])
    nb = int(np.round((n / sr - block) / hop)) + 1
    j = np.arange(nb)
    lo = np.minimum((block * (j * hop / block) * sr).astype(int), n)
    hi = np.minimum((block * (j * hop / block + 1) * sr).astype(int), n)
    return (e[hi] - e[lo]) / B


def _lufs(x, sr):
    """Integrated loudness (gated) in LUFS; NaN for silence / too short."""
    if len(x) < int(0.4 * sr):
        return float("nan")
    z = _block_power(x, sr)
    with np.errstate(divide="ignore"):
        lk = -0.691 + 10 * np.log10(z)
    z = z[lk >= -70.0]
    if not len(z):
        return float("nan")
    rel = -0.691 + 10 * np.log10(np.mean(z)) - 10.0
    with np.errstate(divide="ignore"):
        z = z[-0.691 + 10 * np.log10(z) > rel]
    return float(-0.691 + 10 * np.log10(np.mean(z))) if len(z) else float("nan")


def _mom_max(x, sr):
    """Loudest 400 ms window (momentary loudness, 10 ms hop), LUFS; shorter sounds count as zero-padded."""
    z = _block_power(x, sr, 0.4, 0.01)
    return float(-0.691 + 10 * np.log10(np.max(z) + 1e-20))


def _limit(x, ceil, sr, look=0.004, rel=0.025):
    """Smooth look-ahead peak limiter: gain dips start ``look`` s before a peak, are Hann-smoothed (no hard edges)
    and release over ``rel`` s; the result's peaks stay <= ceil (up to the 4th-order smoothing tolerance)."""
    a = np.max(np.abs(x), axis=1)
    g0 = np.minimum(1.0, ceil / np.maximum(a, 1e-12))
    W = max(1, int(look * sr))
    g1 = ndimage.minimum_filter1d(g0, 2 * W + 1)
    k = np.exp(-1 / (rel * sr))
    g2 = np.minimum(g1, signal.lfilter([1 - k], [1, -k], g1, zi=[g1[0] * k])[0])
    w = np.hanning(2 * W + 3)[1:-1]
    g3 = np.convolve(g2, w / w.sum(), mode="same")
    y = x * g3[:, None]
    over = np.abs(y).max() / ceil
    return y / over if over > 1 else y


def _balance(x, max_db=None):
    """Rebalance L/R so their energies differ by at most max_db (keeps total energy)."""
    max_db = BALANCE_DB if max_db is None else max_db
    eL, eR = np.mean(x[:, 0] ** 2), np.mean(x[:, 1] ** 2)
    if eL <= 0 or eR <= 0:
        return x
    d = 10 * np.log10(eL / eR)
    if abs(d) <= max_db:
        return x
    e = (abs(d) - max_db) * np.sign(d)
    return x * np.array([10 ** (-e / 40), 10 ** (e / 40)])[None, :]


def _spread(rng, k, w=0.6, jit=0.12):
    """k stratified pan positions across [-w, w] (shuffled, jittered): never all on one side."""
    if k <= 0:
        return np.zeros(0)
    if k == 1:
        return np.array([rng.uniform(-0.2, 0.2)])
    return np.clip(rng.permutation(np.linspace(-w, w, k)) + rng.uniform(-jit, jit, k), -1, 1)


class _Alt:
    """Alternating-side pans: each call returns side * |pan| in [lo, hi], sides alternating from a random start."""

    def __init__(self, rng, lo=0.15, hi=0.6):
        self.rng, self.lo, self.hi = rng, lo, hi
        self.s = rng.choice([-1.0, 1.0])

    def __call__(self):
        self.s = -self.s
        return self.s * self.rng.uniform(self.lo, self.hi)


def _softknee(x, th, ceil):
    """Memoryless soft limiter: identity below th, smooth tanh knee approaching ceil above it."""
    a = np.abs(x)
    over = a > th
    if not over.any():
        return x
    y = x.copy()
    y[over] = np.sign(x[over]) * (th + (ceil - th) * np.tanh((a[over] - th) / (ceil - th)))
    return y


def _rotate_quiet(x, sr):
    """Rotate a circular loop so it starts (and ends) on a quiet near-zero sample pair."""
    if len(x) < 8:
        return x
    a = np.max(np.abs(x), axis=1)
    pair = np.maximum(a, np.roll(a, 1))          # |x[i-1]|, |x[i]| -> new end / new start
    env = ndimage.uniform_filter1d(a, max(1, int(0.03 * sr)), mode="wrap")
    i = int(np.argmin(pair + 0.05 * env))
    return np.roll(x, -i, axis=0)


def _osc(freq, sr, phase=0.0):
    return phase + TAU * np.cumsum(freq) / sr


def _ar(t, att, dec, p=1.0):
    """Smooth attack (1-exp)^p then exponential decay; zero before t=0."""
    tt = np.maximum(t, 0.0)
    return np.where(t >= 0, (1 - np.exp(-tt / att)) ** p * np.exp(-tt / dec), 0.0)


def _smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def _swell(d, rise, fall):
    """Envelope vs. time d from its peak: smooth rise over ``rise``, exponential fall, support [-rise, 6 fall]."""
    up = _smoothstep(1 + d / rise)
    dd = np.maximum(d, 0.0)
    dn = np.exp(-dd / fall) * np.clip(6 - dd / fall, 0, 1)
    return np.where(d < 0, up, dn)


def _bump(t, t0, dur, att, rel):
    """Raised-cosine attack, hold, raised-cosine release; total length ``dur`` from t0."""
    tt = t - t0
    a = _smoothstep(tt / att)
    r = _smoothstep((dur - tt) / rel)
    return np.where((tt >= 0) & (tt <= dur), a * r, 0.0)


# ---- magnitude responses for spectral shaping (f in Hz)
def _lpm(f, fc, order=2):
    return 1 / np.sqrt(1 + (f / fc) ** (2 * order))


def _hpm(f, fc, order=2):
    return 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order))


def _bpm(f, lo, hi, order=2):
    return _hpm(f, lo, order) * _lpm(f, hi, order)


def _pinkm(f, ref=1000.0, slope=0.5):
    return (np.maximum(f, 20.0) / ref) ** -slope


def _gauss(f, fc, bw):
    return np.exp(-0.5 * ((f - fc) / bw) ** 2)


def _unit(M):
    """Normalise each column (time frame) of a magnitude mask to unit mean-square -> its coefficient = RMS."""
    return M / np.sqrt(np.mean(M ** 2, axis=0, keepdims=True) + 1e-20)


# ---- filters
def _filt(x, kind, fc, sr, order=2):
    nyq = sr / 2
    if kind == "bp":
        wn, bt = [max(fc[0], 5.0), min(fc[1], 0.98 * nyq)], "bandpass"
    elif kind == "lp":
        wn, bt = min(fc, 0.98 * nyq), "lowpass"
    else:
        wn, bt = max(fc, 5.0), "highpass"
    return signal.sosfilt(signal.butter(order, wn, bt, fs=sr, output="sos"), x, axis=0)


def _reson(x, f, q, sr):
    """Two-pole resonator (peak gain 1) at f with quality q."""
    bw = f / q
    lo, hi = max(f - bw / 2, 10.0), min(f + bw / 2, 0.45 * sr)
    return signal.sosfilt(signal.butter(1, [lo, hi], "bandpass", fs=sr, output="sos"), x, axis=0)


def _fft_shape(x, sr, fn):
    """Zero-phase *circular* filtering by magnitude response fn(f) (keeps loops seamless)."""
    n = x.shape[0]
    X = np.fft.rfft(x, axis=0)
    g = np.asarray(fn(np.fft.rfftfreq(n, 1 / sr)), float)
    X *= g[:, None] if x.ndim == 2 else g
    return np.fft.irfft(X, n=n, axis=0)


def _cnoise(rng, n, sr, fn, ch=1):
    """Periodic (circular) coloured noise of exactly n samples, unit RMS."""
    y = _fft_shape(rng.standard_normal((n, ch)), sr, fn)
    y /= np.sqrt(np.mean(y ** 2)) + 1e-12
    return y[:, 0] if ch == 1 else y


def _norm(x, peak=1.0):
    m = np.abs(x).max()
    return x * (peak / m) if m > 0 else x


def _nrms(x):
    return x / (np.sqrt(np.mean(np.square(x))) + 1e-12)


# ---- periodic control signals and events
def _pnoise(rng, T, rate):
    """Smooth random function of time (~unit std), periodic with period T, varying at about ``rate`` Hz."""
    K = int(round(T * rate))
    v = rng.standard_normal(max(K, 1))
    if K < 2:
        c = 0.5 * float(v[0])
        return lambda t: np.full(np.shape(t), c)
    knots = np.arange(K + 1) * (T / K)
    cs = CubicSpline(knots, np.append(v, v[0]), bc_type="periodic")
    return lambda t: cs(np.mod(t, T))


class _Clock:
    """Periodic control-rate grid over one loop period T (for envelopes, LFOs, event sums)."""

    def __init__(self, T, rate=200.0):
        self.T = T
        self.K = max(32, int(np.ceil(T * rate)))
        self.t = np.arange(self.K) * (T / self.K)

    def ev(self, t0, lo, hi, fn):
        """Sum fn(d) over the periodic images of an event at t0; d = time since event, support [lo, hi]."""
        out = np.zeros(self.K)
        d0 = np.mod(self.t - t0, self.T)
        for k in range(int(np.floor(lo / self.T)) - 1, int(np.floor(hi / self.T)) + 1):
            d = d0 + k * self.T
            sel = (d >= lo) & (d <= hi)
            if sel.any():
                out[sel] += fn(d[sel])
        return out

    def at(self, v, t):
        return np.interp(t, self.t, v, period=self.T)


def _ptimes(rng, T, gap, jitter=0.4, min_one=False):
    """Irregular event times on the circle [0, T), mean spacing ``gap`` (count randomly rounded).
    min_one guarantees at least one event (short loops of sparse sounds are then never silent)."""
    k = int(np.floor(T / gap + rng.random()))
    if min_one:
        k = max(k, 1)
    if k <= 0:
        return np.zeros(0)
    g = gap * (1 + jitter * rng.uniform(-1, 1, k))
    g *= T / g.sum()
    return np.sort(np.mod(rng.uniform(0, T) + np.cumsum(g), T))


def _beats(rng, T, period, jitter=0.02, tol=0.15):
    """Steady pulse times; snaps the period to divide T when close (perfect loop), else keeps tempo."""
    k = max(1, int(round(T / period)))
    if abs(T / k - period) <= tol * period:
        per = T / k
        times = rng.uniform(0, per) + np.arange(k) * per
    else:
        per = period
        times = np.arange(rng.uniform(0, per), T, per)
        if len(times) == 0:                  # loop shorter than one period: still one event
            times = np.array([rng.uniform(0, 0.3 * T)])
    times = times + rng.uniform(-jitter, jitter, len(times)) * per
    return np.mod(times, T), per


def _place(buf, x, i0, pan=0.0, gain=1.0, wrap=True):
    """Add mono (panned) or stereo x into buf at sample i0; circular if wrap."""
    if x.ndim == 1:
        x = x[:, None] * (_pan(pan) * gain)[None, :]
    elif gain != 1.0:
        x = x * gain
    n, m = len(buf), len(x)
    if wrap:
        i0 %= n
        pos = 0
        while pos < m:
            j = (i0 + pos) % n
            k = min(m - pos, n - j)
            buf[j:j + k] += x[pos:pos + k]
            pos += k
    else:
        a, b = max(0, i0), min(n, i0 + m)
        if b > a:
            buf[a:b] += x[a - i0:b - i0]


def _dust(rng, rate, sr, even=False):
    """Random signed impulses; ``rate`` = per-sample array of events/second.
    Amplitudes exponential (sparse sparkle of bigger grains) or, with ``even``, uniform 0.3..1 (no outliers)."""
    hit = np.flatnonzero(rng.random(len(rate)) < np.clip(np.asarray(rate) / sr, 0, 1))
    out = np.zeros(len(rate))
    amp = rng.uniform(0.3, 1.0, len(hit)) if even else rng.exponential(1.0, len(hit))
    out[hit] = amp * rng.choice([-1.0, 1.0], len(hit))
    return out


# ---- noise beds shaped in the STFT domain (time-varying spectra), seamless
def _bed(rng, n, sr, mask_fn, corr=0.3):
    """Stereo noise whose magnitude spectrum is mask_fn(f[F,1], t[1,T], ch); seamless circular loop of n samples.

    mask_fn must be periodic in t with period n/sr. The extra second rendered past the end is cross-faded
    (equal power) into the start, so the last sample flows into the first.
    """
    nper = 2048 if sr > 32000 else 1024
    hop = nper // 4
    X = int(min(sr * 1.0, n // 4))
    m = n + X
    ys = []
    for ch in range(2):
        w = rng.standard_normal(m).astype(np.float32)
        f, tt, Z = signal.stft(w, fs=sr, nperseg=nper, noverlap=nper - hop, boundary="zeros", padded=True)
        with np.errstate(over="ignore", under="ignore"):
            M = np.asarray(mask_fn(f[:, None].astype(np.float64), tt[None, :], ch), np.float32)
        _, y = signal.istft(Z * M, fs=sr, nperseg=nper, noverlap=nper - hop)
        y = np.asarray(y, float)
        if len(y) < m:
            y = np.concatenate([y, np.zeros(m - len(y))])
        ys.append(y[:m])
    y = np.stack(ys, 1)
    if X > 0:
        th = (np.arange(X) + 0.5) / X * (np.pi / 2)
        y[:X] = y[n:n + X] * np.cos(th)[:, None] + y[:X] * np.sin(th)[:, None]
    y = y[:n]
    a = np.sqrt((1 + np.sqrt(1 - corr ** 2)) / 2)
    b = np.sqrt(1 - a * a)
    return np.stack([a * y[:, 0] + b * y[:, 1], a * y[:, 1] + b * y[:, 0]], 1)


def _shaped(rng, m, sr, mask_fn, nper=1024):
    """Mono noise of m samples shaped by mask_fn(f[F,1], t[1,T]) (one-shots; not circular)."""
    hop = nper // 8
    w = rng.standard_normal(m + nper)
    f, tt, Z = signal.stft(w, fs=sr, nperseg=nper, noverlap=nper - hop, boundary="zeros", padded=True)
    with np.errstate(over="ignore", under="ignore"):
        M = mask_fn(f[:, None], tt[None, :])
    _, y = signal.istft(Z * M, fs=sr, nperseg=nper, noverlap=nper - hop)
    return np.asarray(y[:m], float)


# ---- reverb
def _ir(rng, sr, t60=1.0, pre=0.01, lp=5000.0, taps=(), corr=0.0):
    """Stereo decaying-noise impulse response (high frequencies die faster). Normalised to unit energy *before*
    the final low-pass, so ``wet`` in _verb is roughly the wet/dry level ratio in the passband (lows a little
    more, as their decay is longer). taps: (delay_s, gain) discrete reflections relative to the diffuse level.
    corr: L/R correlation of the diffuse noise (0 = fully decorrelated, widest)."""
    L = int(sr * (pre + 1.1 * t60)) + 1
    t = np.arange(L) / sr
    tt = np.maximum(t - pre, 0.0)
    gate = (t >= pre) * (1 - np.exp(-tt / 0.003)) * _smoothstep((t[-1] - t) / (0.1 * t60))
    ir = np.zeros((L, 2))
    ed = np.sqrt(sr * t60 / 13.8)
    common = rng.standard_normal(L) if corr > 0 else None
    for ch in range(2):
        w = rng.standard_normal(L)
        if common is not None:
            w = np.sqrt(corr) * common + np.sqrt(1 - corr) * w
        lo = _filt(w, "lp", 600, sr)
        hi = w - lo
        mid = _filt(hi, "lp", 3000, sr)
        top = hi - mid
        ir[:, ch] = (lo * np.exp(-6.9 * tt / t60) + mid * np.exp(-6.9 * tt / (0.7 * t60))
                     + top * np.exp(-6.9 * tt / (0.35 * t60))) * gate
        for d, g in taps:
            j = int((pre + d * (1 + 0.04 * (2 * ch - 1))) * sr)
            if j < L:
                ir[j, ch] += g * ed * rng.uniform(0.8, 1.2)
    ir /= np.sqrt(np.sum(ir ** 2, axis=0, keepdims=True)) + 1e-12
    return _filt(ir, "lp", lp, sr, 2)


def _verb(x, ir, wet, circular=False):
    """Dry + wet * (x conv ir). Circular folds the tail back onto the start (loops)."""
    x = _stereo(x)
    n = len(x)
    y = np.stack([signal.fftconvolve(x[:, c], ir[:, c]) for c in range(2)], 1)
    if circular:
        out = y[:n].copy()
        r = y[n:]
        while len(r):
            k = min(n, len(r))
            out[:k] += r[:k]
            r = r[k:]
        return x + wet * out
    xp = np.zeros_like(y)
    xp[:n] = x
    return xp + wet * y


# ---- grain kernels (mono)
def _k_plink(rng, sr, f0=None, tau=None, rise=None):
    f0 = rng.uniform(1800, 4200) if f0 is None else f0
    tau = rng.uniform(0.004, 0.009) if tau is None else tau
    rise = rng.uniform(0.2, 0.6) if rise is None else rise
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f0 * (1 + rise * (1 - np.exp(-t / (2 * tau))))
    return np.sin(_osc(f, sr)) * _ar(t, 0.0004, tau)


def _k_tick(rng, sr, lo=None):
    m = int(sr * 0.008)
    t = np.arange(m) / sr
    lo = rng.uniform(1200, 2600) if lo is None else lo
    k = _filt(rng.standard_normal(m), "bp", (lo, lo * rng.uniform(1.8, 3.0)), sr) \
        * _ar(t, 0.0002, rng.uniform(0.0006, 0.0016))
    return _norm(k)


def _k_bubble(sr, f0, tau, rise=1.8, h2=0.1):
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f0 * (1 + (rise - 1) * (1 - np.exp(-t / (1.5 * tau))))
    ph = _osc(f, sr)
    env = _ar(t, 0.0015, tau) * _smoothstep((7 * tau - t) / (1.5 * tau))     # rings out to zero (no -52 dB cut)
    return env * (np.sin(ph) + h2 * np.sin(2 * ph))


def _k_thump(rng, sr, f0, f1, tau, noise=0.3, att=0.003, p=1.0, nlp=300, harm=(1.0, 0.4, 0.15)):
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f1 + (f0 - f1) * np.exp(-t / (tau * 0.4))
    ph = _osc(f, sr)
    y = (harm[0] * np.sin(ph) + harm[1] * np.sin(2 * ph + 0.5) + harm[2] * np.sin(3 * ph)) * _ar(t, att, tau, p)
    nz = _nrms(_filt(rng.standard_normal(m), "lp", nlp, sr))
    return y + noise * nz * _ar(t, 0.002, tau * 0.35, p)


def _k_drop_or_tick(rng, sr):
    return _k_plink(rng, sr) if rng.random() < 0.4 else _k_tick(rng, sr)


def _polyblep_saw(f, sr):
    ph = np.mod(np.cumsum(f) / sr, 1.0)
    dt = np.clip(f / sr, 1e-6, 0.5)
    y = 2 * ph - 1
    a = ph < dt
    x = ph[a] / dt[a]
    y[a] -= x + x - x * x - 1
    b = ph > 1 - dt
    x = (ph[b] - 1) / dt[b]
    y[b] -= x * x + x + x + 1
    return y


# =========================================================================================== loops
def _waves_calm(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    S = np.zeros((2, C.K))
    Fz = np.zeros((2, C.K))
    Dp = np.zeros(C.K)
    laps = []
    alt = _Alt(rng, 0.1, 0.55)
    for t0 in _ptimes(rng, T, 4.6 / p["density"], 0.45, min_one=True):
        a, rise, fall = rng.uniform(0.55, 1.0), rng.uniform(1.1, 2.0), rng.uniform(0.9, 1.5)
        g = _pan(alt())[:, None]
        S += a * g * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
        Fz += a * g * C.ev(t0 + 0.25, -0.5, 6 * 1.8 * fall, lambda d: _swell(d, 0.5, 1.8 * fall))
        for _ in range(rng.integers(1, 4)):        # the water slapping and plopping at the shore after each swell
            tl, al = t0 + rng.uniform(0.35, 2.4), a * rng.uniform(0.45, 1.0)
            laps.append((tl, al, rng.uniform(-0.6, 0.6)))
            Dp += al * C.ev(tl, -0.05, 0.15, lambda d: 0.5 - 0.5 * np.cos(TAU * (d + 0.05) / 0.2))
    dip = 1 - (1 - 10 ** (-3 / 20)) * np.clip(Dp, 0, 1)     # bed dips ~3 dB (150-1200 Hz) under each lap
    lev = 0.30 * (1 + 0.3 * _pnoise(rng, T, 0.12)(C.t))
    bfc = 430 + 130 * _pnoise(rng, T, 0.05)(C.t)

    def mask(f, t, ch):
        pk = _pinkm(f)
        s = C.at(S[ch], t)
        fc = 380 + 2300 * np.clip(s, 0, 1.3) ** 0.8
        bed = C.at(lev, t) * _unit(pk * _bpm(f, 50, C.at(bfc, t)))
        swell = s * _unit(pk * _hpm(f, 80, 1) * _lpm(f, fc))
        fizz = 0.12 * C.at(Fz[ch], t) * _unit(_bpm(f, 1500, 6000) * _pinkm(f, 3000, 0.3))
        duck = 1 - (1 - C.at(dip, t)) * _bpm(f, 150, 1200, 2)
        return (bed + swell) * duck + fizz

    x = _bed(rng, n, sr, mask, corr=0.25)
    _dbg("bed", x)
    lp = np.zeros((n, 2))
    for tl, a, pan in laps:
        _place(lp, _norm(_k_lap(rng, sr)) * a * 2.2, int(tl * sr), pan)
    _dbg("laps", lp)
    _dbg_vs("laps vs bed", lp, x, 150, 1200, sr)
    rate = 260 * C.at(Fz.mean(0), np.arange(n) / sr)
    dz = np.stack([_dust(rng, rate, sr, even=True), _dust(rng, rate, sr, even=True)], 1)
    dz = _fft_shape(dz, sr, lambda f: _bpm(f, 2000, 6500)) * 4.0
    _dbg("fizz grains", dz)
    _dbg_vs("fizz vs bed", dz, x + lp, 2000, 6500, sr)
    return x + lp + dz


def _k_lap(rng, sr):
    """Shore lap: 2-4 quick wet slaps (band noise) and sometimes a soft low plop."""
    m = int(0.4 * sr)
    t = np.arange(m) / sr
    y = np.zeros(m)
    t0 = 0.0
    for j in range(rng.integers(2, 5)):
        nz = _nrms(_filt(rng.standard_normal(m), "bp", (rng.uniform(150, 260), rng.uniform(800, 1400)), sr))
        y += nz * _ar(t - t0, 0.004, rng.uniform(0.03, 0.07)) * (0.75 ** j) * rng.uniform(0.7, 1.0)
        t0 += rng.uniform(0.02, 0.07)
    if rng.random() < 0.5:
        f0 = rng.uniform(220, 380)
        pl = np.sin(_osc(f0 * (1 + 0.5 * np.minimum(t / 0.06, 1)), sr)) * _ar(t - 0.012, 0.004, 0.03)
        y += 0.9 * pl * np.abs(y).max() / (np.abs(pl).max() + 1e-12)
    return y


def _waves_storm(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    B = np.zeros((2, C.K))
    Cr = np.zeros((2, C.K))
    W = np.zeros((2, C.K))
    crashes = []
    alt = _Alt(rng, 0.1, 0.6)
    for t0 in _ptimes(rng, T, 3.3 / p["density"], 0.4, min_one=True):
        a, rise, rc = rng.uniform(0.6, 1.0), rng.uniform(0.7, 1.4), rng.uniform(0.15, 0.25)
        tc, tw = rng.uniform(0.35, 0.6), rng.uniform(1.0, 1.6)
        pan = alt()
        g = _pan(pan)[:, None]
        B += a * g * C.ev(t0, -rise, 1.5, lambda d: _swell(d, rise, 0.2))
        Cr += a * g * C.ev(t0, -rc, 6 * tc, lambda d: _swell(d, rc, tc))
        W += a * g * C.ev(t0, 0, 6 * tw, lambda d: _ar(d, 0.2, tw, 2.0) * np.clip(6 - d / tw, 0, 1))
        crashes.append((t0, a, pan))
    l1, l2, l3 = (_pnoise(rng, T, r)(C.t) for r in (0.15, 0.08, 0.3))
    low = 0.55 * (1 + 0.3 * l1)
    lfc = 380 + 100 * l2
    mid = 0.3 * (1 + 0.4 * l3)

    def mask(f, t, ch):
        pk = _pinkm(f)
        b, c, w = C.at(B[ch], t), C.at(Cr[ch], t), C.at(W[ch], t)
        m = C.at(low, t) * _unit(pk * _bpm(f, 55, C.at(lfc, t)))
        m = m + C.at(mid, t) * _unit(pk * _bpm(f, 250, 1800))
        m = m + 0.8 * b * _unit(pk * _bpm(f, 70, 500 + 900 * np.clip(b, 0, 1.2)))
        m = m + 1.4 * c * _unit(pk ** 0.7 * _bpm(f, 60, 3000))
        m = m + 0.7 * w * _unit(pk * _bpm(f, 400, 4500))
        return m

    x = _bed(rng, n, sr, mask, corr=0.2)
    _dbg("bed", x)
    th = np.zeros((n, 2))
    for t0, a, pan in crashes:          # the body of each wave hitting: a dull boom with some 200-500 Hz weight
        k = _k_thump(rng, sr, 120, 70, 0.25, noise=0.8, att=0.03, p=2.0, nlp=450, harm=(1.0, 0.7, 0.4))
        _place(th, _norm(np.tanh(1.5 * _norm(k))) * a * 1.6, int(t0 * sr), pan)
    _dbg("thumps", th)
    _dbg_vs("thumps vs bed", th, x, 60, 400, sr)
    rate = 500 * C.at(W.mean(0), np.arange(n) / sr)
    dz = np.stack([_dust(rng, rate, sr, even=True), _dust(rng, rate, sr, even=True)], 1)
    dz = _fft_shape(dz, sr, lambda f: _bpm(f, 1800, 5500)) * 4.5
    _dbg("spray", dz)
    _dbg_vs("spray vs bed", dz, x + th, 1800, 5500, sr)
    return x + th + dz


def _storm_wind(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    gust = np.zeros((2, C.K))
    alt = _Alt(rng, 0.1, 0.5)
    for t0 in _ptimes(rng, T, 4.5, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.3, 0.7), rng.uniform(0.8, 1.8), rng.uniform(1.2, 2.5)
        gust += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    base = 0.45 + 0.18 * _pnoise(rng, T, 0.22)(C.t)
    G = [np.clip(base + 0.06 * _pnoise(rng, T, 0.7)(C.t) + gust[ch], 0.12, 1.6) for ch in range(2)]
    vib = [_pnoise(rng, T, 1.5)(C.t) for _ in range(4)]

    def mask(f, t, ch):
        g = C.at(G[ch], t)
        m = g ** 1.3 * _unit(_pinkm(f) * _bpm(f, 70, 2500))
        for k, (base_f, bw, amp) in enumerate(((330, 45, 0.45), (520, 60, 0.3))):
            fc = base_f * (0.7 + 0.55 * g) * (1 + 0.02 * C.at(vib[k], t))
            m = m + amp * g ** 2 * _unit(_gauss(f, fc, bw))
        wh = _smoothstep((g - 0.7) / 0.5)
        for k, (base_f, amp) in enumerate(((1150, 0.14), (1720, 0.08))):
            fc = base_f * (0.8 + 0.35 * g) * (1 + 0.012 * C.at(vib[2 + k], t))
            m = m + amp * wh * _unit(_gauss(f, fc, 16))
        return m + 0.22 * g ** 2 * _unit(_bpm(f, 2000, 6500))

    return _bed(rng, n, sr, mask, corr=0.35)


def _rain(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    l1 = 1 + 0.15 * _pnoise(rng, T, 0.1)(C.t)
    l2 = 1 + 0.2 * _pnoise(rng, T, 0.2)(C.t)

    def mask(f, t, ch):
        return C.at(l1, t) * _unit(_bpm(f, 900, 7000, 1)) + 0.4 * C.at(l2, t) * _unit(_pinkm(f) * _bpm(f, 150, 900))

    x = _bed(rng, n, sr, mask, corr=0.15)
    _dbg("hiss", x)
    kern = [_k_drop_or_tick(rng, sr) for _ in range(24)]
    kern = [_norm(k) for k in kern]
    dr = np.zeros((n, 2))
    times = rng.uniform(0, T, int(140 * p["density"] * T))
    for t0 in times:
        a = 0.6 * rng.lognormal(0, 0.5) * (2.2 if rng.random() < 0.04 else 1.0)
        _place(dr, kern[rng.integers(len(kern))] * a, int(t0 * sr), rng.uniform(-0.9, 0.9))
    _dbg("drops", dr)
    return x + dr


def _wind_soft(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    gust = np.zeros((2, C.K))                   # gentle breaths of breeze every ~6 s
    alt = _Alt(rng, 0.1, 0.5)
    for t0 in _ptimes(rng, T, 6.0, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.2, 0.45), rng.uniform(1.2, 2.5), rng.uniform(1.5, 3.0)
        gust += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    base = 0.5 + 0.2 * _pnoise(rng, T, 0.1)(C.t)
    G = [np.clip(base + gust[ch] + 0.08 * _pnoise(rng, T, 0.35)(C.t), 0.2, 1.2) for ch in range(2)]
    rus = np.clip(_pnoise(rng, T, 0.25)(C.t), 0, None) ** 2
    flut = [0.6 + 0.4 * np.abs(_pnoise(rng, T, 12)(C.t)) for _ in range(2)]

    def mask(f, t, ch):
        g = C.at(G[ch], t)
        m = g * _unit(_pinkm(f) * _bpm(f, 110, 1400 * (0.8 + 0.3 * g)))
        m = m + 0.3 * g ** 2 * _unit(_gauss(f, 380 * (0.85 + 0.3 * g), 120))
        return m + 0.22 * C.at(rus, t) * C.at(flut[ch], t) * _unit(_bpm(f, 1800, 6000))

    return _bed(rng, n, sr, mask, corr=0.3)


def _wind_hot(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    gust = np.zeros((2, C.K))
    alt = _Alt(rng, 0.1, 0.5)
    for t0 in _ptimes(rng, T, 3.2, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.35, 0.8), rng.uniform(0.5, 1.1), rng.uniform(0.9, 1.8)
        gust += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    base = 0.35 + 0.15 * _pnoise(rng, T, 0.3)(C.t)
    G = [np.clip(base + gust[ch], 0.1, 1.5) for ch in range(2)]

    def mask(f, t, ch):
        g = C.at(G[ch], t)
        m = g ** 1.2 * _unit(_pinkm(f, slope=0.25) * _bpm(f, 180, 3000))
        m = m + 0.18 * g ** 2 * _unit(_gauss(f, 520 * (0.75 + 0.45 * g), 90))
        return m + 0.3 * g ** 2.5 * _unit(_bpm(f, 2500, 7500))

    x = _bed(rng, n, sr, mask, corr=0.3)
    _dbg("wind", x)
    # Sand: grains whose rate (3000 G^2 /s) and size (0.3 + 0.7 G) follow the gusts. Below ~300 grains/s single
    # grains would turn into ticks, so there the grains cross-fade into smooth hiss of the same power.
    ts = np.arange(n) / sr
    sand = np.zeros((n, 2))
    for ch in range(2):
        g = C.at(G[ch], ts)
        rate = 3000 * g ** 2
        amp = 0.3 + 0.7 * g
        wg = _smoothstep((rate - 120) / 300)
        grains = _dust(rng, rate, sr, even=True) * amp
        hiss = rng.standard_normal(n) * np.sqrt(0.43 * rate / sr) * amp
        sand[:, ch] = wg * grains + np.sqrt(1 - wg ** 2) * hiss
    sand = _fft_shape(sand, sr, lambda f: _bpm(f, 2500, 6000)) * 3.8
    _dbg("sand", sand)
    return x + sand


def _ship_creak(rng, n, sr, p):
    T = n / sr
    x = np.zeros((n, 2))
    alt = _Alt(rng, 0.1, 0.6)
    for t0 in _ptimes(rng, T, 1.6 / p["density"], 0.65, min_one=True):
        r = rng.random()
        kind = "creak" if r < 0.6 else ("groan" if r < 0.85 else "knock")
        y = _norm(_k_creak(rng, sr, kind, 0.8 * T)) * rng.uniform(0.4, 1.0) * (0.6 if kind == "knock" else 1.0)
        _place(x, y, int(t0 * sr), alt())
    x = _verb(x, _ir(rng, sr, 0.5, 0.006, 3000), 0.5, circular=True)
    _dbg("creaks", x)
    C = _Clock(T)
    lv = 0.03 * (1 + 0.5 * _pnoise(rng, T, 0.2)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 80, 450)), corr=0.3)
    _dbg("hull bed", bed)
    return x + bed


def _k_creak(rng, sr, kind, dmax=9.0):
    if kind == "knock":
        m = int(0.25 * sr)
        imp = np.zeros(m)
        imp[0] = 1.0
        j = int(rng.uniform(0.03, 0.06) * sr)
        imp[j] = rng.uniform(0.25, 0.5)
        imp = signal.fftconvolve(imp, np.hanning(int(0.001 * sr) + 2))[:m]
        f1, f2 = rng.uniform(220, 320), rng.uniform(650, 900)
        return _reson(imp, f1, 14, sr) + 0.5 * _reson(imp, f2, 16, sr)
    if kind == "creak":
        D, r0, glide = min(rng.uniform(0.25, 0.9), dmax), rng.uniform(22, 70), rng.uniform(-0.45, 0.6)
        res = [(rng.uniform(380, 650), 10, 1.0), (rng.uniform(950, 1450), 12, 0.6), (rng.uniform(1900, 2600), 14, 0.25)]
        fr = 0.0
    else:
        D, r0, glide = min(rng.uniform(0.7, 1.6), dmax), rng.uniform(18, 35), rng.uniform(-0.3, 0.3)
        res = [(rng.uniform(180, 300), 6, 1.0), (rng.uniform(520, 800), 8, 0.5)]
        fr = 0.25
    m = int((D + 0.1) * sr)
    t = np.arange(m) / sr
    u = np.clip(t / D, 0, 1)
    jit = _pnoise(rng, D + 0.1, 12)(t)
    rate = r0 * (1 + glide * u) * (1 + 0.12 * jit)
    ph = np.cumsum(rate) / sr
    idx = np.flatnonzero(np.diff(np.floor(ph)) > 0)
    env = np.sin(np.pi * u) ** 0.6 * (t <= D)
    imp = np.zeros(m)
    imp[idx] = env[idx] * rng.uniform(0.5, 1.0, len(idx))
    imp = signal.fftconvolve(imp, np.hanning(int(0.0007 * sr) + 2))[:m]      # soft pulses: no broadband clicks
    y = sum(g * _reson(imp, f, q, sr) for f, q, g in res)
    y = _norm(y)
    if fr:
        y += fr * _norm(_filt(rng.standard_normal(m), "bp", (250, 1000), sr)) * env
    return _fade(y, sr, 0.0, 0.02)


def _underwater(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    l1, l2, l4 = (_pnoise(rng, T, r)(C.t) for r in (0.07, 0.04, 0.2))
    sw = np.zeros(C.K)
    for t0 in _ptimes(rng, T, 7.0, 0.5):
        a, rise, fall = rng.uniform(0.3, 0.7), rng.uniform(1.5, 3.0), rng.uniform(1.5, 3.0)
        sw += a * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    cur = np.zeros((2, C.K))                 # slow water-current swells: the filter opens as they pass
    alt = _Alt(rng, 0.15, 0.6)
    for t0 in _ptimes(rng, T, 5.0, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.4, 1.0), rng.uniform(1.5, 3.0), rng.uniform(1.5, 3.0)
        cur += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    low = 0.45 * np.clip(1 + 0.55 * l1, 0.3, None)
    rum = 0.25 * (0.5 + 0.35 * l2 + sw)
    shm = 0.035 * (1 + 0.5 * l4)

    def mask(f, t, ch):
        c = np.clip(C.at(cur[ch], t), 0, 1.3)
        m = C.at(low, t) * _unit(_pinkm(f, slope=0.8) * _bpm(f, 55, 300))
        m = m + C.at(rum, t) * _unit(_bpm(f, 50, 130))
        m = m + (0.05 + 0.8 * c) * _unit(_pinkm(f) * _bpm(f, 150, 220 + 650 * c))
        return m + C.at(shm, t) * _unit(_bpm(f, 900, 2500))

    x = _bed(rng, n, sr, mask, corr=0.1)
    _dbg("bed", x)
    bb = np.zeros((n, 2))
    alt = _Alt(rng, 0.2, 0.7)
    for t0 in _ptimes(rng, T, 2.2, 0.6):
        pan, f0 = alt(), rng.uniform(220, 450)
        tt = t0
        for j in range(rng.integers(3, 9)):
            k = _k_bubble(sr, f0 * rng.uniform(0.9, 1.3) * (1 + 0.1 * j), rng.uniform(0.03, 0.07), 1.9)
            _place(bb, _filt(k, "lp", 1200, sr) * 1.0 * rng.uniform(0.5, 1.0), int(tt * sr), pan)
            tt += rng.uniform(0.05, 0.2)
    bb = _verb(bb, _ir(rng, sr, 1.2, 0.02, 1500), 1.6, circular=True)
    _dbg("distant bubbles", bb)
    return x + bb


def _bubbles(rng, n, sr, p):
    T = n / sr
    x = np.zeros((n, 2))
    alt = _Alt(rng, 0.1, 0.6)
    for t0 in _ptimes(rng, T, 1.1 / p["density"], 0.6, min_one=True):
        pan, f0 = alt(), rng.uniform(260, 700)
        tt = t0
        for j in range(rng.integers(2, 8)):
            f = f0 * rng.uniform(0.85, 1.3) * (1 + 0.12 * j)
            k = _k_bubble(sr, f, rng.uniform(0.025, 0.06) * (400 / f) ** 0.5, rng.uniform(1.6, 2.4))
            _place(x, k * rng.uniform(0.5, 1.0) * 0.85 ** j, int(tt * sr), pan + rng.uniform(-0.1, 0.1))
            tt += rng.uniform(0.04, 0.16)
        if rng.random() < 0.3:
            k = _k_bubble(sr, rng.uniform(150, 260), rng.uniform(0.09, 0.13), 2.2, 0.15)
            _place(x, k * rng.uniform(0.8, 1.1), int((t0 + rng.uniform(-0.3, 0.3)) * sr), -0.5 * pan)
    x = _verb(x, _ir(rng, sr, 0.6, 0.008, 2500), 0.55, circular=True)
    _dbg("bubbles", x)
    bed = _bed(rng, n, sr, lambda f, t, ch: 0.02 * _unit(_pinkm(f) * _bpm(f, 40, 400)) + 0 * t, corr=0.2)
    _dbg("bed", bed)
    return x + bed


def _heartbeat(rng, n, sr, p):
    T = n / sr
    period = 60.0 / float(p["bpm"])
    times, per = _beats(rng, T, period, jitter=0.012)
    x = np.zeros((n, 2))
    dub_dt = 0.30 * min(1.0, per / 1.2)
    for t0 in times:
        a = rng.uniform(0.92, 1.0)
        lub = _k_beat(rng, sr, 120, 75, 0.11, att=0.012)
        dub = _k_beat(rng, sr, 140, 85, 0.08, att=0.01)
        _place(x, lub * a, int(t0 * sr))
        _place(x, dub * a * 0.65, int((t0 + dub_dt) * sr))
        # soft blood "whoosh" swelling after each beat
        m = int(min(per, 1.2) * sr)
        tt = np.arange(m) / sr
        w = _nrms(_filt(rng.standard_normal(m), "bp", (120, 600), sr)) * _ar(tt - 0.05, 0.08, 0.25, 2.0)
        _place(x, w * 0.12, int(t0 * sr))
    _dbg("beats", x)
    C = _Clock(T)
    lv = 0.05 * (1 + 0.3 * _pnoise(rng, T, 0.1)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 70, 450)), corr=0.3)
    _dbg("belly bed", bed)
    x = _verb(x + bed, _ir(rng, sr, 0.35, 0.005, 900), 0.35, circular=True)
    return x


def _k_beat(rng, sr, f0, f1, tau, att=0.01, knock_db=-2.0, knock_tau=0.08, drive=2.0, sat=0.3,
            harm=(0.8, 0.9, 0.7, 0.5, 0.35, 0.22), kf=(380, 560)):
    """Soft low thump that survives small speakers: a pitch-gliding thump with a rich harmonic series (upper
    harmonics decay faster), gently and slightly asymmetrically saturated (odd and even harmonics imply the
    missing fundamental on a phone), plus a soft 250-600 Hz knock (noise through a Q 2 resonator) at the onset."""
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f1 + (f0 - f1) * np.exp(-t / (tau * 0.4))
    ph = _osc(f, sr)
    y = np.zeros(m)
    for k, a in enumerate(harm, 1):
        y += a * np.sin(k * ph + 0.4 * k) * _ar(t, att, tau * (1.15 - 0.15 * k) if k < 6 else tau * 0.3, 2.0)
    y += 0.4 * _nrms(_filt(rng.standard_normal(m), "bp", (80, 600), sr)) * _ar(t, 0.002, tau * 0.35, 2.0)
    y = _norm(y)
    y = (1 - sat) * y + sat * np.tanh(drive * y) / np.tanh(drive)
    exc = rng.standard_normal(m) * _ar(t, 0.002, knock_tau)
    kn = _reson(exc, rng.uniform(*kf), 2.0, sr)
    return y + 10 ** (knock_db / 20) * _norm(kn)


def _drip(rng, n, sr, p):
    T = n / sr
    dry = np.zeros((n, 2))
    pans = _spread(rng, 3, 0.5, 0.1)
    sources = [(rng.uniform(1.2, 3.4) / p["density"], rng.uniform(700, 1900), pans[i],
                rng.uniform(0.45, 1.0)) for i in range(3)]
    for i, (per, f0, pan, a) in enumerate(sources):
        for t0 in _ptimes(rng, T, per, 0.12, min_one=(i == 0)):
            _place(dry, _k_drip(rng, sr, f0 * rng.uniform(0.96, 1.04)) * a * rng.uniform(0.8, 1.0), int(t0 * sr), pan)
    alt = _Alt(rng, 0.3, 0.8)
    for t0 in _ptimes(rng, T, 5.0 / p["density"], 0.6):
        _place(dry, _k_drip(rng, sr, rng.uniform(600, 2200)) * rng.uniform(0.3, 0.6), int(t0 * sr), alt())
    _dbg("dry drips", dry)
    taps = [(0.045, 0.5), (0.083, 0.4), (0.121, 0.3), (0.16, 0.25), (0.24, 0.35), (0.48, 0.15)]
    x = _verb(dry, _ir(rng, sr, 2.4, 0.02, 3200, taps), 1.3, circular=True)
    bed = _bed(rng, n, sr, lambda f, t, ch: 0.004 * _unit(_pinkm(f) * _bpm(f, 40, 300)) + 0 * t, corr=0.2)
    _dbg("room tone", bed)
    return x + bed


def _k_drip(rng, sr, f0):
    tau = rng.uniform(0.015, 0.03)
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f0 * (1 + 0.7 * (1 - np.exp(-t / 0.012)))
    ph = _osc(f, sr)
    y = (np.sin(ph) + 0.08 * np.sin(2.7 * ph)) * _ar(t, 0.0008, tau)
    tick = _filt(rng.standard_normal(m), "lp", 5000, sr) * _ar(t, 0.0001, 0.0004)
    return _norm(y + 0.25 * _norm(tick))


def _footsteps_any(rng, n, sr, p, run):
    T = n / sr
    times, per = _beats(rng, T, 1.0 / float(p["rate"]), jitter=0.03)
    x = np.zeros((n, 2))
    for i, t0 in enumerate(np.sort(times)):
        side = 1 if i % 2 else -1
        y = _k_step(rng, sr, run)
        _place(x, y * rng.uniform(0.8, 1.0), int(t0 * sr), side * (0.08 if run else 0.12) + rng.uniform(-0.05, 0.05))
    return x


def _footsteps(rng, n, sr, p):
    return _footsteps_any(rng, n, sr, p, run=False)


def _footsteps_run(rng, n, sr, p):
    return _footsteps_any(rng, n, sr, p, run=True)


def _k_step(rng, sr, run):
    m = int(sr * (0.22 if run else 0.32))
    t = np.arange(m) / sr

    def thump(t0, a, tau):
        tt = t - t0
        nz = _nrms(_filt(rng.standard_normal(m), "bp", (90, 380 if run else 320), sr))
        s = np.sin(_osc(95 + 50 * np.exp(-np.maximum(tt, 0) / 0.01), sr))
        return a * (0.7 * nz + 0.6 * s) * _ar(tt, 0.0025, tau)

    def grit(t0, a, count, spread):
        imp = np.zeros(m)
        ts = t0 + rng.exponential(spread, count)
        idx = (ts * sr).astype(int)
        ok = idx < m
        idx, ts = idx[ok], ts[ok]
        np.add.at(imp, idx, rng.uniform(0.2, 1.0, len(idx)) * rng.choice([-1, 1], len(idx))
                  * np.exp(-(ts - t0) / (2 * spread)))
        return a * _norm(_filt(imp, "bp", (900, 4500), sr))

    def scuff(t0, a, tau, lo, hi):
        return a * _nrms(_filt(rng.standard_normal(m), "bp", (lo, hi), sr)) * _ar(t - t0, 0.006, tau)

    if run:
        y = thump(0, 1.0, 0.03) + grit(0.003, 0.6, rng.integers(25, 45), 0.035) + scuff(0.005, 0.45, 0.045, 500, 3000)
        y += grit(0.06, 0.25, rng.integers(8, 18), 0.04)
    else:
        y = thump(0, 1.0, 0.022) + grit(0.002, 0.55, rng.integers(25, 50), 0.03) + scuff(0, 0.3, 0.05, 400, 2500)
        dt = rng.uniform(0.05, 0.075)
        y += thump(dt, 0.45, 0.02) + grit(dt, 0.35, rng.integers(15, 30), 0.025) + scuff(dt, 0.2, 0.04, 600, 3000)
    return _fade(y, sr, 0.0, 0.01)


# ---- crowd babble (formant voices at 16 kHz, distant)
_VOWELS = [(730, 1090, 2440), (530, 1840, 2480), (300, 2200, 2950), (570, 840, 2410), (320, 870, 2240),
           (500, 1450, 2500), (660, 1720, 2410)]


def _crowd(rng, n, sr, p):
    T = n / sr
    vsr = 16000
    nv16 = max(16, int(round(n * vsr / sr)))
    T16 = nv16 / vsr
    vox = np.zeros((nv16, 2))
    nvoices = max(3, int(round(14 * p["density"])))
    pans = _spread(rng, nvoices, 0.8, 0.08)
    for iv in range(nvoices):
        r = rng.random()
        f0, fs = ((rng.uniform(95, 135), 1.0) if r < 0.45 else
                  (rng.uniform(175, 235), 1.12) if r < 0.85 else (rng.uniform(240, 300), 1.25))
        dist = rng.uniform(0.35, 1.0)
        cut = 1300 + 1300 * dist
        pan = pans[iv]
        cur = rng.uniform(0, T16)
        end = cur + T16
        while True:
            room = min(end - cur, T16) - 0.2
            nsyl = min(int(rng.integers(3, 11)), int(room / 0.19))
            if nsyl < 1:
                break
            ph = _phrase(rng, vsr, f0 * rng.uniform(0.95, 1.05), fs, nsyl)
            ph = _filt(ph, "lp", cut, vsr, 2) * dist
            _place(vox, ph, int(cur * vsr), pan)
            cur += len(ph) / vsr + rng.uniform(0.3, 2.2)
    vox = signal.resample(vox, n, axis=0)           # FFT resampling keeps the loop circular
    vox = _verb(vox, _ir(rng, sr, 0.9, 0.015, 2500), 1.1, circular=True)
    vox *= 0.5
    _dbg("voices", vox)
    C = _Clock(T)
    lv = 0.55 * (1 + 0.25 * _pnoise(rng, T, 0.1)(C.t))
    fl = [1 + 0.35 * _pnoise(rng, T, 4.0)(C.t) for _ in range(2)]

    def mask(f, t, ch):
        sh = _gauss(f, 450, 300) + 0.5 * _gauss(f, 1200, 500) + 0.15 * _gauss(f, 2500, 600)
        return C.at(lv, t) * C.at(fl[ch], t) * _unit(sh)

    bed = _bed(rng, n, sr, mask, corr=0.2)
    _dbg("murmur bed", bed)
    return vox + bed


def _phrase(rng, vsr, f0, fs, nsyl, nper=512):
    durs = rng.uniform(0.11, 0.26, nsyl)
    on = 0.06 + np.concatenate([[0.0], np.cumsum(durs)[:-1]])
    L = on[-1] + durs[-1] + 0.12
    m = int(L * vsr)
    t = np.arange(m) / vsr
    cen = on + durs / 2
    acc = rng.uniform(-0.08, 0.1, nsyl)
    pc = f0 * (1.1 - 0.2 * t / L) * (1 + np.interp(t, cen, acc)) * (1 + 0.01 * _pnoise(rng, L, 20)(t))
    src = _filt(_polyblep_saw(pc, vsr), "lp", 900, vsr, 1) + 0.04 * rng.standard_normal(m)
    F = np.array([_VOWELS[i] for i in rng.integers(len(_VOWELS), size=nsyl)], float) * fs
    f, tt, Z = signal.stft(src, vsr, nperseg=nper, noverlap=nper * 3 // 4)
    fc = f[:, None]
    M = 0.03 + sum(a * _gauss(fc, np.interp(tt, cen, F[:, i])[None, :], b * fs)
                   for i, (a, b) in enumerate(((1.0, 90), (0.55, 120), (0.28, 170))))
    _, y = signal.istft(Z * M, vsr, nperseg=nper, noverlap=nper * 3 // 4)
    y = np.asarray(y[:m], float)
    if len(y) < m:
        y = np.concatenate([y, np.zeros(m - len(y))])
    env = np.zeros(m)
    for o, d in zip(on, durs):
        env = np.maximum(env, _bump(t, o, d, 0.035, 0.05))
    env = 0.12 * _bump(t, on[0], L - on[0] - 0.08, 0.05, 0.08) + 0.88 * env
    y = _nrms(y) * env
    for o in on:          # some consonant onsets
        if rng.random() < 0.55:
            k = int(0.06 * vsr)
            c = _filt(rng.standard_normal(k), "bp", (1800, 4500), vsr) * _ar(np.arange(k) / vsr, 0.004, 0.02)
            j = max(0, int((o - 0.02) * vsr))
            y[j:j + k] += 0.25 * _nrms(c)[:len(y[j:j + k])] * _ar(np.arange(len(y[j:j + k])) / vsr, 0.004, 0.02)
    return y


# ---- birds
def _birds(rng, n, sr, p):
    T = n / sr
    x = np.zeros((n, 2))
    nb = max(1, int(round(rng.integers(2, 4) * p["density"])))
    species = list(rng.permutation(["chirper", "warbler", "twitter"]))
    pans = _spread(rng, nb, 0.65, 0.12)
    for b in range(nb):
        sp = species[b % 3]
        s, dist, pan = rng.uniform(0.88, 1.12), rng.uniform(0.45, 1.0), pans[b]
        song = _bird_song(rng, sp)
        cut = 4500 + 2500 * dist
        for t0 in _ptimes(rng, T, rng.uniform(3.5, 6.5) / p["density"], 0.6, min_one=(b == 0)):
            ph = _bird_render(rng, sr, _bird_vary(rng, sp, song), s)
            ph = _filt(ph, "lp", cut, sr, 2) * dist * rng.uniform(0.7, 1.0)
            _place(x, ph, int(t0 * sr), pan + rng.uniform(-0.1, 0.1))
            if rng.random() < 0.35:            # a lone call a little later
                call = _bird_render(rng, sr, [song[rng.integers(len(song))][:2] + (0.0,)], s)
                t1 = t0 + len(ph) / sr + rng.uniform(0.4, 1.2)
                _place(x, _filt(call, "lp", cut, sr, 2) * dist * 0.6, int(t1 * sr), pan)
    x = _verb(x, _ir(rng, sr, 0.9, 0.012, 4500), 0.4, circular=True)
    _dbg("birds", x)
    C = _Clock(T)
    lv = 0.006 * (1 + 0.3 * _pnoise(rng, T, 0.15)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 120, 2500)), corr=0.3)
    _dbg("air", bed)
    return x + bed


_GLIDES = [(2200, 3000), (3300, 2400), (2400, 3300, 2600), (3000, 2300, 2900), (2650, 2850), (2300, 3500, 3100)]


def _bird_song(rng, sp):
    """A bird's song template: list of (duration_s, frequency knots Hz, gap_after_s)."""
    if sp == "chirper":                       # sparrow-like repeated chips, maybe a closing trill
        cnt, slope = rng.integers(3, 7), rng.uniform(-0.04, 0.04)
        song = [(rng.uniform(0.03, 0.045), tuple(np.array([4100, 3300, 3000]) * (1 + slope * i)),
                 rng.uniform(0.07, 0.11)) for i in range(cnt)]
        if rng.random() < 0.5:
            song += [(0.018, (3600, 3200), 0.012)] * int(rng.integers(5, 9))
        return song
    if sp == "warbler":                       # robin-like varied whistled glides
        return [(rng.uniform(0.08, 0.2), tuple(np.array(_GLIDES[rng.integers(len(_GLIDES))]) * rng.uniform(0.85, 1.2)),
                 rng.uniform(0.04, 0.09)) for _ in range(rng.integers(3, 7))]
    song = [(rng.uniform(0.02, 0.03), (3800, 3000) if i % 2 else (3000, 3800), rng.uniform(0.015, 0.025))
            for i in range(rng.integers(8, 15))]                 # finch-like twitter + longer ending notes
    return song + [(0.1, (2600, 3400), 0.05)] * int(rng.integers(1, 3))


def _bird_vary(rng, sp, song):
    song = list(song)
    if sp == "warbler" and len(song) > 2 and rng.random() < 0.4:
        i = rng.integers(len(song) - 1)
        song[i], song[i + 1] = song[i + 1], song[i]
    if len(song) > 2 and rng.random() < 0.3:
        song = song[:-1]
    k = rng.uniform(0.97, 1.03)
    return [(d * rng.uniform(0.9, 1.1), tuple(np.array(f) * k), g * rng.uniform(0.85, 1.15)) for d, f, g in song]


def _bird_render(rng, sr, notes, s):
    parts = []
    for D, knots, gap in notes:
        m = max(8, int(D * sr))
        u = np.arange(m) / m
        kn = np.minimum(np.array(knots, float) * s, 4400)
        f = np.interp(_smoothstep(u) if len(kn) == 2 else u, np.linspace(0, 1, len(kn)), kn)
        if len(kn) > 2:
            f = ndimage.gaussian_filter1d(f, m / 12, mode="nearest")
        ph = _osc(f, sr)
        env = np.sin(np.pi * u ** 0.8) ** 0.7
        parts.append(env * (np.sin(ph) + 0.05 * np.sin(2 * ph)))
        parts.append(np.zeros(int(gap * sr)))
    return np.concatenate(parts)


# ---- snore
def _snore(rng, n, sr, p):
    T = n / sr
    cyc = float(p["cycle"])
    if T < 0.6 * cyc:
        times, per = np.array([0.0]), T          # one compressed snore cycle per loop
    else:
        times, per = _beats(rng, T, cyc, jitter=0.03, tol=0.2)
    x = np.zeros((n, 2))
    for t0 in times:
        _place(x, _snore_cycle(rng, sr, per), int(t0 * sr), rng.uniform(-0.05, 0.05))
    return _verb(x, _ir(rng, sr, 0.35, 0.005, 3000), 0.25, circular=True)


def _snore_cycle(rng, sr, per):
    sc = min(1.0, per / 3.5)
    Di, gap, De = rng.uniform(1.2, 1.5) * sc, 0.15 * sc, rng.uniform(1.0, 1.25) * sc
    m = int((Di + gap + De + 0.1) * sr)
    y = np.zeros(m)
    # inhale: soft-palate flutter (pulse train) through throat resonances + breath
    mi = int(Di * sr)
    ti = np.arange(mi) / sr
    u = ti / Di
    env = u ** 1.4 * _smoothstep((Di - ti) / 0.09) * _smoothstep(ti / 0.05)
    r = rng.uniform(26, 34) * (0.85 + 0.35 * u) * (1 + 0.05 * _pnoise(rng, Di, 8)(ti))
    idx = np.flatnonzero(np.diff(np.floor(np.cumsum(r) / sr)) > 0)
    imp = np.zeros(mi)
    imp[idx] = rng.uniform(0.6, 1.0, len(idx))
    k = int(0.012 * sr)
    flap = _filt(rng.standard_normal(k), "lp", 1600, sr) * _ar(np.arange(k) / sr, 0.0015, 0.005)
    src = signal.fftconvolve(imp, flap)[:mi]
    fs = rng.uniform(0.9, 1.1)
    rasp = _norm(_reson(src, 240 * fs, 4, sr) + 0.6 * _reson(src, 650 * fs, 5, sr)
                 + 0.3 * _reson(src, 1150 * fs, 6, sr))
    am = ndimage.uniform_filter1d(imp, int(0.02 * sr))
    am = am / (am.max() + 1e-9)
    breath = _norm(_filt(rng.standard_normal(mi), "bp", (300, 2200), sr)) * (0.4 + 0.6 * am)
    y[:mi] += env * (0.8 * rasp + 0.25 * breath)
    # exhale: cartoon whistle + soft "hhh"
    j0 = int((Di + gap) * sr)
    me = int(De * sr)
    te = np.arange(me) / sr
    u = te / De
    fw = rng.uniform(650, 820)
    f = fw * (1 + 0.35 * np.sin(np.pi * u * 0.9)) * (1 + 0.012 * np.sin(TAU * 5.5 * te))
    envw = _smoothstep(te / 0.15) * _smoothstep((De - te) / 0.35)
    ph = _osc(f, sr)
    tone = np.sin(ph) + 0.08 * np.sin(2 * ph)
    hh = _norm(_filt(rng.standard_normal(me), "bp", (500, 2400), sr))
    y[j0:j0 + me] += envw * (0.38 * tone + 0.22 * hh)
    return y


# ---- heat (cicadas)
def _heat(rng, n, sr, p):
    """Soft cicada chorus: 3-5 voices of band noise (2.5-4 kHz, wide) pulsed at ~100-150 Hz, each swelling by
    6-10 dB over 3-6 s with staggered phases, the chorus as a whole breathing by ~4-5 dB over 7-11 s, over a little
    warm air. Low-passed at 5 kHz (_FINISH); levelled a little lower than the other beds (LOOP_LUFS)."""
    T = n / sr
    C = _Clock(T)
    ts = np.arange(n) / sr
    x = np.zeros((n, 2))
    k = int(rng.integers(3, 6))
    pans = _spread(rng, k, 0.7, 0.1)
    fcs = rng.permutation(np.linspace(2500, 3700, k)) * rng.uniform(0.96, 1.04, k)
    for i in range(k):
        fc, bw = fcs[i], rng.uniform(1000, 1500)
        fam = max(1, round(rng.uniform(95, 150) * T)) / T
        sharp = rng.uniform(1.5, 3.0)
        car = _cnoise(rng, n, sr, lambda f: _gauss(f, fc, bw / 2) * _lpm(f, 4500, 2))
        am = (0.5 + 0.5 * np.cos(TAU * fam * ts + rng.uniform(0, TAU))) ** sharp
        am /= np.sqrt(np.mean(am ** 2))
        cyc = max(1, int(round(T / rng.uniform(3.0, 6.0))))
        depth = rng.uniform(6.0, 10.0) * min(1.0, T / 3.0)
        warp = _pnoise(rng, T, 0.15)
        sw = 0.5 - 0.5 * np.cos(TAU * cyc * ts / T + TAU * i / k + rng.uniform(-0.4, 0.4) + 0.7 * warp(ts))
        e = 10 ** (-depth * (1 - sw) / 20) * (1 + 0.12 * np.sin(TAU * (max(1, round(3.5 * T)) / T) * ts))
        _place(x, car * am * e * rng.uniform(0.6, 1.0), 0, pans[i])
    # the whole chorus also breathes together (~4-5 dB over 7-11 s), so the bed is never a static band
    gc = max(1, int(round(T / rng.uniform(7.0, 11.0))))
    gw = _pnoise(rng, T, 0.1)
    gs = 0.5 - 0.5 * np.cos(TAU * gc * ts / T + rng.uniform(0, TAU) + 0.6 * gw(ts))
    x *= (10 ** (-rng.uniform(4.0, 5.0) * min(1.0, T / 4.0) * (1 - gs) / 20))[:, None]
    x = _verb(x, _ir(rng, sr, 0.8, 0.012, 5000), 0.55, circular=True)
    _dbg("cicadas", x)
    lv = 0.15 * (1 + 0.3 * _pnoise(rng, T, 0.1)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 80, 1200)), corr=0.3)
    _dbg("warm air", bed)
    return x + bed


def _add(y, k, t0, sr):
    """Add mono kernel k into mono buffer y at time t0 (s), cut at the end (one-shot kernels)."""
    i = max(0, int(t0 * sr))
    j = min(len(y), i + len(k))
    if j > i:
        y[i:j] += k[:j - i]


# ---- oars (rowing)
def _oars(rng, n, sr, p):
    """Rowing, one stroke every ``cycle`` s (1.4), a little irregular in timing and strength. Each stroke, for both
    oars (a few ms apart, left and right): the blade dips in (soft plunk + splash), pulls a gurgling swirl of water
    while the wooden oarlock creaks under the load, lifts out with a small splash and a trickle of drips, and knocks
    softly in its lock on the recovery. Under it a low bed of water along the hull that surges after each pull.

    The loop always holds a whole number of evenly spaced strokes: the stroke period is the one closest to ``cycle``
    that divides the loop length (within 23 % of it for loops of 2.3 s or more, within 8 % from 8 s; a loop under
    ~2 s holds a single stroke, time-compressed when the loop is shorter than ``cycle``)."""
    T = n / sr
    cyc = float(p["cycle"])
    k = max(1, int(np.floor(T / cyc + 1e-9)))
    if T / (k * cyc) > cyc * (k + 1) / T:        # k + 1 strokes are closer to the wanted tempo (log scale)
        k += 1
    per = T / k
    times = np.mod(rng.uniform(0, per) + np.arange(k) * per + rng.uniform(-0.05, 0.05, k) * per, T)
    sc = min(1.0, per / 1.4)                     # faster strokes are compressed in time
    C = _Clock(T)
    surge = np.zeros(C.K)
    x = np.zeros((n, 2))
    side = rng.choice([-1.0, 1.0])
    for t0 in times:
        a = rng.uniform(0.75, 1.0)
        surge += a * C.ev(t0 + 0.3 * sc, -0.3 * sc, 3.0 * sc, lambda d: _swell(d, 0.3 * sc, 0.5 * sc))
        lead = rng.uniform(0.005, 0.035)         # the two blades never enter exactly together
        for s, dt in ((side, 0.0), (-side, lead)):
            k = _k_oar(rng, sr, sc) * a * rng.uniform(0.8, 1.0)
            _place(x, k, int((t0 + dt) * sr), s * rng.uniform(0.3, 0.5))
        side = -side
    _dbg("strokes", x)
    x = _verb(x, _ir(rng, sr, 0.4, 0.008, 4000), 0.2, circular=True)
    lv = 0.045 * (1 + 0.25 * _pnoise(rng, T, 0.2)(C.t))

    def mask(f, t, ch):
        s = np.clip(C.at(surge, t), 0, 1.3)
        m = C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 70, 700))
        return m + 0.05 * s * _unit(_pinkm(f) * _bpm(f, 150, 500 + 1300 * s))

    bed = _bed(rng, n, sr, mask, corr=0.3)
    _dbg("water bed", bed)
    _dbg_vs("strokes vs bed", x, bed, 150, 1500, sr)
    return x + bed


def _k_oar(rng, sr, sc):
    """One oar's stroke (mono, ~1.4 s at sc = 1): dip, pull swirl, oarlock creak, lift-out, drips, recovery knock."""
    m = int((1.35 * sc + 0.15) * sr)
    t = np.arange(m) / sr
    y = np.zeros(m)
    # dip: the blade enters -- a soft low plunk and a short splash
    _add(y, 0.8 * _norm(_k_bubble(sr, rng.uniform(170, 240), rng.uniform(0.03, 0.045), rng.uniform(1.5, 1.9), 0.15)),
         0.0, sr)
    y += 0.4 * _nrms(_filt(rng.standard_normal(m), "bp", (350, 2800), sr)) * _ar(t, 0.002, 0.035)
    # pull: a gurgling swirl of water and a few bubbles
    env = _ar(t - 0.04 * sc, 0.1 * sc, 0.2 * sc, 2.0)
    env /= env.max() + 1e-12
    gurgle = np.clip(1 + 0.6 * _nrms(_filt(rng.standard_normal(m), "lp", 14, sr)), 0.2, None)
    y += 0.22 * _nrms(_filt(rng.standard_normal(m), "bp", (150, 1100), sr)) * env * gurgle
    for _ in range(rng.integers(2, 5)):
        b = _k_bubble(sr, rng.uniform(260, 520), rng.uniform(0.02, 0.035), 1.8)
        _add(y, b * rng.uniform(0.12, 0.25), rng.uniform(0.08, 0.45) * sc, sr)
    # the oarlock creaks under the load of the pull
    _add(y, 1.0 * _k_oarlock(rng, sr, rng.uniform(0.25, 0.36) * sc), rng.uniform(0.07, 0.12) * sc, sr)
    # lift-out: a small splash, then a trickle of drips from the blade
    tl = rng.uniform(0.6, 0.66) * sc
    y += 0.22 * _nrms(_filt(rng.standard_normal(m), "bp", (500, 3000), sr)) * _ar(t - tl, 0.004, 0.03)
    for _ in range(rng.integers(6, 13)):
        td = tl + 0.02 + rng.exponential(0.12 * sc)
        _add(y, _norm(_k_plink(rng, sr, f0=rng.uniform(1100, 2300))) * rng.uniform(0.04, 0.12)
             * np.exp(-(td - tl) / (0.3 * sc)), td, sr)
    # recovery: the oar knocks softly in its lock
    if rng.random() < 0.7:
        _add(y, 0.18 * _k_tock(rng, sr), rng.uniform(0.85, 1.0) * sc, sr)
    return _fade(y, sr, 0.0, 0.02)


def _k_oarlock(rng, sr, D):
    """Short wooden creak of an oar turning in its lock: a rising train of soft stick-slip pulses through small wood
    resonances."""
    m = int((D + 0.05) * sr)
    t = np.arange(m) / sr
    u = np.clip(t / D, 0, 1)
    rate = rng.uniform(45, 75) * (1 + rng.uniform(0.1, 0.5) * u) * (1 + 0.1 * _pnoise(rng, D + 0.05, 15)(t))
    idx = np.flatnonzero(np.diff(np.floor(np.cumsum(rate) / sr)) > 0)
    env = np.sin(np.pi * u) ** 0.7 * (t <= D)
    imp = np.zeros(m)
    imp[idx] = env[idx] * rng.uniform(0.5, 1.0, len(idx))
    imp = signal.fftconvolve(imp, np.hanning(int(0.0006 * sr) + 2))[:m]
    f1 = rng.uniform(430, 600)
    y = (_reson(imp, f1, 9, sr) + 0.55 * _reson(imp, f1 * rng.uniform(2.1, 2.5), 11, sr)
         + 0.2 * _reson(imp, f1 * rng.uniform(4.0, 4.6), 13, sr))
    return _fade(_norm(y), sr, 0.0, 0.02)


# ---- fire
def _fire(rng, n, sr, p):
    """Small altar fire: a soft, flickering flame roar with a gentle whooshing flare-up every few seconds, dry wood
    crackles (single ticks, little clusters and now and then a rounder sap pop; ``density``) and a faint sizzle."""
    T = n / sr
    C = _Clock(T)
    fl = np.zeros((2, C.K))
    alt = _Alt(rng, 0.05, 0.4)
    for t0 in _ptimes(rng, T, 4.0, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.35, 0.8), rng.uniform(0.35, 0.8), rng.uniform(0.6, 1.2)
        fl += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    base = 0.45 + 0.1 * _pnoise(rng, T, 0.25)(C.t)
    G = [np.clip(base + 0.1 * _pnoise(rng, T, 1.5)(C.t) + fl[ch], 0.15, 1.6) for ch in range(2)]
    flick = [np.clip(1 + 0.3 * _pnoise(rng, T, 7.0)(C.t), 0.4, None) for _ in range(2)]

    def mask(f, t, ch):
        g = C.at(G[ch], t)
        m = g * C.at(flick[ch], t) * _unit(_pinkm(f, slope=0.6) * _bpm(f, 110, 400 + 600 * g))
        m = m + 0.4 * g ** 2 * _unit(_pinkm(f) * _bpm(f, 300, 1500 + 1000 * g))
        return m + 0.04 * _unit(_bpm(f, 2500, 5500))

    x = 0.3 * _bed(rng, n, sr, mask, corr=0.4)
    _dbg("flame", x)
    cr = np.zeros((n, 2))
    dens = float(p["density"])
    for t0 in _ptimes(rng, T, 1 / (6 * dens), 0.9):                       # single ticks
        _place(cr, _k_crackle(rng, sr) * min(rng.lognormal(0, 0.45), 2.2) * 0.6, int(t0 * sr), rng.uniform(-0.6, 0.6))
    for t0 in _ptimes(rng, T, 1.6 / dens, 0.7, min_one=True):            # little clusters
        pan, tt = rng.uniform(-0.5, 0.5), t0
        for j in range(rng.integers(3, 9)):
            _place(cr, _k_crackle(rng, sr) * rng.uniform(0.4, 1.1) * 0.85 ** j, int(tt * sr),
                   pan + rng.uniform(-0.1, 0.1))
            tt += 0.006 + rng.exponential(0.025)
    for t0 in _ptimes(rng, T, 5.0 / dens, 0.6):                           # sap pops
        _place(cr, _k_sap(rng, sr) * rng.uniform(0.9, 1.4), int(t0 * sr), rng.uniform(-0.4, 0.4))
    cr = 1.5 * _verb(cr, _ir(rng, sr, 0.3, 0.004, 5000), 0.25, circular=True)
    _dbg("crackles", cr)
    _dbg_vs("crackles vs flame", cr, x, 1000, 4000, sr)
    return x + cr


def _k_crackle(rng, sr):
    """One dry crackle: a tiny noise snap through a couple of soft wood resonances (1-4 kHz)."""
    m = int(0.025 * sr)
    t = np.arange(m) / sr
    exc = rng.standard_normal(m) * _ar(t, 0.0001, rng.uniform(0.0004, 0.0012))
    f1 = rng.uniform(1000, 2400)
    y = _reson(exc, f1, rng.uniform(3, 6), sr) + 0.5 * _reson(exc, f1 * rng.uniform(1.4, 1.9), 5, sr)
    y = y + 0.3 * _filt(exc, "bp", (800, 4000), sr)
    return _norm(y * _ar(t, 0.0001, 0.006))


def _k_sap(rng, sr):
    """A rounder sap pop: a short pitched 'pok' (500-900 Hz) with a crackle on top."""
    m = int(0.06 * sr)
    t = np.arange(m) / sr
    f = rng.uniform(500, 900) * (1 + 0.3 * np.exp(-t / 0.004))
    y = np.sin(_osc(f, sr)) * _ar(t, 0.0005, 0.012)
    _add(y, 0.6 * _k_crackle(rng, sr), 0.0, sr)
    return _norm(y)


# ---- night
def _night(rng, n, sr, p):
    """Calm night: 2-3 crickets (``density``) chirping -- pure 3.1-4.1 kHz tones in 2-4 short pulses every 0.5-1.1 s,
    each chirp a little different (pitch, pulse widths, now and then one pulse more or less). In loops of 4 s or
    more every cricket pauses now and then (about every 5-9 s, for 1.2-3 s; the nearest one only drops back to half
    level), so the chirping is never metronomic. Under them a soft distant cricket chorus that comes and goes in slow
    waves, and a faint, slow night breeze in the leaves."""
    T = n / sr
    C = _Clock(T)
    ts = np.arange(n) / sr
    cr = np.zeros((n, 2))
    k = max(1, int(round(int(rng.integers(2, 4)) * p["density"])))
    pans = _spread(rng, k, 0.6, 0.1)
    fcs = rng.permutation(np.linspace(3100, 4100, k)) * rng.uniform(0.97, 1.03, k)
    for i in range(k):
        dist = 1.0 if i == 0 else rng.uniform(0.45, 0.9)
        npul, pw, ps = int(rng.integers(2, 5)), rng.uniform(0.012, 0.02), rng.uniform(0.028, 0.04)
        times, _ = _beats(rng, T, rng.uniform(0.5, 1.1), jitter=0.03, tol=0.2)
        # pauses: explicit windows on the circle (seamless), soft 0.3 s edges; none in loops under 4 s
        pz = _ptimes(rng, T, rng.uniform(5.0, 9.0), 0.5) if T >= 4.0 else np.zeros(0)
        half = np.minimum(rng.uniform(1.2, 3.0, len(pz)), 0.3 * T) / 2
        lo = 0.5 if i == 0 else 0.0                          # the nearest cricket never stops completely
        for t0 in times:
            gv = 1.0
            for c, h in zip(pz, half):
                dd = abs((t0 - c + T / 2) % T - T / 2)       # circular distance to the pause centre
                gv *= _smoothstep((dd - (h - 0.3)) / 0.3)
            gv = lo + (1 - lo) * gv
            np_i = int(np.clip(npul + (rng.integers(-1, 2) if rng.random() < 0.2 else 0), 2, 5))
            chirp = _k_chirp(rng, sr, fcs[i] * rng.uniform(0.996, 1.004), np_i, pw * rng.uniform(0.9, 1.1),
                             ps * rng.uniform(0.95, 1.05))
            if gv > 0.02:
                _place(cr, chirp * dist * gv * rng.uniform(0.85, 1.0), int(t0 * sr), pans[i])
    _dbg("crickets", cr)
    ch = np.zeros((n, 2))                                    # distant chorus: soft trills in slow waves, with gaps
    fg = max(1, round(rng.uniform(0.1, 0.2) * T)) / T        # a gap every 5-10 s (whole cycles per loop)
    ph0 = rng.uniform(0, TAU)
    for pan in _spread(rng, 2, 0.6, 0.1):
        fc = rng.uniform(2700, 3200)
        car = _cnoise(rng, n, sr, lambda f: _gauss(f, fc, 70))
        fam = max(1, round(rng.uniform(25, 40) * T)) / T
        am = (0.5 + 0.5 * np.cos(TAU * fam * ts + rng.uniform(0, TAU))) ** 2
        sw = np.clip(0.6 + 0.4 * _pnoise(rng, T, 0.15)(ts), 0.15, None)
        gate = _smoothstep((0.25 + 0.5 * np.cos(TAU * fg * ts + ph0 + rng.uniform(-0.6, 0.6))) / 0.5)
        _place(ch, car * am * sw * gate * 0.045, 0, pan)
    _dbg("chorus", ch)
    x = _verb(cr + ch, _ir(rng, sr, 1.0, 0.02, 5000), 0.45, circular=True)
    gust = np.zeros((2, C.K))                                # the breeze: slow soft breaths every ~7 s
    alt = _Alt(rng, 0.1, 0.5)
    for t0 in _ptimes(rng, T, 7.0, 0.5, min_one=True):
        a, rise, fall = rng.uniform(0.2, 0.4), rng.uniform(1.5, 3.0), rng.uniform(2.0, 3.5)
        gust += a * _pan(alt())[:, None] * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    base = 0.4 + 0.12 * _pnoise(rng, T, 0.08)(C.t)
    G = [np.clip(base + gust[c], 0.15, 1.0) for c in range(2)]

    def mask(f, t, c):
        g = C.at(G[c], t)
        m = g * _unit(_pinkm(f) * _bpm(f, 90, 800 * (0.8 + 0.4 * g)))
        return m + 0.08 * g ** 2 * _unit(_bpm(f, 1500, 4000))

    breeze = 0.12 * _bed(rng, n, sr, mask, corr=0.3)
    _dbg("breeze", breeze)
    _dbg_vs("crickets vs breeze", x, breeze, 2500, 4500, sr)
    return x + breeze


def _k_chirp(rng, sr, fc, npul, pw, ps):
    """One cricket chirp: npul raised-cosine tone pulses (width pw, spacing ps) at fc, the first a little softer."""
    m = int((ps * (npul - 1) + pw + 0.004) * sr)
    t = np.arange(m) / sr
    env = np.zeros(m)
    for j in range(npul):
        u = (t - j * ps) / pw
        env += np.where((u >= 0) & (u <= 1), np.sin(np.pi * np.clip(u, 0, 1)) ** 2, 0.0) \
            * (0.7 if j == 0 else 1.0) * rng.uniform(0.85, 1.0)
    f = fc * (1 - 0.006 * np.mod(t, ps) / ps)            # each pulse sags a hair in pitch
    return env * np.sin(_osc(f, sr, rng.uniform(0, TAU)))


# ---- cheer (joyful crowd)
_CLAP_DB = 6.5     # median clap level over the rest of the crowd in the 1-3 kHz band (first 10 ms), dB


def _cheer(rng, n, sr, p):
    """A joyful crowd in the distance: excited babble and happy wordless shouts ('yaaay', 'woo-hoo', 'hey!', 'oooh')
    that swell up together every few seconds, a few people clapping (level set against the crowd in the claps' 1-3 kHz
    band, so they read in every variation), over a bright murmur bed (``density`` = voices).
    Voices are formant-synthesised at 16 kHz like ``crowd`` and resampled (circular)."""
    T = n / sr
    C = _Clock(T)
    sw = np.zeros(C.K)
    peaks = _ptimes(rng, T, 5.0, 0.4, min_one=True)
    for t0 in peaks:
        a, rise, fall = rng.uniform(0.6, 1.0), rng.uniform(1.2, 2.2), rng.uniform(0.8, 1.5)
        sw += a * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    act = 0.5 + 0.5 * np.clip(sw, 0, 1.3)
    vsr = 16000
    nv16 = max(16, int(round(n * vsr / sr)))
    T16 = nv16 / vsr
    vox = np.zeros((nv16, 2))
    nvoices = max(4, int(round(12 * p["density"])))
    pans = _spread(rng, nvoices, 0.8, 0.08)
    voices = []
    for iv in range(nvoices):
        r = rng.random()
        f0, fs = ((rng.uniform(110, 150), 1.0) if r < 0.35 else
                  (rng.uniform(200, 250), 1.12) if r < 0.75 else (rng.uniform(250, 320), 1.25))
        dist = rng.uniform(0.35, 1.0)
        cut = 1400 + 1400 * dist
        voices.append((f0, fs, dist, cut, pans[iv]))
        cur = rng.uniform(0, T16)                            # excited babble, a little higher than talk
        end = cur + T16
        while True:
            room = min(end - cur, T16) - 0.2
            nsyl = min(int(rng.integers(2, 7)), int(room / 0.19))
            if nsyl < 1:
                break
            ph = _phrase(rng, vsr, f0 * rng.uniform(1.1, 1.25), fs, nsyl)
            _place(vox, _filt(ph, "lp", cut, vsr, 2) * dist * 0.7, int(cur * vsr), pans[iv])
            cur += len(ph) / vsr + rng.uniform(0.5, 2.2)
    shouts = [(t0 + rng.uniform(-1.3, 0.3), 1.0) for t0 in peaks for _ in range(rng.integers(3, 7))]
    shouts += [(t0, 0.7) for t0 in _ptimes(rng, T, 2.5, 0.6)]
    shv = np.zeros_like(vox)
    for t0, g in shouts:
        f0, fs, dist, cut, pan = voices[rng.integers(nvoices)]
        sh = _shout(rng, vsr, f0 * rng.uniform(1.15, 1.35), fs)
        _place(shv, _filt(sh, "lp", cut, vsr, 2) * dist * g * 1.5, int(t0 * vsr), pan + rng.uniform(-0.1, 0.1))
    v4 = signal.resample(np.concatenate([vox, shv], 1), n, axis=0)     # FFT resampling keeps the loop circular
    actn = C.at(act, np.arange(n) / sr)[:, None]
    _dbg_vs("shouts vs babble", v4[:, 2:] * actn, v4[:, :2] * actn, 200, 3000, sr)
    vox = (v4[:, :2] + v4[:, 2:]) * actn
    _dbg("voices", vox)
    cl = np.zeros((n, 2))                                    # a few people clapping
    onsets = []
    for t0 in _ptimes(rng, T, 3.5 / p["density"], 0.6, min_one=True):
        pan, rate, dist = rng.uniform(-0.7, 0.7), rng.uniform(3.5, 5.0), rng.uniform(0.4, 1.0)
        hand = rng.uniform(900, 1500)
        for j in range(rng.integers(3, 8)):
            tc = t0 + j / rate + rng.uniform(-0.012, 0.012)
            _place(cl, _k_clap(rng, sr, hand) * dist * rng.uniform(0.7, 1.0), int(tc * sr), pan)
            onsets.append(int(tc * sr))
    ir = _ir(rng, sr, 0.9, 0.015, 3000)
    xv, xc = (_verb(v, ir, 1.0, circular=True) * 0.5 for v in (vox, cl))
    lv = 0.5 * (1 + 0.2 * _pnoise(rng, T, 0.1)(C.t)) * act
    fl = [1 + 0.35 * _pnoise(rng, T, 4.0)(C.t) for _ in range(2)]

    def mask(f, t, ch):
        sh = _gauss(f, 500, 300) + 0.6 * _gauss(f, 1400, 500) + 0.2 * _gauss(f, 2600, 600)
        return C.at(lv, t) * C.at(fl[ch], t) * _unit(sh)

    bed = _bed(rng, n, sr, mask, corr=0.2)
    _dbg("murmur bed", bed)
    # Clap level is set against everything else in their 1-3 kHz band, so they read in every variation: the median
    # clap's first 10 ms sits _CLAP_DB over the voices + murmur at that moment.
    def band(z):
        return _fft_shape(z.mean(axis=1), sr, lambda f: _bpm(f, 1000, 3000, 4))

    cb, rb = band(xc), band(xv + bed)
    idx = (np.asarray(onsets)[:, None] + np.arange(int(0.01 * sr))[None, :]) % n
    d = 10 * np.log10((np.mean(cb[idx] ** 2, axis=1) + 1e-20) / (np.mean(rb[idx] ** 2, axis=1) + 1e-20))
    gdb = float(np.clip(_CLAP_DB - np.median(d), -10.0, 20.0))
    if _DEBUG is not None:
        q = np.percentile(d, [10, 50, 90]) + gdb
        _DEBUG.append(f"[{'claps vs crowd':<16}] 1000-3000 Hz, first 10 ms of each clap vs voices + murmur: "
                      f"p10 {q[0]:+5.1f} dB, median {q[1]:+5.1f} dB, p90 {q[2]:+5.1f} dB (clap gain {gdb:+.1f} dB)")
    xc *= 10 ** (gdb / 20)
    _dbg("claps", xc)
    _dbg("voices + murmur", xv + bed)
    return xv + xc + bed



_SHOUTS = {   # syllables: (duration range, vowel start/middle/end, pitch knots at u = 0, 0.3, 0.7, 1, aspirated)
    "yay": [((0.4, 0.7), ("i", "a", "e"), (1.0, 1.3, 1.25, 1.05), False)],
    "woohoo": [((0.15, 0.22), ("u", "u", "u"), (1.0, 1.1, 1.1, 1.05), False),
               ((0.35, 0.55), ("u", "o", "u"), (1.2, 1.45, 1.4, 1.15), True)],
    "hey": [((0.2, 0.32), ("e", "e", "i"), (1.1, 1.3, 1.2, 1.0), True)],
    "ooh": [((0.35, 0.6), ("o", "o", "o"), (1.0, 1.25, 1.3, 1.1), False)],
    "aah": [((0.35, 0.6), ("a", "a", "a"), (1.0, 1.25, 1.3, 1.1), False)],
}
_VOW = {"a": (730, 1090, 2440), "e": (530, 1840, 2480), "i": (300, 2200, 2950), "o": (570, 840, 2410),
        "u": (320, 870, 2240)}


def _shout(rng, vsr, f0, fs):
    """A happy wordless shout at vsr (16 kHz): voiced formant vowels with a rising-falling pitch."""
    syl = _SHOUTS[list(_SHOUTS)[rng.integers(len(_SHOUTS))]]
    parts = []
    for (dlo, dhi), vw, knots, asp in syl:
        D = rng.uniform(dlo, dhi)
        m = int((D + 0.03) * vsr)
        t = np.arange(m) / vsr
        u = np.clip(t / D, 0, 1)
        f = f0 * np.interp(u, [0, 0.3, 0.7, 1], knots) * (1 + 0.012 * _pnoise(rng, D + 0.03, 9)(t))
        F = [np.interp(u, [0, 0.35, 1], [_VOW[v][i] * fs for v in vw]) for i in range(3)]
        v = _additive_voice(t, f, [(F[0], 90 * fs, 1.0), (F[1], 120 * fs, 0.55), (F[2], 170 * fs, 0.28)], vsr,
                            kmax=30, tilt=0.9)
        env = _bump(t, 0.0, D, 0.04, 0.12)
        y = _nrms(v) * env + 0.04 * rng.standard_normal(m) * env
        if asp:                                              # breathy 'h' onset
            y += 0.35 * _nrms(_filt(rng.standard_normal(m), "bp", (900, 3000), vsr)) * _ar(t, 0.006, 0.03)
        parts += [y, np.zeros(int(rng.uniform(0.04, 0.09) * vsr))]
    return np.concatenate(parts)


def _k_clap(rng, sr, hand):
    """One hand clap: a short noise burst with a hollow cupped-hand resonance (~0.9-1.5 kHz)."""
    m = int(0.05 * sr)
    t = np.arange(m) / sr
    y = _filt(rng.standard_normal(m), "bp", (600, 3500), sr) * _ar(t, 0.0004, rng.uniform(0.006, 0.011))
    y = _norm(y) + 0.8 * _norm(_reson(y, hand * rng.uniform(0.95, 1.05), 3, sr))
    return _norm(_filt(y, "lp", 4000, sr))


# =========================================================================================== one-shots
# Generators may return more than the natural length (decay and reverb tails rendered in full); _render_oneshot
# fits that into NAMES[name][1] with an exponential end fade (END_FADE). Events are timed so each sound has
# decayed by ~40 dB before the fade starts, so nothing is chopped while it still rings.
def _thunder(rng, sr, p):
    L = 3.4
    m = int(L * sr)
    t = np.arange(m) / sr
    tc = 0.03
    crack = np.zeros((m, 2))
    k = int(0.1 * sr)
    tk = np.arange(k) / sr
    for i in range(rng.integers(5, 9)):                   # a cluster of sub-cracks in the first ~0.2 s
        ti = tc + (rng.exponential(0.06) if i else 0.0)
        b = _filt(rng.standard_normal(k), "bp", (200, 3500), sr) * _ar(tk, 0.002, rng.uniform(0.008, 0.025))
        _place(crack, _norm(b) * rng.uniform(0.5, 1.0) * 0.8 ** i, int(ti * sr), rng.uniform(-0.2, 0.2), wrap=False)
    w2 = rng.standard_normal((m, 3))
    w2 = np.stack([0.9 * w2[:, 0] + 0.45 * w2[:, 1], 0.9 * w2[:, 0] + 0.45 * w2[:, 2]], 1)
    crack += 0.5 * _nrms(_filt(w2, "bp", (120, 2000), sr)) * _ar(t - tc, 0.006, 0.18)[:, None]
    crack = np.tanh(1.3 * _norm(crack)) / np.tanh(1.3)
    _dbg("crack", crack)
    env = np.zeros(m)                                     # rolls of the rumble
    rolls = [0.05, rng.uniform(0.35, 0.7), rng.uniform(0.9, 1.3), rng.uniform(1.4, 1.9), rng.uniform(2.0, 2.4)]
    for ti, a in zip(rolls, (1.0, 0.9, 0.75, 0.55, 0.4)):
        env += a * rng.uniform(0.8, 1.1) * _swell(t - ti - 0.15, rng.uniform(0.1, 0.22), rng.uniform(0.22, 0.4))
    env = 0.15 * np.exp(-t / 1.2) * _smoothstep(t / 0.1) + env
    env *= np.exp(-t / 2.2) * _smoothstep((3.2 - t) / 0.9)
    env /= env.max()
    rough = np.clip(1 + 0.7 * _nrms(_filt(rng.standard_normal(m), "lp", 6, sr, 2)), 0.15, None)
    w = rng.standard_normal((m, 3))         # mostly shared noise (L/R corr ~0.8): centred, the width is in the verb
    w = np.stack([0.9 * w[:, 0] + 0.45 * w[:, 1], 0.9 * w[:, 0] + 0.45 * w[:, 2]], 1)
    low = _nrms(_filt(w, "bp", (45, 160), sr))
    body = _nrms(_filt(w, "bp", (150, 450), sr))
    top = _nrms(_filt(w, "bp", (400, 1200), sr))
    rum = (low * env[:, None] + 0.6 * body * (env ** 1.3)[:, None]
           + 0.12 * top * (env ** 2.5)[:, None]) * rough[:, None]
    rum = _norm(rum)
    _dbg("rumble", rum)
    x = 0.7 * crack + rum
    # Partly correlated reverb (and a little less of it): the thunder stays mostly centred (L/R corr ~0.5) so the
    # mixer's pan can place it; the width comes from the reverb only.
    return _verb(x, _ir(rng, sr, 1.2, 0.03, 1800, corr=0.4), 0.6)


def _splash_any(rng, sr, L, big):
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros((m, 2))
    sc = 1.0 if big else 0.7
    th = _k_thump(rng, sr, 110 if big else 160, 70 if big else 95, 0.05 if big else 0.04, noise=0.6,
                  harm=(1.0, 0.6, 0.35))
    _place(x, _norm(th) * 0.7 * sc, 0, 0, wrap=False)
    slap = _nrms(_filt(rng.standard_normal(m), "bp", (500, 6000), sr)) * _ar(t, 0.002, 0.035 if big else 0.03)
    x += (0.8 * slap)[:, None]
    w = rng.standard_normal((m, 3))
    w = np.stack([0.85 * w[:, 0] + 0.5 * w[:, 1], 0.85 * w[:, 0] + 0.5 * w[:, 2]], 1)     # mostly centred
    nz = _nrms(_filt(w, "bp", (300, 1500), sr))
    hz = _nrms(_filt(w[::-1], "bp", (1500, 6000), sr))
    if big:
        e1 = _ar(t, 0.02, 0.2) + 0.5 * _ar(t - 0.2, 0.08, 0.18)
        e2 = _ar(t, 0.01, 0.13) + 0.45 * _ar(t - 0.22, 0.06, 0.16)
        x += 0.65 * nz * e1[:, None] + 0.4 * hz * e2[:, None]
    else:              # crate into water: a fuller 'plunk' (body + plop + wooden knock), short and centred
        x += 0.75 * nz * _ar(t, 0.006, 0.09)[:, None] + 0.45 * hz * _ar(t, 0.003, 0.05)[:, None]
        plop = _k_bubble(sr, rng.uniform(220, 320), 0.06, 2.0, 0.15)
        _place(x, _norm(plop) * 0.9, int(0.004 * sr), 0, wrap=False)
        kn = np.zeros(int(0.2 * sr))
        kn[0] = 1
        knock = _reson(kn, rng.uniform(210, 260), 10, sr) + 0.5 * _reson(kn, rng.uniform(560, 660), 12, sr)
        _place(x, _norm(knock) * 0.4, 0, 0, wrap=False)
    _dbg("impact+body", x)
    dr = np.zeros((m, 2))
    nd = rng.integers(60, 120) if big else rng.integers(15, 30)
    alt = _Alt(rng, 0.05, 0.6)
    for _ in range(nd):
        u = rng.random() ** 1.6
        t0 = (0.12 + 0.8 * u) if big else (0.05 + 0.3 * u)
        a = (1 - 0.75 * u) * rng.uniform(0.15, 0.5)
        _place(dr, _norm(_k_drop_or_tick(rng, sr)) * a, int(t0 * sr), alt(), wrap=False)
    for _ in range(rng.integers(6, 12) if big else rng.integers(3, 6)):
        t0 = rng.uniform(0.08, 0.75) if big else rng.uniform(0.05, 0.3)
        k = _k_bubble(sr, rng.uniform(200, 700), rng.uniform(0.025, 0.05), 1.9)
        _place(dr, k * rng.uniform(0.15, 0.35), int(t0 * sr), alt(), wrap=False)
    _dbg("droplets", dr)
    x = x + dr
    if not big:        # round off the first ~100 ms (soft clip, cross-faded back to linear): a fuller, less spiky plunk
        pk = np.abs(x).max()
        w = _smoothstep((0.1 - t) / 0.03)[:, None]
        x = w * np.tanh(2.0 * x / pk) / np.tanh(2.0) * pk + (1 - w) * x
    return _verb(x, _ir(rng, sr, 0.5, 0.008, 5000), 0.25)


def _splash(rng, sr, p):
    return _splash_any(rng, sr, 1.2, True)


def _splash_small(rng, sr, p):
    return _splash_any(rng, sr, 0.6, False)


def _whoosh(rng, sr, p):
    L = 0.68                          # the swish itself; the natural length adds a little air after it
    m = int(L * sr)
    t = np.arange(m) / sr
    u = t / L
    a, b = 2.0, 3.2
    env = u ** a * (1 - u) ** b
    env /= env.max()
    f_lo, f_hi = rng.uniform(300, 420), rng.uniform(1400, 1900)

    def mask(f, tt):
        uu = np.clip(tt / L, 0, 1)
        fc = f_lo * (f_hi / f_lo) ** np.sin(np.pi * uu ** 0.85)
        return _gauss(np.log(np.maximum(f, 20)), np.log(fc), 0.45)

    y = _nrms(_shaped(rng, m, sr, mask)) * env
    air = _nrms(_filt(rng.standard_normal(m), "lp", 400, sr)) * env * 0.4
    pan = 0.25 * (2 * _smoothstep(u) - 1)
    g = np.stack([np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)], 1) * np.sqrt(2)
    return (y + air)[:, None] * g


def _additive_voice(t, f0, formants, sr, kmax=40, tilt=1.0):
    """Harmonic tone with time-varying f0 shaped by formant resonances: formants = [(F(t), B, gain)]."""
    ph = _osc(f0, sr)
    y = np.zeros(len(t))
    for k in range(1, kmax + 1):
        fk = k * f0
        if np.min(fk) > 0.45 * sr:
            break
        a = np.zeros(len(t))
        for F, B, g in formants:
            a += g / np.sqrt(((F ** 2 - fk ** 2) / (fk * B)) ** 2 + 1)
        y += a * k ** -tilt * np.sin(k * ph) * (fk < 0.45 * sr)
    return y


def _gulp(rng, sr, p):
    L = 0.85
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros(m)
    # 1) wet onset
    k = int(0.1 * sr)
    tk = np.arange(k) / sr
    x[:k] += 0.25 * _nrms(_filt(rng.standard_normal(k), "bp", (400, 1800), sr)) * _ar(tk - 0.01, 0.003, 0.03)

    def add(y, at, g):
        _place(xs, g * y, int(at * sr), wrap=False)

    xs = np.zeros((m, 2))
    add(_norm(_k_bubble(sr, rng.uniform(450, 600), 0.03, 1.6)), 0.012, 0.4)
    # 2) throat swallow: harmonic tone sweeping down through an 'oo' vowel (0.04-0.44 s)
    sw = np.clip((t - 0.05) / 0.36, 0, 1)
    f0 = 75 + 100 * np.exp(-np.maximum(t - 0.05, 0) / 0.14)
    F1 = 330 - 70 * sw
    F2 = 800 - 180 * sw
    v = _additive_voice(t, f0, [(F1, 90, 1.0), (F2, 130, 0.5), (2400, 300, 0.06)], sr, tilt=0.8)
    envv = _smoothstep((t - 0.04) / 0.05) * _smoothstep((0.44 - t) / 0.09) * (1 + 0.25 * np.sin(np.pi * sw))
    x += _norm(v) * envv * 1.0
    # 3) closing bloop, 4) wet pop, 5) slosh + two little bubbles -- all by ~0.5 s, so the tail has rung out
    #    (~-45 dB) before the natural-length end fade starts
    add(_norm(_k_bubble(sr, 120, 0.05, 2.4, 0.2)), 0.385, 0.8)
    kp = int(0.1 * sr)
    tp = np.arange(kp) / sr
    fp = 300 * 3 ** (1 - np.exp(-tp / 0.012))
    pop = (np.sin(_osc(fp, sr)) * _ar(tp, 0.0008, 0.016)
           + 0.15 * _norm(_filt(rng.standard_normal(kp), "lp", 2500, sr)) * _ar(tp, 0.0003, 0.003))
    add(pop, 0.46, 0.6)
    sl = int(0.3 * sr)
    add(_nrms(_filt(rng.standard_normal(sl), "lp", 600, sr)) * _ar(np.arange(sl) / sr, 0.01, 0.05), 0.47, 0.15)
    for _ in range(2):
        add(_norm(_k_bubble(sr, rng.uniform(300, 600), 0.02, 1.8)), rng.uniform(0.48, 0.52), 0.2)
    x = x[:, None] + xs
    _dbg("gulp", x)
    return _verb(x, _ir(rng, sr, 0.35, 0.005, 2500), 0.33)


def _spit(rng, sr, p):
    L = 0.68                     # room for the expelling bloop to ring out (the end fade starts at 0.6 s)
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros((m, 2))
    # pressure hum
    f0 = 110 + 30 * np.clip(t / 0.12, 0, 1)
    hum = _additive_voice(t, f0, [(250, 80, 1.0), (1000, 200, 0.15)], sr, tilt=1.0)
    x += (0.4 * _norm(hum) * _smoothstep(t / 0.08) * _smoothstep((0.125 - t) / 0.01))[:, None]
    tp = 0.12
    # plosive "P"
    pl = _nrms(_filt(rng.standard_normal(m), "bp", (300, 3000), sr)) * _ar(t - tp, 0.001, 0.012)
    x += (0.8 * pl / (np.abs(pl).max() + 1e-9))[:, None]
    th = _k_thump(rng, sr, 140, 80, 0.02, noise=0.4)
    _place(x, _norm(th) * 0.5, int(tp * sr), 0, wrap=False)
    # "tooey": rising voiced glide oo -> ee + a big expelling bloop
    u = np.clip((t - 0.13) / 0.27, 0, 1)
    fv = 160 * 2 ** u
    tooey = _additive_voice(t, fv, [(320, 90, 1.0), (800 + 1400 * u ** 1.5, 150, 0.5), (2600, 300, 0.1)], sr)
    ev = _smoothstep((t - 0.13) / 0.02) * _smoothstep((0.42 - t) / 0.1)
    x += (0.4 * _norm(tooey) * ev)[:, None]
    _place(x, _norm(_k_bubble(sr, 180, 0.07, 3.0, 0.2)) * 0.7, int(0.14 * sr), 0, wrap=False)
    # wet splatter
    alt = _Alt(rng, 0.05, 0.5)
    for _ in range(rng.integers(20, 40)):
        t0 = 0.2 + 0.2 * rng.random() ** 1.3
        _place(x, _norm(_k_drop_or_tick(rng, sr)) * rng.uniform(0.08, 0.3), int(t0 * sr), alt(), wrap=False)
    for _ in range(rng.integers(2, 5)):
        t0 = rng.uniform(0.24, 0.36)
        k = int(0.08 * sr)
        sp = _nrms(_filt(rng.standard_normal(k), "bp", (800, 5000), sr)) * _ar(np.arange(k) / sr, 0.002, 0.025)
        _place(x, sp * 0.18, int(t0 * sr), alt(), wrap=False)
    _dbg("spit", x)
    return x


def _thud(rng, sr, p):
    """Soft landing on sand: a damped low thump (~110 ms body, saturated so phones hear it) with a 250-600 Hz body
    and a soft knock, a smaller settling bump ~70 ms later and a ~150 ms scatter of sand, all within ~0.25 s."""
    L = 0.4
    m = int(L * sr)
    t = np.arange(m) / sr

    def impact(t0, a, f_hi, f_lo, d=1.0):
        tt = np.maximum(t - t0, 0.0)
        on = (t >= t0) * (1 - np.exp(-tt / 0.003))
        th = np.maximum(tt - 0.012 * d, 0.0)                      # a short hold, then a body that the sand damps
        damp = on * np.exp(-th / (0.075 * d) - (th / (0.14 * d)) ** 2)
        ph = _osc(f_lo + (f_hi - f_lo) * np.exp(-tt / 0.015), sr)
        low = _norm((np.sin(ph) + 0.5 * np.sin(2 * ph + 0.3) + 0.25 * np.sin(3 * ph)) * damp)
        low = 0.6 * low + 0.4 * np.tanh(2.5 * low) / np.tanh(2.5)
        body = _nrms(_filt(rng.standard_normal(m), "bp", (250, 600), sr)) * on \
            * np.exp(-tt / (0.05 * d) - (tt / (0.13 * d)) ** 2)
        kn = _reson(rng.standard_normal(m) * _ar(t - t0, 0.001, 0.008), rng.uniform(300, 450), 2.0, sr) \
            * np.exp(-tt / 0.04)
        return a * (0.8 * low + 1.2 * _norm(body) + 1.0 * _norm(kn))

    y = impact(0.0, 1.0, 165, 92, 1.1) + impact(rng.uniform(0.06, 0.08), 0.45, 145, 98, 0.7)
    imp = np.zeros(m)
    ts = rng.exponential(0.045, rng.integers(90, 150))       # ~150 ms scatter of sand grains
    idx = (ts * sr).astype(int)
    idx = idx[idx < m]
    np.add.at(imp, idx, rng.uniform(0.3, 1.0, len(idx)) * rng.choice([-1, 1], len(idx)) * np.exp(-idx / sr / 0.06))
    sand = _norm(_filt(imp, "bp", (600, 3500), sr))
    hiss = _nrms(_filt(rng.standard_normal(m), "bp", (800, 3500), sr)) * _ar(t, 0.003, 0.05)
    y = y + 0.5 * sand + 0.08 * hiss
    # Round off the whole impact (~120 ms; soft clip, cross-faded back to linear for the settling tail): lowers the
    # crest factor so the thud reaches the common one-shot loudness within the peak ceiling without limiting, and
    # its low-order harmonics carry the thump on small speakers.
    pk = np.abs(y).max()
    w = _smoothstep((0.12 - t) / 0.02)
    return w * np.tanh(2.5 * y / pk) / np.tanh(2.5) * pk + (1 - w) * y


def _midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _fold(nn, fmax):
    """MIDI note folded down by octaves until its frequency is <= fmax (stays in key, unlike a frequency clamp)."""
    nn = float(nn)
    while _midi(nn) > fmax:
        nn -= 12
    return nn


def _bell(sr, f, L, tau, rng, partials=((1, 1.0, 1.0), (2.0, 0.25, 0.45), (3.0, 0.08, 0.25), (4.2, 0.05, 0.15),
                                         (5.4, 0.025, 0.1)), att=0.004):
    m = int(L * sr)
    t = np.arange(m) / sr
    y = np.zeros(m)
    for r, a, td in partials:
        if f * r > 7500:
            continue
        for det, g in ((-1, 0.6), (1, 0.4)):          # gentle chorus, same in both channels
            y += g * a * np.sin(TAU * f * r * (1 + det * 0.0006) * t + rng.uniform(0, TAU)) * _ar(t, att, tau * td, 2.0)
    return np.stack([y, y], 1)


def _chime(rng, sr, p):
    L = 2.3                          # bells ring out inside the natural length (reverb tail rendered on top)
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    x = np.zeros((m, 2))
    notes = [0, 4, 7, 12, 16]
    for i, nn in enumerate(notes):
        t0 = 0.07 * i + rng.uniform(-0.01, 0.01)
        f = _midi(_fold(root + nn, 2400))
        _place(x, _bell(sr, f, L - t0, 0.36 * (523 / f) ** 0.3, rng) * 0.5 * (0.9 ** i), int(max(t0, 0) * sr),
               wrap=False)
    _dbg("bells", x)
    pad = np.zeros(m)
    for nn in (0, 4, 7):
        f = _midi(_fold(root - 12 + nn, 1200))
        pad += np.sin(TAU * f * t) + 0.15 * np.sin(TAU * 2 * f * t)
    pad *= _smoothstep(t / 0.4) * np.exp(-np.maximum(t - 0.4, 0) / 0.38) * 0.06       # dies with the bells
    x += pad[:, None]
    _dbg("pad", pad)
    pent = [0, 2, 4, 7, 9]
    side = rng.choice([-1.0, 1.0])
    for _ in range(rng.integers(18, 30)):        # airy sparkle: major-pentatonic pings, alternating sides
        t0 = rng.uniform(0.05, 1.2)
        nn = _fold(root + 24 + pent[rng.integers(5)] + 12 * rng.integers(0, 2), 4700)
        f = _midi(nn)
        k = int(0.3 * sr)
        tk = np.arange(k) / sr
        ping = np.sin(TAU * f * tk) * _ar(tk, 0.0015, rng.uniform(0.04, 0.08))
        side = -side
        _place(x, ping * rng.uniform(0.04, 0.09) * (1 - 0.5 * t0 / 1.2), int(t0 * sr), side * rng.uniform(0.2, 0.6),
               wrap=False)
    air = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (3000, 8000), sr)) * (_ar(t, 0.3, 0.5, 2.0) * 0.02)[:, None]
    x += air
    return _verb(x, _ir(rng, sr, 1.4, 0.02, 6000), 0.5)


def _sparkle(rng, sr, p):
    L = 0.9
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    x = np.zeros((m, 2))
    pent = [0, 2, 4, 7, 9]
    scale = [_fold(root + o * 12 + s, 4700) for o in range(3) for s in pent]
    N = rng.integers(22, 34)
    run = rng.integers(5, 9)
    alt = _Alt(rng, 0.1, 0.5)
    for i in range(N):
        if i < run:                       # opening ascending run
            t0 = 0.035 * i
            nn = scale[min(i * 2, len(scale) - 1)]
        else:                             # glitter thinning out and fading (done by ~0.5 s: rings out by ~0.8 s)
            t0 = 0.1 + 0.4 * rng.random() ** 1.6
            nn = scale[rng.integers(len(scale))]
        f = _midi(nn)
        tau = rng.uniform(0.05, 0.11) * (1 - 0.45 * np.clip((t0 - 0.1) / 0.4, 0, 1))
        k = int(tau * 7 * sr)
        tk = np.arange(k) / sr
        ping = (np.sin(TAU * f * tk) + 0.15 * np.sin(TAU * 2 * f * tk)
                + 0.06 * np.sin(TAU * 2.76 * f * tk) * (2.76 * f < 7500)) * _ar(tk, 0.0015, tau)
        a = rng.uniform(0.5, 1.0) * np.exp(-t0 / 0.35)
        _place(x, ping * a * 0.3, int(t0 * sr), alt(), wrap=False)
    sh = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (2500, 7000), sr))
    am = 0.6 + 0.4 * np.sin(TAU * 18 * t)
    x += sh * (_ar(t, 0.05, 0.18) * am * 0.06)[:, None]
    return _verb(x, _ir(rng, sr, 0.7, 0.012, 7000), 0.42)


def _grow(rng, sr, p):
    """Rising sweep and twinkle run that blooms into a bell at ~1.05 s, then rings out."""
    L = 1.7
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    tb = 1.05                                   # bloom
    f0 = _midi(root - 12) * 0.95
    f = f0 * 4 ** np.clip(t / tb, 0, 1) ** 1.2
    env = _smoothstep(t / 0.25) * (0.35 + 0.65 * np.clip(t / tb, 0, 1)) * _smoothstep((tb + 0.25 - t) / 0.3)
    sw = np.zeros(m)
    for dd in (-0.004, 0.0, 0.004):
        ph = _osc(f * (1 + dd), sr, rng.uniform(0, TAU))
        sw += np.sin(ph) + 0.1 * np.sin(3 * ph) + 0.3 * np.sin(2 * ph)
    y = np.stack([sw, sw], 1) * (env * 0.12)[:, None]
    _dbg("sweep", y)

    def mask(ff, tt):
        fc = 400 * 10 ** np.clip(tt / (tb + 0.1), 0, 1)
        return _gauss(np.log(np.maximum(ff, 20)), np.log(fc), 0.35)

    nz = _nrms(_shaped(rng, m, sr, mask)) * env * 0.12
    y += nz[:, None] * np.array([1.0, 0.9])
    pent = [0, 2, 4, 7, 9]
    scale = [_fold(root + o * 12 + s, 4700) for o in range(3) for s in pent]
    N = rng.integers(10, 16)
    for i in range(N):
        t0 = (tb - 0.05) * (i / N) ** 0.75 + rng.uniform(0, 0.03)
        nn = scale[min(int(i * len(scale) / N), len(scale) - 1)]
        fr = _midi(nn)
        k = int(0.6 * sr)
        tk = np.arange(k) / sr
        ping = (np.sin(TAU * fr * tk) + 0.2 * np.sin(TAU * 2 * fr * tk)) * _ar(tk, 0.002, rng.uniform(0.06, 0.12))
        _place(y, ping * rng.uniform(0.25, 0.45) * 0.5, int(t0 * sr), 0.4 * (-1) ** i, wrap=False)
    _place(y, _bell(sr, _midi(_fold(root + 24, 2400)), 0.9, 0.15, rng) * 0.18, int(tb * sr), wrap=False)
    rate = 50 + 350 * np.clip(t / tb, 0, 1) * (t < tb + 0.05)
    rs = _filt(np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1), "bp", (1500, 5000), sr) * 0.06
    y += rs
    _dbg("twinkles+rustle", y)
    return _verb(y, _ir(rng, sr, 0.9, 0.015, 7000), 0.4)


def _wither(rng, sr, p):
    L = 1.75
    m = int(L * sr)
    t = np.arange(m) / sr
    D = 1.38                     # everything has died away ~0.3 s before the natural-length end fade
    f = 520 * (140 / 520) ** np.clip(t / (D - 0.1), 0, 1) * (1 + 0.02 * np.sin(TAU * 6 * t))
    ph = _osc(f, sr)
    env = _smoothstep(t / 0.05) * np.clip(1 - t / D, 0, 1) ** 1.3
    tone = (np.sin(ph) + 0.11 * np.sin(3 * ph)) * env * 0.6

    def mask(ff, tt):
        fc = 2500 * (500 / 2500) ** np.clip(tt / (D - 0.1), 0, 1)
        return _gauss(np.log(np.maximum(ff, 20)), np.log(fc), 0.5)

    hiss = _nrms(_shaped(rng, m, sr, mask)) * _ar(t, 0.03, 0.4) * 0.4
    x = np.stack([tone + hiss, tone + hiss], 1)
    rate = (300 * np.exp(-t / 0.5) + 40) * _smoothstep((1.18 - t) / 0.2)
    cr = _filt(np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1), "bp", (1500, 6000), sr)
    x += 0.35 * _norm(cr)
    alt = _Alt(rng, 0.1, 0.4)
    for _ in range(rng.integers(5, 9)):
        k = int(0.06 * sr)
        b = _nrms(_filt(rng.standard_normal(k), "bp", (2000, 5000), sr)) * _ar(np.arange(k) / sr, 0.002, 0.015)
        _place(x, b * 0.12, int(rng.uniform(0.05, 1.1) * sr), alt(), wrap=False)
    for t0 in (rng.uniform(0.92, 1.0), rng.uniform(1.08, 1.16)):     # a leaf or two dropping
        _place(x, _norm(_k_thump(rng, sr, 180, 120, 0.02, noise=0.6)) * 0.12, int(t0 * sr), alt(), wrap=False)
    _dbg("wither", x)
    return _verb(x, _ir(rng, sr, 0.6, 0.008, 5000), 0.25)


def _crunch(rng, sr, p):
    L = 1.2
    m = int(L * sr)
    x = np.zeros((m, 2))
    t0, i = 0.02, 0
    nb = rng.integers(6, 10)
    while i < nb and t0 < 0.95:
        a = rng.uniform(0.75, 1.0)
        _place(x, _k_bite(rng, sr) * a, int(t0 * sr), rng.uniform(-0.15, 0.15), wrap=False)
        i += 1
        t0 += rng.uniform(0.1, 0.17) + (0.15 if i % 3 == 0 else 0.0)
    return _verb(x, _ir(rng, sr, 0.35, 0.005, 5000), 0.15)


def _k_bite(rng, sr):
    """One nibble: a dense burst of crisp fragments over a short 400-1500 Hz 'snap' body, gently compressed."""
    k = int(0.12 * sr)
    t = np.arange(k) / sr
    imp = np.zeros(k)
    sp = rng.uniform(0.02, 0.04)
    ts = rng.exponential(sp, rng.integers(50, 90))
    idx = (ts * sr).astype(int)
    idx = idx[idx < k]
    np.add.at(imp, idx, rng.uniform(0.4, 1.0, len(idx)) * rng.choice([-1, 1], len(idx))
              * np.exp(-ts[ts * sr < k] / 0.05))
    cr = _norm(_filt(imp, "bp", (1200, 4500), sr))
    body = _norm(_filt(rng.standard_normal(k), "bp", (400, 1500), sr) * _ar(t, 0.002, 0.025))
    tick = np.sin(TAU * 230 * t) * _ar(t, 0.001, 0.01)
    y = 0.65 * cr + 0.6 * body + 0.2 * tick
    y = np.tanh(1.8 * y / np.abs(y).max()) / np.tanh(1.8)          # per-bite compressor: tames the spikiest grain
    return _fade(y, sr, 0.0, 0.01)


def _gull(rng, sr, p):
    L = 1.15
    m = int(L * sr)
    x = np.zeros(m)
    pitch = float(p["pitch"])
    ncalls = int(p["calls"]) if p["calls"] is not None else int(rng.integers(2, 4))
    t0 = 0.02
    base = rng.uniform(850, 1050) * pitch
    for i in range(ncalls):
        D = rng.uniform(0.24, 0.34) * (0.9 ** i) * (1.0 if ncalls <= 3 else 3.0 / ncalls)
        if t0 + D > 0.86:                    # the calls (and their echo) are over well before the end fade
            break
        k = int(D * sr)
        tt = np.arange(k) / sr
        u = tt / D
        f0 = base * (0.93 ** i) * np.interp(u, [0, 0.2, 0.45, 1.0], [0.9, 1.55, 1.45, 0.85])
        f0 *= 1 + 0.015 * _pnoise(rng, D, 30)(tt)
        ph = _osc(f0, sr)
        y = np.zeros(k)
        for h in range(1, 11):
            fh = h * f0
            a = h ** -0.6 * (0.3 + _gauss(fh, 1900, 500) + 0.6 * _gauss(fh, 3300, 600)) * (fh < 0.45 * sr)
            y += a * np.sin(h * ph)
        rough = 1 + 0.25 * _nrms(_filt(rng.standard_normal(k), "lp", 120, sr))
        env = _smoothstep(tt / 0.02) * _smoothstep((D - tt) / 0.06)
        j = int(t0 * sr)
        x[j:j + k] += _norm(y * rough * env) * (0.8 ** i)
        t0 += D + rng.uniform(0.06, 0.11)
    x = _filt(x, "lp", 6000, sr)
    return _verb(x, _ir(rng, sr, 0.55, 0.02, 4000), 0.3)


def _lots(rng, sr, p):
    """Lots being cast: wooden sticks rattled in a clay jar (dense clicks through the jar's 450-650 Hz body
    resonance), then one stick dropping out and bouncing."""
    L = 1.15
    m = int(L * sr)
    x = np.zeros((m, 2))
    nsh = rng.integers(3, 5)
    sp = rng.uniform(0.14, 0.17)
    for s in range(nsh):
        ts = 0.03 + s * sp
        for _ in range(rng.integers(14, 26)):
            tc = ts + rng.gamma(2.0, 0.018)
            _place(x, _k_click(rng, sr, rng.random() < 0.5) * rng.uniform(0.35, 1.0), int(tc * sr),
                   -0.1 + rng.uniform(-0.12, 0.12), wrap=False)
    jar = np.zeros_like(x)                          # the jar body ringing under the rattle
    for fj, q, g in ((rng.uniform(450, 520), 8, 1.0), (rng.uniform(580, 650), 9, 0.6),
                     (rng.uniform(1050, 1250), 10, 0.3)):
        jar += g * _reson(x, fj, q, sr)
    x = 0.55 * x + 0.9 * _norm(jar) * np.abs(x).max()
    td = 0.03 + nsh * sp + rng.uniform(0.06, 0.1)
    for dt, a in ((0.0, 1.0), (0.08, 0.45), (0.13, 0.2)):
        _place(x, _k_tock(rng, sr) * a * 0.9, int((td + dt * rng.uniform(0.9, 1.1)) * sr), 0.15, wrap=False)
    return _verb(x, _ir(rng, sr, 0.4, 0.006, 6000), 0.22)


def _k_click(rng, sr, jar):
    k = int(0.06 * sr)
    imp = np.zeros(k)
    imp[0] = 1
    y = _reson(imp, rng.uniform(1800, 3200), 12, sr) + 0.3 * _reson(imp, rng.uniform(3600, 5000), 14, sr)
    if jar:
        y = 0.6 * _norm(y) + 0.5 * _norm(_reson(imp, rng.uniform(480, 620), 10, sr))
    return _norm(y)


def _k_tock(rng, sr):
    k = int(0.2 * sr)
    imp = np.zeros(k)
    imp[0] = 1
    y = _reson(imp, rng.uniform(850, 1100), 22, sr) + 0.5 * _reson(imp, rng.uniform(2300, 2800), 25, sr)
    return _norm(y)


def _cloth(rng, sr, p):
    L = 0.6
    m = int(L * sr)
    t = np.arange(m) / sr
    g1 = _swell(t - rng.uniform(0.09, 0.12), 0.07, 0.06)
    g2 = 0.75 * _swell(t - rng.uniform(0.25, 0.29), 0.07, 0.05)
    env = g1 + g2
    fr = 0.65 + 0.35 * np.abs(_nrms(_filt(rng.standard_normal(m), "lp", 40, sr))) / 2

    def mask(f, tt):
        return _bpm(f, 600, 5000) * _pinkm(f, 2000, 0.3)

    y = np.stack([_nrms(_shaped(rng, m, sr, mask)) for _ in range(2)], 1)
    y = 0.85 * y[:, :1] + 0.3 * y
    y *= (env * fr * 0.5)[:, None]
    rate = 150 * env
    cr = _filt(np.stack([_dust(rng, rate, sr, even=True), _dust(rng, rate, sr, even=True)], 1), "bp", (2500, 6000), sr)
    return y + 0.1 * _norm(cr)


def _sheep(rng, sr, p):
    L = 0.95
    m = int(L * sr)
    t = np.arange(m) / sr
    pitch = float(p["pitch"])
    D = rng.uniform(0.56, 0.64)
    base = rng.uniform(230, 270) * pitch
    vr = rng.uniform(6.5, 8.5)
    contour = np.interp(t, [0, 0.13, D], [0.92, 1.05, 0.9])
    f0 = base * contour * (1 + 0.04 * np.sin(TAU * vr * t))
    on = np.clip(t / 0.05, 0, 1)
    F1 = 400 + 380 * on
    F2 = 1100 + 450 * on - 200 * np.clip((t - 0.35) / 0.35, 0, 1)
    v = _additive_voice(t, f0, [(F1, 110, 1.0), (F2, 150, 0.6), (2700 + 0 * t, 250, 0.25), (3700 + 0 * t, 300, 0.1)],
                        sr, tilt=1.0)
    am = 1 - 0.35 * (0.5 + 0.5 * np.sin(TAU * vr * t - 0.5))
    env = _smoothstep(t / 0.04) * _smoothstep((D - t) / 0.12) * am * (t < D)
    y = _norm(v) * env

    def mask(f, tt):
        return 0.02 + _gauss(f, 780, 150) + 0.6 * _gauss(f, 1500, 200) + 0.25 * _gauss(f, 2700, 300)

    br = _nrms(_shaped(rng, m, sr, mask)) * env * 0.06
    return _verb(y + br, _ir(rng, sr, 0.4, 0.01, 5000), 0.2)


def _pop(rng, sr, p):
    """Light cartoon pop: a rising 'bloop' with a ~40 ms body, a soft low thump under it and a puff of air."""
    L = 0.35
    m = int(L * sr)
    t = np.arange(m) / sr
    s = rng.uniform(0.9, 1.1)
    f = (380 + 620 * (1 - np.exp(-t / 0.01))) * s
    y = np.sin(_osc(f, sr)) * _ar(t, 0.0008, 0.035)
    y += 0.45 * np.sin(_osc(np.full(m, 240.0 * s), sr)) * _ar(t, 0.001, 0.03)
    y = np.tanh(1.6 * y) / np.tanh(1.6)
    y += 0.12 * _nrms(_filt(rng.standard_normal(m), "bp", (2000, 6000), sr)) * _ar(t, 0.0005, 0.012)
    return y


def _coins(rng, sr, p):
    """A few small coins dropped into a cupped hand: a soft palm pat as the first lands, short bright coin-on-coin
    clinks (inharmonic disc modes kept below 6.5 kHz, quickly damped by the hand) and a little settling jingle that
    starts by 0.26 s; all done by ~0.38 s."""
    L = 0.8
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros((m, 2))
    t1 = 0.02
    pat = _nrms(_filt(rng.standard_normal(m), "bp", (150, 900), sr)) * _ar(t - t1, 0.002, 0.025)
    pat += 0.6 * np.sin(_osc(np.full(m, rng.uniform(170, 220)), sr)) * _ar(t - t1, 0.003, 0.03)
    x += 0.3 * _norm(pat)[:, None]
    alt = _Alt(rng, 0.05, 0.3)
    tc, i = t1, 0
    nc = rng.integers(4, 7)
    while i < nc and tc < 0.22:
        a = (1.0 if i == 0 else rng.uniform(0.55, 0.9)) * (1 - 0.06 * i)
        k = _k_clink(rng, sr, rng.uniform(1400, 2400), rng.uniform(0.025, 0.045) * (1 - 0.06 * i))
        _place(x, k * a, int(tc * sr), alt(), wrap=False)
        i += 1
        tc += rng.uniform(0.035, 0.075)
    tc = min(tc, 0.26)              # the jingle settles in time (the tail before the end fade stays below -40 dB)
    for _ in range(rng.integers(2, 4)):                       # settling jingle
        tc += rng.uniform(0.012, 0.025)
        k = _k_clink(rng, sr, rng.uniform(1700, 2600), rng.uniform(0.015, 0.025))
        _place(x, k * rng.uniform(0.2, 0.35), int(tc * sr), alt(), wrap=False)
    _dbg("coins", x)
    return _verb(x, _ir(rng, sr, 0.25, 0.004, 6000), 0.15)


def _k_clink(rng, sr, f0, tau):
    """One coin clink: a few inharmonic disc modes (below 6.5 kHz, upper ones softer and dying faster) and a tiny
    contact tick."""
    m = int(tau * 8 * sr)
    t = np.arange(m) / sr
    y = np.zeros(m)
    for r, a, td in ((1.0, 1.0, 1.0), (1.47, 0.7, 0.8), (2.09, 0.45, 0.6), (2.56, 0.25, 0.5), (3.42, 0.12, 0.4)):
        f = f0 * r * rng.uniform(0.98, 1.02)
        if f < 6500:
            y += a * np.sin(TAU * f * t + rng.uniform(0, TAU)) * _ar(t, 0.0003, tau * td)
    tick = _filt(rng.standard_normal(m), "bp", (2000, 6000), sr) * _ar(t, 0.0001, 0.0006)
    return _norm(y + 0.3 * _norm(tick))


def _horn(rng, sr, p):
    """Herald's ram's horn (shofar): a low call, a slur up about a fifth and a long held top note that sags a little
    at the end. Additive brass (pulse-like lip buzz whose harmonics brighten as each note swells, a horn-bell
    resonance near 900 Hz, rolled off above ~3 kHz so it stays warm), a breathy 'blat' at each onset, gentle
    roughness, and an open-air echo off the city walls; done by ~1.4 s."""
    L = 2.0
    m = int(L * sr)
    t = np.arange(m) / sr
    f1 = rng.uniform(200, 235) * float(p["pitch"])
    f2 = f1 * rng.uniform(1.47, 1.52)                       # about a fifth up (the next natural horn partial)
    d1, d2 = rng.uniform(0.3, 0.38), rng.uniform(0.22, 0.28)
    s1 = 0.04
    s2 = s1 + d1 + rng.uniform(0.06, 0.09)
    s3 = s2 + d2 + rng.uniform(0.05, 0.07)
    d3 = min(rng.uniform(0.45, 0.55), 1.38 - s3)
    notes = [(s1, d1, 0.94 * f1, f1, 0.8), (s2, d2, 1.08 * f1, f2, 0.9), (s3, d3, 0.97 * f2, f2, 1.0)]
    f0 = np.full(m, f1)
    env = np.zeros(m)
    for s, d, fa, fb, g in notes:
        tt = t - s
        seg = (t >= s - 0.03) & (t < s + d + 0.1)          # (gaps between notes are >= 0.05 s)
        f0[seg] = (fb + (fa - fb) * np.exp(-np.maximum(tt, 0) / 0.035))[seg]          # lip scoop into the note
        env += g * _smoothstep(tt / 0.05) * (0.85 + 0.15 * np.clip(tt / d, 0, 1)) * _smoothstep((d - tt) / 0.08)
    s, d = notes[-1][:2]
    f0 *= 1 - 0.05 * _smoothstep((t - (s + d - 0.2)) / 0.2)                          # the last note sags
    f0 *= 1 + 0.004 * _pnoise(rng, L, 6)(t)
    ph = _osc(f0, sr)
    rough = np.clip(1 + 0.12 * _nrms(_filt(rng.standard_normal(m), "lp", 60, sr)), 0.5, None)
    y = np.zeros(m)
    for k in range(1, 24):
        fk = k * f0
        if fk.min() > 4500:
            break
        a = np.exp(-(k - 1) * (0.55 - 0.3 * env)) * (1 + 1.5 * _gauss(fk, 900, 450)) * _lpm(fk, 3000, 2)
        y += a * np.cos(k * ph) * (fk < 4500)
    y = _norm(y * env * rough)
    blat = np.zeros(m)
    for s, *_ in notes:
        blat += _ar(t - s, 0.003, 0.03)
    y += 0.12 * _nrms(_filt(rng.standard_normal(m), "bp", (300, 2000), sr)) * blat
    y += 0.025 * _nrms(_filt(rng.standard_normal(m), "bp", (800, 3000), sr)) * env
    _dbg("horn", y)
    return _verb(y, _ir(rng, sr, 0.7, 0.03, 3000, taps=((0.12, 0.3), (0.26, 0.15))), 0.3)


def _hammer(rng, sr, p):
    """A wooden mallet knocking a stake / pole into the ground: 3-4 knocks ~0.25 s apart, each a soft contact click,
    a short low thump of the mallet and the pole ringing briefly at its wood modes (which rise a little as the stake
    goes in); the last knock lighter. Small open-air reverb; done by ~0.9 s."""
    L = 1.3
    m = int(L * sr)
    x = np.zeros((m, 2))
    f = rng.uniform(380, 480)
    nk = rng.integers(3, 5)
    t0 = 0.02
    alt = _Alt(rng, 0.03, 0.15)
    for i in range(nk):
        a = (0.7 if i == nk - 1 else 1.0) * rng.uniform(0.85, 1.0)
        _place(x, _k_mallet(rng, sr, f * (1 + 0.025 * i)) * a, int(t0 * sr), alt(), wrap=False)
        t0 += rng.uniform(0.21, 0.26)
    _dbg("knocks", x)
    return _verb(x, _ir(rng, sr, 0.4, 0.008, 5000), 0.18)


def _k_mallet(rng, sr, f):
    """One wooden mallet knock: a soft contact click, a short low thump and a pole ringing at three wood modes."""
    k = int(0.4 * sr)
    t = np.arange(k) / sr
    y = np.zeros(k)
    for r, a, tau in ((1.0, 1.0, rng.uniform(0.045, 0.06)), (rng.uniform(2.6, 2.9), 0.45, 0.025),
                      (rng.uniform(5.0, 5.6), 0.18, 0.012)):
        y += a * np.sin(TAU * f * r * t) * _ar(t, 0.0006, tau)
    click = _nrms(_filt(rng.standard_normal(k), "bp", (1200, 5000), sr)) * _ar(t, 0.0002, 0.0015)
    body = _filt(rng.standard_normal(k), "bp", (500, 1800), sr) * _ar(t, 0.0005, 0.008)
    th = np.zeros(k)
    _add(th, _k_thump(rng, sr, 190, 120, 0.03, noise=0.5), 0.0, sr)
    y = 0.9 * _norm(y) + 0.35 * click + 0.45 * _norm(body) + 0.5 * _norm(th)
    return np.tanh(1.5 * y / np.abs(y).max()) / np.tanh(1.5)


def _rooster(rng, sr, p):
    """Gentle, friendly rooster crow at dawn ('cock-a-doodle-doo', ~1.1 s): three short voiced syllables climbing in
    pitch and a long last one (~0.65 s) that holds high and then falls away. A nasal, harmonic-rich call (formants
    near 1 kHz, 2 kHz and 2.7 kHz over a flat harmonic tilt, so harmonics 2-5 sit within ~12 dB of the fundamental)
    but only a soft rasp, a little distance (short open-air reverb) and nothing above the 5 kHz low-pass; done by
    ~1.2 s."""
    L = 1.6
    m = int(L * sr)
    t = np.arange(m) / sr
    base = rng.uniform(430, 500) * float(p["pitch"])
    j = rng.uniform(0.97, 1.03, 4)
    syl = [  # (start, duration, pitch knots over u = 0..1, (F1, F2), gain, attack, release)
        (0.03, 0.11 * j[0], (0.95, 1.1), (950, 1800), 0.6, 0.012, 0.03),
        (0.18, 0.09 * j[1], (1.1, 1.2), (1050, 2050), 0.65, 0.012, 0.03),
        (0.31, 0.16 * j[2], (1.2, 1.38), (900, 1850), 0.85, 0.015, 0.04),
        (0.51, 0.64 * j[3], (1.32, 1.5, 1.52, 1.48, 1.38, 1.12), (1000, 2150), 1.0, 0.03, 0.2),
    ]
    f0 = np.full(m, base)
    env = np.zeros(m)
    F1 = np.full(m, 950.0)
    F2 = np.full(m, 1900.0)
    for s, d, kn, (a1, a2), g, att, rel in syl:
        u = (t - s) / d
        seg = (u >= -0.15) & (u <= 1.25)
        f0[seg] = base * np.interp(u[seg], np.linspace(0, 1, len(kn)), kn)
        F1[seg], F2[seg] = a1, a2 * np.interp(u[seg], [0, 1], [1.0, 0.88])
        env += g * _bump(t, s, d, att, rel)
    f0 = ndimage.gaussian_filter1d(f0, 0.008 * sr) * (1 + 0.012 * _pnoise(rng, L, 25)(t))
    F1, F2 = (ndimage.gaussian_filter1d(F, 0.01 * sr) for F in (F1, F2))
    # Formant-shaped harmonics as in _additive_voice, but in cosine phase: a pulse-like (syrinx) waveform whose crest
    # factor lets the crow reach the common one-shot loudness inside the peak range (sine phase is too 'round').
    ph = _osc(f0, sr)
    v = np.zeros(m)
    for k in range(1, 13):
        fk = k * f0
        a = sum(g / np.sqrt(((F ** 2 - fk ** 2) / (fk * B)) ** 2 + 1) for F, B, g in ((F1, 260, 1.0), (F2, 300, 0.5),
                                                                                    (2700.0, 400, 0.2)))
        v += a * k ** -0.7 * np.cos(k * ph) * (fk < 0.45 * sr)
    rasp = np.clip(1 + 0.18 * _nrms(_filt(rng.standard_normal(m), "bp", (60, 160), sr)), 0.3, None)
    y = _norm(v * rasp) * env
    y += 0.03 * _nrms(_filt(rng.standard_normal(m), "bp", (1000, 3500), sr)) * env
    _dbg("crow", y)
    return _verb(y, _ir(rng, sr, 0.35, 0.025, 4500), 0.25)


_LOOPS = {
    "waves_calm": _waves_calm, "waves_storm": _waves_storm, "storm_wind": _storm_wind, "rain": _rain,
    "wind_soft": _wind_soft, "wind_hot": _wind_hot, "ship_creak": _ship_creak, "underwater": _underwater,
    "bubbles": _bubbles, "heartbeat": _heartbeat, "drip": _drip, "footsteps": _footsteps,
    "footsteps_run": _footsteps_run, "crowd": _crowd, "birds": _birds, "snore": _snore, "heat": _heat,
    "oars": _oars, "fire": _fire, "night": _night, "cheer": _cheer,
}
_ONESHOTS = {
    "thunder": _thunder, "splash": _splash, "splash_small": _splash_small, "whoosh": _whoosh, "gulp": _gulp,
    "spit": _spit, "thud": _thud, "chime": _chime, "sparkle": _sparkle, "grow": _grow, "wither": _wither,
    "crunch": _crunch, "gull": _gull, "lots": _lots, "cloth": _cloth, "sheep": _sheep, "pop": _pop,
    "coins": _coins, "horn": _horn, "hammer": _hammer, "rooster": _rooster,
}
assert set(_LOOPS) | set(_ONESHOTS) == set(NAMES)
assert all(NAMES[k][0] == "loop" for k in _LOOPS) and all(NAMES[k][0] == "oneshot" for k in _ONESHOTS)
