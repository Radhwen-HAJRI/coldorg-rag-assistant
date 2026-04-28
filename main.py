
"""
main.py — Interface CLI interactive pour l'assistant RAG COLDORG.

Usage :
    python main.py              # Mode interactif
    python main.py --build      # Force la reconstruction de l'index
    python main.py --debug      # Sans appel LLM (montre juste les docs récupérés)
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  


sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import RAGPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Assistant RAG COLDORG — Diagnostic technique CVC"
    )
    parser.add_argument(
        "--build", action="store_true",
        help="Force la reconstruction de l'index vectoriel"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Mode debug : affiche les docs récupérés sans appel LLM"
    )
    parser.add_argument(
        "--data-dir", default="data",
        help="Chemin vers le dossier de données (défaut: data/)"
    )
    parser.add_argument(
        "--n-results", type=int, default=5,
        help="Nombre de documents à récupérer (défaut: 5)"
    )
    parser.add_argument(
        "--marque", default=None,
        help="Filtre par marque (ex: Frisquet, Daikin, Atlantic, Saunier Duval)"
    )
    parser.add_argument(
        "--question", "-q", default=None,
        help="Poser une question directement (sans mode interactif)"
    )
    return parser.parse_args()


def run_interactive(pipeline: RAGPipeline, args) -> None:
    """Mode interactif — boucle de questions."""
    print("\n" + "="*60)
    print("  🔧 Assistant Technique COLDORG — RAG Prototype")
    print("="*60)
    print("Posez vos questions de diagnostic. Tapez 'quit' pour quitter.")
    if args.debug:
        print("⚠️  Mode DEBUG activé — pas d'appel LLM")
    print()

    while True:
        try:
            question = input("❓ Question : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAu revoir !")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break

        try:
            result = pipeline.ask(
                question,
                n_results=args.n_results,
                filter_marque=args.marque,
                debug=args.debug,
            )
            pipeline.print_result(result)
        except Exception as e:
            print(f"❌ Erreur : {e}")


def main():
    args = parse_args()

    pipeline = RAGPipeline(data_dir=args.data_dir)

    
    db_path = Path("./chroma_db")
    if args.build or not db_path.exists():
        pipeline.build()
    else:
        try:
            pipeline.load()
        except Exception:
            print("Index non trouvé, construction en cours...")
            pipeline.build()

    
    if args.question:
        result = pipeline.ask(
            args.question,
            n_results=args.n_results,
            filter_marque=args.marque,
            debug=args.debug,
        )
        pipeline.print_result(result)
        return

    
    run_interactive(pipeline, args)


if __name__ == "__main__":
    main()
