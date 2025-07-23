/*
# *******************************************************
# Nom ......... : user_dashboard.js
# Rôle ........ : Gérer l'affichage du tableau de bord utilisateur :
#                 statistiques, gestion des tags, filtres et recherche.
# Auteurs ..... : M, L, M
# Version ..... : V2.0 du 20/07/2025
# Licence ..... : Réalisé dans le cadre du cours de la Réalisation de Programmes
# Description . : Ce script contrôle l’interaction côté client du tableau de bord.
#                 Il permet d’ajouter/supprimer des tags, filtrer les modèles,
#                 gérer les erreurs de saisie, et afficher des statistiques à jour.
# Technologies  : JavaScript
# Dépendances . : user_dashboard.html
# Usage ....... : Ouvrir user_dashboard.html dans un navigateur web
# *******************************************************
*/


// Statistiques des patterns et tags
// Met à jour les compteurs affichés : nombre de patrons et de tags 
function updateStats() {
    const patternCards = document.querySelectorAll('.pattern-card');
    const patternsCount = patternCards.length;
        
    const allTags = document.querySelectorAll('.tag.removable');
    const uniqueTags = new Set();
        
    allTags.forEach(tag => {
        const tagText = tag.textContent.replace('×', '').trim().toLowerCase();
        uniqueTags.add(tagText);
    });
        
    document.getElementById('patternsCount').textContent = patternsCount;
    document.getElementById('tagsCount').textContent = uniqueTags.size;
}

// Gestion des messages d’erreur
// Affiche un message d'erreur sous un champ input
function showErrorMessage(errorElement, message) {
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        errorElement.classList.remove('fade-out');
            
        errorElement.offsetHeight;
        errorElement.classList.add('show');
            
        const input = errorElement.parentElement.querySelector('.tag-input');
        if (input) {
            input.classList.add('error');
        }
            
            // Cacher après 2.5s + animation de disparition
        setTimeout(() => {
            errorElement.classList.add('fade-out');
            setTimeout(() => {
                errorElement.classList.remove('show', 'fade-out');
                errorElement.style.display = 'none';
                if (input) {
                    input.classList.remove('error');
                }
            }, 1000); 
        }, 2500);
    }
}

// Supprime un tag et met à jour les statistiques
function removeTag(tagElement) {
    const tagsContainer = tagElement.parentElement;
    tagElement.remove();
            
    // Retirer la classe max-tags si on passe sous 6 tags
    const remainingTags = tagsContainer.querySelectorAll('.tag').length;
    if (remainingTags < 6) {
        tagsContainer.classList.remove('max-tags');
    }
    updateStats();
}

        
// Ajoute un tag à la liste
function addTag(buttonElement) {
    const input = buttonElement.previousElementSibling;
    const tagText = input.value.trim();
    const errorMessage = buttonElement.parentElement.querySelector('.error-message');
    const tagsContainer = buttonElement.parentElement.previousElementSibling;
            
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
            
            // Vérifier que le tag n'est pas vide
    if (!tagText) {
        showErrorMessage(errorMessage, 'Veuillez saisir un tag');
        return;
    }
            
    // Vérifier la limite de 6 tags
    const currentTags = tagsContainer.querySelectorAll('.tag').length;
    if (currentTags >= 6) {
        showErrorMessage(errorMessage, 'Maximum 6 tags autorisés');
        return;
    }
            
    // Vérifier la longueur du tag (maximum 12 caractères)
    if (tagText.length > 12) {
        showErrorMessage(errorMessage, 'Erreur: maximum autorisé 12 lettres');
        return;
    }
            
    // Vérifier si le tag existe déjà
    const existingTags = Array.from(tagsContainer.querySelectorAll('.tag')).map(tag => 
        tag.textContent.replace('×', '').trim().toLowerCase()
    );
            
    if (existingTags.includes(tagText.toLowerCase())) {
        showErrorMessage(errorMessage, 'Ce tag existe déjà');
        return;
    }
            
    // Créer le nouveau tag
    const newTag = document.createElement('span');
    newTag.className = 'tag removable';
    newTag.onclick = function() { removeTag(this); };
    newTag.innerHTML = `${tagText} <span class="remove-tag">×</span>`;
            
    tagsContainer.appendChild(newTag);
    input.value = '';
            
    // Ajouter la classe max-tags si on atteint 6 tags
    const newTagsCount = tagsContainer.querySelectorAll('.tag').length;
    if (newTagsCount >= 6) {
        tagsContainer.classList.add('max-tags');
    }
    // Mettre à jour les statistiques
    updateStats();
}

// Gestion de la touche "Entrée" pour ajouter un tag
function handleTagKeyPress(event, inputElement) {
    if (event.key === 'Enter') {
        event.preventDefault();
        addTag(inputElement.nextElementSibling);
    }
}



// Fonction pour filtrer les patrons par tag
function filterPatterns(searchTerm) {
    const patternCards = document.querySelectorAll('.pattern-card');
    const searchTermLower = searchTerm.toLowerCase();
        
    patternCards.forEach(card => {
        const title = card.querySelector('.pattern-title').textContent.toLowerCase();
        const tags = Array.from(card.querySelectorAll('.tag')).map(tag => 
            tag.textContent.replace('×', '').trim().toLowerCase()
        );
            
        const matchesSearch = title.includes(searchTermLower) || 
            tags.some(tag => tag.includes(searchTermLower));
            
        card.style.display = matchesSearch ? 'block' : 'none';
    });
}

// Fonction pour filtrer les patrons par type
function filterPatternsByType(filterType) {
    const patternCards = document.querySelectorAll('.pattern-card');
        
    patternCards.forEach(card => {
        switch(filterType) {
            case 'all':
                card.style.display = 'block';
                break;
            case 'recent':
                const dateText = card.querySelector('.pattern-date').textContent;
                const isRecent = isPatternRecent(dateText);
                card.style.display = isRecent ? 'block' : 'none';
                break;
            default:
                card.style.display = 'block';
        }
    });
}

// Fonction pour vérifier si un patron est récent
function isPatternRecent(dateText) {
    const dateMatch = dateText.match(/(\d{1,2})\s+(\w+)\s+(\d{4})/);
    if (!dateMatch) return false;
        
    const [, day, monthName, year] = dateMatch;
    const months = {
        'janvier': 0, 'février': 1, 'mars': 2, 'avril': 3, 'mai': 4, 'juin': 5,
        'juillet': 6, 'août': 7, 'septembre': 8, 'octobre': 9, 'novembre': 10, 'décembre': 11
    };
        
    const patternDate = new Date(year, months[monthName.toLowerCase()], day);
    const today = new Date();
    const diffTime = Math.abs(today - patternDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
    return diffDays <= 45;
}
    
    
// Initialiser les statistiques au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    updateStats();
        
    // Recherche texte
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function () {
        filterPatterns(this.value);
    });

    // Filtre par type
    const filterSelect = document.getElementById('filterSelect');
    filterSelect.addEventListener('change', function () {
        filterPatternsByType(this.value);
    });
});