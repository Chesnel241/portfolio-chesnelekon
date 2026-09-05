---
title: "Fuzzing de Bus CAN Automobile : Méthodologie d'Attaque et Guide de Sécurisation ECU"
excerpt: "Comment mener une campagne de fuzzing outillée sur un calculateur automobile (ECU), analyser les plantages et implémenter les contre-mesures SecOC et UDS."
date: 2026-09-02
tags: ["automotive", "can-bus", "fuzzing", "secoc", "iso-21434", "cybersecurity"]
draft: false
---

Dans la sécurité automobile sous la norme **ISO/SAE 21434**, l'analyse de risque théorique (TARA) permet d'identifier les scénarios de menace sur le papier. Cependant, la réalité physique d'un réseau embarqué CAN (ISO 11898) révèle souvent des comportements inattendus lorsque le bus subit des stimuli hors-spécification.

Cet article détaille ma méthodologie complète d'expérimentation, mon raisonnement technique lors d'une campagne de **fuzzing sur bus CAN / CAN-FD**, ainsi que la stratégie de sécurisation industrielle pour remédier aux failles découvertes.

![Schéma Technique Crayon - Fuzzing ECU & Sécurisation](/images/fuzzing-ecu-handdrawn.png)

---

## 1. Mon Raisonnement : Pourquoi Fuzzer un Calculateur (ECU) ?

Le protocole CAN historique a été conçu pour être robuste électriquement et déterministe, mais **sans aucun mécanisme natif d'authentification, de confidentialité ou de vérification d'intégrité**. Toute trame injectée sur le bus est acceptée par les calculateurs écoutant l'ID correspondant.

Lorsque l'on teste un ECU (Gateway, Boîtier Télématique ou BCM), le fuzzing poursuit deux objectifs complémentaires :
1. **Évaluer la robustesse logicielle (Robustness Testing)** : Vérifier que des trames malformées ou envoyées à haute fréquence ne provoquent pas de plantage du microcontrôleur, de déni de service (DoS) ou d'état *Bus-Off*.
2. **Identifier des failles de sécurité applicative (Vulnerability Discovery)** : Repérer des failles d'implémentation dans la pile diagnostique **UDS (ISO 14229-1)**, notamment sur le service d'authentification `0x27 Security Access`.

---

## 2. Mon Banc de Test & Mon Setup Technique

Pour mener mes expérimentations sans risquer d'endommager du matériel véhicule de série ou d'interférer avec la sécurité physique, j'utilise un banc de test isolé sous Linux :

- **Interface Réseau** : Moteur **SocketCAN** natif du noyau Linux (`vcan0` en virtuel ou interface physique `can0` via adaptateur Peak-CAN / USB-to-CAN).
- **Simulateur d'Environnement** : **ICSim** (Instrument Cluster Simulator) pour visualiser les effets du fuzzing sur le combiné d'instruments.
- **Fuzzer sur mesure** : Script Python multithreadé exploitant la librairie `python-can` pour générer les mutations et monitorer la télémétrie en temps réel.

![Capture Terminal - Session de Fuzzing CAN Bus](/images/labs/can_bus_terminal.png)

---

## 3. Ma Méthodologie d'Attaque Étape par Étape

Ma démarche de fuzzing s'articule en 4 phases progressives et méthodiques :

```
[Phase 1: Cartographie Passive] -> [Phase 2: Fuzzing Mutationnel] -> [Phase 3: Arbitration Flood] -> [Phase 4: UDS Injection]
```

### Étape 1 : Cartographie et Sniffing Passif
Avant d'injecter la moindre trame, j'observe le trafic nominal du bus pendant plusieurs minutes (`candump can0`) pour répertorier :
- Les **ID d'arbitrage actifs** (ex: `0x1A4` pour la vitesse, `0x27D` pour la télématique).
- Le cycle d'émission périodique (ex: trames transmises toutes les 10 ms ou 100 ms).
- La structure des payloads DLC (Data Length Code de 8 octets en CAN 2.0B ou 64 octets en CAN-FD).

### Étape 2 : Fuzzing Mutationnel de Payload
À partir des trames valides capturées, mon moteur de mutation altère aléatoirement les octets de données selon plusieurs opérateurs :
- **Bit-Flip** : Inversion sélective de bits pour tester la tolérance des décodeurs applicatifs.
- **Boundary Values** : Injection de valeurs extrêmes (`0x00`, `0xFF`, `0x7FFF`) sur les champs de capteurs.
- **DLC Mismatch** : Modification du DLC annoncé par rapport au nombre d'octets réellement transmis.

### Étape 3 : Arbitration Flood (Test de Saturation DoS)
Le bus CAN utilise un mécanisme d'arbitrage bit à bit basé sur la priorité des identifiants (l'ID `0x000` étant le plus prioritaire).
En injectant une rafale de trames avec des ID très prioritaires (`0x000` à `0x07F`) à haute fréquence (jusqu'à 1 000 trames/sec), je vérifie si l'ECU cible parvient à maintenir son traitement périodique ou s'il entre en latence critique.

### Étape 4 : Fuzzing Diagnostique UDS (ISO 14229-1)
Le protocole UDS permet d'interagir directement avec la mémoire et la configuration des ECU. Je cible spécifiquement :
- **Service `0x11` (ECU Reset)** : Envoi de demandes de réinitialisation sous différentes sessions.
- **Service `0x27` (Security Access)** : Fuzzing des requêtes de graine (`Seed`) et d'envoi de clé (`Key`) pour détecter des implémentations défaillantes (ex: graines prévisibles, absence de limitation de tentatives).

---

## 4. Analyse des Anomalies Constatées

Lors de la session d'expérimentation documentée dans le [Lab CAN Bus Fuzzing](/projets/can-bus-fuzzing-lab), 34 anomalies ont été automatiquement identifiées par le fuzzer :

```bash
[16:48:16] [ANOMALY!] ID: 0x27D | High frequency fuzzed frame detected (980 frames/sec)
[16:48:16] [ANOMALY!] ID: 0x1A4 | Unexpected response pattern (4200ms latency)
[16:48:14] [UDS-EXPLOIT] ID: 0x7E0 (ECU 1) | Seed-Key Bypass confirmed on Service 0x27
```

1. **Latence critique (4,2 secondes)** : L'injection massive sur l'ID `0x27D` a provoqué un débordement de mémoire tampon (*buffer overflow*) dans le contrôleur de télématique, retardant l'affichage des informations critiques.
2. **Faiblesse d'authentification UDS** : Sur l'ECU `0x7E0`, la graine fournie par le service `0x27 01` s'est révélée constante après certains plantages, permettant de déduire la clé d'accès sans privilèges.

---

## 5. La Démarche de Sécurisation : Comment Corriger et Durcir l'ECU ?

Pour corriger ces vulnérabilités et garantir la conformité aux exigences **UNECE R155**, voici les contre-mesures indispensables à déployer dans l'architecture électronique du véhicule :

### A. Intégration d'AUTOSAR SecOC (Secure Onboard Communication)
La mesure de sécurité fondamentale consiste à signer cryptographiquement les trames CAN sensibles à l'aide du standard **SecOC** :
- **Tag d'Authentification (MAC)** : Ajout d'un code HMAC (CMAC-AES-128) truncaté dans la charge utile de la trame.
- **Compteur de Fraîcheur (Freshness Counter)** : Inclusion d'un compteur incrémentable non transmis en clair pour empêcher les attaques par rejeu et garantir que les trames fuzzées/injectées sans MAC valide soient immédiatement rejetées par le contrôleur CAN.

### B. Durcissement des Services UDS & Stockage en HSM
- **Rate Limiting & Lockout Period** : Définition d'une période de verrouillage obligatoire de 60 secondes après 3 tentatives infructueuses sur le service `0x27 Security Access`.
- **Hardware Security Module (HSM / SHE)** : Génération des graines de sécurité par un véritable générateur de nombres aléatoires matériel (TRNG) et stockage des clés d'accès dans une zone sécurisée de l'ECU inaccessible par le processeur d'application.

### C. Filtrage Matériel sur le Contrôleur CAN (Acceptance Filtering)
- Configuration stricte des registres de masque et de filtrage du contrôleur CAN matériel (*CAN acceptance filters*) afin que le microcontrôleur n'interrompe le processeur que pour les identifiants d'arbitrage strictement nécessaires à son fonctionnement.

---

*Le fuzzing de bus CAN est un outil d'évaluation indispensable pour passer de l'analyse de risque théorique à la validation concrète des défenses embarquées d'un véhicule.*
