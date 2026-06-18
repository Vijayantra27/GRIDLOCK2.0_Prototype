# scripts/check_locations.py

import pandas as pd

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

print("\nTop Police Stations")
print(
    df["police_station"]
    .value_counts()
    .head(20)
)

print("\nTop Junctions")
print(
    df["junction_name"]
    .value_counts()
    .head(20)
)