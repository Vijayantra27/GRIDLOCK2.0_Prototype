from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    tags=["Simulation"]
)


@router.get("/simulation")
def get_simulation():

    df = pd.read_csv(
        "outputs/simulation_results.csv"
    )

    return df.to_dict(
        orient="records"
    )