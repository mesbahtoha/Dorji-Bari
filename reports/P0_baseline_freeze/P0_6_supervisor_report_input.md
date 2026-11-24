# P0.6 Supervisor Report Input — Verified Source Material

**Status:** Prepared for supervisor review; final PDF/DOCX not created.  
**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only

This document is source material for the supervisor report, not the final report. It distinguishes verified evidence, limitations, and unresolved issues.

---

## 1. Project Title and Research Objective

**DorjiBari Research — Body Measurement Estimation from Silhouette Imagery**

Objective: evaluate whether body measurements can be estimated from paired front/side body silhouettes and subject height, and assess uncertainty, calibration and selective-verification risk. The P0 work package focuses on baseline integrity, metric reproducibility, clean reproduction of E01/E04, and independent audit of the E05-U uncertainty/risk pipeline.

---

## 2. P0 Scope and Methodology

P0.1–P0.5 covered:

- verified backup and artifact inventory;
- dataset integrity and split/QC audit;
- independent recomputation of E01–E04 metrics;
- isolated E01/E04 clean reproduction;
- E05-U artifact, coverage, uncertainty, risk and provenance audit.

Working mode: read-only against the original project and backup; all reproduction and audit writes confined to the reproduction root. No retraining or recalibration. Historical artifacts were preserved.

---

## 3. Executive Summary

- E01 and E04 reproduce **exactly** in the isolated copy: all predictions, metrics, CV rows and artifact hashes match the backup.
- Metric recomputation is **140/140 MATCH**, maximum difference ~1.8e-15.
- Coverage recomputation is **30/30 exact**; TestA mean coverage **0.89885**; TestB mean **0.81200**.
- **All 15 TestB target × nominal-level combinations are below nominal.**
- Uncertainty baseline mean MAE **1.316222**; ExtraTrees **1.310443**; improvement **0.4391%**, concentrated in hip (+3.85%) and waist (+0.30%).
- Train-OOF Top-20% risk is strongest for hip and waist; hip ±5 cm Ridge capture **50.7519%**, enrichment **2.5351**.
- The E05-U saved artifacts do **not** prove the claimed 5×4 nested procedure: no inner-fold assignments; config says 4 inner folds while the uncertainty code uses 5; the uncertainty base uses fixed alpha 1.0 while the saved point OOF used tuned alpha; actual errors differ in 4,438/10,090 rows (maximum 2.645 cm).
- No saved uncertainty-model binary and no TestA/TestB uncertainty/risk scores are available.
- The shared TestA–TestB ID and the TestB clean-manifest discrepancy remain unresolved and unmodified.
- Recommendation: **CONDITIONAL GO** for the supervisor report, subject to explicit limitation disclosure.

---

## 4. Backup and Artifact Integrity Findings

- Backup: `D:\DorjiBari-P0-Backups\DorjiBari_20261124`.
- 18,125 files; 255,717,339 bytes; 143 critical SHA-256 checks; 0 mismatches.
- P0.1 inventory: 18,125 `PRESENT` rows + 3 `MISSING` expected E02 failure CSVs.
- The three expected E02 feature-extraction failure CSVs remain absent.
- The three preprocessed checkpoint manifests are relocated to `dataset\BodyM\processed\preprocessed_manifests\`; they are present, not missing.
- `PROJECT_INVENTORY.md` is stale and was not modified.
- **Backup is on the same physical D: drive as the source; it is not an independent external backup.**

Evidence: `P0_1B_backup_inventory_summary.md`, `P0_5_E05_artifact_inventory.csv`, `P0_final_deliverable_inventory.csv`.

---

## 5. Dataset Integrity Findings

| Split | Pairs | Subjects |
|---|---:|---:|
| Train | 6,133 | 2,018 |
| TestA | 1,684 | 87 |
| TestB | 1,158 | 400 |

- 17,950 processed PNGs; zero missing or unreferenced processed images.
- Train–TestA subject overlap 0; Train–TestB 0; TestA–TestB **1**.
- Shared source ID: `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`; identity is unverified. Official splits retained.
- Height input is `hwg_metadata.height_cm`; 8,975/8,975 rows match, while `measurements.height` matches zero rows.
- Targets: chest, waist, hip, shoulder-breadth, arm-length; no missing values.
- Units: centimetres.
- QC exclusions: Train 1, TestA 0, TestB 2.
- TestB `clean_manifest` contains 1,159 rows, including QC-excluded pair `578f12cd7dbbf39ccebc3116eaea41d6`; official TestB manifests contain 1,158. No correction was made.

Evidence: `02_P0_dataset_integrity.md`, `P0_5_coverage_recomputation.csv`.

---

## 6. Metric Recomputation Results

- Consolidated metric rows: **140**.
- E01 20/20, E02 30/30, E03 60/60, E04 30/30 — all **MATCH**.
- Maximum absolute differences: MAE/RMSE 1.78e-15; R² 6.66e-16.
- No unexplained metric mismatch.

Evidence: `03_P0_metric_recomputation.csv`, `P0_metric_mismatches.csv`, `P0_3_metric_audit.md`.

---

## 7. E01 and E04 Clean Reproduction Evidence

### E01

- 487/487 predictions exact; 20/20 metrics exact.
- Five artifacts byte-identical to backup: config, medians, predictions, metrics, checkpoint.
- Cell 44 only; 0.795 s cell time; no errors.

### E04

- 7,305/7,305 predictions exact; 30/30 metrics exact; 15/15 CV rows exact.
- Five artifacts byte-identical to backup.
- Full cell 54 executed: Ridge, RandomForest and MLP. No Ridge-only mode exists.
- Ridge alphas: chest 1, waist 10, hip 10, shoulder 1, arm 1.
- Seven MLP `ConvergenceWarning` messages; no error.
- E01 outputs unchanged after E04.

Evidence: `P0_4C_E01_clean_reproduction.md`, `P0_4D_E04_clean_reproduction.md`, `P0_clean_run_log.txt`.

---

## 8. E05-U Uncertainty and Risk Audit

- E05-U artifacts: 41 files in the E05 directory plus four reports; 21/21 historical expected artifacts present.
- OOF: 10,090 rows, 2,018 subjects, 5 targets; 0 duplicate subject-target keys; no TestA/TestB IDs.
- Coverage: 30/30 recomputed exact.
- Uncertainty MAE: median baseline 1.316222; ExtraTrees 1.310443; overall improvement 0.4391%.
- Target improvements: hip +3.85%, waist +0.30%; chest −0.34%, shoulder −3.15%, arm −3.36%.
- Risk (Train OOF only): hip 30.86% capture / 1.541 enrichment; waist 28.51% / 1.424; chest 25.05% / 1.251; arm 22.96% / 1.147; shoulder 22.87% / 1.142.
- Hip ±5 cm: Ridge 50.7519% capture, 2.5351 enrichment; bootstrap 95% CI 44.6804–56.9367% and 2.2673–2.8280; 2,000 iterations, seed 42. ExtraTrees 49.2481%/2.4600.

Evidence: `05_P0_E05_uncertainty_audit.md`, `P0_5_*` files, `P0_5_independent_recomputation_log.txt`.

---

## 9. Coverage Tables

Full precision and interval widths are in `P0_5_coverage_recomputation.csv`; the P0.5 report contains detailed tables. Coverage (gap in parentheses):

### TestA — 87 subjects

| Target | 80% | 90% | 95% |
|---|---:|---:|---:|
| chest | 0.7701 (−0.0299) | 0.8851 (−0.0149) | 0.9425 (−0.0075) |
| waist | 0.9080 (+0.1080) | 0.9540 (+0.0540) | 0.9655 (+0.0155) |
| hip | 0.8161 (+0.0161) | 0.9310 (+0.0310) | 0.9540 (+0.0040) |
| shoulder-breadth | 0.8161 (+0.0161) | 0.9080 (+0.0080) | 0.9885 (+0.0385) |
| arm-length | 0.7356 (−0.0644) | 0.9310 (+0.0310) | 0.9770 (+0.0270) |

Mean TestA coverage: **0.89885**; 4/15 below nominal.

### TestB — 400 subjects

| Target | 80% | 90% | 95% |
|---|---:|---:|---:|
| chest | 0.6925 (−0.1075) | 0.8150 (−0.0850) | 0.9125 (−0.0375) |
| waist | 0.7150 (−0.0850) | 0.8500 (−0.0500) | 0.9100 (−0.0400) |
| hip | 0.6800 (−0.1200) | 0.8000 (−0.1000) | 0.8675 (−0.0825) |
| shoulder-breadth | 0.6975 (−0.1025) | 0.8250 (−0.0750) | 0.9225 (−0.0275) |
| arm-length | 0.7300 (−0.0700) | 0.8525 (−0.0475) | 0.9100 (−0.0400) |

Mean TestB coverage: **0.81200**; **15/15 below nominal**.

---

## 10. OOF Provenance Findings

- 10,090 OOF rows; 2,018 Train subjects; five targets; zero duplicate subject-target keys; finite values.
- Actual values match the Train feature table exactly (max diff 0.0).
- No TestA/TestB IDs in Train OOF.
- Five outer folds; validation counts 404/404/404/403/403 per target.
- **No inner-fold assignments or outer training-set membership saved.**
- Config documents **4 inner folds**; the uncertainty cell uses **5**.
- Uncertainty base uses fixed `Ridge(alpha=1.0)`; saved point OOF used tuned alpha.
- Actual base errors differ in **4,438/10,090** rows; max difference **2.645083 cm**.
- No saved uncertainty model artifact.
- No TestA/TestB uncertainty or risk scores.
- Therefore the full nested 5×4 claim is **NOT VERIFIABLE**.

Evidence: `P0_5_OOF_provenance_audit.csv`, notebook cells 62/76.

---

## 11. E02/E03/E04 Configuration Discrepancy

| Target | E02/E03 | E04 Ridge |
|---|---:|---:|
| Waist | 4.3704144 | 4.2919805 |
| Hip | 3.5435085 | 3.4933525 |

- E02/E03 use fixed Ridge alpha 1.0.
- E04 uses training-only 5-fold GroupKFold CV.
- E04 selected alpha 10 for waist/hip and 1 for chest/shoulder/arm.
- Features, subject IDs, actual values and aggregation were otherwise consistent.
- The difference is a model-configuration difference, not a metric-recomputation error.
- TestA/TestB were not used for tuning; E04 gains are split-specific and do not establish general superiority.

Evidence: `04_P0_config_and_reproduction.md`, `E04_cross_validation_results.csv`, `P0_metric_mismatches.csv`.

---

## 12. Known Data Integrity Issues

1. Shared TestA–TestB source ID `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`; identity unverified.
2. `testB_clean_manifest.csv` has 1,159 rows vs official 1,158; contains QC pair `578f12cd7dbbf39ccebc3116eaea41d6`; unmodified.
3. Three expected E02 feature-extraction failure CSVs missing.
4. Three checkpoint manifests relocated to `dataset/BodyM/processed/preprocessed_manifests/`.
5. Backup is on the same physical drive as the source.

---

## 13. Known Methodological Inconsistencies

1. E05-U config 4 inner folds vs uncertainty code 5.
2. No inner-fold assignments or outer training membership saved.
3. Fixed-alpha uncertainty base vs tuned-alpha saved point OOF; 4,438/10,090 residual rows differ, max 2.645 cm.
4. No saved uncertainty model artifact.
5. No TestA/TestB uncertainty or risk scores; risk analysis is Train OOF only.
6. TestB intervals undercover at all 15 target × nominal combinations.
7. E04 has no Ridge-only mode; RandomForest/MLP also ran.
8. Exact historical Colab command/kernel/hardware and full warning stream unavailable.

---

## 14. Reproducibility Limitations

- Clean reproduction is in an isolated Windows/Python 3.14 copy, not proof of identical Colab runtime behavior.
- Direct E01/E04 packages match local original `.venv`; transitive package differences remain.
- E05-U nested provenance cannot be reconstructed from saved artifacts.
- Bootstrap CIs resample fixed cross-fitted predictions and do not capture model-training uncertainty.
- TestA has only 87 subjects.
- The shared TestA–TestB ID and TestB QC discrepancy remain.
- Risk ranking does not demonstrate that human review improves measurement accuracy.
- Tolerance thresholds are illustrative, not approved clinical/industry thresholds.

---

## 15. Unresolved Issues

- E05-U nested 5×4 implementation and inner-fold leakage cannot be verified.
- E05-U uncertainty model artifact and TestA/TestB risk scores are unavailable.
- TestB undercoverage remains at all nominal levels.
- TestB clean-manifest discrepancy remains.
- Shared ID identity remains unknown.
- No exact historical execution record for E05-U.
- P0.6 final PDF/DOCX is not created.

---

## 16. Completed Deliverables

Core:

```text
01_P0_artifact_inventory.csv
02_P0_dataset_integrity.md
03_P0_metric_recomputation.csv
04_P0_config_and_reproduction.md
05_P0_E05_uncertainty_audit.md
```

Supporting: `P0_metric_mismatches.csv`, `P0_clean_run_log.txt`, `P0_reproducibility_statement.md`, all `P0_5_*` evidence files, phase reports P0.1B–P0.5, `P0_final_deliverable_inventory.csv`, `P0_final_status_matrix.csv`, `P0_final_consolidation_audit.md`, `P0_final_integrity_verification.txt`.

The final `06_P0_Baseline_Freeze_Report.pdf/.docx` is **NOT YET CREATED**.

---

## 17. Recommended Next Actions

1. Prepare P0.6 report from this verified source material; do not add unverified claims.
2. Explicitly disclose E05-U nested-provenance limitations and TestB undercoverage.
3. Preserve the shared ID and TestB clean-manifest discrepancy as open data issues.
4. Do not recalibrate or tune on TestA/TestB.
5. If exact nested-provenance claims are required, plan a future audited rerun with saved fold assignments and uncertainty models; do not silently repair historical artifacts.
6. Keep final 06 PDF/DOCX separate from this input file.

---

## 18. G0 Supervisor Review and Sign-Off Request

Request: G0 review of P0.1–P0.5 evidence and approval/disposition for preparing P0.6. Specific decisions requested:

- accept E01/E04 exact reproduction evidence;
- accept the documented dataset/TestB limitations;
- accept E05-U numerical audit while acknowledging unverified 5×4 provenance;
- approve the **CONDITIONAL GO** path for P0.6 with limitations.

---

## 19. Approval Status

**Supervisor approval is still pending.** No approval is claimed, implied, or requested on the user’s behalf. P0.6 final report creation remains contingent on supervisor review.

**Recommendation: CONDITIONAL GO.**
