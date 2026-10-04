import pandas as pd
from pathlib import Path

nasa_noaa_file = Path("data/processed/combined_daily_data.csv")
imd_file = Path("data/raw/imd_temperature_1997_2023.csv")
output_file = Path("data/processed/final_climate_dataset.csv")

nasa = pd.read_csv(nasa_noaa_file)
imd = pd.read_csv(imd_file)

nasa["DATE"] = pd.to_datetime(nasa["DATE"])
imd["DATE"] = pd.to_datetime(imd["DATE"])

imd = imd[["DATE", "LOCATION", "TMAX"]]

final = pd.merge(
    nasa,
    imd,
    on=["DATE", "LOCATION"],
    how="left"
)

final = final.drop(columns=["T2M"])

columns = [
    "DATE",
    "LOCATION",
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI"
]

final = final[columns]

final = final.sort_values(["LOCATION", "DATE"])

final.to_csv(output_file, index=False)

print("First 5 rows:")
print(final.head())

print("\nShape:")
print(final.shape)

print("\nColumns:")
print(final.columns.tolist())

print("\nMissing values:")
print(final.isnull().sum())

print("\nDate range:")
print(final["DATE"].min())
print(final["DATE"].max())

print("\nLocations:")
print(final["LOCATION"].unique())

print("\nSaved:")
print(output_file)