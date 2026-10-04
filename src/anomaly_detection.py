import pandas as pd
import numpy as np
import os

input_file = "data/processed/event_labeled_dataset.csv"
output_file = "results/multivariate_anomaly_results.csv"

df = pd.read_csv(input_file)

df["DATE"] = pd.to_datetime(df["DATE"])

features = [
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI"
]

train_df = df[df["YEAR"] <= 2019].copy()
test_df = df[df["YEAR"] >= 2020].copy()

means = train_df.groupby("LOCATION")[features].mean()
stds = train_df.groupby("LOCATION")[features].std()

scores = []

for _, row in test_df.iterrows():

    location = row["LOCATION"]

    mean_values = means.loc[location]
    std_values = stds.loc[location]

    z_scores = (
        (row[features] - mean_values) / std_values
    ).abs()

    anomaly_score = z_scores.mean()

    scores.append(anomaly_score)

test_df["Anomaly_Score"] = scores

test_df["Anomaly_Level"] = test_df["Anomaly_Score"].apply(
    lambda x: "EXTREME ANOMALY" if x >= 2.0
    else "UNUSUAL" if x >= 1.5
    else "NORMAL"
)

output = test_df[
    [
        "DATE",
        "LOCATION",
        "TMAX",
        "RH2M",
        "PRECTOTCORR",
        "WS10M",
        "PS",
        "ALLSKY_SFC_SW_DWN",
        "ONI",
        "Anomaly_Score",
        "Anomaly_Level"
    ]
]

os.makedirs("results", exist_ok=True)

output.to_csv(
    output_file,
    index=False
)

print("Multivariate anomaly detection completed.")

print("\nAnomaly counts:")
print(output["Anomaly_Level"].value_counts())

print("\nAverage anomaly score:")
print(round(output["Anomaly_Score"].mean(), 3))

print("\nHighest anomalies:")
print(
    output.sort_values(
        "Anomaly_Score",
        ascending=False
    ).head(20).to_string(index=False)
)

print("\nSaved:")
print(output_file)