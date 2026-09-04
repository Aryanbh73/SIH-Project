import pandas as pd
from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


input_file = "data/processed/mps_ai_ready.xlsx"
output_file = "data/processed/mps_anomaly_results.xlsx"


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


X = df[features].copy()


# Scale the data so features with large numeric ranges
# do not dominate the model.
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# Baseline Isolation Forest
model = IsolationForest(
    n_estimators=200,
    contamination=0.10,
    random_state=42
)

model.fit(X_scaled)


# Isolation Forest prediction:
#  1 = normal
# -1 = anomaly
predictions = model.predict(X_scaled)


# decision_function:
# larger value = more normal
# smaller value = more anomalous
raw_scores = model.decision_function(X_scaled)


df["anomaly_prediction"] = predictions
df["raw_anomaly_score"] = raw_scores


# Convert the model score into an easier 0-100 risk-like scale.
# Lowest model score becomes approximately 100.
minimum = raw_scores.min()
maximum = raw_scores.max()

df["anomaly_score"] = (
    (maximum - raw_scores)
    / (maximum - minimum)
    * 100
).round(2)


def risk_level(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


df["anomaly_level"] = df["anomaly_score"].apply(risk_level)


# Sort the most unusual records first
df = df.sort_values(
    by="anomaly_score",
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


print("\nIsolation Forest completed.")

print("Total records:", len(df))

print(
    "Model anomalies:",
    (df["anomaly_prediction"] == -1).sum()
)

print("\nAnomaly level distribution:")
print(df["anomaly_level"].value_counts())

print("\nTop 10 most anomalous MPs/constituencies:")

columns_to_show = [
    "mp_name",
    "state",
    "constituency",
    "anomaly_score",
    "anomaly_level",
    "utilization_percentage",
    "completion_rate",
    "payment_gap_percentage",
    "unspent_ratio",
    "completion_utilization_gap"
]

print(
    df[columns_to_show]
    .head(10)
    .to_string(index=False)
)

print(
    "\nResults saved to:",
    output_file
)