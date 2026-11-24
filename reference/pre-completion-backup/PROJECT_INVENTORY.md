# Project Inventory — DorjiBari-Research

Snapshot of what exists on disk, what was recovered from the notebooks, and
what still has to be regenerated. Updated 2026-11-19.

Status legend:

| Status | Meaning |
|---|---|
| PRESENT | Exists on disk and is part of the project |
| RECOVERED | Reconstructed exactly from a notebook source literal, a printed table, or an embedded image |
| REQUIRES ORIGINAL DATA | Produced by a pipeline stage; needs `dataset/BodyM` (public S3) and a re-run |
| EMPTY BY DESIGN | Directory intentionally empty |

No numeric result in this project was invented. Every recovered value is a
verbatim transcription of something the original Colab run printed or stored.

---

## 1. Files present on disk

| Path | Bytes | Status |
|---|---:|---|
| `README.md` | 8,816 | PRESENT (expanded) |
| `PROJECT_INVENTORY.md` | this file | PRESENT (new) |
| `requirements.txt` | 14,161 | PRESENT (Colab `pip freeze`; rewritten by notebook 01 on each run) |
| `reference/requirements-colab-original.txt` | 14,161 | PRESENT (archived original, never overwritten) |
| `requirements-local.txt` | 1,647 | PRESENT (new, Python 3.14 CPU stack) |
| `environment_report.txt` | 291 | PRESENT (Colab run; rewritten by notebook 01 on each run) |
| `reference/environment_report-colab-original.txt` | 291 | PRESENT (archived original, never overwritten) |
| `scripts/validate_project.py` | 15,225 | PRESENT (new, read-only validator) |
| `notebooks/01_environment_setup.ipynb` | 27,262 | PRESENT (repaired, 1 Markdown cell) |
| `notebooks/02_dataset_audit.ipynb` | 1,407,638 | PRESENT (repaired, 1 Markdown cell) |
| `notebooks/03_Dataset_Preprocessing.ipynb` | 1,161,714 | PRESENT (repaired, 9 Markdown cells) |
| `configs/preprocessing_config.json` | 1,124 | RECOVERED |
| `figures/*.png` (10 files) | see §2 | RECOVERED |
| `reports/E05_final_evidence_and_limitations.md` | 4,702 | RECOVERED |
| `reports/E05_final_artifact_inventory.csv` | 1,290 | RECOVERED |
| `reports/E05_final_consolidation_audit.json` | 779 | RECOVERED |

Directories that exist but are empty: `dataset/BodyM/`, `dataset/Local_Dataset/`,
`experiments/logs/`, `experiments/metrics/`, `experiments/predictions/`,
`checkpoints/`, `src/`.

---

## 2. Recovered artifacts and their provenance

| Artifact | Recovered from | Method |
|---|---|---|
| `figures/02_task2.10_mask_pair_verification.png` | notebook 02, TASK 2.10 cell output | base64 PNG decoded verbatim |
| `figures/02_task2.13d_outlier_subject_1..3.png` | notebook 02, TASK 2.13-D cell outputs | base64 PNG decoded verbatim |
| `figures/02_task2.13d_all_photo_pairs_1..2.png` | notebook 02, all-photo inspection cell outputs | base64 PNG decoded verbatim |
| `figures/02_task2.13e_alternative_pair_inspection.png` | notebook 02, alternative-pair cell output | base64 PNG decoded verbatim |
| `figures/03_split_overlap_mask_comparison.png` | notebook 03, TestA/TestB overlap cell output | base64 PNG decoded verbatim |
| `figures/03_side_mask_bottom_100_rows.png` | notebook 03, bottom-row diagnostic cell output | base64 PNG decoded verbatim |
| `figures/03_preprocessing_validation_preview.png` | notebook 03, preprocessing validation cell output | base64 PNG decoded verbatim |
| `configs/preprocessing_config.json` | notebook 03, Stage 2 configuration cell | Python dict literal evaluated; static, no data dependency |
| `reports/E05_final_evidence_and_limitations.md` | notebook 03, Stage 10 `report_lines` literal | literal evaluated; f-string counts (21 / 0 / 0) taken from the printed consolidation summary |
| `reports/E05_final_artifact_inventory.csv` | notebook 03, Stage 10 printed `[1] ARTIFACT INVENTORY` table | 21 rows transcribed exactly; `NaN` row/column counts written as empty cells |
| `reports/E05_final_consolidation_audit.json` | notebook 03, Stage 10 printed JSON | parsed verbatim, including the original `created_utc` |

The original filenames of the recovered figures were never set by the
notebooks (figures were only displayed inline), so the names above are new
and follow `notebook_task_description` ordering.

---

## 3. Artifacts that require the original data / a pipeline re-run

### 3.1 `dataset/BodyM/` (notebooks 02 and 03)

| Group | Items | Produced by |
|---|---|---|
| Structure audit | `dataset_structure.txt` | 02, TASK 2.1 |
| Object inventories | `audit/{train,testA,testB}_object_inventory.csv`, `audit/all_splits_object_inventory.csv` | 02, TASK 2.5 |
| Source metadata | `metadata/{split}_hwg_metadata.csv`, `{split}_measurements.csv`, `{split}_subject_to_photo_map.csv` | 02, TASK 2.3 / 2.7 / 2.8 |
| Photo-count audit | `metadata/{split}_photos_per_subject.csv` | 02, TASK 2.9 |
| Measurement / height audits | `metadata/measurement_values_audit.csv`, `metadata/height_discrepancy_audit.csv`, `metadata/research_field_mapping.md` | 02, TASK 2.12 |
| Target outliers | `metadata/outlier_summary.csv`, `metadata/outlier_candidates.csv`, `metadata/outlier_candidate_review.csv`, `metadata/subject_level_outlier_investigation.csv` | 02, TASK 2.13 |
| QC decisions | `metadata/problematic_image_audit.csv`, `metadata/problematic_image_audit_before_overlap_audit_update.csv`, `metadata/alternative_photo_pair_visual_review.csv`, `metadata/affected_subject_impact.csv` | 02, TASK 2.13 / 2.14; 03 Stage 1 |
| Manifests | `processed/{split}_clean_manifest.csv`, `processed/{split}_manifest.csv`, `processed/all_splits_manifest.csv` | 03, Stage 1 |
| Manifest backups | `processed/testB_manifest_before_qc_refresh.csv`, `processed/{split}_manifest_before_split_repair.csv` | 03, Stage 1 |
| Preprocessed manifests | `processed/preprocessed_manifests/{split}_preprocessed_manifest.csv`, `{split}_preprocessed_checkpoint.csv` | 03, Stage 3 |
| Silhouettes | `preprocessed_images/{train,testA,testB}/{front,side}/{photo_id}.png` — 17,950 files | 03, Stage 3 |

Notebook 02 only needs network access to the public bucket. Notebook 03
additionally downloads every `mask` / `mask_left` PNG.

### 3.2 `experiments/`, `checkpoints/`, `experiments/metrics|predictions|logs`

| Group | Items | Produced by |
|---|---|---|
| E01 | `E01_height_only/E01_config.json`, `E01_height_only/training_target_medians.csv` | 03, Stage 5 |
| E02 features | `E02_geometry/E02_feature_config.json`, `E02_experiment_config.json`, `E02_train_feature_statistics.csv`, `E02_test_train_range_comparison.csv`, `E02_feature_range_violations.csv`, `E02_prediction_integrity_audit.json` | 03, Stage 6 |
| E02 tables | `E02_geometry/all_photo_level_features.csv`, `all_subject_level_features.csv`, `photo_level_features/{split}_photo_features.csv` (3), `subject_level_features/{split}_subject_features.csv` (3), `{split}_feature_extraction_failures.csv` (3) | 03, Stage 6 |
| E03 | `E03_view_ablation/E03_view_ablation_config.json`, `E03_prediction_integrity_audit.json` | 03, Stage 7 |
| E04 | `E04_classical_ml/E04_experiment_config.json`, `E04_cross_validation_results.csv` | 03, Stage 8 |
| Metrics | `metrics/E01_height_only_metrics.csv`, `E02_geometry_comparison_metrics.csv`, `E03_view_ablation_metrics.csv`, `E04_classical_ml_metrics.csv`, `E01_E04_consolidated_metrics.csv` | 03, Stages 5-8 and consolidation |
| Predictions | `predictions/E01_height_only_predictions.csv`, `E02_geometry_comparison_predictions.csv`, `E03_view_ablation_predictions.csv`, `E04_classical_ml_predictions.csv` | 03, Stages 5-8 |
| Logs | `logs/preprocessing_summary.csv`, `preprocessing_failures.csv`, `full_preprocessing_integrity_audit.csv`, `{split}_preprocessed_checkpoint.csv` (3) | 03, Stage 3 |
| Checkpoints | `E01_height_only_ridge_models.joblib`, `E02_geometry_comparison_models.joblib`, `E03_view_ablation_models.joblib`, `E04_classical_ml_models.joblib` | 03, Stages 5-8 |

### 3.3 E05 — `experiments/E05_uncertainty_calibration/`

Verified at run time by the Stage 10 inventory (21 files, all `exists=True`):

`nested_cv_oof_predictions.csv`, `nested_cv_fold_results.csv`,
`oof_calibration_thresholds.csv`, `E05_test_prediction_intervals.csv`,
`E05_heldout_coverage_summary.csv`, `E05_residual_distribution_diagnostics.csv`,
`E05_photo_count_error_groups.csv`, `E05_photo_count_error_correlations.csv`,
`E05_verified_ridge_feature_error_dataset.csv`,
`E05_fully_nested_uncertainty_metrics.csv`,
`E05_fully_nested_uncertainty_predictions.csv`,
`E05_selective_verification_risk_analysis.csv`,
`E05_uncertainty_ranking_correlations.csv`,
`E05_top20_risk_bootstrap_confidence_intervals.csv`,
`E05_outer_fold_risk_stability_details.csv`,
`E05_outer_fold_risk_stability_summary.csv`,
`E05_fully_nested_prediction_integrity_audit.json`,
`E05_tolerance_out_of_tolerance_prevalence.csv`,
`E05_tolerance_selective_verification_results.csv`,
`E05_tolerance_top20_bootstrap_confidence_intervals.csv`,
`E04_classical_ml_metrics.csv` (read for comparison).

Additional E05 files written by earlier E05 steps (STEP 40.1-40.17):

`nested_cv_calibration_config.json`, `E05_calibration_quantile_comparison.csv`,
`E05_feature_distribution_shift.csv`, `E05_feature_distribution_shift_summary.csv`,
`E05_top_shifted_features.csv`, `E05_feature_error_associations.csv`,
`E05_shifted_feature_error_associations.csv`,
`E05_top_feature_error_associations.csv`,
`E05_feature_error_association_summary.csv`,
`E05_train_oof_feature_error_associations.csv`,
`E05_train_oof_focus_feature_associations.csv`,
`E05_train_oof_top_feature_associations.csv`,
`E05_train_oof_association_summary.csv`,
`E05_train_oof_vs_testb_association_comparison.csv`,
`E05_association_replication_summary.csv`,
`E05_top_replicated_associations.csv`,
`E05_feature_conditioned_uncertainty_oof_predictions.csv`,
`E05_feature_conditioned_uncertainty_cv_metrics.csv`,
`E05_nonlinear_uncertainty_comparison_metrics.csv`,
`E05_nonlinear_uncertainty_comparison_predictions.csv`,
`E05_fully_nested_prediction_metric_integrity.csv`.

### 3.4 `reports/` — remaining files (not recoverable)

| File | Produced by | Why not recovered |
|---|---|---|
| `subject_split_integrity_audit.md` | 03, Stage 1 | generated from live manifest tables |
| `split_summary.csv`, `subject_overlap_audit.csv`, `qc_exclusion_summary.csv` | 03, Stage 1 | generated from live manifests |
| `E04_CV_model_ranking.csv`, `E01_E04_descriptive_test_ranking.csv`, `E04_testA_testB_performance_gap.csv`, `E01_E04_consolidation_audit.json` | 03, consolidation of E01-E04 | generated from metric files |
| `E04_Ridge_subject_errors.csv`, `E04_Ridge_error_distribution.csv` | 03, STEP 39 | generated from predictions |
| `E05_tolerance_best_model_summary.csv` | 03, Stage 10 | only the 9 display columns were printed; the file has 15 |

---

## 4. Research evidence that exists only inside notebook 03

These were produced and verified during the original run. They are preserved
verbatim as saved outputs and must not be regenerated with different library
versions if the published numbers matter.

| Result | Where | Scale |
|---|---|---|
| Final dataset | Stage 1-3 | 6,133 train pairs / 2,018 subjects; 1,684 testA / 87; 1,158 testB / 400 |
| Preprocessed images | Stage 3 | 17,950 PNG, 0 missing, 0 invalid |
| E01 metrics | Stage 5 | 20 rows |
| E02 metrics | Stage 6 | 30 rows |
| E03 metrics | Stage 7 | 60 rows |
| E04 metrics + CV | Stage 8 | 30 metric rows, 15 CV rows |
| E01-E04 consolidated | Stage 9 boundary | 140 rows, all cross-stage equality checks PASS |
| E05 OOF predictions | Stage 9 | 10,090 rows (2,018 x 5 targets) |
| E05 held-out coverage | Stage 9 | 30 rows; TestB below nominal in 15/15 combinations |
| E05 fully nested metrics | Stage 9 | 15 rows, integrity audit `overall_pass: true` |
| E05 tolerance verification | Stage 9 | 120 result rows, 30 bootstrap rows, 15 prevalence rows |

Two cells (STEP 40.1 and STEP 40.6) still display their original
`AssertionError` output. That is deliberate: it is the record of the failure
that was repaired. Re-running those cells now completes successfully.

### 4.1 Preservation guarantees

- Notebook 01 cell 0 had been left showing a VS Code "requires the ipykernel
  package" error with an empty execution count, replacing the original Colab
  environment report. The original `stream` output and `execution_count = 1`
  were restored from the pre-repair copy.
- In notebook 03, four `stream` outputs carried a `metadata` member, which
  nbformat rejects. Only that key was removed; every `text` and every
  `display_data` payload is byte-identical to the original.
- All other code cells in all three notebooks keep their original outputs and
  execution counts, verified programmatically against the pre-repair copies.
- Because notebook 01 rewrites `requirements.txt` and `environment_report.txt`
  for the environment it runs in, the Colab originals were copied byte for byte
  to `reference/` before any execution test. The top-level files stay as the
  recorded Colab run; the archive cannot be overwritten by a notebook.

---

## 5. How to regenerate everything

```
1. Install the local environment:  pip install -r requirements-local.txt
   (or use Colab with the original environment)
2. Run notebooks/01_environment_setup.ipynb      -> folders, README, reports
3. Run notebooks/02_dataset_audit.ipynb          -> metadata + QC audits  (network)
4. Run notebooks/03_Dataset_Preprocessing.ipynb  -> manifests, images, E01-E05 (network, long)
```

Expected duration on the original Colab T4: notebook 02 minutes; notebook 03
several hours (17,950 image downloads plus nested cross-validation).

Verify a regenerated run against §4: the row counts above should match.

### Structural validation (runs in seconds, no data needed)

```
python scripts/validate_project.py
```

Exit code 0 means notebooks are valid and compile, paths resolve, directories
exist, recovered artifacts parse, the README template is in sync, and all
imports are covered by `requirements-local.txt`. Set
`DORJIBARI_NOTEBOOK_BACKUP` to a directory of pre-repair notebooks to also
prove output preservation.

---

## 6. Remaining blockers

1. **Original artifacts are not in this checkout.** They were produced in
   Colab Drive and only the notebooks were copied locally. Everything in §3
   must be regenerated; nothing is lost from the code side.
2. **Network access to `amazon-bodym`** is required for both notebooks 02 and 03.
3. **Python 3.14 vs Colab Python 3.13.** The local environment uses newer
   pandas/NumPy wheels. Re-running E01-E05 locally can change the last printed
   digits; use Colab with `requirements.txt` for exact parity.
4. **No GPU locally.** All E01-E05 models are scikit-learn, so CPU is enough;
   torch is used only for the dataset/dataloader validation.
5. **TestA/TestB are not fully subject-disjoint** (one shared subject in the
   official metadata). Documented, not fixable without changing official splits.
6. **`dataset/Local_Dataset/` is empty.** No local capture data exists, so the
   smartphone-image path of the research is not yet exercised.

---

## 7. Notebook code fixes applied (no methodology change)

| Notebook | Fix | Why it was needed |
|---|---|---|
| 01, 02, 03 | Portable `_dj_root()` bootstrap replaces hardcoded Colab paths | Notebooks must run from Colab or a local checkout; resolution now fails loudly instead of writing to an unrelated directory |
| 02 | `PROJECT_ROOT` is defined by the bootstrap | Cell 0 used `PROJECT_ROOT` while it was undefined |
| 01 | Torch sanity check only calls `torch.cuda.synchronize()` / `get_device_name` when CUDA exists | Crashed with `Torch not compiled with CUDA enabled` on CPU |
| 01 | `pip freeze` runs as `sys.executable -m pip freeze`, with explicit UTF-8 writes | Wrote the freeze of whichever `pip` was on PATH; not portable on Windows |
| 03 | STEP 40.1 excludes `split` and `photo_count` from the feature list before asserting the count | Assertion expected 53 features but counted the two metadata columns |
| 03 | STEP 40.6 lower-cases `photo_counts["split"]` before merging | Split labels were compared with different casing |
| 03 | Colab-only imports are guarded | `google.colab` is unavailable locally |
| 03 | Two `stream` outputs lost an illegal `metadata` key | nbformat rejects `metadata` on stream outputs |

All other code is unchanged. The original `AssertionError` outputs of
STEP 40.1 and STEP 40.6 remain in the notebook as the record of the failures
that were repaired.
