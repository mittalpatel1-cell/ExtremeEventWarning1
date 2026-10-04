import pandas as pd
import glob
import os

files = glob.glob("data/raw/*_nasa_power.csv")

print("Number of files:", len(files))
print()

for file in files:
    df = pd.read_csv(file)

    print("=" * 60)
    print("File:", os.path.basename(file))
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    if "YEAR" in df.columns:
        print("Year range:", df["YEAR"].min(), "-", df["YEAR"].max())

    print("Missing values:")
    print(df.isnull().sum().to_dict())

print("\nVerification completed.")