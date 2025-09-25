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
    """Configura credenciais essenciais do Supabase"""
    print("🔧 Configuração do Supabase - Informações Essenciais")
    print("=" * 50)
    
    print("📋 Insira apenas as informações essenciais do Supabase:")
    print("   (Encontre em: supabase.com → Projeto → Settings → Database)")
    print()
    
    # Apenas informações essenciais
    db_host = input("🌍 URL do Supabase (ex: xyz.supabase.co): ").strip()
    db_password = input("🔑 Senha do banco: ").strip()
    
    # Valores padrão para as outras configurações
    db_port = "5432"
    db_name = "postgres"
    db_user = "postgres"
    
    # Criar arquivo .env com configurações mínimas
    env_content = f"""# Configurações essenciais do Supabase
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USER={db_user}
DB_PASSWORD={db_password}

# Configurações do Mercado Pago (opcional)
MERCADOPAGO_ACCESS_TOKEN=TEST-your-access-token-here
MERCADOPAGO_PUBLIC_KEY=TEST-your-public-key-here

# Configurações gerais
DEBUG=True
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado com configurações essenciais!")
    print("📝 Configurações padrão aplicadas:")
    print(f"   - Host: {db_host}")
    print(f"   - Porta: {db_port}")
    print(f"   - Banco: {db_name}")
    print(f"   - Usuário: {db_user}")
    print("   - Senha: [configurada]")
    
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
    """Função principal - Configuração simplificada"""
    print("🚀 Configuração Simplificada do Supabase")
    print("=" * 50)
    
    print("Este script irá configurar apenas as informações essenciais:")
    print("✅ URL do Supabase")
    print("✅ Senha do banco")
    print("✅ Configurações padrão (porta, banco, usuário)")
    print()
    
    continuar = input("Deseja continuar? (s/n): ").strip().lower()
    
    if continuar in ['s', 'sim', 'y', 'yes']:
        success = setup_supabase()
        
        if success:
            print("\n🎉 Configuração concluída!")
            print("\n📋 Próximos passos:")
            print("1. Reinicie o servidor: python manage.py runserver")
            print("2. Acesse: http://localhost:8000/")
            print("3. Se houver erro, verifique se a URL e senha estão corretas")
        else:
            print("\n⚠️ Erro na configuração. Tente novamente.")
    else:
        print("❌ Configuração cancelada.")

if __name__ == '__main__':
    main()
