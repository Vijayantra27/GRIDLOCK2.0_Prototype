"use client";

import { useEffect, useState } from "react";
import { getSimulation } from "@/services/api";

export default function SimulationPanel() {

  const [simulation, setSimulation] =
    useState<any>(null);

  const [officers, setOfficers] =
    useState(5);

  const [festival, setFestival] =
    useState(false);

  const [rain, setRain] =
    useState(false);

  const [weekend, setWeekend] =
    useState(false);

  useEffect(() => {

    getSimulation().then((data) => {
      setSimulation(data[0]);
    });

  }, []);

  if (!simulation)
    return null;

  let currentRisk =
    Number(simulation.current_risk);

  let predictedRisk =
    currentRisk;

  predictedRisk -=
    officers * 1.8;

  if (festival)
    predictedRisk += 12;

  if (rain)
    predictedRisk += 8;

  if (weekend)
    predictedRisk += 5;

  predictedRisk =
    Math.max(
      5,
      predictedRisk
    );

  const congestionReduction =
    Math.max(
      0,
      Math.round(
        (currentRisk -
          predictedRisk) *
          0.8
      )
    );

  const propagationReduction =
    Math.max(
      0,
      Math.round(
        (currentRisk -
          predictedRisk) *
          0.6
      )
    );

  const coverageScore =
    Math.min(
      100,
      officers * 8
    );

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-2xl font-bold mb-4">
        🚔 What-If Simulation Engine
      </h2>

      <p className="text-gray-600 mb-6">
        Simulate deployment strategies
        and predict traffic outcomes.
      </p>

      {/* Controls */}

      <div className="mb-6">

        <label className="font-bold block mb-2">

          Additional Officers:
          {" "}
          {officers}

        </label>

        <input
          type="range"
          min="0"
          max="20"
          value={officers}
          onChange={(e) =>
            setOfficers(
              Number(
                e.target.value
              )
            )
          }
          className="w-full"
        />

      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">

        <label className="border rounded p-3 cursor-pointer">

          <input
            type="checkbox"
            checked={festival}
            onChange={() =>
              setFestival(
                !festival
              )
            }
          />

          <span className="ml-2">
            🎉 Festival
          </span>

        </label>

        <label className="border rounded p-3 cursor-pointer">

          <input
            type="checkbox"
            checked={rain}
            onChange={() =>
              setRain(
                !rain
              )
            }
          />

          <span className="ml-2">
            🌧 Rain
          </span>

        </label>

        <label className="border rounded p-3 cursor-pointer">

          <input
            type="checkbox"
            checked={weekend}
            onChange={() =>
              setWeekend(
                !weekend
              )
            }
          />

          <span className="ml-2">
            📅 Weekend
          </span>

        </label>

      </div>

      {/* Metrics */}

      <div className="grid grid-cols-2 gap-4">

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">
            Current Risk
          </h3>

          <p className="text-3xl font-bold text-red-600">

            {currentRisk.toFixed(1)}

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">
            Predicted Risk
          </h3>

          <p className="text-3xl font-bold text-green-600">

            {predictedRisk.toFixed(1)}

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">
            Congestion Reduction
          </h3>

          <p className="text-3xl font-bold">

            {congestionReduction}%

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">
            Coverage Improvement
          </h3>

          <p className="text-3xl font-bold">

            {coverageScore}%

          </p>

        </div>

      </div>

      {/* Progress Bars */}

      <div className="mt-6">

        <h3 className="font-bold mb-2">

          Coverage Score

        </h3>

        <div className="bg-gray-200 rounded-full h-4">

          <div
            className="
            bg-green-500
            h-4
            rounded-full
            "
            style={{
              width:
                `${coverageScore}%`,
            }}
          />

        </div>

      </div>

      {/* AI Recommendation */}

      <div
        className="
        mt-6
        bg-blue-50
        border-l-4
        border-blue-500
        p-4
        rounded
        "
      >

        <h3 className="font-bold mb-2">

          🧠 AI Recommendation

        </h3>

        <p>

          Deploying
          {" "}
          <b>{officers}</b>
          {" "}
          officers is expected to:

        </p>

        <ul className="mt-2 list-disc pl-5">

          <li>
            Reduce congestion by
            {" "}
            {congestionReduction}%
          </li>

          <li>
            Improve hotspot coverage by
            {" "}
            {coverageScore}%
          </li>

          <li>
            Reduce risk propagation by
            {" "}
            {propagationReduction}%
          </li>

        </ul>

      </div>

    </div>

  );

}