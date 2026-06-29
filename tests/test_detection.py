import numpy as np
from tests.test_preprocess import make_synthetic_transit
from src.detection.bls_tls import run_bls, run_tls, compute_snr
def test_bls_recovers_period():
    time, flux = make_synthetic_transit(n_points=4000, period=3.5, depth=0.01, duration=0.12)
    result = run_bls(time, flux, min_period=0.5, max_period=15)
    assert abs(result["period"] - 3.5) < 0.05
    assert result["sde"] > 5
def test_tls_recovers_period():
    time, flux = make_synthetic_transit(n_points=4000, period=3.5, depth=0.01, duration=0.12)
    result = run_tls(time, flux, min_period=0.5, max_period=15)
    assert abs(result["period"] - 3.5) < 0.05
    assert result["sde"] > 5
def test_compute_snr_positive_for_real_transit():
    time, flux = make_synthetic_transit(n_points=4000, period=3.5, depth=0.01, duration=0.12)
    snr = compute_snr(time, flux, period=3.5, t0=0, duration=0.12)
    assert snr > 5
def test_compute_snr_low_for_pure_noise():
    rng = np.random.default_rng(1)
    time = np.linspace(0, 27, 4000)
    flux = np.ones(4000) + rng.normal(0, 0.001, 4000)
    snr = compute_snr(time, flux, period=3.5, t0=0, duration=0.12)
    assert abs(snr) < 5
