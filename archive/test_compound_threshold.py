import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

file = "results/compound_predictions.csv"

df = pd.read_csv(file)

y_true = df["compound_7d_ahead"]
probability = df["Probability"]

thresholds = [0.50, 0.40, 0.30, 0.20, 0.10]

print("\nCOMPOUND 7-DAY-AHEAD THRESHOLD TEST")
print("=" * 60)

for threshold in thresholds:

    prediction = (probability >= threshold).astype(int)

    precision = precision_score(
        y_true,
        prediction,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        prediction,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        prediction,
        zero_division=0
    )

    print("\nThreshold:", threshold)
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 Score:", round(f1, 3))
    print("Predicted Events:", prediction.sum())