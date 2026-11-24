
import json
from pathlib import Path

path = Path(
    r"D:\DorjiBari-Research\notebooks\03_Dataset_Preprocessing.ipynb"
)

with open(path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print("=" * 75)
print("NOTEBOOK 03 FINAL CELL STRUCTURE")
print("=" * 75)

for i, cell in enumerate(nb["cells"]):
    if i >= 75:
        source = "".join(cell.get("source", []))
        outputs = cell.get("outputs", [])

        print(f"\nIndex: {i}")
        print("Type:", cell.get("cell_type"))
        print("Execution count:", cell.get("execution_count"))
        print("Source length:", len(source.strip()))
        print("Output count:", len(outputs))

        if source.strip():
            print("Source preview:", source[:300])

print("\nTotal cells:", len(nb["cells"]))
print("CHECK COMPLETE")
