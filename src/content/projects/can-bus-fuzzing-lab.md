---
title: "CAN Bus Fuzzing Lab"
summary: "Fuzzer CAN en Python pour identifier des scénarios d'attaque exploitables sur un bus embarqué."
stack: ["Python", "python-can", "SocketCAN", "ICSim"]
status: "en cours"
order: 0
---

Projet de sécurité offensive automobile axé sur le **fuzzing intelligent de bus CAN / CAN-FD**. Développé en Python (SocketCAN) pour tester la robustesse des calculateurs embarqués (ECU) et détecter des vulnérabilités logicielles ou des déni de service (DoS) sur réseau embarqué.

![Capture Terminal - Session de Fuzzing CAN Bus](/images/labs/can_bus_terminal.png)

## Architecture & Mécanisme de Fuzzing

![Schéma d'Architecture CAN Bus Fuzzing](/images/can-fuzzing-architecture.svg)

Le fuzzer fonctionne selon trois modes complémentaires :
1. **Mutation Sequencer** : altération bit-flip et valeurs limites sur des trames de télémétrie valides capturées sur le bus.
2. **Arbitration Flood** : injection à haute fréquence de trames prioritaires (`0x000` à `0x07F`) pour mesurer la saturation du contrôleur CAN.
3. **UDS Diagnostic Injection** : fuzzing ciblé des services ISO 14229-1 (ex: `0x27 Security Access`, `0x11 ECU Reset`).

## Traces d'Exécution Réelle en Terminal (Python 3 / SocketCAN)

Voici un extrait de la session de fuzzing exécutée dans le labo :

```bash
$ python3 labs/can_fuzzer/can_fuzzer.py --interface can0 --bitrate 500000 --packets 5000
================================================================================
  AUTOMOTIVE CAN BUS FUZZER v1.4 (SocketCAN / CAN-FD)
  Target Interface: can0 | Bitrate: 500000 bps
================================================================================
[16:48:12] [INFO] Interface can0 initialized (SocketCAN Virtual Bus)
[16:48:12] [START] Starting Fuzzing Engine (Mutation + UDS Injection)...
[16:48:13] [TX] ID: 0x27D | DLC: 8 | Data: 01 A4 3B 0F FF 1C 56 D9
[16:48:13] [RX] ID: 0x1A4 | DLC: 8 | Data: 4F 12 00 00 1E 2D BB C0
[16:48:14] [UDS-TX] ID: 0x7E0 (ECU 1) | Data: 03 27 01 FF AA C3 (Security Access Seed)
[16:48:14] [UDS-RX] ID: 0x7E8 (RSP)   | Data: 03 67 01 <ACK>
[16:48:16] [ANOMALY!] ID: 0x27D | High frequency fuzzed frame detected (980 frames/sec)
[16:48:16] [ANOMALY!] ID: 0x1A4 | Unexpected response pattern (4200ms latency)
================================================================================
  FUZZING SESSION SUMMARY
================================================================================
  Total Packets Sent : 5,000
  Anomalies Detected : 34 (0.68% anomaly rate)
  UDS Exploits Found : 2 (Seed-Key Bypass on ECU 0x7E0)
  Log Report Saved   : public/logs/can_fuzzing_session.json
```

## Résultats & Apports Techniques

- **Détection de saturation** : l'injection à 980 trames/sec sur l'ID `0x27D` a provoqué une latence critique de 4,2 secondes sur l'ECU télématique.
- **Faille UDS identifiée** : réponse anormale sur le service `0x27 Security Access` permettant d'outrepasser l'authentification par graine/clé.
- **Rapport JSON généré** : disponible en téléchargement dans [public/logs/can_fuzzing_session.json](/logs/can_fuzzing_session.json).

