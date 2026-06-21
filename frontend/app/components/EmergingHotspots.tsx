"use client";

import { useEffect, useState } from "react";
import { getEmerging } from "@/services/api";

export default function EmergingHotspots() {

  const [data, setData] =
    useState<any[]>([]);

  useEffect(() => {
    getEmerging().then(setData);
  }, []);

  return (
    <div className="bg-white p-4 rounded-xl shadow">

      <table className="w-full">

        <thead>
          <tr>
            <th>Station</th>
            <th>Growth %</th>
          </tr>
        </thead>

        <tbody>

          {data.map((row, index) => (

            <tr
              key={index}
              className="border-b"
            >

              <td>
                {row.police_station}
              </td>

              <td>
                {Number(
                  row.growth_percent
                ).toFixed(2)}%
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}