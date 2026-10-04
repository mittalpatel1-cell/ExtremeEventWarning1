import pandas as pd
import numpy as np
import joblib
import shap

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

DATA_FILE = "data/processed/event_labeled_dataset.csv"

FEATURES = [
    "TMAX",
    "RH2M",
    "PRECTOTCORR",
    "WS10M",
    "PS",
    "ALLSKY_SFC_SW_DWN",
    "ONI",
    "MONTH",
    "DAY_OF_YEAR",
    "TMAX_7D",
    "RAIN_7D",
    "RH_7D"
]

TARGETS = {
    "heatwave": "heatwave_7d_ahead",
    "drought": "drought_7d_ahead",
    "compound": "compound_7d_ahead"
}

df = pd.read_csv(DATA_FILE)

train_df = df[df["YEAR"] <= 2019].copy()
test_df = df[df["YEAR"] >= 2020].copy()

X_train = train_df[FEATURES]
X_test = test_df[FEATURES]

tscv = TimeSeriesSplit(n_splits=5)


def cross_validate_model(X, y, name):

    print("\n" + "=" * 60)
    print(name.upper(), "TIME-SERIES CROSS VALIDATION")
    print("=" * 60)

    scores = []

    for fold, (train_index, val_index) in enumerate(
        tscv.split(X), start=1
    ):

        X_fold_train = X.iloc[train_index]
        X_fold_val = X.iloc[val_index]

        y_fold_train = y.iloc[train_index]
        y_fold_val = y.iloc[val_index]

        model = RandomForestClassifier(
            n_estimators=150,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )

        model.fit(X_fold_train, y_fold_train)

        predictions = model.predict(X_fold_val)

        accuracy = accuracy_score(y_fold_val, predictions)
        precision = precision_score(
            y_fold_val,
            predictions,
            zero_division=0
        )
        recall = recall_score(
            y_fold_val,
            predictions,
            zero_division=0
        )
        f1 = f1_score(
            y_fold_val,
            predictions,
            zero_division=0
        )

        scores.append(
            [accuracy, precision, recall, f1]
        )

        print(
            f"Fold {fold}: "
            f"Accuracy={accuracy:.3f}, "
            f"Precision={precision:.3f}, "
            f"Recall={recall:.3f}, "
            f"F1={f1:.3f}"
        )

    scores = np.array(scores)

    print("\nAverage:")
    print("Accuracy:", round(scores[:, 0].mean(), 3))
    print("Precision:", round(scores[:, 1].mean(), 3))
    print("Recall:", round(scores[:, 2].mean(), 3))
    print("F1:", round(scores[:, 3].mean(), 3))


for name, target in TARGETS.items():

    y_train = train_df[target]
    y_test = test_df[target]

    cross_validate_model(
        X_train,
        y_train,
        name
    )

    print("\n" + "-" * 60)
    print(name.upper(), "FINAL TEST")
    print("-" * 60)

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    print("Accuracy:", round(accuracy, 3))
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1:", round(f1, 3))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    joblib.dump(
        model,
        f"results/{name}_random_forest_model.pkl"
    )

    prediction_output = test_df[
        ["DATE", "LOCATION", target]
    ].copy()

    prediction_output["Probability"] = probabilities
    prediction_output["Prediction"] = predictions

    prediction_output.to_csv(
        f"results/{name}_predictions.csv",
        index=False
    )

    print(
        f"\nModel saved: "
        f"results/{name}_random_forest_model.pkl"
    )

    print(
        f"Predictions saved: "
        f"results/{name}_predictions.csv"
    )

    print("\nCalculating SHAP...")

    shap_sample = X_test.sample(
        n=min(1000, len(X_test)),
        random_state=42
    )

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(shap_sample)

    if isinstance(shap_values, list):
        values = np.array(shap_values[1])
    else:
        values = np.array(shap_values)

        if values.ndim == 3:
            values = values[:, :, 1]

    mean_abs_shap = np.abs(values).mean(axis=0)

    shap_df = pd.DataFrame({
        "Feature": FEATURES,
        "Mean_Absolute_SHAP": mean_abs_shap
    })

    shap_df = shap_df.sort_values(
        "Mean_Absolute_SHAP",
        ascending=False
    )

    shap_df.to_csv(
        f"results/{name}_shap_importance.csv",
        index=False
    )

    print(
        f"SHAP saved: "
        f"results/{name}_shap_importance.csv"
    )