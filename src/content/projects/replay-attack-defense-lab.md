---
title: "Lab Attaque par Rejeu & Cryptographie Anti-Replay"
summary: "Démonstration expérimentale d'une attaque par rejeu sur protocole non sécurisé et mise en place de contre-mesures HMAC/Nonce."
stack: ["Python", "Cryptography", "HMAC-SHA256", "Nonce", "ISO/IEC 27001", "RF Security"]
status: "actif"
order: 5
---

Laboratoire complet d'analyse de vulnérabilité aux **attaques par rejeu (Replay Attacks)** sur les protocoles radiofréquence (RF) et API Web, suivi du développement et de la validation de contre-mesures cryptographiques (**Horodatage, Monotonic Nonce et HMAC-SHA256**).

![Capture Terminal - Session d'Attaque par Rejeu & Défense Anti-Replay](/images/labs/replay_attack_terminal.png)

## Concept & Vulnérabilité Traitée

Une **attaque par rejeu** consiste pour un attaquant à intercepter une transmission valide (jeton d'authentification API, trame radio de télécommande) et à la réémettre ultérieurement à l'identique pour usurper des privilèges sans connaître les secrets cryptographiques du système.

Ce laboratoire s'articule en deux phases expérimentales :
1. **Phase 1 : Système Vulnérable à Code Fixe / Jeton Statique**
   - Interception d'un paquet valide d'ouverture de session.
   - Rejeu du paquet 10 minutes plus tard sur le récepteur/ECU.
   - Constat : Le système valide la demande car il ne vérifie pas la fraîcheur du paquet (`200 OK`).
2. **Phase 2 : Implémentation du Protocole Anti-Replay (HMAC + Nonce Monotone)**
   - Ajout d'un compteur séquentiel à usage unique (**Nonce**), d'un horodatage Unix et d'une signature **HMAC-SHA256**.
   - Rejeu exact de la trame capturée.
   - Constat : Rejet immédiat par le récepteur (`REJECTED: Nonce already consumed`).

## Traces d'Exécution du Lab (Python 3 CLI)

```bash
$ python3 labs/replay_attack/replay_lab.py
=====================================================================================
  REPLAY ATTACK & ANTI-REPLAY DEFENSE LAB v1.5 (RF / Session Security)
  Scenario: Fixed Code Signal Capture vs Cryptographic Nonce & Rolling Code Defense
  Compliance: ISO/IEC 27001 / UNECE R155 / OWASP Anti-Replay Standards
=====================================================================================

[PHASE 1] VULNERABLE SYSTEM TEST (Fixed Session Token / Static Code)
  - Capturing legit RF unlock transmission from Alice to Vehicle ECU...
  - Legitimate Transmission Sent: ID=KEY_REMOTE_0892 Code=0x9F4A8B12C3D4E5F6
  [ECU RESPONSE]: 200 OK -> DOORS UNLOCKED (Valid Code)

  - Attacker Replaying Captured Packet 10 minutes later...
  - Replayed Transmission Sent : ID=KEY_REMOTE_0892 Code=0x9F4A8B12C3D4E5F6
  [VULNERABLE ECU RESPONSE]: 200 OK -> DOORS UNLOCKED! (CRITICAL VULNERABILITY DETECTED)
  [ALERT] Replay Attack Succeeded! Static token accepted without freshness check.

[PHASE 2] ANTI-REPLAY COUNTERMEASURE TEST (Monotonic Nonce + HMAC-SHA256)
  - Legitimate Transmission (Counter 1)...
  [SECURE ECU VERIFICATION]: ACCEPTED: Authentic & Fresh Transmission

  - Attacker Replaying Legitimate Packet 1 (Exact Binary Copy)...
  [SECURE ECU VERIFICATION]: REJECTED: Replay Attack Detected! Nonce already consumed.
  (SECURITY PASS - ATTACK BLOCKED)

=====================================================================================
✔ REPLAY LAB COMPLETE: Anti-Replay Defense verified (100% Replay Mitigation)
[INFO] Session log exported to public/logs/replay_attack_session.json
=====================================================================================
```

## Résultats & Recommandations Industrielles

- **Rapport de session JSON** : Téléchargeable sur [public/logs/replay_attack_session.json](/logs/replay_attack_session.json).
- **Mise en œuvre des défenses** :
  - Utilisation de **Rolling Codes / Keeloq / AES-128 CCM** dans les systèmes RF embarqués.
  - Utilisation des en-têtes HTTP `X-Nonce` et `X-Timestamp` signés par HMAC sur les API REST financières et critiques.
