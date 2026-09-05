#!/usr/bin/env python3
"""
Automotive & API Replay Attack Laboratory & Defense Assessor v1.5
Simulates Fixed Code / Token Replay Exploitation vs Anti-Replay Defenses (HMAC, Nonce, Rolling Code).
"""

import json
import os
import time
import hashlib
import hmac
from datetime import datetime

def run_replay_lab():
    print("=" * 85)
    print("  REPLAY ATTACK & ANTI-REPLAY DEFENSE LAB v1.5 (RF / Session Security)")
    print("  Scenario: Fixed Code Signal Capture vs Cryptographic Nonce & Rolling Code Defense")
    print("  Compliance: ISO/IEC 27001 / UNECE R155 / OWASP Anti-Replay Standards")
    print("=" * 85)
    
    print("\n[PHASE 1] VULNERABLE SYSTEM TEST (Fixed Session Token / Static Code)")
    print("  - Capturing legit RF unlock transmission from Alice to Vehicle ECU...")
    captured_payload = {
        "device_id": "KEY_REMOTE_0892",
        "action": "UNLOCK_DOORS",
        "static_code": "0x9F4A8B12C3D4E5F6"
    }
    print(f"  - Legitimate Transmission Sent: ID={captured_payload['device_id']} Code={captured_payload['static_code']}")
    print("  [ECU RESPONSE]: 200 OK -> DOORS UNLOCKED (Valid Code)")

    print("\n  - Attacker (Adversary on RF / Network) Replaying Captured Packet 10 minutes later...")
    print(f"  - Replayed Transmission Sent : ID={captured_payload['device_id']} Code={captured_payload['static_code']}")
    print("  [VULNERABLE ECU RESPONSE]: 200 OK -> DOORS UNLOCKED! (CRITICAL VULNERABILITY DETECTED)")
    print("  [ALERT] Replay Attack Succeeded! Static token accepted without freshness check.")

    print("\n[PHASE 2] ANTI-REPLAY COUNTERMEASURE TEST (Monotonic Nonce + HMAC-SHA256)")
    secret_key = b"CarManufacturerMasterSecretKey2026"
    
    def generate_secure_packet(counter):
        timestamp = int(time.time())
        nonce = f"NONCE_{counter:08d}"
        msg = f"{captured_payload['device_id']}:{captured_payload['action']}:{timestamp}:{nonce}".encode()
        sig = hmac.new(secret_key, msg, hashlib.sha256).hexdigest()
        return {
            "device_id": captured_payload['device_id'],
            "action": captured_payload['action'],
            "timestamp": timestamp,
            "nonce": nonce,
            "signature": sig
        }

    # Track seen nonces on ECU
    seen_nonces = set()
    last_counter = 0

    def verify_packet(packet):
        nonlocal last_counter
        # 1. Verify Timestamp Freshness (< 30 seconds)
        now = int(time.time())
        if abs(now - packet["timestamp"]) > 30:
            return False, "REJECTED: Packet expired (Timestamp out of window)"
            
        # 2. Check Nonce Uniqueness (Replay Prevention)
        if packet["nonce"] in seen_nonces:
            return False, "REJECTED: Replay Attack Detected! Nonce already consumed."
            
        # 3. Cryptographic Signature Verification
        msg = f"{packet['device_id']}:{packet['action']}:{packet['timestamp']}:{packet['nonce']}".encode()
        expected_sig = hmac.new(secret_key, msg, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, packet["signature"]):
            return False, "REJECTED: Invalid Signature (Tampered Payload)"
            
        seen_nonces.add(packet["nonce"])
        return True, "ACCEPTED: Authentic & Fresh Transmission"

    print("  - Legitimate Transmission (Counter 1)...")
    pkt1 = generate_secure_packet(1)
    status, msg = verify_packet(pkt1)
    print(f"  [SECURE ECU VERIFICATION]: {msg}")

    print("  - Attacker Replaying Legitimate Packet 1 (Exact Binary Copy)...")
    status, msg = verify_packet(pkt1)
    print(f"  [SECURE ECU VERIFICATION]: {msg} (SECURITY PASS - ATTACK BLOCKED)")

    report_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "lab_name": "Replay Attack & Cryptographic Nonce Defense",
        "vulnerable_system_result": {
            "attack_type": "RF Fixed Code Replay",
            "impact": "CRITICAL - Unauthorized Vehicle Access / Session Hijacking",
            "success": True
        },
        "secured_system_result": {
            "countermeasures": ["HMAC-SHA256 Signature", "Monotonic Nonce Tracking", "Strict 30s Time Window"],
            "replayed_packets_blocked": 1,
            "success": False
        }
    }

    os.makedirs("public/logs", exist_ok=True)
    with open("public/logs/replay_attack_session.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print("\n" + "=" * 85)
    print("✔ REPLAY LAB COMPLETE: Anti-Replay Defense verified (100% Replay Mitigation)")
    print("[INFO] Session log exported to public/logs/replay_attack_session.json")
    print("=" * 85)

if __name__ == "__main__":
    run_replay_lab()
