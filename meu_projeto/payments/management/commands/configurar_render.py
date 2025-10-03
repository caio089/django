"""
Comando para configurar o Mercado Pago no Render
Execute: python manage.py configurar_render
"""

from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Configura o Mercado Pago para o ambiente do Render'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Configurando Mercado Pago para Render...")
        
        # Verificar se já existe configuração
        existing_config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if existing_config:
            self.stdout.write(f"✅ Configuração ativa já existe: {existing_config.ambiente}")
            return
        
        # Obter variáveis de ambiente
        access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
        public_key = os.getenv('MERCADOPAGO_PUBLIC_KEY')
        webhook_url = os.getenv('MERCADOPAGO_WEBHOOK_URL')
        webhook_secret = os.getenv('MERCADOPAGO_WEBHOOK_SECRET')
        
        if not access_token or not public_key:
            self.stdout.write(
                self.style.ERROR("❌ MERCADOPAGO_ACCESS_TOKEN ou MERCADOPAGO_PUBLIC_KEY não encontrados!")
            )
            return
        
        # Determinar ambiente baseado no token
        ambiente = 'production' if access_token.startswith('APP-') else 'sandbox'
        
        # Criar configuração
        try:
            config = ConfiguracaoPagamento.objects.create(
                webhook_url=webhook_url or 'https://dojo-on.onrender.com/payments/webhook/',
                ambiente=ambiente,
                ativo=True
            )
            
            # Criptografar e salvar tokens
            config.set_access_token(access_token)
            config.set_public_key(public_key)
            if webhook_secret:
                config.set_webhook_secret(webhook_secret)
            
            config.save()
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Configuração criada com sucesso!")
            )
            self.stdout.write(f"   Ambiente: {ambiente}")
            self.stdout.write(f"   Webhook URL: {config.webhook_url}")
            self.stdout.write(f"   Access Token: {access_token[:20]}...")
            self.stdout.write(f"   Public Key: {public_key[:20]}...")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao criar configuração: {e}")
            )
