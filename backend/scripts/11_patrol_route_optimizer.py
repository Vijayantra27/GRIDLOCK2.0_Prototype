import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

print("\nLoading Hotspots...")

hotspots = pd.read_csv(
    "outputs/hotspot_results.csv"
)

# Top 10 hotspots only

hotspots = hotspots.head(10).reset_index(drop=True)

# --------------------------------
# Distance Function
# --------------------------------

def haversine(lat1, lon1, lat2, lon2):

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

# --------------------------------
# Nearest Neighbor Route
# --------------------------------

unvisited = list(range(len(hotspots)))

route = [unvisited.pop(0)]

while unvisited:

    current = route[-1]

    nearest = min(
        unvisited,
        key=lambda x:
        haversine(
            hotspots.iloc[current]["avg_lat"],
            hotspots.iloc[current]["avg_lon"],
            hotspots.iloc[x]["avg_lat"],
            hotspots.iloc[x]["avg_lon"]
        )
    )

    route.append(nearest)

    unvisited.remove(nearest)

# --------------------------------
# Route Output
# --------------------------------

print("\nOptimized Patrol Route\n")

for idx, stop in enumerate(route):

    row = hotspots.iloc[stop]

    print(
        f"{idx+1}. "
        f"{row['police_station']} | "
        f"{row['top_junction']}"
    )