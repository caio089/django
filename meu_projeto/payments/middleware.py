"""
Middleware para verificação de acesso premium
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from .views import verificar_acesso_premium
from django.utils import timezone
from datetime import timedelta
from home.models import Profile
import logging

logger = logging.getLogger(__name__)

class PremiumAccessMiddleware:
    """
    Middleware que verifica se o usuário tem acesso premium
    para páginas que requerem assinatura
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Páginas que requerem acesso premium
        self.premium_pages = [
            '/pagina1/',
            '/pagina2/', 
            '/pagina3/',
            '/pagina4/',
            '/pagina5/',
            '/pagina6/',
            '/pagina7/',
            '/quiz/',
            '/ukemis/',
            '/palavras/',
            '/historia/',
            '/regras/'
        ]
        
        # URLs que NÃO devem ser interceptadas pelo middleware
        self.excluded_urls = [
            '/payments/',
            '/login/',
            '/register/',
            '/admin/',
            '/static/',
            '/media/',
            '/',
            '/index/',
            '/sucesso/',
            '/bem-vindo/',
            '/falha/',
            '/pendente/'
        ]
    
    def __call__(self, request):
        # Verificar se a URL está na lista de exclusões
        if any(request.path.startswith(url) for url in self.excluded_urls):
            response = self.get_response(request)
            return response
        
        # Verificar se a página atual requer acesso premium
        if any(request.path.startswith(page) for page in self.premium_pages):
            # Verificar se usuário está logado
            if not request.user.is_authenticated:
                messages.warning(request, 'Você precisa fazer login para acessar esta página.')
                return redirect('login')
            
            # Verificar acesso premium
            tem_acesso, assinatura = verificar_acesso_premium(request.user)
            
            if not tem_acesso:
                # Fallback: garantir trial ativo direto no middleware (robustez extra)
                try:
                    profile = request.user.profile
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(
                        user=request.user,
                        nome=request.user.get_full_name() or request.user.username or (request.user.email if hasattr(request.user, "email") else "Usuário"),
                        idade=18,
                        faixa='branca'
                    )
                if not getattr(profile, "trial_inicio", None):
                    now = timezone.now()
                    profile.trial_inicio = now
                    profile.trial_fim = now + timedelta(days=3)
                    profile.save(update_fields=["trial_inicio", "trial_fim"])
                # Se trial estiver ativo, permitir acesso
                if getattr(profile, "is_trial_ativo", None) and profile.is_trial_ativo():
                    request.assinatura = None
                else:
                    messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
                    return redirect('payments:planos')
            
            # Adicionar assinatura ao contexto da requisição
            request.assinatura = assinatura
        
        response = self.get_response(request)
        return response
