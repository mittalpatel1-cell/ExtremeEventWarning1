import pandas as pd
import joblib

DATA_FILE = "data/processed/event_labeled_dataset.csv"

FEATURES = [
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI",
    "MONTH",
    "DAY_OF_YEAR",
    "TMAX_7D",
    "RAIN_7D",
    "RH_7D"
]

models = {
    "heatwave": joblib.load("results/heatwave_random_forest_model.pkl"),
    "drought": joblib.load("results/drought_random_forest_model.pkl"),
    "compound": joblib.load("results/compound_random_forest_model.pkl")
}

df = pd.read_csv(DATA_FILE)

X = df[FEATURES]

df["Prediction_Date"] = (
    pd.to_datetime(df["DATE"]) + pd.Timedelta(days=7)
).dt.strftime("%Y-%m-%d")

heatwave_probability = models["heatwave"].predict_proba(X)[:, 1]
drought_probability = models["drought"].predict_proba(X)[:, 1]
compound_probability = models["compound"].predict_proba(X)[:, 1]

df["Heatwave_Probability"] = heatwave_probability
df["Drought_Probability"] = drought_probability
df["Compound_Probability"] = compound_probability


def warning_level(probability):
    if probability >= 0.70:
        return "HIGH RISK"
    elif probability >= 0.40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"


df["Heatwave_Warning"] = df["Heatwave_Probability"].apply(warning_level)
df["Drought_Warning"] = df["Drought_Probability"].apply(warning_level)

df["Compound_Warning"] = df["Compound_Probability"].apply(
    lambda x: "COMPOUND EVENT WARNING" if x >= 0.20 else "LOW RISK"
)

output_columns = [
    "DATE",
    "Prediction_Date",
    "LOCATION",
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI",
    "Heatwave_Probability",
    "Heatwave_Warning",
    "Drought_Probability",
    "Drought_Warning",
    "Compound_Probability",
    "Compound_Warning"
]

output = df[output_columns]

output.to_csv(
    "results/extreme_event_warnings.csv",
    index=False
)

print("7-day-ahead predictions generated successfully.")
print("Rows:", len(output))
print("Output: results/extreme_event_warnings.csv")

print("\nCompound warnings:")
print(
    output["Compound_Warning"]
    .value_counts()
)