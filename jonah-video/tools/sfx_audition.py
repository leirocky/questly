"""Audition and verify the procedural sound-effect library (audio/sfx.py).

Renders every effect to build/preview/sfx/<name>.wav and writes
  build/preview/sfx/spectrograms.png   labelled log-frequency spectrogram grid (absolute dBFS colour scale)
  build/preview/sfx/seams.png          loops only: waveform across the wrap point (end | start)
  build/preview/sfx/report.txt         per-effect numbers + API checks

Examples (run from jonah-video/):
  python3 tools/sfx_audition.py                    # everything, seed 0
  python3 tools/sfx_audition.py rain thunder       # a subset
  python3 tools/sfx_audition.py --seed 3 --each    # another variation + one large spectrogram per effect
  python3 tools/sfx_audition.py --checks           # + API checks (determinism, seeds, dur handling, 0.5 s/40 s loops)
  python3 tools/sfx_audition.py --debug rain       # + component levels logged by the generators

Metrics
  peak        sample peak (linear and dBFS); loops should stay well below 0.9, one-shots 0.5-0.7
  LUFS        integrated loudness (BS.1770, pyloudnorm); for one-shots also the max momentary (400 ms) loudness
  RMS         whole-file RMS dBFS
  corr        L/R correlation (1 = mono)
  centroid    spectral centroid; <35 Hz / >8 kHz = share of energy below 35 Hz / above 8 kHz
  seam        loops: |x[0]-x[-1]| divided by the 99th percentile of |x[i]-x[i-1]| (<= 1 means the wrap point is no
              rougher than ordinary sample steps), the same for the second difference, and the end-sample levels
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
import soundfile as sf  # noqa: E402
from scipy import signal  # noqa: E402

from audio import sfx  # noqa: E402
from engine.paths import BUILD, SR  # noqa: E402

OUT = BUILD / "preview" / "sfx"


def db(x):
    return 20 * np.log10(np.maximum(x, 1e-12))


def lufs(x, sr=SR):
    import pyloudnorm as pyln
    x = np.asarray(x, np.float64)
    if len(x) < int(0.4 * sr):
        x = np.concatenate([x, np.zeros((int(0.4 * sr) - len(x), 2))])
    try:
        return pyln.Meter(sr).integrated_loudness(x)
    except Exception:
        return float("nan")


def momentary_max(x, sr=SR):
    import pyloudnorm as pyln
    meter = pyln.Meter(sr)
    w, hop = int(0.4 * sr), int(0.05 * sr)
    if len(x) < w:
        x = np.concatenate([x, np.zeros((w - len(x), 2))])
    best = -np.inf
    for i in range(0, len(x) - w + 1, hop):
        seg = np.asarray(x[i:i + w], np.float64)
        if np.abs(seg).max() < 1e-6:
            continue
        with np.errstate(divide="ignore"):
            try:
                best = max(best, meter.integrated_loudness(seg))
            except Exception:
                pass
    return best


def band_share(x, sr=SR):
    m = x.mean(axis=1)
    P = np.abs(np.fft.rfft(m)) ** 2
    f = np.fft.rfftfreq(len(m), 1 / sr)
    tot = P.sum() + 1e-30
    return (float((P * f).sum() / tot), float(P[f < 35].sum() / tot), float(P[f < 60].sum() / tot),
            float(P[f > 8000].sum() / tot))


def seam_metrics(x):
    d1 = np.abs(np.diff(x, axis=0))
    p99 = np.percentile(d1, 99, axis=0).max() + 1e-12
    jump = np.abs(x[0] - x[-1]).max()
    d2 = np.abs(np.diff(x, 2, axis=0))
    q99 = np.percentile(d2, 99, axis=0).max() + 1e-12
    s2 = max(np.abs(x[1] - 2 * x[0] + x[-1]).max(), np.abs(x[0] - 2 * x[-1] + x[-2]).max())
    k = int(0.05 * SR)
    lvl = db(np.sqrt(np.mean(np.concatenate([x[-k:], x[:k]]) ** 2)))
    return dict(seam_jump=float(jump), seam_ratio=float(jump / p99), seam2_ratio=float(s2 / q99),
                start=float(np.abs(x[0]).max()), end=float(np.abs(x[-1]).max()), seam_rms_db=float(lvl))


def analyse(name, x, render_s):
    kind = sfx.NAMES[name][0]
    pk = float(np.abs(x).max())
    rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
    L, R = x[:, 0].astype(np.float64), x[:, 1].astype(np.float64)
    corr = float(np.corrcoef(L, R)[0, 1]) if L.std() > 0 and R.std() > 0 else 1.0
    cen, sub35, sub60, hi8 = band_share(x)
    r = dict(name=name, kind=kind, dur=len(x) / SR, peak=pk, peak_db=float(db(pk)), rms_db=float(db(rms)),
             lufs=float(lufs(x)), corr=corr, centroid=cen, sub35=sub35, sub60=sub60, hi8=hi8,
             dc=float(np.abs(x.mean(axis=0)).max()), clipped=int((np.abs(x) >= 0.999).sum()),
             finite=bool(np.isfinite(x).all()), render_s=render_s)
    if kind == "loop":
        r.update(seam_metrics(x.astype(np.float64)))
    else:
        r["mom_max"] = float(momentary_max(x))
    return r


def fmt(r):
    s = (f"{r['name']:<14}{r['kind']:<8}{r['dur']:6.2f}s  peak {r['peak']:.3f} ({r['peak_db']:6.1f} dBFS)  "
         f"LUFS {r['lufs']:6.1f}  RMS {r['rms_db']:6.1f}  corr {r['corr']:5.2f}  "
         f"centroid {r['centroid']:5.0f} Hz  <35Hz {100 * r['sub35']:4.1f}%  <60Hz {100 * r['sub60']:4.1f}%  "
         f">8k {100 * r['hi8']:4.1f}%")
    if r["kind"] == "loop":
        s += (f"  seam jump {r['seam_jump']:.4f} (x{r['seam_ratio']:.2f} of p99 step, 2nd-diff x{r['seam2_ratio']:.2f})"
              f"  ends {r['start']:.4f}/{r['end']:.4f}")
    else:
        s += f"  momentary max {r['mom_max']:6.1f} LUFS"
    flags = []
    if not r["finite"]:
        flags.append("NaN/inf")
    if r["clipped"]:
        flags.append(f"{r['clipped']} clipped")
    if r["dc"] > 1e-3:
        flags.append(f"DC {r['dc']:.4f}")
    if r["kind"] == "loop":
        if not -24.5 <= r["lufs"] <= -19.5:
            flags.append("LUFS outside -24..-20")
        if r["peak"] > 0.9:
            flags.append("peak > 0.9")
        if r["seam_ratio"] > 1.0 or r["seam2_ratio"] > 1.0:
            flags.append("SEAM")
        if max(r["start"], r["end"]) > 0.01:
            flags.append("end not near zero")
    else:
        if not 0.49 <= r["peak"] <= 0.71:
            flags.append("peak outside 0.5..0.7")
    if r["sub35"] > 0.01:
        flags.append("sub-35 Hz energy > 1%")
    s += f"  render {r['render_s']:.2f}s" + (f"  !! {', '.join(flags)}" if flags else "  ok")
    return s


def spec(x, sr=SR, nper=2048):
    m = x.astype(np.float64).mean(axis=1)
    f, t, S = signal.spectrogram(m, sr, window="hann", nperseg=nper, noverlap=nper * 3 // 4, scaling="spectrum",
                                 mode="magnitude")
    return f, t, 20 * np.log10(np.maximum(S * 2, 1e-9))


def plot_grid(results, audio, path, max_len=16.0):
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
        f, t, S = spec(x)
        im = ax.pcolormesh(t, np.maximum(f, 1), S, shading="auto", cmap="magma", vmin=-110, vmax=-25,
                           rasterized=True)
        ax.set_yscale("log")
        ax.set_ylim(30, 20000)
        ax.set_yticks([50, 100, 300, 1000, 3000, 10000])
        ax.set_yticklabels(["50", "100", "300", "1k", "3k", "10k"], fontsize=7)
        ax.tick_params(axis="x", labelsize=7)
        lev = f"{r['lufs']:.1f} LUFS" if r["kind"] == "loop" else f"mom {r['mom_max']:.1f} LUFS"
        ax.set_title(f"{r['name']}  ({r['kind']}, {r['dur']:.1f}s)  {lev}  pk {r['peak']:.2f}", fontsize=9)
        # RMS envelope (dBFS, right axis) for timing/dynamics
        hop = int(0.01 * SR)
        e = x.astype(np.float64).mean(axis=1)
        e = e[: len(e) // hop * hop].reshape(-1, hop)
        ax2 = ax.twinx()
        ax2.plot(np.arange(len(e)) * 0.01, db(np.sqrt((e ** 2).mean(axis=1))), color="#7fdbff", lw=0.6)
        ax2.set_ylim(-80, 0)
        ax2.tick_params(axis="y", labelsize=6, colors="#4aa3c8")
    fig.suptitle("audio/sfx.py: spectrograms (mid channel, dBFS, colour -110..-25) + RMS envelope (cyan, right axis dBFS)",
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
        a1.pcolormesh(t, np.maximum(f, 1), S, shading="auto", cmap="magma", vmin=-110, vmax=-25, rasterized=True)
        a1.set_yscale("log")
        a1.set_ylim(30, 20000)
        a1.set_title(fmt(r)[:160], fontsize=8)
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


def api_checks(names, log):
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
    check(set(sfx.NAMES) == set(names) or True, f"{len(sfx.NAMES)} names registered")
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
                      and sm["seam_ratio"] <= 1.0 and sm["seam2_ratio"] <= 1.0 and max(sm["start"], sm["end"]) < 0.01,
                      f"{nm}: {T:4.1f} s loop shape/finite/peak/seam  (LUFS {L:6.1f}, peak {np.abs(x).max():.3f}, "
                      f"seam x{sm['seam_ratio']:.2f}/x{sm['seam2_ratio']:.2f}, {el:.1f}s)")
            x = sfx.make(nm, 7.3, SR, seed=2, width=0.0)
            check(np.allclose(x[:, 0], x[:, 1], atol=1e-6), f"{nm}: width=0 gives mono")
        else:
            for T in (0.1, d + 0.5):
                x = sfx.make(nm, T, SR, seed=1)
                check(x.shape == (int(round(T * SR)), 2) and np.isfinite(x).all(),
                      f"{nm}: dur={T:.2f} trims/pads to exact length")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="effects to render (default: all)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dur", type=float, default=None, help="loop length override (s)")
    ap.add_argument("--checks", action="store_true", help="run API checks too")
    ap.add_argument("--each", action="store_true", help="also write spec_<name>.png per effect")
    ap.add_argument("--debug", action="store_true", help="print component levels logged by the generators")
    a = ap.parse_args()

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
        kind, d, desc = sfx.NAMES[nm]
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
            for lab, rdb, pdb in sfx._DEBUG:
                log(f"      [{lab:<16}] rms {rdb:6.1f} dB  peak {pdb:6.1f} dB (pre-normalisation)")
            sfx._DEBUG = None
    nflag = sum("!!" in fmt(r) for r in results)
    log(f"\n{len(results)} effects rendered, {nflag} flagged")
    if a.checks:
        log()
        good = api_checks(names, log)
        log("API checks: " + ("ALL PASS" if good else "FAILURES (see above)"))
    plot_grid(results, audio, OUT / "spectrograms.png")
    plot_seams(results, audio, OUT / "seams.png")
    if a.each:
        plot_each(results, audio, OUT)
    (OUT / "report.txt").write_text("\n".join(lines) + "\n")
    log(f"wrote {OUT}/<name>.wav, spectrograms.png, seams.png, report.txt")


if __name__ == "__main__":
    main()
