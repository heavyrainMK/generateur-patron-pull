/*
# *******************************************************
# Nom ......... : script.js
# Rôle ........ : La collecte et l'affichage des données du formulaire de tricot
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 03/06/2025 
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Récupération des données saisies dans le formulaire HTML,
#                 puis affichage ces valeurs (version sans envoi vers le serveur backend)
#
# Technologies  : JavaScript
# Dépendances . : index.html, style.css, pull.py
# Usage ....... : Ouvrir la page index.html
# *******************************************************
*/


// Démarrage une fois la page chargée
document.addEventListener("DOMContentLoaded", () => {
  
  // Récupère l'élément <form> de la page
  const formulaire = document.querySelector("form");

  // Récupère le conteneur où seront affichés les résultats
  const conteneurResultat = document.getElementById("résultat");


  formulaire.addEventListener("submit", (evenement) => {
    evenement.preventDefault();

    // Liste des identifiants des champs du formulaire:
    const identifiantsIds = [
      "mailles_10cm", "rangs_10cm", "taille_aig_corps", "taille_aig_cotes",
      "tour_cou", "tour_poitrine", "tour_taille", "hauteur_nuque_taille",
      "tour_hanches", "largeur_epaules", "hauteur_emmanchure", "longueur_totale",
      "longueur_manches", "tour_bras", "tour_poignet", "tour_coude", "aisance", "appliquer_aisance",
      "encolure", "cotes_bas", "cotes_poignets"
    ];

    // Stocage des données saisies par l'utilisateur
    const donneesFormulaire = {};

    // Pour chaque identifiant, on récupère la valeur 
    identifiantsIds.forEach(id => {
      const element = document.getElementById(id);
      donneesFormulaire[id] = element ? element.value : null; 
    });

    // Affiche les résultats à l’écran
    conteneurResultat.innerHTML = "<h2>Valeurs saisies :</h2><ul>";
    for (const [cle, valeur] of Object.entries(donneesFormulaire)) {
      conteneurResultat.innerHTML += `<li><strong>${cle}</strong> : ${valeur}</li>`;
    }
    conteneurResultat.innerHTML += "</ul>";

    /*
     TODO : Envoyer les données au backend via fetch() (POST JSON)
    */
  });
});
