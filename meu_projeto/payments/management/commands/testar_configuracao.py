from django.core.management.base import BaseCommand
from payments.mercadopago_config import validate_credentials, get_mercadopago_credentials, is_sandbox
import mercadopago

class Command(BaseCommand):
    help = 'Testa a configuração do Mercado Pago'

    def handle(self, *args, **options):
        self.stdout.write('🔧 TESTANDO CONFIGURAÇÃO DO MERCADO PAGO\n')
        
        # 1. Validar credenciais
        self.stdout.write('1️⃣ Validando credenciais...')
        is_valid, message = validate_credentials()
        
        if is_valid:
            self.stdout.write(self.style.SUCCESS(f'   ✅ {message}'))
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ {message}'))
            return
        
        # 2. Testar SDK
        self.stdout.write('\n2️⃣ Testando SDK do Mercado Pago...')
        try:
            access_token, public_key, webhook_url, ambiente = get_mercadopago_credentials()
            sdk = mercadopago.SDK(access_token)
            self.stdout.write(self.style.SUCCESS(f'   ✅ SDK criado com sucesso'))
            self.stdout.write(f'   📊 Ambiente: {ambiente}')
            self.stdout.write(f'   🔑 Access Token: {access_token[:20]}...')
            self.stdout.write(f'   🔑 Public Key: {public_key[:20]}...')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Erro ao criar SDK: {e}'))
            return
        
        # 3. Testar criação de preferência
        self.stdout.write('\n3️⃣ Testando criação de preferência...')
        try:
            preference_data = {
                "items": [
                    {
                        "title": "Teste de Pagamento",
                        "description": "Teste de configuração",
                        "quantity": 1,
                        "unit_price": 1.00,
                        "currency_id": "BRL"
                    }
                ],
                "payer": {
                    "email": "test@example.com"
                },
                "external_reference": "test_config"
            }
            
            preference = sdk.preference().create(preference_data)
            
            if preference["status"] == 201:
                self.stdout.write(self.style.SUCCESS('   ✅ Preferência criada com sucesso'))
                pref_data = preference["response"]
                self.stdout.write(f'   📋 ID: {pref_data["id"]}')
                self.stdout.write(f'   🔗 Init Point: {pref_data["init_point"][:50]}...')
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Erro ao criar preferência: {preference}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Erro na criação de preferência: {e}'))
        
        # 4. Testar criação de PIX
        self.stdout.write('\n4️⃣ Testando criação de PIX...')
        try:
            payment_data = {
                "transaction_amount": 1.00,
                "description": "Teste PIX",
                "payment_method_id": "pix",
                "payer": {
                    "email": "test@example.com",
                    "identification": {
                        "type": "CPF",
                        "number": "12345678901"
                    }
                },
                "external_reference": "test_pix"
            }
            
            payment_result = sdk.payment().create(payment_data)
            
            if payment_result["status"] == 201:
                self.stdout.write(self.style.SUCCESS('   ✅ PIX criado com sucesso'))
                payment_info = payment_result["response"]
                self.stdout.write(f'   📋 Payment ID: {payment_info["id"]}')
                self.stdout.write(f'   📊 Status: {payment_info["status"]}')
                
                # Verificar se tem QR Code
                point_of_interaction = payment_info.get("point_of_interaction", {})
                transaction_data = point_of_interaction.get("transaction_data", {})
                qr_code = transaction_data.get("qr_code")
                
                if qr_code:
                    self.stdout.write(self.style.SUCCESS('   ✅ QR Code PIX gerado'))
                    self.stdout.write(f'   📱 QR Code: {qr_code[:50]}...')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️ PIX criado mas sem QR Code'))
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Erro ao criar PIX: {payment_result}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Erro na criação de PIX: {e}'))
        
        # 5. Resumo final
        self.stdout.write('\n📋 RESUMO DA CONFIGURAÇÃO:')
        self.stdout.write(f'   🌍 Ambiente: {ambiente}')
        self.stdout.write(f'   🧪 É Sandbox: {"Sim" if is_sandbox() else "Não"}')
        self.stdout.write(f'   🔗 Webhook URL: {webhook_url}')
        
        if is_sandbox():
            self.stdout.write('\n💡 DICAS PARA SANDBOX:')
            self.stdout.write('   • Use cartões de teste fornecidos pelo MP')
            self.stdout.write('   • PIX funciona com qualquer email')
            self.stdout.write('   • Não há cobrança real')
        else:
            self.stdout.write('\n💡 DICAS PARA PRODUÇÃO:')
            self.stdout.write('   • Use cartões reais')
            self.stdout.write('   • PIX precisa de email válido')
            self.stdout.write('   • Cobrança real será efetuada')
        
        self.stdout.write('\n✅ Teste de configuração concluído!')
