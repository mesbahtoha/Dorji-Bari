
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

INPUT_FILE = (
    ROOT / "experiments" / "predictions"
    / "E04_classical_ml_predictions.csv"
)

OUTPUT_FILE = (
    ROOT / "reports" / "testb_overlap_sensitivity.csv"
)

SHARED_SUBJECT_ID = (
    "TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ"
)

EXPECTED_TARGETS = [
    "chest",
    "waist",
    "hip",
    "shoulder-breadth",
    "arm-length",
]

EXPECTED_SUBJECTS = 400


# --------------------------------------------------
# Metric calculation
# --------------------------------------------------

def calculate_metrics(df):

    actual = df["actual"].to_numpy(dtype=float)
    predicted = df["predicted"].to_numpy(dtype=float)

    return {
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": np.sqrt(mean_squared_error(actual, predicted)),
        "R2": r2_score(actual, predicted),
    }


# --------------------------------------------------
# Main analysis
# --------------------------------------------------

def main():

    print("\nDORJIBARI - TESTB OVERLAP SENSITIVITY")
    print("=" * 55)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "model",
        "target",
        "split",
        "subject_id",
        "actual",
        "predicted",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Select existing Ridge TestB predictions
    testb = df[
        (df["model"] == "Ridge") &
        (df["split"] == "testB")
    ].copy()

    if set(testb["target"].unique()) != set(EXPECTED_TARGETS):
        raise ValueError("Unexpected target names in TestB.")

    if testb["subject_id"].isna().any():
        raise ValueError("Missing subject IDs detected.")

    testb["actual"] = pd.to_numeric(
        testb["actual"], errors="coerce"
    )

    testb["predicted"] = pd.to_numeric(
        testb["predicted"], errors="coerce"
    )

    if not np.isfinite(
        testb[["actual", "predicted"]].to_numpy(dtype=float)
    ).all():
        raise ValueError("Non-finite actual/predicted values found.")

    # Check duplicate subject-target records
    duplicates = testb.duplicated(
        subset=["target", "subject_id"]
    )

    if duplicates.any():
        raise ValueError("Duplicate subject-target records found.")

    results = []

    for target in EXPECTED_TARGETS:

        group = testb[
            testb["target"] == target
        ].copy()

        unique_count = group["subject_id"].nunique()

        if len(group) != EXPECTED_SUBJECTS:
            raise ValueError(
                f"{target}: Expected 400 rows, found {len(group)}"
            )

        if unique_count != EXPECTED_SUBJECTS:
            raise ValueError(
                f"{target}: Expected 400 unique subjects."
            )

        if SHARED_SUBJECT_ID not in set(group["subject_id"]):
            raise ValueError(
                f"{target}: Shared subject not found."
            )

        # Primary official TestB: 400 subjects
        primary = calculate_metrics(group)

        # Supplementary TestB: 399 subjects
        supplementary_df = group[
            group["subject_id"] != SHARED_SUBJECT_ID
        ].copy()

        if len(supplementary_df) != 399:
            raise ValueError(
                f"{target}: Expected 399 supplementary rows."
            )

        supplementary = calculate_metrics(supplementary_df)

        results.append({
            "target": target,
            "official_subjects": 400,
            "sensitivity_subjects": 399,
            "official_MAE": primary["MAE"],
            "sensitivity_MAE": supplementary["MAE"],
            "delta_MAE": supplementary["MAE"] - primary["MAE"],
            "official_RMSE": primary["RMSE"],
            "sensitivity_RMSE": supplementary["RMSE"],
            "delta_RMSE": supplementary["RMSE"] - primary["RMSE"],
            "official_R2": primary["R2"],
            "sensitivity_R2": supplementary["R2"],
            "delta_R2": supplementary["R2"] - primary["R2"],
        })

    # Save supplementary results only
    result_df = pd.DataFrame(results)

    OUTPUT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\nVALIDATION PASSED")
    print("-" * 55)

    print(result_df.to_string(index=False, float_format=lambda x: f"{x:.5f}"))

    print("\nOutput saved:")
    print(OUTPUT_FILE)

    print("\nOriginal prediction file was not modified.")
    print("No model retraining was performed.")
    print("Official TestB results remain unchanged.")

    print("\nSENSITIVITY ANALYSIS COMPLETED")


if __name__ == "__main__":
    main()
