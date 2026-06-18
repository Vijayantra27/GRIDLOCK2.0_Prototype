import pandas as pd

print("\nLoading Data...")

risk = pd.read_csv(
    "outputs/risk_scores.csv"
)

allocation = pd.read_csv(
    "outputs/officer_allocation.csv"
)

# -------------------------
# Example Scenario
# -------------------------

TARGET_CLUSTER = 2

ADDITIONAL_OFFICERS = 5

# -------------------------
# Get Current Data
# -------------------------

row = risk[
    risk["cluster"] == TARGET_CLUSTER
]

if len(row) == 0:

    print("Cluster not found")
    exit()

current_risk = (
    row["risk_score"]
    .iloc[0]
)

# -------------------------
# Simulation Formula
# -------------------------

risk_reduction = (
    ADDITIONAL_OFFICERS * 2
)

new_risk = max(
    0,
    current_risk - risk_reduction
)

risk_change = (
    current_risk - new_risk
)

congestion_reduction = (
    risk_change * 0.8
)

propagation_reduction = (
    risk_change * 0.6
)

# -------------------------
# Output
# -------------------------

print("\nWHAT-IF SIMULATION")

print(
    f"\nCluster: {TARGET_CLUSTER}"
)

print(
    f"Current Risk: {current_risk:.2f}"
)

print(
    f"Additional Officers: {ADDITIONAL_OFFICERS}"
)

print(
    f"New Risk: {new_risk:.2f}"
)

print(
    f"Estimated Congestion Reduction: "
    f"{congestion_reduction:.2f}%"
)

print(
    f"Estimated Propagation Reduction: "
    f"{propagation_reduction:.2f}%"
)

# -------------------------
# Save
# -------------------------

results = pd.DataFrame([{

    "cluster":
        TARGET_CLUSTER,

    "current_risk":
        current_risk,

    "additional_officers":
        ADDITIONAL_OFFICERS,

    "new_risk":
        new_risk,

    "congestion_reduction":
        congestion_reduction,

    "propagation_reduction":
        propagation_reduction

}])

results.to_csv(
    "outputs/simulation_results.csv",
    index=False
)

print(
    "\nSaved outputs/simulation_results.csv"
)