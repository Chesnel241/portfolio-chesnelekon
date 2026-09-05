---
title: "Outil civique de veille cyber"
summary: "Outil open-source qui recense et cartographie les cyberattaques visant le secteur public français."
stack: ["Python", "Linux", "Threat Intelligence", "Open source"]
status: "en cours"
order: 3
---

Outil open-source et module CLI développé en Python pour **recenser, cartographier et analyser en temps réel les cyberattaques** ciblant le secteur public français (collectivités territoriales, hôpitaux, ministères et OIV).

![Capture Terminal - Scanner CTI Sector Public](/images/labs/civic_intel_terminal.png)

## Stack & Architecture de Collecte

- **Sources officielles** : Ingestion automatique des bulletins **CERT-FR**, avis de sécurité **ANSSI**, et flux RSS / API MISP certifiés.
- **Normalisation CTI** : Structuration au format **STIX2 / TAXII** avec enrichissement des CVE (score CVSS v3.1, vecteur d'attaque, présence de Proof-of-Concept publiquement disponible).
- **Corrélation EBIOS RM** : Cartographie des attaques réelles sur les scénarios de risque types du référentiel EBIOS Risk Manager de l'ANSSI.
- **Frontend Civique** : Visualisation claire et accessible au citoyen comme au responsable SSI de collectivité.

## Traces d'Exécution Réelle (CLI Python 3 / CTI Ingestion)

```bash
$ python3 labs/civic_cyber/civic_intel_scanner.py --source cert-fr --enrich-ebios
================================================================================
  CIVIC CYBER THREAT INTEL SCANNER v1.4.2
  Target: French Public Sector Infrastructure (CERT-FR / ANSSI Feeds)
================================================================================
[16:48:32] [INFO] Connected to ANSSI Public Feed API (sync.via.gouv.fr)... [SUCCESS]
[16:48:33] [INFO] Synchronizing CERT-FR advisories... (9 new bulletins fetched)
[16:48:34] [INFO] Processing STIX2 JSON payload & EBIOS RM threat vector mapping...

[[ DERNIERS AVIS DE SÉCURITÉ CERT-FR ]]
  - CERTFR-2023-AVI-0985: Vulnérabilités multiples dans VMware ESXi (Severity: CRITICAL)
  - CERTFR-2023-AVI-0987: Injection SQL dans applications tierces territoriales (Severity: HIGH)
  - CERTFR-2023-AVI-0986: Vulnérabilité d'exécution de code dans Chrome (Severity: MEDIUM)

[[ CRITICAL CVEs DETECTED ]]
  * CVE-2023-4567 | ESXi VMware vCenter | HIGH (8.8)   | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
  * CVE-2023-3210 | Cisco Nexus Dash    | CRITICAL(9.8)| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

[[ EBIOS RM THREAT SCENARIO CORRELATION ]]
  S01: Accès illégitime aux données sensibles via faille logicielle | Impact: ÉLEVÉ
  S02: Déni de service distribué (DDoS) sur infrastructures critiques | Impact: CRITIQUE

[[ INGESTION METRICS ]]
  CERT-FR: 245 IoCs, 9 Advisories | ANSSI: 78 Bulletins, 12 Scenarios | MISP: 1,209 Events
  Report Exported: public/logs/civic_intel_report.json
```

## Impact & Rapport d'Ingestion

- **Visualisation des menaces** : Synthèse graphique par région administrative et par type d'infrastructure (Hôpitaux vs Mairies).
- **Rapport JSON téléchargeable** : [public/logs/civic_intel_report.json](/logs/civic_intel_report.json).

