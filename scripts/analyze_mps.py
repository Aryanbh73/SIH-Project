import json
from pathlib import Path
from collections import Counter


INPUT_FILE = Path("data/raw/mps_raw.json")


def main():
    print("Loading MPLADS data...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    records = data["data"]

    print(f"\nTotal records: {len(records)}")

    # -------------------------
    # 1. States
    # -------------------------
    states = sorted(set(record.get("state") for record in records))

    print(f"\nNumber of states: {len(states)}")
    print("States:")

    for state in states:
        print(f"- {state}")

    # -------------------------
    # 2. Houses
    # -------------------------
    houses = Counter(record.get("house") for record in records)

    print("\nRecords by House:")

    for house, count in houses.items():
        print(f"- {house}: {count}")

    # -------------------------
    # 3. Duplicate IDs
    # -------------------------
    ids = [record.get("id") for record in records]

    duplicate_ids = [
        item
        for item, count in Counter(ids).items()
        if count > 1
    ]

    print(f"\nDuplicate IDs: {len(duplicate_ids)}")

    if duplicate_ids:
        print("Duplicate ID values:")
        for item in duplicate_ids[:20]:
            print(f"- {item}")

    # -------------------------
    # 4. Missing values
    # -------------------------
    print("\nMissing values:")

    fields = records[0].keys()

    for field in fields:
        missing = sum(
            1
            for record in records
            if record.get(field) is None
            or record.get(field) == ""
        )

        print(f"- {field}: {missing}")

    # -------------------------
    # 5. Numeric ranges
    # -------------------------
    numeric_fields = [
        "allocatedAmount",
        "totalExpenditure",
        "utilizationPercentage",
        "completedWorksCount",
        "recommendedWorksCount",
        "completionRate",
        "pendingWorks",
        "unspentAmount",
        "completedWorksValue",
        "totalCompletedAmount",
        "inProgressPayments",
        "paymentGapPercentage",
    ]

    print("\nNumeric ranges:")

    for field in numeric_fields:

        values = []

        for record in records:
            value = record.get(field)

            if isinstance(value, (int, float)):
                values.append(value)

        if values:
            print(
                f"- {field}: "
                f"min={min(values)}, "
                f"max={max(values)}"
            )


if __name__ == "__main__":
    main()