document.addEventListener('DOMContentLoaded', function() {
    // ===== NAVEGAÇÃO JAPONESA =====
    const nageWazaNav = document.getElementById('nage-waza-nav');
    const imobilizacoesNav = document.getElementById('imobilizacoes-nav');
    const chaveBracoNav = document.getElementById('chave-braco-nav');
    const estrangulamentoNav = document.getElementById('estrangulamento-nav');
    const ataqueCombinadoNav = document.getElementById('ataque-combinado-nav');
    const contraAtaqueNav = document.getElementById('contra-ataque-nav');
    const nageWazaSection = document.getElementById('nage-waza-section');
    const imobilizacoesSection = document.getElementById('imobilizacoes-section');
    const chaveBracoSection = document.getElementById('chave-braco-section');
    const estrangulamentoSection = document.getElementById('estrangulamento-section');
    const ataqueCombinadoSection = document.getElementById('ataque-combinado-section');
    const contraAtaqueSection = document.getElementById('contra-ataque-section');
    const navs = [nageWazaNav, imobilizacoesNav, chaveBracoNav, estrangulamentoNav, ataqueCombinadoNav, contraAtaqueNav];
    
    function hideAllSections() {
        nageWazaSection.classList.add('hidden');
        imobilizacoesSection.classList.add('hidden');
        chaveBracoSection.classList.add('hidden');
        estrangulamentoSection.classList.add('hidden');
        ataqueCombinadoSection.classList.add('hidden');
        contraAtaqueSection.classList.add('hidden');
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
        // Calcular posição de destino
        const targetPosition = targetElement.offsetTop - 100;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 1200;
        let start = null;
        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }
        function animation(currentTime) {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const progress = Math.min(timeElapsed / duration, 1);
            const easedProgress = easeInOutCubic(progress);
            window.scrollTo(0, startPosition + distance * easedProgress);
            if (progress < 1) {
                requestAnimationFrame(animation);
            } else {
                setTimeout(() => {
                    cardElement.classList.remove('clicked');
                    targetElement.classList.add('destination-highlight');
                    setTimeout(() => {
                        targetElement.classList.remove('destination-highlight');
                    }, 2000);
                }, 300);
            }
        }
        requestAnimationFrame(animation);
    }
    
    function removeClickedFromAll() {
        navs.forEach(nav => nav && nav.classList.remove('clicked'));
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
    
    if (ataqueCombinadoNav && ataqueCombinadoSection) {
        ataqueCombinadoNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(ataqueCombinadoSection);
            setTimeout(() => smoothScrollToSection('ataque-combinado-section', this), 300);
        });
    }
    
    if (contraAtaqueNav && contraAtaqueSection) {
        contraAtaqueNav.addEventListener('click', function(e) {
            hideAllSections();
            showSectionWithAnimation(contraAtaqueSection);
            setTimeout(() => smoothScrollToSection('contra-ataque-section', this), 300);
        });
    }

    // ===== CARROSSEIS =====
    
    // Função genérica para configurar carrossel
    function setupCarousel(carouselId, leftBtnId, rightBtnId) {
        const carousel = document.getElementById(carouselId);
        const leftBtn = document.getElementById(leftBtnId);
        const rightBtn = document.getElementById(rightBtnId);
        
        console.log(`Configurando carrossel: ${carouselId}`, { carousel, leftBtn, rightBtn });
        
        if (!carousel || !leftBtn || !rightBtn) {
            console.log(`Elementos não encontrados para: ${carouselId}`);
            return;
        }
        
        // Função para rolar
        function scrollCarousel(direction) {
            const scrollAmount = carousel.offsetWidth * 0.8;
            carousel.scrollBy({ 
                left: direction === 'left' ? -scrollAmount : scrollAmount, 
                behavior: 'smooth' 
            });
            
            // Animação da seta clicada usando Tailwind
            const clickedBtn = direction === 'left' ? leftBtn : rightBtn;
            clickedBtn.classList.add('scale-110', 'transition-transform', 'duration-200');
            setTimeout(() => {
                clickedBtn.classList.remove('scale-110', 'transition-transform', 'duration-200');
            }, 200);
        }
        
        // Event listeners
        leftBtn.addEventListener('click', () => {
            console.log(`Clicou na seta esquerda do ${carouselId}`);
            scrollCarousel('left');
        });
        rightBtn.addEventListener('click', () => {
            console.log(`Clicou na seta direita do ${carouselId}`);
            scrollCarousel('right');
        });
        
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
    console.log('Configurando carrosséis...');
    setupCarousel('carouselProj', 'carouselLeft', 'carouselRight');
    setupCarousel('carouselImob', 'imobLeft', 'imobRight');
    setupCarousel('carouselChave', 'carouselChaveLeft', 'carouselChaveRight');
    setupCarousel('carouselEstrang', 'carouselEstrangLeft', 'carouselEstrangRight');
    setupCarousel('carouselAtaqueCombinado', 'carouselAtaqueCombinadoLeft', 'carouselAtaqueCombinadoRight');
    setupCarousel('carouselContraAtaque', 'carouselContraAtaqueLeft', 'carouselContraAtaqueRight');
    console.log('Carrosséis configurados!');
    
    // ===== PROGRESSO =====
    const projCheckboxes = document.querySelectorAll('.proj-checkbox');
    const imobCheckboxes = document.querySelectorAll('.imob-checkbox');
    const chaveCheckboxes = document.querySelectorAll('.chave-checkbox');
    const estrangCheckboxes = document.querySelectorAll('.estrang-checkbox');
    const ataqueCombinadoCheckboxes = document.querySelectorAll('.ataque-combinado-checkbox');
    const contraAtaqueCheckboxes = document.querySelectorAll('.contra-ataque-checkbox');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    let hasShownCongratulations = false;
    
    function updateProgress() {
        const totalProjChecked = document.querySelectorAll('.proj-checkbox:checked').length;
        const totalImobChecked = document.querySelectorAll('.imob-checkbox:checked').length;
        const totalChaveChecked = document.querySelectorAll('.chave-checkbox:checked').length;
        const totalEstrangChecked = document.querySelectorAll('.estrang-checkbox:checked').length;
        const totalAtaqueCombinadoChecked = document.querySelectorAll('.ataque-combinado-checkbox:checked').length;
        const totalContraAtaqueChecked = document.querySelectorAll('.contra-ataque-checkbox:checked').length;
        const totalQuestions = projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataqueCombinadoCheckboxes.length + contraAtaqueCheckboxes.length;
        const completedQuestions = totalProjChecked + totalImobChecked + totalChaveChecked + totalEstrangChecked + totalAtaqueCombinadoChecked + totalContraAtaqueChecked;
        const progress = (completedQuestions / totalQuestions) * 100;
        
        console.log('=== DEBUG PROGRESS ===');
        console.log('Proj checked:', totalProjChecked, '/', projCheckboxes.length);
        console.log('Imob checked:', totalImobChecked, '/', imobCheckboxes.length);
        console.log('Chave checked:', totalChaveChecked, '/', chaveCheckboxes.length);
        console.log('Estrang checked:', totalEstrangChecked, '/', estrangCheckboxes.length);
        console.log('Ataque Combinado checked:', totalAtaqueCombinadoChecked, '/', ataqueCombinadoCheckboxes.length);
        console.log('Contra Ataque checked:', totalContraAtaqueChecked, '/', contraAtaqueCheckboxes.length);
        console.log('Total completed:', completedQuestions, '/', totalQuestions);
        console.log('Progress:', progress + '%');
        console.log('Has shown congratulations:', hasShownCongratulations);
        console.log('=== END DEBUG ===');
        
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        // Verificar se chegou a 100% e mostrar parabéns
        if (progress >= 100 && !hasShownCongratulations) {
            console.log('Progress is 100% - checking for congratulations');
            
            // Verificar se todos os checkboxes estão marcados
            const allChecked = Array.from(projCheckboxes).every(cb => cb.checked) && 
                             Array.from(imobCheckboxes).every(cb => cb.checked) &&
                             Array.from(chaveCheckboxes).every(cb => cb.checked) &&
                             Array.from(estrangCheckboxes).every(cb => cb.checked) &&
                             Array.from(ataqueCombinadoCheckboxes).every(cb => cb.checked) &&
                             Array.from(contraAtaqueCheckboxes).every(cb => cb.checked);
            
            if (allChecked) {
                console.log('Showing congratulations!');
                setTimeout(() => {
                    showCongratulations();
                }, 500);
            }
        }
        
        // Verificação adicional: se todos os checkboxes estão marcados, mostrar parabéns
        if (completedQuestions >= 75 && !hasShownCongratulations) {
            console.log('Todos os 75 checkboxes marcados - mostrando parabéns!');
            setTimeout(() => {
                showCongratulations();
            }, 500);
        }
        
        // Mostrar barra de progresso flutuante
        showFloatingProgress(progress);
    }
    
    function showFloatingProgress(progress) {
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = Math.round(progress) + '%';
        
        floatingProgress.classList.remove('opacity-0', 'pointer-events-none');
        floatingProgress.classList.add('opacity-100');
        
        setTimeout(() => {
            floatingProgress.classList.remove('opacity-100');
            floatingProgress.classList.add('opacity-0', 'pointer-events-none');
        }, 5000);
    }
    
    // Event listeners para checkboxes
    console.log('=== DEBUG CHECKBOXES ===');
    console.log('Proj checkboxes encontrados:', projCheckboxes.length);
    console.log('Imob checkboxes encontrados:', imobCheckboxes.length);
    console.log('Chave checkboxes encontrados:', chaveCheckboxes.length);
    console.log('Estrang checkboxes encontrados:', estrangCheckboxes.length);
    console.log('Ataque Combinado checkboxes encontrados:', ataqueCombinadoCheckboxes.length);
    console.log('Contra Ataque checkboxes encontrados:', contraAtaqueCheckboxes.length);
    console.log('=== FIM DEBUG CHECKBOXES ===');
    
    projCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    imobCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    chaveCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    estrangCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    ataqueCombinadoCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    contraAtaqueCheckboxes.forEach(checkbox => checkbox.addEventListener('change', updateProgress));
    
    // Inicializar progresso
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
    
    // Handler para o botão voltar ao topo
    function backToTopHandler() {
        const button = this;
        createBackToTopParticles(button);
        button.style.transform = 'scale(0.95)';
        button.style.transition = 'transform 0.1s ease';
        const startPosition = window.pageYOffset;
        const duration = 1000;
        let start = null;
        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
        }
        function animation(currentTime) {
            if (start === null) start = currentTime;
            const timeElapsed = currentTime - start;
            const progress = Math.min(timeElapsed / duration, 1);
            const easedProgress = easeInOutCubic(progress);
            window.scrollTo(0, startPosition * (1 - easedProgress));
            if (progress < 1) {
                requestAnimationFrame(animation);
            } else {
                setTimeout(() => {
                    button.style.transform = 'scale(1)';
                    button.style.transition = 'transform 0.3s ease';
                }, 100);
            }
        }
        requestAnimationFrame(animation);
    }
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.remove('hidden');
        } else {
            backToTopBtn.classList.add('hidden');
        }
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
    setInterval(() => {
        const buttons = document.querySelectorAll('.back-to-top-section');
        const uninitializedButtons = Array.from(buttons).filter(button => {
            return !button.hasAttribute('data-initialized');
        });
        if (uninitializedButtons.length > 0) {
            initializeBackToTopSectionButtons();
        }
    }, 2000);
    
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
});