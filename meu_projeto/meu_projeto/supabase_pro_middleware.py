"""
Middleware para Supabase Pro - keep-alive automático
"""
import logging
from django.db import connection, connections
from .supabase_keepalive import start_supabase_keepalive

logger = logging.getLogger(__name__)


class SupabaseProMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            start_supabase_keepalive()
        except Exception as e:
            logger.warning(f"Erro ao iniciar keep-alive: {e}")

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            if "MaxClientsInSessionMode" in str(e):
                logger.warning("Pool esgotado - fechando conexões")
                for conn in connections.all():
                    conn.close()
                return self.get_response(request)
            raise
