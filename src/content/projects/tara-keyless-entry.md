---
title: "TARA Keyless Entry"
summary: "Analyse de risque ISO/SAE 21434 complète sur un système d'entrée sans clé."
stack: ["ISO/SAE 21434", "TARA", "Medini Analyze"]
status: "archivé"
order: 1
---

Analyse de risque cybersécurité (**TARA - Threat Analysis and Risk Assessment**) menée de bout en bout sur un système d'entrée et démarrage sans clé (PKES / Keyless Go), selon les méthodologies d'homologation **ISO/SAE 21434** et le règlement **UNECE R155**.

![Capture Terminal - Moteur d'Analyse TARA Python](/images/labs/tara_keyless_terminal.png)

## Matrice de Risque & Architecture TARA

![Matrice d'Analyse de Risque TARA Keyless Entry](/images/tara-matrix-diagram.svg)

Le processus d'analyse s'articule autour de 6 étapes normalisées :
1. **Item Definition** : Périmètre du calculateur Gateway, des antennes LF 125 kHz et RF 433 MHz, et du Body Control Module (BCM).
2. **Asset Identification & Security Properties** : Propriétés d'authenticité de la clé, confidentialité de la clé partagée AES-128, et intégrité du bus CAN.
3. **Threat Scenarios & Damage Assessment** : Évaluation des dommages sur la sécurité des personnes (Impact 4) et financières/opérationnelles.
4. **Attack Feasibility Rating** : Méthode basée sur les facteurs (Temps requis, Expertise, Connaissance du composant, Fenêtre d'opportunité, Matériel nécessaire).
5. **Risk Determination** : Matrice croisant l'Impact (1 à 4) et la Faisabilité (1 à 4) pour attribuer un niveau de risque global de 1 à 5.
6. **Cybersecurity Goals & Requirements** : Déduction des exigences techniques (ex: protocole UWB à mesure de temps de vol ToF pour contrer les relais).

## Traces d'Exécution du Moteur d'Analyse TARA (Python 3 CLI)

```bash
$ python3 labs/tara_keyless/tara_engine.py --model V2G_system.json --report full
================================================================================
  ISO/SAE 21434 & UNECE R155 TARA ENGINE v1.2.1
  Target System: Keyless Entry & Passive Start Subsystem
================================================================================
[INFO] Loading Vehicle System Model (ECU: Gateway, Infotainment, Engine Ctrl)...
[INFO] 18 Assets, 42 Threat Scenarios identified. Evaluating Risks...

--- TARA Threat Analysis & Risk Matrix ---
ID  | Asset / Attack Scenario               | Impact  | Attack Feasibility | Risk Level | Mitigation Status
---------------------------------------------------------------------------------------------------------
T01 | Relay Attack (Keyless Go)            | Severe (L4) | Medium (2)       | [ RISK 3 ] | Mitigated (UWB ToF)
T02 | UDS Seed-Key Bypass                  | Severe (L4) | High (1)         | [ RISK 4 ] | Critical (Remediation Req.)
T03 | Firmware Mod via OBD                 | Major (L3)  | Low (3)          | [ RISK 2 ] | Adequate
T04 | Denial of Service (CAN Bus)          | Minor (L2)  | High (1)         | [ RISK 1 ] | Adequate
T05 | Sensor Spoofing (LiDAR / Camera)     | Moderate(L3)| Medium (2)       | [ RISK 3 ] | Partial (Filtering)
T06 | Root Access (IVI OS / Linux)         | Severe (L4) | High (1)         | [ RISK 4 ] | Critical (Hardening Req.)

--- Detailed Attack Feasibility Scores ---
Relay Attack: Impact: 4, Feasibility: 2 -> Risk Score: 8 (Level 3) [YELLOW] CAL 3
UDS Seed-Key Bypass: Impact: 4, Feasibility: 1 -> Risk Score: 16 (Level 4) [RED] CAL 4

--- TARA Status & UNECE R155 Compliance Summary ---
[ CAL 3 ] Overall Target Cybersecurity Assurance Level (System)
[ CAL 4 ] Threshold breached by Critical Threats: T02, T06.
[UNRESOLVED] 2 Critical Threats identified (CAL 4 impact). R155 compliance requires mitigation.

Compliance Check: UNECE R155 -> FAILED for CAL 4 requirements (Sec 7.3, Annex 5).
Remediation required for all Risk 4 threats before homologation certification.
```

## Résultats & Rapports d'Audit

- **Rapport de synthèse JSON** : téléchargeable à l'adresse [public/logs/tara_keyless_report.json](/logs/tara_keyless_report.json).
- **Mesure de sécurité retenue** : Intégration de la technologie Ultra-Wideband (UWB) IEEE 802.15.4z avec mesure précise du Temps de Vol (ToF) pour rejeter les signaux amplifiés à distance par les boîtiers relais.

