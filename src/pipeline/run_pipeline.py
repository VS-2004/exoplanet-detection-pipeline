import argparse
import os
from src.data_acquisition.preprocess import load_and_clean, save_cleaned
def run_single(filepath, star_id, out_dir="data/processed"):
    time, flux = load_and_clean(filepath)
    save_cleaned(star_id, time, flux, out_dir)
    return time, flux
def run_batch(raw_dir, out_dir="data/processed"):
    results = []
    for root, dirs, files in os.walk(raw_dir):
        for fname in files:
            if fname.endswith(".fits"):
                star_id = fname.split(".")[0]
                try:
                    time, flux = run_single(os.path.join(root, fname), star_id, out_dir)
                    results.append({"star_id": star_id, "status": "ok", "n_points": len(time)})
                except Exception as e:
                    results.append({"star_id": star_id, "status": "failed", "error": str(e)})
    return results
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", type=str, default="data/raw")
    parser.add_argument("--out_dir", type=str, default="data/processed")
    args = parser.parse_args()
    results = run_batch(args.raw_dir, args.out_dir)
    print(f"Processed {len(results)} files")