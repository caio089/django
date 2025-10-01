from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import PlanoPremium, ConfiguracaoPagamento
from payments.views import criar_pagamento
from django.test import RequestFactory
import json
import mercadopago

class Command(BaseCommand):
    help = 'Testa especificamente se PIX aparece no checkout do Mercado Pago'

    def add_arguments(self, parser):
        parser.add_argument('--plano-id', type=int, help='ID do plano para testar')
        parser.add_argument('--usuario-id', type=int, help='ID do usuário para testar')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🧪 Testando configuração PIX no checkout...'))
        
        # Verificar configuração do Mercado Pago
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        if not config:
            self.stdout.write(self.style.ERROR('❌ Nenhuma configuração ativa do Mercado Pago encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Configuração: {config.ambiente}'))
        
        # Buscar plano
        plano_id = options.get('plano_id')
        if not plano_id:
            plano = PlanoPremium.objects.filter(ativo=True).first()
        else:
            try:
                plano = PlanoPremium.objects.get(id=plano_id, ativo=True)
            except PlanoPremium.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Plano {plano_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Plano: {plano.nome} - R$ {plano.preco}'))
        
        # Buscar usuário
        usuario_id = options.get('usuario_id')
        if not usuario_id:
            usuario = User.objects.filter(is_active=True).first()
        else:
            try:
                usuario = User.objects.get(id=usuario_id, is_active=True)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Usuário {usuario_id} não encontrado'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Usuário: {usuario.username}'))
        
        # Testar criação de preferência diretamente
        try:
            sdk = mercadopago.SDK(config.get_access_token())
            
            # Dados da preferência com PIX habilitado
            preference_data = {
                "items": [
                    {
                        "title": plano.nome,
                        "description": plano.descricao,
                        "quantity": 1,
                        "unit_price": float(plano.preco),
                        "currency_id": "BRL"
                    }
                ],
                "payer": {
                    "email": "teste@exemplo.com",
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
            
            self.stdout.write(self.style.WARNING('🔄 Criando preferência de teste...'))
            self.stdout.write(f'Dados da preferência: {json.dumps(preference_data, indent=2)}')
            
            # Criar preferência
            preference_result = sdk.preference().create(preference_data)
            
            if preference_result["status"] == 201:
                preference = preference_result["response"]
                preference_id = preference["id"]
                init_point = preference.get("init_point")
                
                self.stdout.write(self.style.SUCCESS('✅ Preferência criada com sucesso!'))
                self.stdout.write(f'   ID: {preference_id}')
                self.stdout.write(f'   Init Point: {init_point}')
                
                # Analisar métodos de pagamento disponíveis
                payment_methods = preference.get("payment_methods", {})
                excluded_methods = payment_methods.get("excluded_payment_methods", [])
                excluded_types = payment_methods.get("excluded_payment_types", [])
                default_method = payment_methods.get("default_payment_method_id")
                
                self.stdout.write(self.style.SUCCESS('📋 Análise dos métodos de pagamento:'))
                self.stdout.write(f'   Métodos excluídos: {excluded_methods}')
                self.stdout.write(f'   Tipos excluídos: {excluded_types}')
                self.stdout.write(f'   Método padrão: {default_method}')
                
                # Verificar se PIX está disponível
                pix_available = "pix" not in [method.get("id") for method in excluded_types]
                self.stdout.write(f'   PIX disponível: {"✅ SIM" if pix_available else "❌ NÃO"}')
                
                if pix_available:
                    self.stdout.write(self.style.SUCCESS('🎉 PIX está habilitado na preferência!'))
                    self.stdout.write(f'🔗 Acesse o checkout: {init_point}')
                    self.stdout.write('📱 No checkout, procure pela opção PIX')
                else:
                    self.stdout.write(self.style.ERROR('❌ PIX não está disponível na preferência'))
                    self.stdout.write('💡 Possíveis causas:')
                    self.stdout.write('   - Conta do Mercado Pago não tem PIX habilitado')
                    self.stdout.write('   - Configuração da conta incompleta')
                    self.stdout.write('   - Ambiente sandbox pode ter limitações')
                
                # Mostrar informações da conta
                self.stdout.write(self.style.WARNING('🔍 Informações da conta:'))
                self.stdout.write(f'   Collector ID: {preference.get("collector_id")}')
                self.stdout.write(f'   Site ID: {preference.get("site_id")}')
                self.stdout.write(f'   Ambiente: {config.ambiente}')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar preferência: {preference_result}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante o teste: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        
        self.stdout.write(self.style.SUCCESS('🏁 Teste concluído!'))


