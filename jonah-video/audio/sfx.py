"""Procedural sound-effect library for 约拿的故事: every sound is synthesised from code (no samples).

API (used by audio/mix.py, keep exactly):

    make(name, dur, sr=48000, seed=0, **params) -> np.float32 array, shape (n, 2)
    NAMES = {name: (kind, default_dur_seconds, description)}       kind: 'loop' | 'oneshot'

Loops      ``dur`` is required (0.5 s .. 40 s+; ``None`` falls back to the default). The result is a seamless
           circular loop: every component is periodic in ``dur`` (periodic random LFOs, events wrapped around the
           end, reverb tails folded back to the start, noise beds cross-faded at the seam), and the loop is rotated
           so it starts and ends on a quiet near-zero sample, so there is no click at either end or at the seam.
           Integrated loudness is LOOP_LUFS[name] (-24..-20 LUFS). Renders shorter than REF_DUR are levelled
           against a REF_DUR render of the same seed, so a 0.5 s and a 40 s render sit at the same level.
One-shots  ``dur=None`` gives the natural length (NAMES default). A given ``dur`` trims (with a 15 ms fade) or
           pads with silence. Sample peak is ONESHOT_PEAK[name] (0.5..0.7), mostly centred.

Deterministic for (name, dur, sr, seed, params); different seeds give different variations. Unknown names raise
ValueError. Unknown params are ignored with a warning; supported params are listed in PARAMS (every effect also
accepts ``width``: stereo width multiplier, 1 = as designed, 0 = mono).

Character: a soft, warm children's picture book (cartoony for gulp, spit, snore and pop), never harsh. Everything
is high-passed at 35 Hz (small speakers) and gently low-passed where the material allows.

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
    # ---- one-shots (dur=None -> natural length)
    "thunder": ("oneshot", 3.6, "crack + long deep rolling rumble, not ear-splitting"),
    "splash": ("oneshot", 1.5, "big body splash with falling droplets"),
    "splash_small": ("oneshot", 0.8, "crate plopping into water"),
    "whoosh": ("oneshot", 0.8, "soft swish"),
    "gulp": ("oneshot", 1.0, "big cartoon gulp: low sweep + wet pop"),
    "spit": ("oneshot", 0.8, "cartoon 'ptooey': big bloop expelling + wet splatter"),
    "thud": ("oneshot", 0.4, "soft landing on sand"),
    "chime": ("oneshot", 2.6, "warm divine shimmer: celesta major chord + airy sparkle"),
    "sparkle": ("oneshot", 1.2, "magical glitter"),
    "grow": ("oneshot", 2.0, "rising magical sweep with twinkles"),
    "wither": ("oneshot", 2.0, "descending dry rustle / deflate"),
    "crunch": ("oneshot", 1.5, "small nibbling crunches"),
    "gull": ("oneshot", 1.5, "seagull calls"),
    "lots": ("oneshot", 1.5, "wooden sticks rattling in a jar, then one dropping"),
    "cloth": ("oneshot", 0.8, "fabric rustle"),
    "sheep": ("oneshot", 1.0, "gentle sheep 'baa'"),
    "pop": ("oneshot", 0.3, "light pop"),
}

LOOP_LUFS = {
    "waves_calm": -22.0, "waves_storm": -20.5, "storm_wind": -21.0, "rain": -22.0, "wind_soft": -23.5,
    "wind_hot": -22.0, "ship_creak": -23.0, "underwater": -22.5, "bubbles": -23.0, "heartbeat": -22.0,
    "drip": -23.0, "footsteps": -22.0, "footsteps_run": -21.5, "crowd": -23.0, "birds": -23.0, "snore": -22.0,
    "heat": -24.0,
}

ONESHOT_PEAK = {
    "thunder": 0.6, "splash": 0.65, "splash_small": 0.6, "whoosh": 0.55, "gulp": 0.65, "spit": 0.6, "thud": 0.6,
    "chime": 0.5, "sparkle": 0.5, "grow": 0.55, "wither": 0.55, "crunch": 0.6, "gull": 0.55, "lots": 0.6,
    "cloth": 0.5, "sheep": 0.6, "pop": 0.55,
}

# Optional per-effect params and their defaults (``width`` is accepted everywhere).
PARAMS = {
    "waves_calm": {"density": 1.0}, "waves_storm": {"density": 1.0}, "rain": {"density": 1.0},
    "ship_creak": {"density": 1.0}, "bubbles": {"density": 1.0}, "drip": {"density": 1.0},
    "crowd": {"density": 1.0}, "birds": {"density": 1.0},
    "heartbeat": {"bpm": 50.0}, "footsteps": {"rate": 2.0}, "footsteps_run": {"rate": 4.0},
    "snore": {"cycle": 3.5},
    "chime": {"root": 72}, "sparkle": {"root": 79}, "grow": {"root": 67},
    "sheep": {"pitch": 1.0}, "gull": {"pitch": 1.0, "calls": None},
}

# Final filtering per effect: (high-pass Hz, low-pass Hz or None).
_FINISH = {
    "waves_calm": (35, 9000), "waves_storm": (35, 7000), "storm_wind": (35, 7500), "rain": (35, 8500),
    "wind_soft": (35, 7000), "wind_hot": (35, 8000), "ship_creak": (35, 5000), "underwater": (35, 3500),
    "bubbles": (35, 5000), "heartbeat": (35, 1500), "drip": (35, 6000), "footsteps": (35, 7000),
    "footsteps_run": (35, 7000), "crowd": (35, 4000), "birds": (35, 7000), "snore": (35, 5000),
    "heat": (35, 7000),
    "thunder": (35, 6000), "splash": (35, 8000), "splash_small": (35, 8000), "whoosh": (35, 7000),
    "gulp": (35, 6000), "spit": (35, 7000), "thud": (35, 6000), "chime": (35, 10000), "sparkle": (35, 8000),
    "grow": (35, 9000), "wither": (35, 7500), "crunch": (35, 7000), "gull": (35, 6500), "lots": (35, 8000),
    "cloth": (35, 7000), "sheep": (35, 6000), "pop": (35, 8000),
}

_DEBUG = None      # tools/sfx_audition.py --debug sets a list here to collect component levels


def _dbg(label, x):
    if _DEBUG is not None:
        x = np.asarray(x, float)
        rms = np.sqrt(np.mean(x ** 2)) if x.size else 0.0
        _DEBUG.append((label, 20 * np.log10(rms + 1e-12), 20 * np.log10(np.abs(x).max() + 1e-12) if x.size else -240))


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
    if kind == "loop":
        T = float(default if dur is None else dur)
        n = int(round(T * sr))
        if n <= 0:
            return np.zeros((0, 2), np.float32)
        x = _render_loop(name, n, sr, seed, p)
    else:
        x = _render_oneshot(name, sr, seed, p)
        if dur is not None:
            x = _fit_len(x, int(round(float(dur) * sr)), sr)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    return np.ascontiguousarray(x, dtype=np.float32)


def _render_loop(name, n, sr, seed, p):
    m = max(n, int(0.25 * sr))
    x = _loop_core(name, m, sr, seed, p)
    nref = int(REF_DUR * sr)
    ref = x if m >= nref else _loop_core(name, nref, sr, seed, p)
    lufs = _lufs(ref, sr)
    if np.isfinite(lufs):
        x = x * 10 ** ((LOOP_LUFS[name] - lufs) / 20)
    pk = np.abs(x).max()
    if pk > 0.9:
        x *= 0.9 / pk
    x = _rotate_quiet(x, sr)
    if m != n:                    # below the documented range: cut and fade (not seamless)
        x = _fade(x[:n], sr, 0.004, 0.004)
    return x


def _loop_core(name, n, sr, seed, p):
    rng = _rng(name, seed)
    x = _stereo(_LOOPS[name](rng, n, sr, p))
    hp, lp = _FINISH[name]
    x = _fft_shape(x, sr, lambda f: _hpm(f, hp, 4) * (_lpm(f, lp, 2) if lp else 1.0))
    return _width(x, p["width"])


def _render_oneshot(name, sr, seed, p):
    rng = _rng(name, seed)
    x = _stereo(_ONESHOTS[name](rng, sr, p))
    hp, lp = _FINISH[name]
    x = _filt(x, "hp", hp, sr, 4)
    if lp:
        x = _filt(x, "lp", lp, sr, 2)
    x = _width(x, p["width"])
    L = int(round(NAMES[name][1] * sr))
    x = _fit_len(x, L, sr, fade=min(0.12, 0.25 * NAMES[name][1]))
    x = _fade(x, sr, 0.002, 0.0)
    pk = np.abs(x).max()
    if pk > 0:
        x = x * (ONESHOT_PEAK[name] / pk)
    return x


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


def _fit_len(x, m, sr, fade=0.015):
    if len(x) >= m:
        return _fade(x[:m], sr, 0.0, min(fade, m / sr / 4))
    return np.concatenate([x, np.zeros((m - len(x),) + x.shape[1:], x.dtype)])


def _lufs(x, sr):
    import pyloudnorm as pyln
    try:
        return pyln.Meter(sr).integrated_loudness(np.asarray(x, np.float64))
    except Exception:          # pragma: no cover - too short etc.
        return float("nan")


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


def _ptimes(rng, T, gap, jitter=0.4):
    """Irregular event times on the circle [0, T), mean spacing ``gap`` (count randomly rounded)."""
    k = int(np.floor(T / gap + rng.random()))
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


def _dust(rng, rate, sr):
    """Random signed impulses; ``rate`` = per-sample array of events/second. Exponential amplitudes."""
    hit = np.flatnonzero(rng.random(len(rate)) < np.clip(np.asarray(rate) / sr, 0, 1))
    out = np.zeros(len(rate))
    out[hit] = rng.exponential(1.0, len(hit)) * rng.choice([-1.0, 1.0], len(hit))
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
def _ir(rng, sr, t60=1.0, pre=0.01, lp=5000.0, taps=()):
    """Stereo decaying-noise impulse response (high frequencies die faster), unit energy per channel.
    taps: (delay_s, gain) discrete reflections relative to the diffuse level."""
    L = int(sr * (pre + 1.1 * t60)) + 1
    t = np.arange(L) / sr
    tt = np.maximum(t - pre, 0.0)
    gate = (t >= pre) * (1 - np.exp(-tt / 0.003)) * _smoothstep((t[-1] - t) / (0.1 * t60))
    ir = np.zeros((L, 2))
    ed = np.sqrt(sr * t60 / 13.8)
    for ch in range(2):
        w = rng.standard_normal(L)
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
    ir = _filt(ir, "lp", lp, sr, 2)
    ir /= np.sqrt(np.sum(ir ** 2, axis=0, keepdims=True)) + 1e-12
    return ir


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
    m = int(sr * tau * 6)
    t = np.arange(m) / sr
    f = f0 * (1 + (rise - 1) * (1 - np.exp(-t / (1.5 * tau))))
    ph = _osc(f, sr)
    return _ar(t, 0.0015, tau) * (np.sin(ph) + h2 * np.sin(2 * ph))


def _k_thump(rng, sr, f0, f1, tau, noise=0.3, att=0.003, p=1.0, nlp=300):
    m = int(sr * tau * 7)
    t = np.arange(m) / sr
    f = f1 + (f0 - f1) * np.exp(-t / (tau * 0.4))
    ph = _osc(f, sr)
    y = (np.sin(ph) + 0.4 * np.sin(2 * ph + 0.5) + 0.15 * np.sin(3 * ph)) * _ar(t, att, tau, p)
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
    laps = []
    for t0 in _ptimes(rng, T, 4.6 / p["density"], 0.45):
        a, rise, fall = rng.uniform(0.55, 1.0), rng.uniform(1.1, 2.0), rng.uniform(0.9, 1.5)
        g = _pan(rng.uniform(-0.55, 0.55))[:, None]
        S += a * g * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
        Fz += a * g * C.ev(t0 + 0.25, -0.5, 6 * 1.8 * fall, lambda d: _swell(d, 0.5, 1.8 * fall))
        for _ in range(rng.integers(1, 4)):
            laps.append((t0 + rng.uniform(0.35, 2.4), a * rng.uniform(0.35, 1.0), rng.uniform(-0.6, 0.6)))
    lev = 0.30 * (1 + 0.3 * _pnoise(rng, T, 0.12)(C.t))
    bfc = 430 + 130 * _pnoise(rng, T, 0.05)(C.t)

    def mask(f, t, ch):
        pk = _pinkm(f)
        s = C.at(S[ch], t)
        fc = 380 + 2300 * np.clip(s, 0, 1.3) ** 0.8
        bed = C.at(lev, t) * _unit(pk * _bpm(f, 50, C.at(bfc, t)))
        swell = s * _unit(pk * _hpm(f, 80, 1) * _lpm(f, fc))
        fizz = 0.22 * C.at(Fz[ch], t) * _unit(_bpm(f, 1500, 6000) * _pinkm(f, 3000, 0.3))
        return bed + swell + fizz

    x = _bed(rng, n, sr, mask, corr=0.25)
    _dbg("bed", x)
    lp = np.zeros((n, 2))
    for tl, a, pan in laps:
        _place(lp, _norm(_k_lap(rng, sr)) * a * 0.35, int(tl * sr), pan)
    _dbg("laps", lp)
    rate = 260 * C.at(Fz.mean(0), np.arange(n) / sr)
    dz = np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1)
    dz = _fft_shape(dz, sr, lambda f: _bpm(f, 2000, 6500)) * 0.35
    _dbg("fizz grains", dz)
    return x + lp + dz


def _k_lap(rng, sr):
    m = int(0.4 * sr)
    t = np.arange(m) / sr
    nz = _nrms(_filt(rng.standard_normal(m), "bp", (rng.uniform(160, 260), rng.uniform(700, 1100)), sr))
    y = nz * _ar(t, 0.01, rng.uniform(0.06, 0.13))
    if rng.random() < 0.6:
        f0 = rng.uniform(170, 320)
        y += 1.8 * np.sin(_osc(f0 * (1 + 0.8 * np.minimum(t / 0.12, 1)), sr)) * _ar(t - 0.01, 0.004, 0.04)
    return y


def _waves_storm(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    B = np.zeros((2, C.K))
    Cr = np.zeros((2, C.K))
    W = np.zeros((2, C.K))
    crashes = []
    for t0 in _ptimes(rng, T, 3.3 / p["density"], 0.4):
        a, rise = rng.uniform(0.6, 1.0), rng.uniform(0.7, 1.4)
        tc, tw = rng.uniform(0.35, 0.6), rng.uniform(1.0, 1.6)
        pan = rng.uniform(-0.6, 0.6)
        g = _pan(pan)[:, None]
        B += a * g * C.ev(t0, -rise, 1.5, lambda d: _swell(d, rise, 0.2))
        Cr += a * g * C.ev(t0, 0, 6 * tc, lambda d: _ar(d, 0.03, tc) * np.clip(6 - d / tc, 0, 1))
        W += a * g * C.ev(t0, 0, 6 * tw, lambda d: _ar(d, 0.15, tw) * np.clip(6 - d / tw, 0, 1))
        crashes.append((t0, a, pan))
    l1, l2, l3 = (_pnoise(rng, T, r)(C.t) for r in (0.15, 0.08, 0.3))
    low = 0.55 * (1 + 0.3 * l1)
    lfc = 380 + 100 * l2
    mid = 0.3 * (1 + 0.4 * l3)

    def mask(f, t, ch):
        pk = _pinkm(f)
        b, c, w = C.at(B[ch], t), C.at(Cr[ch], t), C.at(W[ch], t)
        m = C.at(low, t) * _unit(pk * _bpm(f, 40, C.at(lfc, t)))
        m = m + C.at(mid, t) * _unit(pk * _bpm(f, 250, 1800))
        m = m + 0.8 * b * _unit(pk * _bpm(f, 60, 500 + 900 * np.clip(b, 0, 1.2)))
        m = m + 1.4 * c * _unit(pk ** 0.6 * _bpm(f, 45, 4500))
        m = m + 0.7 * w * _unit(pk * _bpm(f, 400, 5500))
        return m

    x = _bed(rng, n, sr, mask, corr=0.2)
    _dbg("bed", x)
    th = np.zeros((n, 2))
    for t0, a, pan in crashes:
        _place(th, _norm(_k_thump(rng, sr, 75, 45, 0.28, noise=0.6, att=0.01)) * a * 0.45, int(t0 * sr), pan)
    _dbg("thumps", th)
    rate = 500 * C.at(W.mean(0), np.arange(n) / sr)
    dz = np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1)
    dz = _fft_shape(dz, sr, lambda f: _bpm(f, 1800, 6500)) * 0.4
    _dbg("spray", dz)
    return x + th + dz


def _storm_wind(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    gust = np.zeros((2, C.K))
    for t0 in _ptimes(rng, T, 4.5, 0.5):
        a, rise, fall = rng.uniform(0.3, 0.7), rng.uniform(0.8, 1.8), rng.uniform(1.2, 2.5)
        gust += a * _pan(rng.uniform(-0.5, 0.5))[:, None] * C.ev(t0, -rise, 6 * fall,
                                                                  lambda d: _swell(d, rise, fall))
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
        a = 0.35 * rng.lognormal(0, 0.5) * (2.2 if rng.random() < 0.04 else 1.0)
        _place(dr, kern[rng.integers(len(kern))] * a, int(t0 * sr), rng.uniform(-0.9, 0.9))
    _dbg("drops", dr)
    return x + dr


def _wind_soft(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    base = 0.6 + 0.2 * _pnoise(rng, T, 0.1)(C.t)
    G = [np.clip(base + 0.08 * _pnoise(rng, T, 0.35)(C.t), 0.25, 1.1) for _ in range(2)]
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
    for t0 in _ptimes(rng, T, 3.2, 0.5):
        a, rise, fall = rng.uniform(0.35, 0.8), rng.uniform(0.5, 1.1), rng.uniform(0.9, 1.8)
        gust += a * _pan(rng.uniform(-0.5, 0.5))[:, None] * C.ev(t0, -rise, 6 * fall,
                                                                  lambda d: _swell(d, rise, fall))
    base = 0.35 + 0.15 * _pnoise(rng, T, 0.3)(C.t)
    G = [np.clip(base + gust[ch], 0.1, 1.5) for ch in range(2)]

    def mask(f, t, ch):
        g = C.at(G[ch], t)
        m = g ** 1.2 * _unit(_pinkm(f, slope=0.25) * _bpm(f, 180, 3000))
        m = m + 0.18 * g ** 2 * _unit(_gauss(f, 520 * (0.75 + 0.45 * g), 90))
        return m + 0.3 * g ** 2.5 * _unit(_bpm(f, 2500, 7500))

    x = _bed(rng, n, sr, mask, corr=0.3)
    _dbg("wind", x)
    ts = np.arange(n) / sr
    sand = np.stack([_dust(rng, 2500 * C.at(G[ch], ts) ** 2, sr) for ch in range(2)], 1)
    sand = _fft_shape(sand, sr, lambda f: _bpm(f, 2500, 8000)) * 0.5
    _dbg("sand", sand)
    return x + sand


def _ship_creak(rng, n, sr, p):
    T = n / sr
    x = np.zeros((n, 2))
    for t0 in _ptimes(rng, T, 1.6 / p["density"], 0.65):
        r = rng.random()
        kind = "creak" if r < 0.6 else ("groan" if r < 0.85 else "knock")
        y = _norm(_k_creak(rng, sr, kind)) * rng.uniform(0.4, 1.0) * (0.6 if kind == "knock" else 1.0)
        _place(x, y, int(t0 * sr), rng.uniform(-0.6, 0.6))
    x = _verb(x, _ir(rng, sr, 0.5, 0.006, 3000), 0.35, circular=True)
    _dbg("creaks", x)
    C = _Clock(T)
    lv = 0.05 * (1 + 0.5 * _pnoise(rng, T, 0.2)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 60, 450)), corr=0.3)
    _dbg("hull bed", bed)
    return x + bed


def _k_creak(rng, sr, kind):
    if kind == "knock":
        m = int(0.25 * sr)
        imp = np.zeros(m)
        imp[0] = 1.0
        j = int(rng.uniform(0.03, 0.06) * sr)
        imp[j] = rng.uniform(0.25, 0.5)
        f1, f2 = rng.uniform(220, 320), rng.uniform(650, 900)
        return _reson(imp, f1, 14, sr) + 0.5 * _reson(imp, f2, 16, sr)
    if kind == "creak":
        D, r0, glide = rng.uniform(0.25, 0.9), rng.uniform(22, 70), rng.uniform(-0.45, 0.6)
        res = [(rng.uniform(380, 650), 10, 1.0), (rng.uniform(950, 1450), 12, 0.6), (rng.uniform(1900, 2600), 14, 0.25)]
        fr = 0.0
    else:
        D, r0, glide = rng.uniform(0.7, 1.6), rng.uniform(18, 35), rng.uniform(-0.3, 0.3)
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
    y = sum(g * _reson(imp, f, q, sr) for f, q, g in res)
    y = _norm(y)
    if fr:
        y += fr * _norm(_filt(rng.standard_normal(m), "bp", (250, 1000), sr)) * env
    return _fade(y, sr, 0.0, 0.02)


def _underwater(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    l1, l2, l3, l4 = (_pnoise(rng, T, r)(C.t) for r in (0.07, 0.04, 0.1, 0.2))
    sw = np.zeros(C.K)
    for t0 in _ptimes(rng, T, 7.0, 0.5):
        a, rise, fall = rng.uniform(0.3, 0.7), rng.uniform(1.5, 3.0), rng.uniform(1.5, 3.0)
        sw += a * C.ev(t0, -rise, 6 * fall, lambda d: _swell(d, rise, fall))
    low = 0.8 * (1 + 0.3 * l1)
    rum = 0.45 * (0.6 + 0.3 * l2 + sw)
    muf = 0.25 * (1 + 0.4 * l3)
    shm = 0.05 * (1 + 0.5 * l4)

    def mask(f, t, ch):
        m = C.at(low, t) * _unit(_pinkm(f, slope=0.9) * _bpm(f, 35, 320))
        m = m + C.at(rum, t) * _unit(_bpm(f, 40, 140))
        m = m + C.at(muf, t) * _unit(_pinkm(f) * _bpm(f, 200, 900))
        return m + C.at(shm, t) * _unit(_bpm(f, 1000, 3000))

    x = _bed(rng, n, sr, mask, corr=0.1)
    _dbg("bed", x)
    bb = np.zeros((n, 2))
    for t0 in _ptimes(rng, T, 3.5, 0.6):
        pan, f0 = rng.uniform(-0.7, 0.7), rng.uniform(250, 500)
        tt = t0
        for j in range(rng.integers(3, 8)):
            k = _k_bubble(sr, f0 * rng.uniform(0.9, 1.3) * (1 + 0.1 * j), rng.uniform(0.03, 0.07), 1.9)
            _place(bb, _filt(k, "lp", 1200, sr) * 0.12 * rng.uniform(0.5, 1.0), int(tt * sr), pan)
            tt += rng.uniform(0.05, 0.2)
    bb = _verb(bb, _ir(rng, sr, 1.2, 0.02, 1500), 0.5, circular=True)
    _dbg("distant bubbles", bb)
    return x + bb


def _bubbles(rng, n, sr, p):
    T = n / sr
    x = np.zeros((n, 2))
    for t0 in _ptimes(rng, T, 1.1 / p["density"], 0.6):
        pan, f0 = rng.uniform(-0.6, 0.6), rng.uniform(260, 700)
        tt = t0
        for j in range(rng.integers(2, 8)):
            f = f0 * rng.uniform(0.85, 1.3) * (1 + 0.12 * j)
            k = _k_bubble(sr, f, rng.uniform(0.025, 0.06) * (400 / f) ** 0.5, rng.uniform(1.6, 2.4))
            _place(x, k * rng.uniform(0.5, 1.0) * 0.85 ** j, int(tt * sr), pan + rng.uniform(-0.1, 0.1))
            tt += rng.uniform(0.04, 0.16)
        if rng.random() < 0.3:
            k = _k_bubble(sr, rng.uniform(150, 260), rng.uniform(0.09, 0.13), 2.2, 0.15)
            _place(x, k * rng.uniform(0.8, 1.1), int((t0 + rng.uniform(-0.3, 0.3)) * sr), rng.uniform(-0.4, 0.4))
    x = _verb(x, _ir(rng, sr, 0.6, 0.008, 2500), 0.25, circular=True)
    _dbg("bubbles", x)
    C = _Clock(T)
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
        lub = _k_thump(rng, sr, 95, 52, 0.11, noise=0.35, att=0.012, p=2.0, nlp=260)
        dub = _k_thump(rng, sr, 115, 62, 0.08, noise=0.3, att=0.01, p=2.0, nlp=300)
        _place(x, lub * a, int(t0 * sr))
        _place(x, dub * a * 0.65, int((t0 + dub_dt) * sr))
        # soft blood "whoosh" swelling after each beat
        m = int(min(per, 1.2) * sr)
        tt = np.arange(m) / sr
        w = _nrms(_filt(rng.standard_normal(m), "lp", 380, sr)) * _ar(tt - 0.05, 0.08, 0.25, 2.0)
        _place(x, w * 0.12, int(t0 * sr))
    _dbg("beats", x)
    C = _Clock(T)
    lv = 0.05 * (1 + 0.3 * _pnoise(rng, T, 0.1)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 40, 260)), corr=0.3)
    _dbg("belly bed", bed)
    x = _verb(x + bed, _ir(rng, sr, 0.35, 0.005, 900), 0.3, circular=True)
    return x


def _drip(rng, n, sr, p):
    T = n / sr
    dry = np.zeros((n, 2))
    sources = [(rng.uniform(1.2, 3.4) / p["density"], rng.uniform(700, 1900), rng.uniform(-0.7, 0.7),
                rng.uniform(0.45, 1.0)) for _ in range(3)]
    for per, f0, pan, a in sources:
        for t0 in _ptimes(rng, T, per, 0.12):
            _place(dry, _k_drip(rng, sr, f0 * rng.uniform(0.96, 1.04)) * a * rng.uniform(0.8, 1.0), int(t0 * sr), pan)
    for t0 in _ptimes(rng, T, 5.0 / p["density"], 0.6):
        _place(dry, _k_drip(rng, sr, rng.uniform(600, 2200)) * rng.uniform(0.3, 0.6), int(t0 * sr),
               rng.uniform(-0.8, 0.8))
    _dbg("dry drips", dry)
    taps = [(0.045, 0.5), (0.083, 0.4), (0.121, 0.3), (0.16, 0.25), (0.24, 0.35), (0.48, 0.15)]
    x = _verb(dry, _ir(rng, sr, 2.4, 0.02, 3200, taps), 0.7, circular=True)
    C = _Clock(T)
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
        nz = _nrms(_filt(rng.standard_normal(m), "lp", 300 if run else 240, sr))
        s = np.sin(_osc(70 + 40 * np.exp(-np.maximum(tt, 0) / 0.01), sr))
        return a * (0.6 * nz + 0.7 * s) * _ar(tt, 0.0015, tau)

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
    for _ in range(nvoices):
        r = rng.random()
        f0, fs = ((rng.uniform(95, 135), 1.0) if r < 0.45 else
                  (rng.uniform(175, 235), 1.12) if r < 0.85 else (rng.uniform(240, 300), 1.25))
        dist = rng.uniform(0.35, 1.0)
        cut = 1300 + 1300 * dist
        pan = rng.uniform(-0.85, 0.85)
        cur = rng.uniform(0, T16)
        end = cur + T16
        while cur < end - 0.5:
            ph = _phrase(rng, vsr, f0 * rng.uniform(0.95, 1.05), fs, int(rng.integers(3, 11)))
            ph = _filt(ph, "lp", cut, vsr, 2) * dist
            _place(vox, ph, int(cur * vsr), pan)
            cur += len(ph) / vsr + rng.uniform(0.3, 2.2)
    vox = signal.resample(vox, n, axis=0)           # FFT resampling keeps the loop circular
    vox = _verb(vox, _ir(rng, sr, 0.9, 0.015, 2500), 0.5, circular=True)
    vox *= 0.5
    _dbg("voices", vox)
    C = _Clock(T)
    lv = 0.12 * (1 + 0.25 * _pnoise(rng, T, 0.1)(C.t))
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
    kinds = ["up", "down", "trill", "whistle", "tweet"]
    for _ in range(nb):
        s, dist, pan = rng.uniform(0.82, 1.12), rng.uniform(0.4, 1.0), rng.uniform(-0.8, 0.8)
        song = [(kinds[rng.integers(len(kinds))], rng.uniform(0.03, 0.09)) for _ in range(rng.integers(2, 7))]
        cut = 4500 + 2500 * dist
        for t0 in _ptimes(rng, T, rng.uniform(3.5, 6.5) / p["density"], 0.6):
            parts = []
            for kind, gap in song[: len(song) - (1 if rng.random() < 0.3 else 0)] or song:
                parts.append(_bird_note(rng, sr, kind, s * rng.uniform(0.96, 1.04)))
                parts.append(np.zeros(int(gap * rng.uniform(0.85, 1.15) * sr)))
            ph = _filt(np.concatenate(parts), "lp", cut, sr, 2) * dist * rng.uniform(0.7, 1.0)
            _place(x, ph, int(t0 * sr), pan + rng.uniform(-0.1, 0.1))
    x = _verb(x, _ir(rng, sr, 0.9, 0.012, 4500), 0.25, circular=True)
    _dbg("birds", x)
    C = _Clock(T)
    lv = 0.006 * (1 + 0.3 * _pnoise(rng, T, 0.15)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 120, 2500)), corr=0.3)
    _dbg("air", bed)
    return x + bed


def _bird_note(rng, sr, kind, s):
    if kind == "trill":
        D = rng.uniform(0.15, 0.3)
    elif kind == "whistle":
        D = rng.uniform(0.12, 0.22)
    elif kind == "tweet":
        D = rng.uniform(0.025, 0.045)
    else:
        D = rng.uniform(0.05, 0.09)
    m = int(D * sr)
    u = np.arange(m) / m
    am = 1.0
    if kind == "up":
        f = (2300 + 1600 * u ** rng.uniform(0.6, 1.6)) * s
    elif kind == "down":
        f = (3900 - 1400 * u ** rng.uniform(0.6, 1.6)) * s
    elif kind == "tweet":
        f = (4100 - 700 * u) * s
    elif kind == "whistle":
        f = (2550 + 350 * np.sin(np.pi * u / 2)) * s
    else:
        rate = rng.uniform(24, 34)
        f = (3150 + 420 * np.sin(TAU * rate * u * D)) * s
        am = 0.6 + 0.4 * np.sin(TAU * rate * u * D + 1.0)
    f = np.minimum(f, 4400)
    ph = _osc(f, sr)
    env = np.sin(np.pi * u) ** 0.7 * am
    return env * (np.sin(ph) + 0.08 * np.sin(2 * ph))


# ---- snore
def _snore(rng, n, sr, p):
    T = n / sr
    times, per = _beats(rng, T, float(p["cycle"]), jitter=0.03, tol=0.2)
    x = np.zeros((n, 2))
    for t0 in times:
        _place(x, _snore_cycle(rng, sr, per), int(t0 * sr), rng.uniform(-0.05, 0.05))
    return _verb(x, _ir(rng, sr, 0.35, 0.005, 3000), 0.12, circular=True)


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
    flap = rng.standard_normal(k) * _ar(np.arange(k) / sr, 0.0008, 0.004)
    src = signal.fftconvolve(imp, flap)[:mi]
    fs = rng.uniform(0.9, 1.1)
    rasp = _norm(_reson(src, 240 * fs, 4, sr) + 0.6 * _reson(src, 650 * fs, 5, sr) + 0.3 * _reson(src, 1150 * fs, 6, sr))
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
    hh = _norm(_filt(rng.standard_normal(me), "bp", (500, 2800), sr))
    y[j0:j0 + me] += envw * (0.38 * tone + 0.22 * hh)
    return y


# ---- heat (cicadas)
def _heat(rng, n, sr, p):
    T = n / sr
    C = _Clock(T)
    ts = np.arange(n) / sr
    x = np.zeros((n, 2))
    for _ in range(rng.integers(3, 6)):
        fc, bw = rng.uniform(3300, 4600), rng.uniform(500, 800)
        fam = max(1, round(rng.uniform(95, 150) * T)) / T
        sharp = rng.uniform(3, 6)
        car = _cnoise(rng, n, sr, lambda f: _gauss(f, fc, bw / 2))
        am = (0.5 + 0.5 * np.cos(TAU * fam * ts + rng.uniform(0, TAU))) ** sharp
        am /= np.sqrt(np.mean(am ** 2))
        puls = max(1, round(rng.uniform(2.5, 5) * T)) / T
        env = np.zeros(C.K)
        for t0 in _ptimes(rng, T, 7.0, 0.5):
            rise, hold, fall = rng.uniform(1.0, 2.5), rng.uniform(2, 6), rng.uniform(1.5, 3)
            env += rng.uniform(0.5, 1.0) * C.ev(t0, 0, rise + hold + fall,
                                                 lambda d: _smoothstep(d / rise) * _smoothstep((rise + hold + fall - d) / fall))
        if T < 4:
            env += 0.6
        env = np.clip(env, 0, 1.2)
        e = C.at(env, ts) * (1 + 0.15 * np.sin(TAU * puls * ts))
        _place(x, car * am * e * rng.uniform(0.5, 1.0), 0, rng.uniform(-0.7, 0.7))
    _dbg("cicadas", x)
    lv = 0.15 * (1 + 0.3 * _pnoise(rng, T, 0.1)(C.t))
    bed = _bed(rng, n, sr, lambda f, t, ch: C.at(lv, t) * _unit(_pinkm(f) * _bpm(f, 80, 1200)), corr=0.3)
    _dbg("warm air", bed)
    return x + bed


# =========================================================================================== one-shots
def _thunder(rng, sr, p):
    L = 4.0
    m = int(L * sr)
    t = np.arange(m) / sr
    out = np.zeros((m, 2))
    tc = 0.03
    k = int(0.08 * sr)
    tk = np.arange(k) / sr
    for i in range(rng.integers(5, 9)):
        ti = tc + (rng.exponential(0.06) if i else 0.0)
        b = _filt(rng.standard_normal(k), "bp", (250, 4500), sr) * _ar(tk, 0.0015, rng.uniform(0.006, 0.02))
        _place(out, _norm(b) * rng.uniform(0.4, 1.0) * 0.75 ** i, int(ti * sr), rng.uniform(-0.3, 0.3), wrap=False)
    body = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (150, 3000), sr)) * _ar(t - tc, 0.004, 0.14)[:, None]
    out += 0.35 * body
    _dbg("crack", out)
    env = np.zeros(m)
    rolls = [0.08, rng.uniform(0.35, 0.7), rng.uniform(0.9, 1.4), rng.uniform(1.5, 2.1), rng.uniform(2.2, 2.8)]
    for ti, a in zip(rolls, (1.0, 0.85, 0.7, 0.5, 0.35)):
        env += a * rng.uniform(0.75, 1.1) * _swell(t - ti - 0.15, rng.uniform(0.1, 0.25), rng.uniform(0.4, 0.8))
    env *= np.exp(-t / 2.5) * _smoothstep((3.6 - t) / 0.6)
    low = _nrms(_filt(rng.standard_normal((m, 2)), "lp", 170, sr, 2))
    mid = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (150, 900), sr))
    rum = (low * env[:, None] + 0.45 * mid * (env ** 1.5)[:, None]) * 0.42
    _dbg("rumble", rum)
    x = out + rum
    x = _verb(x, _ir(rng, sr, 1.8, 0.03, 2500), 0.35)[:m]
    return np.tanh(x * 1.6) / 1.6


def _splash_any(rng, sr, L, big):
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros((m, 2))
    sc = 1.0 if big else 0.55
    th = _k_thump(rng, sr, 110 if big else 160, 60 if big else 90, 0.05 if big else 0.035, noise=0.6)
    _place(x, _norm(th) * 0.7 * sc, 0, 0, wrap=False)
    slap = _nrms(_filt(rng.standard_normal(m), "bp", (500, 6000), sr)) * _ar(t, 0.002, 0.035 if big else 0.025)
    x += (0.8 * slap)[:, None]
    nz = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (300, 1500), sr))
    hz = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (1500, 6000), sr))
    if big:
        e1 = _ar(t, 0.02, 0.25) + 0.5 * _ar(t - 0.2, 0.08, 0.25)
        e2 = _ar(t, 0.01, 0.15) + 0.45 * _ar(t - 0.22, 0.06, 0.2)
        x += 0.65 * nz * e1[:, None] + 0.4 * hz * e2[:, None]
    else:
        x += 0.4 * nz * _ar(t, 0.006, 0.12)[:, None] + 0.45 * hz * _ar(t, 0.003, 0.06)[:, None]
        plop = _k_bubble(sr, rng.uniform(220, 320), 0.07, 2.2, 0.15)
        _place(x, _norm(plop) * 0.9, int(0.004 * sr), 0, wrap=False)
        kn = np.zeros(int(0.2 * sr))
        kn[0] = 1
        knock = _reson(kn, rng.uniform(210, 260), 10, sr) + 0.5 * _reson(kn, rng.uniform(560, 660), 12, sr)
        _place(x, _norm(knock) * 0.3, 0, 0, wrap=False)
    _dbg("impact+body", x)
    dr = np.zeros((m, 2))
    nd = rng.integers(60, 120) if big else rng.integers(15, 30)
    for _ in range(nd):
        u = rng.random() ** 1.6
        t0 = (0.12 + (L - 0.35) * u) if big else (0.06 + (L - 0.3) * u)
        a = (1 - 0.7 * u) * rng.uniform(0.15, 0.5)
        _place(dr, _norm(_k_drop_or_tick(rng, sr)) * a, int(t0 * sr), rng.uniform(-0.6, 0.6), wrap=False)
    for _ in range(rng.integers(6, 12) if big else rng.integers(3, 6)):
        t0 = rng.uniform(0.08, 0.9 * L)
        k = _k_bubble(sr, rng.uniform(200, 700), rng.uniform(0.025, 0.06), 1.9)
        _place(dr, k * rng.uniform(0.15, 0.35), int(t0 * sr), rng.uniform(-0.5, 0.5), wrap=False)
    _dbg("droplets", dr)
    x = x + dr
    return _verb(x, _ir(rng, sr, 0.6, 0.008, 5000), 0.15)[:m]


def _splash(rng, sr, p):
    return _splash_any(rng, sr, 1.5, True)


def _splash_small(rng, sr, p):
    return _splash_any(rng, sr, 0.8, False)


def _whoosh(rng, sr, p):
    L = 0.8
    m = int(L * sr)
    t = np.arange(m) / sr
    u = t / L
    a, b = 2.2, 2.7
    env = u ** a * (1 - u) ** b
    env /= env.max()
    f_lo, f_hi = rng.uniform(300, 420), rng.uniform(1400, 1900)

    def mask(f, tt):
        uu = np.clip(tt / L, 0, 1)
        fc = f_lo * (f_hi / f_lo) ** np.sin(np.pi * uu ** 0.9)
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
    L = 1.0
    m = int(L * sr)
    t = np.arange(m) / sr
    x = np.zeros(m)
    # 1) wet onset
    k = int(0.1 * sr)
    tk = np.arange(k) / sr
    x[:k] += 0.25 * _nrms(_filt(rng.standard_normal(k), "bp", (400, 1800), sr)) * _ar(tk - 0.01, 0.003, 0.03)
    _place2 = lambda y, at, g: x.__setitem__(slice(int(at * sr), int(at * sr) + len(y)),
                                             x[int(at * sr): int(at * sr) + len(y)] + g * y[: m - int(at * sr)])
    _place2(_norm(_k_bubble(sr, rng.uniform(450, 600), 0.03, 1.6)), 0.012, 0.4)
    # 2) throat swallow: harmonic tone sweeping down through an 'oo' vowel
    f0 = 70 + 105 * np.exp(-np.maximum(t - 0.05, 0) / 0.18)
    F1 = 320 - 70 * np.clip((t - 0.05) / 0.5, 0, 1)
    F2 = 780 - 180 * np.clip((t - 0.05) / 0.5, 0, 1)
    v = _additive_voice(t, f0, [(F1, 90, 1.0), (F2, 130, 0.45), (2400, 300, 0.06)], sr, tilt=0.8)
    envv = _smoothstep((t - 0.04) / 0.05) * _smoothstep((0.58 - t) / 0.12) * (1 + 0.25 * np.sin(np.pi * np.clip((t - 0.05) / 0.5, 0, 1)))
    x += _norm(v) * envv * 1.0
    # 3) closing bloop, 4) wet pop, 5) slosh
    _place2(_norm(_k_bubble(sr, 120, 0.06, 2.4, 0.2)), 0.52, 0.8)
    kp = int(0.12 * sr)
    tp = np.arange(kp) / sr
    fp = 1100 - 750 * np.exp(-tp / 0.004)
    pop = np.sin(_osc(fp, sr)) * _ar(tp, 0.0005, 0.03) + 0.2 * _norm(_filt(rng.standard_normal(kp), "lp", 3000, sr)) * _ar(tp, 0.0002, 0.003)
    _place2(pop, 0.64, 0.6)
    sl = int(0.35 * sr)
    _place2(_nrms(_filt(rng.standard_normal(sl), "lp", 600, sr)) * _ar(np.arange(sl) / sr, 0.01, 0.12), 0.65, 0.15)
    for _ in range(2):
        _place2(_norm(_k_bubble(sr, rng.uniform(300, 600), 0.03, 1.8)), rng.uniform(0.7, 0.85), 0.2)
    _dbg("gulp", x)
    return _verb(x, _ir(rng, sr, 0.4, 0.005, 2500), 0.15)[:m]


def _spit(rng, sr, p):
    L = 0.8
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
    u = np.clip((t - 0.13) / 0.3, 0, 1)
    fv = 160 * 2 ** u
    tooey = _additive_voice(t, fv, [(320, 90, 1.0), (800 + 1400 * u ** 1.5, 150, 0.5), (2600, 300, 0.1)], sr)
    ev = _smoothstep((t - 0.13) / 0.02) * _smoothstep((0.47 - t) / 0.12)
    x += (0.35 * _norm(tooey) * ev)[:, None]
    _place(x, _norm(_k_bubble(sr, 180, 0.08, 3.0, 0.2)) * 0.7, int(0.14 * sr), 0, wrap=False)
    # wet splatter
    for _ in range(rng.integers(20, 40)):
        t0 = rng.uniform(0.22, 0.72)
        _place(x, _norm(_k_drop_or_tick(rng, sr)) * rng.uniform(0.08, 0.3), int(t0 * sr), rng.uniform(-0.5, 0.5), wrap=False)
    for _ in range(rng.integers(2, 5)):
        t0 = rng.uniform(0.3, 0.6)
        k = int(0.08 * sr)
        sp = _nrms(_filt(rng.standard_normal(k), "bp", (800, 5000), sr)) * _ar(np.arange(k) / sr, 0.002, 0.03)
        _place(x, sp * 0.18, int(t0 * sr), rng.uniform(-0.4, 0.4), wrap=False)
    _dbg("spit", x)
    return x


def _thud(rng, sr, p):
    L = 0.4
    m = int(L * sr)
    t = np.arange(m) / sr
    f = 65 + 45 * np.exp(-t / 0.02)
    y = np.sin(_osc(f, sr)) * _ar(t, 0.003, 0.07)
    y += 0.6 * _nrms(_filt(rng.standard_normal(m), "lp", 350, sr)) * _ar(t, 0.002, 0.04) * 0.5
    imp = np.zeros(m)
    ts = rng.exponential(0.06, rng.integers(40, 80))
    idx = (ts * sr).astype(int)
    idx = idx[idx < m]
    np.add.at(imp, idx, rng.uniform(0.2, 1.0, len(idx)) * rng.choice([-1, 1], len(idx)) * np.exp(-idx / sr / 0.1))
    sand = 0.25 * _norm(_filt(imp, "bp", (700, 4000), sr))
    hiss = 0.15 * _nrms(_filt(rng.standard_normal(m), "bp", (1000, 5000), sr)) * _ar(t, 0.003, 0.08)
    return _norm(y) + sand + hiss * 0.5


def _midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _bell(sr, f, L, tau, rng, partials=((1, 1.0, 1.0), (2.0, 0.25, 0.45), (3.0, 0.08, 0.25), (4.2, 0.05, 0.15),
                                         (5.4, 0.025, 0.1)), att=0.004):
    m = int(L * sr)
    t = np.arange(m) / sr
    y = np.zeros((m, 2))
    for r, a, td in partials:
        for ch, det in enumerate((-1, 1)):
            fr = f * r * (1 + det * 0.0009)
            if fr < 0.45 * sr:
                y[:, ch] += a * np.sin(TAU * fr * t + rng.uniform(0, TAU)) * _ar(t, att, tau * td, 2.0)
    return y


def _chime(rng, sr, p):
    L = 3.2
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    x = np.zeros((m, 2))
    notes = [0, 4, 7, 12, 16]
    for i, nn in enumerate(notes):
        t0 = 0.07 * i + rng.uniform(-0.01, 0.01)
        f = _midi(root + nn)
        _place(x, _bell(sr, f, L - t0, 0.8 * (523 / f) ** 0.3, rng) * 0.5 * (0.9 ** i), int(max(t0, 0) * sr), wrap=False)
    _dbg("bells", x)
    pad = np.zeros(m)
    for nn in (0, 4, 7):
        f = _midi(root - 12 + nn)
        pad += np.sin(TAU * f * t) + 0.15 * np.sin(TAU * 2 * f * t)
    pad *= _smoothstep(t / 0.4) * np.exp(-np.maximum(t - 0.4, 0) / 0.9) * 0.06
    x += pad[:, None]
    _dbg("pad", pad)
    pent = [0, 2, 4, 7, 9]
    for _ in range(rng.integers(18, 30)):
        t0 = rng.uniform(0.05, 1.6) ** 1.0
        nn = root + 24 + pent[rng.integers(5)] + 12 * rng.integers(0, 2)
        f = min(_midi(nn), 4800)
        k = int(0.3 * sr)
        tk = np.arange(k) / sr
        ping = np.sin(TAU * f * tk) * _ar(tk, 0.0015, rng.uniform(0.04, 0.09))
        _place(x, ping * rng.uniform(0.04, 0.09) * (1 - 0.4 * t0 / 1.6), int(t0 * sr), rng.uniform(-0.6, 0.6), wrap=False)
    air = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (3000, 8000), sr)) * (_ar(t, 0.3, 0.8, 2.0) * 0.02)[:, None]
    x += air
    return _verb(x, _ir(rng, sr, 2.2, 0.02, 6000), 0.35)[:m]


def _sparkle(rng, sr, p):
    L = 1.6
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    x = np.zeros((m, 2))
    pent = [0, 2, 4, 7, 9]
    scale = [root + o * 12 + s for o in range(3) for s in pent]
    N = rng.integers(22, 34)
    run = rng.integers(5, 9)
    for i in range(N):
        if i < run:                       # opening ascending run
            t0 = 0.035 * i
            nn = scale[min(i * 2, len(scale) - 1)]
        else:
            t0 = 0.12 + 0.85 * rng.random() ** 1.5
            nn = scale[rng.integers(len(scale))]
        f = min(_midi(nn), 4500)
        tau = rng.uniform(0.08, 0.22)
        k = int(tau * 6 * sr)
        tk = np.arange(k) / sr
        ping = (np.sin(TAU * f * tk) + 0.15 * np.sin(TAU * 2 * f * tk) + 0.06 * np.sin(TAU * 2.76 * f * tk)) * _ar(tk, 0.0015, tau)
        a = rng.uniform(0.5, 1.0) * (1 - 0.6 * min(t0, 1.0))
        _place(x, ping * a * 0.3, int(t0 * sr), rng.uniform(-0.5, 0.5), wrap=False)
    sh = _nrms(_filt(rng.standard_normal((m, 2)), "bp", (2500, 7000), sr))
    am = 0.6 + 0.4 * np.sin(TAU * 18 * t)
    x += sh * (_ar(t, 0.05, 0.35) * am * 0.06)[:, None]
    return _verb(x, _ir(rng, sr, 1.2, 0.012, 7000), 0.35)[:m]


def _grow(rng, sr, p):
    L = 2.3
    m = int(L * sr)
    t = np.arange(m) / sr
    root = float(p["root"])
    f0 = _midi(root - 12) * 0.95
    f = f0 * 4 ** np.clip(t / 1.6, 0, 1) ** 1.2
    env = _smoothstep(t / 0.25) * (0.35 + 0.65 * np.clip(t / 1.5, 0, 1)) * _smoothstep((1.95 - t) / 0.45)
    y = np.zeros((m, 2))
    for ch, det in enumerate((-1, 1)):
        for dd in (-0.004, 0.0, 0.004):
            ph = _osc(f * (1 + dd + det * 0.002), sr, rng.uniform(0, TAU))
            y[:, ch] += np.sin(ph) + 0.1 * np.sin(3 * ph) + 0.3 * np.sin(2 * ph)
    y *= (env * 0.12)[:, None]
    _dbg("sweep", y)

    def mask(ff, tt):
        fc = 400 * 10 ** np.clip(tt / 1.7, 0, 1)
        return _gauss(np.log(np.maximum(ff, 20)), np.log(fc), 0.35)

    nz = _nrms(_shaped(rng, m, sr, mask)) * env * 0.12
    y += nz[:, None] * np.array([1.0, 0.9])
    pent = [0, 2, 4, 7, 9]
    scale = [root + o * 12 + s for o in range(3) for s in pent]
    N = rng.integers(10, 16)
    for i in range(N):
        t0 = 1.8 * (i / N) ** 0.75 + rng.uniform(0, 0.03)
        nn = scale[min(int(i * len(scale) / N), len(scale) - 1)]
        fr = min(_midi(nn), 4200)
        k = int(0.6 * sr)
        tk = np.arange(k) / sr
        ping = (np.sin(TAU * fr * tk) + 0.2 * np.sin(TAU * 2 * fr * tk)) * _ar(tk, 0.002, rng.uniform(0.08, 0.16))
        _place(y, ping * rng.uniform(0.25, 0.45) * 0.5, int(t0 * sr), 0.4 * (-1) ** i, wrap=False)
    k = int(0.8 * sr)
    tk = np.arange(k) / sr
    _place(y, _bell(sr, _midi(root + 24), 0.8, 0.35, rng) * 0.18, int(1.8 * sr), wrap=False)
    rate = 50 + 350 * np.clip(t / 1.8, 0, 1) * (t < 1.9)
    rs = _filt(np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1), "bp", (1500, 5000), sr) * 0.06
    y += rs
    _dbg("twinkles+rustle", y)
    return _verb(y, _ir(rng, sr, 1.4, 0.015, 7000), 0.3)[:m]


def _wither(rng, sr, p):
    L = 2.1
    m = int(L * sr)
    t = np.arange(m) / sr
    f = 520 * (140 / 520) ** np.clip(t / 1.8, 0, 1) * (1 + 0.02 * np.sin(TAU * 6 * t))
    ph = _osc(f, sr)
    env = _smoothstep(t / 0.05) * np.clip(1 - t / 1.9, 0, 1) ** 1.2
    tone = (np.sin(ph) + 0.11 * np.sin(3 * ph)) * env * 0.6

    def mask(ff, tt):
        fc = 2500 * (500 / 2500) ** np.clip(tt / 1.7, 0, 1)
        return _gauss(np.log(np.maximum(ff, 20)), np.log(fc), 0.5)

    hiss = _nrms(_shaped(rng, m, sr, mask)) * _ar(t, 0.03, 0.7) * 0.4
    x = np.stack([tone + hiss, tone + hiss], 1)
    rate = 300 * np.exp(-t / 0.7) + 40 * (t < 1.8)
    cr = _filt(np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1), "bp", (1500, 6000), sr)
    x += 0.35 * _norm(cr)
    for _ in range(rng.integers(5, 9)):
        k = int(0.06 * sr)
        b = _nrms(_filt(rng.standard_normal(k), "bp", (2000, 5000), sr)) * _ar(np.arange(k) / sr, 0.002, 0.015)
        _place(x, b * 0.12, int(rng.uniform(0.05, 1.5) * sr), rng.uniform(-0.4, 0.4), wrap=False)
    for t0 in (rng.uniform(1.35, 1.5), rng.uniform(1.65, 1.8)):
        _place(x, _norm(_k_thump(rng, sr, 180, 120, 0.02, noise=0.6)) * 0.12, int(t0 * sr), rng.uniform(-0.3, 0.3), wrap=False)
    _dbg("wither", x)
    return _verb(x, _ir(rng, sr, 0.6, 0.008, 5000), 0.15)[:m]


def _crunch(rng, sr, p):
    L = 1.5
    m = int(L * sr)
    x = np.zeros((m, 2))
    t0, i = 0.02, 0
    nb = rng.integers(6, 10)
    while i < nb and t0 < 1.3:
        a = rng.uniform(0.6, 1.0)
        _place(x, _k_bite(rng, sr) * a, int(t0 * sr), rng.uniform(-0.15, 0.15), wrap=False)
        i += 1
        t0 += rng.uniform(0.11, 0.2) + (0.22 if i % 3 == 0 else 0.0)
    return _verb(x, _ir(rng, sr, 0.4, 0.005, 5000), 0.1)[:m]


def _k_bite(rng, sr):
    k = int(0.12 * sr)
    t = np.arange(k) / sr
    imp = np.zeros(k)
    sp = rng.uniform(0.025, 0.06)
    ts = rng.exponential(sp / 2, rng.integers(15, 40))
    idx = (ts * sr).astype(int)
    idx = idx[idx < k]
    np.add.at(imp, idx, rng.uniform(0.3, 1.0, len(idx)) * rng.choice([-1, 1], len(idx)))
    cr = 0.7 * _norm(_filt(imp, "bp", (1200, 5000), sr))
    body = 0.5 * _norm(_filt(rng.standard_normal(k), "bp", (350, 1200), sr) * _ar(t, 0.002, 0.015))
    tick = 0.2 * np.sin(TAU * 220 * t) * _ar(t, 0.001, 0.008)
    return cr + body + tick


def _gull(rng, sr, p):
    L = 1.6
    m = int(L * sr)
    x = np.zeros(m)
    pitch = float(p["pitch"])
    ncalls = int(p["calls"]) if p.get("calls") else int(rng.integers(2, 4))
    t0 = 0.02
    base = rng.uniform(850, 1050) * pitch
    for i in range(ncalls):
        D = rng.uniform(0.25, 0.38) * (0.9 ** i)
        if t0 + D > L - 0.05:
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
        _place2 = int(t0 * sr)
        x[_place2:_place2 + k] += _norm(y * rough * env) * (0.8 ** i)
        t0 += D + rng.uniform(0.08, 0.16)
    x = _filt(x, "lp", 6000, sr)
    return _verb(x, _ir(rng, sr, 0.9, 0.02, 4000), 0.2)[:m]


def _lots(rng, sr, p):
    L = 1.5
    m = int(L * sr)
    x = np.zeros((m, 2))
    nsh = rng.integers(3, 5)
    sp = rng.uniform(0.2, 0.24)
    for s in range(nsh):
        ts = 0.03 + s * sp
        for _ in range(rng.integers(6, 13)):
            tc = ts + rng.exponential(0.025)
            jar = rng.random() < 0.3
            _place(x, _k_click(rng, sr, jar) * rng.uniform(0.4, 1.0), int(tc * sr), -0.15 + rng.uniform(-0.1, 0.1),
                   wrap=False)
    td = 0.03 + nsh * sp + rng.uniform(0.12, 0.2)
    for j, (dt, a) in enumerate(((0.0, 1.0), (0.08, 0.45), (0.13, 0.2))):
        _place(x, _k_tock(rng, sr) * a * 0.9, int((td + dt * rng.uniform(0.9, 1.1)) * sr), 0.2, wrap=False)
    return _verb(x, _ir(rng, sr, 0.5, 0.006, 6000), 0.15)[:m]


def _k_click(rng, sr, jar):
    k = int(0.12 * sr)
    imp = np.zeros(k)
    imp[0] = 1
    y = _reson(imp, rng.uniform(1800, 3200), 18, sr) + 0.3 * _reson(imp, rng.uniform(3600, 5000), 20, sr)
    if jar:
        y = 0.6 * _norm(y) + 0.5 * _norm(_reson(imp, rng.uniform(480, 620), 12, sr))
    return _norm(y)


def _k_tock(rng, sr):
    k = int(0.2 * sr)
    imp = np.zeros(k)
    imp[0] = 1
    y = _reson(imp, rng.uniform(850, 1100), 22, sr) + 0.5 * _reson(imp, rng.uniform(2300, 2800), 25, sr)
    return _norm(y)


def _cloth(rng, sr, p):
    L = 0.8
    m = int(L * sr)
    t = np.arange(m) / sr
    g1 = _swell(t - rng.uniform(0.1, 0.16), 0.08, 0.1)
    g2 = 0.7 * _swell(t - rng.uniform(0.42, 0.5), 0.08, 0.12)
    env = g1 + g2
    fr = 0.55 + 0.45 * np.abs(_nrms(_filt(rng.standard_normal(m), "lp", 40, sr))) / 2

    def mask(f, tt):
        return _bpm(f, 700, 5000) * _pinkm(f, 2000, 0.3)

    y = np.stack([_nrms(_shaped(rng, m, sr, mask)) for _ in range(2)], 1)
    y = 0.85 * y[:, :1] + 0.3 * y
    y *= (env * fr * 0.5)[:, None]
    rate = 200 * env
    cr = _filt(np.stack([_dust(rng, rate, sr), _dust(rng, rate, sr)], 1), "bp", (2500, 6500), sr)
    return y + 0.15 * _norm(cr)


def _sheep(rng, sr, p):
    L = 1.0
    m = int(L * sr)
    t = np.arange(m) / sr
    pitch = float(p["pitch"])
    D = rng.uniform(0.78, 0.88)
    base = rng.uniform(230, 270) * pitch
    vr = rng.uniform(6.5, 8.5)
    contour = np.interp(t, [0, 0.15, D], [0.92, 1.05, 0.9])
    f0 = base * contour * (1 + 0.04 * np.sin(TAU * vr * t))
    on = np.clip(t / 0.05, 0, 1)
    F1 = 400 + 380 * on
    F2 = 1100 + 450 * on - 200 * np.clip((t - 0.4) / 0.4, 0, 1)
    v = _additive_voice(t, f0, [(F1, 110, 1.0), (F2, 150, 0.6), (2700 + 0 * t, 250, 0.25), (3700 + 0 * t, 300, 0.1)],
                        sr, tilt=1.0)
    am = 1 - 0.35 * (0.5 + 0.5 * np.sin(TAU * vr * t - 0.5))
    env = _smoothstep(t / 0.04) * _smoothstep((D - t) / 0.12) * am
    y = _norm(v) * env

    def mask(f, tt):
        return 0.02 + _gauss(f, 780, 150) + 0.6 * _gauss(f, 1500, 200) + 0.25 * _gauss(f, 2700, 300)

    br = _nrms(_shaped(rng, m, sr, mask)) * env * 0.06
    return _verb(y + br, _ir(rng, sr, 0.5, 0.01, 5000), 0.12)[:m]


def _pop(rng, sr, p):
    L = 0.3
    m = int(L * sr)
    t = np.arange(m) / sr
    f = 1100 - 720 * np.exp(-t / 0.004)
    y = np.sin(_osc(f * rng.uniform(0.9, 1.1), sr)) * _ar(t, 0.0005, 0.035)
    y += 0.3 * _norm(_filt(rng.standard_normal(m), "lp", 4000, sr) * _ar(t, 0.0002, 0.0012))
    y += 0.12 * np.sin(TAU * 2300 * t) * _ar(t, 0.0005, 0.015)
    return y


_LOOPS = {
    "waves_calm": _waves_calm, "waves_storm": _waves_storm, "storm_wind": _storm_wind, "rain": _rain,
    "wind_soft": _wind_soft, "wind_hot": _wind_hot, "ship_creak": _ship_creak, "underwater": _underwater,
    "bubbles": _bubbles, "heartbeat": _heartbeat, "drip": _drip, "footsteps": _footsteps,
    "footsteps_run": _footsteps_run, "crowd": _crowd, "birds": _birds, "snore": _snore, "heat": _heat,
}
_ONESHOTS = {
    "thunder": _thunder, "splash": _splash, "splash_small": _splash_small, "whoosh": _whoosh, "gulp": _gulp,
    "spit": _spit, "thud": _thud, "chime": _chime, "sparkle": _sparkle, "grow": _grow, "wither": _wither,
    "crunch": _crunch, "gull": _gull, "lots": _lots, "cloth": _cloth, "sheep": _sheep, "pop": _pop,
}
assert set(_LOOPS) | set(_ONESHOTS) == set(NAMES)
assert all(NAMES[k][0] == "loop" for k in _LOOPS) and all(NAMES[k][0] == "oneshot" for k in _ONESHOTS)
