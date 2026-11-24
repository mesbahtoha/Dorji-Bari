# P0.2 — Dataset Integrity Audit

**Date:** 2026-11-24  
**Root:** `D:\DorjiBari-Research`  
**Mode:** read-only; no source, manifest, image, split, or backup file was modified. No training was run.  
**Report:** `reports\P0_baseline_freeze\02_P0_dataset_integrity.md`

Official basis: `dataset\BodyM\processed\{split}_manifest.csv`, `processed\preprocessed_manifests\{split}_preprocessed_manifest.csv`, `reports\split_summary.csv`, and `reports\subject_split_integrity_audit.md`. Source-level counts use `dataset\BodyM\audit\{split}_object_inventory.csv`.

---

## 1. Verification summary

| # | Check | Result |
|---|---|---|
| 1 | Train/TestA/TestB pair and unique-subject counts | **PASS** — official counts match audit; clean-manifest exception in check 11 |
| 2 | Front/side pairing and missing image files | **PASS** — 0 unpaired source pairs, 0 missing processed images |
| 3 | Pairwise subject overlap | **PASS** — 0 / 0 / 1 |
| 4 | Shared source ID identified with evidence | **PASS** — exact ID located; identity match **NOT VERIFIABLE** |
| 5 | Height input is `hwg_metadata.height_cm`, not `measurements.height` | **PASS** — 8,975/8,975 rows match `height_cm`; 0 match `measurements.height` |
| 6 | Five targets present and correct | **PASS** — 5/5 columns, 0 missing, 0 mismatches |
| 7 | Units are centimetres | **PASS** — documented and range-consistent |
| 8 | QC exclusions: Train 1, TestA 0, TestB 2 | **PASS** — reconciled exactly; see QC section |
| 9 | Duplicate image paths and subject partition containment | **PASS** — 0 duplicate paths; one disclosed cross-partition ID |
| 10 | Official TestB 400 vs 399 sensitivity | **PASS** — 400 official, 399 supplementary; metrics reproduce |
| 11 | `testB_clean_manifest.csv` consistency with official/QC | **FAIL** — 1,159 rows, includes one QC-excluded pair |

---

## 2. Counts

| Split | Source pairs (object inventory) | Official pairs | Clean-manifest rows | Unique subjects |
|---|---:|---:|---:|---:|
| Train | 6,134 | 6,133 | 6,133 | 2,018 |
| TestA | 1,684 | 1,684 | 1,684 | 87 |
| TestB | 1,160 | 1,158 | **1,159** | 400 |
| **Total** | **8,978** | **8,975** | **8,976** | **2,504 globally unique** |

- Subject memberships sum to **2,505**; globally unique IDs are **2,504** (one ID is in two splits).
- Source image pairs total **8,978** (17,956 PNGs); processed pairs total **8,975** (17,950 PNGs) after 3 QC exclusions.
- `all_splits_manifest.csv`: 8,975 rows, 8,975 unique photo IDs, 2,504 unique subjects.
- 1,802 subjects have multiple photo pairs; maximum 45 pairs; minimum 1.

The TestB clean-manifest discrepancy is detailed in check 11; it does not change the official counts above.

---

## 3. Subject overlap

| | Train | TestA | TestB |
|---|---:|---:|---:|
| **Train** | — | 0 | 0 |
| **TestA** | 0 | — | **1** |
| **TestB** | 0 | **1** | — |

Exact overlapping subject ID:

```text
TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ
```

No photo ID is shared across splits: Train–TestA 0, Train–TestB 0, TestA–TestB 0.

### Shared-ID evidence

- Present in both original maps: `testA_subject_to_photo_map.csv` (22 rows) and `testB_subject_to_photo_map.csv` (7 rows).
- TestA: 22 official photo pairs. TestB: 7 source pairs, **6 official** pairs after QC exclusion of `578f12cd7dbbf39ccebc3116eaea41d6`.
- `testA_hwg_metadata.csv`: female, **163.2 cm**, 61.7 kg.
- `testB_hwg_metadata.csv`: female, **168.0 cm**, 62.0 kg.
- `testA_measurements.csv`: `height=164.765`, chest 101.439, waist 82.465, hip 94.533, shoulder 34.678, arm 48.871 cm.
- `testB_measurements.csv`: `height=164.940`, chest 100.627, waist 80.231, hip 94.271, shoulder 34.905, arm 48.628 cm.

The two splits carry the same source subject ID but conflicting height and measurement records. This establishes an ID collision/shared source identifier, **not** a confirmed identity match. The ID is preserved in the official splits and was not removed. The reason for the repeated ID remains unresolved.

---

## 4. Height and target mapping

### Height input

| Comparison | Rows checked | Exact matches | Mismatches | Maximum absolute difference |
|---|---:|---:|---:|---:|
| Manifest `height_cm` vs `hwg_metadata.height_cm` | 8,975 | 8,975 | **0** | 0.0000 cm |
| Manifest `height_cm` vs `measurements.height` | 8,975 | **0** | 8,975 | **30.4486 cm** |

Per-split maximum difference from `measurements.height`: Train 22.8542 cm, TestA 13.7463 cm, TestB 30.4486 cm.

Evidence that `height_cm` is the model input:

- `notebooks\03_Dataset_Preprocessing.ipynb` joins `hwg_metadata` on `["subject_id", "height_cm"]` and asserts `height_cm` is present.
- `experiments\E01_height_only\E01_config.json`: `input_features = ["height_cm"]`, `target_unit = "cm"`.
- `dataset\BodyM\metadata\research_field_mapping.md`: explicitly says not to use `measurements.height`; `hwg_metadata.height_cm` is subject stature.
- Manifest height range: **141.0–197.5 cm**; all 2,018/87/400 subjects match their split `hwg_metadata` exactly.

### Five targets

Columns present exactly: `chest`, `waist`, `hip`, `shoulder-breadth`, `arm-length`.

| Target | Missing | Mismatches vs `measurements.csv` | Observed range (cm) |
|---|---:|---:|---:|
| chest | 0 | 0 | 76.874–158.098 |
| waist | 0 | 0 | 61.852–164.297 |
| hip | 0 | 0 | 80.676–166.852 |
| shoulder-breadth | 0 | 0 | 28.628–44.323 |
| arm-length | 0 | 0 | 39.386–60.157 |

All 8,975 official rows have non-null targets and exact agreement with `measurements.csv` (maximum absolute difference 0.0).

---

## 5. Units

**PASS (documented).**

- `research_field_mapping.md` lists `height_cm`, `chest`, `waist`, `hip`, `shoulder-breadth`, and `arm-length` in **cm**, and requires all five targets to remain in centimetres.
- `README.md` states: “Report all measurements in centimetres.”
- `E01_config.json` sets `target_unit: "cm"`.
- Observed ranges are consistent with centimetres (height 141–197.5; chest/waist/hip approximately 62–167; shoulder 28.6–44.3; arm 39.4–60.2).

Units are not independently derivable from the CSV values; this conclusion rests on the project’s source-schema documentation plus range consistency.

---

## 6. QC decisions

Source pairs minus official pairs gives exactly **1 / 0 / 2** exclusions. The post-QC `qc_excluded` column is `False` for every retained row, so the exclusions were reconstructed from source object inventories versus official manifests and corroborated by `qc_exclusion_summary.csv` and `problematic_image_audit.csv`.

| Split | Excluded subject | Excluded photo | Reason | Official decision |
|---|---|---|---|---|
| Train | `Xgshyw2K_FeeM3GNCyfoS5pJoTNIfEGMf1qKQxiO5YU` | `49e8f991af693b63836a077a636aa037` | side: large irregular foreground region (High) | Exclude pair; 6 alternatives accepted |
| TestA | — | — | — | none |
| TestB | `3hpDSNj5_25ceylKU4jJLSldgKCE4QJRGi2mmPqAcOA` | `6b25639753d2cecde54f99523f675ccc` | front: large detached component (High); side: detached component below feet (Medium) | Exclude pair; 2 alternatives accepted |
| TestB | `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ` | `578f12cd7dbbf39ccebc3116eaea41d6` | side: silhouette truncated at bottom boundary (Medium) | Exclude complete pair |

- `problematic_image_audit.csv` records all four view-level findings; `affected_subject_impact.csv` and `alternative_photo_pair_visual_review.csv` document accepted replacements.
- All three have `removed_from_dataset = False`: original source images are retained; exclusion applies only to the paired-view input.
- `testB_manifest.csv`, `testB_manifest_before_qc_refresh.csv`, and the object inventory corroborate the two TestB exclusions.

### Check 11 — FAIL: stale TestB clean manifest

`testB_clean_manifest.csv` contains **1,159** rows, including the QC-excluded pair:

```text
subject: TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ
photo:   578f12cd7dbbf39ccebc3116eaea41d6
front:   testB/mask/578f12cd7dbbf39ccebc3116eaea41d6.png
side:    testB/mask_left/578f12cd7dbbf39ccebc3116eaea41d6.png
```

By contrast, `testB_manifest.csv` and `testB_preprocessed_manifest.csv` both have **1,158** rows, and the TestB image folder contains **2,316** files (1,158 pairs). The clean manifest therefore has one row without a corresponding preprocessed image pair and contradicts the documented QC decision. The row was **not** removed or altered during this audit. Downstream use of `testB_clean_manifest.csv` was not established here.

---

## 7. Images, duplicates, and partition containment

### Front/side pairing

| Split | Source front | Source side | Unpaired source | Processed front | Processed side | Missing |
|---|---:|---:|---:|---:|---:|---:|
| Train | 6,134 | 6,134 | 0 | 6,133 | 6,133 | 0 |
| TestA | 1,684 | 1,684 | 0 | 1,684 | 1,684 | 0 |
| TestB | 1,160 | 1,160 | 0 | 1,158 | 1,158 | 0 |

- All 17,950 processed PNGs exist; every path in the preprocessed manifests resolves to a non-zero file.
- All processed filenames are `<photo_id>.png`; front/side directories and split paths are correct.
- No unreferenced processed PNGs; expected 2 × 8,975 = 17,950.
- Source pairing (17,956 images) is verified from `*_object_inventory.csv` key sets; raw source images are not present locally.

### Duplicates

| Check | Result |
|---|---:|
| Duplicate processed front paths | 0 |
| Duplicate processed side paths | 0 |
| Same path used for front and side | 0 |
| Duplicate `front_s3_key` values | 0 |
| Duplicate `side_s3_key` values | 0 |
| Duplicate official photo IDs | 0 |
| Photo ID overlap across splits | 0 |

### Partition containment

- 2,504 globally unique subjects; 2,505 split memberships.
- **One** subject is in more than one split: the shared `TlIG_...` ID in TestA and TestB.
- Every other subject’s pairs remain within one partition, including all 1,802 multi-pair subjects.
- The Train split has no subject-ID overlap with TestA or TestB.

---

## 8. TestB 400 vs 399 reconciliation

**PASS.**

- Official TestB: **400 unique subject IDs**, 1,158 pairs. This is the primary evaluation split.
- Supplementary sensitivity analysis removes the shared TestA–TestB ID, leaving **399 subjects** and 1,152 pairs.
- `reports\testb_overlap_sensitivity.csv` records `official_subjects = 400` and `sensitivity_subjects = 399` for all five targets.
- Recomputing Ridge metrics from `experiments\predictions\E04_classical_ml_predictions.csv` with the shared ID excluded reproduces the reported metrics to floating-point precision (maximum difference ≤ 2.3e-16).

Reported MAE change when moving from 400 to 399 subjects:

| Target | ΔMAE (cm) | ΔR² |
|---|---:|---:|
| chest | −0.00126 | +0.000231 |
| waist | −0.01656 | +0.001336 |
| hip | −0.01292 | +0.001230 |
| shoulder-breadth | +0.00053 | +0.000207 |
| arm-length | +0.00177 | +0.000026 |

The 400 vs 399 difference is therefore fully explained by excluding the one shared subject: it is a supplementary sensitivity analysis, not a change to the official TestB split.

---

## 9. Commands/scripts used

Read-only Python 3.14.6 (`.venv\Scripts\python.exe`) scripts were kept outside the project root:

```text
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_2_dataset_audit.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_2_qc_source.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_2_official_stats.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_2_diag.py
C:\Users\Mesbahul Alam Toha\AppData\Local\Temp\opencode\p0_2_diag2.py
```

Core operations: CSV reads with `csv.DictReader(..., encoding="utf-8-sig")`; manifest subject/photo set intersections; source object-inventory front/side key comparison; preprocessed-path `os.path.exists` and file-size checks; joins to `*_hwg_metadata.csv` and `*_measurements.csv`; and MAE/RMSE/R² recomputation from E04 Ridge predictions. PowerShell was used only for directory listings and targeted `Select-String` evidence lookup.

No source, backup, split, notebook, or experiment file was written, renamed, deleted, or moved. Only this report was created.

---

## 10. Limitations

1. Raw BodyM source images are not present locally; front/side source pairing was verified against the S3 object inventory keys, not by re-reading source pixels.
2. Unit verification is documentary plus range-consistency evidence, not an independent measurement of the original source schema.
3. The shared TestA–TestB ID has conflicting height and measurement records; the cause is unresolved and identity must not be asserted.
4. `testB_clean_manifest.csv` is inconsistent with the official/QC manifests (1,159 vs 1,158). It was not modified; its downstream use and impact were not verified.
5. The post-QC manifests have `qc_excluded = False` for all retained rows; QC counts were reconstructed from source-vs-official differences and audit files.
6. TestB sensitivity metrics were recomputed from existing predictions; no model was retrained and the official TestB results were not replaced.
