"use client";

import { useEffect, useState } from "react";
import { getDNA } from "../../services/api";

export default function ParkingDNA() {

  const [dna, setDNA] = useState<any[]>([]);

  useEffect(() => {

    getDNA()
      .then((data) => {

        console.log("DNA Data:", data);

        if (Array.isArray(data)) {
          setDNA(data);
        } else {
          setDNA([]);
        }

      })
      .catch((err) => {
        console.error(err);
        setDNA([]);
      });

  }, []);

  const getProfile = (item: any) => {

    const violations =
      Number(item?.violations || 0);

    if (violations > 50000) {
      return {
        type: "🚨 Chronic Offender Zone",
        risk: "Critical",
        action: "Immediate Enforcement",
        color:
          "border-red-500 bg-red-50",
      };
    }

    if (violations > 20000) {
      return {
        type: "⚠ High Activity Zone",
        risk: "High",
        action: "Frequent Patrols",
        color:
          "border-orange-500 bg-orange-50",
      };
    }

    return {
      type: "✅ Stable Zone",
      risk: "Moderate",
      action: "Routine Monitoring",
      color:
        "border-green-500 bg-green-50",
    };

  };

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <div className="flex justify-between items-center mb-4">

        <h2 className="text-2xl font-bold">
          🧬 Parking Behavior Intelligence
        </h2>

        <span
          className="
          bg-blue-100
          text-blue-700
          px-3
          py-1
          rounded-full
          text-sm
          "
        >
          AI Profiles
        </span>

      </div>

      {dna.length === 0 ? (

        <div
          className="
          bg-slate-50
          p-6
          rounded-lg
          text-center
          text-gray-500
          "
        >
          No parking profiles available
        </div>

      ) : (

        <>

          <div className="space-y-4 max-h-96 overflow-y-auto">

            {dna.map(
              (item: any, index) => {

                const profile =
                  getProfile(item);

                return (

                  <div
                    key={index}
                    className={`
                    border-l-4
                    rounded-lg
                    p-4
                    ${profile.color}
                    `}
                  >

                    <div className="flex justify-between">

                      <div>

                        <h3 className="font-bold text-lg">

                          {item.police_station}

                        </h3>

                        <p className="text-sm mt-1">

                          {profile.type}

                        </p>

                      </div>

                      <div className="text-right">

                        <div className="font-bold">

                          {profile.risk}

                        </div>

                        <div className="text-sm">

                          Risk Level

                        </div>

                      </div>

                    </div>

                    <div className="grid grid-cols-2 gap-4 mt-4">

                      <div>

                        <p className="text-sm text-gray-600">

                          Violations

                        </p>

                        <p className="font-bold">

                          {Number(
                            item?.violations || 0
                          ).toLocaleString()}

                        </p>

                      </div>

                      <div>

                        <p className="text-sm text-gray-600">

                          Recommended Action

                        </p>

                        <p className="font-bold">

                          {profile.action}

                        </p>

                      </div>

                    </div>

                  </div>

                );

              }
            )}

          </div>

          <div
            className="
            mt-6
            bg-slate-100
            p-4
            rounded-lg
            "
          >

            <h3 className="font-bold mb-2">

              🧠 AI Insight

            </h3>

            <p>

              The system has identified
              parking behavior patterns
              across police jurisdictions.
              High violation zones should
              receive increased patrol
              frequency and enforcement
              resources.

            </p>

          </div>

        </>

      )}

    </div>

  );

}