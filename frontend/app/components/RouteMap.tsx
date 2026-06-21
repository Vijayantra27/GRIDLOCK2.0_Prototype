"use client";

import { useEffect, useState } from "react";

import {
  MapContainer,
  TileLayer,
  Polyline,
  CircleMarker,
  Popup,
} from "react-leaflet";

import type { LatLngExpression } from "leaflet";

import { getRoutes } from "@/services/api";

import "leaflet/dist/leaflet.css";

export default function RouteMap({
  routeData = [],
  geometry = [],
  selectedStation,
}: any) {
  const [routes, setRoutes] = useState<any[]>([]);

  useEffect(() => {
    getRoutes()
      .then((data) => {
        console.log("Routes:", data);
        setRoutes(data);
      })
      .catch((err) =>
        console.error("Route API Error:", err)
      );
  }, []);

  const positions =
  geometry.length
    ? geometry.map(
        (p: any) => [
          p[1],
          p[0],
        ]
      )
    : [];

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-xl font-bold mb-4">
        Patrol Route Optimizer
      </h2>

      <MapContainer
        center={[12.97, 77.59]}
        zoom={11}
        style={{
          height: "500px",
          width: "100%",
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {selectedStation && (

          <CircleMarker
            center={[
              selectedStation.avg_lat,
              selectedStation.avg_lon
            ]}
            radius={14}
            pathOptions={{
              color: "green",
              fillColor: "green",
              fillOpacity: 1,
            }}
          >

            <Popup>

              🚔 Police Station

              <br />

              {
                selectedStation
                .police_station
              }

            </Popup>

          </CircleMarker>

        )}
        {positions.length > 0 && (

          <Polyline
            positions={positions}
            pathOptions={{
              color: "red",
              weight: 6,
            }}
          />

        )}

        {routes.map((route) => (
          <CircleMarker
            key={route.cluster}
            center={[
              Number(route.avg_lat),
              Number(route.avg_lon),
            ]}
            radius={10}
            pathOptions={{
              color: "blue",
              fillColor: "blue",
              fillOpacity: 0.8,
            }}
          >
            <Popup>
              <b>
                Stop #{route.priority_rank}
              </b>

              <br />

              {route.police_station}

              <br />

              Priority Score:{" "}
              {Number(
                route.priority_score
              ).toFixed(2)}
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}