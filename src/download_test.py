import requests
import pandas as pd
from io import StringIO

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "T2M,RH2M,PRECTOTCORR,WS10M,PS,ALLSKY_SFC_SW_DWN",
    "community": "AG",
    "longitude": 72.8777,
    "latitude": 19.0760,
    "start": "19970101",
    "end": "20231231",
    "format": "CSV"
}

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

lines = response.text.splitlines()

header_index = None

for i, line in enumerate(lines):
    if line.startswith("YEAR") or line.startswith("PARAMETER"):
        header_index = i
        break

if header_index is None:
    print("Could not find CSV header.")
    print(response.text[:2000])
    raise SystemExit

csv_data = "\n".join(lines[header_index:])

df = pd.read_csv(StringIO(csv_data))

df.to_csv("data/raw/mumbai_nasa_power.csv", index=False)

print("Download successful")
print("Rows:", len(df))
print("Columns:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())