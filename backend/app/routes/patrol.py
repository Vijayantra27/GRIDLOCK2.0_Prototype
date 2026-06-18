from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    tags=["Patrol"]
)


@router.get("/patrol")
def get_patrol():

    df = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/allocation")
def get_allocation():

    df = pd.read_csv(
        "outputs/officer_allocation.csv"
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/route")
def get_route():

    df = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    return df.head(10).to_dict(
        orient="records"
    )