import pandas as pd
import os

input_file = "data/processed/ml_ready_dataset.csv"
output_file = "data/processed/event_labeled_dataset.csv"

df = pd.read_csv(input_file)
df["DATE"] = pd.to_datetime(df["DATE"])

df = df.sort_values(["LOCATION", "DATE"]).reset_index(drop=True)

df["TMAX_90"] = df.groupby("LOCATION")["TMAX"].transform(
    lambda x: x.quantile(0.90)
)

df["RAIN_20"] = df.groupby("LOCATION")["PRECTOTCORR"].transform(
    lambda x: x.quantile(0.20)
)

df["RH_20"] = df.groupby("LOCATION")["RH2M"].transform(
    lambda x: x.quantile(0.20)
)

df["heatwave_day"] = (
    df["TMAX"] >= df["TMAX_90"]
).astype(int)

df["dry_day"] = (
    (df["PRECTOTCORR"] <= df["RAIN_20"]) &
    (df["RH2M"] <= df["RH_20"])
).astype(int)

df["compound_event"] = (
    (df["heatwave_day"] == 1) &
    (df["dry_day"] == 1)
).astype(int)

df["TMAX_7D"] = df.groupby("LOCATION")["TMAX"].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
)

df["RAIN_7D"] = df.groupby("LOCATION")["PRECTOTCORR"].transform(
    lambda x: x.rolling(7, min_periods=1).sum()
)

df["RH_7D"] = df.groupby("LOCATION")["RH2M"].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
)

df["heatwave_7d_ahead"] = df.groupby("LOCATION")["heatwave_day"].shift(-7)
df["drought_7d_ahead"] = df.groupby("LOCATION")["dry_day"].shift(-7)
df["compound_7d_ahead"] = df.groupby("LOCATION")["compound_event"].shift(-7)

df = df.dropna(
    subset=[
        "heatwave_7d_ahead",
        "drought_7d_ahead",
        "compound_7d_ahead"
    ]
)

df["heatwave_7d_ahead"] = df["heatwave_7d_ahead"].astype(int)
df["drought_7d_ahead"] = df["drought_7d_ahead"].astype(int)
df["compound_7d_ahead"] = df["compound_7d_ahead"].astype(int)

os.makedirs("data/processed", exist_ok=True)

df.to_csv(output_file, index=False)

print("Shape:")
print(df.shape)

print("\n7-Day Ahead Heatwave Events:")
print(df["heatwave_7d_ahead"].sum())

print("\n7-Day Ahead Drought Events:")
print(df["drought_7d_ahead"].sum())

print("\n7-Day Ahead Compound Events:")
print(df["compound_7d_ahead"].sum())

print("\nColumns:")
print(df.columns.tolist())

print("\nSaved:")
print(output_file)