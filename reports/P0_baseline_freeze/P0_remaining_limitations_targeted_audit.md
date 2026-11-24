# P0 Remaining Limitations — Targeted Audit

**Date:** 2026-11-24  
**Working root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original and verified backup:** read-only  
**Mode:** investigation and documentation only; no training, recalibration, or historical-artifact edits.

**Overall status:** **UNRESOLVED — DISCLOSE AS LIMITATION**

---

## A. E05-U Nested GroupKFold and Fold Provenance

### Verified facts

- `nested_cv_calibration_config.json` states:
  - outer CV: GroupKFold, 5 folds;
  - inner CV: GroupKFold, 4 folds;
  - grouping: subject_id;
  - training subjects: 2,018.
- Notebook cell 62 (`nested_cv_oof_predictions.csv` producer) uses:
  - `outer_cv = GroupKFold(n_splits=5)`;
  - `inner_cv = GroupKFold(n_splits=4)`;
  - `GridSearchCV(cv=inner_cv)` inside each outer fold.
- Notebook cell 76 (fully nested uncertainty producer) uses:
  - `outer_cv = GroupKFold(n_splits=5)`;
  - `inner_cv = GroupKFold(n_splits=5)`.
- `nested_cv_fold_results.csv` has 25 rows = 5 targets × 5 outer folds and records `outer_train_subjects`, `outer_validation_subjects`, `selected_alpha`, `inner_cv_best_mae`, and `outer_validation_mae`.
- Outer validation counts are 404/404/404/403/403 per target (2,018 total).
- `nested_cv_oof_predictions.csv` has 10,090 rows, 2,018 subjects and five targets; it has **no outer_fold column**.
- `E05_fully_nested_uncertainty_predictions.csv` has 10,090 rows and five `outer_fold` values; every subject has one outer-fold label.
- No CSV in the E05 directory contains an `inner_fold` column.

### What the evidence supports

- **Outer 5-fold:** supported by config, both code cells, 25 fold-result rows, and five outer_fold values in the uncertainty predictions.
- **Inner 4-fold for the saved point OOF:** supported by config and cell 62 code only. No inner-fold assignment artifact exists.
- **Inner 5-fold for the uncertainty sub-pipeline:** supported by cell 76 code only. This contradicts the config's inner_folds=4.
- **Outer training membership:** not saved. Outer validation membership can be inferred from `outer_fold` labels, but the actual outer training set is not recorded at subject level.
- **Inner training/validation membership:** not saved anywhere.

### Why the uncertainty code uses 5 inner folds

No documented rationale exists in the notebook, config, README, or inventory. The project has no Git history. The 5-fold line in cell 76 is a separate implementation choice from the 4-fold line in cell 62. This audit does **not** infer an unrecorded reason.

### Remaining unknown

The saved artifacts cannot establish inner-fold assignments, inner/outer training-set membership, or no-leakage claims. The full 5×4 nested design is **not proven**.

**Safely resolvable without new experiments:** NO for full provenance; documentation-only disclosure is possible.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION.**

Evidence:

```text
experiments\E05_uncertainty_calibration\nested_cv_calibration_config.json
experiments\E05_uncertainty_calibration\nested_cv_fold_results.csv
experiments\E05_uncertainty_calibration\nested_cv_oof_predictions.csv
experiments\E05_uncertainty_calibration\E05_fully_nested_uncertainty_predictions.csv
notebooks\03_Dataset_Preprocessing.ipynb  (cells 62 and 76)
```

---

## B. Fixed-Alpha Versus Tuned-Alpha Residual Mismatch

### Verified facts

- Keyed merge of `nested_cv_oof_predictions.csv` and `E05_fully_nested_uncertainty_predictions.csv`:
  - **4,438 / 10,090** rows differ by more than 1e-9 in absolute residual;
  - maximum difference **2.645083246527065 cm**;
  - mismatch by target: waist 2,018; hip 1,614; chest 403; shoulder-breadth 403; arm-length 0.
- Source distinction:
  - saved point OOF (cell 62): `Pipeline(StandardScaler, Ridge())` with `GridSearchCV` over alpha `{0.1, 1, 10, 100}`, `GroupKFold(4)` inner; actual residuals are generated from the selected per-fold alpha.
  - fully nested uncertainty audit (cell 76): `BASE_ALPHA = 1.0` fixed; inner `GroupKFold(5)`; residuals are regenerated within each outer training fold.
- The fully nested predictions contain `actual_base_absolute_error`, not the saved point OOF error.

### Classification

This is an **implementation/configuration inconsistency between two E05 sub-pipelines**, not a metric-arithmetic error. The saved point OOF and the uncertainty audit do not use the same base predictor. Because the uncertainty audit intentionally regenerates residuals, the mismatch is also a consequence of a different model configuration; it is not evidence that the saved point OOF arithmetic is wrong.

No historical prediction or residual was replaced.

**Safely resolvable without new experiments:** YES for documentation; the cause is established from code and artifacts.  
**Status: DOCUMENTATION CORRECTION ONLY.**

Evidence:

```text
experiments\E05_uncertainty_calibration\nested_cv_oof_predictions.csv
experiments\E05_uncertainty_calibration\E05_fully_nested_uncertainty_predictions.csv
experiments\E05_uncertainty_calibration\nested_cv_fold_results.csv
notebooks\03_Dataset_Preprocessing.ipynb  (cells 62 and 76)
```

---

## C. Missing Uncertainty-Model Artifact

### Verified facts

- Serialized files found in the reproduction root:
  - `checkpoints\E01_height_only_ridge_models.joblib`;
  - `checkpoints\E02_geometry_comparison_models.joblib`;
  - `checkpoints\E03_view_ablation_models.joblib`;
  - `checkpoints\E04_classical_ml_models.joblib`;
  - audit preservation copies of E01/E04.
- No E05 uncertainty model `.joblib`, `.pkl`, `.pickle`, `.onnx`, `.pt`, or `.pth` exists in the reproduction root.
- The E05 directory contains predictions, metrics, configurations, and code, but no fitted uncertainty model.
- Cell 76 defines the uncertainty models in memory; it does not save them.

### Remaining unknown

The fitted E05-U uncertainty model cannot be reloaded or inspected. Saved predictions alone do not independently prove the fitted model state. No evidence indicates the model is stored elsewhere.

**Safely resolvable without new experiments:** NO without retraining or a newly saved model.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION.**

Evidence:

```text
experiments\E05_uncertainty_calibration\
checkpoints\
notebooks\03_Dataset_Preprocessing.ipynb  (cell 76)
```

---

## D. Missing TestA/TestB Risk Scores

### Verified facts

- `E05_test_prediction_intervals.csv` contains Ridge point predictions, threshold-based intervals and coverage for TestA/TestB. It contains no uncertainty score or risk ranking.
- `E05_selective_verification_risk_analysis.csv` and `E05_tolerance_selective_verification_results.csv` have n=2,018 Train OOF subjects, not TestA/TestB.
- `E05_fully_nested_uncertainty_predictions.csv` contains Train subjects only.
- `E05_verified_ridge_feature_error_dataset.csv` contains TestA/TestB features, predictions and absolute errors, but no uncertainty/risk estimate.

### Remaining unknown

No saved artifact supports TestA/TestB risk ranking. The reported hip ±5 cm 50.7519% capture / 2.5351 enrichment is Train OOF, not TestB.

**Safely resolvable without new experiments:** NO; generating test scores would require using TestA/TestB and is outside this restricted audit.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION.**

Evidence:

```text
experiments\E05_uncertainty_calibration\E05_test_prediction_intervals.csv
experiments\E05_uncertainty_calibration\E05_selective_verification_risk_analysis.csv
experiments\E05_uncertainty_calibration\E05_tolerance_selective_verification_results.csv
experiments\E05_uncertainty_calibration\E05_verified_ridge_feature_error_dataset.csv
```

---

## E. TestB Interval Undercoverage

### Verified measured facts

- All 30 interval groups recompute exactly from saved lower/upper bounds; coverage/gap difference 0.0; mean-width difference ≤7.1e-15 cm.
- TestA mean coverage **0.89885**; 4/15 combinations below nominal.
- TestB mean coverage **0.81200**; **15/15 combinations below nominal**.
- TestB empirical coverage ranges:
  - 80%: 0.6800–0.7300;
  - 90%: 0.8000–0.8525;
  - 95%: 0.8675–0.9225.

### Possible explanation, not established cause

The intervals are fixed Train-OOF thresholds. TestB undercoverage is consistent with distribution shift or calibration drift; feature-shift diagnostics exist, but this audit does not establish causality. No recalibration was performed and TestB cannot be used for tuning.

**Safely resolvable without new experiments:** NO for correcting coverage; documentation-only disclosure is possible.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION.**

Evidence:

```text
experiments\E05_uncertainty_calibration\E05_test_prediction_intervals.csv
experiments\E05_uncertainty_calibration\E05_heldout_coverage_summary.csv
reports\P0_baseline_freeze\P0_5_coverage_recomputation.csv
experiments\E05_uncertainty_calibration\E05_feature_distribution_shift_summary.csv
```

---

## F. Shared TestA–TestB Source ID

### Verified facts

- Exact ID: `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`.
- Present in:
  - `testA_subject_to_photo_map.csv` — 22 rows;
  - `testB_subject_to_photo_map.csv` — 7 rows;
  - both split hwg/measurement and photos-per-subject tables;
  - `problematic_image_audit.csv`.
- TestA: 22 official pairs; TestB: 6 official pairs after one QC exclusion.
- Conflicting attributes:
  - TestA `height_cm` 163.2; TestB 168.0;
  - measurement and target values also differ.
- The official split retains the ID; no removal or reassignment was made.
- `reports\subject_split_integrity_audit.md` records that the reason is not established.

### Remaining unknown

No source-level provenance or authoritative metadata establishes that the two records represent the same person. Identity must not be inferred from the ID alone. No evidence explains why the source ID repeats.

**Safely resolvable without new experiments:** NO without authoritative source metadata; documentation-only disclosure is possible.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION.**

Evidence:

```text
dataset\BodyM\metadata\testA_subject_to_photo_map.csv
dataset\BodyM\metadata\testB_subject_to_photo_map.csv
dataset\BodyM\metadata\testA_hwg_metadata.csv
dataset\BodyM\metadata\testB_hwg_metadata.csv
dataset\BodyM\metadata\testA_measurements.csv
dataset\BodyM\metadata\testB_measurements.csv
reports\subject_split_integrity_audit.md
```

---

## G. TestB Clean-Manifest 1,159 vs 1,158

### Verified facts

- `testB_clean_manifest.csv`: **1,159 rows**.
- Official `testB_manifest.csv` and `testB_preprocessed_manifest.csv`: **1,158 rows**.
- The single extra row is:

```text
subject_id: TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ
photo_id:   578f12cd7dbbf39ccebc3116eaea41d6
height_cm:  168.0
split:      testB
```

- The pair is recorded as QC-excluded in `problematic_image_audit.csv` (“Foreground silhouette truncated at bottom image boundary”).
- The clean manifest was not modified; official manifests and splits were not modified.

### Remaining unknown

The precise reason the stale QC row remains in the clean manifest is not documented. Repair would alter a historical manifest and is not permitted.

**Safely resolvable without new experiments:** YES for documentation only; no safe source edit.  
**Status: DOCUMENTATION CORRECTION ONLY.**

Evidence:

```text
dataset\BodyM\processed\testB_clean_manifest.csv
dataset\BodyM\processed\testB_manifest.csv
dataset\BodyM\processed\preprocessed_manifests\testB_preprocessed_manifest.csv
dataset\BodyM\metadata\problematic_image_audit.csv
reports\qc_exclusion_summary.csv
```

---

## H. Historical Colab Environment and Execution Evidence

### Available evidence

`reference\environment_report-colab-original.txt` reports:

```text
Python 3.13.16
Linux x86_64 / glibc 2.39
PyTorch 2.14.1+cu130
OpenCV 4.14.0
NumPy 2.4.6
pandas 2.2.3
scikit-learn 1.6.1
GPU: Tesla T4
CUDA: 13.0
```

`reference\requirements-colab-original.txt` is the archived freeze (14,161 bytes). README says notebooks were run top-to-bottom; `PROJECT_INVENTORY.md` provides execution order and notes original Colab outputs.

Current `notebooks\03_Dataset_Preprocessing.ipynb` metadata names `.venv (3.14.6)` and Python 3.14.6; it reflects the local environment, not the historical Colab kernel.

### Unverifiable information

No exact historical command, kernel spec, session log, GPU session identifier, or complete warning stream is archived. Hardware model and package versions are documented in the reference report, but exact runtime behavior cannot be proven.

**Safely resolvable without new experiments:** PARTIAL — environment facts are documented; exact command/runtime is not recoverable.  
**Status: UNRESOLVED — DISCLOSE AS LIMITATION** (uses only the available archived environment facts).

Evidence:

```text
reference\environment_report-colab-original.txt
reference\requirements-colab-original.txt
README.md
PROJECT_INVENTORY.md
notebooks\03_Dataset_Preprocessing.ipynb  (metadata)
environment_report.txt
```

---

## Status Summary

| Issue | Status | Safely resolvable now? |
|---|---|---|
| A. Nested 5×4 provenance | UNRESOLVED — DISCLOSE AS LIMITATION | No (new audited run needed for full proof) |
| B. Fixed vs tuned alpha | DOCUMENTATION CORRECTION ONLY | Yes (cause documented) |
| C. Missing uncertainty model | UNRESOLVED — DISCLOSE AS LIMITATION | No |
| D. Missing test risk scores | UNRESOLVED — DISCLOSE AS LIMITATION | No (forbidden Test scoring) |
| E. TestB undercoverage | UNRESOLVED — DISCLOSE AS LIMITATION | No (would require recalibration/external validation) |
| F. Shared source ID | UNRESOLVED — DISCLOSE AS LIMITATION | No (authoritative source needed) |
| G. TestB clean-manifest discrepancy | DOCUMENTATION CORRECTION ONLY | Yes (document; no manifest edit) |
| H. Historical Colab environment | UNRESOLVED — DISCLOSE AS LIMITATION | Partial (environment documented; command/runtime not) |

**Overall: UNRESOLVED — DISCLOSE AS LIMITATION.**

No historical notebook, dataset, manifest, prediction, metric, checkpoint or E05 artifact was modified. This is not the final supervisor report.
