"""
Sistema de Keep-Alive para Supabase Pro
Evita hibernação do banco de dados mantendo conexões ativas
"""
import os
import time
import threading
import logging
import requests
from django.db import connection, connections
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)

class SupabaseKeepAlive:
    """
    Sistema de Keep-Alive para manter Supabase ativo
    """
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.interval = 300  # 5 minutos
        self.last_ping = None
        self.failed_pings = 0
        self.max_failed_pings = 3
        
    def start(self):
        """Inicia o sistema de keep-alive"""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.thread.start()
        logger.info("✅ Sistema de Keep-Alive iniciado")
        
    def stop(self):
        """Para o sistema de keep-alive"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("❌ Sistema de Keep-Alive parado")
        
    def _keep_alive_loop(self):
        """Loop principal do keep-alive"""
        while self.is_running:
            try:
                self._ping_database()
                self._ping_supabase_health()
                self.last_ping = timezone.now()
                self.failed_pings = 0
                
            except Exception as e:
                self.failed_pings += 1
                logger.warning(f"⚠️ Keep-alive falhou ({self.failed_pings}/{self.max_failed_pings}): {e}")
                
                if self.failed_pings >= self.max_failed_pings:
                    logger.error("❌ Muitas falhas no keep-alive - tentando reconectar")
                    self._force_reconnect()
                    self.failed_pings = 0
            
            # Aguardar próximo ping
            time.sleep(self.interval)
    
    def _ping_database(self):
        """Faz ping no banco de dados"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    logger.debug("✅ Ping no banco bem-sucedido")
                else:
                    raise Exception("Ping retornou resultado vazio")
                    
        except Exception as e:
            logger.warning(f"⚠️ Erro no ping do banco: {e}")
            raise
    
    def _ping_supabase_health(self):
        """Faz ping no endpoint de saúde do Supabase"""
        try:
            # Tentar ping no endpoint de saúde do Supabase
            database_url = os.getenv('DATABASE_URL')
            if database_url and 'supabase' in database_url:
                # Extrair informações da URL
                import urllib.parse
                parsed = urllib.parse.urlparse(database_url)
                host = parsed.hostname
                
                if host:
                    # Tentar conectar na porta 5432 para verificar se está ativa
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    result = sock.connect_ex((host, 5432))
                    sock.close()
                    
                    if result == 0:
                        logger.debug("✅ Porta 5432 do Supabase ativa")
                    else:
                        raise Exception(f"Porta 5432 não responde (código: {result})")
                        
        except Exception as e:
            logger.warning(f"⚠️ Erro no ping do Supabase: {e}")
            # Não re-raise para não interromper o keep-alive do banco
    
    def _force_reconnect(self):
        """Força reconexão com o banco"""
        try:
            logger.info("🔄 Forçando reconexão com Supabase...")
            
            # Fechar todas as conexões
            for conn in connections.all():
                if hasattr(conn, 'close'):
                    conn.close()
                if hasattr(conn, 'connection') and conn.connection:
                    try:
                        conn.connection.close()
                    except:
                        pass
            
            # Limpar cache de conexões
            if hasattr(connections, '_databases'):
                connections._databases.clear()
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Testar nova conexão
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                logger.info("✅ Reconexão bem-sucedida")
                
        except Exception as e:
            logger.error(f"❌ Erro na reconexão: {e}")
    
    def get_status(self):
        """Retorna status do keep-alive"""
        return {
            'is_running': self.is_running,
            'last_ping': self.last_ping,
            'failed_pings': self.failed_pings,
            'interval': self.interval
        }


class SupabaseConnectionMonitor:
    """
    Monitor de conexões para detectar problemas
    """
    
    def __init__(self):
        self.connection_issues = []
        self.last_check = None
        
    def check_connection_health(self):
        """Verifica saúde das conexões"""
        try:
            start_time = time.time()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            response_time = time.time() - start_time
            
            if response_time > 5:  # Mais de 5 segundos
                self.connection_issues.append({
                    'timestamp': timezone.now(),
                    'issue': 'slow_response',
                    'response_time': response_time
                })
                logger.warning(f"⚠️ Resposta lenta do banco: {response_time:.2f}s")
            
            return True
            
        except Exception as e:
            self.connection_issues.append({
                'timestamp': timezone.now(),
                'issue': 'connection_error',
                'error': str(e)
            })
            logger.error(f"❌ Erro na verificação de saúde: {e}")
            return False
    
    def get_health_report(self):
        """Retorna relatório de saúde"""
        recent_issues = [
            issue for issue in self.connection_issues 
            if (timezone.now() - issue['timestamp']).total_seconds() < 3600  # Última hora
        ]
        
        return {
            'total_issues': len(self.connection_issues),
            'recent_issues': len(recent_issues),
            'last_check': self.last_check,
            'issues': recent_issues[-10:]  # Últimos 10 problemas
        }


# Instâncias globais
keep_alive = SupabaseKeepAlive()
connection_monitor = SupabaseConnectionMonitor()


def start_supabase_keepalive():
    """Inicia o keep-alive do Supabase"""
    if not keep_alive.is_running:
        keep_alive.start()
        logger.info("🚀 Keep-alive do Supabase iniciado")


def stop_supabase_keepalive():
    """Para o keep-alive do Supabase"""
    if keep_alive.is_running:
        keep_alive.stop()
        logger.info("🛑 Keep-alive do Supabase parado")


def get_supabase_status():
    """Retorna status completo do Supabase"""
    return {
        'keep_alive': keep_alive.get_status(),
        'connection_health': connection_monitor.get_health_report()
    }


# Comando de gerenciamento para iniciar keep-alive
class Command(BaseCommand):
    help = 'Inicia o sistema de keep-alive do Supabase'
    
    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando keep-alive do Supabase...")
        start_supabase_keepalive()
        self.stdout.write("✅ Keep-alive iniciado com sucesso!")
        
        # Manter o comando rodando
        try:
            while True:
                time.sleep(60)
                status = get_supabase_status()
                self.stdout.write(f"📊 Status: {status}")
        except KeyboardInterrupt:
            self.stdout.write("🛑 Parando keep-alive...")
            stop_supabase_keepalive()
            self.stdout.write("✅ Keep-alive parado!")
