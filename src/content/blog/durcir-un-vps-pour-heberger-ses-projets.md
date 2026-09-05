---
title: "Durcir un VPS pour héberger ses propres projets : Guide Pratique & Audit ANSSI"
excerpt: "Retour d'expérience et configuration pas-à-pas pour sécuriser un serveur Linux (Ubuntu 22.04 LTS) hébergeant des applications web et conteneurs Docker en production."
date: 2026-08-25
tags: ["infra", "hardening", "anssi", "docker", "self-hosting"]
draft: false
---

Héberger soi-même ses projets web (comme la plateforme [CloudHack Labs](/projets/cloudhack-labs)) sur un VPS non aménagé expose immédiatement le serveur à des scans de ports automatisés, des attaques par force brute SSH et des tentatives d'exploitation de vulnérabilités Web.

Voici le guide complet de durcissement (hardening) appliqué sur mon serveur de production, validé par un script d'audit automatisé respectant les recommandations de l'**ANSSI** et du **CIS Benchmark**.

![Capture Terminal - Session d'Audit de Sécurité VPS](/images/labs/vps_hardening_terminal.png)

## 1. Sécurisation de l'Accès SSH (`/etc/ssh/sshd_config`)

L'accès SSH root par mot de passe est la première cible des bots. La première étape consiste à imposer l'authentification par clé publique Ed25519 uniquement et désactiver le login root.

```bash
# /etc/ssh/sshd_config.d/99-hardening.conf
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
```

Redémarrage et vérification : `sudo systemctl restart ssh`

## 2. Pare-feu Réseau Strict (`UFW / nftables`)

Par défaut, tout trafic entrant non explicitement autorisé doit être rejeté (`DEFAULT DENY`). Seuls les ports Web HTTPS (443) et le port SSH personnalisé sont ouverts.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp comment 'SSH Port Securise'
sudo ufw allow 443/tcp comment 'HTTPS Reverse Proxy'
sudo ufw enable
```

## 3. Protection Anti-Bruteforce (`Fail2ban`)

Fail2ban surveille les fichiers de logs (`/var/log/auth.log`, Nginx access log) et bannit temporairement ou définitivement les adresses IP suspectes via des règles iptables/nftables.

```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = 2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
findtime = 600
bantime = 86400

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
```

## 4. Isolation & Securing Docker Sandbox

Lorsqu'on orchestre des conteneurs (par exemple pour exécuter des challenges CTF utilisateurs), l'isolation doit empêcher toute élévation de privilèges vers l'hôte Linux.

Exemple de configuration `docker-compose.yml` durcie :

```yaml
version: '3.8'
services:
  ctf-sandbox:
    image: cloudhack/sandbox:latest
    security_opt:
      - no-new-privileges:true
      - seccomp=default
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 256M
```

## 5. Reverse Proxy Nginx & Configuration TLS 1.3

Nginx intercepte l'ensemble du trafic entrant, gère les certificats SSL/TLS automatisés via Let's Encrypt et injecte les en-têtes HTTP recommandés par l'ANSSI.

```nginx
# /etc/nginx/conf.d/security_headers.conf
ssl_protocols TLSv1.3;
ssl_prefer_server_ciphers off;

add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';" always;
```

## 6. Audit Automatisé & Score de Conformité

Pour vérifier en continu que la configuration du serveur ne dérive pas, un script Python d'audit effectue un contrôle périodique.

Exemple d'audit exécuté en production :

```bash
$ python3 labs/vps_hardening/vps_audit_hardening.py
✔ HARDENING AUDIT COMPLETE: 7/7 Checks Passed (100% Compliance Score)
Rapport d'audit disponible dans : public/logs/vps_hardening_audit.json
```

---

*Ce durcissement permet de maintenir un niveau de sécurité élevé tout en conservant une grande agilité pour le déploiement continu des projets personnels.*

