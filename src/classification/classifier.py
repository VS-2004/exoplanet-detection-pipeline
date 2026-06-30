import numpy as np
from sklearn.ensemble import RandomForestClassifier
def _transit_mask(time, t0, period, duration, factor=1.0):
    phase = ((time - t0 + 0.5 * period) % period) - 0.5 * period
    return np.abs(phase) < (duration * factor / 2)
def odd_even_depth_mismatch(time, flux, t0, period, duration):
    epoch = np.round((time - t0) / period)
    odd_mask = _transit_mask(time, t0, period, duration) & (epoch % 2 == 1)
    even_mask = _transit_mask(time, t0, period, duration) & (epoch % 2 == 0)
    if np.sum(odd_mask) < 5 or np.sum(even_mask) < 5:
        return 0.0
    odd_depth = 1 - np.nanmedian(flux[odd_mask])
    even_depth = 1 - np.nanmedian(flux[even_mask])
    if odd_depth == 0 and even_depth == 0:
        return 0.0
    mismatch = abs(odd_depth - even_depth) / max(abs(odd_depth), abs(even_depth), 1e-8)
    return float(mismatch)
def secondary_eclipse_depth(time, flux, t0, period, duration):
    secondary_t0 = t0 + period / 2
    sec_mask = _transit_mask(time, secondary_t0, period, duration)
    out_mask = ~_transit_mask(time, t0, period, duration, factor=3.0)
    if np.sum(sec_mask) < 5 or np.sum(out_mask) < 5:
        return 0.0
    sec_depth = 1 - np.nanmedian(flux[sec_mask])
    baseline_std = np.nanstd(flux[out_mask])
    if baseline_std == 0:
        return 0.0
    return float(sec_depth / baseline_std)
def transit_shape_vu_ratio(time, flux, t0, period, duration):
    in_mask = _transit_mask(time, t0, period, duration)
    if np.sum(in_mask) < 10:
        return 0.0
    phase = ((time - t0 + 0.5 * period) % period) - 0.5 * period
    in_phase = phase[in_mask]
    in_flux = flux[in_mask]
    order = np.argsort(in_phase)
    in_phase, in_flux = in_phase[order], in_flux[order]
    edge_frac = 0.3
    n = len(in_phase)
    n_edge = max(int(n * edge_frac), 1)
    edge_depth = 1 - np.nanmedian(np.concatenate([in_flux[:n_edge], in_flux[-n_edge:]]))
    center_depth = 1 - np.nanmedian(in_flux[n_edge:-n_edge]) if n - 2 * n_edge > 0 else edge_depth
    if center_depth == 0:
        return 0.0
    return float(edge_depth / center_depth)
def depth_duration_period_consistency(period, duration, depth):
    if duration <= 0 or period <= 0:
        return 0.0
    return float(duration / period)
def extract_features(time, flux, period, t0, duration, depth):
    return {
        "odd_even_mismatch": odd_even_depth_mismatch(time, flux, t0, period, duration),
        "secondary_eclipse_snr": secondary_eclipse_depth(time, flux, t0, period, duration),
        "shape_vu_ratio": transit_shape_vu_ratio(time, flux, t0, period, duration),
        "duration_period_ratio": depth_duration_period_consistency(period, duration, depth),
        "depth": depth,
        "period": period,
        "duration": duration
    }
def heuristic_classify(features, odd_even_threshold=0.3, secondary_snr_threshold=3.0, shape_threshold=0.7):
    if features["secondary_eclipse_snr"] > secondary_snr_threshold:
        return "eclipsing_binary"
    if features["odd_even_mismatch"] > odd_even_threshold:
        return "eclipsing_binary"
    if features["shape_vu_ratio"] >= shape_threshold:
        return "transit"
    return "other"
def train_classifier(X, y, n_estimators=200, random_state=42):
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X, y)
    return model
def predict(model, X):
    return model.predict(X), model.predict_proba(X)