"""PLACEHOLDER sound-effect library (replaced by the real synthesiser)."""
import numpy as np


def make(name, dur, sr=48000, seed=0, **params):
    n = int((dur or 1.0) * sr)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n).astype(np.float32) * 0.02
    return np.stack([x, x], axis=1)
