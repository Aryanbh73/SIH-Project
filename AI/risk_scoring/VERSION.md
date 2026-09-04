# Risk Engine Version

Current MVP Version: v2

Status: FROZEN

Do not change scoring weights or thresholds during backend/frontend development unless a documented validation issue is found.

Frozen components:

- Financial utilization: 25
- Completion: 25
- Payment gap: 20
- Utilization-completion mismatch: 15
- Isolation Forest contribution: 15

Total: 100

Risk levels:

- LOW: 0–39.99
- MEDIUM: 40–59.99
- HIGH: 60–79.99
- CRITICAL: 80–100