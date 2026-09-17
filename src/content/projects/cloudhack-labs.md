---
title: "CloudHack Labs"
summary: "Plateforme de formation cybersécurité gamifiée, façon CTF, avec 6 parcours, 24 modules et plus de 72 challenges."
stack: ["Next.js", "Node.js", "Dockerode", "xterm.js", "Supabase", "Traefik", "Docker Compose"]
status: "actif"
nature: "projet personnel"
environment: "Plateforme personnelle auto-hébergée sur VPS"
order: 2
---

CloudHack Labs est une plateforme d'entraînement à la cybersécurité de type CTF (Capture The Flag), pensée pour progresser à travers des scénarios pratiques exécutés en conteneurs isolés.

![Architecture CloudHack Labs : navigateur, Traefik/Nginx, Next.js/Node.js, Dockerode, conteneurs CTF isolés](/images/diagrams/cloudhack-architecture.webp)

*Architecture de la plateforme, du navigateur jusqu'aux conteneurs de challenge isolés.*

## Architecture & Isolation Conteneurs

Le front-end est développé en **Next.js**, le backend en **Node.js**. Chaque challenge CTF s'exécute dans un conteneur temporaire totalement isolé orchestré via **Dockerode**, avec un terminal interactif WebSockets alimenté par **xterm.js**.

- **6 parcours pédagogiques** : Débutant, Web Security, System Hardening, Network Analysis, Forensic, Cryptography.
- **24 modules progressifs** & **72+ challenges** interactifs.
- **Isolation renforcée** : Option `--security-opt no-new-privileges:true`, quotas CPU/RAM via cgroups Linux v2, réseau bridge interne étanche sans accès réseau externe non autorisé.

## Durcissement de l'Infrastructure

L'ensemble de la plateforme repose sur un VPS personnel durci à l'aide d'une **checklist de durcissement personnelle, inspirée de recommandations de l'ANSSI (Guide de Recommandations de Sécurité Linux) et des CIS Benchmarks**. Cette checklist vérifie quelques contrôles clés ; elle ne constitue pas un audit de conformité ANSSI ou CIS.

Voici la sortie du script de vérification exécuté sur le serveur :

```bash
$ python3 labs/vps_hardening/vps_audit_hardening.py --target vps-prod-toulouse-01
==================================================================================
  LINUX VPS HARDENING CHECKLIST (CloudHack Labs)
  Reference: project checklist inspired by ANSSI & CIS recommendations
  Scope: this project's own VPS — not a conformity audit
==================================================================================

CATEGORY               HARDENING CHECK                                  SEVERITY   STATUS
-----------------------------------------------------------------------------------------------
SSH Hardening          Disable Root Login (PermitRootLogin no)          HIGH       PASS
SSH Hardening          Disable Password Auth (PasswordAuthentication no) HIGH      PASS
Firewall & Ports       UFW Minimal Port Exposure (Default DENY In)      CRITICAL   PASS
Bruteforce Defense     Fail2ban Jail Protection on SSH & Nginx Auth     HIGH       PASS
Docker Isolation       Container Security Opts (no-new-privileges:true) CRITICAL   PASS
Docker Resource Limit  CPU & Memory Cgroups Quotas per CTF Sandbox      HIGH       PASS
TLS/SSL Config         Nginx / Traefik TLS 1.3 & HSTS Preload           HIGH       PASS
-----------------------------------------------------------------------------------------------

✔ 7/7 checks passed in the project hardening checklist
[INFO] Report exported to public/logs/vps_hardening_audit.json
```

## Ressources & Rapports

- **Rapport de la checklist au format JSON** : [public/logs/vps_hardening_audit.json](/logs/vps_hardening_audit.json). Il rend compte des contrôles listés ci-dessus, et d'eux seuls.
- **Reverse Proxy** : Nginx + Let's Encrypt TLS 1.3 avec redirection stricte HTTPS et en-têtes HTTP de sécurité (`Content-Security-Policy`, `X-Frame-Options: DENY`, `HSTS Preload`).

