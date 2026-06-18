# backend/app/utils/feature_engineering.py

import pandas as pd


def create_time_features(df):

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

    return df