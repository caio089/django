document.addEventListener('DOMContentLoaded', function() {
    // --- SISTEMA DE THUMBNAILS ESTÁTICOS PARA VÍDEOS ---
    
    // Função para extrair ID do YouTube da URL
    function extractYouTubeId(url) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
        const match = url.match(regExp);
        return (match && match[2].length === 11) ? match[2] : null;
    }
    
    // Função para criar thumbnail do YouTube
    function createVideoThumbnail(iframe) {
        const src = iframe.getAttribute('src');
        const videoId = extractYouTubeId(src);
        
        if (!videoId) return iframe;
        
        // Criar container do thumbnail
        const thumbnailContainer = document.createElement('div');
        thumbnailContainer.className = 'video-thumbnail-container';
        thumbnailContainer.style.cssText = `
            position: relative;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            overflow: hidden;
        `;
        
        // Criar imagem do thumbnail
        const thumbnailImg = document.createElement('img');
        thumbnailImg.src = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
        thumbnailImg.alt = 'Thumbnail do vídeo';
        thumbnailImg.style.cssText = `
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
        `;
        
        // Criar overlay com botão de play
        const playOverlay = document.createElement('div');
        playOverlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            transition: background 0.3s ease;
        `;
        
        // Criar botão de play
        const playButton = document.createElement('div');
        playButton.innerHTML = `
            <div style="
                width: 80px;
                height: 80px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            ">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="#8B5C2A">
                    <path d="M8 5v14l11-7z"/>
                </svg>
            </div>
        `;
        
        // Adicionar elementos ao container
        thumbnailContainer.appendChild(thumbnailImg);
        playOverlay.appendChild(playButton);
        thumbnailContainer.appendChild(playOverlay);
        
        // Adicionar efeitos de hover
        thumbnailContainer.addEventListener('mouseenter', function() {
            playOverlay.style.background = 'rgba(0, 0, 0, 0.4)';
            playButton.querySelector('div').style.transform = 'scale(1.1)';
            playButton.querySelector('div').style.background = 'rgba(255, 255, 255, 1)';
        });
        
        thumbnailContainer.addEventListener('mouseleave', function() {
            playOverlay.style.background = 'rgba(0, 0, 0, 0.3)';
            playButton.querySelector('div').style.transform = 'scale(1)';
            playButton.querySelector('div').style.background = 'rgba(255, 255, 255, 0.9)';
        });
        
        // Adicionar evento de clique para carregar vídeo
        thumbnailContainer.addEventListener('click', function() {
            loadVideo(thumbnailContainer, iframe);
        });
        
        return thumbnailContainer;
    }
    
    // Função para carregar vídeo quando clicado
    function loadVideo(thumbnailContainer, originalIframe) {
        // Adicionar indicador de carregamento
        const loadingSpinner = document.createElement('div');
        loadingSpinner.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 40px;
            height: 40px;
            border: 4px solid #e5e7eb;
            border-top: 4px solid #8B5C2A;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        `;
        
        // Adicionar CSS para animação de spin se não existir
        if (!document.querySelector('#spin-animation')) {
            const style = document.createElement('style');
            style.id = 'spin-animation';
            style.textContent = `
                @keyframes spin {
                    0% { transform: translate(-50%, -50%) rotate(0deg); }
                    100% { transform: translate(-50%, -50%) rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
        
        thumbnailContainer.appendChild(loadingSpinner);
        
        // Simular carregamento (opcional - pode ser removido para carregamento instantâneo)
        setTimeout(() => {
            // Substituir thumbnail pelo iframe original
            thumbnailContainer.parentNode.replaceChild(originalIframe, thumbnailContainer);
            
            // Adicionar classe para indicar que foi carregado
            originalIframe.classList.add('video-loaded');
            
            console.log('Vídeo carregado:', originalIframe.src);
        }, 500); // Delay de 500ms para mostrar o loading
    }
    
    // Função para inicializar thumbnails em todos os vídeos
    function initializeVideoThumbnails() {
        const videoContainers = document.querySelectorAll('.video-container');
        
        videoContainers.forEach(container => {
            // Verificar se já tem lazy-video
            const lazyVideo = container.querySelector('.lazy-video');
            if (lazyVideo) {
                // Converter lazy-video existente para thumbnail
                convertLazyVideoToThumbnail(lazyVideo);
            } else {
                // Converter iframe direto para thumbnail
                const iframe = container.querySelector('iframe');
                if (iframe && iframe.src.includes('youtube.com')) {
                    const thumbnail = createVideoThumbnail(iframe);
                    container.replaceChild(thumbnail, iframe);
                }
            }
        });
        
        console.log(`Inicializados ${videoContainers.length} thumbnails de vídeo`);
    }
    
    // Função para converter lazy-video existente para thumbnail
    function convertLazyVideoToThumbnail(lazyVideo) {
        const src = lazyVideo.dataset.src;
        const title = lazyVideo.dataset.title;
        
        if (!src || !src.includes('youtube.com')) return;
        
        // Criar iframe temporário para extrair dados
        const tempIframe = document.createElement('iframe');
        tempIframe.src = src;
        tempIframe.title = title;
        
        const thumbnail = createVideoThumbnail(tempIframe);
        lazyVideo.parentNode.replaceChild(thumbnail, lazyVideo);
    }
    
    // Inicializar thumbnails quando a página carregar
    initializeVideoThumbnails();
    
    // --- ANIMAÇÕES DE HABILIDADES E CONDIÇÕES ---
    
    // Função otimizada para animar habilidades (versão mais leve)
    function animateHabilidades() {
        const habilidades = document.querySelectorAll('.habilidade-item');
        
        // Animação mais simples e eficiente
        habilidades.forEach((habilidade, index) => {
            habilidade.style.opacity = '0';
            habilidade.style.transform = 'translateY(10px)';
            habilidade.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            
            setTimeout(() => {
                habilidade.style.opacity = '1';
                habilidade.style.transform = 'translateY(0)';
            }, index * 100); // Delay reduzido
        });
    }
    
    // Selecionar elementos de habilidades para animações
    const habilidadesTyping = document.getElementById('habilidadesTyping');
    const habilidadesItems = document.querySelectorAll('.habilidade-item');
    
    // Inicializar animações quando a página carregar
    setTimeout(() => {
        animateHabilidades();
    }, 500);
    
    // --- PROGRESSO E ANIMAÇÃO DOS CARDS ---
    const projCheckboxes = document.querySelectorAll('.proj-checkbox');
    const imobCheckboxes = document.querySelectorAll('.imob-checkbox');
    const chaveCheckboxes = document.querySelectorAll('.chave-checkbox');
    const estrangCheckboxes = document.querySelectorAll('.estrang-checkbox');
    const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
    const kaeshiWazaCheckboxes = document.querySelectorAll('.kaeshi-waza-checkbox');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    let hasShownCongratulations = false;
    
    // Função otimizada para atualizar progresso
    function updateProgress() {
        // Calcular progresso de forma mais eficiente
        const checkboxTypes = [
            { selector: '.proj-checkbox', elements: projCheckboxes },
            { selector: '.imob-checkbox', elements: imobCheckboxes },
            { selector: '.chave-checkbox', elements: chaveCheckboxes },
            { selector: '.estrang-checkbox', elements: estrangCheckboxes },
            { selector: '.henkakuenka-checkbox', elements: henkakuenkaCheckboxes },
            { selector: '.kaeshi-waza-checkbox', elements: kaeshiWazaCheckboxes }
        ];
        
        let totalQuestions = 0;
        let completedQuestions = 0;
        let allChecked = true;
        
        checkboxTypes.forEach(type => {
            const checked = document.querySelectorAll(`${type.selector}:checked`).length;
            totalQuestions += type.elements.length;
            completedQuestions += checked;
            
            // Verificar se todos estão marcados
            if (checked !== type.elements.length) {
                allChecked = false;
            }
        });
        
        const progress = (completedQuestions / totalQuestions) * 100;
        
        // Atualizar barra de progresso
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        // Mostrar barra de progresso flutuante
        showFloatingProgress(progress);
        
        // Verificar se chegou a 100% e mostrar parabéns (verificação única)
        if (progress >= 100 && allChecked && !hasShownCongratulations) {
            console.log('Progress is 100% - showing congratulations!');
            setTimeout(() => {
                showCongratulations();
            }, 500);
        }
    }

    // Função para mostrar barra de progresso flutuante
    function showFloatingProgress(progress) {
        // Atualizar valores da barra flutuante
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = Math.round(progress) + '%';
        
        // Mostrar a barra
        floatingProgress.style.opacity = '1';
        floatingProgress.style.pointerEvents = 'auto';
        
        // Esconder após 5 segundos
        setTimeout(() => {
            floatingProgress.style.opacity = '0';
            floatingProgress.style.pointerEvents = 'none';
        }, 5000);
    }
    
    // Função centralizada para adicionar event listeners
    function addCheckboxListeners() {
        const allCheckboxes = [
            ...projCheckboxes,
            ...imobCheckboxes,
            ...chaveCheckboxes,
            ...estrangCheckboxes,
            ...henkakuenkaCheckboxes,
            ...kaeshiWazaCheckboxes
        ];
        
        allCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateProgress);
        });
    }
    
    // Inicializar listeners e progresso
    addCheckboxListeners();
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

    // Botão voltar ao topo
    const backToTopBtn = document.getElementById('backToTop');
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.remove('hidden');
        } else {
            backToTopBtn.classList.add('hidden');
        }
    });
    // Sistema de partículas otimizado (reutiliza elementos)
    const particlePool = [];
    const maxParticles = 20;
    
    // Criar pool de partículas reutilizáveis
    function createParticlePool() {
        for (let i = 0; i < maxParticles; i++) {
            const particle = document.createElement('div');
            particle.className = 'back-to-top-particle';
            particle.style.position = 'fixed';
            particle.style.width = '8px';
            particle.style.height = '8px';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = 9999;
            particle.style.opacity = '0';
            particle.style.transition = 'opacity 0.6s ease';
            document.body.appendChild(particle);
            particlePool.push(particle);
        }
    }
    
    // Função otimizada para criar partículas
    function createBackToTopParticles(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const particleCount = Math.min(8, particlePool.length); // Reduzido de 12 para 8
        
        for (let i = 0; i < particleCount; i++) {
            const particle = particlePool[i];
            if (particle) {
                particle.style.left = centerX + (Math.random() - 0.5) * 40 + 'px';
                particle.style.top = centerY + (Math.random() - 0.5) * 40 + 'px';
                particle.style.background = `rgba(255, 255, 255, ${0.6 + Math.random() * 0.4})`;
                particle.style.opacity = '1';
                
                setTimeout(() => {
                    particle.style.opacity = '0';
                }, 600);
            }
        }
    }
    
    // Inicializar pool de partículas
    createParticlePool();
    // Handler otimizado para o botão voltar ao topo
    function backToTopHandler() {
        createBackToTopParticles(this);
        this.style.transform = 'scale(0.95)';
        this.style.transition = 'transform 0.1s ease';
        
        // Scroll otimizado usando scrollTo nativo
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        
        // Resetar transformação
        setTimeout(() => {
            this.style.transform = 'scale(1)';
            this.style.transition = 'transform 0.2s ease';
        }, 200);
    }
    // Inicializar botão flutuante
    backToTopBtn.removeEventListener('click', backToTopHandler);
    backToTopBtn.addEventListener('click', backToTopHandler);

    // Animação otimizada para as divs de navegação japonesa
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(10px)';
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + (index * 50)); // Delay reduzido
    });
    
    // Sistema de partículas para navegação otimizado
    const navParticlePool = [];
    const maxNavParticles = 15;
    
    // Criar pool de partículas para navegação
    function createNavParticlePool() {
        const particlesContainer = document.getElementById('scrollParticles');
        if (!particlesContainer) return;
        
        for (let i = 0; i < maxNavParticles; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.position = 'absolute';
            particle.style.width = '6px';
            particle.style.height = '6px';
            particle.style.background = 'linear-gradient(45deg, #22c55e, #15803d)';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '9999';
            particle.style.opacity = '0';
            particle.style.transition = 'opacity 0.8s ease';
            particlesContainer.appendChild(particle);
            navParticlePool.push(particle);
        }
    }
    
    // Função otimizada para criar partículas de navegação
    function createParticles(x, y, count = 6) {
        const particleCount = Math.min(count, navParticlePool.length);
        
        for (let i = 0; i < particleCount; i++) {
            const particle = navParticlePool[i];
            if (particle) {
                particle.style.left = x + Math.random() * 30 - 15 + 'px';
                particle.style.top = y + Math.random() * 30 - 15 + 'px';
                particle.style.opacity = '1';
                
                setTimeout(() => {
                    particle.style.opacity = '0';
                }, 1000);
            }
        }
    }
    
    // Inicializar pool de partículas de navegação
    createNavParticlePool();

    // Navegação interna
    const nageWazaNav = document.getElementById('nage-waza-nav');
    const imobilizacoesNav = document.getElementById('imobilizacoes-nav');
    const chaveBracoNav = document.getElementById('chave-braco-nav');
    const estrangulamentoNav = document.getElementById('estrangulamento-nav');
    const henkakuenkaNav = document.getElementById('henkakuenka-nav');
    const kaeshiWazaNav = document.getElementById('kaeshi-waza-nav');
    
    const nageWazaSection = document.getElementById('nage-waza-section');
    const imobilizacoesSection = document.getElementById('imobilizacoes-section');
    const chaveBracoSection = document.getElementById('chave-braco-section');
    const estrangulamentoSection = document.getElementById('estrangulamento-section');
    const henkakuenkaSection = document.getElementById('henkakuenka-section');
    const kaeshiWazaSection = document.getElementById('kaeshi-waza-section');

    // Função centralizada para navegação
    function setupNavigation() {
        const navItems = [
            { nav: nageWazaNav, section: nageWazaSection, sectionId: 'nage-waza-section' },
            { nav: imobilizacoesNav, section: imobilizacoesSection, sectionId: 'imobilizacoes-section' },
            { nav: chaveBracoNav, section: chaveBracoSection, sectionId: 'chave-braco-section' },
            { nav: estrangulamentoNav, section: estrangulamentoSection, sectionId: 'estrangulamento-section' },
            { nav: henkakuenkaNav, section: henkakuenkaSection, sectionId: 'henkakuenka-section' },
            { nav: kaeshiWazaNav, section: kaeshiWazaSection, sectionId: 'kaeshi-waza-section' }
        ];
        
        navItems.forEach(item => {
            if (item.nav && item.section) {
                item.nav.addEventListener('click', function(e) {
                    hideAllSections();
                    showSectionWithAnimation(item.section);
                    setTimeout(() => smoothScrollToSection(item.sectionId, this), 300);
                });
            }
        });
    }
    
    // Inicializar navegação
    setupNavigation();

    // --- SISTEMA DE CARROSSÉIS OTIMIZADO ---
    // Função reutilizável para inicializar carrosséis
    function initializeCarousel(carouselId, leftBtnId, rightBtnId) {
        const carousel = document.getElementById(carouselId);
        const leftBtn = document.getElementById(leftBtnId);
        const rightBtn = document.getElementById(rightBtnId);
        
        if (!carousel || !leftBtn || !rightBtn) return;
        
        // Função para animar botão
        function animateButton(btn) {
            btn.classList.add('carousel-arrow-anim');
            setTimeout(() => btn.classList.remove('carousel-arrow-anim'), 700);
        }
        
        // Event listeners otimizados
        leftBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: -carousel.offsetWidth * 0.8, behavior: 'smooth' });
            animateButton(leftBtn);
        });
        
        rightBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: carousel.offsetWidth * 0.8, behavior: 'smooth' });
            animateButton(rightBtn);
        });
    }
    
    // Inicializar todos os carrosséis
    initializeCarousel('carouselProj', 'carouselLeft', 'carouselRight');
    initializeCarousel('carouselImob', 'carouselImobLeft', 'carouselImobRight');
    initializeCarousel('carouselChave', 'carouselChaveLeft', 'carouselChaveRight');
    initializeCarousel('carouselEstrang', 'carouselEstrangLeft', 'carouselEstrangRight');

    function hideAllSections() {
      nageWazaSection.classList.add('hidden');
      imobilizacoesSection.classList.add('hidden');
      chaveBracoSection.classList.add('hidden');
      estrangulamentoSection.classList.add('hidden');
      if (henkakuenkaSection) henkakuenkaSection.classList.add('hidden');
      if (kaeshiWazaSection) kaeshiWazaSection.classList.add('hidden');
    }
    function showSectionWithAnimation(section) {
      section.classList.remove('hidden');
      section.classList.add('animate-fade-in');
      setTimeout(() => section.classList.remove('animate-fade-in'), 1300);
    }
    function smoothScrollToSection(sectionId, cardElement) {
        const targetElement = document.getElementById(sectionId);
        if (!targetElement) return;
        cardElement.classList.add('clicked');
        
        // Criar partículas no ponto de clique (otimizado)
        const rect = cardElement.getBoundingClientRect();
        createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2, 4); // Reduzido de 8 para 4
        
        // Scroll suave otimizado usando scrollTo nativo
        const targetPosition = targetElement.offsetTop - 100;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
        
        // Limpar classes após animação
        setTimeout(() => {
            cardElement.classList.remove('clicked');
            targetElement.classList.add('destination-highlight');
            setTimeout(() => {
                targetElement.classList.remove('destination-highlight');
            }, 1500); // Reduzido de 2000 para 1500
        }, 800); // Reduzido de 300 para 800
    }
    // Inicializar botões das seções (otimizado - sem loop infinito)
    function initializeBackToTopSectionButtons() {
        document.querySelectorAll('.back-to-top-section').forEach(button => {
            if (!button.hasAttribute('data-initialized')) {
                button.removeEventListener('click', backToTopHandler);
                button.classList.add('animate-in');
                button.addEventListener('click', backToTopHandler);
                button.setAttribute('data-initialized', 'true');
            }
        });
    }
    initializeBackToTopSectionButtons();
});
 // Sistema de lazy loading para vídeos
 class LazyVideoLoader {
    constructor() {
        this.loadedVideos = new Set();
        this.init();
    }
    
    init() {
        // Converter todos os iframes existentes para lazy loading
        this.convertExistingVideos();
        
        // Carregar vídeos visíveis na tela
        this.loadVisibleVideos();
        
        // Observer para carregar vídeos quando ficarem visíveis
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadVideo(entry.target);
                    }
                });
            }, {
                rootMargin: '100px 0px', // Carregar 100px antes de ficar visível
                threshold: 0.1
            });
            
            document.querySelectorAll('.lazy-video').forEach(video => {
                this.observer.observe(video);
            });
        }
        
        // Fallback: carregar ao clicar
        document.addEventListener('click', (e) => {
            const lazyVideo = e.target.closest('.lazy-video');
            if (lazyVideo && !lazyVideo.classList.contains('loaded')) {
                this.loadVideo(lazyVideo);
            }
        });
    }
    
    convertExistingVideos() {
        const iframes = document.querySelectorAll('iframe[src*="youtube.com"]');
        iframes.forEach(iframe => {
            const container = iframe.parentElement;
            const src = iframe.src;
            const title = iframe.title;
            
            // Criar estrutura lazy
            const lazyDiv = document.createElement('div');
            lazyDiv.className = 'lazy-video';
            lazyDiv.dataset.src = src;
            lazyDiv.dataset.title = title;
            
            const placeholder = document.createElement('div');
            placeholder.className = 'video-placeholder bg-gray-200 rounded-lg flex items-center justify-center h-full';
            placeholder.innerHTML = `
                <div class="text-center">
                    <div class="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-2">
                        <svg class="w-8 h-8 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M8 5v14l11-7z"/>
                        </svg>
                    </div>
                    <p class="text-gray-600 text-sm">Clique para carregar vídeo</p>
                </div>
            `;
            
            lazyDiv.appendChild(placeholder);
            container.replaceChild(lazyDiv, iframe);
        });
    }
    
    loadVisibleVideos() {
        document.querySelectorAll('.lazy-video:not(.loaded)').forEach(video => {
            const rect = video.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight + 200 && rect.bottom > -200;
            
            if (isVisible) {
                this.loadVideo(video);
            }
        });
    }
    
    loadVideo(videoElement) {
        if (this.loadedVideos.has(videoElement)) return;
        
        const src = videoElement.dataset.src;
        const title = videoElement.dataset.title;
        
        if (!src) return;
        
        // Criar iframe
        const iframe = document.createElement('iframe');
        iframe.src = src;
        iframe.title = title;
        iframe.frameBorder = '0';
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        iframe.referrerPolicy = 'strict-origin-when-cross-origin';
        iframe.allowFullscreen = true;
        
        // Adicionar iframe ao container
        videoElement.appendChild(iframe);
        videoElement.classList.add('loaded');
        
        // Marcar como carregado
        this.loadedVideos.add(videoElement);
        
        // Parar de observar este vídeo
        if (this.observer) {
            this.observer.unobserve(videoElement);
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new LazyVideoLoader();
});

// Otimização para mobile: carregar apenas vídeos próximos ao scroll
let scrollTimeout;
window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        const videos = document.querySelectorAll('.lazy-video:not(.loaded)');
        videos.forEach(video => {
            const rect = video.getBoundingClientRect();
            const distance = Math.abs(rect.top - window.innerHeight);
            
            // Carregar se estiver próximo (300px) do viewport
            if (distance < 300) {
                const loader = new LazyVideoLoader();
                loader.loadVideo(video);
            }
        });
    }, 150); // Debounce de 150ms
});