document.addEventListener('DOMContentLoaded', function() {
    // --- SISTEMA DE VÍDEOS OTIMIZADO ---
    
    // Função simplificada para extrair ID do YouTube
    function extractYouTubeId(url) {
        const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/);
        return match ? match[1] : null;
    }
    
    // Função otimizada para criar thumbnail
    function createVideoThumbnail(iframe) {
        const src = iframe.getAttribute('src');
        const videoId = extractYouTubeId(src);
        if (!videoId) return iframe;
        
        const container = document.createElement('div');
        container.className = 'video-thumbnail-container';
        container.innerHTML = `
            <img src="https://img.youtube.com/vi/${videoId}/maxresdefault.jpg" alt="Vídeo" style="width:100%;height:100%;object-fit:cover;border-radius:12px;">
            <div class="play-overlay">
                <div class="play-button">▶</div>
            </div>
        `;
        
        container.addEventListener('click', () => {
            container.parentNode.replaceChild(iframe, container);
        });
        
        return container;
    }
    
    // Inicializar thumbnails
    document.querySelectorAll('.video-container iframe[src*="youtube.com"]').forEach(iframe => {
        const thumbnail = createVideoThumbnail(iframe);
        iframe.parentNode.replaceChild(thumbnail, iframe);
    });
    
    // --- ANIMAÇÕES SIMPLIFICADAS ---
    function animateHabilidades() {
        document.querySelectorAll('.habilidade-item').forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(10px)';
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }
    
    // Inicializar animações
    setTimeout(animateHabilidades, 300);
    
    // --- SISTEMA DE PROGRESSO OTIMIZADO ---
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    let hasShownCongratulations = false;
    
    function updateProgress() {
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        const checked = document.querySelectorAll('input[type="checkbox"]:checked');
        const progress = (checked.length / allCheckboxes.length) * 100;
        
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        if (progress >= 100 && !hasShownCongratulations) {
            hasShownCongratulations = true;
            showCongratulations();
        }
    }
    
    // Adicionar listeners a todos os checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateProgress);
    });
    
    updateProgress();
    
    // --- SISTEMA DE PARABÉNS SIMPLIFICADO ---
    function showCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'flex';
            modal.classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    function closeCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
        }
    }
    
    // Event listeners para botões do modal
    const continueBtn = document.getElementById('continueTraining');
    const closeBtn = document.getElementById('closeCongratulations');
    
    if (continueBtn) continueBtn.addEventListener('click', closeCongratulations);
    if (closeBtn) closeBtn.addEventListener('click', closeCongratulations);

    // --- BOTÃO VOLTAR AO TOPO SIMPLIFICADO ---
    const backToTopBtn = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        backToTopBtn.classList.toggle('hidden', window.pageYOffset <= 300);
    });
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // --- ANIMAÇÕES DE NAVEGAÇÃO SIMPLIFICADAS ---
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(10px)';
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });

    // --- NAVEGAÇÃO SIMPLIFICADA ---
    function setupNavigation() {
        const navItems = [
            { nav: 'nage-waza-nav', section: 'nage-waza-section' },
            { nav: 'imobilizacoes-nav', section: 'imobilizacoes-section' },
            { nav: 'chave-braco-nav', section: 'chave-braco-section' },
            { nav: 'estrangulamento-nav', section: 'estrangulamento-section' },
            { nav: 'henkakuenka-nav', section: 'henkakuenka-section' },
            { nav: 'kaeshi-waza-nav', section: 'kaeshi-waza-section' }
        ];
        
        navItems.forEach(item => {
            const nav = document.getElementById(item.nav);
            const section = document.getElementById(item.section);
            
            if (nav && section) {
                nav.addEventListener('click', () => {
                    hideAllSections();
                    section.classList.remove('hidden');
                    section.classList.add('animate-fade-in');
                    setTimeout(() => section.classList.remove('animate-fade-in'), 1000);
                    
                    setTimeout(() => {
                        const targetPosition = section.offsetTop - 100;
                        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
                    }, 300);
                });
            }
        });
    }
    
    setupNavigation();

    // --- SISTEMA DE CARROSSÉIS SIMPLIFICADO ---
    function initializeCarousel(carouselId, leftBtnId, rightBtnId) {
        const carousel = document.getElementById(carouselId);
        const leftBtn = document.getElementById(leftBtnId);
        const rightBtn = document.getElementById(rightBtnId);
        
        if (!carousel || !leftBtn || !rightBtn) return;
        
        leftBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: -carousel.offsetWidth * 0.8, behavior: 'smooth' });
        });
        
        rightBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: carousel.offsetWidth * 0.8, behavior: 'smooth' });
        });
    }
    
    // Inicializar carrosséis
    initializeCarousel('carouselProj', 'carouselLeft', 'carouselRight');
    initializeCarousel('carouselImob', 'carouselImobLeft', 'carouselImobRight');
    initializeCarousel('carouselChave', 'carouselChaveLeft', 'carouselChaveRight');
    initializeCarousel('carouselEstrang', 'carouselEstrangLeft', 'carouselEstrangRight');

    function hideAllSections() {
        const sections = [
            'nage-waza-section', 'imobilizacoes-section', 'chave-braco-section',
            'estrangulamento-section', 'henkakuenka-section', 'kaeshi-waza-section'
        ];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) section.classList.add('hidden');
        });
    }
    
    // Inicializar botões de voltar ao topo das seções
    document.querySelectorAll('.back-to-top-section').forEach(button => {
        if (!button.hasAttribute('data-initialized')) {
            button.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            button.setAttribute('data-initialized', 'true');
        }
    });
});