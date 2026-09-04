import pandas as pd

file_path = "data/processed/mps_clean.xlsx"

df = pd.read_excel(file_path)

print("\n--- BASIC RANGE CHECKS ---")

checks = {
    "utilization_percentage": (0, 200),
    "completion_rate": (0, 100),
    "payment_gap_percentage": (0, 100),
    "allocated_amount": (0, None),
    "total_expenditure": (0, None),
    "unspent_amount": (0, None),
    "completed_works_count": (0, None),
    "recommended_works_count": (0, None),
    "pending_works": (0, None),
}

for column, (minimum, maximum) in checks.items():
    invalid = df[df[column] < minimum]

    if maximum is not None:
        invalid = pd.concat([
            invalid,
            df[df[column] > maximum]
        ]).drop_duplicates()

    print(f"{column}: {len(invalid)} suspicious rows")


print("\n--- LOGICAL CONSISTENCY CHECKS ---")

# Completed works should usually not exceed recommended works
invalid_completed = df[
    df["completed_works_count"] > df["recommended_works_count"]
]

print(
    "Completed works > Recommended works:",
    len(invalid_completed)
)


# Pending works should ideally relate to recommended - completed
df["calculated_pending"] = (
    df["recommended_works_count"]
    - df["completed_works_count"]
)

pending_mismatch = df[
    df["pending_works"] != df["calculated_pending"]
]

print(
    "Pending works mismatch:",
    len(pending_mismatch)
)


# Expenditure greater than allocation
expenditure_over_allocation = df[
    df["total_expenditure"] > df["allocated_amount"]
]

print(
    "Total expenditure > Allocated amount:",
    len(expenditure_over_allocation)
)


# Check utilization percentage mathematically
df["calculated_utilization"] = (
    df["total_expenditure"]
    / df["allocated_amount"]
    * 100
)

utilization_difference = (
    df["utilization_percentage"]
    - df["calculated_utilization"]
).abs()

utilization_mismatch = df[
    utilization_difference > 1
]

print(
    "Utilization percentage mismatch > 1%:",
    len(utilization_mismatch)
)


print("\n--- SUMMARY STATISTICS ---")

columns_to_check = [
    "allocated_amount",
    "total_expenditure",
    "utilization_percentage",
    "completed_works_count",
    "recommended_works_count",
    "completion_rate",
    "pending_works",
    "unspent_amount",
    "payment_gap_percentage"
]

print(df[columns_to_check].describe())