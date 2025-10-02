from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento
import mercadopago
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Configura o webhook do Mercado Pago para receber notificações automáticas'

    def handle(self, *args, **options):
        """
        Configura o webhook do Mercado Pago para receber notificações automáticas
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
            webhook_url = config.webhook_url
            
            if not access_token:
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Access token não encontrado ou não pode ser descriptografado.'
                    )
                )
                return

            self.stdout.write('🔄 Configurando webhook do Mercado Pago...')
            
            try:
                # Inicializar SDK
                sdk = mercadopago.SDK(access_token)
                
                # Verificar webhooks existentes
                webhooks_result = sdk.webhook().get()
                
                if webhooks_result["status"] == 200:
                    webhooks = webhooks_result["response"]
                    
                    self.stdout.write(f'📋 Webhooks existentes: {len(webhooks)}')
                    
                    # Verificar se já existe webhook para nossa URL
                    webhook_existente = None
                    for webhook in webhooks:
                        if webhook.get("url") == webhook_url:
                            webhook_existente = webhook
                            break
                    
                    if webhook_existente:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✅ Webhook já configurado!\n'
                                f'   ID: {webhook_existente.get("id")}\n'
                                f'   URL: {webhook_existente.get("url")}\n'
                                f'   Status: {webhook_existente.get("status")}\n'
                                f'   Eventos: {", ".join(webhook_existente.get("events", []))}'
                            )
                        )
                    else:
                        # Criar novo webhook
                        self.stdout.write('🔄 Criando novo webhook...')
                        
                        webhook_data = {
                            "url": webhook_url,
                            "events": ["payment", "subscription"],
                            "status": "active"
                        }
                        
                        create_result = sdk.webhook().create(webhook_data)
                        
                        if create_result["status"] == 201:
                            webhook_criado = create_result["response"]
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'✅ Webhook criado com sucesso!\n'
                                    f'   ID: {webhook_criado.get("id")}\n'
                                    f'   URL: {webhook_criado.get("url")}\n'
                                    f'   Status: {webhook_criado.get("status")}\n'
                                    f'   Eventos: {", ".join(webhook_criado.get("events", []))}'
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'❌ Erro ao criar webhook: {create_result}'
                                )
                            )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Erro ao buscar webhooks: {webhooks_result}'
                        )
                    )
                
                # Testar webhook
                self.stdout.write('\n🔄 Testando webhook...')
                
                # Criar preferência de teste para testar webhook
                preference_data = {
                    "items": [
                        {
                            "title": "Teste de Webhook",
                            "description": "Teste de notificação automática",
                            "quantity": 1,
                            "unit_price": 1.00,
                            "currency_id": "BRL"
                        }
                    ],
                    "back_urls": {
                        "success": f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/payments/success/",
                        "failure": f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/payments/failure/",
                        "pending": f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}/payments/pending/"
                    },
                    "auto_return": "approved",
                    "notification_url": webhook_url
                }
                
                preference_result = sdk.preference().create(preference_data)
                
                if preference_result["status"] == 201:
                    preference = preference_result["response"]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Preferência de teste criada!\n'
                            f'   ID: {preference.get("id")}\n'
                            f'   URL de pagamento: {preference.get("init_point")}\n'
                            f'   Webhook URL: {webhook_url}'
                        )
                    )
                    
                    self.stdout.write(
                        self.style.WARNING(
                            '\n📱 COMO TESTAR AS NOTIFICAÇÕES:\n'
                            '1. Acesse a URL de pagamento acima\n'
                            '2. Faça um pagamento de teste\n'
                            '3. O webhook será chamado automaticamente\n'
                            '4. Você receberá notificação no app do Mercado Pago\n'
                            '5. O sistema processará o pagamento automaticamente'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Erro ao criar preferência de teste: {preference_result}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Erro ao configurar webhook: {e}'
                    )
                )
                logger.error(f"Erro ao configurar webhook: {e}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro geral: {e}')
            )
            logger.error(f"Erro geral ao configurar webhook: {e}")






