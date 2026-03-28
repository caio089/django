"""
Middleware para sincronização automática de status de pagamento
"""
import time
from django.utils import timezone
from payments.models import Assinatura
from home.models import Profile
import logging

logger = logging.getLogger(__name__)

SYNC_TTL_SECONDS = 300  # re-sync a cada 5 minutos


class PaymentSyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._sync_cache = {}

    def __call__(self, request):
        if request.user.is_authenticated:
            self._maybe_sync(request.user)
        return self.get_response(request)

    def _maybe_sync(self, user):
        now = time.monotonic()
        last = self._sync_cache.get(user.id)
        if last and (now - last) < SYNC_TTL_SECONDS:
            return
        self._sync_cache[user.id] = now

        try:
            self._sync_user(user)
        except Exception as e:
            logger.error(f"Erro ao sincronizar pagamento para {user.username}: {e}")

    @staticmethod
    def _sync_user(user):
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(
                user=user, nome=user.username, idade=18, faixa='branca'
            )

        agora = timezone.now()

        expiradas = Assinatura.objects.filter(
            usuario=user, status='ativa', data_vencimento__lt=agora
        )
        if expiradas.exists():
            expiradas.update(status='expirada')

        assinatura_ativa = Assinatura.objects.filter(
            usuario=user, status='ativa', data_vencimento__gt=agora
        ).first()

        deve_premium = assinatura_ativa is not None
        precisa_atualizar = (
            profile.conta_premium != deve_premium or
            (deve_premium and profile.data_vencimento_premium != assinatura_ativa.data_vencimento)
        )

        if precisa_atualizar:
            profile.conta_premium = deve_premium
            profile.data_vencimento_premium = (
                assinatura_ativa.data_vencimento if assinatura_ativa else None
            )
            profile.save(update_fields=['conta_premium', 'data_vencimento_premium'])
