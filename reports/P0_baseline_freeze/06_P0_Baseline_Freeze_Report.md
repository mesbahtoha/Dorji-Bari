# DORJIBARI — P0 Baseline Freeze Report

**Evidence Reproduction, Consistency Audit & Baseline Freeze**

> **Corrected report source.** The final PDF/DOCX has not been created or registered. This Markdown file is the corrected source for rendering that final artifact.

| Report information | Details |
|---|---|
| Project | DorjiBari Research |
| Reporting stage | P0.1–P0.5 recheck complete; P0.6 supervisor review package |
| Report date | 24 November 2026 |
| Working reproduction copy | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124` |
| Status | CONDITIONAL GO — source material ready for supervisor review; approval pending |
| Intended audience | Project Supervisor / Research Review |

Prepared from the P0 audit results and targeted-limitation findings.

---

## 1. Executive Summary

The P0 evidence-reproduction and baseline-freeze work has completed its P0.1–P0.5 recheck. The work covered preservation of the historical project, dataset and split integrity, independent metric recalculation, clean reproduction of E01 and E04 in an isolated copy, and an audit of the historical E05 uncertainty results.

Independent metric recalculation and E01/E04 reproduction provide strong evidence of consistency for the audited outputs. However, E05-U nested cross-validation provenance is incomplete, no saved E05 uncertainty-model artifact or TestA/TestB risk scores were found, and TestB coverage is below nominal across all 15 audited target-by-level combinations.

Overall recommendation: **CONDITIONAL GO** for P0.6 supervisor review, with limitations disclosed. Supervisor approval remains pending. This report does not declare G0 approved or authorize a new research phase.

---

## 2. Scope, Rules and Non-Goals

P0 was treated as an audit and reproducibility sprint, not a new model-development phase. Official BodyM Train/TestA/TestB assignments were preserved, including the shared TestA–TestB source ID. Historical E05 is referred to as E05-U in new reporting; the historical folder and artifacts were not renamed or overwritten.

- No new CNN, Transformer, or uncertainty-model training was performed during this audit.
- TestA and TestB were not used for model selection, hyperparameter tuning, threshold selection, or recalibration.
- No historical notebook, dataset, manifest, prediction, metric, checkpoint, or E05 artifact was modified.
- Reproduction was performed in an isolated copy; the original project and verified backup remained read-only.
- Missing evidence was not fabricated; unverifiable runtime details and incomplete provenance are disclosed.

---

## 3. P0 Status at a Glance

| Work package | Result | Evidence summary |
|---|---|---|
| P0.1 Backup / inventory | PASS WITH LIMITATIONS | 18,125 files; 255,717,339 bytes; 143 critical hashes; zero reported mismatches; three expected E02 failure CSVs missing. |
| P0.2 Dataset integrity | PASS WITH LIMITATIONS | Official split counts, subject counts, processed images, overlap, height mapping, targets, units and QC reviewed. |
| P0.3 Metric recalculation | PASS | 140/140 MATCH; maximum absolute difference 1.78e-15. |
| P0.4 E01 | PASS | 487/487 predictions; 20/20 metrics; five artifacts SHA-identical. |
| P0.4 E04 | PASS WITH LIMITATIONS | 7,305/7,305 predictions; 30/30 metrics; 15/15 CV rows; full cell also ran RF and MLP. |
| P0.5 E05-U | PASS WITH LIMITATIONS | 30/30 coverage calculations exact; nested-CV provenance and uncertainty artifacts incomplete. |
| P0.6 | READY WITH LIMITATIONS | P0.6 source material ready with limitations; final PDF/DOCX not created; signoff pending. |

---

## 4. P0.1 — Backup and Artifact Inventory

The verified backup contains 18,125 files totaling 255,717,339 bytes. The reported comparison found zero missing, extra, size-mismatched, or hash-mismatched files, and all 143 critical CSV/JSON/JOBLIB/IPYNB hashes matched. The inventory records 18,125 PRESENT entries and three MISSING E02 feature-extraction failure CSVs.

- The missing files are the E02 train, testA and testB feature-extraction failure CSVs.
- Three checkpoint manifests were located under `dataset\BodyM\processed\preprocessed_manifests\` rather than the expected `experiments\logs\` path; relocation is documented.
- `PROJECT_INVENTORY.md` was stale relative to actual files and was not silently rewritten.
- The backup is on the same physical D: drive as the source project; this is a resilience limitation.

---

## 5. P0.2 — Dataset and Split Integrity

| Split | Pairs | Subjects |
|---|---:|---:|
| Train | 6,133 | 2,018 |
| TestA | 1,684 | 87 |
| TestB | 1,158 | 400 |

A total of 17,950 processed PNG images were reported, with no missing or unreferenced images. Subject overlap was zero for Train–TestA and Train–TestB, while one shared source ID remained between TestA and TestB. The identity represented by that ID has not been independently verified.

- Shared source ID: `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`; associated with 22 TestA pairs and six official TestB pairs.
- Conflicting height values are reported (TestA 163.2 cm; TestB 168.0 cm); identity remains unverified and official split assignments were preserved.
- `testB_clean_manifest.csv` has 1,159 rows while official TestB manifests have 1,158. The additional row is QC-excluded pair `578f12cd7dbbf39ccebc3116eaea41d6`.
- Height mapping, five target measurements, units and QC exclusions were checked. `hwg_metadata.height_cm` matched for 8,975/8,975 records; `measurements.height` did not match that mapping.

---

## 6. P0.3 — Independent Metric Recalculation

The independent recalculation compared 140 metric rows across E01–E04. All 140 matched. Maximum absolute differences were 1.78e-15 cm for MAE/RMSE and 6.66e-16 for R². No MAE or RMSE difference exceeded the 0.0001 cm investigation threshold.

E02/E03 predictions were identical. E04 differed for waist and hip because E02/E03 used fixed Ridge alpha=1, while E04’s training-only five-fold GroupKFold selection chose alpha=10 for waist and hip (alpha=1 for the other targets). This is a configuration difference, not a metric mismatch.

| TestB target | E02/E03 MAE (cm) | E04 MAE (cm) | E04 alpha |
|---|---:|---:|---:|
| Chest | 3.5484469 | 3.5484469 | 1 |
| Waist | 4.3704144 | 4.2919805 | 10 |
| Hip | 3.5435085 | 3.4933525 | 10 |
| Shoulder breadth | 1.0554480 | 1.0554480 | 1 |
| Arm length | 1.0102939 | 1.0102939 | 1 |

---

## 7. P0.4 — Clean Reproduction

### 7.1 E01

The designated E01 baseline/model cell (cell 44) completed successfully in the isolated reproduction copy. All 487/487 predictions and 20/20 metrics matched; five regenerated artifacts were SHA-identical to preserved historical versions.

### 7.2 E04

The designated E04 cell (cell 54) completed successfully. All 7,305/7,305 predictions, 30/30 metrics and 15/15 CV rows matched; five artifacts were SHA-identical. The cell has no Ridge-only mode, so Ridge, RandomForest and MLP all ran. Seven MLP `ConvergenceWarning` occurrences were reported; no execution errors were reported.

The local reproduction environment used Python 3.14.6. Archived Colab metadata provides some historical environment information (Python 3.13.16, T4, CUDA 13.0 and package versions), but the exact historical command, kernel, runtime state and complete warning stream remain unavailable. Artifact equality does not establish identical local and Colab runtimes.

---

## 8. P0.5 — E05-U Uncertainty Audit

The audit inventoried 41 historical E05 files and reported all 21 expected historical artifacts present. Independent coverage recomputation matched 30/30 comparisons; coverage and gap differences were zero, and width differences were at most 7.1e-15 cm.

| Measure | TestA | TestB |
|---|---:|---:|
| Mean empirical coverage | 0.89885 | 0.81200 |
| Mean absolute coverage gap | 0.031073 | 0.071333 |
| Below-nominal combinations | 4/15 | 15/15 |

The uncertainty-model comparison reported mean MAE 1.316222 for the baseline and 1.310443 for ExtraTrees, an improvement of 0.4391%. Target-level results were mixed: hip improved 3.85% and waist 0.30%, while chest, shoulder and arm results were worse. This is not evidence of uniformly better uncertainty performance.

Risk ranking was based on Train OOF only (n=2,018 subjects). The reported hip ±5 cm Ridge capture was 50.7519%, with enrichment 2.5351; bootstrap confidence intervals were reproduced using 2,000 percentile-bootstrap iterations and seed 42. This is not TestA/TestB risk validation.

---

## 9. Remaining Scientific and Reproducibility Limitations

| Issue | Verified finding | Required treatment |
|---|---|---|
| Nested CV provenance | Outer 5-fold supported by config, code and 25 fold rows; inner 4 appears in config/cell 62, while uncertainty cell uses 5. No inner assignments or outer training membership saved. | Disclose; do not claim verified nested 5×4 execution. |
| Alpha / residual mismatch | 4,438/10,090 residual rows differ; maximum difference 2.645083 cm. Saved point OOF uses tuned alpha; uncertainty calculation uses fixed alpha=1.0. | Documentation correction only; explain distinct configurations; preserve both sources. |
| Uncertainty model artifact | No saved E05 uncertainty-model artifact; only E01–E04 checkpoints exist. | Disclose; do not claim artifact-level uncertainty-model reproducibility. |
| TestA/TestB risk scores | No TestA/TestB uncertainty or risk scores found; ranking is Train OOF only. | Disclose; do not imply external-split risk performance. |
| TestB coverage | All 15/15 target × nominal-level combinations below nominal; mean coverage 0.81200. | Disclose undercoverage; no recalibration performed. |
| Shared source ID | One source ID appears in TestA and TestB; identity unverified and height values conflict. | Preserve official splits; disclose unresolved identity. |
| TestB manifest | Clean manifest 1,159 rows; official manifest 1,158. One QC-excluded pair accounts for difference. | Documentation correction only; do not edit manifests. |
| Historical Colab runtime | Some archived environment details exist, but exact command/kernel/runtime/warnings unavailable. | Disclose unavailable details; avoid claiming exact runtime recreation. |

---

## 10. Integrity and Preservation Statement

- Original project: 18,132 non-venv files reported unchanged.
- Verified backup: 18,125 files reported unchanged.
- E01/E04 reproduction artifacts: 10/10 reported byte-identical to backup.
- E05 historical artifacts: 41/41 reported SHA-256 matches to backup.
- Official manifests and split assignments: unchanged.
- All generated audit files were reported inside the reproduction root.
- No historical notebook, dataset, manifest, prediction, metric, checkpoint or E05 artifact was modified.

The integrity statements are sourced from the verified P0 audit artifacts; direct hash verification was performed during P0.1–P0.5.

---

## 11. P0.6 Recommendation and Supervisor Decisions Requested

**Recommendation: CONDITIONAL GO** for supervisor review of the P0.6 report, with all limitations explicitly disclosed. Supervisor approval remains pending. The evidence does not support claiming that E05-U’s nested 5×4 procedure, uncertainty-model artifact reproducibility, or TestA/TestB risk performance has been fully validated.

1. Review and accept, reject, or request further investigation of unresolved E05-U provenance limitations.
2. Confirm whether the shared TestA–TestB source ID requires a separate identity/provenance investigation, without altering official split assignments.
3. Confirm whether any additional uncertainty-model reproduction is within the approved scope; no such training has been performed in P0.
4. Confirm the next phase and its boundaries. Any prospective participant image collection must wait for applicable ethics approval and informed consent.
5. Provide formal G0 supervisor signoff before literature-gap confirmation and prospective local-study preparation proceed.

---

## 12. Final Status

**P0.1–P0.5 RECHECK COMPLETE — P0.6 READY WITH LIMITATIONS**

This status means the P0.6 source material is ready with limitations. **The final PDF/DOCX has not been created.** This status does not mean all scientific limitations are resolved, G0 has been approved, or the next research phase is authorized.

---

## Appendix A — Supporting Evidence Register

The complete and authoritative list of P0 deliverables, phase reports, logs, evidence CSVs, and their recorded status is maintained in `P0_final_deliverable_inventory.csv` in `reports\P0_baseline_freeze\`. SHA-256 hashes are recorded as columns in `01_P0_artifact_inventory.csv`. This appendix intentionally does not duplicate or substitute for the final deliverable inventory.

— End of Report —
