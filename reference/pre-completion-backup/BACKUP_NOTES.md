# Pre-repair backup (2026-11-19)

This folder holds a byte-for-byte copy of the project files taken **before**
the final notebook-repair pass. It exists so that the live notebooks and
documents can always be compared with a known earlier state.

Contents:

| File | Purpose |
|---|---|
| `01_environment_setup.ipynb` | Notebook before the final code repairs |
| `02_dataset_audit.ipynb` | Notebook before the final code repairs |
| `03_Dataset_Preprocessing.ipynb` | Notebook before the final code repairs |
| `README.md` | Documentation before the final repair notes |
| `PROJECT_INVENTORY.md` | Inventory before the final status update |
| `requirements.txt` | Colab `pip freeze` as it stood at backup time |
| `requirements-local.txt` | Local CPU pins as they stood at backup time |
| `environment_report.txt` | Environment report at backup time |
| `validate_project.py` | Validator at backup time |

## Do not edit these files

They are evidence, not working copies. The live project lives two levels up.
This note is the only file added after the backup was taken.

Verify that saved outputs were preserved by running the validator with this
directory as the comparison source:

```powershell
$env:DORJIBARI_NOTEBOOK_BACKUP = "D:\DorjiBari-Research\reference\pre-completion-backup"
python scripts/validate_project.py
```

On macOS / Linux:

```bash
DORJIBARI_NOTEBOOK_BACKUP="$(pwd)/reference/pre-completion-backup" \
  python scripts/validate_project.py
```

The only accepted difference is the removal of an illegal `metadata` key from
two `stream` outputs in notebook 03 (nbformat rejects that key; the text is
identical). Every other saved output and every execution count must match.
