"""
ingestion.py — Chargement et découpage des documents pour le RAG COLDORG.

Deux sources de données :
  - interventions.json  : 30 fiches d'interventions passées (JSON)
  - docs/*.txt          : Fiches techniques par équipement (texte structuré)

Stratégie de chunking :
  - Interventions : 1 chunk = 1 intervention, texte auto-généré depuis les champs JSON
  - Fiches techniques : découpage par section (--- délimiteur), avec conservation
    du contexte (nom du document + marque en préfixe de chaque chunk)
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    """Un chunk = un morceau de document prêt à être indexé."""
    id: str
    text: str
    source: str                    # "intervention" | "fiche_technique"
    marque: Optional[str] = None
    type_equipement: Optional[str] = None
    code_erreur: Optional[str] = None
    metadata: dict = field(default_factory=dict)


# ─────────────────────────────────────────────
# Ingestion des interventions
# ─────────────────────────────────────────────

def load_interventions(path: str | Path) -> list[Chunk]:
    """
    Charge les interventions JSON et crée un chunk par intervention.

    Chaque chunk est une représentation textuelle naturelle de l'intervention,
    conçue pour maximiser la pertinence lors de la recherche sémantique.
    Les métadonnées (marque, type, code erreur) sont conservées pour le filtrage.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    chunks = []
    for item in data:
        pieces = item.get("pieces_remplacees", [])
        pieces_str = ", ".join(pieces) if pieces else "Aucune"

        # Texte lisible = ce qu'un LLM peut facilement exploiter en contexte
        text = (
            f"[INTERVENTION {item['id']} — {item['date']}]\n"
            f"Équipement : {item['equipement']}\n"
            f"Marque : {item['marque']} | Type : {item['type_equipement']}\n"
            f"Code erreur : {item.get('code_erreur') or 'Aucun'}\n"
            f"Symptôme : {item['symptome']}\n"
            f"Diagnostic : {item['diagnostic']}\n"
            f"Solution : {item['solution']}\n"
            f"Pièces remplacées : {pieces_str}\n"
            f"Durée : {item['temps_intervention_min']} min | "
            f"Difficulté : {item['difficulte']} | Technicien : {item['technicien']}"
        )

        chunks.append(Chunk(
            id=f"int_{item['id'].lower()}",
            text=text,
            source="intervention",
            marque=item.get("marque"),
            type_equipement=item.get("type_equipement"),
            code_erreur=item.get("code_erreur"),
            metadata={
                "date": item["date"],
                "difficulte": item["difficulte"],
                "temps_min": item["temps_intervention_min"],
                "technicien": item["technicien"],
            }
        ))

    return chunks


# ─────────────────────────────────────────────
# Ingestion des fiches techniques
# ─────────────────────────────────────────────

def _extract_brand_from_header(text: str) -> Optional[str]:
    """Extrait la marque depuis la première ligne de la fiche."""
    for line in text.splitlines():
        if "Frisquet" in line:
            return "Frisquet"
        if "Daikin" in line:
            return "Daikin"
        if "Saunier Duval" in line:
            return "Saunier Duval"
        if "Atlantic" in line:
            return "Atlantic"
    return None


def _extract_equipment_type(filename: str) -> str:
    """Déduit le type d'équipement depuis le nom du fichier."""
    name = filename.lower()
    if "frisquet" in name or "saunier" in name or "thema" in name:
        return "chaudiere_gaz"
    if "daikin" in name or "altherma" in name:
        return "pac_air_eau"
    if "atlantic" in name or "climatisation" in name:
        return "climatisation"
    return "inconnu"


def _extract_error_codes_from_section(text: str) -> list[str]:
    """Extrait les codes erreur mentionnés dans un chunk de fiche technique."""
    # Codes comme E133, F28, U4, A3, 7H, AH, etc.
    return re.findall(r'\b([A-Z]{0,2}\d{1,3}[A-Z]?)\b', text)


def load_technical_docs(docs_dir: str | Path) -> list[Chunk]:
    """
    Charge et découpe les fiches techniques TXT.

    Stratégie de chunking :
    - Découpage sur les séparateurs `---` (sections naturelles du document)
    - Chaque section hérite du contexte global (marque, type équipement)
    - Les sections trop courtes (<50 chars) sont fusionnées avec la précédente
    - Le nom de l'équipement est injecté en préfixe de chaque chunk pour
      que la recherche sémantique retrouve les bons chunks même via la marque
    """
    docs_path = Path(docs_dir)
    chunks = []

    for filepath in sorted(docs_path.glob("*.txt")):
        content = filepath.read_text(encoding="utf-8").strip()
        marque = _extract_brand_from_header(content)
        type_eq = _extract_equipment_type(filepath.name)

        # On extrait le titre de la fiche (première ligne =====)
        title_match = re.search(r'=== (.+?) ===', content)
        doc_title = title_match.group(1) if title_match else filepath.stem

        # Découpage par sections (délimiteur ---)
        raw_sections = re.split(r'\n---+\n', content)

        merged_sections = []
        buffer = ""
        for section in raw_sections:
            section = section.strip()
            if not section:
                continue
            if len(buffer) + len(section) < 150 and buffer:
                buffer += "\n" + section
            else:
                if buffer:
                    merged_sections.append(buffer)
                buffer = section
        if buffer:
            merged_sections.append(buffer)

        for i, section in enumerate(merged_sections):
            if len(section) < 30:
                continue

            # Préfixe de contexte pour améliorer la recherche
            chunk_text = f"[FICHE TECHNIQUE : {doc_title}]\n{section}"
            error_codes = _extract_error_codes_from_section(section)

            chunks.append(Chunk(
                id=f"doc_{filepath.stem}_s{i}",
                text=chunk_text,
                source="fiche_technique",
                marque=marque,
                type_equipement=type_eq,
                code_erreur=error_codes[0] if error_codes else None,
                metadata={
                    "fichier": filepath.name,
                    "titre_doc": doc_title,
                    "section_index": i,
                }
            ))

    return chunks


# ─────────────────────────────────────────────
# Point d'entrée principal
# ─────────────────────────────────────────────

def load_all_documents(data_dir: str | Path) -> list[Chunk]:
    """Charge l'ensemble des documents (interventions + fiches techniques)."""
    data_path = Path(data_dir)
    interventions = load_interventions(data_path / "interventions.json")
    docs = load_technical_docs(data_path / "docs")
    print(f"✅ {len(interventions)} interventions chargées")
    print(f"✅ {len(docs)} chunks de fiches techniques chargés")
    return interventions + docs
