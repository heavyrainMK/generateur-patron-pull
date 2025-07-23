/*
# *******************************************************
# Nom ......... : server.js
# Rôle ........ : Serveur principal - gestion des utilisateurs et des routes
# Auteurs ..... : M, L, M
# Version ..... : V2.0 du 20/07/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Gère les routes de login, enregistrement et dashboard utilisateur
# Technologies  : JavaScript
# Dépendances . : login.html, register.html, user_dashboard.html
# Usage ....... : node server.js puis ouvrir http://localhost:3000
# *******************************************************
*/

// Importation des modules nécessaires
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());
app.use(express.static(path.join(__dirname, '../frontend'))); // Fichiers HTML/CSS

// Connexion à la base de données MongoDB
mongoose.connect('mongodb+srv://pull:b7SOBeu4HqfABfct@cluster.puhrkui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster')
    .then(() => console.log('Connecté à MongoDB'))
    .catch(err => console.error('Erreur MongoDB :', err));


// Schéma utilisateur pour MongoDB
const utilisateurSchema = new mongoose.Schema({
    prenom: String,
    nom: String,
    email: String,       
    motdepasse: String,  
    experience: String
});

// Modèle utilisateur basé sur le schéma
const Utilisateur = mongoose.model('Utilisateur', utilisateurSchema);


// Routes API
// Route de connexion utilisateur (login.html)
app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        console.log('Tentative de connexion pour:', email);

        // Vérification des champs requis
        if (!email || !password) {
            return res.status(400).json({ message: 'Email et mot de passe requis' });
        }

        // Recherche de l'utilisateur par email
        const user = await Utilisateur.findOne({ email: email });
        
        console.log('Utilisateur trouvé:', user ? 'Oui' : 'Non');

        // Vérification de l'existence de l'utilisateur
        if (!user) {
            return res.status(401).json({ message: 'Email ou mot de passe incorrect' });
        }

        // Vérification du mot de passe
        if (user.motdepasse !== password) {
            console.log('Mot de passe incorrect');
            return res.status(401).json({ message: 'Email ou mot de passe incorrect' });
        }

        // Connexion réussie
        console.log('Connexion réussie pour:', email);
        res.status(200).json({ 
            message: 'Connexion réussie',
            user: {
                prenom: user.prenom,
                nom: user.nom,
                email: user.email
            }
        });
    } catch (err) {
        // Gestion des erreurs serveur
        console.error('Erreur serveur lors de la connexion:', err);
        res.status(500).json({ message: 'Erreur serveur : ' + err.message });
    }
});

// Route d'inscription utilisateur (register.html)
app.post('/api/register', async (req, res) => {
    try {
        const { prenom, nom, email, password, experience } = req.body;

        // Vérification des champs requis
        if (!prenom || !nom || !email || !password || !experience) {
            return res.status(400).json({ message: 'Tous les champs obligatoires doivent être remplis.' });
        }

        // Vérifier si l'utilisateur existe déjà
        const existingUser = await Utilisateur.findOne({ email: email });
        
        if (existingUser) {
            return res.status(400).json({ message: 'Cet email est déjà utilisé.' });
        }

        // Créer nouvel utilisateur
        const nouvelUtilisateur = new Utilisateur({
            prenom,
            nom,
            email: email,        
            motdepasse: password,
            experience,
        });

        // Sauvegarde dans la base de données
        await nouvelUtilisateur.save();
        console.log('Nouvel utilisateur enregistré:', email);
        // Redirect with a success query parameter
        res.status(201).json({ message: 'Utilisateur enregistré avec succès.' });
    } catch (error) {
        // Gestion des erreurs serveur
        console.error('Erreur lors de l\'enregistrement :', error);
        res.status(500).json({ message: 'Erreur serveur lors de l\'enregistrement.' });
    }
});

// Route pour voir tous les utilisateurs
app.get('/api/utilisateurs', async (req, res) => {
    try {
        const utilisateurs = await Utilisateur.find({});
        res.json(utilisateurs);
    } catch (error) {
        console.error('Erreur lors de la récupération:', error);
        res.status(500).json({ message: 'Erreur lors de la récupération des utilisateurs' });
    }
});

// Route pour récupérer les informations de l'utilisateur connecté
app.get('/api/user/:email', async (req, res) => {
    try {
        const email = req.params.email;
        console.log('Récupération des infos pour:', email);

        const user = await Utilisateur.findOne({ email: email });
        
        if (!user) {
            return res.status(404).json({ message: 'Utilisateur non trouvé' });
        }

        console.log('Utilisateur trouvé:', user.prenom, user.nom);
        res.status(200).json({ 
            prenom: user.prenom,
            nom: user.nom,
            email: user.email,
            experience: user.experience
        });
    } catch (err) {
        console.error('Erreur lors de la récupération:', err);
        res.status(500).json({ message: 'Erreur serveur : ' + err.message });
    }
});

// Routes pour servir les pages HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/page_accueille.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/login.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/register.html'));
});

app.get('/user_dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/user_dashboard.html'));
});

// Lancement du serveur
const PORT = 3000;
app.listen(PORT, () => {
    console.log(` Serveur en cours d'exécution sur http://localhost:${PORT}`);
    console.log(` Fichiers servis depuis: ${__dirname}`);
    console.log(` Pages disponibles:`);
    console.log(`   - Accueil: http://localhost:${PORT}/`);
    console.log(`   - Connexion: http://localhost:${PORT}/login.html`);
    console.log(`   - Inscription: http://localhost:${PORT}/register.html`);
    console.log(`   - Page utilisateur: http://localhost:${PORT}/user_dashboard.html`);
    console.log(`   - Utilisateurs: http://localhost:${PORT}/api/utilisateurs`);
});


