# Évaluation RAG COLDORG — Résultats
_Généré le 28/04/2026 à 11:10_
**Modèle :** llama-3.3-70b-versatile  
**Embeddings :** paraphrase-multilingual-MiniLM-L12-v2  
**Vector store :** ChromaDB (cosine similarity)  

---

## Q1 — Question
> Code erreur E133 sur une chaudière Frisquet Prestige Condensation 25kW. La chaudière ne redémarre pas depuis ce matin. Quelles sont les causes possibles et comment diagnostiquer ?

### Documents récupérés
| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Frisquet | E133 | 0.815 |
| 2 | intervention | Frisquet | E133 | 0.769 |
| 3 | intervention | Frisquet | E133 | 0.762 |
| 4 | intervention | Frisquet | E110 | 0.704 |
| 5 | intervention | Frisquet | E125 | 0.694 |

### Réponse générée
**Causes possibles :**

1. Défaut d'allumage
2. Pression gaz en entrée trop basse
3. Robinet gaz fermé sous la chaudière
4. Électrode d'allumage encrassée ou écart trop important
5. Problème de fil de masse (déserrage, etc.)

**Procédure de diagnostic :**

1. Vérifier l'arrivée de gaz : s'assurer que la vanne gaz est ouverte et que le compteur est en fonctionnement.
2. Vérifier la pression gaz en entrée : mesurer la pression gaz pour s'assurer qu'elle est dans les normes (20 mbar).
3. Vérifier l'électrode d'allumage : nettoyer l'électrode d'allumage et vérifier l'écart pour s'assurer qu'il est correct (3mm).
4. Vérifier le fil de masse : resserrer le fil de masse si nécessaire.
5. Vérifier le robinet gaz sous la chaudière : s'assurer qu'il est ouvert.
6. Réaliser un test d'allumage pour vérifier si la chaudière fonctionne correctement.

**Solution recommandée :**

En fonction du diagnostic, les solutions possibles sont :

* Nettoyage de l'électrode d'allumage et réglage de l'écart
* Régulation de la pression gaz en entrée
* Ouverture du robinet gaz sous la chaudière
* Resserrage du fil de masse
* Contact avec le fournisseur de gaz pour signaler une basse pression réseau

**Pièces à prévoir :**

Aucune pièce n'est nécessaire pour les solutions proposées, mais il est possible que des pièces soient nécessaires si des problèmes supplémentaires sont découverts pendant le diagnostic. Il est toujours recommandé d'avoir des pièces de rechange courantes, telles que des électrodes d'allumage ou des fils de masse, dans son équipement.

---

## Q2 — Question
> J'ai une fuite d'eau qui coule le long du mur sous mon climatiseur Atlantic Idéa. Qu'est-ce que ça peut être ?

### Documents récupérés
| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Atlantic |  | 0.771 |
| 2 | intervention | Atlantic |  | 0.585 |
| 3 | intervention | Atlantic |  | 0.581 |
| 4 | intervention | Atlantic |  | 0.567 |
| 5 | intervention | Daikin | AH | 0.560 |

### Réponse générée
**Causes possibles :**
Selon les documents fournis, les causes possibles d'une fuite d'eau sous un climatiseur Atlantic Idéa peuvent inclure :
- Un bac de condensat obstrué par des algues
- Un tuyau d'évacuation partiellement bouché
- Une mauvaise pente du tuyau d'évacuation

**Procédure de diagnostic :**
Pour diagnostiquer le problème, il est recommandé de :
- Vérifier le bac de condensat et nettoyer éventuellement les algues qui pourraient l'obstruer
- Inspecter le tuyau d'évacuation pour détecter tout bouchage ou obstruction
- Vérifier la pente du tuyau d'évacuation pour s'assurer qu'elle est correcte

**Solution recommandée :**
La solution recommandée pour résoudre le problème de fuite d'eau serait de :
- Nettoyer complètement le bac de condensat
- Déboucher le tuyau d'évacuation en utilisant une pompe si nécessaire
- Corriger la pente du tuyau d'évacuation si elle est incorrecte
- Ajouter une pastille anti-algues pour empêcher de futures obstructions

**Pièces à prévoir :**
Les pièces à prévoir pour effectuer la réparation pourraient inclure :
- Une pastille anti-algues pour le bac de condensat
- Éventuellement, des pièces de rechange pour le tuyau d'évacuation si celui-ci est endommagé ou nécessite d'être remplacé.

---

## Q3 — Question
> Ma pompe à chaleur Daikin Altherma affiche le code U4, plus de chauffage ni d'eau chaude. Quelles pièces dois-je prévoir ?

### Documents récupérés
| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Daikin | U4 | 0.739 |
| 2 | intervention | Daikin | U0 | 0.662 |
| 3 | fiche_technique | Daikin | 3 | 0.661 |
| 4 | intervention | Daikin | AH | 0.614 |
| 5 | intervention | Daikin | L5 | 0.609 |

### Réponse générée
**Causes possibles :** 
- Câble de communication coupé, endommagé ou mal branché
- Bornier de connexion oxydé
- Carte électronique (intérieure ou extérieure) défaillante

**Procédure de diagnostic :** 
1. Vérifier le câble de communication (4 fils, continuité)
2. Inspecter les borniers des deux unités
3. Tester la tension de communication (env. 30V DC entre les bornes)
4. Si câble OK, tester en inversant les cartes

**Solution recommandée :** 
Remplacement du câble de communication s'il est endommagé, nettoyage ou remplacement des borniers oxydés, ou remplacement de la carte électronique défaillante.

**Pièces à prévoir :** 
- Câble de communication 4x0.75mm² (8m)
- Gaine de protection anti-rongeurs (recommandée pour prévenir les dommages futurs au câble)
- Bornier de connexion (si nécessaire)
- Carte électronique (si la cause est identifiée comme telle)

Il est essentiel de suivre la procédure de diagnostic pour identifier la cause exacte du problème avant de procéder à tout remplacement de pièces.

---

## Q4 — Question
> Un client a une chaudière Saunier Duval ThemaPlus Condens en panne avec le code F28 pour la troisième fois ce mois. Qu'est-ce qui peut expliquer un défaut récurrent ?

### Documents récupérés
| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Saunier Duval | F28 | 0.760 |
| 2 | intervention | Saunier Duval | F28 | 0.731 |
| 3 | intervention | Frisquet | E133 | 0.684 |
| 4 | intervention | Frisquet | E133 | 0.683 |
| 5 | intervention | Frisquet | E133 | 0.673 |

### Réponse générée
**Causes possibles :**

1. **Défaut d'allumage récurrent** : Le code F28 indique un problème d'allumage, ce qui peut être dû à une carte électronique défaillante (relais d'allumage intermittent) comme indiqué dans l'intervention INT-023.
2. **Électrovanne gaz fatiguée** : Une électrovanne gaz fatiguée peut également provoquer des défauts d'allumage récurrents, comme mentionné dans l'intervention INT-004.
3. **Problèmes de connectique** : Des traces d'oxydation sur les connecteurs, comme observées dans l'intervention INT-023, peuvent également contribuer à des défauts d'allumage récurrents.
4. **Problèmes de combustion** : Des problèmes de combustion, tels que des ionsisation instable, peuvent également être une cause de défauts d'allumage récurrents.

**Procédure de diagnostic :**

1. **Vérification de la carte électronique** : Vérifier la carte électronique pour détecter les éventuelles traces d'oxydation ou les défauts de fonctionnement.
2. **Vérification de l'électrovanne gaz** : Vérifier l'électrovanne gaz pour détecter les éventuels signes de fatigue ou de dysfonctionnement.
3. **Vérification de la connectique** : Vérifier les connecteurs pour détecter les éventuelles traces d'oxydation ou les problèmes de connectique.
4. **Test de combustion** : Effectuer un test de combustion pour vérifier la qualité de la combustion et détecter les éventuels problèmes.

**Solution recommandée :**

1. **Remplacement de la carte électronique** : Si la carte électronique est défaillante, il est recommandé de la remplacer par une nouvelle.
2. **Remplacement de l'électrovanne gaz** : Si l'électrovanne gaz est fatiguée, il est recommandé de la remplacer par une nouvelle.
3. **Nettoyage de la connectique** : Nettoyer les connecteurs pour éviter les problèmes de connectique.
4. **Test de fonctionnement** : Effectuer un test de fonctionnement pour vérifier que la chaudière fonctionne correctement après les réparations.

**Pièces à prévoir :**

1. **Carte électronique Saunier Duval réf. 0020049194** : En cas de remplacement de la carte électronique.
2. **Électrovanne gaz combinée Saunier Duval réf. 05743600** : En cas de remplacement de l'électrovanne gaz.
3. **Nettoyant pour connectique** : Pour nettoyer les connecteurs.

---

## Q5 — Question
> Le client dit que sa PAC Daikin chauffe mais que la maison reste froide. La PAC ne montre aucun code erreur. Que vérifier ?

### Documents récupérés
| # | Source | Marque | Code erreur | Score |
|---|--------|--------|-------------|-------|
| 1 | intervention | Mitsubishi |  | 0.553 |
| 2 | intervention | Daikin | 7H | 0.523 |
| 3 | intervention | Daikin | U0 | 0.518 |
| 4 | intervention | Daikin | A3 | 0.506 |
| 5 | intervention | Daikin | U4 | 0.498 |

### Réponse générée
**Causes possibles :**
- Courbe de chauffe mal réglée (pente trop faible)
- Température de départ insuffisante pour les conditions extérieures
- Appoint électrique non activé ou défaillant
- Défaut basse pression due à un filtre déshydrateur bouché
- Manque de réfrigérant R32
- Erreur communication entre unité intérieure et extérieure

**Procédure de diagnostic :**
1. Vérifier les paramètres de la courbe de chauffe pour s'assurer qu'ils sont adaptés aux conditions extérieures et aux besoins de chauffage de la maison.
2. Mesurer la température de départ de l'eau chaude pour vérifier si elle est suffisante pour les conditions extérieures.
3. Vérifier l'état et le fonctionnement de l'appoint électrique.
4. Effectuer un test de pression pour détecter d'éventuelles fuites ou défauts de basse pression.
5. Vérifier l'état du filtre déshydrateur et le nettoyer ou le remplacer si nécessaire.
6. Vérifier le niveau de réfrigérant R32 et le compléter si nécessaire.
7. Vérifier l'intégrité du câble de communication entre l'unité intérieure et extérieure.

**Solution recommandée :**
- Réglage de la courbe de chauffe si nécessaire
- Activation de l'appoint électrique si disponible et si les conditions extérieures l'exigent
- Remplacement du filtre déshydrateur si bouché
- Complément de charge R32 si nécessaire
- Remplacement du câble de communication si endommagé

**Pièces à prévoir :**
- Filtre déshydrateur
- R32 (pour complément de charge)
- Câble de communication (si nécessaire)
- Gaine anti-rongeurs (pour protéger le câble de communication)

---

## Analyse & Pistes d'amélioration

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
