import pandas as pd

print("\nLoading Risk Scores...")

risk = pd.read_csv(
    "outputs/risk_scores.csv"
)

# Normalize violations

max_v = risk["violations"].max()

risk["violation_density"] = (
    risk["violations"] / max_v
) * 100

# Priority Score

risk["priority_score"] = (
    0.70 * risk["risk_score"]
    +
    0.30 * risk["violation_density"]
)

risk = risk.sort_values(
    "priority_score",
    ascending=False
)

risk["priority_rank"] = (
    range(
        1,
        len(risk) + 1
    )
)

print("\nTop Patrol Priorities")

print(
    risk[
        [
            "priority_rank",
            "cluster",
            "violations",
            "risk_score",
            "priority_score"
        ]
    ]
    .head(15)
)

risk.to_csv(
    "outputs/patrol_plan.csv",
    index=False
)

print(
    "\nSaved: outputs/patrol_plan.csv"
)