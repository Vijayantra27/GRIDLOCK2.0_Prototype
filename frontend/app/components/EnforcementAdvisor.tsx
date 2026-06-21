"use client";

import {
  useEffect,
  useState
} from "react";

import {
  getAdvisor
} from "@/services/api";

export default function EnforcementAdvisor() {

  const [
    plan,
    setPlan
  ] = useState<any[]>([]);

  useEffect(() => {

    getAdvisor()
    .then(setPlan);

  }, []);

  return (

    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-2xl font-bold mb-4">

        🚨 AI Enforcement Plan

      </h2>

      {plan.map((item,index)=>(

        <div
        key={index}
        className="
        border
        rounded
        p-4
        mb-3
        "
        >

          <h3 className="font-bold">

            {index+1}.
            {" "}
            {item.location}

          </h3>

          <p>

            Priority:
            {" "}
            {item.priority}

          </p>

          <p>

            Officers:
            {" "}
            {item.officers}

          </p>

          <p>

            Risk Score:
            {" "}
            {item.risk_score}

          </p>

          <p>

            Violations:
            {" "}
            {item.violations}

          </p>

        </div>

      ))}

    </div>
  );
}