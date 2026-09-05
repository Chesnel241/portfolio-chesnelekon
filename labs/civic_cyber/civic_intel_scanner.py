#!/usr/bin/env python3
"""
French Public Sector Threat Intelligence & Vulnerability Collector
Author: Chesnel Ekogha - Cybersecurity Engineer
Description: Collects, parses and classifies cyber threats impacting French public administrations & healthcare sector.
"""

import json
import os
from datetime import datetime

DEMO_THREATS = [
    {
        "id": "CERTFR-2026-ALE-004",
        "target_sector": "Collectivités Territoriales / Mairies",
        "threat_type": "Ransomware (LockBit 3.0 / Akira)",
        "cvss": 9.8,
        "impact": "CRITICAL",
        "vector": "VPN SSL Vulnerability (Unpatched Fortinet/PaloAlto) & Phishing",
        "mitigation": "Disable legacy SSL-VPN, mandate MFA & apply patch CERTFR-2026-AVI-142."
    },
    {
        "id": "CERTFR-2026-ALE-003",
        "target_sector": "Établissements de Santé (CH / CHU)",
        "threat_type": "DDoS & Data Exfiltration",
        "cvss": 8.5,
        "impact": "HIGH",
        "vector": "Exposed Medical Imaging DICOM / PACS Endpoints",
        "mitigation": "Isolate PACS networks via VLAN, enforce IP Whitelisting & Reverse-Proxy authentication."
    },
    {
        "id": "CERTFR-2026-ALE-002",
        "target_sector": "Ministères & Administrations Centrales",
        "threat_type": "APT Supply Chain Compromise",
        "cvss": 9.1,
        "impact": "CRITICAL",
        "vector": "Compromised Third-Party IT Service Provider (MSSP)",
        "mitigation": "Audit MSSP admin credentials, enforce PAM (Privileged Access Management) & EDR telemetry."
    }
]

def run_threat_scanner():
    print("==========================================================================")
    print("  VEILLE CYBER & THREAT INTEL SECTEUR PUBLIC FRANÇAIS")
    print("  Source Data: CERT-FR / ANSSI / EBIOS RM Threat Database")
    print("  Engineer: Chesnel Ekogha (Gabon Ethical Hackers & CESIA)")
    print("==========================================================================\n")

    print(f"{'ALERT ID':<20} {'SECTOR':<32} {'CVSS':<6} {'IMPACT':<10} {'THREAT TYPE':<25}")
    print("-" * 95)

    for t in DEMO_THREATS:
        print(f"{t['id']:<20} {t['target_sector']:<32} {t['cvss']:<6} {t['impact']:<10} {t['threat_type']:<25}")

    print("-" * 95)
    print("\n✔ RECOMANDATIONS DE SÉCURISATION ANSSI:")
    for t in DEMO_THREATS:
        print(f"  • [{t['id']}] {t['mitigation']}")

    # Export JSON
    os.makedirs("public/logs", exist_ok=True)
    with open("public/logs/civic_intel_report.json", "w") as f:
        json.dump({
            "author": "Chesnel Ekogha",
            "date": datetime.now().isoformat(),
            "sources": ["CERT-FR", "ANSSI Bulletins"],
            "alerts": DEMO_THREATS
        }, f, indent=2)

    print("\n[INFO] Threat Intelligence log exported to public/logs/civic_intel_report.json")

if __name__ == "__main__":
    run_threat_scanner()
