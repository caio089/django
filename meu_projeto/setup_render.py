#!/usr/bin/env python
"""
Script para configurar o projeto após deploy no Render
Execute este script após o primeiro deploy para configurar dados iniciais
"""

import os
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

def setup_initial_data():
    """Configurar dados iniciais do sistema"""
    from django.contrib.auth.models import User
    from payments.models import PlanoPremium, ConfiguracaoPagamento
    
    print("🚀 Configurando dados iniciais...")
    
    # 1. Criar superusuário se não existir
    if not User.objects.filter(is_superuser=True).exists():
        print("📝 Criando superusuário...")
        User.objects.create_superuser(
            username='admin',
            email='admin@dojo.com',
            password='admin123'
        )
        print("✅ Superusuário criado: admin/admin123")
    else:
        print("ℹ️ Superusuário já existe")
    
    # 2. Criar plano premium se não existir
    if not PlanoPremium.objects.exists():
        print("💎 Criando plano premium...")
        PlanoPremium.objects.create(
            nome="Plano Premium",
            descricao="Acesso completo a todas as funcionalidades",
            preco=29.90,
            ativo=True
        )
        print("✅ Plano premium criado")
    else:
        print("ℹ️ Plano premium já existe")
    
    # 3. Configurar Mercado Pago
    print("💳 Configurando Mercado Pago...")
    from django.core.management import call_command
    try:
        call_command('configurar_render')
        print("✅ Configuração de pagamento concluída")
    except Exception as e:
        print(f"❌ Erro ao configurar pagamento: {e}")
    
    print("🎉 Configuração inicial concluída!")

if __name__ == '__main__':
    setup_initial_data()





