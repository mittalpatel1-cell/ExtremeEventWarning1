
import pandas as pd
import joblib
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]

df = pd.read_csv("data/processed/event_labeled_dataset.csv")
df = df[df["YEAR"] >= 2020].copy()

X_test = df[features]
y_test = df["compound_7d_ahead"]

model = joblib.load(
    "results/compound_random_forest_model_improved.pkl"
)

probabilities = model.predict_proba(X_test)[:, 1]

print("\nIMPROVED COMPOUND MODEL: THRESHOLD TEST")
print("=" * 55)
print("Actual events:", int(y_test.sum()))

for threshold in [0.50, 0.45, 0.40, 0.35, 0.30]:
    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test, predictions, labels=[0, 1]
    ).ravel()

    print(f"\nThreshold: {threshold:.2f}")
    print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 3))
    print("Recall:", round(recall_score(y_test, predictions, zero_division=0), 3))
    print("F1-score:", round(f1_score(y_test, predictions, zero_division=0), 3))
    print("Detected events:", tp)
    print("False alarms:", fp)
    print("Missed events:", fn)
