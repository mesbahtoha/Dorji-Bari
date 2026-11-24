# P0.4 Reproducibility Statement

**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only

---

## 1. What was reproduced and verified

### E01 — height-only median + Ridge

- Executed only notebook 03 cell 44 after the non-writing bootstrap prefix.
- Inputs: official preprocessed Train/TestA/TestB manifests (6,133 / 1,684 / 1,158 rows; 2,018 / 87 / 400 subjects).
- Predictions: **487/487 rows exact**; subject IDs, columns, actual values and predictions all exact.
- Metrics: **20/20 rows exact**; maximum MAE, RMSE and R² differences all **0.0**.
- Artifacts: config, target medians, predictions, metrics and checkpoint are **byte-identical** to the verified backup by SHA-256.
- Execution: cell 44 exit 0; 0.795 s cell time; no errors.

### E04 — Ridge, RandomForest and MLP with 5-fold GroupKFold

- Executed only notebook 03 cell 54 after the non-writing bootstrap prefix.
- Inputs: official E02 subject-level feature tables (2,018 / 87 / 400 subjects; 53 ordered features).
- Validation: 5-fold subject-level `GroupKFold`; Train-only selection; TestA/TestB used only after refit.
- Ridge alphas: chest 1.0, waist 10.0, hip 10.0, shoulder 1.0, arm-length 1.0.
- Predictions: **7,305/7,305 rows exact** across Ridge, RandomForest and MLP; all subject IDs, columns, actual values and predictions exact.
- Metrics: **30/30 rows exact**; MAE, RMSE, R² and CV MAE maximum differences all **0.0**.
- CV results: **15/15 rows exact**, including best parameters.
- Artifacts: config, CV results, predictions, metrics and checkpoint are **byte-identical** to the verified backup by SHA-256.
- Execution: cell 54 exit 0; 893.667 s cell time; seven observed MLP `ConvergenceWarning` messages; no errors.

### Protection and isolation

- `DORJIBARI_ROOT` resolved to the reproduction root before notebook paths were resolved.
- All E01/E04 inputs and outputs remained inside the reproduction copy.
- E01 outputs remained unchanged after E04.
- Original project remains at 18,132 non-venv files; backup remains at 18,125 files.
- No official manifest, split, dataset, configuration, prediction, metric, checkpoint or historical artifact was modified.
- The shared TestA–TestB source ID was retained; no split assignment changed.

---

## 2. What was not reproduced or remains unverifiable

- E02, E03 and E05 were not re-run. This statement covers E01 and E04 only.
- The exact historical Colab execution command, kernel, hardware, and original runtime warning stream are not archived and cannot be reconstructed exactly.
- The original Colab environment used Python 3.13.16 / NumPy 2.4.6 / pandas 2.2.3 / scikit-learn 1.6.1; this reproduction used Python 3.14.6 / NumPy 2.5.5 / pandas 3.1.1 / scikit-learn 1.9.1. Artifact equality does **not** prove identical runtime behavior.
- E04 has no Ridge-only execution mode; the full cell also trained RandomForest and MLP. Their results matched exactly, but they were unavoidable additional runs.
- The warning capture for E04 is incomplete at the process-stream level: seven `ConvergenceWarning` messages were observed on the console, while child-process warnings were not present in the redirected Python log. This is documented in `P0_clean_run_log.txt`.
- No supervisor approval is claimed. No P0.5 or E05 uncertainty work was started.

---

## 3. Environment differences and limitations

### Reproduction environment

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

### Historical environment

```text
Python 3.13.16
NumPy 2.4.6
pandas 2.2.3
scikit-learn 1.6.1
PyTorch 2.14.1+cu130 (GPU)
```

The local reproduction is CPU-only. Direct E01/E04 packages match the local original `.venv`; four transitive versions differ (IPython, python-dateutil, packaging, platformdirs). `pip check` passed.

### Epistemic limitation

This is a **clean reproduction in an isolated copy**, not proof of identical Colab runtime behavior. The evidence establishes:

1. the same code and configurations were used;
2. the same official inputs were used;
3. the outputs, predictions, metrics and checkpoints are byte-identical to the verified backup;
4. the isolated paths did not touch the original project or backup.

It does not establish that the original Colab kernel, hardware, library internals, or runtime warnings were identical.

---

## 4. Evidence map

```text
reports\P0_baseline_freeze\P0_4C_E01_clean_reproduction.md
reports\P0_baseline_freeze\P0_4D_E04_clean_reproduction.md
reports\P0_baseline_freeze\04_P0_config_and_reproduction.md
reports\P0_baseline_freeze\P0_clean_run_log.txt
reports\P0_baseline_freeze\pre_run_E01\
reports\P0_baseline_freeze\pre_run_E04\
```

**P0.4 reproduction evidence is complete for the documented E01 and E04 scope.**
