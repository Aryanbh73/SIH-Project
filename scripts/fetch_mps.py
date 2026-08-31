import requests
import json
from pathlib import Path

URL = "https://api.empoweredindian.in/api/summary/mps?page=1&limit=800"

OUTPUT_FILE = Path("data/raw/mps_raw.json")


def main():
    print("Downloading MPLADS data...")

    response = requests.get(URL, timeout=30)

    response.raise_for_status()

    data = response.json()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print("Download successful!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()