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

import pandas as pd
from sklearn.cluster import DBSCAN

print("\nLoading Dataset...")

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

# --------------------------
# Datetime Conversion
# --------------------------

df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)

# --------------------------
# Hotspot Detection
# --------------------------

coords = df[
    [
        "latitude",
        "longitude"
    ]
]

dbscan = DBSCAN(
    eps=0.0015,
    min_samples=50
)

df["cluster"] = dbscan.fit_predict(
    coords
)

df = df[
    df["cluster"] != -1
]

# --------------------------
# Peak Hour Flag
# --------------------------

peak_hours = [
    8, 9, 10,
    17, 18, 19, 20, 21
]

df["is_peak_hour"] = (
    df["hour"].isin(peak_hours)
).astype(int)

# --------------------------
# Frequency Score
# --------------------------

frequency = (
    df.groupby("cluster")
      .size()
      .reset_index(name="violations")
)

max_freq = frequency["violations"].max()

frequency["frequency_score"] = (
    frequency["violations"] / max_freq
) * 100

# --------------------------
# Peak Hour Score
# --------------------------

peak_score = (
    df.groupby("cluster")
      ["is_peak_hour"]
      .mean()
      .reset_index()
)

peak_score["peak_score"] = (
    peak_score["is_peak_hour"]
    * 100
)

# --------------------------
# Recurrence Score
# --------------------------

df["date"] = (
    df["created_datetime"]
    .dt.date
)

recurrence = (
    df.groupby("cluster")
      ["date"]
      .nunique()
      .reset_index()
)

max_days = (
    recurrence["date"]
    .max()
)

recurrence["recurrence_score"] = (
    recurrence["date"]
    / max_days
) * 100

# --------------------------
# Growth Score
# --------------------------

df["month"] = (
    df["created_datetime"]
    .dt.month
)

early = df[
    df["month"].isin(
        [11,12,1]
    )
]

late = df[
    df["month"].isin(
        [2,3,4]
    )
]

early_counts = (
    early.groupby("cluster")
         .size()
)

late_counts = (
    late.groupby("cluster")
        .size()
)

growth_df = pd.DataFrame({
    "early": early_counts,
    "late": late_counts
}).fillna(0)

growth_df["growth"] = (
    growth_df["late"]
    - growth_df["early"]
)

growth_df["growth_score"] = (
    growth_df["growth"]
    .rank(pct=True)
    * 100
)

growth_df = (
    growth_df
    .reset_index()
)

# --------------------------
# Merge Everything
# --------------------------

risk = frequency.merge(
    peak_score,
    on="cluster"
)

risk = risk.merge(
    recurrence[
        [
            "cluster",
            "recurrence_score"
        ]
    ],
    on="cluster"
)

risk = risk.merge(
    growth_df[
        [
            "cluster",
            "growth_score"
        ]
    ],
    on="cluster"
)

# --------------------------
# Final Risk Score
# --------------------------

risk["risk_score"] = (
    0.40 * risk["frequency_score"]
    +
    0.25 * risk["peak_score"]
    +
    0.20 * risk["recurrence_score"]
    +
    0.15 * risk["growth_score"]
)

# --------------------------
# Risk Level
# --------------------------

def risk_level(score):

    if score >= 80:
        return "Critical"

    elif score >= 60:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"


risk["risk_level"] = (
    risk["risk_score"]
    .apply(risk_level)
)

risk = risk.sort_values(
    "risk_score",
    ascending=False
)

print("\nTop Risk Zones")

print(
    risk[
        [
            "cluster",
            "violations",
            "risk_score",
            "risk_level"
        ]
    ]
    .head(15)
)

risk.to_csv(
    "outputs/risk_scores.csv",
    index=False
)

print(
    "\nSaved: outputs/risk_scores.csv"
)