import pandas as pd
from pathlib import Path

input_file = "data/processed/mps_clean.xlsx"
output_file = "data/processed/mps_features.xlsx"

df = pd.read_excel(input_file)

# Avoid division-by-zero problems
safe_allocated = df["allocated_amount"].replace(0, pd.NA)
safe_recommended = df["recommended_works_count"].replace(0, pd.NA)

# 1. Unspent ratio
df["unspent_ratio"] = (
    df["unspent_amount"] / safe_allocated
) * 100

# 2. Pending work ratio
df["pending_work_ratio"] = (
    df["pending_works"] / safe_recommended
) * 100

# 3. Completed work ratio
df["completed_work_ratio"] = (
    df["completed_works_count"] / safe_recommended
) * 100

# 4. Expenditure ratio
df["expenditure_ratio"] = (
    df["total_expenditure"] / safe_allocated
) * 100

# 5. Completion-utilization gap
# High value can indicate high spending with relatively low completion,
# or completion not aligned with expenditure.
df["completion_utilization_gap"] = (
    df["utilization_percentage"]
    - df["completion_rate"]
).abs()

# 6. Uncompleted works count
df["work_count_gap"] = (
    df["recommended_works_count"]
    - df["completed_works_count"]
)

# 7. Payment pressure indicator
df["payment_pressure"] = (
    df["in_progress_payment"] / safe_allocated
) * 100

# 8. Completed value ratio
df["completed_value_ratio"] = (
    df["completed_works_value"] / safe_allocated
) * 100

# Replace infinite values
df = df.replace([float("inf"), float("-inf")], pd.NA)

# Save feature-engineered dataset
Path("data/processed").mkdir(parents=True, exist_ok=True)
df.to_excel(output_file, index=False)

print("\nFeature engineering complete.")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nNew feature columns:")
new_features = [
    "unspent_ratio",
    "pending_work_ratio",
    "completed_work_ratio",
    "expenditure_ratio",
    "completion_utilization_gap",
    "work_count_gap",
    "payment_pressure",
    "completed_value_ratio",
]

for feature in new_features:
    print(feature)

print("\nMissing values in new features:")
print(df[new_features].isnull().sum())

print("\nFeature summary:")
print(df[new_features].describe())