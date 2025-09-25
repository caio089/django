from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.conf import settings
from .models import UserSubscription

class PaymentMiddleware:
    """
    Middleware para controlar acesso baseado em status de pagamento
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que requerem pagamento
        self.premium_urls = [
            '/pagina1/',
            '/pagina2/', 
            '/pagina3/',
            '/pagina4/',
            '/pagina5/',
            '/pagina6/',
            '/pagina7/',
            '/quiz/',
            '/ukemis/',
            '/historia/',
            '/palavras/',
            '/regras/',
        ]
        
        # URLs que não requerem pagamento
        self.free_urls = [
            '/',
            '/login/',
            '/register/',
            '/pricing/',
            '/checkout/',
            '/success/',
            '/cancel/',
            '/access-denied/',
            '/admin/',
            '/logout/',
        ]
    
    def __call__(self, request):
        # Verificar se o usuário está autenticado
        if request.user.is_authenticated:
            # Verificar se a URL requer pagamento
            if self.requires_payment(request.path):
                # Verificar se o usuário tem pagamento ativo
                if not self.has_active_payment(request.user):
                    # Redirecionar para página de preços em vez de acesso negado
                    return redirect('pricing')
        
        response = self.get_response(request)
        return response
    
    def requires_payment(self, path):
        """Verifica se a URL requer pagamento"""
        # Verificar se é uma URL premium
        for premium_url in self.premium_urls:
            if path.startswith(premium_url):
                return True
        
        # Verificar se não é uma URL gratuita
        for free_url in self.free_urls:
            if path.startswith(free_url):
                return False
        
        return False
    
    def has_active_payment(self, user):
        """
        Verifica se o usuário tem pagamento ativo
        """
        # Se estiver em modo de desenvolvimento, sempre redireciona para página de preços
        if getattr(settings, 'DEVELOPMENT_MODE', True):
            return False
        
        # Código para produção
        try:
            subscription = UserSubscription.objects.get(user=user)
            return subscription.is_valid()
        except UserSubscription.DoesNotExist:
            return False
