# Portfolio — Chesnel Ekogha

Site statique (Astro) : présentation, projets, blog technique. Pensé pour être
hébergé sur ton propre VPS, à côté de tes autres projets.

## Structure

```
src/
├── content.config.ts        # schémas des collections "projects" et "blog"
├── content/
│   ├── projects/*.md        # une fiche par projet (dupliquer un fichier existant)
│   └── blog/*.md            # un article par fichier (draft: true pour masquer)
├── layouts/Base.astro       # head, polices, header/footer
├── components/              # Header, Footer, SectionHead, ProjectCard, ArticleRow
└── pages/
    ├── index.astro           # accueil
    ├── projets/index.astro   # liste des projets
    ├── projets/[slug].astro  # fiche projet
    ├── blog/index.astro      # liste des articles
    └── blog/[slug].astro     # article
```

## Ajouter un projet (avec capture d'écran)

1. Duplique un fichier existant dans `src/content/projects/`, par exemple :
   ```bash
   cp src/content/projects/cloudhack-labs.md src/content/projects/mon-nouveau-projet.md
   ```
2. Dépose ta capture d'écran **dans ce même dossier**, à côté du `.md`
   (ex. `src/content/projects/mon-nouveau-projet.png`).
3. Dans le frontmatter du `.md`, ajoute `thumbnail: ./mon-nouveau-projet.png`
   — Astro l'optimise et la sert automatiquement (formats modernes,
   dimensions adaptées). Complète aussi `title`, `summary`, `stack`,
   `status`, `githubUrl`, `date`.
4. `git add . && git commit -m "Ajoute mon-nouveau-projet" && git push`
5. Le workflow GitHub Actions build et redéploie automatiquement sur ton
   VPS — rien d'autre à faire.

Même logique pour un article : duplique un fichier dans
`src/content/blog/`, adapte le frontmatter, `draft: false` pour publier.

Les badges technos sur la page d'accueil se génèrent automatiquement à
partir du champ `stack` de tous tes projets (`src/lib/badges.ts`) — pas
besoin d'y toucher, ajoute juste une techno dans le mapping si tu veux
son logo au lieu d'un badge texte simple.

## Stats GitHub live

Retirées volontairement. Ce portfolio est indépendant de ton compte
GitHub : chaque projet affiché vient uniquement de
`src/content/projects/` — un projet n'a même pas besoin d'exister sur
GitHub pour apparaître ici (`githubUrl` est optionnel). Une carte de
stats GitHub live aurait remonté l'activité de *tous* tes dépôts
publics, y compris ceux sans rapport avec ton profil cybersécurité —
l'inverse du contrôle que tu veux garder sur ce qui s'affiche.

## Dates

Aucune date de publication n'est affichée sur les fiches projets (ni
sur la liste, ni sur le détail) — seul `order` détermine l'ordre
d'affichage. Les dates n'apparaissent que sur les articles de blog
(normal pour ce type de contenu).

## À personnaliser avant de mettre en ligne

- [x] Coordonnées : email réel (`ekoghachesneloff@gmail.com`) et CV
      (`public/cv-chesnel-ekogha.pdf`, téléchargeable depuis le hero et
      la section À propos) déjà branchés
- [ ] `public/cv-chesnel-ekogha.pdf` : remplace ce fichier à chaque
      nouvelle version de ton CV (même nom de fichier, pas de code à
      changer)
- [ ] Chaque fiche dans `src/content/projects/` : ajouter `githubUrl` /
      `demoUrl` quand ils existent, compléter les descriptions marquées
      "à compléter" — en particulier `can-bus-fuzzing-lab.md` et
      `tara-keyless-entry.md`, dont j'ai mis un statut par défaut
      (`en cours` / `archivé`) à ajuster selon la réalité
- [ ] `public/favicon.svg` : remplacer par ton propre favicon
- [ ] Le brouillon `durcir-un-vps-pour-heberger-ses-projets.md` : à terminer,
      puis passer `draft: false` pour le publier

## Commandes

| Commande          | Action                                      |
| ----------------- | -------------------------------------------- |
| `npm install`     | Installe les dépendances                     |
| `npm run dev`     | Serveur local sur `localhost:4321`           |
| `npm run build`   | Build statique dans `./dist/`                |
| `npm run preview` | Prévisualise le build en local               |

## Déploiement sur ton VPS Netcup

Le site est 100% statique après build : pas besoin d'un process Node qui
tourne en permanence, juste servir le dossier `dist/` avec Nginx — comme le
reste de ton infra (CloudHack Labs, etc.), en le mettant sur un `server{}`
séparé.

### 1. Sur le VPS

```bash
sudo mkdir -p /var/www/portfolio
sudo chown $USER:$USER /var/www/portfolio
```

Copie `deploy/nginx-portfolio.conf` vers `/etc/nginx/sites-available/portfolio`
en remplaçant `ton-domaine.fr`, puis :

```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d ton-domaine.fr -d www.ton-domaine.fr
```

### 2. Déploiement manuel (première fois, ou en dépannage)

```bash
npm run build
rsync -avzr --delete dist/ user@ton-vps:/var/www/portfolio/dist/
```

### 3. Déploiement automatique (GitHub Actions)

Le workflow `.github/workflows/deploy.yml` build le site et le pousse sur le
VPS à chaque push sur `main`. Ajoute ces secrets dans les paramètres du repo
GitHub (Settings → Secrets and variables → Actions) :

| Secret            | Valeur                                      |
| ----------------- | -------------------------------------------- |
| `VPS_HOST`        | IP ou domaine du VPS                        |
| `VPS_USER`        | utilisateur SSH de déploiement (pas `root`) |
| `VPS_SSH_KEY`     | clé privée SSH dédiée au déploiement        |
| `VPS_DEPLOY_PATH` | `/var/www/portfolio/dist/`                  |

### 4. Durcissement & Sécurisation du VPS (Hardening)

Pour respecter les meilleures pratiques de cybersécurité :

1. **Privilèges Sudo restreints pour la CI/CD** :
   Pour autoriser l'utilisateur de déploiement à recharger Nginx sans mot de passe (et sans accès `root` complet) :
   ```bash
   sudo visudo -f /etc/sudoers.d/portfolio-deploy
   # Ajouter la ligne suivante (remplacer `deploy-user` par l'utilisateur du secret VPS_USER) :
   deploy-user ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx, /usr/sbin/nginx -t
   ```

2. **Pare-feu (UFW)** :
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

3. **Protection contre les attaques par force brute (Fail2ban)** :
   ```bash
   sudo apt install fail2ban -y
   sudo systemctl enable fail2ban --now
   ```

## Commandes de Test & Validation

| Commande          | Action                                      |
| ----------------- | -------------------------------------------- |
| `npm run check`   | Diagnostic et contrôle de type Astro/TS      |
| `npm run dev`     | Serveur local sur `localhost:4321`           |
| `npm run build`   | Build statique dans `./dist/`                |
| `npm run preview` | Prévisualise le build en local               |

## Note sur la version de Node

Ce projet demande Node ≥ 22 (`engines` dans `package.json`), fixé par le
générateur Astro. Le workflow GitHub Actions utilise automatiquement Node 22 (`actions/setup-node@v4`).

