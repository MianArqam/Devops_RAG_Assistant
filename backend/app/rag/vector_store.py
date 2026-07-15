import json
import math
from pathlib import Path
from threading import Lock

from app.core.config import settings
from app.rag.document_loader import iter_documents, read_document
from app.rag.embeddings import create_embedding_provider
from app.rag.text_splitter import split_text

try:
    import faiss
except Exception:
    faiss = None

try:
    import numpy as np
except Exception:
    np = None


class VectorStore:
    def __init__(self) -> None:
        self.embedder = create_embedding_provider(settings.embedding_model)
        self.storage_dir = settings.resolved_storage_dir
        self.index_path = self.storage_dir / "faiss.index"
        self.metadata_path = self.storage_dir / "metadata.json"
        self.vectors_path = self.storage_dir / "vectors.json"
        self.lock = Lock()
        self.metadata: list[dict[str, str]] = []
        self.vectors: list[list[float]] = []
        self.index = None
        self._load_or_create()

    @property
    def dimension(self) -> int:
        return self.embedder.dimension

    def _load_or_create(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        if faiss and self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            return
        loaded_vectors = False
        if self.vectors_path.exists() and self.metadata_path.exists():
            self.vectors = json.loads(self.vectors_path.read_text(encoding="utf-8"))
            self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            loaded_vectors = True
        if faiss:
            self.index = faiss.IndexFlatIP(self.dimension)
            if self.vectors and np is not None:
                self.index.add(np.asarray(self.vectors, dtype="float32"))
        if not loaded_vectors:
            self.metadata = []

    def save(self) -> None:
        if faiss and self.index is not None:
            faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.metadata, indent=2), encoding="utf-8")
        self.vectors_path.write_text(json.dumps(self.vectors), encoding="utf-8")

    def _embed(self, texts: list[str]) -> list[list[float]]:
        return self.embedder.encode(texts)

    def add_document(self, text: str, source: str) -> int:
        chunks = split_text(text)
        if not chunks:
            return 0

        vectors = self._embed(chunks)
        with self.lock:
            if faiss and self.index is not None and np is not None:
                self.index.add(np.asarray(vectors, dtype="float32"))
            self.vectors.extend(vectors)
            self.metadata.extend({"source": source, "text": chunk} for chunk in chunks)
            self.save()
        return len(chunks)

    def ingest_knowledge_base(self) -> int:
        total = 0
        for path in iter_documents(settings.resolved_knowledge_base_dir):
            text = read_document(path)
            source = str(path.relative_to(settings.resolved_knowledge_base_dir))
            total += self.add_document(text, source)
        return total

    def search(self, query: str, top_k: int | None = None) -> list[dict[str, str | float]]:
        if not self.metadata:
            return []

        k = min(top_k or settings.top_k, len(self.metadata))
        query_vector = self._embed([query])

        if faiss and self.index is not None and self.index.ntotal > 0 and np is not None:
            scores, indices = self.index.search(np.asarray(query_vector, dtype="float32"), k)
            pairs = zip(scores[0], indices[0], strict=False)
        else:
            scored = [
                (self._cosine_similarity(query_vector[0], vector), index)
                for index, vector in enumerate(self.vectors)
            ]
            pairs = sorted(scored, reverse=True)[:k]

        results: list[dict[str, str | float]] = []
        for score, index in pairs:
            if index < 0:
                continue
            item = self.metadata[index]
            results.append(
                {
                    "source": item["source"],
                    "text": item["text"],
                    "score": float(score),
                }
            )
        return results

    def count(self) -> int:
        return len(self.metadata)

    def _cosine_similarity(self, left: list[float], right: list[float]) -> float:
        dot = sum(a * b for a, b in zip(left, right, strict=False))
        left_norm = math.sqrt(sum(value * value for value in left)) or 1.0
        right_norm = math.sqrt(sum(value * value for value in right)) or 1.0
        return dot / (left_norm * right_norm)


vector_store = VectorStore()
