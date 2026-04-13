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
            
            # IMPORTANTE (Render): não iniciar loops/threads infinitos no web dyno.
            # Toda rotina pesada deve ser executada via job (cron/worker) explícito.
            logger.info("Payments ready: signals carregados; jobs pesados desativados no boot")
            
        except Exception as e:
            logger.error(f"Erro ao agendar inicialização de pagamentos: {e}")