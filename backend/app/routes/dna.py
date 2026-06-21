from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/dna")
def get_dna():

    df = pd.read_csv(
        "outputs/dna_profiles.csv"
    )

    return df.to_dict(
        orient="records"
    )