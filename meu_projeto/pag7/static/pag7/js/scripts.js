document.addEventListener('DOMContentLoaded', function() {
    // --- SISTEMA DE LAZY LOADING PARA VÍDEOS ---
    
    // Função para extrair ID do YouTube
    function extractYouTubeId(url) {
        const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/);
        return match ? match[1] : null;
    }
    
    // Função para criar thumbnail
    function createVideoThumbnail(iframe) {
        const src = iframe.getAttribute('src');
        const videoId = extractYouTubeId(src);
        if (!videoId) return iframe;
        
        const container = document.createElement('div');
        container.className = 'video-thumbnail-container';
        
        // Criar imagem com fallback para sddefault se maxresdefault falhar
        const img = document.createElement('img');
        img.style.cssText = 'width:100%;height:200px;object-fit:cover;border-radius:8px;';
        img.alt = 'Vídeo';
        
        // Tentar maxresdefault primeiro
        img.src = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
        
        // Fallback para sddefault se maxresdefault falhar
        img.onerror = function() {
            this.onerror = null; // Evitar loop infinito
            this.src = `https://img.youtube.com/vi/${videoId}/sddefault.jpg`;
        };
        
        const playOverlay = document.createElement('div');
        playOverlay.className = 'play-overlay';
        playOverlay.innerHTML = '<div class="play-button">▶</div>';
        
        container.appendChild(img);
        container.appendChild(playOverlay);
        
        container.addEventListener('click', () => {
            container.parentNode.replaceChild(iframe, container);
        });
        
        return container;
    }
    
    // Inicializar thumbnails para todos os vídeos
    document.querySelectorAll('.video-container iframe[src*="youtube.com"]').forEach(iframe => {
        const thumbnail = createVideoThumbnail(iframe);
        iframe.parentNode.replaceChild(thumbnail, iframe);
    });
    
    // --- ANIMAÇÕES REMOVIDAS PARA PERFORMANCE ---
    // Animações removidas para melhorar performance mobile
    
    // --- SISTEMA DE PROGRESSO SIMPLIFICADO ---
    // Total de técnicas da Faixa Marrom:
    // - Nage Waza (Projeções): 7 técnicas
    // - Imobilizações: 5 técnicas
    // - Chave de Braço: 4 técnicas (removido: HARA-GARAME)
    // - Estrangulamento: 6 técnicas (removido: UDO-JIME, restaurado: TOMO-JIME)
    // - Ataque Combinado: 9 combinações (removido: IPPON-SEOI-NAGUE → TAMA-GURUMA)
    // - Contra-Ataque: 9 técnicas (removido: SASSAE-TSURI-KOMI-ASHI → MAE-TE-GURUMA)
    // TOTAL: 40 checkboxes
    
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    let hasShownCongratulations = false;
    let hideFloatingTimeout = null;
    
    function showFloatingProgress(progress) {
        if (!floatingProgress) return;
        
        // Cancelar timeout anterior se existir
        if (hideFloatingTimeout) {
            clearTimeout(hideFloatingTimeout);
        }
        
        // Atualizar barra flutuante com !important para sobrescrever CSS
        if (floatingProgressBar) {
            floatingProgressBar.style.setProperty('width', progress + '%', 'important');
        }
        if (floatingProgressText) floatingProgressText.textContent = Math.round(progress) + '%';
        
        // Mostrar barra flutuante
        floatingProgress.classList.remove('hidden');
        setTimeout(() => {
            floatingProgress.style.opacity = '1';
        }, 10);
        
        // Esconder automaticamente após 3 segundos
        hideFloatingTimeout = setTimeout(() => {
            floatingProgress.style.opacity = '0';
            setTimeout(() => {
                floatingProgress.classList.add('hidden');
            }, 300);
        }, 3000);
    }
    
    function updateProgress() {
        // Contar todos os checkboxes dinamicamente
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        const checked = document.querySelectorAll('input[type="checkbox"]:checked');
        const progress = allCheckboxes.length > 0 ? (checked.length / allCheckboxes.length) * 100 : 0;
        
        // Atualizar barra do header
        if (progressBar) progressBar.style.width = progress + '%';
        if (progressText) progressText.textContent = Math.round(progress) + '%';
        
        // Mostrar barra flutuante
        showFloatingProgress(progress);
        
        // Mostrar parabéns quando completar 100%
        if (progress >= 100 && !hasShownCongratulations) {
            hasShownCongratulations = true;
            showCongratulations();
        }
    }
    
    // Adicionar listeners a todos os checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateProgress);
    });
    
    // Inicializar progresso ao carregar a página
    updateProgress();
    
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
    
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.remove('hidden');
            } else {
                backToTopBtn.classList.add('hidden');
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // --- ANIMAÇÕES DE NAVEGAÇÃO REMOVIDAS ---
    // Animações removidas para melhorar performance mobile

    // --- NAVEGAÇÃO SIMPLIFICADA ---
    function setupNavigation() {
        const navItems = [
            { nav: 'nage-waza-nav', section: 'nage-waza-section' },
            { nav: 'imobilizacoes-nav', section: 'imobilizacoes-section' },
            { nav: 'chave-braco-nav', section: 'chave-braco-section' },
            { nav: 'estrangulamento-nav', section: 'estrangulamento-section' },
            { nav: 'ataque-combinado-nav', section: 'ataque-combinado-section' },
            { nav: 'contra-ataque-nav', section: 'contra-ataque-section' }
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
    
    function hideAllSections() {
        const sections = [
            'nage-waza-section', 'imobilizacoes-section', 'chave-braco-section',
            'estrangulamento-section', 'ataque-combinado-section', 'contra-ataque-section'
        ];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) section.classList.add('hidden');
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
    initializeCarousel('carousel', 'carouselLeft', 'carouselRight');
    initializeCarousel('carouselProj', 'carouselProjLeft', 'carouselProjRight');
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
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        
        const elementos = [];
        
        allCheckboxes.forEach((checkbox, index) => {
            let tipo = 'proj-checkbox';
            if (checkbox.classList.contains('imob-checkbox')) tipo = 'imob-checkbox';
            else if (checkbox.classList.contains('chave-checkbox')) tipo = 'chave-checkbox';
            else if (checkbox.classList.contains('shime-checkbox')) tipo = 'shime-checkbox';
            else if (checkbox.classList.contains('ataque-combinado-checkbox')) tipo = 'ataque-combinado-checkbox';
            else if (checkbox.classList.contains('contra-ataque-checkbox')) tipo = 'contra-ataque-checkbox';
            
            elementos.push({
                id: `checkbox_${index}`,
                tipo: tipo,
                aprendido: checkbox.checked
            });
        });
        
        // Salvar no banco de dados
        fetch('/pagina7/salvar-progresso/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                pagina: 'pagina7',
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
        fetch('/pagina7/carregar-progresso/?pagina=pagina7')
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
            updateProgress();
            saveProgress(); // Salvar no banco quando mudar
        }
    });
    
    // Carregar progresso ao inicializar
    loadProgress();
});