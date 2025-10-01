from django.core.management.base import BaseCommand
from payments.views import get_mercadopago_config

class Command(BaseCommand):
    help = 'Verifica se PIX está habilitado na conta do Mercado Pago'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Verificando PIX na conta do Mercado Pago...'))
        
        sdk, config = get_mercadopago_config()
        if not sdk:
            self.stdout.write(self.style.ERROR('❌ SDK do Mercado Pago não disponível'))
            return
        
        # Criar preferência de teste apenas com PIX
        preference_data = {
            "items": [
                {
                    "title": "Teste PIX",
                    "description": "Verificação de PIX",
                    "quantity": 1,
                    "unit_price": 1.0,
                    "currency_id": "BRL"
                }
            ],
            "payment_methods": {
                "excluded_payment_methods": [
                    {"id": "credit_card"},
                    {"id": "debit_card"},
                    {"id": "bank_transfer"},
                    {"id": "digital_wallet"},
                    {"id": "digital_currency"},
                    {"id": "ticket"},
                    {"id": "atm"}
                ],
                "excluded_payment_types": [
                    {"id": "credit_card"},
                    {"id": "debit_card"},
                    {"id": "bank_transfer"},
                    {"id": "digital_wallet"},
                    {"id": "digital_currency"},
                    {"id": "ticket"},
                    {"id": "atm"}
                ],
                "installments": 1,
                "default_payment_method_id": "pix"
            },
            "purpose": "wallet_purchase",
            "binary_mode": False
        }
        
        try:
            self.stdout.write('🔄 Criando preferência apenas com PIX...')
            result = sdk.preference().create(preference_data)
            
            if result["status"] == 201:
                preference = result["response"]
                self.stdout.write(self.style.SUCCESS('✅ Preferência criada com sucesso!'))
                
                # Verificar métodos de pagamento disponíveis
                payment_methods = preference.get("payment_methods", {})
                excluded_methods = payment_methods.get("excluded_payment_methods", [])
                excluded_types = payment_methods.get("excluded_payment_types", [])
                
                self.stdout.write(f'📋 Métodos excluídos: {excluded_methods}')
                self.stdout.write(f'📋 Tipos excluídos: {excluded_types}')
                
                # Verificar se PIX está disponível
                pix_available = True
                for method in excluded_methods:
                    if method.get("id") == "pix":
                        pix_available = False
                        break
                
                for ptype in excluded_types:
                    if ptype.get("id") == "pix":
                        pix_available = False
                        break
                
                if pix_available:
                    self.stdout.write(self.style.SUCCESS('✅ PIX está disponível na conta!'))
                    self.stdout.write(f'🔗 URL de teste: {preference.get("init_point")}')
                else:
                    self.stdout.write(self.style.ERROR('❌ PIX NÃO está disponível na conta!'))
                    self.stdout.write(self.style.WARNING('💡 Para habilitar PIX:'))
                    self.stdout.write('1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials')
                    self.stdout.write('2. Vá em "Configurações" > "Meios de pagamento"')
                    self.stdout.write('3. Habilite PIX se disponível')
                    self.stdout.write('4. Verifique se a conta está verificada')
                    self.stdout.write('5. No sandbox, PIX pode ter limitações')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar preferência: {result["status"]}'))
                if "response" in result:
                    self.stdout.write(f'   Detalhes: {result["response"]}')
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Verificação concluída!'))



