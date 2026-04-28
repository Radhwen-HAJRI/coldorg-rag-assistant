"""
retrieval.py — Indexation vectorielle et recherche sémantique (FAISS + sentence-transformers).

Choix techniques :
  - FAISS      : bibliothèque Meta, wheels précompilés sur Windows/Mac/Linux,
                 pas de dépendances C++ à compiler manuellement
  - Embeddings : sentence-transformers "paraphrase-multilingual-MiniLM-L12-v2"
                 → modèle multilingue, performant sur le français, ~120MB, gratuit

Pourquoi FAISS plutôt que ChromaDB ici ?
  - ChromaDB nécessite chroma-hnswlib qui se compile depuis les sources
    (requiert Visual C++ Build Tools sur Windows) → problème d'installation fréquent
  - FAISS propose des wheels binaires prêts à l'emploi sur toutes les plateformes
  - Pour 30-500 documents, les deux sont équivalents en performance
  - Migration vers ChromaDB/Qdrant triviale si besoin de persistance avancée
"""

import pickle
from pathlib import Path
from typing import Optional

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.ingestion import Chunk


EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
INDEX_PATH = "./faiss_index"


class FAISSIndex:
    """Index vectoriel FAISS avec métadonnées associées."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: list[Chunk] = []

    def build(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        print(f"  Génération des embeddings pour {len(chunks)} chunks...")
        texts = [c.text for c in chunks]
        embeddings = self.model.encode(
            texts, batch_size=32, show_progress_bar=True, normalize_embeddings=True
        )
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings.astype(np.float32))
        print(f"  ✅ Index FAISS : {self.index.ntotal} vecteurs dim={dim}")

    def save(self, path: str = INDEX_PATH) -> None:
        p = Path(path)
        p.mkdir(exist_ok=True)
        faiss.write_index(self.index, str(p / "index.faiss"))
        with open(p / "chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        print(f"  ✅ Index sauvegardé dans {path}/")

    def load(self, path: str = INDEX_PATH) -> None:
        p = Path(path)
        self.index = faiss.read_index(str(p / "index.faiss"))
        with open(p / "chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)
        print(f"  ✅ Index rechargé : {self.index.ntotal} documents")

    def search(self, query: str, n_results: int = 5,
               filter_marque: Optional[str] = None,
               filter_type: Optional[str] = None) -> list[dict]:
        k = n_results * 10 if (filter_marque or filter_type) else n_results
        k = min(k, self.index.ntotal)
        query_vec = self.model.encode([query], normalize_embeddings=True).astype(np.float32)
        scores, indices = self.index.search(query_vec, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = self.chunks[idx]
            if filter_marque and (chunk.marque or "").lower() != filter_marque.lower():
                continue
            if filter_type and (chunk.type_equipement or "") != filter_type:
                continue
            results.append({
                "text": chunk.text,
                "metadata": {
                    "source": chunk.source,
                    "marque": chunk.marque or "",
                    "type_equipement": chunk.type_equipement or "",
                    "code_erreur": chunk.code_erreur or "",
                    **chunk.metadata,
                },
                "score": round(float(score), 4),
            })
            if len(results) >= n_results:
                break
        return results


_index: Optional[FAISSIndex] = None


def build_index(chunks: list[Chunk], persist_dir: str = INDEX_PATH) -> FAISSIndex:
    global _index
    _index = FAISSIndex()
    _index.build(chunks)
    _index.save(persist_dir)
    return _index


def load_index(persist_dir: str = INDEX_PATH) -> FAISSIndex:
    global _index
    _index = FAISSIndex()
    _index.load(persist_dir)
    return _index


def search(index: FAISSIndex, query: str, n_results: int = 5,
           filter_marque: Optional[str] = None,
           filter_type: Optional[str] = None) -> list[dict]:
    return index.search(query, n_results, filter_marque, filter_type)
