// Lazy Loading Otimizado para Vídeos - Intersection Observer
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se o dispositivo é mobile
    const isMobile = window.innerWidth <= 768;
    
    if (!isMobile) {
        // Desktop: todos os vídeos podem carregar normalmente
        return;
    }
    
    // Mobile: usar Intersection Observer para carregar vídeos apenas quando visíveis
    const videoContainers = document.querySelectorAll('.video-container iframe');
    
    // Configurar Intersection Observer
    const observerOptions = {
        root: null,
        rootMargin: '50px', // Começar a carregar 50px antes de entrar na tela
        threshold: 0.1
    };
    
    const videoObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = entry.target;
                
                // Se o iframe ainda não tem src (foi removido), restaurar
                if (!iframe.src && iframe.dataset.src) {
                    iframe.src = iframe.dataset.src;
                }
                
                // Parar de observar este vídeo
                observer.unobserve(iframe);
            }
        });
    }, observerOptions);
    
    // Para cada vídeo, salvar o src e observar
    videoContainers.forEach((iframe, index) => {
        // Manter os primeiros 2 vídeos carregados imediatamente
        if (index < 2) {
            return;
        }
        
        // Para os demais, preparar para lazy loading
        if (iframe.src) {
            iframe.dataset.src = iframe.src;
            iframe.removeAttribute('src');
        }
        
        // Observar o iframe
        videoObserver.observe(iframe);
    });
    
    console.log('✅ Lazy loading de vídeos ativado para mobile (' + videoContainers.length + ' vídeos)');
});

