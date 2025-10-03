from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
import mercadopago
import requests

class Command(BaseCommand):
    help = 'Verifica a configuração da conta do Mercado Pago para PIX'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Verificando configuração PIX no Mercado Pago...'))
        
        # Verificar configuração
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração: {config.ambiente}'))
        
        try:
            sdk = mercadopago.SDK(config.get_access_token())
            
            # Testar criação de preferência simples
            test_preference = {
                "items": [
                    {
                        "title": "Teste PIX",
                        "quantity": 1,
                        "unit_price": 1.0,
                        "currency_id": "BRL"
                    }
                ],
                "payment_methods": {
                    "excluded_payment_methods": [],
                    "excluded_payment_types": [],
                    "default_payment_method_id": "pix"
                }
            }
            
            self.stdout.write(self.style.WARNING('🔄 Testando criação de preferência...'))
            result = sdk.preference().create(test_preference)
            
            if result["status"] == 201:
                preference = result["response"]
                self.stdout.write(self.style.SUCCESS('✅ Preferência criada com sucesso!'))
                
                # Analisar métodos de pagamento
                payment_methods = preference.get("payment_methods", {})
                excluded_types = payment_methods.get("excluded_payment_types", [])
                default_method = payment_methods.get("default_payment_method_id")
                
                self.stdout.write(self.style.SUCCESS('📋 Análise da configuração:'))
                self.stdout.write(f'   Método padrão: {default_method}')
                self.stdout.write(f'   Tipos excluídos: {excluded_types}')
                
                # Verificar se PIX está disponível
                pix_excluded = any(method.get("id") == "pix" for method in excluded_types)
                pix_available = not pix_excluded
                
                self.stdout.write(f'   PIX disponível: {"✅ SIM" if pix_available else "❌ NÃO"}')
                
                if pix_available:
                    self.stdout.write(self.style.SUCCESS('🎉 PIX está habilitado na conta!'))
                    self.stdout.write('💡 Se PIX não aparece no checkout, pode ser:')
                    self.stdout.write('   1. Limitação do ambiente sandbox')
                    self.stdout.write('   2. Configuração da conta incompleta')
                    self.stdout.write('   3. Interface do checkout não mostra PIX claramente')
                else:
                    self.stdout.write(self.style.ERROR('❌ PIX não está habilitado na conta'))
                    self.stdout.write('🔧 Para habilitar PIX:')
                    self.stdout.write('   1. Acesse o painel do Mercado Pago')
                    self.stdout.write('   2. Vá em Configurações > Meios de pagamento')
                    self.stdout.write('   3. Habilite PIX')
                    self.stdout.write('   4. Complete a verificação da conta se necessário')
                
                # Mostrar informações da conta
                self.stdout.write(self.style.WARNING('🔍 Informações da conta:'))
                self.stdout.write(f'   Collector ID: {preference.get("collector_id")}')
                self.stdout.write(f'   Site ID: {preference.get("site_id")}')
                self.stdout.write(f'   Ambiente: {config.ambiente}')
                
                # Mostrar URL do checkout
                init_point = preference.get("init_point")
                if init_point:
                    self.stdout.write(self.style.SUCCESS('🔗 URL do checkout:'))
                    self.stdout.write(f'   {init_point}')
                    self.stdout.write('📱 Acesse esta URL para verificar se PIX aparece')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar preferência: {result}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante a verificação: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Orientações adicionais
        self.stdout.write(self.style.WARNING('📚 Orientações para habilitar PIX:'))
        self.stdout.write('1. Acesse: https://www.mercadopago.com.br/developers/panel/credentials')
        self.stdout.write('2. Verifique se a conta está verificada')
        self.stdout.write('3. Vá em Configurações > Meios de pagamento')
        self.stdout.write('4. Habilite PIX se disponível')
        self.stdout.write('5. No ambiente sandbox, PIX pode ter limitações')
        self.stdout.write('6. Para produção, certifique-se de que a conta está aprovada para PIX')
        
        self.stdout.write(self.style.SUCCESS('🏁 Verificação concluída!'))






