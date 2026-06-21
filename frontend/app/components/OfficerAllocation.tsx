"use client";

import { useEffect, useState } from "react";
import { getOfficers } from "../../services/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";


export default function OfficerAllocation() {

    const [data, setData] = useState([]);
    useEffect(() => {
        getOfficers().then(setData);
    }, []);

  return (
    <div className="bg-white p-4 rounded-xl shadow">

      <h2 className="text-xl font-bold mb-4">
        Officer Allocation Plan
      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >
        <BarChart data={data}>
          <XAxis dataKey="cluster" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="allocated_officers" />
        </BarChart>
      </ResponsiveContainer>

    </div>
  );
}