import pandas as pd

file = "data/raw/imd_temperature_1997_2023.csv"

df = pd.read_csv(file)

print("Values >= 50:")
print(df[df["TMAX"] >= 50].head(20))

print("\nCount of values >= 50:")
print((df["TMAX"] >= 50).sum())

print("\nUnique suspicious values:")
print(sorted(df.loc[df["TMAX"] >= 50, "TMAX"].unique()))