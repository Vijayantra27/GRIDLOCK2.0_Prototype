# scripts/07_prepare_prediction_data.py

import pandas as pd
from sklearn.cluster import DBSCAN

print("Loading dataset...")

df = pd.read_csv(
    "data/processed/cleaned_data.csv"
)

coords = df[
    ["latitude", "longitude"]
]

dbscan = DBSCAN(
    eps=0.0015,
    min_samples=50
)

df["cluster"] = dbscan.fit_predict(coords)

df = df[
    df["cluster"] != -1
]

cluster_counts = (
    df.groupby("cluster")
      .size()
      .reset_index(name="violations")
)
print(cluster_counts["violations"].describe())
threshold = (
    cluster_counts["violations"]
    .quantile(0.95)
)

high_risk_clusters = (
    cluster_counts[
        cluster_counts["violations"]
        >= threshold
    ]["cluster"]
)

df["high_risk_hotspot"] = (
    df["cluster"]
    .isin(high_risk_clusters)
).astype(int)

print(
    df["high_risk_hotspot"]
    .value_counts()
)

df.to_csv(
    "data/processed/prediction_dataset.csv",
    index=False
)

print(
    "Saved prediction_dataset.csv"
)