#!/usr/bin/env python
"""
Script para debugar problemas de pagamento no Render
Execute este script para identificar exatamente onde está o erro
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from payments.models import ConfiguracaoPagamento, PlanoPremium
from payments.views import get_mercadopago_config
import mercadopago
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("🔍 DEBUG DE PAGAMENTO")
print("=" * 50)

# 1. Verificar configuração do Mercado Pago
print("1. CONFIGURAÇÃO DO MERCADO PAGO:")
config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
if config:
    print(f"   ID: {config.id}")
    print(f"   Ambiente: {config.ambiente}")
    print(f"   Ativo: {config.ativo}")
    print(f"   Webhook URL: {config.webhook_url}")
    
    # Testar obtenção de tokens
    try:
        access_token = config.get_access_token()
        if access_token:
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   Token válido: {access_token.startswith(('TEST-', 'APP-'))}")
        else:
            print("   ❌ Access Token não obtido")
    except Exception as e:
        print(f"   ❌ Erro ao obter Access Token: {e}")
    
    try:
        public_key = config.get_public_key()
        if public_key:
            print(f"   Public Key: {public_key[:20]}...")
            print(f"   Key válida: {public_key.startswith(('TEST-', 'APP-'))}")
        else:
            print("   ❌ Public Key não obtida")
    except Exception as e:
        print(f"   ❌ Erro ao obter Public Key: {e}")
else:
    print("   ❌ Nenhuma configuração ativa encontrada!")

print()

# 2. Testar função get_mercadopago_config
print("2. TESTE DA FUNÇÃO get_mercadopago_config:")
try:
    sdk, config_obj = get_mercadopago_config()
    if sdk and config_obj:
        print("   ✅ SDK criado com sucesso")
        print(f"   ✅ Configuração: {config_obj.ambiente}")
    else:
        print("   ❌ Falha ao criar SDK")
except Exception as e:
    print(f"   ❌ Erro na função get_mercadopago_config: {e}")

print()

# 3. Testar criação de preferência diretamente
print("3. TESTE DE CRIAÇÃO DE PREFERÊNCIA:")
try:
    sdk, config_obj = get_mercadopago_config()
    if sdk:
        # Dados de teste
        preference_data = {
            "items": [
                {
                    "title": "Teste de Pagamento",
                    "description": "Teste de debug",
                    "quantity": 1,
                    "unit_price": 1.0,
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "email": "teste@exemplo.com",
                "identification": {
                    "type": "CPF",
                    "number": "12345678901"
                }
            },
            "back_urls": {
                "success": "https://dojo-on.onrender.com/payments/sucesso/",
                "failure": "https://dojo-on.onrender.com/payments/falha/",
                "pending": "https://dojo-on.onrender.com/payments/pendente/"
            },
            "external_reference": "teste_debug_123",
            "notification_url": config_obj.webhook_url,
            "payment_methods": {
                "excluded_payment_methods": [],
                "excluded_payment_types": [],
                "installments": 12
            },
            "auto_return": "approved",
            "binary_mode": False,
            "statement_descriptor": "DOJO-ON",
            "metadata": {
                "teste": "debug"
            }
        }
        
        print("   Criando preferência de teste...")
        print(f"   Dados: {preference_data}")
        
        preference = sdk.preference().create(preference_data)
        print(f"   Resposta: {preference}")
        
        if preference["status"] == 201:
            print("   ✅ Preferência criada com sucesso!")
            print(f"   ID: {preference['response']['id']}")
        else:
            print(f"   ❌ Erro ao criar preferência: {preference}")
    else:
        print("   ❌ SDK não disponível")
except Exception as e:
    print(f"   ❌ Erro ao testar criação de preferência: {e}")
    import traceback
    print(f"   Traceback: {traceback.format_exc()}")

print()

# 4. Verificar planos disponíveis
print("4. PLANOS DISPONÍVEIS:")
planos = PlanoPremium.objects.filter(ativo=True)
if planos:
    for plano in planos:
        print(f"   - {plano.nome}: R$ {plano.preco} (ID: {plano.id})")
else:
    print("   ❌ Nenhum plano ativo encontrado!")

print()

# 5. Verificar variáveis de ambiente
print("5. VARIÁVEIS DE AMBIENTE:")
env_vars = [
    'DEBUG', 'MERCADOPAGO_ACCESS_TOKEN', 'MERCADOPAGO_PUBLIC_KEY',
    'MERCADOPAGO_WEBHOOK_URL', 'DATABASE_URL'
]

for var in env_vars:
    value = os.getenv(var, 'NÃO DEFINIDA')
    if 'TOKEN' in var or 'KEY' in var:
        value = value[:20] + '...' if len(value) > 20 else value
    print(f"   {var}: {value}")

print("\n" + "=" * 50)
print("✅ Debug concluído!")
print("\nSe você vê erros aqui, eles indicam exatamente onde está o problema.")
