---
title: "Lab Attaque par Rejeu & Contre-mesures Anti-Replay"
summary: "Simulation Python d'une attaque par rejeu et illustration de mécanismes de fraîcheur et d'authentification."
stack: ["Python", "Cryptography", "HMAC-SHA256", "Nonce"]
status: "actif"
nature: "simulation pédagogique"
environment: "Simulation logicielle Python : aucun matériel radio, véhicule ou ECU physique"
order: 5
---

Ce laboratoire est une simulation logicielle pédagogique. Il modélise un émetteur, un attaquant et un récepteur afin d'illustrer la différence entre un message statique rejouable et un message protégé par un authenticator et une information de fraîcheur.

Aucun signal radio n'est émis ou capturé, et aucun équipement embarqué n'est sollicité : les trois rôles sont des objets Python échangeant des messages en mémoire.

![Comparaison entre un message statique rejouable et un message protégé par compteur, horodatage et authenticator](/images/diagrams/replay-fraicheur.webp)

*Les deux scénarios modélisés par la simulation : à gauche le message statique, à droite le message protégé.*

## Concept Illustré

Une **attaque par rejeu** consiste, pour un attaquant, à capter une transmission valide puis à la réémettre à l'identique pour obtenir le même effet, sans connaître les secrets cryptographiques du système.

La simulation se déroule en deux phases :

1. **Phase 1 : message statique, sans vérification de fraîcheur**
   - Le modèle d'émetteur envoie un message valide au modèle de récepteur.
   - L'attaquant conserve une copie exacte du message, puis la rejoue.
   - Le récepteur simulé l'accepte, car rien dans le message ne permet de distinguer une émission légitime d'une copie.

2. **Phase 2 : message protégé (compteur monotone + horodatage + HMAC-SHA256)**
   - Le message transporte un compteur à usage unique, un horodatage et une signature.
   - L'attaquant rejoue exactement la même trame.
   - Le récepteur simulé la rejette : le compteur a déjà été consommé.

## Exemple de sortie générée par la simulation

```bash
$ python3 labs/replay_attack/replay_lab.py
=====================================================================================
  REPLAY ATTACK & ANTI-REPLAY DEFENSE - PEDAGOGICAL SIMULATION
  Environment: pure Python model (sender / attacker / receiver objects)
  Radio hardware: NO | Real ECU: NO | Physical vehicle: NO
=====================================================================================

[PHASE 1] STATIC MESSAGE MODEL (no freshness check)
  - Legitimate message sent: ID=SIM_SENDER_0892 Code=0x9F4A8B12C3D4E5F6
  [SIMULATED RECEIVER]: ACCEPTED (valid code)

  - Attacker replays the captured message...
  - Replayed message sent  : ID=SIM_SENDER_0892 Code=0x9F4A8B12C3D4E5F6
  [SIMULATED RECEIVER]: ACCEPTED -> replay succeeds in this model
  [NOTE] The static message carries nothing that proves freshness.

[PHASE 2] PROTECTED MESSAGE MODEL (monotonic counter + HMAC-SHA256)
  - Legitimate message sent (counter 1)...
  [SIMULATED RECEIVER]: ACCEPTED (authentic and fresh)

  - Attacker replays the exact same message...
  [SIMULATED RECEIVER]: Replay rejected in the simulated scenario
                        (counter already consumed)

=====================================================================================
  SIMULATION COMPLETE - session log: public/logs/replay_attack_session.json
=====================================================================================
```

## Ce que la simulation permet de travailler

- **Le rôle de la fraîcheur** : comprendre pourquoi un authenticator seul ne suffit pas, et pourquoi une information de fraîcheur (compteur, horodatage, nonce) est nécessaire pour distinguer une émission d'une copie.
- **Le lien avec les mécanismes embarqués** : c'est le même raisonnement qui sous-tend les rolling codes des systèmes RF et la combinaison authenticator + Freshness Value d'AUTOSAR SecOC sur réseau embarqué.
- **La transposition côté services web** : en-têtes de type nonce et horodatage signés sur des API critiques.
- **Journal de session JSON de démonstration** : [public/logs/replay_attack_session.json](/logs/replay_attack_session.json).

> Les identifiants, codes et résultats présentés sont des données de démonstration produites par le modèle Python. Le rejet du rejeu observé en phase 2 vaut pour ce scénario simulé et ne constitue pas une mesure d'efficacité sur un système réel.
