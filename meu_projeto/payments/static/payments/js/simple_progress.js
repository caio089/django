/**
 * Sistema de Progresso Simplificado
 * Salva progresso apenas quando necessário, sem loops infinitos
 */

class SimpleProgressManager {
    constructor() {
        this.userId = null;
        this.init();
    }

    init() {
        // Verificar se o usuário está logado
        this.checkUserLogin();
    }

    checkUserLogin() {
        const userData = localStorage.getItem('userData');
        if (userData) {
            const user = JSON.parse(userData);
            this.userId = user.id;
        }
    }

    // Método principal para salvar progresso
    async saveProgress(type, data) {
        if (!this.userId) {
            console.log('Usuário não logado, progresso não salvo');
            return;
        }

        try {
            let url = '';
            switch(type) {
                case 'faixa':
                    url = '/pricing/progress/save-faixa/';
                    break;
                case 'quiz':
                    url = '/pricing/progress/save-quiz/';
                    break;
                case 'rolamentos':
                    url = '/pricing/progress/save-rolamentos/';
                    break;
                default:
                    console.error('Tipo de progresso inválido:', type);
                    return;
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            if (result.success) {
                console.log('Progresso salvo:', type, result.progress);
            } else {
                console.error('Erro ao salvar progresso:', result.message);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
        }
    }

    // Carregar progresso do usuário
    async loadProgress() {
        if (!this.userId) return;

        try {
            const response = await fetch('/pricing/progress/get/');
            const data = await response.json();
            
            if (data.success) {
                this.applyProgressToUI(data);
                console.log('Progresso carregado:', data);
            }
        } catch (error) {
            console.error('Erro ao carregar progresso:', error);
        }
    }

    // Aplicar progresso na interface
    applyProgressToUI(data) {
        // Aplicar progresso das faixas
        if (data.faixas_progress) {
            data.faixas_progress.forEach(faixa => {
                this.updateProgressBar(`[data-faixa="${faixa.faixa}"] .progress-bar`, faixa.progress_percentage);
            });
        }

        // Aplicar progresso do quiz
        if (data.quiz_progress) {
            this.updateProgressBar('.quiz-progress-bar', data.quiz_progress.progress_percentage);
        }

        // Aplicar progresso dos rolamentos
        if (data.rolamentos_progress) {
            this.updateProgressBar('.rolamentos-progress-bar', data.rolamentos_progress.progress_percentage);
        }
    }

    // Atualizar barra de progresso
    updateProgressBar(selector, percentage) {
        const element = document.querySelector(selector);
        if (element) {
            element.style.width = `${percentage}%`;
            element.setAttribute('aria-valuenow', percentage);
            
            // Atualizar texto de porcentagem
            const textElement = element.parentElement.querySelector('.progress-text');
            if (textElement) {
                textElement.textContent = `${percentage}%`;
            }
        }
    }

    // Métodos específicos para cada tipo
    saveFaixaProgress(faixa, percentage, timeSpent = 0) {
        this.saveProgress('faixa', {
            faixa: faixa,
            progress_percentage: percentage,
            time_spent: timeSpent,
            lessons_completed: Math.floor(percentage / 10),
            total_lessons: 10
        });
    }

    saveQuizProgress(percentage, correctAnswers = 0, totalQuestions = 0) {
        this.saveProgress('quiz', {
            total_questions: totalQuestions,
            correct_answers: correctAnswers,
            wrong_answers: totalQuestions - correctAnswers,
            time_spent: 0
        });
    }

    saveRolamentosProgress(percentage, completed = 0, total = 0) {
        this.saveProgress('rolamentos', {
            total_rolamentos: total,
            completed_rolamentos: completed,
            time_spent: 0,
            current_rolamento: `Rolamento ${completed}`
        });
    }

    // Login/Logout
    onUserLogin(userData) {
        this.userId = userData.id;
        localStorage.setItem('userData', JSON.stringify(userData));
        this.loadProgress();
    }

    onUserLogout() {
        this.userId = null;
        localStorage.removeItem('userData');
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }
}

// Inicializar o gerenciador simplificado
const simpleProgress = new SimpleProgressManager();

// Exportar para uso global
window.simpleProgress = simpleProgress;
