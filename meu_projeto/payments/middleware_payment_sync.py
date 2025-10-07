"""
Middleware para sincronização automática de status de pagamento
Garante que o status premium seja sempre atualizado
"""
from django.utils import timezone
from django.contrib.auth.models import User
from payments.models import Assinatura
from home.models import Profile
import logging

logger = logging.getLogger(__name__)

class PaymentSyncMiddleware:
    """
    Middleware que sincroniza automaticamente o status de pagamento
    Verifica e corrige inconsistências entre assinaturas e perfis
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Cache para evitar verificações repetidas na mesma sessão
        self._sync_cache = {}
    
    def __call__(self, request):
        # Sincronizar status apenas para usuários autenticados
        if request.user.is_authenticated:
            self.sync_user_payment_status(request.user)
        
        response = self.get_response(request)
        return response
    
    def sync_user_payment_status(self, user):
        """
        Sincroniza o status de pagamento de um usuário
        """
        try:
            # Verificar se já foi sincronizado recentemente
            cache_key = f"sync_{user.id}"
            if cache_key in self._sync_cache:
                return
            
            # Marcar como sincronizado
            self._sync_cache[cache_key] = True
            
            # Verificar se tem assinatura ativa
            assinatura_ativa = Assinatura.objects.filter(
                usuario=user,
                status='ativa',
                data_vencimento__gt=timezone.now()
            ).first()
            
            # Verificar se tem perfil
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                # Criar perfil se não existir
                Profile.objects.create(
                    user=user,
                    nome=user.username,
                    idade=18,
                    faixa='branca'
                )
                profile = user.profile
                logger.info(f"Perfil criado para usuário {user.username}")
            
            # Determinar se deve ter acesso premium
            deve_ter_premium = assinatura_ativa is not None
            
            # Verificar se precisa atualizar
            precisa_atualizar = (
                profile.conta_premium != deve_ter_premium or
                (deve_ter_premium and assinatura_ativa and 
                 profile.data_vencimento_premium != assinatura_ativa.data_vencimento)
            )
            
            if precisa_atualizar:
                # Atualizar perfil
                profile.conta_premium = deve_ter_premium
                if assinatura_ativa:
                    profile.data_vencimento_premium = assinatura_ativa.data_vencimento
                else:
                    profile.data_vencimento_premium = None
                
                profile.save()
                
                logger.info(f"Status premium sincronizado para {user.username}: {deve_ter_premium}")
            
            # Verificar e corrigir assinaturas expiradas
            assinaturas_expiradas = Assinatura.objects.filter(
                usuario=user,
                status='ativa',
                data_vencimento__lt=timezone.now()
            )
            
            if assinaturas_expiradas.exists():
                for assinatura in assinaturas_expiradas:
                    assinatura.status = 'expirada'
                    assinatura.save()
                    logger.info(f"Assinatura expirada marcada para {user.username}")
                
                # Atualizar perfil se necessário
                if not Assinatura.objects.filter(
                    usuario=user,
                    status='ativa',
                    data_vencimento__gt=timezone.now()
                ).exists():
                    profile.conta_premium = False
                    profile.data_vencimento_premium = None
                    profile.save()
                    logger.info(f"Status premium removido para {user.username} (assinatura expirada)")
        
        except Exception as e:
            logger.error(f"Erro ao sincronizar status de pagamento para {user.username}: {e}")
    
    def clear_cache(self):
        """Limpa o cache de sincronização"""
        self._sync_cache.clear()
