"use client";

export default function Navbar() {
  return (
    <div className="bg-black text-white p-5 flex justify-between items-center">

      <div>
        <h1 className="text-3xl font-bold">
          GridLock AI
        </h1>

        <p className="text-sm text-gray-300">
          AI-Powered Parking Intelligence Platform
        </p>
      </div>

      <button
        onClick={() =>
          window.open(
            "http://127.0.0.1:8000/report",
            "_blank"
          )
        }
        className="bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-gray-200"
      >
        Export Report
      </button>

    </div>
  );
}