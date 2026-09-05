---
title: "Lab EBIOS Risk Manager (ANSSI)"
summary: "Analyse de risque complète selon la méthode ANSSI EBIOS Risk Manager (Ateliers 1 à 5) sur une infrastructure critique OIV."
stack: ["EBIOS RM", "ANSSI", "ISO 27005", "Python", "MITRE ATT&CK"]
status: "actif"
order: 4
---

Analyse de risque structurée et outillée selon la méthode **ANSSI EBIOS Risk Manager (2018)** appliquée au Système d'Information Hospitalier (SIH) d'un Organisme d'Importance Vitale (OIV), en conformité avec la directive **NIS 2** et la norme **ISO/IEC 27005**.

![Capture Terminal - Moteur d'Analyse EBIOS Risk Manager ANSSI](/images/labs/ebios_rm_terminal.png)

## Cadre et Déroulement des 5 Ateliers EBIOS RM

Le laboratoire déroule l'intégralité du processus d'analyse de risque ANSSI à travers un moteur CLI développé en Python :

### 1. Atelier 1 : Socle de Sécurité & Valeurs Métiers
- **Valeurs Métiers** : Dossier Patient Informatisé (DPI), Systèmes de Prescription Médicale, Télé-médecine.
- **Biens Supports** : Base de données PostgreSQL, API REST, Postes de travail des praticiens, Réseau Wi-Fi médical.
- **Événements Redoutés (ER)** :
  - `ER-01` : Interruption de disponibilité du DPI > 2h (Impact: **CRITIQUE - 4/4**).
  - `ER-02` : Fuite massive de données de santé (Impact: **CRITIQUE - 4/4**).

### 2. Atelier 2 : Sources de Risques (SR) & Objectifs Visés (OV)
- **SR-01 (Cybercriminalité Darknet / Ransomware)** : Motivation financière via extorsion et double-exfiltration (Groupes type LockBit / BlackCat).
- **SR-02 (APT / Espionnage d'État)** : Infiltration discrète pour exfiltration de données de recherche biomédicale.

### 3. Atelier 3 : Scénarios Stratégiques (Cartographie de l'Écosystème)
- Évaluation des dépendances et de la **Supply Chain** : Prestataires Cloud, Infogéreur SOC externe, Télé-maintenance des équipements biomédicaux.
- **Scénario SS-01** : Infiltration initiale via compromission des identifiants VPN d'un sous-traitant (fuite de credentials identifiée sur les réseaux spécialisés) et pivot vers le réseau sensible.

### 4. Atelier 4 : Scénarios Opératoires & Matrice MITRE ATT&CK
- **Mode Opératoire (MO-01)** :
  1. `T1078 - Valid Accounts` : Exploitation d'accès VPN compromis.
  2. `T1068 - Exploitation for Privilege Escalation` : Élévation de privilèges Active Directory.
  3. `T1486 - Data Encrypted for Impact` : Chiffrement du SIH par Ransomware.

### 5. Atelier 5 : Traitement du Risque & Plan d'Action ANSSI
- **Mesures Correctives imposées** :
  - Enforcement du **MFA FIDO2 (YubiKey)** sur 100% des accès distants VPN / PAM.
  - Micro-segmentation du réseau selon les principes **Zero-Trust (802.1X)**.
  - Déploiement d'un Bastion d'Administration (PAM) avec session recording.
  - Supervision 24/7 via **EDR/XDR** interconnecté au SIEM du SOC.

## Traces d'Exécution du Moteur d'Analyse (Python 3 CLI)

```bash
$ python3 labs/ebios_rm/ebios_analysis.py
=====================================================================================
  ANSSI EBIOS RISK MANAGER v2.4 (Evaluation Method & Threat Analysis Engine)
  Target Scope: Infrastructure Critique & Système d'Information Hospitalier (OIV)
  Compliance: ANSSI EBIOS RM 2018 / ISO 27005 / NIS 2 Directive
=====================================================================================

[ATELIER 1] SOCLE DE SÉCURITÉ & VALEURS MÉTIERS
  - Valeurs Métiers : Dossier Patient Informatisé (DPI), Pilotage Médical, Télé-médecine
  - Événements Redoutés :
    * ER-01: Disponibilité DPI interrompue > 2h  | Impact: CRITIQUE (4/4)
    * ER-02: Fuite massive de données médicales   | Impact: CRITIQUE (4/4)

[ATELIER 2] SOURCES DE RISQUES (SR) & OBJECTIFS VISÉS (OV)
  - SR-01: Cybercriminels motivés par le gain (Ransomware/Exfiltration - Cybercrime Darknet)
  - SR-02: État / Cyber-espionnage (APT)

[ATELIER 3] SCÉNARIOS STRATÉGIQUES (Cartographie de la Menace)
  - SS-01 (Supply Chain VPN) : Vraisemblance 3/4 | Impact 4/4 | Niveau: CRITIQUE

[ATELIER 4] SCÉNARIOS OPÉRATIONNELS (MITRE ATT&CK)
  - MO-01 : T1078 (Valid Accounts) -> T1068 (PrivEsc) -> T1486 (Ransomware)

[ATELIER 5] TRAITEMENT DU RISQUE & PLAN D'ACTION CYBER
  [M-01] MFA Obligatoire FIDO2 sur l'ensemble des accès VPN
  [M-02] Segmentation Micro-réseau Zero-Trust
  [M-03] Bastion d'Administration PAM
  [M-04] Détection EDR & SOC Managed 24/7

✔ EBIOS RM ASSESSMENT COMPLETE: Risk Level reduced from CRITICAL to ACCEPTABLE
[INFO] Full risk audit report exported to public/logs/ebios_risk_report.json
```

## Rapports & Livrables

- **Rapport de synthèse au format JSON** : Téléchargeable sur [public/logs/ebios_risk_report.json](/logs/ebios_risk_report.json).
- **Conformité finale** : Réduction du score de risque de **12 (Critique)** à **3 (Acceptable)** après application des recommandations de l'Atelier 5.
