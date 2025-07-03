const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

// Servir les fichiers statiques 
app.use(express.static(path.join(__dirname, '.')));

// Connexion MongoDB
mongoose.connect('mongodb+srv://pull:b7SOBeu4HqfABfct@cluster.puhrkui.mongodb.net/?retryWrites=true&w=majority&appName=Cluster')
    .then(() => console.log('✅ Connecté à MongoDB'))
    .catch(err => console.error('❌ Erreur MongoDB :', err));

// Schéma utilisateur 
const utilisateurSchema = new mongoose.Schema({
    prenom: String,
    nom: String,
    email: String,       
    motdepasse: String,  
    experience: String
});

const Utilisateur = mongoose.model('Utilisateur', utilisateurSchema);

// Route de connexion (pour login.html)
app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        
        console.log('🔍 Tentative de connexion pour:', email);

        if (!email || !password) {
            return res.status(400).json({ message: 'Email et mot de passe requis' });
        }

        // Chercher l'utilisateur par email
        const user = await Utilisateur.findOne({ email: email });
        
        console.log('👤 Utilisateur trouvé:', user ? 'Oui' : 'Non');

        if (!user) {
            return res.status(401).json({ message: 'Email ou mot de passe incorrect' });
        }

        // Vérifier le mot de passe
        if (user.motdepasse !== password) {
            console.log('❌ Mot de passe incorrect');
            return res.status(401).json({ message: 'Email ou mot de passe incorrect' });
        }

        console.log('✅ Connexion réussie pour:', email);
        res.status(200).json({ 
            message: 'Connexion réussie',
            user: {
                prenom: user.prenom,
                nom: user.nom,
                email: user.email
            }
        });
    } catch (err) {
        console.error('❌ Erreur serveur lors de la connexion:', err);
        res.status(500).json({ message: 'Erreur serveur : ' + err.message });
    }
});

// Route d'inscription (pour register.html)
app.post('/api/register', async (req, res) => {
    try {
        const { prenom, nom, email, password, experience } = req.body;

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

        await nouvelUtilisateur.save();
        console.log('✅ Nouvel utilisateur enregistré:', email);
        res.status(201).json({ message: 'Utilisateur enregistré avec succès.' });
    } catch (error) {
        console.error('❌ Erreur lors de l\'enregistrement :', error);
        res.status(500).json({ message: 'Erreur serveur lors de l\'enregistrement.' });
    }
});

// Route pour voir tous les utilisateurs (pour debug)
app.get('/api/utilisateurs', async (req, res) => {
    try {
        const utilisateurs = await Utilisateur.find({});
        res.json(utilisateurs);
    } catch (error) {
        console.error('❌ Erreur lors de la récupération:', error);
        res.status(500).json({ message: 'Erreur lors de la récupération des utilisateurs' });
    }
});

// Routes pour servir les pages HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'page_accueille.html'));
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, 'register.html'));
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
    console.log(`   - Utilisateurs: http://localhost:${PORT}/api/utilisateurs`);
});