/*
# *******************************************************
# Nom ......... : register.js
# Rôle ........ : Gérer le processus d'inscription utilisateur
# Auteurs ..... : M, L, M
# Version ..... : V2.0 du 20/07/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Ce script gère la soumission du formulaire d'inscription, 
#                 la validation des champs, et l'affichage des popups de succès/erreur.
# Technologies  : JavaScript
# Dépendances . : register.html
# Usage ....... : Ouvrir register.html dans un navigateur
# *******************************************************
*/


//Gestion des popups (succès et erreur)
// Ferme le popup de succès et redirige vers la page de connexion
function closeSuccessPopup() {
    const popup = document.getElementById('success-popup');
    if (popup) {
        popup.classList.remove('active');
    }
    
    // Redirection vers la page de login
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 300);
}

// Ferme le popup d'erreur
function closeErrorPopup() {
    const popup = document.getElementById('error-popup');
    if (popup) {
        popup.classList.remove('active');
    }
}


// Fonction pour afficher le popup de succès
function showSuccessPopup() {
    const popup = document.getElementById('success-popup');
    if (popup) {
        popup.classList.add('active');
    }
}


// Fonction pour afficher le popup d'erreur
function showErrorPopup(message) {
    const popup = document.getElementById('error-popup');
    const messageElement = document.getElementById('error-message');
            
    if (popup && messageElement) {
        messageElement.textContent = message;
        popup.classList.add('active');
        console.log('Popup d\'erreur affichée avec le message:', message);
    } else {
        console.error('Élément popup d\'erreur non trouvé');
    }
}

function getUserEmail() {
    return sessionStorage.getItem('userEmail') || 
           localStorage.getItem('userEmail') || 
           null;
}

// Gestion de l'inscription utilisateur
// Formulaire d'inscription
// Désactive les messages d'erreur HTML5 natifs en interceptant les événements "invalid".
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        // Désactive la validation HTML5 par défaut
        registerForm.setAttribute('novalidate', 'novalidate');
        // Empêche l'affichage des bulles d'erreur par défaut
        registerForm.addEventListener('invalid', function(e) {
            e.preventDefault();
        }, true);
    }
});

document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Empêcher le rechargement de la page

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Nettoyage des champs
    data.prenom = data.prenom ? data.prenom.trim() : '';
    data.nom    = data.nom ? data.nom.trim()    : '';
    data.email  = data.email ? data.email.trim()  : '';
    data.experience = data.experience || '';

    // Expressions régulières pour validations
    const emailRegex    = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const nameRegex     = /^[A-Za-zÀ-ÖØ-öø-ÿ'\-\s]+$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

    // Vérifications du prénom et du nom (non vides et alphabétiques)
    if (!data.prenom || !nameRegex.test(data.prenom)) {
        showErrorPopup("Veuillez saisir un prénom valide (lettres uniquement).");
        return;
    }
    if (!data.nom || !nameRegex.test(data.nom)) {
        showErrorPopup("Veuillez saisir un nom valide (lettres uniquement).");
        return;
    }
    // Vérification de l'adresse e‑mail
    if (!data.email || !emailRegex.test(data.email)) {
        showErrorPopup("Format de l'adresse e-mail invalide.");
        return;
    }
    // Vérification que l'expérience est sélectionnée
    if (!data.experience) {
        showErrorPopup("Veuillez sélectionner votre niveau d'expérience en tricot.");
        return;
    }

    // Validation des champs
    if (data.password !== data['confirm-password']) {
        showErrorPopup("Les mots de passe ne correspondent pas.");
        return;
    }

    // Validation du mot de passe (longueur et complexité)
    if (!passwordRegex.test(data.password)) {
        showErrorPopup("Le mot de passe doit contenir au moins 8 caractères, dont une majuscule, une minuscule et un chiffre.");
        return;
    }

    try {
        console.log('Envoi de la demande d\'inscription...');
                
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
    });

    console.log('Réponse reçue:', response.status);

    if (response.ok) {
            // Inscription réussie
            console.log('Inscription réussie, affichage du popup de succès');
            const responseData = await response.json();
            console.log('Données de réponse:', responseData);
                    
            form.reset(); 
            // Affiche le message de succès
            showSuccessPopup();
                    
    } else {
            // Erreur côté serveur
            const errorData = await response.json();
            console.error('Erreur d\'inscription:', errorData);
                    
            // Afficher l'erreur
            showErrorPopup(errorData.message || "Une erreur est survenue lors de l'inscription.");
            }
    } catch (error) {
            // Erreur réseau
            console.error('Erreur lors de l\'inscription:', error);
            showErrorPopup("Une erreur réseau est survenue. Veuillez vérifier votre connexion et réessayer.");
        }
});
