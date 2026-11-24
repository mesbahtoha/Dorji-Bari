# P0.4D — E04 Clean Reproduction

**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Historical reference:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124`  
**Execution mode:** isolated reproduction `.venv`; notebook 03 bootstrap prefix + cell 54 only  
**Outcome:** E04 reproduced exactly on all compared artifacts.

E01 was not rerun. E02, E03, and E05 were not executed.

---

## 1. Pre-run safety

Operational checks:

| Item | Value |
|---|---|
| Python executable | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124\.venv\Scripts\python.exe` |
| Python version | 3.14.6 |
| `sys.prefix` | Reproduction `.venv` |
| `DORJIBARI_ROOT` | `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124` |
| Resolved project root | Reproduction root |
| Root match | True |

### E04 inputs

All resolve inside the reproduction root and exist:

```text
experiments\E02_geometry\subject_level_features\train_subject_features.csv
experiments\E02_geometry\subject_level_features\testA_subject_features.csv
experiments\E02_geometry\subject_level_features\testB_subject_features.csv
```

These tables contain 2,018 / 87 / 400 subjects respectively, 61 columns, and 53 model features in the configured order.

### E04 outputs

All resolve inside the reproduction root:

```text
experiments\E04_classical_ml\E04_experiment_config.json
experiments\E04_classical_ml\E04_cross_validation_results.csv
experiments\predictions\E04_classical_ml_predictions.csv
experiments\metrics\E04_classical_ml_metrics.csv
checkpoints\E04_classical_ml_models.joblib
```

Pre-run copies and SHA-256 hashes were preserved at:

```text
reports\P0_baseline_freeze\pre_run_E04\
```

All five pre-run files matched the verified backup. E01’s five output files were checked before E04 and remained byte-identical to the backup.

---

## 2. Execution

Only the bootstrap prefix (through its `PROJECT_ROOT` print) and notebook cell **54** were executed. The cell source was not modified.

- Cell 54 source SHA-256: `69950cfb2090d45d0e4e5e51857dba88d55a4458b86e4ce2649010b3cfee53eb`
- Cell 54 exit code: **0**
- Cell 54 elapsed: **893.667 s** (about 14 min 54 s)
- Execution started: 2026-11-24T09:12:13Z
- Execution ended: 2026-11-24T09:27:01Z
- Errors: none

### Full-cell execution disclosure

E04 cell 54 has no Ridge-only mode. It necessarily trained and evaluated:

- Ridge
- RandomForest
- MLP

RandomForest and MLP were therefore executed as unavoidable additional runs. No feature, target, split, hyperparameter-grid, or configuration change was made.

### Warnings

Seven `ConvergenceWarning` occurrences from MLP fitting were observed in the execution console:

```text
sklearn\neural_network\_multilayer_perceptron.py:785:
ConvergenceWarning: Stochastic Optimizer: Maximum iterations (1500) reached
and the optimization hasn't converged yet.
```

No error occurred. The child-process warning stream was not captured in the redirected Python log; it is recorded explicitly in `P0_clean_run_log.txt`.

### Ridge selection

| Target | Selected alpha | Best CV MAE (cm) |
|---|---:|---:|
| chest | 1.0 | 2.8261939582419444 |
| waist | 10.0 | 3.507116705916009 |
| hip | 10.0 | 2.6184019850468316 |
| shoulder-breadth | 1.0 | 0.8911365617971663 |
| arm-length | 1.0 | 0.8323156232524678 |

Selection used 5-fold subject-level `GroupKFold`, `scoring="neg_mean_absolute_error"`, on Train only. TestA/TestB were used only after refit.

---

## 3. Independent verification

### Predictions

| Check | Result |
|---|---|
| Rows | 7,305 vs 7,305 — exact |
| Unique `(model,target,split,subject_id)` keys | 7,305 vs 7,305 — exact |
| Columns / order | 6 vs 6 — exact |
| Model rows | Ridge 2,435; RandomForest 2,435; MLP 2,435 — exact |
| Actual values | maximum absolute difference **0.0** |
| Predictions | maximum absolute difference **0.0** |
| Per-model prediction differences | Ridge 0; RandomForest 0; MLP 0 |

### Metrics

| Metric | Rows | Maximum absolute difference |
|---|---:|---:|
| MAE | 30 | **0.0** |
| RMSE | 30 | **0.0** |
| R² | 30 | **0.0** |
| CV MAE | 30 | **0.0** |

All 30 metric rows and all 15 CV rows are exact.

### CV and configuration

- CV rows: 15 vs 15; keys and best parameters exact.
- E04 configuration: exact, 53 features and 5 targets.
- Feature order: exact.
- Selected alphas: exact.
- No TestA/TestB tuning.

### Generated artifact hashes

| Artifact | Size | SHA-256 equal to backup |
|---|---:|---|
| `E04_experiment_config.json` | 2,218 B | **yes** |
| `E04_cross_validation_results.csv` | 1,532 B | **yes** |
| `E04_classical_ml_predictions.csv` | 749,763 B | **yes** |
| `E04_classical_ml_metrics.csv` | 3,201 B | **yes** |
| `E04_classical_ml_models.joblib` | 142,942,729 B | **yes** |

---

## 4. Numerical differences

**None.**

- Actual-value maximum difference: 0.0
- Prediction maximum difference: 0.0
- MAE maximum difference: 0.0 cm
- RMSE maximum difference: 0.0 cm
- R² maximum difference: 0.0
- CV MAE maximum difference: 0.0
- Config/checkpoint: byte-identical

The reproduced E04 Ridge results, and the additionally executed RandomForest/MLP results, match the historical backup exactly.

---

## 5. Protection and limitations

- Original project remains 18,132 non-venv files.
- Verified backup remains 18,125 files.
- E01 outputs remain byte-identical after E04.
- E04 input manifests/features remain byte-identical to the backup.
- No official Train/TestA/TestB assignment or shared TestA–TestB ID was changed.
- No E02/E03/E05 training was run.
- The exact historical Colab command, kernel, hardware, and warning stream are not directly reproducible from the repository; only artifact-level equality is proven.
- Local Python 3.14.6 and scientific package versions differ from the original Colab freeze, so exact artifact equality here is evidence for this reproduction, not proof of identical runtime behavior.
- E04 remains non-selectable for Ridge-only execution.

**E04 REPRODUCED**
