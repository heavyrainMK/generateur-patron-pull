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

require('dotenv').config();              // Chargement des variables d'environnement
const express = require('express');
const mongoose = require('mongoose');    // Connexion MongoDB
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const app = express();

const multer = require('multer');
const { v2: cloudinary } = require('cloudinary'); // API Cloudinary v
const { CloudinaryStorage } = require('multer-storage-cloudinary'); // Storage pour multer/Cloudinary
const bcrypt = require('bcrypt'); // Hachage des mots de passe
const NBhachage = 10; 

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());
app.use(express.static(path.join(__dirname, '../frontend'))); // Fichiers HTML/CSS

// Connexion à la base de données MongoDB
mongoose.connect(process.env.MONGODB_URI)
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

        // Vérification des champs requis
        if (!email || !password) {
            return res.status(400).json({ message: 'Email et mot de passe requis' });
        }

        // Recherche de l'utilisateur par email
        const user = await Utilisateur.findOne({ email: email });

        // Vérification de l'existence de l'utilisateur
        if (!user) {
            return res.status(401).json({ message: 'Email ou mot de passe incorrect' });
        }

        // Vérification avec bcrypt
        const isPasswordValid = await bcrypt.compare(password, user.motdepasse);
        
        // Vérification du mot de passe
        if (!isPasswordValid) {
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
        // Hachage du mot de passe
        const hashedPassword = await bcrypt.hash(password, NBhachage);

        // Créer nouvel utilisateur
        const nouvelUtilisateur = new Utilisateur({
            prenom,
            nom,
            email: email,        
            motdepasse: hashedPassword,
            experience,
        });

        // Sauvegarde dans la base de données
        await nouvelUtilisateur.save();
        console.log('Nouvel utilisateur enregistré:', email);
        // Réponse de succès
        res.status(201).json({ message: 'Utilisateur enregistré avec succès.' });
    } catch (error) {
        // Gestion des erreurs serveur
        console.error('Erreur lors de l\'enregistrement :', error);
        res.status(500).json({ message: 'Erreur serveur lors de l\'enregistrement.' });
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
});

// Configuration Cloudinary
cloudinary.config({
    cloud_name: process.env.CLOUDINARY_CLOUD_NAME || 'cloud_name',
    api_key: process.env.CLOUDINARY_API_KEY || 'api_key',
    api_secret: process.env.CLOUDINARY_API_SECRET || 'api_secret'
});

// Configuration du storage Cloudinary
const storage = new CloudinaryStorage({
    cloudinary: cloudinary,
    params: {
        folder: 'pattern-pulls', // Dossier dans Cloudinary
        allowed_formats: ['jpg', 'png', 'jpeg'], // Formats autorisés
        transformation: [
            { width: 500, height: 400, crop: 'limit' },
            { quality: 'auto:good' }
        ],
        public_id: (req, file) => {
            // Nom unique pour chaque image
            const userEmail = req.body.userEmail;
            const patternId = req.params.patternId;
            const timestamp = Date.now();
            return `${userEmail}_${patternId}_${timestamp}`;
        }
    }
});

// Configuration Multer avec Cloudinary
const upload = multer({ 
    storage: storage,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB 
    }
});


// Route pour uploader une image vers Cloudinary
app.post('/api/pattern/:patternId/upload-image', upload.single('patternImage'), async (req, res) => {
    try {
        const patternId = req.params.patternId;
        const userEmail = req.body.userEmail;

        if (!req.file) {
            return res.status(400).json({ message: 'Aucune image fournie' });
        }

        // Vérifier que l'utilisateur existe
        const user = await Utilisateur.findOne({ email: userEmail });
        if (!user) {
            return res.status(404).json({ message: 'Utilisateur non trouvé' });
        }

        console.log('Image uploadée vers Cloudinary:', req.file.path);

        // Les informations Cloudinary sont dans req.file
        const imageData = {
            url: req.file.path,           // URL Cloudinary
            publicId: req.file.filename,  // Public ID
            originalName: req.file.originalname
        };


        res.status(200).json({ 
            message: 'Image uploadée avec succès vers le cloud',
            imageUrl: imageData.url,
            publicId: imageData.publicId
        });

    } catch (error) {
        console.error('Erreur upload Cloudinary:', error);
        res.status(500).json({ message: 'Erreur lors de l\'upload: ' + error.message });
    }
});

// Route pour supprimer une image de Cloudinary
app.delete('/api/pattern/image/:publicId', async (req, res) => {
    try {
        const publicId = decodeURIComponent(req.params.publicId);

        if (!publicId || publicId === 'undefined') {
            return res.status(400).json({ 
                message: 'Public ID manquant ou invalide',
                receivedPublicId: publicId 
            });
        }

        const result = await cloudinary.uploader.destroy(publicId);

        if (result.result === 'ok') {
            res.status(200).json({ 
                message: 'Image supprimée avec succès du cloud'
            });
        } else if (result.result === 'not found') {
            res.status(404).json({ 
                message: 'Image non trouvée dans le cloud'
            });
        } else {
            res.status(500).json({ 
                message: 'Échec de la suppression dans le cloud'
            });
        }

    } catch (error) {
        console.error('Erreur suppression Cloudinary:', error);
        res.status(500).json({ 
            message: 'Erreur serveur lors de la suppression: ' + error.message
        });
    }
});