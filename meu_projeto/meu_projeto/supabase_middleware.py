"""
Middleware para gerenciar conexões com Supabase
"""
import time
import logging
from django.db import connection
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

class SupabaseConnectionMiddleware:
    """
    Middleware para gerenciar conexões com Supabase de forma robusta
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.connection_retries = 3
        self.retry_delay = 2

    def __call__(self, request):
        # Fechar conexões antigas antes de cada requisição
        self.cleanup_connections()
        
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Erro na requisição: {e}")
            # Tentar reconectar se houver erro de conexão
            if "connection" in str(e).lower():
                self.handle_connection_error()
            raise e

    def cleanup_connections(self):
        """Limpa conexões antigas"""
        try:
            if connection.connection:
                connection.close()
        except Exception as e:
            logger.debug(f"Erro ao fechar conexão: {e}")

    def handle_connection_error(self):
        """Lida com erros de conexão"""
        for attempt in range(self.connection_retries):
            try:
                time.sleep(self.retry_delay * (attempt + 1))
                connection.ensure_connection()
                logger.info(f"Conexão restaurada na tentativa {attempt + 1}")
                return
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt == self.connection_retries - 1:
                    logger.error("Todas as tentativas de reconexão falharam")
                    raise e
