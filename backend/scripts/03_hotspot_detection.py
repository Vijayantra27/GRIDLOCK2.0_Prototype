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

from sklearn.cluster import DBSCAN
import pandas as pd


print("\nLoading cleaned dataset...")

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

# Remove rows with missing coordinates

df = df.dropna(
    subset=[
        "latitude",
        "longitude"
    ]
)

print(f"\nRows with coordinates: {len(df)}")

# GPS coordinates

coords = df[
    [
        "latitude",
        "longitude"
    ]
]

print("\nRunning DBSCAN...")

dbscan = DBSCAN(
    eps=0.0015,
    min_samples=50
)

df["cluster"] = dbscan.fit_predict(
    coords
)

print("\nCluster Summary")

print(
    df["cluster"]
    .value_counts()
    .head(20)
)

# Remove noise points

hotspots = df[
    df["cluster"] != -1
]

print(
    f"\nHotspot Records: {len(hotspots)}"
)

# Hotspot summary

summary = (
    hotspots
    .groupby("cluster")
    .agg(
        violations=("id", "count"),
        avg_lat=("latitude", "mean"),
        avg_lon=("longitude", "mean"),
        top_junction=("junction_name", lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown"),
        police_station=("police_station", lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown")
    )
    .reset_index()
)

summary = summary.sort_values(
    by="violations",
    ascending=False
)

print("\nTop Hotspots")

print(
    summary.head(10)
)

summary.to_csv(
    "outputs/hotspot_results.csv",
    index=False
)

print(
    "\nSaved hotspot results to outputs/hotspot_results.csv"
)
df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)
print("\nDate Range")

print(
    df["created_datetime"].min()
)

print(
    df["created_datetime"].max()
)

print(
    "Unique Months:",
    sorted(
        df["created_datetime"]
        .dt.month
        .dropna()
        .unique()
    )
)