"""
Middleware para verificação de acesso premium
Acesso somente para quem tem assinatura paga ativa.
"""
from django.shortcuts import redirect
from django.contrib import messages
from .views import verificar_acesso_premium
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
            '/pag1/','/pag2/','/pag3/','/pag4/','/pag5/','/pag6/','/pag7/',
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
            '/dashboard/',
            '/django-admin/',
            '/static/',
            '/media/',
            '/index/',
            '/sucesso/',
            '/bem-vindo/',
            '/falha/',
            '/pendente/',
            '/quiz/api/',  # ranking e submit públicos (sem login)
        ]
    
    def __call__(self, request):
        # Bypass global: se usuário autenticado e tem assinatura paga ativa, liberar acesso
        if request.user.is_authenticated:
            tem_acesso, _ = verificar_acesso_premium(request.user)
            if tem_acesso:
                return self.get_response(request)
        
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
            
            # Garantir profile mínimo
            try:
                request.user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(
                    user=request.user,
                    nome=request.user.get_full_name() or request.user.username or (request.user.email if hasattr(request.user, "email") else "Usuário"),
                    idade=18,
                    faixa='branca'
                )
            
            # Verificar assinatura premium (acesso somente para quem pagou)
            tem_acesso, assinatura = verificar_acesso_premium(request.user)
        
            if not tem_acesso:
                messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
                return redirect('payments:planos')
            
            # Adicionar assinatura ao contexto da requisição
            request.assinatura = assinatura
        
        response = self.get_response(request)
        return response
