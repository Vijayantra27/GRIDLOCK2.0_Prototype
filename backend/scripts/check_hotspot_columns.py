import pandas as pd

df = pd.read_csv(
    "outputs/hotspot_results.csv"
)

print(df.columns.tolist())

print("\nSample:")
print(df.head())