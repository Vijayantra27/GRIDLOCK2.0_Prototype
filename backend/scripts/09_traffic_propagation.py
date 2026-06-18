import pandas as pd
from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2

print("\nLoading Hotspots...")

hotspots = pd.read_csv(
    "outputs/hotspot_results.csv"
)

# ----------------------------------
# Haversine Distance
# ----------------------------------

def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):

    R = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat/2)**2
        +
        cos(lat1)
        *
        cos(lat2)
        *
        sin(dlon/2)**2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1-a)
    )

    return R * c


# ----------------------------------
# Propagation Search
# ----------------------------------

propagation_results = []

RADIUS_KM = 2

for i, source in hotspots.iterrows():

    for j, target in hotspots.iterrows():

        if i == j:
            continue

        distance = haversine(
            source["avg_lat"],
            source["avg_lon"],
            target["avg_lat"],
            target["avg_lon"]
        )

        if distance <= RADIUS_KM:

            if distance <= 0.5:
                risk = "Very High"

            elif distance <= 1:
                risk = "High"

            elif distance <= 1.5:
                risk = "Medium"

            else:
                risk = "Low"

            propagation_results.append({
                "source_cluster":
                    source["cluster"],

                "source_station":
                    source["police_station"],

                "source_junction":
                    source["top_junction"],

                "affected_cluster":
                    target["cluster"],

                "affected_station":
                    target["police_station"],

                "affected_junction":
                    target["top_junction"],

                "distance_km":
                    round(distance, 3),

                "propagation_risk":
                    risk
            })

# ----------------------------------
# Save
# ----------------------------------

propagation_df = pd.DataFrame(
    propagation_results
)

propagation_df = propagation_df.sort_values(
    by="distance_km"
)

print("\nTraffic Propagation Results")

print(
    propagation_df.head(20)
)

propagation_df.to_csv(
    "outputs/traffic_propagation.csv",
    index=False
)

print(
    "\nSaved: outputs/traffic_propagation.csv"
)

print(
    f"\nTotal Links Found: {len(propagation_df)}"
)