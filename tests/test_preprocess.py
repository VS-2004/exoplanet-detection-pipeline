import numpy as np
import lightkurve as lk
from src.data_acquisition.preprocess import clean_lightcurve
def make_synthetic_transit(n_points=2000, period=3.5, depth=0.01, duration=0.1, seed=0):
    rng = np.random.default_rng(seed)
    time = np.linspace(0, 27, n_points)
    flux = np.ones(n_points) + rng.normal(0, 0.001, n_points)
    phase = ((time + period / 2) % period) - period / 2
    in_transit = np.abs(phase) < (duration / 2)
    flux[in_transit] -= depth
    return time, flux
def test_clean_lightcurve_runs():
    time, flux = make_synthetic_transit()
    lc = lk.LightCurve(time=time, flux=flux)
    t, f = clean_lightcurve(lc)
    assert len(t) == len(f)
    assert len(t) > 0
def test_clean_lightcurve_normalized():
    time, flux = make_synthetic_transit()
    lc = lk.LightCurve(time=time, flux=flux)
    t, f = clean_lightcurve(lc)
    assert abs(np.nanmedian(f) - 1.0) < 0.05
