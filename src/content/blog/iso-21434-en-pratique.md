---
title: "ISO 21434 en pratique : ce que ça change pour l'ingénierie des exigences"
excerpt: "La norme ISO/SAE 21434 et le règlement UNECE R155 structurent la cybersécurité automobile autour de la traçabilité des exigences et de la TARA. Explication technique et démonstration outillée."
date: 2026-07-15
tags: ["automotive", "iso-21434", "tara", "requirements-engineering"]
draft: false
---

L'ISO/SAE 21434 encadre la gestion de la cybersécurité tout au long du cycle de vie d'un véhicule : conception, développement, production, exploitation, jusqu'à la fin de vie. Sur le papier, c'est un cadre de gouvernance. En pratique, ça change concrètement la façon dont on écrit, on calcule le risque et on trace les exigences de sécurité.

![Capture Terminal - Moteur d'Analyse TARA ISO/SAE 21434](/images/labs/tara_keyless_terminal.png)

## Trois piliers méthodologiques en ingénierie automobile

**1. La traçabilité stricte TARA -> Exigences -> Tests.**
Chaque exigence de sécurité doit pouvoir remonter jusqu'à une menace identifiée (via une **TARA - Threat Analysis and Risk Assessment**) et descendre jusqu'à sa vérification sur banc de test ou bus CAN. Un identifiant d'exigence (ex: `SEC-REQ-PKES-042`) n'est pas juste une référence pratique : c'est une preuve d'audit opposable pour l'homologation UNECE R155.

![Exemple de Matrice de Risque TARA sous ISO/SAE 21434](/images/tara-matrix-diagram.svg)

**2. Le calcul de risque et les niveaux CAL (Cybersecurity Assurance Level).**
La TARA évalue chaque scénario de menace selon deux axes :
- **Impact (Severe 4, Major 3, Moderate 2, Negligible 1)** : Sécurité des personnes, pertes financières, atteinte à la vie privée.
- **Faisabilité d'attaque (High 1, Medium 2, Low 3, Very Low 4)** : Basée sur le temps d'attaque, l'expertise, les connaissances requises et le matériel.

Le score combiné définit le niveau d'assurance requis (**CAL 1 à CAL 4**), qui impose la rigueur de développement et de revue du composant.

**3. Automatisation de l'évaluation TARA via CLI.**

Dans le cadre du projet [TARA Keyless Entry](/projets/tara-keyless-entry), un moteur d'évaluation en Python a été développé pour parser la topologie du système et calculer dynamiquement les scores de risque et le statut de conformité R155 :

```bash
$ python3 labs/tara_keyless/tara_engine.py --model V2G_system.json --report summary
================================================================================
  ISO/SAE 21434 & UNECE R155 TARA ENGINE v1.2.1
================================================================================
[T01] Relay Attack (Keyless Go)    : Impact 4 | Feasibility 2 -> RISK 3 [CAL 3] (Mitigated)
[T02] UDS Seed-Key Bypass          : Impact 4 | Feasibility 1 -> RISK 4 [CAL 4] (Critical)
[T06] Root Access (IVI OS / Linux) : Impact 4 | Feasibility 1 -> RISK 4 [CAL 4] (Critical)

[ CAL 4 ] Threshold breached by Critical Threats: T02, T06.
Compliance Check: UNECE R155 -> FAILED for CAL 4 requirements (Sec 7.3, Annex 5).
```

## Ce que ça implique au quotidien pour l'ingénieur

Sur le terrain, la démarche ISO 21434 transforme les échanges entre équipes sécurité et équipes système :
- Les exigences ne sont plus écrites de manière générique ("le système doit être sécurisé"), mais formulées comme des contre-mesures explicites adressant une menace identifiée (ex: "L'ECU Gateway doit rejeter toute demande UDS Security Access 0x27 après 3 tentatives infructueuses et déclencher une période de blocage de 60s").
- La matrice de traçabilité est tenue à jour en continu et versionnée dans les dépôts de code.

