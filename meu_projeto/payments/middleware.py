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
            '/static/',
            '/media/',
            '/index/',
            '/sucesso/',
            '/bem-vindo/',
            '/falha/',
            '/pendente/'
        ]
    
    def __call__(self, request):
        logger.info(f"[PremiumAccessMiddleware] Path={request.path}")
        print(f"[PremiumAccessMiddleware] Path={request.path}")

        # Bypass global: se usuário autenticado e trial ativo, liberar acesso a qualquer rota de conteúdo
        if request.user.is_authenticated:
            # Garantir profile e trial logo no início (funciona para qualquer rota)
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                logger.info("[PremiumAccessMiddleware] Profile inexistente, criando perfil padrão")
                print("[PremiumAccessMiddleware] Profile inexistente, criando perfil padrão")
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
                logger.info(f"[PremiumAccessMiddleware] Trial iniciado (global). inicio={profile.trial_inicio} fim={profile.trial_fim}")
                print(f"[PremiumAccessMiddleware] Trial iniciado (global). inicio={profile.trial_inicio} fim={profile.trial_fim}")
            # Se trial ativo, seguir direto (libera conteúdo em qualquer rota)
            if (profile.trial_fim and timezone.now() < profile.trial_fim) or (
                profile.trial_inicio and timezone.now() < (profile.trial_inicio + timedelta(days=3))
            ):
                logger.info(f"[PremiumAccessMiddleware] Trial ativo (global). Liberando: {request.path}")
                print(f"[PremiumAccessMiddleware] Trial ativo (global). Liberando: {request.path}")
                return self.get_response(request)
        
        # Verificar se a URL está na lista de exclusões
        if any(request.path.startswith(url) for url in self.excluded_urls):
            logger.info(f"[PremiumAccessMiddleware] URL excluída: {request.path}")
            print(f"[PremiumAccessMiddleware] URL excluída: {request.path}")
            response = self.get_response(request)
            return response
        
        # Verificar se a página atual requer acesso premium
        if any(request.path.startswith(page) for page in self.premium_pages):
            # Verificar se usuário está logado
            if not request.user.is_authenticated:
                messages.warning(request, 'Você precisa fazer login para acessar esta página.')
                logger.info(f"[PremiumAccessMiddleware] Não autenticado. Redirecionando para login: {request.path}")
                print(f"[PremiumAccessMiddleware] Não autenticado. Redirecionando para login: {request.path}")
                return redirect('login')
            
            # Garantir profile e trial mínimos antes de qualquer checagem
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                logger.info("[PremiumAccessMiddleware] Profile inexistente (premium page), criando agora.")
                print("[PremiumAccessMiddleware] Profile inexistente (premium page), criando agora.")
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
                logger.info(f"[PremiumAccessMiddleware] Trial iniciado (premium page). inicio={profile.trial_inicio} fim={profile.trial_fim}")
                print(f"[PremiumAccessMiddleware] Trial iniciado (premium page). inicio={profile.trial_inicio} fim={profile.trial_fim}")
            
            # Se o trial estiver ativo, liberar imediatamente (fallback por início + 3 dias)
            if (profile.trial_fim and timezone.now() < profile.trial_fim) or (
                profile.trial_inicio and timezone.now() < (profile.trial_inicio + timedelta(days=3))
            ):
                request.assinatura = None
                response = self.get_response(request)
                logger.info(f"[PremiumAccessMiddleware] Trial ativo (premium page). Liberando: {request.path}")
                print(f"[PremiumAccessMiddleware] Trial ativo (premium page). Liberando: {request.path}")
                return response
            
            # Caso contrário, verificar assinatura premium
            tem_acesso, assinatura = verificar_acesso_premium(request.user)
        
            if not tem_acesso:
                # Se chegou aqui, não tem trial ativo nem assinatura válida
                messages.warning(request, 'Esta página requer assinatura premium. Escolha um plano para continuar.')
                logger.info(f"[PremiumAccessMiddleware] Sem trial/assinatura. Redirecionando planos: {request.path}")
                print(f"[PremiumAccessMiddleware] Sem trial/assinatura. Redirecionando planos: {request.path}")
                return redirect('payments:planos')
            
            # Adicionar assinatura ao contexto da requisição
            request.assinatura = assinatura
            logger.info(f"[PremiumAccessMiddleware] Acesso por assinatura ativo para {request.path}")
            print(f"[PremiumAccessMiddleware] Acesso por assinatura ativo para {request.path}")
        
        response = self.get_response(request)
        return response
