import { ScanSearch } from "lucide-react";
import React, { useState } from "react";
import SourceList from "../components/SourceList.jsx";
import { analyzeLog } from "../lib/api.js";

export default function LogAnalysisPage({ onHistory }) {
  const [log, setLog] = useState("CrashLoopBackOff: back-off restarting failed container");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    const data = await analyzeLog(log);
    setResult(data);
    onHistory({ type: "Log", input: log, answer: data.answer, sources: data.sources });
    setLoading(false);
  }

  return (
    <section className="grid gap-5">
      <div>
        <h2 className="text-2xl font-semibold">Error analysis</h2>
        <p className="mt-1 text-sm text-zinc-600">Analyze raw logs and connect them to operational documentation.</p>
      </div>
      <form onSubmit={handleSubmit} className="rounded border border-zinc-200 bg-white p-4">
        <textarea
          value={log}
          onChange={(event) => setLog(event.target.value)}
          className="min-h-44 w-full resize-y rounded border border-zinc-300 bg-zinc-950 p-3 font-mono text-sm text-zinc-50 outline-none focus:border-emerald-600"
        />
        <div className="mt-3 flex justify-end">
          <button className="inline-flex items-center gap-2 rounded bg-zinc-900 px-4 py-2 text-sm font-semibold text-white hover:bg-zinc-800">
            <ScanSearch size={16} />
            {loading ? "Analyzing" : "Analyze"}
          </button>
        </div>
      </form>
      {result && (
        <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <article className="rounded border border-zinc-200 bg-white p-5">
            <h3 className="mb-3 text-base font-semibold">Diagnosis</h3>
            <pre className="whitespace-pre-wrap text-sm leading-6 text-zinc-700">{result.answer}</pre>
          </article>
          <div>
            <h3 className="mb-3 text-base font-semibold">Sources</h3>
            <SourceList sources={result.sources} />
          </div>
        </div>
      )}
    </section>
  );
}
