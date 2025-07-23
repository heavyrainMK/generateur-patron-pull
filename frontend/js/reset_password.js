/*
# *******************************************************
# Nom ......... : reset_password.js
# Rôle ........ : Gestion de la réinitialisation du mot de passe côté client
# Auteurs ..... : M, L, M
# Version ..... : V2.0 du 20/07/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Vérifie l’email, affiche un message de confirmation
#                 et gère l’affichage/fermeture du popup de succès.
# Technologies  : JavaScript
# Dépendances . : reset_password.html, reset_password.css
# Usage ....... : Ouvrir password_reset.html dans un navigateur
# *******************************************************
*/

// Initialisation
function initPasswordResetPage() {
  const form = document.getElementById('forgot-form'); // Formulaire de récupération
  const overlay = document.getElementById('popup-overlay'); // Popup


  form.addEventListener('submit', handleFormSubmit);
  overlay.addEventListener('click', handleOutsideClick);
}

document.addEventListener('DOMContentLoaded', initPasswordResetPage);

// Vérifie si l'email est au bon format
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Gestion du formulaire
function handleFormSubmit(event) {
  event.preventDefault();

  const email = document.getElementById('reset-email').value.trim();

  if (!isValidEmail(email)) {
    showAlert("Format d'email invalide", "error"); // Message d'erreur si email incorrect
    return;
  }

  showSuccessPopup(email); // Affiche le popup de confirmation
}

//  Alertes 
function showAlert(message, type) {
  const container = document.getElementById('alert-container');
  container.innerHTML = `<div class="alert ${type}">${message}</div>`;
}

// Popup de succès 
function showSuccessPopup(email) {
  const popup = document.getElementById('popup-overlay');
  const emailSpan = document.getElementById('popup-email');

  emailSpan.textContent = email;
  popup.classList.add('active');

  setTimeout(closePopup, 10000); // Fermeture automatique après 10s
}

// Ferme le popup et réinitialise le formulaire
function closePopup() {
  const popup = document.getElementById('popup-overlay');
  popup.classList.remove('active');
  document.getElementById('forgot-form').reset();
}


// Gère le clic en dehors du popup pour le fermer
function handleOutsideClick(event) {
  if (event.target === event.currentTarget) {
    closePopup();
  }
}

// Redirige vers la page de connexion
function goBackToLogin() {
  window.location.href = "login.html";
}