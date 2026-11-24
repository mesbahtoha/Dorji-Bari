# P0.4B.2 — Isolated Environment Setup

**Date:** 2026-11-24  
**Reproduction root:** `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124`  
**Original project:** `D:\DorjiBari-Research` — read-only  
**Verified backup:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124` — read-only

No training was run. No E01/E04 cell was executed. No original project or backup file was modified.

---

## 1. Dependency inspection

- `requirements.txt` is the archived Colab freeze for Python 3.13.16; it was not used for this Python 3.14.6 environment.
- `requirements-local.txt` is the verified Python 3.14.6 CPU stack and the source of the exact direct pins.
- `environment_report.txt` records Python 3.14.6, NumPy 2.5.5, pandas 3.1.1, scikit-learn 1.9.1, and no GPU.
- E01 cell 44 imports: `os`, `json`, `joblib`, `numpy`, `pandas`, and `sklearn` pipeline/model/metrics modules.
- E04 cell 54 imports: the same core stack plus `warnings`, `sklearn.model_selection`, `RandomForestRegressor`, and `MLPRegressor`.
- Notebook cell 1 also imports `IPython.display`, so IPython/ipykernel is required to execute the notebook bootstrap.

### Minimum installed set

Installed into the reproduction `.venv` only:

```text
numpy==2.5.5
pandas==3.1.1
scipy==1.18.1
scikit-learn==1.9.1
joblib==1.6.0
matplotlib==3.11.2
ipykernel==7.4.0
```

Rationale: NumPy/pandas/scikit-learn/joblib are direct E01/E04 requirements; SciPy is a scikit-learn runtime dependency; matplotlib was explicitly requested for verification; ipykernel provides IPython for notebook cell 1. No unrelated project stack (torch, OpenCV, boto3, statsmodels, tqdm) was installed.

Install command used (no `--upgrade`):

```powershell
.venv\Scripts\python.exe -m pip install --no-cache-dir --only-binary=:all: `
  numpy==2.5.5 pandas==3.1.1 scipy==1.18.1 scikit-learn==1.9.1 `
  joblib==1.6.0 matplotlib==3.11.2 ipykernel==7.4.0
```

`PIP_EXIT=0`; all packages resolved to Python 3.14 (`cp314`/abi3/pure-Python) wheels.

---

## 2. Version comparison and import verification

| Package | Original `.venv` | Reproduction `.venv` | Match |
|---|---:|---:|---|
| Python | 3.14.6 | 3.14.6 | YES |
| NumPy | 2.5.5 | 2.5.5 | YES |
| pandas | 3.1.1 | 3.1.1 | YES |
| SciPy | 1.18.1 | 1.18.1 | YES |
| scikit-learn | 1.9.1 | 1.9.1 | YES |
| joblib | 1.6.0 | 1.6.0 | YES |
| matplotlib | 3.11.2 | 3.11.2 | YES |
| ipykernel | 7.4.0 | 7.4.0 | YES |
| IPython | 9.18.1 | 9.19.1 | no (transitive) |
| python-dateutil | 2.9.0.post0 | 4.0.0 | no (transitive) |
| packaging | 26.3 | 26.4 | no (transitive) |
| platformdirs | 4.14.7 | 4.14.8 | no (transitive) |
| threadpoolctl | 3.8.0 | 3.8.0 | YES |
| tzdata | 2026.6 | 2026.6 | YES |
| pillow | 13.0.0 | 13.0.0 | YES |

The four direct E01/E04 packages and matplotlib/ipykernel match exactly. Transitive differences are resolver-level: E01/E04 do not use date parsing, IPython display internals, packaging, or platformdirs in model computation. `pip check` reports **no broken requirements**.

Import test results:

```text
python       3.14.6
numpy        2.5.5
pandas       3.1.1
scipy        1.18.1
sklearn      1.9.1
joblib       1.6.0
matplotlib   3.11.2
IPython      9.19.1
ipykernel    7.4.0
```

---

## 3. Read-only data and no-fit smoke test

Run with the reproduction `.venv`; no model was fitted.

| Check | Result |
|---|---|
| E01 Train manifest | 6,133 rows, 2,018 subjects |
| E01 TestA manifest | 1,684 rows, 87 subjects |
| E01 TestB manifest | 1,158 rows, 400 subjects |
| E01 subject collapse | 2,018 rows; target medians match saved values |
| E04 training features | 2,018 rows, 61 columns, 53 model features, 0 missing |
| E04 GroupKFold | 5 folds: 404/404/404/403/403 validation subjects |
| Ridge pipeline construction | successful (`StandardScaler + Ridge`) |
| Model fit | **not performed** |

This confirms pandas/scikit-learn can read the actual E01/E04 inputs and construct the intended folds/model in the new environment.

---

## 4. Path resolver verification

Notebook cell 1 resolves the root in this order:

1. `DORJIBARI_ROOT` environment variable;
2. Colab Drive location;
3. nearest parent of the working directory containing `notebooks/`.

The exact bootstrap prefix was executed in a subprocess with:

```text
DORJIBARI_ROOT=D:\DorjiBari-P0-Reproduction\DorjiBari_20261124
```

It returned:

```text
DorjiBari project root: D:\DorjiBari-P0-Reproduction\DorjiBari_20261124
RESOLVED_MATCHES=True
```

Only the bootstrap prefix (through the `PROJECT_ROOT` print) was executed; the rest of cell 1, which writes clean manifests, was **not** executed.

All 16 checked E01/E04 input/output paths resolved inside the reproduction root:

| Group | Inputs / outputs checked |
|---|---|
| E01 inputs | 3 preprocessed manifests — all exist |
| E01 outputs | config, target medians, predictions, metrics, checkpoint |
| E04 inputs | 3 subject-feature tables — all exist |
| E04 outputs | config, CV results, predictions, metrics, checkpoint |

`ALL_PATHS_INSIDE=True`. No checked path points to `D:\DorjiBari-Research` or the backup.

### Reliable `DORJIBARI_ROOT` setting

Set the environment variable in the process that launches the notebook kernel, **before cell 1 runs**:

```powershell
$env:DORJIBARI_ROOT = "D:\DorjiBari-P0-Reproduction\DorjiBari_20261124"
```

Then launch Jupyter/VS Code from that environment, or select the reproduction `.venv` as the kernel. Do not rely on the current shell default: `DORJIBARI_ROOT` is currently unset, and if a notebook is launched from the original working directory without it, fallback resolution could select the original project. No notebook or config was modified to force the path.

---

## 5. Source and backup protection

- Package installation occurred only in `D:\DorjiBari-P0-Reproduction\DorjiBari_20261124\.venv`.
- No package was installed into `D:\DorjiBari-Research\.venv`.
- The original project still has 18,132 non-venv files; the verified backup still has 18,125 files.
- No source, backup, dataset, manifest, config, prediction, metric, notebook, or checkpoint was edited.
- The only report created is this file inside the reproduction copy.

---

## 6. Remaining conditions

1. `DORJIBARI_ROOT` must be set in the kernel-launch environment; it is not persisted globally.
2. E04 cell 54 still has no Ridge-only selector; it will train all three models if executed.
3. Exact numerical parity with the original Colab/older `.venv` run is not guaranteed because four transitive package versions differ; direct E01/E04 libraries match.
4. No model fitting or E01/E04 execution was performed, per the strict restrictions.

**READY FOR E01**
