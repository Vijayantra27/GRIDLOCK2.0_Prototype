from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

class CoverageRequest(BaseModel):
    selected_clusters: list[int]

@router.post("/coverage")
def coverage(data: CoverageRequest):

    df = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    uncovered = df[
        ~df["cluster"].isin(
            data.selected_clusters
        )
    ]

    top_uncovered = (
        uncovered
        .sort_values(
            "risk_score",
            ascending=False
        )
        .head(5)
    )

    return top_uncovered[
        [
            "cluster",
            "risk_score",
            "priority_rank"
        ]
    ].to_dict(
        orient="records"
    )