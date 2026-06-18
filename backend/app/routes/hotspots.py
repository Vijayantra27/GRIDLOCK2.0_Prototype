from fastapi import APIRouter
import pandas as pd

router = APIRouter(
    tags=["Hotspots"]
)


@router.get("/hotspots")
def get_hotspots():

    df = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    return df.to_dict(
        orient="records"
    )


@router.get("/dna")
def get_dna():

    df = pd.read_csv(
        "outputs/dna_profiles.csv"
    )

    return df.to_dict(
        orient="records"
    )