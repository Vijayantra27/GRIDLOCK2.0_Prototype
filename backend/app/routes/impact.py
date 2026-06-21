from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/impact/{cluster}")
def impact(cluster:int):

    df = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    row = df[
        df["cluster"] == cluster
    ].iloc[0]

    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    congestion_growth = round(
        row["risk_score"] * 0.3,
        1
    )

    nearby = hotspots[
        hotspots["cluster"] != cluster
    ].head(5)

    spillover = round(
        row["risk_score"] * 0.2,
        1
    )

    affected_roads = max(
        1,
        round(
            row["risk_score"] / 8
        )
    )
    affected_road_names = (
        nearby["top_junction"]
        .fillna("Unknown")
        .tolist()
    )

    return {
        "cluster": cluster,
        "congestion_growth":
        congestion_growth,

        "spillover":
        spillover,

        "affected_roads":
        affected_roads,

        "roads":
        affected_road_names
    }