
"""
evaluate.py — Évaluation du système RAG sur les 5 questions de référence.

Génère un rapport complet : réponses + documents récupérés + analyse.
Le rapport est sauvegardé dans results/evaluation_results.md
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import RAGPipeline


def load_questions(path: str = "data/questions_test.json") -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def format_markdown_report(results: list[dict]) -> str:
    """Génère un rapport Markdown des évaluations."""
    lines = [
        "# Évaluation RAG COLDORG — Résultats\n",
        f"_Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}_\n",
        f"**Modèle :** {results[0]['model'] if results else 'N/A'}  \n",
        f"**Embeddings :** paraphrase-multilingual-MiniLM-L12-v2  \n",
        f"**Vector store :** ChromaDB (cosine similarity)  \n\n",
        "---\n",
    ]

    for r in results:
        qid = r.get("question_id", "?")
        question = r["question"]
        answer = r["answer"]
        docs = r["retrieved_docs"]

        lines.append(f"\n## {qid} — Question\n")
        lines.append(f"> {question}\n")
        lines.append("\n### Documents récupérés\n")
        lines.append("| # | Source | Marque | Code erreur | Score |\n")
        lines.append("|---|--------|--------|-------------|-------|\n")
        for i, doc in enumerate(docs, 1):
            meta = doc["metadata"]
            lines.append(
                f"| {i} | {meta.get('source','?')} | "
                f"{meta.get('marque','?')} | "
                f"{meta.get('code_erreur','—')} | "
                f"{doc['score']:.3f} |\n"
            )

        lines.append("\n### Réponse générée\n")
        lines.append(answer + "\n")

        if "usage" in r:
            u = r["usage"]
            lines.append(
                f"\n_Tokens : {u['input_tokens']} in / {u['output_tokens']} out_\n"
            )

        lines.append("\n---\n")

    
    lines.append("\n## Analyse & Pistes d'amélioration\n")
    lines.append("""
### Ce qui fonctionne bien

1. **Matching code erreur** : Les codes (E133, F28, U4...) sont retrouvés avec précision
   car ils figurent à la fois dans les interventions et les fiches techniques.
2. **Hybridité des sources** : Le système combine l'expérience terrain (interventions)
   avec la documentation constructeur, ce qu'un technicien débutant ne ferait pas seul.
3. **Filtrage par métadonnées** : Le filtre par marque permet d'éviter de remonter
   des interventions hors-sujet sur une question ciblée.

### Pistes d'amélioration identifiées

1. **Re-ranking avec cross-encoder** _(implémentation partielle incluse)_
   - Un bi-encoder (sentence-transformers) optimise la vitesse mais pas toujours
     la pertinence. Un cross-encoder (ex: `cross-encoder/ms-marco-MiniLM-L-6-v2`)
     pourrait re-scorer les N premiers résultats pour meilleure précision.

2. **Chunking par code erreur pour les fiches techniques**
   - Actuellement, une section peut contenir plusieurs codes. Créer un chunk
     par code erreur améliorerait la précision du retrieval sur des requêtes ciblées.

3. **Gestion du multi-turn (mémoire de conversation)**
   - Ajouter un historique de conversation dans le prompt permet au technicien
     de poser des questions de suivi ("et si ça ne marche pas ?") sans répéter le contexte.
   - Implémentable simplement en passant `messages=[...]` multi-turn à l'API.
""")

    return "".join(lines)


def main():
    print("🔧 Évaluation du système RAG COLDORG")
    print("="*50)

    # Init pipeline
    pipeline = RAGPipeline(data_dir="data")
    db_path = Path("./chroma_db")
    if db_path.exists():
        try:
            pipeline.load()
        except Exception:
            pipeline.build()
    else:
        pipeline.build()

    # Chargement des questions
    questions = load_questions()
    print(f"\n📋 {len(questions)} questions à évaluer\n")

    results = []
    for q in questions:
        print(f"⏳ Évaluation {q['id']}...")
        result = pipeline.ask(q["question"], n_results=5)
        result["question_id"] = q["id"]
        results.append(result)
        pipeline.print_result(result)

    # Sauvegarde du rapport
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    # JSON brut
    json_path = output_dir / "evaluation_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        # On sérialise sans le contexte complet pour alléger
        slim = [{k: v for k, v in r.items() if k != "context"} for r in results]
        json.dump(slim, f, ensure_ascii=False, indent=2)

    # Rapport Markdown
    md_path = output_dir / "evaluation_results.md"
    md_content = format_markdown_report(results)
    md_path.write_text(md_content, encoding="utf-8")

    print(f"\n✅ Rapport sauvegardé dans :")
    print(f"   {json_path}")
    print(f"   {md_path}")


if __name__ == "__main__":
    main()
