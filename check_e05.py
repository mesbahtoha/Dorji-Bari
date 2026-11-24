
import pandas as pd
from pathlib import Path

ROOT = Path(r"D:\DorjiBari-Research")

inventory_path = ROOT / "reports" / "E05_final_artifact_inventory.csv"

df = pd.read_csv(inventory_path)

print("=" * 75)
print("E05 EXPECTED ARTIFACT VERIFICATION")
print("=" * 75)

print("\nInventory columns:")
print(df.columns.tolist())

print("\nExpected artifact records:")
print("Total:", len(df))

for _, row in df.iterrows():
    print(row.to_dict())

print("\n" + "=" * 75)
print("ACTUAL E05-RELATED FILES")
print("=" * 75)

for folder in ["experiments", "checkpoints", "reports", "configs"]:
    base = ROOT / folder

    for path in base.rglob("*"):
        if path.is_file() and "E05" in path.name.upper():
            print(path.relative_to(ROOT))
