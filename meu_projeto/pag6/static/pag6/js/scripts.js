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
    // Função para atualizar progresso
    function updateProgress() {
        const totalProjChecked = document.querySelectorAll('.proj-checkbox:checked').length;
        const totalImobChecked = document.querySelectorAll('.imob-checkbox:checked').length;
        const totalChaveChecked = document.querySelectorAll('.chave-checkbox:checked').length;
        const totalEstrangChecked = document.querySelectorAll('.estrang-checkbox:checked').length;
        const totalAtaquesCombinadosChecked = document.querySelectorAll('.ataques-combinados-checkbox:checked').length;
        const totalContraAtaquesChecked = document.querySelectorAll('.contra-ataques-checkbox:checked').length;
        const totalQuestions = projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length;
        const completedQuestions = totalProjChecked + totalImobChecked + totalChaveChecked + totalEstrangChecked + totalAtaquesCombinadosChecked + totalContraAtaquesChecked;
        const progress = (completedQuestions / totalQuestions) * 100;
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
                             Array.from(ataquesCombinadosCheckboxes).every(cb => cb.checked) &&
                             Array.from(contraAtaquesCheckboxes).every(cb => cb.checked);
            
            if (allChecked) {
                console.log('Showing congratulations!');
                setTimeout(() => {
                    showCongratulations();
                }, 500);
            }
        }
        
        // Verificação adicional: se todos os checkboxes estão marcados, mostrar parabéns
        const totalCheckboxes = 37 + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length;
        if (completedQuestions >= totalCheckboxes && !hasShownCongratulations) {
            console.log(`Todos os ${totalCheckboxes} checkboxes marcados - mostrando parabéns!`);
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
    projCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
    });
    imobCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
    });
    chaveCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
    });
    estrangCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
    });

    // Event listeners para os novos checkboxes
    ataquesCombinadosCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
    });

    contraAtaquesCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateProgress();
            if (this.checked) {
                showFloatingProgress((document.querySelectorAll('.proj-checkbox:checked').length + document.querySelectorAll('.imob-checkbox:checked').length + document.querySelectorAll('.chave-checkbox:checked').length + document.querySelectorAll('.estrang-checkbox:checked').length + document.querySelectorAll('.ataques-combinados-checkbox:checked').length + document.querySelectorAll('.contra-ataques-checkbox:checked').length) / (projCheckboxes.length + imobCheckboxes.length + chaveCheckboxes.length + estrangCheckboxes.length + ataquesCombinadosCheckboxes.length + contraAtaquesCheckboxes.length) * 100);
            }
        });
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

    // Botão voltar ao topo
    const backToTopBtn = document.getElementById('backToTop');
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.remove('hidden');
        } else {
            backToTopBtn.classList.add('hidden');
        }
    });
    
    // Função para criar partículas no botão voltar ao topo
    function createBackToTopParticles(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        for (let i = 0; i < 12; i++) {
            const particle = document.createElement('div');
            particle.className = 'back-to-top-particle';
            particle.style.left = centerX + (Math.random() - 0.5) * 60 + 'px';
            particle.style.top = centerY + (Math.random() - 0.5) * 60 + 'px';
            particle.style.background = `rgba(255, 255, 255, ${0.7 + Math.random() * 0.3})`;
            particle.style.position = 'fixed';
            particle.style.width = '10px';
            particle.style.height = '10px';
            particle.style.borderRadius = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = 9999;
            particle.style.transition = 'opacity 0.8s';
            document.body.appendChild(particle);
            setTimeout(() => {
                particle.style.opacity = 0;
                setTimeout(() => {
                    if (particle.parentNode) {
                        particle.parentNode.removeChild(particle);
                    }
                }, 400);
            }, 800);
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

    // JavaScript para carrossel de Projeções
    const carouselProj = document.getElementById('carouselProj');
    const projLeftBtn = document.getElementById('carouselLeft');
    const projRightBtn = document.getElementById('carouselRight');
    
    if (carouselProj && projLeftBtn && projRightBtn) {
        projLeftBtn.addEventListener('click', () => {
            carouselProj.scrollBy({ left: -carouselProj.offsetWidth * 0.8, behavior: 'smooth' });
            projLeftBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => projLeftBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        projRightBtn.addEventListener('click', () => {
            carouselProj.scrollBy({ left: carouselProj.offsetWidth * 0.8, behavior: 'smooth' });
            projRightBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => projRightBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        
        // Botões sempre visíveis - removida a lógica de ocultar/mostrar
    }

    // JavaScript para carrossel de Imobilizações
    const carouselImob = document.getElementById('carouselImob');
    const imobLeftBtn = document.getElementById('carouselImobLeft');
    const imobRightBtn = document.getElementById('carouselImobRight');
    
    if (carouselImob && imobLeftBtn && imobRightBtn) {
        imobLeftBtn.addEventListener('click', () => {
            carouselImob.scrollBy({ left: -carouselImob.offsetWidth * 0.6, behavior: 'smooth' });
            imobLeftBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => imobLeftBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        imobRightBtn.addEventListener('click', () => {
            // Se estiver próximo do final, ir direto para o final
            const remainingScroll = carouselImob.scrollWidth - carouselImob.scrollLeft - carouselImob.offsetWidth;
            if (remainingScroll < carouselImob.offsetWidth * 0.8) {
                carouselImob.scrollTo({ left: carouselImob.scrollWidth - carouselImob.offsetWidth, behavior: 'smooth' });
            } else {
                carouselImob.scrollBy({ left: carouselImob.offsetWidth * 0.6, behavior: 'smooth' });
            }
            imobRightBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => imobRightBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        
        // Botões sempre visíveis - removida a lógica de ocultar/mostrar
    }

    // JavaScript para carrossel de Chave de Braço
    const carouselChave = document.getElementById('carouselChave');
    const chaveLeftBtn = document.getElementById('carouselChaveLeft');
    const chaveRightBtn = document.getElementById('carouselChaveRight');
    
    if (carouselChave && chaveLeftBtn && chaveRightBtn) {
        chaveLeftBtn.addEventListener('click', () => {
            carouselChave.scrollBy({ left: -carouselChave.offsetWidth * 0.8, behavior: 'smooth' });
            chaveLeftBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => chaveLeftBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        chaveRightBtn.addEventListener('click', () => {
            carouselChave.scrollBy({ left: carouselChave.offsetWidth * 0.8, behavior: 'smooth' });
            chaveRightBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => chaveRightBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        
        // Botões sempre visíveis - removida a lógica de ocultar/mostrar
    }

    // JavaScript para carrossel de Estrangulamento
    const carouselEstrang = document.getElementById('carouselEstrang');
    const estrangLeftBtn = document.getElementById('carouselEstrangLeft');
    const estrangRightBtn = document.getElementById('carouselEstrangRight');
    
    if (carouselEstrang && estrangLeftBtn && estrangRightBtn) {
        estrangLeftBtn.addEventListener('click', () => {
            carouselEstrang.scrollBy({ left: -carouselEstrang.offsetWidth * 0.8, behavior: 'smooth' });
            estrangLeftBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => estrangLeftBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        estrangRightBtn.addEventListener('click', () => {
            carouselEstrang.scrollBy({ left: carouselEstrang.offsetWidth * 0.8, behavior: 'smooth' });
            estrangRightBtn.classList.add('carousel-arrow-anim');
            setTimeout(() => estrangRightBtn.classList.remove('carousel-arrow-anim'), 700);
        });
        
        // Botões sempre visíveis - removida a lógica de ocultar/mostrar
    }

});