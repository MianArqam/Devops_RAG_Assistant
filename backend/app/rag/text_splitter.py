def split_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = max(end - overlap, start + 1)
    return chunks
