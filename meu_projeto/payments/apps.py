"""
Configuração do app payments com inicialização automática
"""
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    verbose_name = 'Sistema de Pagamentos'
    
    def ready(self):
        """
        Executa sincronização automática quando o Django inicia
        NOTA: Evita acessar DB durante ready() - executa em thread separada
        """
        # Só executar sincronizações se não estiver em migrations/testes
        import sys
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv or 'test' in sys.argv:
            return
            
        try:
            # Importar signals para auto-sincronização
            from . import signals
            
            # Agendar sincronização para executar após inicialização completa
            import threading
            
            def delayed_startup():
                """Executa tarefas de inicialização em thread separada"""
                try:
                    from django.conf import settings
                    
                    # Verificar se processos pesados estão desabilitados
                    if getattr(settings, 'DISABLE_HEAVY_PROCESSES', False):
                        logger.info("Processos pesados desabilitados - modo leve ativado")
                        return
                    
                    from .startup_sync import StartupPaymentSync
                    StartupPaymentSync.run_automatic_sync()
                    
                    from .signals import PeriodicSyncManager
                    PeriodicSyncManager.start_periodic_sync()
                    
                    from .auto_monitor import AutoMonitor
                    AutoMonitor.start_monitoring()
                    
                    from .auto_notifications import AutoNotificationManager
                    AutoNotificationManager.send_system_health_report()
                    
                    logger.info("Sistema de pagamentos inicializado com sucesso")
                except Exception as e:
                    logger.error(f"Erro na inicialização de pagamentos: {e}")
            
            # Executar em thread separada para não bloquear a inicialização
            thread = threading.Thread(target=delayed_startup, daemon=True)
            thread.start()
            
        except Exception as e:
            logger.error(f"Erro ao agendar inicialização de pagamentos: {e}")