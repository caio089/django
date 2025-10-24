#!/usr/bin/env python
"""
Script para testar conexão com Supabase
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def testar_conexao_supabase():
    """Testa a conexão com o Supabase"""
    print("🔍 Testando conexão com Supabase...")
    
    try:
        # Testar conexão básica
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Conexão básica funcionando: {result}")
        
        # Testar informações do banco
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"📊 Versão do PostgreSQL: {version[0]}")
        
        # Testar informações da conexão
        db_config = connection.settings_dict
        print(f"🔗 Host: {db_config.get('HOST', 'N/A')}")
        print(f"🔗 Port: {db_config.get('PORT', 'N/A')}")
        print(f"🔗 Database: {db_config.get('NAME', 'N/A')}")
        print(f"🔗 User: {db_config.get('USER', 'N/A')}")
        
        print("✅ Conexão com Supabase funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        return False

def testar_migracoes():
    """Testa se as migrações funcionam"""
    print("\n🔄 Testando migrações...")
    
    try:
        # Executar check das migrações
        execute_from_command_line(['manage.py', 'check', '--database', 'default'])
        print("✅ Check das migrações passou!")
        
        # Executar migrate --dry-run
        execute_from_command_line(['manage.py', 'migrate', '--dry-run'])
        print("✅ Migrações podem ser executadas!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Iniciando testes do Supabase...")
    
    # Verificar variáveis de ambiente
    database_url = os.getenv('DATABASE_URL')
    db_host = os.getenv('DB_HOST')
    
    print(f"📋 DATABASE_URL: {'✅ Configurado' if database_url else '❌ Não configurado'}")
    print(f"📋 DB_HOST: {'✅ Configurado' if db_host else '❌ Não configurado'}")
    
    if not database_url and not db_host:
        print("❌ Nenhuma configuração de banco encontrada!")
        sys.exit(1)
    
    # Testar conexão
    conexao_ok = testar_conexao_supabase()
    
    if conexao_ok:
        # Testar migrações
        migracoes_ok = testar_migracoes()
        
        if migracoes_ok:
            print("\n🎉 Todos os testes passaram! Supabase está funcionando!")
        else:
            print("\n⚠️ Conexão OK, mas há problemas com migrações")
    else:
        print("\n❌ Problemas de conexão com Supabase")
        sys.exit(1)
