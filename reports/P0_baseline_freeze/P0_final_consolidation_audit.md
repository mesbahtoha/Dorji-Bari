# P0 Final Consolidation Audit — P0.1–P0.5 Recheck

**Date:** 2026-11-24  
**Working root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only  
**Scope:** final documentation and evidence recheck; no model training, no E01/E04 rerun, no E05-U retraining.

---

## 1. Deliverable reconciliation

### Core deliverables

| # | Deliverable | Status |
|---|---|---|
| 01 | `01_P0_artifact_inventory.csv` | Present in reproduction; copied from original with hash verification |
| 02 | `02_P0_dataset_integrity.md` | Present in reproduction; copied from original with hash verification |
| 03 | `03_P0_metric_recomputation.csv` | Present in reproduction; copied from original with hash verification |
| 04 | `04_P0_config_and_reproduction.md` | Present in reproduction |
| 05 | `05_P0_E05_uncertainty_audit.md` | Present in reproduction |
| 06 | `06_P0_Baseline_Freeze_Report.pdf/.docx` | **NOT YET CREATED** — intentionally deferred |

### Supporting files

All listed supporting files are present in the reproduction report directory:

```text
P0_metric_mismatches.csv
P0_clean_run_log.txt
P0_reproducibility_statement.md
P0_5_E05_artifact_inventory.csv
P0_5_OOF_provenance_audit.csv
P0_5_coverage_recomputation.csv
P0_5_uncertainty_model_comparison.csv
P0_5_risk_ranking_audit.csv
P0_5_independent_recomputation_log.txt
P0_1B_backup_inventory_summary.md
P0_3_metric_audit.md
P0_4A_reproduction_preflight.md
P0_4B1_isolation_setup.md
P0_4B2_environment_setup.md
P0_4C_E01_clean_reproduction.md
P0_4D_E04_clean_reproduction.md
P0_4D_E04_run_log.txt
```

`P0_final_deliverable_inventory.csv` records exact paths, sizes, timestamps, SHA-256, presence in original/backup/reproduction, and current/superseded status.

---

## 2. Safe documentation corrections made

1. Seven P0 documentation files were copied from the original project into the reproduction report directory after SHA-256 verification:
   01, 02, 03, `P0_metric_mismatches.csv`, `P0_1B_backup_inventory_summary.md`, `P0_3_metric_audit.md`, `P0_4A_reproduction_preflight.md`.
   The original files remain unchanged.
2. `P0_1B_backup_inventory_summary.md` now explicitly documents the three relocated preprocessed checkpoint manifests under `dataset\BodyM\processed\preprocessed_manifests\`. They are not missing.
3. A double-encoded ± symbol in the generated `P0_5_risk_ranking_audit.csv` note was corrected. No numerical values were changed.
4. No historical notebook, dataset, manifest, config, prediction, metric, checkpoint or E05-U artifact was changed.

No scientific numbers were altered. No final PDF/DOCX was created.

---

## 3. P0.1 recheck — backup and artifact snapshot

| Check | Result |
|---|---|
| Backup path | `D:\DorjiBari-P0-Backups\DorjiBari_20261124` |
| Backup files / bytes | 18,125 / 255,717,339 |
| Critical SHA-256 | 143 critical files; 0 mismatches |
| Inventory | 18,125 `PRESENT` rows + 3 `MISSING` rows |
| Missing expected E02 failure CSVs | 3 remain absent |
| Relocated checkpoint manifests | 3 present under `dataset\BodyM\processed\preprocessed_manifests\` |
| Same-drive limitation | documented |
| Stale `PROJECT_INVENTORY.md` claims | documented |

The later P0 reports in the original project were created after the backup. They are not historical missing files and are not treated as such.

**Status: PASS WITH LIMITATIONS.**

---

## 4. P0.2 recheck — dataset integrity

| Check | Result |
|---|---|
| Train | 6,133 pairs / 2,018 subjects |
| TestA | 1,684 pairs / 87 subjects |
| TestB official | 1,158 pairs / 400 subjects |
| Processed PNGs | 17,950; 0 missing; 0 unreferenced |
| Subject overlap | Train–TestA 0; Train–TestB 0; TestA–TestB **1** |
| Shared ID | `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`; identity unverified |
| Height input | `hwg_metadata.height_cm`; 8,975/8,975 rows match |
| Five targets | chest, waist, hip, shoulder-breadth, arm-length; 0 missing |
| Units | cm |
| QC exclusions | Train 1, TestA 0, TestB 2 |
| TestB clean manifest | **1,159 rows**, includes QC pair `578f12cd7dbbf39ccebc3116eaea41d6`; official manifests 1,158 |

The shared ID and the TestB clean-manifest discrepancy remain unresolved and unmodified. No official split was changed.

**Status: PASS WITH LIMITATIONS.**

---

## 5. P0.3 recheck — metric recomputation

- 140/140 consolidated metric rows are `MATCH`.
- Maximum absolute difference: **1.78e-15** (MAE/RMSE), **6.66e-16** (R²).
- E01: 20/20; E02: 30/30; E03: 60/60; E04: 30/30.
- `P0_metric_mismatches.csv` has no recomputation mismatch; its cross-configuration rows document the E02/E03 vs E04 difference.

### E02/E03 vs E04 TestB

| Target | E02/E03 (alpha=1) | E04 Ridge | Evidence |
|---|---:|---:|---|
| Waist | 4.3704144 | 4.2919805 | E04 CV selected alpha 10 for waist |
| Hip | 3.5435085 | 3.4933525 | E04 CV selected alpha 10 for hip |

E02/E03 use fixed Ridge alpha 1.0. E04 uses training-only 5-fold GroupKFold CV; selected alpha is 10 for waist/hip and 1 for chest/shoulder/arm. Features, subjects, actual values and subject-level aggregation were identical. The difference is a **model-configuration difference**, not a metric recomputation error. It is split-specific and does not establish general E04 superiority.

**Status: PASS.**

---

## 6. P0.4 recheck — E01/E04 clean reproduction

### E01

- 487/487 predictions exact; 20/20 metrics exact.
- Five artifacts byte-identical to backup.
- Cell 44 only; 0.795 s cell time; no errors.

### E04

- 7,305/7,305 predictions exact; 30/30 metrics exact; 15/15 CV rows exact.
- Five artifacts byte-identical to backup.
- Full cell 54 executed; Ridge, RandomForest and MLP all trained because no Ridge-only mode exists.
- Ridge alphas: chest 1, waist 10, hip 10, shoulder 1, arm 1.
- Seven MLP `ConvergenceWarning` messages observed; no error.
- E01 outputs remained unchanged after E04.

Environment: Python 3.14.6; NumPy 2.5.5; pandas 3.1.1; scikit-learn 1.9.1; joblib 1.6.0. `DORJIBARI_ROOT` resolved to the reproduction root; all inputs/outputs stayed inside it.

Exact historical Colab command, kernel, hardware and complete warning stream are not archived. Exact artifact equality does not prove identical Colab runtime behavior.

**Status: E01 PASS; E04 PASS WITH LIMITATIONS (full-cell execution and historical runtime).**

---

## 7. P0.5 recheck — E05-U uncertainty audit

- 21/21 expected historical E05 artifacts present; 41 E05 directory files plus reports/notebook inventoried.
- OOF: 10,090 rows, 2,018 subjects, 5 targets, 0 duplicate subject-target keys; no TestA/TestB IDs.
- Coverage: 30/30 recomputed exact; TestA mean 0.89885; TestB mean 0.81200; TestA 4/15 below nominal; **TestB 15/15 below nominal**.
- Uncertainty: median baseline 1.316222; ExtraTrees 1.310443; improvement **0.4391%**; hip +3.85%, waist +0.30%, chest/shoulder/arm worse.
- Risk (Train OOF only): hip 30.8592% capture / 1.5414 enrichment; waist 28.5120% / 1.4242; chest 25.0506% / 1.2513; arm 22.9572% / 1.1467; shoulder 22.8716% / 1.1424.
- Hip ±5 cm: Ridge 50.7519% capture, 2.5351 enrichment, 266 events; bootstrap CI 44.6804–56.9367% and 2.2673–2.8280, reproducible with 2,000 iterations, seed 42.

### OOF provenance limitations

- No inner-fold assignments or outer training membership saved.
- Config documents 4 inner folds; cell 76 uses 5.
- Uncertainty base uses fixed Ridge alpha 1.0; saved point OOF uses tuned alpha.
- Actual base errors differ in 4,438/10,090 rows; maximum difference **2.645083 cm**.
- No saved uncertainty model artifact.
- No TestA/TestB uncertainty or risk scores; test risk ranking is **NOT VERIFIABLE**.
- The nested 5×4 procedure is **not fully verified by artifacts**.

**Status: PASS WITH LIMITATIONS; OOF nested-5×4 provenance NOT VERIFIABLE.**

---

## 8. Unresolved scientific issues

1. Shared TestA–TestB source ID; identity unverified.
2. TestB `clean_manifest` 1,159 rows vs official 1,158; unmodified.
3. Four E05-U provenance issues: no inner assignments; 4-vs-5 inner folds; fixed-alpha vs tuned-alpha residuals; no saved uncertainty model.
4. TestB undercoverage at all 15 target × nominal combinations.
5. No TestA/TestB risk scores; risk results are Train OOF only.
6. Exact historical Colab command/runtime and complete warning stream unavailable.
7. E04 has no Ridge-only execution mode; RandomForest/MLP were also executed.
8. Three E02 feature-extraction failure CSVs remain absent.
9. Backup is on the same physical drive as the source.

These issues are documented, not silently repaired.

---

## 9. Status matrix

`P0_final_status_matrix.csv` contains 11 phase/core rows:

- P0.1 backup/inventory: PASS WITH LIMITATIONS
- P0.1 01 inventory: PASS WITH LIMITATIONS
- P0.2 dataset/02: PASS WITH LIMITATIONS
- P0.3 03: PASS
- P0.4 E01: PASS
- P0.4 E04: PASS WITH LIMITATIONS
- P0.4 04: PASS WITH LIMITATIONS
- P0.5 05: PASS WITH LIMITATIONS
- P0.5 OOF provenance: NOT VERIFIABLE
- P0.6 readiness input: PASS WITH LIMITATIONS
- P0.6 final report 06: NOT YET CREATED

---

## 10. Recommendation for P0.6

**CONDITIONAL GO** for preparing the P0.6 supervisor report.

Rationale: P0.1–P0.5 deliverables are present and the numerical coverage/metric/risk claims are reproducible; E01/E04 are exact. However, the E05-U 5×4 nested provenance is not verified, TestB intervals are undercovered, TestB clean-manifest and shared-ID issues remain, and test-set risk ranking is unavailable. The supervisor report must present these as limitations, not as fully validated claims.

No supervisor approval is claimed. No P0.6 PDF/DOCX has been created.
