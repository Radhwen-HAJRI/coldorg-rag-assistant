"""
pipeline.py — Orchestration du pipeline RAG complet.

Encapsule les 4 étapes : Ingestion → Embedding → Retrieval → Generation
"""

from pathlib import Path
from typing import Optional

from src.ingestion import load_all_documents
from src.retrieval import build_index, search, load_index
from src.generation import generate_response


class RAGPipeline:
    """
    Pipeline RAG pour l'assistant technique COLDORG.

    Usage:
        pipeline = RAGPipeline(data_dir="data")
        pipeline.build()                    # première fois
        result = pipeline.ask("Ma chaudière affiche E133...")
    """

    def __init__(self, data_dir: str = "data", db_dir: str = "./chroma_db"):
        self.data_dir = Path(data_dir)
        self.db_dir = db_dir
        self.collection = None

    def build(self) -> None:
        """Charge les documents, génère les embeddings, crée l'index."""
        print("📂 Chargement des documents...")
        chunks = load_all_documents(self.data_dir)

        print("\n🔢 Génération des embeddings et indexation...")
        self.collection = build_index(chunks, persist_dir=self.db_dir)
        print("\n✅ Pipeline prêt !\n")

    def load(self) -> None:
        """Recharge un index existant depuis le disque (plus rapide)."""
        self.collection = load_index(persist_dir=self.db_dir)
        print(f"✅ Index rechargé ({self.collection.count()} documents)")

    def ask(
        self,
        question: str,
        n_results: int = 5,
        filter_marque: Optional[str] = None,
        filter_type: Optional[str] = None,
        debug: bool = False,
    ) -> dict:
        """
        Pose une question et retourne la réponse RAG.

        Args:
            question     : Question du technicien
            n_results    : Nombre de documents à récupérer (défaut: 5)
            filter_marque: Filtre optionnel par marque
            filter_type  : Filtre optionnel par type d'équipement
            debug        : Retourne le contexte sans générer de réponse LLM

        Returns:
            dict {'answer', 'retrieved_docs', 'model', ...}
        """
        if self.collection is None:
            raise RuntimeError("Pipeline non initialisé. Appelez .build() ou .load() d'abord.")

        # 1. Retrieval
        retrieved = search(
            self.collection,
            query=question,
            n_results=n_results,
            filter_marque=filter_marque,
            filter_type=filter_type,
        )

        # 2. Generation
        result = generate_response(question, retrieved, debug=debug)
        result["question"] = question
        return result

    def print_result(self, result: dict) -> None:
        """Affiche un résultat RAG de façon lisible."""
        print("\n" + "="*70)
        print(f"❓ QUESTION : {result['question']}")
        print("="*70)
        print("\n📚 DOCUMENTS RÉCUPÉRÉS :")
        for i, doc in enumerate(result["retrieved_docs"], 1):
            meta = doc["metadata"]
            print(f"  [{i}] {meta.get('source','?').upper()} | "
                  f"{meta.get('marque','?')} | "
                  f"score={doc['score']:.2f} | "
                  f"code={meta.get('code_erreur','—')}")
        print("\n🤖 RÉPONSE :")
        print(result["answer"])
        if "usage" in result:
            u = result["usage"]
            print(f"\n📊 Tokens: {u['input_tokens']} in / {u['output_tokens']} out")
        print("="*70 + "\n")
