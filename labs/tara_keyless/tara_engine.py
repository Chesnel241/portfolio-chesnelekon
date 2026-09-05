#!/usr/bin/env python3
"""
TARA Risk Assessment & Feasibility Calculation Engine (ISO/SAE 21434 & EBIOS RM)
Author: Chesnel Ekogha - Automotive Cybersecurity Engineer
Description: Calculates Attack Feasibility Rating (AFR) & Impact Ratings to deduce Cybersecurity Goals (CSG).
"""

import json
import os
from datetime import datetime

# ISO/SAE 21434 Annex H Values
FEASIBILITY_TABLE = {
    "elapsed_time": {"< 1 day": 0, "< 1 week": 1, "< 1 month": 2, "< 6 months": 3, "> 6 months": 4},
    "expertise": {"layman": 0, "proficient": 1, "expert": 2, "multiple_experts": 3},
    "knowledge": {"public": 0, "restricted": 1, "confidential": 2, "strict_secret": 3},
    "opportunity": {"unlimited": 0, "easy": 1, "moderate": 2, "difficult": 3},
    "equipment": {"standard": 0, "specialized": 1, "bespoke": 2}
}

THREAT_SCENARIOS = [
    {
        "id": "TS-01",
        "title": "Relay Attack on Keyless Fob (125kHz LF / 433MHz UHF)",
        "asset": "Keyless Door Locking & Engine Start Signal",
        "attack_path": "Attacker uses dual-transceiver relay RF hardware to extend key fob signal range up to 100m.",
        "feasibility": {"elapsed_time": "< 1 day", "expertise": "proficient", "knowledge": "public", "opportunity": "easy", "equipment": "specialized"},
        "impact": {"safety": "Low", "financial": "High", "operational": "Medium", "privacy": "Medium"},
        "csg": "CSG-01: Protect against LF/UHF signal relay attacks using Time-of-Flight (UWB) distance bounding."
    },
    {
        "id": "TS-02",
        "title": "RF Replay Attack on Unencrypted Unlock Code",
        "asset": "Rolling Code Counter & MAC Integrity",
        "attack_path": "SDR (Software Defined Radio) captures rolling code frame and replays sequence during RF jam.",
        "feasibility": {"elapsed_time": "< 1 week", "expertise": "proficient", "knowledge": "public", "opportunity": "easy", "equipment": "standard"},
        "impact": {"safety": "Negligible", "financial": "High", "operational": "Low", "privacy": "Low"},
        "csg": "CSG-02: Ensure strict freshness value manager (FVM) and anti-replay counters on RF frames."
    },
    {
        "id": "TS-03",
        "title": "UDS SecurityAccess Key Bruteforce on Door ECU",
        "asset": "ECU Firmware & Cryptographic Master Key",
        "attack_path": "OBD-II diagnostic tool sends Seed-Key request 0x27 and bruteforces 16-bit key.",
        "feasibility": {"elapsed_time": "< 1 day", "expertise": "layman", "knowledge": "public", "opportunity": "unlimited", "equipment": "standard"},
        "impact": {"safety": "Moderate", "financial": "High", "operational": "High", "privacy": "High"},
        "csg": "CSG-03: Implement 32-bit/128-bit HSM Seed-Key algorithm with exponential penalty delay per failed attempt."
    },
    {
        "id": "TS-04",
        "title": "CAN Frame Injection & Spoofing on Powertrain Bus",
        "asset": "Engine Start Authorization CAN Message",
        "attack_path": "Physical compromise of headlight/radar wiring harness to inject CAN ID 0x120 start command.",
        "feasibility": {"elapsed_time": "< 1 week", "expertise": "proficient", "knowledge": "restricted", "opportunity": "easy", "equipment": "specialized"},
        "impact": {"safety": "Severe", "financial": "High", "operational": "High", "privacy": "Low"},
        "csg": "CSG-04: Mandate AUTOSAR SecOC (Secure Onboard Communication) with AES-CMAC authenticators on Start CAN frames."
    }
]

def calculate_attack_feasibility_score(f_dict):
    score = (
        FEASIBILITY_TABLE["elapsed_time"][f_dict["elapsed_time"]] +
        FEASIBILITY_TABLE["expertise"][f_dict["expertise"]] +
        FEASIBILITY_TABLE["knowledge"][f_dict["knowledge"]] +
        FEASIBILITY_TABLE["opportunity"][f_dict["opportunity"]] +
        FEASIBILITY_TABLE["equipment"][f_dict["equipment"]]
    )
    # ISO/SAE 21434 Rating: 0-2: High Feasibility, 3-7: Medium, 8-13: Low, >=14: Very Low
    if score <= 2:
        return score, "HIGH"
    elif score <= 7:
        return score, "MEDIUM"
    elif score <= 13:
        return score, "LOW"
    else:
        return score, "VERY LOW"

def run_tara_assessment():
    print("==========================================================================")
    print("  ISO/SAE 21434 & EBIOS RM RISK ASSESSMENT ENGINE")
    print("  Target System: Automotive Keyless Entry & Start System (KESS)")
    print("  Engineer: Chesnel Ekogha | Document Ref: TARA-KESS-2026-V3")
    print("==========================================================================\n")

    results = []

    print(f"{'ID':<7} {'THREAT SCENARIO':<40} {'FEASIBILITY':<14} {'IMPACT':<12} {'RISK LEVEL':<12}")
    print("-" * 90)

    for ts in THREAT_SCENARIOS:
        score, feat_rating = calculate_attack_feasibility_score(ts["feasibility"])
        max_impact = max(ts["impact"].values(), key=lambda x: ["Negligible", "Low", "Medium", "Moderate", "High", "Severe"].index(x))
        
        # Risk Matrix Lookup
        if feat_rating in ["HIGH", "MEDIUM"] and max_impact in ["High", "Severe"]:
            risk_level = "CRITICAL (Risk 5)"
        elif feat_rating == "MEDIUM" or max_impact in ["High", "Moderate"]:
            risk_level = "HIGH (Risk 4)"
        else:
            risk_level = "MEDIUM (Risk 3)"

        results.append({
            "id": ts["id"],
            "title": ts["title"],
            "asset": ts["asset"],
            "attack_path": ts["attack_path"],
            "feasibility_score": score,
            "feasibility_rating": feat_rating,
            "max_impact": max_impact,
            "risk_level": risk_level,
            "csg": ts["csg"]
        })

        print(f"{ts['id']:<7} {ts['title'][:38]:<40} {feat_rating:<14} {max_impact:<12} {risk_level:<12}")

    print("-" * 90)
    print("\n✔ DERIVED CYBERSECURITY GOALS (CSG):")
    for r in results:
        print(f"  • [{r['id']}] {r['csg']}")

    # Export to public logs
    os.makedirs("public/logs", exist_ok=True)
    with open("public/logs/tara_keyless_report.json", "w") as f:
        json.dump({
            "system": "Keyless Entry & Passive Start (KESS)",
            "standard": "ISO/SAE 21434 Clause 15 & Annex H",
            "author": "Chesnel Ekogha",
            "date": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)

    print("\n[INFO] TARA Risk Report exported to public/logs/tara_keyless_report.json")

if __name__ == "__main__":
    run_tara_assessment()
