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
        """
        try:
            # Importar signals para auto-sincronização
            from . import signals
            
            # Importar e executar sincronização de inicialização
            from .startup_sync import StartupPaymentSync
            StartupPaymentSync.run_automatic_sync()
            
            # Iniciar sincronização periódica
            from .signals import PeriodicSyncManager
            PeriodicSyncManager.start_periodic_sync()
            
            # Iniciar monitor automático
            from .auto_monitor import AutoMonitor
            AutoMonitor.start_monitoring()
            
            # Iniciar notificações automáticas
            from .auto_notifications import AutoNotificationManager
            # Enviar relatório inicial
            AutoNotificationManager.send_system_health_report()
            
            logger.info("🚀 Sistema de pagamentos inicializado com sincronização automática completa")
            
        except Exception as e:
            logger.error(f"Erro na inicialização automática de pagamentos: {e}")