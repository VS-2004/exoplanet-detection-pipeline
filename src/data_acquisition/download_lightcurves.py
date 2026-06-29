import lightkurve as lk
import argparse
import os
import urllib.request
def download_target(tic_id, download_dir, author="SPOC", exptime=None, tic_sector=None):
    search = lk.search_lightcurve(f"TIC {tic_id}", mission="TESS", author=author, exptime=exptime, sector=tic_sector)
    if len(search) == 0:
        print(f"No light curves found for TIC {tic_id} with author={author} exptime={exptime} sector={tic_sector}")
        return []
    print(search)
    os.makedirs(download_dir, exist_ok=True)
    results = []
    for i in range(len(search)):
        fname = search.table["productFilename"][i]
        try:
            lc = search[i].download(download_dir=download_dir)
            results.append(lc)
            print(f"OK: {fname}")
        except Exception as e:
            print(f"FAILED: {fname} -> {e}")
    return results
def download_sector_bulk_script(sector, out_path):
    url = f"https://archive.stsci.edu/missions/tess/download_scripts/sector/tesscurl_sector_{sector}_lc.sh"
    urllib.request.urlretrieve(url, out_path)
    return out_path
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tic", type=str, default=None)
    parser.add_argument("--sector", type=int, default=None)
    parser.add_argument("--author", type=str, default="SPOC")
    parser.add_argument("--exptime", type=int, default=120)
    parser.add_argument("--out", type=str, default="data/raw")
    args = parser.parse_args()
    if args.tic:
        results = download_target(args.tic, args.out, author=args.author, exptime=args.exptime, tic_sector=args.sector)
        print(f"{len(results)} file(s) downloaded successfully")
    elif args.sector:
        os.makedirs(args.out, exist_ok=True)
        script_path = os.path.join(args.out, f"tesscurl_sector_{args.sector}_lc.sh")
        download_sector_bulk_script(args.sector, script_path)
        print(f"Bulk download script saved to {script_path}")
        print(f"Run: bash {script_path}")
    else:
        print("Provide --tic TIC_ID for a single star or --sector SECTOR_NUM for the full-sector bulk script")