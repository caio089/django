document.addEventListener('DOMContentLoaded', function() {
    // ===== LAZY LOADING PARA VÍDEOS =====
    function initLazyLoading() {
        const iframes = document.querySelectorAll('iframe[data-src]');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const iframe = entry.target;
                    if (iframe.dataset.src) {
                        iframe.src = iframe.dataset.src;
                        iframe.removeAttribute('data-src');
                        observer.unobserve(iframe);
                    }
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });

        iframes.forEach(iframe => {
            observer.observe(iframe);
        });
    }

    // Inicializar lazy loading
    initLazyLoading();

    // ===== CONFIGURAÇÕES GLOBAIS OTIMIZADAS =====
    const elements = {
        progressBar: document.getElementById('progressBar'),
        progressText: document.getElementById('progressText'),
        floatingProgress: document.getElementById('floatingProgress'),
        floatingProgressBar: document.getElementById('floatingProgressBar'),
        floatingProgressText: document.getElementById('floatingProgressText'),
        backToTopBtn: document.getElementById('backToTop')
    };
    
    const checkboxes = {
        proj: document.querySelectorAll('.proj-checkbox'),
        imob: document.querySelectorAll('.imob-checkbox'),
        chave: document.querySelectorAll('.chave-checkbox'),
        renrakuenka: document.querySelectorAll('.renrakuenka-checkbox'),
        kaeshiWaza: document.querySelectorAll('.kaeshi-waza-checkbox')
    };
    
    let hasShownCongratulations = false;
    
    // ===== SISTEMA DE PROGRESSO OTIMIZADO =====
    function updateProgress() {
        const totalQuestions = Object.values(checkboxes).reduce((total, checkboxList) => total + checkboxList.length, 0);
        const completedQuestions = Object.values(checkboxes).reduce((total, checkboxList) => 
            total + Array.from(checkboxList).filter(cb => cb.checked).length, 0);
        const progress = (completedQuestions / totalQuestions) * 100;
        
        elements.progressBar.style.width = progress + '%';
        elements.progressText.textContent = Math.round(progress) + '%';
        
        showFloatingProgress(progress);
        
        if (progress >= 100 && !hasShownCongratulations) {
            hasShownCongratulations = true;
            setTimeout(() => showCongratulations(), 500);
        }
    }

    // ===== BARRA DE PROGRESSO FLUTUANTE OTIMIZADA =====
    let floatingProgressTimeout;
    function showFloatingProgress(progress) {
        elements.floatingProgressBar.style.width = progress + '%';
        elements.floatingProgressText.textContent = Math.round(progress) + '%';
        elements.floatingProgress.classList.remove('hidden');
        elements.floatingProgress.style.opacity = '1';
        elements.floatingProgress.style.pointerEvents = 'auto';
        
        if (floatingProgressTimeout) clearTimeout(floatingProgressTimeout);
        
        if (progress === 0) {
            elements.floatingProgress.style.opacity = '0';
            elements.floatingProgress.style.pointerEvents = 'none';
            setTimeout(() => elements.floatingProgress.classList.add('hidden'), 300);
        } else {
            floatingProgressTimeout = setTimeout(() => {
                elements.floatingProgress.style.opacity = '0';
                elements.floatingProgress.style.pointerEvents = 'none';
                setTimeout(() => elements.floatingProgress.classList.add('hidden'), 300);
            }, 3000);
        }
    }
    
    // ===== EVENT LISTENERS CONSOLIDADOS =====
    function addCheckboxListeners() {
        Object.values(checkboxes).forEach(checkboxList => {
            checkboxList.forEach(checkbox => {
                checkbox.addEventListener('change', updateProgress);
            });
        });
    }
    
    addCheckboxListeners();
    updateProgress();
    
    // ===== SISTEMA DE PARABÉNS OTIMIZADO =====
    function showCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (!modal) return;
        
        modal.style.display = 'flex';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        modal.style.opacity = '1';
        modal.style.visibility = 'visible';
        modal.style.pointerEvents = 'auto';
        
        const modalContent = modal.querySelector('div');
        if (modalContent) {
            modalContent.classList.add('modal-enter');
        }
        
        localStorage.setItem('congratulationsShown', 'true');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function closeCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    }
    
    // Event listeners para botões do modal
    const continueBtn = document.getElementById('continueTraining');
    const closeBtn = document.getElementById('closeCongratulations');
    
    if (continueBtn) {
        continueBtn.addEventListener('click', closeCongratulations);
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeCongratulations);
    }

    // ===== SCROLL E BOTÃO VOLTAR AO TOPO OTIMIZADO =====
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            elements.backToTopBtn.classList.remove('hidden');
        } else {
            elements.backToTopBtn.classList.add('hidden');
        }
    });
    
    function backToTopHandler() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    if (elements.backToTopBtn) {
        elements.backToTopBtn.addEventListener('click', backToTopHandler);
    }

    // ===== ANIMAÇÕES DE NAVEGAÇÃO JAPONESA OTIMIZADAS =====
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });

    // ===== NAVEGAÇÃO JAPONESA OTIMIZADA =====
    const sections = {
        nageWaza: { nav: 'nage-waza-nav', section: 'nage-waza-section' },
        imobilizacoes: { nav: 'imobilizacoes-nav', section: 'imobilizacoes-section' },
        chaveBraco: { nav: 'chave-braco-nav', section: 'chave-braco-section' },
        estrangulamento: { nav: 'estrangulamento-nav', section: 'estrangulamento-section' },
        henkakuenka: { nav: 'henkakuenka-nav', section: 'henkakuenka-section' },
        kaeshiWaza: { nav: 'kaeshi-waza-nav', section: 'kaeshi-waza-section' }
    };
    
    function hideAllSections() {
        Object.values(sections).forEach(({ section }) => {
            const element = document.getElementById(section);
            if (element) element.classList.add('hidden');
        });
    }
    // ===== FUNÇÕES DE NAVEGAÇÃO SIMPLIFICADAS =====
    function smoothScrollTo(element) {
        const targetElement = document.getElementById(element);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    function showSectionWithAnimation(section) {
        section.classList.remove('hidden');
        section.classList.add('animate-fade-in');
        setTimeout(() => section.classList.remove('animate-fade-in'), 1300);
    }
    
    function animateJapaneseNavCard(card) {
        card.classList.add('clicked');
        setTimeout(() => card.classList.remove('clicked'), 800);
    }
    // ===== EVENT LISTENERS DE NAVEGAÇÃO CONSOLIDADOS =====
    Object.values(sections).forEach(({ nav, section }) => {
        const navElement = document.getElementById(nav);
        const sectionElement = document.getElementById(section);
        
        if (navElement && sectionElement) {
            navElement.addEventListener('click', function() {
                animateJapaneseNavCard(this);
                hideAllSections();
                showSectionWithAnimation(sectionElement);
                setTimeout(() => smoothScrollTo(section), 300);
            });
        }
    });
    


    // ===== CARROSSÉIS OTIMIZADOS =====
    const carousels = [
        { carousel: 'carouselProj', left: 'carouselLeft', right: 'carouselRight' },
        { carousel: 'carouselImob', left: 'carouselImobLeft', right: 'carouselImobRight' }
    ];
    
    carousels.forEach(({ carousel, left, right }) => {
        const carouselElement = document.getElementById(carousel);
        const leftBtn = document.getElementById(left);
        const rightBtn = document.getElementById(right);
        
        if (carouselElement && leftBtn && rightBtn) {
            leftBtn.addEventListener('click', () => {
                carouselElement.scrollBy({ left: -carouselElement.offsetWidth * 0.8, behavior: 'smooth' });
            });
            
            rightBtn.addEventListener('click', () => {
                carouselElement.scrollBy({ left: carouselElement.offsetWidth * 0.8, behavior: 'smooth' });
            });
        }
    });
    




    // ===== BOTÕES VOLTAR AO TOPO DAS SEÇÕES =====
    document.querySelectorAll('.back-to-top-section').forEach(button => {
        button.addEventListener('click', backToTopHandler);
    });
    
}); // Fim do DOMContentLoaded