"use client";

import { useEffect, useState } from "react";
import Select from "react-select";
import { getHotspots } from "@/services/api";
import { optimizeRoute } from "@/services/api";
import {
 getRecommendations
}
from "@/services/api";
import {
  getCoverage
} from "@/services/api";
export default function PatrolPlanner({
  setOptimizedRoute,
  setGeometry,
  setSelectedStationMap
}: any) {
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [selected, setSelected] = useState<any[]>([]);
  const [selectedStation, setSelectedStation] = useState<any>(null);
  useEffect(() => {
    getHotspots().then(setHotspots);
  }, []);

  const [result, setResult] = useState<any>(null);

  const [coverageData,setCoverageData] = useState<any[]>([]);

  const options = hotspots.map((spot) => ({
    value: spot.cluster,
    label: `${spot.police_station} (${spot.violations})`,
    data: spot,
  }));

  const stationOptions = [
    ...new Map(
        hotspots.map((spot) => [
        spot.police_station,
        {
            value: spot.cluster,
            label: spot.police_station,
            data: spot,
        },
        ])
    ).values(),
    ];

  const totalViolations = selected.reduce(
    (sum: number, item: any) =>
      sum + Number(item.data.violations),
    0
  );

  

  const coverageScore =
  Math.min(
    100,
    selected.length * 15
  );

  const recommendedOfficers =
  Math.max(
    2,
    Math.ceil(
      totalViolations / 15000
    )
  );
  const patrolCars =
  Math.max(
    1,
    Math.ceil(
      recommendedOfficers / 4
    )
  );
  const congestionReduction =
  Math.min(
    40,
    Math.round(
      coverageScore * 0.25
    )
  );

  const buildTimeline = () => {

  if (!result?.route)
    return [];

  let currentHour = 8;
  let currentMinute = 0;

  const stopTime =
  Math.max(
    5,
    Math.round(
      Number(
        result.duration_min || 30
      ) /
      result.route.length
    )
  );

  return result.route.map(
    (
      stop:any,
      index:number
    ) => {

      const time =
      `${String(
        currentHour
      ).padStart(2,"0")}:${String(
        currentMinute
      ).padStart(2,"0")}`;

      currentMinute += stopTime;

      while (
        currentMinute >= 60
      ) {
        currentHour += 1;
        currentMinute -= 60;
      }

      return {
        time,
        station:
        stop.station
      };
    }
  );
};

const patrolTimeline =
buildTimeline();

  const fuelEstimate =
  result
  ? Number(
      result.distance_km
    ).toFixed(1)
  : 0;

  const priority =
  totalViolations > 100000
  ? "HIGH"
  : totalViolations > 50000
  ? "MEDIUM"
  : "LOW";
  return (
    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-2xl font-bold mb-4">
        Smart Patrol Planner
      </h2>

        <div className="grid grid-cols-2 gap-4 mb-4">

    <div>
        <label className="font-bold block mb-2">
        Starting Police Station
        </label>

        <Select
        options={stationOptions}
        value={selectedStation}
        onChange={(station:any)=>{

          setSelectedStation(
            station
          );

          setSelectedStationMap(
            station?.data
          );

        }}
        placeholder="Choose station..."
        />
    </div>
    <button
        className="bg-green-600 text-white px-4 py-2 rounded"
        onClick={async()=>{

        if(!selectedStation) return;

        const recs =
        await getRecommendations(
        selectedStation.value
        );

        const formatted =
        recs.map((r:any)=>({
        value:r.cluster,
        label:
        `${r.police_station}
        (${r.violations})`,
        data:r
        }));

        setSelected(formatted);

        }}
        >
        🚔 Auto Recommend
        </button>

    <div>
        <label className="font-bold block mb-2">
        Patrol Hotspots
        </label>

        <Select
        isMulti
        options={options}
        placeholder="Search hotspots..."
        onChange={(items: any) =>
            setSelected(items || [])
        }
        />
    </div>

    </div>

      <div className="mt-6">

        <h3 className="font-bold mb-3">
          Selected Locations
        </h3>

        {selected.map((item: any) => (
          <div
            key={item.value}
            className="border rounded p-2 mb-2"
          >
            <div>
              <b>
                {item.data.police_station}
              </b>

              <div className="text-sm text-gray-500">
                Violations:
                {item.data.violations}
              </div>

              {item.data.distance && (
                <div className="text-sm text-gray-500">
                  Distance:
                  {Number(
                    item.data.distance
                  ).toFixed(2)}
                  km
                </div>
              )}
            </div>
          </div>
        ))}

      </div>

      <div className="grid grid-cols-3 gap-4 mt-6">

        <div className="border rounded p-4">
          <h4>Hotspots Covered</h4>
          <p className="text-2xl font-bold">
            {selected.length}
          </p>
        </div>

        <div className="border rounded p-4">
          <h4>Violations Covered</h4>
          <p className="text-2xl font-bold">
            {totalViolations.toLocaleString()}
          </p>
        </div>

        <div className="border rounded p-4">
          <h4>Estimated Officers</h4>
          <p className="text-2xl font-bold">
            {Math.ceil(selected.length * 1.5)}
          </p>
        </div>

      </div>

      <button
            disabled={
                !selectedStation ||
                selected.length === 0
            }
            onClick={async () => {

                const clusters =
                selected.map(
                    (s: any) =>
                    s.data.cluster
                );
                
                if (!selectedStation) return;
                const response =
                await optimizeRoute(
                    clusters,
                    selectedStation.value
                );

                setOptimizedRoute(
                    response.route
                );

                setGeometry(
                    response.geometry
                );

                setResult(response);

                const coverage =
                await getCoverage(
                  clusters
                );

                setCoverageData(
                  coverage
                );
            }}
            className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg disabled:opacity-50"
        >
            Generate Optimal Route
        </button>

        
        {result && (

            <div className="mt-6 border p-4 rounded">
                <div className="grid grid-cols-4 gap-4 mb-6">

                    <div className="border rounded p-3">
                        <h4>Stops</h4>
                        <p className="text-2xl font-bold">
                        {result.route.length}
                        </p>
                    </div>

                    <div className="border rounded p-3">
                        <h4>Distance</h4>
                        <p className="text-2xl font-bold">
                        {result.distance_km}
                        </p>
                    </div>

                    <div className="border rounded p-3">
                        <h4>Coverage</h4>
                        <p className="text-2xl font-bold">
                        {Math.min(selected.length * 15,100)}%
                        </p>
                    </div>

                    <div className="border rounded p-3">
                        <h4>Violations</h4>
                        <p className="text-2xl font-bold">
                        {totalViolations.toLocaleString()}
                        </p>
                    </div>

                </div>

                <div className="
                  grid
                  grid-cols-5
                  gap-4
                  mb-6
                  ">

                    <div className="
                    bg-blue-50
                    p-4
                    rounded-lg
                    ">

                      <h4>
                        Officers
                      </h4>

                      <p className="
                      text-2xl
                      font-bold
                      ">

                        {recommendedOfficers}

                      </p>

                    </div>

                    <div className="
                    bg-green-50
                    p-4
                    rounded-lg
                    ">

                      <h4>
                        Patrol Cars
                      </h4>

                      <p className="
                      text-2xl
                      font-bold
                      ">

                        {patrolCars}

                      </p>

                    </div>

                    <div className="
                    bg-yellow-50
                    p-4
                    rounded-lg
                    ">

                      <h4>
                        Distance
                      </h4>

                      <p className="
                      text-2xl
                      font-bold
                      ">

                        {fuelEstimate}
                        km

                      </p>

                    </div>

                    <div className="
                    bg-purple-50
                    p-4
                    rounded-lg
                    ">

                      <h4>
                        Coverage
                      </h4>

                      <p className="
                      text-2xl
                      font-bold
                      ">

                        {coverageScore}%

                      </p>

                    </div>

                    <div className="
                    bg-red-50
                    p-4
                    rounded-lg
                    ">

                      <h4>
                        Reduction
                      </h4>

                      <p className="
                      text-2xl
                      font-bold
                      ">

                        {congestionReduction}%

                      </p>

                    </div>

                </div>

                <div
                  className="
                  mb-6
                  bg-indigo-50
                  border-l-4
                  border-indigo-500
                  p-4
                  rounded
                  "
                  >

                  <h3 className="
                  font-bold
                  text-lg
                  mb-2
                  ">

                  🎯 Operational Recommendation

                  </h3>

                  <div
                    className="
                    mb-6
                    bg-white
                    border
                    rounded-xl
                    p-4
                    "
                    >

                    <h3
                    className="
                    font-bold
                    text-lg
                    mb-3
                    "
                    >

                    📍 Patrol Timeline

                    </h3>

                    {
                    patrolTimeline.map(
                    (
                    item:any,
                    index:number
                    )=>(

                    <div
                    key={index}
                    className="
                    flex
                    justify-between
                    border-b
                    py-2
                    "
                    >

                    <span>

                    🕒 {item.time}

                    </span>

                    <span>

                    {index+1}.
                    {" "}
                    {item.station}

                    </span>

                    </div>

                    ))
                    }

                    </div>

                  <p>

                  Deploy
                  {" "}
                  <b>
                  {recommendedOfficers}
                  </b>
                  {" "}
                  officers using
                  {" "}
                  <b>
                  {patrolCars}
                  </b>
                  {" "}
                  patrol vehicles.

                  </p>

                  <p className="mt-2">

                  Expected congestion reduction:

                  <b>
                  {" "}
                  {congestionReduction}%
                  </b>

                  </p>

                </div>

                <h3 className="font-bold mb-2">
                    🚔 Patrol Route
                </h3>

                <div className="mt-6 bg-yellow-50 p-4 rounded-xl border">

                  <h3 className="font-bold text-xl mb-3">
                    🧠 AI Route Assessment
                  </h3>

                  <p>
                    Coverage Score:
                    {coverageScore}%
                  </p>

                  <p>
                    Recommended Officers:
                    {recommendedOfficers}
                  </p>

                  <p>
                    Expected Congestion Reduction:
                    {congestionReduction}%
                  </p>

                  <p>
                    Priority:
                    {priority}
                  </p>

                  <p className="mt-3 text-sm text-gray-700">

                    This patrol route covers
                    {selected.length}
                    high-risk locations and
                    approximately
                    {" "}
                    {totalViolations.toLocaleString()}
                    {" "}
                    violations.

                  </p>

                </div>
                <p className="text-sm text-gray-500 mb-3">
                    Starting Station:
                    {selectedStation?.label}
                </p>

                {result.route.map(
                (r: any, i: number) => (
                    <div key={i}>
                    {i + 1}. {r.station}
                    </div>
                )
                )}

                <div className="mt-4">

                Distance:
                {result.distance_km} km

                </div>

                <div>

                Estimated Time:
                {result.duration_min} min

                </div>

                <div className="mt-2">
                    Stops:
                    {result.route.length}
                </div>


                <div>
                    Coverage:
                    {totalViolations.toLocaleString()}
                    violations
                </div>
            </div>

        )}
        {
          coverageData.length > 0 && (

          <div className="
          mt-6
          bg-red-50
          p-4
          rounded-xl
          ">

          <h3 className="
          font-bold
          text-xl
          mb-3
          ">

          🎯 Coverage Gap Analysis

          </h3>

          {
          coverageData.map(
          (item:any)=>(

          <div
          key={item.cluster}
          className="
          border-b
          py-2
          "
          >

          🔴 Cluster:
          {item.cluster}

          <br />

          Risk Score:
          {Number(
          item.risk_score
          ).toFixed(2)}

          </div>

          ))
          }

          </div>

          )}
    </div>
  );
}