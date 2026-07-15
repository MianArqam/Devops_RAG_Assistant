import { Send } from "lucide-react";
import React, { useState } from "react";
import SourceList from "../components/SourceList.jsx";
import { chat } from "../lib/api.js";

export default function ChatPage({ onHistory }) {
  const [query, setQuery] = useState("Error: AccessDenied: User is not authorized to perform s3:PutObject");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await chat(query);
      setResult(data);
      onHistory({ type: "Chat", input: query, answer: data.answer, sources: data.sources });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="grid gap-5">
      <div>
        <h2 className="text-2xl font-semibold">Chat with documentation</h2>
        <p className="mt-1 text-sm text-zinc-600">Paste an AWS, Docker, or Kubernetes error and retrieve likely fixes.</p>
      </div>
      <form onSubmit={handleSubmit} className="rounded border border-zinc-200 bg-white p-4">
        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="min-h-32 w-full resize-y rounded border border-zinc-300 p-3 text-sm outline-none focus:border-emerald-600"
        />
        <div className="mt-3 flex justify-end">
          <button className="inline-flex items-center gap-2 rounded bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700">
            <Send size={16} />
            {loading ? "Thinking" : "Ask"}
          </button>
        </div>
      </form>
      {error && <p className="rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</p>}
      {result && (
        <div className="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <article className="rounded border border-zinc-200 bg-white p-5">
            <h3 className="mb-3 text-base font-semibold">Answer</h3>
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
