/**
 * Sistema de Progresso do Usuário
 * Gerencia o salvamento e carregamento do progresso em todas as seções
 */

class UserProgressManager {
    constructor() {
        this.userId = null;
        this.sessionId = null;
        this.progressData = null;
        this.autoSaveInterval = null;
        this.init();
    }

    init() {
        // Verificar se o usuário está logado
        this.checkUserLogin();
        
        // Carregar progresso existente
        this.loadUserProgress();
    }

    checkUserLogin() {
        // Verificar se há dados de usuário no localStorage
        const userData = localStorage.getItem('userData');
        if (userData) {
            const user = JSON.parse(userData);
            this.userId = user.id;
            this.createUserSession();
        }
    }

    async createUserSession() {
        try {
            const response = await fetch('/pricing/progress/create-session/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            const data = await response.json();
            if (data.success) {
                this.sessionId = data.session_id;
                console.log('Sessão criada:', this.sessionId);
            }
        } catch (error) {
            console.error('Erro ao criar sessão:', error);
        }
    }

    async loadUserProgress() {
        try {
            const response = await fetch('/pricing/progress/get/');
            const data = await response.json();
            
            if (data.success) {
                this.progressData = data;
                this.applyProgressToUI();
                console.log('Progresso carregado:', this.progressData);
            }
        } catch (error) {
            console.error('Erro ao carregar progresso:', error);
        }
    }

    applyProgressToUI() {
        if (!this.progressData) return;

        // Aplicar progresso das faixas
        if (this.progressData.faixas_progress) {
            this.progressData.faixas_progress.forEach(faixa => {
                this.updateFaixaProgress(faixa.faixa, faixa.progress_percentage);
            });
        }

        // Aplicar progresso do quiz
        if (this.progressData.quiz_progress) {
            this.updateQuizProgress(this.progressData.quiz_progress.progress_percentage);
        }

        // Aplicar progresso dos rolamentos
        if (this.progressData.rolamentos_progress) {
            this.updateRolamentosProgress(this.progressData.rolamentos_progress.progress_percentage);
        }
    }

    updateFaixaProgress(faixa, percentage) {
        // Encontrar elementos de progresso da faixa
        const progressElements = document.querySelectorAll(`[data-faixa="${faixa}"] .progress-bar`);
        progressElements.forEach(element => {
            element.style.width = `${percentage}%`;
            element.setAttribute('aria-valuenow', percentage);
            
            // Atualizar texto de porcentagem
            const percentageText = element.parentElement.querySelector('.progress-text');
            if (percentageText) {
                percentageText.textContent = `${percentage}%`;
            }
        });
    }

    updateQuizProgress(percentage) {
        const quizProgressElements = document.querySelectorAll('.quiz-progress-bar');
        quizProgressElements.forEach(element => {
            element.style.width = `${percentage}%`;
            element.setAttribute('aria-valuenow', percentage);
            
            const percentageText = element.parentElement.querySelector('.quiz-progress-text');
            if (percentageText) {
                percentageText.textContent = `${percentage}%`;
            }
        });
    }

    updateRolamentosProgress(percentage) {
        const rolamentosProgressElements = document.querySelectorAll('.rolamentos-progress-bar');
        rolamentosProgressElements.forEach(element => {
            element.style.width = `${percentage}%`;
            element.setAttribute('aria-valuenow', percentage);
            
            const percentageText = element.parentElement.querySelector('.rolamentos-progress-text');
            if (percentageText) {
                percentageText.textContent = `${percentage}%`;
            }
        });
    }

    async saveFaixaProgress(faixa, progressData) {
        try {
            const response = await fetch('/pricing/progress/save-faixa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    faixa: faixa,
                    ...progressData
                })
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('Progresso da faixa salvo:', data.progress);
            }
        } catch (error) {
            console.error('Erro ao salvar progresso da faixa:', error);
        }
    }

    async saveQuizProgress(quizData) {
        try {
            const response = await fetch('/pricing/progress/save-quiz/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(quizData)
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('Progresso do quiz salvo:', data.progress);
            }
        } catch (error) {
            console.error('Erro ao salvar progresso do quiz:', error);
        }
    }

    async saveRolamentosProgress(rolamentosData) {
        try {
            const response = await fetch('/pricing/progress/save-rolamentos/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(rolamentosData)
            });
            
            const data = await response.json();
            if (data.success) {
                console.log('Progresso dos rolamentos salvo:', data.progress);
            }
        } catch (error) {
            console.error('Erro ao salvar progresso dos rolamentos:', error);
        }
    }

    // Método simplificado para salvar progresso manualmente
    saveProgress(type, data) {
        switch(type) {
            case 'faixa':
                this.saveFaixaProgress(data.faixa, data);
                break;
            case 'quiz':
                this.saveQuizProgress(data);
                break;
            case 'rolamentos':
                this.saveRolamentosProgress(data);
                break;
        }
    }

    // Métodos auxiliares simplificados
    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    // Método para ser chamado quando o usuário faz login
    onUserLogin(userData) {
        this.userId = userData.id;
        localStorage.setItem('userData', JSON.stringify(userData));
        localStorage.setItem('sessionStartTime', Date.now().toString());
        this.createUserSession();
        this.loadUserProgress();
    }

    // Método para ser chamado quando o usuário faz logout
    onUserLogout() {
        this.userId = null;
        this.sessionId = null;
        this.progressData = null;
        localStorage.removeItem('userData');
    }
}

// Inicializar o gerenciador de progresso
const progressManager = new UserProgressManager();

// Exportar para uso global
window.progressManager = progressManager;
