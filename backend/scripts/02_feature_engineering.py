import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.utils.data_loader import load_data

import pandas as pd


df = load_data()

print("\nCreating Time Features...")

df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)

df["hour"] = df["created_datetime"].dt.hour

df["day"] = df["created_datetime"].dt.day

df["month"] = df["created_datetime"].dt.month

df["weekday"] = df["created_datetime"].dt.day_name()

df["is_weekend"] = (
    df["created_datetime"].dt.dayofweek >= 5
).astype(int)

print("\nNew Features Created:")

print(
    df[
        [
            "created_datetime",
            "hour",
            "day",
            "month",
            "weekday",
            "is_weekend"
        ]
    ].head()
)

output_path = (
    "data/processed/cleaned_data.csv"
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nSaved cleaned dataset to: {output_path}"
)