"use client";

import { getRisk } from "@/services/api";
import { useEffect, useState } from "react";

export default function RiskChart() {

  const [data, setData] = useState<any[]>([]);

  useEffect(() => {

    getRisk().then((riskData) => {
      setData(riskData);
    });

  }, []);

  if (data.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl shadow">
        Loading...
      </div>
    );
  }

  const avgRisk =
    data.reduce(
      (sum, item) =>
        sum + Number(item.risk_score),
      0
    ) / data.length;

  const readinessScore =
    Math.max(
      0,
      Math.min(
        100,
        Math.floor(
          100 - avgRisk
        )
      )
    );

  const criticalZones =
    data.filter(
      (d) =>
        Number(d.risk_score) > 60
    ).length;

  const highRiskZones =
    data.filter(
      (d) =>
        Number(d.risk_score) > 40
    ).length;

  const officersNeeded =
    Math.max(
      4,
      Math.ceil(
        highRiskZones * 7.5
      )
    );

  const status =
    readinessScore > 75
      ? "Operational"
      : readinessScore > 50
      ? "Needs Attention"
      : "Critical";

  const statusColor =
    readinessScore > 75
      ? "text-green-600"
      : readinessScore > 50
      ? "text-orange-500"
      : "text-red-600";

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-2xl font-bold mb-6">

        🚔 Patrol Readiness Center

      </h2>

      <div className="flex justify-center">

        <div
          className="
          w-44
          h-44
          rounded-full
          border-[12px]
          border-blue-500
          flex
          flex-col
          justify-center
          items-center
          "
        >

          <div className="text-5xl font-bold">

            {readinessScore}

          </div>

          <div className="text-sm text-gray-500">

            /100

          </div>

        </div>

      </div>

      <div className="text-center mt-4">

        <div
          className={`font-bold text-xl ${statusColor}`}
        >

          {status}

        </div>

      </div>

      <div className="grid grid-cols-2 gap-4 mt-8">

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">

            Critical Zones

          </h3>

          <p className="text-3xl font-bold text-red-600">

            {criticalZones}

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">

            Major Risk Zones

          </h3>

          <p className="text-3xl font-bold text-orange-500">

            {highRiskZones}

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">

            Avg Risk Score

          </h3>

          <p className="text-3xl font-bold">

            {avgRisk.toFixed(1)}

          </p>

        </div>

        <div className="border rounded-lg p-4">

          <h3 className="text-gray-500">

            Officers Needed

          </h3>

          <p className="text-3xl font-bold text-blue-600">

            {officersNeeded}

          </p>

        </div>

      </div>

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

          Current patrol readiness is

          {" "}

          <b>{readinessScore}%</b>.

        </p>

        <p className="mt-2">

          Deploy approximately

          {" "}

          <b>{officersNeeded}</b>

          {" "}

          officers across

          {" "}

          <b>{highRiskZones}</b>

          {" "}

          active hotspots to improve
          traffic flow and reduce
          parking-related congestion.

        </p>

      </div>

    </div>

  );

}