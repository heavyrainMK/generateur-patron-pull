/*
# *******************************************************
# Nom ......... : script.js
# Rôle ........ : Navigation multi-étapes, validations et gestion de l’envoi de données pour le générateur de patrons
# Auteurs ..... : M, L, M
# Version ..... : V2.0.0 du 05/06/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Gestion de la navigation en 4 étapes, validation côté client des champs,
#                 récupération des données et préparation de l’envoi JSON au backend
#                 (en attente d’implémentation serveur).
#
# Technologies  : JavaScript
# Dépendances . : index.html, style.css, pull.py
# Usage ....... : Ouvrir index.html dans un navigateur, remplir le formulaire étape par étape ;
#                 genererPatron() prépare un POST JSON vers /api/calculer-patron.
# *******************************************************
*/

// Variables globales pour la gestion des étapes
let etapeCourante = 1;
const nombreEtapes = 4;

// Démarrage une fois la page chargée
document.addEventListener('DOMContentLoaded', function() {
    initialiserNavigationEtapes();
    mettreAJourBarreProgression();
    mettreAJourAffichageEtape();
    mettreAJourBoutonsNavigation();
});

// Initialise la navigation par étapes
function initialiserNavigationEtapes() {
    const boutonSuivant = document.getElementById('boutonSuivant');
    const boutonPrecedent = document.getElementById('boutonPrecedent');
    const elementFormulaire = document.getElementById('formulaire');
    
    // Gestion du bouton Suivant
    boutonSuivant.addEventListener('click', function() {
        if (validerEtapeCourante()) {
            if (etapeCourante < nombreEtapes) {
                etapeCourante++;
                mettreAJourAffichageEtape();
                mettreAJourBarreProgression();
                mettreAJourBoutonsNavigation();
                mettreAJourIndicateursEtapes();
            }
        }
    });
    
    // Gestion du bouton Précédent
    boutonPrecedent.addEventListener('click', function() {
        if (etapeCourante > 1) {
            etapeCourante--;
            mettreAJourAffichageEtape();
            mettreAJourBarreProgression();
            mettreAJourBoutonsNavigation();
            mettreAJourIndicateursEtapes();
        }
    });
    
    // Gestion de la soumission du formulaire
    elementFormulaire.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validerToutesEtapes()) {
            // Récupération des données du formulaire
            const donneesForm = new FormData(elementFormulaire);
            const donneesFormulaire = Object.fromEntries(donneesForm.entries());
            
            // Affichage des données saisies (facultatif, pour debug)
            const conteneurDonnees = document.getElementById('résultat');
            if (conteneurDonnees) {
                // On réinitialise le contenu HTML
                conteneurDonnees.innerHTML = "<h2>Valeurs saisies :</h2><ul>";
                for (const [cle, valeur] of Object.entries(donneesFormulaire)) {
                    conteneurDonnees.innerHTML += `<li><strong>${cle}</strong> : ${valeur}</li>`;
                }
                conteneurDonnees.innerHTML += "</ul>";
            }

            // Génération du patron
            genererPatron();
        }
    });
    
    // Navigation en cliquant sur les indicateurs d'étapes
    const indicateursEtape = document.querySelectorAll('.etape');
    indicateursEtape.forEach(indicateur => {
        indicateur.addEventListener('click', function() {
            const etapeCible = parseInt(this.dataset.etape);
            if (etapeCible <= obtenirEtapesTerminees() + 1) {
                etapeCourante = etapeCible;
                mettreAJourAffichageEtape();
                mettreAJourBarreProgression();
                mettreAJourBoutonsNavigation();
                mettreAJourIndicateursEtapes();
            }
        });
    });
}

// Met à jour l'affichage des étapes
function mettreAJourAffichageEtape() {
    const etapes = document.querySelectorAll('.etape-formulaire');
    etapes.forEach(etape => {
        etape.classList.remove('active');
    });
    
    const elementEtapeCourante = document.querySelector(`.etape-formulaire[data-etape="${etapeCourante}"]`);
    if (elementEtapeCourante) {
        elementEtapeCourante.classList.add('active');
    }
}

// Met à jour la barre de progression
function mettreAJourBarreProgression() {
    const remplissage = document.getElementById('remplissageProgression');
    const pourcentage = (etapeCourante / nombreEtapes) * 100;
    remplissage.style.width = pourcentage + '%';
}

// Met à jour les boutons de navigation
function mettreAJourBoutonsNavigation() {
    const boutonSuivant = document.getElementById('boutonSuivant');
    const boutonPrecedent = document.getElementById('boutonPrecedent');
    const boutonSoumettre = document.getElementById('boutonSoumettre');
    
    if (etapeCourante === 1) {
        boutonPrecedent.style.display = 'none';
    } else {
        boutonPrecedent.style.display = 'inline-block';
    }
    
    if (etapeCourante === nombreEtapes) {
        boutonSuivant.style.display = 'none';
        boutonSoumettre.style.display = 'inline-block';
    } else {
        boutonSuivant.style.display = 'inline-block';
        boutonSoumettre.style.display = 'none';
    }
}

// Met à jour les indicateurs d'étapes (numéros, état terminé, etc.)
function mettreAJourIndicateursEtapes() {
    const indicateurs = document.querySelectorAll('.etape');
    indicateurs.forEach((indicateur, index) => {
        const numero = index + 1;
        indicateur.classList.remove('active', 'terminee');
        
        if (numero === etapeCourante) {
            indicateur.classList.add('active');
        } else if (numero < etapeCourante) {
            indicateur.classList.add('terminee');
        }
    });
}

// Valide l'étape courante
function validerEtapeCourante() {
    const elementEtape = document.querySelector(`.etape-formulaire[data-etape="${etapeCourante}"]`);
    const champs = elementEtape.querySelectorAll('input[required], select[required]');
    let estValide = true;
    
    effacerMessagesErreur(elementEtape);
    
    champs.forEach(champ => {
        if (!validerChamp(champ)) {
            estValide = false;
        }
    });
    
    if (etapeCourante === 1) {
        estValide = validerEtape1() && estValide;
    } else if (etapeCourante === 2) {
        estValide = validerEtape2() && estValide;
    } else if (etapeCourante === 3) {
        estValide = validerEtape3() && estValide;
    } else if (etapeCourante === 4) {
        estValide = validerEtape4() && estValide;
    }
    
    return estValide;
}

// Valide un champ de saisie générique (nombre, sélection, etc.)
function validerChamp(champ) {
    const elementErreur = champ.parentElement.querySelector('.message-erreur');
    let estValide = true;
    
    champ.classList.remove('erreur');
    
    if (champ.type === 'number') {
        const valeur = parseFloat(champ.value);
        const min = parseFloat(champ.min);
        const max = parseFloat(champ.max);
        
        if (!champ.value || isNaN(valeur)) {
            afficherErreurChamp(champ, elementErreur, 'Ce champ est obligatoire');
            estValide = false;
        } else if (valeur < min) {
            afficherErreurChamp(champ, elementErreur, `La valeur doit être au moins ${min}`);
            estValide = false;
        } else if (valeur > max) {
            afficherErreurChamp(champ, elementErreur, `La valeur doit être au maximum ${max}`);
            estValide = false;
        }
    } else if (champ.tagName === 'SELECT') {
        if (!champ.value) {
            afficherErreurChamp(champ, elementErreur, 'Veuillez faire un choix');
            estValide = false;
        }
    } else if (champ.required && !champ.value) {
        afficherErreurChamp(champ, elementErreur, 'Ce champ est obligatoire');
        estValide = false;
    }
    
    return estValide;
}

// Affiche un message d'erreur pour un champ
function afficherErreurChamp(champ, elementErreur, message) {
    champ.classList.add('erreur');
    if (elementErreur) {
        elementErreur.textContent = message;
    }
}

// Efface tous les messages d'erreur d'une étape donnée
function effacerMessagesErreur(elementEtape) {
    const messagesErreur = elementEtape.querySelectorAll('.message-erreur');
    const champs = elementEtape.querySelectorAll('input, select');
    
    messagesErreur.forEach(err => err.textContent = '');
    champs.forEach(champ => champ.classList.remove('erreur'));
}

// Validations spécifiques à l'étape 1 (aiguilles pour côtes plus petites)
function validerEtape1() {
    const tailleAigCorps  = parseFloat(document.getElementById('taille_aig_corps').value);
    const tailleAigCotes  = parseFloat(document.getElementById('taille_aig_cotes').value);
    
    let estValide = true;
    
    if (tailleAigCotes >= tailleAigCorps) {
        const elementErreur = document.getElementById('taille_aig_cotes').parentElement.querySelector('.message-erreur');
        afficherErreurChamp(
          document.getElementById('taille_aig_cotes'),
          elementErreur,
          'Les aiguilles pour les côtes doivent être plus petites que celles du corps'
        );
        estValide = false;
    }
    
    return estValide;
}

// Validations spécifiques à l'étape 2 (hauteur d’emmanchure vs longueur totale)
function validerEtape2() {
    const hauteurEmmanchure = parseFloat(document.getElementById('hauteur_emmanchure').value);
    const longueurTotale    = parseFloat(document.getElementById('longueur_totale').value);
    
    let estValide = true;
    
    if (hauteurEmmanchure >= longueurTotale) {
        const elementErreur = document.getElementById('hauteur_emmanchure').parentElement.querySelector('.message-erreur');
        afficherErreurChamp(
          document.getElementById('hauteur_emmanchure'),
          elementErreur,
          'La hauteur d’emmanchure doit être inférieure à la longueur totale'
        );
        estValide = false;
    }
    
    return estValide;
}

// Validations spécifiques à l'étape 3 (tour de poignet et tour de coude inférieurs au tour de bras)
function validerEtape3() {
    const tourBras    = parseFloat(document.getElementById('tour_bras').value);
    const tourPoignet = parseFloat(document.getElementById('tour_poignet').value);
    const tourCoude   = parseFloat(document.getElementById('tour_coude').value);
    
    let estValide = true;
    
    if (tourPoignet >= tourBras) {
        const elementErreur = document.getElementById('tour_poignet').parentElement.querySelector('.message-erreur');
        afficherErreurChamp(
          document.getElementById('tour_poignet'),
          elementErreur,
          'Le tour de poignet doit être inférieur au tour de bras'
        );
        estValide = false;
    }
    
    if (tourCoude >= tourBras) {
        const elementErreur = document.getElementById('tour_coude').parentElement.querySelector('.message-erreur');
        afficherErreurChamp(
          document.getElementById('tour_coude'),
          elementErreur,
          'Le tour de coude doit être inférieur au tour de bras'
        );
        estValide = false;
    }
    
    return estValide;
}

// Validations spécifiques à l'étape 4
function validerEtape4() {
    return true;
}

// Valide toutes les étapes avant génération
function validerToutesEtapes() {
    let estValide = true;
    
    for (let etape = 1; etape <= nombreEtapes; etape++) {
        const etapeOriginale = etapeCourante;
        etapeCourante = etape;
        
        if (!validerEtapeCourante()) {
            estValide = false;
            mettreAJourAffichageEtape();
            mettreAJourBarreProgression();
            mettreAJourBoutonsNavigation();
            mettreAJourIndicateursEtapes();
            break;
        }
        
        etapeCourante = etapeOriginale;
    }
    
    return estValide;
}

// Retourne le nombre d'étapes complétées
function obtenirEtapesTerminees() {
    let termine = 0;
    
    for (let etape = 1; etape <= nombreEtapes; etape++) {
        const elementEtape = document.querySelector(`.etape-formulaire[data-etape="${etape}"]`);
        const champs = elementEtape.querySelectorAll('input[required], select[required]');
        let etapeValide = true;
        
        champs.forEach(champ => {
            if (champ.type === 'number') {
                const valeur = parseFloat(champ.value);
                if (!champ.value || isNaN(valeur)) {
                    etapeValide = false;
                }
            } else if (champ.tagName === 'SELECT') {
                if (!champ.value) {
                    etapeValide = false;
                }
            } else if (champ.required && !champ.value) {
                etapeValide = false;
            }
        });
        
        if (etapeValide) {
            termine = etape;
        } else {
            break;
        }
    }
    
    return termine;
}

// Affiche un message à l'utilisateur
function afficherMessage(message, type = 'info') {
    const elementMessage = document.getElementById('message');
    elementMessage.textContent = message;
    elementMessage.className = type;
    elementMessage.style.display = 'block';
    elementMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Génère le patron de tricot en envoyant les données au serveur
async function genererPatron() {
    try {
        const donneesForm = new FormData(document.getElementById('formulaire'));
        const donnees = Object.fromEntries(donneesForm.entries());
        
        // Conversion des valeurs numériques
        const identifiantsIds = [
            'mailles_10cm', 'rangs_10cm', 'taille_aig_corps', 'taille_aig_cotes',
            'tour_cou', 'tour_poitrine', 'tour_taille', 'hauteur_nuque_taille',
            'tour_hanches', 'largeur_epaules', 'hauteur_emmanchure', 'longueur_totale',
            'longueur_manches', 'tour_bras', 'tour_poignet', 'tour_coude',
            'aisance', 'cotes_bas', 'cotes_poignets'
        ];
        
        identifiantsIds.forEach(champ => {
            if (donnees[champ]) {
                donnees[champ] = parseFloat(donnees[champ]);
            }
        });
        
        // Envoi des données au serveur
        const reponse = await fetch('/api/calculer-patron', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(donnees),
        });
        
        if (!reponse.ok) {
            throw new Error('Erreur lors de la communication avec le serveur');
        }
        
        const resultat = await reponse.json();
        
        // Afficher le patron généré
        document.getElementById('résultat').textContent = resultat.patron;
        document.getElementById('boutonTelecharger').style.display = 'inline-block';
        
        afficherMessage('Patron généré avec succès !', 'success');
        
    } catch (erreur) {
        console.error('Erreur lors de la génération du patron :', erreur);
        afficherMessage('Erreur lors de la génération du patron. Veuillez réessayer plus tard.', 'error');
    }
}
