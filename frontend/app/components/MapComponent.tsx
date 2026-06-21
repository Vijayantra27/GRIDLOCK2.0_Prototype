"use client";
import { useEffect, useState } from "react";
import { getHotspots } from "../../services/api";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

export default function MapComponent() {
    const [hotspots, setHotspots] = useState<any[]>([]);
    useEffect(() => {
        getHotspots().then(setHotspots);
    }, []);
    console.log(hotspots);
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-xl font-bold mb-4">
        Hotspot Map
      </h2>

      <MapContainer
        center={[12.97, 77.59]}
        zoom={11}
        style={{
          height: "400px",
          width: "100%",
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {hotspots.map((spot: any, index) => (
          <CircleMarker
            key={index}
            center={[
              Number(spot.avg_lat),
              Number(spot.avg_lon),
            ]}
            radius={10}
          >
            <Popup>
              <b>{spot.police_station}</b>

              <br />

              Violations: {spot.violations}

              <br />

              Junction: {spot.top_junction}
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}