"""
Comando para debugar problemas no Render
Execute: python manage.py debug_render
"""

from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento, PlanoPremium
from payments.views import get_mercadopago_config
from django.contrib.auth.models import User
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Debug de problemas no Render'

    def handle(self, *args, **options):
        self.stdout.write("🔍 DEBUG DO RENDER")
        self.stdout.write("=" * 50)
        
        # 1. Verificar configurações do Django
        from django.conf import settings
        self.stdout.write("1. CONFIGURAÇÕES DO DJANGO:")
        self.stdout.write(f"   DEBUG: {settings.DEBUG}")
        self.stdout.write(f"   TIME_ZONE: {settings.TIME_ZONE}")
        self.stdout.write(f"   DATABASE: {settings.DATABASES['default']['ENGINE']}")
        
        # 2. Verificar variáveis de ambiente
        self.stdout.write("\n2. VARIÁVEIS DE AMBIENTE:")
        env_vars = [
            'DEBUG', 'SECRET_KEY', 'DATABASE_URL', 'DB_HOST',
            'MERCADOPAGO_ACCESS_TOKEN', 'MERCADOPAGO_PUBLIC_KEY',
            'MERCADOPAGO_WEBHOOK_URL', 'MERCADOPAGO_WEBHOOK_SECRET'
        ]
        
        for var in env_vars:
            value = os.getenv(var, 'NÃO DEFINIDA')
            if 'TOKEN' in var or 'KEY' in var or 'SECRET' in var:
                value = value[:20] + '...' if len(value) > 20 else value
            self.stdout.write(f"   {var}: {value}")
        
        # 3. Verificar configuração do Mercado Pago
        self.stdout.write("\n3. CONFIGURAÇÃO DO MERCADO PAGO:")
        configs = ConfiguracaoPagamento.objects.all()
        if configs:
            for config in configs:
                self.stdout.write(f"   ID: {config.id}")
                self.stdout.write(f"   Ambiente: {config.ambiente}")
                self.stdout.write(f"   Ativo: {config.ativo}")
                self.stdout.write(f"   Webhook URL: {config.webhook_url}")
                
                try:
                    access_token = config.get_access_token()
                    if access_token:
                        self.stdout.write(f"   Access Token: {access_token[:20]}...")
                        self.stdout.write(f"   Token válido: {access_token.startswith(('TEST-', 'APP-'))}")
                    else:
                        self.stdout.write("   ❌ Access Token não obtido")
                except Exception as e:
                    self.stdout.write(f"   ❌ Erro ao obter Access Token: {e}")
                
                try:
                    public_key = config.get_public_key()
                    if public_key:
                        self.stdout.write(f"   Public Key: {public_key[:20]}...")
                        self.stdout.write(f"   Key válida: {public_key.startswith(('TEST-', 'APP-'))}")
                    else:
                        self.stdout.write("   ❌ Public Key não obtida")
                except Exception as e:
                    self.stdout.write(f"   ❌ Erro ao obter Public Key: {e}")
                
                self.stdout.write("   ---")
        else:
            self.stdout.write("   ❌ Nenhuma configuração encontrada!")
        
        # 4. Testar função get_mercadopago_config
        self.stdout.write("\n4. TESTE DA FUNÇÃO get_mercadopago_config:")
        try:
            sdk, config_obj = get_mercadopago_config()
            if sdk and config_obj:
                self.stdout.write("   ✅ SDK criado com sucesso")
                self.stdout.write(f"   ✅ Configuração: {config_obj.ambiente}")
            else:
                self.stdout.write("   ❌ Falha ao criar SDK")
        except Exception as e:
            self.stdout.write(f"   ❌ Erro na função get_mercadopago_config: {e}")
        
        # 5. Verificar planos
        self.stdout.write("\n5. PLANOS DISPONÍVEIS:")
        planos = PlanoPremium.objects.filter(ativo=True)
        if planos:
            for plano in planos:
                self.stdout.write(f"   - {plano.nome}: R$ {plano.preco} (ID: {plano.id})")
        else:
            self.stdout.write("   ❌ Nenhum plano ativo encontrado!")
        
        # 6. Verificar usuários
        self.stdout.write("\n6. USUÁRIOS:")
        users = User.objects.all()
        if users:
            self.stdout.write(f"   Total de usuários: {users.count()}")
            for user in users:
                self.stdout.write(f"   - {user.email} (Ativo: {user.is_active})")
        else:
            self.stdout.write("   ❌ Nenhum usuário encontrado!")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("✅ Debug concluído!")
