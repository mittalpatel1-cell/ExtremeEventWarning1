import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

df = pd.read_csv("results/compound_predictions.csv")
y = df["compound_7d_ahead"]
p = df["Probability"]

print("\nCOMPOUND EVENT THRESHOLD COMPARISON")
print("=" * 85)
print(f"{'Threshold':<12}{'TP':<8}{'FP':<8}{'FN':<8}{'TN':<8}{'Precision':<12}{'Recall':<10}{'F1':<10}")

for t in [0.5, 0.4, 0.3, 0.2, 0.1]:
    pred = (p >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()

    print(f"{t:<12}{tp:<8}{fp:<8}{fn:<8}{tn:<8}{precision_score(y, pred, zero_division=0):<12.3f}{recall_score(y, pred, zero_division=0):<10.3f}{f1_score(y, pred, zero_division=0):<10.3f}")
