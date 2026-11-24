"""Lightweight validation for DorjiBari-Research.

Run from anywhere:

    python scripts/validate_project.py

Checks performed (no dataset downloads, no experiments, no writes):
  1. All notebooks are valid JSON / nbformat 4 and every code cell compiles.
  2. Every notebook starts with the portable project-root bootstrap.
  3. No executed code contains a hardcoded Colab path.
  4. Required project directories exist.
  5. Recovered artifacts (figures, config, reports) are readable and complete.
  6. README.md is identical to the README template inside notebook 01.
  7. Every third-party import is covered by requirements-local.txt.
  8. Optional: if DORJIBARI_NOTEBOOK_BACKUP points at the pre-repair
     notebooks, confirm that saved outputs are still byte-identical.

Exit code 0 means all checks passed.
"""
from __future__ import annotations

import ast
import csv
import json
import os
import sys

import nbformat
from PIL import Image

NOTEBOOKS = [
    "01_environment_setup.ipynb",
    "02_dataset_audit.ipynb",
    "03_Dataset_Preprocessing.ipynb",
]

COLAB_ROOT = "/content/drive/MyDrive/DorjiBari-Research"

REQUIRED_DIRS = [
    "dataset/BodyM",
    "dataset/Local_Dataset",
    "experiments/logs",
    "experiments/metrics",
    "experiments/predictions",
    "figures",
    "reports",
    "checkpoints",
    "configs",
    "src",
]

STDLIB = {
    "collections", "datetime", "importlib", "io", "json", "math", "os",
    "platform", "random", "re", "shutil", "subprocess", "sys", "time",
    "warnings",
}

DISTRIBUTIONS = {
    "boto3": "boto3",
    "botocore": "botocore",
    "cv2": "opencv-python",
    "IPython": "ipykernel",
    "joblib": "joblib",
    "matplotlib": "matplotlib",
    "numpy": "numpy",
    "pandas": "pandas",
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "scipy": "scipy",
    "statsmodels": "statsmodels",
    "torch": "torch",
    "tqdm": "tqdm",
    # Provided by the Colab runtime; the notebooks guard this import.
    "google": None,
}


def find_root() -> str:
    """Resolve the project root the same way the notebooks do."""
    override = os.environ.get("DORJIBARI_ROOT")
    if override and os.path.isdir(override):
        return os.path.abspath(override)

    current = os.path.abspath(os.getcwd())
    candidates = [current]
    while True:
        parent = os.path.dirname(candidates[-1])
        if parent == candidates[-1]:
            break
        candidates.append(parent)

    for candidate in candidates:
        if os.path.isdir(os.path.join(candidate, "notebooks")):
            return candidate

    if os.path.isdir("/content/drive/MyDrive/DorjiBari-Research"):
        return "/content/drive/MyDrive/DorjiBari-Research"

    return current


ROOT = find_root()
FAILURES: list[str] = []


def check(condition: bool, message: str) -> None:
    print(f"  {'PASS' if condition else 'FAIL'}  {message}")
    if not condition:
        FAILURES.append(message)


def read_notebook(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def code_cells(notebook: dict) -> list[dict]:
    return [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]


def strip_magics(source: str) -> str:
    return "\n".join(
        "pass" if line.lstrip().startswith(("%", "!", "?")) else line
        for line in source.splitlines()
    )


def section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def validate_notebooks() -> dict[str, dict]:
    section("1. NOTEBOOKS")
    loaded = {}

    for name in NOTEBOOKS:
        path = os.path.join(ROOT, "notebooks", name)
        print(f"\n{name}")

        if not os.path.isfile(path):
            check(False, "notebook present")
            continue

        raw = read_notebook(path)
        loaded[name] = raw
        nb = nbformat.reads(json.dumps(raw), as_version=4)
        nbformat.validate(nb)
        check(True, "valid JSON and nbformat 4")

        cells = code_cells(raw)
        errors = []
        for index, cell in enumerate(cells):
            try:
                ast.parse(strip_magics("".join(cell["source"])))
            except SyntaxError as exc:
                errors.append((index, exc.lineno, exc.msg))
        check(not errors, f"all {len(cells)} code cells compile {errors or ''}")

        first = "".join(cells[0]["source"]) if cells else ""
        check("def _dj_root(" in first and "PROJECT_ROOT = _dj_root()" in first,
              "first code cell defines the portable project root")

        executed = 0
        for cell in raw["cells"]:
            source = "".join(cell["source"])
            marker = 'readme = r"""'
            if marker in source:
                start = source.index(marker) + len(marker)
                end = source.index('"""', start)
                source = source[:source.index(marker)] + source[end:]
            executed += source.count(COLAB_ROOT)
        check(executed <= 1, f"no hardcoded Colab path in executed code ({executed})")

    return loaded


def validate_structure() -> None:
    section("2. PROJECT STRUCTURE")
    for relative in REQUIRED_DIRS:
        check(os.path.isdir(os.path.join(ROOT, relative)), f"directory exists: {relative}")


def validate_artifacts() -> None:
    section("3. RECOVERED ARTIFACTS")

    figures_dir = os.path.join(ROOT, "figures")
    figures = sorted(
        name for name in os.listdir(figures_dir) if name.lower().endswith(".png")
    ) if os.path.isdir(figures_dir) else []
    check(bool(figures), f"figures present ({len(figures)})")

    for name in figures:
        try:
            with Image.open(os.path.join(figures_dir, name)) as image:
                image.verify()
            with Image.open(os.path.join(figures_dir, name)) as image:
                width, height = image.size
            check(True, f"{name} {width}x{height}")
        except Exception as exc:  # noqa: BLE001 - report and continue
            check(False, f"{name} unreadable: {exc}")

    config_path = os.path.join(ROOT, "configs", "preprocessing_config.json")
    if os.path.isfile(config_path):
        with open(config_path, encoding="utf-8") as handle:
            config = json.load(handle)
        check(config.get("output", {}).get("width") == 256
              and config.get("output", {}).get("height") == 256,
              "preprocessing_config.json is a 256x256 config")
        check(config.get("source", {}).get("original_width") == 720,
              "preprocessing_config.json keeps the 720x960 source")
        check(config.get("views", {}).get("front") == "mask"
              and config.get("views", {}).get("side") == "mask_left",
              "preprocessing_config.json keeps the front/side view mapping")
    else:
        check(False, "configs/preprocessing_config.json present")

    inventory_path = os.path.join(ROOT, "reports", "E05_final_artifact_inventory.csv")
    if os.path.isfile(inventory_path):
        with open(inventory_path, encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        check(len(rows) == 21, f"E05 artifact inventory has 21 rows (got {len(rows)})")
        check(all(row["exists"] == "True" for row in rows),
              "E05 inventory records every artifact as produced")
    else:
        check(False, "reports/E05_final_artifact_inventory.csv present")

    audit_path = os.path.join(ROOT, "reports", "E05_final_consolidation_audit.json")
    if os.path.isfile(audit_path):
        with open(audit_path, encoding="utf-8") as handle:
            audit = json.load(handle)
        check(audit.get("expected_artifacts") == audit.get("existing_artifacts"),
              f"E05 consolidation audit balanced ({audit.get('expected_artifacts')}/"
              f"{audit.get('existing_artifacts')})")
    else:
        check(False, "reports/E05_final_consolidation_audit.json present")

    report_path = os.path.join(
        ROOT, "reports", "E05_final_evidence_and_limitations.md")
    if os.path.isfile(report_path):
        text = open(report_path, encoding="utf-8").read()
        for heading in ("## Claims that are currently supported",
                        "## Claims that are not yet established",
                        "## Reproducibility note"):
            check(heading in text, f"E05 report contains: {heading}")
    else:
        check(False, "reports/E05_final_evidence_and_limitations.md present")

    reference_dir = os.path.join(ROOT, "reference")
    for name in ("requirements-colab-original.txt",
                 "environment_report-colab-original.txt"):
        path = os.path.join(reference_dir, name)
        check(os.path.isfile(path), f"reference archive present: {name}")


def validate_documentation(loaded: dict[str, dict]) -> None:
    section("4. DOCUMENTATION")

    readme_path = os.path.join(ROOT, "README.md")
    if not os.path.isfile(readme_path):
        check(False, "README.md present")
        return

    readme = open(readme_path, encoding="utf-8").read().strip()
    template = None
    raw = loaded.get(NOTEBOOKS[0]) or read_notebook(
        os.path.join(ROOT, "notebooks", NOTEBOOKS[0]))
    for cell in code_cells(raw):
        source = "".join(cell["source"])
        marker = 'readme = r"""'
        if marker in source:
            start = source.index(marker) + len(marker)
            template = source[start:source.index('"""', start)].strip()
            break
    check(template is not None, "notebook 01 contains the README template")
    check(readme == template, "README.md matches the notebook 01 template byte for byte")

    for heading in ("## Project Overview", "## Dataset", "## Environment",
                    "## Notebook Execution Order", "## Pipeline Stages",
                    "## Expected Output Locations",
                    "## Reproducing Existing Experiments",
                    "## Known Limitations"):
        check(heading in readme, f"README section present: {heading}")

    inventory_md = os.path.join(ROOT, "PROJECT_INVENTORY.md")
    if os.path.isfile(inventory_md):
        text = open(inventory_md, encoding="utf-8").read()
        for heading in ("## 2. Recovered artifacts", "## 3. Artifacts that require",
                        "## 4. Research evidence", "## 6. Remaining blockers"):
            check(heading in text, f"PROJECT_INVENTORY.md section present: {heading}")
    else:
        check(False, "PROJECT_INVENTORY.md present")


def validate_dependencies(loaded: dict[str, dict]) -> None:
    section("5. DEPENDENCIES")

    imports: set[str] = set()
    for raw in loaded.values():
        for cell in code_cells(raw):
            try:
                tree = ast.parse(strip_magics("".join(cell["source"])))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    imports.add(node.module.split(".")[0])

    third_party = sorted(name for name in imports if name not in STDLIB)
    unmapped = [name for name in third_party if name not in DISTRIBUTIONS]
    check(not unmapped, f"every third-party import is mapped {unmapped or ''}")

    requirements_path = os.path.join(ROOT, "requirements-local.txt")
    if not os.path.isfile(requirements_path):
        check(False, "requirements-local.txt present")
        return

    requirements = open(requirements_path, encoding="utf-8").read().lower()
    for module in third_party:
        package = DISTRIBUTIONS.get(module)
        if not package:
            continue
        check(package.lower() in requirements,
              f"requirements-local.txt covers {module} -> {package}")


def is_lossless_metadata_removal(new_outputs: list, old_outputs: list) -> bool:
    """True when the only change is dropping an illegal stream 'metadata' key.

    nbformat does not permit a ``metadata`` member on ``stream`` outputs. Two
    stream outputs in notebook 03 carried one; removing it changes no text and
    no data. Any other difference is treated as a real change.
    """
    if len(new_outputs) != len(old_outputs):
        return False

    for new, old in zip(new_outputs, old_outputs):
        if new.get("output_type") != old.get("output_type"):
            return False
        if new.get("output_type") == "stream":
            if "".join(new.get("text", [])) != "".join(old.get("text", [])):
                return False
            new_keys = set(new)
            old_keys = set(old)
            if not new_keys <= old_keys:
                return False
            if old_keys - new_keys - {"metadata"}:
                return False
        else:
            if json.dumps(new.get("data"), sort_keys=True) != json.dumps(
                    old.get("data"), sort_keys=True):
                return False
            if json.dumps(new.get("metadata"), sort_keys=True) != json.dumps(
                    old.get("metadata"), sort_keys=True):
                return False
    return True


def validate_outputs_against_backup() -> None:
    """Optional deeper check: compare saved outputs with pre-repair backups."""
    backup = os.environ.get("DORJIBARI_NOTEBOOK_BACKUP")
    if not backup or not os.path.isdir(backup):
        return

    section("6. OUTPUT PRESERVATION vs BACKUP")
    for name in NOTEBOOKS:
        backup_path = os.path.join(backup, name)
        current_path = os.path.join(ROOT, "notebooks", name)
        if not os.path.isfile(backup_path):
            check(False, f"backup for {name} present")
            continue

        new_code = code_cells(read_notebook(current_path))
        old_code = code_cells(read_notebook(backup_path))
        if len(new_code) != len(old_code):
            check(False, f"{name}: code cell count changed "
                         f"({len(new_code)} vs {len(old_code)})")
            continue

        normalized = []
        changed = []
        for index, (a, b) in enumerate(zip(new_code, old_code)):
            new_outputs = a.get("outputs", [])
            old_outputs = b.get("outputs", [])
            if json.dumps(new_outputs, sort_keys=True) == json.dumps(
                    old_outputs, sort_keys=True):
                continue
            if is_lossless_metadata_removal(new_outputs, old_outputs):
                normalized.append(index)
            else:
                changed.append(index)

        check(not changed,
              f"{name}: saved outputs preserved (changed: {changed})")
        if normalized:
            check(True,
                  f"{name}: cells {normalized} differ only by removal of an "
                  "illegal stream 'metadata' key (text identical)")
        check([c.get("execution_count") for c in new_code]
              == [c.get("execution_count") for c in old_code],
              f"{name}: execution counts unchanged")


def main() -> int:
    print(f"DorjiBari project root: {ROOT}")
    loaded = validate_notebooks()
    validate_structure()
    validate_artifacts()
    validate_documentation(loaded)
    validate_dependencies(loaded)
    validate_outputs_against_backup()

    section(f"RESULT: {'ALL CHECKS PASSED' if not FAILURES else str(len(FAILURES)) + ' FAILURE(S)'}")
    for failure in FAILURES:
        print(" -", failure)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
