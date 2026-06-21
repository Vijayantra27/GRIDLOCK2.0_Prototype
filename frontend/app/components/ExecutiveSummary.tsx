"use client";

import { useEffect, useState } from "react";
import { getDashboard } from "@/services/api";

export default function ExecutiveSummary() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    getDashboard().then(setStats);
  }, []);

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-2xl font-bold mb-4">
        AI Executive Summary
      </h2>

      <ul className="space-y-2">
        <li>
          🚨 Total Violations: {stats?.violations}
        </li>

        <li>
          📍 Hotspots Identified: {stats?.hotspots}
        </li>

        <li>
          ⚠️ High Risk Zones: {stats?.high_risk}
        </li>

        <li>
          👮 Active Police Stations: {stats?.police_stations}
        </li>

        <li>
          📈 Recommended Action:
          Prioritize Cluster 2 (Upparpet)
        </li>
      </ul>
    </div>
  );
}