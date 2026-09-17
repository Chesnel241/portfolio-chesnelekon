---
title: "Simulation pédagogique de fuzzing CAN : méthodologie et réflexion sur la sécurisation d'un ECU"
excerpt: "Construire une campagne de fuzzing CAN/UDS en environnement virtuel SocketCAN/ICSim, lire les comportements observés et raisonner sur les contre-mesures embarquées."
date: 2026-09-02
tags: ["automotive", "can-bus", "fuzzing", "secoc", "iso-21434", "cybersecurity"]
draft: false
---

Cet article présente une démarche expérimentale réalisée en environnement virtuel SocketCAN/ICSim. Les résultats illustrent des comportements simulés et non des vulnérabilités découvertes sur un véhicule ou ECU réel.

Dans la sécurité automobile sous la norme **ISO/SAE 21434**, la TARA permet d'identifier les scénarios de menace au niveau du concept. Le test de robustesse, lui, cherche à observer ce que fait réellement une implémentation lorsqu'elle reçoit des stimuli hors-spécification. Comprendre comment on construit une telle campagne (et comment on interprète ce qu'elle produit) est utile même lorsqu'on n'est pas soi-même l'ingénieur de validation : c'est ce qui permet de discuter utilement d'une stratégie de vérification avec les équipes qui la mènent.

L'article détaille donc la méthode de construction d'une campagne de **fuzzing sur bus CAN / CAN-FD**, puis le raisonnement de sécurisation associé.

![Schéma - Simulation de fuzzing CAN en environnement virtuel et raisonnement de sécurisation](/images/fuzzing-ecu-handdrawn.svg)

---

## 1. Mon Raisonnement : Pourquoi Fuzzer un Calculateur (ECU) ?

Le CAN classique comporte des mécanismes de détection d'erreurs de transmission, notamment un CRC, mais ne fournit nativement ni authentification cryptographique de l'émetteur ni confidentialité, et son CRC n'est pas conçu pour empêcher une modification malveillante. Une trame correctement formée, injectée sur le bus, est donc traitée par les calculateurs qui écoutent l'ID correspondant, quelle qu'en soit l'origine.

Lorsque l'on teste un ECU (Gateway, Boîtier Télématique ou BCM), le fuzzing poursuit deux objectifs complémentaires :
1. **Évaluer la robustesse logicielle (Robustness Testing)** : Vérifier que des trames malformées ou envoyées à haute fréquence ne provoquent pas de plantage du microcontrôleur, de déni de service (DoS) ou d'état *Bus-Off*.
2. **Identifier des failles de sécurité applicative (Vulnerability Discovery)** : Repérer des faiblesses d'implémentation dans la pile diagnostique **UDS (ISO 14229-1)**, notamment sur le service `0x27 SecurityAccess`, un mécanisme de contrôle d'accès challenge-response.

---

## 2. Le Setup : un Environnement Entièrement Virtuel

L'environnement utilisé ici ne comporte ni véhicule, ni calculateur physique, ni adaptateur CAN matériel. Tout se passe dans le noyau Linux et en espace utilisateur :

- **Interface réseau** : interface **SocketCAN virtuelle** (`vcan0`) du noyau Linux. Sur un banc réel, la même chaîne d'outils s'appliquerait à une interface `can0` reliée à un adaptateur matériel, mais ce n'est pas le cas ici.
- **Simulateur d'environnement** : **ICSim** (Instrument Cluster Simulator), qui génère un trafic CAN plausible et affiche un combiné d'instruments simulé.
- **Fuzzer sur mesure** : script Python multithreadé s'appuyant sur `python-can` pour produire les mutations et observer le trafic.

C'est une limite importante à garder en tête pour la suite : un simulateur reproduit un protocole, pas le comportement d'un microcontrôleur embarqué sous contrainte. Il permet de travailler la méthode, pas de conclure sur la robustesse d'une implémentation réelle.

---

## 3. La Méthodologie de Test Étape par Étape

La démarche de fuzzing s'articule en 4 phases progressives :

```
[Phase 1: Cartographie Passive] -> [Phase 2: Fuzzing Mutationnel] -> [Phase 3: Arbitration Flood] -> [Phase 4: UDS Injection]
```

### Étape 1 : Cartographie et Sniffing Passif
Avant d'injecter la moindre trame, on observe le trafic nominal du bus pendant plusieurs minutes (`candump vcan0`) pour répertorier :
- Les **ID d'arbitrage actifs** (ex: `0x1A4` pour la vitesse, `0x27D` pour la télématique).
- Le cycle d'émission périodique (ex: trames transmises toutes les 10 ms ou 100 ms).
- La structure des payloads DLC (Data Length Code de 8 octets en CAN 2.0B ou 64 octets en CAN-FD).

### Étape 2 : Fuzzing Mutationnel de Payload
À partir des trames valides capturées, le moteur de mutation altère aléatoirement les octets de données selon plusieurs opérateurs :
- **Bit-Flip** : Inversion sélective de bits pour tester la tolérance des décodeurs applicatifs.
- **Boundary Values** : Injection de valeurs extrêmes (`0x00`, `0xFF`, `0x7FFF`) sur les champs de capteurs.
- **DLC Mismatch** : Modification du DLC annoncé par rapport au nombre d'octets réellement transmis.

### Étape 3 : Arbitration Flood (Test de Saturation DoS)
Le bus CAN utilise un mécanisme d'arbitrage bit à bit basé sur la priorité des identifiants (l'ID `0x000` étant le plus prioritaire).
En injectant une rafale de trames avec des ID très prioritaires (`0x000` à `0x07F`) à haute fréquence (jusqu'à 1 000 trames/sec), on observe si le récepteur parvient à maintenir son traitement périodique. Sur un banc réel, c'est là que l'on chercherait un passage en état *Bus-Off* ou une dégradation du temps de cycle.

### Étape 4 : Fuzzing Diagnostique UDS (ISO 14229-1)
Le protocole UDS permet d'interagir avec la mémoire et la configuration des calculateurs. Les services ciblés sont :
- **Service `0x11` (ECU Reset)** : Envoi de demandes de réinitialisation sous différentes sessions.
- **Service `0x27` (SecurityAccess)** : Fuzzing des requêtes de graine (`Seed`) et d'envoi de clé (`Key`) pour détecter des implémentations défaillantes (ex: graines prévisibles, absence de limitation de tentatives).

---

## 4. Lire les Résultats, et Savoir ce qu'ils ne Disent Pas

Lors de la session documentée dans le [Lab CAN Bus Fuzzing](/projets/can-bus-fuzzing-lab), 34 anomalies ont été remontées par l'outil dans l'environnement simulé :

```bash
[16:48:16] [ANOMALY] ID: 0x27D | High frequency fuzzed frame detected (980 frames/sec)
[16:48:16] [ANOMALY] ID: 0x1A4 | Simulated response delay injected (4200 ms)
[16:48:14] [UDS-SIM] ID: 0x7E0 | SecurityAccess response flagged for investigation
```

C'est ici que le raisonnement compte plus que la sortie du terminal :

1. **La latence (4,2 s)** est introduite artificiellement par le scénario simulé. Elle illustre la manière dont un outil pourrait détecter un comportement anormal, rien de plus. Sur un banc réel, une latence est un **symptôme**, pas une cause : elle peut venir d'une file de réception saturée, d'un ordonnancement dégradé, d'un traitement d'interruption trop long. En déduire un débordement de mémoire tampon serait une erreur de méthode : établir une cause demande d'instrumenter la cible, de reproduire le cas et d'examiner le code ou la trace d'exécution.
2. **Les réponses `0x27 SecurityAccess` signalées** sont, de la même façon, des scénarios à investiguer et non des vulnérabilités établies. Les points qu'un ingénieur examinerait ensuite sont connus : la graine est-elle réellement imprévisible ? le nombre de tentatives est-il borné ? une temporisation est-elle appliquée après échec ? le comportement est-il identique après un reset ?

Cette distinction entre « l'outil a levé un signal » et « une vulnérabilité est démontrée » est au cœur de l'activité de vérification : c'est elle qui sépare un résultat exploitable d'un faux positif coûteux.

---

## 5. Raisonner sur les Contre-mesures

Les mécanismes ci-dessous sont ceux qu'on relie classiquement à ce type de scénario de menace. Le choix effectif, son dimensionnement et son paramétrage relèvent de l'architecture du système et des équipes qui la conçoivent ; l'intérêt, côté analyse de risque, est de savoir quelle mesure adresse quel scénario, et pourquoi.

### A. AUTOSAR SecOC (Secure Onboard Communication)
SecOC protège l'authenticité et la fraîcheur des messages échangés sur le réseau embarqué :
- **Authenticator** : ajout d'un authenticator, par exemple un MAC ; certaines configurations SecOC utilisent notamment AES-CMAC. AUTOSAR définit l'authenticator à partir notamment du Data Identifier, des données de l'I-PDU et de la Freshness Value ; l'authenticator et la freshness information peuvent aussi être tronqués selon la configuration.
- **Freshness Value** : une information de fraîcheur entre dans le calcul de l'authenticator, ce qui permet au récepteur de rejeter un message rejoué. La façon dont cette valeur est gérée et transmise dépend du profil SecOC retenu : elle n'est pas nécessairement transmise en totalité, ni nécessairement omise.
- **Portée réelle de la mesure** : la vérification est faite par la couche SecOC côté récepteur, pas par le contrôleur CAN matériel. SecOC protège les messages qu'on a choisi de protéger : le périmètre des I-PDU concernés est lui-même une décision d'architecture issue de l'analyse de risque.

### B. Durcissement du Diagnostic & Stockage des Secrets
- **Limitation des tentatives** : mécanismes de limitation de tentatives et temporisation définis selon les exigences du système. Un exemple fréquemment rencontré est un verrouillage temporisé après un petit nombre d'échecs consécutifs sur `0x27 SecurityAccess` ; les valeurs exactes relèvent de la spécification du produit.
- **Hardware Security Module (HSM / SHE)** : génération des graines par un générateur d'aléa matériel et stockage des clés dans une zone protégée, inaccessible au processeur applicatif.

### C. Filtrage Matériel sur le Contrôleur CAN (Acceptance Filtering)
- Configuration stricte des registres de masque et de filtrage du contrôleur CAN matériel (*CAN acceptance filters*) afin que le microcontrôleur n'interrompe le processeur que pour les identifiants d'arbitrage strictement nécessaires à son fonctionnement.

---

*Le fuzzing est l'un des moyens de confronter une analyse de risque à une implémentation. En environnement simulé, il ne prouve rien sur un produit réel, mais il apprend à construire une campagne, à formuler ce qu'on cherche et à interpréter un signal sans sur-conclure. C'est exactement ce dont on a besoin pour discuter d'une stratégie de vérification avec les équipes qui la mettent en œuvre.*
