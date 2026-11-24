# P0.4C — E01 Clean Reproduction

**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Historical comparison source:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124`  
**Execution environment:** reproduction `.venv` only  
**Status:** **E01 REPRODUCED**

No E02/E03/E04/E05 cell was run. No original project or backup file was modified.

---

## 1. Pre-execution setup

Fresh PowerShell session; reproduction environment activated:

```powershell
. .\.venv\Scripts\Activate.ps1
$env:DORJIBARI_ROOT = "D:\DorjiBari-P0-Reproduction\DorjiBari_20261124"
```

Confirmed in the run log:

| Item | Value |
|---|---|
| Python | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124\.venv\Scripts\python.exe` |
| Python version | 3.14.6 |
| `sys.prefix` | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124\.venv` |
| `DORJIBARI_ROOT` | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124` |
| Resolved `PROJECT_ROOT` | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124` |
| Root match | **True** |

### E01 cell 44 outputs

| Output | Pre-run inside copy |
|---|---|
| `experiments\E01_height_only\E01_config.json` | yes |
| `experiments\E01_height_only\training_target_medians.csv` | yes |
| `experiments\predictions\E01_height_only_predictions.csv` | yes |
| `experiments\metrics\E01_height_only_metrics.csv` | yes |
| `checkpoints\E01_height_only_ridge_models.joblib` | yes |

All five paths resolve under the reproduction root; none reaches the original project or backup.

### Pre-run preservation

Existing E01 artifacts were copied to:

```text
reports\P0_baseline_freeze\pre_run_E01\
```

with hashes in `reports\P0_baseline_freeze\pre_run_E01\pre_run_hashes.json`.

| File | SHA-256 (pre-run, short) |
|---|---|
| `E01_config.json` | `79B1EB81C6E0B99F...` |
| `training_target_medians.csv` | `85CD2739355B4509...` |
| `E01_height_only_predictions.csv` | `579E9D128D646F8E...` |
| `E01_height_only_metrics.csv` | `3641B88334009DE8...` |
| `E01_height_only_ridge_models.joblib` | `D6BE77A1A1E12C20...` |

All pre-run E01 hashes matched the verified backup exactly.

---

## 2. Execution

Executed only:

1. notebook 03 cell 1 bootstrap prefix (through the `PROJECT_ROOT` print; the manifest-writing body was not executed);
2. notebook 03 cell **44** (E01 only).

Cell 44 source SHA-256:

```text
fbd5b8e5f8a971288a88de9fa983b5fa54f4a68cd8ddf2fd568e1ac95b02ca1c
```

| Item | Result |
|---|---|
| Command exit code | 0 |
| Cell 44 exit code | 0 |
| Cell 44 elapsed | **0.795 s** |
| Wall time | **6.592 s** |
| Errors | none |
| E02–E05 execution | none |
| Test tuning | none — fit on Train, evaluate TestA/TestB |

Capture file:

```text
reports\P0_baseline_freeze\P0_clean_run_log.txt
```

The log contains complete stdout/stderr, package versions, resolved root, execution timestamps, cell exit code, and elapsed time. Its mixed PowerShell UTF-8/UTF-16 capture was normalized to UTF-8 without removing text.

Environment:

```text
Python 3.14.6
NumPy 2.5.5
pandas 3.1.1
scikit-learn 1.9.1
joblib 1.6.0
```

---

## 3. Comparison with historical E01

Historical source: verified backup directly (identical to the pre-run reproduction artifacts).

### Predictions

| Check | Result |
|---|---|
| Prediction rows | 487 vs 487 — match |
| Unique `(split, subject_id)` keys | 487 vs 487 — exact set match |
| Subject IDs | exact match |
| Columns | 18 vs 18 — exact order match |
| Split counts | TestA 87, TestB 400 — match |
| Actual-value maximum absolute difference | **0.0** |
| Prediction maximum absolute difference | **0.0** |
| Prediction columns with any difference | **none** |

The 15 numeric columns are `actual_*`, `median_pred_*`, and `ridge_pred_*` for the five targets.

### Metrics

| Check | Result |
|---|---|
| Metric rows | 20 vs 20 — exact key match |
| MAE maximum absolute difference | **0.0** |
| RMSE maximum absolute difference | **0.0** |
| R² maximum absolute difference | **0.0** |
| Rows with any metric difference | **0** |

All E01 metric values are bit-identical, including both `training_median` and `ridge` on TestA/TestB.

### Other E01 artifacts

| File | Size | SHA-256 equal to backup |
|---|---:|---|
| `E01_config.json` | 590 B | **yes** |
| `training_target_medians.csv` | 152 B | **yes** |
| `E01_height_only_predictions.csv` | 160,338 B | **yes** |
| `E01_height_only_metrics.csv` | 1,898 B | **yes** |
| `E01_height_only_ridge_models.joblib` | 3,863 B | **yes** |

The E01 config, target medians, predictions, metrics, and checkpoint are all byte-identical to the verified backup.

---

## 4. Numerical differences

**None.**

- Prediction rows: 487/487, exact.
- Metric rows: 20/20, exact.
- Maximum MAE difference: 0.0 cm.
- Maximum RMSE difference: 0.0 cm.
- Maximum R² difference: 0.0.
- Actual values: 0.0 maximum difference.
- Config/medians/checkpoint: byte-identical.

No result was fabricated, rounded, or substituted.

---

## 5. Protection and limitations

- Original project remains at 18,132 non-venv files; verified backup remains at 18,125 files.
- Original E01 artifacts still match the backup hashes.
- No package was installed into the original `.venv`.
- No original or backup file was modified.
- Only the reproduction copy's E01 outputs were regenerated; pre-run copies are retained.
- The only post-run file-encoding adjustment was the run log normalization noted above.
- E04 and other models were not executed.

**E01 REPRODUCED**
