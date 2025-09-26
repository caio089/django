from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento
import mercadopago
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Testa a conexão com o Mercado Pago'

    def handle(self, *args, **options):
        """
        Testa a conexão com o Mercado Pago usando as credenciais configuradas
        """
        try:
            # Obter configuração ativa
            config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            
            if not config:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Nenhuma configuração ativa do Mercado Pago encontrada.\n'
                        'Execute: python manage.py configurar_mercadopago'
                    )
                )
                return

            # Obter credenciais
            access_token = config.get_access_token()
            public_key = config.get_public_key()
            
            if not access_token:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Access token não encontrado ou não pode ser descriptografado.'
                    )
                )
                return

            # Testar conexão com Mercado Pago
            self.stdout.write('🔄 Testando conexão com Mercado Pago...')
            
            try:
                # Inicializar SDK
                sdk = mercadopago.SDK(access_token)
                
                # Testar API - buscar informações da conta
                result = sdk.user().get()
                
                if result["status"] == 200:
                    user_info = result["response"]
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Conexão com Mercado Pago estabelecida com sucesso!\n'
                            f'   ID da Conta: {user_info.get("id", "N/A")}\n'
                            f'   Nome: {user_info.get("nickname", "N/A")}\n'
                            f'   Email: {user_info.get("email", "N/A")}\n'
                            f'   País: {user_info.get("country_id", "N/A")}\n'
                            f'   Ambiente: {config.ambiente}\n'
                            f'   Public Key: {public_key[:20]}...' if public_key else 'N/A'
                        )
                    )
                    
                    # Testar criação de preferência (opcional)
                    self.stdout.write('\n🔄 Testando criação de preferência de teste...')
                    
                    preference_data = {
                        "items": [
                            {
                                "title": "Teste de Conexão",
                                "description": "Teste de integração com Mercado Pago",
                                "quantity": 1,
                                "unit_price": 1.00,
                                "currency_id": "BRL"
                            }
                        ],
                        "back_urls": {
                            "success": "https://example.com/success",
                            "failure": "https://example.com/failure",
                            "pending": "https://example.com/pending"
                        },
                        "auto_return": "approved"
                    }
                    
                    preference_result = sdk.preference().create(preference_data)
                    
                    if preference_result["status"] == 201:
                        preference = preference_result["response"]
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Preferência de teste criada com sucesso!\n'
                                f'   ID: {preference.get("id", "N/A")}\n'
                                f'   Status: {preference.get("status", "N/A")}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠️ Erro ao criar preferência de teste: {preference_result}'
                            )
                        )
                    
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Erro na conexão com Mercado Pago: {result}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Erro ao conectar com Mercado Pago: {e}'
                    )
                )
                logger.error(f"Erro ao testar Mercado Pago: {e}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro geral: {e}')
            )
            logger.error(f"Erro geral ao testar Mercado Pago: {e}")
