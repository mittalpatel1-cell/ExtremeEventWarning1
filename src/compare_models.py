
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

df = pd.read_csv("data/processed/event_labeled_dataset.csv")

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M",
    "PS", "ALLSKY_SFC_SW_DWN", "ONI",
    "MONTH", "DAY_OF_YEAR", "TMAX_7D",
    "RAIN_7D", "RH_7D"
]

targets = {
    "Heatwave": "heatwave_7d_ahead",
    "Drought": "drought_7d_ahead",
    "Compound": "compound_7d_ahead"
}

train = df[df["YEAR"] <= 2019]
test = df[df["YEAR"] >= 2020]

X_train = train[features]
X_test = test[features]

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=150,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),
    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ),
    "SVM": make_pipeline(
        StandardScaler(),
        LinearSVC(
            class_weight="balanced",
            random_state=42,
            max_iter=10000
        )
    )
}

results = []

for event, target in targets.items():
    y_train = train[target]
    y_test = test[target]

    for name, model in models.items():
        print(f"Training {name} for {event}...", flush=True)

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        results.append({
            "Event": event,
            "Model": name,
            "Accuracy": accuracy_score(y_test, predictions),
            "Precision": precision_score(y_test, predictions, zero_division=0),
            "Recall": recall_score(y_test, predictions, zero_division=0),
            "F1-Score": f1_score(y_test, predictions, zero_division=0)
        })

results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON RESULTS")
print(results_df.to_string(index=False))

results_df.to_csv("results/model_comparison.csv", index=False)

print("\nResults saved successfully!")
