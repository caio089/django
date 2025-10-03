#!/usr/bin/env python
"""
Script para verificar se o deploy está funcionando corretamente
Execute este script para diagnosticar problemas de deploy
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.conf import settings
from payments.models import ConfiguracaoPagamento
from django.contrib.auth.models import User

print("🔍 VERIFICAÇÃO DE DEPLOY")
print("=" * 50)

# 1. Verificar configurações do Django
print("1. CONFIGURAÇÕES DO DJANGO:")
print(f"   DEBUG: {settings.DEBUG}")
print(f"   TIME_ZONE: {settings.TIME_ZONE}")
print(f"   LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
print(f"   LOGIN_REDIRECT_URL: {getattr(settings, 'LOGIN_REDIRECT_URL', 'NÃO DEFINIDO')}")
print(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'NÃO DEFINIDO')}")

# 2. Verificar banco de dados
print("\n2. BANCO DE DADOS:")
print(f"   ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"   NAME: {settings.DATABASES['default']['NAME']}")
print(f"   HOST: {settings.DATABASES['default']['HOST']}")

# 3. Verificar configurações do Mercado Pago
print("\n3. CONFIGURAÇÕES DO MERCADO PAGO:")
configs = ConfiguracaoPagamento.objects.all()
if configs:
    for config in configs:
        print(f"   ID: {config.id}")
        print(f"   Ambiente: {config.ambiente}")
        print(f"   Ativo: {config.ativo}")
        access_token = config.get_access_token()
        if access_token:
            print(f"   Token: {access_token[:20]}...")
            if access_token.startswith('TEST-'):
                print("   ✓ Token SANDBOX")
            elif access_token.startswith('APP-'):
                print("   ✓ Token PRODUÇÃO")
        print("   ---")
else:
    print("   ❌ Nenhuma configuração encontrada!")

# 4. Verificar usuários
print("\n4. USUÁRIOS:")
users = User.objects.all()
if users:
    print(f"   Total de usuários: {users.count()}")
    for user in users:
        print(f"   - {user.email} (Ativo: {user.is_active})")
else:
    print("   ❌ Nenhum usuário encontrado!")

# 5. Verificar variáveis de ambiente
print("\n5. VARIÁVEIS DE AMBIENTE:")
env_vars = [
    'DEBUG', 'SECRET_KEY', 'DB_HOST', 'DB_NAME', 'DB_USER', 
    'MERCADOPAGO_ACCESS_TOKEN', 'MERCADOPAGO_PUBLIC_KEY'
]

for var in env_vars:
    value = os.getenv(var, 'NÃO DEFINIDA')
    if var == 'SECRET_KEY' and value != 'NÃO DEFINIDA':
        value = value[:20] + '...'
    print(f"   {var}: {value}")

print("\n" + "=" * 50)
print("✅ Verificação concluída!")
print("\nSe você está vendo 'DEBUG: True' e 'USE_SQLITE_FALLBACK: True',")
print("isso significa que o Render não está usando as variáveis de ambiente corretas.")
print("\nConfigure as variáveis de ambiente no painel do Render:")
print("- DEBUG = False")
print("- USE_SQLITE_FALLBACK = False")
print("- Todas as outras variáveis do arquivo .env")
