"""
Middleware para otimizar conexões com o banco de dados Supabase
"""
from django.db import connection, connections
from django.core.cache import cache
import time
import logging
import psycopg2
from psycopg2 import OperationalError

logger = logging.getLogger(__name__)


class DatabaseOptimizationMiddleware:
    """
    Middleware para otimizar conexões com o banco de dados
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Fechar TODAS as conexões antes de processar a requisição
        self.force_close_all_connections()
        
        try:
            response = self.get_response(request)
        except (OperationalError, psycopg2.OperationalError) as e:
            logger.error(f"Erro de conexão: {e}")
            # Tentar fechar todas as conexões e recriar
            self.force_close_all_connections()
            response = self.get_response(request)
        finally:
            # Fechar TODAS as conexões após processar a requisição
            self.force_close_all_connections()
        
        return response
    
    def force_close_all_connections(self):
        """Forçar fechamento de todas as conexões"""
        try:
            # Fechar conexão padrão
            if hasattr(connection, 'close'):
                connection.close()
            
            # Fechar todas as conexões
            for conn in connections.all():
                if hasattr(conn, 'close'):
                    conn.close()
        except Exception as e:
            logger.debug(f"Erro ao fechar conexões: {e}")


class ConnectionPoolMiddleware:
    """
    Middleware ultra-agressivo para gerenciar pool de conexões Supabase
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.last_cleanup = time.time()
        self.retry_count = 0
        self.max_retries = 2  # Reduzir tentativas
        self.connection_count = 0

    def __call__(self, request):
        # Limpar conexões a cada 5 segundos (ultra-agressivo)
        current_time = time.time()
        if current_time - self.last_cleanup > 5:  # 5 segundos
            self.force_cleanup_all_connections()
            self.last_cleanup = current_time
        
        # Limpar conexões antes de cada requisição
        self.force_cleanup_all_connections()
        
        try:
            response = self.get_response(request)
            self.retry_count = 0  # Reset retry count on success
        except (OperationalError, psycopg2.OperationalError) as e:
            error_msg = str(e)
            if "MaxClientsInSessionMode" in error_msg:
                logger.error("Pool de conexões esgotado - forçando limpeza total")
                self.force_cleanup_all_connections()
                time.sleep(2)  # Aguardar mais tempo
                
                if self.retry_count < self.max_retries:
                    self.retry_count += 1
                    logger.info(f"Tentativa {self.retry_count} após limpeza total")
                    response = self.get_response(request)
                else:
                    logger.error("Máximo de tentativas atingido")
                    raise e
            else:
                logger.error(f"Erro de conexão: {e}")
                raise e
        finally:
            # Limpar conexões após cada requisição
            self.force_cleanup_all_connections()
        
        return response

    def force_cleanup_all_connections(self):
        """Limpeza ultra-agressiva de todas as conexões"""
        try:
            from django.db import connections, connection
            
            # Fechar conexão padrão
            if hasattr(connection, 'close'):
                connection.close()
            
            # Fechar todas as conexões
            for conn in connections.all():
                if hasattr(conn, 'close'):
                    conn.close()
                # Forçar fechamento de conexões internas
                if hasattr(conn, 'connection') and conn.connection:
                    try:
                        conn.connection.close()
                    except:
                        pass
                # Limpar estado interno
                if hasattr(conn, '_connection'):
                    conn._connection = None
                    
        except Exception as e:
            logger.debug(f"Erro na limpeza ultra-agressiva: {e}")

    def cleanup_connections(self):
        """Limpar conexões antigas de forma agressiva"""
        self.force_cleanup_all_connections()
