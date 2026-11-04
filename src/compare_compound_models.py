
import pandas as pd
import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

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

test = df[df["YEAR"] >= 2020].copy()

X_test = test[FEATURES]
y_test = test[TARGET]

models = {
    "Original": joblib.load(
        "results/compound_random_forest_model.pkl"
    ),
    "Improved": joblib.load(
        "results/compound_random_forest_model_improved.pkl"
    )
}

print("\nCOMPOUND MODEL COMPARISON")
print("=" * 55)
print("Test period:", test["DATE"].min().date(), "to", test["DATE"].max().date())
print("Test rows:", len(test))
print("Actual compound events:", int(y_test.sum()))

for name, model in models.items():
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test, predictions, labels=[0, 1]
    ).ravel()

    print("\n", name.upper())
    print("-" * 40)
    print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
    print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 3))
    print("Recall:", round(recall_score(y_test, predictions, zero_division=0), 3))
    print("F1-score:", round(f1_score(y_test, predictions, zero_division=0), 3))
    print("True positives:", tp)
    print("False alarms:", fp)
    print("Missed events:", fn)
    print("True negatives:", tn)
