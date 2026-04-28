# 🔧 RAG COLDORG — Assistant Technique pour Techniciens CVC

Prototype de système RAG (Retrieval-Augmented Generation) permettant à des techniciens de maintenance de diagnostiquer des pannes en s'appuyant sur l'historique d'interventions et la documentation technique constructeurs.

**Candidature :** Radhwen Hajri — Alternance Data / IA ENSEM  
**Délai :** rendu le 28/04/2026

---

## Démo rapide

```bash
# Installation
git clone https://github.com/votre-username/rag-coldorg
cd rag-coldorg
pip install -r requirements.txt
cp .env.example .env 

# Première utilisation 
python main.py --build

# Mode interactif
python main.py

# Question directe
python main.py -q "Code erreur E133 sur une Frisquet Prestige, que faire ?"

# Évaluation sur les 5 questions de test
python evaluate.py
```

---

## Architecture du projet

```
rag_coldorg/
├── main.py                  # CLI interactive (bonus)
├── evaluate.py              # Évaluation sur les 5 questions de test
├── requirements.txt
├── .env.example
├── data/
│   ├── interventions.json   # 30 fiches d'interventions
│   ├── questions_test.json  # 5 questions de référence
│   └── docs/
│       ├── fiche_frisquet_prestige.txt
│       ├── fiche_daikin_altherma.txt
│       ├── fiche_saunier_duval_themaplus.txt
│       └── fiche_atlantic_climatisation.txt
├── src/
│   ├── ingestion.py         # Chargement & chunking des documents
│   ├── retrieval.py         # Indexation ChromaDB + recherche vectorielle
│   ├── generation.py        # Génération LLM (Claude API)
│   └── pipeline.py          # Orchestration RAG end-to-end
└── results/
    ├── evaluation_results.md
    └── evaluation_results.json
```

---

## Choix techniques

### Stack

| Composant | Choix | Justification |
|-----------|-------|---------------|
| Langage | Python 3.11+ | Écosystème ML/data le plus riche |
| Embeddings | `sentence-transformers` `paraphrase-multilingual-MiniLM-L12-v2` | Multilingue (FR/EN), ~120MB, gratuit, offline |
| Vector store | ChromaDB (mode persistant) | Embarqué, pas de serveur, facile à déployer, supporte le filtrage par métadonnées |
| Similarité | Cosine similarity | Plus robuste que L2 pour les embeddings normalisés |
| LLM | Claude claude-sonnet-4-6 (Anthropic) | Excellent en contexte long, excellent en français |
| Fallback | Mode `--debug` (affiche docs sans LLM) | Fonctionne sans clé API |

### Pourquoi `paraphrase-multilingual-MiniLM-L12-v2` ?

- **Multilingue** : gère bien le mélange français/codes techniques anglais
- **Léger** : 120MB, tourne sur CPU en < 1s par requête
- **Gratuit et local** : pas de coût d'API, pas de données envoyées à l'extérieur
- **Alternative** si besoin de meilleure qualité : `OpenAI text-embedding-3-small` (~0.02$/1M tokens)

---

## Stratégie de chunking

### Interventions JSON → 1 chunk = 1 intervention

Chaque intervention est transformée en un texte lisible et structuré :

```
[INTERVENTION INT-001 — 2025-11-15]
Équipement : Chaudière gaz Frisquet Prestige Condensation 25kW
Marque : Frisquet | Type : chaudiere_gaz
Code erreur : E133
Symptôme : La chaudière s'est arrêtée pendant la nuit...
Diagnostic : Défaut d'allumage. Vérification de l'arrivée de gaz OK...
Solution : Nettoyage électrode d'allumage, réglage de l'écart à 3mm...
Pièces remplacées : Aucune
Durée : 45 min | Difficulté : moyen | Technicien : Martin D.
```

**Pourquoi 1 chunk = 1 intervention ?**
- Une intervention est une unité logique complète (symptôme → diagnostic → solution)
- Fragmenter casserait cette cohérence causale
- Les 30 interventions tiennent facilement dans un seul contexte LLM

### Fiches techniques TXT → découpage par sections (`---`)

Les fiches techniques sont naturellement structurées en sections séparées par `---`. Chaque section devient un chunk, avec injection du titre de la fiche en préfixe pour conserver le contexte :

```
[FICHE TECHNIQUE : Frisquet Prestige Condensation]
E133 — Défaut d'allumage
  Causes possibles :
  - Pas d'arrivée de gaz...
```

**Résultat :** ~4-6 chunks par fiche, soit ~20 chunks de documentation au total.

### Gestion des métadonnées

Chaque chunk est stocké avec des métadonnées qui permettent le filtrage ultérieur :

| Métadonnée | Exemple | Usage |
|------------|---------|-------|
| `marque` | "Frisquet" | Filtrer les interventions Frisquet uniquement |
| `type_equipement` | "chaudiere_gaz" | Limiter au type d'équipement concerné |
| `code_erreur` | "E133" | Recherche ciblée par code |
| `source` | "intervention" | Distinguer terrain vs documentation |
| `difficulte` | "moyen" | Évaluer la complexité de l'intervention |

---

## Pipeline RAG

```
Question technicien
       ↓
   [Embedding]  paraphrase-multilingual-MiniLM-L12-v2
       ↓
 [Recherche vectorielle]  ChromaDB — top-5 cosine similarity
       |
       ├── Filtre optionnel : marque / type_équipement
       ↓
 [Construction du contexte]  concatenation des 5 chunks les plus proches
       ↓
 [Génération LLM]  Claude claude-sonnet-4-6 avec prompt système spécialisé
       ↓
   Réponse structurée
```

---

## Résultats sur les 5 questions de test

### Q1 — Code E133 Frisquet Prestige Condensation 25kW

> *"Code erreur E133 sur une chaudière Frisquet Prestige Condensation 25kW. La chaudière ne redémarre pas depuis ce matin. Quelles sont les causes possibles et comment diagnostiquer ?"*

**Documents récupérés :** INT-001, INT-011, INT-029 (interventions E133 Frisquet) + section E133 de la fiche Frisquet Prestige

**Réponse générée :**

## Diagnostic — Code E133 Frisquet Prestige Condensation 25kW

### Causes possibles
L'E133 signale un **défaut d'allumage** : la chaudière a tenté de s'allumer plusieurs fois sans succès et s'est mise en sécurité.
- Arrivée de gaz interrompue (robinet gaz fermé, pression réseau insuffisante, compteur bloqué)
- Électrode d'allumage encrassée ou écart hors tolérance (correct = 3 mm)
- Fil de masse desserré sur le boîtier de contrôle
- Courant d'ionisation insuffisant (doit être > 1 µA)
- Carte électronique défaillante (cause rare)

### Procédure de diagnostic
1. Vérifier que le robinet gaz est bien ouvert
2. Mesurer la pression gaz en entrée (valeur nominale : 20 mbar pour G20)
3. Inspecter visuellement l'électrode d'allumage (encrassement, fissures) et nettoyer
4. Contrôler l'écart électrode → ajuster à **3 mm** si nécessaire
5. Vérifier le fil de masse et toutes les connexions du boîtier de contrôle
6. Mesurer le courant d'ionisation : si < 1 µA, remplacer l'électrode
7. Si tout est conforme → suspecter la carte électronique

### Retours d'expérience (interventions similaires)
- **INT-001** (15/11/2025) : E133 résolu par nettoyage électrode + réglage écart à 3 mm + resserrage fil de masse. Reset boîtier, test OK sur 3 cycles. Durée : 45 min.
- **INT-011, INT-029** : même procédure avec succès.

### Pièces à prévoir
- Électrode d'allumage/ionisation (remplacement recommandé si > 3-5 ans)

---

### Q2 — Fuite Atlantic Idéa

> *"J'ai une fuite d'eau qui coule le long du mur sous mon climatiseur Atlantic Idéa. Qu'est-ce que ça peut être ?"*

**Documents récupérés :** INT-003 (fuite Atlantic identique) + section "Fuite d'eau unité intérieure" de la fiche Atlantic

**Réponse générée :**

## Diagnostic — Fuite d'eau Atlantic Idéa (unité intérieure)

### Causes possibles
Une fuite coulant le long du mur indique un problème d'évacuation des condensats :
- Bac de condensat obstrué par des algues, de la poussière ou des débris
- Tuyau d'évacuation bouché ou à pente insuffisante (minimum 1%)
- Pompe de relevage défaillante (si installation haute)
- Unité intérieure non de niveau

### Solution recommandée
- Nettoyer complètement le bac de condensat
- Déboucher le tuyau (pompe à main)
- Corriger la pente si nécessaire
- **Ajouter une pastille anti-algues** dans le bac

### Retour d'expérience
- **INT-003** (08/09/2025) : cas identique sur Atlantic Idéa 3.5kW — bac obstrué par algues + tuyau bouché + mauvaise pente. Résolu en 35 min.

---

### Q3 — Code U4 Daikin Altherma

> *"Ma pompe à chaleur Daikin Altherma affiche le code U4, plus de chauffage ni d'eau chaude. Quelles pièces dois-je prévoir ?"*

**Documents récupérés :** INT-002 (U4 Daikin Altherma causé par câble rongé) + section U4 de la fiche Daikin

**Pièces à prévoir identifiées :** Câble communication 4x0.75mm² + gaine anti-rongeurs (si applicable) + éventuellement carte PCB

---

### Q4 — Code F28 récurrent Saunier Duval ThemaPlus

> *"Un client a une chaudière Saunier Duval ThemaPlus Condens en panne avec le code F28 pour la troisième fois ce mois. Qu'est-ce qui peut expliquer un défaut récurrent ?"*

**Documents récupérés :** INT-004 + INT-023 (deux F28 Saunier Duval résolus) + section F28 de la fiche SD

**Cause identifiée :** Électrovanne gaz fatiguée (courant de commande faible) — **réf. Saunier Duval 05743600** à commander

---

### Q5 — PAC Daikin chauffe mais maison froide (sans code erreur)

> *"Le client dit que sa PAC Daikin chauffe mais que la maison reste froide. La PAC ne montre aucun code erreur. Que vérifier ?"*

**Documents récupérés :** INT-026 (7H, sous-performance basse pression) + INT-019 (L5, dégivrage anormal) + fiche Daikin entretien

**Checklist terrain générée :**
- Mesurer T° départ / retour eau (delta T normal : 5-10°C)
- Vérifier réglage courbe de chauffe
- Inspecter et nettoyer la batterie extérieure
- Contrôler pressions HP/BP avec manifold
- Vérifier compatibilité puissance PAC vs émetteurs (radiateurs HT ≠ plancher chauffant)

---

## Pistes d'amélioration

### 1. Re-ranking avec cross-encoder *(prioritaire)*
Le bi-encoder actuel optimise la vitesse mais peut retourner des faux positifs.  
Un cross-encoder (ex: `cross-encoder/ms-marco-MiniLM-L-6-v2`) pourrait re-scorer les top-10 pour ne garder que les 5 vraiment pertinents.

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = reranker.predict([(query, doc["text"]) for doc in retrieved])
reranked = sorted(zip(retrieved, scores), key=lambda x: x[1], reverse=True)
```

### 2. Chunking par code erreur dans les fiches techniques
Actuellement, une section "CODES ERREUR" contient E133, E125 et E110 ensemble.  
Créer un chunk par code erreur améliorerait la précision du retrieval sur des questions ciblées.

### 3. Gestion multi-turn (mémoire de conversation)
Permettre au technicien de poser des questions de suivi sans répéter le contexte.  
Implémentable avec `messages=[...]` multi-turn dans l'API Claude.

---

## Passage à l'échelle (10 000 interventions)

| Aspect | Aujourd'hui (30) | À 10 000 |
|--------|-----------------|----------|
| Vector store | ChromaDB embarqué | ChromaDB toujours viable, ou migration vers Qdrant/Weaviate si besoin de filtres complexes |
| Embeddings | Recalcul complet à chaque build | Cache sur disque, ingestion incrémentale |
| Retrieval | top-5 sur tout le corpus | Pré-filtrage par marque/type en metadata, puis top-5 dans le sous-ensemble |
| Latence | <1s | Ajout d'un ANN index (HNSW) + cache requêtes fréquentes |
| Coût | Gratuit (local) | OpenAI embeddings ou modèle hébergé si besoin de perf accrue |

---

## Lancer le projet

```bash
# Cloner et installer
git clone https://github.com/votre-username/rag-coldorg
cd rag-coldorg
pip install -r requirements.txt

# Configurer la clé API
cp .env.example .env
# Éditer .env → ANTHROPIC_API_KEY=sk-ant-...

# Builder l'index (télécharge le modèle d'embedding ~120MB au 1er run)
python main.py --build

# Mode interactif
python main.py

# Filtrer par marque
python main.py --marque Frisquet

# Sans LLM (debug)
python main.py --debug

# Évaluation complète
python evaluate.py
```

---

*Radhwen Hajri — ENSEM Nancy — Candidature alternance Data / IA COLDORG*
