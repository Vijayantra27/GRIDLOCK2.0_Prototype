from fastapi import APIRouter
import pandas as pd
import math

router = APIRouter()

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )

@router.get("/recommend/{station}")
def recommend(station: int):

    df = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    station_row = df[
        df["cluster"] == station
    ].iloc[0]

    df["distance"] = df.apply(
        lambda row: distance(
            station_row["avg_lat"],
            station_row["avg_lon"],
            row["avg_lat"],
            row["avg_lon"]
        ),
        axis=1
    )


    recommendations = (
        df[df["cluster"] != station]
        .sort_values(
            ["distance", "violations"],
            ascending=[True, False]
        )
        .head(8)
    )
    recommendations["priority_score"] = (
        recommendations["violations"] * 0.7
        +
        (1/(recommendations["distance"]+0.001))
        * 1000 * 0.3
    )

    return recommendations[
    [
    "cluster",
    "police_station",
    "violations",
    "distance",
    "priority_score"
    ]
    ].to_dict(
    orient="records"
    )