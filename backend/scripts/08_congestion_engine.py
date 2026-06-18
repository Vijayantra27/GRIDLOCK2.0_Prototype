import pandas as pd

print("\nLoading Risk Data...")

risk = pd.read_csv(
    "outputs/risk_scores.csv"
)

patrol = pd.read_csv(
    "outputs/patrol_plan.csv"
)

# -----------------------------
# Merge Data
# -----------------------------

df = risk.merge(
    patrol[
        [
            "cluster",
            "priority_score"
        ]
    ],
    on="cluster"
)

# -----------------------------
# Congestion Score
# -----------------------------

df["congestion_score"] = (
    0.6 * df["risk_score"]
    +
    0.4 * df["priority_score"]
)

# -----------------------------
# Congestion Level
# -----------------------------

def congestion_level(score):

    if score >= 70:
        return "Critical"

    elif score >= 50:
        return "High"

    elif score >= 30:
        return "Medium"

    return "Low"

df["congestion_level"] = (
    df["congestion_score"]
    .apply(congestion_level)
)

# -----------------------------
# Sort
# -----------------------------

df = df.sort_values(
    "congestion_score",
    ascending=False
)

print("\nTop Congestion Zones")

print(
    df[
        [
            "cluster",
            "risk_score",
            "priority_score",
            "congestion_score",
            "congestion_level"
        ]
    ]
    .head(15)
)

df.to_csv(
    "outputs/congestion_results.csv",
    index=False
)

print(
    "\nSaved outputs/congestion_results.csv"
)