import lightkurve as lk
import numpy as np
import pandas as pd
import os
def clean_lightcurve(lc, sigma_upper=5, sigma_lower=20, window_length=401):
    lc = lc.remove_nans()
    lc = lc.remove_outliers(sigma_upper=sigma_upper, sigma_lower=sigma_lower)
    lc = lc.flatten(window_length=window_length)
    flux = lc.flux.value
    time = lc.time.value
    flux = flux / np.nanmedian(flux)
    return time, flux
def load_and_clean(filepath, sigma_upper=5, sigma_lower=20, window_length=401):
    lc = lk.read(filepath)
    return clean_lightcurve(lc, sigma_upper, sigma_lower, window_length)
def save_cleaned(star_id, time, flux, out_dir="data/processed"):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame({"time": time, "flux": flux})
    df.to_csv(os.path.join(out_dir, f"{star_id}.csv"), index=False)
def load_cleaned(star_id, in_dir="data/processed"):
    df = pd.read_csv(os.path.join(in_dir, f"{star_id}.csv"))
    return df["time"].values, df["flux"].values
