/**
 * JavaScript otimizado para login
 * Versão: 1.0
 * Otimizações: Cache de elementos, IIFE, event delegation, performance
 */
(function() {
    'use strict';
    
    // Cache de elementos DOM para melhor performance
    const elements = {
        togglePassword: null,
        senhaInput: null,
        form: null,
        loginBtn: null,
        loginBtnText: null,
        loginSpinner: null,
        criarContaLink: null,
        fazerLoginLink: null
    };
    
    // Configurações
    const config = {
        passwordToggleSelector: '#togglePassword',
        senhaInputSelector: '#senha',
        formSelector: '#login-form',
        loginBtnSelector: '#login-btn',
        loginBtnTextSelector: '#login-btn-text',
        loginSpinnerSelector: '#login-spinner',
        criarContaLinkSelector: '#criar-conta-link',
        fazerLoginLinkSelector: '#fazer-login-link'
    };
    
    // Inicializar elementos DOM uma única vez
    function initElements() {
        elements.togglePassword = document.querySelector(config.passwordToggleSelector);
        elements.senhaInput = document.querySelector(config.senhaInputSelector);
        elements.form = document.querySelector(config.formSelector);
        elements.loginBtn = document.querySelector(config.loginBtnSelector);
        elements.loginBtnText = document.querySelector(config.loginBtnTextSelector);
        elements.loginSpinner = document.querySelector(config.loginSpinnerSelector);
        elements.criarContaLink = document.querySelector(config.criarContaLinkSelector);
        elements.fazerLoginLink = document.querySelector(config.fazerLoginLinkSelector);
    }
    
    // Toggle de senha otimizado
    function initPasswordToggle() {
        if (elements.togglePassword && elements.senhaInput) {
            elements.togglePassword.addEventListener('click', function(e) {
                e.preventDefault();
                
                const isPassword = elements.senhaInput.type === 'password';
                elements.senhaInput.type = isPassword ? 'text' : 'password';
                
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('fa-eye');
                    icon.classList.toggle('fa-eye-slash');
                }
            });
        }
    }
    
    // Loading do formulário otimizado
    function initFormLoading() {
        if (elements.form) {
            elements.form.addEventListener('submit', function() {
                // Usar requestAnimationFrame para melhor performance
                requestAnimationFrame(function() {
                    if (elements.loginBtn) {
                        elements.loginBtn.disabled = true;
                        elements.loginBtn.setAttribute('aria-disabled', 'true');
                        
                        if (elements.loginBtnText) {
                            elements.loginBtnText.style.display = 'none';
                        }
                        
                        if (elements.loginSpinner) {
                            elements.loginSpinner.classList.remove('hidden');
                        }
                    }
                });
            });
        }
    }
    
    // Navegação otimizada com event delegation
    function initNavigation() {
        const navigationContainer = document.querySelector('.login-card');
        
        if (navigationContainer) {
            navigationContainer.addEventListener('click', function(e) {
                const target = e.target.closest('a');
                if (!target) return;
                
                const href = target.getAttribute('href');
                if (href && (href.includes('register') || href.includes('login'))) {
                    e.preventDefault();
                    window.location.href = href;
                }
            });
        }
    }
    
    // Validação básica de email (se necessário)
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Feedback visual otimizado
    function showFeedback(message, type = 'success') {
        const feedback = document.getElementById('login-feedback');
        if (!feedback) return;
        
        feedback.textContent = message;
        feedback.className = `fixed left-1/2 -translate-x-1/2 top-8 px-4 py-2 rounded-lg shadow-lg font-semibold text-xs transition-all duration-500 z-50`;
        
        const colorClass = type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white';
        feedback.classList.add(...colorClass.split(' '));
        
        feedback.style.opacity = '1';
        feedback.style.pointerEvents = 'auto';
        
        // Usar setTimeout com clearTimeout para evitar vazamentos
        const timeoutId = setTimeout(() => {
            feedback.style.opacity = '0';
            feedback.style.pointerEvents = 'none';
        }, 3000);
        
        // Limpar timeout se elemento for removido
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.removedNodes.length > 0) {
                    clearTimeout(timeoutId);
                    observer.disconnect();
                }
            });
        });
        observer.observe(document.body, { childList: true, subtree: true });
    }
    
    // Debounce para inputs (se necessário)
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Limpar erros quando usuário digita (otimizado)
    function initInputClearing() {
        const form = elements.form;
        if (!form) return;
        
        const clearError = debounce(function(e) {
            if (e.target.classList.contains('input')) {
                const fieldId = e.target.id;
                const errorDiv = document.getElementById(fieldId + '-error');
                if (errorDiv) {
                    errorDiv.style.display = 'none';
                }
                e.target.classList.remove('error');
            }
        }, 300);
        
        form.addEventListener('input', clearError);
    }
    
    // Inicialização principal otimizada
    function init() {
        try {
            initElements();
            initPasswordToggle();
            initFormLoading();
            initNavigation();
            initInputClearing();
            
            // Log de inicialização (apenas em desenvolvimento)
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                console.log('Login JS otimizado carregado com sucesso');
            }
        } catch (error) {
            console.error('Erro ao inicializar login JS:', error);
        }
    }
    
    // Executar quando DOM estiver pronto (otimizado)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM já está pronto
        init();
    }
    
    // Expor funções globais se necessário
    window.LoginJS = {
        showFeedback: showFeedback,
        validateEmail: validateEmail
    };
    
})();

