from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
from payments.views import get_mercadopago_config
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Verifica a configuração do Mercado Pago em produção'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Verificando configuracao do Mercado Pago...'))
        
        # Verificar configurações no banco
        total_configs = ConfiguracaoPagamento.objects.count()
        active_configs = ConfiguracaoPagamento.objects.filter(ativo=True).count()
        
        self.stdout.write(f'Configuracoes totais: {total_configs}')
        self.stdout.write(f'Configuracoes ativas: {active_configs}')
        
        if active_configs == 0:
            self.stdout.write(self.style.ERROR('Nenhuma configuracao ativa encontrada!'))
            self.stdout.write(self.style.WARNING('Para corrigir:'))
            self.stdout.write('1. Acesse o admin do Django')
            self.stdout.write('2. Va em Payments > Configuracoes de Pagamento')
            self.stdout.write('3. Marque uma configuracao como "Ativo"')
            return
        
        # Listar configurações ativas
        configs = ConfiguracaoPagamento.objects.filter(ativo=True)
        for config in configs:
            self.stdout.write(f'Configuracao ID {config.id}:')
            self.stdout.write(f'   Ambiente: {config.ambiente}')
            self.stdout.write(f'   Usage Count: {config.usage_count}')
            self.stdout.write(f'   Ultima Atualizacao: {config.data_atualizacao}')
            
            # Testar access token
            try:
                access_token = config.get_access_token()
                if access_token:
                    self.stdout.write(f'   Access Token: {access_token[:20]}...')
                else:
                    self.stdout.write(f'   Access Token: Nao pode ser obtido')
            except Exception as e:
                self.stdout.write(f'   Erro ao obter Access Token: {e}')
        
        # Testar função get_mercadopago_config
        self.stdout.write('\nTestando funcao get_mercadopago_config...')
        try:
            sdk, config = get_mercadopago_config()
            if sdk and config:
                self.stdout.write(self.style.SUCCESS('Configuracao funcionando corretamente!'))
                self.stdout.write(f'   SDK: {type(sdk).__name__}')
                self.stdout.write(f'   Config: ID {config.id}')
            else:
                self.stdout.write(self.style.ERROR('Configuracao nao esta funcionando'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao testar configuracao: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
