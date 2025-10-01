from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Configura o Mercado Pago para produção usando variáveis de ambiente'

    def add_arguments(self, parser):
        parser.add_argument('--access-token', type=str, help='Access Token do Mercado Pago')
        parser.add_argument('--public-key', type=str, help='Public Key do Mercado Pago')
        parser.add_argument('--webhook-secret', type=str, help='Webhook Secret do Mercado Pago')
        parser.add_argument('--webhook-url', type=str, help='URL do Webhook')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Configurando Mercado Pago para producao...'))
        
        # Obter valores das variáveis de ambiente ou argumentos
        access_token = options.get('access_token') or os.getenv('MERCADOPAGO_ACCESS_TOKEN')
        public_key = options.get('public_key') or os.getenv('MERCADOPAGO_PUBLIC_KEY')
        webhook_secret = options.get('webhook_secret') or os.getenv('MERCADOPAGO_WEBHOOK_SECRET')
        webhook_url = options.get('webhook_url') or os.getenv('MERCADOPAGO_WEBHOOK_URL')
        
        if not access_token:
            self.stdout.write(self.style.ERROR('Access Token nao fornecido!'))
            self.stdout.write('Use --access-token ou defina MERCADOPAGO_ACCESS_TOKEN')
            return
        
        if not public_key:
            self.stdout.write(self.style.ERROR('Public Key nao fornecida!'))
            self.stdout.write('Use --public-key ou defina MERCADOPAGO_PUBLIC_KEY')
            return
        
        # Desativar configurações existentes
        ConfiguracaoPagamento.objects.filter(ativo=True).update(ativo=False)
        self.stdout.write('Configuracoes existentes desativadas')
        
        # Criar nova configuração
        config = ConfiguracaoPagamento.objects.create(
            ambiente='production',
            ativo=True,
            webhook_url=webhook_url or 'https://dojo-on.onrender.com/payments/webhook/'
        )
        
        # Definir tokens
        config.set_access_token(access_token)
        config.set_public_key(public_key)
        if webhook_secret:
            config.set_webhook_secret(webhook_secret)
        
        config.save()
        
        self.stdout.write(self.style.SUCCESS('Configuracao criada com sucesso!'))
        self.stdout.write(f'   ID: {config.id}')
        self.stdout.write(f'   Ambiente: {config.ambiente}')
        self.stdout.write(f'   Ativo: {config.ativo}')
        self.stdout.write(f'   Webhook URL: {config.webhook_url}')
        
        # Testar configuração
        self.stdout.write('\nTestando configuracao...')
        try:
            from payments.views import get_mercadopago_config
            sdk, test_config = get_mercadopago_config()
            if sdk and test_config:
                self.stdout.write(self.style.SUCCESS('Configuracao testada com sucesso!'))
            else:
                self.stdout.write(self.style.ERROR('Erro ao testar configuracao'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao testar: {e}'))
