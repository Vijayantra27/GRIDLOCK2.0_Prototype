from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    risk = pd.read_csv(
        "outputs/risk_scores.csv"
    )

    return {
        "violations": int(
            hotspots["violations"].sum()
        ),

        "hotspots": len(hotspots),

        "police_stations": hotspots[
            "police_station"
        ].nunique(),

        "high_risk": len(
            risk[
                risk["risk_level"] == "High"
            ]
        )
    }