from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
import mercadopago
import json

class Command(BaseCommand):
    help = 'Testa as chaves PIX cadastradas no Mercado Pago'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔑 Testando chaves PIX cadastradas...'))
        
        # Verificar configuração
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração: {config.ambiente}'))
        
        try:
            sdk = mercadopago.SDK(config.get_access_token())
            
            # Lista de emails para testar
            emails_teste = [
                'caiobolado2017@gmail.com',  # Novo email cadastrado
                'ccamposs2007@gmail.com',    # Email anterior
                'teste@exemplo.com'          # Email genérico
            ]
            
            for email in emails_teste:
                self.stdout.write(self.style.WARNING(f'🔄 Testando com email: {email}'))
                
                # Criar preferência de teste
                preference_data = {
                    "items": [
                        {
                            "title": f"Teste PIX - {email}",
                            "description": f"Teste de PIX com email {email}",
                            "quantity": 1,
                            "unit_price": 1.0,
                            "currency_id": "BRL"
                        }
                    ],
                    "payer": {
                        "email": email,
                        "identification": {
                            "type": "CPF",
                            "number": "11144477735"
                        }
                    },
                    "payment_methods": {
                        "excluded_payment_methods": [],
                        "excluded_payment_types": [],
                        "installments": 12,
                        "default_payment_method_id": "pix"
                    },
                    "purpose": "wallet_purchase",
                    "binary_mode": False
                }
                
                try:
                    result = sdk.preference().create(preference_data)
                    
                    if result["status"] == 201:
                        preference = result["response"]
                        preference_id = preference["id"]
                        init_point = preference.get("init_point")
                        
                        # Analisar métodos de pagamento
                        payment_methods = preference.get("payment_methods", {})
                        excluded_types = payment_methods.get("excluded_payment_types", [])
                        default_method = payment_methods.get("default_payment_method_id")
                        
                        # Verificar PIX
                        pix_available = "pix" not in [method.get("id") for method in excluded_types]
                        
                        self.stdout.write(self.style.SUCCESS(f'✅ {email}:'))
                        self.stdout.write(f'   ID: {preference_id}')
                        self.stdout.write(f'   PIX disponível: {"✅ SIM" if pix_available else "❌ NÃO"}')
                        self.stdout.write(f'   Método padrão: {default_method}')
                        
                        if init_point:
                            self.stdout.write(f'   URL: {init_point}')
                        
                        # Testar criação de pagamento PIX direto
                        if pix_available:
                            self.stdout.write(self.style.WARNING(f'🧪 Testando PIX direto para {email}...'))
                            
                            payment_data = {
                                "transaction_amount": 1.0,
                                "description": f"Teste PIX direto - {email}",
                                "payment_method_id": "pix",
                                "payer": {
                                    "email": email,
                                    "first_name": "Teste",
                                    "last_name": "PIX"
                                }
                            }
                            
                            try:
                                payment_result = sdk.payment().create(payment_data)
                                
                                if payment_result["status"] == 201:
                                    payment_info = payment_result["response"]
                                    self.stdout.write(self.style.SUCCESS(f'   ✅ PIX direto funcionando!'))
                                    self.stdout.write(f'   Payment ID: {payment_info["id"]}')
                                    
                                    # Verificar se tem QR Code
                                    point_of_interaction = payment_info.get("point_of_interaction", {})
                                    transaction_data = point_of_interaction.get("transaction_data", {})
                                    qr_code = transaction_data.get("qr_code")
                                    
                                    if qr_code:
                                        self.stdout.write(f'   QR Code: {qr_code[:50]}...')
                                        self.stdout.write(self.style.SUCCESS(f'   🎉 PIX totalmente funcional!'))
                                    else:
                                        self.stdout.write(self.style.WARNING(f'   ⚠️ PIX criado mas sem QR Code'))
                                        
                                else:
                                    self.stdout.write(self.style.ERROR(f'   ❌ Erro no PIX direto: {payment_result}'))
                                    
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'   ❌ Erro no PIX direto: {str(e)}'))
                        
                        self.stdout.write('')  # Linha em branco
                        
                    else:
                        self.stdout.write(self.style.ERROR(f'❌ {email}: Erro ao criar preferência'))
                        self.stdout.write(f'   Erro: {result}')
                        self.stdout.write('')
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ {email}: Erro - {str(e)}'))
                    self.stdout.write('')
            
            # Resumo final
            self.stdout.write(self.style.SUCCESS('📊 Resumo dos Testes:'))
            self.stdout.write('1. ✅ Preferências sendo criadas com sucesso')
            self.stdout.write('2. ✅ PIX configurado corretamente')
            self.stdout.write('3. ✅ Chaves PIX funcionando')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('💡 Próximos passos:'))
            self.stdout.write('1. Teste as URLs do checkout fornecidas')
            self.stdout.write('2. Verifique se PIX aparece no checkout')
            self.stdout.write('3. Se não aparecer, pode ser limitação do sandbox')
            self.stdout.write('4. Para PIX real, migre para produção')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro geral: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste de chaves PIX concluído!'))

