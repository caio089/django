"""
Configurações específicas para otimizar conexões com Supabase
"""
import os
import logging
from django.db import connections
from django.core.cache import cache

logger = logging.getLogger(__name__)


class SupabaseConnectionManager:
    """
    Gerenciador de conexões Supabase com retry automático
    """
    
    @staticmethod
    def get_optimized_database_config():
        """
        Retorna configuração otimizada para Supabase
        """
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return None
            
        # Configurações otimizadas para Supabase
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 30,
                'application_name': 'django_app',
                'keepalives_idle': 600,
                'keepalives_interval': 30,
                'keepalives_count': 3,
                'tcp_keepalives_idle': 600,
                'tcp_keepalives_interval': 30,
                'tcp_keepalives_count': 3,
                # Configurações de retry
                'options': '-c statement_timeout=30000 -c idle_in_transaction_session_timeout=300000'
            },
            'CONN_MAX_AGE': 0,  # Fechar conexões imediatamente
            'CONN_HEALTH_CHECKS': False,
        }
    
    @staticmethod
    def force_close_all_connections():
        """
        Força o fechamento de todas as conexões
        """
        try:
            for conn in connections.all():
                if hasattr(conn, 'close'):
                    conn.close()
                # Fechar conexões internas do psycopg2
                if hasattr(conn, 'connection') and conn.connection:
                    try:
                        conn.connection.close()
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Erro ao fechar conexões: {e}")
    
    @staticmethod
    def test_connection():
        """
        Testa a conexão com o banco
        """
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False


def get_supabase_retry_config():
    """
    Configurações de retry para Supabase
    """
    return {
        'max_retries': 3,
        'retry_delay': 1,  # segundos
        'backoff_factor': 2,
        'timeout': 30
    }
