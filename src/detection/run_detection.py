import argparse
from src.detection.stitch import find_star_ids, stitch_sectors
from src.detection.bls_tls import run_bls, run_tls, compute_snr
from src.visualization.plot_lightcurve import plot_phase_folded
def detect_for_tic(tic_id, processed_dir="data/processed", min_period=0.5, max_period=15, tls_window_frac=0.03, out_plot=None):
    star_ids = find_star_ids(tic_id, processed_dir)
    time, flux = stitch_sectors(star_ids, processed_dir)
    if len(time) == 0:
        print(f"No processed data found for TIC {tic_id}")
        return None
    print(f"Stitched {len(star_ids)} sectors, {len(time)} points, time range {time.min():.1f}-{time.max():.1f}")
    print("Running BLS full-range search (fast coarse pass)...")
    bls_result = run_bls(time, flux, min_period, max_period)
    bls_snr = compute_snr(time, flux, bls_result["period"], bls_result["t0"], bls_result["duration"])
    print("BLS:", bls_result, "snr:", bls_snr)
    tls_min = bls_result["period"] * (1 - tls_window_frac)
    tls_max = bls_result["period"] * (1 + tls_window_frac)
    print(f"Running TLS refinement in narrow window [{tls_min:.4f}, {tls_max:.4f}] days around BLS candidate...")
    print("Note: on a multi-year baseline this can still take several minutes even in a narrow window.")
    tls_result = run_tls(time, flux, tls_min, tls_max)
    tls_snr = compute_snr(time, flux, tls_result["period"], tls_result["t0"], tls_result["duration"])
    print("TLS:", tls_result, "snr:", tls_snr)
    duration_disagreement = abs(bls_result["duration"] - tls_result["duration"]) / max(bls_result["duration"], tls_result["duration"])
    if duration_disagreement > 0.3:
        print(f"WARNING: BLS and TLS duration estimates disagree by {duration_disagreement*100:.0f}% "
              f"(BLS={bls_result['duration']:.4f}d, TLS={tls_result['duration']:.4f}d). "
              f"Treat both as coarse detection-stage estimates only - Phase 4 transit model fitting "
              f"(batman) is needed for a trustworthy duration before reporting it.")
    if out_plot:
        plot_phase_folded(time, flux, tls_result["period"], tls_result["t0"], title=f"TIC {tic_id} phase folded at TLS period {tls_result['period']:.4f}d", save_path=out_plot)
        print(f"Saved phase-folded plot to {out_plot}")
    return {"bls": bls_result, "tls": tls_result, "bls_snr": bls_snr, "tls_snr": tls_snr, "n_sectors": len(star_ids), "n_points": len(time)}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tic", type=str, required=True)
    parser.add_argument("--processed_dir", type=str, default="data/processed")
    parser.add_argument("--min_period", type=float, default=0.5)
    parser.add_argument("--max_period", type=float, default=15)
    parser.add_argument("--tls_window_frac", type=float, default=0.03)
    parser.add_argument("--out_plot", type=str, default="results/combined_phase_folded.png")
    args = parser.parse_args()
    detect_for_tic(args.tic, args.processed_dir, args.min_period, args.max_period, args.tls_window_frac, args.out_plot)
    