import React from "react";

export default function SourceList({ sources = [] }) {
  if (!sources.length) {
    return <p className="text-sm text-zinc-500">No sources returned yet.</p>;
  }

  return (
    <div className="grid gap-3">
      {sources.map((source, index) => (
        <article key={`${source.source}-${index}`} className="rounded border border-zinc-200 bg-white p-4">
          <div className="mb-2 flex items-center justify-between gap-3">
            <h3 className="text-sm font-semibold text-zinc-900">{source.source}</h3>
            <span className="rounded bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700">
              {source.score.toFixed(3)}
            </span>
          </div>
          <p className="line-clamp-4 text-sm leading-6 text-zinc-600">{source.text}</p>
        </article>
      ))}
    </div>
  );
}
