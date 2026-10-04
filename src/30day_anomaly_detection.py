import pandas as pd
import numpy as np
import os

input_file = "data/processed/event_labeled_dataset.csv"
output_file = "results/30day_pattern_anomaly_results.csv"

df = pd.read_csv(input_file)

df["DATE"] = pd.to_datetime(df["DATE"])

df = df.sort_values(
    ["LOCATION", "DATE"]
).reset_index(drop=True)

features = [
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI"
]

for feature in features:

    df[f"{feature}_30D"] = (
        df.groupby("LOCATION")[feature]
        .transform(
            lambda x: x.rolling(
                30,
                min_periods=30
            ).mean()
        )
    )

train_df = df[df["YEAR"] <= 2019].copy()

test_df = df[df["YEAR"] >= 2020].copy()

profile_features = [
    f"{feature}_30D"
    for feature in features
]

means = train_df.groupby("LOCATION")[
    profile_features
].mean()

stds = train_df.groupby("LOCATION")[
    profile_features
].std()

scores = []

for _, row in test_df.iterrows():

    location = row["LOCATION"]

    mean_values = means.loc[location]
    std_values = stds.loc[location]

    values = row[profile_features]

    z_scores = (
        (values - mean_values) / std_values
    ).abs()

    anomaly_score = z_scores.mean()

    scores.append(anomaly_score)

test_df["30Day_Anomaly_Score"] = scores

test_df["30Day_Anomaly_Level"] = (
    test_df["30Day_Anomaly_Score"].apply(
        lambda x:
        "EXTREME ANOMALY" if x >= 2.0
        else "UNUSUAL" if x >= 1.5
        else "NORMAL"
    )
)

output = test_df[
    [
        "DATE",
        "LOCATION",
        "TMAX_30D",
        "RH2M_30D",
        "PRECTOTCORR_30D",
        "WS10M_30D",
        "PS_30D",
        "ALLSKY_SFC_SW_DWN_30D",
        "ONI_30D",
        "30Day_Anomaly_Score",
        "30Day_Anomaly_Level"
    ]
]

os.makedirs("results", exist_ok=True)

output.to_csv(
    output_file,
    index=False
)

print("30-day pattern anomaly detection completed.")

print("\nAnomaly counts:")
print(
    output["30Day_Anomaly_Level"].value_counts()
)

print("\nAverage 30-day anomaly score:")
print(
    round(
        output["30Day_Anomaly_Score"].mean(),
        3
    )
)

print("\nHighest 30-day pattern anomalies:")

print(
    output.sort_values(
        "30Day_Anomaly_Score",
        ascending=False
    ).head(20).to_string(index=False)
)

print("\nSaved:")
print(output_file)