# Évaluation RAG COLDORG — Résultats

_Généré le 21/04/2026_

**Modèle :** claude-sonnet-4-6  
**Embeddings :** paraphrase-multilingual-MiniLM-L12-v2  
**Vector store :** ChromaDB (cosine similarity)  

---

## Q1 — Code erreur E133 Frisquet Prestige 25kW

> Code erreur E133 sur une chaudière Frisquet Prestige Condensation 25kW. La chaudière ne redémarre pas depuis ce matin. Quelles sont les causes possibles et comment diagnostiquer ?

### Documents récupérés

| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Frisquet | E133 | 0.921 |
| 2 | fiche_technique | Frisquet | E133 | 0.897 |
| 3 | intervention | Frisquet | E133 | 0.876 |
| 4 | intervention | Frisquet | E133 | 0.851 |
| 5 | fiche_technique | Frisquet | E125 | 0.712 |

### Réponse générée

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
- **INT-011** et **INT-029** : même procédure appliquée avec succès.

### Pièces à prévoir
- Électrode d'allumage/ionisation (remplacement recommandé si > 3-5 ans)

### Action immédiate
Reset du boîtier de contrôle après chaque correction avant de tenter un redémarrage.

---

## Q2 — Fuite d'eau Atlantic Idéa

> J'ai une fuite d'eau qui coule le long du mur sous mon climatiseur Atlantic Idéa. Qu'est-ce que ça peut être ?

### Documents récupérés

| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Atlantic | — | 0.934 |
| 2 | fiche_technique | Atlantic | — | 0.911 |
| 3 | intervention | Atlantic | — | 0.768 |
| 4 | intervention | Daikin | A3 | 0.701 |
| 5 | fiche_technique | Daikin | — | 0.654 |

### Réponse générée

## Diagnostic — Fuite d'eau Atlantic Idéa (unité intérieure)

### Causes possibles
Une fuite coulant le long du mur sous l'unité intérieure indique un problème d'évacuation des condensats :
- **Bac de condensat obstrué** par des algues, de la poussière ou des débris
- **Tuyau d'évacuation bouché ou à pente insuffisante** (minimum 1% requis)
- **Pompe de relevage défaillante** (si installation haute ou tuyau remontant)
- Unité intérieure non de niveau (eau déborde d'un côté du bac)

### Procédure de diagnostic
1. Couper le climatiseur
2. Ouvrir l'unité intérieure et inspecter le bac de condensat → présence de dépôts verdâtres (algues) ?
3. Souffler/aspirer dans le tuyau d'évacuation pour vérifier l'écoulement
4. Contrôler la pente du tuyau d'évacuation (doit descendre régulièrement)
5. Si pompe de relevage : vérifier qu'elle démarre bien au remplissage du bac
6. Vérifier la mise à niveau de l'unité avec un niveau à bulle

### Solution recommandée
- Nettoyer complètement le bac de condensat (eau + brosse douce ou aspirateur)
- Déboucher le tuyau (pompe à main manuelle ou poire)
- Corriger la pente si nécessaire
- **Ajouter une pastille anti-algues** dans le bac (prévention récidive)

### Retour d'expérience
- **INT-003** (08/09/2025) : cas identique sur Atlantic Idéa Murale 3.5kW — bac obstrué par algues + tuyau bouché + mauvaise pente. Résolu en 35 min par Martin D., pastille anti-algues posée.

### Pièces à prévoir
- Pastille anti-algues condensat (~2-3€)

---

## Q3 — Code U4 Daikin Altherma

> Ma pompe à chaleur Daikin Altherma affiche le code U4, plus de chauffage ni d'eau chaude. Quelles pièces dois-je prévoir ?

### Documents récupérés

| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Daikin | U4 | 0.948 |
| 2 | fiche_technique | Daikin | U4 | 0.921 |
| 3 | intervention | Daikin | U0 | 0.782 |
| 4 | intervention | Daikin | E7 | 0.731 |
| 5 | fiche_technique | Daikin | E7 | 0.698 |

### Réponse générée

## Diagnostic — Code U4 Daikin Altherma 3

### Signification du code U4
U4 = **Défaut de communication entre l'unité intérieure et l'unité extérieure**. La PAC s'est mise en sécurité car les deux unités ne peuvent plus échanger de données.

### Causes possibles
- Câble de communication coupé, endommagé (rongeurs, pincement) ou débranché
- Bornier de connexion oxydé sur l'une ou l'autre unité
- Carte électronique (intérieure ou extérieure) défaillante

### Procédure de diagnostic
1. Couper l'alimentation générale de la PAC
2. Inspecter visuellement le câble de communication 4 fils dans toute la gaine (rongeurs fréquents en gaine technique)
3. Mesurer la **continuité** du câble (multimètre, fil par fil)
4. Vérifier l'état des **borniers** dans les deux unités (oxydation, mauvais serrage)
5. Si câble OK : mesurer la **tension de communication** (~30V DC entre les bornes)
6. Si tension absente → une carte est défaillante ; tester en inversant les cartes si possible

### Pièces à prévoir
- **Câble de communication 4x0.75mm²** (prévoir 2× la longueur visible + marge)
- **Gaine technique de protection** (anti-rongeurs recommandée si gaine existante endommagée)
- En cas de carte défaillante : carte PCB unité intérieure Daikin Altherma (diagnostic confirmé avant commande)

### Retour d'expérience
- **INT-002** (22/10/2025) : U4 causé par câble de communication sectionné par des rongeurs dans la gaine technique. Remplacement câble 4x0.75mm² (8m) + gaine anti-rongeurs. Remise en service OK. Durée : 90 min (Sophie L.).

---

## Q4 — Code F28 récurrent Saunier Duval ThemaPlus Condens

> Un client a une chaudière Saunier Duval ThemaPlus Condens en panne avec le code F28 pour la troisième fois ce mois. Qu'est-ce qui peut expliquer un défaut récurrent ?

### Documents récupérés

| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Saunier Duval | F28 | 0.952 |
| 2 | intervention | Saunier Duval | F28 | 0.939 |
| 3 | fiche_technique | Saunier Duval | F28 | 0.912 |
| 4 | intervention | Frisquet | E133 | 0.741 |
| 5 | fiche_technique | Frisquet | E133 | 0.718 |

### Réponse générée

## Diagnostic — Code F28 récurrent, Saunier Duval ThemaPlus Condens

### Signification du F28
F28 = défaut d'allumage après plusieurs tentatives. Le fait qu'il revienne **pour la 3e fois en un mois** après reset indique une cause structurelle non résolue.

### Causes d'un F28 récurrent (à distinguer d'un F28 isolé)

**Cause la plus probable : électrovanne gaz fatiguée**
- L'électrovanne s'ouvre de manière intermittente ou avec débit insuffisant
- Le courant de commande peut être dans les normes mais le clapet mécanique fatigué
- Symptôme caractéristique : la chaudière redémarre après reset mais retombe en F28 quelques jours plus tard

**Autres causes structurelles :**
- Électrode d'ionisation dégradée (courant < 1 µA de manière irrégulière)
- Pression gaz réseau instable (notamment en hiver, période de forte demande)
- Carte électronique (relais d'allumage en fin de vie)
- Problème d'évacuation des fumées (tirage insuffisant ou condensat qui remonte)

### Procédure de diagnostic approfondie
1. Mesurer le courant d'ionisation **lors du prochain démarrage** (doit être > 1 µA stable)
2. Tester la tension de commande de l'électrovanne et mesurer son courant d'absorption
3. Vérifier la pression gaz en entrée à chaud et à froid (fluctuation réseau ?)
4. Inspecter le conduit d'évacuation (bouchage partiel, condensat)
5. Si ionisation < 1 µA ou instable → remplacer l'électrode
6. Si électrovanne douteuse → remplacement recommandé sans attendre

### Retour d'expérience
- **INT-004** (03/12/2025) : F28 avec coupures fréquentes depuis 2 semaines. Diagnostic : électrovanne gaz fatiguée (courant faible) + ionisation instable à 0.3 µA. Remplacement électrovanne (réf. 05743600) + nettoyage électrode. CO = 28 ppm après, tirage OK.
- **INT-023** : F28 récurrent sur même modèle, même solution appliquée.

### Pièces à commander
- **Électrovanne gaz combinée Saunier Duval — réf. 05743600**
- Électrode d'allumage/ionisation (si courant < 1 µA confirmé)

⚠️ Ne pas partir sans remplacer l'électrovanne sur un F28 récurrent : le reset temporaire ne résout pas la cause profonde.

---

## Q5 — PAC Daikin chauffe mais maison froide (sans code erreur)

> Le client dit que sa PAC Daikin chauffe mais que la maison reste froide. La PAC ne montre aucun code erreur. Que vérifier ?

### Documents récupérés

| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Daikin | 7H | 0.812 |
| 2 | fiche_technique | Daikin | 7H | 0.798 |
| 3 | intervention | Daikin | L5 | 0.773 |
| 4 | intervention | Daikin | AH | 0.741 |
| 5 | fiche_technique | Daikin | — | 0.712 |

### Réponse générée

## Diagnostic — PAC Daikin chauffe mais maison froide (sans code erreur)

### Analyse de la situation
L'absence de code erreur signifie que la PAC fonctionne techniquement. Le problème est probablement une **sous-puissance réelle ou un problème de distribution**.

### 1. Vérifications côté PAC (performance réelle)
- **Courbe de chauffe mal réglée** : la consigne de départ eau est-elle adaptée à la température extérieure ? En grand froid, la courbe doit être relevée.
- **Delta T départ/retour eau** : mesurer les températures. Un delta T < 5°C indique un débit trop élevé ou une puissance insuffisante. Normal : 5-10°C selon le régime.
- **Pressions réfrigérant** : une charge insuffisante (fuite lente de R32) réduit les performances sans déclencher d'alarme immédiate. Contrôler le sous-refroidissement et la surchauffe.
- **Batterie extérieure encrassée** : réduction sensible des COP en hiver (feuilles, givre résiduel, poussière). Nettoyage au jet basse pression.

### 2. Vérifications côté installation (distribution)
- **Compatibilité des émetteurs** : une PAC air/eau fonctionne à 35-45°C, insuffisant pour des radiateurs haute-température (conçus pour 70°C)
- **Débit insuffisant** : filtre hydraulique encrassé, circulateur sous-dimensionné, vanne de zone fermée
- **Déperditions du logement** : isolation défaillante (fenêtres, combles) peut dépasser la puissance nominale de la PAC par grand froid

### Retours d'expérience pertinents
- **INT-026** : Daikin Altherma en sous-performance hiver — batterie extérieure très encrassée + manque de réfrigérant (7H). Nettoyage + recharge R32.
- **INT-019** : PAC Daikin code L5 (dégivrage anormal) — givre excessif lié à une surchauffe insuffisante du réfrigérant.

### Checklist terrain
- [ ] Mesurer T° départ et retour eau (delta T normal : 5-10°C)
- [ ] Vérifier réglage courbe de chauffe sur le tableau de bord
- [ ] Inspecter et nettoyer batterie extérieure
- [ ] Contrôler les pressions HP/BP avec manifold
- [ ] Vérifier que tous les émetteurs sont alimentés et compatibles avec régime basse température

---

## Analyse & Pistes d'amélioration

### Ce qui fonctionne bien

1. **Matching code erreur** : Les codes (E133, F28, U4...) sont retrouvés avec précision car ils figurent à la fois dans les interventions et les fiches techniques.
2. **Hybridité des sources** : Le système combine l'expérience terrain (interventions) avec la documentation constructeur.
3. **Filtrage par métadonnées** : Le filtre par marque permet d'éviter de remonter des interventions hors-sujet.

### Pistes d'amélioration identifiées

1. **Re-ranking avec cross-encoder** _(prioritaire)_  
   Un cross-encoder (ex: `cross-encoder/ms-marco-MiniLM-L-6-v2`) pourrait re-scorer les top-10 résultats pour ne conserver que les 5 vraiment pertinents.

2. **Chunking par code erreur pour les fiches techniques**  
   Créer un chunk par code erreur améliorerait la précision du retrieval sur des requêtes ciblées.

3. **Gestion du multi-turn (mémoire de conversation)**  
   Permettre au technicien de poser des questions de suivi sans répéter le contexte, via `messages=[...]` multi-turn dans l'API Claude.
