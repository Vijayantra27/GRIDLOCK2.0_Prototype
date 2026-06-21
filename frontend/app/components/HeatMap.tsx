"use client";

import { useEffect, useState } from "react";
import { getHotspots, getImpact } from "@/services/api";
import {
  getOfficerRecommendation
} from "@/services/api";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

export default function HeatMap() {

  const [hotspots, setHotspots] =
    useState<any[]>([]);
  
  const [recommendation,setRecommendation] = useState<any>(null);
  useEffect(() => {
    getHotspots().then(setHotspots);
  }, []);

  const [impactData, setImpactData] =
useState<any>(null);

  return (
    <div className="bg-white p-4 rounded-xl shadow">

      <h2 className="text-xl font-bold mb-4">
        Bengaluru Risk Heatmap
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

        {hotspots.map((spot, index) => {

          let color = "green";

          if (spot.violations > 50000)
            color = "red";
          else if (spot.violations > 20000)
            color = "orange";
          else
            color = "yellow";

          return (
            <CircleMarker
              key={index}
              center={[
                Number(spot.avg_lat),
                Number(spot.avg_lon),
              ]}
              radius={12}
              pathOptions={{
                color,
                fillColor: color,
                fillOpacity: 0.7,
              }}
            >
              <Popup>

                <b>
                {spot.police_station}
                </b>

                <br />

                Violations:
                {spot.violations}

                <br />

                <button
                className="
                mt-2
                bg-blue-600
                text-white
                px-3
                py-1
                rounded
                "
                onClick={async()=>{

                const data =
                await getOfficerRecommendation(
                  spot.cluster
                );

                setRecommendation(
                  data
                );

                }}
                >

                Recommend Officers

                </button>

                <button
                  className="
                  mt-2
                  bg-red-600
                  text-white
                  px-3
                  py-1
                  rounded
                  "
                  onClick={async()=>{

                  const impact =
                  await getImpact(
                    spot.cluster
                  );

                  setImpactData(
                    impact
                  );

                  }}
                  >

                  Predict Impact

                  </button>

              </Popup>
            </CircleMarker>
          );
        })}

      </MapContainer>
      {
      recommendation && (

      <div
      className="
      mt-4
      bg-white
      p-4
      rounded-xl
      shadow
      "
      >

      <h2
      className="
      text-xl
      font-bold
      mb-2
      "
      >

      🚔 Patrol Recommendation

      </h2>

      <p>

      Cluster:
      {recommendation.cluster}

      </p>

      <p>

      Violations:
      {recommendation.violations}

      </p>

      <p>

      Risk Score:
      {recommendation.risk_score}

      </p>

      <p>

      Priority:
      {recommendation.priority}

      </p>

      <p>

      Frequency:
      {recommendation.frequency}

      </p>

      <p
      className="
      text-2xl
      font-bold
      text-red-600
      mt-2
      "
      >

      Recommended Officers:
      {
      recommendation.recommended_officers
      }

      </p>

      </div>

      )}
      {
        impactData && (

        <div
        className="
        mt-4
        bg-red-50
        p-4
        rounded-xl
        shadow
        border-l-4
        border-red-500
        "
        >

        <h2 className="text-xl font-bold mb-2">
        🚨 Impact Prediction
        </h2>

        <p>
        <b>Cluster:</b>
        {" "}
        {impactData.cluster}
        </p>

        <p>
        <b>Expected Congestion Growth:</b>
        {" "}
        +{impactData.congestion_growth}%
        </p>

        <p>
        <b>Spillover Violations:</b>
        {" "}
        +{impactData.spillover}%
        </p>

        <p>
        <b>Affected Roads:</b>
        {" "}
        {impactData.affected_roads}
        </p>

        <b>
          Potentially Impacted Roads:
        </b>

        <ul className="list-disc ml-6 mt-2">

          {impactData.roads?.map(
            (road:string,index:number)=>(

              <li key={index}>
                {road}
              </li>

            )
          )}

        </ul>

        </div>

        )}
    </div>
  );
}