document.addEventListener('DOMContentLoaded', function() {
    // --- ANIMAÇÕES DE HABILIDADES E CONDIÇÕES ---
    
    // Função para animar habilidades com efeito de digitação
    function animateHabilidades() {
        const habilidades = document.querySelectorAll('.habilidade-item');
        
        // Todas as habilidades animam ao mesmo tempo
        habilidades.forEach((habilidade, index) => {
            setTimeout(() => {
                habilidade.style.opacity = '0';
                habilidade.style.transform = 'translateY(20px) scale(0.9)';
                habilidade.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                
                setTimeout(() => {
                    habilidade.style.opacity = '1';
                    habilidade.style.transform = 'translateY(0) scale(1)';
                }, 100);
            }, index * 150); // Delay escalonado para cada habilidade
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
    const ataquesCombinadosCheckboxes = document.querySelectorAll('.ataques-combinados-checkbox');
    const contraAtaquesCheckboxes = document.querySelectorAll('.contra-ataques-checkbox');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    let hasShownCongratulations = false;
    // Função otimizada para atualizar progresso
    function updateProgress() {
        const checkboxTypes = [
            { selector: '.proj-checkbox:checked', total: projCheckboxes.length },
            { selector: '.imob-checkbox:checked', total: imobCheckboxes.length },
            { selector: '.chave-checkbox:checked', total: chaveCheckboxes.length },
            { selector: '.estrang-checkbox:checked', total: estrangCheckboxes.length },
            { selector: '.ataques-combinados-checkbox:checked', total: ataquesCombinadosCheckboxes.length },
            { selector: '.contra-ataques-checkbox:checked', total: contraAtaquesCheckboxes.length }
        ];
        
        let completedQuestions = 0;
        let totalQuestions = 0;
        let allChecked = true;
        
        checkboxTypes.forEach(type => {
            const checked = document.querySelectorAll(type.selector).length;
            completedQuestions += checked;
            totalQuestions += type.total;
            if (checked < type.total) allChecked = false;
        });
        
        const progress = (completedQuestions / totalQuestions) * 100;
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        // Verificar se chegou a 100% e mostrar parabéns
        if (progress >= 100 && allChecked && !hasShownCongratulations) {
            setTimeout(() => showCongratulations(), 500);
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
    // Função otimizada para adicionar event listeners aos checkboxes
    function addCheckboxListeners(checkboxes) {
        checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                    // Calcular progresso atual para mostrar na barra flutuante
                    const checkboxTypes = [
                        { selector: '.proj-checkbox:checked', total: projCheckboxes.length },
                        { selector: '.imob-checkbox:checked', total: imobCheckboxes.length },
                        { selector: '.chave-checkbox:checked', total: chaveCheckboxes.length },
                        { selector: '.estrang-checkbox:checked', total: estrangCheckboxes.length },
                        { selector: '.ataques-combinados-checkbox:checked', total: ataquesCombinadosCheckboxes.length },
                        { selector: '.contra-ataques-checkbox:checked', total: contraAtaquesCheckboxes.length }
                    ];
                    
                    let completed = 0;
                    let total = 0;
                    checkboxTypes.forEach(type => {
                        completed += document.querySelectorAll(type.selector).length;
                        total += type.total;
                    });
                    
                    showFloatingProgress((completed / total) * 100);
            }
        });
    });
    }
    
    // Adicionar listeners para todos os tipos de checkbox
    addCheckboxListeners(projCheckboxes);
    addCheckboxListeners(imobCheckboxes);
    addCheckboxListeners(chaveCheckboxes);
    addCheckboxListeners(estrangCheckboxes);
    addCheckboxListeners(ataquesCombinadosCheckboxes);
    addCheckboxListeners(contraAtaquesCheckboxes);

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
    
    // Pool de partículas para melhor performance
    const particlePool = [];
    const maxParticles = 20;
    
    // Função otimizada para criar partículas
    function createBackToTopParticles(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Reutilizar partículas do pool ou criar novas
        for (let i = 0; i < 8; i++) {
            let particle = particlePool.pop();
            if (!particle) {
                particle = document.createElement('div');
            particle.className = 'back-to-top-particle';
            particle.style.position = 'fixed';
                particle.style.width = '8px';
                particle.style.height = '8px';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = 9999;
                particle.style.transition = 'opacity 0.6s ease';
            document.body.appendChild(particle);
            }
            
            particle.style.left = centerX + (Math.random() - 0.5) * 40 + 'px';
            particle.style.top = centerY + (Math.random() - 0.5) * 40 + 'px';
            particle.style.background = `rgba(255, 255, 255, ${0.6 + Math.random() * 0.4})`;
            particle.style.opacity = '1';
            
            setTimeout(() => {
                particle.style.opacity = '0';
                setTimeout(() => {
                    if (particlePool.length < maxParticles) {
                        particlePool.push(particle);
                    } else if (particle.parentNode) {
                        particle.parentNode.removeChild(particle);
                    }
                }, 600);
            }, 600);
        }
    }
    
    // Handler otimizado para o botão voltar ao topo
    function backToTopHandler() {
        const button = this;
        createBackToTopParticles(button);
        button.style.transform = 'scale(0.95)';
        button.style.transition = 'transform 0.1s ease';
        
        // Usar scroll nativo do browser para melhor performance
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
                setTimeout(() => {
                    button.style.transform = 'scale(1)';
                    button.style.transition = 'transform 0.3s ease';
                }, 100);
    }
    
    // Inicializar botão flutuante
    backToTopBtn.removeEventListener('click', backToTopHandler);
    backToTopBtn.addEventListener('click', backToTopHandler);

    // Animação para as divs de navegação japonesa
    document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + (index * 100)); // Delay escalonado para cada card
    });

    // Navegação interna
    const nageWazaNav = document.getElementById('nage-waza-nav');
    const imobilizacoesNav = document.getElementById('imobilizacoes-nav');
    const chaveBracoNav = document.getElementById('chave-braco-nav');
    const estrangulamentoNav = document.getElementById('estrangulamento-nav');
    const ataquesCombinadosNav = document.getElementById('ataques-combinados-nav');
    const contraAtaquesNav = document.getElementById('contra-ataques-nav');
    
    const nageWazaSection = document.getElementById('nage-waza-section');
    const imobilizacoesSection = document.getElementById('imobilizacoes-section');
    const chaveBracoSection = document.getElementById('chave-braco-section');
    const estrangulamentoSection = document.getElementById('estrangulamento-section');
    const ataquesCombinadosSection = document.getElementById('ataques-combinados-section');
    const contraAtaquesSection = document.getElementById('contra-ataques-section');

    function hideAllSections() {
        nageWazaSection.classList.add('hidden');
        imobilizacoesSection.classList.add('hidden');
        chaveBracoSection.classList.add('hidden');
        estrangulamentoSection.classList.add('hidden');
        ataquesCombinadosSection.classList.add('hidden');
        contraAtaquesSection.classList.add('hidden');
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
        
        // Usar scroll nativo para melhor performance
        const targetPosition = targetElement.offsetTop - 100;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
        
                setTimeout(() => {
                    cardElement.classList.remove('clicked');
                    targetElement.classList.add('destination-highlight');
                    setTimeout(() => {
                        targetElement.classList.remove('destination-highlight');
                    }, 2000);
        }, 800);
    }

    if (nageWazaNav && nageWazaSection) {
        nageWazaNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(nageWazaSection);
            setTimeout(() => smoothScrollToSection('nage-waza-section', this), 300);
        });
    }

    if (imobilizacoesNav && imobilizacoesSection) {
        imobilizacoesNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(imobilizacoesSection);
            setTimeout(() => smoothScrollToSection('imobilizacoes-section', this), 300);
        });
    }

    if (chaveBracoNav && chaveBracoSection) {
        chaveBracoNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(chaveBracoSection);
            setTimeout(() => smoothScrollToSection('chave-braco-section', this), 300);
        });
    }

    if (estrangulamentoNav && estrangulamentoSection) {
        estrangulamentoNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(estrangulamentoSection);
            setTimeout(() => smoothScrollToSection('estrangulamento-section', this), 300);
        });
    }





    if (ataquesCombinadosNav && ataquesCombinadosSection) {
        ataquesCombinadosNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(ataquesCombinadosSection);
            setTimeout(() => smoothScrollToSection('ataques-combinados-section', this), 300);
        });
    }

    if (contraAtaquesNav && contraAtaquesSection) {
        contraAtaquesNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(contraAtaquesSection);
            setTimeout(() => smoothScrollToSection('contra-ataques-section', this), 300);
        });
    }

    // Inicializar botões de voltar ao topo das seções (otimizado)
    function initializeBackToTopSectionButtons() {
        document.querySelectorAll('.back-to-top-section').forEach(button => {
            if (!button.hasAttribute('data-initialized')) {
                button.addEventListener('click', backToTopHandler);
                button.setAttribute('data-initialized', 'true');
            }
        });
    }
    initializeBackToTopSectionButtons();

    // Função reutilizável para inicializar carrosséis
    function initializeCarousel(carouselId, leftBtnId, rightBtnId, scrollAmount = 0.8) {
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
            carousel.scrollBy({ left: -carousel.offsetWidth * scrollAmount, behavior: 'smooth' });
            animateButton(leftBtn);
        });
        
        rightBtn.addEventListener('click', () => {
            carousel.scrollBy({ left: carousel.offsetWidth * scrollAmount, behavior: 'smooth' });
            animateButton(rightBtn);
        });
    }
    
    // Inicializar todos os carrosséis
    initializeCarousel('carouselProj', 'carouselLeft', 'carouselRight');
    initializeCarousel('carouselImob', 'carouselImobLeft', 'carouselImobRight', 0.6);
    initializeCarousel('carouselChave', 'carouselChaveLeft', 'carouselChaveRight');
    initializeCarousel('carouselEstrang', 'carouselEstrangLeft', 'carouselEstrangRight');

    // --- SISTEMA DE LAZY LOADING AUTOMÁTICO ---
    function setupLazyVideos() {
        console.log('Configurando lazy loading...');
        
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
    
    // TESTE: Carregar vídeos imediatamente para debug
    setTimeout(() => {
        const videos = document.querySelectorAll('iframe[src*="youtube.com"]');
        console.log('🔍 TESTE: Vídeos encontrados:', videos.length);
        
        if (videos.length > 0) {
            console.log('✅ Vídeos estão sendo encontrados pelo JavaScript');
            videos.forEach((video, index) => {
                console.log(`Vídeo ${index + 1}:`, video.src);
            });
        } else {
            console.log('❌ Nenhum vídeo encontrado - problema na seleção');
        }
    }, 2000);
    
    // Inicializar lazy loading
    setupLazyVideos();

});