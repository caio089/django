from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento

class Command(BaseCommand):
    help = 'Configura credenciais de produção do Mercado Pago'

    def add_arguments(self, parser):
        parser.add_argument('--access-token', type=str, help='Access Token de produção')
        parser.add_argument('--public-key', type=str, help='Public Key de produção')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Configurando credenciais de produção...'))
        
        # Obter ou criar configuração
        config, created = ConfiguracaoPagamento.objects.get_or_create(
            defaults={
                'ambiente': 'sandbox',
                'access_token_encrypted': '',
                'public_key_encrypted': '',
                'webhook_url': 'https://dojo-on.onrender.com/payments/webhook/'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Configuração criada'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Configuração encontrada'))
        
        # Mostrar configuração atual
        self.stdout.write(self.style.WARNING('📋 Configuração atual:'))
        self.stdout.write(f'   Ambiente: {config.ambiente}')
        self.stdout.write(f'   Access Token: {config.get_access_token()[:20]}...')
        self.stdout.write(f'   Public Key: {config.get_public_key()[:20]}...')
        
        # Solicitar credenciais de produção
        if options['access_token'] and options['public_key']:
            access_token = options['access_token']
            public_key = options['public_key']
        else:
            self.stdout.write(self.style.WARNING('\n🔑 Para configurar produção, você precisa:'))
            self.stdout.write('1. Acessar: https://www.mercadopago.com.br/developers/panel/credentials')
            self.stdout.write('2. Copiar suas credenciais de PRODUÇÃO (não sandbox)')
            self.stdout.write('3. Executar: python manage.py configurar_producao --access-token SEU_ACCESS_TOKEN --public-key SUA_PUBLIC_KEY')
            return
        
        # Validar se são credenciais de produção
        if not access_token.startswith('APP-'):
            self.stdout.write(self.style.ERROR('❌ Access Token inválido! Deve começar com "APP-"'))
            return
            
        if not public_key.startswith('APP-'):
            self.stdout.write(self.style.ERROR('❌ Public Key inválida! Deve começar com "APP-"'))
            return
        
        # Atualizar configuração
        config.ambiente = 'producao'
        config.set_access_token(access_token)
        config.set_public_key(public_key)
        config.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Credenciais de produção configuradas!'))
        self.stdout.write(f'   Ambiente: {config.ambiente}')
        self.stdout.write(f'   Access Token: {config.get_access_token()[:20]}...')
        self.stdout.write(f'   Public Key: {config.get_public_key()[:20]}...')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Configuração de produção concluída!'))
        self.stdout.write(self.style.WARNING('💡 Agora teste o PIX novamente'))



