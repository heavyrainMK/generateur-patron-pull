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
7. L’historique des patrons générés et les profils utilisateurs sont sauvegardés dans MongoDB.

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

### 1. Backend Node.js/Express

```bash
cd node-backend
npm install
npm start
```

- Par défaut, le serveur écoute sur [http://localhost:3000](http://localhost:3000).

💡 **Important** : si tu fais appel à l’API Python Flask depuis le frontend, pense à **modifier l’URL dans la requête `fetch` dans le fichier `script.js`** :

Remplace :
```js
const reponse = await fetch('https://patron-flask-api.onrender.com/api/calculer-patron', {
```
par :
```js
const reponse = await fetch('http://127.0.0.1:10000/api/calculer-patron', {
```
ou, si tu testes depuis un autre appareil sur le réseau local :
```js
const reponse = await fetch('http://192.168.1.46:10000/api/calculer-patron', {
```

### 2. API Flask (Python)

Assure-toi d’avoir Python 3.9+ et pip.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

- Par défaut, l’API Flask écoute sur le port 5000 ou selon config Render.

### 3. Frontend

- Les fichiers statiques sont servis automatiquement par Node.js (voir `/frontend`).

---

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
