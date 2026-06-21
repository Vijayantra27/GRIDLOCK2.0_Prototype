from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/emerging")
def get_emerging():

    df = pd.read_csv(
        "outputs/emerging_hotspots.csv"
    )

    return df.to_dict(
        orient="records"
    )