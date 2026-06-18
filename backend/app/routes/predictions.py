from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    tags=["Predictions"]
)


@router.get("/predictions")
def get_predictions():

    df = pd.read_csv(
        "outputs/risk_scores.csv"
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/emerging-hotspots")
def get_emerging_hotspots():

    df = pd.read_csv(
        "outputs/emerging_hotspots.csv"
    )

    return df.to_dict(
        orient="records"
    )