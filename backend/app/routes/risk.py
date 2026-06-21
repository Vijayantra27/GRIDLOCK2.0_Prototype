from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/risk")
def get_risk():

    df = pd.read_csv(
        "outputs/risk_scores.csv"
    )

    return (
        df.head(20)
        .to_dict(orient="records")
    )