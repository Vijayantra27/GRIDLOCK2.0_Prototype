"use client";
import { useEffect, useState } from "react";
import { getPropagation } from "../../services/api";
import ReactFlow from "reactflow";
import "reactflow/dist/style.css";


export default function TrafficNetwork() {
    const [links, setLinks] = useState<any[]>([]);
    useEffect(() => {
        getPropagation().then(setLinks);
    }, []);
    const uniqueClusters = [
      ...new Set(
        links.flatMap((item: any) => [
          item.source_cluster,
          item.target_cluster,
        ])
      ),
    ];

    const nodes = uniqueClusters.map(
      (cluster: any, index: number) => ({
        id: String(cluster),
        position: {
          x: (index % 5) * 250,
          y: Math.floor(index / 5) * 150,
        },
        data: {
          label: `Cluster ${cluster}`,
        },
      })
    );

    const edges = links.map(
      (item: any, index: number) => ({
        id: `edge-${index}`,
        source: String(item.source_cluster),
        target: String(item.target_cluster),
        label: item.propagation_risk,
      })
    );
    console.log("Links:", links);
    console.log("Nodes:", nodes);
    console.log("Edges:", edges);
  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-xl font-bold mb-4">
        Traffic Propagation Network
      </h2>

      <div style={{ height: 500 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
        />
      </div>
    </div>
  );
}