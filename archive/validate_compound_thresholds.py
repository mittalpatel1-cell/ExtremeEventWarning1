import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]

df = pd.read_csv("data/processed/event_labeled_dataset.csv")
train = df[df["YEAR"] <= 2014].copy()
valid = df[df["YEAR"].between(2015, 2019)].copy()

model = RandomForestClassifier(
    n_estimators=150,
    min_samples_leaf=5,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(train[features], train["compound_7d_ahead"])

y = valid["compound_7d_ahead"]
probabilities = model.predict_proba(valid[features])[:, 1]

print("\nCOMPOUND EVENT VALIDATION")
print("=" * 45)
print("Training rows:", len(train))
print("Validation rows:", len(valid))
print("Actual events:", int(y.sum()))

for threshold in [0.50, 0.45, 0.40, 0.35, 0.30, 0.20]:
    pred = (probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()

    print(f"\nThreshold: {threshold:.2f}")
    print("Precision:", round(precision_score(y, pred, zero_division=0), 3))
    print("Recall:", round(recall_score(y, pred, zero_division=0), 3))
    print("F1-score:", round(f1_score(y, pred, zero_division=0), 3))
    print("Detected events:", tp)
    print("False alarms:", fp)
    print("Missed events:", fn)
