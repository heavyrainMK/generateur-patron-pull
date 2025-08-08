/*
# *******************************************************
# Nom .......... : user_dashboard.js
# Rôle ......... : Gérer l'affichage du tableau de bord utilisateur :
#                  statistiques, gestion des tags, ajout et suppression d'images.
# Auteurs ...... : M, L, M
# Version ...... : V2.1 du 06/08/2025
# Licence ...... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description .. : Ce script contrôle l'interaction côté client du tableau de bord.
#                  Il permet d'ajouter/supprimer des tags, d'ajouter/supprimer des images,
#                  de gérer les erreurs de saisie et d'afficher des statistiques.
# Technologies . : JavaScript 
# Dépendances .. : user_dashboard.html
# Usage ........ : Ouvrir user_dashboard.html dans un navigateur web
# *******************************************************
*/



// CONSTANTES ET CONFIGURATION
const CONFIG = {
    MAX_TAGS: 6,
    MAX_TAG_LENGTH: 12,
    MAX_FILE_SIZE: 10 * 1024 * 1024, 
    ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/jpg', 'image/png'],
    ALERT_DISPLAY_TIME: 4000,
    ERROR_DISPLAY_TIME: 2500,
    ANIMATION_DELAY: 100
};



/**
 * Récupère un template HTML et le clone
 * @param {string} templateId - L'ID du template à récupérer
 * @returns {Element|null} - Le template cloné ou null si non trouvé
 */
function getTemplate(templateId) {
    const template = document.getElementById(templateId);
    return template ? template.cloneNode(true) : null;
}

/**
 * Récupère l'email utilisateur depuis sessionStorage
 * @returns {string|null} - L'email de l'utilisateur ou null
 */
function getUserEmail() {
    return sessionStorage.getItem('userEmail');
}

/**
 * Génère une clé pour le localStorage basée sur l'utilisateur et le pattern
 * @param {string|number} patternId - L'ID du pattern
 * @returns {string} - La clé générée
 */
function generateStorageKey(patternId) {
    const userEmail = getUserEmail();
    return `pattern_image_${userEmail}_${patternId}`;
}


// GESTION DES STATISTIQUES
/**
 * Met à jour les compteurs de patterns et tags affichés
 */
function updateStats() {
    const patternCards = document.querySelectorAll('.pattern-card');
    const patternsCount = patternCards.length;
    
    // Compter tous les tags uniques
    const allTags = new Set();
    patternCards.forEach(card => {
        const tagElements = card.querySelectorAll('.tag');
        tagElements.forEach(tagElement => {
            const tagText = tagElement.textContent.replace('×', '').trim().toLowerCase();
            if (tagText) {
                allTags.add(tagText);
            }
        });
    });
    
    // Mettre à jour l'affichage
    updateElementText('patternsCount', patternsCount);
    updateElementText('tagsCount', allTags.size);
    
}

/**
 * Met à jour le texte d'un élément par son ID
 * @param {string} elementId - L'ID de l'élément
 * @param {string|number} text - Le nouveau texte
 */
function updateElementText(elementId, text) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = text;
    }
}


// GESTION DES MESSAGES D'ERREUR
/**
 * Affiche un message d'erreur sous un champ input
 * @param {Element} errorElement - L'élément qui affichera l'erreur
 * @param {string} message - Le message d'erreur
 */
function showErrorMessage(errorElement, message) {
    if (!errorElement) return;
    
    const input = errorElement.parentElement.querySelector('.tag-input');
    
    // Configurer et afficher l'erreur
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    errorElement.classList.remove('fade-out');
    
    // Appliquer les styles en cours
    errorElement.offsetHeight;
    errorElement.classList.add('show');
    
    // Ajouter la classe d'erreur à l'input
    if (input) {
        input.classList.add('error');
    }
    
    // Programmer la disparition
    setTimeout(() => {
        hideErrorMessage(errorElement, input);
    }, CONFIG.ERROR_DISPLAY_TIME);
}

/**
 * Cache le message d'erreur 
 * @param {Element} errorElement - L'élément d'erreur
 * @param {Element} input - L'input associé
 */
function hideErrorMessage(errorElement, input) {
    errorElement.classList.add('fade-out');
    setTimeout(() => {
        errorElement.classList.remove('show', 'fade-out');
        errorElement.style.display = 'none';
        if (input) {
            input.classList.remove('error');
        }
    }, 1000);
}


// GESTION DES TAGS

/**
 * Valide un nouveau tag
 * @param {string} tagText - Le texte du tag à valider
 * @param {Element} tagsContainer - Le conteneur des tags
 * @returns {Object} - Objet avec isValid et errorMessage
 */
function validateTag(tagText, tagsContainer) {
    if (!tagText) {
        return { isValid: false, errorMessage: 'Veuillez saisir un tag' };
    }
    
    const currentTagsCount = tagsContainer.querySelectorAll('.tag').length;
    if (currentTagsCount >= CONFIG.MAX_TAGS) {
        return { isValid: false, errorMessage: `Maximum ${CONFIG.MAX_TAGS} tags autorisés` };
    }
    
    if (tagText.length > CONFIG.MAX_TAG_LENGTH) {
        return { isValid: false, errorMessage: `Erreur: maximum autorisé ${CONFIG.MAX_TAG_LENGTH} lettres` };
    }
    
    // Vérifier les doublons
    const existingTags = Array.from(tagsContainer.querySelectorAll('.tag'))
        .map(tag => tag.textContent.replace('×', '').trim().toLowerCase());
    
    if (existingTags.includes(tagText.toLowerCase())) {
        return { isValid: false, errorMessage: 'Ce tag existe déjà' };
    }
    
    return { isValid: true };
}

/**
 * Crée un nouvel élément tag
 * @param {string} tagText - Le texte du tag
 * @returns {Element|null} - L'élément tag créé
 */
function createTagElement(tagText) {
    const template = getTemplate('template-new-tag');
    if (!template) return null;
    
    template.id = '';
    template.querySelector('.tag-text').textContent = tagText;
    template.addEventListener('click', function() { 
        removeTag(this); 
    });
    
    return template;
}

/**
 * Ajoute un tag à la liste
 * @param {Element} buttonElement - Le bouton d'ajout cliqué
 */
function addTag(buttonElement) {
    const input = buttonElement.previousElementSibling;
    const tagText = input.value.trim();
    const errorMessage = buttonElement.parentElement.querySelector('.error-message');
    const tagsContainer = buttonElement.parentElement.previousElementSibling;
    
    // Cacher les erreurs précédentes
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
    
    // Valider le tag
    const validation = validateTag(tagText, tagsContainer);
    if (!validation.isValid) {
        showErrorMessage(errorMessage, validation.errorMessage);
        return;
    }
    
    // Créer et ajouter le tag
    const tagElement = createTagElement(tagText);
    if (tagElement) {
        tagsContainer.appendChild(tagElement);
        input.value = '';
        
        updateMaxTagsClass(tagsContainer);
        updateStats();
    }
}

/**
 * Supprime un tag et met à jour les statistiques
 * @param {Element} tagElement - L'élément tag à supprimer
 */
function removeTag(tagElement) {
    const tagsContainer = tagElement.parentElement;
    tagElement.remove();
    
    updateMaxTagsClass(tagsContainer);
    updateStats();
}

/**
 * Met à jour la classe max-tags selon le nombre de tags
 * @param {Element} tagsContainer - Le conteneur des tags
 */
function updateMaxTagsClass(tagsContainer) {
    const tagsCount = tagsContainer.querySelectorAll('.tag').length;
    tagsContainer.classList.toggle('max-tags', tagsCount >= CONFIG.MAX_TAGS);
}

/**
 * Gère la touche "Entrée" pour ajouter un tag
 * @param {Event} event - L'événement clavier
 * @param {Element} inputElement - L'élément input
 */
function handleTagKeyPress(event, inputElement) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const addButton = inputElement.nextElementSibling;
        if (addButton) {
            addTag(addButton);
        }
    }
}


// GESTION DES IMAGES

/**
 * Valide un fichier image
 * @param {File} file - Le fichier à valider
 * @returns {Object} - Objet avec isValid et errorMessage
 */
function validateImageFile(file) {
    if (file.size > CONFIG.MAX_FILE_SIZE) {
        return { 
            isValid: false, 
            errorMessage: `L'image est trop grande. Taille maximum : ${CONFIG.MAX_FILE_SIZE / (1024 * 1024)}MB` 
        };
    }
    
    if (!CONFIG.ALLOWED_IMAGE_TYPES.includes(file.type)) {
        return { 
            isValid: false, 
            errorMessage: 'Type de fichier non autorisé. Utilisez JPG, PNG ou GIF.' 
        };
    }
    
    return { isValid: true };
}

/**
 * Gère l'upload d'images vers Cloudinary
 * @param {Event} event - L'événement de changement de fichier
 * @param {string|number} patternId - L'ID du pattern
 */
async function handleImageUpload(event, patternId) {
    const file = event.target.files[0];
    if (!file) return;

    // Validation côté client
    const validation = validateImageFile(file);
    if (!validation.isValid) {
        showAlert(validation.errorMessage, 'error');
        return;
    }

    showImageLoading(patternId, 'Upload vers le cloud...');

    try {
        const formData = new FormData();
        formData.append('patternImage', file);
        formData.append('userEmail', getUserEmail());

        const response = await fetch(`/api/pattern/${patternId}/upload-image`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            saveImageToLocal(patternId, {
                url: result.imageUrl,
                publicId: result.publicId
            });
            
            displayUploadedImage(patternId, result.imageUrl, result.publicId);
            showAlert('Image sauvegardée dans le cloud ! ☁️', 'success');
        } else {
            throw new Error(result.message || 'Erreur lors de l\'upload');
        }

    } catch (error) {
        console.error('Erreur upload Cloudinary:', error);
        showAlert('Erreur lors de l\'upload vers le cloud', 'error');
        restoreImagePlaceholder(patternId);
    }
}

/**
 * Affiche l'état de chargement pendant l'upload
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} message - Le message à afficher
 */
function showImageLoading(patternId, message = 'Téléchargement...') {
    const container = document.getElementById(`imageContainer-${patternId}`);
    const template = getTemplate('template-image-loading');
    
    if (template && container) {
        template.id = '';
        template.querySelector('.loading-message').textContent = message;
        container.innerHTML = '';
        container.appendChild(template);
    }
}

/**
 * Affiche l'image uploadée
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} imageUrl - L'URL de l'image
 * @param {string} publicId - L'ID public Cloudinary
 */
function displayUploadedImage(patternId, imageUrl, publicId) {
    const container = document.getElementById(`imageContainer-${patternId}`);
    const template = getTemplate('template-image-preview');
    
    if (!template || !container) return;
    
    template.id = `imagePreview-${patternId}`;
    
    // Configurer l'image
    const img = template.querySelector('.preview-img');
    img.id = `previewImg-${patternId}`;
    img.src = imageUrl;
    
    // Configurer les contrôles
    setupImageControls(template, patternId, publicId);
    
    container.innerHTML = '';
    container.appendChild(template);
}

/**
 * Configure une modification d'image (changer, supprimer)
 * @param {Element} template - Le template d'image
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} publicId - L'ID public Cloudinary
 */
function setupImageControls(template, patternId, publicId) {
    const changeBtn = template.querySelector('.change-image-btn');
    const removeBtn = template.querySelector('.remove-image-btn');
    const fileInput = template.querySelector('.hidden-file-input');
    
    fileInput.id = `imageInput-${patternId}`;
    fileInput.addEventListener('change', (event) => handleImageUpload(event, patternId));
    
    changeBtn.addEventListener('click', () => fileInput.click());
    
    removeBtn.setAttribute('data-pattern-id', patternId);
    removeBtn.setAttribute('data-public-id', publicId);
    removeBtn.addEventListener('click', function() {
        const patternId = this.getAttribute('data-pattern-id');
        const publicId = this.getAttribute('data-public-id');
        showImageDeleteModal(patternId, publicId);
    });
}


// GESTION DE LA POPUP DE SUPPRESSION D'IMAGE

/**
 * Affiche la popup de confirmation de suppression d'image
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} publicId - L'ID public Cloudinary
 */
function showImageDeleteModal(patternId, publicId) {
    let deleteOverlay = document.getElementById('image-delete-overlay');
    
    if (!deleteOverlay) {
        // Créer la popup
        deleteOverlay = createImageDeleteModal();
        if (!deleteOverlay) return;
        
        document.body.appendChild(deleteOverlay);
    }
    
    // Configurer les données pour cette suppression
    const confirmBtn = deleteOverlay.querySelector('.delete-btn-confirm');
    confirmBtn.setAttribute('data-pattern-id', patternId);
    confirmBtn.setAttribute('data-public-id', publicId);
    
    // Afficher la popup
    deleteOverlay.classList.add('show');
    
    const cancelBtn = deleteOverlay.querySelector('.delete-btn-cancel');
    if (cancelBtn) {
        setTimeout(() => cancelBtn.focus(), 100);
    }
}

/**
 * Crée dynamiquement la popup de suppression d'image
 * @returns {Element|null} - L'élément popup créé
 */

// Fonction pour créer la popup de suppression d'image
function createImageDeleteModal() {
    const template = document.getElementById('template-image-delete');
    const overlay = template.cloneNode(true);
    overlay.id = 'image-delete-overlay'; 
    overlay.style.display = 'flex';

    // Configurer les événements
    const cancelBtn = overlay.querySelector('.delete-btn-cancel');
    const confirmBtn = overlay.querySelector('.delete-btn-confirm');

    cancelBtn.addEventListener('click', hideImageDeleteModal);
    confirmBtn.addEventListener('click', function() {
        const patternId = this.getAttribute('data-pattern-id');
        const publicId = this.getAttribute('data-public-id');
        performImageDeletion(patternId, publicId);
    });

    // Fermer
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            hideImageDeleteModal();
        }
    });

    // Fermer avec Echap
    const escapeHandler = function(e) {
        if (e.key === 'Escape' && overlay.classList.contains('show')) {
            hideImageDeleteModal();
        }
    };

    overlay._escapeHandler = escapeHandler;
    document.addEventListener('keydown', escapeHandler);

    return overlay;
}

document.querySelectorAll('.remove-image-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const modal = createImageDeleteModal();
        document.body.appendChild(modal);

        const confirmBtn = modal.querySelector('.delete-btn-confirm');
        confirmBtn.setAttribute('data-pattern-id', btn.dataset.patternId || '');
        confirmBtn.setAttribute('data-public-id', btn.dataset.publicId || '');
    });
});


/**
 * Cache la popup de suppression d'image
 */
function hideImageDeleteModal() {
    const deleteOverlay = document.getElementById('image-delete-overlay');
    if (deleteOverlay) {
        deleteOverlay.classList.remove('show');
        deleteOverlay.classList.add('hide');
        
        setTimeout(() => {
            deleteOverlay.classList.remove('hide');
            
            // Nettoyer les attributs de données
            const confirmBtn = deleteOverlay.querySelector('.delete-btn-confirm');
            if (confirmBtn) {
                confirmBtn.removeAttribute('data-pattern-id');
                confirmBtn.removeAttribute('data-public-id');
            }
        }, 300);
    }
}

/**
 * Effectue la suppression de l'image après confirmation
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} publicId - L'ID public Cloudinary
 */
async function performImageDeletion(patternId, publicId) {
    // Cacher la popup d'abord
    hideImageDeleteModal();
    
    // Attendre la fermeture de la popup puis supprimer
    setTimeout(async () => {
        await removeImage(patternId, publicId);
    }, 300);
}

/**
 * Supprime une image de Cloudinary 
 * @param {string|number} patternId - L'ID du pattern
 * @param {string} publicId - L'ID public Cloudinary
 */
async function removeImage(patternId, publicId) {
    try {
        // Récupérer publicId depuis localStorage
        if (!publicId) {
            const imageData = getImageFromLocal(patternId);
            publicId = imageData?.publicId;
        }

        if (!publicId) {
            throw new Error('Impossible de trouver l\'identifiant de l\'image');
        }

        showImageLoading(patternId, 'Suppression du cloud...');
        
        const encodedPublicId = encodeURIComponent(publicId);
        const response = await fetch(`/api/pattern/image/${encodedPublicId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok || response.status === 404) {
            // Succès ou image déjà supprimée
            removeImageFromLocal(patternId);
            restoreImagePlaceholder(patternId);
            
            const message = response.status === 404 
                ? 'Image supprimée (était déjà absente du cloud)'
                : 'Image supprimée du cloud ☁️';
            
            showAlert(message, 'success');
        } else {
            throw new Error(result.message || 'Erreur lors de la suppression');
        }

    } catch (error) {
        console.error('Erreur suppression Cloudinary:', error);
        showAlert('Erreur lors de la suppression: ' + error.message, 'error');
        restoreImagePlaceholder(patternId);
    }
}

/**
 * Restaure le placeholder d'image original
 * @param {string|number} patternId - L'ID du pattern
 */
function restoreImagePlaceholder(patternId) {
    const container = document.getElementById(`imageContainer-${patternId}`);
    const template = getTemplate('template-image-placeholder');
    
    if (!template || !container) return;
    
    template.id = `placeholder-${patternId}`;
    
    const fileInput = template.querySelector('.hidden-file-input');
    const uploadBtn = template.querySelector('.upload-btn');
    
    fileInput.id = `imageInput-${patternId}`;
    fileInput.addEventListener('change', (event) => handleImageUpload(event, patternId));
    
    uploadBtn.addEventListener('click', () => fileInput.click());
    
    container.innerHTML = '';
    container.appendChild(template);
}


// GESTION DU STOCKAGE LOCAL

/**
 * Sauvegarde les infos image en localStorage
 * @param {string|number} patternId - L'ID du pattern
 * @param {Object} imageData - Les données de l'image
 */
function saveImageToLocal(patternId, imageData) {
    const key = generateStorageKey(patternId);
    localStorage.setItem(key, JSON.stringify(imageData));
}

/**
 * Récupère les infos image depuis localStorage
 * @param {string|number} patternId - L'ID du pattern
 * @returns {Object|null} - Les données de l'image ou null
 */
function getImageFromLocal(patternId) {
    const key = generateStorageKey(patternId);
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

/**
 * Supprime les infos image du localStorage
 * @param {string|number} patternId - L'ID du pattern
 */
function removeImageFromLocal(patternId) {
    const key = generateStorageKey(patternId);
    localStorage.removeItem(key);
}


// GESTION DES ALERTES

/**
 * Affiche une alerte utilisateur
 * @param {string} message - Le message à afficher
 * @param {string} type - Le type d'alerte ('success' ou 'error')
 */
function showAlert(message, type) {
    let alertContainer = document.getElementById('alert-container');
    
    // Créer le conteneur s'il n'existe pas
    if (!alertContainer) {
        const template = getTemplate('template-alert-container');
        if (template) {
            template.id = 'alert-container';
            document.body.appendChild(template);
            alertContainer = template;
        }
    }

    const template = getTemplate('template-alert');
    if (!template || !alertContainer) return;
    
    template.id = '';
    template.classList.add(type);
    template.querySelector('.alert-message').textContent = message;
    
    alertContainer.appendChild(template);

    // Animation d'entrée
    setTimeout(() => {
        template.classList.add('show');
    }, CONFIG.ANIMATION_DELAY);

    // Suppression automatique
    setTimeout(() => {
        template.classList.add('hide');
        setTimeout(() => {
            if (alertContainer.contains(template)) {
                alertContainer.removeChild(template);
            }
        }, 300);
    }, CONFIG.ALERT_DISPLAY_TIME);
}


// GESTION DE LA POPUP DE DÉCONNEXION

/**
 * Affiche la popup de déconnexion
 */
function showLogoutModal() {
    let logoutOverlay = document.getElementById('logout-overlay');
    
    if (!logoutOverlay) {
        // Créer la popup depuis le template
        const template = document.getElementById('template-logout-modal');
        if (template) {
            logoutOverlay = template.cloneNode(true);
            logoutOverlay.id = 'logout-overlay';
            document.body.appendChild(logoutOverlay);
            
            // Configurer les événements
            const cancelBtn = logoutOverlay.querySelector('.logout-btn-cancel');
            const confirmBtn = logoutOverlay.querySelector('.logout-btn-confirm');
            
            cancelBtn.addEventListener('click', hideLogoutModal);
            confirmBtn.addEventListener('click', performLogout);
            
            // Fermer en cliquant sur l'overlay
            logoutOverlay.addEventListener('click', function(e) {
                if (e.target === logoutOverlay) {
                    hideLogoutModal();
                }
            });
            
            // Fermer avec Echap
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && logoutOverlay.classList.contains('show')) {
                    hideLogoutModal();
                }
            });
        }
    }
    
    // Afficher la popup
    if (logoutOverlay) {
        logoutOverlay.classList.add('show');

        const cancelBtn = logoutOverlay.querySelector('.logout-btn-cancel');
        if (cancelBtn) {
            setTimeout(() => cancelBtn.focus(), 100);
        }
    }
}

/**
 * Cache la popup de déconnexion
 */
function hideLogoutModal() {
    const logoutOverlay = document.getElementById('logout-overlay');
    if (logoutOverlay) {
        logoutOverlay.classList.remove('show');
        logoutOverlay.classList.add('hide');
        
        setTimeout(() => {
            logoutOverlay.classList.remove('hide');
        }, 300);
    }
}

/**
 * Effectue la déconnexion
 */
function performLogout() {
    // Cacher la popup d'abord
    hideLogoutModal();
    
    // Attendre la fermeture de la popup puis déconnecter
    setTimeout(() => {
        // Nettoyer les données
        sessionStorage.clear();
        
        // Rediriger vers la page de connexion
        window.location.href = 'page_accueille.html';
    }, 300);
}

/**
 * Fonction de déconnexion 
 */
function logout() {
    showLogoutModal();
}


// INITIALISATION

/**
 * Initialise les event listeners pour les tags existants
 */
function initializeExistingTags() {
    document.querySelectorAll('.tag.removable').forEach(tag => {
        tag.addEventListener('click', function() { 
            removeTag(this); 
        });
    });
}

/**
 * Initialise les event listeners pour les inputs de tags
 */
function initializeTagInputs() {
    document.querySelectorAll('.tag-input').forEach(input => {
        input.addEventListener('keypress', function(event) {
            handleTagKeyPress(event, this);
        });
    });
}

/**
 * Initialise les event listeners pour les boutons d'ajout de tags
 */
function initializeAddTagButtons() {
    document.querySelectorAll('.add-tag-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            addTag(this);
        });
    });
}

/**
 * Initialise les event listeners pour l'upload d'images
 */
function initializeImageUpload() {
    document.querySelectorAll('.upload-btn').forEach(btn => {
        const container = btn.closest('.image-container');
        if (container) {
            const patternId = container.id.split('-')[1];
            const fileInput = container.querySelector('input[type="file"]');
            
            btn.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', (event) => handleImageUpload(event, patternId));
        }
    });
}

/**
 * Charge les images sauvegardées depuis localStorage
 */
function loadSavedImages() {
    // Patterns 1 à 4
    [1, 2, 3, 4].forEach(patternId => {
        const imageData = getImageFromLocal(patternId);
        if (imageData) {
            displayUploadedImage(patternId, imageData.url, imageData.publicId);
        }
    });
}


/**
 * Initialise tous les composants de la page
 */
function initializeApp() {
    
    updateStats();
    initializeExistingTags();
    initializeTagInputs();
    initializeAddTagButtons();
    initializeImageUpload();
    loadSavedImages();
}


document.addEventListener('DOMContentLoaded', initializeApp);

window.logout = logout;