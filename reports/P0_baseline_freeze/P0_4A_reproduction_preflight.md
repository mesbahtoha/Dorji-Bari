# P0.4A — Clean Reproduction Preflight

**Date:** 2026-11-24  
**Root:** `D:\DorjiBari-Research`  
**Mode:** read-only; no training, tuning, source edits, or artifact writes performed.  
**Backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124`

Scope: A) E01 height-only median + Ridge; B) E04 Ridge with 5-fold GroupKFold by `subject_id`.

---

## 1. Entry points and historical command

### Exact entry points

There are **no standalone E01/E04 training scripts** in `scripts/`. The only script there is `scripts\validate_project.py` (structural validation, not training).

| Experiment | Entry point | Exact code location |
|---|---|---|
| E01 | `notebooks\03_Dataset_Preprocessing.ipynb`, Stage 5 (0-based cell index **44**) | `load_subject_level_data()`, Ridge fit loop, evaluation, config write |
| E04 | `notebooks\03_Dataset_Preprocessing.ipynb`, Stage 8 (0-based cell index **54**) | data load, feature selection, `GroupKFold`, `GridSearchCV`, evaluation, config write |

- E01 cell 44 defines `load_subject_level_data(split)`, trains one `StandardScaler + Ridge` pipeline per target, and writes metrics, predictions, medians, config, and checkpoint.
- E04 cell 54 defines the feature matrix and `model_searches`, runs `GridSearchCV` for Ridge, RandomForest, and MLP, then writes predictions, metrics, CV results, config, and checkpoint.
- Both cells contain their own imports but depend on `PROJECT_ROOT` from the notebook bootstrap in cell **1** (`_dj_root()`).
- E04 cell 54 is **not Ridge-selectable**: it always fits Ridge, RandomForest, and MLP. There is no separate Ridge-only entry point.

### Historical command

**NOT VERIFIABLE — no exact command is documented.**

The archived instructions only say to run notebooks top-to-bottom:

1. `notebooks\01_environment_setup.ipynb`
2. `notebooks\02_dataset_audit.ipynb`
3. `notebooks\03_Dataset_Preprocessing.ipynb`

Evidence: `README.md` lines 100–114 and `PROJECT_INVENTORY.md` lines 221–229. No `nbconvert`, `papermill`, `jupyter execute`, or equivalent training command is recorded anywhere in the project. No CLI command should be invented.

The original artifacts came from a Colab run; notebook 03 was not re-executed locally (`PROJECT_INVENTORY.md` lines 260–263).

---

## 2. Inputs and dependencies

### E01 inputs

`dataset\BodyM\processed\preprocessed_manifests\{train,testA,testB}_preprocessed_manifest.csv`

| Split | Rows (photo pairs) | Unique subjects | Columns | Missing height/targets |
|---|---:|---:|---:|---:|
| Train | 6,133 | 2,018 | 16 | 0 |
| TestA | 1,684 | 87 | 16 | 0 |
| TestB | 1,158 | 400 | 16 | 0 |

E01 loads `subject_id`, `height_cm`, and the five targets, verifies that each subject's labels are consistent, then collapses photo rows to one row per subject with `.first()`. It does **not** read images when these manifests exist.

### E04 inputs

`experiments\E02_geometry\subject_level_features\{train,testA,testB}_subject_features.csv`

| Split | Rows | Unique subjects | Columns | Geometry features | Missing/non-finite |
|---|---:|---:|---:|---:|---:|
| Train | 2,018 | 2,018 | 61 | 52 | 0 / 0 |
| TestA | 87 | 87 | 61 | 52 | 0 / 0 |
| TestB | 400 | 400 | 61 | 52 | 0 / 0 |

E04 selects `[height_cm] + all columns starting with front_ or side_`. The resulting 53-feature order **exactly matches** `E04_experiment_config.json`.

Upstream dependency: these feature tables are produced by E02 cell **46** from `preprocessed_manifests` and the 17,950 processed silhouettes. The tables exist now. A from-raw reproduction must also reproduce E02 feature extraction and therefore needs `dataset\BodyM\preprocessed_images\` and the E02 stage, not just cell 54.

### Required packages

Verified installed in `.venv`:

```text
Python  3.14.6
numpy   2.5.5
pandas  3.1.1
scikit-learn 1.9.1
scipy   1.18.1
joblib  1.6.0
```

`requirements-local.txt` pins the same versions. E01/E04 need `numpy`, `pandas`, `scikit-learn`, `joblib`; no GPU or network is required when using the existing manifests/features. Full notebook 03 from raw additionally needs network/S3 and imaging dependencies.

Current shell `python` resolves to `C:\Python314\python.exe`, not the project `.venv`; use `.venv\Scripts\python.exe` explicitly or activate `.venv`.

---

## 3. Target order, feature order, aggregation

| Item | E01 | E04 |
|---|---|---|
| Target order | `chest`, `waist`, `hip`, `shoulder-breadth`, `arm-length` | same five-target order |
| Feature order | `height_cm` only | `height_cm` + 26 `front_*` + 26 `side_*` = 53, in data/column order |
| Aggregation | `.first()` per subject after consistency check | feature table is already subject-level; E02 uses `subject_level_median` |
| Training unit | unique subject (2,018) | unique subject (2,018) |
| Baseline | training target medians (`training_medians = Y_train.median()`) | none |

**Important distinction:** E01 does not aggregate measurements by median. It collapses duplicate subject rows with `.first()` after asserting consistent labels. The saved `training_target_medians.csv` is the median target prediction baseline, and it matches a fresh calculation from the 2,018 training subjects exactly.

E04’s feature table is the E02 subject-level median aggregate (`E02_feature_config.json`: `aggregation: subject_level_median`); E04 performs no further aggregation. `photo_count` is present in the feature table but excluded from `FEATURES`.

---

## 4. Model parameters

### E01

- `Pipeline([("scaler", StandardScaler()), ("ridge", Ridge(alpha=1.0))])`, one model per target.
- No cross-validation, no alpha search, no random seed.
- Training median per target is computed from the 2,018 training subjects.
- TestA/TestB are used only for post-fit evaluation. `E01_config.json` records `test_data_used_for_training: false`.
- Saved medians: chest 101.16202545166016, waist 88.2764778137207, hip 101.24799346923828, shoulder-breadth 36.26937484741211, arm-length 49.67952919006348.

### E04 Ridge

- Estimator: `Pipeline([("scaler", StandardScaler()), ("model", Ridge())])`.
- Search space: `model__alpha ∈ {0.1, 1.0, 10.0, 100.0}`.
- `GridSearchCV`: `scoring="neg_mean_absolute_error"`, `cv=GroupKFold(n_splits=5)`, `groups=train_df["subject_id"].astype(str)`, `refit=True`, `n_jobs=-1`, `return_train_score=False`, `error_score="raise"`.
- Training subjects: 2,018. GroupKFold fold sizes: 404/404/404/403/403 validation subjects.
- `random_state=42` is recorded; it is used by RandomForest and MLP, not by Ridge or GroupKFold. GroupKFold has no shuffle.
- No test data is used for alpha selection; `test_data_used_for_hyperparameter_selection: false`.

CV-selected Ridge parameters (`E04_cross_validation_results.csv`):

| Target | Best CV MAE (cm) | Alpha |
|---|---:|---:|
| chest | 2.8261939582419444 | 1.0 |
| waist | 3.507116705916009 | 10.0 |
| hip | 2.6184019850468316 | 10.0 |
| shoulder-breadth | 0.8911365617971663 | 1.0 |
| arm-length | 0.8323156232524678 | 1.0 |

The same cell also fits RandomForest and MLP; their parameters are defined in cell 54 but are outside the E04 Ridge scope.

---

## 5. Prediction and metric code

| E01 | E04 |
|---|---|
| Test predictions saved per subject, wide format | Test predictions saved per model/target/subject, long format |
| Training-median predictions tiled per subject; Ridge predictions from fitted pipelines | `best_model.predict(X_test)` after refit |
| `mean_absolute_error`, `sqrt(mean_squared_error)`, `r2_score` | same sklearn functions |
| `experiments\predictions\E01_height_only_predictions.csv` | `experiments\predictions\E04_classical_ml_predictions.csv` |
| `experiments\metrics\E01_height_only_metrics.csv` | `experiments\metrics\E04_classical_ml_metrics.csv` |
| `experiments\E01_height_only\E01_config.json` | `experiments\E04_classical_ml\E04_experiment_config.json` |
| `experiments\E01_height_only\training_target_medians.csv` | `experiments\E04_classical_ml\E04_cross_validation_results.csv` |
| `checkpoints\E01_height_only_ridge_models.joblib` | `checkpoints\E04_classical_ml_models.joblib` |

Existing reference artifacts are present: E01 metrics 20 rows, predictions 487 rows, checkpoint 3,863 bytes; E04 metrics 30 rows, predictions 7,305 rows, CV results 15 rows, checkpoint 142,942,729 bytes.

---

## 6. Config archive comparison

| Comparison | Result |
|---|---|
| Current `E01_config.json` vs P0.1B backup | **Byte-identical** (SHA-256 `79b1eb81…`) |
| Current `E04_experiment_config.json` vs P0.1B backup | **Byte-identical** (SHA-256 `421d8624…`) |
| Current notebook config block vs pre-repair archived notebook 03 | **Identical** for both E01 cell 44 and E04 cell 54 |
| Standalone archived E01/E04 config JSON in `reference/pre-completion-backup` | **NOT FOUND** — that archive contains notebooks/documents, not config JSON |

No config drift was found. E01 and E04 config values match the code literals that generate them. The P0.1B backup is a copy of the current state, not an independent historical config set; the pre-repair notebook 03 is the only archived older code source.

---

## 7. Isolation assessment

**Direct in-place execution is NOT SAFE.** Both cells write fixed `PROJECT_ROOT`-relative outputs and would overwrite the existing E01/E04 metrics, predictions, configs, medians/CV, and joblib checkpoints.

A fresh run can be isolated safely:

- `_dj_root()` prioritizes the `DORJIBARI_ROOT` environment variable; all output paths derive from `PROJECT_ROOT` (notebook cell 1).
- Copy the project to a separate directory, set `DORJIBARI_ROOT` to that copy, and run there.
- Use `.venv\Scripts\python.exe` explicitly or activate `.venv`.
- E01 and E04 cells can be run after bootstrap cell 1 using existing manifests/feature tables; no network is needed for that path.
- E04 cell 54 writes a ~143 MB checkpoint; D: has **129.47 GB free**.
- A full notebook 03 top-to-bottom run additionally regenerates Stage 3, requires S3/network, runs E05, and overwrites many artifacts; do not use that path for a narrow E01/E04 reproduction.
- No stage-selection flag or standalone runner exists; cell-level execution is the only narrow route.
- The current `DORJIBARI_ROOT` is unset.

---

## 8. Gaps and limitations

1. No exact historical CLI command is archived.
2. No standalone E01/E04 scripts; both are notebook cells embedded in notebook 03.
3. E04 cell 54 cannot run Ridge alone; it fits all three models.
4. Local scientific versions differ from the recorded Colab run (Python 3.14.6 / sklearn 1.9.1 / pandas 3.1.1 vs Python 3.13.16 / sklearn 1.6.1 / pandas 2.2.3). Exact numerical parity is **not guaranteed**; use the archived Colab environment if byte-level parity is required.
5. A clean from-raw E04 reproduction requires E02 feature generation and 17,950 processed images; using the existing subject-feature tables bypasses that upstream stage.
6. No training was performed in this preflight; readiness is based on code/config/input/dependency inspection.

---

## READINESS

**E01 — READY for isolated reproduction.**  
Entry point is notebook 03 cell 44; `preprocessed_manifests` are present with 2,018/87/400 subjects, the E01 config is unchanged, and required packages are installed. Run only in a copied root with `DORJIBARI_ROOT` set. The exact historical command is **NOT VERIFIABLE**, and local numerical parity with the Colab run is not guaranteed.

**E04 — READY for isolated full-E04 reproduction; NOT READY for a Ridge-only run.**  
Entry point is notebook 03 cell 54; the 53-feature subject tables, 5-fold GroupKFold configuration, Ridge alpha grid, and all inputs are present. However, cell 54 always fits Ridge, RandomForest, and MLP and writes all E04 artifacts; there is no Ridge-only selector. The exact historical command is **NOT VERIFIABLE**, and local numerical parity is not guaranteed. A clean from-raw run also requires the E02 feature-generation stage and processed images.
