from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento

class Command(BaseCommand):
    help = 'Configura tokens do Mercado Pago via admin'

    def handle(self, *args, **options):
        self.stdout.write('Configurando tokens do Mercado Pago...')
        
        # Buscar configuração ativa
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        
        if not config:
            self.stdout.write(self.style.ERROR('Nenhuma configuracao ativa encontrada!'))
            self.stdout.write('Crie uma configuracao ativa no admin primeiro.')
            return
        
        # Tokens de teste
        access_token = "TEST-3670731395523817-092513-dbcd061d092f64599cb62b72dddb8930-2270907901"
        public_key = "TEST-cdb0e326-f455-4ad3-a5b8-a768910a01ef"
        webhook_secret = "c77ff2936adfc464fd8612b4f28c59b9cd3fef143d0f7dad23eb5ec31b0b5028"
        
        # Configurar tokens
        config.set_access_token(access_token)
        config.set_public_key(public_key)
        config.set_webhook_secret(webhook_secret)
        config.save()
        
        self.stdout.write(self.style.SUCCESS('Tokens configurados com sucesso!'))
        self.stdout.write(f'Configuracao ID: {config.id}')
        self.stdout.write(f'Ambiente: {config.ambiente}')
        self.stdout.write(f'Ativo: {config.ativo}')
        
        # Testar
        try:
            from payments.views import get_mercadopago_config
            sdk, test_config = get_mercadopago_config()
            if sdk and test_config:
                self.stdout.write(self.style.SUCCESS('Configuracao testada com sucesso!'))
            else:
                self.stdout.write(self.style.ERROR('Erro ao testar configuracao'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao testar: {e}'))
