from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from .models import ConfiguracaoPagamento

def setup_mercadopago_config(sender, **kwargs):
    """
    Configura automaticamente o Mercado Pago após migrações
    """
    # Criar superusuário se não existir
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@exemplo.com',
            password='admin123'
        )
        print("Superusuário admin criado!")
    
    # Configurar Mercado Pago se não existir configuração ativa
    if not ConfiguracaoPagamento.objects.filter(ativo=True).exists():
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
        
        print("Configuração do Mercado Pago criada automaticamente!")

class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    
    def ready(self):
        post_migrate.connect(setup_mercadopago_config, sender=self)
