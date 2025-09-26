from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento
import mercadopago
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug da configuração do Mercado Pago'

    def handle(self, *args, **options):
        """
        Debug da configuração do Mercado Pago
        """
        try:
            # Obter configuração ativa
            config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            
            if not config:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Nenhuma configuração ativa do Mercado Pago encontrada.'
                    )
                )
                return

            # Obter credenciais
            access_token = config.get_access_token()
            public_key = config.get_public_key()
            
            self.stdout.write(f'🔍 DEBUG - Configuração:')
            self.stdout.write(f'   ID: {config.id}')
            self.stdout.write(f'   Ambiente: {config.ambiente}')
            self.stdout.write(f'   Access Token: {access_token[:20] + "..." if access_token else "Não encontrado"}')
            self.stdout.write(f'   Public Key: {public_key[:20] + "..." if public_key else "Não encontrado"}')
            self.stdout.write(f'   Webhook URL: {config.webhook_url}')
            
            if not access_token:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Access token não encontrado ou não pode ser descriptografado.'
                    )
                )
                return

            # Testar inicialização do SDK
            self.stdout.write('\n🔄 Testando inicialização do SDK...')
            try:
                sdk = mercadopago.SDK(access_token)
                self.stdout.write('✅ SDK inicializado com sucesso')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao inicializar SDK: {e}')
                )
                return

            # Testar criação de preferência simples
            self.stdout.write('\n🔄 Testando criação de preferência simples...')
            try:
                preference_data = {
                    "items": [
                        {
                            "title": "Teste Debug",
                            "description": "Teste de debug do sistema",
                            "quantity": 1,
                            "unit_price": 1.00,
                            "currency_id": "BRL"
                        }
                    ],
                    "back_urls": {
                        "success": "http://127.0.0.1:8000/payments/success/",
                        "failure": "http://127.0.0.1:8000/payments/failure/",
                        "pending": "http://127.0.0.1:8000/payments/pending/"
                    },
                    "auto_return": "approved"
                }
                
                self.stdout.write(f'📋 Dados da preferência: {preference_data}')
                
                preference_result = sdk.preference().create(preference_data)
                self.stdout.write(f'📋 Resultado: {preference_result}')
                
                if preference_result["status"] == 201:
                    preference = preference_result["response"]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Preferência criada com sucesso!\n'
                            f'   ID: {preference.get("id")}\n'
                            f'   Status: {preference_result["status"]}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Erro ao criar preferência:\n'
                            f'   Status: {preference_result["status"]}\n'
                            f'   Response: {preference_result.get("response", {})}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao criar preferência: {e}')
                )
                import traceback
                self.stdout.write(f'Traceback: {traceback.format_exc()}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro geral: {e}')
            )
            import traceback
            self.stdout.write(f'Traceback: {traceback.format_exc()}')

