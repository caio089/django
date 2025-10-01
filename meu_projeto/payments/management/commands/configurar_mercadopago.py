from django.core.management.base import BaseCommand
from django.conf import settings
from payments.models import ConfiguracaoPagamento
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Configura as credenciais do Mercado Pago no banco de dados'

    def handle(self, *args, **options):
        """
        Configura automaticamente as credenciais do Mercado Pago
        usando as variáveis de ambiente do arquivo .env
        """
        try:
            # Verificar se as credenciais estão definidas
            access_token = settings.MERCADOPAGO_ACCESS_TOKEN
            public_key = settings.MERCADOPAGO_PUBLIC_KEY
            webhook_secret = settings.MERCADOPAGO_WEBHOOK_SECRET
            webhook_url = settings.MERCADOPAGO_WEBHOOK_URL

            if not all([access_token, public_key, webhook_url]):
                self.stdout.write(
                    self.style.ERROR(
                        '❌ Credenciais do Mercado Pago não encontradas no arquivo .env\n'
                        'Verifique se as seguintes variáveis estão definidas:\n'
                        '- MERCADOPAGO_ACCESS_TOKEN\n'
                        '- MERCADOPAGO_PUBLIC_KEY\n'
                        '- MERCADOPAGO_WEBHOOK_URL'
                    )
                )
                return

            # Verificar se já existe uma configuração ativa
            config_existente = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            
            if config_existente:
                # Atualizar configuração existente
                config_existente.set_access_token(access_token)
                config_existente.set_public_key(public_key)
                config_existente.set_webhook_secret(webhook_secret)
                config_existente.webhook_url = webhook_url
                config_existente.ambiente = 'sandbox' if 'TEST-' in access_token else 'production'
                config_existente.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Configuração do Mercado Pago atualizada com sucesso!\n'
                        f'   Ambiente: {config_existente.ambiente}\n'
                        f'   Webhook URL: {webhook_url}'
                    )
                )
            else:
                # Criar nova configuração
                config = ConfiguracaoPagamento.objects.create(
                    webhook_url=webhook_url,
                    ambiente='sandbox' if 'TEST-' in access_token else 'production',
                    ativo=True
                )
                
                # Definir credenciais criptografadas
                config.set_access_token(access_token)
                config.set_public_key(public_key)
                config.set_webhook_secret(webhook_secret)
                config.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Configuração do Mercado Pago criada com sucesso!\n'
                        f'   ID: {config.id}\n'
                        f'   Ambiente: {config.ambiente}\n'
                        f'   Webhook URL: {webhook_url}'
                    )
                )

            # Verificar se as credenciais foram salvas corretamente
            config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
            if config:
                # Testar descriptografia
                token_test = config.get_access_token()
                key_test = config.get_public_key()
                secret_test = config.get_webhook_secret()
                
                if all([token_test, key_test]):
                    self.stdout.write(
                        self.style.SUCCESS(
                            '✅ Credenciais criptografadas e salvas com sucesso!\n'
                            '✅ Sistema de pagamento configurado e pronto para uso.'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            '❌ Erro ao verificar credenciais criptografadas'
                        )
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao configurar Mercado Pago: {e}')
            )
            logger.error(f"Erro ao configurar Mercado Pago: {e}")




