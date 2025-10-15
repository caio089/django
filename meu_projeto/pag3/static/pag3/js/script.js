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
    const isMobile = window.innerWidth <= 768;
    
    // Cache de elementos DOM para evitar queries repetidas
    const elements = {
        progressBar: document.getElementById('progressBar'),
        progressText: document.getElementById('progressText'),
        floatingProgress: document.getElementById('floatingProgress'),
        floatingProgressBar: document.getElementById('floatingProgressBar'),
        floatingProgressText: document.getElementById('floatingProgressText'),
        backToTopBtn: document.getElementById('backToTop')
    };
    
    // ===== FUNÇÃO PARA MOSTRAR/ESCONDER SEÇÕES =====
    window.showSection = function(sectionId) {
        const allSections = [
            'nage-waza-section',
            'imobilizacoes-section', 
            'henkakuenka-section',
            'technique-cards-section',
            'kaeshi-waza-section'
        ];
        
        allSections.forEach(id => {
            const section = document.getElementById(id);
            if (section) section.classList.add('hidden');
        });
        
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.remove('hidden');
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };
    

    
    // ===== SISTEMA DE PROGRESSO OTIMIZADO =====
    const projCheckboxes = document.querySelectorAll('.proj-checkbox');
    const imobCheckboxes = document.querySelectorAll('.imob-checkbox');
    const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
    const kaeshiWazaCheckboxes = document.querySelectorAll('.kaeshi-waza-checkbox');
    let hasShownCongratulations = false;

    // Função otimizada para atualizar progresso
    function updateProgress() {
        const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
        const completedQuestions = Array.from(projCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(imobCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
        const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
        
        if (elements.progressBar) elements.progressBar.style.width = progress + '%';
        if (elements.progressText) elements.progressText.textContent = Math.round(progress) + '%';
        
        // Mostrar parabéns quando completar
        if (progress >= 100 && !hasShownCongratulations) {
            hasShownCongratulations = true;
            setTimeout(() => showCongratulations(), 500);
        }
    }
    
    // ===== SISTEMA DE PARABÉNS OTIMIZADO =====
    function showCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (!modal) return;
        
        modal.style.display = 'flex';
        modal.classList.remove('hidden');
        modal.style.opacity = '1';
        modal.style.visibility = 'visible';
        modal.style.pointerEvents = 'auto';
        
        localStorage.setItem('congratulationsShown', 'true');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    function closeCongratulations() {
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
        }
    }
    
    // Inicializar botões de parabéns
        const continueBtn = document.getElementById('continueTraining');
        const closeBtn = document.getElementById('closeCongratulations');
        
    if (continueBtn) continueBtn.addEventListener('click', closeCongratulations);
    if (closeBtn) closeBtn.addEventListener('click', closeCongratulations);

    // Função otimizada para barra de progresso flutuante
    function showFloatingProgress(progress) {
        if (!elements.floatingProgress || !elements.floatingProgressBar || !elements.floatingProgressText) return;
        
        elements.floatingProgressBar.style.width = progress + '%';
        elements.floatingProgressText.textContent = Math.round(progress) + '%';
        
        elements.floatingProgress.classList.remove('hidden');
        elements.floatingProgress.style.opacity = '1';
        
        setTimeout(() => {
            elements.floatingProgress.style.opacity = '0';
            setTimeout(() => elements.floatingProgress.classList.add('hidden'), 300);
        }, 2000);
    }

    // Inicializar barra flutuante
    if (elements.floatingProgress) {
        elements.floatingProgress.classList.add('hidden');
        elements.floatingProgress.style.opacity = '0';
    }
    

    
    // Esconder seções inicialmente
    const sectionsToHide = ['nage-waza-section', 'imobilizacoes-section', 'henkakuenka-section'];
    sectionsToHide.forEach(id => {
        const section = document.getElementById(id);
        if (section) section.classList.add('hidden');
    });
    
    // ===== EVENT LISTENERS OTIMIZADOS =====
    function addCheckboxListeners(checkboxes) {
        checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            updateProgress();
            if (e.target.checked) {
                const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
                    const completedQuestions = Array.from(projCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(imobCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
                const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                showFloatingProgress(progress);
            }
        });
    });
    }
    
    // Adicionar listeners para todos os checkboxes
    addCheckboxListeners(projCheckboxes);
    addCheckboxListeners(imobCheckboxes);
    addCheckboxListeners(henkakuenkaCheckboxes);
    addCheckboxListeners(kaeshiWazaCheckboxes);
    // ===== SCROLL OTIMIZADO =====
    if (elements.backToTopBtn) {
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
                elements.backToTopBtn.classList.remove('hidden');
        } else {
                elements.backToTopBtn.classList.add('hidden');
        }
    });
        
        elements.backToTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    }

    // Animação para as divs de navegação japonesa (OTIMIZADA PARA MOBILE)
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        if (isMobile) {
            // Em mobile: mostrar imediatamente sem animação
            card.style.opacity = '1';
            card.style.transform = 'none';
        } else {
            // Em desktop: animação completa
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 200 + (index * 100)); // Delay escalonado para cada card
        }
    });

        // Função para criar partículas (APENAS EM DESKTOP)
    function createParticles(x, y, count = 8) {
        if (isMobile) return; // Pular partículas em mobile
        
        const particlesContainer = document.getElementById('scrollParticles');
        
        if (!particlesContainer) return;
        
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = x + Math.random() * 40 - 20 + 'px';
            particle.style.top = y + Math.random() * 40 - 20 + 'px';
            particle.style.animationDelay = Math.random() * 0.5 + 's';
            
            particlesContainer.appendChild(particle);
            
            // Remover partícula após animação
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 1500);
        }
    }
    
    // Função para criar partículas no botão voltar ao topo (APENAS EM DESKTOP)
    function createBackToTopParticles(button) {
        if (isMobile) return; // Pular partículas em mobile
        
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 12; i++) {
            const particle = document.createElement('div');
            particle.className = 'back-to-top-particle';
            particle.style.left = centerX + (Math.random() - 0.5) * 60 + 'px';
            particle.style.top = centerY + (Math.random() - 0.5) * 60 + 'px';
            particle.style.animationDelay = Math.random() * 0.5 + 's';
            particle.style.background = `rgba(255, 255, 255, ${0.7 + Math.random() * 0.3})`;
            
            document.body.appendChild(particle);
            
            // Remover partícula após animação
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 1200);
        }
    }
    
    // ===== FUNÇÃO DE SCROLL OTIMIZADA =====
    function smoothScrollTo(element, cardElement) {
        const targetElement = document.getElementById(element);
        if (!targetElement) return;
        
        // Scroll simples e rápido
        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    // Função para inicializar animações dos botões back-to-top
    function initializeBackToTopButtons() {
        document.querySelectorAll('.back-to-top-section').forEach(button => {
            // Verificar se o botão está visível
            const isVisible = button.offsetParent !== null;
            
            if (isVisible && !button.hasAttribute('data-initialized')) {
                // Remover event listeners existentes para evitar duplicação
                button.removeEventListener('click', backToTopHandler);
                
                // Adicionar animação de entrada quando o botão aparece
                button.classList.add('animate-in');
                
                // Adicionar event listener
                button.addEventListener('click', backToTopHandler);
                
                // Marcar como inicializado
                button.setAttribute('data-initialized', 'true');
                
                console.log('Botão back-to-top inicializado:', button.textContent.trim());
            }
        });
    }
    
    // Handler para o botão voltar ao topo (OTIMIZADO PARA MOBILE)
    function backToTopHandler() {
        // Criar partículas (APENAS EM DESKTOP)
        if (!isMobile) {
            createBackToTopParticles(this);
        }
        
        // Adicionar efeito visual ao clicar (SIMPLIFICADO EM MOBILE)
        if (!isMobile) {
            this.style.transform = 'scale(0.95)';
            this.style.transition = 'transform 0.1s ease';
        }
        
        // Scroll suave com easing personalizado
        const startPosition = window.pageYOffset;
        const targetPosition = 0;
        const distance = targetPosition - startPosition;
        
        // Duração mais rápida em mobile
        const duration = isMobile ? 500 : 1000;
        let start = null;
        
        // Função de easing suave
        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }
        
        // Função de animação
        function animation(currentTime) {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const progress = Math.min(timeElapsed / duration, 1);
            const easedProgress = easeInOutCubic(progress);
            
            window.scrollTo(0, startPosition + distance * easedProgress);
            
            if (progress < 1) {
                requestAnimationFrame(animation);
            } else {
                // Restaurar o botão após a animação (APENAS EM DESKTOP)
                if (!isMobile) {
                    setTimeout(() => {
                        this.style.transform = 'scale(1)';
                        this.style.transition = 'transform 0.3s ease';
                    }, 100);
                }
            }
        }
        
        requestAnimationFrame(animation);
    }
    
    // Inicializar botões back-to-top
    initializeBackToTopButtons();
    
    // LOOP INFINITO REMOVIDO - Era o principal problema de performance!


    
    // ===== NAVEGAÇÃO OTIMIZADA =====
    const navItems = [
        { nav: 'nage-waza-nav', section: 'nage-waza-section' },
        { nav: 'imobilizacoes-nav', section: 'imobilizacoes-section' },
        { nav: 'henkakuenka-nav', section: 'henkakuenka-section' },
        { nav: 'kaeshi-waza-nav', section: 'kaeshi-waza-section' }
    ];
    
    navItems.forEach(item => {
        const navElement = document.getElementById(item.nav);
        if (navElement) {
            navElement.addEventListener('click', function(e) {
            e.preventDefault();
                showSection(item.section);
            });
        }
    });
    
    // Adicionar animação para todos os cards de navegação japonesa
    document.querySelectorAll('.japanese-nav-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Verificar se é um link de navegação (não interceptar)
            if (this.tagName === 'A' || this.querySelector('a')) {
                // Permitir navegação normal para links
                return;
            }
            
            // Se não for um dos cards principais, criar uma animação genérica
            if (!this.id || (this.id !== 'nage-waza-nav' && this.id !== 'imobilizacoes-nav' && this.id !== 'henkakuenka-nav')) {
                e.preventDefault();
                
                // Adicionar efeito visual
                this.classList.add('clicked');
                
                // Criar partículas
                const rect = this.getBoundingClientRect();
                createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2);
                
                // Remover efeitos após animação
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 500);
            }
        });
    });
    


    
    // --- CARROSSEL IMOBILIZAÇÃO ---
    const carouselImob = document.getElementById('carouselImob');
    const imobLeftBtn = document.getElementById('carouselImobLeft');
    const imobRightBtn = document.getElementById('carouselImobRight');
    if (carouselImob && imobLeftBtn && imobRightBtn) {
        imobLeftBtn.addEventListener('click', () => {
            carouselImob.scrollBy({ left: -carouselImob.offsetWidth * 0.8, behavior: 'smooth' });
            // Animação apenas em desktop
            if (!isMobile) {
                imobLeftBtn.classList.add('carousel-arrow-anim');
                setTimeout(() => imobLeftBtn.classList.remove('carousel-arrow-anim'), 700);
            }
        });
        imobRightBtn.addEventListener('click', () => {
            carouselImob.scrollBy({ left: carouselImob.offsetWidth * 0.8, behavior: 'smooth' });
            // Animação apenas em desktop
            if (!isMobile) {
                imobRightBtn.classList.add('carousel-arrow-anim');
                setTimeout(() => imobRightBtn.classList.remove('carousel-arrow-anim'), 700);
            }
        });
                    // Botões sempre visíveis - removida a lógica de ocultar/mostrar
    }

    // Navegação para Ukemi
    document.getElementById('ukemi-nav').addEventListener('click', function() {
        window.location.href = '/ukemis/';
    });

    // --- FUNÇÕES PARA CARDS DE TÉCNICAS INDIVIDUAIS ---
    
    // Função para mostrar o card de uma técnica específica
    window.showTechniqueCard = function(techniqueId) {
        // Esconder a seção de ataques combinados
        document.getElementById('henkakuenka-section').classList.add('hidden');
        
        // Mostrar a seção de cards de técnicas
        document.getElementById('technique-cards-section').classList.remove('hidden');
        
        // Esconder todos os cards de técnicas
        document.querySelectorAll('.technique-individual-card').forEach(card => {
            card.classList.add('hidden');
        });
        
        // Mostrar o card da técnica selecionada
        const selectedCard = document.getElementById(techniqueId + '-card');
        if (selectedCard) {
            selectedCard.classList.remove('hidden');
        }
        
        // Scroll suave para a seção de técnicas
        setTimeout(() => {
            document.getElementById('technique-cards-section').scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }, 100);
    };
    
    // Função para voltar à seção de ataques combinados
    window.backToHenkakuenka = function() {
        // Esconder a seção de cards de técnicas
        document.getElementById('technique-cards-section').classList.add('hidden');
        
        // Mostrar a seção de ataques combinados
        document.getElementById('henkakuenka-section').classList.remove('hidden');
        
        // Scroll suave para a seção de ataques combinados
        setTimeout(() => {
            document.getElementById('henkakuenka-section').scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        }, 100);
    };
    
    // ===== OTIMIZAÇÕES FINAIS PARA MOBILE =====
    
    // Log de inicialização com informações sobre otimizações
    console.log('Script da Página 3 carregado com sucesso!');
    console.log('Dispositivo detectado:', isMobile ? 'Mobile' : 'Desktop');
    console.log('Animações otimizadas para:', isMobile ? 'Performance mobile' : 'Experiência completa desktop');
    
    // Verificar se é mobile e aplicar otimizações imediatas
    if (isMobile) {
        console.log('Aplicando otimizações mobile...');
        disableMobileAnimations();
    }
    
    // ===== ANIMAÇÕES DO MODAL =====
    // Animações de modal simplificadas para melhorar performance mobile
    function animateModalEnter(modal) {
        if (!modal) return;
        modal.style.display = 'flex';
        modal.style.opacity = '1';
        modal.style.transform = 'scale(1)';
    }
    
    function animateModalExit(modal) {
        if (!modal) return;
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
        }, 200);
    }
    
    // Aplicar animações aos modais existentes
    document.querySelectorAll('.modal').forEach(modal => {
        // Adicionar classe para animação
        modal.classList.add('modal-animated');
        
        // Interceptar abertura do modal
        const openTriggers = modal.querySelectorAll('[data-modal-open]');
        openTriggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                animateModalEnter(modal);
            });
        });
        
        // Interceptar fechamento do modal
        const closeTriggers = modal.querySelectorAll('[data-modal-close], .close-btn');
        closeTriggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                animateModalExit(modal);
            });
        });
    });
    
    // ===== SCROLL SIMPLIFICADO PARA MELHORAR PERFORMANCE MOBILE =====
    function smoothScrollToOptimized(targetId) {
        const targetElement = document.getElementById(targetId);
        if (!targetElement) return;
        
        // Scroll simples sem animações pesadas
        targetElement.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
    
    // Scroll simplificado para voltar ao topo
    function backToTopOptimized() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

// Substituir funções originais pelas otimizadas
// (Estas serão chamadas quando necessário)
window.smoothScrollToOptimized = smoothScrollToOptimized;
window.backToTopOptimized = backToTopOptimized;

// ===== SETAS DE NAVEGAÇÃO DO CARROSSEL - DESKTOP E MOBILE =====

// Função para inicializar as setas de navegação do carrossel
function initializeCarouselArrows() {
    console.log('🔍 Inicializando setas do carrossel...');
    
    // Selecionar todos os containers de carrossel
    const carouselContainers = [
        { id: 'nage-waza-section', selector: '#carouselProj' },
        { id: 'imobilizacoes-section', selector: '.grid' },
        { id: 'henkakuenka-section', selector: '.max-w-6xl' },
        { id: 'kaeshi-waza-section', selector: '.max-w-6xl' }
    ];
    
    carouselContainers.forEach(container => {
        console.log(`🔍 Verificando container: ${container.id} com seletor: ${container.selector}`);
        
        const section = document.getElementById(container.id);
        if (!section) {
            console.log(`❌ Seção ${container.id} não encontrada`);
            return;
        }
        
        console.log(`✅ Seção ${container.id} encontrada`);
        
        const carousel = section.querySelector(container.selector);
        if (!carousel) {
            console.log(`❌ Carrossel não encontrado em ${container.id}`);
            return;
        }
        
        console.log(`✅ Carrossel encontrado em ${container.id}`);
        
        // Verificar se já existem setas para evitar duplicação
        const existingArrows = section.querySelectorAll('.carousel-arrow-left, .carousel-arrow-right');
        if (existingArrows.length > 0) {
            console.log(`⚠️ Setas já existem em ${container.id}, removendo antigas...`);
            existingArrows.forEach(arrow => arrow.remove());
        }
        
        // Criar setas de navegação
        const leftArrow = document.createElement('button');
        const rightArrow = document.createElement('button');
        
        leftArrow.className = 'carousel-arrow-left';
        rightArrow.className = 'carousel-arrow-right';
        
        // Adicionar texto às setas como fallback
        leftArrow.innerHTML = '‹';
        rightArrow.innerHTML = '›';
        
        // Adicionar setas ao container
        section.appendChild(leftArrow);
        section.appendChild(rightArrow);
        
        console.log(`✅ Setas criadas para ${container.id}`);
        console.log(`📍 Posição das setas:`, {
            left: leftArrow.getBoundingClientRect(),
            right: rightArrow.getBoundingClientRect(),
            section: section.getBoundingClientRect()
        });
        
        // Função para verificar se as setas devem estar visíveis
        function updateArrowVisibility() {
            const isAtStart = carousel.scrollLeft <= 0;
            const isAtEnd = carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth;
            const hasScroll = carousel.scrollWidth > carousel.clientWidth;
            
            // Para debug: sempre mostrar as setas inicialmente
            if (container.id === 'nage-waza-section') {
                leftArrow.classList.remove('hidden');
                rightArrow.classList.remove('hidden');
                console.log(`🎯 Setas de projeção sempre visíveis para debug`);
            } else {
                leftArrow.classList.toggle('hidden', isAtStart);
                rightArrow.classList.toggle('hidden', isAtEnd);
            }
            
            console.log(`🔄 Visibilidade das setas em ${container.id}: Esquerda=${!isAtStart}, Direita=${!isAtEnd}, HasScroll=${hasScroll}`);
        }
        
        // Event listeners para as setas
        leftArrow.addEventListener('click', () => {
            console.log(`⬅️ Seta esquerda clicada em ${container.id}`);
            const scrollAmount = carousel.clientWidth * 0.8;
            carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            
            // Atualizar visibilidade após scroll
            setTimeout(updateArrowVisibility, 500);
        });
        
        rightArrow.addEventListener('click', () => {
            console.log(`➡️ Seta direita clicada em ${container.id}`);
            const scrollAmount = carousel.clientWidth * 0.8;
            carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            
            // Atualizar visibilidade após scroll
            setTimeout(updateArrowVisibility, 500);
        });
        
        // Adicionar classe específica para identificação
        leftArrow.setAttribute('data-section', container.id);
        rightArrow.setAttribute('data-section', container.id);
        
        // Atualizar visibilidade inicial
        updateArrowVisibility();
        
        // Atualizar visibilidade durante scroll
        carousel.addEventListener('scroll', updateArrowVisibility);
        
        // Atualizar visibilidade quando a tela é redimensionada
        window.addEventListener('resize', updateArrowVisibility);
        
        // Log adicional para debug
        console.log(`🎯 Setas configuradas para ${container.id}:`, {
            carouselWidth: carousel.clientWidth,
            scrollWidth: carousel.scrollWidth,
            hasScroll: carousel.scrollWidth > carousel.clientWidth
        });
    });
    
    console.log('✅ Inicialização das setas concluída');
}

}); // End of DOMContentLoaded

// Inicializar setas de navegação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM carregado, aguardando inicialização das setas...');
    // Aguardar um pouco para garantir que todas as seções estejam carregadas
    setTimeout(() => {
        console.log('⏰ Inicializando setas após delay...');
        initializeCarouselArrows();
    }, 1000);
});

// Inicializar setas quando uma seção é mostrada
window.showSection = function(sectionId) {
    console.log('Mostrando seção:', sectionId);
    
    // Esconder todas as seções primeiro
    const allSections = [
        'nage-waza-section',
        'imobilizacoes-section', 
        'henkakuenka-section',
        'technique-cards-section',
        'kaeshi-waza-section'
    ];
    
    allSections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.add('hidden');
        }
    });
    
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        
        targetSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Inicializar setas para a seção mostrada
        setTimeout(() => {
            console.log('🎯 Inicializando setas para seção:', sectionId);
            initializeCarouselArrows();
            
            // Se for a seção de projeção, também testar as setas
            if (sectionId === 'nage-waza-section') {
                setTimeout(() => {
                    console.log('🎯 Testando setas para seção de projeção...');
                    forceProjectionArrows(); // Usar a função forçada
                }, 200);
            }
        }, 500);
    }
};





    // ===== FUNÇÕES DE TÉCNICAS INDIVIDUAIS =====
    window.showTechniqueCard = function(techniqueId) {
        document.getElementById('henkakuenka-section').classList.add('hidden');
        document.getElementById('technique-cards-section').classList.remove('hidden');
        
        document.querySelectorAll('.technique-individual-card').forEach(card => {
            card.classList.add('hidden');
        });
        
        const selectedCard = document.getElementById(techniqueId + '-card');
        if (selectedCard) {
            selectedCard.classList.remove('hidden');
        }
        
        setTimeout(() => {
            document.getElementById('technique-cards-section').scrollIntoView({ 
                behavior: 'smooth', block: 'start' 
            });
        }, 100);
    };
    
    window.backToHenkakuenka = function() {
        document.getElementById('technique-cards-section').classList.add('hidden');
        document.getElementById('henkakuenka-section').classList.remove('hidden');
        
        setTimeout(() => {
            document.getElementById('henkakuenka-section').scrollIntoView({ 
                behavior: 'smooth', block: 'start' 
            });
        }, 100);
    };
    
    // Navegação para Ukemi
    const ukemiNav = document.getElementById('ukemi-nav');
    if (ukemiNav) {
        ukemiNav.addEventListener('click', function() {
            window.location.href = '/ukemis/';
        });
    }
    
    // ===== SISTEMA DE PROGRESSO NO BANCO DE DADOS =====
    
    // Salvar progresso no banco de dados
    function saveProgress() {
        const allCheckboxes = [
            ...projCheckboxes,
            ...imobCheckboxes,
            ...henkakuenkaCheckboxes,
            ...kaeshiWazaCheckboxes
        ];
        
        const elementos = [];
        
        allCheckboxes.forEach((checkbox, index) => {
            let tipo = 'proj-checkbox';
            if (checkbox.classList.contains('imob-checkbox')) tipo = 'imob-checkbox';
            else if (checkbox.classList.contains('henkakuenka-checkbox')) tipo = 'henkakuenka-checkbox';
            else if (checkbox.classList.contains('kaeshi-waza-checkbox')) tipo = 'kaeshi-waza-checkbox';
            
            elementos.push({
                id: `checkbox_${index}`,
                tipo: tipo,
                aprendido: checkbox.checked
            });
        });
        
        // Salvar no banco de dados
        fetch('/pagina3/salvar-progresso/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                pagina: 'pagina3',
                elementos: elementos
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Progresso salvo no banco de dados:', data.message);
            } else {
                console.error('Erro ao salvar progresso:', data.error);
            }
        })
        .catch(error => {
            console.error('Erro ao salvar progresso:', error);
        });
    }
    
    // Carregar progresso do banco de dados
    function loadProgress() {
        fetch('/pagina3/carregar-progresso/?pagina=pagina3')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.elementos.length > 0) {
                console.log('Carregando progresso do banco de dados:', data.elementos);
                
                const allCheckboxes = [
                    ...projCheckboxes,
                    ...imobCheckboxes,
                    ...henkakuenkaCheckboxes,
                    ...kaeshiWazaCheckboxes
                ];
                
                data.elementos.forEach(elemento => {
                    const index = parseInt(elemento.id.replace('checkbox_', ''));
                    if (allCheckboxes[index]) {
                        allCheckboxes[index].checked = elemento.aprendido;
                    }
                });
                
                updateProgress();
            } else {
                console.log('Nenhum progresso no banco, usando estado atual');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar progresso do banco:', error);
        });
    }
    
    // Modificar a função addCheckboxListeners para salvar progresso
    function addCheckboxListeners(checkboxes) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function(e) {
                updateProgress();
                saveProgress(); // Salvar no banco quando mudar
                
                if (e.target.checked) {
                    const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
                    const completedQuestions = Array.from(projCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(imobCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length +
                                             Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
                    const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                    showFloatingProgress(progress);
                }
            });
        });
    }
    
    // Carregar progresso ao inicializar
    loadProgress();
    
    // ===== INICIALIZAÇÃO FINAL =====
    console.log('✅ Script da Página 3 otimizado carregado!');
    console.log('📱 Mobile:', isMobile);
    
 // Fim do DOMContentLoaded