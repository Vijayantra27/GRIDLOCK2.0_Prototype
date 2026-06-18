import pandas as pd

TOTAL_OFFICERS = 100

print("\nLoading Patrol Plan...")

df = pd.read_csv(
    "outputs/patrol_plan.csv"
)

# Only Top 20 Hotspots

df = (
    df.sort_values(
        "priority_score",
        ascending=False
    )
    .head(20)
)

# --------------------------
# Allocation
# --------------------------

total_priority = (
    df["priority_score"]
    .sum()
)

df["officer_share"] = (
    df["priority_score"]
    /
    total_priority
)

df["allocated_officers"] = (
    df["officer_share"]
    *
    TOTAL_OFFICERS
)

df["allocated_officers"] = (
    df["allocated_officers"]
    .round()
    .astype(int)
)

# --------------------------
# Sort
# --------------------------

df = df.sort_values(
    "allocated_officers",
    ascending=False
)

print("\nOfficer Allocation Plan")

print(
    df[
        [
            "priority_rank",
            "cluster",
            "priority_score",
            "allocated_officers"
        ]
    ]
    .head(20)
)

df.to_csv(
    "outputs/officer_allocation.csv",
    index=False
)

print(
    "\nSaved outputs/officer_allocation.csv"
)