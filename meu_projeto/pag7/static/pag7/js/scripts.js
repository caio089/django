document.addEventListener('DOMContentLoaded', function() {
    // ===== NAVEGAÇÃO JAPONESA OTIMIZADA =====
    const navigationConfig = [
        { navId: 'nage-waza-nav', sectionId: 'nage-waza-section' },
        { navId: 'imobilizacoes-nav', sectionId: 'imobilizacoes-section' },
        { navId: 'chave-braco-nav', sectionId: 'chave-braco-section' },
        { navId: 'estrangulamento-nav', sectionId: 'estrangulamento-section' },
        { navId: 'ataque-combinado-nav', sectionId: 'ataque-combinado-section' },
        { navId: 'contra-ataque-nav', sectionId: 'contra-ataque-section' }
    ];
    
    const sections = navigationConfig.map(config => document.getElementById(config.sectionId));
    
    function hideAllSections() {
        sections.forEach(section => section && section.classList.add('hidden'));
    }
    
    function showSectionWithAnimation(section) {
        if (!section) return;
        section.classList.remove('hidden');
        section.classList.add('animate-fade-in');
        setTimeout(() => section.classList.remove('animate-fade-in'), 1300);
    }
    
    function smoothScrollToSection(sectionId, cardElement) {
        const targetElement = document.getElementById(sectionId);
        if (!targetElement) return;
        
        cardElement.classList.add('clicked');
        
        // Usar scroll nativo para melhor performance
        const targetPosition = targetElement.offsetTop - 100;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        
        setTimeout(() => {
            cardElement.classList.remove('clicked');
            targetElement.classList.add('destination-highlight');
            setTimeout(() => targetElement.classList.remove('destination-highlight'), 2000);
        }, 1000);
    }
    
    // Configurar navegação de forma otimizada
    navigationConfig.forEach(config => {
        const nav = document.getElementById(config.navId);
        const section = document.getElementById(config.sectionId);
        
        if (nav && section) {
            nav.addEventListener('click', function(e) {
                hideAllSections();
                showSectionWithAnimation(section);
                setTimeout(() => smoothScrollToSection(config.sectionId, this), 300);
            });
        }
    });

    // ===== CARROSSEIS OTIMIZADOS =====
    
    // Função genérica para configurar carrossel
    function setupCarousel(carouselId, leftBtnId, rightBtnId) {
        const carousel = document.getElementById(carouselId);
        const leftBtn = document.getElementById(leftBtnId);
        const rightBtn = document.getElementById(rightBtnId);
        
        if (!carousel || !leftBtn || !rightBtn) return;
        
        // Função para rolar com animação otimizada
        function scrollCarousel(direction) {
            const scrollAmount = carousel.offsetWidth * 0.8;
            carousel.scrollBy({ 
                left: direction === 'left' ? -scrollAmount : scrollAmount, 
                behavior: 'smooth' 
            });
            
            // Animação da seta clicada
            const clickedBtn = direction === 'left' ? leftBtn : rightBtn;
            clickedBtn.style.transform = 'scale(0.95)';
            setTimeout(() => clickedBtn.style.transform = 'scale(1)', 150);
        }
        
        // Event listeners otimizados
        leftBtn.addEventListener('click', () => scrollCarousel('left'));
        rightBtn.addEventListener('click', () => scrollCarousel('right'));
        
        // Função para atualizar visibilidade das setas
        function updateArrowVisibility() {
            const isAtStart = carousel.scrollLeft <= 10;
            const isAtEnd = carousel.scrollLeft + carousel.offsetWidth >= carousel.scrollWidth - 10;
            
            leftBtn.classList.toggle('hidden', isAtStart);
            rightBtn.classList.toggle('hidden', isAtEnd);
        }
        
        // Event listeners para scroll e resize
        carousel.addEventListener('scroll', updateArrowVisibility);
        window.addEventListener('resize', updateArrowVisibility);
        
        // Inicialização
        setTimeout(updateArrowVisibility, 100);
    }
    
    // Configurar todos os carrosséis
    const carouselConfigs = [
        { id: 'carouselProj', left: 'carouselLeft', right: 'carouselRight' },
        { id: 'carouselImob', left: 'imobLeft', right: 'imobRight' },
        { id: 'carouselChave', left: 'carouselChaveLeft', right: 'carouselChaveRight' },
        { id: 'carouselEstrang', left: 'carouselEstrangLeft', right: 'carouselEstrangRight' },
        { id: 'carouselAtaqueCombinado', left: 'carouselAtaqueCombinadoLeft', right: 'carouselAtaqueCombinadoRight' },
        { id: 'carouselContraAtaque', left: 'carouselContraAtaqueLeft', right: 'carouselContraAtaqueRight' }
    ];
    
    carouselConfigs.forEach(config => setupCarousel(config.id, config.left, config.right));
    
    // ===== PROGRESSO OTIMIZADO =====
    const checkboxTypes = [
        '.proj-checkbox',
        '.imob-checkbox', 
        '.chave-checkbox',
        '.estrang-checkbox',
        '.ataque-combinado-checkbox',
        '.contra-ataque-checkbox'
    ];
    
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    let hasShownCongratulations = false;
    
    function updateProgress() {
        let totalChecked = 0;
        let totalQuestions = 0;
        
        // Calcular progresso de forma otimizada
        checkboxTypes.forEach(selector => {
            const checkboxes = document.querySelectorAll(selector);
            const checked = document.querySelectorAll(`${selector}:checked`);
            totalChecked += checked.length;
            totalQuestions += checkboxes.length;
        });
        
        const progress = totalQuestions > 0 ? (totalChecked / totalQuestions) * 100 : 0;
        
        // Atualizar barra de progresso
        if (progressBar) progressBar.style.width = progress + '%';
        if (progressText) progressText.textContent = Math.round(progress) + '%';
        
        // Verificar se chegou a 100% e mostrar parabéns
        if (progress >= 100 && !hasShownCongratulations) {
            hasShownCongratulations = true;
            setTimeout(() => showCongratulations(), 500);
        }
        
        // Mostrar barra de progresso flutuante
        showFloatingProgress(progress);
    }
    
    function showFloatingProgress(progress) {
        if (!floatingProgress || !floatingProgressBar || !floatingProgressText) return;
        
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = Math.round(progress) + '%';
        
        floatingProgress.classList.remove('opacity-0', 'pointer-events-none');
        floatingProgress.classList.add('opacity-100');
        
        setTimeout(() => {
            floatingProgress.classList.remove('opacity-100');
            floatingProgress.classList.add('opacity-0', 'pointer-events-none');
        }, 5000);
    }
    
    // Event listeners otimizados para checkboxes
    function addCheckboxListeners() {
        checkboxTypes.forEach(selector => {
            document.querySelectorAll(selector).forEach(checkbox => {
                checkbox.addEventListener('change', updateProgress);
            });
        });
    }
    
    addCheckboxListeners();
    updateProgress();
    
    // ===== BOTÃO VOLTAR AO TOPO =====
    const backToTopBtn = document.getElementById('backToTop');
    
    // Função para criar partículas no botão voltar ao topo
    function createBackToTopParticles(button) {
        // Função simplificada para melhor performance mobile
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Criar apenas 3 partículas para economizar recursos
        for (let i = 0; i < 3; i++) {
            const particle = document.createElement('div');
            particle.style.left = centerX + (Math.random() - 0.5) * 40 + 'px';
            particle.style.top = centerY + (Math.random() - 0.5) * 40 + 'px';
            particle.style.background = 'rgba(255, 255, 255, 0.8)';
            particle.style.position = 'fixed';
            particle.style.width = '6px';
            particle.style.height = '6px';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = 9999;
            document.body.appendChild(particle);
            
            // Remover partícula mais rapidamente
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 400);
        }
    }
    
    // Handler otimizado para o botão voltar ao topo
    function backToTopHandler() {
        const button = this;
        createBackToTopParticles(button);
        button.style.transform = 'scale(0.95)';
        button.style.transition = 'transform 0.1s ease';
        
        // Usar scroll nativo para melhor performance
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        setTimeout(() => {
            button.style.transform = 'scale(1)';
            button.style.transition = 'transform 0.3s ease';
        }, 1000);
    }
    
    // Scroll listener otimizado com debounce
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        if (scrollTimeout) clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.remove('hidden');
            } else {
                backToTopBtn.classList.add('hidden');
            }
        }, 100);
    });
    
    // Inicializar botão flutuante
    backToTopBtn.removeEventListener('click', backToTopHandler);
    backToTopBtn.addEventListener('click', backToTopHandler);
    
    // Inicializar botões de voltar ao topo das seções
    function initializeBackToTopSectionButtons() {
        document.querySelectorAll('.back-to-top-section').forEach(button => {
            if (!button.hasAttribute('data-initialized')) {
                button.removeEventListener('click', backToTopHandler);
                button.addEventListener('click', backToTopHandler);
                button.setAttribute('data-initialized', 'true');
            }
        });
    }
    initializeBackToTopSectionButtons();
    // Removido loop infinito - inicialização única é suficiente
    
    // ===== ANIMAÇÕES DE CARDS =====
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });






    updateProgress();
    
    // --- SISTEMA DE PARABÉNS ---
    
    // Função para mostrar modal de parabéns
    function showCongratulations() {
        console.log('=== SHOW CONGRATULATIONS ===');
        
        const modal = document.getElementById('congratulationsModal');
        if (!modal) {
            console.log('ERRO: Modal não encontrado!');
            return;
        }
        
        console.log('Modal encontrado, mostrando...');
        
        // Forçar exibição
        modal.style.display = 'flex';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        modal.style.opacity = '1';
        modal.style.visibility = 'visible';
        modal.style.pointerEvents = 'auto';
        
        hasShownCongratulations = true;
        
        // Adicionar animação de entrada
        const modalContent = modal.querySelector('div');
        if (modalContent) {
            modalContent.classList.add('modal-enter');
        }
        
        // Salvar que já mostrou parabéns
        localStorage.setItem('congratulationsShown', 'true');
        
        // Scroll suave para o topo
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        console.log('Modal deve estar visível agora!');
        console.log('=== FIM SHOW CONGRATULATIONS ===');
    }
    
    // Função para fechar modal
    function closeCongratulations() {
        console.log('Closing congratulations modal');
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            console.log('Modal closed successfully');
        } else {
            console.log('Modal not found for closing');
        }
    }
    
    // Event listeners para botões do modal
    function initializeCongratulationsButtons() {
        const continueBtn = document.getElementById('continueTraining');
        const closeBtn = document.getElementById('closeCongratulations');
        
        console.log('Initializing congratulations buttons');
        console.log('Continue button found:', !!continueBtn);
        console.log('Close button found:', !!closeBtn);
        
        if (continueBtn) {
            continueBtn.addEventListener('click', function() {
                console.log('Continue training clicked');
                closeCongratulations();
                // Aqui você pode adicionar lógica para continuar treinando
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                console.log('Close congratulations clicked');
                closeCongratulations();
            });
        }
    }
    
    // Inicializar botões do modal
    initializeCongratulationsButtons();
    
    // ===== LAZY LOADING DE VÍDEOS =====
    function setupLazyVideos() {
        console.log('Configurando lazy loading de vídeos...');
        
        // Aguardar DOM estar pronto
        setTimeout(() => {
            const videos = document.querySelectorAll('iframe[src*="youtube.com"]');
            console.log('Total de vídeos encontrados:', videos.length);
            
            if (videos.length === 0) {
                console.log('Nenhum vídeo encontrado, tentando novamente em 2 segundos...');
                setTimeout(setupLazyVideos, 2000);
                return;
            }
            
            // Processar cada vídeo
            videos.forEach((video, index) => {
                console.log(`Vídeo ${index + 1}:`, video.src);
                
                // Criar placeholder
                const container = video.parentElement;
                const placeholder = document.createElement('div');
                placeholder.className = 'lazy-video';
                placeholder.innerHTML = `
                    <div class="video-placeholder">
                        <div class="loading-spinner"></div>
                        <p>Carregando vídeo...</p>
                    </div>
                `;
                
                // Salvar dados originais
                placeholder.dataset.src = video.src;
                placeholder.dataset.title = video.title;
                placeholder.dataset.allow = video.allow;
                placeholder.dataset.allowfullscreen = video.allowFullscreen;
                placeholder.dataset.referrerpolicy = video.referrerPolicy;
                
                // Substituir iframe pelo placeholder
                container.replaceChild(placeholder, video);
                
                // Configurar observer para este placeholder
                if ('IntersectionObserver' in window) {
                    const observer = new IntersectionObserver((entries) => {
                        entries.forEach(entry => {
                            if (entry.isIntersecting) {
                                console.log('Vídeo visível, carregando:', entry.target.dataset.src);
                                loadVideo(entry.target);
                                observer.unobserve(entry.target);
                            }
                        });
                    }, {
                        rootMargin: '50px 0px',
                        threshold: 0.1
                    });
                    
                    observer.observe(placeholder);
                } else {
                    // Sem IntersectionObserver, carregar imediatamente
                    console.log('Carregando vídeo imediatamente (sem IntersectionObserver)');
                    loadVideo(placeholder);
                }
            });
            
            console.log('Lazy loading configurado para', videos.length, 'vídeos');
        }, 1500);
    }
    
    function loadVideo(placeholder) {
        const container = placeholder.parentElement;
        const iframe = document.createElement('iframe');
        
        // Configurar iframe
        iframe.src = placeholder.dataset.src;
        iframe.title = placeholder.dataset.title || 'YouTube video player';
        iframe.frameBorder = '0';
        iframe.allow = placeholder.dataset.allow || 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        iframe.referrerPolicy = placeholder.dataset.referrerpolicy || 'strict-origin-when-cross-origin';
        iframe.allowFullscreen = placeholder.dataset.allowfullscreen !== 'false';
        iframe.className = 'w-full h-full border-0 rounded-lg';
        
        // Substituir placeholder pelo iframe
        container.replaceChild(iframe, placeholder);
        console.log('✅ Vídeo carregado:', iframe.src);
    }
    
    // Inicializar lazy loading
    setupLazyVideos();
});