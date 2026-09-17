---
title: "TARA Keyless Entry (étude de cas)"
summary: "Étude de cas pédagogique d'une TARA ISO/SAE 21434 appliquée à un système d'entrée et démarrage sans clé."
stack: ["ISO/SAE 21434", "TARA", "Python"]
status: "actif"
nature: "simulation pédagogique"
environment: "Environnement virtuel/local — aucun véhicule ou ECU physique"
order: 0
---

Étude de cas pédagogique d'une TARA appliquée à un système d'entrée et de démarrage sans clé (PKES / Keyless Entry), structurée à partir de la méthodologie ISO/SAE 21434.

Le modèle est volontairement simplifié et ne représente aucun produit, constructeur ou équipement réel. Les valeurs de risque, chemins d'attaque et contre-mesures sont utilisés à des fins d'apprentissage.

![Chaîne de traçabilité TARA du cas PKES : Damage Scenario, Threat Scenario, Attack Path, Cybersecurity Goal, Requirement, Vérification](/images/diagrams/tara-tracabilite-pkes.webp)

*Chaîne de traçabilité complète appliquée au modèle PKES fictif de cette étude de cas.*

## Démarche & Périmètre de l'Étude de Cas

![Matrice d'Analyse de Risque TARA Keyless Entry](/images/tara-matrix-diagram.svg)

Le raisonnement suit les étapes de la méthodologie :
1. **Item Definition** : périmètre du système PKES — antennes LF et RF, module PEPS, Body Control Module (BCM) et lien diagnostic.
2. **Asset Identification & Security Properties** : authenticité de la clé, confidentialité du secret partagé, intégrité des messages d'autorisation sur le réseau embarqué.
3. **Damage & Threat Scenarios** : formulation des dommages (accès non autorisé au véhicule, vol) puis des scénarios de menace correspondants.
4. **Attack Feasibility Rating** : évaluation par facteurs (temps requis, expertise, connaissance du système, fenêtre d'opportunité, équipement nécessaire).
5. **Risk Determination** : croisement de l'impact et de la faisabilité d'attaque pour situer le risque.
6. **Cybersecurity Goals & Requirements** : déduction des objectifs de cybersécurité puis des exigences associées, et discussion des mesures envisageables.

## Exemple de sortie générée par la simulation

```bash
$ python3 labs/tara_keyless/tara_engine.py --model pkes_case_study.json --report full
================================================================================
  TARA CASE STUDY ENGINE — PEDAGOGICAL SIMULATION
  Scope: Keyless Entry & Passive Start (simplified model)
  Real product: NO | Vehicle manufacturer: NONE (fictional model)
================================================================================
[INFO] Loading simplified system model (PEPS module, BCM, diagnostic link)...
[INFO] Assets and threat scenarios loaded. Evaluating illustrative risk values...

--- Threat Scenarios & Illustrative Risk Values ---
ID  | Threat Scenario                                  | Impact      | Feasibility | Risk
-----------------------------------------------------------------------------------------------
T01 | Relay attack sur la communication clé/véhicule   | Severe (4)  | Medium (2)  | [ 3 ]
T02 | Replay / spoofing d'une commande d'ouverture     | Severe (4)  | Medium (2)  | [ 3 ]
T03 | Accès diagnostic UDS non autorisé au BCM/PEPS    | Major (3)   | Low (3)     | [ 2 ]
T04 | Modification non autorisée du firmware           | Severe (4)  | Low (3)     | [ 3 ]
T05 | Injection CAN d'un message d'autorisation        | Severe (4)  | Medium (2)  | [ 3 ]
T06 | Extraction ou compromission d'un secret crypto.  | Severe (4)  | Low (3)     | [ 3 ]

--- Risk Treatment (illustrative) ---
T01 -> Mesure envisagée : mesure de distance robuste (ex. UWB ToF)
T02 -> Mesure envisagée : fraîcheur + authentification des commandes
T03 -> Mesure envisagée : contrôle d'accès diagnostic et cloisonnement des sessions
T06 -> Mesure envisagée : stockage des secrets en zone matérielle protégée

R155 context: this case study illustrates risk identification, traceability
and risk-treatment reasoning. It is not a conformity assessment or
type-approval evaluation.
```

## Ce que l'étude de cas permet de travailler

- **Raisonnement de bout en bout** : partir d'un dommage redouté, remonter aux scénarios de menace, puis descendre jusqu'à une exigence traçable.
- **Cohérence du périmètre** : tous les scénarios retenus restent dans le champ du système PKES/BCM, ce qui est une condition de qualité d'une TARA.
- **Discussion des mesures** : par exemple, l'Ultra-Wideband (IEEE 802.15.4z) avec mesure du temps de vol est souvent cité comme réponse aux attaques par relais — l'étude sert à comprendre pourquoi cette mesure adresse ce scénario précis, et non à affirmer un choix produit.
- **Rapport de synthèse JSON de démonstration** : [public/logs/tara_keyless_report.json](/logs/tara_keyless_report.json).

### Note sur les Cybersecurity Assurance Levels (CAL)

La TARA permet de déterminer et traiter les risques à partir de l'impact et de la faisabilité d'attaque. L'ISO/SAE 21434 présente également, dans son annexe E informative, le concept de Cybersecurity Assurance Level (CAL) pour exprimer un niveau de rigueur d'assurance ; celui-ci n'est toutefois pas une simple conversion directe du score de risque.

> Les valeurs d'impact, de faisabilité et de risque présentées ci-dessus sont des données de démonstration servant à illustrer la méthode. Elles ne constituent pas l'évaluation d'un produit réel.
