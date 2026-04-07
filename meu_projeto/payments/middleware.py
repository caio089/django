"""
Middleware para verificação de acesso premium
Acesso somente para quem tem assinatura paga ativa.
"""
from django.shortcuts import redirect
from django.contrib import messages
from .views import verificar_acesso_premium
from home.models import Profile

class PremiumAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.premium_pages = [
            '/pagina1/', '/pagina2/', '/pagina3/', '/pagina4/',
            '/pagina5/', '/pagina6/', '/pagina7/',
            '/pag1/', '/pag2/', '/pag3/', '/pag4/',
            '/pag5/', '/pag6/', '/pag7/',
        ]
        self.excluded_urls = [
            '/payments/', '/login/', '/register/', '/admin/',
            '/dashboard/', '/django-admin/', '/static/', '/media/',
            '/index/', '/sucesso/', '/bem-vindo/', '/falha/',
            '/pendente/', '/quiz/api/',
        ]

    def __call__(self, request):
        if any(request.path.startswith(url) for url in self.excluded_urls):
            return self.get_response(request)

        is_premium_page = any(request.path.startswith(p) for p in self.premium_pages)
        if not is_premium_page:
            return self.get_response(request)

        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa fazer login para acessar esta página.')
            return redirect('login')

        try:
            request.user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=request.user,
                nome=request.user.get_full_name() or request.user.username or 'Usuário',
                idade=18, faixa='branca'
            )

        tem_acesso, assinatura = verificar_acesso_premium(request.user)
        if not tem_acesso:
            messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
            return redirect('payments:planos')

        request.assinatura = assinatura
        return self.get_response(request)
