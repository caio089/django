from django.core.management.base import BaseCommand
from payments.models import ConfiguracaoPagamento
import mercadopago
import json

class Command(BaseCommand):
    help = 'Ajuda a configurar PIX com chave de email no Mercado Pago'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email para usar como chave PIX')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Configurando PIX com chave de email...'))
        
        # Verificar configuração
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração: {config.ambiente}'))
        
        # Email para PIX
        email_pix = options.get('email')
        if not email_pix:
            email_pix = 'seu-email@exemplo.com'
            self.stdout.write(self.style.WARNING(f'⚠️ Usando email padrão: {email_pix}'))
            self.stdout.write('💡 Use --email seu-email@exemplo.com para definir seu email')
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Email PIX: {email_pix}'))
        
        try:
            sdk = mercadopago.SDK(config.get_access_token())
            
            # Criar preferência com configuração específica para PIX
            preference_data = {
                "items": [
                    {
                        "title": "Teste PIX Email",
                        "description": "Teste de PIX com chave de email",
                        "quantity": 1,
                        "unit_price": 1.0,
                        "currency_id": "BRL"
                    }
                ],
                "payer": {
                    "email": email_pix,
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
            
            self.stdout.write(self.style.WARNING('🔄 Criando preferência com PIX...'))
            self.stdout.write(f'Dados: {json.dumps(preference_data, indent=2)}')
            
            result = sdk.preference().create(preference_data)
            
            if result["status"] == 201:
                preference = result["response"]
                preference_id = preference["id"]
                init_point = preference.get("init_point")
                
                self.stdout.write(self.style.SUCCESS('✅ Preferência criada com sucesso!'))
                self.stdout.write(f'   ID: {preference_id}')
                self.stdout.write(f'   Email PIX: {email_pix}')
                
                # Analisar métodos de pagamento
                payment_methods = preference.get("payment_methods", {})
                excluded_types = payment_methods.get("excluded_payment_types", [])
                default_method = payment_methods.get("default_payment_method_id")
                
                self.stdout.write(self.style.SUCCESS('📋 Análise dos métodos:'))
                self.stdout.write(f'   Método padrão: {default_method}')
                self.stdout.write(f'   Tipos excluídos: {excluded_types}')
                
                # Verificar PIX
                pix_available = "pix" not in [method.get("id") for method in excluded_types]
                self.stdout.write(f'   PIX disponível: {"✅ SIM" if pix_available else "❌ NÃO"}')
                
                if init_point:
                    self.stdout.write(self.style.SUCCESS('🔗 URL do checkout:'))
                    self.stdout.write(f'   {init_point}')
                    self.stdout.write('📱 Acesse esta URL para testar PIX')
                
                # Orientações específicas para PIX
                self.stdout.write(self.style.WARNING('📚 Para PIX aparecer no checkout:'))
                self.stdout.write('1. Acesse o painel do Mercado Pago: https://www.mercadopago.com.br/developers/panel')
                self.stdout.write('2. Vá em Configurações > Meios de pagamento')
                self.stdout.write('3. Habilite PIX se não estiver habilitado')
                self.stdout.write('4. Configure uma chave PIX de email:')
                self.stdout.write(f'   - Email: {email_pix}')
                self.stdout.write('   - Vá em PIX > Minhas chaves')
                self.stdout.write('   - Adicione uma chave de email')
                self.stdout.write('5. Verifique se a conta está verificada')
                self.stdout.write('6. No sandbox, PIX pode ter limitações')
                
                # Verificar se é sandbox
                if config.ambiente == 'sandbox':
                    self.stdout.write(self.style.WARNING('⚠️ AMBIENTE SANDBOX:'))
                    self.stdout.write('   - PIX pode não aparecer no checkout')
                    self.stdout.write('   - Use cartão de crédito para testes')
                    self.stdout.write('   - Para PIX real, migre para produção')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar preferência: {result}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        # Orientações adicionais
        self.stdout.write(self.style.SUCCESS('🎯 Próximos passos:'))
        self.stdout.write('1. Configure a chave PIX de email no Mercado Pago')
        self.stdout.write('2. Teste a URL do checkout fornecida')
        self.stdout.write('3. Se PIX não aparecer, verifique as configurações da conta')
        self.stdout.write('4. Considere migrar para ambiente de produção')
        
        self.stdout.write(self.style.SUCCESS('🏁 Configuração concluída!'))
