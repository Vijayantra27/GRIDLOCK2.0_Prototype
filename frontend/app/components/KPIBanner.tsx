"use client";

import { useEffect, useState } from "react";
import { getDashboard } from "@/services/api";

export default function KPIBanner() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    getDashboard().then(setStats);
  }, []);

  return (
    <div className="grid grid-cols-4 gap-4">

      <div className="bg-red-500 text-white p-6 rounded-xl">
        <p>Total Violations</p>
        <h1 className="text-3xl font-bold">
          {stats?.violations || 0}
        </h1>
      </div>

      <div className="bg-orange-500 text-white p-6 rounded-xl">
        <p>Hotspots</p>
        <h1 className="text-3xl font-bold">
          {stats?.hotspots || 0}
        </h1>
      </div>

      <div className="bg-blue-500 text-white p-6 rounded-xl">
        <p>Police Stations</p>
        <h1 className="text-3xl font-bold">
          {stats?.police_stations || 0}
        </h1>
      </div>

      <div className="bg-green-500 text-white p-6 rounded-xl">
        <p>High Risk Zones</p>
        <h1 className="text-3xl font-bold">
          {stats?.high_risk || 0}
        </h1>
      </div>

    </div>
  );
}