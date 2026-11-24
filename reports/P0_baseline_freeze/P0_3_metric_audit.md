# P0.3 — Independent Metric Recomputation

**Date:** 2026-11-24  
**Root:** `D:\DorjiBari-Research`  
**Mode:** read-only; no training, tuning, test-based selection, source edits, or split changes.  
**Scope:** E01–E04, all saved predictions, all targets and both evaluation splits.

**Outputs**

- `reports\P0_baseline_freeze\03_P0_metric_recomputation.csv` — 140 metric rows
- `reports\P0_baseline_freeze\P0_metric_mismatches.csv` — recomputation summary + cross-configuration investigation
- `reports\P0_baseline_freeze\P0_3_metric_audit.md` — this report

---

## 1. Result summary

| Stage | Expected rows | Recomputed | MATCH | MISMATCH | NOT VERIFIABLE |
|---|---:|---:|---:|---:|---:|
| E01 | 20 | 20 | 20 | 0 | 0 |
| E02 | 30 | 30 | 30 | 0 | 0 |
| E03 | 60 | 60 | 60 | 0 | 0 |
| E04 | 30 | 30 | 30 | 0 | 0 |
| **Total** | **140** | **140** | **140** | **0** | **0** |

- Maximum absolute difference: **MAE 1.78e-15 cm**, **RMSE 1.78e-15 cm**, **R² 6.66e-16**.
- Metric rows with recomputation MAE or RMSE difference **> 0.0001 cm: 0**.
- No missing values, non-finite values, or duplicate subject keys were found.
- All 140 rows have **87 (TestA)** or **400 (TestB)** subjects, matching `n_subjects` and the official split manifests.
- All 140 consolidated metric rows agree with their individual metric files (`E01=individual`, etc.).

**Status: all 140 rows MATCH. No metric was repaired or overwritten.**

---

## 2. Prediction schemas and aggregation

| File | Layout | Rows | Key / level | Configurations |
|---|---|---:|---|---|
| `experiments\predictions\E01_height_only_predictions.csv` | wide | 487 | one row per `split,subject_id`; no `photo_id` | 2 methods × 5 targets × 2 splits |
| `experiments\predictions\E02_geometry_comparison_predictions.csv` | wide | 1,461 | one row per `experiment,split,subject_id` | 3 feature sets × 5 × 2 |
| `experiments\predictions\E03_view_ablation_predictions.csv` | wide | 2,922 | one row per `experiment,split,subject_id` | 6 view sets × 5 × 2 |
| `experiments\predictions\E04_classical_ml_predictions.csv` | long | 7,305 | one row per `model,target,split,subject_id` | 3 models × 5 × 2 |

- **All saved predictions are subject-level.** There is no `photo_id` column and no photo-level prediction file.
- E01–E03 use `actual_<target>` and `predicted_<target>` (E01 uses method-specific `median_pred_*` / `ridge_pred_*`).
- E04 uses long `actual` / `predicted` columns.
- E01/E02/E03 have 487 rows per configuration over both splits (87 TestA + 400 TestB); E01 has 486 globally unique subjects because the disclosed TestA–TestB shared ID appears once in each split.
- Per split, each configuration has exactly 87 or 400 unique subjects.
- E02 feature construction documents `aggregation: subject_level_median`; the saved model predictions are already subject-level and were evaluated directly, without a second photo-to-subject aggregation.

### Documented metric calculation

`notebooks\03_Dataset_Preprocessing.ipynb`, cells 44, 48, 51 and 54 compute:

```text
MAE  = mean_absolute_error(y_true, y_pred)
RMSE = sqrt(mean_squared_error(y_true, y_pred))
R²   = r2_score(y_true, y_pred)
```

These are direct subject-level calculations. No hidden grouping or weighted aggregation is used for E01–E04.

Recomputation followed the same formulas on the saved `actual` and `predicted` values, then compared against the full-precision consolidated values in `experiments\metrics\E01_E04_consolidated_metrics.csv`.

---

## 3. Validation evidence

| Check | Result |
|---|---|
| Metric row coverage | 140/140 (E01 20, E02 30, E03 60, E04 30) |
| Reconciled `n_subjects` | 140/140; 87 or 400 |
| Duplicate `(model,target,split,subject)` keys | 0 |
| Missing or non-finite actual/predicted values | 0 |
| Prediction subject IDs match official manifests | 140/140 (`YES`) |
| Actual values match official manifest targets | 0 mismatches |
| Consolidated vs individual metric files | 140/140 agree |
| Units | cm (`MAE_cm`, `RMSE_cm`; E01 config `target_unit=cm`) |

Actual/predicted ranges are consistent with centimetres; no unit conversion was applied. The tested target ranges include chest 76.9–158.1, waist 61.9–137.8, hip 81.1–150.8, shoulder 28.9–43.0, and arm length 41.3–60.2 cm. The shared TestA–TestB subject is retained in both splits and is not treated as a duplicate within either split.

---

## 4. E02/E03 combined vs E04 Ridge — explanation

### Observed TestB metrics

| Target | E02 `height_plus_geometry` MAE | E03 `height_plus_both` MAE | E04 Ridge MAE | Δ E04−E02 | E04 Ridge α | Max abs prediction difference |
|---|---:|---:|---:|---:|---:|---:|
| chest | 3.5484469 | 3.5484469 | 3.5484469 | 0.0000000 | 1.0 | 0.0000000 |
| waist | **4.3704144** | **4.3704144** | **4.2919805** | **−0.0784339** | **10.0** | **2.1281467** |
| hip | **3.5435085** | **3.5435085** | **3.4933525** | **−0.0501561** | **10.0** | **1.6864107** |
| shoulder-breadth | 1.0554480 | 1.0554480 | 1.0554480 | 0.0000000 | 1.0 | 0.0000000 |
| arm-length | 1.0102939 | 1.0102939 | 1.0102939 | 0.0000000 | 1.0 | 0.0000000 |

- E02 and E03 combined predictions are **exactly identical** (maximum difference 0.0) for every target on TestB and TestA.
- E04 Ridge predictions are **exactly identical** to E02/E03 for chest, shoulder breadth, and arm length.
- E04 Ridge differs only for **waist and hip**, where the E04 CV-selected α is **10.0** rather than **1.0**.
- TestA shows the split-specific pattern: waist ΔMAE = −0.000355 cm, hip ΔMAE = **+0.008973 cm** (slightly worse). The TestB gains should not be generalized to TestA or to other targets.

### Configuration comparison

| Aspect | E02 `height_plus_geometry` | E03 `height_plus_both` | E04 Ridge |
|---|---|---|---|
| Feature count | 53 | 53 | 53 |
| Feature order | exact list | exact list | **exactly equal to E02/E03** |
| Feature values / actuals | same subjects and actuals | same subjects and actuals | **same actuals**; 0 differences |
| Prediction IDs | 87/400 per split | 87/400 per split | 87/400 per split |
| Prediction level | subject-level | subject-level | subject-level |
| Estimator | `StandardScaler + Ridge(alpha=1.0)` | `StandardScaler + Ridge(alpha=1.0)` | `StandardScaler + Ridge`, CV-selected α |
| CV selection | none; fixed α | none; fixed α | 5-fold `GroupKFold`, MAE, train only |
| α used for waist / hip | 1.0 / 1.0 | 1.0 / 1.0 | **10.0 / 10.0** |

Evidence:

- `experiments\E02_geometry\E02_experiment_config.json`: `feature_sets.height_plus_geometry` = 53 features; `ridge_alpha=1.0`.
- `experiments\E03_view_ablation\E03_view_ablation_config.json`: `feature_sets.height_plus_both` = 53 features; `ridge_alpha=1.0`.
- `experiments\E04_classical_ml\E04_experiment_config.json`: 53-feature list; `models=["Ridge","RandomForest","MLP"]`; `cv_folds=5`; `cv_selection_metric=MAE`; `test_data_used_for_hyperparameter_selection=false`.
- `experiments\E04_classical_ml\E04_cross_validation_results.csv`: Ridge best α = 1.0 for chest/shoulder/arm, **10.0 for waist and hip**.
- The α grid in notebook cell 54 is `[0.1, 1.0, 10.0, 100.0]`.
- The 53 feature names and order are exactly equal across E02 `height_plus_geometry`, E03 `height_plus_both`, and E04 `features`.

**Evidence-supported conclusion:** the E02/E03 combined vs E04 Ridge difference is a documented model-configuration difference (Ridge α=10 for waist/hip), not a recomputation, ID, feature-order, unit, or aggregation mismatch. The saved predictions and actuals are identical up to the model output; the α=1 targets match exactly. Because no retraining was permitted, this audit does not run a counterfactual α=1 E04 model; it establishes the configuration difference, not an isolated causal estimate.

---

## 5. Mismatch file

`P0_metric_mismatches.csv` contains:

- **1 recomputation summary row:** `NO_MISMATCH`, 140/140 MATCH.
- **10 cross-configuration TestB rows:** E02 vs E04 Ridge and E03 vs E04 Ridge for all five targets.
  - 6 rows are `IDENTICAL` (chest, shoulder, arm for both combined configurations).
  - 4 rows are `EXPLAINED_BY_ALPHA` (waist and hip for both combined configurations).

There are **no rows with recomputation status MISMATCH** and no unrepaired discrepancy.

---

## 6. Commands/scripts and evidence paths

Temporary read-only scripts (outside the project root):

```text
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_3_audit_dry.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_3_cross.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_3_write_csvs.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_3_validate_csvs.py
```

Primary evidence:

```text
experiments\predictions\E01_height_only_predictions.csv
experiments\predictions\E02_geometry_comparison_predictions.csv
experiments\predictions\E03_view_ablation_predictions.csv
experiments\predictions\E04_classical_ml_predictions.csv
experiments\metrics\E01_height_only_metrics.csv
experiments\metrics\E02_geometry_comparison_metrics.csv
experiments\metrics\E03_view_ablation_metrics.csv
experiments\metrics\E04_classical_ml_metrics.csv
experiments\metrics\E01_E04_consolidated_metrics.csv
experiments\E02_geometry\E02_experiment_config.json
experiments\E03_view_ablation\E03_view_ablation_config.json
experiments\E04_classical_ml\E04_experiment_config.json
experiments\E04_classical_ml\E04_cross_validation_results.csv
dataset\BodyM\processed\testA_manifest.csv
dataset\BodyM\processed\testB_manifest.csv
reports\E01_E04_consolidation_audit.json
notebooks\03_Dataset_Preprocessing.ipynb  (cells 44, 48, 51, 54, 57)
```

No source, prediction, metric, manifest, split, notebook, checkpoint, or backup file was modified.

---

## 7. Limitations

1. Recomputation validates the arithmetic from saved subject-level predictions; it cannot reconstruct photo-level predictions or re-verify the upstream subject aggregation because no photo-level prediction file exists.
2. The original metric files and consolidated table are internally consistent; this does not independently validate model training or model selection methodology.
3. E01/E02/E03 prediction files are wide and E04 is long; target/split/model mapping was explicit and checked, not assumed from column position.
4. The TestA–TestB shared subject ID remains in the official splits. It produces 487 total rows but 486 globally unique subjects; per-split counts remain 87/400.
5. No serialized library-version metadata was used to compare “model versions”; the comparison is based on the estimators and α values recorded in project configs/code and the E04 CV result file.
6. The E02/E03 vs E04 waist/hip explanation is configuration-level evidence. No retraining or counterfactual α=1 E04 run was performed.
7. Units are established by metric suffixes (`_cm`), E01 config `target_unit=cm`, dataset field documentation, and value ranges; no independent physical-unit measurement was performed.
