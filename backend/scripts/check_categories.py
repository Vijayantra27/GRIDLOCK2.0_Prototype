import pandas as pd

df = pd.read_csv("data/processed/cleaned_data.csv")

print("\nVehicle Types")
print(df["vehicle_type"].value_counts().head(20))

print("\nViolation Types")
print(df["violation_type"].value_counts().head(20))