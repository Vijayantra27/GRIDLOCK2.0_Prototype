from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/assistant")
def assistant(q: str = ""):

    q = q.lower()

    risk = pd.read_csv(
        "outputs/risk_scores.csv"
    )

    dna = pd.read_csv(
        "outputs/dna_profiles.csv"
    )

    patrol = pd.read_csv(
        "outputs/patrol_plan.csv"
    )

    if "highest risk" in q:

        top = risk.sort_values(
            "risk_score",
            ascending=False
        ).iloc[0]

        return {
            "answer":
            f"Cluster {top['cluster']} has the highest risk score of {top['risk_score']:.2f}."
        }

    elif "hotspot" in q:

        top = dna.sort_values(
            "total_violations",
            ascending=False
        ).iloc[0]

        return {
            "answer":
            f"{top['police_station']} is currently the highest violation hotspot with {int(top['total_violations'])} violations."
        }

    elif "officer" in q or "patrol" in q:

        top = patrol.iloc[0]

        return {
            "answer":
            f"Highest patrol priority is Cluster {top['cluster']}."
        }

    elif "congestion" in q:

        return {
            "answer":
            "Upparpet, Shivajinagar and Vijayanagara are currently the most congestion-prone regions."
        }

    return {
        "answer":
        "Try asking: highest risk zone, top hotspot, congestion hotspots, patrol recommendation."
    }