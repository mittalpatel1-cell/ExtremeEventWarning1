import requests
import pandas as pd
import os
import time

locations = {
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "kolkata": (22.5726, 88.3639),
    "chennai": (13.0827, 80.2707),
    "bengaluru": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "ahmedabad": (23.0225, 72.5714),
    "pune": (18.5204, 73.8567),
    "jaipur": (26.9124, 75.7873),
    "lucknow": (26.8467, 80.9462),
    "guwahati": (26.1445, 91.7362),
    "srinagar": (34.0837, 74.7973)
}

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

parameters = "T2M,RH2M,PRECTOTCORR,WS10M,PS,ALLSKY_SFC_SW_DWN"

os.makedirs("data/raw", exist_ok=True)

for city, (latitude, longitude) in locations.items():

    print(f"\nDownloading {city.title()}...")

    params = {
        "parameters": parameters,
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": "19970101",
        "end": "20231231",
        "format": "CSV"
    }

    try:
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()

        lines = response.text.splitlines()

        header_index = None

        for i, line in enumerate(lines):
            if line.startswith("YEAR") or line.startswith("PARAMETER"):
                header_index = i
                break

        if header_index is None:
            print(f"Could not find CSV header for {city}")
            continue

        csv_data = "\n".join(lines[header_index:])

        df = pd.read_csv(pd.io.common.StringIO(csv_data))

        df["LOCATION"] = city.title()

        filename = f"data/raw/{city}_nasa_power.csv"

        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")

    except Exception as e:
        print(f"Error downloading {city}: {e}")

    time.sleep(1)

print("\nAll downloads completed.")