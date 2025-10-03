from django.core.management.base import BaseCommand
from payments.mercadopago_config import validate_credentials, get_mercadopago_credentials, is_sandbox
import mercadopago

class Command(BaseCommand):
    help = 'Verifica se o Mercado Pago está configurado para produção'

    def handle(self, *args, **options):
        self.stdout.write('TESTANDO CONFIGURACAO DO MERCADO PAGO\n')
        
        # 1. Validar credenciais
        self.stdout.write('1. Validando credenciais...')
        is_valid, message = validate_credentials()
        
        if is_valid:
            self.stdout.write(self.style.SUCCESS(f'   OK: {message}'))
        else:
            self.stdout.write(self.style.ERROR(f'   ERRO: {message}'))
            return
        
        # 2. Verificar ambiente
        self.stdout.write('\n2. Verificando ambiente...')
        access_token, public_key, webhook_url, ambiente = get_mercadopago_credentials()
        
        if ambiente == 'production':
            self.stdout.write(self.style.SUCCESS('   AMBIENTE: PRODUCAO'))
            self.stdout.write(self.style.SUCCESS('   STATUS: Configurado para pagamentos reais'))
        elif ambiente == 'sandbox':
            self.stdout.write(self.style.WARNING('   AMBIENTE: SANDBOX (TESTE)'))
            self.stdout.write(self.style.WARNING('   STATUS: Apenas para testes'))
        else:
            self.stdout.write(self.style.ERROR('   AMBIENTE: DESCONHECIDO'))
            self.stdout.write(self.style.ERROR('   STATUS: Configuracao invalida'))
            return
        
        # 3. Mostrar credenciais (mascaradas)
        self.stdout.write('\n3. Credenciais configuradas:')
        self.stdout.write(f'   Access Token: {access_token[:20]}...')
        self.stdout.write(f'   Public Key: {public_key[:20]}...')
        self.stdout.write(f'   Webhook URL: {webhook_url}')
        
        # 4. Testar SDK
        self.stdout.write('\n4. Testando SDK...')
        try:
            sdk = mercadopago.SDK(access_token)
            self.stdout.write(self.style.SUCCESS('   SDK: Criado com sucesso'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   SDK: Erro - {e}'))
            return
        
        # 5. Resumo final
        self.stdout.write('\nRESUMO:')
        if ambiente == 'production':
            self.stdout.write(self.style.SUCCESS('SISTEMA CONFIGURADO PARA PRODUCAO'))
            self.stdout.write(self.style.SUCCESS('PIX e cartao funcionarao com pagamentos reais'))
        else:
            self.stdout.write(self.style.WARNING('SISTEMA CONFIGURADO PARA TESTE'))
            self.stdout.write(self.style.WARNING('Para producao, use credenciais que comecam com APP-'))
        
        self.stdout.write('\nTeste concluido!')
