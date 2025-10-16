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
    
    // Remover objeto checkboxes estático - usar apenas allCheckboxes dinâmico
    
    let hasShownCongratulations = false;
    
    // ===== SISTEMA DE PROGRESSO OTIMIZADO =====
    function updateProgress() {
        // Buscar TODOS os checkboxes da página, incluindo os ocultos
        const allCheckboxes = {
            proj: document.querySelectorAll('.proj-checkbox'),
            imob: document.querySelectorAll('.imob-checkbox'),
            chave: document.querySelectorAll('.chave-checkbox'),
            shime: document.querySelectorAll('.shime-checkbox'),
            henkakuenka: document.querySelectorAll('.henkakuenka-checkbox'),
            kaeshiWaza: document.querySelectorAll('.kaeshi-waza-checkbox')
        };
        
        console.log('=== PROGRESS DEBUG ===');
        console.log('Henkakuenka checkboxes found:', allCheckboxes.henkakuenka.length);
        
        // Debug específico para henkakuenka
        if (allCheckboxes.henkakuenka.length === 0) {
            console.log('❌ PROBLEMA: Nenhum checkbox henkakuenka encontrado!');
            console.log('Tentando buscar novamente...');
            const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
            console.log('Nova busca encontrou:', henkakuenkaCheckboxes.length);
        } else {
            console.log('✅ Henkakuenka checkboxes encontrados:', allCheckboxes.henkakuenka.length);
        }
        
        // Contar total e completados
        let totalQuestions = 0;
        let completedQuestions = 0;
        
        Object.keys(allCheckboxes).forEach(category => {
            const categoryCheckboxes = allCheckboxes[category];
            totalQuestions += categoryCheckboxes.length;
            completedQuestions += Array.from(categoryCheckboxes).filter(cb => cb.checked).length;
        });
        
        // Calcular progresso (cada checkbox = 100/totalQuestions %)
        const progressPerCheckbox = totalQuestions > 0 ? 100 / totalQuestions : 0;
        const progress = completedQuestions * progressPerCheckbox;
        
        console.log('=== PROGRESS DEBUG ===');
        console.log('Total Questions:', totalQuestions);
        console.log('Completed Questions:', completedQuestions);
        console.log('Progress per checkbox:', progressPerCheckbox.toFixed(2) + '%');
        console.log('Current Progress:', Math.round(progress) + '%');
        
        // Debug por categoria
        console.log('=== CATEGORY DEBUG ===');
        Object.keys(allCheckboxes).forEach(category => {
            const categoryCheckboxes = allCheckboxes[category];
            const checkedCount = Array.from(categoryCheckboxes).filter(cb => cb.checked).length;
            const remaining = categoryCheckboxes.length - checkedCount;
            console.log(`${category}: ${checkedCount}/${categoryCheckboxes.length} checked (${remaining} remaining)`);
            
            // Debug específico para henkakuenka
            if (category === 'henkakuenka') {
                console.log('=== HENKAKUENKA DETAILED DEBUG ===');
                categoryCheckboxes.forEach((checkbox, index) => {
                    console.log(`Henkakuenka ${index + 1}:`, {
                        element: checkbox,
                        checked: checkbox.checked,
                        visible: checkbox.offsetParent !== null,
                        className: checkbox.className
                    });
                });
            }
        });
        
        // Mostrar o que falta para completar
        const totalRemaining = totalQuestions - completedQuestions;
        if (totalRemaining > 0) {
            console.log(`🎯 Faltam ${totalRemaining} checkboxes para completar 100%!`);
        } else {
            console.log('🎉 Todos os checkboxes estão marcados!');
        }
        
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
    
    // ===== EVENT LISTENERS SIMPLIFICADOS =====
    // Event listener universal para TODOS os checkboxes
    document.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox') {
            console.log('Checkbox changed:', e.target.className, e.target.checked);
            updateProgress();
        }
    });
    
    // Event listener específico para henkakuenka checkboxes
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('henkakuenka-checkbox')) {
            console.log('=== HENKAKUENKA CLICK ===');
            console.log('Antes:', e.target.checked);
            
            // Aguardar um pouco para o estado mudar
            setTimeout(() => {
                console.log('Depois:', e.target.checked);
                updateProgress();
            }, 10);
        }
    });
    
    // Event listener adicional com mousedown para garantir funcionamento
    document.addEventListener('mousedown', function(e) {
        if (e.target.classList.contains('henkakuenka-checkbox')) {
            console.log('=== HENKAKUENKA MOUSEDOWN ===');
            e.preventDefault();
            e.stopPropagation();
            
            // Forçar toggle e atualização
            setTimeout(() => {
                e.target.checked = !e.target.checked;
                updateProgress();
            }, 10);
        }
    });
    
    // Event listener adicional para garantir que funcione mesmo com seção oculta
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('henkakuenka-checkbox')) {
            console.log('=== HENKAKUENKA CHANGE ===');
            console.log('Checkbox changed:', e.target.checked);
            updateProgress();
        }
    });
    
    // Aguardar um pouco para garantir que todos os elementos estejam carregados
    setTimeout(() => {
        updateProgress();
        
        // Debug para verificar se os checkboxes estão sendo encontrados
        console.log('=== CHECKBOX DEBUG ===');
        const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
        console.log('Henkakuenka checkboxes found:', henkakuenkaCheckboxes.length);
        
        henkakuenkaCheckboxes.forEach((checkbox, index) => {
            console.log(`Henkakuenka ${index + 1}:`, {
                exists: !!checkbox,
                visible: checkbox.offsetParent !== null,
                checked: checkbox.checked
            });
        });
    }, 100);
    
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
    
    // Função para re-adicionar event listeners quando seções são mostradas
    function reAddEventListeners() {
        // Agora não é mais necessário, pois usamos listeners universais
        console.log('Event listeners are now universal - no need to re-add');
    }
    
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
        
        // Atualizar progresso após mostrar a seção
        setTimeout(() => {
            updateProgress();
            
            // Debug específico para seção de ataques combinados
            if (section.id === 'henkakuenka-section') {
                console.log('=== HENKAKUENKA SECTION SHOWN ===');
                const henkakuenkaCheckboxes = section.querySelectorAll('.henkakuenka-checkbox');
                console.log('Henkakuenka checkboxes in section:', henkakuenkaCheckboxes.length);
                
                // Debug para cada checkbox
                henkakuenkaCheckboxes.forEach((checkbox, index) => {
                    console.log(`Section henkakuenka ${index + 1}:`, {
                        checked: checkbox.checked,
                        className: checkbox.className,
                        visible: checkbox.offsetParent !== null
                    });
                });
            }
        }, 100);
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
                
                // Forçar atualização do progresso após mostrar seção
                setTimeout(() => {
                    console.log('Forcing progress update after showing section:', section);
                    updateProgress();
                }, 500);
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
    
    // ===== SISTEMA DE PROGRESSO NO BANCO DE DADOS =====
    
    // Salvar progresso no banco de dados
    function saveProgress() {
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        
        const elementos = [];
        
        allCheckboxes.forEach((checkbox, index) => {
            let tipo = 'proj-checkbox';
            if (checkbox.classList.contains('imob-checkbox')) tipo = 'imob-checkbox';
            else if (checkbox.classList.contains('chave-checkbox')) tipo = 'chave-checkbox';
            else if (checkbox.classList.contains('shime-checkbox')) tipo = 'shime-checkbox';
            else if (checkbox.classList.contains('henkakuenka-checkbox')) tipo = 'henkakuenka-checkbox';
            else if (checkbox.classList.contains('kaeshi-waza-checkbox')) tipo = 'kaeshi-waza-checkbox';
            
            elementos.push({
                id: `checkbox_${index}`,
                tipo: tipo,
                aprendido: checkbox.checked
            });
        });
        
        // Salvar no banco de dados
        fetch('/pagina4/salvar-progresso/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                pagina: 'pagina4',
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
        fetch('/pagina4/carregar-progresso/?pagina=pagina4')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.elementos.length > 0) {
                console.log('Carregando progresso do banco de dados:', data.elementos);
                
                const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                
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
    
    // Modificar o event listener para salvar progresso
    document.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox') {
            console.log('Checkbox changed:', e.target.className, e.target.checked);
            updateProgress();
            saveProgress(); // Salvar no banco quando mudar
        }
    });
    
    // Carregar progresso ao inicializar
    loadProgress();
    
}); // Fim do DOMContentLoaded