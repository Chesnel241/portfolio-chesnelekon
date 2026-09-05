#!/usr/bin/env python3
"""
EBIOS Risk Manager (ANSSI) Threat Risk Engine & Compliance Assessor
Simulates complete 5-Atelier EBIOS RM risk modeling for an OIV / Public Health Infrastructure.
"""

import json
import os
import sys
from datetime import datetime

def run_ebios_analysis():
    print("=" * 85)
    print("  ANSSI EBIOS RISK MANAGER v2.4 (Evaluation Method & Threat Analysis Engine)")
    print("  Target Scope: Infrastructure Critique & Système d'Information Hospitalier (OIV)")
    print("  Compliance: ANSSI EBIOS RM 2018 / ISO 27005 / NIS 2 Directive")
    print("=" * 85)
    
    print("\n[ATELIER 1] SOCLE DE SÉCURITÉ & VALEURS MÉTIERS")
    print("  - Valeurs Métiers : Dossier Patient Informatisé (DPI), Pilotage Médical, Télé-médecine")
    print("  - Biens Supports  : Cluster Base de Données PostgreSQL, Serveur API REST, Postes de Travail")
    print("  - Événements Redoutés :")
    print("    * ER-01: Disponibilité DPI interrompue > 2h  | Impact: CRITIQUE (4/4)")
    print("    * ER-02: Fuite massive de données médicales   | Impact: CRITIQUE (4/4)")
    print("    * ER-03: Altération de la traçabilité soin   | Impact: ÉLEVÉ (3/4)")

    print("\n[ATELIER 2] SOURCES DE RISQUES (SR) & OBJECTIFS VISÉS (OV)")
    print("  - SR-01: Cybercriminels motivés par le gain (Ransomware/Exfiltration - Cybercrime Darknet)")
    print("    * OV-01: Extorsion financière par chiffrement et double-extorsion (LockBit/BlackCat pattern)")
    print("  - SR-02: État / Cyber-espionnage (APT)")
    print("    * OV-02: Espionnage stratégique et exfiltration de données de recherche médicale")

    print("\n[ATELIER 3] SCÉNARIOS STRATÉGIQUES (Cartographie de la Menace)")
    print("  - Parties Prenantes : Prestataire Cloud, Infogéreur SOC, Fournisseur Télé-maintenance")
    print("  - Scénario Stratégique SS-01 (Vecteur Supply Chain) :")
    print("    * Attaque initiale via compromission des identifiants VPN d'un sous-traitant (Dark Web Leak)")
    print("    * Pivotement du réseau d'infogérance vers le réseau interne SIH (Vraisemblance: 3/4)")

    print("\n[ATELIER 4] SCÉNARIOS OPÉRATIONNELS (Attaque & Modes Opératoires MITRE ATT&CK)")
    print("  - Mode Opératoire MO-01 :")
    print("    1. T1078 - Valid Accounts (Compromission accès VPN prestataire)")
    print("    2. T1068 - Exploitation for Privilege Escalation (PrivEsc Active Directory)")
    print("    3. T1486 - Data Encrypted for Impact & Exfiltration STIX2 (Ransomware)")
    print("  - Faisabilité Technique : ÉLEVÉE (3/4)")

    print("\n[ATELIER 5] TRAITEMENT DU RISQUE & PLAN D'ACTION CYBER")
    print("  - Mesures Réduisant le Risque (Plan d'Action ANSSI) :")
    print("    [M-01] MFA Obligatoire FIDO2 sur l'ensemble des accès VPN / Remote Desktop")
    print("    [M-02] Segmentation Micro-réseau Zero-Trust (802.1X & Pare-feu applicatif)")
    print("    [M-03] Bastion d'Administration avec enregistrement des sessions (PAM)")
    print("    [M-04] Détection EDR & Corrélation SIEM / SOC 24/7 avec règles de détection ANSSI")

    report_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "methodology": "ANSSI EBIOS Risk Manager 2018",
        "target_organization": "SIH - CHU Métropolitain (OIV)",
        "ateliers": {
            "atelier_1_socle": {
                "valeurs_metiers": ["DPI", "Pilotage Médical", "Télé-médecine"],
                "impact_max": 4
            },
            "atelier_2_sources_risques": [
                {"sr": "Cybercriminalité organisée", "motivation": "Financière / Ransomware"},
                {"sr": "APT d'État", "motivation": "Espionnage / Sabotage"}
            ],
            "atelier_3_scenarios_strategiques": [
                {"id": "SS-01", "name": "Compromission Supply Chain VPN", "vraisemblance": 3, "impact": 4, "niveau_risque": "CRITIQUE"}
            ],
            "atelier_4_scenarios_operationnels": [
                {"id": "MO-01", "mitre_techniques": ["T1078", "T1068", "T1486"], "faisabilite": 3}
            ],
            "atelier_5_traitement": [
                "MFA FIDO2", "Zero-Trust Microsegmentation", "PAM Admin Bastion", "EDR / XDR Managed SOC"
            ]
        },
        "risk_summary": {
            "initial_risk_score": 12,
            "residual_risk_score": 3,
            "status": "ACCEPTABLE AFTER REMEDIATION"
        }
    }

    os.makedirs("public/logs", exist_ok=True)
    with open("public/logs/ebios_risk_report.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print("\n" + "=" * 85)
    print("✔ EBIOS RM ASSESSMENT COMPLETE: 5 Ateliers Compiled | Risk Level reduced from CRITICAL to ACCEPTABLE")
    print("[INFO] Full risk audit report exported to public/logs/ebios_risk_report.json")
    print("=" * 85)

if __name__ == "__main__":
    run_ebios_analysis()
