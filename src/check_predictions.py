import pandas as pd

file = "results/extreme_event_warnings.csv"

df = pd.read_csv(file)

print("\nFINAL PREDICTION FILE CHECK")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 predictions:")
print(
    df[
        [
            "DATE",
            "Prediction_Date",
            "LOCATION",
            "Heatwave_Probability",
            "Drought_Probability",
            "Compound_Probability",
            "Heatwave_Warning",
            "Drought_Warning",
            "Compound_Warning"
        ]
    ].head()
)

print("\nPrediction date check:")
dates = pd.to_datetime(df["DATE"])
prediction_dates = pd.to_datetime(df["Prediction_Date"])

print(
    "All predictions are exactly 7 days ahead:",
    ((prediction_dates - dates).dt.days == 7).all()
)

print("\nWarning counts:")
print("\nHeatwave:")
print(df["Heatwave_Warning"].value_counts())

print("\nDrought:")
print(df["Drought_Warning"].value_counts())

print("\nCompound:")
print(df["Compound_Warning"].value_counts())