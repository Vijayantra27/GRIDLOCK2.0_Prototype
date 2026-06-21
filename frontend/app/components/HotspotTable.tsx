import { getHotspots } from "@/services/api";
import { useEffect, useState } from "react";

export default function HotspotTable() {
  const [hotspots, setHotspots] = useState<any[]>([]);

  useEffect(() => {
    getHotspots().then(setHotspots);
  }, []);
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <table className="w-full">

        <tbody>

          {hotspots.map((hotspot) => (

          <tr
            key={hotspot.cluster}
            className="border-b"
          >

          <td className="py-2">
            {hotspot.police_station}
          </td>

          <td className="py-2">
            {hotspot.top_junction}
          </td>

          <td className="py-2">
            {hotspot.violations}
          </td>

          </tr>

          ))}

        </tbody>

        <tbody>

          {hotspots.map((hotspot) => (

            <tr
              key={hotspot.cluster}
              className="border-b"
            >

              <td className="py-2">
                {hotspot.cluster}
              </td>

              <td className="py-2">
                {hotspot.violations}
              </td>

              <td className="py-2">
                {hotspot.police_station}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}