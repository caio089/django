from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
from payments.views import get_mercadopago_config

class Command(BaseCommand):
    help = 'Testa as credenciais de produção do Mercado Pago'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando credenciais de produção...'))
        
        # Obter configuração
        config = ConfiguracaoPagamento.objects.first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Configuração não encontrada'))
            return
        
        self.stdout.write(f'📋 Ambiente atual: {config.ambiente}')
        self.stdout.write(f'   Access Token: {config.get_access_token()[:20]}...')
        self.stdout.write(f'   Public Key: {config.get_public_key()[:20]}...')
        
        # Verificar se são credenciais de produção
        access_token = config.get_access_token()
        public_key = config.get_public_key()
        
        if access_token.startswith('TEST-'):
            self.stdout.write(self.style.ERROR('❌ Você está usando credenciais de SANDBOX!'))
            self.stdout.write(self.style.WARNING('💡 Para usar produção, execute:'))
            self.stdout.write('   python manage.py configurar_producao --access-token SEU_ACCESS_TOKEN --public-key SUA_PUBLIC_KEY')
            return
        elif access_token.startswith('APP-'):
            self.stdout.write(self.style.SUCCESS('✅ Credenciais de produção detectadas!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Formato de credenciais não reconhecido'))
        
        # Testar SDK
        try:
            sdk, config_obj = get_mercadopago_config()
            if sdk:
                self.stdout.write(self.style.SUCCESS('✅ SDK do Mercado Pago inicializado'))
                
                # Testar criação de preferência
                self.stdout.write('🔄 Testando criação de preferência...')
                
                preference_data = {
                    "items": [
                        {
                            "title": "Teste Produção",
                            "description": "Teste de PIX em produção",
                            "quantity": 1,
                            "unit_price": 1.0,
                            "currency_id": "BRL"
                        }
                    ],
                    "payment_methods": {
                        "excluded_payment_methods": [],
                        "excluded_payment_types": [],
                        "installments": 12,
                        "default_payment_method_id": "pix"
                    },
                    "purpose": "wallet_purchase",
                    "binary_mode": False
                }
                
                result = sdk.preference().create(preference_data)
                
                if result["status"] == 201:
                    self.stdout.write(self.style.SUCCESS('✅ Preferência criada com sucesso!'))
                    preference = result["response"]
                    
                    self.stdout.write(f'   ID: {preference["id"]}')
                    self.stdout.write(f'   Init Point: {preference.get("init_point", "N/A")}')
                    
                    # Verificar se PIX está disponível
                    payment_methods = preference.get("payment_methods", {})
                    excluded_types = payment_methods.get("excluded_payment_types", [])
                    pix_available = "pix" not in excluded_types
                    
                    if pix_available:
                        self.stdout.write(self.style.SUCCESS('✅ PIX está disponível!'))
                    else:
                        self.stdout.write(self.style.ERROR('❌ PIX não está disponível'))
                        
                else:
                    self.stdout.write(self.style.ERROR(f'❌ Erro ao criar preferência: {result["status"]}'))
                    if "response" in result:
                        self.stdout.write(f'   Detalhes: {result["response"]}')
            else:
                self.stdout.write(self.style.ERROR('❌ Erro ao inicializar SDK'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de produção concluído!'))

