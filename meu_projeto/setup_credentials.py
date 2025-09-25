#!/usr/bin/env python
"""
Script para configurar credenciais do Supabase e Mercado Pago
"""

import os
import sys
import django
from pathlib import Path

# Adiciona o diretório do projeto ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from payments.models import ConfiguracaoPagamento

def setup_supabase():
    """Configura credenciais do Supabase"""
    print("🔧 Configuração do Supabase")
    print("=" * 40)
    
    print("📋 Insira suas credenciais do Supabase:")
    print("   (Encontre em: supabase.com → Projeto → Settings → Database)")
    print()
    
    db_host = input("🌍 Host (ex: xyz.supabase.co): ").strip()
    db_port = input("🔌 Porta (padrão: 5432): ").strip() or "5432"
    db_name = input("🗄️ Nome do banco (padrão: postgres): ").strip() or "postgres"
    db_user = input("👤 Usuário (padrão: postgres): ").strip() or "postgres"
    db_password = input("🔑 Senha: ").strip()
    
    # Criar arquivo .env
    env_content = f"""# Configurações do Supabase
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}

# Configurações do Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=TEST-your-access-token-here
MERCADOPAGO_PUBLIC_KEY=TEST-your-public-key-here

# Configurações gerais
SITE_URL=https://your-domain.com
SECRET_KEY=your-django-secret-key-here
DEBUG=True
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado com credenciais do Supabase!")
    print("📝 Configure as credenciais do Mercado Pago no arquivo .env")
    
    return True

def setup_mercadopago():
    """Configura credenciais do Mercado Pago"""
    print("\n🔧 Configuração do Mercado Pago")
    print("=" * 40)
    
    print("📋 Insira suas credenciais do Mercado Pago:")
    print("   (Encontre em: mercadopago.com.br → Desenvolvedores → Suas integrações)")
    print()
    
    access_token = input("🔑 Access Token: ").strip()
    public_key = input("🔑 Public Key: ").strip()
    dominio = input("🌍 Domínio (ex: https://meusite.com): ").strip()
    
    if not dominio.startswith('http'):
        dominio = f"https://{dominio}"
    
    webhook_url = f"{dominio}/payments/webhook/"
    
    try:
        # Verificar se já existe configuração
        config = ConfiguracaoPagamento.objects.filter(ativo=True).first()
        
        if config:
            config.access_token = access_token
            config.public_key = public_key
            config.webhook_url = webhook_url
            config.save()
            print("✅ Configuração do Mercado Pago atualizada!")
        else:
            ConfiguracaoPagamento.objects.create(
                access_token=access_token,
                public_key=public_key,
                webhook_url=webhook_url,
                ambiente='sandbox',
                ativo=True
            )
            print("✅ Configuração do Mercado Pago criada!")
        
        print(f"\n🔗 Webhook URL: {webhook_url}")
        print("📝 Configure esta URL no painel do Mercado Pago")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configuração de Credenciais")
    print("=" * 50)
    
    print("Escolha o que configurar:")
    print("1. Supabase (banco de dados)")
    print("2. Mercado Pago (pagamentos)")
    print("3. Ambos")
    
    opcao = input("\nDigite sua opção (1, 2 ou 3): ").strip()
    
    success = True
    
    if opcao in ['1', '3']:
        success &= setup_supabase()
    
    if opcao in ['2', '3']:
        success &= setup_mercadopago()
    
    if success:
        print("\n🎉 Configuração concluída!")
        print("\n📋 Próximos passos:")
        print("1. Reinicie o servidor: python manage.py runserver")
        print("2. Acesse: http://localhost:8000/payments/planos/")
        print("3. Teste os pagamentos!")
    else:
        print("\n⚠️ Alguns erros ocorreram. Verifique as configurações.")

if __name__ == '__main__':
    main()
