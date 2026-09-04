# MPLADS Risk Scoring Engine

## Version

MVP Risk Engine Version: v2

Status: FROZEN FOR MVP

## Purpose

The risk engine prioritizes MPLADS MP/constituency-level records for review.

It does not determine or prove fraud.

The system combines:

1. Rule-based implementation indicators
2. Statistical anomaly detection using Isolation Forest

## Final Risk Score

The final score ranges from 0 to 100.

### 1. Fund Utilization Risk

Maximum: 25 points

Low utilization increases the review score.

This component measures whether allocated funds are being utilized at comparatively low levels.

### 2. Work Completion Risk

Maximum: 25 points

Low completion rates increase the review score.

This indicates possible implementation inefficiency or incomplete execution.

### 3. Payment Gap Risk

Maximum: 20 points

Higher payment-gap percentages increase the review score.

### 4. Utilization-Completion Mismatch

Maximum: 15 points

A large difference between utilization percentage and completion rate may indicate an implementation mismatch requiring review.

### 5. AI Anomaly Contribution

Maximum: 15 points

Isolation Forest produces an anomaly score based on unusual combinations of implementation indicators.

The anomaly model does not determine risk independently.

## Risk Classification

| Score | Level |
|---|---|
| 0–39.99 | LOW |
| 40–59.99 | MEDIUM |
| 60–79.99 | HIGH |
| 80–100 | CRITICAL |

## AI Model

Algorithm:

Isolation Forest

Reason:

The available dataset does not contain verified labels such as:

- Fraud
- Non-fraud

Therefore, supervised fraud classification is not used in the MVP.

Isolation Forest identifies records that differ significantly from typical implementation patterns.

## Important Distinction

Anomaly does not mean fraud.

A statistically unusual record may be:

- a legitimate exceptional case
- a newly initiated implementation cycle
- a data-quality issue
- an unusual but valid implementation pattern
- a record requiring administrative review

Therefore the platform uses the terminology:

"Flagged for review"

rather than:

"Fraud detected"

## Dataset Level

The current MVP dataset contains MP/constituency-level summary information.

Therefore, this risk engine currently performs:

MP/constituency-level implementation risk prioritization.

It does not yet perform:

- contractor fraud detection
- individual project-level fraud classification
- vendor-network analysis
- project-delay prediction
- exact project-location anomaly detection

These require additional verified datasets.

## Current Input Features

The MVP uses indicators derived from:

- utilization percentage
- completion rate
- payment gap percentage
- unspent funds
- recommended works
- completed works
- in-progress payment
- completed works value

Feature engineering also produces:

- unspent ratio
- pending work ratio
- completed work ratio
- expenditure ratio
- completion-utilization gap
- work count gap
- payment pressure
- completed value ratio

## Limitations

The scoring thresholds are prototype heuristics.

They are not official MPLADS audit thresholds.

Future versions should calibrate the thresholds using:

- official MPLADS rules
- historical audit findings
- expert validation
- project age
- tenure information
- project-level data

## Frozen MVP Files

AI anomaly model:

ai/anomaly_detection/isolation_forest.py

Anomaly explanation:

ai/anomaly_detection/explain_anomalies.py

Risk scoring engine:

ai/risk_scoring/risk_engine_v2.py

Final output:

data/processed/mps_risk_results_v2.xlsx