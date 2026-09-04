import pandas as pd
from pathlib import Path

input_file = "data/processed/mps_features.xlsx"
output_file = "data/processed/mps_ai_ready.xlsx"

df = pd.read_excel(input_file)

features = [
    "utilization_percentage",
    "completion_rate",
    "payment_gap_percentage",
    "unspent_ratio",
    "pending_work_ratio",
    "completed_work_ratio",
    "expenditure_ratio",
    "completion_utilization_gap",
    "work_count_gap",
    "payment_pressure",
    "completed_value_ratio"
]

print("\n--- MISSING VALUES BEFORE PREPARATION ---")
print(df[features].isnull().sum())

# Fill missing feature values with column medians
for feature in features:
    median_value = df[feature].median()
    df[feature] = df[feature].fillna(median_value)

print("\n--- MISSING VALUES AFTER PREPARATION ---")
print(df[features].isnull().sum())

Path("data/processed").mkdir(parents=True, exist_ok=True)

df.to_excel(output_file, index=False)

print("\nAI-ready dataset created.")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Saved to:", output_file)