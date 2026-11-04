import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

df = pd.read_csv("data/processed/event_labeled_dataset.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df.sort_values(["DATE", "LOCATION"]).reset_index(drop=True)

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]
target = "compound_7d_ahead"

train = df[df["YEAR"] <= 2019]
test = df[df["YEAR"] >= 2020]

for leaf in [1, 5]:
    model = RandomForestClassifier(
        n_estimators=150,
        min_samples_leaf=leaf,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )
    model.fit(train[features], train[target])
    pred = model.predict(test[features])

    print(f"\nmin_samples_leaf={leaf}")
    print("Precision:", round(precision_score(test[target], pred, zero_division=0), 3))
    print("Recall:", round(recall_score(test[target], pred, zero_division=0), 3))
    print("F1-score:", round(f1_score(test[target], pred, zero_division=0), 3))
    print("Confusion matrix:")
    print(confusion_matrix(test[target], pred))
