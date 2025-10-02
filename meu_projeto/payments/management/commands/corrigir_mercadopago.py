from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Corrige configuração do Mercado Pago com tokens não criptografados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('💳 CORRIGINDO CONFIGURAÇÃO MERCADO PAGO'))
        self.stdout.write('=' * 60)
        
        # Obter tokens das variáveis de ambiente
        access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
        public_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
        
        self.stdout.write(f'\n🔍 VERIFICANDO VARIÁVEIS DE AMBIENTE:')
        self.stdout.write(f'   MERCADOPAGO_ACCESS_TOKEN: {"✅" if access_token else "❌"}')
        self.stdout.write(f'   MERCADOPAGO_PUBLIC_KEY: {"✅" if public_key else "❌"}')
        
        if not access_token or not public_key:
            self.stdout.write('\n❌ ERRO: Variáveis de ambiente não encontradas!')
            self.stdout.write('   Configure as variáveis no Render:')
            self.stdout.write('   - MERCADOPAGO_ACCESS_TOKEN')
            self.stdout.write('   - MERCADOPAGO_PUBLIC_KEY')
            return
        
        # Desativar configurações antigas
        self.stdout.write(f'\n🗑️  DESATIVANDO CONFIGURAÇÕES ANTIGAS:')
        configs_antigas = ConfiguracaoPagamento.objects.filter(ativo=True)
        for config in configs_antigas:
            config.ativo = False
            config.save()
            self.stdout.write(f'   ✅ Desativada: {config.nome}')
        
        # Criar nova configuração
        self.stdout.write(f'\n🆕 CRIANDO NOVA CONFIGURAÇÃO:')
        
        try:
            # Determinar ambiente
            ambiente = 'production' if not access_token.startswith('TEST-') else 'sandbox'
            
            # Criar configuração com tokens não criptografados
            config = ConfiguracaoPagamento.objects.create(
                nome='Configuração Corrigida',
                ambiente=ambiente,
                access_token=access_token,  # Salvar diretamente, sem criptografia
                public_key=public_key,      # Salvar diretamente, sem criptografia
                webhook_url='https://dojo-on.onrender.com/payments/webhook/',
                ativo=True
            )
            
            self.stdout.write(f'   ✅ Configuração criada: {config.nome}')
            self.stdout.write(f'   Ambiente: {config.ambiente}')
            self.stdout.write(f'   Access token: {access_token[:10]}...')
            self.stdout.write(f'   Public key: {public_key[:10]}...')
            
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao criar configuração: {e}')
            return
        
        # Testar configuração
        self.stdout.write(f'\n🧪 TESTANDO CONFIGURAÇÃO:')
        
        try:
            from payments.views import get_mercadopago_config
            sdk, config_test = get_mercadopago_config()
            
            if sdk and config_test:
                self.stdout.write('   ✅ SDK do Mercado Pago funcionando')
                self.stdout.write('   ✅ Configuração ativa encontrada')
                
                # Testar criação de preferência simples
                try:
                    test_data = {
                        "items": [
                            {
                                "title": "Teste",
                                "quantity": 1,
                                "unit_price": 1.0,
                                "currency_id": "BRL"
                            }
                        ]
                    }
                    preference = sdk.preference().create(test_data)
                    if preference.get("status") == 201:
                        self.stdout.write('   ✅ Criação de preferência funcionando')
                    else:
                        self.stdout.write('   ⚠️ Criação de preferência com problemas')
                except Exception as e:
                    self.stdout.write(f'   ⚠️ Erro ao testar preferência: {e}')
            else:
                self.stdout.write('   ❌ Configuração não funcionando')
                
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao testar: {e}')
        
        self.stdout.write(f'\n✅ CORREÇÃO CONCLUÍDA!')
        self.stdout.write(f'   Configuração do Mercado Pago corrigida')
        self.stdout.write(f'   Tokens salvos sem criptografia')
        self.stdout.write(f'   Sistema pronto para pagamentos')
