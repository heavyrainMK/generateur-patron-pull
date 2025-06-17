# 🧶 Générateur de Patrons de Tricot - Pull sur Mesure

Ce projet permet de générer automatiquement un patron de tricot personnalisé pour un pull, à partir des mesures fournies par l'utilisateur. Conçu pour être accessible via une interface web simple et intuitive, ce générateur guide les utilisateurs pas à pas dans la création de leur pull.

## ✨ Fonctionnalités

- Interface web conviviale pour saisir les mesures du pull (en cm).
- Génération automatique d'instructions de tricot personnalisées.
- Téléchargement du patron au format PDF.
- Traitement des données côté serveur via Python pour des calculs précis.
- Structure permettant une extension future (ex : base de données).

## 💡 Comment ça fonctionne

1. L'utilisateur ouvre la page `index.html`.
2. Il renseigne ses mesures (tour de poitrine, longueur, manches, etc.).
3. Un script en JavaScript envoie ces données au backend Python.
4. Python calcule les instructions détaillées pour tricoter un pull sur mesure.
5. Le texte généré s'affiche dans la page et peut être téléchargé en PDF.

## 🛠 Technologies utilisées

- **HTML / CSS** : Interface utilisateur et mise en page.
- **JavaScript** : Liaison entre le frontend et le backend.
- **Python** : Moteur de calculs pour générer les instructions
- *(Optionnel)* **Base de données** : Sauvegarde des patrons générés.

## 🚧 Fonctionnalités futures

- Intégration complète en ligne via un hébergement web.
- *(Optionnel)* Ajout d'une base de données pour sauvegarder et consulter les patrons.
- *(Optionnel)*  Personnalisation avancée: d’autres types de cols (col en V, col bateau, ras du cou)

## 👩‍💻 Équipe de développement

Projet réalisé par :
- Maxime
- Liubov
- Mathilde

Dans le cadre d’un projet étudiant L2.

## 📄 Licence

Ce projet a été réalisé dans le cadre du cours *Réalisation de programme* à des fins éducatives.  
Il est destiné à l'apprentissage et au développement de compétences en programmation.

