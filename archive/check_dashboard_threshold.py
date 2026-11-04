
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

threshold = 0.45

df = pd.read_csv("data/processed/event_labeled_dataset.csv")
df = df[df["YEAR"] >= 2020].copy()

preds = pd.read_csv("results/extreme_event_warnings.csv")

preds["DATE"] = pd.to_datetime(preds["DATE"])
df["DATE"] = pd.to_datetime(df["DATE"])

test = df[["DATE", "LOCATION", "compound_7d_ahead"]].merge(
    preds[["DATE", "LOCATION", "Compound_Probability"]],
    on=["DATE", "LOCATION"],
    how="inner"
)

y_true = test["compound_7d_ahead"].astype(int)
y_pred = (test["Compound_Probability"] >= threshold).astype(int)

tn, fp, fn, tp = confusion_matrix(
    y_true, y_pred, labels=[0, 1]
).ravel()

print("\nDASHBOARD COMPOUND WARNING EVALUATION")
print("=" * 45)
print("Matched test rows:", len(test))
print("Actual events:", int(y_true.sum()))
print("Threshold:", threshold)
print("Precision:", round(precision_score(y_true, y_pred, zero_division=0), 3))
print("Recall:", round(recall_score(y_true, y_pred, zero_division=0), 3))
print("F1-score:", round(f1_score(y_true, y_pred, zero_division=0), 3))
print("Detected events:", tp)
print("False alarms:", fp)
print("Missed events:", fn)
print("True negatives:", tn)
