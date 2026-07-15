import React from "react";

export default function HistoryPage({ items }) {
  return (
    <section className="grid gap-5">
      <div>
        <h2 className="text-2xl font-semibold">History</h2>
        <p className="mt-1 text-sm text-zinc-600">Recent questions and analyses from this browser session.</p>
      </div>
      <div className="grid gap-3">
        {items.length === 0 && (
          <article className="rounded border border-zinc-200 bg-white p-5 text-sm text-zinc-500">
            No history yet.
          </article>
        )}
        {items.map((item, index) => (
          <article key={`${item.type}-${index}`} className="rounded border border-zinc-200 bg-white p-5">
            <div className="mb-2 flex items-center justify-between gap-3">
              <h3 className="text-sm font-semibold">{item.type}</h3>
              <span className="text-xs text-zinc-500">{item.sources.length} sources</span>
            </div>
            <p className="mb-3 text-sm text-zinc-600">{item.input}</p>
            <pre className="max-h-40 overflow-auto whitespace-pre-wrap rounded bg-zinc-50 p-3 text-xs leading-5 text-zinc-700">
              {item.answer}
            </pre>
          </article>
        ))}
      </div>
    </section>
  );
}
