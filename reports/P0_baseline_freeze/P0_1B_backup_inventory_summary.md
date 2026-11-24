# P0.1B — Backup and Artifact Inventory Summary

**Date:** 2026-11-24
**Project root:** `D:\DorjiBari-Research`
**Backup path:** `D:\DorjiBari-P0-Backups\DorjiBari_20261124`
**Operation mode:** read-only source; no training; no source file overwritten, deleted, renamed, or moved.

---

## 1. Backup

| Item | Value |
|---|---:|
| Backup created | 2026-11-24 12:07 local |
| Source files (excl. `.venv`, `.vscode`) | 18,125 |
| Backup files | 18,125 |
| Source bytes | 255,717,339 (243.87 MiB) |
| Backup bytes | 255,717,339 (243.87 MiB) |
| Robocopy exit code | 1 (success; files copied) |
| Elapsed | 0:00:22 |

Command applied:

```text
robocopy D:\DorjiBari-Research D:\DorjiBari-P0-Backups\DorjiBari_20261124 ^
  /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /XD "<root>\.venv" "<root>\.vscode"
```

The destination did not exist before this run. No `/MIR` or `/MOVE` was used, and no existing backup was overwritten.

### Verification

| Check | Result |
|---|---|
| File count source vs backup | 18,125 = 18,125 — PASS |
| Total bytes source vs backup | 255,717,339 = 255,717,339 — PASS |
| Missing relative paths | 0 — PASS |
| Extra relative paths | 0 — PASS |
| Per-file size mismatches | 0 — PASS |
| Critical files hashed (`.csv`, `.json`, `.joblib`, `.ipynb`) | 143 |
| SHA-256 mismatches | **0** — PASS |

**Verification outcome: PASS.** No hash mismatch was found. All 143 critical files in the backup were re-hashed and matched the source byte-for-byte.

---

## 2. Artifact inventory

- **File:** `reports\P0_baseline_freeze\01_P0_artifact_inventory.csv`
- **Observed rows:** 18,125 (`observed_status = PRESENT`)
- **Observed bytes:** 255,717,339
- **Critical files hashed:** 143 (all present critical files; 64-character SHA-256 populated)
- **Non-critical files:** SHA-256 intentionally blank, as permitted
- **Invalid roles:** 0
- **MISSING rows:** 3 (sizes and hashes intentionally blank)
- **Cross-check:** every populated inventory hash and size matched the backup copy — 0 mismatches

Role distribution:

| Role | Files |
|---|---:|
| image | 17,960 |
| input | 47 |
| metric | 45 |
| raw_prediction | 21 |
| reference | 13 |
| other | 12 |
| config | 9 |
| report | 7 |
| code | 4 |
| model | 4 |
| notebook | 3 |

### Missing expected files

The following expected E02 Stage 6 outputs are absent. They are recorded as `MISSING` in the CSV notes section with no invented size or hash:

- `experiments\E02_geometry\photo_level_features\train_feature_extraction_failures.csv`
- `experiments\E02_geometry\photo_level_features\testA_feature_extraction_failures.csv`
- `experiments\E02_geometry\photo_level_features\testB_feature_extraction_failures.csv`

No other expected-artifact absence was confirmed during this task.

### Relocated preprocessed checkpoint manifests

The three expected `experiments\logs\{train,testA,testB}_preprocessed_checkpoint.csv` paths are absent, but the same checkpoint manifests are present at:

- `dataset\BodyM\processed\preprocessed_manifests\train_preprocessed_checkpoint.csv`
- `dataset\BodyM\processed\preprocessed_manifests\testA_preprocessed_checkpoint.csv`
- `dataset\BodyM\processed\preprocessed_manifests\testB_preprocessed_checkpoint.csv`

These are recorded as `PRESENT` in `01_P0_artifact_inventory.csv` at their actual dataset paths. They are relocated, not missing. No historical artifact was changed.

---

## 3. Exclusions and scope

Excluded from both backup and inventory:

- `.venv\` — recreate from `requirements-local.txt` (Python 3.14.6)
- `.vscode\` — optional editor settings (1 file)

Included in full: `dataset`, `experiments`, `checkpoints`, `reports`, `notebooks`, `scripts`, `configs`, `reference`, `figures`, and root project files.

---

## 4. Limitations

1. **The backup is on the same physical drive (D:) as the source. It is not an independent external backup.** A drive failure, filesystem corruption, or ransomware event could affect both copies. An off-drive copy is still required.
2. The project has no Git repository; this snapshot is the only versioned recovery point.
3. Integrity is hash-verified for the 143 critical files only; all other files were verified by relative path, file count, and byte size, not by SHA-256.
4. The inventory describes the pre-audit snapshot that was backed up. Its two P0.1B outputs (`01_P0_artifact_inventory.csv` and this summary) were created afterward and are not self-inventoried; a file cannot contain a stable hash of itself.
5. `PROJECT_INVENTORY.md` was deliberately not modified and remains stale about the now-complete dataset and populated `experiments/logs|metrics|predictions`.
6. Point-in-time backup only; no subsequent project changes are covered.
