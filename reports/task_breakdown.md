# Exoplanet Detection Pipeline — Task Breakdown

**Roles:** S1 = Strong #1 (Detection Lead) · S2 = Strong #2 (Classification Lead) · A = Average (Data/Integration) · W = Weak (Viz/QA/Report)

---

## Phase 0 — Setup
- [ ] (A) Create shared GitHub repo, folder structure, `requirements.txt`
- [ ] (All) Install core libs: `lightkurve`, `astropy`, `transitleastsquares`, `wotan`, `batman-package`, `scikit-learn`, `xgboost`, `matplotlib`/`plotly`
- [ ] (S1+S2) Pull ~50 sample light curves to prototype against before full data lands

## Phase 1 — Data Acquisition & Preprocessing (Owner: A)
- [ ] Download one TESS sector via `lightkurve.search_lightcurve` (MAST) instead of manual archive browsing
- [ ] Download curated labeled set (confirmed planets / false positives / eclipsing binaries) — supplement from TOI catalog / NASA Exoplanet Archive dispositions if needed
- [ ] Write FITS → flux/time array parser
- [ ] Detrending (flatten with `wotan`/`lightkurve`) + sigma-clip outliers + normalize flux
- [ ] Save cleaned light curves in a standard format (one file per star, e.g. parquet/CSV)
- [ ] **Deliverable:** clean light-curve dataset + labeled training table, handed to S1/S2

## Phase 2 — Periodic Dip Detection (Owner: S1)
- [ ] Implement Box Least Squares (BLS) search
- [ ] Implement Transit Least Squares (TLS) search (gives SDE significance built-in)
- [ ] Compute SNR / significance metric per candidate
- [ ] Tune detection threshold to control false positives
- [ ] Build phase-folding utility (reusable by S2 and W)
- [ ] **Deliverable:** candidate table — `star_id, period, t0, duration, depth, SNR` — fixed format, shared early so others can build against it

## Phase 3 — Classification (Owner: S2)
- [ ] Engineer features: transit shape (U vs V), odd-even depth mismatch, secondary eclipse presence, depth/duration/period self-consistency, centroid shift if available
- [ ] Train baseline classifier (Random Forest / XGBoost) on curated labels
- [ ] Cross-validate, report accuracy/precision/recall
- [ ] (Stretch) CNN on phase-folded image inputs
- [ ] **Deliverable:** class label (transit/eclipse/blend/other) + confidence score per candidate

## Phase 4 — Parameter Estimation (Owner: S2, support from S1)
- [ ] Fit transit model (`batman` or `exoplanet`) to phase-folded transit candidates
- [ ] Re-estimate period, duration, depth with uncertainties (bootstrap or simple MCMC)
- [ ] Flag low-confidence/poor fits
- [ ] **Deliverable:** final parameter table with error bars

## Phase 5 — Pipeline Integration (Owner: A)
- [ ] Chain Phases 1→2→3→4 into one runnable script/notebook with config
- [ ] Batch runner across full sector (thousands of stars)
- [ ] Logging + error handling for failed fits/missing data
- [ ] Consolidate into one results table: `star_id, period, depth, duration, class, confidence, SNR`
- [ ] **Deliverable:** end-to-end pipeline + master results file

## Phase 6 — Visualization (Owner: W)
- [ ] Raw light curve plot
- [ ] Phase-folded plot with fitted model overlay
- [ ] Annotate class, confidence, SNR, parameters directly on plot
- [ ] Batch-generate plots for top-N candidates
- [ ] (Optional) simple results dashboard (plotly/streamlit)
- [ ] Can start as soon as S1 has *any* sample output — doesn't need to wait for full pipeline

## Phase 7 — QA / Validation (Owner: W, support from all)
- [ ] Sanity-check pipeline on known confirmed TOIs — does it recover them correctly?
- [ ] Spot-check a sample of misclassifications
- [ ] Compile validation summary (precision/recall on labeled holdout set)

## Phase 8 — Report (Owner: W, content fed in by S1/S2/A)
- [ ] Methodology section (S1 + S2 provide technical write-ups of their methods)
- [ ] Assumptions made
- [ ] Tools/libraries used
- [ ] Uncertainty estimation explanation (from Phase 4)
- [ ] Results + example figures (from Phase 6/7)
- [ ] Final formatting to fit 3-page limit

---

## Dependency Order
1. **A** starts data download immediately; **S1/S2** prototype in parallel on ~50-star sample
2. Once **S1** fixes candidate-table format → **S2** and **A** build against it
3. Once **S2** has class+confidence output → **A** finishes integration; **W** starts visualization
4. **W** runs QA once full results table exists, then writes report using everyone's notes
