from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/advisor")
def advisor():

    df = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    merged = pd.merge(
        df,
        hotspots[
            [
                "cluster",
                "top_junction",
                "police_station"
            ]
        ],
        on="cluster",
        how="left"
    )

    top = merged.sort_values(
        "priority_rank"
    ).head(5)

    plan = []

    for _, row in top.iterrows():

        officers = max(
            2,
            round(
                row["violations"]/10000
                +
                row["risk_score"]/20
            )
        )

        if row["risk_score"] > 60:
            priority = "HIGH"

        elif row["risk_score"] > 40:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        location = row["top_junction"]

        if (
            pd.isna(location)
            or location == "No Junction"
        ):
            location = (
                row["police_station"]
                + " Area"
            )

        plan.append({

            "location":
            location,

            "priority":
            priority,

            "officers":
            officers,

            "risk_score":
            round(
                row["risk_score"],
                2
            ),

            "violations":
            int(
                row["violations"]
            )
        })

    return plan