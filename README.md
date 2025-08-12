# 🧶 Générateur de Patrons de Tricot – Pull sur Mesure

Ce projet génère automatiquement un patron de tricot personnalisé pour un pull, à partir des mesures fournies par l’utilisateur, avec gestion d’authentification, sauvegarde de profils, et génération intelligente d’instructions.  
Accessible via une interface web moderne, il guide les utilisateurs pas à pas dans la création de leur pull idéal.

---

## ✨ Fonctionnalités principales

- **Inscription / Connexion utilisateur** avec enregistrement en base MongoDB.
- **Interface web** pour saisir toutes les mesures et options du pull.
- **Génération automatique** d’instructions de tricot, 100 % personnalisées.
- **Téléchargement du patron** généré au format PDF.
- **Sauvegarde en base de données** (MongoDB) des profils et historiques utilisateurs.
- **Déploiement facile** en local ou sur le web (API Node.js, API Python déportée).
- **Mode debug** pour consulter la liste des utilisateurs (à désactiver en prod).

---

## 🖼️ Aperçu Architecture

```
[ Frontend HTML/CSS/JS ]
            │
            ▼
[ Backend Node.js/Express ] <───────┐
     (API REST & BFF)               │
            │                       │
            ▼                       │
   [ MongoDB – Sauvegarde           │
      utilisateurs ]                │
            │                       │
            ▼                       │
[ Proxy vers API Flask (Python) – Calcul Patron ]
```

---

## 💡 Comment ça fonctionne ?

1. L’utilisateur ouvre la page d’accueil ou de connexion.
2. Il s’inscrit (profil enregistré sur MongoDB) ou se connecte.
3. Il saisit ses mesures et options de pull via l’interface web.
4. Le **backend Node.js** reçoit la demande, la transmet à l’API Python (Flask) dédiée au calcul du patron.
5. L’API Flask retourne les instructions de tricot détaillées.
6. L’utilisateur obtient son patron personnalisé, avec possibilité de téléchargement PDF.
7. Les profils utilisateurs sont sauvegardés dans MongoDB.

---

## 🛠️ Technologies utilisées

- **Frontend** : HTML5, CSS3, JavaScript ES6
- **Backend** : Node.js + Express (API REST & BFF)
- **Base de données** : MongoDB Atlas (hébergé)
- **API Calcul Patron** : Python (Flask), microservice séparé (peut être hébergé à part)
- **PDF** : Génération côté frontend
- **Libs** : Axios, body-parser, cors, mongoose, etc.

---

## 🚀 Installation & Lancement local

Ce projet utilise un **Makefile** pour simplifier l'installation, le lancement et l'arrêt des serveurs.

### 1️⃣ Installation des dépendances
```bash
make install
```
> Cette commande installe automatiquement :
> - Les dépendances **Node.js** dans `node-backend/`
> - Les dépendances **Python** dans un environnement virtuel `venv/`

### 2️⃣ Lancement en mode développement
```bash
make dev
```
> Lance simultanément :
> - Le serveur **Flask** sur le port `10000`
> - Le serveur **Node.js** sur le port `3000`

### 3️⃣ Arrêter les serveurs
```bash
make stop
```
> Arrête proprement Flask et Node.js et restaure l'état du terminal.

### 4️⃣ Nettoyer l'environnement
```bash
make clean
```
> Supprime l'environnement Python, `node_modules` et les fichiers PID.

Pour plus de commandes disponibles :
```bash
make help
```

💡 **Astuce :** Après `make stop`, si votre terminal semble bloqué ou que les touches ne s'affichent pas correctement, tapez :  
```bash
stty sane
```
## 🔐 Configuration & Sécurité

- Les identifiants MongoDB sont à placer dans une variable d’environnement ou un fichier `.env` (jamais en dur en production !).
- Pour la prod, désactiver la route de debug `/api/utilisateurs`.

---

## 🛣️ Déploiement

- **Local** : Démarrer les deux backends (Node.js et Flask).
- **Cloud** : Possibilité d’héberger le backend Node.js (API + frontend) sur Render, Vercel, Heroku, etc., et l’API Flask sur un service cloud (Render, PythonAnywhere, etc.).
- **MongoDB Atlas** : recommandé pour une BDD partagée et sécurisée.

---

## 🚧 Fonctionnalités futures

- **Personnalisation avancée** : types de cols, motifs, manches, etc.
- **Gestion avancée des historiques utilisateurs** (profils multiples, favoris…).
- **Refonte UI/UX** pour une expérience encore plus fluide.
- **Ajout d’un assistant tricot pas-à-pas** (notifications, étapes animées).

---

## 👩‍💻 Équipe de développement

Projet réalisé par :
- Maxime
- Liubov
- Mathilde

Dans le cadre du cours universitaire "Réalisation de programmes" (L2).

---

## 📄 Licence

Ce projet a été conçu à des fins pédagogiques, pour l’apprentissage du développement fullstack.
