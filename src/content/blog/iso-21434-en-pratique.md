---
title: "ISO 21434 en pratique : ce que ça change pour l'ingénierie des exigences"
excerpt: "La norme ISO/SAE 21434 et le règlement UNECE R155 structurent la cybersécurité automobile autour de la traçabilité des exigences et de la TARA. Explication technique et démonstration outillée."
date: 2026-07-15
tags: ["automotive", "iso-21434", "tara", "requirements-engineering"]
draft: false
---

L'ISO/SAE 21434 encadre la gestion de la cybersécurité tout au long du cycle de vie d'un véhicule : conception, développement, production, exploitation, jusqu'à la fin de vie. Sur le papier, c'est un cadre de gouvernance. En pratique, ça change concrètement la façon dont on écrit, on calcule le risque et on trace les exigences de sécurité.

![Capture Terminal - Moteur d'Analyse TARA ISO/SAE 21434](/images/labs/tara_keyless_terminal.png)

*Capture de démonstration issue de l'étude de cas pédagogique ; les valeurs proviennent d'un modèle fictif.*

## Trois piliers méthodologiques en ingénierie automobile

**1. La traçabilité stricte TARA -> Exigences -> Tests.**
Chaque exigence de sécurité doit pouvoir remonter jusqu'à une menace identifiée (via une **TARA - Threat Analysis and Risk Assessment**) et descendre jusqu'à son activité de vérification. Un identifiant d'exigence (ex: `SEC-REQ-PKES-042`) n'est pas qu'une référence pratique : c'est ce qui rend la couverture du risque démontrable lors des revues et des activités de conformité menées dans le contexte UNECE R155.

![Exemple de Matrice de Risque TARA sous ISO/SAE 21434](/images/tara-matrix-diagram.svg)

*Matrice d'illustration construite sur un modèle fictif, à des fins pédagogiques.*

**2. La détermination du risque, et la place des CAL.**
La TARA évalue chaque scénario de menace selon deux axes :
- **Impact (Severe 4, Major 3, Moderate 2, Negligible 1)** : Sécurité des personnes, pertes financières, atteinte à la vie privée, pertes opérationnelles.
- **Faisabilité d'attaque (High 1, Medium 2, Low 3, Very Low 4)** : Basée sur le temps d'attaque, l'expertise, les connaissances requises, la fenêtre d'opportunité et le matériel.

La TARA permet de déterminer et traiter les risques à partir de l'impact et de la faisabilité d'attaque. L'ISO/SAE 21434 présente également, dans son annexe E informative, le concept de Cybersecurity Assurance Level (CAL) pour exprimer un niveau de rigueur d'assurance ; celui-ci n'est toutefois pas une simple conversion directe du score de risque.

C'est une confusion fréquente et lourde de conséquences en revue : le risque se traite (réduction, transfert, acceptation, évitement), tandis qu'un CAL exprime le niveau de rigueur des activités d'assurance. Les deux notions se nourrissent l'une l'autre, mais lire un CAL directement dans une case de la matrice de risque n'est pas conforme à ce que dit la norme.

**3. Outiller le raisonnement TARA.**

Dans le cadre de l'étude de cas [TARA Keyless Entry](/projets/tara-keyless-entry) — un modèle pédagogique simplifié, sans lien avec un produit réel — un petit moteur Python sert à dérouler le calcul d'impact et de faisabilité sur un ensemble de scénarios et à en restituer le traitement :

```bash
$ python3 labs/tara_keyless/tara_engine.py --model pkes_case_study.json --report summary
================================================================================
  TARA CASE STUDY ENGINE — PEDAGOGICAL SIMULATION
  Real product: NO | Vehicle manufacturer: NONE (fictional model)
================================================================================
[T01] Relay attack sur la communication clé/véhicule : Impact 4 | Feasibility 2 -> RISK 3
[T02] Replay / spoofing d'une commande d'ouverture   : Impact 4 | Feasibility 2 -> RISK 3
[T03] Accès diagnostic UDS non autorisé au BCM/PEPS  : Impact 3 | Feasibility 3 -> RISK 2

Risk treatment recorded for each scenario (mitigate / accept / transfer / avoid).

R155 context: this case study illustrates risk identification, traceability
and risk-treatment reasoning. It is not a conformity assessment or
type-approval evaluation.
```

L'intérêt de l'outillage n'est pas le calcul lui-même — une feuille de calcul y suffirait — mais la **cohérence** : garantir qu'un scénario ajouté produit bien un objectif de cybersécurité, et que celui-ci porte une exigence traçable.

## Ce que ça implique au quotidien pour l'ingénieur

Sur le terrain, la démarche ISO 21434 transforme les échanges entre équipes sécurité et équipes système :
- Les exigences ne sont plus écrites de manière générique ("le système doit être sécurisé"), mais formulées comme des contre-mesures explicites adressant une menace identifiée, avec des valeurs fixées par la spécification du produit (ex: "L'ECU Gateway doit limiter le nombre de tentatives consécutives sur le service UDS SecurityAccess 0x27 et appliquer une temporisation de verrouillage après échec").
- La matrice de traçabilité est tenue à jour en continu et versionnée dans les dépôts de code.

