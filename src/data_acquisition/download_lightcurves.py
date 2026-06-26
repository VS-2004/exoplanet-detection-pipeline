import lightkurve as lk
import argparse
import os
import urllib.request
def download_target(tic_id, download_dir):
    search = lk.search_lightcurve(f"TIC {tic_id}", mission="TESS")
    os.makedirs(download_dir, exist_ok=True)
    return search.download_all(download_dir=download_dir)
def download_sector_bulk_script(sector, out_path):
    url = f"https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_{sector}_lc.sh"
    urllib.request.urlretrieve(url, out_path)
    return out_path
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tic", type=str, default=None)
    parser.add_argument("--sector", type=int, default=None)
    parser.add_argument("--out", type=str, default="data/raw")
    args = parser.parse_args()
    if args.tic:
        result = download_target(args.tic, args.out)
        print(result)
    elif args.sector:
        os.makedirs(args.out, exist_ok=True)
        script_path = os.path.join(args.out, f"tesscurl_sector_{args.sector}_lc.sh")
        download_sector_bulk_script(args.sector, script_path)
        print(f"Bulk download script saved to {script_path}")
        print(f"Run: bash {script_path}")
    else:
        print("Provide --tic TIC_ID for a single star or --sector SECTOR_NUM for the full-sector bulk script")
