from pathlib import Path
import numpy as np
import pandas as pd
import re

folder = Path("data/raw/imd_temperature")
output = Path("data/raw/imd_temperature_1997_2023.csv")

locations = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Guwahati": (26.1445, 91.7362),
    "Srinagar": (34.0837, 74.7973)
}

latitudes = np.arange(7.5, 38.0, 1.0)
longitudes = np.arange(67.5, 98.0, 1.0)

rows = []

files = sorted(folder.glob("Maxtemp_MaxT_*.GRD"))

print("Files found:", len(files))

for file in files:

    match = re.search(r"(\d{4})", file.name)

    if not match:
        continue

    year = int(match.group(1))

    days = 366 if year % 4 == 0 else 365

    data = np.fromfile(file, dtype=np.float32)

    expected = days * 31 * 31

    print(f"{year}: {len(data)} values, expected {expected}")

    if len(data) != expected:
        print(f"Skipping {year}: incorrect file size")
        continue

    data = data.reshape(days, 31, 31)

    dates = pd.date_range(
        start=f"{year}-01-01",
        periods=days,
        freq="D"
    )

    for city, (lat, lon) in locations.items():

        lat_index = np.abs(latitudes - lat).argmin()
        lon_index = np.abs(longitudes - lon).argmin()

        temperatures = data[:, lat_index, lon_index]

        for date, temperature in zip(dates, temperatures):

            rows.append({
                "DATE": date,
                "LOCATION": city,
                "TMAX": float(temperature)
            })

df = pd.DataFrame(rows)

df["DATE"] = pd.to_datetime(df["DATE"])

df.loc[df["TMAX"] >= 50, "TMAX"] = np.nan
df = df.dropna(subset=["TMAX"])

df = df.dropna(subset=["TMAX"])

df = df.sort_values(["LOCATION", "DATE"])

df.to_csv(output, index=False)

print("\nFirst 5 rows:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nDate range:")
print(df["DATE"].min())
print(df["DATE"].max())

print("\nLocations:")
print(df["LOCATION"].unique())

print("\nTemperature range:")
print(df["TMAX"].min(), "to", df["TMAX"].max())

print("\nSaved:")
print(output)