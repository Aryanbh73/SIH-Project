import pandas as pd
from pathlib import Path

file_path = "data/processed/mps_clean.xlsx"

df = pd.read_excel(file_path)

output_dir = Path("data/validation")
output_dir.mkdir(parents=True, exist_ok=True)

numeric_columns = [
    "allocated_amount",
    "total_expenditure",
    "utilization_percentage",
    "completed_works_count",
    "recommended_works_count",
    "completion_rate",
    "pending_works",
    "unspent_amount",
    "completed_works_value",
    "total_completed_amount",
    "in_progress_payment",
    "payment_gap_percentage"
]

# -------------------------------------------------
# 1. Find rows containing missing numeric values
# -------------------------------------------------

missing_numeric = df[
    df[numeric_columns].isna().any(axis=1)
]

print("\n--- ROWS WITH MISSING NUMERIC VALUES ---")
print(missing_numeric)

missing_numeric.to_excel(
    output_dir / "missing_numeric_rows.xlsx",
    index=False
)

# -------------------------------------------------
# 2. Completed works > recommended works
# -------------------------------------------------

completed_over_recommended = df[
    df["completed_works_count"] >
    df["recommended_works_count"]
]

print(
    "\nCompleted > Recommended:",
    len(completed_over_recommended)
)

completed_over_recommended.to_excel(
    output_dir / "completed_over_recommended.xlsx",
    index=False
)

# -------------------------------------------------
# 3. Negative pending works
# -------------------------------------------------

negative_pending = df[
    df["pending_works"] < 0
]

print(
    "Negative pending works:",
    len(negative_pending)
)

negative_pending.to_excel(
    output_dir / "negative_pending_works.xlsx",
    index=False
)

# -------------------------------------------------
# 4. Pending calculation mismatch
# -------------------------------------------------

df["calculated_pending"] = (
    df["recommended_works_count"]
    - df["completed_works_count"]
)

pending_mismatch = df[
    (df["pending_works"] - df["calculated_pending"]).abs() > 0.01
]

print(
    "Pending calculation mismatch:",
    len(pending_mismatch)
)

pending_mismatch.to_excel(
    output_dir / "pending_mismatch.xlsx",
    index=False
)

# -------------------------------------------------
# 5. Negative payment gap
# -------------------------------------------------

negative_payment_gap = df[
    df["payment_gap_percentage"] < 0
]

print(
    "Negative payment gap:",
    len(negative_payment_gap)
)

negative_payment_gap.to_excel(
    output_dir / "negative_payment_gap.xlsx",
    index=False
)

# -------------------------------------------------
# 6. Show examples
# -------------------------------------------------

print("\n--- EXAMPLE: COMPLETED > RECOMMENDED ---")

print(
    completed_over_recommended[
        [
            "mp_name",
            "state",
            "constituency",
            "recommended_works_count",
            "completed_works_count",
            "pending_works"
        ]
    ].head(10)
)

print("\n--- NEGATIVE PAYMENT GAP RECORD ---")

print(
    negative_payment_gap[
        [
            "mp_name",
            "state",
            "constituency",
            "allocated_amount",
            "total_expenditure",
            "in_progress_payment",
            "payment_gap_percentage"
        ]
    ]
)

print("\nInvestigation files saved in data/validation/")