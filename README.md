# DorjiBari Research

## Project Overview
Smartphone-based body measurement estimation
using front-view image, side-view image,
and measured human height.

## Research Objectives
- Dual-view body measurement regression
- Measurement-specific uncertainty estimation
- Cost-aware accept, retake, and manual verification

## BodyM Target Measurements
1. Chest
2. Waist
3. Hip
4. Shoulder Breadth
5. Arm Length

## Experiments
- E01: Height-only baseline
- E02: Silhouette geometry baseline
- E03: Front vs Side vs Both
- E04: Classical ML comparison
- E05: Uncertainty calibration and tolerance-based selective verification

## Research Rules
- Prevent subject-level data leakage.
- Preserve official dataset splits.
- Never tune using official test sets.
- Save configurations, predictions and metrics.
- Report all measurements in centimetres.

## Dataset
Source: the official BodyM dataset in the public `amazon-bodym` S3 bucket
(region `us-west-2`, unsigned access, no credentials required). The official
Train / TestA / TestB split definitions are preserved.

Expected local layout:

```
dataset/
  BodyM/
    dataset_structure.txt          S3 structure audit
    audit/                         object inventories per split
    metadata/                      source CSVs and QC audit tables
    processed/                     manifests, split-repair backups
    preprocessed_images/
      train/{front,side}/*.png     normalised 256x256 silhouettes
      testA/{front,side}/*.png
      testB/{front,side}/*.png
  Local_Dataset/                   optional local capture images (unused by E01-E05)
```

`dataset/BodyM/` is empty in a fresh checkout. Notebook 02 downloads the
metadata CSVs; notebook 03 downloads the silhouette images and builds the
preprocessed tree (8,975 photo pairs, 17,950 PNG files).

## Environment
### Original environment (Google Colab)
The unmodified Colab records are archived in `reference/`:
`reference/environment_report-colab-original.txt` and
`reference/requirements-colab-original.txt`. They describe:
Python 3.13.16, PyTorch 2.14.1+cu130, OpenCV 4.14.0, NumPy 2.4.6,
Pandas 2.2.3, scikit-learn 1.6.1, Tesla T4 GPU.

The archived freeze is kept for reference only. Do not install it blindly on
another machine.

### Most recent local run
`requirements.txt` and `environment_report.txt` at the project root describe
the most recent notebook 01 run (currently Python 3.14.6, CPU only). Notebook 01
rewrites both files on every run; it creates the `reference/` archive first if
the archive is missing, then never overwrites it. The archive is the Colab
record; the top-level files always describe the latest run.

### Local CPU environment (Python 3.14)
Use `requirements-local.txt`. The pipeline runs on CPU; no CUDA is required.

```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements-local.txt
```

Python 3.14 has no wheels for the exact Colab versions of pandas and NumPy,
so the local pins are newer (pandas 3.x). The APIs used by the notebooks are
unchanged, but small formatting-level differences are possible. Use Colab with
the original freeze when byte-level parity with the recorded run matters.

### VS Code / Jupyter
`.vscode/settings.json` selects `.venv/Scripts/python.exe` and sets the
notebook working directory to the project root. If VS Code still shows missing
imports, select the same interpreter as the notebook kernel:
**Python Environments → `.venv`**. The notebooks detect Google Colab through
`importlib`, not a static `import google.colab`, so Pylance does not report an
unresolved Colab import.

## Notebook Execution Order
1. `notebooks/01_environment_setup.ipynb`
2. `notebooks/02_dataset_audit.ipynb`
3. `notebooks/03_Dataset_Preprocessing.ipynb`

Run each notebook top to bottom. Every notebook starts with the same project
root bootstrap (`_dj_root()`), which resolves the project root in this order:

1. the `DORJIBARI_ROOT` environment variable, if set;
2. `/content/drive/MyDrive/DorjiBari-Research` on Google Colab;
3. the nearest parent directory that contains a `notebooks/` folder.

No path editing is required when moving between Colab and a local checkout.
If no location matches, the notebook stops with an explicit error instead of
writing into an unrelated directory.

### Restart and re-run rules
- Notebook 01 is safe to re-run from top to bottom. It rewrites `README.md`,
  `requirements.txt` and `environment_report.txt`, and creates the `reference/`
  Colab archive only if it is missing.
- Notebook 02 is the authoritative producer of the visual-QC tables
  (`problematic_image_audit.csv`, `alternative_photo_pair_visual_review.csv`).
  Notebook 03 contains a restart-safe fallback: if those files already exist,
  it validates and preserves them instead of overwriting them.
- Notebook 03 cells 28-32 are the recorded subject-overlap investigation. They
  temporarily remove the one TestA/TestB shared subject. Cells 33-34 restore the
  official split membership, so do not stop before cell 34 and do not interpret
  split counts from that temporary state.
- Saved notebook outputs are evidence from the original Colab run, except for
  notebooks 01 and 02, which were deliberately re-executed locally on
  Windows/CPU. Their live outputs describe that local run; the Colab outputs
  stay in `reference/pre-completion-backup/`. Notebook 03 still holds the
  original Colab evidence and must not be re-executed without a backup.
- `reference/pre-completion-backup/` keeps the notebooks and documents exactly
  as they were before this repair pass. The live files can therefore be
  compared against a known earlier state.

## Pipeline Stages
| Stage | Notebook | Content | Main outputs |
|---|---|---|---|
| 1 | 01 | Environment check and project skeleton | `README.md`, `requirements.txt`, `environment_report.txt` |
| 2 | 02 | BodyM audit and QC decisions | `dataset/BodyM/metadata/`, `dataset/BodyM/audit/` |
| 3 | 03 | Manifests, split repair, image preprocessing | `dataset/BodyM/processed/`, `preprocessed_images/` |
| 4 | 03 | E01 height-only baseline | `experiments/E01_height_only/` |
| 5 | 03 | E02 silhouette geometry (52 features) | `experiments/E02_geometry/` |
| 6 | 03 | E03 front / side / both ablation | `experiments/E03_view_ablation/` |
| 7 | 03 | E04 Ridge / RandomForest / MLP comparison | `experiments/E04_classical_ml/` |
| 8 | 03 | E05 uncertainty calibration and selective verification | `experiments/E05_uncertainty_calibration/` |
| 9 | 03 | Evidence consolidation | `reports/` |

## Expected Output Locations
- `dataset/BodyM/` - source metadata, QC audits, manifests, preprocessed silhouettes
- `experiments/E01_height_only/` - E01 config, target medians
- `experiments/E02_geometry/` - feature tables, feature audits, configs
- `experiments/E03_view_ablation/` - ablation config and integrity audit
- `experiments/E04_classical_ml/` - CV results and experiment config
- `experiments/E05_uncertainty_calibration/` - OOF predictions, calibration
  thresholds, coverage, associations, nested uncertainty, risk ranking,
  tolerance-based verification tables
- `experiments/metrics/` - E01-E04 metric tables and the consolidated table
- `experiments/predictions/` - E01-E04 prediction tables
- `experiments/logs/` - preprocessing summary, failures, integrity audit
- `checkpoints/` - fitted model bundles (`joblib`)
- `configs/` - preprocessing configuration
- `figures/` - figures recovered from notebook outputs
- `reports/` - E05 evidence report, inventories and ranking tables
- `src/` - reserved for extracted modules; all logic currently lives in notebooks
- `scripts/` - `validate_project.py`, the project validator (no data required)
- `reference/` - unmodified Colab `requirements.txt` and `environment_report.txt`
  archives; never overwritten by notebook runs

## Reproducing Existing Experiments
1. Create the environment (`requirements-local.txt`) or open the notebooks in
   Colab with the original environment.
2. Run notebook 01 to create the folder skeleton.
3. Run notebook 02 to download the BodyM metadata and produce the QC audits.
   This requires network access to `amazon-bodym`.
4. Run notebook 03 top to bottom. Stage 3 downloads and preprocesses 17,950
   silhouette images; Stage 9 runs nested cross-validation for E05.

Long-running stages are not executed automatically. Check
`PROJECT_INVENTORY.md` for which artifacts already exist on disk and which
must be regenerated by re-running.

## Known Limitations and Unresolved Dependencies
- The original Colab output tree is not fully present in this checkout. A
  partial local run has produced the BodyM metadata/audit tables, the manifests
  and the Train silhouettes (Stage 3 is still filling the image tree); the
  TestA/TestB images and the `experiments/` tables are still missing.
  `PROJECT_INVENTORY.md` lists every expected artifact, its producing stage,
  and its current status.
- Figures, the preprocessing config and the E05 evidence report were recovered
  from the notebook sources and saved outputs; numeric prediction and metric
  tables must be regenerated by re-running the pipeline.
- TestA and TestB share one subject ID in the official metadata. Train is
  disjoint from both splits, but TestA and TestB are not fully subject-disjoint.
  This is documented as an E05 limitation and must be reported in any write-up.
- E05 tolerances (+/- cm) are illustrative sensitivity thresholds, not clinical
  or industry standards.
- Recommendation thresholds calibrated on Train undercover on TestB (15 of 15
  target/level combinations), so TestB must not be used to tune thresholds.
- E01 waist behaves differently on TestA and TestB; the height-only Ridge model
  does not beat the training-median baseline on TestA. This is carried into E05
  and is not resolved.
- `dataset/Local_Dataset/` is empty by design; no local capture data exists yet.

## Validation
A lightweight validator checks the repairs without downloading data or
running experiments:

```
python scripts/validate_project.py
```

It verifies notebook JSON/nbformat validity, that every code cell compiles,
that the project-root bootstrap is present, that no Colab-only path remains in
executed code, that the required directories exist, that the recovered figures
and reports parse, that `README.md` matches the notebook 01 template, and that
every third-party import is covered by `requirements-local.txt`.

To additionally check what happened to the saved notebook outputs, point it at
the pre-repair notebook copies (PowerShell):

```
$env:DORJIBARI_NOTEBOOK_BACKUP = "D:\DorjiBari-Research\reference\pre-completion-backup"
python scripts/validate_project.py
```

Notebook 03 holds the experiment evidence, so its saved outputs and execution
counts must match the backup exactly. The only accepted difference there is the
removal of an illegal `metadata` key from two `stream` outputs, which nbformat
rejects; the text is byte-identical. Notebooks 01 and 02 were intentionally
re-executed locally, so their output differences are reported as `INFO` lines
instead of failures; the original Colab outputs stay in the backup.

### Verification status
- `python scripts/validate_project.py` passes on the current checkout
  (`ALL CHECKS PASSED`). With `DORJIBARI_NOTEBOOK_BACKUP` set it prints only
  `INFO` lines for notebooks 01 and 02 (re-executed locally) and a strict
  `PASS` for notebook 03.
- Notebook 01 was executed end-to-end in a fresh isolated kernel: all 8 code
  cells completed, the README template reproduced `README.md` byte for byte,
  and the `reference/` archives were unchanged. OpenCV is imported explicitly,
  so the environment report no longer depends on earlier kernel state.
- Notebook 02 was re-executed on the available BodyM metadata; its saved
  outputs describe that local run.
- Notebook 03 was validated statically (JSON, nbformat, cell compilation,
  dependency coverage) and its saved outputs were preserved byte for byte, but
  it was not re-executed end-to-end. It requires the BodyM images from S3 plus
  long preprocessing and nested-CV runs; see `PROJECT_INVENTORY.md` for the
  exact remaining work.

## Project Inventory
See `PROJECT_INVENTORY.md` for the complete artifact inventory, recovery
provenance and remaining regeneration steps.
