import json
from pathlib import Path


INPUT_FILE = Path("data/raw/mps_raw.json")


def main():
    print("Reading MPLADS data...")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    print("\nData loaded successfully!")
    print("\nTop-level structure:")
    print(type(data))

    if isinstance(data, dict):
        print("\nTop-level keys:")
        for key in data.keys():
            print(f"- {key}")

    if isinstance(data, dict) and "data" in data:
        records = data["data"]

        print(f"\nNumber of records: {len(records)}")

        if records:
            print("\nFields in first record:")

            for field in records[0].keys():
                print(f"- {field}")

            print("\nFirst record:")
            print(json.dumps(records[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()