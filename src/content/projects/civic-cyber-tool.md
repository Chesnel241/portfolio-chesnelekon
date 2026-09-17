---
title: "Outil civique de veille cyber"
summary: "Prototype pédagogique d'ingestion et de corrélation de données CTI sur le secteur public français."
stack: ["Python", "Linux", "Threat Intelligence", "Open source"]
status: "en cours"
nature: "prototype"
environment: "Prototype local — jeux de données d'exemple, aucun flux opérationnel connecté"
order: 3
---

Prototype pédagogique de traitement de données CTI destiné à illustrer l'ingestion, la normalisation et la corrélation d'informations de cybersécurité relatives au secteur public français.

La démonstration utilise des jeux de données d'exemple et ne constitue pas un flux opérationnel CERT-FR, ANSSI ou MISP. Aucun connecteur vers ces sources n'est actif dans le prototype.

![Capture Terminal - Prototype CTI Secteur Public](/images/labs/civic_intel_terminal.png)

*Capture de démonstration du prototype, alimentée par un jeu de données d'exemple local.*

## Architecture Visée

- **Sources envisagées** : bulletins CERT-FR, avis de sécurité ANSSI, flux RSS et API MISP — modélisés ici par des fichiers d'exemple locaux.
- **Normalisation CTI** : structuration au format **STIX2 / TAXII** avec enrichissement des vulnérabilités (score CVSS v3.1, vecteur d'attaque, disponibilité d'une preuve de concept publique).
- **Corrélation EBIOS RM** : rapprochement entre les entrées ingérées et des scénarios de risque types du référentiel EBIOS Risk Manager.
- **Frontend civique** : restitution lisible pour le citoyen comme pour le responsable SSI d'une collectivité.

## Exemple de sortie générée par le prototype

```bash
$ python3 labs/civic_cyber/civic_intel_scanner.py --source sample-dataset --enrich-ebios
================================================================================
  CIVIC CYBER THREAT INTEL SCANNER — PEDAGOGICAL PROTOTYPE
  Data source: local sample dataset (no live feed connected)
  CERT-FR / ANSSI / MISP connectors: NOT ACTIVE
================================================================================
[16:48:32] [INFO] Loading local sample dataset... [OK]
[16:48:33] [INFO] Parsing demonstration advisories... (9 sample entries)
[16:48:34] [INFO] Processing STIX2 JSON payload & EBIOS RM threat vector mapping...

[[ AVIS DE SÉCURITÉ — DONNÉES DE DÉMONSTRATION ]]
  - DEMO-ADVISORY-001: Vulnérabilités multiples dans un hyperviseur (Severity: CRITICAL)
  - DEMO-ADVISORY-002: Injection SQL dans une application métier   (Severity: HIGH)
  - DEMO-ADVISORY-003: Exécution de code dans un navigateur        (Severity: MEDIUM)

[[ VULNÉRABILITÉS — IDENTIFIANTS FICTIFS ]]
  * CVE-20XX-XXXX | Sample hypervisor  | HIGH (8.8)    | CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
  * CVE-20XX-YYYY | Sample network OS  | CRITICAL (9.8)| CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

[[ EBIOS RM THREAT SCENARIO CORRELATION ]]
  S01: Accès illégitime aux données sensibles via faille logicielle | Impact: ÉLEVÉ
  S02: Déni de service distribué (DDoS) sur infrastructures critiques | Impact: CRITIQUE

[[ INGESTION METRICS — SAMPLE DATASET ]]
  DEMO-IOC entries: 245 | DEMO advisories: 9 | DEMO events: 1,209
  Report Exported: public/logs/civic_intel_report.json
```

## Ce que le prototype permet de travailler

- **Chaîne de traitement CTI** : ingestion, normalisation, enrichissement et corrélation, de bout en bout.
- **Restitution** : synthèse par région administrative et par type d'infrastructure, dans un format lisible par un public non spécialiste.
- **Rapport JSON de démonstration** : [public/logs/civic_intel_report.json](/logs/civic_intel_report.json).

> Les avis, identifiants de vulnérabilité et volumétries affichés ci-dessus sont délibérément fictifs (`DEMO-*`, `CVE-20XX-XXXX`). Ils ne reprennent aucune publication officielle et ne doivent pas être lus comme des données de veille réelles.
