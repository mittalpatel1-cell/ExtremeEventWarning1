import requests
import pandas as pd
from io import StringIO
import os

url = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/oni/v6/"

response = requests.get(url, timeout=60)
response.raise_for_status()

tables = pd.read_html(StringIO(response.text))

print("Tables found:", len(tables))

all_oni_tables = []

for table in tables:

    if table.shape[1] != 13:
        continue

    years = pd.to_numeric(table.iloc[:, 0], errors="coerce")

    valid_years = years.between(1950, 2030).sum()

    if valid_years >= 3:

        table = table.copy()

        table.columns = [
            "Year",
            "DJF",
            "JFM",
            "FMA",
            "MAM",
            "AMJ",
            "MJJ",
            "JJA",
            "JAS",
            "ASO",
            "SON",
            "OND",
            "NDJ"
        ]

        table["Year"] = pd.to_numeric(table["Year"], errors="coerce")

        for column in table.columns[1:]:
            table[column] = pd.to_numeric(
                table[column],
                errors="coerce"
            )

        table = table.dropna(subset=["Year"])

        table["Year"] = table["Year"].astype(int)

        all_oni_tables.append(table)

if len(all_oni_tables) == 0:
    raise ValueError("NOAA ONI table could not be found.")

df = pd.concat(all_oni_tables, ignore_index=True)

df = df.drop_duplicates(subset=["Year"])

df = df[
    (df["Year"] >= 1997) &
    (df["Year"] <= 2023)
]

df = df.sort_values("Year")

os.makedirs("data/raw", exist_ok=True)

output_file = "data/raw/noaa_oni_1997_2023.csv"

df.to_csv(output_file, index=False)

print("\nNOAA ONI download successful")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nSaved to:")
print(output_file)