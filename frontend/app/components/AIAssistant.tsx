"use client";

import { useState } from "react";
import { askAssistant } from "@/services/api";

export default function AIAssistant() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {

    if (!question.trim()) return;

    setLoading(true);

    try {

      const result = await askAssistant(
        question
      );

      setAnswer(result.answer);

    } catch (error) {

      setAnswer(
        "Unable to fetch AI insights."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow">

      <h2 className="text-2xl font-bold mb-4">
        AI Traffic Assistant
      </h2>

      <input
        type="text"
        placeholder="Ask about hotspots, patrols, risk zones..."
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        className="border p-3 w-full rounded"
      />

      <button
        onClick={handleAsk}
        className="bg-black text-white px-4 py-2 rounded mt-3"
      >
        Ask AI
      </button>

      {loading && (
        <div className="mt-4">
          Thinking...
        </div>
      )}

      {answer && (
        <div className="mt-4 border p-4 rounded-lg bg-gray-50">
          {answer}
        </div>
      )}

    </div>
  );
}