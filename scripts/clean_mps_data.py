import pandas as pd
from pathlib import Path

# -----------------------------
# 1. Load raw dataset
# -----------------------------
input_file = "data/raw/mps_raw.xlsx"
output_file = "data/processed/mps_clean.xlsx"

df = pd.read_excel(input_file)

print("Original shape:", df.shape)

# -----------------------------
# 2. Standardize column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -----------------------------
# 3. Define numeric columns
# -----------------------------
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

# -----------------------------
# 4. Convert numeric columns
# -----------------------------
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# -----------------------------
# 5. Check if conversion created missing values
# -----------------------------
print("\nMissing values after numeric conversion:")
print(df[numeric_columns].isnull().sum())

# -----------------------------
# 6. Remove exact duplicates
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# 7. Create processed directory
# -----------------------------
Path("data/processed").mkdir(parents=True, exist_ok=True)

# -----------------------------
# 8. Save cleaned dataset
# -----------------------------
df.to_excel(output_file, index=False)

print("\nClean dataset saved successfully.")
print("Final shape:", df.shape)

print("\nData types:")
print(df.dtypes)