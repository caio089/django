"""
Comando para monitorar e manter Supabase ativo
"""
import time
import logging
from django.core.management.base import BaseCommand
from django.db import connection
from meu_projeto.supabase_keepalive import start_supabase_keepalive, stop_supabase_keepalive, get_supabase_status

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Monitora e mantém Supabase ativo para evitar hibernação'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=300,
            help='Intervalo entre pings em segundos (padrão: 300 = 5 minutos)'
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Mostra apenas o status atual'
        )
        parser.add_argument(
            '--stop',
            action='store_true',
            help='Para o sistema de keep-alive'
        )
    
    def handle(self, *args, **options):
        if options['status']:
            self.show_status()
            return
            
        if options['stop']:
            self.stop_keepalive()
            return
            
        # Iniciar monitoramento
        self.start_monitoring(options['interval'])
    
    def show_status(self):
        """Mostra status atual do Supabase"""
        try:
            status = get_supabase_status()
            
            self.stdout.write("📊 Status do Supabase:")
            self.stdout.write(f"  Keep-alive ativo: {'✅' if status['keep_alive']['is_running'] else '❌'}")
            self.stdout.write(f"  Último ping: {status['keep_alive']['last_ping'] or 'Nunca'}")
            self.stdout.write(f"  Falhas: {status['keep_alive']['failed_pings']}")
            self.stdout.write(f"  Intervalo: {status['keep_alive']['interval']}s")
            
            health = status['connection_health']
            self.stdout.write(f"  Problemas totais: {health['total_issues']}")
            self.stdout.write(f"  Problemas recentes: {health['recent_issues']}")
            
            # Testar conexão atual
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    self.stdout.write("  Conexão atual: ✅ Ativa")
            except Exception as e:
                self.stdout.write(f"  Conexão atual: ❌ Erro: {e}")
                
        except Exception as e:
            self.stdout.write(f"❌ Erro ao obter status: {e}")
    
    def stop_keepalive(self):
        """Para o sistema de keep-alive"""
        try:
            stop_supabase_keepalive()
            self.stdout.write("🛑 Keep-alive parado com sucesso!")
        except Exception as e:
            self.stdout.write(f"❌ Erro ao parar keep-alive: {e}")
    
    def start_monitoring(self, interval):
        """Inicia o monitoramento contínuo"""
        self.stdout.write("🚀 Iniciando monitoramento do Supabase...")
        self.stdout.write(f"⏰ Intervalo: {interval} segundos")
        self.stdout.write("💡 Pressione Ctrl+C para parar")
        
        try:
            # Iniciar keep-alive
            start_supabase_keepalive()
            
            # Loop de monitoramento
            while True:
                try:
                    # Testar conexão
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT 1")
                    
                    self.stdout.write(f"✅ Ping bem-sucedido - {time.strftime('%H:%M:%S')}")
                    
                except Exception as e:
                    self.stdout.write(f"⚠️ Erro no ping: {e}")
                
                # Aguardar próximo ping
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write("\n🛑 Parando monitoramento...")
            stop_supabase_keepalive()
            self.stdout.write("✅ Monitoramento parado!")
        except Exception as e:
            self.stdout.write(f"❌ Erro no monitoramento: {e}")
            stop_supabase_keepalive()
