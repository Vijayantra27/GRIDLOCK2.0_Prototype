from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get(
    "/officer-recommendation/{cluster}"
)
def get_recommendation(cluster: int):

    df = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    row = df[
        df["cluster"] == cluster
    ].iloc[0]

    officers = max(
        2,
        round(
            row["violations"] / 10000
            +
            row["risk_score"] / 20
        )
    )

    if row["risk_score"] > 60:
        priority = "HIGH"
        frequency = "Every 30 min"

    elif row["risk_score"] > 40:
        priority = "MEDIUM"
        frequency = "Every 1 hour"

    else:
        priority = "LOW"
        frequency = "Every 2 hours"

    return {
        "cluster":
        int(row["cluster"]),

        "violations":
        int(row["violations"]),

        "risk_score":
        round(
            row["risk_score"],
            2
        ),

        "recommended_officers":
        officers,

        "priority":
        priority,

        "frequency":
        frequency
    }