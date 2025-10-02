from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import ConfiguracaoPagamento, Pagamento
from home.models import Profile
import os

class Command(BaseCommand):
    help = 'Diagnóstico completo do sistema para deploy'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 DIAGNÓSTICO DO SISTEMA'))
        self.stdout.write('=' * 50)
        
        # 1. Verificar usuários
        self.stdout.write('\n👥 USUÁRIOS:')
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        self.stdout.write(f'Total de usuários: {total_users}')
        self.stdout.write(f'Usuários ativos: {active_users}')
        
        # Listar alguns usuários
        for user in User.objects.all()[:5]:
            self.stdout.write(f'  - {user.email} (ativo: {user.is_active})')
        
        # 2. Verificar perfis
        self.stdout.write('\n👤 PERFIS:')
        total_profiles = Profile.objects.count()
        self.stdout.write(f'Total de perfis: {total_profiles}')
        
        # 3. Verificar configuração do Mercado Pago
        self.stdout.write('\n💳 MERCADO PAGO:')
        configs = ConfiguracaoPagamento.objects.all()
        self.stdout.write(f'Configurações encontradas: {configs.count()}')
        
        for config in configs:
            self.stdout.write(f'  - Configuração ID: {config.id} (ativo: {config.ativo})')
            self.stdout.write(f'    Ambiente: {config.ambiente}')
            self.stdout.write(f'    Access token: {"✅" if config.get_access_token() else "❌"}')
            self.stdout.write(f'    Public key: {"✅" if config.get_public_key() else "❌"}')
        
        # 4. Verificar pagamentos
        self.stdout.write('\n💰 PAGAMENTOS:')
        total_payments = Pagamento.objects.count()
        self.stdout.write(f'Total de pagamentos: {total_payments}')
        
        # 5. Verificar variáveis de ambiente
        self.stdout.write('\n🌍 VARIÁVEIS DE AMBIENTE:')
        env_vars = [
            'DEBUG',
            'SECRET_KEY',
            'ALLOWED_HOSTS',
            'MERCADOPAGO_ACCESS_TOKEN',
            'MERCADOPAGO_PUBLIC_KEY'
        ]
        
        for var in env_vars:
            value = os.getenv(var, 'NÃO DEFINIDA')
            if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
                value = f'{value[:10]}...' if len(value) > 10 else value
            self.stdout.write(f'  {var}: {value}')
        
        # 6. Verificar URLs
        self.stdout.write('\n🔗 URLs IMPORTANTES:')
        from django.conf import settings
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        self.stdout.write('\n✅ Diagnóstico concluído!')
