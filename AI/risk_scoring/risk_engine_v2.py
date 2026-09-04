import pandas as pd
from pathlib import Path

input_file = "data/processed/mps_explained_results.xlsx"
output_file = "data/processed/mps_risk_results_v2.xlsx"

df = pd.read_excel(input_file)


def clamp(value, minimum=0, maximum=1):
    return max(minimum, min(value, maximum))


def calculate_risk(row):

    reasons = []

    # ------------------------------------------------
    # 1. FINANCIAL UTILIZATION COMPONENT - MAX 25
    # ------------------------------------------------
    # Do NOT separately add unspent_ratio because
    # unspent and utilization contain highly
    # overlapping information.

    utilization = row["utilization_percentage"]

    if utilization < 50:
        financial_score = clamp(
            (50 - utilization) / 50
        ) * 25
    else:
        financial_score = 0

    if utilization < 25:
        reasons.append("Very low fund utilization")
    elif utilization < 50:
        reasons.append("Below-average fund utilization")


    # ------------------------------------------------
    # 2. WORK COMPLETION COMPONENT - MAX 25
    # ------------------------------------------------

    completion = row["completion_rate"]

    if completion < 50:
        completion_score = clamp(
            (50 - completion) / 50
        ) * 25
    else:
        completion_score = 0

    if completion < 25:
        reasons.append("Very low work completion rate")
    elif completion < 50:
        reasons.append("Low work completion rate")


    # ------------------------------------------------
    # 3. PAYMENT GAP COMPONENT - MAX 20
    # ------------------------------------------------

    payment_gap = max(
        row["payment_gap_percentage"],
        0
    )

    payment_score = clamp(
        payment_gap / 100
    ) * 20

    if payment_gap > 75:
        reasons.append("Very high payment gap")
    elif payment_gap > 50:
        reasons.append("High payment gap")


    # ------------------------------------------------
    # 4. COMPLETION / UTILIZATION MISMATCH - MAX 15
    # ------------------------------------------------

    mismatch = row["completion_utilization_gap"]

    mismatch_score = clamp(
        mismatch / 70
    ) * 15

    if mismatch > 50:
        reasons.append(
            "Large mismatch between utilization and completion"
        )
    elif mismatch > 30:
        reasons.append(
            "Moderate mismatch between utilization and completion"
        )


    # ------------------------------------------------
    # 5. AI ANOMALY COMPONENT - MAX 15
    # ------------------------------------------------

    anomaly_score = row["anomaly_score"]

    ai_score = (
        anomaly_score / 100
    ) * 15


    # ------------------------------------------------
    # FINAL SCORE
    # ------------------------------------------------

    final_score = (
        financial_score
        + completion_score
        + payment_score
        + mismatch_score
        + ai_score
    )

    final_score = min(
        round(final_score, 2),
        100
    )

    if not reasons:
        reasons.append(
            "No major implementation-risk indicators detected"
        )

    return pd.Series([
        round(financial_score, 2),
        round(completion_score, 2),
        round(payment_score, 2),
        round(mismatch_score, 2),
        round(ai_score, 2),
        final_score,
        "; ".join(reasons)
    ])


columns = [
    "financial_risk_component",
    "completion_risk_component",
    "payment_risk_component",
    "mismatch_risk_component",
    "ai_risk_component",
    "risk_score_v2",
    "risk_reasons_v2"
]


df[columns] = df.apply(
    calculate_risk,
    axis=1
)


def risk_level(score):

    if score >= 80:
        return "CRITICAL"

    elif score >= 60:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


df["risk_level_v2"] = (
    df["risk_score_v2"]
    .apply(risk_level)
)


df = df.sort_values(
    "risk_score_v2",
    ascending=False
)


Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)


df.to_excel(
    output_file,
    index=False
)


print("\nRisk Engine V2 complete.")

print("\nRisk distribution:")

print(
    df["risk_level_v2"]
    .value_counts()
)


print("\nRisk score statistics:")

print(
    df["risk_score_v2"]
    .describe()
)


print("\nTop 10 review-priority records:\n")

show_columns = [
    "mp_name",
    "state",
    "constituency",
    "anomaly_score",
    "risk_score_v2",
    "risk_level_v2",
    "financial_risk_component",
    "completion_risk_component",
    "payment_risk_component",
    "mismatch_risk_component",
    "ai_risk_component",
    "risk_reasons_v2"
]

print(
    df[show_columns]
    .head(10)
    .to_string(index=False)
)

print(
    "\nResults saved to:",
    output_file
)