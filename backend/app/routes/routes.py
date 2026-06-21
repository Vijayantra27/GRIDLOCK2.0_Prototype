from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/routes")
def get_routes():

    patrol = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    merged = patrol.merge(
        hotspots,
        on="cluster"
    )

    merged = merged.sort_values(
        "priority_rank"
    )

    return merged[
        [
            "priority_rank",
            "cluster",
            "police_station",
            "avg_lat",
            "avg_lon",
            "priority_score"
        ]
    ].to_dict(
        orient="records"
    )