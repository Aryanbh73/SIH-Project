import pandas as pd
import numpy as np
from pathlib import Path

input_file = "data/processed/mps_anomaly_results.xlsx"
output_file = "data/processed/mps_explained_results.xlsx"

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

# Calculate median and standard deviation for comparison
medians = df[features].median()
stds = df[features].std()

def build_explanation(row):
    reasons = []

    # Utilization anomaly
    if row["utilization_percentage"] < medians["utilization_percentage"] - stds["utilization_percentage"]:
        reasons.append("Unusually low fund utilization")

    elif row["utilization_percentage"] > medians["utilization_percentage"] + stds["utilization_percentage"]:
        reasons.append("Unusually high fund utilization")


    # Completion anomaly
    if row["completion_rate"] < medians["completion_rate"] - stds["completion_rate"]:
        reasons.append("Completion rate significantly below typical records")

    elif row["completion_rate"] > medians["completion_rate"] + stds["completion_rate"]:
        reasons.append("Completion rate unusually high compared with peers")


    # Payment gap anomaly
    if row["payment_gap_percentage"] > medians["payment_gap_percentage"] + stds["payment_gap_percentage"]:
        reasons.append("Large payment gap compared with typical records")


    # Unspent funds
    if row["unspent_ratio"] > medians["unspent_ratio"] + stds["unspent_ratio"]:
        reasons.append("High proportion of allocated funds remains unspent")


    # Completion vs utilization mismatch
    if row["completion_utilization_gap"] > medians["completion_utilization_gap"] + stds["completion_utilization_gap"]:
        reasons.append("Large mismatch between fund utilization and work completion")


    # Work count anomaly
    if abs(row["work_count_gap"]) > abs(medians["work_count_gap"]) + stds["work_count_gap"]:
        reasons.append("Unusual gap between recommended and completed works")


    # Payment pressure
    if row["payment_pressure"] > medians["payment_pressure"] + stds["payment_pressure"]:
        reasons.append("High in-progress payment pressure relative to allocation")


    # Completed value
    if row["completed_value_ratio"] > medians["completed_value_ratio"] + stds["completed_value_ratio"]:
        reasons.append("Completed-work value unusually high relative to allocation")


    if not reasons:
        reasons.append("Unusual combination of multiple implementation indicators")

    return "; ".join(reasons)


df["anomaly_explanation"] = df.apply(
    build_explanation,
    axis=1
)

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

df.to_excel(
    output_file,
    index=False
)

print("\nExplainable anomaly analysis complete.")

print("\nTop 10 explained anomalies:\n")

columns = [
    "mp_name",
    "state",
    "constituency",
    "anomaly_score",
    "anomaly_level",
    "anomaly_explanation"
]

print(
    df[columns]
    .head(10)
    .to_string(index=False)
)

print(
    "\nResults saved to:",
    output_file
)