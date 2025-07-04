/*
# *******************************************************
# Nom ......... : script.js
# Rôle ........ : Navigation multi-étapes, validations et gestion de l’envoi de données pour le générateur de patrons
# Auteurs ..... : M, L, M
# Version ..... : V2.2.4 du 03/07/2025 (modif aisance corps + manches)
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Gestion de la navigation en 5 étapes, validation côté client des champs,
#                 récupération des données et préparation de l’envoi JSON au backend
#
# Technologies  : JavaScript
# Dépendances . : formulaire.html, style.css, knit.py
# Usage ....... : Ouvrir formulaire.html dans un navigateur, remplir le formulaire étape par étape ;
#                 genererPatron() prépare un POST JSON vers /api/calculer-patron.
# *******************************************************
*/

// Variables globales pour la gestion des étapes
let etapeCourante = 1;
const nombreEtapes = 5;

document.addEventListener('DOMContentLoaded', function() {
    initialiserNavigationEtapes();
    mettreAJourBarreProgression();
    mettreAJourAffichageEtape();
    mettreAJourBoutonsNavigation();
    initialiserAisances();
    initialiserChampsAjustes();

    // Patch compatibilité bouton "Générer le patron" en barre flottante
    const boutonSoumettre = document.getElementById('boutonSoumettre');
    const formulaire = document.getElementById('formulaire');
    if (boutonSoumettre && formulaire) {
        boutonSoumettre.type = "button"; // évite le submit natif hors formulaire
        boutonSoumettre.addEventListener('click', function(e) {
            formulaire.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        });
    }
});

function initialiserAisances() {
    // Corps
    const modeAisanceCorps = document.getElementById('mode_aisance_corps');
    const containerPersoCorps = document.getElementById('containerAisancePersoCorps');
    const champAisanceCorps = document.getElementById('aisance_corps');
    function updateAisanceCorps() {
        if (modeAisanceCorps.value === 'personnalise') {
            containerPersoCorps.style.display = 'block';
            champAisanceCorps.required = true;
        } else {
            containerPersoCorps.style.display = 'none';
            champAisanceCorps.required = false;
            champAisanceCorps.value = '';
        }
        afficherMasquerChampsAjustes(modeAisanceCorps.value); // optionnel
    }
    modeAisanceCorps.addEventListener('change', updateAisanceCorps);
    updateAisanceCorps();

    // Manches
    const modeAisanceManches = document.getElementById('mode_aisance_manches');
    const containerPersoManches = document.getElementById('containerAisancePersoManches');
    const champAisanceManches = document.getElementById('aisance_manches');
    function updateAisanceManches() {
        if (modeAisanceManches.value === 'personnalise') {
            containerPersoManches.style.display = 'block';
            champAisanceManches.required = true;
        } else {
            containerPersoManches.style.display = 'none';
            champAisanceManches.required = false;
            champAisanceManches.value = '';
        }
    }
    modeAisanceManches.addEventListener('change', updateAisanceManches);
    updateAisanceManches();
}

function initialiserChampsAjustes() {
    // Affiche/masque selon la valeur initiale
    afficherMasquerChampsAjustes(document.getElementById('mode_aisance_corps').value);
    document.getElementById('mode_aisance_corps').addEventListener('change', function() {
        afficherMasquerChampsAjustes(this.value);
    });
}

// Affichage des champs "ajustés" en fonction du mode d'aisance du CORPS
function afficherMasquerChampsAjustes(mode) {
    // Champs de classe champ-ajuste
    const champsAjuste = document.querySelectorAll('.champ-ajuste');
    if (mode === "tres_ajuste" || mode === "ajuste") {
        champsAjuste.forEach(label => {
            label.style.display = '';
            // Rends les champs obligatoires
            const input = label.querySelector('input');
            if (input) input.required = true;
        });
        // Les champs "hauteur_nuque_taille" et "tour_hanches" n'ont pas toujours la classe, on force ici aussi :
        const champsSpecials = ["hauteur_nuque_taille", "tour_hanches", "tour_coude"];
        champsSpecials.forEach(id => {
            const input = document.getElementById(id);
            if (input) input.required = true;
            if (input && input.parentElement) input.parentElement.style.display = '';
        });
    } else {
        champsAjuste.forEach(label => {
            label.style.display = 'none';
            const input = label.querySelector('input');
            if (input) {
                input.required = false;
                input.value = '';
            }
        });
        // On masque/retire aussi ceux qui n'avaient pas la classe sur le label
        const champsSpecials = ["hauteur_nuque_taille", "tour_hanches", "tour_coude"];
        champsSpecials.forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.required = false;
                input.value = '';
                if (input.parentElement) input.parentElement.style.display = 'none';
            }
        });
    }
}

function initialiserNavigationEtapes() {
    const boutonSuivant = document.getElementById('boutonSuivant');
    const boutonPrecedent = document.getElementById('boutonPrecedent');
    const elementFormulaire = document.getElementById('formulaire');
    
    boutonSuivant.addEventListener('click', function() {
        if (validerEtapeCourante()) {
            boutonSuivant.classList.add('glow');
            setTimeout(() => boutonSuivant.classList.remove('glow'), 500);

            if (etapeCourante < nombreEtapes) {
                etapeCourante++;
                mettreAJourAffichageEtape();
                mettreAJourBarreProgression();
                mettreAJourBoutonsNavigation();
                mettreAJourIndicateursEtapes();
            }
        }
    });
    boutonPrecedent.addEventListener('click', function() {
        if (etapeCourante > 1) {
            boutonPrecedent.classList.add('glow');
            setTimeout(() => boutonPrecedent.classList.remove('glow'), 500);
            etapeCourante--;
            mettreAJourAffichageEtape();
            mettreAJourBarreProgression();
            mettreAJourBoutonsNavigation();
            mettreAJourIndicateursEtapes();
        }
    });
    elementFormulaire.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validerToutesEtapes()) {
            const donneesForm = new FormData(elementFormulaire);
            const donneesFormulaire = Object.fromEntries(donneesForm.entries());
            const conteneurDonnees = document.getElementById('résultat');
            if (conteneurDonnees) {
                conteneurDonnees.innerHTML = "<h2>Valeurs saisies :</h2><ul>";
                for (const [cle, valeur] of Object.entries(donneesFormulaire)) {
                    conteneurDonnees.innerHTML += `<li><strong>${cle}</strong> : ${valeur}</li>`;
                }
                conteneurDonnees.innerHTML += "</ul>";
            }
            genererPatron();
        }
    });
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

function mettreAJourAffichageEtape() {
    const etapes = document.querySelectorAll('.etape-formulaire');
    etapes.forEach(etape => {
        etape.classList.remove('active');
    });
    const elementEtapeCourante = document.querySelector(`.etape-formulaire[data-etape="${etapeCourante}"]`);
    if (elementEtapeCourante) {
        elementEtapeCourante.classList.add('active');
    }
    afficherMasquerChampsAjustes(document.getElementById('mode_aisance_corps').value);
}

function mettreAJourBarreProgression() {
    const remplissage = document.getElementById('remplissageProgression');
    const pourcentage = (etapeCourante / nombreEtapes) * 100;
    remplissage.style.width = pourcentage + '%';
}

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
    // Ajout validation de l’aisance personnalisée si affichée
    if (etapeCourante === 1) {
        estValide = validerAisanceEtape1() && estValide;
    } else if (etapeCourante === 2) {
        estValide = validerEtape2() && estValide;
    } else if (etapeCourante === 3) {
        estValide = validerEtape3() && estValide;
    }
    return estValide;
}

function validerChamp(champ) {
    const elementErreur = champ.parentElement.querySelector('.message-erreur');
    let estValide = true;
    champ.classList.remove('erreur');
    if (champ.type === 'number') {
        const valeur = parseFloat(champ.value);
        const min = parseFloat(champ.min);
        const max = parseFloat(champ.max);
        if (champ.required && (!champ.value || isNaN(valeur))) {
            afficherErreurChamp(champ, elementErreur, 'Ce champ est obligatoire');
            estValide = false;
        } else if (champ.required && valeur < min) {
            afficherErreurChamp(champ, elementErreur, `La valeur doit être au moins ${min}`);
            estValide = false;
        } else if (champ.required && valeur > max) {
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

function afficherErreurChamp(champ, elementErreur, message) {
    champ.classList.add('erreur');
    if (elementErreur) {
        elementErreur.textContent = message;
    }
}

function effacerMessagesErreur(elementEtape) {
    const messagesErreur = elementEtape.querySelectorAll('.message-erreur');
    const champs = elementEtape.querySelectorAll('input, select');
    messagesErreur.forEach(err => err.textContent = '');
    champs.forEach(champ => champ.classList.remove('erreur'));
}

function validerAisanceEtape1() {
    let estValide = true;
    // Corps
    const modeAisanceCorps = document.getElementById('mode_aisance_corps');
    if (!modeAisanceCorps.value) estValide = false;
    if (modeAisanceCorps.value === "personnalise") {
        const champAisanceCorps = document.getElementById('aisance_corps');
        const valeur = parseFloat(champAisanceCorps.value);
        if (champAisanceCorps.value === "" || isNaN(valeur)) {
            afficherErreurChamp(champAisanceCorps, champAisanceCorps.parentElement.querySelector('.message-erreur'), 'Valeur obligatoire');
            estValide = false;
        }
        if (valeur < parseFloat(champAisanceCorps.min) || valeur > parseFloat(champAisanceCorps.max)) {
            afficherErreurChamp(champAisanceCorps, champAisanceCorps.parentElement.querySelector('.message-erreur'), `L'aisance doit être entre ${champAisanceCorps.min} et ${champAisanceCorps.max} cm`);
            estValide = false;
        }
    }
    // Manches
    const modeAisanceManches = document.getElementById('mode_aisance_manches');
    if (!modeAisanceManches.value) estValide = false;
    if (modeAisanceManches.value === "personnalise") {
        const champAisanceManches = document.getElementById('aisance_manches');
        const valeur = parseFloat(champAisanceManches.value);
        if (champAisanceManches.value === "" || isNaN(valeur)) {
            afficherErreurChamp(champAisanceManches, champAisanceManches.parentElement.querySelector('.message-erreur'), 'Valeur obligatoire');
            estValide = false;
        }
        if (valeur < parseFloat(champAisanceManches.min) || valeur > parseFloat(champAisanceManches.max)) {
            afficherErreurChamp(champAisanceManches, champAisanceManches.parentElement.querySelector('.message-erreur'), `L'aisance doit être entre ${champAisanceManches.min} et ${champAisanceManches.max} cm`);
            estValide = false;
        }
    }
    return estValide;
}

function validerEtape2() {
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

function validerEtape3() {
    const tourBras    = parseFloat(document.getElementById('tour_bras').value);
    const tourPoignet = parseFloat(document.getElementById('tour_poignet').value);
    const tourCoude   = document.getElementById('tour_coude') ? parseFloat(document.getElementById('tour_coude').value) : null;
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
    // Teste tour_coude uniquement s'il est affiché et requis
    const tourCoudeInput = document.getElementById('tour_coude');
    if (tourCoudeInput && tourCoudeInput.required && tourCoude >= tourBras) {
        const elementErreur = tourCoudeInput.parentElement.querySelector('.message-erreur');
        afficherErreurChamp(
          tourCoudeInput,
          elementErreur,
          'Le tour de coude doit être inférieur au tour de bras'
        );
        estValide = false;
    }
    return estValide;
}

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
function obtenirEtapesTerminees() {
    let termine = 0;
    for (let etape = 1; etape <= nombreEtapes; etape++) {
        const elementEtape = document.querySelector(`.etape-formulaire[data-etape="${etape}"]`);
        const champs = elementEtape.querySelectorAll('input[required], select[required]');
        let etapeValide = true;
        champs.forEach(champ => {
            if (champ.type === 'number') {
                const valeur = parseFloat(champ.value);
                if (champ.required && (!champ.value || isNaN(valeur))) {
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

function afficherMessage(message, type = 'info') {
    const elementMessage = document.getElementById('message');
    elementMessage.textContent = message;
    elementMessage.className = type;
    elementMessage.style.display = 'block';
    elementMessage.style.opacity = "1";
    elementMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });

    if (type === 'success' || type === 'error' || type === 'info') {
        setTimeout(() => {
            elementMessage.style.opacity = "0";
            setTimeout(() => {
                elementMessage.style.display = "none";
                elementMessage.className = "";
            }, 600);
        }, 3500);
    }
}

// Génère le patron de tricot en envoyant les données au serveur
async function genererPatron() {
    try {
        // Affiche le loader
        document.getElementById('loader').style.display = 'flex';
        document.getElementById('résultat').style.display = 'none';
        document.getElementById('message').style.display = 'none';

        // Désactive le bouton "Générer le patron"
        const boutonSoumettre = document.getElementById('boutonSoumettre');
        if (boutonSoumettre) boutonSoumettre.disabled = true;

        const donneesForm = new FormData(document.getElementById('formulaire'));
        const donnees = Object.fromEntries(donneesForm.entries());
        // Conversion des valeurs numériques
        const identifiantsIds = [
            'mailles_10cm', 'rangs_10cm', 'taille_aig_corps', 'taille_aig_cotes',
            'tour_cou', 'tour_poitrine', 'tour_taille', 'hauteur_nuque_taille',
            'tour_hanches', 'largeur_nuque', 'hauteur_emmanchure', 'longueur_totale',
            'longueur_manches', 'tour_bras', 'tour_poignet', 'tour_coude',
            'aisance_corps', 'aisance_manches', 'cotes_bas', 'cotes_poignets'
        ];
        identifiantsIds.forEach(champ => {
            if (donnees[champ]) {
                donnees[champ] = parseFloat(donnees[champ]);
            }
        });

        // Nettoyage : si l’un des modes n’est pas "personnalisé", on retire la valeur personnalisée correspondante
        if (donnees['mode_aisance_corps'] !== 'personnalise') {
            delete donnees['aisance_corps'];
        }
        if (donnees['mode_aisance_manches'] !== 'personnalise') {
            delete donnees['aisance_manches'];
        }
        // Supprime les champs non affichés/non demandés si mode standard, large, personnalisé (pour le corps !)
        if (!['tres_ajuste', 'ajuste'].includes(donnees['mode_aisance_corps'])) {
            ['tour_taille','tour_hanches','hauteur_nuque_taille','tour_coude'].forEach(cle => delete donnees[cle]);
        }

        const reponse = await fetch('/api/calculer-patron', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(donnees),
        });
        if (!reponse.ok) throw new Error('Erreur lors de la communication avec le serveur');
        const resultat = await reponse.json();

        // Cache loader, affiche résultat
        document.getElementById('loader').style.display = 'none';
        document.getElementById('résultat').textContent = resultat.patron;
        document.getElementById('résultat').style.display = '';
        document.getElementById('boutonTelecharger').style.display = 'inline-block';
        if (boutonSoumettre) boutonSoumettre.disabled = false;
        afficherMessage('Patron généré avec succès !', 'success');
    } catch (erreur) {
        document.getElementById('loader').style.display = 'none';
        if (document.getElementById('boutonSoumettre')) {
            document.getElementById('boutonSoumettre').disabled = false;
        }
        console.error('Erreur lors de la génération du patron :', erreur);
        afficherMessage('Erreur lors de la génération du patron. Veuillez réessayer plus tard.', 'error');
    }
}

// Fonction pour télécharger le patron en PDF
function telechargerPDF() {
    const resultatDiv = document.getElementById('résultat');
    if (!resultatDiv || !resultatDiv.textContent.trim()) {
        afficherMessage("Aucun patron à télécharger !", "error");
        return;
    }

    const titre = "Patron de pull généré";
    const date = new Date().toLocaleDateString();
    const textePatron = resultatDiv.textContent.trim();
    const texteFinal = `${titre}\n${date}\n\n${textePatron}`;
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4"
    });

    // Header stylé
    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text(titre, 105, 22, { align: "center" });
    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);
    doc.text(date, 105, 30, { align: "center" });

    // Séparateur
    doc.setLineWidth(0.5);
    doc.line(20, 35, 190, 35);

    // Texte du patron
    doc.setFont("Courier", "normal");
    doc.setFontSize(11);
    const lignes = doc.splitTextToSize(textePatron, 170);
    doc.text(lignes, 20, 45);

    doc.save(`patron_pull_${date.replaceAll("/", "-")}.pdf`);
}
