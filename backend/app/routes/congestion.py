from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    tags=["Congestion"]
)


@router.get("/congestion")
def get_congestion():

    df = pd.read_csv(
        "outputs/congestion_results.csv"
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/propagation")
def get_propagation():

    df = pd.read_csv(
        "outputs/traffic_propagation.csv"
    )

    return df.head(500).to_dict(
        orient="records"
    )