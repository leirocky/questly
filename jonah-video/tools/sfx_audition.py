"""Audition and verify the procedural sound-effect library (audio/sfx.py).

Renders every effect to build/preview/sfx/<name>.wav and writes
  build/preview/sfx/spectrograms.png        labelled log-frequency spectrogram grid (mid channel, absolute dBFS)
  build/preview/sfx/spectrograms_side.png   the same for the side channel (L-R)/2   (--side)
  build/preview/sfx/seams.png               loops only: waveform across the wrap point (end | start)
  build/preview/sfx/report.txt              per-effect numbers, flags, API checks and the seed/length sweep

Examples (run from jonah-video/):
  python3 tools/sfx_audition.py                    # everything, seed 0
  python3 tools/sfx_audition.py rain thunder       # a subset
  python3 tools/sfx_audition.py --seed 3 --each    # another variation + one large spectrogram per effect
  python3 tools/sfx_audition.py --checks           # + API checks (names, determinism, seeds, dur/param edge cases)
                                                   #   and behaviour checks (night pauses, oars strokes, rooster crow)
  python3 tools/sfx_audition.py --sweep            # + loudness sweep: loops 2/4/6/9/13 s x 8 seeds, one-shots x 8 seeds
  python3 tools/sfx_audition.py --sweep --seeds 64 coins rooster   # a deeper sweep (more seeds) of a few effects
  python3 tools/sfx_audition.py --debug waves_calm # + component / layer-vs-bed levels logged by the generators
  python3 tools/sfx_audition.py --all              # --checks --sweep --side

Metrics (independent of sfx.py's own meter: pyloudnorm's integrated loudness and K-weighting filters)
  peak        sample peak; loops should stay well below 0.9, one-shots 0.5-0.7
  LUFS        integrated loudness (BS.1770); loops are checked against sfx.LOOP_LUFS[name] (+-1 dB) and -25..-20
  mom         one-shots: loudest 400 ms window (momentary max, 10 ms hop); flagged if > 2 dB from sfx.ONESHOT_LUFS
  hp300       loudness lost through a 4th-order 300 Hz high-pass (phone-sized speaker); flagged above 6 dB
              (integrated LUFS for loops, momentary max for one-shots)
  L/R         channel energy difference in dB; flagged above 1.5 dB
  corr/mono   L/R correlation (1 = mono); mono = level of (L+R)/2 relative to L/R (-3 dB for decorrelated noise,
              near 0 for centred sounds; below -4.5 dB would mean phasey cancellation on mono speakers)
  centroid    spectral centroid; <35 Hz / >8 kHz = share of energy below 35 Hz / above 8 kHz
  tail        one-shots: RMS of the last W s before the end fade (sfx.END_FADE) relative to the loudest 50 ms
              (W = 0.2 s, or 15 % of the length for sounds under 1.33 s); flagged above -40 dB (a tail chopped
              while still ringing). mixfade = momentary-max change if mix.py's default 0.3 s fade_out is applied.
  seam        loops: |x[0]-x[-1]| divided by the 99th percentile of |x[i]-x[i-1]| (<= 1 means the wrap point is no
              rougher than ordinary sample steps), the second difference across the wrap divided by the largest one
              within +-10 ms of it (<= 1: no kink), and the end-sample levels
"""
import argparse
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from scipy import signal  # noqa: E402

from audio import sfx  # noqa: E402
from engine.paths import BUILD, SR  # noqa: E402

OUT = BUILD / "preview" / "sfx"

# The contract from the brief: exactly these names and kinds.
EXPECTED = {
    **{k: "loop" for k in ("waves_calm", "waves_storm", "storm_wind", "rain", "wind_soft", "wind_hot", "ship_creak",
                           "underwater", "bubbles", "heartbeat", "drip", "footsteps", "footsteps_run", "crowd",
                           "birds", "snore", "heat",
                           "oars", "fire", "night", "cheer")},                 # added for the ~9-10 min version
    **{k: "oneshot" for k in ("thunder", "splash", "splash_small", "whoosh", "gulp", "spit", "thud", "chime",
                              "sparkle", "grow", "wither", "crunch", "gull", "lots", "cloth", "sheep", "pop",
                              "coins", "horn", "hammer", "rooster")},           # added for the ~9-10 min version
}
LOOP_RANGE = (-25.0, -20.0)          # brief: "about -24..-20"; heat sits at -25 on purpose (sensitive 3 kHz band)
SWEEP_DURS = (2.0, 4.0, 6.0, 9.0, 13.0)
SWEEP_SEEDS = range(8)
HP300 = signal.butter(4, 300, "hp", fs=SR, output="sos")


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-12))


def _pad(x, sec=0.4):
    m = int(sec * SR)
    return x if len(x) >= m else np.concatenate([x, np.zeros((m - len(x), x.shape[1]))])


def lufs(x, sr=SR):
    import pyloudnorm as pyln
    try:
        return pyln.Meter(sr).integrated_loudness(_pad(np.asarray(x, np.float64)))
    except Exception:
        return float("nan")


def momentary_max(x, sr=SR, hop=0.01):
    """Loudest 400 ms window, using pyloudnorm's K-weighting filters on the whole (zero-padded) signal."""
    import pyloudnorm as pyln
    x = _pad(np.asarray(x, np.float64))
    y = x.copy()
    for f in pyln.Meter(sr)._filters.values():
        for c in range(y.shape[1]):
            y[:, c] = f.apply_filter(y[:, c])
    e = np.concatenate([[0.0], np.cumsum((y ** 2).sum(axis=1))])
    w, h = int(0.4 * sr), int(hop * sr)
    st = np.arange(0, len(y) - w + 1, h)
    z = (e[st + w] - e[st]) / w
    return float(-0.691 + 10 * np.log10(z.max() + 1e-20))


def hp300_loss(x, kind):
    y = signal.sosfilt(HP300, np.asarray(x, np.float64), axis=0)
    if kind == "loop":
        return float(lufs(x) - lufs(y))
    return float(momentary_max(x) - momentary_max(y))


def lr_db(x):
    eL, eR = np.mean(np.square(x[:, 0], dtype=np.float64)), np.mean(np.square(x[:, 1], dtype=np.float64))
    return float(10 * np.log10((eL + 1e-20) / (eR + 1e-20)))


def band_share(x, sr=SR):
    m = x.mean(axis=1)
    P = np.abs(np.fft.rfft(m)) ** 2
    f = np.fft.rfftfreq(len(m), 1 / sr)
    tot = P.sum() + 1e-30
    return (float((P * f).sum() / tot), float(P[f < 35].sum() / tot), float(P[f < 60].sum() / tot),
            float(P[f > 8000].sum() / tot))


def seam_metrics(x, local=0.01):
    """Wrap-point continuity of a loop (x[-1] -> x[0]).

    seam_ratio   |x[0] - x[-1]| / 99th percentile of all |x[i] - x[i-1]|: a step (click) at the wrap.
    seam2_ratio  largest second difference across the wrap / largest second difference within +-``local`` s of it
                 (circular, wrap samples excluded): a kink (slope break) that stands out from the local waveform.
                 Compared locally rather than with a global percentile, because the wrap is rotated to a quiet
                 spot and a continuous loop's wrap curvature is an ordinary sample (a global p99 test fails ~1 %
                 of seamless renders by chance).
    """
    d1 = np.abs(np.diff(x, axis=0))
    p99 = np.percentile(d1, 99, axis=0).max() + 1e-12
    jump = np.abs(x[0] - x[-1]).max()
    k = max(4, min(int(local * SR), len(x) // 2 - 2))
    w = np.concatenate([x[-(k + 1):], x[:k + 1]])            # the wrap lies between w[k] (= x[-1]) and w[k+1]
    d2 = np.abs(w[2:] - 2 * w[1:-1] + w[:-2])                 # d2[j] is centred on w[j+1]
    s2 = d2[[k - 1, k]].max()
    others = max(np.delete(d2, [k - 1, k], axis=0).max(), 1e-6)       # floor: -120 dB curvature is not a kink
    return dict(seam_jump=float(jump), seam_ratio=float(jump / p99), seam2_ratio=float(s2 / others),
                start=float(np.abs(x[0]).max()), end=float(np.abs(x[-1]).max()))


def win_rms_db(x, win=0.05, hop=0.01):
    """RMS (channel-summed energy) of win-second windows every hop seconds, dB."""
    e = np.concatenate([[0.0], np.cumsum((np.asarray(x, np.float64) ** 2).sum(axis=1))])
    w, h = int(win * SR), int(hop * SR)
    st = np.arange(0, max(1, len(x) - w + 1), h)
    return 10 * np.log10((e[np.minimum(st + w, len(x))] - e[st]) / w + 1e-20)


def tail_metric(name, x):
    """(tail dB re loudest 50 ms, window used): RMS of the last W s before the end fade."""
    L = len(x) / SR
    F = sfx.END_FADE[name]
    W = min(0.2, max(0.03, 0.15 * L))
    a, b = int((L - F - W) * SR), int((L - F) * SR)
    seg = np.asarray(x[a:b], np.float64)
    tail = 10 * np.log10(np.mean((seg ** 2).sum(axis=1)) + 1e-20)
    return float(tail - win_rms_db(x).max()), W


def mixfade_loss(x, fo=0.3):
    """mix.py applies a linear fade_out (default 0.3 s) over the end of every cue: momentary-max change."""
    y = np.asarray(x, np.float64).copy()
    k = min(len(y), int(fo * SR))
    y[-k:] *= np.linspace(1, 0, k)[:, None]
    return float(momentary_max(y) - momentary_max(x))


def analyse(name, x, render_s=0.0):
    kind = sfx.NAMES[name][0]
    pk = float(np.abs(x).max())
    rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
    L, R = x[:, 0].astype(np.float64), x[:, 1].astype(np.float64)
    corr = float(np.corrcoef(L, R)[0, 1]) if L.std() > 0 and R.std() > 0 else 1.0
    cen, sub35, sub60, hi8 = band_share(x)
    mono_db = float(db(np.sqrt(np.mean(((L + R) / 2) ** 2))) - db(np.sqrt((np.mean(L ** 2) + np.mean(R ** 2)) / 2)))
    r = dict(name=name, kind=kind, dur=len(x) / SR, peak=pk, peak_db=float(db(pk)), rms_db=float(db(rms)),
             lufs=float(lufs(x)), corr=corr, mono_db=mono_db, centroid=cen, sub35=sub35, sub60=sub60, hi8=hi8,
             dc=float(np.abs(x.mean(axis=0)).max()), clipped=int((np.abs(x) >= 0.999).sum()),
             finite=bool(np.isfinite(x).all()), render_s=render_s, lr=lr_db(x), hp300=hp300_loss(x, kind))
    if kind == "loop":
        r.update(seam_metrics(x.astype(np.float64)))
        r["target"] = sfx.LOOP_LUFS[name]
    else:
        r["mom_max"] = momentary_max(x)
        r["target"] = sfx.ONESHOT_LUFS[name]
        r["tail"], r["tail_w"] = tail_metric(name, x)
        r["mixfade"] = mixfade_loss(x)
    return r


def flags_of(r):
    flags = []
    if not r["finite"]:
        flags.append("NaN/inf")
    if r["clipped"]:
        flags.append(f"{r['clipped']} clipped")
    if r["dc"] > 1e-3:
        flags.append(f"DC {r['dc']:.4f}")
    if r["kind"] == "loop":
        if abs(r["lufs"] - r["target"]) > 1.0:
            flags.append(f"LUFS {r['lufs'] - r['target']:+.1f} dB off target")
        if not LOOP_RANGE[0] - 0.5 <= r["lufs"] <= LOOP_RANGE[1] + 0.5:
            flags.append("LUFS outside -25..-20")
        if r["peak"] > 0.9:
            flags.append("peak > 0.9")
        if r["seam_ratio"] > 1.0 or r["seam2_ratio"] > 1.0:
            flags.append("SEAM")
        if max(r["start"], r["end"]) > 0.01:
            flags.append("end not near zero")
    else:
        if not 0.49 <= r["peak"] <= 0.71:
            flags.append("peak outside 0.5..0.7")
        if abs(r["mom_max"] - r["target"]) > 2.0:
            flags.append(f"momentary {r['mom_max'] - r['target']:+.1f} dB off target")
        if r["tail"] > -40:
            flags.append(f"tail {r['tail']:.0f} dB (chopped?)")
    if r["hp300"] > 6.0:
        flags.append(f"loses {r['hp300']:.1f} dB on small speakers")
    if abs(r["lr"]) > 1.5:
        flags.append(f"L/R {r['lr']:+.1f} dB")
    if r["mono_db"] < -4.5:
        flags.append("poor mono compatibility")
    if r["sub35"] > 0.01:
        flags.append("sub-35 Hz energy > 1%")
    return flags


def fmt(r):
    s = (f"{r['name']:<14}{r['kind']:<8}{r['dur']:6.2f}s  peak {r['peak']:.3f} ({r['peak_db']:5.1f} dBFS)  "
         f"LUFS {r['lufs']:6.1f}  RMS {r['rms_db']:6.1f}  hp300 -{r['hp300']:4.1f}  L/R {r['lr']:+4.1f}  "
         f"corr {r['corr']:5.2f}  mono {r['mono_db']:5.1f}  centroid {r['centroid']:5.0f} Hz  "
         f"<35Hz {100 * r['sub35']:3.1f}%  <60Hz {100 * r['sub60']:4.1f}%  >8k {100 * r['hi8']:4.1f}%")
    if r["kind"] == "loop":
        s += (f"  seam x{r['seam_ratio']:.2f}/x{r['seam2_ratio']:.2f}  ends {r['start']:.4f}/{r['end']:.4f}")
    else:
        s += (f"  mom {r['mom_max']:6.1f} (target {r['target']:.0f})  tail {r['tail']:5.1f} dB/{r['tail_w']:.2f}s"
              f"  mixfade {r['mixfade']:+4.1f}")
    fl = flags_of(r)
    return s + f"  render {r['render_s']:.2f}s" + (f"  !! {', '.join(fl)}" if fl else "  ok")


# ------------------------------------------------------------------------------------------------- plots
def spec(x, sr=SR, nper=2048, side=False):
    x = x.astype(np.float64)
    m = (x[:, 0] - x[:, 1]) / 2 if side else x.mean(axis=1)
    f, t, S = signal.spectrogram(m, sr, window="hann", nperseg=nper, noverlap=nper * 3 // 4, scaling="spectrum",
                                 mode="magnitude")
    return f, t, 20 * np.log10(np.maximum(S * 2, 1e-9))


def plot_grid(results, audio, path, max_len=16.0, side=False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [r["name"] for r in results]
    cols = 4 if len(names) > 6 else max(1, len(names))
    rows = (len(names) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5.2 * cols, 2.9 * rows), squeeze=False)
    for ax in axes.flat:
        ax.set_visible(False)
    im = None
    for ax, r in zip(axes.flat, results):
        ax.set_visible(True)
        x = audio[r["name"]][: int(max_len * SR)]
        f, t, S = spec(x, nper=512 if r["dur"] < 1.0 else 1024 if r["dur"] < 4 else 2048, side=side)
        im = ax.pcolormesh(t, np.maximum(f, 1), S, shading="auto", cmap="magma", vmin=-105, vmax=-15,
                           rasterized=True)
        ax.set_yscale("log")
        ax.set_ylim(30, 20000)
        ax.set_yticks([50, 100, 300, 1000, 3000, 10000])
        ax.set_yticklabels(["50", "100", "300", "1k", "3k", "10k"], fontsize=7)
        ax.tick_params(axis="x", labelsize=7)
        lev = f"{r['lufs']:.1f} LUFS" if r["kind"] == "loop" else f"mom {r['mom_max']:.1f} LUFS"
        ax.set_title(f"{r['name']}  ({r['kind']}, {r['dur']:.1f}s)  {lev}  pk {r['peak']:.2f}", fontsize=9)
        hop = int(0.01 * SR)
        xx = x.astype(np.float64)
        e = (xx[:, 0] - xx[:, 1]) / 2 if side else xx.mean(axis=1)
        e = e[: len(e) // hop * hop].reshape(-1, hop)
        ax2 = ax.twinx()
        ax2.plot(np.arange(len(e)) * 0.01, db(np.sqrt((e ** 2).mean(axis=1))), color="#7fdbff", lw=0.6)
        ax2.set_ylim(-80, 0)
        ax2.tick_params(axis="y", labelsize=6, colors="#4aa3c8")
    ch = "side channel (L-R)/2" if side else "mid channel (L+R)/2"
    fig.suptitle(f"audio/sfx.py: spectrograms ({ch}, dBFS, colour -105..-15) + RMS envelope (cyan, right axis dBFS)",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    if im is not None:
        fig.colorbar(im, ax=axes, shrink=0.3, pad=0.01, label="dBFS")
    fig.savefig(path, dpi=70)
    plt.close(fig)


def plot_each(results, audio, outdir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for r in results:
        x = audio[r["name"]]
        f, t, S = spec(x, nper=1024 if r["dur"] < 3 else 2048)
        fig, (a1, a2) = plt.subplots(2, 1, figsize=(14, 7), gridspec_kw=dict(height_ratios=[3, 1]), sharex=True)
        a1.pcolormesh(t, np.maximum(f, 1), S, shading="auto", cmap="magma", vmin=-105, vmax=-15, rasterized=True)
        a1.set_yscale("log")
        a1.set_ylim(30, 20000)
        a1.set_title(fmt(r)[:170], fontsize=8)
        tt = np.arange(len(x)) / SR
        a2.plot(tt, x[:, 0], lw=0.3, color="#1f77b4")
        a2.plot(tt, x[:, 1], lw=0.3, color="#d62728", alpha=0.6)
        a2.set_ylim(-1, 1)
        fig.tight_layout()
        fig.savefig(outdir / f"spec_{r['name']}.png", dpi=72)
        plt.close(fig)


def plot_seams(results, audio, path, ms=12.0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    loops = [r for r in results if r["kind"] == "loop"]
    if not loops:
        return
    cols = 4
    rows = (len(loops) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.5 * cols, 2.2 * rows), squeeze=False)
    for ax in axes.flat:
        ax.set_visible(False)
    k = int(ms / 1000 * SR)
    for ax, r in zip(axes.flat, loops):
        ax.set_visible(True)
        x = audio[r["name"]]
        w = np.concatenate([x[-k:], x[:k]])
        tt = (np.arange(2 * k) - k) / SR * 1000
        ax.plot(tt, w[:, 0], lw=0.7, label="L")
        ax.plot(tt, w[:, 1], lw=0.7, label="R", alpha=0.7)
        ax.axvline(0, color="k", lw=0.5, ls="--")
        lim = max(1e-3, np.abs(w).max()) * 1.1
        ax.set_ylim(-lim, lim)
        ax.set_title(f"{r['name']}: wrap point (ms)  jump x{r['seam_ratio']:.2f}", fontsize=8)
        ax.tick_params(labelsize=6)
    fig.tight_layout()
    fig.savefig(path, dpi=70)
    plt.close(fig)


# ------------------------------------------------------------------------------------------------- sweep
def _sweep_job(job):
    name, dur, seed = job
    import warnings
    warnings.simplefilter("ignore")
    x = sfx.make(name, dur, SR, seed=seed)
    kind = sfx.NAMES[name][0]
    out = dict(name=name, dur=dur, seed=seed, peak=float(np.abs(x).max()), lr=lr_db(x))
    if kind == "loop":
        out["lufs"] = float(lufs(x))
        sm = seam_metrics(x.astype(np.float64))
        out["seam"] = max(sm["seam_ratio"], sm["seam2_ratio"])
        out["ends"] = max(sm["start"], sm["end"])
        out["hp300"] = hp300_loss(x, kind)
    else:
        out["mom"] = momentary_max(x)
        out["tail"] = tail_metric(name, x)[0]
        out["hp300"] = hp300_loss(x, kind)
    return out


def sweep(names, log, workers=4, seeds=SWEEP_SEEDS):
    loops = [n for n in names if sfx.NAMES[n][0] == "loop"]
    shots = [n for n in names if sfx.NAMES[n][0] == "oneshot"]
    jobs = [(n, d, s) for n in loops for d in SWEEP_DURS for s in seeds]
    jobs += [(n, None, s) for n in shots for s in seeds]
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        res = list(ex.map(_sweep_job, jobs, chunksize=2))
    log(f"Sweep: {len(jobs)} renders in {time.time() - t0:.0f} s ({workers} workers)")
    ok = True
    if loops:
        log(f"  loops: integrated LUFS min..max over seeds {seeds.start}-{seeds.stop - 1} per length; "
            f"flag: outside {LOOP_RANGE[0]:.0f}..{LOOP_RANGE[1]:.0f} or > 1.5 dB from target, |L/R| > 1.5 dB, seam, "
            "300 Hz high-pass loss > 6 dB, peak > 0.9")
        log("  " + f"{'loop':<14}{'target':>7}" + "".join(f"{f'{d:g} s':>15}" for d in SWEEP_DURS)
            + f"{'max|L/R|':>10}{'max peak':>10}{'max hp300':>11}{'max seam':>10}")
        for n in loops:
            rr = [r for r in res if r["name"] == n]
            cells, bad = [], []
            for d in SWEEP_DURS:
                v = np.array([r["lufs"] for r in rr if r["dur"] == d])
                cells.append(f"{v.min():6.1f}..{v.max():5.1f}")
                if (v.min() < LOOP_RANGE[0] - 1e-6 or v.max() > LOOP_RANGE[1] + 1e-6
                        or np.abs(v - sfx.LOOP_LUFS[n]).max() > 1.5):
                    bad.append(f"{d:g}s LUFS")
            lr = max(abs(r["lr"]) for r in rr)
            pk = max(r["peak"] for r in rr)
            hp = max(r["hp300"] for r in rr)
            sm = max(r["seam"] for r in rr)
            if lr > 1.5:
                bad.append("L/R")
            if sm > 1.0 or max(r["ends"] for r in rr) > 0.01:
                bad.append("seam")
            if pk > 0.9:
                bad.append("peak")
            if hp > 6.0:
                bad.append("small speaker")
            ok &= not bad
            log("  " + f"{n:<14}{sfx.LOOP_LUFS[n]:7.1f}" + "".join(f"{c:>15}" for c in cells)
                + f"{lr:10.1f}{pk:10.2f}{-hp:11.1f}{sm:10.2f}" + (f"  !! {', '.join(bad)}" if bad else "  ok"))
    if shots:
        log(f"  one-shots over seeds {seeds.start}-{seeds.stop - 1}: momentary max (target +-2 dB), peak (0.5..0.7), "
            "tail (<= -40 dB), 300 Hz high-pass loss (<= 6 dB), |L/R| (<= 1.5 dB)")
        for n in shots:
            rr = [r for r in res if r["name"] == n]
            mom = np.array([r["mom"] for r in rr])
            pk = np.array([r["peak"] for r in rr])
            tail = max(r["tail"] for r in rr)
            hp = max(r["hp300"] for r in rr)
            lr = max(abs(r["lr"]) for r in rr)
            bad = []
            if np.abs(mom - sfx.ONESHOT_LUFS[n]).max() > 2.0:
                bad.append("momentary")
            if pk.min() < 0.49 or pk.max() > 0.71:
                bad.append("peak")
            if tail > -40:
                bad.append("tail")
            if hp > 6.0:
                bad.append("small speaker")
            if lr > 1.5:
                bad.append("L/R")
            ok &= not bad
            nt = sum(r["tail"] > -40 for r in rr)
            log(f"  {n:<14} mom {mom.min():6.1f}..{mom.max():6.1f}  peak {pk.min():.2f}..{pk.max():.2f}  "
                f"tail max {tail:6.1f} dB" + (f" ({nt}/{len(rr)} seeds over)" if nt else "")
                + f"  hp300 max -{hp:4.1f} dB  |L/R| max {lr:3.1f}" + (f"  !! {', '.join(bad)}" if bad else "  ok"))
    log("Sweep: " + ("ALL OK" if ok else "FLAGGED (see above)"))
    return ok


# ------------------------------------------------------------------------------------------------- API checks
def api_checks(names, log):
    import warnings
    ok = True

    def check(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        log(("  PASS " if cond else "  FAIL ") + msg)

    log("API checks")
    try:
        sfx.make("no_such_effect", 1.0)
        check(False, "unknown name raises ValueError")
    except ValueError:
        check(True, "unknown name raises ValueError")
    reg = {k: v[0] for k, v in sfx.NAMES.items()}
    check(reg == EXPECTED, f"NAMES is exactly the {len(EXPECTED)} names/kinds of the brief "
          f"(missing {sorted(set(EXPECTED) - set(reg))}, extra {sorted(set(reg) - set(EXPECTED))}, "
          f"wrong kind {sorted(k for k in reg if k in EXPECTED and reg[k] != EXPECTED[k])})")
    check(all(isinstance(v[1], float) and v[1] > 0 and isinstance(v[2], str) for v in sfx.NAMES.values()),
          "NAMES values are (kind, default seconds, description)")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sfx.make("pop", None, SR, seed=0, bogus=1)
        check(any("bogus" in str(i.message) for i in w), "unknown params warn (and are ignored)")
    for nm in names:
        kind, d, _ = sfx.NAMES[nm]
        a = sfx.make(nm, d if kind == "loop" else None, SR, seed=5)
        b = sfx.make(nm, d if kind == "loop" else None, SR, seed=5)
        c = sfx.make(nm, d if kind == "loop" else None, SR, seed=6)
        check(a.dtype == np.float32 and a.ndim == 2 and a.shape[1] == 2, f"{nm}: float32 (n, 2)")
        check(np.array_equal(a, b), f"{nm}: deterministic for a seed")
        diff = len(a) != len(c) or float(np.sqrt(np.mean((a.astype(float) - c) ** 2))) > 1e-4
        check(diff, f"{nm}: seeds 5 and 6 differ")
        if kind == "loop":
            for T in (0.5, 40.0):
                t0 = time.time()
                x = sfx.make(nm, T, SR, seed=1)
                el = time.time() - t0
                sm = seam_metrics(x.astype(np.float64))
                L = lufs(x)
                check(x.shape == (int(round(T * SR)), 2) and np.isfinite(x).all() and np.abs(x).max() <= 0.9
                      and sm["seam_ratio"] <= 1.0 and sm["seam2_ratio"] <= 1.0 and max(sm["start"], sm["end"]) < 0.01
                      and abs(L - sfx.LOOP_LUFS[nm]) <= 1.5,
                      f"{nm}: {T:4.1f} s loop shape/finite/peak/seam/level  (LUFS {L:6.1f} vs {sfx.LOOP_LUFS[nm]}, "
                      f"peak {np.abs(x).max():.3f}, seam x{sm['seam_ratio']:.2f}/x{sm['seam2_ratio']:.2f}, {el:.1f}s)")
            x = sfx.make(nm, 7.3, SR, seed=2, width=0.0)
            check(np.allclose(x[:, 0], x[:, 1], atol=1e-6), f"{nm}: width=0 gives mono")
            x = sfx.make(nm, 0.0, SR)
            check(x.shape == (0, 2), f"{nm}: dur=0 gives an empty array")
        else:
            for T in (0.1, d + 0.5):
                x = sfx.make(nm, T, SR, seed=1)
                check(x.shape == (int(round(T * SR)), 2) and np.isfinite(x).all(),
                      f"{nm}: dur={T:.2f} trims/pads to exact length")
            x = sfx.make(nm, -0.1, SR)
            check(x.shape == (0, 2), f"{nm}: negative dur gives an empty array")
            x = sfx.make(nm, None, SR, seed=2, width=0.0)
            check(np.allclose(x[:, 0], x[:, 1], atol=1e-6), f"{nm}: width=0 gives mono")
    # degenerate params must not raise or produce NaN (they are clamped)
    for nm, kw in (("heartbeat", dict(bpm=0)), ("heartbeat", dict(bpm=1e6)), ("footsteps", dict(rate=0)),
                   ("footsteps_run", dict(rate=-3)), ("waves_calm", dict(density=0)), ("birds", dict(density=0)),
                   ("drip", dict(density=0)), ("rain", dict(density=0)), ("bubbles", dict(density=0)),
                   ("ship_creak", dict(density=0)), ("crowd", dict(density=0)), ("waves_storm", dict(density=0)),
                   ("snore", dict(cycle=0)), ("chime", dict(root=0)), ("sheep", dict(pitch=0)),
                   ("gull", dict(pitch=-1)), ("whoosh", dict(width=-5)),
                   ("oars", dict(cycle=0)), ("oars", dict(cycle=1e6)), ("fire", dict(density=0)),
                   ("fire", dict(density=1e6)), ("night", dict(density=0)), ("cheer", dict(density=0)),
                   ("horn", dict(pitch=0)), ("horn", dict(pitch=1e6)), ("rooster", dict(pitch=-1)),
                   ("rooster", dict(pitch=1e6))):
        kind = sfx.NAMES[nm][0]
        try:
            x = sfx.make(nm, 3.0 if kind == "loop" else None, SR, seed=1, **kw)
            check(np.isfinite(x).all() and len(x) > 0, f"{nm} {kw}: clamped, finite (peak {np.abs(x).max():.2f})")
        except Exception as e:  # noqa: BLE001
            check(False, f"{nm} {kw}: raised {type(e).__name__}: {e}")
    # pitched pings (chime, sparkle, grow) are folded down by octaves, never clamped off-key
    bad = [(nn, fm) for nn in range(36, 145) for fm in (1200.0, 2400.0, 4700.0)
           if not (sfx._midi(sfx._fold(nn, fm)) <= fm * 1.0001 and (sfx._fold(nn, fm) - nn) % 12 == 0)]
    check(not bad, f"_fold keeps every note (MIDI 36-144) in key and under its limit (failures {bad[:3]})")
    x = sfx.make("gull", None, SR, seed=1, calls=0)
    check(np.abs(x).max() == 0, "gull calls=0 gives silence (0 is not treated as 'unset')")
    x1 = sfx.make("gull", None, SR, seed=1, calls=1)
    x3 = sfx.make("gull", None, SR, seed=1, calls=3)
    check(np.abs(x1).max() > 0 and not np.array_equal(x1, x3), "gull calls=1 / calls=3 differ")
    behaviour_checks(names, check)
    return ok


def _spy(kernel, on_kernel, on_place):
    """Temporarily wrap sfx.<kernel> and sfx._place: on_kernel(args) when the kernel is made, on_place(buf, x, i0)
    for every placement. Returns a restore function."""
    k0, p0 = getattr(sfx, kernel), sfx._place

    def k1(*a, **kw):
        on_kernel(a)
        return k0(*a, **kw)

    def p1(buf, x, i0, *a, **kw):
        on_place(buf, x, i0)
        return p0(buf, x, i0, *a, **kw)

    setattr(sfx, kernel, k1)
    sfx._place = p1

    def restore():
        setattr(sfx, kernel, k0)
        sfx._place = p0
    return restore


def behaviour_checks(names, check):
    """Rhythm / structure promises of individual effects (instrumented renders, so they test the generator itself)."""
    if "night" in names:
        # every cricket pauses now and then (the nearest one drops back to about half level) at the default length
        ev = []
        restore = _spy("_k_chirp", lambda a: ev.append([a[2], 0.0]),
                       lambda buf, x, i0: ev[-1].__setitem__(1, float(np.abs(x).max()))
                       if x.ndim == 1 and len(x) < len(buf) and ev else None)
        try:
            worst = []
            for seed in range(4):
                ev.clear()
                sfx.make("night", sfx.NAMES["night"][1], SR, seed=seed)
                groups = []
                for fc, pk in ev:
                    for g in groups:
                        if abs(fc / g[0][0] - 1) < 0.02:
                            g.append((fc, pk))
                            break
                    else:
                        groups.append([(fc, pk)])
                worst += [min(pk for _, pk in g) / max(pk for _, pk in g) if max(pk for _, pk in g) > 0 else 1.0
                          for g in groups]                # a cricket that never sounds fails too
        finally:
            restore()
        check(max(worst) < 0.6, f"night: every cricket pauses or drops back at the default length, seeds 0-3 "
              f"(softest chirp / loudest per cricket: max {max(worst):.2f})")
    if "oars" in names:
        # a whole number of evenly spaced strokes at any loop length, close to the 1.4 s cycle
        ons = []
        pending = [False]

        def on_place(buf, x, i0):
            if pending[0]:
                ons.append((len(buf), i0 % len(buf)))
                pending[0] = False

        restore = _spy("_k_oar", lambda a: pending.__setitem__(0, True), on_place)
        try:
            res = []
            for T in (2.3, 3.5, 5.0, 7.7, 11.9):
                ons.clear()
                sfx.make("oars", T, SR, seed=3)
                n = int(round(T * SR))
                tt = np.sort([i for L, i in ons if L == n]) / SR
                st = [tt[0]]
                for v in tt[1:]:                     # two blades per stroke, a few ms apart
                    if v - st[-1] > 0.1:
                        st.append(v)
                g = np.diff(np.append(st, st[0] + T))
                res.append((T, g.mean(), (g.max() - g.min()) / g.mean()))
        finally:
            restore()
        check(all(abs(m / 1.4 - 1) <= 0.25 and s <= 0.25 for _, m, s in res),
              "oars: evenly spaced strokes near 1.4 s at 2.3-11.9 s loops ("
              + ", ".join(f"{T:g} s: {m:.2f} s +-{50 * s:.0f}%" for T, m, s in res) + ")")
    if "rooster" in names:
        # the crow itself lasts over a second (10 ms RMS within 25 dB of its loudest)
        lens = []
        for seed in range(4):
            m = sfx.make("rooster", None, SR, seed=seed).mean(axis=1).astype(np.float64)
            h = int(0.01 * SR)
            e = 10 * np.log10((m[: len(m) // h * h].reshape(-1, h) ** 2).mean(axis=1) + 1e-20)
            on = np.flatnonzero(e > e.max() - 25)
            lens.append((on[-1] + 1 - on[0]) * 0.01)
        check(min(lens) >= 1.0, f"rooster: the crow lasts over a second, seeds 0-3 ({min(lens):.2f}-{max(lens):.2f} s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="effects to render (default: all)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dur", type=float, default=None, help="loop length override (s)")
    ap.add_argument("--checks", action="store_true", help="run API checks too")
    ap.add_argument("--sweep", action="store_true", help="loudness/balance sweep over lengths and seeds")
    ap.add_argument("--side", action="store_true", help="also write spectrograms_side.png (side channel)")
    ap.add_argument("--all", action="store_true", help="--checks --sweep --side")
    ap.add_argument("--each", action="store_true", help="also write spec_<name>.png per effect")
    ap.add_argument("--debug", action="store_true", help="print component levels logged by the generators")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=len(SWEEP_SEEDS), help="seeds per sweep cell (default 8)")
    a = ap.parse_args()
    if a.all:
        a.checks = a.sweep = a.side = True

    names = a.names or list(sfx.NAMES)
    for nm in names:
        if nm not in sfx.NAMES:
            ap.error(f"unknown effect {nm!r}")
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []

    def log(s=""):
        print(s, flush=True)
        lines.append(s)

    log(f"sfx audition  seed={a.seed}  sr={SR}  ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    results, audio = [], {}
    for nm in names:
        kind, d, _ = sfx.NAMES[nm]
        if a.debug:
            sfx._DEBUG = []
        t0 = time.time()
        x = sfx.make(nm, (a.dur or d) if kind == "loop" else None, SR, seed=a.seed)
        el = time.time() - t0
        sf.write(OUT / f"{nm}.wav", x, SR, subtype="PCM_24")
        audio[nm] = x
        r = analyse(nm, x, el)
        results.append(r)
        log(fmt(r))
        if a.debug:
            for s in sfx._DEBUG:
                log("      " + s)
            sfx._DEBUG = None
    nflag = sum(bool(flags_of(r)) for r in results)
    log(f"\n{len(results)} effects rendered, {nflag} flagged")
    good = True
    if a.checks:
        log()
        good &= api_checks(names, log)
        log("API checks: " + ("ALL PASS" if good else "FAILURES (see above)"))
    if a.sweep:
        log()
        good &= sweep(names, log, a.workers, range(max(1, a.seeds)))
    plot_grid(results, audio, OUT / "spectrograms.png")
    if a.side:
        plot_grid(results, audio, OUT / "spectrograms_side.png", side=True)
    plot_seams(results, audio, OUT / "seams.png")
    if a.each:
        plot_each(results, audio, OUT)
    (OUT / "report.txt").write_text("\n".join(lines) + "\n")
    log(f"wrote {OUT}/<name>.wav, spectrograms.png{', spectrograms_side.png' if a.side else ''}, seams.png, report.txt")
    return 0 if (good and not nflag) else 1


if __name__ == "__main__":
    sys.exit(main())
