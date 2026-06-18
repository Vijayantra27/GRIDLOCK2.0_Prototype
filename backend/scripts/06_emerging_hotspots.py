import pandas as pd

print("\nLoading Dataset...")

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)

df["month"] = (
    df["created_datetime"]
    .dt.month
)

# Early Period

early = df[
    df["month"].isin(
        [11, 12, 1]
    )
]

# Late Period

late = df[
    df["month"].isin(
        [2, 3, 4]
    )
]

early_counts = (
    early.groupby("police_station")
         .size()
         .reset_index(name="early_count")
)

late_counts = (
    late.groupby("police_station")
        .size()
        .reset_index(name="late_count")
)

growth = early_counts.merge(
    late_counts,
    on="police_station",
    how="outer"
).fillna(0)

growth["growth_percent"] = (
    (
        growth["late_count"]
        -
        growth["early_count"]
    )
    /
    (
        growth["early_count"] + 1
    )
) * 100

growth = growth.sort_values(
    "growth_percent",
    ascending=False
)

print("\nTop Emerging Hotspots")

print(
    growth[
        [
            "police_station",
            "early_count",
            "late_count",
            "growth_percent"
        ]
    ]
    .head(15)
)

growth.to_csv(
    "outputs/emerging_hotspots.csv",
    index=False
)

print(
    "\nSaved: outputs/emerging_hotspots.csv"
)