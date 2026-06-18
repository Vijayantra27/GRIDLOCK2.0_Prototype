import pandas as pd

print("\nLoading Dataset...")

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

# ------------------------
# Datetime Features
# ------------------------

df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)

df["hour"] = (
    df["created_datetime"]
    .dt.hour
)

df["is_weekend"] = (
    df["created_datetime"]
    .dt.dayofweek
    .isin([5, 6])
).astype(int)

# ------------------------
# Build DNA Profiles
# ------------------------

dna_profiles = []

stations = (
    df["police_station"]
    .dropna()
    .unique()
)

for station in stations:

    temp = df[
        df["police_station"] == station
    ]

    if len(temp) < 50:
        continue

    dominant_vehicle = (
        temp["vehicle_type"]
        .mode()
        .iloc[0]
        if not temp["vehicle_type"].mode().empty
        else "Unknown"
    )

    dominant_violation = (
        temp["violation_type"]
        .mode()
        .iloc[0]
        if not temp["violation_type"].mode().empty
        else "Unknown"
    )

    peak_hour = (
        temp["hour"]
        .mode()
        .iloc[0]
        if not temp["hour"].mode().empty
        else -1
    )

    weekend_ratio = round(
        (
            temp["is_weekend"]
            .mean()
        ) * 100,
        2
    )

    dna_profiles.append({

        "police_station":
            station,

        "dominant_vehicle":
            dominant_vehicle,

        "dominant_violation":
            dominant_violation,

        "peak_hour":
            peak_hour,

        "weekend_ratio":
            weekend_ratio,

        "total_violations":
            len(temp)
    })

# ------------------------
# Save Results
# ------------------------

dna_df = pd.DataFrame(
    dna_profiles
)

dna_df = dna_df.sort_values(
    by="total_violations",
    ascending=False
)

print("\nParking DNA Profiles")

print(
    dna_df.head(15)
)

dna_df.to_csv(
    "outputs/dna_profiles.csv",
    index=False
)

print(
    "\nSaved: outputs/dna_profiles.csv"
)