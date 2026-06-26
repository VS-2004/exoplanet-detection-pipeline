# AI-Enabled Exoplanet Detection Pipeline

Detects and classifies periodic dips in TESS light curves (transits, eclipses, blends, other) and estimates transit parameters (period, depth, duration) with uncertainties.

## Status
- [x] Phase 0: Setup
- [x] Phase 1: Data acquisition + preprocessing (tested on synthetic data, ready for real TESS data)
- [ ] Phase 2: Detection (BLS/TLS) — stub in `src/detection/bls_tls.py`
- [ ] Phase 3: Classification — stub in `src/classification/classifier.py`
- [ ] Phase 4: Parameter estimation — stub in `src/parameter_estimation/transit_fit.py`
- [ ] Phase 5: Pipeline integration — `src/pipeline/run_pipeline.py`
- [x] Phase 6: Visualization — working in `src/visualization/plot_lightcurve.py`
- [ ] Phase 7: QA / validation
- [ ] Phase 8: Report

Full task breakdown with owners: see `reports/task_breakdown.md`.

## Setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Getting TESS data
Single star (for prototyping/testing):
```
python -m src.data_acquisition.download_lightcurves --tic <TIC_ID> --out data/raw
```
Full sector (20-30k stars, via MAST bulk download script):
```
python -m src.data_acquisition.download_lightcurves --sector <SECTOR_NUM> --out data/raw
bash data/raw/tesscurl_sector_<SECTOR_NUM>_lc.sh
```

## Running preprocessing
```
python -m src.pipeline.run_pipeline --raw_dir data/raw --out_dir data/processed
```

## Running tests
```
python -m pytest tests/ -v
```
Tests use a synthetic transit light curve generated in-code, so they don't require any TESS data download.

## Project structure
```
src/
  data_acquisition/   download + clean light curves
  detection/           BLS/TLS periodic dip search
  classification/      transit/eclipse/blend/other classifier
  parameter_estimation/  transit model fitting
  pipeline/            chains all stages together
  visualization/       plotting
data/
  raw/        downloaded FITS files (gitignored)
  processed/  cleaned time/flux CSVs (gitignored)
  labels/     curated training labels
results/      output plots and result tables
reports/      final 3-page report
```

## Team
| Owner | Phase |
|---|---|
| Data/Integration | Phases 1, 5 |
| Detection Lead | Phase 2 |
| Classification Lead | Phases 3, 4 |
| Viz/QA/Report | Phases 6, 7, 8 |
