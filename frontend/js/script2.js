/*
# *******************************************************
# Nom ......... : script2.js
# Rôle ........ : Gestion des interactions utilisateur
# Auteurs ..... : M, L, M
# Version ..... : V2.0.1 du 26/06/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Script  pour le pages login.html, page_accueille.html
#
# Technologies  : JavaScript
# Dépendances . : formulaire.html, login.html, page_accueille.html, style.css
# Usage ....... : Ouvrir page_accueille.html dans un navigateur 
# *******************************************************
*/


// INITIALISATION PRINCIPALE

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('user_dashboard')) {
        checkSession();
        loadUserInfo();
    }
    initBackButton();
    initAboutModal();
    initFloatingAnimations();
    initButtonAnimations();
    initLoginForm();
});


// GESTION DU BOUTON RETOUR
function initBackButton() {
    const backBtn = document.getElementById('back-button');
    if (backBtn) {
        backBtn.addEventListener('click', function(e) {
            e.preventDefault();
            goBack();
        });
    }
}


// GESTION DE LA MODAL "À PROPOS"
function initAboutModal() {
    const modal = document.getElementById('about-overlay');
    const aboutBtn = document.getElementById('about-button');
    const closeBtn = document.getElementById('close-modal');
    const mainContainer = document.getElementById('main-container');

    if (!aboutBtn || !modal || !closeBtn) return;

    // Fonction pour fermer la modal
    function closeModal() {
        modal.classList.remove('active');
        if (mainContainer) {
            mainContainer.classList.remove('blur-background');
        }
        document.body.style.overflow = '';
    }

    // Ouvrir la modal
    aboutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.classList.add('active');
        if (mainContainer) {
            mainContainer.classList.add('blur-background');
        }
        document.body.style.overflow = 'hidden';
    });

    // Fermer avec le bouton
    closeBtn.addEventListener('click', closeModal);

    // Fermer en cliquant sur l'overlay
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Fermer avec la touche Échap
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}


// ANIMATIONS FLOTTANTES
function initFloatingAnimations() {
    const floatingElements = document.querySelectorAll('.floating-active, .floating-element');
    
    if (floatingElements.length === 0) return;

    // Initialiser les éléments flottants
    floatingElements.forEach(el => {
        el.classList.add('floating-active');
    });

    // Mouvement avec la souris
    window.addEventListener('mousemove', function(e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        floatingElements.forEach((el, i) => {
            const speed = (i + 1) * 0.5;
            el.style.transform = `translate(${(x - 0.5) * speed * 20}px, ${(y - 0.5) * speed * 20}px)`;
        });
    });
}


// ANIMATIONS DES BOUTONS
function initButtonAnimations() {
    const clickableButtons = document.querySelectorAll('.login-button, .cta-button');
    
    clickableButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => this.style.transform = '', 150);
        });
    });
}


// GESTION DU FORMULAIRE DE CONNEXION
function initLoginForm() {
    const loginForm = document.getElementById('loginForm');
    
    if (!loginForm) return;

    loginForm.addEventListener('submit', handleLoginSubmit);
    initRealTimeValidation();
}

function handleLoginSubmit(e) {
    e.preventDefault();
    
    clearErrors();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!validateLoginForm(email, password)) {
        showAlert('Veuillez corriger les erreurs ci-dessus', 'error');
        return;
    }
    
    performLogin(email, password);
}

function validateLoginForm(email, password) {
    let hasErrors = false;
    
    if (!email) {
        showFieldError('email', 'L\'adresse e-mail est requise');
        hasErrors = true;
    } else if (!isValidEmail(email)) {
        // Si l'e‑mail est renseigné mais invalide
        showFieldError('email', 'Format d\'e-mail invalide');
        hasErrors = true;
    }
    if (!password) {
        showFieldError('password', 'Le mot de passe est requis');
        hasErrors = true;
    }

    return !hasErrors;
}

function initRealTimeValidation() {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    
    if (emailField) {
        emailField.addEventListener('blur', function() {
            const email = this.value.trim();
            if (email && !isValidEmail(email)) {
                showFieldError('email', 'Format d\'e-mail invalide');
                this.classList.add('error');
            } else if (email) {
                clearFieldError('email');
                this.classList.remove('error');
                this.classList.add('success');
            }
        });
    }

    if (passwordField) {
        passwordField.addEventListener('input', function() {
            const password = this.value.trim();
            if (password.length === 0) {
                // Retirer les classes si vide
                this.classList.remove('success');
                this.classList.remove('error');
            } else {
                // Mot de passe présent : succès
                clearFieldError('password');
                this.classList.remove('error');
                this.classList.add('success');
            }
        });
    }
}

// UTILITAIRES DE VALIDATION

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}


// GESTION DES ERREURS

function showFieldError(fieldName, message) {
    const field = document.getElementById(fieldName);
    const errorDiv = document.getElementById(fieldName + '-error');
    
    if (field && errorDiv) {
        field.classList.add('error');
        field.classList.remove('success');
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
    }
}

function clearFieldError(fieldName) {
    const field = document.getElementById(fieldName);
    const errorDiv = document.getElementById(fieldName + '-error');
    
    if (field && errorDiv) {
        field.classList.remove('error');
        errorDiv.classList.remove('show');
        errorDiv.textContent = '';
    }
}

function clearErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    const inputs = document.querySelectorAll('.form-input');
    
    errorMessages.forEach(error => {
        error.classList.remove('show');
        error.textContent = '';
    });
    
    inputs.forEach(input => {
        input.classList.remove('error');
    });
}


// GESTION DES ALERTES

function showAlert(message, type) {
    const alertContainer = document.getElementById('alert-container');
    
    if (!alertContainer) return;

    alertContainer.innerHTML = `
        <div class="alert ${type}">
            ${message}
        </div>
    `;
    
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.add('show');
        }
    }, 100);
    
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => {
                alertContainer.innerHTML = '';
            }, 300);
        }
    }, 5000);
}


// GESTION DE LA CONNEXION API
async function performLogin(email, password) {
    const remember = document.getElementById('remember')?.checked || false;

    try {
        // Appel API vers votre serveur
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Connexion réussie
            showAlert('Connexion réussie !', 'success');
            
            // Sauvegarder les informations utilisateur si "Se souvenir de moi" est coché
            if (remember) {
                localStorage.setItem('userEmail', email);
                localStorage.setItem('rememberMe', 'true');
            }
            // Sauvegarder les infos utilisateur pour la session
            sessionStorage.setItem('userEmail', email);
            sessionStorage.setItem('userPrenom', data.user.prenom);
            sessionStorage.setItem('userNom', data.user.nom);
            sessionStorage.setItem('isLoggedIn', 'true');
            
            // Rediriger vers le dashboard après un court délai
            setTimeout(() => {
                window.location.href = 'user_dashboard.html';
            }, 1000);
            
        } else {
            // Erreur de connexion
            showAlert(data.message || 'Email ou mot de passe incorrect', 'error');
        }
        
    } catch (error) {
        console.error('Erreur:', error);
        showAlert('Erreur de connexion', 'error');
    }}

// GESTION DES INFORMATIONS UTILISATEUR SUR LE DASHBOARD
async function loadUserInfo() {
    try {
        // Vérifier si l'utilisateur est connecté
        const isLoggedIn = sessionStorage.getItem('isLoggedIn');
        const userEmail = sessionStorage.getItem('userEmail');
        
        if (!isLoggedIn || !userEmail) {
            // Rediriger vers la page de connexion si pas connecté
            window.location.href = 'login.html';
            return;
        }

        // Récupérer les infos depuis sessionStorage d'abord
        const userPrenom = sessionStorage.getItem('userPrenom');
        const userNom = sessionStorage.getItem('userNom');
        
        if (userPrenom) {
            updateUserDisplay(userPrenom, userNom);
        } else {
            // Si pas dans sessionStorage, récupérer depuis l'API
            const response = await fetch(`/api/user/${userEmail}`);
            
            if (response.ok) {
                const userData = await response.json();
                updateUserDisplay(userData.prenom, userData.nom);
                
                // Sauvegarder dans sessionStorage pour les prochaines fois
                sessionStorage.setItem('userPrenom', userData.prenom);
                sessionStorage.setItem('userNom', userData.nom);
            } else {
                console.error('Erreur lors de la récupération des infos utilisateur');
                // Rediriger vers la page de connexion en cas d'erreur
                window.location.href = 'login.html';
            }
        }
    } catch (error) {
        console.error('Erreur:', error);
        // Rediriger vers la page de connexion en cas d'erreur
        window.location.href = 'login.html';
    }
}

function updateUserDisplay(prenom, nom) {
    // Mettre à jour l'affichage du prénom
    const userInfoElement = document.querySelector('.user-info span');
    if (userInfoElement) {
        userInfoElement.textContent = `Bonjour, ${prenom}`;
    }
    
    // Mettre à jour l'avatar avec la première lettre du prénom
    const userAvatar = document.querySelector('.user-avatar');
    if (userAvatar) {
        userAvatar.textContent = prenom.charAt(0).toUpperCase();
    }
}

// FONCTION DE DÉCONNEXION
function logout() {
    // Supprimer toutes les informations de session
    sessionStorage.clear();
    
    // Supprimer les informations "se souvenir de moi" si nécessaire
    const rememberMe = localStorage.getItem('rememberMe');
    if (!rememberMe) {
        localStorage.removeItem('userEmail');
    }
    
    // Rediriger vers la page d'accueil
    window.location.href = 'page_accueille.html';
}

// VÉRIFICATION DE LA SESSION AU CHARGEMENT
function checkSession() {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    const currentPath = window.location.pathname;
    
    // Si on est sur une page protégée et pas connecté
    if (currentPath.includes('user_dashboard') && !isLoggedIn) {
        window.location.href = 'login.html';
        return;
    }
    
    // Si on est sur la page de connexion et déjà connecté
    if (currentPath.includes('login.html') && isLoggedIn) {
        window.location.href = 'user_dashboard.html';
        return;
    }
}

function goBack() {
    window.history.back();
}