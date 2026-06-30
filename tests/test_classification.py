import numpy as np
from src.classification.classifier import extract_features, heuristic_classify
def make_synthetic_planet(period=3.5, depth=0.01, duration=0.15, n=20000, seed=1):
    rng = np.random.default_rng(seed)
    time = np.linspace(0, 200, n)
    flux = np.ones(n) + rng.normal(0, 0.0008, n)
    phase = ((time + period / 2) % period) - period / 2
    in_transit = np.abs(phase) < duration / 2
    flux[in_transit] -= depth
    return time, flux
def make_synthetic_eb(period=3.5, primary_depth=0.03, secondary_depth=0.015, duration=0.15, n=20000, seed=2):
    rng = np.random.default_rng(seed)
    time = np.linspace(0, 200, n)
    flux = np.ones(n) + rng.normal(0, 0.0008, n)
    phase = ((time + period / 2) % period) - period / 2
    in_primary = np.abs(phase) < duration / 2
    v_shape = 1 - np.abs(phase[in_primary]) / (duration / 2)
    flux[in_primary] -= primary_depth * v_shape
    sec_phase = ((time + period / 2 - period / 2) % period) - period / 2
    in_secondary = np.abs(sec_phase) < duration / 2
    v_shape_sec = 1 - np.abs(sec_phase[in_secondary]) / (duration / 2)
    flux[in_secondary] -= secondary_depth * v_shape_sec
    return time, flux
def test_planet_classified_as_transit():
    time, flux = make_synthetic_planet()
    feats = extract_features(time, flux, period=3.5, t0=0, duration=0.15, depth=0.01)
    assert heuristic_classify(feats) == "transit"
def test_eb_classified_as_eclipsing_binary():
    time, flux = make_synthetic_eb()
    feats = extract_features(time, flux, period=3.5, t0=0, duration=0.15, depth=0.03)
    assert heuristic_classify(feats) == "eclipsing_binary"
def test_box_shape_has_high_vu_ratio():
    time, flux = make_synthetic_planet()
    feats = extract_features(time, flux, period=3.5, t0=0, duration=0.15, depth=0.01)
    assert feats["shape_vu_ratio"] > 0.85
def test_v_shape_has_low_vu_ratio():
    time, flux = make_synthetic_eb()
    feats = extract_features(time, flux, period=3.5, t0=0, duration=0.15, depth=0.03)
    assert feats["shape_vu_ratio"] < 0.7