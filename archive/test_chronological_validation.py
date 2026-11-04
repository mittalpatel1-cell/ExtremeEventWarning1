import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

DATA_FILE = "data/processed/event_labeled_dataset.csv"

FEATURES = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]

TARGET = "compound_7d_ahead"

df = pd.read_csv(DATA_FILE)
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values(["DATE", "LOCATION"]).reset_index(drop=True)

print("CHRONOLOGICAL VALIDATION")
print("=" * 55)

years = [(2007, 2010), (2011, 2014), (2015, 2019)]

for start_year, end_year in years:
    train = df[df["YEAR"] < start_year]
    valid = df[(df["YEAR"] >= start_year) & (df["YEAR"] <= end_year)]

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(train[FEATURES], train[TARGET])
    probabilities = model.predict_proba(valid[FEATURES])[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    print(f"\nValidation period: {start_year}-{end_year}")
    print("Training through:", train["DATE"].max().date())
    print("Validation from:", valid["DATE"].min().date())
    print("Actual events:", int(valid[TARGET].sum()))
    print("Predicted events:", int(predictions.sum()))
    print("Precision:", round(precision_score(valid[TARGET], predictions, zero_division=0), 3))
    print("Recall:", round(recall_score(valid[TARGET], predictions, zero_division=0), 3))
    print("F1-score:", round(f1_score(valid[TARGET], predictions, zero_division=0), 3))
