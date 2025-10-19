// --- VARIÁVEIS GLOBAIS ---
let allCheckboxes;
let hasShownCongratulations = false;

// --- FUNÇÕES GLOBAIS ---
function showSection(sectionId) {
    console.log('🔍 showSection chamada com:', sectionId);
    
    // Esconder todas as seções primeiro
    const sections = [
        'nage-waza-section', 'imobilizacoes-section', 'chave-braco-section',
        'estrangulamento-section', 'henkakuenka-section', 'kaeshi-waza-section'
    ];
    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) section.classList.add('hidden');
    });
    
    // Mostrar a seção selecionada
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        console.log('✅ Seção', sectionId, 'mostrada com sucesso!');
        targetSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    } else {
        console.error('❌ Seção', sectionId, 'não encontrada!');
    }
}

// Tornar a função globalmente acessível
window.showSection = showSection;

// Função para mostrar barra flutuante de progresso
function showFloatingProgress(progress) {
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    if (floatingProgress && floatingProgressBar && floatingProgressText) {
        // Atualizar barra e texto
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = `Progresso: ${Math.round(progress)}%`;
        
        // Mostrar barra
        floatingProgress.style.display = 'block';
        
        // Esconder após 3 segundos
        setTimeout(() => {
            floatingProgress.style.display = 'none';
        }, 3000);
    }
}

// Tornar a função globalmente acessível
window.showFloatingProgress = showFloatingProgress;


document.addEventListener('DOMContentLoaded', function() {
    // Inicializar variáveis
    allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    
    // --- ANIMAÇÕES ---
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
    
    // --- SISTEMA DE PROGRESSO REMOVIDO ---
    // O sistema de progresso foi removido conforme solicitado
    
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

    
    // Inicializar botões de voltar ao topo das seções
    document.querySelectorAll('.back-to-top-section').forEach(button => {
        if (!button.hasAttribute('data-initialized')) {
            button.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            button.setAttribute('data-initialized', 'true');
        }
    });

    // ===== SISTEMA DE PROGRESSO NO BANCO DE DADOS =====
    
    // Salvar progresso no banco de dados
    function saveProgress() {
        // Atualizar variável global
        allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        
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
        fetch('/pagina5/salvar-progresso/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                pagina: 'pagina5',
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
        fetch('/pagina5/carregar-progresso/?pagina=pagina5')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.elementos.length > 0) {
                console.log('Carregando progresso do banco de dados:', data.elementos);
                
                // Atualizar variável global
        allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                
                data.elementos.forEach(elemento => {
                    const index = parseInt(elemento.id.replace('checkbox_', ''));
                    if (allCheckboxes[index]) {
                        allCheckboxes[index].checked = elemento.aprendido;
                    }
                });
                
                // Atualizar barra de progresso após carregar do banco
                // Atualizar variável global
        allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                const checked = document.querySelectorAll('input[type="checkbox"]:checked');
                const progress = (checked.length / allCheckboxes.length) * 100;
                
                const progressBar = document.getElementById('progressBar');
                const progressText = document.getElementById('progressText');
                
                if (progressBar) {
                    progressBar.style.width = progress + '%';
                }
                if (progressText) {
                    progressText.textContent = Math.round(progress) + '%';
                }
            } else {
                console.log('Nenhum progresso no banco, usando estado atual');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar progresso do banco:', error);
        });
    }
    
    // Event listener para salvar progresso e atualizar barra
    document.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox') {
            // Calcular progresso
            // Atualizar variável global
            allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
            const checked = document.querySelectorAll('input[type="checkbox"]:checked');
            const progress = (checked.length / allCheckboxes.length) * 100;
            
            // Atualizar barra de progresso
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            
            if (progressBar) {
                progressBar.style.width = progress + '%';
            }
            if (progressText) {
                progressText.textContent = Math.round(progress) + '%';
            }
            
            // Mostrar barra flutuante quando checkbox é marcado
            if (e.target.checked) {
                showFloatingProgress(progress);
            }
            
            // Salvar progresso no banco de dados
            saveProgress();
            
            // Verificar se completou 100%
            if (progress >= 100 && !hasShownCongratulations) {
                hasShownCongratulations = true;
                showCongratulations();
            }
        }
    });
    
    // Carregar progresso ao inicializar
    loadProgress();
});