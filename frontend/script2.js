document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('about-overlay');
    const aboutBtn = document.getElementById('about-button');
    const closeBtn = document.getElementById('close-modal');
    const mainContainer = document.getElementById('main-container');

    // Ouvrir la fenêtre
    aboutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        modal.classList.add('active');
        mainContainer.classList.add('blur-background');
        document.body.style.overflow = 'hidden';
    });

    // Fermer la fenêtre
    function closeModal() {
        modal.classList.remove('active');
        mainContainer.classList.remove('blur-background');
        document.body.style.overflow = '';
    }

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

    // Liens internes avec alertes démo
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.getAttribute('href').substring(1);
            if (id === 'login') alert('Bouton de connexion. À supprimer si non nécessaire.');
            else if (id === 'login') alert('Redirection vers la page de connexion...');
        });
    });

    // Souris
    window.addEventListener('mousemove', function (e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        document.querySelectorAll('.floating-element').forEach((el, i) => {
            const speed = (i + 1) * 0.5;
            el.style.transform = `translate(${(x - 0.5) * speed * 20}px, ${(y - 0.5) * speed * 20}px)`;
        });
    });

    // Animation bouton au clic
    document.querySelectorAll('.cta-button').forEach(btn => {
        btn.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => this.style.transform = '', 150);
        });
    });
});
