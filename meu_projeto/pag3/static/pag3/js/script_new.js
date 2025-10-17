// ===== FUNÇÃO GLOBAL PARA MOSTRAR/ESCONDER SEÇÕES =====
window.showSection = function(sectionId) {
    console.log('🔍 showSection chamada com:', sectionId);
    
    const allSections = [
        'nage-waza-section',
        'imobilizacoes-section', 
        'henkakuenka-section',
        'technique-cards-section',
        'kaeshi-waza-section'
    ];
    
    console.log('🔍 Seções disponíveis:', allSections);
    
    // Esconder todas as seções primeiro
    allSections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.add('hidden');
            console.log('🔍 Escondendo seção:', id);
        } else {
            console.log('⚠️ Seção não encontrada:', id);
        }
    });
    
    // Mostrar a seção selecionada
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        console.log('✅ Removendo classe hidden de:', sectionId);
        targetSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        console.log('✅ Seção', sectionId, 'mostrada com sucesso!');
    } else {
        console.error('❌ Seção', sectionId, 'não encontrada!');
    }
};

// ===== SISTEMA DE PROGRESSO =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script da Página 3 carregado!');
    
    // Variáveis globais
    const projCheckboxes = document.querySelectorAll('.proj-checkbox');
    const imobCheckboxes = document.querySelectorAll('.imob-checkbox');
    const henkakuenkaCheckboxes = document.querySelectorAll('.henkakuenka-checkbox');
    const kaeshiWazaCheckboxes = document.querySelectorAll('.kaeshi-waza-checkbox');
    
    // Elementos DOM
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const floatingProgress = document.getElementById('floatingProgress');
    const floatingProgressBar = document.getElementById('floatingProgressBar');
    const floatingProgressText = document.getElementById('floatingProgressText');
    
    // Função para mostrar barra flutuante
    function showFloatingProgress(progress) {
        if (!floatingProgress || !floatingProgressBar || !floatingProgressText) return;
        
        floatingProgressBar.style.width = progress + '%';
        floatingProgressText.textContent = Math.round(progress) + '%';
        
        // Mostrar barra flutuante
        floatingProgress.classList.remove('hidden');
        floatingProgress.style.opacity = '1';
        
        // Esconder após 3 segundos
        setTimeout(() => {
            floatingProgress.style.opacity = '0';
            setTimeout(() => floatingProgress.classList.add('hidden'), 300);
        }, 3000);
    }
    
    // Função para atualizar progresso
    function updateProgress() {
        const totalQuestions = projCheckboxes.length + imobCheckboxes.length + henkakuenkaCheckboxes.length + kaeshiWazaCheckboxes.length;
        const completedQuestions = Array.from(projCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(imobCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(henkakuenkaCheckboxes).filter(cb => cb.checked).length +
                                 Array.from(kaeshiWazaCheckboxes).filter(cb => cb.checked).length;
        const progress = totalQuestions > 0 ? (completedQuestions / totalQuestions) * 100 : 0;
        
        if (progressBar) progressBar.style.width = progress + '%';
        if (progressText) progressText.textContent = Math.round(progress) + '%';
        
        console.log('📊 Progresso atualizado:', Math.round(progress) + '%');
    }
    
    // Função para salvar progresso
    function saveProgress() {
        console.log('[DEBUG] saveProgress() chamada - Página 3');
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
                console.log('✅ Progresso salvo no banco de dados:', data.message);
            } else {
                console.error('❌ Erro ao salvar progresso:', data.error);
            }
        })
        .catch(error => {
            console.error('❌ Erro ao salvar progresso:', error);
        });
    }
    
    // Função para carregar progresso
    function loadProgress() {
        console.log('[DEBUG] loadProgress() chamada - Página 3');
        fetch('/pagina3/carregar-progresso/?pagina=pagina3')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.elementos.length > 0) {
                console.log('✅ Carregando progresso do banco de dados:', data.elementos);
                
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
    
    // Event listeners para checkboxes
    function addCheckboxListeners(checkboxes) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function(e) {
                console.log(`[DEBUG] Checkbox mudou para:`, e.target.checked);
                updateProgress();
                saveProgress();
                
                // Mostrar barra flutuante apenas quando marcar (não desmarcar)
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
    
    // Carregar progresso ao inicializar
    loadProgress();
    
    console.log('✅ Sistema de progresso inicializado!');
});
