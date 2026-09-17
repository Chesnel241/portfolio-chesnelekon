---
title: "CAN Bus Fuzzing Lab"
summary: "Simulation pédagogique d'une campagne de fuzzing CAN/UDS en Python avec SocketCAN et environnement virtuel."
stack: ["Python", "python-can", "SocketCAN", "ICSim"]
status: "en cours"
nature: "simulation pédagogique"
environment: "Environnement virtuel/local — aucun véhicule ou ECU physique"
order: 0
---

Ce laboratoire pédagogique illustre une démarche de fuzzing CAN / UDS dans un environnement entièrement virtuel basé sur Python, SocketCAN et ICSim.

L'objectif n'est pas de présenter une vulnérabilité découverte sur un ECU réel, mais de comprendre comment construire une campagne de test, générer des trames anormales et analyser les comportements qu'un ingénieur rechercherait sur un véritable banc de validation.

![Capture Terminal - Session de Fuzzing CAN Bus simulée](/images/labs/can_bus_terminal.png)

*Capture de démonstration illustrant l'interface du fuzzer. La session a été produite en environnement virtuel ; aucun bus physique ni calculateur réel n'est impliqué.*

## Architecture & Mécanisme de Fuzzing

![Schéma d'Architecture CAN Bus Fuzzing](/images/can-fuzzing-architecture.svg)

Le fuzzer fonctionne selon trois modes complémentaires :
1. **Mutation Sequencer** : altération bit-flip et valeurs limites sur des trames de télémétrie générées par le simulateur.
2. **Arbitration Flood** : injection à haute fréquence de trames prioritaires (`0x000` à `0x07F`) pour observer le comportement du bus virtuel en saturation.
3. **UDS Diagnostic Injection** : fuzzing ciblé de services ISO 14229-1 simulés (ex: `0x27 SecurityAccess`, `0x11 ECU Reset`).

## Exemple de sortie générée par la simulation

L'extrait ci-dessous est une sortie de démonstration produite par le script sur une interface CAN virtuelle (`vcan`) :

```bash
$ python3 labs/can_fuzzer/can_fuzzer.py --interface vcan0 --packets 5000
================================================================================
  AUTOMOTIVE CAN BUS FUZZER — PEDAGOGICAL SIMULATION
  Environment: SocketCAN / vcan
  Real ECU: NO
  Physical vehicle: NO
================================================================================
[16:48:12] [INFO] Interface vcan0 initialized (SocketCAN Virtual Bus)
[16:48:12] [START] Starting Fuzzing Engine (Mutation + UDS Injection)...
[16:48:13] [TX] ID: 0x27D | DLC: 8 | Data: 01 A4 3B 0F FF 1C 56 D9
[16:48:13] [RX] ID: 0x1A4 | DLC: 8 | Data: 4F 12 00 00 1E 2D BB C0
[16:48:14] [UDS-TX] ID: 0x7E0 (sim) | Data: 03 27 01 FF AA C3 (SecurityAccess Seed)
[16:48:14] [UDS-RX] ID: 0x7E8 (sim) | Data: 03 67 01 <ACK>
[16:48:16] [ANOMALY] ID: 0x27D | High frequency fuzzed frame detected (980 frames/sec)
[16:48:16] [ANOMALY] ID: 0x1A4 | Simulated response delay injected (4200 ms)
================================================================================
  SIMULATION SESSION SUMMARY
================================================================================
  Total Packets Sent  : 5,000
  Anomalies Detected  : 34 (0.68% anomaly rate)
  Simulated UDS anomalies : 2
  Scenarios requiring further investigation : SecurityAccess responses
  Log Report Saved    : public/logs/can_fuzzing_session.json
```

## Ce que la simulation permet de travailler

- **Détection de saturation** : le scénario simulé introduit artificiellement une augmentation de latence afin d'illustrer la manière dont un outil pourrait détecter un comportement anormal sur un bus chargé. Sur un banc réel, une telle observation ne serait qu'un point de départ : elle demanderait une instrumentation de l'ECU pour en établir la cause.
- **Lecture d'un échange UDS** : les réponses simulées du service `0x27 SecurityAccess` servent à comprendre la logique challenge-response et les points d'attention qu'un ingénieur examinerait (prévisibilité de la graine, limitation des tentatives, temporisation).
- **Structure d'un rapport de campagne** : un rapport JSON de démonstration est généré — [public/logs/can_fuzzing_session.json](/logs/can_fuzzing_session.json).

> Les valeurs, identifiants et comportements présentés ci-dessus sont des données de démonstration produites par le simulateur. Ils ne correspondent à aucun calculateur, produit ou constructeur réel, et ne constituent pas la description d'une vulnérabilité existante.
