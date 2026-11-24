# 04 — P0 Configuration and Reproduction

**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only

This document consolidates the E01 and E04 configurations, execution methods, isolation evidence, and reproduction results.

---

## 1. Execution entry points

| Experiment | Entry point | Method |
|---|---|---|
| E01 | Notebook `03_Dataset_Preprocessing.ipynb`, cell **44** | Bootstrap prefix (cell 1) + E01 cell only |
| E04 | Notebook `03_Dataset_Preprocessing.ipynb`, cell **54** | Bootstrap prefix (cell 1) + full E04 cell |

No standalone training scripts exist. The notebook cells were executed via a Python driver that read the unmodified notebook, executed only the bootstrap prefix and target cell, and redirected output to the run log.

- E01 cell source SHA-256: `fbd5b8e5f8a971288a88de9fa983b5fa54f4a68cd8ddf2fd568e1ac95b02ca1c`
- E04 cell source SHA-256: `69950cfb2090d45d0e4e5e51857dba88d55a4458b86e4ce2649010b3cfee53eb`

E01 was not rerun during E04. E02, E03, and E05 were not executed.

---

## 2. E01 configuration

**Inputs:**

```text
dataset\BodyM\processed\preprocessed_manifests\train_preprocessed_manifest.csv
dataset\BodyM\processed\preprocessed_manifests\testA_preprocessed_manifest.csv
dataset\BodyM\processed\preprocessed_manifests\testB_preprocessed_manifest.csv
```

- Rows: 6,133 Train / 1,684 TestA / 1,158 TestB.
- Unique subjects: 2,018 / 87 / 400.
- Input feature: `height_cm` only.
- Targets, in order: `chest`, `waist`, `hip`, `shoulder-breadth`, `arm-length`.
- Subject aggregation: `.first()` per `subject_id` after asserting consistent subject labels.
- Target unit: cm.
- Baseline: training target median across the 2,018 training subjects.
- Model: `StandardScaler + Ridge(alpha=1.0)`, one per target; no CV; no random seed.
- Training split: Train only. TestA/TestB used only after fit.

**Outputs:**

```text
experiments\E01_height_only\E01_config.json
experiments\E01_height_only\training_target_medians.csv
experiments\predictions\E01_height_only_predictions.csv
experiments\metrics\E01_height_only_metrics.csv
checkpoints\E01_height_only_ridge_models.joblib
```

E01 result: **exact reproduction**. Predictions 487/487 rows, metrics 20/20, all five artifacts byte-identical to the backup. Cell time 0.795 s; wall time 6.592 s; exit 0.

---

## 3. E04 configuration

**Inputs:**

```text
experiments\E02_geometry\subject_level_features\train_subject_features.csv
experiments\E02_geometry\subject_level_features\testA_subject_features.csv
experiments\E02_geometry\subject_level_features\testB_subject_features.csv
```

- Rows: 2,018 Train / 87 TestA / 400 TestB.
- Columns: 61; model features: 53.
- Features, in order: `height_cm` + 26 `front_*` + 26 `side_*`; exact order matches `E04_experiment_config.json`.
- Feature aggregation: E02 subject-level median; no additional E04 aggregation.
- Targets, in order: `chest`, `waist`, `hip`, `shoulder-breadth`, `arm-length`.
- Models: Ridge, RandomForest, MLP.
- Validation: `GroupKFold(n_splits=5)`, groups = `subject_id`, 2,018 training subjects; folds 404/404/404/403/403.
- Search: `GridSearchCV`, `scoring="neg_mean_absolute_error"`, `refit=True`, `n_jobs=-1`; Ridge alpha grid `0.1, 1.0, 10.0, 100.0`.
- Random state: 42 (used by RF/MLP; GroupKFold has no shuffle).
- TestA/TestB were not used for model or alpha selection.

**Ridge alpha results:**

| Target | Alpha | CV MAE (cm) |
|---|---:|---:|
| chest | 1.0 | 2.8261939582419444 |
| waist | 10.0 | 3.507116705916009 |
| hip | 10.0 | 2.6184019850468316 |
| shoulder-breadth | 1.0 | 0.8911365617971663 |
| arm-length | 1.0 | 0.8323156232524678 |

**Outputs:**

```text
experiments\E04_classical_ml\E04_experiment_config.json
experiments\E04_classical_ml\E04_cross_validation_results.csv
experiments\predictions\E04_classical_ml_predictions.csv
experiments\metrics\E04_classical_ml_metrics.csv
checkpoints\E04_classical_ml_models.joblib
```

### Full-cell disclosure

There is no Ridge-only execution mode verified for cell 54. The complete cell was executed; RandomForest and MLP were therefore trained as unavoidable additional runs alongside Ridge. No configuration, feature, target, split, or hyperparameter-grid change was made.

E04 result: **exact reproduction** for all three models. Predictions 7,305/7,305 rows, metrics 30/30, CV rows 15/15; all five artifacts byte-identical to the backup. Cell time 893.667 s; exit 0. Seven MLP `ConvergenceWarning` messages were observed; no error occurred.

---

## 4. Isolation and path safety

`DORJIBARI_ROOT` was set before the notebook bootstrap:

```text
D:\DorjiBari-P0-Reproduction\DorjiBari_20261124
```

The bootstrap resolved `PROJECT_ROOT` to exactly that path. All E01/E04 inputs and outputs resolve inside the reproduction root; none points to the original project or backup.

- E01 inputs: 3 preprocessed manifests; all inside/exist.
- E01 outputs: 5 files; all inside.
- E04 inputs: 3 subject-feature tables; all inside/exist.
- E04 outputs: 5 files; all inside.
- Original/backup artifacts were never used as write targets.

---

## 5. Environment

Local reproduction environment:

```text
Python 3.14.6
NumPy 2.5.5
pandas 3.1.1
SciPy 1.18.1
scikit-learn 1.9.1
joblib 1.6.0
matplotlib 3.11.2
ipykernel 7.4.0
```

Original historical environment recorded by the project: Python 3.13.16, NumPy 2.4.6, pandas 2.2.3, scikit-learn 1.6.1, PyTorch 2.14.1+cu130 (GPU). The reproduction is CPU-only.

The direct E01/E04 package versions match the local original `.venv`. Four transitive versions differ locally: IPython 9.19.1 vs 9.18.1, python-dateutil 4.0.0 vs 2.9.0.post0, packaging 26.4 vs 26.3, platformdirs 4.14.8 vs 4.14.7. `pip check` passed and imports succeeded.

---

## 6. Result classification

| Class | E01 | E04 |
|---|---|---|
| Exact artifact match | config, medians, predictions, metrics, checkpoint | config, CV results, predictions, metrics, checkpoint |
| Numerical differences | none | none |
| Test tuning | none | none |
| Warnings | none observed | 7 MLP ConvergenceWarnings |
| Historical command/runtime | not archived; **unverifiable** | not archived; **unverifiable** |
| Colab runtime equivalence | not proven | not proven |

The exact SHA-256 equality is evidence of artifact-level reproduction in this isolated copy. It does not prove that the original Colab hardware/kernel/package runtime behaved identically; that historical execution record is incomplete.

---

## 7. Consolidated evidence

- E01 detailed report: `reports\P0_baseline_freeze\P0_4C_E01_clean_reproduction.md`
- E04 detailed report: `reports\P0_baseline_freeze\P0_4D_E04_clean_reproduction.md`
- Combined run log: `reports\P0_baseline_freeze\P0_clean_run_log.txt`
- E01 pre-run preservation: `reports\P0_baseline_freeze\pre_run_E01\`
- E04 pre-run preservation: `reports\P0_baseline_freeze\pre_run_E04\`
- Reproducibility statement: `reports\P0_baseline_freeze\P0_reproducibility_statement.md`

No supervisor approval is claimed. No P0.5/E05 work was started.
