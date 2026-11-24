# P0.5 — E05-U Uncertainty and Risk Audit

**Date:** 2026-11-24  
**Working root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only  
**Scope:** independent audit of saved E05-U artifacts only. No E05 retraining, no E01/E04 rerun, no threshold recalibration.

---

## 1. Executive Summary

- E05-U artifacts are present and preserved. The E05 directory contains 41 files; four E05 reports and the pipeline notebook were also inventoried. The historical 21-file E05 inventory reports **21/21 present, 0 missing, 0 read errors**.
- **Coverage recomputation: exact.** All 30 official interval groups (TestA/TestB × five targets × 80/90/95%) reproduce the saved coverage and gap values with **0.0 absolute difference**. All 15 TestB target × nominal-level combinations are **below nominal**.
- **Uncertainty-model metric recomputation: exact.** The fully nested E05 metrics reproduce to ≤1.1e-16. Mean target MAE is **1.316222** for the median baseline and **1.310443** for ExtraTrees, a **0.4391%** improvement. The improvement is concentrated in hip (+3.85%) and waist (+0.30%); chest, shoulder and arm are worse.
- **Risk ranking: exact point values and bootstrap intervals.** On Train OOF (2,018 subjects), the highest-risk 20% (404 subjects) captures 30.86% of hip error (enrichment 1.541) and 28.51% of waist error (1.424), versus 25.05% chest, 22.96% arm, and 22.87% shoulder.
- **Hip ±5 cm:** Ridge Top-20% captures **50.7519%** of 266 out-of-tolerance events with enrichment **2.5351**; percentile bootstrap 95% CIs (2,000 iterations, seed 42) are **44.68–56.94%** and **2.267–2.828**. These are **Train OOF** results, not TestB.
- **Critical provenance limitation:** saved artifacts do **not** prove the claimed 5×4 nested process. No inner-fold assignments or training-fold membership are saved; the config documents 4 inner folds while the uncertainty cell uses **5**. The uncertainty base model also uses fixed `Ridge(alpha=1.0)`, whereas the saved point OOF used per-fold tuned alpha; actual residuals differ in **4,438 / 10,090** rows (max 2.645 cm).
- TestA/TestB risk ranking is **not verifiable**: no test uncertainty/risk scores are saved. No E05 uncertainty model artifact is saved.

---

## 2. Scope and Evidence Sources

Evidence used:

```text
experiments\E05_uncertainty_calibration\*            (41 files)
reports\E05_final_evidence_and_limitations.md
reports\E05_final_artifact_inventory.csv
reports\E05_final_consolidation_audit.json
reports\E05_tolerance_best_model_summary.csv
notebooks\03_Dataset_Preprocessing.ipynb             (cells 62–84)
experiments\E02_geometry\subject_level_features\*.csv
```

All E05 artifacts were copied to:

```text
reports\P0_baseline_freeze\pre_run_E05\
```

before analysis (45 files, 12,191,732 bytes). Original E05 files were not modified.

Environment: Python 3.14.6; NumPy 2.5.5; pandas 3.1.1; SciPy 1.18.1; scikit-learn 1.9.1; joblib 1.6.0.

No E05 pipeline, E01, E04, or other training was executed. The only operations were reads, hashes, aggregations, and deterministic bootstrap resampling from saved predictions.

---

## 3. E05-U Artifact Inventory

`P0_5_E05_artifact_inventory.csv` lists 46 present artifacts:

- 41 files in `experiments\E05_uncertainty_calibration\`
- 4 E05 reports
- notebook `03_Dataset_Preprocessing.ipynb`

All have SHA-256 hashes. Key artifacts:

| Artifact | Rows / structure | Size |
|---|---:|---:|
| `nested_cv_oof_predictions.csv` | 10,090 OOF rows | 1,286,424 B |
| `nested_cv_fold_results.csv` | 25 outer-fold/target rows | 1,686 B |
| `E05_fully_nested_uncertainty_predictions.csv` | 10,090 rows, 5 outer folds | 1,308,234 B |
| `E05_fully_nested_uncertainty_metrics.csv` | 15 target/model rows | 1,739 B |
| `E05_test_prediction_intervals.csv` | 7,305 rows (30 groups) | 1,344,567 B |
| `E05_heldout_coverage_summary.csv` | 30 rows | 3,632 B |
| `E05_selective_verification_risk_analysis.csv` | 40 rows | 6,556 B |
| `E05_tolerance_top20_bootstrap_confidence_intervals.csv` | 30 rows | 8,251 B |
| `E05_top20_risk_bootstrap_confidence_intervals.csv` | 10 rows | 2,250 B |

### Execution history

- E05 files are timestamped **2026-11-19 17:01–17:13** local.
- The generating code is notebook 03 cells **62–84** (nested OOF, intervals, uncertainty comparison, risk ranking, tolerance and bootstrap, consolidation).
- There is no standalone E05 script and no saved E05 model artifact (`*.joblib`, `*.pkl`, `*.pickle`) in the E05 directory.
- The exact historical E05 command, kernel, and hardware are not archived. The notebook contains code and outputs; these are evidence of the pipeline, not proof of exact runtime.

### Missing / inconsistent / unverifiable evidence

- No expected file from the historical 21-artifact inventory is missing.
- No saved uncertainty-model binary.
- No inner-fold assignments or outer training-fold membership at subject level.
- No TestA/TestB uncertainty scores or test risk-ranking predictions.
- The E05 config documents 4 inner folds; notebook cell 76 uses 5.
- The fully nested uncertainty base uses fixed `Ridge(alpha=1.0)`; the saved point OOF used tuned alpha.
- Alternate uncertainty tables exist (`E05_nonlinear_uncertainty_comparison_metrics.csv`, `E05_feature_conditioned_uncertainty_cv_metrics.csv`) with values that differ from the fully nested table. They are not the source of the 1.3104/1.3162 claim.

---

## 4. Nested GroupKFold and OOF Provenance

Expected design: 2,018 Train subjects × 5 targets × 5 outer folds, 4 inner folds, subject-level GroupKFold, 10,090 OOF rows.

| Check | Result | Evidence |
|---|---|---|
| OOF row count | **PASS** — 10,090 | `nested_cv_oof_predictions.csv` |
| Training subjects | **PASS** — 2,018 | same |
| Targets | **PASS** — 5 | same |
| Duplicate subject-target keys | **PASS** — 0 | same |
| Missing/non-finite OOF values | **PASS** — 0 | same |
| Every Train subject appears | **PASS** — 2,018 per target | same |
| Actual values match feature table | **PASS** — 0.0 max diff | E02 Train features |
| TestA/TestB IDs in OOF | **PASS** — 0 overlap | feature subject sets |
| Outer folds | **PASS** — 5; 404/404/404/403/403 validations per target | `E05_fully_nested_uncertainty_predictions.csv` |
| One outer fold per subject | **PASS** — max 1 | same |
| Inner-fold assignments saved | **NOT VERIFIABLE** — no inner-fold columns/artifact | E05 directory |
| Documented inner-fold count | **INCONSISTENT** — config says 4; cell 62 base uses 4; cell 76 uncertainty uses 5 | config vs notebook cells 62/76 |
| Outer-validation exclusion from outer training | **NOT VERIFIABLE** — no subject-level training membership saved | `nested_cv_fold_results.csv` only has counts |
| Inner GroupKFold/no subject leakage | **NOT VERIFIABLE** — no inner assignments | no artifact |
| Uncertainty inputs are the saved OOF residuals | **INCONSISTENT/PARTIAL** — actual base errors differ in 4,438/10,090 rows; max diff 2.645083 cm | `nested_cv_oof_predictions.csv` vs `E05_fully_nested_uncertainty_predictions.csv`; cell 76 `BASE_ALPHA=1.0` |
| No TestA/B labels/errors used | **PARTIAL** — OOF IDs are Train-only and config says false; no execution log | OOF IDs/config |
| Artifacts prove nested 5×4 | **NOT VERIFIABLE** | no fold membership; 5×5 uncertainty implementation |
| Uncertainty model artifact saved | **NOT FOUND** | no joblib/pickle in E05 directory |

### Why the uncertainty residuals differ

Notebook cell 76:

- uses fixed `BASE_ALPHA = 1.0` for the base Ridge model;
- uses `GroupKFold(n_splits=5)` for the inner residual generation;
- regenerates residuals inside each outer training fold rather than reusing `nested_cv_oof_predictions.csv`;
- explicitly states that the saved OOF data are used only to verify subject/target coverage.

By contrast, notebook cell 62 created `nested_cv_oof_predictions.csv` using `GridSearchCV` with per-fold alpha selection and `GroupKFold(n_splits=4)`.

Therefore the saved point OOF and the uncertainty evaluation are two related but **not identical** nested procedures. The uncertainty metrics are internally reproducible from the saved uncertainty predictions, but the 5×4 provenance claim is **not established by artifacts**.

---

## 5. Uncertainty Model and Baseline Comparison

`P0_5_uncertainty_model_comparison.csv` recomputes all 15 target/model rows from `E05_fully_nested_uncertainty_predictions.csv`.

- Evaluation rows: 2,018 Train OOF subjects per target.
- Target actual value: `actual_base_absolute_error`.
- Quality metric: MAE between estimated absolute error and actual absolute error; R² and correlation also reported.
- Baseline: per-outer-fold median of inner OOF absolute errors (`median_baseline_estimate`).
- ExtraTrees: 200 trees, `min_samples_leaf=10`, `max_features=0.7`, `random_state=42`, `n_jobs=2`.
- Ridge uncertainty: `StandardScaler + Ridge(alpha=10.0)`.

| Target | Median baseline MAE | Ridge uncertainty MAE | ExtraTrees MAE | ExtraTrees vs baseline |
|---|---:|---:|---:|---:|
| chest | 1.758611 | 1.808919 | 1.764677 | **−0.3449%** |
| waist | 2.150722 | 2.170137 | 2.144338 | **+0.2968%** |
| hip | 1.624903 | 1.614833 | 1.562322 | **+3.8514%** |
| shoulder-breadth | 0.545657 | 0.568761 | 0.562840 | **−3.1490%** |
| arm-length | 0.501219 | 0.517794 | 0.518039 | **−3.3559%** |
| **Unweighted mean** | **1.316222** | **1.336089** | **1.310443** | **+0.4391%** |

Recomputation vs historical:

- MAE: max absolute difference **1.11e-16**
- R²: max absolute difference **1.11e-16**
- Correlation: max absolute difference **5.55e-17**

The previously observed **1.3104 / 1.3162 / 0.44%** figures are verified for this fully nested table. The improvement is **small and concentrated**: only hip (3.85%) and waist (0.30%) improve; chest, shoulder and arm worsen. A 0.44% MAE reduction does not establish reliable uncertainty calibration or deployment readiness. The alternate `E05_nonlinear` table yields means of 1.317953 (baseline) and 1.315061 (ExtraTrees), so it is a different comparison, not the fully nested claim.

---

## 6. TestA Coverage Results

TestA: 87 subjects. Historical and independent values match exactly (all 30 groups; see `P0_5_coverage_recomputation.csv`). TestA mean observed coverage is **0.89885**; 4/15 combinations are below nominal.

| Nominal | Target | Empirical coverage | Gap | Mean width (cm) | Outside |
|---:|---|---:|---:|---:|---:|
| 80% | arm-length | 0.735632 | −0.064368 | 2.631552 | 23 |
| 80% | chest | 0.770115 | −0.029885 | 8.939034 | 20 |
| 80% | hip | 0.816092 | +0.016092 | 8.201262 | 16 |
| 80% | shoulder-breadth | 0.816092 | +0.016092 | 2.825025 | 16 |
| 80% | waist | 0.908046 | +0.108046 | 10.931806 | 8 |
| 90% | arm-length | 0.931034 | +0.031034 | 3.564905 | 6 |
| 90% | chest | 0.885057 | −0.014943 | 11.812462 | 10 |
| 90% | hip | 0.931034 | +0.031034 | 11.110846 | 6 |
| 90% | shoulder-breadth | 0.908046 | +0.008046 | 3.819605 | 8 |
| 90% | waist | 0.954023 | +0.054023 | 14.576907 | 4 |
| 95% | arm-length | 0.977011 | +0.027011 | 4.225049 | 2 |
| 95% | chest | 0.942529 | −0.007471 | 15.189279 | 5 |
| 95% | hip | 0.954023 | +0.004023 | 13.722850 | 4 |
| 95% | shoulder-breadth | 0.988506 | +0.038506 | 4.637998 | 1 |
| 95% | waist | 0.965517 | +0.015517 | 18.056278 | 3 |

TestA mean absolute coverage gap: **0.031073**.

---

## 7. TestB Coverage Results

TestB: 400 subjects. All **15/15** combinations are below nominal. TestB mean observed coverage is **0.81200**; mean absolute gap is **0.071333**.

| Nominal | Target | Empirical coverage | Gap | Mean width (cm) | Outside |
|---:|---|---:|---:|---:|---:|
| 80% | arm-length | 0.730000 | −0.070000 | 2.631552 | 108 |
| 80% | chest | 0.692500 | −0.107500 | 8.939034 | 123 |
| 80% | hip | 0.680000 | −0.120000 | 8.201262 | 128 |
| 80% | shoulder-breadth | 0.697500 | −0.102500 | 2.825025 | 121 |
| 80% | waist | 0.715000 | −0.085000 | 10.931806 | 114 |
| 90% | arm-length | 0.852500 | −0.047500 | 3.564905 | 59 |
| 90% | chest | 0.815000 | −0.085000 | 11.812462 | 74 |
| 90% | hip | 0.800000 | −0.100000 | 11.110846 | 80 |
| 90% | shoulder-breadth | 0.825000 | −0.075000 | 3.819605 | 70 |
| 90% | waist | 0.850000 | −0.050000 | 14.576907 | 60 |
| 95% | arm-length | 0.910000 | −0.040000 | 4.225049 | 36 |
| 95% | chest | 0.912500 | −0.037500 | 15.189279 | 35 |
| 95% | hip | 0.867500 | −0.082500 | 13.722850 | 53 |
| 95% | shoulder-breadth | 0.922500 | −0.027500 | 4.637998 | 31 |
| 95% | waist | 0.910000 | −0.040000 | 18.056278 | 36 |

The largest TestB 80% gaps are hip (−0.1200), chest (−0.1075), and shoulder (−0.1025). TestB undercoverage persists at all three nominal levels.

---

## 8. Mean Interval Width Analysis

All intervals are finite and have `lower <= upper`; zero invalid intervals. Within each target × nominal level, mean, median, minimum and maximum widths are equal to floating precision; the interval is symmetric `predicted ± threshold`.

| Target | 80% width (cm) | 90% width (cm) | 95% width (cm) |
|---|---:|---:|---:|
| chest | 8.939033974 | 11.812462370 | 15.189278579 |
| waist | 10.931805651 | 14.576906814 | 18.056278260 |
| hip | 8.201261951 | 11.110845996 | 13.722850273 |
| shoulder-breadth | 2.825025001 | 3.819605150 | 4.637997823 |
| arm-length | 2.631551571 | 3.564904595 | 4.225048766 |

Widths are identical in TestA and TestB because the thresholds are fixed from Train OOF. Larger widths naturally produce higher coverage for hip/waist/chest; direct width comparisons across targets are not meaningful because target scales differ. Historical mean-width values match recomputation within **7.1e-15 cm** (floating serialization).

---

## 9. Risk Ranking and Top-20% Audit

The saved risk artifacts operate on **Train OOF predictions only** (`n=2,018` per target; 404 flagged at 20%; expected capture 20.0198%). There are **no saved TestA/TestB uncertainty scores or test risk scores**, so evaluation-split risk ranking is **NOT VERIFIABLE**.

| Target | Model | Top-20% error capture | Enrichment | Flagged mean error (cm) | Remaining MAE (cm) |
|---|---|---:|---:|---:|---:|
| chest | Ridge | 25.0506% | 1.2513 | 3.5364 | 2.6485 |
| chest | ExtraTrees | 26.4263% | 1.3200 | 3.7307 | 2.5999 |
| waist | Ridge | 28.5120% | 1.4242 | 5.0052 | 3.1413 |
| waist | ExtraTrees | 27.5755% | 1.3774 | 4.8408 | 3.1824 |
| hip | Ridge | 30.8592% | 1.5414 | 4.0497 | 2.2712 |
| hip | ExtraTrees | 30.6157% | 1.5293 | 4.0177 | 2.2792 |
| shoulder-breadth | Ridge | 22.8716% | 1.1424 | 1.0181 | 0.8594 |
| shoulder-breadth | ExtraTrees | 22.4114% | 1.1195 | 0.9976 | 0.8645 |
| arm-length | Ridge | 22.9572% | 1.1467 | 0.9544 | 0.8018 |
| arm-length | ExtraTrees | 22.2790% | 1.1128 | 0.9262 | 0.8088 |

All point estimates match `E05_selective_verification_risk_analysis.csv` exactly (delta 0.0). Hip and waist show the strongest enrichment; chest is intermediate; shoulder and arm are weakest. This supports a **relative ranking signal**, not a deployment-level guarantee.

---

## 10. Hip ±5 cm Tolerance Analysis

- Train OOF subjects: 2,018.
- Out-of-tolerance events: **266** (error > 5 cm).
- Top-20% flagged: 404.
- Ridge captured **135** events: **50.7519%** capture; enrichment **2.5351**.
- Ridge bootstrap 95% CI, percentile method, 2,000 iterations, seed **42**: capture **44.6804–56.9367%**, enrichment **2.2673–2.8280**.
- ExtraTrees captured 131 events: **49.2481%**; enrichment **2.4600**; CI capture **43.5126–55.2636%**, enrichment **2.2052–2.7535**.

The previously reported 50.75%/2.54 values are verified, but they describe **Train OOF**, not TestB. The ±5 cm threshold is illustrative and is not a clinical, regulatory, or industry-approved tolerance.

---

## 11. Calibration Drift and Known Failures

1. **TestA vs TestB coverage:** TestA mean coverage 0.89885, mean absolute gap 0.031073; TestB mean coverage 0.81200, mean absolute gap 0.071333. TestA is closer to nominal.
2. **Undercoverage:** All 15 TestB target × nominal combinations are below nominal; TestA has 4/15 below.
3. **Target-specific weaknesses:** TestB is worst for hip, chest and shoulder at 80%; hip remains substantially below nominal at 95% (0.8675 vs 0.95).
4. **All 15 TestB below nominal:** **verified independently**.
5. **Hip/waist vs shoulder/arm:** risk enrichment is strongest for hip/waist and weakest for shoulder/arm; uncertainty MAE improvement is also concentrated in hip/waist.
6. **Calibration drift / distribution sensitivity:** TestB undercoverage and feature-shift diagnostics are consistent with a Train-to-TestB distribution/calibration shift. The evidence does **not** establish the cause or guarantee that recalibration would fix it.
7. **Deployment-level uncertainty:** Not supported. The artifacts show empirical undercoverage on TestB and no external validation.

### Known provenance failures

- Full 5×4 nested design is **not demonstrated by artifacts**; no inner-fold assignments or outer training membership are saved.
- The config says 4 inner folds; the uncertainty cell uses 5.
- The uncertainty base uses fixed alpha 1.0; the saved point OOF uses tuned alpha. Actual errors differ in 4,438/10,090 rows (max 2.645 cm).
- No saved uncertainty model artifact.
- No TestA/TestB uncertainty/risk predictions.
- The TestB clean-manifest discrepancy and shared TestA–TestB source ID remain as documented in P0.2; no correction or split change was made.

---

## 12. Statistical and Methodological Limitations

- **OOF training vs evaluation:** The base model and uncertainty model are trained on 1,614/1,615 outer-training subjects, while final deployment models would use more data; residual distributions may differ.
- **Inner vs outer size mismatch:** Inner OOF base errors come from smaller training folds than outer base predictions; this can bias the uncertainty estimate.
- **Fixed cross-fitted predictions:** Bootstrap intervals resample fixed predictions; they do not capture model-training, hyperparameter, or data-collection uncertainty.
- **No saved model:** The uncertainty model cannot be reloaded or independently inspected; only saved predictions and metrics are available.
- **TestA sample size:** 87 subjects; 80/90/95 coverage has wide binomial uncertainty (e.g., one subject changes coverage by about 1.15 percentage points).
- **Shared source ID:** The TestA–TestB shared source ID remains; identity is unverified. Official splits were not changed.
- **TestB QC discrepancy:** The `testB_clean_manifest.csv` extra QC-excluded row remains documented in P0.2 and was not silently corrected.
- **TestB undercoverage:** Intervals are Train-OOF-calibrated and undercover on TestB; no TestB recalibration was performed.
- **Feature-error associations:** Exploratory correlations; not causal evidence.
- **Risk ranking:** Does not demonstrate that human review improves measurement accuracy or garment fit.
- **Tolerance thresholds:** Illustrative only; no approved operational standard.
- **Historical execution:** Exact E05 CLI command, kernel, hardware and full warning stream are not archived.

---

## 13. Verified Findings

1. All 30 coverage rows recompute exactly from saved interval bounds; maximum coverage/gap difference 0.0; mean-width difference ≤7.1e-15 cm.
2. All 15 TestB target × nominal-level combinations are below nominal coverage.
3. TestA is closer to nominal than TestB (mean absolute gap 0.031073 vs 0.071333).
4. All 15 fully nested uncertainty metric rows recompute to ≤1.11e-16 MAE/R² difference.
5. Overall mean target MAE: median baseline **1.316222**, ExtraTrees **1.310443**, improvement **0.4391%**.
6. ExtraTrees improves hip (+3.8514%) and waist (+0.2968%); chest, shoulder and arm are worse.
7. Train OOF Top-20% risk point estimates match exactly; hip/waist have the strongest enrichment.
8. Hip ±5 cm Ridge: 50.7519% capture, 2.5351 enrichment, 266 events; bootstrap CIs reproduce exactly with seed 42 and 2,000 iterations.
9. E05 artifact hashes are preserved; no E05 file was modified.
10. E01/E04 artifacts remain byte-identical to the verified backup.
11. No TestA/TestB subject IDs appear in the Train OOF file.

---

## 14. Not Verifiable Claims

- The exact **5 outer × 4 inner** nested procedure from saved artifacts alone.
- Subject-level inner-fold membership, no inner leakage, and outer training/validation exclusion.
- That the uncertainty model consumed exactly the saved `nested_cv_oof_predictions.csv` residuals (it did not; fixed-alpha/5-inner residuals differ).
- TestA/TestB risk ranking (no test uncertainty scores saved).
- The exact historical E05 execution command/runtime and the complete original warning stream.
- Any claim that the uncertainty model is deployment-calibrated, that TestB coverage is nominal, or that human verification improves real-world accuracy.
- Any claim that ±5 cm is an approved clinical/industry tolerance.

---

## 15. Recommendations

1. Preserve the E05 artifact set and this audit; do not overwrite or retrain.
2. In future work, save inner-fold assignments, outer training membership, and uncertainty model binaries.
3. Reconcile the documented 4-inner-fold configuration with the 5-inner-fold uncertainty implementation before claiming a 5×4 nested design.
4. Pre-specify one base-residual procedure (fixed alpha vs tuned alpha) and use it consistently for OOF, uncertainty, and coverage.
5. Treat TestB undercoverage as evidence of calibration/distribution sensitivity; do not recalibrate on TestB if retaining it as held-out evaluation.
6. Validate intervals on an external population or a prospective split with adequate sample size.
7. Report TestA uncertainty intervals as exploratory because n=87.
8. Keep the shared TestA–TestB ID and QC discrepancy visible in all downstream reports.
9. Report tolerance thresholds as illustrative and operationally unvalidated.
10. Do not run P0.6 or E05 retraining as part of this audit.

---

## 16. P0.5 Final Status

- Original project: 18,132 non-venv files; unchanged.
- Verified backup: 18,125 files; unchanged.
- Official manifests, feature tables, splits and shared ID: unchanged; TestB clean-manifest discrepancy still documented, not corrected.
- E01 and E04 artifacts: unchanged and byte-identical to backup.
- E05 artifacts: preserved in `pre_run_E05`; original E05 files unchanged.
- All generated P0.5 files are inside the reproduction root.
- No supervisor approval is claimed. No P0.6 or E05 retraining was started.

**P0.5 COMPLETE WITH DOCUMENTED LIMITATIONS**
