import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/processed/event_labeled_dataset.csv")

features = [
    "TMAX", "RH2M", "PRECTOTCORR", "WS10M", "PS",
    "ALLSKY_SFC_SW_DWN", "ONI", "MONTH", "DAY_OF_YEAR",
    "TMAX_7D", "RAIN_7D", "RH_7D"
]

train = df[df["YEAR"] <= 2019]

model = RandomForestClassifier(
    n_estimators=150,
    min_samples_leaf=5,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(train[features], train["compound_7d_ahead"])

joblib.dump(model, "results/compound_random_forest_model_improved.pkl")

print("Improved compound model saved successfully!")
print("File: results/compound_random_forest_model_improved.pkl")
