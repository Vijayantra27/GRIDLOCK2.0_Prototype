from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import math
import requests

router = APIRouter()

class RouteRequest(BaseModel):
    clusters: list[int]
    station: int

def distance(lat1, lon1, lat2, lon2):
    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    )

@router.post("/optimize-route")
def optimize_route(req: RouteRequest):

    hotspots = pd.read_csv(
        "outputs/hotspot_results.csv"
    )

    selected = hotspots[
        hotspots["cluster"].isin(
            req.clusters
        )
    ]

    station_row = hotspots[
        hotspots["cluster"] == req.station
    ].iloc[0]

    route = []

    remaining = selected.to_dict(
        "records"
    )

    current = {
        "cluster": int(station_row["cluster"]),
        "avg_lat": float(station_row["avg_lat"]),
        "avg_lon": float(station_row["avg_lon"]),
        "police_station": station_row["police_station"],
    }

    current = remaining.pop(0)

    route.append(current)

    while remaining:

        nearest = min(
            remaining,
            key=lambda x:
            distance(
                current["avg_lat"],
                current["avg_lon"],
                x["avg_lat"],
                x["avg_lon"]
            )
        )

        route.append(nearest)

        remaining.remove(nearest)

        current = nearest

    optimized_route = []

    for row in route:

        optimized_route.append({
            "cluster":
                int(row["cluster"]),
            "station":
                row["police_station"],
            "lat":
                float(row["avg_lat"]),
            "lon":
                float(row["avg_lon"])
        })
    
    coordinates = []

    for point in optimized_route:
        coordinates.append(
            f"{point['lon']},{point['lat']}"
        )

    coord_string = ";".join(coordinates)

    osrm_url = (
        f"https://router.project-osrm.org/"
        f"route/v1/driving/"
        f"{coord_string}"
        f"?overview=full&geometries=geojson"
    )

    response = requests.get(osrm_url)

    route_geometry = []

    distance_km = 0
    duration_min = 0

    if response.status_code == 200:

        data = response.json()

        route_geometry = (
            data["routes"][0]
            ["geometry"]["coordinates"]
        )

        distance_km = round(
            data["routes"][0]
            ["distance"] / 1000,
            2
        )

        duration_min = round(
            data["routes"][0]
            ["duration"] / 60,
            1
        )
    total_distance = 0

    for i in range(
        len(optimized_route) - 1
    ):
        total_distance += distance(
            optimized_route[i]["lat"],
            optimized_route[i]["lon"],
            optimized_route[i+1]["lat"],
            optimized_route[i+1]["lon"]
        )

    return {
        "route": optimized_route,
        "geometry": route_geometry,
        "distance_km": distance_km,
        "duration_min": duration_min,
    }