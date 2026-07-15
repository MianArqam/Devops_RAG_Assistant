import hashlib
import math
from typing import Protocol


class EmbeddingProvider(Protocol):
    dimension: int

    def encode(self, texts: list[str]) -> list[list[float]]:
        ...


class HashEmbeddingProvider:
    dimension = 384

    def encode(self, texts: list[str]) -> list[list[float]]:
        return [self._encode_one(text) for text in texts]

    def _encode_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for token in text.lower().split():
            digest = hashlib.md5(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "little") % self.dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]


class SentenceTransformerProvider:
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()


def create_embedding_provider(model_name: str) -> EmbeddingProvider:
    try:
        return SentenceTransformerProvider(model_name)
    except Exception:
        return HashEmbeddingProvider()
