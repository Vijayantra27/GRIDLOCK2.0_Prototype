"use client";
import dynamic from "next/dynamic";
import Navbar from "./components/Navbar";
import StatCard from "./components/StatCard";
import RiskChart from "./components/RiskChart";
import HotspotTable from "./components/HotspotTable";
import OfficerAllocation from "./components/OfficerAllocation";
import ParkingDNA from "./components/ParkingDNA";
import SimulationPanel from "./components/SimulationPanel";
import AIAssistant from "./components/AIAssistant";
import TrafficNetwork from "./components/TrafficNetwork";
import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";
import EmergingHotspots from "./components/EmergingHotspots";
import ExecutiveSummary from "./components/ExecutiveSummary";
import KPIBanner from "./components/KPIBanner";
import PatrolPlanner from "./components/PatrolPlanner";
import AlertBanner from "./components/AlertBanner";

const HeatMap = dynamic(
  () => import("./components/HeatMap"),
  {
    ssr: false,
  }
);

const RouteMap = dynamic(
  () => import("./components/RouteMap"),
  {
    ssr: false,
  }
);


export default function Home() {
  const [stats, setStats] = useState<any>(null);
  const [selectedStationMap,
setSelectedStationMap] =
    useState<any>(null);

  useEffect(() => {
    getDashboard().then(setStats);
  }, []);

  const [geometry,setGeometry] = useState<any[]>([]);

  const [optimizedRoute,setOptimizedRoute] = useState<any[]>([]);
  return (
    <main className="bg-gray-100 min-h-screen">

      <Navbar />

      <div className="p-6">

        
        <div className="p-6">
          <AlertBanner />
        </div>

        <div className="mt-6">
          <KPIBanner />
        </div>


        <div>
          <HeatMap />

          <RiskChart />

        </div>

        <div className="mt-6">
          <RouteMap
            routeData={optimizedRoute}
            geometry={geometry}
            selectedStation={
              selectedStationMap
            }
          />
        </div>

        <div className="mt-6">
          <PatrolPlanner
            setOptimizedRoute={
              setOptimizedRoute
            }
            setGeometry={
              setGeometry
            }
            setSelectedStationMap={
              setSelectedStationMap
            }
          />
        </div>
        
        

        <div className="bg-white p-4 rounded-xl shadow">

          <h2 className="text-xl font-bold mb-4">
            Top Hotspots
          </h2>

          <div className="max-h-80 overflow-y-auto">

            <HotspotTable />

          </div>

        </div>

        <div className="mt-6">
          <SimulationPanel />
        </div>

        <div className="bg-white p-4 rounded-xl shadow">

          <h2 className="text-xl font-bold mb-4">
            Emerging Hotspots
          </h2>

          <div className="max-h-80 overflow-y-auto">

            <EmergingHotspots />

          </div>

        </div>

        <div className="mt-6">
          <AIAssistant />
        </div>

        <div className="mt-6">
          <TrafficNetwork />
        </div>
      </div>

    </main>
  );
}