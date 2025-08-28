document.addEventListener('DOMContentLoaded', function() {
    // --- FUNÇÃO PARA MOSTRAR/ESCONDER SEÇÕES ---
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
        
        // Mostrar a seção selecionada
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.remove('hidden');
            
            // Scroll suave para a seção
            targetSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }
    };
    
    // --- DETECÇÃO DE DISPOSITIVO MÓVEL ---
    let isMobile = window.innerWidth <= 768;
    
    // Função para atualizar estado mobile quando a tela é redimensionada
    function updateMobileState() {
        const wasMobile = isMobile;
        isMobile = window.innerWidth <= 768;
        
        // Se mudou de desktop para mobile, desabilitar animações
        if (wasMobile !== isMobile && isMobile) {
            console.log('Mudou para mobile - desabilitando animações');
            disableMobileAnimations();
        }
        // Se mudou de mobile para desktop, reabilitar animações
        else if (wasMobile !== isMobile && !isMobile) {
            console.log('Mudou para desktop - reabilitando animações');
            enableDesktopAnimations();
        }
    }
    
    // Função para desabilitar animações em mobile
    function disableMobileAnimations() {
        // Remover classes de animação ativas
        document.querySelectorAll('.carousel-arrow-anim').forEach(el => {
            el.classList.remove('carousel-arrow-anim');
        });
        
        // Resetar transformações
        document.querySelectorAll('.japanese-nav-card, .habilidade-item').forEach(el => {
            el.style.transform = 'none';
            el.style.opacity = '1';
        });
    }
    
    // Função para reabilitar animações em desktop
    function enableDesktopAnimations() {
        // Reabilitar animações de entrada se necessário
        if (document.readyState === 'complete') {
            document.querySelectorAll('.japanese-nav-card').forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 200 + (index * 100));
            });
        }
    }
    
    // Listener para mudanças de tamanho de tela
    window.addEventListener('resize', updateMobileState);
    
    // --- ANIMAÇÕES DE HABILIDADES E CONDIÇÕES ---
    
    // Função para animar habilidades com efeito de digitação (APENAS EM DESKTOP)
    function animateHabilidades() {
        if (isMobile) return; // Pular animações em mobile
        
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
    
    // Inicializar animações quando a página carregar (APENAS EM DESKTOP)
    if (!isMobile) {
        setTimeout(() => {
            animateHabilidades();
        }, 500);
    }
    

    
    // --- PROGRESSO E ANIMAÇÃO DOS CARDS (já existente) ---
    const projCheckboxes = document.querySelectorAll('.proj-checkbox');
    const imobCheckboxes = document.querySelectorAll('.imob-checkbox');
    const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
    const kaeshiWazaCheckboxes = document.querySelectorAll('.kaeshi-waza-checkbox');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    const backToTopBtn = document.getElementById('backToTop');
    let answeredQuestions = 0;
    const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
    let hasShownCongratulations = false;

    // Função para atualizar progresso (SEM mostrar barra flutuante)
    function updateProgress() {
        const totalProjChecked = Array.from(projCheckboxes).filter(cb => cb.checked).length;
        const totalImobChecked = Array.from(imobCheckboxes).filter(cb => cb.checked).length;
        const totalHenkakuenkaChecked = Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length;
        const totalKaeshiWazaChecked = Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
        const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
        const completedQuestions = totalProjChecked + totalImobChecked + totalHenkakuenkaChecked + totalKaeshiWazaChecked;
        const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
        

        
        progressBar.style.width = progress + '%';
        progressText.textContent = Math.round(progress) + '%';
        
        // Verificar se chegou a 100% e mostrar parabéns
        if (progress >= 100 && !hasShownCongratulations) {
            console.log('Progress is 100% - checking for congratulations'); // Debug
            
            // Verificar se todos os checkboxes estão marcados
            const allChecked = Array.from(projCheckboxes).every(cb => cb.checked) && 
                             Array.from(imobCheckboxes).every(cb => cb.checked) &&
                             Array.from(henkakuenkaCheckboxes).every(cb => cb.checked) &&
                             Array.from(kaeshiWazaCheckboxes).every(cb => cb.checked);
            
            if (allChecked) {
                console.log('Showing congratulations!'); // Debug
                setTimeout(() => {
                    showCongratulations();
                }, 500);
            }
        }
        
        // Verificação adicional: se todos os checkboxes estão marcados, mostrar parabéns
        if (completedQuestions >= 16 && !hasShownCongratulations) {
            console.log('Todos os 16 checkboxes marcados - mostrando parabéns!');
            setTimeout(() => {
                showCongratulations();
            }, 500);
        }
    }
    
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
        console.log('Closing congratulations modal'); // Debug
        const modal = document.getElementById('congratulationsModal');
        if (modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            console.log('Modal closed successfully'); // Debug
        } else {
            console.log('Modal not found for closing'); // Debug
        }
    }
    
    // Event listeners para botões do modal
    function initializeCongratulationsButtons() {
        const continueBtn = document.getElementById('continueTraining');
        const closeBtn = document.getElementById('closeCongratulations');
        
        console.log('Initializing congratulations buttons'); // Debug
        console.log('Continue button found:', !!continueBtn); // Debug
        console.log('Close button found:', !!closeBtn); // Debug
        
        if (continueBtn) {
            continueBtn.addEventListener('click', function() {
                console.log('Continue training clicked'); // Debug
                closeCongratulations();
                // Aqui você pode adicionar lógica para continuar treinando
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                console.log('Close congratulations clicked'); // Debug
                closeCongratulations();
            });
        }
    }
    
    // Inicializar botões de parabéns
    initializeCongratulationsButtons();

    // Função para mostrar barra de progresso flutuante
    function showFloatingProgress(progress) {
        // Atualizar valores da barra flutuante
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = Math.round(progress) + '%';
        
        // Mostrar a barra
        floatingProgress.classList.remove('hidden');
        floatingProgress.style.opacity = '1';
        floatingProgress.style.pointerEvents = 'auto';
        
        // Esconder após 3 segundos (tempo mais adequado)
        setTimeout(() => {
            floatingProgress.style.opacity = '0';
            floatingProgress.style.pointerEvents = 'none';
            setTimeout(() => {
                floatingProgress.classList.add('hidden');
            }, 300); // Aguarda a transição de opacity
        }, 3000);
    }

    // Garantir que a barra flutuante comece escondida
    floatingProgress.classList.add('hidden');
    floatingProgress.style.opacity = '0';
    floatingProgress.style.pointerEvents = 'none';
    

    
    // Esconder seções inicialmente
    document.getElementById('nage-waza-section').classList.add('hidden');
    document.getElementById('imobilizacoes-section').classList.add('hidden');
    document.getElementById('henkakuenka-section').classList.add('hidden');
    

    

    


    // Event listeners para as opções
    projCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            updateProgress();
            // Mostrar barra flutuante apenas quando marcar (não desmarcar)
            if (e.target.checked) {
                const totalProjChecked = Array.from(projCheckboxes).filter(cb => cb.checked).length;
                const totalImobChecked = Array.from(imobCheckboxes).filter(cb => cb.checked).length;
                const totalHenkakuenkaChecked = Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length;
                const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length;
                const completedQuestions = totalProjChecked + totalImobChecked + totalHenkakuenkaChecked;
                const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                showFloatingProgress(progress);
            }
        });
    });
    imobCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            updateProgress();
            // Mostrar barra flutuante apenas quando marcar (não desmarcar)
            if (e.target.checked) {
                const totalProjChecked = Array.from(projCheckboxes).filter(cb => cb.checked).length;
                const totalImobChecked = Array.from(imobCheckboxes).filter(cb => cb.checked).length;
                const totalHenkakuenkaChecked = Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length;
                const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length;
                const completedQuestions = totalProjChecked + totalImobChecked + totalHenkakuenkaChecked;
                const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                showFloatingProgress(progress);
            }
        });
    });
    henkakuenkaCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            updateProgress();
            // Mostrar barra flutuante apenas quando marcar (não desmarcar)
            if (e.target.checked) {
                const totalProjChecked = Array.from(projCheckboxes).filter(cb => cb.checked).length;
                const totalImobChecked = Array.from(imobCheckboxes).filter(cb => cb.checked).length;
                const totalHenkakuenkaChecked = Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length;
                const totalKaeshiWazaChecked = Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
                const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
                const completedQuestions = totalProjChecked + totalImobChecked + totalHenkakuenkaChecked + totalKaeshiWazaChecked;
                const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                showFloatingProgress(progress);
            }
        });
    });

    kaeshiWazaCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function(e) {
            updateProgress();
            // Mostrar barra flutuante apenas quando marcar (não desmarcar)
            if (e.target.checked) {
                const totalProjChecked = Array.from(projCheckboxes).filter(cb => cb.checked).length;
                const totalImobChecked = Array.from(imobCheckboxes).filter(cb => cb.checked).length;
                const totalHenkakuenkaChecked = Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length;
                const totalKaeshiWazaChecked = Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
                const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
                const completedQuestions = totalProjChecked + totalImobChecked + totalHenkakuenkaChecked + totalKaeshiWazaChecked;
                const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
                showFloatingProgress(progress);
            }
        });
    });
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.remove('hidden');
        } else {
            backToTopBtn.classList.add('hidden');
        }
    });
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

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
    
    // Função para animação de scroll com efeitos (OTIMIZADA PARA MOBILE)
    function smoothScrollTo(element, cardElement) {
        const targetElement = document.getElementById(element);
        const scrollIndicator = document.getElementById('scrollIndicator');
        const scrollText = document.getElementById('scrollText');
        
        if (!targetElement) return;
        
        // Adicionar classe clicked ao card (APENAS EM DESKTOP)
        if (!isMobile) {
            cardElement.classList.add('clicked');
            
            // Criar partículas no ponto de clique (APENAS EM DESKTOP)
            const rect = cardElement.getBoundingClientRect();
            createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2);
        }
        
        // Mostrar indicador de scroll
        scrollText.textContent = 'Navegando...';
        scrollIndicator.classList.add('show');
        
        // Calcular posição de destino
        const targetPosition = targetElement.offsetTop - 100;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        
        // Duração mais rápida em mobile
        const duration = isMobile ? 600 : 1200;
        let start = null;
        
        // Função de easing personalizada
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
            
            // Atualizar texto do indicador (APENAS EM DESKTOP)
            if (!isMobile) {
                if (progress < 0.5) {
                    scrollText.textContent = 'Navegando...';
                } else {
                    scrollText.textContent = 'Chegando...';
                }
            }
            
            if (progress < 1) {
                requestAnimationFrame(animation);
            } else {
                // Animação concluída
                setTimeout(() => {
                    scrollIndicator.classList.remove('show');
                    if (!isMobile) {
                        cardElement.classList.remove('clicked');
                        
                        // Adicionar destaque no destino (APENAS EM DESKTOP)
                        targetElement.classList.add('destination-highlight');
                        setTimeout(() => {
                            targetElement.classList.remove('destination-highlight');
                        }, 2000);
                    }
                }, isMobile ? 100 : 300);
            }
        }
        
        requestAnimationFrame(animation);
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
    
    // Verificar periodicamente se há botões não inicializados
    setInterval(() => {
        const buttons = document.querySelectorAll('.back-to-top-section');
        const uninitializedButtons = Array.from(buttons).filter(button => {
            const isVisible = button.offsetParent !== null;
            return isVisible && !button.hasAttribute('data-initialized');
        });
        
        if (uninitializedButtons.length > 0) {
            console.log('Encontrados botões não inicializados:', uninitializedButtons.length);
            initializeBackToTopButtons();
        }
    }, 2000);

    // Função para animação de scroll com efeitos (copiada da página2.html)
    function smoothScrollTo(element, cardElement) {
        const targetElement = document.getElementById(element);
        const scrollIndicator = document.getElementById('scrollIndicator');
        const scrollText = document.getElementById('scrollText');
        
        if (!targetElement) return;
        
        // Adicionar classe clicked ao card
        cardElement.classList.add('clicked');
        
        // Criar partículas no ponto de clique
        const rect = cardElement.getBoundingClientRect();
        createParticles(rect.left + rect.width / 2, rect.top + rect.height / 2);
        
        // Mostrar indicador de scroll
        scrollText.textContent = 'Navegando...';
        scrollIndicator.classList.add('show');
        
        // Calcular posição de destino
        const targetPosition = targetElement.offsetTop - 100;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 1200; // 1.2 segundos
        let start = null;
        
        // Função de easing personalizada
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
            
            // Atualizar texto do indicador
            if (progress < 0.5) {
                scrollText.textContent = 'Navegando...';
            } else {
                scrollText.textContent = 'Chegando...';
            }
            
            if (progress < 1) {
                requestAnimationFrame(animation);
            } else {
                // Animação concluída
                setTimeout(() => {
                    scrollIndicator.classList.remove('show');
                    cardElement.classList.remove('clicked');
                    
                    // Adicionar destaque no destino
                    targetElement.classList.add('destination-highlight');
                    setTimeout(() => {
                        targetElement.classList.remove('destination-highlight');
                    }, 2000);
                }, 300);
            }
        }
        
        requestAnimationFrame(animation);
    }
    
    // Navegação interna com animações visuais
    const nageWazaNav = document.getElementById('nage-waza-nav');
    const imobilizacoesNav = document.getElementById('imobilizacoes-nav');
    const henkakuenkaNav = document.getElementById('henkakuenka-nav');
    const nageWazaSection = document.getElementById('nage-waza-section');
    const imobilizacoesSection = document.getElementById('imobilizacoes-section');
    const henkakuenkaSection = document.getElementById('henkakuenka-section');

    if (nageWazaNav && nageWazaSection) {
        nageWazaNav.addEventListener('click', function(e) {
            e.preventDefault();
            // Esconder todas as seções primeiro
            document.getElementById('imobilizacoes-section').classList.add('hidden');
            document.getElementById('henkakuenka-section').classList.add('hidden');
            document.getElementById('kaeshi-waza-section').classList.add('hidden');
            // Mostrar a seção de técnicas de projeção
            document.getElementById('nage-waza-section').classList.remove('hidden');
            // Reinicializar botões back-to-top após mostrar a seção
            setTimeout(() => {
                smoothScrollTo('nage-waza-section', this);
            }, 100);
            
            // Inicializar botões após a seção estar completamente visível
            setTimeout(() => {
                initializeBackToTopButtons();
            }, 300);
            
            // Forçar inicialização das setas para Nage-waza
            setTimeout(() => {
                console.log('🔄 Forçando inicialização das setas para Nage-waza...');
                initializeCarouselArrows();
            }, 500);
        });
    }

    if (imobilizacoesNav && imobilizacoesSection) {
        imobilizacoesNav.addEventListener('click', function(e) {
            e.preventDefault();
            // Esconder todas as seções primeiro
            document.getElementById('nage-waza-section').classList.add('hidden');
            document.getElementById('henkakuenka-section').classList.add('hidden');
            document.getElementById('kaeshi-waza-section').classList.add('hidden');
            // Mostrar a seção de imobilizações
            document.getElementById('imobilizacoes-section').classList.remove('hidden');
            // Reinicializar botões back-to-top após mostrar a seção
            setTimeout(() => {
                smoothScrollTo('imobilizacoes-section', this);
            }, 100);
            
            // Inicializar botões após a seção estar completamente visível
            setTimeout(() => {
                initializeBackToTopButtons();
            }, 300);
        });
    }

    if (henkakuenkaNav && henkakuenkaSection) {
        henkakuenkaNav.addEventListener('click', function(e) {
            e.preventDefault();
            // Esconder todas as seções primeiro
            document.getElementById('nage-waza-section').classList.add('hidden');
            document.getElementById('imobilizacoes-section').classList.add('hidden');
            document.getElementById('kaeshi-waza-section').classList.add('hidden');
            // Mostrar a seção de ataques combinados
            document.getElementById('henkakuenka-section').classList.remove('hidden');
            // Reinicializar botões back-to-top após mostrar a seção
            setTimeout(() => {
                smoothScrollTo('henkakuenka-section', this);
            }, 100);
            
            // Inicializar botões após a seção estar completamente visível
            setTimeout(() => {
                initializeBackToTopButtons();
            }, 300);
        });
    }

    // Navegação para Kaeshi-waza
    const kaeshiWazaNav = document.getElementById('kaeshi-waza-nav');
    const kaeshiWazaSection = document.getElementById('kaeshi-waza-section');

    if (kaeshiWazaNav && kaeshiWazaSection) {
        kaeshiWazaNav.addEventListener('click', function(e) {
            e.preventDefault();
            // Esconder todas as seções primeiro
            document.getElementById('nage-waza-section').classList.add('hidden');
            document.getElementById('imobilizacoes-section').classList.add('hidden');
            document.getElementById('henkakuenka-section').classList.add('hidden');
            // Mostrar a seção de contra-ataques
            document.getElementById('kaeshi-waza-section').classList.remove('hidden');
            // Reinicializar botões back-to-top após mostrar a seção
            setTimeout(() => {
                smoothScrollTo('kaeshi-waza-section', this);
            }, 100);
            
            // Inicializar botões após a seção estar completamente visível
            setTimeout(() => {
                initializeBackToTopButtons();
            }, 300);
        });
    }
    
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
                
                // Mostrar indicador
                const scrollIndicator = document.getElementById('scrollIndicator');
                const scrollText = document.getElementById('scrollText');
                scrollText.textContent = 'Em desenvolvimento...';
                scrollIndicator.classList.add('show');
                
                // Remover efeitos após animação
                setTimeout(() => {
                    this.classList.remove('clicked');
                    scrollIndicator.classList.remove('show');
                }, 1500);
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
    // Função para animar a entrada do modal
    function animateModalEnter(modal) {
        if (!modal) return;
        
        // Reset do estado inicial
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.8) translateY(-20px)';
        modal.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        // Mostrar modal
        modal.style.display = 'flex';
        
        // Animar entrada
        setTimeout(() => {
            modal.style.opacity = '1';
            modal.style.transform = 'scale(1) translateY(0)';
        }, 10);
    }
    
    // Função para animar a saída do modal
    function animateModalExit(modal) {
        if (!modal) return;
        
        modal.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.8) translateY(-20px)';
        
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
    
    // ===== OTIMIZAÇÕES DE ANIMAÇÃO =====
    // Reduzir duração das animações de scroll para barra japonesa
    function smoothScrollToOptimized(targetId, duration = 800) {
        const targetElement = document.getElementById(targetId);
        if (!targetElement) return;
        
        const targetPosition = targetElement.offsetTop - 100;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const startTime = performance.now();
        
        function animation(currentTime) {
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            // Easing suave mas mais rápido
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            
            window.scrollTo(0, startPosition + (distance * easeProgress));
            
            if (progress < 1) {
                requestAnimationFrame(animation);
            }
        }
        
        requestAnimationFrame(animation);
    }
    
    // Reduzir duração das animações de voltar ao topo
    function backToTopOptimized() {
        const startPosition = window.pageYOffset;
        const startTime = performance.now();
        const duration = 600; // Reduzido de 1000ms para 600ms
        
        function animation(currentTime) {
            const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        
        // Easing mais suave
        const easeProgress = 1 - Math.pow(1 - progress, 2);
        
        window.scrollTo(0, startPosition * (1 - easeProgress));
        
        if (progress < 1) {
            requestAnimationFrame(animation);
        }
    }
    
    requestAnimationFrame(animation);
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

// Função específica para testar setas de projeção
window.testProjectionArrows = function() {
    console.log('🧪 Testando setas de projeção...');
    
    const section = document.getElementById('nage-waza-section');
    const carousel = document.getElementById('carouselProj');
    
    if (!section) {
        console.log('❌ Seção nage-waza-section não encontrada');
        return;
    }
    
    if (!carousel) {
        console.log('❌ Carrossel carouselProj não encontrado');
        return;
    }
    
    console.log('✅ Elementos encontrados');
    console.log('📊 Estado atual:', {
        sectionVisible: !section.classList.contains('hidden'),
        carouselWidth: carousel.clientWidth,
        scrollWidth: carousel.scrollWidth,
        hasArrows: section.querySelectorAll('.carousel-arrow-left, .carousel-arrow-right').length
    });
    
    // Forçar criação das setas
    const existingArrows = section.querySelectorAll('.carousel-arrow-left, .carousel-arrow-right');
    existingArrows.forEach(arrow => arrow.remove());
    
    const leftArrow = document.createElement('button');
    const rightArrow = document.createElement('button');
    
    leftArrow.className = 'carousel-arrow-left';
    rightArrow.className = 'carousel-arrow-right';
    leftArrow.innerHTML = '‹';
    rightArrow.innerHTML = '›';
    
    // Estilos inline para garantir visibilidade
    leftArrow.style.cssText = `
        position: absolute !important; 
        left: -1.5rem !important; 
        top: 50% !important; 
        transform: translateY(-50%) !important; 
        z-index: 999 !important; 
        background: rgba(249, 115, 22, 0.9) !important; 
        border: none !important; 
        border-radius: 50% !important; 
        width: 3rem !important; 
        height: 3rem !important; 
        color: white !important; 
        font-size: 2rem !important; 
        cursor: pointer !important; 
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    `;
    
    rightArrow.style.cssText = `
        position: absolute !important; 
        right: -1.5rem !important; 
        top: 50% !important; 
        transform: translateY(-50%) !important; 
        z-index: 999 !important; 
        background: rgba(249, 115, 22, 0.9) !important; 
        border: none !important; 
        border-radius: 50% !important; 
        width: 3rem !important; 
        height: 3rem !important; 
        color: white !important; 
        font-size: 2rem !important; 
        cursor: pointer !important; 
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    `;
    
    leftArrow.addEventListener('click', () => {
        console.log('⬅️ Seta esquerda clicada');
        carousel.scrollBy({ left: -carousel.clientWidth * 0.8, behavior: 'smooth' });
    });
    
    rightArrow.addEventListener('click', () => {
        console.log('➡️ Seta direita clicada');
        carousel.scrollBy({ left: carousel.clientWidth * 0.8, behavior: 'smooth' });
    });
    
    section.appendChild(leftArrow);
    section.appendChild(rightArrow);
    
    console.log('🎯 Setas de teste criadas com sucesso!');
    console.log('📍 Setas criadas:', {
        left: leftArrow,
        right: rightArrow,
        leftVisible: leftArrow.offsetParent !== null,
        rightVisible: rightArrow.offsetParent !== null
    });
};

// Função para adicionar setas diretamente no HTML
window.addArrowsToHTML = function() {
    console.log('🔧 Adicionando setas diretamente no HTML...');
    
    const section = document.getElementById('nage-waza-section');
    if (!section) {
        console.log('❌ Seção não encontrada');
        return;
    }
    
    console.log('📊 Estado da seção:', {
        section: section,
        sectionVisible: !section.classList.contains('hidden'),
        sectionPosition: section.getBoundingClientRect(),
        sectionStyle: window.getComputedStyle(section)
    });
    
    // Remover setas existentes primeiro
    const existingArrows = section.querySelectorAll('.carousel-arrow-left, .carousel-arrow-right');
    existingArrows.forEach(arrow => {
        console.log('🗑️ Removendo seta existente:', arrow);
        arrow.remove();
    });
    
    // Adicionar setas diretamente no HTML com estilos mais explícitos
    const arrowsHTML = `
        <button class="carousel-arrow-left" style="
            position: absolute !important; 
            left: -1.5rem !important; 
            top: 50% !important; 
            transform: translateY(-50%) !important; 
            z-index: 9999 !important; 
            background: rgba(249, 115, 22, 1) !important; 
            border: 2px solid white !important; 
            border-radius: 50% !important; 
            width: 3rem !important; 
            height: 3rem !important; 
            color: white !important; 
            font-size: 2rem !important; 
            font-weight: bold !important;
            cursor: pointer !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
            opacity: 1 !important;
            visibility: visible !important;
        ">‹</button>
        <button class="carousel-arrow-right" style="
            position: absolute !important; 
            right: -1.5rem !important; 
            top: 50% !important; 
            transform: translateY(-50%) !important; 
            z-index: 9999 !important; 
            background: rgba(249, 115, 22, 1) !important; 
            border: 2px solid white !important; 
            border-radius: 50% !important; 
            width: 3rem !important; 
            height: 3rem !important; 
            color: white !important; 
            font-size: 2rem !important; 
            font-weight: bold !important;
            cursor: pointer !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
            opacity: 1 !important;
            visibility: visible !important;
        ">›</button>
    `;
    
    section.insertAdjacentHTML('beforeend', arrowsHTML);
    
    // Verificar se as setas foram criadas
    const leftArrow = section.querySelector('.carousel-arrow-left');
    const rightArrow = section.querySelector('.carousel-arrow-right');
    const carousel = document.getElementById('carouselProj');
    
    console.log('🔍 Setas criadas:', {
        leftArrow: leftArrow,
        rightArrow: rightArrow,
        leftVisible: leftArrow ? leftArrow.offsetParent !== null : false,
        rightVisible: rightArrow ? rightArrow.offsetParent !== null : false,
        leftStyle: leftArrow ? window.getComputedStyle(leftArrow) : null,
        rightStyle: rightArrow ? window.getComputedStyle(rightArrow) : null
    });
    
    if (leftArrow && rightArrow && carousel) {
        leftArrow.addEventListener('click', () => {
            console.log('⬅️ Seta esquerda clicada');
            carousel.scrollBy({ left: -carousel.clientWidth * 0.8, behavior: 'smooth' });
        });
        
        rightArrow.addEventListener('click', () => {
            console.log('➡️ Seta direita clicada');
            carousel.scrollBy({ left: carousel.clientWidth * 0.8, behavior: 'smooth' });
        });
        
        console.log('✅ Setas adicionadas ao HTML com sucesso!');
        
        // Forçar reflow para garantir visibilidade
        leftArrow.offsetHeight;
        rightArrow.offsetHeight;
        
        // Adicionar classe de debug
        leftArrow.classList.add('debug-arrow');
        rightArrow.classList.add('debug-arrow');
        
            } else {
            console.log('❌ Erro ao criar setas:', { leftArrow, rightArrow, carousel });
        }
    };

// Função de teste que adiciona setas no body para debug
window.testArrowsInBody = function() {
    console.log('🧪 Testando setas no body...');
    
    // Remover setas existentes do body
    const existingBodyArrows = document.querySelectorAll('.test-arrow');
    existingBodyArrows.forEach(arrow => arrow.remove());
    
    // Criar setas de teste no body
    const leftArrow = document.createElement('button');
    const rightArrow = document.createElement('button');
    
    leftArrow.className = 'test-arrow';
    rightArrow.className = 'test-arrow';
    
    leftArrow.innerHTML = '‹';
    rightArrow.innerHTML = '›';
    
    // Estilos inline para teste
    leftArrow.style.cssText = `
        position: fixed !important;
        left: 20px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 10000 !important;
        background: red !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        width: 4rem !important;
        height: 4rem !important;
        color: white !important;
        font-size: 2rem !important;
        font-weight: bold !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    `;
    
    rightArrow.style.cssText = `
        position: fixed !important;
        right: 20px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 10000 !important;
        background: blue !important;
        border: 2px solid white !important;
        border-radius: 50% !important;
        width: 4rem !important;
        height: 4rem !important;
        color: white !important;
        font-size: 2rem !important;
        font-weight: bold !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    `;
    
    document.body.appendChild(leftArrow);
    document.body.appendChild(rightArrow);
    
    console.log('🎯 Setas de teste criadas no body!');
    console.log('🔴 Seta vermelha à esquerda, 🔵 Seta azul à direita');
    
    // Adicionar event listeners de teste
    leftArrow.addEventListener('click', () => {
        console.log('🔴 Seta vermelha clicada!');
        alert('Seta vermelha funcionando!');
    });
    
    rightArrow.addEventListener('click', () => {
        console.log('🔵 Seta azul clicada!');
        alert('Seta azul funcionando!');
    });
};

// Função que força a criação das setas na seção de projeção
window.forceProjectionArrows = function() {
    console.log('💪 Forçando criação das setas de projeção...');
    
    const section = document.getElementById('nage-waza-section');
    if (!section) {
        console.log('❌ Seção nage-waza-section não encontrada');
        return;
    }
    
    // Verificar se a seção está visível
    if (section.classList.contains('hidden')) {
        console.log('⚠️ Seção está oculta, removendo classe hidden...');
        section.classList.remove('hidden');
    }
    
    // Verificar se o carrossel existe
    const carousel = document.getElementById('carouselProj');
    if (!carousel) {
        console.log('❌ Carrossel carouselProj não encontrado');
        return;
    }
    
    // Remover setas existentes
    const existingArrows = section.querySelectorAll('.carousel-arrow-left, .carousel-arrow-right, .force-arrow');
    existingArrows.forEach(arrow => arrow.remove());
    
    // Criar setas com ID único
    const leftArrow = document.createElement('button');
    const rightArrow = document.createElement('button');
    
    leftArrow.id = 'forceLeftArrow';
    rightArrow.id = 'forceRightArrow';
    leftArrow.className = 'force-arrow';
    rightArrow.className = 'force-arrow';
    
    leftArrow.innerHTML = '‹';
    rightArrow.innerHTML = '›';
    
    // Estilos inline ultra-específicos
    const arrowStyles = `
        position: absolute !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 99999 !important;
        background: rgba(249, 115, 22, 1) !important;
        border: 3px solid white !important;
        border-radius: 50% !important;
        width: 4rem !important;
        height: 4rem !important;
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6) !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
    `;
    
    leftArrow.style.cssText = arrowStyles + 'left: -2rem !important;';
    rightArrow.style.cssText = arrowStyles + 'right: -2rem !important;';
    
    // Adicionar ao DOM
    section.appendChild(leftArrow);
    section.appendChild(rightArrow);
    
    console.log('🎯 Setas forçadas criadas:', {
        leftArrow: leftArrow,
        rightArrow: rightArrow,
        leftVisible: leftArrow.offsetParent !== null,
        rightVisible: rightArrow.offsetParent !== null
    });
    
    // Adicionar event listeners
    leftArrow.addEventListener('click', () => {
        console.log('⬅️ Seta esquerda forçada clicada!');
        carousel.scrollBy({ left: -carousel.clientWidth * 0.8, behavior: 'smooth' });
    });
    
    rightArrow.addEventListener('click', () => {
        console.log('➡️ Seta direita forçada clicada!');
        carousel.scrollBy({ left: carousel.clientWidth * 0.8, behavior: 'smooth' });
    });
    
    console.log('✅ Setas forçadas criadas com sucesso!');
};