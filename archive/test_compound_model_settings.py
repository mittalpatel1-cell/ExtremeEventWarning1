import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

df = pd.read_csv("data/processed/event_labeled_dataset.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values(["DATE", "LOCATION"]).reset_index(drop=True)

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]
target = "compound_7d_ahead"

for start, end in [(2007, 2010), (2011, 2014), (2015, 2019)]:
    train = df[df["YEAR"] < start]
    valid = df[(df["YEAR"] >= start) & (df["YEAR"] <= end)]

    print(f"\nValidation: {start}-{end}")

    for leaf in [1, 5]:
        model = RandomForestClassifier(
            n_estimators=150,
            min_samples_leaf=leaf,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )
        model.fit(train[features], train[target])
        prob = model.predict_proba(valid[features])[:, 1]
        pred = (prob >= 0.5).astype(int)

        print(
            f"min_samples_leaf={leaf}: "
            f"Precision={precision_score(valid[target], pred, zero_division=0):.3f}, "
            f"Recall={recall_score(valid[target], pred, zero_division=0):.3f}, "
            f"F1={f1_score(valid[target], pred, zero_division=0):.3f}"
        )
