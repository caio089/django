"""
Middleware específico para Supabase em modo Session
Resolve o problema de MaxClientsInSessionMode
"""
import time
import threading
import logging
from django.db import connection, connections
from django.conf import settings

logger = logging.getLogger(__name__)

# Semáforo global para controlar conexões simultâneas
connection_semaphore = threading.Semaphore(3)  # Máximo 3 conexões simultâneas


class SupabaseSessionMiddleware:
    """
    Middleware para gerenciar conexões no modo Session do Supabase
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.active_connections = 0
        self.max_connections = getattr(settings, 'MAX_CONCURRENT_CONNECTIONS', 3)
        self.connection_lock = threading.Lock()

    def __call__(self, request):
        # Usar semáforo para limitar conexões simultâneas
        with connection_semaphore:
            try:
                # Fechar todas as conexões antes de processar
                self.force_close_all_connections()
                
                response = self.get_response(request)
                
                # Fechar todas as conexões após processar
                self.force_close_all_connections()
                
                return response
                
            except Exception as e:
                error_msg = str(e)
                if "MaxClientsInSessionMode" in error_msg:
                    logger.warning("Pool de conexões esgotado - aguardando liberação")
                    time.sleep(2)  # Aguardar 2 segundos
                    self.force_close_all_connections()
                    
                    # Tentar novamente apenas uma vez
                    try:
                        response = self.get_response(request)
                        self.force_close_all_connections()
                        return response
                    except:
                        raise e
                else:
                    raise e

    def force_close_all_connections(self):
        """Força fechamento de todas as conexões"""
        try:
            with self.connection_lock:
                # Fechar conexão padrão
                if hasattr(connection, 'close'):
                    connection.close()
                
                # Fechar todas as conexões
                for conn in connections.all():
                    if hasattr(conn, 'close'):
                        conn.close()
                    # Limpar estado interno
                    if hasattr(conn, '_connection'):
                        conn._connection = None
                        
        except Exception as e:
            logger.debug(f"Erro ao fechar conexões: {e}")


class SupabaseSessionConnectionManager:
    """
    Gerenciador de conexões para modo Session
    """
    def __init__(self):
        self.active_connections = 0
        self.max_connections = 3
        self.connection_history = []
        self.lock = threading.Lock()

    def acquire_connection(self):
        """Adquire uma conexão (com limite)"""
        with self.lock:
            if self.active_connections < self.max_connections:
                self.active_connections += 1
                self.connection_history.append(time.time())
                return True
            return False

    def release_connection(self):
        """Libera uma conexão"""
        with self.lock:
            if self.active_connections > 0:
                self.active_connections -= 1

    def get_stats(self):
        """Retorna estatísticas"""
        with self.lock:
            return {
                'active_connections': self.active_connections,
                'max_connections': self.max_connections,
                'utilization': (self.active_connections / self.max_connections) * 100
            }

    def cleanup_old_connections(self):
        """Limpa conexões antigas"""
        with self.lock:
            current_time = time.time()
            # Remover conexões mais antigas que 5 minutos
            self.connection_history = [
                t for t in self.connection_history 
                if current_time - t < 300
            ]
            # Ajustar contador se necessário
            if len(self.connection_history) < self.active_connections:
                self.active_connections = len(self.connection_history)


# Instância global do gerenciador
connection_manager = SupabaseSessionConnectionManager()
