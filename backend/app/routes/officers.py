from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/officers")
def get_officers():

    df = pd.read_csv(
        "outputs/officer_allocation.csv"
    )

    return df.to_dict(
        orient="records"
    )