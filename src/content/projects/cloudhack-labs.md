---
title: "CloudHack Labs"
summary: "Plateforme de formation cybersécurité gamifiée, façon CTF, avec 6 parcours, 24 modules et plus de 72 challenges."
stack: ["Next.js", "Node.js", "Dockerode", "xterm.js", "Supabase", "Traefik", "Docker Compose"]
status: "actif"
order: 2
---

CloudHack Labs est une plateforme d'entraînement à la cybersécurité de type CTF (Capture The Flag), pensée pour progresser à travers des scénarios pratiques exécutés en conteneurs isolés.

![Capture Terminal - Script d'Audit & Hardening VPS Linux](/images/labs/vps_hardening_terminal.png)

## Architecture & Isolation Conteneurs

Le front-end est développé en **Next.js**, le backend en **Node.js**. Chaque challenge CTF s'exécute dans un conteneur temporaire totalement isolé orchestré via **Dockerode**, avec un terminal interactif WebSockets alimenté par **xterm.js**.

- **6 parcours pédagogiques** : Débutant, Web Security, System Hardening, Network Analysis, Forensic, Cryptography.
- **24 modules progressifs** & **72+ challenges** interactifs.
- **Isolation renforcée** : Option `--security-opt no-new-privileges:true`, quotas CPU/RAM via cgroups Linux v2, réseau bridge interne étanche sans accès réseau externe non autorisé.

## Durcissement de l'Infrastructure & Audit de Sécurité

L'ensemble de la plateforme repose sur un serveur VPS de production sécurisé selon les recommandations de l'**ANSSI (Guide de Recommandations de Sécurité Linux)** et les standards **CIS Benchmark**.

Voici les traces de l'audit de sécurité automatisé exécuté directement sur l'infra VPS :

```bash
$ python3 labs/vps_hardening/vps_audit_hardening.py --target vps-prod-toulouse-01
==================================================================================
  LINUX VPS HARDENING & DOCKER CTF AUDITOR v1.8 (CloudHack Labs)
  Compliance: ANSSI Recommandations de Sécurité Linux & CIS Benchmark
  Engineer: Chesnel Ekogha | Host: vps-prod-toulouse-01
==================================================================================

CATEGORY               SECURITY CHECK                                   SEVERITY   STATUS
-----------------------------------------------------------------------------------------------
SSH Hardening          Disable Root Login (PermitRootLogin no)          HIGH       PASS
SSH Hardening          Disable Password Auth (PasswordAuthentication no) HIGH      PASS
Firewall & Ports       UFW Minimal Port Exposure (Default DENY In)      CRITICAL   PASS
Bruteforce Defense     Fail2ban Jail Protection on SSH & Nginx Auth     HIGH       PASS
Docker Isolation       Container Security Opts (no-new-privileges:true) CRITICAL   PASS
Docker Resource Limit  CPU & Memory Cgroups Quotas per CTF Sandbox      HIGH       PASS
TLS/SSL Config         Nginx / Traefik TLS 1.3 & HSTS Preload           HIGH       PASS
-----------------------------------------------------------------------------------------------

✔ HARDENING AUDIT COMPLETE: 7/7 Checks Passed (100% Compliance Score)
[INFO] Audit report exported to public/logs/vps_hardening_audit.json
```

## Ressources & Rapports

- **Rapport d'audit complet JSON** : disponible en téléchargement dans [public/logs/vps_hardening_audit.json](/logs/vps_hardening_audit.json).
- **Reverse Proxy** : Nginx + Let's Encrypt TLS 1.3 avec redirection stricte HTTPS et en-têtes HTTP de sécurité (`Content-Security-Policy`, `X-Frame-Options: DENY`, `HSTS Preload`).

