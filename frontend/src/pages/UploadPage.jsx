import { UploadCloud } from "lucide-react";
import React, { useState } from "react";
import { uploadDocument } from "../lib/api.js";

export default function UploadPage() {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setLoading(true);
    setStatus("");
    try {
      const data = await uploadDocument(file);
      setStatus(`${data.filename} indexed with ${data.chunks_added} chunks.`);
    } catch (err) {
      setStatus(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="grid gap-5">
      <div>
        <h2 className="text-2xl font-semibold">Upload documents</h2>
        <p className="mt-1 text-sm text-zinc-600">Add PDF, TXT, or Markdown files to the FAISS knowledge base.</p>
      </div>
      <label className="grid cursor-pointer place-items-center rounded border border-dashed border-zinc-300 bg-white px-6 py-16 text-center hover:border-emerald-600">
        <UploadCloud className="mb-3 text-emerald-600" size={34} />
        <span className="text-base font-semibold">{loading ? "Indexing document" : "Choose a document"}</span>
        <span className="mt-1 text-sm text-zinc-500">PDF, TXT, or MD</span>
        <input type="file" accept=".pdf,.txt,.md" className="hidden" onChange={handleUpload} />
      </label>
      {status && <p className="rounded border border-zinc-200 bg-white p-3 text-sm text-zinc-700">{status}</p>}
    </section>
  );
}
