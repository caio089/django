"""
Middleware otimizado para Supabase Pro - aproveita melhor o plano pago
Sistema anti-hibernação com keep-alive automático
"""
import time
import threading
import logging
from django.db import connection, connections
from django.conf import settings
from .supabase_keepalive import start_supabase_keepalive, get_supabase_status

logger = logging.getLogger(__name__)


class SupabaseProMiddleware:
    """
    Middleware otimizado para Supabase Pro - gerencia conexões de forma inteligente
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.connection_pool = {}
        self.last_cleanup = time.time()
        self.max_connections = 20  # Aproveitar limite do plano Pro
        self.connection_timeout = 300  # 5 minutos
        self.keep_alive_started = False
        
        # Iniciar keep-alive automaticamente
        if not self.keep_alive_started:
            try:
                start_supabase_keepalive()
                self.keep_alive_started = True
                logger.info("🚀 Keep-alive automático iniciado")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao iniciar keep-alive: {e}")

    def __call__(self, request):
        # Limpeza inteligente a cada 30 segundos (menos agressiva)
        current_time = time.time()
        if current_time - self.last_cleanup > 30:
            self.smart_cleanup()
            self.last_cleanup = current_time
        
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            error_msg = str(e)
            if "MaxClientsInSessionMode" in error_msg:
                logger.warning("Pool esgotado - limpando conexões antigas")
                self.force_cleanup_old_connections()
                # Tentar novamente apenas uma vez
                try:
                    response = self.get_response(request)
                    return response
                except:
                    raise e
            else:
                raise e

    def smart_cleanup(self):
        """Limpeza inteligente - remove apenas conexões antigas"""
        try:
            current_time = time.time()
            for conn_name, conn_info in list(self.connection_pool.items()):
                if current_time - conn_info['last_used'] > self.connection_timeout:
                    self.close_connection(conn_name)
                    del self.connection_pool[conn_name]
        except Exception as e:
            logger.debug(f"Erro na limpeza inteligente: {e}")

    def force_cleanup_old_connections(self):
        """Força limpeza de conexões antigas"""
        try:
            # Fechar apenas conexões antigas (mais de 2 minutos)
            current_time = time.time()
            for conn in connections.all():
                if hasattr(conn, 'connection') and conn.connection:
                    # Verificar se a conexão é antiga
                    if hasattr(conn, '_last_used'):
                        if current_time - conn._last_used > 120:  # 2 minutos
                            conn.close()
                    else:
                        conn._last_used = current_time
        except Exception as e:
            logger.debug(f"Erro na limpeza forçada: {e}")

    def close_connection(self, conn_name):
        """Fecha uma conexão específica"""
        try:
            if conn_name in connections:
                connections[conn_name].close()
        except Exception as e:
            logger.debug(f"Erro ao fechar conexão {conn_name}: {e}")


class SupabaseProConnectionPool:
    """
    Pool de conexões otimizado para Supabase Pro
    """
    def __init__(self):
        self.max_connections = 20
        self.active_connections = 0
        self.connection_history = []

    def get_connection(self):
        """Obtém uma conexão do pool"""
        if self.active_connections < self.max_connections:
            self.active_connections += 1
            self.connection_history.append(time.time())
            return True
        return False

    def release_connection(self):
        """Libera uma conexão do pool"""
        if self.active_connections > 0:
            self.active_connections -= 1

    def get_stats(self):
        """Retorna estatísticas do pool"""
        return {
            'active_connections': self.active_connections,
            'max_connections': self.max_connections,
            'utilization': (self.active_connections / self.max_connections) * 100
        }
