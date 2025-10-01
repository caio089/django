from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import ConfiguracaoPagamento

class Command(BaseCommand):
    help = 'Configura automaticamente o sistema para produção'

    def handle(self, *args, **options):
        self.stdout.write('Configurando sistema para producao...')
        
        # 1. Criar/atualizar superusuário
        self.stdout.write('1. Configurando superusuario...')
        if User.objects.filter(username='admin').exists():
            user = User.objects.get(username='admin')
            self.stdout.write('   Usuario admin ja existe. Atualizando...')
        else:
            user = User.objects.create_user(
                username='admin',
                email='admin@exemplo.com',
                password='admin123'
            )
            self.stdout.write('   Usuario admin criado.')
        
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password('admin123')
        user.save()
        
        self.stdout.write('   Credenciais: admin / admin123')
        
        # 2. Configurar Mercado Pago
        self.stdout.write('2. Configurando Mercado Pago...')
        
        # Desativar configurações existentes
        ConfiguracaoPagamento.objects.filter(ativo=True).update(ativo=False)
        
        # Criar nova configuração
        config = ConfiguracaoPagamento.objects.create(
            ambiente='production',
            ativo=True,
            webhook_url='https://dojo-on.onrender.com/payments/webhook/'
        )
        
        # Configurar tokens
        config.set_access_token("TEST-3670731395523817-092513-dbcd061d092f64599cb62b72dddb8930-2270907901")
        config.set_public_key("TEST-cdb0e326-f455-4ad3-a5b8-a768910a01ef")
        config.set_webhook_secret("c77ff2936adfc464fd8612b4f28c59b9cd3fef143d0f7dad23eb5ec31b0b5028")
        config.save()
        
        self.stdout.write('   Configuracao do Mercado Pago criada!')
        
        # 3. Testar configuração
        self.stdout.write('3. Testando configuracao...')
        try:
            from payments.views import get_mercadopago_config
            sdk, test_config = get_mercadopago_config()
            if sdk and test_config:
                self.stdout.write(self.style.SUCCESS('   Configuracao funcionando!'))
            else:
                self.stdout.write(self.style.ERROR('   Erro na configuracao!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Erro: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Configuracao concluida!'))
        self.stdout.write('Acesse: https://dojo-on.onrender.com/admin/')
        self.stdout.write('Usuario: admin')
        self.stdout.write('Senha: admin123')
