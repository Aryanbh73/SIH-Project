import pandas as pd
from pathlib import Path


input_file = "data/processed/mps_explained_results.xlsx"
output_file = "data/processed/mps_risk_results.xlsx"


df = pd.read_excel(input_file)


def calculate_risk(row):

    risk = 0
    reasons = []

    # -----------------------------------
    # 1. LOW UTILIZATION
    # -----------------------------------

    utilization = row["utilization_percentage"]

    if utilization < 25:
        risk += 25
        reasons.append("Very low fund utilization")

    elif utilization < 50:
        risk += 15
        reasons.append("Low fund utilization")


    # -----------------------------------
    # 2. LOW COMPLETION RATE
    # -----------------------------------

    completion = row["completion_rate"]

    if completion < 25:
        risk += 25
        reasons.append("Very low work completion rate")

    elif completion < 50:
        risk += 15
        reasons.append("Low work completion rate")


    # -----------------------------------
    # 3. HIGH PAYMENT GAP
    # -----------------------------------

    payment_gap = row["payment_gap_percentage"]

    if payment_gap > 75:
        risk += 20
        reasons.append("Very high payment gap")

    elif payment_gap > 50:
        risk += 12
        reasons.append("High payment gap")


    # -----------------------------------
    # 4. HIGH UNSPENT FUNDS
    # -----------------------------------

    unspent = row["unspent_ratio"]

    if unspent > 75:
        risk += 20
        reasons.append("Very high proportion of funds remains unspent")

    elif unspent > 50:
        risk += 12
        reasons.append("High proportion of funds remains unspent")


    # -----------------------------------
    # 5. UTILIZATION-COMPLETION MISMATCH
    # -----------------------------------

    mismatch = row["completion_utilization_gap"]

    if mismatch > 50:
        risk += 15
        reasons.append(
            "Large mismatch between fund utilization and work completion"
        )

    elif mismatch > 30:
        risk += 8
        reasons.append(
            "Moderate mismatch between fund utilization and work completion"
        )


    # -----------------------------------
    # 6. AI ANOMALY SUPPORT
    # -----------------------------------

    anomaly_score = row["anomaly_score"]

    # AI contributes only part of final risk.
    # It does NOT determine risk by itself.

    ai_component = anomaly_score * 0.20

    risk += ai_component


    # Maximum final score = 100

    risk = min(risk, 100)


    if not reasons:
        reasons.append(
            "No major rule-based risk indicators detected"
        )


    return pd.Series([
        round(risk, 2),
        "; ".join(reasons)
    ])


df[
    [
        "risk_score",
        "risk_reasons"
    ]
] = df.apply(
    calculate_risk,
    axis=1
)


def assign_risk_level(score):

    if score >= 80:
        return "CRITICAL"

    elif score >= 60:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


df["risk_level"] = df[
    "risk_score"
].apply(assign_risk_level)


# Sort highest-risk records first

df = df.sort_values(
    "risk_score",
    ascending=False
)


Path(
    "data/processed"
).mkdir(
    parents=True,
    exist_ok=True
)


df.to_excel(
    output_file,
    index=False
)


print("\nHybrid risk scoring complete.")

print("\nRisk distribution:")

print(
    df["risk_level"]
    .value_counts()
)


print("\nTop 10 highest-risk records:\n")

columns = [
    "mp_name",
    "state",
    "constituency",
    "anomaly_score",
    "risk_score",
    "risk_level",
    "utilization_percentage",
    "completion_rate",
    "payment_gap_percentage",
    "unspent_ratio",
    "risk_reasons"
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