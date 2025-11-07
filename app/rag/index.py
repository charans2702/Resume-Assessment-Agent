from __future__ import annotations

import faiss
import numpy as np
import os
from app.utils.config import settings
from app.utils.gemini import embed_texts


class VectorIndex:
    def __init__(self) -> None:
        self.dim: int | None = None
        self.index: faiss.IndexFlatIP | None = None
        self.corpus: list[str] = []
        self._load_if_exists()

    def _load_if_exists(self) -> None:
        path = settings.vector_index_path
        if os.path.exists(path):
            faiss.read_index(path)

    def add(self, texts: list[str]) -> None:
        if not texts:
            return
        embeddings = embed_texts(texts)
        # Initialize index lazily based on first vector dimension
        if self.index is None:
            self.dim = len(embeddings[0])
            self.index = faiss.IndexFlatIP(self.dim)
        # Normalize for cosine similarity
        arr = np.array(embeddings, dtype="float32")
        norms = np.linalg.norm(arr, axis=1, keepdims=True) + 1e-12
        arr = arr / norms
        self.index.add(arr)  # type: ignore[arg-type]
        self.corpus.extend(texts)

    def search(self, query: str, top_k: int = 5) -> list[str]:
        if self.index is None or self.index.ntotal == 0:
            return []
        q = embed_texts([query])[0]
        q = np.array([q], dtype="float32")
        q = q / (np.linalg.norm(q, axis=1, keepdims=True) + 1e-12)
        D, I = self.index.search(q, top_k)  # type: ignore[arg-type]
        return [self.corpus[i] for i in I[0] if i < len(self.corpus)]


vector_index = VectorIndex()


