from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/propagation")
def get_propagation():

    df = pd.read_csv(
        "outputs/traffic_propagation.csv"
    )

    return df.head(100).to_dict(
        orient="records"
    )