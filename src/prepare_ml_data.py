import pandas as pd
import os

input_file = "data/processed/final_climate_dataset.csv"
output_file = "data/processed/ml_ready_dataset.csv"

df = pd.read_csv(input_file)
df["DATE"] = pd.to_datetime(df["DATE"])

df = df.sort_values(["LOCATION", "DATE"]).reset_index(drop=True)

numeric_columns = [
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN"
]

for col in numeric_columns:
    df[col] = df.groupby("LOCATION")[col].transform(
        lambda x: x.interpolate(method="linear").bfill().ffill()
    )

df["ONI"] = df["ONI"].interpolate(method="linear").bfill().ffill()

df["YEAR"] = df["DATE"].dt.year
df["MONTH"] = df["DATE"].dt.month
df["DAY"] = df["DATE"].dt.day
df["DAY_OF_YEAR"] = df["DATE"].dt.dayofyear

os.makedirs("data/processed", exist_ok=True)

df.to_csv(output_file, index=False)

print("Shape:")
print(df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nColumns:")
print(df.columns.tolist())

print("\nSaved:")
print(output_file)