from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from ..config import settings


class SemanticIndex:
    """Simple TF-IDF backed semantic index for lesson materials."""

    def __init__(self, persist_path: str | Path | None = None):
        self.persist_path = Path(persist_path or settings.semantic_index_path)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.vectors: np.ndarray | None = None
        self.documents: list[dict] = []
        if self.persist_path.exists():
            self._load()

    def build(self, materials: Iterable[dict]) -> None:
        self.documents = list(materials)
        corpus = [doc.get("content_text", "") for doc in self.documents]
        if not corpus:
            self.vectors = None
            return
        self.vectors = self.vectorizer.fit_transform(corpus)
        self._save()

    def upsert(self, material: dict) -> None:
        existing_ids = {doc["id"]: idx for idx, doc in enumerate(self.documents)}
        if material["id"] in existing_ids:
            self.documents[existing_ids[material["id"]]] = material
        else:
            self.documents.append(material)
        self.build(self.documents)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        if not self.documents or self.vectors is None:
            return []
        query_vec = self.vectorizer.transform([query])
        similarities = (self.vectors @ query_vec.T).toarray().ravel()
        ranked = np.argsort(similarities)[::-1][:limit]
        return [self.documents[i] | {"score": float(similarities[i])} for i in ranked]

    def _save(self) -> None:
        payload = {
            "documents": self.documents,
            "vectorizer": self.vectorizer,
        }
        self.persist_path.write_bytes(pickle_dumps(payload))

    def _load(self) -> None:
        payload = pickle_loads(self.persist_path.read_bytes())
        self.documents = payload.get("documents", [])
        self.vectorizer = payload.get("vectorizer", TfidfVectorizer(stop_words="english"))
        if self.documents:
            corpus = [doc.get("content_text", "") for doc in self.documents]
            self.vectors = self.vectorizer.fit_transform(corpus)
        else:
            self.vectors = None


def pickle_dumps(obj: object) -> bytes:
    import pickle

    return pickle.dumps(obj)


def pickle_loads(data: bytes) -> object:
    import pickle

    return pickle.loads(data)


semantic_index = SemanticIndex()
