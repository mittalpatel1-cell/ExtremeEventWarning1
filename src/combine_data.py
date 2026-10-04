import pandas as pd
import glob
import os

raw_path = "data/raw"

nasa_files = glob.glob(os.path.join(raw_path, "*_nasa_power.csv"))

all_nasa = []

for file in nasa_files:
    df = pd.read_csv(file)
    all_nasa.append(df)

nasa = pd.concat(all_nasa, ignore_index=True)

nasa["DATE"] = pd.to_datetime(
    nasa["YEAR"].astype(str) + nasa["DOY"].astype(str),
    format="%Y%j"
)

nasa = nasa.sort_values(["LOCATION", "DATE"])

oni = pd.read_csv(
    os.path.join(raw_path, "noaa_oni_1997_2023.csv")
)

season_months = {
    "DJF": 3,
    "JFM": 4,
    "FMA": 5,
    "MAM": 6,
    "AMJ": 7,
    "MJJ": 8,
    "JJA": 9,
    "JAS": 10,
    "ASO": 11,
    "SON": 12,
    "OND": 1,
    "NDJ": 2
}

oni_long = oni.melt(
    id_vars=["Year"],
    var_name="Season",
    value_name="ONI"
)

oni_long["Month"] = oni_long["Season"].map(season_months)

oni_long["Year_Adjusted"] = oni_long["Year"]

oni_long.loc[
    oni_long["Season"].isin(["OND", "NDJ"]),
    "Year_Adjusted"
] += 1

oni_long["DATE"] = pd.to_datetime(
    oni_long["Year_Adjusted"].astype(str)
    + "-"
    + oni_long["Month"].astype(str)
    + "-01"
)

oni_long = oni_long[["DATE", "ONI"]]

nasa["MONTH"] = nasa["DATE"].dt.to_period("M")
oni_long["MONTH"] = oni_long["DATE"].dt.to_period("M")

nasa = nasa.merge(
    oni_long[["MONTH", "ONI"]],
    on="MONTH",
    how="left"
)

nasa = nasa.drop(columns=["MONTH"])

nasa["ONI"] = nasa.groupby("LOCATION")["ONI"].ffill()

os.makedirs("data/processed", exist_ok=True)

output_file = "data/processed/combined_daily_data.csv"

nasa.to_csv(output_file, index=False)

print("Combined dataset created successfully")
print("Shape:", nasa.shape)

print("\nColumns:")
print(nasa.columns.tolist())

print("\nFirst 5 rows:")
print(nasa.head())

print("\nLast 5 rows:")
print(nasa.tail())

print("\nMissing values:")
print(nasa.isnull().sum())

print("\nONI statistics:")
print(nasa["ONI"].describe())

print("\nSaved to:")
print(output_file)