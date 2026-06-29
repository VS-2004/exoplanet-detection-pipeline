import os
import numpy as np
import pandas as pd
def stitch_sectors(star_ids, processed_dir="data/processed"):
    times, fluxes = [], []
    for star_id in star_ids:
        path = os.path.join(processed_dir, f"{star_id}.csv")
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        times.append(df["time"].values)
        fluxes.append(df["flux"].values)
    if not times:
        return np.array([]), np.array([])
    time = np.concatenate(times)
    flux = np.concatenate(fluxes)
    order = np.argsort(time)
    return time[order], flux[order]
def find_star_ids(tic_id, processed_dir="data/processed"):
    ids = []
    for fname in os.listdir(processed_dir):
        if fname.endswith(".csv") and str(tic_id) in fname:
            ids.append(fname[:-4])
    return sorted(ids)