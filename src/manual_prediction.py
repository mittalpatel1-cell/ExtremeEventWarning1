import pandas as pd
import joblib

model = joblib.load("results/random_forest_model.pkl")

location = input("Enter location: ")
tmax = float(input("Enter temperature (°C): "))
rh = float(input("Enter humidity (%): "))
rain = float(input("Enter rainfall (mm): "))
wind = float(input("Enter wind speed (m/s): "))
pressure = float(input("Enter pressure: "))
solar = float(input("Enter solar radiation: "))
oni = float(input("Enter ONI: "))
month = int(input("Enter month (1-12): "))
day_of_year = int(input("Enter day of year: "))
tmax_7d = float(input("Enter 7-day average temperature: "))
rain_7d = float(input("Enter 7-day rainfall total: "))
rh_7d = float(input("Enter 7-day average humidity: "))

data = pd.DataFrame([{
    "TMAX": tmax,
    "RH2M": rh,
    "PRECTOTCORR": rain,
    "WS10M": wind,
    "PS": pressure,
    "ALLSKY_SFC_SW_DWN": solar,
    "ONI": oni,
    "MONTH": month,
    "DAY_OF_YEAR": day_of_year,
    "TMAX_7D": tmax_7d,
    "RAIN_7D": rain_7d,
    "RH_7D": rh_7d
}])

probability = model.predict_proba(data)[0][1]

if probability >= 0.70:
    warning = "HIGH RISK"
elif probability >= 0.40:
    warning = "MEDIUM RISK"
else:
    warning = "LOW RISK"

print("\nLocation:", location)
print("Compound Event Probability:", round(probability * 100, 2), "%")
print("Warning Level:", warning)

if warning == "HIGH RISK":
    print("🚨 Early Warning: Compound extreme event risk is high.")
elif warning == "MEDIUM RISK":
    print("⚠️ Monitor conditions closely.")
else:
    print("✅ No significant compound event risk detected.")